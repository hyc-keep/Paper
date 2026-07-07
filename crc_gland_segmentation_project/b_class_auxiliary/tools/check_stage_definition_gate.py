"""Validate the stage definition card before Pre-check starts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


PLACEHOLDER_PATTERN = re.compile(
    r"^\[(?:路径|文件|章节|定位|原因|说明|结论|任务|阶段|动作|对象|约束|落点|命令).*\]$"
    r"|^xx_.*$|^xxx.*$|^\.\.\.$",
    re.IGNORECASE,
)
PATH_ANCHOR_PATTERN = re.compile(r"`([^`\n]*(?:/|\\|\.md|\.py|\.yaml|\.csv|\.txt)[^`\n]*)`")
VALID_STAGE_LOCK_RESULTS = {"allow_precheck", "blocked"}


@dataclass
class Issue:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the stage definition card before Pre-check."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--stage-card",
        required=True,
        help="Relative path to 00_阶段实现卡.md.",
    )
    parser.add_argument(
        "--output",
        default="",
        help=(
            "Optional relative path for the generated report. "
            "Defaults to the stage-card directory + stage_definition_gate_report.md."
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


def analyze_anchor_resolution(project_root: Path, doc_path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    anchors = [normalize_relpath(item) for item in PATH_ANCHOR_PATTERN.findall(text)]
    if not anchors:
        issues.append(Issue("partial", "阶段实现卡没有留下任何可解析路径锚点。"))
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
                f"阶段实现卡当前只留下 `{resolved_count}` 个可解析路径锚点，低于最小要求 `4`。",
            )
        )
    if missing:
        sample = "`, `".join(missing[:5])
        issues.append(
            Issue(
                "partial",
                f"阶段实现卡存在无法解析到真实文件的路径锚点: `{sample}`。",
            )
        )
    return issues


def analyze_task(project_root: Path, stage_card_path: Path) -> tuple[str, list[str]]:
    issues: list[Issue] = []
    if not stage_card_path.exists():
        return "fail", [f"- [fail] 阶段实现卡不存在: `{stage_card_path}`"]

    text = read_text(stage_card_path)
    if count_meaningful_lines(text) < 35:
        issues.append(Issue("partial", "阶段实现卡有效正文仍然过空，无法支撑阶段锁定。"))

    required_headings = (
        "## 1. 卡片角色与执行边界",
        "## 2. 本轮直接依赖的已读文件",
        "## 3. 当前阶段唯一目标",
        "## 4. 为什么现在做这个,而不是下一个阶段",
        "## 5. 当前阶段允许改动 / 禁止改动",
        "## 6. 论文依据 / 官方依据 / 代码依据",
        "## 7. 本轮工程落点",
        "## 8. 本轮最小运行验证计划",
        "## 9. 当前未决问题与阻断项",
        "## 10. 阶段锁定结论",
    )
    for heading in required_headings:
        if heading not in text:
            issues.append(Issue("fail", f"阶段实现卡缺少关键章节 `{heading}`。"))

    if any(issue.severity == "fail" for issue in issues):
        return "fail", [f"- [{issue.severity}] {issue.message}" for issue in issues]

    role_section = extract_level2_section(text, "## 1. 卡片角色与执行边界")
    for label in ("- 当前阶段:", "- 当前任务:", "- 本卡片只负责:", "- 本卡片不负责:"):
        if not has_substantive_value(extract_field_value(role_section, label)):
            issues.append(Issue("partial", f"阶段实现卡的 `{label}` 仍是空壳或占位内容。"))

    read_section = extract_level2_section(text, "## 2. 本轮直接依赖的已读文件")
    try:
        read_rows = extract_table_rows(text, "## 2. 本轮直接依赖的已读文件")
    except ValueError:
        read_rows = []
        issues.append(Issue("fail", "阶段实现卡缺少 `## 2. 本轮直接依赖的已读文件` 表格。"))
    if len(read_rows) < 3:
        issues.append(Issue("partial", "阶段实现卡已读文件表格过空，无法证明研究定标真的完成。"))
    for row in read_rows:
        for key in ("类型", "文件", "章节/定位", "为什么本轮必须读"):
            if not has_substantive_value(row.get(key, "")):
                issues.append(Issue("partial", f"已读文件表格字段 `{key}` 存在空壳或占位内容。"))
        if not any(token in row.get("文件", "") for token in ("结直肠腺体分割_plan_优化版", "结直肠腺体分割_正式参考资料", ".md", ".py")):
            issues.append(Issue("partial", f"已读文件 `{row.get('文件', '')}` 缺少明确来源路径痕迹。"))

    goal_section = extract_level2_section(text, "## 3. 当前阶段唯一目标")
    for label in ("- 用一句话说清:", "- 当前阶段进入条件:", "- 上一阶段已经交付:"):
        if not has_substantive_value(extract_field_value(goal_section, label)):
            issues.append(Issue("partial", f"`{label}` 尚未写清，阶段目标仍不够锁定。"))

    why_now_section = extract_level2_section(text, "## 4. 为什么现在做这个,而不是下一个阶段")
    for label in (
        "- 当前阶段必须先解决的阻断:",
        "- 如果现在提前做下一个阶段,会破坏什么:",
        "- 下一个阶段此刻还不允许进入的原因:",
    ):
        if not has_substantive_value(extract_field_value(why_now_section, label)):
            issues.append(Issue("partial", f"`{label}` 尚未写清，无法证明阶段边界真的锁住。"))

    boundary_section = extract_level2_section(text, "## 5. 当前阶段允许改动 / 禁止改动")
    for label in ("- 明确允许改:", "- 明确禁止改:", "- 如果越界,会破坏哪份正式协议:"):
        if not has_substantive_value(extract_field_value(boundary_section, label)):
            issues.append(Issue("partial", f"`{label}` 尚未写清，允许改/禁止改边界仍然过空。"))

    try:
        evidence_rows = extract_table_rows(text, "## 6. 论文依据 / 官方依据 / 代码依据")
    except ValueError:
        evidence_rows = []
        issues.append(Issue("fail", "阶段实现卡缺少 `## 6. 论文依据 / 官方依据 / 代码依据` 表格。"))
    evidence_types = {normalize_markdown_value(row.get("依据类型", "")) for row in evidence_rows}
    for required_type in ("论文依据", "官方依据", "代码依据"):
        if required_type not in evidence_types:
            issues.append(Issue("partial", f"阶段实现卡未完整覆盖 `{required_type}`。"))
    for row in evidence_rows:
        for key in ("来源", "章节/文件/commit", "提取出的硬约束", "本轮怎么落到代码"):
            if not has_substantive_value(row.get(key, "")):
                issues.append(Issue("partial", f"依据表字段 `{key}` 存在空壳或占位内容。"))

    try:
        landing_rows = extract_table_rows(text, "## 7. 本轮工程落点")
    except ValueError:
        landing_rows = []
        issues.append(Issue("fail", "阶段实现卡缺少 `## 7. 本轮工程落点` 表格。"))
    if len(landing_rows) < 2:
        issues.append(Issue("partial", "阶段实现卡工程落点表仍然过空。"))
    for row in landing_rows:
        for key in ("对象层", "允许动作", "预期落点", "为什么落这里"):
            if not has_substantive_value(row.get(key, "")):
                issues.append(Issue("partial", f"工程落点表字段 `{key}` 存在空壳或占位内容。"))

    try:
        verify_rows = extract_table_rows(text, "## 8. 本轮最小运行验证计划")
    except ValueError:
        verify_rows = []
        issues.append(Issue("fail", "阶段实现卡缺少 `## 8. 本轮最小运行验证计划` 表格。"))
    verify_items = {normalize_markdown_value(row.get("验证项", "")) for row in verify_rows}
    for required_item in ("import / py_compile", "smoke run", "dataloader batch", "loss / backward / optimizer.step"):
        if required_item not in verify_items:
            issues.append(Issue("partial", f"最小运行验证计划未覆盖 `{required_item}`。"))
    for row in verify_rows:
        for key in ("计划动作", "预期物理证据"):
            if not has_substantive_value(row.get(key, "")):
                issues.append(Issue("partial", f"最小运行验证计划字段 `{key}` 存在空壳或占位内容。"))

    unresolved_section = extract_level2_section(text, "## 9. 当前未决问题与阻断项")
    for label in ("- 当前仍未解决:", "- 如果这些问题不解,后续会卡在哪:", "- 本轮是否允许继续进入 Pre-check:"):
        if not has_substantive_value(extract_field_value(unresolved_section, label)):
            issues.append(Issue("partial", f"`{label}` 尚未写清，阻断项说明不完整。"))

    result_section = extract_level2_section(text, "## 10. 阶段锁定结论")
    stage_lock_result = normalize_markdown_value(extract_field_value(result_section, "- 阶段锁定状态:"))
    if stage_lock_result not in VALID_STAGE_LOCK_RESULTS:
        issues.append(
            Issue(
                "fail",
                f"`阶段锁定状态` 不在允许集合内: `{stage_lock_result}`。",
            )
        )
    if not has_substantive_value(extract_field_value(result_section, "- 结论说明:")):
        issues.append(Issue("partial", "`阶段锁定结论` 缺少结论说明。"))

    issues.extend(analyze_anchor_resolution(project_root, stage_card_path, text))

    detail_lines = [f"- [{issue.severity}] {issue.message}" for issue in issues]
    if any(issue.severity == "fail" for issue in issues):
        return "fail", detail_lines
    if any(issue.severity == "partial" for issue in issues):
        return "partial", detail_lines
    if stage_lock_result != "allow_precheck":
        return "fail", ["- [fail] 阶段实现卡正文完整，但 `阶段锁定状态` 不是 `allow_precheck`。"]
    return "pass", ["- [pass] 阶段实现卡的已读依据、边界、阶段原因、工程落点与最小运行验证计划检查通过。"]


def build_report(
    project_root: Path,
    stage_card: Path,
    status: str,
    details: Iterable[str],
) -> str:
    lines = [
        "# Stage Definition Gate Report",
        "",
        "## 1. 输入文件",
        f"- `project_root`: `{project_root}`",
        f"- `stage_card`: `{stage_card.relative_to(project_root).as_posix()}`",
        "",
        "## 2. 检查范围",
        "- 检查 `00_阶段实现卡.md` 是否覆盖角色边界、已读文件、阶段唯一目标、为什么不是下一个阶段、允许改/禁止改、依据、工程落点、最小运行验证计划、未决问题和阶段锁定结论。",
        "- 检查阶段实现卡里的表格字段是否仍是空壳或占位内容。",
        "- 检查阶段实现卡里的路径锚点是否能解析到真实存在的文件。",
        "- 检查阶段锁定状态是否已经明确裁成 `allow_precheck` 或 `blocked`。",
        "",
        "## 3. 结论",
        f"- `stage_definition_gate_status`: `{status}`",
        "",
        "## 4. 详细结果",
        *details,
        "",
    ]
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    stage_card = resolve_input_path(project_root, args.stage_card)
    if args.output:
        output_path = (project_root / normalize_relpath(args.output)).resolve()
    else:
        output_path = stage_card.parent / "stage_definition_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status, details = analyze_task(project_root, stage_card)
    output_path.write_text(
        build_report(project_root, stage_card, status, details),
        encoding="utf-8",
    )
    print(f"stage_definition_gate_status={status}")
    print(f"wrote_report={output_path}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
