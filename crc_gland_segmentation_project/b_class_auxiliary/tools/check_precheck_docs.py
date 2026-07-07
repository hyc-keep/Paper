"""Validate the Pre-check guard bundle before implementation starts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import Iterable


VALID_STAGE_GATE_RESULTS = {"allow", "blocked"}
VALID_STAGE_DEFINITION_RESULTS = {"pass", "partial", "fail"}
VALID_MAPPING_ACTIONS = {"create", "update", "append_version", "not_applicable"}
REQUIRED_CONSTRAINT_TYPES = (
    "官方协议固定项",
    "路线层已锁定",
    "论文支持的候选范围",
    "工程冻结规则",
)
REQUIRED_SCAN_DIRS = (
    "datasets/",
    "splits/",
    "configs/",
    "src/",
    "scripts/",
    "tools/",
    "b_class_auxiliary/",
    "experiments/",
    "external/",
    "reports/",
)
PATH_ANCHOR_PATTERN = re.compile(r"`([^`\n]*(?:/|\\|\.md|\.py|\.yaml|\.csv|\.txt)[^`\n]*)`")
NUMERIC_EVIDENCE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\b")
PLACEHOLDER_PATTERN = re.compile(
    r"^\[(?:目录|文件|路径|说明|状态|动作|原因|结论|结果|资产|字段|样本).*\]$"
    r"|^xx_.*$|^xxx.*$|^\.\.\.$",
    re.IGNORECASE,
)
SCAN_EXISTENCE_KEYWORDS = (
    "存在",
    "不存在",
    "缺失",
    "占位",
    "已实现",
    "未实现",
    "可复用",
    "空目录",
    "沿用",
)
SCAN_IMPACT_KEYWORDS = ("受影响", "不受影响", "是", "否", "会改", "不改", "新增", "修改", "沿用")
SCAN_SAMPLE_KEYWORDS = (
    ".csv",
    ".yaml",
    ".yml",
    ".py",
    ".md",
    ".txt",
    ".ckpt",
    "metrics",
    "样本",
    "文件",
    "资产",
    "目录",
)
SCAN_EMPTY_KEYWORDS = ("空目录", "暂无", "未产生", "没有", "not_applicable", "不适用")
SCAN_EXISTS_POSITIVE_KEYWORDS = ("已存在", "存在", "已成体系", "可运行", "已齐全")
SCAN_EXISTS_NEGATIVE_KEYWORDS = ("不存在", "缺失", "未创建", "为空")


@dataclass
class Issue:
    severity: str
    message: str


@dataclass
class MappingRow:
    object_path: str
    doc_path: str
    action: str
    note: str


@dataclass
class DirSnapshot:
    rel_path: str
    abs_path: Path
    exists: bool
    file_count: int
    dir_count: int
    sample_files: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Pre-check guard documents before coding starts."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--precheck-guard",
        required=True,
        help="Relative path to the task Pre-check Guard markdown file.",
    )
    parser.add_argument(
        "--output",
        default="",
        help=(
            "Optional relative path for the generated report. "
            "Defaults to the Pre-check guard directory + precheck_doc_gate_report.md."
        ),
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def resolve_input_path(project_root: Path, raw_path: str, base_dir: Path | None = None) -> Path:
    normalized = normalize_relpath(raw_path)
    workspace_root = project_root.parent
    candidates = [
        project_root / normalized,
        workspace_root / normalized,
    ]
    if base_dir is not None:
        candidates.append(base_dir / normalized)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (project_root / normalized).resolve()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_markdown_value(value: str) -> str:
    return value.strip().strip("`").strip()


def is_placeholder_value(value: str) -> bool:
    normalized = normalize_markdown_value(value)
    if not normalized:
        return True
    return bool(PLACEHOLDER_PATTERN.match(normalized))


def has_substantive_value(value: str) -> bool:
    normalized = normalize_markdown_value(value)
    return bool(normalized) and not is_placeholder_value(normalized)


def contains_any_keyword(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


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
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)"
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_field_value(section: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}\s*(.+)$", section)
    return match.group(1).strip() if match else ""


def count_meaningful_lines(text: str) -> int:
    count = 0
    in_code_block = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not line:
            continue
        count += 1
    return count


def parse_stage_definition_result(report_text: str) -> str:
    match = re.search(
        r"(?m)^- `stage_definition_gate_status`:\s*`?(pass|partial|fail)`?\s*$",
        report_text,
    )
    return match.group(1) if match else ""


def extract_backtick_paths(text: str) -> list[str]:
    return [normalize_relpath(value) for value in PATH_ANCHOR_PATTERN.findall(text)]


def should_skip_anchor(anchor: str) -> bool:
    if not anchor:
        return True
    lowered = anchor.lower()
    if lowered.startswith(("http://", "https://")):
        return True
    if "*" in anchor:
        return True
    if "[" in anchor and "]" in anchor:
        return True
    return False


def resolve_anchor_path(project_root: Path, doc_path: Path, anchor: str) -> Path | None:
    normalized = normalize_relpath(anchor)
    if should_skip_anchor(normalized):
        return None

    workspace_root = project_root.parent
    plan_root = workspace_root / "结直肠腺体分割_plan_优化版"
    plan_exec_root = plan_root / "01_实验执行"
    plan_overview_root = plan_exec_root / "00_总览与规范"

    candidate_strings = (
        normalized,
        normalized.lstrip("./"),
    )
    candidates: list[Path] = []
    for candidate_text in candidate_strings:
        candidate_path = Path(candidate_text)
        if candidate_path.is_absolute():
            candidates.append(candidate_path)
        candidates.append(project_root / candidate_text)
        candidates.append(workspace_root / candidate_text)
        candidates.append(doc_path.parent / candidate_text)
        candidates.append(plan_root / candidate_text)
        candidates.append(plan_exec_root / candidate_text)
        candidates.append(plan_overview_root / candidate_text)

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate.resolve()
    return None


def collect_resolved_anchors(project_root: Path, doc_path: Path, text: str) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()
    for anchor in extract_backtick_paths(text):
        normalized = normalize_relpath(anchor)
        if normalized in seen or should_skip_anchor(normalized):
            continue
        seen.add(normalized)
        if resolve_anchor_path(project_root, doc_path, normalized) is not None:
            resolved.append(normalized)
        else:
            missing.append(normalized)
    return resolved, missing


def row_value(row: dict[str, str], key: str) -> str:
    return row.get(key, "").strip()


def anchor_belongs_to_scan_dir(anchor: str, scan_dir: str) -> bool:
    normalized = normalize_relpath(anchor)
    if scan_dir == "reports/":
        return normalized.startswith("reports/") and normalized != "reports/"
    return normalized.startswith(scan_dir) and normalized != scan_dir


def scan_directory_snapshot(project_root: Path, scan_dir: str) -> DirSnapshot:
    abs_path = (project_root / scan_dir).resolve()
    if not abs_path.exists():
        return DirSnapshot(
            rel_path=scan_dir,
            abs_path=abs_path,
            exists=False,
            file_count=0,
            dir_count=0,
            sample_files=[],
        )

    file_count = 0
    dir_count = 0
    sample_files: list[str] = []
    try:
        for current_root, dirnames, filenames in os.walk(abs_path):
            dir_count += len(dirnames)
            file_count += len(filenames)
            if len(sample_files) < 3:
                root_path = Path(current_root)
                for filename in filenames:
                    if len(sample_files) >= 3:
                        break
                    sample_files.append(root_path.joinpath(filename).relative_to(project_root).as_posix())
    except OSError:
        return DirSnapshot(
            rel_path=scan_dir,
            abs_path=abs_path,
            exists=True,
            file_count=file_count,
            dir_count=dir_count,
            sample_files=sample_files,
        )

    return DirSnapshot(
        rel_path=scan_dir,
        abs_path=abs_path,
        exists=True,
        file_count=file_count,
        dir_count=dir_count,
        sample_files=sample_files,
    )


def text_claims_exists(text: str) -> bool:
    return contains_any_keyword(text, SCAN_EXISTS_POSITIVE_KEYWORDS)


def text_claims_missing(text: str) -> bool:
    return contains_any_keyword(text, SCAN_EXISTS_NEGATIVE_KEYWORDS)


def text_claims_empty(text: str) -> bool:
    return contains_any_keyword(text, SCAN_EMPTY_KEYWORDS)


def analyze_current_codebase_scan(
    project_root: Path,
    codebase_state_path: Path,
    codebase_state_text: str,
) -> list[Issue]:
    issues: list[Issue] = []
    dir_snapshots = {
        scan_dir: scan_directory_snapshot(project_root, scan_dir)
        for scan_dir in REQUIRED_SCAN_DIRS
    }

    try:
        scope_rows = extract_table_rows(codebase_state_text, "## 0. 本轮最小扫描范围")
    except ValueError:
        scope_rows = []
        issues.append(
            Issue(
                "fail",
                "`current_codebase_状态.md` 缺少 `## 0. 本轮最小扫描范围` 表格，无法证明扫描范围已经按模板展开。",
            )
        )

    scope_map: dict[str, dict[str, str]] = {
        normalize_relpath(row_value(row, "目录")): row for row in scope_rows if row_value(row, "目录")
    }
    for scan_dir in REQUIRED_SCAN_DIRS:
        row = scope_map.get(scan_dir)
        snapshot = dir_snapshots[scan_dir]
        if row is None:
            issues.append(
                Issue(
                    "fail",
                    f"`current_codebase_状态.md` 的最小扫描范围缺少目录 `{scan_dir}`。",
                )
            )
            continue

        if not snapshot.exists:
            issues.append(
                Issue(
                    "fail",
                    f"项目真实目录缺失 `{scan_dir}`，但 `current_codebase_状态.md` 仍把它当作最小扫描范围的一部分。",
                )
            )
            continue

        why_scan = row_value(row, "为什么必须扫描")
        min_check = row_value(row, "最低检查动作")
        if not has_substantive_value(why_scan):
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“为什么必须扫描”仍是空壳或占位内容。",
                )
            )
        if not has_substantive_value(min_check):
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“最低检查动作”仍是空壳或占位内容。",
                )
            )
        elif not (
            contains_any_keyword(min_check, SCAN_EXISTENCE_KEYWORDS)
            or contains_any_keyword(min_check, SCAN_SAMPLE_KEYWORDS)
            or NUMERIC_EVIDENCE_PATTERN.search(min_check)
        ):
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“最低检查动作”没有写出存在性/样本/计数类物理检查信号。",
                )
            )
        if not any(anchor_belongs_to_scan_dir(anchor, scan_dir) for anchor in extract_backtick_paths(min_check)):
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“最低检查动作”没有留下该目录下的真实路径锚点，"
                    "更像抽象说明而不是实际扫描。",
                )
            )

    try:
        scan_rows = extract_table_rows(codebase_state_text, "## 1. 当前阶段相关目录扫描")
    except ValueError:
        scan_rows = []
        issues.append(
            Issue(
                "fail",
                "`current_codebase_状态.md` 缺少 `## 1. 当前阶段相关目录扫描` 表格，无法证明逐目录扫描结果。",
            )
        )

    resolved_anchors, _ = collect_resolved_anchors(project_root, codebase_state_path, codebase_state_text)
    dir_anchor_map = {
        scan_dir: [anchor for anchor in resolved_anchors if anchor_belongs_to_scan_dir(anchor, scan_dir)]
        for scan_dir in REQUIRED_SCAN_DIRS
    }
    section_1 = extract_level2_section(codebase_state_text, "## 1. 当前阶段相关目录扫描")

    for scan_dir in REQUIRED_SCAN_DIRS:
        snapshot = dir_snapshots[scan_dir]
        matching_rows = [
            row for row in scan_rows if scan_dir in normalize_relpath(row_value(row, "目录"))
        ]
        if not matching_rows:
            issues.append(
                Issue(
                    "fail",
                    f"`current_codebase_状态.md` 的 `## 1. 当前阶段相关目录扫描` 没有为 `{scan_dir}` 留下逐目录扫描结果。",
                )
            )
            continue

        assets_present = False
        status_present = False
        status_signal_present = False
        impact_present = False
        impact_signal_present = False
        row_has_evidence = False
        for row in matching_rows:
            assets = row_value(row, "已有文件/资产")
            status = row_value(row, "状态")
            impact = row_value(row, "本次是否受影响")
            row_text = " ".join((assets, status, impact))
            if has_substantive_value(assets):
                assets_present = True
            if has_substantive_value(status):
                status_present = True
                if (
                    contains_any_keyword(status, SCAN_EXISTENCE_KEYWORDS)
                    or NUMERIC_EVIDENCE_PATTERN.search(status)
                ):
                    status_signal_present = True
            if has_substantive_value(impact):
                impact_present = True
                if contains_any_keyword(impact, SCAN_IMPACT_KEYWORDS):
                    impact_signal_present = True

            row_has_anchor = any(anchor_belongs_to_scan_dir(anchor, scan_dir) for anchor in extract_backtick_paths(row_text))
            row_has_numeric = bool(NUMERIC_EVIDENCE_PATTERN.search(row_text))
            row_has_sample_signal = contains_any_keyword(row_text, SCAN_SAMPLE_KEYWORDS)
            if row_has_anchor and (row_has_numeric or row_has_sample_signal):
                row_has_evidence = True

            if snapshot.exists and text_claims_missing(row_text) and not text_claims_empty(row_text):
                issues.append(
                    Issue(
                        "fail",
                        f"`current_codebase_状态.md` 把 `{scan_dir}` 写成缺失/不存在，但真实目录 `{snapshot.abs_path}` 实际存在。",
                    )
                )
            if not snapshot.exists and text_claims_exists(row_text):
                issues.append(
                    Issue(
                        "fail",
                        f"`current_codebase_状态.md` 把 `{scan_dir}` 写成已存在，但真实目录 `{snapshot.abs_path}` 并不存在。",
                    )
                )
            if snapshot.file_count == 0 and snapshot.dir_count == 0 and not text_claims_empty(row_text):
                issues.append(
                    Issue(
                        "partial",
                        f"`current_codebase_状态.md` 没有诚实说明 `{scan_dir}` 当前为空目录/暂无正式资产。",
                    )
                )

        if not assets_present:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“已有文件/资产”仍是空壳或占位内容。",
                )
            )
        if not status_present:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“状态”仍是空壳或占位内容。",
                )
            )
        elif not status_signal_present:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“状态”没有写出存在性/实现度判断信号。",
                )
            )
        if not impact_present:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“本次是否受影响”仍是空壳或占位内容。",
                )
            )
        elif not impact_signal_present:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 中 `{scan_dir}` 的“本次是否受影响”没有写出明确影响判断。",
                )
            )

        anchor_count = len(dir_anchor_map[scan_dir])
        if not row_has_evidence:
            if anchor_count == 0:
                issues.append(
                    Issue(
                        "fail",
                        f"`current_codebase_状态.md` 对 `{scan_dir}` 没有留下任何可解析到真实文件的扫描样本路径。",
                    )
                )
            elif not NUMERIC_EVIDENCE_PATTERN.search(section_1):
                issues.append(
                    Issue(
                        "partial",
                        f"`current_codebase_状态.md` 对 `{scan_dir}` 虽然出现了真实路径，但没有同时留下行数/计数/字段值等物理证据。",
                    )
                )
        if snapshot.exists and snapshot.file_count > 0 and anchor_count == 0:
            sample_hint = "`, `".join(snapshot.sample_files[:2]) if snapshot.sample_files else scan_dir
            issues.append(
                Issue(
                    "fail",
                    f"`current_codebase_状态.md` 对 `{scan_dir}` 没有留下任何真实样本路径，"
                    f"但磁盘扫描显示该目录已有文件，可至少回链 `{sample_hint}`。",
                )
            )
        if snapshot.exists and snapshot.file_count > 0 and not NUMERIC_EVIDENCE_PATTERN.search(" ".join(
            row_value(row, "已有文件/资产") + " " + row_value(row, "状态")
            for row in matching_rows
        )):
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 对 `{scan_dir}` 没有留下文件数/样本数/字段值等量化信号，"
                    f"当前真实扫描至少识别到 `{snapshot.file_count}` 个文件。",
                )
            )

    return issues


def parse_mapping_rows(markdown_text: str) -> list[MappingRow]:
    rows = extract_table_rows(markdown_text, "## 6.1 预期文档映射")
    mapping_rows: list[MappingRow] = []
    for row in rows:
        doc_path = row.get("对应学习型说明文", row.get("对象级说明文", ""))
        mapping_rows.append(
            MappingRow(
                object_path=normalize_relpath(row["本轮变更对象"]),
                doc_path=normalize_relpath(doc_path),
                action=normalize_relpath(row["计划动作"]),
                note=row["备注"].strip(),
            )
        )
    return mapping_rows


def parse_stage_gate_result(text: str) -> str:
    for source in (extract_level2_section(text, "## 5. 结论"), text):
        match = re.search(r"Stage Gate Result:\s*`?([a-z_ /]+)`?", source)
        if match:
            return normalize_relpath(match.group(1)).split("/")[0].strip()
    return ""


def analyze_anchor_resolution(project_root: Path, doc_path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    resolved_anchors, missing = collect_resolved_anchors(project_root, doc_path, text)
    resolved = len(resolved_anchors)

    if resolved < 2:
        issues.append(
            Issue(
                "partial",
                f"文档 `{doc_path.name}` 的真实存在路径锚点数为 `{resolved}`，低于最小要求 `2`。",
            )
        )
    if missing:
        sample = "`, `".join(missing[:5])
        issues.append(
            Issue(
                "partial",
                f"文档 `{doc_path.name}` 存在无法解析到真实文件的路径锚点: `{sample}`。",
            )
        )
    return issues


def evaluate_task(project_root: Path, precheck_guard_path: Path) -> tuple[str, list[str]]:
    issues: list[Issue] = []
    guard_dir = precheck_guard_path.parent
    stage_definition_report_path = guard_dir / "stage_definition_gate_report.md"
    extraction_path = guard_dir / "pre_check_extraction.md"
    stage_gate_path = guard_dir / "stage_gate_check.md"
    codebase_state_path = guard_dir / "current_codebase_状态.md"

    for required_path in (
        stage_definition_report_path,
        extraction_path,
        stage_gate_path,
        codebase_state_path,
        precheck_guard_path,
    ):
        if not required_path.exists():
            issues.append(Issue("fail", f"Pre-check 前置文件缺失: `{required_path.name}`"))

    if any(issue.severity == "fail" for issue in issues):
        return "fail", [f"- [{issue.severity}] {issue.message}" for issue in issues]

    guard_text = read_text(precheck_guard_path)
    stage_definition_report_text = read_text(stage_definition_report_path)
    extraction_text = read_text(extraction_path)
    stage_gate_text = read_text(stage_gate_path)
    codebase_state_text = read_text(codebase_state_path)

    guard_section_1 = extract_level2_section(guard_text, "## 1. 本次任务归属")
    guard_section_6 = extract_level2_section(guard_text, "## 6. 预期代码落点")
    guard_section_7 = extract_level2_section(guard_text, "## 7. 上游 guard 文件回链")

    stage_card_path_value = normalize_relpath(extract_field_value(guard_section_1, "- 阶段实现卡路径:"))
    stage_card_path = resolve_input_path(project_root, stage_card_path_value, precheck_guard_path.parent) if stage_card_path_value else None
    stage_definition_result = normalize_relpath(extract_field_value(guard_section_1, "- 阶段锁定门禁结论:")).split("/")[0].strip()
    guard_stage_gate = normalize_relpath(extract_field_value(guard_section_1, "- Stage Gate Result:")).split("/")[0].strip()
    report_stage_definition_result = parse_stage_definition_result(stage_definition_report_text)
    if not stage_card_path_value:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `阶段实现卡路径`。"))
    elif Path(stage_card_path_value).name != "00_阶段实现卡.md":
        issues.append(Issue("fail", f"Pre-check Guard 的 `阶段实现卡路径` 不是 `00_阶段实现卡.md`: `{stage_card_path_value}`。"))
    elif stage_card_path is None or not stage_card_path.exists():
        issues.append(Issue("fail", f"Pre-check Guard 指向的阶段实现卡不存在: `{stage_card_path_value}`。"))
    if stage_definition_result not in VALID_STAGE_DEFINITION_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"Pre-check Guard 的 `阶段锁定门禁结论` 不在允许集合内: `{stage_definition_result}`。",
            )
        )
    if report_stage_definition_result not in VALID_STAGE_DEFINITION_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"`stage_definition_gate_report.md` 的 `stage_definition_gate_status` 不在允许集合内: `{report_stage_definition_result}`。",
            )
        )
    if (
        stage_definition_result in VALID_STAGE_DEFINITION_RESULTS
        and report_stage_definition_result in VALID_STAGE_DEFINITION_RESULTS
        and stage_definition_result != report_stage_definition_result
    ):
        issues.append(
            Issue(
                "fail",
                "Pre-check Guard 与 `stage_definition_gate_report.md` 的阶段锁定结论不一致: "
                f"`{stage_definition_result}` vs `{report_stage_definition_result}`。",
            )
        )
    if report_stage_definition_result != "pass":
        issues.append(
            Issue(
                "fail",
                "`stage_definition_gate_report.md` 不是 `pass`，当前任务还不允许被视为正式 Pre-check。",
            )
        )
    if any(issue.severity == "fail" for issue in issues):
        return "fail", [f"- [{issue.severity}] {issue.message}" for issue in issues]

    stage_card_text = read_text(stage_card_path)
    stage_gate_result = parse_stage_gate_result(stage_gate_text)
    if guard_stage_gate not in VALID_STAGE_GATE_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"Pre-check Guard 的 `Stage Gate Result` 不在允许集合内: `{guard_stage_gate}`。",
            )
        )
    if stage_gate_result not in VALID_STAGE_GATE_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"`stage_gate_check.md` 的 `Stage Gate Result` 不在允许集合内: `{stage_gate_result}`。",
            )
        )
    if (
        guard_stage_gate in VALID_STAGE_GATE_RESULTS
        and stage_gate_result in VALID_STAGE_GATE_RESULTS
        and guard_stage_gate != stage_gate_result
    ):
        issues.append(
            Issue(
                "fail",
                "Pre-check Guard 与 `stage_gate_check.md` 的 `Stage Gate Result` 不一致: "
                f"`{guard_stage_gate}` vs `{stage_gate_result}`。",
            )
        )

    if count_meaningful_lines(guard_section_6) < 4:
        issues.append(
            Issue(
                "partial",
                "Pre-check Guard 的 `## 6. 预期代码落点` 仍然过空，无法支撑后续越界核对。",
            )
        )

    if "pre_check_extraction.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `pre_check_extraction.md` 回链。"))
    if "00_阶段实现卡.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `00_阶段实现卡.md` 回链。"))
    if "stage_definition_gate_report.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `stage_definition_gate_report.md` 回链。"))
    if "stage_gate_check.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `stage_gate_check.md` 回链。"))
    if "current_codebase_状态.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `current_codebase_状态.md` 回链。"))
    if "precheck_doc_gate_report.md" not in guard_section_7:
        issues.append(Issue("fail", "Pre-check Guard 缺少 `precheck_doc_gate_report.md` 回链。"))

    try:
        mapping_rows = parse_mapping_rows(guard_text)
    except ValueError:
        mapping_rows = []
        issues.append(
            Issue(
                "fail",
                "Pre-check Guard 缺少 `## 6.1 预期文档映射`，无法证明对象-说明文关系已在编码前声明。",
            )
        )
    for row in mapping_rows:
        if row.action not in VALID_MAPPING_ACTIONS:
            issues.append(
                Issue(
                    "fail",
                    f"预期文档映射对象 `{row.object_path}` 的动作 `{row.action}` 不在允许集合内。",
                )
            )
        if not row.note:
            issues.append(
                Issue(
                    "partial",
                    f"预期文档映射对象 `{row.object_path}` 缺少 `备注`，无法解释为什么这样判定。",
                )
            )
        if row.action == "not_applicable":
            continue
        if not row.doc_path.startswith("reports/stage_reports/implementation_tracking/"):
            issues.append(
                Issue(
                    "fail",
                    f"预期文档映射对象 `{row.object_path}` 的说明文路径不在 `implementation_tracking` 下: `{row.doc_path}`。",
                )
            )

    try:
        extraction_rows = extract_table_rows(extraction_text, "## 2. 规划约束提取")
    except ValueError:
        extraction_rows = []
        issues.append(
            Issue(
                "fail",
                "`pre_check_extraction.md` 缺少 `## 2. 规划约束提取` 表格。",
            )
        )
    extraction_types = {normalize_relpath(row["约束类型"]) for row in extraction_rows}
    missing_types = [name for name in REQUIRED_CONSTRAINT_TYPES if name not in extraction_types]
    if missing_types:
        issues.append(
            Issue(
                "partial",
                "`pre_check_extraction.md` 未完整覆盖四类约束类型: "
                f"`{', '.join(missing_types)}`。",
            )
        )

    expected_landing_section = extract_level2_section(extraction_text, "## 2.1 预期工程落点")
    if count_meaningful_lines(expected_landing_section) < 4:
        issues.append(
            Issue(
                "partial",
                "`pre_check_extraction.md` 的 `## 2.1 预期工程落点` 仍然过空，无法支撑 Pre-check 预判。",
            )
        )

    route_section = extract_level2_section(extraction_text, "## 3. 路线层约束提取")
    reference_section = extract_level2_section(extraction_text, "## 4. 文献/参考实现提取")
    variable_section = extract_level2_section(extraction_text, "## 5. 当前阶段唯一允许改动的变量")
    if count_meaningful_lines(route_section) < 3:
        issues.append(Issue("partial", "`pre_check_extraction.md` 的路线层约束提取仍然过空。"))
    if count_meaningful_lines(reference_section) < 3:
        issues.append(Issue("partial", "`pre_check_extraction.md` 的文献/参考实现提取仍然过空。"))
    if "允许改" not in variable_section or "不允许改" not in variable_section:
        issues.append(
            Issue(
                "partial",
                "`pre_check_extraction.md` 没有把“允许改 / 不允许改”写清楚。",
            )
        )

    stage_card_goal = extract_level2_section(stage_card_text, "## 3. 当前阶段唯一目标")
    stage_card_why_now = extract_level2_section(stage_card_text, "## 4. 为什么现在做这个,而不是下一个阶段")
    stage_card_boundary = extract_level2_section(stage_card_text, "## 5. 当前阶段允许改动 / 禁止改动")
    stage_card_landing = extract_level2_section(stage_card_text, "## 7. 本轮工程落点")
    stage_card_verify = extract_level2_section(stage_card_text, "## 8. 本轮最小运行验证计划")
    if count_meaningful_lines(stage_card_goal) < 3:
        issues.append(Issue("partial", "`00_阶段实现卡.md` 的阶段唯一目标章节仍然过空。"))
    if count_meaningful_lines(stage_card_why_now) < 3:
        issues.append(Issue("partial", "`00_阶段实现卡.md` 没有把“为什么现在做而不是下一个阶段”写清。"))
    if count_meaningful_lines(stage_card_boundary) < 3:
        issues.append(Issue("partial", "`00_阶段实现卡.md` 的允许改/禁止改章节仍然过空。"))
    if count_meaningful_lines(stage_card_landing) < 3:
        issues.append(Issue("partial", "`00_阶段实现卡.md` 的工程落点章节仍然过空。"))
    if count_meaningful_lines(stage_card_verify) < 3:
        issues.append(Issue("partial", "`00_阶段实现卡.md` 的最小运行验证计划仍然过空。"))

    stage_gate_conditions = extract_level2_section(stage_gate_text, "## 3. 当前阶段进入条件")
    stage_gate_blockers = extract_level2_section(stage_gate_text, "## 4. 阻断项")
    stage_gate_landing = extract_level2_section(stage_gate_text, "## 5.1 本轮允许进入的工程落点")
    if count_meaningful_lines(stage_gate_conditions) < 4:
        issues.append(Issue("partial", "`stage_gate_check.md` 的进入条件表仍然过空。"))
    if count_meaningful_lines(stage_gate_blockers) < 4:
        issues.append(Issue("partial", "`stage_gate_check.md` 的阻断项表仍然过空。"))
    if count_meaningful_lines(stage_gate_landing) < 4:
        issues.append(Issue("partial", "`stage_gate_check.md` 的工程落点表仍然过空。"))

    scan_scope_section = extract_level2_section(codebase_state_text, "## 0. 本轮最小扫描范围")
    missing_scan_dirs = [name for name in REQUIRED_SCAN_DIRS if name not in scan_scope_section]
    if missing_scan_dirs:
        issues.append(
            Issue(
                "fail",
                "`current_codebase_状态.md` 没有覆盖最小扫描目录范围: "
                f"`{', '.join(missing_scan_dirs)}`。",
            )
        )
    for heading in (
        "## 1. 当前阶段相关目录扫描",
        "## 2. 已实现能力",
        "## 3. 缺口与风险",
        "## 4. 本次预计新增/修改",
        "## 5. 预期工程落点汇总",
    ):
        section = extract_level2_section(codebase_state_text, heading)
        if count_meaningful_lines(section) < 3:
            issues.append(
                Issue(
                    "partial",
                    f"`current_codebase_状态.md` 的 `{heading}` 章节仍然过空。",
                )
            )

    issues.extend(analyze_current_codebase_scan(project_root, codebase_state_path, codebase_state_text))

    for doc_path, doc_text in (
        (stage_card_path, stage_card_text),
        (stage_definition_report_path, stage_definition_report_text),
        (precheck_guard_path, guard_text),
        (extraction_path, extraction_text),
        (stage_gate_path, stage_gate_text),
        (codebase_state_path, codebase_state_text),
    ):
        issues.extend(analyze_anchor_resolution(project_root, doc_path, doc_text))

    detail_lines = [f"- [{issue.severity}] {issue.message}" for issue in issues]
    if any(issue.severity == "fail" for issue in issues):
        return "fail", detail_lines
    if any(issue.severity == "partial" for issue in issues):
        return "partial", detail_lines
    return "pass", ["- [pass] Pre-check 四件套存在、Stage Gate 一致、约束提取与工程扫描锚点检查均通过。"]


def build_report(
    project_root: Path,
    precheck_guard: Path,
    status: str,
    details: Iterable[str],
) -> str:
    lines = [
        "# Precheck Doc Gate Report",
        "",
        "## 1. 输入文件",
        f"- `project_root`: `{project_root}`",
        f"- `precheck_guard`: `{precheck_guard.relative_to(project_root).as_posix()}`",
        "",
        "## 2. 检查范围",
        "- 检查 `00_阶段实现卡.md` 与 `stage_definition_gate_report.md` 是否存在，并确认阶段锁定门禁已经先于 Pre-check 裁成 `pass`。",
        "- 检查 `pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md` 与 `Pre-check Guard` 是否全部存在。",
        "- 检查 `Pre-check Guard` 与 `stage_definition_gate_report.md` 的阶段锁定结论是否一致。",
        "- 检查 `Pre-check Guard` 与 `stage_gate_check.md` 的 `Stage Gate Result` 是否一致。",
        "- 检查 `Pre-check Guard` 是否回链 `00_阶段实现卡.md`、`stage_definition_gate_report.md`、四件套与 `precheck_doc_gate_report.md`，并保留 `6.1 预期文档映射`。",
        "- 检查 `pre_check_extraction.md` 是否覆盖 `官方协议固定项 / 路线层已锁定 / 论文支持的候选范围 / 工程冻结规则` 四类约束。",
        "- 检查 `current_codebase_状态.md` 是否覆盖 `datasets/`、`splits/`、`configs/`、`src/`、`scripts/`、`tools/`、`b_class_auxiliary/`、`experiments/`、`external/`、`reports/` 的最小扫描范围。",
        "- 检查阶段实现卡和 Pre-check 文件中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。",
        "",
        "## 3. 结论",
        f"- `precheck_doc_gate_status`: `{status}`",
        "",
        "## 4. 详细结果",
        *details,
        "",
    ]
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    precheck_guard = (project_root / normalize_relpath(args.precheck_guard)).resolve()
    if not precheck_guard.exists():
        raise FileNotFoundError(f"Pre-check guard not found: {precheck_guard}")

    if args.output:
        output_path = (project_root / normalize_relpath(args.output)).resolve()
    else:
        output_path = precheck_guard.parent / "precheck_doc_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status, details = evaluate_task(project_root, precheck_guard)
    output_path.write_text(
        build_report(project_root, precheck_guard, status, details),
        encoding="utf-8",
    )

    print(f"precheck_doc_gate_status={status}")
    print(f"wrote_report={output_path}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
