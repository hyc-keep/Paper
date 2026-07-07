"""Validate code-quality evidence against real runtime evidence files."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any


VALID_STATUS = {"pass", "partial", "fail", "not_applicable"}
CODE_OBJECT_PREFIXES = (
    "src/",
    "scripts/",
    "tools/",
    "b_class_auxiliary/tools/",
    "configs/",
    "external/",
)
CODE_OBJECT_SUFFIXES = (".py", ".yaml", ".yml", ".json", ".toml")
RUNTIME_DIAGNOSTICS_KEYS = (
    "smoke_run_pass",
    "dataloader_batch_check_pass",
    "tensor_shape_dtype_pass",
    "loss_finite_pass",
    "grad_step_pass",
)
PREFLIGHT_NOT_APPLICABLE_RUNTIME_KEYS = {"loss_finite_pass", "grad_step_pass"}
IMPLEMENTATION_RECORD_REQUIRED_HEADINGS = (
    "## 4. 本轮直接依赖的已读文件",
    "## 5. 正式文件到依据的回链",
    "## 6. 参数与规则冻结回填",
)
POST_QC_ROW_TO_RUNTIME_KEY = {
    "最小 smoke run": "smoke_run_pass",
    "dataloader batch 检查": "dataloader_batch_check_pass",
    "tensor shape / dtype 检查": "tensor_shape_dtype_pass",
    "loss finite 检查": "loss_finite_pass",
    "backward / optimizer.step 检查": "grad_step_pass",
}
PLACEHOLDER_PATTERN = re.compile(
    r"^\[(?:文件|路径|结果|说明|对象|动作|证据|原因).*\]$|^xxx.*$|^xx_.*$|^\.\.\.$",
    re.IGNORECASE,
)


@dataclass
class Issue:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate code-quality gate evidence.")
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--post-qc-guard",
        required=True,
        help="Relative path to the task Post-QC Guard markdown file.",
    )
    parser.add_argument(
        "--output",
        default="",
        help=(
            "Optional relative path for the generated report. "
            "Defaults to the Post-QC guard directory + code_quality_gate_report.md."
        ),
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def infer_runtime_profile(stage_code: str, model_code: str) -> str:
    normalized_stage_code = normalize_relpath(stage_code).lower()
    normalized_model_code = normalize_relpath(model_code).lower()
    if (
        normalized_stage_code == "01_data_protocol_preflight"
        or normalized_model_code == "train_entrypoint_preflight_only"
    ):
        return "data_protocol_preflight"
    return "full_training_runtime"


def infer_runtime_profile_from_runtime_report(runtime_report_text: str) -> str:
    explicit = normalize_relpath(
        extract_field_value(extract_level2_section(runtime_report_text, "## 1. Inputs"), "- runtime_profile:")
    )
    if explicit in {"data_protocol_preflight", "full_training_runtime"}:
        return explicit
    stage_code = extract_field_value(extract_level2_section(runtime_report_text, "## 1. Inputs"), "- stage_code:")
    model_code = extract_field_value(extract_level2_section(runtime_report_text, "## 1. Inputs"), "- model_code:")
    return infer_runtime_profile(stage_code, model_code)


def infer_runtime_profile_from_runtime_evidence(runtime_evidence: dict[str, Any]) -> str:
    explicit = normalize_relpath(str(runtime_evidence.get("runtime_profile", "")))
    if explicit in {"data_protocol_preflight", "full_training_runtime"}:
        return explicit
    return infer_runtime_profile(
        str(runtime_evidence.get("stage_code", "")),
        str(runtime_evidence.get("model_code", "")),
    )


def runtime_key_allows_not_applicable(runtime_profile: str, key: str) -> bool:
    return runtime_profile == "data_protocol_preflight" and key in PREFLIGHT_NOT_APPLICABLE_RUNTIME_KEYS


def required_runtime_fields(runtime_profile: str) -> tuple[str, ...]:
    common_fields = (
        "sample_path",
        "sample_id",
        "input_shape",
        "input_dtype",
        "target_shape",
        "target_dtype",
        "target_unique_values",
    )
    if runtime_profile == "data_protocol_preflight":
        return common_fields
    return common_fields + (
        "output_shape",
        "output_dtype",
        "loss_value",
        "loss_is_finite",
        "backward_executed",
        "optimizer_step_executed",
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping JSON: {path}")
    return data


def is_placeholder_value(value: str) -> bool:
    normalized = normalize_relpath(value)
    if not normalized:
        return True
    return bool(PLACEHOLDER_PATTERN.match(normalized))


def has_substantive_value(value: str) -> bool:
    normalized = normalize_relpath(value)
    return bool(normalized) and not is_placeholder_value(normalized)


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


def extract_level2_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_field_value(section: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}\s*(.+)$", section)
    return match.group(1).strip() if match else ""


def resolve_anchor_path(project_root: Path, doc_path: Path, anchor: str) -> Path | None:
    normalized = normalize_relpath(anchor)
    if not normalized:
        return None
    workspace_root = project_root.parent
    candidate_path = Path(normalized)
    candidates = []
    if candidate_path.is_absolute():
        candidates.append(candidate_path)
    candidates.extend(
        (
            doc_path.parent / normalized,
            project_root / normalized,
            workspace_root / normalized,
        )
    )
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate.resolve()
    return None


def parse_simple_status_lines(text: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^-\s*([^:]+):\s*`?([A-Za-z_]+)`?", line)
        if match:
            results[match.group(1).strip()] = normalize_relpath(match.group(2))
    return results


def is_code_object(path_value: str) -> bool:
    normalized = normalize_relpath(path_value)
    return normalized.startswith(CODE_OBJECT_PREFIXES) and normalized.endswith(CODE_OBJECT_SUFFIXES)


def code_quality_review_required(post_qc_text: str) -> tuple[bool, list[str], list[Issue]]:
    issues: list[Issue] = []
    try:
        file_rows = extract_table_rows(post_qc_text, "## 2. 实际创建/修改文件")
    except ValueError:
        return False, [], [Issue("fail", "Post-QC Guard 缺少 `## 2. 实际创建/修改文件` 表格。")]

    code_paths: list[str] = []
    for row in file_rows:
        file_path = normalize_relpath(row.get("文件", ""))
        action = normalize_relpath(row.get("动作", ""))
        if not file_path or action == "not_applicable":
            continue
        if is_code_object(file_path):
            code_paths.append(file_path)
    return bool(code_paths), list(dict.fromkeys(code_paths)), issues


def analyze_diagnostics(
    diagnostics_path: Path | None,
    diagnostics_text: str,
    review_required: bool,
    runtime_profile: str,
) -> tuple[list[Issue], dict[str, str]]:
    issues: list[Issue] = []
    diagnostics_map = parse_simple_status_lines(diagnostics_text)

    if not diagnostics_path:
        issues.append(Issue("fail", "Post-QC Guard 没有回链到真实存在的 `diagnostics_result.txt`。"))
        return issues, diagnostics_map

    required_always = ("py_compile", "import_check", "stage_boundary_pass")
    required_when_code = RUNTIME_DIAGNOSTICS_KEYS + ("code_quality_gate_pass",)

    for key in required_always:
        status = diagnostics_map.get(key, "")
        if status not in VALID_STATUS:
            issues.append(Issue("fail", f"`diagnostics_result.txt` 缺少或写错 `{key}`。"))

    if review_required:
        for key in required_when_code:
            status = diagnostics_map.get(key, "")
            if status not in VALID_STATUS:
                issues.append(Issue("fail", f"`diagnostics_result.txt` 缺少或写错 `{key}`。"))
            elif status == "not_applicable" and not runtime_key_allows_not_applicable(runtime_profile, key):
                issues.append(Issue("fail", f"本轮存在正式代码改动，但 `{key}` 仍写成 `not_applicable`。"))

    return issues, diagnostics_map


def extract_runtime_report_path(project_root: Path, post_qc_guard: Path, post_qc_text: str) -> Path | None:
    backchain = extract_level2_section(post_qc_text, "## 5.1 关键回链")
    runtime_report_rel = normalize_relpath(
        extract_field_value(backchain, "- `runtime_check_report.md` 路径:")
    )
    if not runtime_report_rel:
        return None
    return resolve_anchor_path(project_root, post_qc_guard, runtime_report_rel)


def extract_runtime_evidence_path(
    project_root: Path,
    runtime_report_path: Path,
    runtime_report_text: str,
) -> Path | None:
    match = re.search(
        r"(?m)^- runtime_evidence_json:\s*`([^`\n]+)`\s*$",
        runtime_report_text,
    )
    if not match:
        return None
    return resolve_anchor_path(project_root, runtime_report_path, match.group(1))


def extract_implementation_record_path(
    project_root: Path,
    post_qc_guard: Path,
    post_qc_text: str,
) -> Path | None:
    backchain = extract_level2_section(post_qc_text, "## 5.1 关键回链")
    record_rel = normalize_relpath(extract_field_value(backchain, "- `实现依据记录.md` 路径:"))
    if record_rel:
        return resolve_anchor_path(project_root, post_qc_guard, record_rel)
    default_path = post_qc_guard.parent / "实现依据记录.md"
    return default_path.resolve() if default_path.exists() else None


def extract_current_stage_name(record_text: str) -> str:
    match = re.search(r"(?m)^- 当前阶段:\s*`([^`\n]+)`\s*$", record_text)
    return normalize_relpath(match.group(1)) if match else ""


def expected_stage_archive_path(project_root: Path, stage_name: str) -> Path | None:
    normalized = normalize_relpath(stage_name)
    if not normalized:
        return None
    return (project_root / "reports" / "stage_reports" / "implementation_tracking" / normalized / "实现依据记录.md").resolve()


def analyze_runtime_evidence(
    project_root: Path,
    post_qc_guard: Path,
    post_qc_text: str,
    diagnostics_map: dict[str, str],
    review_required: bool,
    runtime_profile_hint: str,
) -> tuple[list[Issue], dict[str, Any], dict[str, str], Path | None, str]:
    issues: list[Issue] = []
    runtime_status_map: dict[str, str] = {}
    runtime_evidence: dict[str, Any] = {}
    runtime_report_path = extract_runtime_report_path(project_root, post_qc_guard, post_qc_text)
    runtime_profile = runtime_profile_hint
    if not review_required:
        return issues, runtime_evidence, runtime_status_map, runtime_report_path, runtime_profile
    if runtime_report_path is None or not runtime_report_path.exists():
        issues.append(Issue("fail", "Post-QC Guard 没有回链到真实存在的 `runtime_check_report.md`。"))
        return issues, runtime_evidence, runtime_status_map, runtime_report_path, runtime_profile

    runtime_report_text = read_text(runtime_report_path)
    runtime_profile = infer_runtime_profile_from_runtime_report(runtime_report_text)
    runtime_status_map = parse_simple_status_lines(runtime_report_text)
    for key in ("runtime_check_status",) + RUNTIME_DIAGNOSTICS_KEYS:
        status = runtime_status_map.get(key, "")
        if status not in VALID_STATUS:
            issues.append(Issue("fail", f"`runtime_check_report.md` 缺少或写错 `{key}`。"))

    runtime_evidence_path = extract_runtime_evidence_path(
        project_root,
        runtime_report_path,
        runtime_report_text,
    )
    if runtime_evidence_path is None or not runtime_evidence_path.exists():
        issues.append(Issue("fail", "`runtime_check_report.md` 没有回链到真实存在的 `runtime_evidence.json`。"))
        return issues, runtime_evidence, runtime_status_map, runtime_report_path, runtime_profile

    try:
        runtime_evidence = read_json(runtime_evidence_path)
    except Exception as exc:  # pragma: no cover - local file dependent
        issues.append(Issue("fail", f"`runtime_evidence.json` 无法解析: `{exc}`。"))
        return issues, runtime_evidence, runtime_status_map, runtime_report_path, runtime_profile

    runtime_profile = infer_runtime_profile_from_runtime_evidence(runtime_evidence)

    checks = runtime_evidence.get("checks", {})
    runtime_fields = runtime_evidence.get("runtime_fields", {})
    execution = runtime_evidence.get("runtime_execution", {})
    if not isinstance(checks, dict):
        issues.append(Issue("fail", "`runtime_evidence.json` 缺少 `checks` 映射。"))
        checks = {}
    if not isinstance(runtime_fields, dict):
        issues.append(Issue("fail", "`runtime_evidence.json` 缺少 `runtime_fields` 映射。"))
        runtime_fields = {}
    if not isinstance(execution, dict):
        issues.append(Issue("fail", "`runtime_evidence.json` 缺少 `runtime_execution` 映射。"))
        execution = {}

    evidence_status = normalize_relpath(str(runtime_evidence.get("overall_status", "")))
    if evidence_status not in VALID_STATUS:
        issues.append(Issue("fail", "`runtime_evidence.json` 缺少合法的 `overall_status`。"))
    elif runtime_status_map.get("runtime_check_status") in VALID_STATUS and evidence_status != runtime_status_map.get("runtime_check_status"):
        issues.append(
            Issue(
                "fail",
                "`runtime_check_report.md` 与 `runtime_evidence.json` 的 `runtime_check_status` 不一致: "
                f"`{runtime_status_map.get('runtime_check_status')}` vs `{evidence_status}`。",
            )
        )

    for key in RUNTIME_DIAGNOSTICS_KEYS:
        check_status = normalize_relpath(str(checks.get(key, "")))
        report_status = runtime_status_map.get(key, "")
        diagnostics_status = diagnostics_map.get(key, "")
        if check_status not in VALID_STATUS:
            issues.append(Issue("fail", f"`runtime_evidence.json` 缺少合法的 `{key}`。"))
            continue
        if check_status == "not_applicable" and not runtime_key_allows_not_applicable(runtime_profile, key):
            issues.append(Issue("fail", f"`runtime_evidence.json` 不允许把 `{key}` 写成 `not_applicable`。"))
        if report_status in VALID_STATUS and report_status != check_status:
            issues.append(
                Issue(
                    "fail",
                    f"`runtime_check_report.md` 与 `runtime_evidence.json` 在 `{key}` 上不一致: `{report_status}` vs `{check_status}`。",
                )
            )
        if diagnostics_status in VALID_STATUS and diagnostics_status != check_status:
            issues.append(
                Issue(
                    "fail",
                    f"`diagnostics_result.txt` 与 `runtime_evidence.json` 在 `{key}` 上不一致: `{diagnostics_status}` vs `{check_status}`。",
                )
            )

    if normalize_relpath(str(execution.get("status", ""))) != "pass":
        issues.append(
            Issue(
                "partial",
                "正式 runtime subprocess 没有成功完成，因此代码质量门禁不能通过。"
                f" 当前状态: `{execution.get('status')}` / `{execution.get('reason')}`。",
            )
        )

    for field_name in required_runtime_fields(runtime_profile):
        if runtime_fields.get(field_name) in (None, "", []):
            issues.append(Issue("partial", f"`runtime_evidence.json` 缺少物理字段 `{field_name}`。"))

    if runtime_profile == "data_protocol_preflight":
        payload = execution.get("payload", {})
        if not isinstance(payload, dict) or payload.get("entrypoint_check_pass") is not True:
            issues.append(
                Issue(
                    "partial",
                    "`runtime_evidence.json` 没有证明 preflight 入口已通过 `entrypoint_check_pass == true`。",
                )
            )
    else:
        if runtime_fields.get("loss_is_finite") is not True:
            issues.append(Issue("partial", "`runtime_evidence.json` 没有证明 `loss_is_finite == true`。"))
        if runtime_fields.get("backward_executed") is not True:
            issues.append(Issue("partial", "`runtime_evidence.json` 没有证明 `backward_executed == true`。"))
        if runtime_fields.get("optimizer_step_executed") is not True:
            issues.append(Issue("partial", "`runtime_evidence.json` 没有证明 `optimizer_step_executed == true`。"))

    return issues, runtime_evidence, runtime_status_map, runtime_report_path, runtime_profile


def analyze_implementation_record(
    project_root: Path,
    post_qc_guard: Path,
    post_qc_text: str,
    review_required: bool,
    code_paths: list[str],
) -> list[Issue]:
    issues: list[Issue] = []
    if not review_required:
        return issues

    record_path = extract_implementation_record_path(project_root, post_qc_guard, post_qc_text)
    if record_path is None or not record_path.exists():
        issues.append(Issue("fail", "本轮存在正式代码/配置/正式资产改动,但缺少真实存在的 `实现依据记录.md`。"))
        return issues

    record_text = read_text(record_path)
    for heading in IMPLEMENTATION_RECORD_REQUIRED_HEADINGS:
        if heading not in record_text:
            issues.append(Issue("partial", f"`实现依据记录.md` 缺少关键章节 `{heading}`。"))

    for code_path in code_paths:
        if code_path not in record_text:
            issues.append(Issue("partial", f"`实现依据记录.md` 尚未回链本轮正式改动 `{code_path}`。"))

    if "结直肠腺体分割_plan_优化版/01_实验执行" not in record_text:
        issues.append(Issue("partial", "`实现依据记录.md` 没有回链到 `结直肠腺体分割_plan_优化版/01_实验执行`。"))
    if "结直肠腺体分割_正式参考资料" not in record_text and "03_文献证据" not in record_text:
        issues.append(Issue("partial", "`实现依据记录.md` 没有留下正式参考资料或文献证据回链。"))

    current_stage = extract_current_stage_name(record_text)
    if not current_stage:
        issues.append(Issue("partial", "`实现依据记录.md` 没有明确写出 `当前阶段`。"))
        return issues

    archive_path = expected_stage_archive_path(project_root, current_stage)
    if archive_path is None or not archive_path.exists():
        issues.append(
            Issue(
                "partial",
                f"当前阶段 `{current_stage}` 缺少独立归档 `reports/stage_reports/implementation_tracking/{current_stage}/实现依据记录.md`。",
            )
        )
        return issues

    normalized_record_path = record_path.as_posix().replace("\\", "/")
    if "/b_class_auxiliary/runtime_checks/" in normalized_record_path:
        if "当前文件角色" not in record_text or "当前阶段副本" not in record_text:
            issues.append(Issue("partial", "根路径 `实现依据记录.md` 缺少“当前阶段副本”角色声明。"))
        archive_rel = archive_path.relative_to(project_root).as_posix()
        if archive_rel not in record_text:
            issues.append(Issue("partial", f"根路径 `实现依据记录.md` 没有回链到当前阶段归档 `{archive_rel}`。"))

    return issues


def analyze_post_qc_table(
    post_qc_text: str,
    review_required: bool,
    runtime_checks: dict[str, Any],
    runtime_profile: str,
) -> list[Issue]:
    issues: list[Issue] = []
    try:
        protocol_rows = extract_table_rows(post_qc_text, "## 3. 协议级质检结果")
    except ValueError:
        return [Issue("fail", "Post-QC Guard 缺少 `## 3. 协议级质检结果` 表格。")]

    row_map = {normalize_relpath(row.get("检查项", "")): row for row in protocol_rows}
    if not review_required:
        return issues

    for row_name, runtime_key in POST_QC_ROW_TO_RUNTIME_KEY.items():
        row = row_map.get(row_name)
        if row is None:
            issues.append(Issue("fail", f"Post-QC Guard 缺少代码质量检查项 `{row_name}`。"))
            continue
        result = normalize_relpath(row.get("结果", ""))
        evidence = row.get("物理证据", "").strip()
        runtime_status = normalize_relpath(str(runtime_checks.get(runtime_key, "")))
        if result not in VALID_STATUS:
            issues.append(Issue("fail", f"代码质量检查项 `{row_name}` 的结果不在允许集合内。"))
        elif result == "not_applicable" and not runtime_key_allows_not_applicable(runtime_profile, runtime_key):
            issues.append(Issue("fail", f"本轮存在正式代码改动，但 `{row_name}` 仍写成 `not_applicable`。"))
        elif runtime_status in VALID_STATUS and result != runtime_status:
            issues.append(
                Issue(
                    "fail",
                    f"Post-QC Guard `{row_name}` 与 `runtime_evidence.json` 不一致: `{result}` vs `{runtime_status}`。",
                )
            )
        if not has_substantive_value(evidence):
            issues.append(Issue("fail", f"代码质量检查项 `{row_name}` 的物理证据仍是空壳或占位内容。"))

    gate_row = row_map.get("代码质量门禁")
    if gate_row is None:
        issues.append(Issue("fail", "Post-QC Guard 缺少 `代码质量门禁` 行。"))
    else:
        result = normalize_relpath(gate_row.get("结果", ""))
        evidence = gate_row.get("物理证据", "").strip()
        if result not in VALID_STATUS:
            issues.append(Issue("fail", "`代码质量门禁` 行的结果不在允许集合内。"))
        if not has_substantive_value(evidence):
            issues.append(Issue("fail", "`代码质量门禁` 行缺少真实物理证据。"))

    return issues


def analyze_consistency(
    post_qc_text: str,
    diagnostics_map: dict[str, str],
    review_required: bool,
    runtime_status_map: dict[str, str],
) -> list[Issue]:
    issues: list[Issue] = []
    if not review_required:
        return issues

    diagnostics_conclusion = extract_field_value(
        extract_level2_section(post_qc_text, "## 5. Diagnostics 结果"),
        "- 结论:",
    )
    final_status = extract_field_value(
        extract_level2_section(post_qc_text, "## 6. 最终状态"),
        "- Final Status:",
    )
    gate_status = diagnostics_map.get("code_quality_gate_pass", "")
    runtime_status = runtime_status_map.get("runtime_check_status", "")

    if gate_status in {"partial", "fail"} and final_status == "pass":
        issues.append(Issue("fail", "代码质量门禁仍是 `partial / fail`，但 Post-QC Guard 最终状态写成了 `pass`。"))
    if diagnostics_conclusion in {"partial", "fail"} and final_status == "pass":
        issues.append(Issue("fail", "Diagnostics 结果仍是 `partial / fail`，但 Post-QC Guard 最终状态写成了 `pass`。"))
    if runtime_status in {"partial", "fail"} and final_status == "pass":
        issues.append(Issue("fail", "runtime_check_status 仍是 `partial / fail`，但 Post-QC Guard 最终状态写成了 `pass`。"))

    return issues


def render_report(
    post_qc_guard: Path,
    review_required: bool,
    code_paths: list[str],
    issues: list[Issue],
    runtime_profile: str,
) -> tuple[str, str]:
    severity_rank = {"fail": 3, "partial": 2, "pass": 1}
    if any(issue.severity == "fail" for issue in issues):
        status = "fail"
    elif any(issue.severity == "partial" for issue in issues):
        status = "partial"
    else:
        status = "pass"

    issue_lines = issues or [Issue("pass", "未发现代码质量门禁异常。")]
    issue_lines = sorted(issue_lines, key=lambda item: severity_rank.get(item.severity, 0), reverse=True)

    lines = [
        "# Code Quality Gate Report",
        "",
        "## 1. 输入文档",
        f"- `{post_qc_guard.as_posix()}`",
        "",
        "## 2. 本轮是否触发代码质量门禁",
        f"- 触发结果: `{ 'yes' if review_required else 'no' }`",
        f"- runtime_profile: `{runtime_profile}`",
    ]
    if code_paths:
        lines.append(f"- 触发对象: `{ '`, `'.join(code_paths) }`")
    lines.extend(
        [
            "",
            "## 3. 检查范围",
            "- 检查 `diagnostics_result.txt` 是否补齐代码质量相关状态项。",
            "- 检查 `实现依据记录.md` 是否真实存在,并回链到本轮正式改动、计划依据和参考资料依据。",
            "- 检查 `runtime_check_report.md` 是否回链到真实存在的 `runtime_evidence.json`。",
            "- 检查 `runtime_evidence.json` 是否真实包含样本路径/身份、shape/dtype、loss finite、backward、optimizer.step 等字段。",
            "- 检查 Post-QC Guard 表格、runtime 报告、runtime 证据 JSON、diagnostics 四者是否一致。",
            "- 检查代码质量门禁是否只在真实运行证据成立时才返回 `pass`。",
            "",
            "## 4. 检查结果",
        ]
    )
    for issue in issue_lines:
        lines.append(f"- `{issue.severity}`: {issue.message}")
    lines.extend(
        [
            "",
            "## 5. 结论",
            f"- `code_quality_gate_status`: `{status}`",
        ]
    )
    return status, "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    post_qc_guard = (project_root / normalize_relpath(args.post_qc_guard)).resolve()
    if not post_qc_guard.exists():
        raise SystemExit(f"Post-QC Guard does not exist: {post_qc_guard}")

    post_qc_text = read_text(post_qc_guard)
    review_required, code_paths, issues = code_quality_review_required(post_qc_text)

    backchain = extract_level2_section(post_qc_text, "## 5.1 关键回链")
    diagnostics_rel = normalize_relpath(extract_field_value(backchain, "- `diagnostics_result.txt` 路径:"))
    if not diagnostics_rel:
        diagnostics_rel = "diagnostics_result.txt"
    diagnostics_path = resolve_anchor_path(project_root, post_qc_guard, diagnostics_rel)
    diagnostics_text = read_text(diagnostics_path) if diagnostics_path else ""
    runtime_profile = "full_training_runtime"
    runtime_report_path = extract_runtime_report_path(project_root, post_qc_guard, post_qc_text)
    if runtime_report_path and runtime_report_path.exists():
        runtime_profile = infer_runtime_profile_from_runtime_report(read_text(runtime_report_path))

    diagnostics_issues, diagnostics_map = analyze_diagnostics(
        diagnostics_path,
        diagnostics_text,
        review_required,
        runtime_profile,
    )
    issues.extend(diagnostics_issues)
    issues.extend(
        analyze_implementation_record(
            project_root,
            post_qc_guard,
            post_qc_text,
            review_required,
            code_paths,
        )
    )

    runtime_issues, runtime_evidence, runtime_status_map, _, runtime_profile = analyze_runtime_evidence(
        project_root,
        post_qc_guard,
        post_qc_text,
        diagnostics_map,
        review_required,
        runtime_profile,
    )
    issues.extend(runtime_issues)
    issues.extend(
        analyze_post_qc_table(
            post_qc_text,
            review_required,
            runtime_evidence.get("checks", {}) if isinstance(runtime_evidence, dict) else {},
            runtime_profile,
        )
    )
    issues.extend(
        analyze_consistency(
            post_qc_text,
            diagnostics_map,
            review_required,
            runtime_status_map,
        )
    )

    status, report_text = render_report(post_qc_guard, review_required, code_paths, issues, runtime_profile)
    if args.output:
        output_path = (project_root / normalize_relpath(args.output)).resolve()
    else:
        output_path = post_qc_guard.parent / "code_quality_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")

    print(f"code_quality_gate_status={status}")
    print(f"report_path={output_path.as_posix()}")


if __name__ == "__main__":
    main()
