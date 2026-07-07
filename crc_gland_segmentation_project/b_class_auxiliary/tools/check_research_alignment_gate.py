"""Validate the research alignment record before stage locking starts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


PLACEHOLDER_PATTERN = re.compile(
    r"^\[(?:路径|文件|章节|定位|原因|说明|结论|任务|阶段|动作|对象|约束|落点|命令|影响).*\]$"
    r"|^xx_.*$|^xxx.*$|^\.\.\.$",
    re.IGNORECASE,
)
PATH_ANCHOR_PATTERN = re.compile(r"`([^`\n]*(?:/|\\|\.md|\.py|\.yaml|\.csv|\.txt)[^`\n]*)`")
VALID_RESEARCH_RESULTS = {"allow_stage_lock", "blocked"}
IGNORED_FUTURE_OUTPUT_ANCHORS = {
    "00_阶段实现卡.md",
    "stage_definition_gate_report.md",
}


@dataclass
class Issue:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the research alignment record before stage locking."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--research-record",
        required=True,
        help="Relative path to `研究定标记录.md`.",
    )
    parser.add_argument(
        "--output",
        default="",
        help=(
            "Optional relative path for the generated report. "
            "Defaults to the research-record directory + research_alignment_gate_report.md."
        ),
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


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


def extract_level2_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)")
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_field_value(section: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}\s*(.+)$", section)
    return match.group(1).strip() if match else ""


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


def resolve_anchor(project_root: Path, doc_path: Path, anchor: str) -> Path | None:
    anchor = normalize_relpath(anchor)
    if not anchor or anchor.startswith(("http://", "https://")):
        return None

    workspace_root = project_root.parent
    candidates = [
        project_root / anchor,
        workspace_root / anchor,
        doc_path.parent / anchor,
    ]
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate.resolve()) if candidate.exists() else str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate.resolve()
    return None


def analyze_anchor_resolution(project_root: Path, doc_path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    anchors = [
        normalize_relpath(item)
        for item in PATH_ANCHOR_PATTERN.findall(text)
        if normalize_relpath(item) not in IGNORED_FUTURE_OUTPUT_ANCHORS
    ]
    if not anchors:
        issues.append(Issue("partial", "研究定标记录没有留下任何可解析路径锚点。"))
        return issues

    missing: list[str] = []
    resolved_count = 0
    for anchor in anchors:
        resolved = resolve_anchor(project_root, doc_path, anchor)
        if resolved is None:
            missing.append(anchor)
        else:
            resolved_count += 1

    if resolved_count < 4:
        issues.append(
            Issue(
                "partial",
                f"研究定标记录当前只留下 `{resolved_count}` 个可解析路径锚点，低于最小要求 `4`。",
            )
        )
    if missing:
        sample = "`, `".join(missing[:5])
        issues.append(
            Issue(
                "partial",
                f"研究定标记录存在无法解析到真实文件的路径锚点: `{sample}`。",
            )
        )
    return issues


def analyze_table_rows(
    issues: list[Issue],
    rows: list[dict[str, str]],
    required_columns: tuple[str, ...],
    table_name: str,
    min_rows: int,
) -> None:
    if len(rows) < min_rows:
        issues.append(Issue("partial", f"{table_name} 当前有效行数为 `{len(rows)}`，低于最小要求 `{min_rows}`。"))
    substantive_rows = 0
    for row in rows:
        if all(has_substantive_value(row.get(column, "")) for column in required_columns):
            substantive_rows += 1
    if substantive_rows < min_rows:
        issues.append(
            Issue(
                "partial",
                f"{table_name} 当前只有 `{substantive_rows}` 行满足关键列非占位要求，低于最小要求 `{min_rows}`。",
            )
        )


def analyze_task(project_root: Path, research_record_path: Path) -> tuple[str, list[str]]:
    issues: list[Issue] = []
    if not research_record_path.exists():
        return "fail", [f"- [fail] 研究定标记录不存在: `{research_record_path}`"]

    text = read_text(research_record_path)
    if count_meaningful_lines(text) < 30:
        issues.append(Issue("partial", "研究定标记录有效正文仍然过空，无法支撑进入阶段锁定。"))

    required_headings = (
        "## 1. 记录角色与边界",
        "## 2. 本轮直接依赖的已读文件",
        "## 3. 当前阶段研究目标",
        "## 4. 从计划与协议中提取的硬约束",
        "## 5. 从参考资料 / 论文 / 官方脚本中提取的硬约束",
        "## 6. 当前阶段边界初判",
        "## 7. 对后续阶段锁定的输入",
        "## 8. 当前未决问题与阻断项",
        "## 9. 研究结论",
    )
    for heading in required_headings:
        if heading not in text:
            issues.append(Issue("partial", f"研究定标记录缺少关键章节: `{heading}`。"))

    issues.extend(analyze_anchor_resolution(project_root, research_record_path, text))

    section_1 = extract_level2_section(text, "## 1. 记录角色与边界")
    for label in ("- 当前阶段:", "- 当前任务:", "- 本记录只负责:", "- 本记录不负责:"):
        if not has_substantive_value(extract_field_value(section_1, label)):
            issues.append(Issue("partial", f"`{label}` 缺少有效内容。"))

    section_3 = extract_level2_section(text, "## 3. 当前阶段研究目标")
    for label in ("- 当前阶段唯一研究问题:", "- 这一轮研究要先回答什么:", "- 如果现在不先研究清楚,后面会在哪一步开始靠猜:"):
        if not has_substantive_value(extract_field_value(section_3, label)):
            issues.append(Issue("partial", f"`{label}` 缺少有效内容。"))

    section_6 = extract_level2_section(text, "## 6. 当前阶段边界初判")
    for label in ("- 当前阶段应该做什么:", "- 当前阶段不该做什么:", "- 为什么现在不能直接进入下一个阶段:", "- 如果现在跳过边界锁定,最容易犯什么错:"):
        if not has_substantive_value(extract_field_value(section_6, label)):
            issues.append(Issue("partial", f"`{label}` 缺少有效内容。"))

    section_7 = extract_level2_section(text, "## 7. 对后续阶段锁定的输入")
    for label in ("- 后续 `00_阶段实现卡.md` 必须写清的关键点:", "- 后续阶段锁定最容易写空的地方:", "- 后续最小运行验证计划至少要覆盖:"):
        if not has_substantive_value(extract_field_value(section_7, label)):
            issues.append(Issue("partial", f"`{label}` 缺少有效内容。"))

    section_8 = extract_level2_section(text, "## 8. 当前未决问题与阻断项")
    for label in ("- 目前仍未完全搞清的问题:", "- 哪些问题允许留到阶段锁定再处理:", "- 哪些问题如果不解决,阶段锁定就不能开始:"):
        if not has_substantive_value(extract_field_value(section_8, label)):
            issues.append(Issue("partial", f"`{label}` 缺少有效内容。"))

    section_9 = extract_level2_section(text, "## 9. 研究结论")
    research_result = normalize_markdown_value(extract_field_value(section_9, "- 研究结论状态:"))
    if research_result not in VALID_RESEARCH_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"`研究结论状态` 不在允许集合内: `{research_result}`。",
            )
        )
    if not has_substantive_value(extract_field_value(section_9, "- 结论说明:")):
        issues.append(Issue("partial", "`结论说明` 缺少有效内容。"))
    if not has_substantive_value(extract_field_value(section_9, "- 下一步动作:")):
        issues.append(Issue("partial", "`下一步动作` 缺少有效内容。"))
    if research_result != "allow_stage_lock":
        issues.append(Issue("fail", "研究定标记录正文完整，但 `研究结论状态` 不是 `allow_stage_lock`。"))

    try:
        read_rows = extract_table_rows(text, "## 2. 本轮直接依赖的已读文件")
        analyze_table_rows(
            issues,
            read_rows,
            ("类型", "文件", "为什么本轮必须读", "提取到的直接结论"),
            "已读文件表格",
            3,
        )
    except ValueError as exc:
        issues.append(Issue("partial", str(exc)))

    try:
        plan_rows = extract_table_rows(text, "## 4. 从计划与协议中提取的硬约束")
        analyze_table_rows(
            issues,
            plan_rows,
            ("来源", "提取出的硬约束", "对本阶段的直接影响"),
            "计划与协议硬约束表格",
            3,
        )
    except ValueError as exc:
        issues.append(Issue("partial", str(exc)))

    try:
        ref_rows = extract_table_rows(text, "## 5. 从参考资料 / 论文 / 官方脚本中提取的硬约束")
        analyze_table_rows(
            issues,
            ref_rows,
            ("来源类型", "来源", "提取出的硬约束", "为什么这条约束对本轮必要"),
            "参考资料硬约束表格",
            2,
        )
    except ValueError as exc:
        issues.append(Issue("partial", str(exc)))

    ordered_issues = sorted(issues, key=lambda item: {"fail": 0, "partial": 1}.get(item.severity, 2))
    status = "pass" if not ordered_issues else "blocked"
    lines = [f"- [{item.severity}] {item.message}" for item in ordered_issues]
    if not lines:
        lines.append("- [pass] 研究定标记录章节、来源锚点、约束提取和结论状态都已满足进入阶段锁定的最低要求。")
    return status, lines


def render_report(
    research_record_relpath: str,
    status: str,
    lines: list[str],
) -> str:
    body = [
        "# Research Alignment Gate Report",
        "",
        "## 1. 输入对象",
        f"- research_record_path: `{research_record_relpath}`",
        "",
        "## 2. 检查结果",
        f"- research_alignment_gate_status: `{status}`",
        "",
        "## 3. 详细问题",
        *lines,
        "",
        "## 4. 固定结论",
        "- 规则: 只有 `研究定标记录.md` 的章节、来源锚点、约束提取和研究结论状态都成立,才允许进入阶段锁定。",
        "- 规则: 只要 `research_alignment_gate_status` 不是 `pass`,就不允许把研究阶段口头放行成“已完成”。",
        "",
    ]
    return "\n".join(body)


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    research_record = (project_root / normalize_relpath(args.research_record)).resolve()
    if not research_record.exists():
        workspace_root = project_root.parent
        alternate = (workspace_root / normalize_relpath(args.research_record)).resolve()
        if alternate.exists():
            research_record = alternate

    if args.output:
        output_path = (project_root / normalize_relpath(args.output)).resolve()
    else:
        output_path = research_record.parent / "research_alignment_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status, lines = analyze_task(project_root, research_record)
    research_record_relpath = research_record.as_posix()
    try:
        research_record_relpath = research_record.relative_to(project_root).as_posix()
    except ValueError:
        pass
    output_path.write_text(
        render_report(research_record_relpath, status, lines),
        encoding="utf-8",
    )
    print(f"research_alignment_gate_status={status}")
    print(f"report_path={output_path.as_posix()}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
