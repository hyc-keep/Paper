"""Run the formal workflow gates in a fixed, non-skippable order."""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
import re


CODE_OBJECT_PREFIXES = (
    "src/",
    "scripts/",
    "tools/",
    "b_class_auxiliary/tools/",
    "configs/",
    "external/",
)
CODE_OBJECT_SUFFIXES = (".py", ".yaml", ".yml", ".json", ".toml")
REQUIRED_ALWAYS_ARTIFACTS = (
    "研究定标记录.md",
    "research_alignment_gate_report.md",
    "00_阶段实现卡.md",
    "stage_definition_gate_report.md",
    "precheck_doc_gate_report.md",
    "workflow_gate_report.md",
)
REQUIRED_CODE_ARTIFACTS = (
    "实现依据记录.md",
    "runtime_check_report.md",
    "runtime_evidence.json",
    "runtime_check.log",
    "code_quality_gate_report.md",
)


@dataclass
class StepResult:
    name: str
    status: str
    command: list[str]
    output_path: str | None
    reason: str
    stdout: str
    stderr: str
    return_code: int | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enforce research -> stage-card -> precheck -> runtime -> code-quality -> workflow gates."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--research-record",
        default="",
        help="Optional relative path to `研究定标记录.md`.",
    )
    parser.add_argument(
        "--stage-card",
        required=True,
        help="Relative path to `00_阶段实现卡.md`.",
    )
    parser.add_argument(
        "--precheck-guard",
        default="",
        help="Relative path to the task Pre-check Guard markdown file.",
    )
    parser.add_argument(
        "--post-qc-guard",
        default="",
        help="Relative path to the task Post-QC Guard markdown file.",
    )
    parser.add_argument(
        "--experiment-config",
        default="",
        help="Relative path to the experiment YAML file for runtime/code-quality checks.",
    )
    parser.add_argument(
        "--runtime-split",
        default="train",
        choices=("train", "val", "testA", "testB", "test"),
        help="Split passed to `run_minimal_runtime_check.py`.",
    )
    parser.add_argument(
        "--runtime-sample-index",
        type=int,
        default=0,
        help="Sample index passed to `run_minimal_runtime_check.py`.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional relative path for the generated workflow gate report.",
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_path(project_root: Path, raw_path: str) -> Path:
    return (project_root / normalize_relpath(raw_path)).resolve()


def default_output_dir(project_root: Path, args: argparse.Namespace) -> Path:
    for raw_path in (args.post_qc_guard, args.precheck_guard, args.stage_card):
        if raw_path:
            return resolve_path(project_root, raw_path).parent
    return project_root / "b_class_auxiliary" / "workflow_gates"


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def extract_current_stage_name(text: str) -> str:
    match = re.search(r"(?m)^- 当前阶段:\s*`([^`\n]+)`\s*$", text)
    return normalize_relpath(match.group(1)) if match else ""


def expected_stage_archive_path(project_root: Path, stage_name: str) -> Path | None:
    normalized = normalize_relpath(stage_name)
    if not normalized:
        return None
    return (project_root / "reports" / "stage_reports" / "implementation_tracking" / normalized / "实现依据记录.md").resolve()


def extract_table_rows(markdown_text: str, heading: str) -> list[dict[str, str]]:
    lines = markdown_text.splitlines()
    start_index = -1
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start_index = index + 1
            break
    if start_index == -1:
        raise ValueError(f"Missing heading: {heading}")

    while start_index < len(lines) and not lines[start_index].strip():
        start_index += 1

    table_lines: list[str] = []
    while start_index < len(lines):
        current = lines[start_index].rstrip()
        if not current.startswith("|"):
            break
        table_lines.append(current)
        start_index += 1

    if len(table_lines) < 2:
        raise ValueError(f"Missing markdown table under heading: {heading}")

    headers = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            raise ValueError(f"Malformed table row under heading {heading}: {line}")
        rows.append(dict(zip(headers, cells)))
    return rows


def post_qc_has_code_targets(post_qc_path: Path) -> bool:
    text = read_text(post_qc_path)
    rows = extract_table_rows(text, "## 2. 实际创建/修改文件")
    for row in rows:
        file_path = normalize_relpath(row.get("文件", ""))
        action = normalize_relpath(row.get("动作", ""))
        if not file_path or action == "not_applicable":
            continue
        if file_path.startswith(CODE_OBJECT_PREFIXES) and file_path.endswith(CODE_OBJECT_SUFFIXES):
            return True
    return False


def parse_status(stdout: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}=([A-Za-z_]+)\s*$", stdout)
    return match.group(1) if match else "fail"


def run_step(
    project_root: Path,
    name: str,
    command: list[str],
    status_key: str,
    output_path: Path | None,
) -> StepResult:
    completed = subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    status = parse_status(completed.stdout, status_key)
    reason = "completed"
    if completed.returncode != 0 and status == "pass":
        status = "fail"
        reason = f"nonzero_return_code:{completed.returncode}"
    elif completed.returncode != 0:
        reason = f"nonzero_return_code:{completed.returncode}"
    return StepResult(
        name=name,
        status=status,
        command=command,
        output_path=output_path.as_posix() if output_path else None,
        reason=reason,
        stdout=completed.stdout,
        stderr=completed.stderr,
        return_code=completed.returncode,
    )


def blocked_step(name: str, reason: str, output_path: Path | None = None) -> StepResult:
    return StepResult(
        name=name,
        status="blocked",
        command=[],
        output_path=output_path.as_posix() if output_path else None,
        reason=reason,
        stdout="",
        stderr="",
        return_code=None,
    )


def build_required_artifact_paths(
    output_dir: Path,
    has_code_targets: bool,
) -> list[Path]:
    artifact_paths = [output_dir / name for name in REQUIRED_ALWAYS_ARTIFACTS[3:]]
    if has_code_targets:
        artifact_paths.extend(output_dir / name for name in REQUIRED_CODE_ARTIFACTS)
    return artifact_paths


def collect_missing_artifacts(
    project_root: Path,
    research_record_path: Path,
    research_gate_report_path: Path,
    stage_card_path: Path,
    output_dir: Path,
    has_code_targets: bool,
) -> list[str]:
    expected_paths = [research_record_path, research_gate_report_path, stage_card_path]
    expected_paths.extend(build_required_artifact_paths(output_dir, has_code_targets))
    if has_code_targets:
        stage_name = extract_current_stage_name(read_text(stage_card_path))
        archive_path = expected_stage_archive_path(project_root, stage_name)
        if archive_path is not None:
            expected_paths.append(archive_path)
    missing: list[str] = []
    for path in expected_paths:
        if not path.exists():
            missing.append(safe_relpath(path, project_root))
    return missing


def render_report(
    project_root: Path,
    research_record_path: Path,
    research_gate_report_path: Path,
    stage_card_path: Path,
    output_dir: Path,
    step_results: list[StepResult],
    final_status: str,
    has_code_targets: bool,
    missing_artifacts: list[str],
) -> str:
    required_artifacts = [
        safe_relpath(research_record_path, project_root),
        safe_relpath(research_gate_report_path, project_root),
        safe_relpath(stage_card_path, project_root),
    ]
    required_artifacts.extend(
        safe_relpath(path, project_root)
        for path in build_required_artifact_paths(output_dir, has_code_targets)
    )
    if has_code_targets:
        stage_name = extract_current_stage_name(read_text(stage_card_path))
        archive_path = expected_stage_archive_path(project_root, stage_name)
        if archive_path is not None:
            required_artifacts.append(safe_relpath(archive_path, project_root))
    lines = [
        "# Workflow Gate Report",
        "",
        "## 1. 固定执行顺序",
        "- `research_alignment_record` -> `stage_definition_gate` -> `precheck_doc_gate` -> `runtime_check` -> `code_quality_gate` -> `workflow_gate`",
        "",
        "## 2. 本轮正式产物要求",
    ]
    for item in required_artifacts:
        lines.append(f"- required_artifact: `{item}`")
    if missing_artifacts:
        lines.append(f"- missing_artifacts: `{ '`, `'.join(missing_artifacts) }`")
    else:
        lines.append("- missing_artifacts: `none`")
    lines.extend(
        [
            "",
            "## 3. 各步结果",
        ]
    )
    for item in step_results:
        lines.extend(
            [
                f"### {item.name}",
                f"- status: `{item.status}`",
                f"- reason: `{item.reason}`",
                f"- output_path: `{item.output_path}`",
                f"- return_code: `{item.return_code}`",
                f"- command: `{ ' '.join(item.command) if item.command else 'blocked' }`",
                "",
            ]
        )
    lines.extend(
        [
            "## 4. 结论",
            f"- workflow_gate_status: `{final_status}`",
            "- 规则: 任一步不是 `pass`，后续依赖步骤一律 `blocked`，不允许跳步放行。",
            "- 规则: 缺少任何本轮必需正式产物，也不允许宣称“正式任务已通过”。",
            "- 说明: `learning_doc_gate` 与 `formal_doc_gate` 属于后续 `说明文档` 或治理阶段检查，不属于当前 `workflow_gate_report.md` 的前置条件。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report_and_exit(
    project_root: Path,
    workflow_report_path: Path,
    research_record_path: Path,
    research_gate_report_path: Path,
    stage_card_path: Path,
    output_dir: Path,
    step_results: list[StepResult],
    final_status: str,
    has_code_targets: bool,
    exit_code: int,
) -> int:
    missing_artifacts = collect_missing_artifacts(
        project_root,
        research_record_path,
        research_gate_report_path,
        stage_card_path,
        output_dir,
        has_code_targets,
    )
    workflow_rel = safe_relpath(workflow_report_path, project_root)
    missing_artifacts = [item for item in missing_artifacts if item != workflow_rel]
    effective_status = final_status if not missing_artifacts and final_status == "pass" else "blocked"
    workflow_report_path.write_text(
        render_report(
            project_root,
            research_record_path,
            research_gate_report_path,
            stage_card_path,
            output_dir,
            step_results,
            effective_status,
            has_code_targets,
            missing_artifacts,
        ),
        encoding="utf-8",
    )
    print(f"workflow_gate_status={effective_status}")
    print(f"report_path={workflow_report_path.as_posix()}")
    return 0 if effective_status == "pass" else exit_code


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    stage_card_path = resolve_path(project_root, args.stage_card)
    if not stage_card_path.exists():
        raise SystemExit(f"Stage card does not exist: {stage_card_path}")
    if stage_card_path.name != "00_阶段实现卡.md":
        raise SystemExit(
            "Stage card filename must be exactly `00_阶段实现卡.md`, "
            f"got: {stage_card_path.name}"
        )

    output_dir = default_output_dir(project_root, args)
    output_dir.mkdir(parents=True, exist_ok=True)
    research_record_path = (
        resolve_path(project_root, args.research_record)
        if args.research_record
        else output_dir / "研究定标记录.md"
    )
    research_gate_output = output_dir / "research_alignment_gate_report.md"
    workflow_report_path = (
        resolve_path(project_root, args.output)
        if args.output
        else output_dir / "workflow_gate_report.md"
    )

    step_results: list[StepResult] = []
    python = sys.executable

    if not research_record_path.exists():
        research_result = blocked_step("research_alignment_gate", "missing_research_record", research_gate_output)
    else:
        research_command = [
            python,
            str(project_root / "b_class_auxiliary" / "tools" / "check_research_alignment_gate.py"),
            "--project-root",
            project_root.as_posix(),
            "--research-record",
            safe_relpath(research_record_path, project_root),
            "--output",
            research_gate_output.relative_to(project_root).as_posix(),
        ]
        research_result = run_step(
            project_root,
            "research_alignment_gate",
            research_command,
            "research_alignment_gate_status",
            research_gate_output,
        )
    step_results.append(research_result)

    if research_result.status != "pass":
        step_results.extend(
            [
                blocked_step("stage_definition_gate", "blocked_by_research_alignment_gate"),
                blocked_step("precheck_doc_gate", "blocked_by_research_alignment_gate"),
                blocked_step("runtime_check", "blocked_by_research_alignment_gate"),
                blocked_step("code_quality_gate", "blocked_by_research_alignment_gate"),
            ]
        )
        return write_report_and_exit(
            project_root,
            workflow_report_path,
            research_record_path,
            research_gate_output,
            stage_card_path,
            output_dir,
            step_results,
            "blocked",
            False,
            1,
        )

    stage_output = output_dir / "stage_definition_gate_report.md"
    stage_command = [
        python,
        str(project_root / "b_class_auxiliary" / "tools" / "check_stage_definition_gate.py"),
        "--project-root",
        project_root.as_posix(),
        "--stage-card",
        normalize_relpath(args.stage_card),
        "--output",
        stage_output.relative_to(project_root).as_posix(),
    ]
    stage_result = run_step(
        project_root,
        "stage_definition_gate",
        stage_command,
        "stage_definition_gate_status",
        stage_output,
    )
    step_results.append(stage_result)

    if stage_result.status != "pass":
        step_results.extend(
            [
                blocked_step("precheck_doc_gate", "blocked_by_stage_definition_gate"),
                blocked_step("runtime_check", "blocked_by_stage_definition_gate"),
                blocked_step("code_quality_gate", "blocked_by_stage_definition_gate"),
            ]
        )
        return write_report_and_exit(
            project_root,
            workflow_report_path,
            research_record_path,
            research_gate_output,
            stage_card_path,
            output_dir,
            step_results,
            "blocked",
            False,
            1,
        )

    precheck_path = resolve_path(project_root, args.precheck_guard) if args.precheck_guard else None
    if precheck_path is None or not precheck_path.exists():
        precheck_result = blocked_step("precheck_doc_gate", "missing_precheck_guard")
    else:
        precheck_output = output_dir / "precheck_doc_gate_report.md"
        precheck_command = [
            python,
            str(project_root / "b_class_auxiliary" / "tools" / "check_precheck_docs.py"),
            "--project-root",
            project_root.as_posix(),
            "--precheck-guard",
            normalize_relpath(args.precheck_guard),
            "--output",
            precheck_output.relative_to(project_root).as_posix(),
        ]
        precheck_result = run_step(
            project_root,
            "precheck_doc_gate",
            precheck_command,
            "precheck_doc_gate_status",
            precheck_output,
        )
    step_results.append(precheck_result)

    if precheck_result.status != "pass":
        step_results.extend(
            [
                blocked_step("runtime_check", "blocked_by_precheck_doc_gate"),
                blocked_step("code_quality_gate", "blocked_by_precheck_doc_gate"),
            ]
        )
        return write_report_and_exit(
            project_root,
            workflow_report_path,
            research_record_path,
            research_gate_output,
            stage_card_path,
            output_dir,
            step_results,
            "blocked",
            False,
            1,
        )

    post_qc_path = resolve_path(project_root, args.post_qc_guard) if args.post_qc_guard else None
    has_code_targets = False
    if post_qc_path and post_qc_path.exists():
        has_code_targets = post_qc_has_code_targets(post_qc_path)

    if has_code_targets:
        if not args.experiment_config:
            runtime_result = blocked_step("runtime_check", "missing_experiment_config")
            code_quality_result = blocked_step("code_quality_gate", "blocked_by_runtime_check")
            step_results.extend([runtime_result, code_quality_result])
            step_results.extend(
                [
                ]
            )
            return write_report_and_exit(
                project_root,
                workflow_report_path,
                research_record_path,
                research_gate_output,
                stage_card_path,
                output_dir,
                step_results,
                "blocked",
                True,
                1,
            )

        runtime_output = output_dir / "runtime_check_report.md"
        runtime_command = [
            python,
            str(project_root / "b_class_auxiliary" / "tools" / "run_minimal_runtime_check.py"),
            "--project-root",
            project_root.as_posix(),
            "--experiment-config",
            normalize_relpath(args.experiment_config),
            "--split",
            args.runtime_split,
            "--sample-index",
            str(args.runtime_sample_index),
            "--output",
            runtime_output.relative_to(project_root).as_posix(),
            "--evidence-output",
            (output_dir / "runtime_evidence.json").relative_to(project_root).as_posix(),
            "--log-output",
            (output_dir / "runtime_check.log").relative_to(project_root).as_posix(),
            "--train-runtime-output",
            (output_dir / "train_runtime_payload.json").relative_to(project_root).as_posix(),
        ]
        runtime_result = run_step(
            project_root,
            "runtime_check",
            runtime_command,
            "runtime_check_status",
            runtime_output,
        )
        step_results.append(runtime_result)
        if runtime_result.status != "pass":
            step_results.extend(
                [
                    blocked_step("code_quality_gate", "blocked_by_runtime_check"),
                ]
            )
            return write_report_and_exit(
                project_root,
                workflow_report_path,
                research_record_path,
                research_gate_output,
                stage_card_path,
                output_dir,
                step_results,
                "blocked",
                True,
                1,
            )

        code_quality_output = output_dir / "code_quality_gate_report.md"
        code_quality_command = [
            python,
            str(project_root / "b_class_auxiliary" / "tools" / "check_code_quality_gate.py"),
            "--project-root",
            project_root.as_posix(),
            "--post-qc-guard",
            normalize_relpath(args.post_qc_guard),
            "--output",
            code_quality_output.relative_to(project_root).as_posix(),
        ]
        code_quality_result = run_step(
            project_root,
            "code_quality_gate",
            code_quality_command,
            "code_quality_gate_status",
            code_quality_output,
        )
        step_results.append(code_quality_result)
        if code_quality_result.status != "pass":
            step_results.extend(
                [
                ]
            )
            return write_report_and_exit(
                project_root,
                workflow_report_path,
                research_record_path,
                research_gate_output,
                stage_card_path,
                output_dir,
                step_results,
                "blocked",
                True,
                1,
            )
    else:
        step_results.append(blocked_step("runtime_check", "not_required_for_non_code_task"))
        step_results.append(blocked_step("code_quality_gate", "not_required_for_non_code_task"))

    final_status = "pass"
    return write_report_and_exit(
        project_root,
        workflow_report_path,
        research_record_path,
        research_gate_output,
        stage_card_path,
        output_dir,
        step_results,
        final_status,
        has_code_targets,
        1,
    )


if __name__ == "__main__":
    raise SystemExit(main())
