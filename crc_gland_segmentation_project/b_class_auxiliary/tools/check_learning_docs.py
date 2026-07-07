"""Validate learning-doc coverage against Pre-check and Post-QC guard files."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Sequence


VALID_MAPPING_ACTIONS = {"create", "update", "append_version", "not_applicable"}
VALID_REVIEW_STATUSES = {"pass", "partial", "fail", "not_applicable"}
CORE_SCRIPT_DOC_MIN_LINES = 120
UTILITY_SCRIPT_DOC_MIN_LINES = 80
ASSET_DOC_MIN_LINES = 60
THIN_ASSET_DOC_MIN_LINES = 50
ACCEPTANCE_DOC_MIN_LINES = 80
ENTRY_DOC_MIN_LINES = 40
VERSION_RECORD_HEADING = "## 版本更新记录"
TRACEABILITY_CARD_HEADING = "## 结构化溯源卡片"
STAGE_TRACEABILITY_HEADING = "## 阶段协议回链卡片"
PROTOCOL_RESULTS_HEADING = "## 3. 协议级质检结果"
MANUAL_REVIEW_HEADING = "## 4.3 学习型说明文人工审稿回填"
TCGA_RAW_DOC_MARKER = "01_tcga_unet_project"
README_REQUIRED_SECTIONS = (
    "## 先看结论",
    "## 最推荐阅读顺序",
    "## 这一版和旧版最重要的区别",
    "## 你现在最该先搞明白的四件事",
)
IMPLEMENTATION_STATUS_REQUIRED_SECTIONS = (
    "## 当前状态",
    "## 为什么要重建这一组文档",
    "## 当前阅读入口",
    "## 当前最重要的诚实结论",
)
TRACEABILITY_KEYWORDS = {
    "理论来源": ("溯源锚点", "理论依据", "论文", "公式", "文献"),
    "代码来源": ("代码参考来源", "代码参考", "仓库", "当前实现", "参考行数"),
    "冻结回链": ("冻结表", "参数冻结总表", "冻结依据", "冻结表对应"),
}
PHYSICAL_EVIDENCE_KEYWORDS = {
    "路径": ("文件路径", "具体路径", "路径 `", "目录", "split_dir", "raw_root"),
    "字段": ("字段", "列", "csv_files", "dataset_name", "threshold_source"),
    "结果": ("当前真实结果", "实际结果", "关键指标", "数值", "样本数", "行数"),
}
VALIDATION_KEYWORDS = {
    "验证动作": ("检查方法", "验证", "如何验证", "如何手工验证", "检查什么"),
    "通过标准": ("通过标准", "期望结果", "判断正确", "检查结果"),
}
EXEMPLAR_SCRIPT_STYLE_GROUPS = {
    "类比导入": (r"你可以把它理解成", r"你可以先把它想成", r"你可以先记住这一句"),
    "提问引导": (r"你现在可能会问", r"你可能会问", r"你现在可能觉得"),
    "白话解释": (r"用人话说(?:就是)?", r"换句话说", r"说白了"),
    "取舍讨论": (r"为什么不用别的设计", r"为什么不用", r"为什么不选"),
    "联读收口": (r"建议联读", r"学完后你应该具备什么能力", r"5\s*分钟自检任务"),
}
EXPLANATION_STYLE_GROUPS = {
    "类比导入": (r"你可以把它理解成", r"你可以先把它想成"),
    "提问引导": (r"你现在可能会问", r"你可能会问", r"你现在可能觉得"),
    "白话解释": (r"用人话说(?:就是)?", r"换句话说", r"说白了"),
    "联读收口": (r"建议联读", r"下一步建议看", r"学完后你应该具备什么能力"),
}
ENTRY_STYLE_GROUPS = {
    "阅读引导": (r"你现在不用再", r"请直接按", r"如果你只想最快理解"),
    "白话解释": (r"当前最真实的(?:结论|说法)", r"真正已经", r"目前真正支持", r"说白了"),
    "诚实边界": (r"不指", r"不要误会", r"还没有", r"不冲突"),
}
ENTRY_RISK_PATTERNS = {
    "README.md": (r"不指", r"不要误会", r"不等于", r"不是"),
    "implementation_status.md": (r"还没有", r"不是所有", r"不冲突", r"诚实结论"),
}
ENTRY_CLOSING_PATTERNS = {
    "README.md": (r"后面进入", r"下一步", r"直接从 `01` 往下读"),
    "implementation_status.md": (r"最短路径", r"下一个阶段", r"请直接按编号"),
}
VISUAL_STRUCTURE_RULES = {
    "script": {"min_headings": 6, "min_short_paragraphs": 6, "min_numbered_steps": 3, "min_table_rows": 2},
    "asset": {"min_headings": 5, "min_short_paragraphs": 5, "min_numbered_steps": 2, "min_table_rows": 2},
    "acceptance": {"min_headings": 5, "min_short_paragraphs": 5, "min_numbered_steps": 2, "min_table_rows": 2},
    "entry": {"min_headings": 4, "min_short_paragraphs": 5, "min_numbered_steps": 3, "min_table_rows": 0},
}
MAX_PLAIN_PARAGRAPH_LINES = {
    "script": 10,
    "asset": 8,
    "acceptance": 8,
    "entry": 8,
}
SECTION_LEAD_REQUIREMENTS = {
    "script": 4,
    "asset": 3,
    "acceptance": 3,
    "entry": 3,
}
DOC_TYPE_DENSITY_RULES = {
    "script": {"traceability": 4, "physical": 4, "validation": 3},
    "asset": {"traceability": 2, "physical": 4, "validation": 2},
    "acceptance": {"traceability": 2, "physical": 4, "validation": 2},
    "entry": {"traceability": 1, "physical": 2, "validation": 2},
}
TRACEABILITY_CARD_FIELD_GROUPS = {
    "base": ("- 正式对象:", "- 对应阶段:"),
    "paper": ("- 论文:", "- 章节:", "- 公式/定义:"),
    "code": ("- 仓库:", "- 文件:", "- commit:", "- 许可证:"),
    "freeze": ("- 冻结文件:", "- 对应字段:"),
    "implementation": ("### 当前实现落点", "- 文件:", "- 符号:"),
}
FORMAL_RULE_BASENAMES = {
    "00_执行导航.md",
    "02_参数冻结总表.md",
    "03_命名与结果记录规范.md",
    "04_评估口径与官方脚本对齐.md",
    "05_代码工程映射与实现策略.md",
    "06_实验执行证据化写作模板.md",
    "07_实验执行全局修订与质检规范.md",
}
SOURCE_TRACEABILITY_REQUIRED_FIELDS = (
    "对应阶段",
    "理论依据",
    "代码参考",
    "本项目调整",
)
SOURCE_TRACEABILITY_CODE_MARKERS = ("仓库", "文件", "commit", "许可证")
SOURCE_TRACEABILITY_PAPER_MARKERS = ("论文", "章节", "公式", "定义")
STAGE_SEQUENCE = (
    "01_数据协议",
    "02_UNet流程验证",
    "03_UNet稳定性",
    "04_Baseline",
    "05_LKMA",
    "06_Boundary",
    "07_Distance",
    "08_外部对比",
    "09_CRAG验证",
    "10_结果汇总",
    "11_总验收与止损",
)
BACKTICK_PATH_PATTERN = re.compile(r"`([^`\n]*(?:/|\\|\.csv|\.yaml|\.md|\.py)[^`\n]*)`")
NUMERIC_EVIDENCE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\b")
PLACEHOLDER_PATTERN = re.compile(
    r"^\[(?:文件|路径|说明|描述|结果|字段|参数|章节|阶段|模块|函数|符号|对象|日期|任务|原因).*\]$"
    r"|^xx_.*$|^xxx.*$|^\.\.\.$",
    re.IGNORECASE,
)
QUESTION_RULES = {
    "script": {
        "定位": ("## 这个脚本的作用", "## 这个脚本在整个阶段中的位置"),
        "设计": ("为什么不用", "为什么不选", "为什么要这样设计", "候选方案", "最终决策"),
        "流程": ("## 脚本核心逻辑", "### 主要流程", "## 如何运行这个脚本"),
        "规则/原理": ("### 关键规则", "### 关键函数说明", "## 代码参考来源", TRACEABILITY_CARD_HEADING),
        "衔接": ("上游依赖", "下游消费者", "## 与项目其他部分的关联"),
        "误区": ("误区", "容易误解", "协议违规风险", "常见问题"),
        "自检": ("## 如何验证脚本运行结果", "5 分钟自检任务", "验证点"),
    },
    "asset": {
        "定位": ("这个文件是干什么的", "这个文件长什么样", "## 当前这个文件说明了什么"),
        "设计": ("为什么", "这个文件没说明什么", "局限性"),
        "流程": ("## 这张表/这个文件长什么样", "## 当前真实结果"),
        "规则/原理": ("## 这些列/字段分别是什么意思", "字段", "列"),
        "衔接": ("## 当前这个文件说明了什么", "对比", "上游", "下游"),
        "误区": ("## 常见问题", "容易误解", "误读"),
        "自检": ("## 如何手工验证这个文件的正确性", "验证步骤", "期望结果"),
    },
    "acceptance": {
        "定位": ("## 当前阶段通过的判定标准", "## 为什么现在能 pass"),
        "设计": ("为什么", "不影响放行", "为什么能pass"),
        "流程": ("## 当前阶段交付的正式资产清单", "## 下一步工作清单"),
        "规则/原理": ("验证方法", "判定结果", "通过标准"),
        "衔接": ("## 下游阶段的放行条件", "## 下一步工作清单"),
        "误区": ("不满足", "不适用", "回退", "风险"),
        "自检": ("## 当前阶段的物理验收证据", "验证命令", "检测方法"),
    },
    "generic": {
        "定位": ("作用", "位置", "职责"),
        "设计": ("为什么", "原因", "设计"),
        "流程": ("流程", "步骤"),
        "规则/原理": ("公式", "规则", "字段", "参数"),
        "衔接": ("上游", "下游", "依赖", "衔接"),
        "误区": ("误区", "注意", "不要"),
        "自检": ("验证", "检查", "通过标准"),
    },
}
SCRIPT_REQUIRED_SECTIONS = (
    TRACEABILITY_CARD_HEADING,
    "## 这个脚本的作用",
    "## 这个脚本在整个阶段中的位置",
    "## 当前实现状态",
    "## 脚本核心逻辑",
    "## 如何运行这个脚本",
    "## 如何验证脚本运行结果",
)
ASSET_REQUIRED_SECTION_GROUPS = (
    ("结构", ("## 这张表/这个文件长什么样", "## 当前真实结果")),
    ("解释", ("## 这些列/字段分别是什么意思",)),
    ("验证", ("## 如何手工验证这个文件的正确性", "## 如何验证")),
    ("误区", ("## 常见问题", "## 当前最该注意的一点")),
)
ACCEPTANCE_REQUIRED_SECTION_GROUPS = (
    ("结论", ("## 为什么现在能 pass", "## 当前阶段通过的判定标准")),
    ("证据", ("## 当前哪些证据最能支持 `pass`", "## 当前阶段的物理验收证据")),
    ("下一步", ("## 下一步应该怎么看", "## 下游阶段的放行条件", "## 下一步工作清单")),
)
AUTO_FORMAL_PREFIXES = (
    "src/",
    "scripts/",
    "configs/",
    "datasets/",
    "splits/",
    "experiments/",
    "external/",
    "reports/data_checks/",
    "reports/data_preview/",
    "reports/tables/",
    "reports/figures/",
)
CONDITIONAL_FORMAL_PREFIXES = (
    "tools/",
    "reports/stage_reports/",
)
IGNORE_PREFIXES = (
    ".trae/skills/",
    "b_class_auxiliary/",
    "reports/stage_reports/implementation_tracking/",
)


@dataclass
class ChangedFileRow:
    file_path: str
    action: str
    expected_status: str
    note: str


@dataclass
class MappingRow:
    object_path: str
    doc_path: str
    action: str
    note: str


@dataclass
class Issue:
    severity: str
    message: str


@dataclass
class DocStructureResult:
    issues: list[Issue]
    seven_question_hits: dict[str, bool]


@dataclass
class EvidenceResult:
    issues: list[Issue]
    traceability_hits: dict[str, bool]
    physical_hits: dict[str, bool]
    validation_hits: dict[str, bool]


@dataclass
class ProtocolResultRow:
    item: str
    result: str
    evidence: str


@dataclass
class ManualReviewRecord:
    present: bool
    checklist_path: str
    tcga_checklist_path: str
    exemplar_path: str
    review_objects: list[str]
    status: str
    pass_evidence: list[str]
    remaining_gaps: list[str]


@dataclass
class PrecheckContext:
    current_stage: str
    previous_stage: str
    current_stage_protocol_paths: set[str]
    previous_stage_acceptance_paths: set[str]
    route_lock_paths: set[str]
    formal_rule_paths: set[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate whether formal objects are properly linked to learning docs."
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
        "--post-qc-guard",
        required=True,
        help="Relative path to the task Post-QC Guard markdown file.",
    )
    parser.add_argument(
        "--output",
        default="",
        help=(
            "Optional relative path for the generated report. "
            "Defaults to the Post-QC guard directory + learning_doc_gate_report.md."
        ),
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def parse_changed_files(markdown_text: str) -> list[ChangedFileRow]:
    rows = extract_table_rows(markdown_text, "## 2. 实际创建/修改文件")
    changed_rows: list[ChangedFileRow] = []
    for row in rows:
        expected_status = ""
        if "是否符合预期" in row:
            expected_status = normalize_relpath(row["是否符合预期"])

        note_key = "备注" if "备注" in row else "说明" if "说明" in row else ""
        note = row[note_key].strip() if note_key else ""

        changed_rows.append(
            ChangedFileRow(
                file_path=normalize_relpath(row["文件"]),
                action=normalize_relpath(row["动作"]),
                expected_status=expected_status,
                note=note,
            )
        )
    return changed_rows


def parse_mapping_rows(markdown_text: str, heading: str) -> list[MappingRow]:
    rows = extract_table_rows(markdown_text, heading)
    object_key = "本轮变更对象"
    action_key = "计划动作" if "计划动作" in rows[0] else "实际动作"
    note_key = "备注" if "备注" in rows[0] else "结果"

    def resolve_doc_path(row: dict[str, str]) -> str:
        if "对象级说明文" in row:
            object_doc = normalize_relpath(row["对象级说明文"])
            if object_doc and object_doc not in {"-", "not_applicable"}:
                return object_doc
            entry_doc = normalize_relpath(row.get("入口同步项", ""))
            if (
                entry_doc
                and is_learning_doc_path(entry_doc)
                and Path(entry_doc).name in {"README.md", "implementation_status.md"}
            ):
                return entry_doc
            if entry_doc in {"README.md", "implementation_status.md"}:
                return entry_doc
            return object_doc or entry_doc
        return normalize_relpath(row["对应学习型说明文"])

    return [
        MappingRow(
            object_path=normalize_relpath(row[object_key]),
            doc_path=resolve_doc_path(row),
            action=normalize_relpath(row[action_key]),
            note=row[note_key].strip(),
        )
        for row in rows
    ]


def normalize_stage_name(value: str) -> str:
    normalized = normalize_relpath(value)
    match = re.search(r"(0[1-9]|1[0-1])_[^/\\`]+", normalized)
    return match.group(0) if match else normalized


def extract_stage_value(markdown_text: str, headings: Sequence[str], labels: Sequence[str]) -> str:
    for heading in headings:
        section = extract_level2_section(markdown_text, heading)
        if not section:
            continue
        for label in labels:
            value = normalize_stage_name(extract_field_value(section, label))
            if value:
                return value
    return ""


def resolved_anchor_map(project_root: Path, doc_path: Path, text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for anchor in extract_backtick_paths(text):
        normalized = normalize_relpath(anchor)
        if not normalized or normalized in mapping:
            continue
        resolved = resolve_anchor_path(project_root, doc_path, normalized)
        if resolved is not None:
            mapping[normalized] = resolved.as_posix().lower()
    return mapping


def extract_stage_anchor_paths(
    project_root: Path,
    doc_path: Path,
    text: str,
    target_stage: str,
    suffix_keywords: Sequence[str],
) -> set[str]:
    if not target_stage:
        return set()
    resolved_paths: set[str] = set()
    for _, resolved in resolved_anchor_map(project_root, doc_path, text).items():
        if "/01_实验执行/" not in resolved:
            continue
        if f"/01_实验执行/{target_stage.lower()}/" not in resolved:
            continue
        basename = Path(resolved).name
        if any(keyword in basename for keyword in suffix_keywords):
            resolved_paths.add(resolved)
    return resolved_paths


def extract_filtered_anchor_paths(
    project_root: Path,
    doc_path: Path,
    text: str,
    include_predicate,
) -> set[str]:
    resolved_paths: set[str] = set()
    for _, resolved in resolved_anchor_map(project_root, doc_path, text).items():
        if include_predicate(resolved):
            resolved_paths.add(resolved)
    return resolved_paths


def build_precheck_context(
    project_root: Path,
    precheck_guard_path: Path,
    precheck_text: str,
    stage_gate_text: str,
    extraction_text: str,
) -> PrecheckContext:
    current_stage = extract_stage_value(
        precheck_text,
        ("## 1. 本次任务归属",),
        ("- 当前阶段:",),
    ) or extract_stage_value(
        stage_gate_text,
        ("## 1. 阶段信息",),
        ("- 当前阶段:",),
    ) or extract_stage_value(
        extraction_text,
        ("## 1. 本次任务",),
        ("- 当前阶段:",),
    )
    previous_stage = extract_stage_value(
        precheck_text,
        ("## 1. 本次任务归属",),
        ("- 上一阶段:",),
    ) or extract_stage_value(
        stage_gate_text,
        ("## 1. 阶段信息",),
        ("- 上一阶段:",),
    ) or extract_stage_value(
        extraction_text,
        ("## 1. 本次任务",),
        ("- 上一阶段:",),
    )

    combined_stage_text = "\n".join((precheck_text, stage_gate_text))
    current_stage_protocol_paths = extract_stage_anchor_paths(
        project_root,
        precheck_guard_path,
        combined_stage_text,
        current_stage,
        ("00_阶段总协议.md",),
    )
    previous_stage_acceptance_paths = extract_stage_anchor_paths(
        project_root,
        precheck_guard_path,
        combined_stage_text,
        previous_stage,
        ("阶段验收",),
    )
    route_lock_paths = extract_filtered_anchor_paths(
        project_root,
        precheck_guard_path,
        "\n".join((precheck_text, extraction_text)),
        lambda resolved: "/02_路线与投稿/" in resolved,
    )
    formal_rule_paths = extract_filtered_anchor_paths(
        project_root,
        precheck_guard_path,
        "\n".join((precheck_text, extraction_text)),
        lambda resolved: Path(resolved).name in FORMAL_RULE_BASENAMES,
    )
    return PrecheckContext(
        current_stage=current_stage,
        previous_stage=previous_stage,
        current_stage_protocol_paths=current_stage_protocol_paths,
        previous_stage_acceptance_paths=previous_stage_acceptance_paths,
        route_lock_paths=route_lock_paths,
        formal_rule_paths=formal_rule_paths,
    )


def parse_protocol_results(markdown_text: str) -> dict[str, ProtocolResultRow]:
    rows = extract_table_rows(markdown_text, PROTOCOL_RESULTS_HEADING)
    result: dict[str, ProtocolResultRow] = {}
    for row in rows:
        item = row["检查项"].strip()
        result[item] = ProtocolResultRow(
            item=item,
            result=normalize_relpath(row["结果"]),
            evidence=row["物理证据"].strip(),
        )
    return result


def try_parse_protocol_results(markdown_text: str) -> tuple[dict[str, ProtocolResultRow], bool]:
    try:
        return parse_protocol_results(markdown_text), True
    except ValueError:
        return {}, False


def extract_level2_or_3_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|^###\s|\Z)"
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_bullet_block(section: str, label: str) -> str:
    pattern = re.compile(
        rf"(?ms)^- {re.escape(label)}:\s*(.*?)(?=^- [^\n]+:|\Z)"
    )
    match = pattern.search(section)
    return match.group(1).strip() if match else ""


def extract_first_value_from_block(block: str) -> str:
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        return line
    return ""


def extract_list_from_block(block: str) -> list[str]:
    values: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        values.append(line)
    return values


def parse_manual_review_record(markdown_text: str) -> ManualReviewRecord:
    section = extract_level2_or_3_section(markdown_text, MANUAL_REVIEW_HEADING)
    if not section:
        return ManualReviewRecord(
            present=False,
            checklist_path="",
            tcga_checklist_path="",
            exemplar_path="",
            review_objects=[],
            status="",
            pass_evidence=[],
            remaining_gaps=[],
        )

    return ManualReviewRecord(
        present=True,
        checklist_path=normalize_relpath(
            extract_first_value_from_block(extract_bullet_block(section, "审稿清单"))
        ),
        tcga_checklist_path=normalize_relpath(
            extract_first_value_from_block(extract_bullet_block(section, "TCGA原始标杆清单"))
        ),
        exemplar_path=normalize_relpath(
            extract_first_value_from_block(extract_bullet_block(section, "对照示范稿"))
        ),
        review_objects=[
            normalize_relpath(value)
            for value in extract_list_from_block(extract_bullet_block(section, "审稿对象"))
        ],
        status=normalize_relpath(
            extract_first_value_from_block(extract_bullet_block(section, "审稿结论"))
        ),
        pass_evidence=extract_list_from_block(
            extract_bullet_block(section, "本轮最关键的通过证据")
        ),
        remaining_gaps=extract_list_from_block(
            extract_bullet_block(section, "本轮仍需补强的问题")
        ),
    )


def try_parse_mapping_rows(markdown_text: str, heading: str) -> tuple[list[MappingRow], bool]:
    try:
        return parse_mapping_rows(markdown_text, heading), True
    except ValueError:
        return [], False


def is_guard_or_learning_doc(rel_path: str) -> bool:
    return rel_path.startswith(IGNORE_PREFIXES)


def is_formal_object_candidate(rel_path: str) -> bool:
    if not rel_path or "*" in rel_path:
        return False
    if is_guard_or_learning_doc(rel_path):
        return False
    return rel_path.startswith(AUTO_FORMAL_PREFIXES)


def is_conditional_formal_object_candidate(rel_path: str) -> bool:
    if not rel_path or "*" in rel_path:
        return False
    if is_guard_or_learning_doc(rel_path):
        return False
    return rel_path.startswith(CONDITIONAL_FORMAL_PREFIXES)


def is_learning_doc_path(rel_path: str) -> bool:
    return rel_path.startswith("reports/stage_reports/implementation_tracking/")


def is_object_learning_doc_name(file_name: str) -> bool:
    lowered = file_name.lower()
    if lowered in {"readme.md", "implementation_status.md"}:
        return False
    if "为什么能pass" in file_name:
        return False
    return lowered.endswith(
        (".py.md", ".yaml.md", ".yml.md", ".csv.md", ".png.md", ".jpg.md", ".jpeg.md", ".bmp.md", ".md.md")
    )


def is_changed_in_post_qc(rel_path: str, changed_paths: set[str]) -> bool:
    return rel_path in changed_paths


def stage_root_for_learning_doc(rel_path: str) -> str:
    normalized = normalize_relpath(rel_path)
    parts = normalized.split("/")
    if parts[:3] != ["reports", "stage_reports", "implementation_tracking"]:
        return ""
    if len(parts) < 4:
        return ""
    return "/".join(parts[:4])


def contains_version_record(text: str) -> bool:
    return VERSION_RECORD_HEADING in text


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


def count_heading_lines(text: str) -> int:
    return sum(
        1
        for raw_line in text.splitlines()
        if raw_line.lstrip().startswith(("## ", "### ", "#### "))
    )


def count_table_rows(text: str) -> int:
    return sum(1 for raw_line in text.splitlines() if raw_line.strip().startswith("|"))


def count_numbered_steps(text: str) -> int:
    return sum(1 for raw_line in text.splitlines() if re.match(r"^\s*\d+\.\s", raw_line))


def collect_plain_paragraphs(text: str) -> list[list[str]]:
    paragraphs: list[list[str]] = []
    current: list[str] = []
    in_code_block = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            if current:
                paragraphs.append(current)
                current = []
            continue
        if in_code_block:
            continue
        if not stripped:
            if current:
                paragraphs.append(current)
                current = []
            continue
        if stripped.startswith(("#", "|", "-", "*")) or re.match(r"^\d+\.\s", stripped):
            if current:
                paragraphs.append(current)
                current = []
            continue
        current.append(stripped)
    if current:
        paragraphs.append(current)
    return paragraphs


def count_short_paragraphs(text: str) -> int:
    paragraphs = collect_plain_paragraphs(text)
    return sum(1 for paragraph in paragraphs if 1 <= len(paragraph) <= 3)


def contains_any_keyword(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def contains_any_pattern(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def count_pattern_group_hits(text: str, pattern_groups: dict[str, Iterable[str]]) -> dict[str, bool]:
    return {
        group_name: contains_any_pattern(text, patterns)
        for group_name, patterns in pattern_groups.items()
    }


def max_plain_paragraph_length(text: str) -> int:
    paragraphs = collect_plain_paragraphs(text)
    if not paragraphs:
        return 0
    return max(len(paragraph) for paragraph in paragraphs)


def count_sections_with_lead_signal(text: str) -> int:
    pattern = re.compile(r"(?ms)^(##\s.+?|###\s.+?)\s*$\n(.*?)(?=^(?:##|###)\s|\Z)")
    count = 0
    for _, body in pattern.findall(text):
        in_code_block = False
        for raw_line in body.splitlines():
            stripped = raw_line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block or not stripped:
                continue
            if stripped.startswith("|"):
                continue
            if stripped.startswith(("-", "*", ">")) or re.match(r"^\d+\.\s", stripped):
                count += 1
                break
            if len(stripped) <= 80:
                count += 1
            break
    return count


def analyze_visual_structure(doc_path: str, doc_text: str, doc_type: str) -> list[Issue]:
    issues: list[Issue] = []
    rule = VISUAL_STRUCTURE_RULES[doc_type]
    heading_count = count_heading_lines(doc_text)
    short_paragraph_count = count_short_paragraphs(doc_text)
    numbered_step_count = count_numbered_steps(doc_text)
    table_row_count = count_table_rows(doc_text)
    longest_plain_paragraph = max_plain_paragraph_length(doc_text)
    lead_signal_sections = count_sections_with_lead_signal(doc_text)

    if heading_count < rule["min_headings"]:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 的标题层次不足，当前只识别到 `{heading_count}` 个二级/三级标题，"
                f"低于 `{rule['min_headings']}`，阅读引导容易退化成长段正文。",
            )
        )
    if short_paragraph_count < rule["min_short_paragraphs"]:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 的短段落数量不足，当前只识别到 `{short_paragraph_count}` 段，"
                f"低于 `{rule['min_short_paragraphs']}`，视觉留白和结论先行节奏偏弱。",
            )
        )
    if numbered_step_count < rule["min_numbered_steps"] and table_row_count < rule["min_table_rows"]:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少稳定的结构化阅读信号：当前编号链为 `{numbered_step_count}` 条、"
                f"表格行为 `{table_row_count}` 行，未达到最小要求（编号链 `{rule['min_numbered_steps']}` 或表格 `{rule['min_table_rows']}`）。",
            )
        )
    max_allowed_plain_lines = MAX_PLAIN_PARAGRAPH_LINES[doc_type]
    if longest_plain_paragraph > max_allowed_plain_lines:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 的最长连续纯正文达到 `{longest_plain_paragraph}` 行，"
                f"超过建议上限 `{max_allowed_plain_lines}`，视觉对比不足，容易退化成密集长段。",
            )
        )
    required_lead_sections = SECTION_LEAD_REQUIREMENTS[doc_type]
    if lead_signal_sections < required_lead_sections:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 只有 `{lead_signal_sections}` 个章节在开头先给出短结论或总结 bullet，"
                f"低于要求 `{required_lead_sections}`，结论先行信号偏弱。",
            )
        )
    return issues


def count_keyword_hits(text: str, keywords: Iterable[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def heading_exists(text: str, heading: str) -> bool:
    return heading in text


def expected_min_lines(doc_path: str, object_path: str) -> int | None:
    file_name = Path(doc_path).name
    object_suffix = Path(object_path).suffix.lower()

    if file_name in {"README.md", "implementation_status.md"}:
        return ENTRY_DOC_MIN_LINES
    if "为什么能pass" in file_name:
        return ACCEPTANCE_DOC_MIN_LINES
    if object_suffix == ".py" or file_name.lower().endswith(".py.md"):
        if object_path.startswith("tools/"):
            return UTILITY_SCRIPT_DOC_MIN_LINES
        return CORE_SCRIPT_DOC_MIN_LINES
    if object_suffix in {".yaml", ".yml"}:
        return THIN_ASSET_DOC_MIN_LINES
    if is_object_learning_doc_name(file_name):
        return ASSET_DOC_MIN_LINES
    return None


def classify_doc_type(doc_path: str, object_path: str) -> str:
    file_name = Path(doc_path).name
    object_suffix = Path(object_path).suffix.lower()
    if file_name in {"README.md", "implementation_status.md"}:
        return "entry"
    if "为什么能pass" in file_name:
        return "acceptance"
    if object_suffix == ".py" or file_name.lower().endswith(".py.md"):
        return "script"
    if is_object_learning_doc_name(file_name):
        return "asset"
    return "generic"


def has_all_keywords(text: str, keywords: Iterable[str]) -> bool:
    return all(keyword in text for keyword in keywords)


def extract_level2_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)"
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_level3_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^{re.escape(heading)}\s*$\n(.*?)(?=^###\s|^##\s|\Z)"
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def extract_field_value(section: str, label: str) -> str:
    match = re.search(rf"(?m)^{re.escape(label)}\s*(.+)$", section)
    return match.group(1).strip() if match else ""


def normalize_markdown_value(value: str) -> str:
    normalized = value.strip().strip("`")
    normalized = re.sub(r"^[>\-\*\d\.\)\s]+", "", normalized).strip()
    return normalized
 
 
def is_placeholder_value(value: str) -> bool:
    normalized = normalize_markdown_value(value)
    if not normalized:
        return True
    if PLACEHOLDER_PATTERN.match(normalized):
        return True
    return normalized.startswith("<") and normalized.endswith(">")


def extract_backtick_paths(text: str) -> list[str]:
    return [normalize_relpath(match) for match in BACKTICK_PATH_PATTERN.findall(text)]


def find_first_section_text(text: str, headings: Sequence[str]) -> str:
    for heading in headings:
        section = extract_level2_section(text, heading)
        if section:
            return section
    return ""


def has_substantive_content(text: str, minimum_lines: int = 2) -> bool:
    if count_meaningful_lines(text) < minimum_lines:
        return False
    for raw_line in text.splitlines():
        line = normalize_markdown_value(raw_line)
        if not line:
            continue
        if line.startswith(("## ", "### ")):
            continue
        if re.fullmatch(r"[-|:\s]+", line):
            continue
        if not is_placeholder_value(line):
            return True
    return False


def validate_substantive_sections(
    doc_path: str,
    doc_text: str,
    section_rules: Sequence[tuple[str, Sequence[str], int]],
) -> list[Issue]:
    issues: list[Issue] = []
    for label, headings, minimum_lines in section_rules:
        section_text = find_first_section_text(doc_text, headings)
        if not section_text:
            continue
        if not has_substantive_content(section_text, minimum_lines):
            joined = " / ".join(headings)
            issues.append(
                Issue(
                    "partial",
                    f"说明文 `{doc_path}` 的 `{label}` 章节命中了标题 `{joined}`，"
                    "但正文仍然过空、过短或以占位内容为主。",
                )
            )
    return issues


def parse_version_record_rows(doc_text: str) -> list[dict[str, str]]:
    return extract_table_rows(doc_text, VERSION_RECORD_HEADING)


def has_complete_version_record(doc_text: str) -> bool:
    try:
        rows = parse_version_record_rows(doc_text)
    except ValueError:
        return False
    if not rows:
        return False

    required_fields = ("日期", "改动内容", "影响范围", "是否需要重新验证")
    latest = rows[-1]
    if any(field not in latest for field in required_fields):
        return False
    return all(not is_placeholder_value(latest[field]) for field in required_fields)


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
        candidates.append(project_root.parent / candidate_text)
        candidates.append(doc_path.parent / candidate_text)

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate.resolve()
    return None


def collect_resolved_anchors(project_root: Path, doc_fs_path: Path, text: str) -> tuple[list[str], list[str]]:
    anchors = extract_backtick_paths(text)
    resolved: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()
    for anchor in anchors:
        normalized = normalize_relpath(anchor)
        if normalized in seen or should_skip_anchor(normalized):
            continue
        seen.add(normalized)
        if resolve_anchor_path(project_root, doc_fs_path, normalized) is not None:
            resolved.append(normalized)
        else:
            missing.append(normalized)
    return resolved, missing


def doc_mentions_object(doc_text: str, object_path: str) -> bool:
    normalized = normalize_relpath(object_path)
    basename = Path(normalized).name
    return normalized in doc_text or basename in doc_text


def manual_review_required(
    post_rows: Sequence[MappingRow],
    changed_row_map: dict[str, ChangedFileRow],
) -> bool:
    for row in post_rows:
        if row.action == "not_applicable" or not is_learning_doc_path(row.doc_path):
            continue
        doc_name = Path(row.doc_path).name
        doc_change = changed_row_map.get(row.doc_path)
        if row.action == "create":
            return True
        if doc_change and doc_change.action == "create":
            return True
        if doc_name in {"README.md", "implementation_status.md"} and row.action in {"create", "update"}:
            return True
        if "为什么能pass" in doc_name and row.action in {"create", "update"}:
            return True
        if is_object_learning_doc_name(doc_name) and row.action == "update":
            return True
    return False


def analyze_manual_review(
    project_root: Path,
    post_qc_guard_path: Path,
    post_qc_text: str,
    post_rows: Sequence[MappingRow],
    changed_row_map: dict[str, ChangedFileRow],
) -> list[Issue]:
    issues: list[Issue] = []
    protocol_results, has_protocol_results = try_parse_protocol_results(post_qc_text)
    manual_protocol = protocol_results.get("学习型说明文人工审稿")
    learning_doc_protocol = protocol_results.get("学习型说明文门禁")
    manual_record = parse_manual_review_record(post_qc_text)
    review_is_required = manual_review_required(post_rows, changed_row_map)

    if not has_protocol_results:
        if review_is_required:
            issues.append(
                Issue(
                    "fail",
                    f"Post-QC Guard 缺少 `{PROTOCOL_RESULTS_HEADING}`，"
                    "无法核对人工审稿与协议级质检结果是否一致。",
                )
            )
        return issues

    if manual_protocol is None:
        if review_is_required:
            issues.append(
                Issue(
                    "fail",
                    "Post-QC Guard 的协议级质检结果缺少 `学习型说明文人工审稿` 行，"
                    "无法判断人工终审是否已经正式执行。",
                )
            )
        return issues

    if manual_protocol.result not in VALID_REVIEW_STATUSES:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 的 `学习型说明文人工审稿` 结果不在允许集合 "
                f"`{sorted(VALID_REVIEW_STATUSES)}` 内: `{manual_protocol.result}`。",
            )
        )

    if not manual_record.present:
        if review_is_required:
            issues.append(
                Issue(
                    "fail",
                    f"本轮已触发人工终审条件，但 Post-QC Guard 缺少 `{MANUAL_REVIEW_HEADING}`。",
                )
            )
        return issues

    if manual_record.status not in VALID_REVIEW_STATUSES:
        issues.append(
            Issue(
                "fail",
                f"`{MANUAL_REVIEW_HEADING}` 的 `审稿结论` 不在允许集合 "
                f"`{sorted(VALID_REVIEW_STATUSES)}` 内: `{manual_record.status}`。",
            )
        )
    elif manual_protocol.result and manual_protocol.result != manual_record.status:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 的协议级质检表与 `4.3` 人工审稿回填结论不一致: "
                f"`{manual_protocol.result}` vs `{manual_record.status}`。",
            )
        )

    if review_is_required and manual_record.status == "not_applicable":
        issues.append(
            Issue(
                "fail",
                "本轮已经新建或重写学习型说明文主体，但人工审稿仍回填为 `not_applicable`。",
            )
        )

    if manual_record.checklist_path:
        checklist_resolved = resolve_anchor_path(project_root, post_qc_guard_path, manual_record.checklist_path)
        if checklist_resolved is None:
            issues.append(
                Issue(
                    "fail",
                    f"`4.3` 的审稿清单路径不存在: `{manual_record.checklist_path}`。",
                )
            )
    elif manual_record.status != "not_applicable":
        issues.append(Issue("fail", "`4.3` 缺少 `审稿清单` 路径。"))

    if manual_record.tcga_checklist_path:
        tcga_checklist_resolved = resolve_anchor_path(
            project_root,
            post_qc_guard_path,
            manual_record.tcga_checklist_path,
        )
        if tcga_checklist_resolved is None:
            issues.append(
                Issue(
                    "fail",
                    f"`4.3` 的 TCGA 原始标杆清单路径不存在: `{manual_record.tcga_checklist_path}`。",
                )
            )
    elif manual_record.status != "not_applicable":
        issues.append(Issue("fail", "`4.3` 缺少 `TCGA原始标杆清单` 路径。"))

    if manual_record.exemplar_path:
        exemplar_resolved = resolve_anchor_path(project_root, post_qc_guard_path, manual_record.exemplar_path)
        if exemplar_resolved is None:
            issues.append(
                Issue(
                    "partial",
                    f"`4.3` 的对照示范稿路径不存在: `{manual_record.exemplar_path}`。",
                )
            )
    elif manual_record.status != "not_applicable":
        issues.append(Issue("partial", "`4.3` 缺少 `对照示范稿` 路径。"))

    if manual_record.status == "not_applicable":
        if not manual_record.remaining_gaps:
            issues.append(
                Issue(
                    "partial",
                    "`4.3` 把人工审稿标为 `not_applicable`，但没有写清不适用原因。",
                )
            )
        return issues

    if not manual_record.review_objects:
        issues.append(Issue("fail", "`4.3` 缺少 `审稿对象` 列表。"))
    else:
        for review_object in manual_record.review_objects:
            resolved = resolve_anchor_path(project_root, post_qc_guard_path, review_object)
            if resolved is None:
                issues.append(
                    Issue(
                        "fail",
                        f"`4.3` 的审稿对象路径不存在: `{review_object}`。",
                    )
                )
                continue
            normalized_object = normalize_relpath(review_object)
            if not is_learning_doc_path(normalized_object):
                issues.append(
                    Issue(
                        "fail",
                        f"`4.3` 的审稿对象不在 `implementation_tracking` 下: `{review_object}`。",
                    )
                )

    if not manual_record.pass_evidence:
        issues.append(Issue("fail", "`4.3` 缺少 `本轮最关键的通过证据`。"))
    elif all(is_placeholder_value(value) for value in manual_record.pass_evidence):
        issues.append(
            Issue(
                "fail",
                "`4.3` 的通过证据仍然是占位内容，没有真实章节/表述/物理证据。",
            )
        )

    if not manual_record.remaining_gaps:
        issues.append(Issue("partial", "`4.3` 缺少 `本轮仍需补强的问题`。"))
    elif all(is_placeholder_value(value) for value in manual_record.remaining_gaps):
        issues.append(
            Issue(
                "partial",
                "`4.3` 的补强问题仍然是占位内容，没有诚实记录剩余短板或不适用原因。",
            )
        )

    tcga_raw_paths = [
        anchor
        for anchor in extract_backtick_paths(extract_level2_or_3_section(post_qc_text, MANUAL_REVIEW_HEADING))
        if TCGA_RAW_DOC_MARKER in anchor
    ]
    unique_tcga_raw_paths = list(dict.fromkeys(tcga_raw_paths))
    if len(unique_tcga_raw_paths) < 2:
        issues.append(
            Issue(
                "fail",
                "`4.3` 没有明确回填至少 2 份真实 TCGA 原始学习说明文路径，"
                "无法证明已经对齐用户指定的原始标杆。",
            )
        )

    if manual_record.status in {"partial", "fail"}:
        issues.append(
            Issue(
                "partial",
                f"人工审稿结论为 `{manual_record.status}`，本轮学习型说明文门禁不能返回 `pass`。",
            )
        )
    if (
        manual_record.status == "pass"
        and learning_doc_protocol is not None
        and learning_doc_protocol.result in {"partial", "fail"}
    ):
        issues.append(
            Issue(
                "partial",
                "人工审稿回填为 `pass`，但协议级质检中的 `学习型说明文门禁` 仍未通过，"
                "请确认自动门禁与人工终审结论是否冲突。",
            )
        )

    return issues


def analyze_seven_questions(doc_text: str, doc_type: str) -> dict[str, bool]:
    rules = QUESTION_RULES.get(doc_type, QUESTION_RULES["generic"])
    return {
        question: contains_any_keyword(doc_text, markers)
        for question, markers in rules.items()
    }


def analyze_traceability_card(
    project_root: Path,
    doc_path: str,
    object_path: str,
    doc_text: str,
) -> list[Issue]:
    doc_type = classify_doc_type(doc_path, object_path)
    if doc_type != "script":
        return []

    issues: list[Issue] = []
    if TRACEABILITY_CARD_HEADING not in doc_text:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 缺少 `{TRACEABILITY_CARD_HEADING}`。",
            )
        )
        return issues

    section = extract_level2_section(doc_text, TRACEABILITY_CARD_HEADING)
    if not section:
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的溯源卡片内容为空。"))
        return issues

    paper_section = extract_level3_section(section, "### 论文依据")
    code_section = extract_level3_section(section, "### 代码依据")
    freeze_section = extract_level3_section(section, "### 冻结回链")
    implementation_section = extract_level3_section(section, "### 当前实现落点")

    if not has_all_keywords(section, TRACEABILITY_CARD_FIELD_GROUPS["base"]):
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的溯源卡片缺少基础字段（正式对象 / 对应阶段）。",
            )
        )
    if not has_all_keywords(section, TRACEABILITY_CARD_FIELD_GROUPS["freeze"]):
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的溯源卡片缺少冻结回链字段。",
            )
        )
    if not has_all_keywords(section, TRACEABILITY_CARD_FIELD_GROUPS["implementation"]):
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的溯源卡片缺少当前实现落点字段。",
            )
        )

    doc_fs_path = project_root / doc_path
    object_value = extract_field_value(section, "- 正式对象:")
    freeze_value = extract_field_value(freeze_section, "- 冻结文件:")
    impl_file_value = extract_field_value(implementation_section, "- 文件:")
    symbol_value = extract_field_value(implementation_section, "- 符号:")
    field_value = extract_field_value(freeze_section, "- 对应字段:")
    chapter_value = extract_field_value(paper_section, "- 章节:")
    formula_value = extract_field_value(paper_section, "- 公式/定义:")
    code_file_value = extract_field_value(code_section, "- 文件:")
    commit_value = extract_field_value(code_section, "- commit:")
    license_value = extract_field_value(code_section, "- 许可证:")

    if is_placeholder_value(object_value):
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的 `正式对象` 仍是占位值。"))
    elif Path(normalize_relpath(object_value)).name != Path(normalize_relpath(object_path)).name:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的 `正式对象` 与映射对象 `{object_path}` 不一致。",
            )
        )
    elif resolve_anchor_path(project_root, doc_fs_path, object_value) is None:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的 `正式对象` 路径不存在: `{object_value}`。",
            )
        )

    if is_placeholder_value(freeze_value):
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的 `冻结文件` 仍是占位值。"))
    elif resolve_anchor_path(project_root, doc_fs_path, freeze_value) is None:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的 `冻结文件` 路径不存在: `{freeze_value}`。",
            )
        )

    if is_placeholder_value(impl_file_value):
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的 `当前实现落点 -> 文件` 仍是占位值。"))
    elif resolve_anchor_path(project_root, doc_fs_path, impl_file_value) is None:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的 `当前实现落点 -> 文件` 路径不存在: `{impl_file_value}`。",
            )
        )

    if is_placeholder_value(symbol_value):
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的 `当前实现落点 -> 符号` 仍是占位值。"))
    if is_placeholder_value(field_value):
        issues.append(Issue("partial", f"脚本说明文 `{doc_path}` 的 `冻结回链 -> 对应字段` 仍是占位值。"))

    paper_complete = has_all_keywords(section, TRACEABILITY_CARD_FIELD_GROUPS["paper"])
    code_complete = has_all_keywords(section, TRACEABILITY_CARD_FIELD_GROUPS["code"])
    if not (paper_complete or code_complete):
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的溯源卡片缺少完整来源组（论文依据或代码依据至少要完整命中一组）。",
            )
        )
    if paper_complete and (is_placeholder_value(chapter_value) or is_placeholder_value(formula_value)):
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 的论文依据组仍存在占位值（章节/公式）。",
            )
        )
    if code_complete:
        if is_placeholder_value(code_file_value):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 的代码依据组 `文件` 仍是占位值。",
                )
            )
        elif resolve_anchor_path(project_root, doc_fs_path, code_file_value) is None:
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 的代码依据文件路径不存在: `{code_file_value}`。",
                )
            )
        if is_placeholder_value(commit_value):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 的代码依据组 `commit` 仍是占位值。",
                )
            )
        if is_placeholder_value(license_value):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 的代码依据组 `许可证` 仍是占位值。",
                )
            )

    return issues


def analyze_anchor_evidence(
    project_root: Path,
    doc_path: str,
    object_path: str,
    doc_text: str,
) -> list[Issue]:
    doc_fs_path = project_root / doc_path
    resolved, missing = collect_resolved_anchors(project_root, doc_fs_path, doc_text)

    issues: list[Issue] = []
    doc_type = classify_doc_type(doc_path, object_path)
    minimum_existing = {"script": 2, "asset": 2, "acceptance": 2}.get(doc_type, 1)
    if len(resolved) < minimum_existing:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 的真实存在路径锚点数为 `{len(resolved)}`，低于最小要求 `{minimum_existing}`。",
            )
        )
    if missing:
        sample = "`, `".join(missing[:5])
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 存在无法解析到真实文件的路径锚点: `{sample}`。",
            )
        )
    if doc_type in {"script", "asset"} and not doc_mentions_object(doc_text, object_path):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 没有显式回链本轮对象 `{object_path}`。",
            )
        )
    if doc_type in {"script", "asset", "acceptance"} and not NUMERIC_EVIDENCE_PATTERN.search(doc_text):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少数值级物理证据（未识别到行数/字段值/指标数值）。",
            )
        )
    return issues


def extract_stage_name_from_learning_doc(doc_path: str) -> str:
    parts = normalize_relpath(doc_path).split("/")
    if len(parts) >= 5 and parts[:3] == ["reports", "stage_reports", "implementation_tracking"]:
        return parts[3]
    return ""


def analyze_stage_protocol_traceability(
    project_root: Path,
    doc_path: str,
    object_path: str,
    doc_text: str,
    precheck_context: PrecheckContext,
) -> list[Issue]:
    doc_type = classify_doc_type(doc_path, object_path)
    if doc_type not in {"script", "asset", "acceptance"}:
        return []

    doc_fs_path = project_root / doc_path
    require_previous_stage = bool(precheck_context.previous_stage) and (
        precheck_context.current_stage != STAGE_SEQUENCE[0]
    )
    resolved_doc_paths = set(resolved_anchor_map(project_root, doc_fs_path, doc_text).values())
    current_stage_protocol = bool(
        resolved_doc_paths & precheck_context.current_stage_protocol_paths
    ) if precheck_context.current_stage_protocol_paths else False
    previous_stage_acceptance = bool(
        resolved_doc_paths & precheck_context.previous_stage_acceptance_paths
    ) if precheck_context.previous_stage_acceptance_paths else False
    route_lock = bool(resolved_doc_paths & precheck_context.route_lock_paths) if precheck_context.route_lock_paths else False
    formal_rule = bool(resolved_doc_paths & precheck_context.formal_rule_paths) if precheck_context.formal_rule_paths else False

    issues: list[Issue] = []
    if STAGE_TRACEABILITY_HEADING not in doc_text:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少 `{STAGE_TRACEABILITY_HEADING}`，阶段协议与路线裁决链不够显式。",
            )
        )

    if (
        doc_type in {"script", "acceptance"}
        and precheck_context.current_stage_protocol_paths
        and not current_stage_protocol
    ):
        issues.append(
            Issue(
                "fail",
                f"说明文 `{doc_path}` 没有回链 Pre-check/Stage Gate 已声明的当前阶段协议 `{precheck_context.current_stage}`，"
                "无法证明本轮实现与当前阶段协议真正对齐。",
            )
        )
    if (
        doc_type in {"script", "acceptance"}
        and require_previous_stage
        and precheck_context.previous_stage_acceptance_paths
        and not previous_stage_acceptance
    ):
        issues.append(
            Issue(
                "fail",
                f"说明文 `{doc_path}` 没有回链 Pre-check/Stage Gate 已声明的上一阶段放行文件 `{precheck_context.previous_stage}`，"
                "无法说明当前阶段为什么被允许进入。",
            )
        )
    if (
        doc_type in {"script", "acceptance"}
        and (precheck_context.route_lock_paths or precheck_context.formal_rule_paths)
        and not (route_lock or formal_rule)
    ):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 没有回链本轮 Pre-check 已声明的路线锁定文件或直接依赖正式规则文件，论文级约束链仍然偏弱。",
            )
        )
    if doc_type == "asset" and precheck_context.current_stage_protocol_paths and not current_stage_protocol:
        issues.append(
            Issue(
                "partial",
                f"资产说明文 `{doc_path}` 没有回链本轮当前阶段协议 `{precheck_context.current_stage}`，阶段上下文不够完整。",
            )
        )
    if (
        doc_type == "asset"
        and (precheck_context.route_lock_paths or precheck_context.formal_rule_paths)
        and not (route_lock or formal_rule)
    ):
        issues.append(
            Issue(
                "partial",
                f"资产说明文 `{doc_path}` 没有回链本轮 Pre-check 已声明的路线文件或直接依赖正式规则文件，难以解释这个资产为什么这样组织。",
            )
        )
    return issues


def analyze_precheck_context_integrity(precheck_context: PrecheckContext) -> list[Issue]:
    issues: list[Issue] = []
    current_stage = precheck_context.current_stage
    is_first_stage = current_stage == STAGE_SEQUENCE[0]

    if not current_stage:
        issues.append(
            Issue(
                "fail",
                "无法从 Pre-check / Stage Gate / Pre-check Extraction 中解析出当前阶段，"
                "学习型说明文门禁失去了阶段协议裁决基线。",
            )
        )
        return issues

    if current_stage not in STAGE_SEQUENCE:
        issues.append(
            Issue(
                "partial",
                f"当前阶段 `{current_stage}` 不在既定阶段序列中，可能会导致阶段回链校验失真。",
            )
        )

    if not precheck_context.current_stage_protocol_paths:
        issues.append(
            Issue(
                "fail",
                f"Pre-check / Stage Gate 没有留下当前阶段 `{current_stage}` 的真实 `00_阶段总协议.md` 锚点，"
                "后续说明文无法执行精确阶段回链检查。",
            )
        )

    if not is_first_stage and not precheck_context.previous_stage:
        issues.append(
            Issue(
                "fail",
                f"当前阶段 `{current_stage}` 不是首阶段，但 Pre-check / Stage Gate 没有声明上一阶段。",
            )
        )
    if (
        precheck_context.previous_stage
        and not is_first_stage
        and not precheck_context.previous_stage_acceptance_paths
    ):
        issues.append(
            Issue(
                "fail",
                f"Pre-check / Stage Gate 没有留下上一阶段 `{precheck_context.previous_stage}` 的正式放行文件锚点，"
                "无法证明当前阶段为什么允许进入。",
            )
        )

    if not precheck_context.route_lock_paths and not precheck_context.formal_rule_paths:
        issues.append(
            Issue(
                "partial",
                "Pre-check 没有留下路线锁定文件或本轮直接依赖正式规则文件的真实锚点，"
                "学习型说明文的论文级约束链会退化成泛描述。",
            )
        )
    return issues


def node_display_name(node: ast.AST) -> str:
    if isinstance(node, ast.ClassDef):
        return f"类 `{node.name}`"
    if isinstance(node, ast.AsyncFunctionDef):
        return f"异步函数 `{node.name}()`"
    if isinstance(node, ast.FunctionDef):
        return f"函数 `{node.name}()`"
    return "未知符号"


def is_public_top_level_node(node: ast.AST) -> bool:
    return isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")


def is_core_symbol_node(node: ast.AST) -> bool:
    if isinstance(node, ast.ClassDef):
        return True
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    if node.name in {"main", "run", "train", "evaluate", "validate", "predict", "build", "load", "save", "forward"}:
        return True
    if len(node.body) >= 8:
        return True
    complex_stmt_count = sum(
        isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Match))
        for child in node.body
    )
    return complex_stmt_count >= 2


def validate_source_traceability_docstring(
    object_path: str,
    scope_label: str,
    docstring: str | None,
    current_stage: str,
) -> list[Issue]:
    issues: list[Issue] = []
    if not docstring:
        issues.append(
            Issue(
                "fail",
                f"源码对象 `{object_path}` 的 {scope_label} 缺少结构化来源 docstring，"
                "至少要写出 `对应阶段 / 理论依据 / 代码参考 / 本项目调整`。",
            )
        )
        return issues

    missing_fields = [
        field for field in SOURCE_TRACEABILITY_REQUIRED_FIELDS if field not in docstring
    ]
    if missing_fields:
        issues.append(
            Issue(
                "fail",
                f"源码对象 `{object_path}` 的 {scope_label} docstring 缺少字段: `{', '.join(missing_fields)}`。",
            )
        )

    if current_stage and current_stage not in docstring:
        issues.append(
            Issue(
                "partial",
                f"源码对象 `{object_path}` 的 {scope_label} docstring 没有显式写出当前阶段 `{current_stage}`。",
            )
        )

    if "理论依据" in docstring and not any(marker in docstring for marker in SOURCE_TRACEABILITY_PAPER_MARKERS):
        issues.append(
            Issue(
                "fail",
                f"源码对象 `{object_path}` 的 {scope_label} docstring 写了 `理论依据`，"
                "但没有给出论文/章节/公式或定义级锚点。",
            )
        )
    if "代码参考" in docstring and not all(marker in docstring for marker in SOURCE_TRACEABILITY_CODE_MARKERS):
        issues.append(
            Issue(
                "fail",
                f"源码对象 `{object_path}` 的 {scope_label} docstring 写了 `代码参考`，"
                "但没有把 `仓库 / 文件 / commit / 许可证` 四项写完整。",
            )
        )
    if "本项目调整" in docstring:
        adjustment_section = docstring.split("本项目调整", 1)[-1]
        if not has_substantive_content(adjustment_section, 1):
            issues.append(
                Issue(
                    "partial",
                    f"源码对象 `{object_path}` 的 {scope_label} `本项目调整` 仍然过空，"
                    "没有写清相对论文或参考实现到底改了什么。",
                )
            )
    return issues


def analyze_source_traceability(
    project_root: Path,
    object_path: str,
    precheck_context: PrecheckContext,
) -> list[Issue]:
    if Path(object_path).suffix.lower() != ".py":
        return []

    issues: list[Issue] = []
    object_fs_path = (project_root / object_path).resolve()
    if not object_fs_path.exists():
        issues.append(Issue("fail", f"源码对象不存在，无法检查来源 docstring: `{object_path}`。"))
        return issues

    try:
        module = ast.parse(read_text(object_fs_path), filename=str(object_fs_path))
    except SyntaxError as exc:
        issues.append(
            Issue(
                "fail",
                f"源码对象 `{object_path}` 无法通过 AST 解析，因而无法检查来源 docstring: "
                f"`line {exc.lineno}: {exc.msg}`。",
            )
        )
        return issues

    issues.extend(
        validate_source_traceability_docstring(
            object_path,
            "模块级 docstring",
            ast.get_docstring(module),
            precheck_context.current_stage,
        )
    )

    public_nodes = [node for node in module.body if is_public_top_level_node(node)]
    core_nodes = [node for node in public_nodes if is_core_symbol_node(node)]
    if not core_nodes and public_nodes:
        core_nodes = public_nodes[:1]

    if public_nodes and not core_nodes:
        issues.append(
            Issue(
                "partial",
                f"源码对象 `{object_path}` 没有识别到核心类/函数，建议确认顶层正式符号是否仍停留在占位状态。",
            )
        )
        return issues

    for node in core_nodes:
        issues.extend(
            validate_source_traceability_docstring(
                object_path,
                f"{node_display_name(node)} 的来源 docstring",
                ast.get_docstring(node),
                precheck_context.current_stage,
            )
        )
    return issues


def parse_diagnostics_result_text(text: str) -> dict[str, str]:
    results: dict[str, str] = {}
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        match = re.match(r"^-\s*([A-Za-z0-9_]+)\s*:\s*([A-Za-z_]+)\s*$", stripped)
        if match:
            results[normalize_relpath(match.group(1))] = normalize_relpath(match.group(2))
    return results


def extract_post_qc_simple_field(markdown_text: str, heading: str, label: str) -> str:
    section = extract_level2_section(markdown_text, heading)
    if not section:
        return ""
    return normalize_relpath(extract_field_value(section, label))


def analyze_diagnostics_consistency(
    project_root: Path,
    post_qc_guard_path: Path,
    post_qc_text: str,
) -> list[Issue]:
    issues: list[Issue] = []
    protocol_results, has_protocol_results = try_parse_protocol_results(post_qc_text)
    if not has_protocol_results:
        return issues

    diagnostics_section_conclusion = extract_post_qc_simple_field(post_qc_text, "## 5. Diagnostics 结果", "- 结论:")
    final_status = extract_post_qc_simple_field(post_qc_text, "## 6. 最终状态", "- Final Status:")
    backchain_section = extract_level2_section(post_qc_text, "## 5.1 关键回链")
    diagnostics_rel = normalize_relpath(extract_field_value(backchain_section, "- `diagnostics_result.txt` 路径:"))
    if not diagnostics_rel:
        diagnostics_rel = "diagnostics_result.txt"

    diagnostics_path = resolve_anchor_path(project_root, post_qc_guard_path, diagnostics_rel)
    if diagnostics_path is None:
        issues.append(
            Issue(
                "fail",
                f"Post-QC Guard 没有回链到真实存在的 `diagnostics_result.txt`: `{diagnostics_rel}`。",
            )
        )
        return issues

    diagnostics_map = parse_diagnostics_result_text(read_text(diagnostics_path))
    learning_gate_status = diagnostics_map.get("learning_doc_gate_pass", "")
    formal_gate_status = diagnostics_map.get("formal_doc_gate_pass", "")
    diagnostics_result = diagnostics_map.get("diagnostics_result", "")
    learning_protocol = protocol_results.get("学习型说明文门禁")
    formal_protocol = protocol_results.get("正式模板文档门禁")

    if not diagnostics_result:
        issues.append(
            Issue(
                "fail",
                f"`{diagnostics_path.name}` 缺少 `diagnostics_result` 总结行。",
            )
        )
    if not learning_gate_status and learning_protocol is not None:
        issues.append(
            Issue(
                "fail",
                f"`{diagnostics_path.name}` 缺少 `learning_doc_gate_pass`，无法和 Post-QC Guard 对账。",
            )
        )
    if not formal_gate_status and formal_protocol is not None:
        issues.append(
            Issue(
                "fail",
                f"`{diagnostics_path.name}` 缺少 `formal_doc_gate_pass`，无法和 Post-QC Guard 对账。",
            )
        )

    if learning_protocol is not None and learning_gate_status and learning_gate_status != learning_protocol.result:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 的 `学习型说明文门禁` 与 `diagnostics_result.txt` 的 `learning_doc_gate_pass` 不一致: "
                f"`{learning_protocol.result}` vs `{learning_gate_status}`。",
            )
        )
    if formal_protocol is not None and formal_gate_status and formal_gate_status != formal_protocol.result:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 的 `正式模板文档门禁` 与 `diagnostics_result.txt` 的 `formal_doc_gate_pass` 不一致: "
                f"`{formal_protocol.result}` vs `{formal_gate_status}`。",
            )
        )
    if diagnostics_section_conclusion and diagnostics_result and diagnostics_section_conclusion != diagnostics_result:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard `## 5. Diagnostics 结果` 的结论与 `diagnostics_result.txt` 不一致: "
                f"`{diagnostics_section_conclusion}` vs `{diagnostics_result}`。",
            )
        )
    if diagnostics_result in {"partial", "fail"} and final_status == "pass":
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 把最终状态写成 `pass`，但 `diagnostics_result.txt` 仍是 "
                f"`{diagnostics_result}`，状态口径没有同步。",
            )
        )
    return issues


def analyze_doc_specific_quality(doc_path: str, object_path: str, doc_text: str) -> list[Issue]:
    issues: list[Issue] = []
    doc_type = classify_doc_type(doc_path, object_path)

    if doc_type == "script":
        issues.extend(analyze_visual_structure(doc_path, doc_text, "script"))
        issues.extend(
            validate_substantive_sections(
                doc_path,
                doc_text,
                (
                    ("脚本作用", ("## 这个脚本的作用",), 3),
                    ("阶段位置", ("## 这个脚本在整个阶段中的位置",), 4),
                    ("核心逻辑", ("## 脚本核心逻辑",), 6),
                    ("运行说明", ("## 如何运行这个脚本",), 4),
                    ("验证说明", ("## 如何验证脚本运行结果",), 5),
                ),
            )
        )
        if not contains_any_keyword(doc_text, ("为什么不用", "为什么不选", "候选方案", "最终决策")):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 缺少显式设计取舍说明（如“为什么不用/为什么不选/候选方案”）。",
                )
            )
        if not contains_any_keyword(doc_text, ("误区", "容易误解", "协议违规风险")):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 缺少误区或协议违规风险提醒。",
                )
            )
        if not contains_any_keyword(doc_text, ("5 分钟自检任务", "学完后你应该具备什么能力")):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 缺少“学完后你应该具备什么能力”或“5 分钟自检任务”收口块。",
                )
            )
        if not contains_any_keyword(doc_text, ("你可以把它理解成", "你现在可能会问", "用人话说")):
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 缺少明显的口语化解释信号，难以证明已经按“小白友好”标准讲透。",
                )
            )
        exemplar_hits = count_pattern_group_hits(doc_text, EXEMPLAR_SCRIPT_STYLE_GROUPS)
        hit_count = sum(exemplar_hits.values())
        if hit_count < 3:
            missing = [name for name, hit in exemplar_hits.items() if not hit]
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 与融合版示范稿的风格对齐度不足，"
                    f"当前只命中 `{hit_count}` 组示范风格信号，缺少 `{', '.join(missing[:3])}`。",
                )
            )
    elif doc_type == "asset":
        issues.extend(analyze_visual_structure(doc_path, doc_text, "asset"))
        issues.extend(
            validate_substantive_sections(
                doc_path,
                doc_text,
                (
                    ("结构展示", ("## 这张表/这个文件长什么样",), 3),
                    ("真实结果", ("## 当前真实结果",), 3),
                    ("字段解释", ("## 这些列/字段分别是什么意思",), 4),
                    ("验证步骤", ("## 如何手工验证这个文件的正确性", "## 如何验证"), 4),
                ),
            )
        )
        if "## 当前真实结果" not in doc_text:
            issues.append(
                Issue(
                    "partial",
                    f"资产说明文 `{doc_path}` 缺少 `## 当前真实结果`，无法证明使用了真实数据而不是抽象例子。",
                )
            )
        if "## 这个文件没说明什么" not in doc_text and "局限性" not in doc_text:
            issues.append(
                Issue(
                    "partial",
                    f"资产说明文 `{doc_path}` 缺少边界/局限性说明，容易把文件能力讲过头。",
                )
            )
        style_hits = count_pattern_group_hits(doc_text, EXPLANATION_STYLE_GROUPS)
        style_hit_count = sum(style_hits.values())
        if style_hit_count < 2:
            missing = [name for name, hit in style_hits.items() if not hit]
            issues.append(
                Issue(
                    "partial",
                    f"资产说明文 `{doc_path}` 的口语化解释信号不足，"
                    f"当前只命中 `{style_hit_count}` 组风格信号，缺少 `{', '.join(missing[:2])}`。",
                )
            )
        if not contains_any_keyword(doc_text, ("建议联读", "下一步建议看", "学完后你应该具备什么能力")):
            issues.append(
                Issue(
                    "partial",
                    f"资产说明文 `{doc_path}` 缺少联读或收口提示，难以支撑 tcga 风格阅读引导。",
                )
            )
    elif doc_type == "acceptance":
        issues.extend(analyze_visual_structure(doc_path, doc_text, "acceptance"))
        issues.extend(
            validate_substantive_sections(
                doc_path,
                doc_text,
                (
                    ("通过判定标准", ("## 为什么现在能 pass", "## 当前阶段通过的判定标准"), 4),
                    ("物理证据", ("## 当前哪些证据最能支持 `pass`", "## 当前阶段的物理验收证据"), 4),
                    ("交付资产", ("## 当前阶段交付的正式资产清单",), 3),
                    ("回退条件", ("## 回退触发条件",), 3),
                    ("下一步", ("## 下一步应该怎么看", "## 下游阶段的放行条件", "## 下一步工作清单"), 3),
                ),
            )
        )
        if "## 当前阶段交付的正式资产清单" not in doc_text:
            issues.append(
                Issue(
                    "partial",
                    f"验收说明文 `{doc_path}` 缺少 `## 当前阶段交付的正式资产清单`。",
                )
            )
        if "## 回退触发条件" not in doc_text:
            issues.append(
                Issue(
                    "partial",
                    f"验收说明文 `{doc_path}` 缺少 `## 回退触发条件`。",
                )
            )
        style_hits = count_pattern_group_hits(doc_text, EXPLANATION_STYLE_GROUPS)
        style_hit_count = sum(style_hits.values())
        if style_hit_count < 2:
            missing = [name for name, hit in style_hits.items() if not hit]
            issues.append(
                Issue(
                    "partial",
                    f"验收说明文 `{doc_path}` 的口语化解释信号不足，"
                    f"当前只命中 `{style_hit_count}` 组风格信号，缺少 `{', '.join(missing[:2])}`。",
                )
            )
        if not contains_any_keyword(doc_text, ("误区", "容易误解", "风险", "为什么现在不能")):
            issues.append(
                Issue(
                    "partial",
                    f"验收说明文 `{doc_path}` 缺少误判风险或误区提醒，容易把阶段结论写成机械 checklist。",
                )
            )
    return issues


def analyze_entry_doc_quality(doc_path: str, doc_text: str) -> list[Issue]:
    issues: list[Issue] = []
    file_name = Path(doc_path).name
    issues.extend(analyze_visual_structure(doc_path, doc_text, "entry"))
    meaningful_lines = count_meaningful_lines(doc_text)
    if meaningful_lines < ENTRY_DOC_MIN_LINES:
        issues.append(
            Issue(
                "partial",
                f"阶段入口 `{doc_path}` 的有效正文行数为 `{meaningful_lines}`，低于要求 `{ENTRY_DOC_MIN_LINES}`。",
            )
        )

    style_hits = count_pattern_group_hits(doc_text, ENTRY_STYLE_GROUPS)
    style_hit_count = sum(style_hits.values())
    if style_hit_count < 2:
        missing = [name for name, hit in style_hits.items() if not hit]
        issues.append(
            Issue(
                "partial",
                f"阶段入口 `{doc_path}` 的口语化解释信号不足，当前只命中 `{style_hit_count}` 组，缺少 `{', '.join(missing[:2])}`。",
            )
        )

    risk_patterns = ENTRY_RISK_PATTERNS[file_name]
    if not contains_any_pattern(doc_text, risk_patterns):
        issues.append(
            Issue(
                "partial",
                f"阶段入口 `{doc_path}` 缺少诚实边界或误区提醒，容易把阶段结论写成过度乐观的目录说明。",
            )
        )

    closing_patterns = ENTRY_CLOSING_PATTERNS[file_name]
    if not contains_any_pattern(doc_text, closing_patterns):
        issues.append(
            Issue(
                "partial",
                f"阶段入口 `{doc_path}` 缺少联读收口或下一步引导，难以形成稳定阅读入口。",
            )
        )

    return issues


def analyze_evidence(
    project_root: Path,
    doc_path: str,
    object_path: str,
    doc_text: str,
) -> EvidenceResult:
    traceability_hits = {
        name: contains_any_keyword(doc_text, keywords)
        for name, keywords in TRACEABILITY_KEYWORDS.items()
    }
    physical_hits = {
        name: contains_any_keyword(doc_text, keywords)
        for name, keywords in PHYSICAL_EVIDENCE_KEYWORDS.items()
    }
    validation_hits = {
        name: contains_any_keyword(doc_text, keywords)
        for name, keywords in VALIDATION_KEYWORDS.items()
    }
    issues: list[Issue] = []
    missing_traceability = [name for name, hit in traceability_hits.items() if not hit]
    missing_physical = [name for name, hit in physical_hits.items() if not hit]
    missing_validation = [name for name, hit in validation_hits.items() if not hit]

    if len(missing_traceability) == len(traceability_hits):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少来源锚点，未识别到论文/代码/冻结回链类证据。",
            )
        )
    if len(missing_physical) == len(physical_hits):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少物理证据锚点，未识别到路径/字段/结果类证据。",
            )
        )
    if len(missing_validation) == len(validation_hits):
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少验证锚点，未识别到检查方法或通过标准。",
            )
        )

    doc_type = classify_doc_type(doc_path, object_path)
    if doc_type == "script" and not traceability_hits["冻结回链"]:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 缺少冻结表回链痕迹，未识别到 `冻结表/参数冻结总表/冻结依据`。",
            )
        )
    if doc_type == "script" and not traceability_hits["代码来源"]:
        issues.append(
            Issue(
                "partial",
                f"脚本说明文 `{doc_path}` 缺少代码来源锚点，未识别到 `代码参考/仓库/当前实现/参考行数`。",
            )
        )

    density_rule = DOC_TYPE_DENSITY_RULES.get(doc_type)
    if density_rule is not None:
        traceability_density = sum(
            count_keyword_hits(doc_text, keywords)
            for keywords in TRACEABILITY_KEYWORDS.values()
        )
        physical_density = sum(
            count_keyword_hits(doc_text, keywords)
            for keywords in PHYSICAL_EVIDENCE_KEYWORDS.values()
        )
        validation_density = sum(
            count_keyword_hits(doc_text, keywords)
            for keywords in VALIDATION_KEYWORDS.values()
        )

        if traceability_density < density_rule["traceability"]:
            issues.append(
                Issue(
                    "partial",
                    f"说明文 `{doc_path}` 的来源锚点密度为 `{traceability_density}`，"
                    f"低于 `{doc_type}` 文档要求 `{density_rule['traceability']}`。",
                )
            )
        if physical_density < density_rule["physical"]:
            issues.append(
                Issue(
                    "partial",
                    f"说明文 `{doc_path}` 的物理证据锚点密度为 `{physical_density}`，"
                    f"低于 `{doc_type}` 文档要求 `{density_rule['physical']}`。",
                )
            )
        if validation_density < density_rule["validation"]:
            issues.append(
                Issue(
                    "partial",
                    f"说明文 `{doc_path}` 的验证锚点密度为 `{validation_density}`，"
                    f"低于 `{doc_type}` 文档要求 `{density_rule['validation']}`。",
                )
            )

    issues.extend(analyze_anchor_evidence(project_root, doc_path, object_path, doc_text))
    return EvidenceResult(
        issues=issues,
        traceability_hits=traceability_hits,
        physical_hits=physical_hits,
        validation_hits=validation_hits,
    )


def analyze_doc_structure(doc_path: str, object_path: str, doc_text: str) -> DocStructureResult:
    issues: list[Issue] = []
    doc_type = classify_doc_type(doc_path, object_path)
    seven_hits = analyze_seven_questions(doc_text, doc_type)
    missing_questions = [name for name, hit in seven_hits.items() if not hit]
    if missing_questions:
        issues.append(
            Issue(
                "partial",
                f"说明文 `{doc_path}` 缺少 7 问的显式结构或强信号: `{', '.join(missing_questions)}`。",
            )
        )

    if doc_type == "script":
        missing_sections = [heading for heading in SCRIPT_REQUIRED_SECTIONS if not heading_exists(doc_text, heading)]
        if missing_sections:
            issues.append(
                Issue(
                    "partial",
                    f"脚本说明文 `{doc_path}` 缺少关键章节: `{', '.join(missing_sections)}`。",
                )
            )
    elif doc_type == "asset":
        for group_name, heading_group in ASSET_REQUIRED_SECTION_GROUPS:
            if not any(heading_exists(doc_text, heading) for heading in heading_group):
                issues.append(
                    Issue(
                        "partial",
                        f"资产说明文 `{doc_path}` 缺少 `{group_name}` 类关键章节。",
                    )
                )
    elif doc_type == "acceptance":
        for group_name, heading_group in ACCEPTANCE_REQUIRED_SECTION_GROUPS:
            if not any(heading_exists(doc_text, heading) for heading in heading_group):
                issues.append(
                    Issue(
                        "partial",
                        f"验收说明文 `{doc_path}` 缺少 `{group_name}` 类关键章节。",
                    )
                )

    issues.extend(analyze_doc_specific_quality(doc_path, object_path, doc_text))
    return DocStructureResult(issues=issues, seven_question_hits=seven_hits)


def analyze_stage_entry_sync(
    project_root: Path,
    post_rows: list[MappingRow],
    changed_paths: set[str],
) -> list[Issue]:
    issues: list[Issue] = []
    stage_rows: dict[str, list[MappingRow]] = {}
    for row in post_rows:
        if row.action == "not_applicable" or not is_learning_doc_path(row.doc_path):
            continue
        stage_root = stage_root_for_learning_doc(row.doc_path)
        if stage_root:
            stage_rows.setdefault(stage_root, []).append(row)

    for stage_root, rows in stage_rows.items():
        readme_rel = f"{stage_root}/README.md"
        status_rel = f"{stage_root}/implementation_status.md"
        readme_path = project_root / readme_rel
        status_path = project_root / status_rel

        if not readme_path.exists():
            issues.append(Issue("fail", f"阶段入口缺少 README: `{readme_rel}`"))
            continue
        if not status_path.exists():
            issues.append(Issue("fail", f"阶段入口缺少 implementation_status: `{status_rel}`"))
            continue

        created_non_entry_doc = any(
            row.action == "create"
            and Path(row.doc_path).name not in {"README.md", "implementation_status.md"}
            for row in rows
        )
        acceptance_doc_changed = any(
            "为什么能pass" in Path(row.doc_path).name for row in rows
        )

        if created_non_entry_doc and readme_rel not in changed_paths:
            issues.append(
                Issue(
                    "partial",
                    f"阶段 `{stage_root}` 本轮新增了学习型说明文，但 `{readme_rel}` 未同步更新。",
                )
            )
        if created_non_entry_doc and status_rel not in changed_paths:
            issues.append(
                Issue(
                    "partial",
                    f"阶段 `{stage_root}` 本轮新增了学习型说明文，但 `{status_rel}` 未同步更新。",
                )
            )
        if acceptance_doc_changed and status_rel not in changed_paths:
            issues.append(
                Issue(
                    "partial",
                    f"阶段 `{stage_root}` 本轮更新了验收入口文档，但 `{status_rel}` 未同步更新。",
                )
            )

        readme_text = read_text(readme_path)
        status_text = read_text(status_path)
        missing_readme_sections = [
            heading for heading in README_REQUIRED_SECTIONS if heading not in readme_text
        ]
        missing_status_sections = [
            heading
            for heading in IMPLEMENTATION_STATUS_REQUIRED_SECTIONS
            if heading not in status_text
        ]
        if missing_readme_sections:
            issues.append(
                Issue(
                    "partial",
                    f"阶段入口 `{readme_rel}` 缺少关键章节: `{', '.join(missing_readme_sections)}`。",
                )
            )
        if missing_status_sections:
            issues.append(
                Issue(
                    "partial",
                    f"阶段状态页 `{status_rel}` 缺少关键章节: `{', '.join(missing_status_sections)}`。",
                )
            )

        issues.extend(analyze_entry_doc_quality(readme_rel, readme_text))
        issues.extend(analyze_entry_doc_quality(status_rel, status_text))

    return issues


def evaluate_task(
    project_root: Path,
    precheck_guard_path: Path,
    post_qc_guard_path: Path,
) -> tuple[str, list[str]]:
    issues: list[Issue] = []
    guard_dir = precheck_guard_path.parent
    stage_gate_path = guard_dir / "stage_gate_check.md"
    extraction_path = guard_dir / "pre_check_extraction.md"
    precheck_text = read_text(precheck_guard_path)
    post_qc_text = read_text(post_qc_guard_path)
    stage_gate_text = read_text(stage_gate_path) if stage_gate_path.exists() else ""
    extraction_text = read_text(extraction_path) if extraction_path.exists() else ""
    precheck_context = build_precheck_context(
        project_root,
        precheck_guard_path,
        precheck_text,
        stage_gate_text,
        extraction_text,
    )
    changed_rows = parse_changed_files(post_qc_text)
    precheck_rows, has_precheck_mapping = try_parse_mapping_rows(precheck_text, "## 6.1 预期文档映射")
    post_rows, has_post_mapping = try_parse_mapping_rows(post_qc_text, "## 4.1 对象-说明文映射回填")

    changed_paths = {row.file_path for row in changed_rows}
    changed_row_map = {row.file_path: row for row in changed_rows}
    candidate_paths = [row.file_path for row in changed_rows if is_formal_object_candidate(row.file_path)]
    explicitly_declared_conditional_paths = {
        row.object_path
        for row in (*precheck_rows, *post_rows)
        if row.action != "not_applicable" and is_conditional_formal_object_candidate(row.object_path)
    }
    candidate_paths.extend(
        path
        for path in changed_paths
        if path in explicitly_declared_conditional_paths and path not in candidate_paths
    )
    precheck_map = {row.object_path: row for row in precheck_rows}
    post_map = {row.object_path: row for row in post_rows}
    actionable_candidate_paths = [
        path
        for path in candidate_paths
        if post_map.get(path) is not None and post_map[path].action != "not_applicable"
    ]

    if actionable_candidate_paths:
        issues.extend(analyze_precheck_context_integrity(precheck_context))

    if candidate_paths and not has_precheck_mapping:
        issues.append(
            Issue(
                "fail",
                "Pre-check Guard 缺少 `## 6.1 预期文档映射`，无法证明正式对象在编码前已经声明对应学习型说明文。",
            )
        )
    if candidate_paths and not has_post_mapping:
        issues.append(
            Issue(
                "fail",
                "Post-QC Guard 缺少 `## 4.1 对象-说明文映射回填`，无法证明正式对象与学习型说明文的最终回填关系。",
            )
        )

    for candidate_path in candidate_paths:
        if candidate_path not in post_map:
            issues.append(Issue("fail", f"缺少 Post-QC 对象映射: `{candidate_path}`"))

    for row in post_rows:
        if row.action not in VALID_MAPPING_ACTIONS:
            issues.append(
                Issue(
                    "fail",
                    f"对象 `{row.object_path}` 的动作 `{row.action}` 不在允许集合 "
                    f"`{sorted(VALID_MAPPING_ACTIONS)}` 内。",
                )
            )
        if not row.note:
            issues.append(Issue("fail", f"对象 `{row.object_path}` 的映射结果/原因为空。"))

        if row.object_path in precheck_map:
            planned_action = precheck_map[row.object_path].action
            if planned_action != row.action:
                issues.append(
                    Issue(
                        "partial",
                        f"对象 `{row.object_path}` 的 Pre-check 动作为 `{planned_action}`，"
                        f"但 Post-QC 回填为 `{row.action}`。",
                    )
                )
        elif is_formal_object_candidate(row.object_path):
            issues.append(Issue("partial", f"对象 `{row.object_path}` 未在 Pre-check 映射表中提前声明。"))

        if row.action == "not_applicable":
            continue

        if not row.doc_path or row.doc_path == "-":
            issues.append(Issue("fail", f"对象 `{row.object_path}` 缺少对应学习型说明文路径。"))
            continue

        if not is_learning_doc_path(row.doc_path):
            issues.append(
                Issue(
                    "fail",
                    f"对象 `{row.object_path}` 的说明文路径 `{row.doc_path}` 不在 "
                    "`reports/stage_reports/implementation_tracking/` 下。",
                )
            )
            continue

        doc_path = project_root / row.doc_path
        if not doc_path.exists():
            issues.append(Issue("fail", f"对象 `{row.object_path}` 的说明文不存在: `{row.doc_path}`"))
            continue

        if not is_changed_in_post_qc(row.doc_path, changed_paths):
            issues.append(
                Issue(
                    "fail",
                    f"对象 `{row.object_path}` 标记为 `{row.action}`，但对应说明文 "
                    f"`{row.doc_path}` 不在 Post-QC 实际修改文件表中。",
                )
            )

        doc_text = read_text(doc_path)
        if row.action == "append_version":
            if not contains_version_record(doc_text):
                issues.append(
                    Issue(
                        "fail",
                        f"对象 `{row.object_path}` 标记为 `append_version`，但 `{row.doc_path}` "
                        f"缺少 `{VERSION_RECORD_HEADING}`。",
                    )
                )
            elif not has_complete_version_record(doc_text):
                issues.append(
                    Issue(
                        "fail",
                        f"对象 `{row.object_path}` 标记为 `append_version`，但 `{row.doc_path}` 的版本记录表缺少"
                        "完整的最新一行（日期 / 改动内容 / 影响范围 / 是否需要重新验证）。",
                    )
                )

            object_change = changed_row_map.get(row.object_path)
            doc_change = changed_row_map.get(row.doc_path)
            if object_change and object_change.action == "create":
                issues.append(
                    Issue(
                        "fail",
                        f"对象 `{row.object_path}` 是本轮新建文件，却被回填为 `append_version`；"
                        "首次正式可用对象必须使用 `create` 或 `update` 对应的完整说明动作。",
                    )
                )
            if doc_change and doc_change.action == "create":
                issues.append(
                    Issue(
                        "fail",
                        f"说明文 `{row.doc_path}` 是本轮新建文件，却被回填为 `append_version`；"
                        "新说明文不能只靠版本追加交差。",
                    )
                )

        minimum = expected_min_lines(row.doc_path, row.object_path)
        if minimum is not None:
            actual = count_meaningful_lines(doc_text)
            if actual < minimum:
                issues.append(
                    Issue(
                        "partial",
                        f"说明文 `{row.doc_path}` 的有效正文行数为 `{actual}`，低于要求 `{minimum}`。",
                    )
                )

        structure_result = analyze_doc_structure(row.doc_path, row.object_path, doc_text)
        issues.extend(structure_result.issues)
        evidence_result = analyze_evidence(project_root, row.doc_path, row.object_path, doc_text)
        issues.extend(evidence_result.issues)
        issues.extend(analyze_traceability_card(project_root, row.doc_path, row.object_path, doc_text))
        issues.extend(
            analyze_stage_protocol_traceability(
                project_root,
                row.doc_path,
                row.object_path,
                doc_text,
                precheck_context,
            )
        )
        issues.extend(analyze_source_traceability(project_root, row.object_path, precheck_context))

    for row in precheck_rows:
        if is_formal_object_candidate(row.object_path) and row.object_path not in post_map:
            issues.append(
                Issue(
                    "partial",
                    f"Pre-check 预期对象 `{row.object_path}` 没有在 Post-QC 映射表中回填。",
                )
            )

    issues.extend(
        analyze_manual_review(
            project_root,
            post_qc_guard_path,
            post_qc_text,
            post_rows,
            changed_row_map,
        )
    )
    issues.extend(analyze_diagnostics_consistency(project_root, post_qc_guard_path, post_qc_text))
    issues.extend(analyze_stage_entry_sync(project_root, post_rows, changed_paths))

    issue_lines = [f"- [{issue.severity}] {issue.message}" for issue in issues]
    if any(issue.severity == "fail" for issue in issues):
        return "fail", issue_lines
    if any(issue.severity == "partial" for issue in issues):
        return "partial", issue_lines
    if not actionable_candidate_paths:
        return "not_applicable", ["- [not_applicable] 本轮没有需要学习型说明文映射的正式对象。"]
    return "pass", ["- [pass] 映射覆盖、目标文档存在性、真实路径锚点和结构化质量检查均通过。"]


def build_report(
    project_root: Path,
    precheck_guard: Path,
    post_qc_guard: Path,
    status: str,
    details: Iterable[str],
) -> str:
    detail_list = list(details)
    report_group_rules = (
        (
            "映射与同步",
            ("映射", "Pre-check 预期对象", "Post-QC", "README.md", "implementation_status.md", "阶段入口"),
        ),
        (
            "存在性与路径",
            ("路径", "真实存在", "不存在", "implementation_tracking", "无法解析", "位于 `reports/stage_reports/implementation_tracking/`"),
        ),
        (
            "结构与体量",
            ("体量", "标题层次", "短段落", "结构化阅读信号", "最长连续纯正文", "关键章节", "正文"),
        ),
        (
            "七问与表达",
            ("7 问", "口语化", "风格信号", "联读", "误区", "设计取舍", "视觉层次"),
        ),
        (
            "溯源与证据",
            ("结构化溯源卡片", "来源", "证据", "验证步骤", "数值级物理证据", "append_version"),
        ),
        (
            "人工终审",
            ("人工审稿", "人工终审", "TCGA", "学习型说明文人工审稿清单", "对照示范稿"),
        ),
    )
    lines = [
        "# Learning Doc Gate Report",
        "",
        "## 1. 输入文件",
        f"- `project_root`: `{project_root}`",
        f"- `precheck_guard`: `{precheck_guard.relative_to(project_root).as_posix()}`",
        f"- `post_qc_guard`: `{post_qc_guard.relative_to(project_root).as_posix()}`",
        "",
        "## 2. 检查范围",
        "- 检查 Post-QC `实际创建/修改文件` 表中的正式对象是否进入学习型说明文映射。",
        "- 检查 Pre-check `预期文档映射` 与 Post-QC `对象-说明文映射回填` 是否前后对齐。",
        "- 检查说明文路径是否真实存在，且是否位于 `reports/stage_reports/implementation_tracking/` 下。",
        f"- 检查 `append_version` 是否真的落到 `{VERSION_RECORD_HEADING}`。",
        "- 检查当某个阶段本轮新增学习型说明文或重写验收入口时，对应 `README.md` 与 `implementation_status.md` 是否同步更新。",
        f"- 检查说明文体量是否达到当前规程的最小要求（核心脚本文档 `{CORE_SCRIPT_DOC_MIN_LINES}` 行，工具脚本文档 `{UTILITY_SCRIPT_DOC_MIN_LINES}` 行，正式资产文档 `{ASSET_DOC_MIN_LINES}` 行，薄配置资产 `{THIN_ASSET_DOC_MIN_LINES}` 行，验收说明文 `{ACCEPTANCE_DOC_MIN_LINES}` 行）。",
        "- 检查脚本说明文、资产说明文、验收说明文是否缺少当前规程要求的关键章节骨架。",
        "- 检查阶段入口 `README.md` / `implementation_status.md` 是否也达到最小正文、口语化解释、诚实边界和联读收口要求。",
        "- 检查 7 问是否以显式结构或强信号真正落盘，而不是只靠零散关键词蹭命中。",
        "- 检查说明文中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。",
        "- 检查说明文是否包含数值级物理证据、验证步骤和设计取舍说明。",
        "- 检查关键章节是否真的写入了非占位、非空壳的正文，而不是只有标题或几行模板残留。",
        "- 检查脚本说明文是否保留了明显的口语化解释信号，避免只剩审计术语和 checklist。",
        "- 检查脚本说明文是否至少命中融合版示范稿中的多组风格信号，而不是只有一两句口语化点缀。",
        "- 检查资产说明文和验收说明文是否也保留最小口语化解释、联读收口和误判风险提示，避免只有结构过关。",
        "- 检查说明文是否保留最小视觉层次信号：标题层次、短段落留白、表格或编号链，避免整篇退化成密集长段落。",
        f"- 对脚本说明文额外检查 `{TRACEABILITY_CARD_HEADING}` 是否存在、字段是否完整、路径是否真实存在。",
        f"- 检查 Post-QC `{PROTOCOL_RESULTS_HEADING}` 与 `{MANUAL_REVIEW_HEADING}` 是否一致，并在需要时强制要求人工终审回填。",
        "- 检查人工终审是否回填 `学习型说明文人工审稿清单.md`、`TCGA原始标杆对齐清单.md` 与真实 TCGA 原始文档对照锚点。",
        "- 说明: 本报告会检查人工终审是否真正落盘，但它仍不能替代人工阅读本身。",
        "",
        "## 3. 结论",
        f"- `learning_doc_gate_status`: `{status}`",
        "",
        "## 4. 检查摘要",
        "",
    ]
    if status == "pass":
        lines.extend(
            [
                "- `映射与同步`: 未发现 learning gate 异常。",
                "- `存在性与路径`: 未发现 learning gate 异常。",
                "- `结构与体量`: 未发现 learning gate 异常。",
                "- `七问与表达`: 未发现 learning gate 异常。",
                "- `溯源与证据`: 未发现 learning gate 异常。",
                "- `人工终审`: 未发现 learning gate 异常。",
            ]
        )
    elif status == "not_applicable":
        lines.append("- `总体`: 本轮没有需要学习型说明文映射的正式对象。")
    else:
        grouped: dict[str, list[str]] = {group_name: [] for group_name, _ in report_group_rules}
        grouped["其他"] = []
        for detail in detail_list:
            matched = False
            for group_name, keywords in report_group_rules:
                if any(keyword in detail for keyword in keywords):
                    grouped[group_name].append(detail)
                    matched = True
                    break
            if not matched:
                grouped["其他"].append(detail)

        for group_name in [name for name, _ in report_group_rules] + ["其他"]:
            entries = grouped[group_name]
            if not entries:
                continue
            fail_count = sum(1 for entry in entries if "[fail]" in entry)
            partial_count = sum(1 for entry in entries if "[partial]" in entry)
            pass_count = sum(1 for entry in entries if "[pass]" in entry)
            summary_bits: list[str] = []
            if fail_count:
                summary_bits.append(f"`fail={fail_count}`")
            if partial_count:
                summary_bits.append(f"`partial={partial_count}`")
            if pass_count and not (fail_count or partial_count):
                summary_bits.append(f"`pass={pass_count}`")
            if not summary_bits:
                summary_bits.append("`issue_count=0`")
            lines.append(f"- `{group_name}`: {' / '.join(summary_bits)}")

    lines.extend(
        [
            "",
            "## 5. 详细结果",
            *detail_list,
            "",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    precheck_guard = (project_root / args.precheck_guard).resolve()
    post_qc_guard = (project_root / args.post_qc_guard).resolve()
    if not precheck_guard.exists():
        raise FileNotFoundError(f"Pre-check guard not found: {precheck_guard}")
    if not post_qc_guard.exists():
        raise FileNotFoundError(f"Post-QC guard not found: {post_qc_guard}")

    if args.output:
        output_path = (project_root / args.output).resolve()
    else:
        output_path = post_qc_guard.parent / "learning_doc_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    status, details = evaluate_task(project_root, precheck_guard, post_qc_guard)
    report_text = build_report(project_root, precheck_guard, post_qc_guard, status, details)
    output_path.write_text(report_text, encoding="utf-8")

    print(f"learning_doc_gate_status={status}")
    print(f"wrote_report={output_path}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
