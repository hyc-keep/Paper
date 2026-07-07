"""Validate formal stage/template markdown docs updated in the current task."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


PATH_ANCHOR_PATTERN = re.compile(r"`[^`\n]*(?:/|\\|\.md|\.py|\.yaml|\.csv|\.txt)[^`\n]*`")
PATH_ANCHOR_VALUE_PATTERN = re.compile(r"`([^`\n]*(?:/|\\|\.md|\.py|\.yaml|\.csv|\.txt)[^`\n]*)`")
SECTION_RULES = {
    "governance": (
        (
            "角色/入口",
            (
                "## 正式角色",
                "## 角色/入口",
                "## 1. 角色/入口",
                "## 调用入口",
                "## 目的",
                "## 核心理念",
                "## 何时必须调用",
                "## 1. 当前唯一有效的使用顺序",
            ),
        ),
        (
            "边界/分层",
            (
                "## 边界/分层",
                "## 2. 边界/分层",
                "## 当前边界",
                "## 状态口径边界",
                "## 2. 当前目录的角色划分",
                "## 强制三阶段流程",
                "## 通过标准",
                "## 红线(触发立即回退)",
            ),
        ),
        (
            "门禁/审查",
            (
                "## 门禁/审查",
                "## 8. 门禁/审查回链",
                "## 八、强制执行机制",
                "## 3. 冲突时谁说了算",
                "## 5. 最短选择指南",
                "#### 3.1 代码验证",
                "#### 3.4 Post-QC 协议级质检固定模板",
            ),
        ),
    ),
    "tcga_benchmark_checklist": (
        ("角色/入口", ("## 正式角色", "## 当前边界", "## 1. 当前唯一有效的原始标杆")),
        ("标杆定义", ("## 2. 这份原始标杆真正强在哪里", "## 3. 后续写作时最低要对照什么")),
        ("审查/回填", ("## 4. 写前最低动作", "## 5. 人工审稿时必须留下的物理证据")),
        ("验收/回退", ("## 7. 验收与回退", "## 6. 红线")),
    ),
    "manual_review_checklist": (
        ("角色/入口", ("## 正式角色", "## 1. 这份清单负责什么")),
        ("边界/触发", ("## 当前边界", "## 3. 什么时候必须用")),
        ("执行/审查", ("## 4. 人工审稿执行顺序", "## 6. 核心审稿问题")),
        ("结论/回填", ("## 7. 审稿结论怎么判", "## 8. Post-QC Guard 回填模板", "## 红线(触发立即回退)")),
    ),
    "template_stage_card": (
        ("角色边界", ("## 1. 卡片角色与执行边界",)),
        ("已读依据", ("## 2. 本轮直接依赖的已读文件",)),
        ("阶段原因", ("## 3. 当前阶段唯一目标", "## 4. 为什么现在做这个,而不是下一个阶段")),
        ("工程验证", ("## 7. 本轮工程落点", "## 8. 本轮最小运行验证计划", "## 10. 阶段锁定结论")),
    ),
    "template_research_record": (
        ("角色边界", ("## 1. 记录角色与边界",)),
        ("已读依据", ("## 2. 本轮直接依赖的已读文件",)),
        ("研究目标", ("## 3. 当前阶段研究目标", "## 4. 从计划与协议中提取的硬约束")),
        ("边界结论", ("## 6. 当前阶段边界初判", "## 7. 对后续阶段锁定的输入", "## 9. 研究结论")),
    ),
    "research_record": (
        ("角色边界", ("## 1. 记录角色与边界",)),
        ("已读依据", ("## 2. 本轮直接依赖的已读文件",)),
        ("研究目标", ("## 3. 当前阶段研究目标", "## 4. 从计划与协议中提取的硬约束")),
        ("边界结论", ("## 6. 当前阶段边界初判", "## 7. 对后续阶段锁定的输入", "## 9. 研究结论")),
    ),
    "template_precheck_guard": (
        ("元信息", ("> **使用场景**", "> **调用顺序**", "> **与中央门禁的关系**")),
        ("模板正文", ("```markdown", "```text")),
        ("风险提示", ("**红线提醒:**", "## 6. 红线提醒", "## 7. 上游 guard 文件回链")),
    ),
    "template_post_guard": (
        ("元信息", ("> **使用场景**", "> **调用顺序**", "> **与中央门禁的关系**")),
        ("模板正文", ("```markdown", "```text")),
        ("风险提示", ("**红线提醒:**", "**怎么判 `not_applicable`:**")),
    ),
    "template_stage_protocol": (
        ("角色边界", ("## 1. 文件角色与执行边界",)),
        ("前置依赖", ("## 2. 本轮直接依赖的前置文件",)),
        ("变量边界", ("## 3. 本阶段唯一允许处理的变量",)),
        ("阶段门控", ("## 4. 阶段门控表达式",)),
    ),
    "template_design": (
        ("角色边界", ("## 1. 文件角色与执行边界",)),
        ("前置依赖", ("## 2. 前置文件依赖",)),
        ("设计动机", ("## 3. 任务难点与设计动机",)),
        ("设计边界", ("## 4. 设计边界(做什么/不做什么)",)),
    ),
    "template_acceptance": (
        ("角色边界", ("## 1. 为什么要拆成两个子模板", "## 1. 当前文件的角色边界", "## 6. 当前文件的角色边界")),
        ("选型规则", ("## 2. 先判断当前阶段属于哪一类", "## 3. 一张表快速选型")),
        ("共同底线", ("## 4. 两类子模板共同必须满足的底线", "## 4. 红线条件")),
        ("使用方式", ("## 5. 正式使用方式", "## 5. 阶段通过声明")),
    ),
    "template_evidence": (
        ("基本信息", ("## 1. 论文基本信息",)),
        ("可引句子", ("## 2. 可以直接用于论文写作的句子",)),
        ("实验数字", ("## 3. 可以直接引用的实验数字",)),
        ("公式算法", ("## 4. 核心公式和算法",)),
    ),
    "stage_protocol": (
        ("角色边界", ("## 1. 文件角色与执行边界",)),
        ("前置依赖", ("## 2. 本轮直接依赖的前置文件", "## 2. 前置文件依赖")),
        ("变量或边界", ("## 3. 本阶段唯一允许处理的变量", "## 4. 设计边界(做什么/不做什么)")),
        ("门控/通过线", ("## 4. 阶段门控表达式", "## 5. 如何判断设计有效(验收标准)")),
    ),
    "design_basis": (
        ("角色边界", ("## 1. 文件角色与执行边界",)),
        ("前置依赖", ("## 2. 前置文件依赖",)),
        ("设计动机", ("## 3. 任务难点与设计动机",)),
        ("边界声明", ("## 4. 设计边界(做什么/不做什么)",)),
    ),
    "stage_acceptance": (
        ("交付物", ("## 1. 本阶段最小交付物", "## 1. 当前阶段最小交付物")),
        ("验收问题", ("## 2. 定量验收标准", "## 2. 核心验收问题")),
        ("红线", ("## 4. 红线条件",)),
        ("结论", ("## 5. 阶段通过声明",)),
    ),
    "literature_evidence": (
        ("基本信息", ("## 1. 论文基本信息",)),
        ("原文证据", ("## 2. 可以直接用于论文写作的句子",)),
        ("实验数字", ("## 3. 可以直接引用的实验数字",)),
        ("公式算法", ("## 4. 核心公式和算法",)),
    ),
}
MIN_MEANINGFUL_LINES = {
    "governance": 60,
    "tcga_benchmark_checklist": 60,
    "manual_review_checklist": 60,
    "template_stage_card": 60,
    "template_research_record": 55,
    "research_record": 55,
    "template_precheck_guard": 20,
    "template_post_guard": 20,
    "template_stage_protocol": 60,
    "template_design": 60,
    "template_acceptance": 50,
    "template_evidence": 50,
    "stage_protocol": 80,
    "design_basis": 80,
    "stage_acceptance": 80,
    "literature_evidence": 80,
}
MIN_PATH_ANCHOR_COUNTS = {
    "governance": 2,
    "tcga_benchmark_checklist": 3,
    "manual_review_checklist": 3,
    "template_stage_card": 2,
    "template_research_record": 2,
    "research_record": 2,
    "template_precheck_guard": 0,
    "template_post_guard": 0,
    "template_stage_protocol": 1,
    "template_design": 1,
    "template_acceptance": 1,
    "template_evidence": 1,
    "stage_protocol": 2,
    "design_basis": 2,
    "stage_acceptance": 2,
    "literature_evidence": 2,
}
MIN_RESOLVED_PATH_ANCHOR_COUNTS = {
    "governance": 2,
    "tcga_benchmark_checklist": 3,
    "manual_review_checklist": 3,
    "template_stage_card": 2,
    "template_research_record": 2,
    "research_record": 2,
    "template_precheck_guard": 0,
    "template_post_guard": 0,
    "template_stage_protocol": 1,
    "template_design": 1,
    "template_acceptance": 1,
    "template_evidence": 1,
    "stage_protocol": 2,
    "design_basis": 2,
    "stage_acceptance": 2,
    "literature_evidence": 2,
}
SOURCE_KEYWORDS = ("依据", "文献", "路线", "来源", "论文", "引用")
BOUNDARY_KEYWORDS = ("负责什么", "不负责什么", "边界", "做什么", "不做什么", "禁止", "只负责", "不替代")
CODE_KEYWORDS = (
    "代码落点",
    "工程落点",
    "代码实现约束",
    "代码落地接口",
    "代码文件",
    "入口类/函数",
    "预期代码落点",
    "run / report / external",
)
VALIDATION_KEYWORDS = ("验收", "验证", "通过标准", "回退", "Diagnostics", "质检", "检查方法", "Stage Gate Result", "关键回链")
STATE_SPACE_SIGNATURES = (
    "allow / blocked",
    "pass / partial / fail / not_applicable",
    "not_started / blocked / partial / pass",
)
IMPLEMENTATION_TRACKING_ENTRY_TARGETS = (
    "README.md",
    "implementation_status.md",
    "implementation_tracking",
    "阶段入口",
)
STATE_SEMANTIC_GUARDRAILS = (
    "不要",
    "不得",
    "不能",
    "禁止",
    "误写",
    "偷换",
    "检查",
    "错误",
    "只允许",
    "只能使用",
)
COMMAND_SIGNATURES = (
    "b_class_auxiliary/tools/check_research_alignment_gate.py",
    "b_class_auxiliary/tools/check_stage_definition_gate.py",
    "b_class_auxiliary/tools/check_precheck_docs.py",
    "b_class_auxiliary/tools/check_learning_docs.py",
    "b_class_auxiliary/tools/check_formal_stage_docs.py",
)
PATH_LIKE_PREFIXES = (
    "./",
    "../",
    ".trae/",
    "b_class_auxiliary/",
    "reports/",
    "src/",
    "tools/",
    "scripts/",
    "configs/",
    "datasets/",
    "splits/",
    "experiments/",
    "external/",
    "crc_gland_segmentation_project/",
    "结直肠腺体分割_plan_优化版/",
)
PATH_LIKE_SUFFIXES = (".md", ".py", ".yaml", ".yml", ".csv", ".txt")
SKIP_BARE_FILENAMES = {
    "00_阶段总协议.md",
    "阶段验收.md",
    "source_file.py.md",
    "implementation_status.md",
    "config.yaml",
    "run_meta.yaml",
    "train_log.csv",
    "val_metrics.csv",
    "testa_metrics.csv",
    "testb_metrics.csv",
    "test_metrics.csv",
    "diagnostics_result.txt",
    "stage_definition_gate_report.md",
    "learning_doc_gate_report.md",
    "formal_doc_gate_report.md",
    "pre_check_extraction.md",
    "stage_gate_check.md",
    "current_codebase_状态.md",
    "pre_check_guard.md",
    "post_qc_guard.md",
}
ALLOWED_BARE_FILENAMES = {
    "研究定标记录.md",
    "00_阶段实现卡.md",
    "00_技能体系导航.md",
    "论文实验项目文档编写规范_完整版.md",
    "实验执行文档编写规范.md",
    "TCGA原始标杆对齐清单.md",
    "示例_学习型说明文_融合版.md",
    "学习型说明文人工审稿清单.md",
    "00_执行导航.md",
    "01_工程目录框架.md",
    "02_参数冻结总表.md",
    "03_命名与结果记录规范.md",
    "04_评估口径与官方脚本对齐.md",
    "05_代码工程映射与实现策略.md",
    "06_实验执行证据化写作模板.md",
    "07_实验执行全局修订与质检规范.md",
    "skill.md",
}
CANONICAL_GOVERNANCE_DOCS = {
    "global_skill": ".trae/skills/crc-gland-coding-guard/SKILL.md",
    "nav": "crc_gland_segmentation_project/.trae/skills/00_技能体系导航.md",
    "master": "crc_gland_segmentation_project/.trae/skills/论文实验项目文档编写规范_完整版.md",
    "impl": "crc_gland_segmentation_project/.trae/skills/实验执行文档编写规范.md",
    "tcga": "crc_gland_segmentation_project/.trae/skills/TCGA原始标杆对齐清单.md",
    "manual_review": "crc_gland_segmentation_project/.trae/skills/学习型说明文人工审稿清单.md",
}
COMMAND_ALIGNMENT_GOVERNANCE_KEYS = ("global_skill", "nav", "master", "impl")
GOVERNANCE_REQUIRED_MARKERS = {
    "global_skill": (
        "00_技能体系导航.md",
        "论文实验项目文档编写规范_完整版.md",
        "实验执行文档编写规范.md",
        "TCGA原始标杆对齐清单.md",
        "学习型说明文人工审稿清单.md",
        "Guard 留痕",
        "模板R_研究定标记录.md",
        "模板0_阶段实现卡.md",
        "学习型说明文",
        *COMMAND_SIGNATURES,
    ),
    "nav": (
        "00_技能体系导航.md",
        "研究定标记录.md",
        "模板R_研究定标记录.md",
        "模板0_阶段实现卡.md",
        "论文实验项目文档编写规范_完整版.md",
        "实验执行文档编写规范.md",
        "TCGA原始标杆对齐清单.md",
        "学习型说明文人工审稿清单.md",
        *COMMAND_SIGNATURES,
    ),
    "master": (
        "00_技能体系导航.md",
        "研究定标记录.md",
        "模板R_研究定标记录.md",
        "模板0_阶段实现卡.md",
        "实验执行文档编写规范.md",
        "TCGA原始标杆对齐清单.md",
        "学习型说明文人工审稿清单.md",
        *COMMAND_SIGNATURES,
    ),
    "impl": (
        "00_技能体系导航.md",
        "研究定标记录.md",
        "模板R_研究定标记录.md",
        "模板0_阶段实现卡.md",
        "模板1~10",
        "TCGA原始标杆对齐清单.md",
        "学习型说明文人工审稿清单.md",
        *COMMAND_SIGNATURES,
    ),
    "tcga": (
        "TCGA原始标杆对齐清单.md",
        "实验执行文档编写规范.md",
        "示例_学习型说明文_融合版.md",
        "学习型说明文人工审稿清单.md",
        "Post-QC Guard",
    ),
    "manual_review": (
        "学习型说明文人工审稿清单.md",
        "TCGA原始标杆对齐清单.md",
        "示例_学习型说明文_融合版.md",
        "b_class_auxiliary/tools/check_learning_docs.py",
        "Post-QC Guard",
    ),
}
DUAL_MODE_DOC_TYPES = {
    "template_stage_protocol",
    "template_design",
    "template_acceptance",
    "template_evidence",
    "stage_protocol",
    "design_basis",
    "stage_acceptance",
    "literature_evidence",
}
DUAL_MODE_TRIGGER_MARKERS = (
    "单文档双达标模式",
    "## 0. 先给结论",
    "仅在单文档双达标模式启用时强制",
)
DUAL_MODE_REQUIRED_MARKERS = {
    "设计取舍对比": (
        "候选方案对比",
        "为什么不选",
        "候选用法对比",
        "为什么不是只看单个最好数字",
        "不能只看单个最好数字",
        "不能只看 README",
        "不能只看 README 的一句话结论",
    ),
    "误区预防": (
        "高频误区",
        "误区预防",
        "误读提醒",
        "误判提醒",
        "最不能误判成",
    ),
    "联读顺序": (
        "联读顺序",
        "阅读顺序",
        "阅读路径",
        "如果你只想最快",
        "如果你只想最快读懂",
        "如果你只想最快理解",
    ),
    "收口自检": (
        "五分钟自检",
        "五分钟复核",
        "5~10 分钟自检动作",
        "5~10 分钟",
        "自检动作",
        "复核动作",
    ),
}
DUAL_MODE_CORRECTION_MARKERS = ("正确理解", "纠正", "不能", "不要", "误写", "误判", "误读", "越界")
DUAL_MODE_NAVIGATION_CUES = ("先读", "先看", "再读", "再看", "最后读", "最后看", "最后回看", "回到", "→")
DUAL_MODE_ACTION_VERBS = ("打开", "确认", "查看", "核对", "反查", "指出", "说清", "定位", "检查", "复述")
DUAL_MODE_EVIDENCE_HINTS = (
    "字段",
    "结论",
    "页码",
    "公式",
    "文件",
    "路径",
    "变量",
    "指标",
    "数字",
    "阶段",
    "代码位置",
    "run_meta.yaml",
    "val_metrics.csv",
    "test",
    "README",
    "implementation_status",
)
BULLET_LINE_PATTERN = re.compile(r"^(?:[-*]|\d+\.)\s+")
REPORT_GROUP_RULES = (
    (
        "章节与边界",
        ("关键章节", "角色边界", "边界声明", "前置依赖", "验收/回退", "门控", "通过标准"),
    ),
    (
        "证据与锚点",
        ("路径锚点", "来源/依据", "代码或工程落点", "真实存在路径锚点", "无法解析到真实文件"),
    ),
    (
        "状态口径",
        ("状态口径", "二元 diagnostics", "implementation_tracking", "Stage Gate", "Diagnostics"),
    ),
    (
        "治理一致性",
        ("治理文件", "自动门禁命令", "调用顺序", "共享门禁标记", "引用顺序发生反转"),
    ),
    (
        "双达标模式",
        ("单文档双达标模式", "先给结论", "设计取舍对比", "误区预防", "联读顺序", "收口自检", "人工终审", "人工审稿"),
    ),
)


@dataclass
class Issue:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate formal markdown docs updated in the current task."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--post-qc-guard",
        default="",
        help="Relative path to the task Post-QC Guard markdown file.",
    )
    parser.add_argument(
        "--docs",
        nargs="*",
        default=[],
        help="Optional additional markdown docs to validate.",
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional relative path for the generated report.",
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_changed_markdown_docs(post_qc_path: Path) -> list[str]:
    text = read_text(post_qc_path)
    lines = text.splitlines()
    start_index = -1
    for index, line in enumerate(lines):
        if line.strip() == "## 2. 实际创建/修改文件":
            start_index = index + 1
            break
    if start_index == -1:
        raise ValueError("Missing heading: ## 2. 实际创建/修改文件")

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
        raise ValueError("Missing markdown table under ## 2. 实际创建/修改文件")

    docs: list[str] = []
    for row in table_lines[2:]:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if not cells:
            continue
        path_value = normalize_relpath(cells[0])
        if path_value.endswith(".md"):
            docs.append(path_value)
    return docs


def is_formal_doc_candidate(path_value: str) -> bool:
    normalized = normalize_relpath(path_value)
    if not normalized.endswith(".md"):
        return False
    if "/_archive/" in normalized or normalized.startswith(".trae/skills/_archive/"):
        return False
    basename = Path(normalized).name
    if basename.startswith("示例"):
        return False
    if "终极版_part" in basename:
        return False
    if normalized.startswith(".trae/skills/") or "/.trae/skills/" in normalized:
        return True
    if "01_实验执行/" in normalized or "/01_实验执行/" in normalized:
        return True
    return False


def resolve_doc_path(project_root: Path, path_value: str) -> Path:
    normalized = normalize_relpath(path_value)
    path = Path(normalized)
    if path.is_absolute():
        return path.resolve()

    workspace_root = project_root.parent
    candidate_strings = (normalized, normalized.lstrip("./"))
    candidates: list[Path] = []
    for candidate_text in candidate_strings:
        candidate_path = Path(candidate_text)
        if candidate_path.is_absolute():
            candidates.append(candidate_path)
        candidates.append(project_root / candidate_text)
        candidates.append(workspace_root / candidate_text)
        if candidate_text.startswith(".trae/skills/"):
            candidates.append(workspace_root / candidate_text)

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return (project_root / normalized).resolve()


def display_path(project_root: Path, path: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return path.as_posix()


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


def extract_fenced_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    in_block = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if line.strip().startswith("```"):
            if in_block:
                blocks.append("\n".join(current))
                current = []
                in_block = False
            else:
                in_block = True
                current = []
            continue
        if in_block:
            current.append(line)
    return blocks


def extract_sections(text: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            if current_heading:
                sections.append((current_heading, current_lines))
            current_heading = stripped
            current_lines = []
            continue
        if current_heading:
            current_lines.append(raw_line)
    if current_heading:
        sections.append((current_heading, current_lines))
    return sections


def count_backticked_spans(text: str) -> int:
    return len(re.findall(r"`[^`\n]+`", text))


def find_sections_with_keywords(
    sections: list[tuple[str, list[str]]],
    keywords: tuple[str, ...],
) -> list[tuple[str, list[str]]]:
    matches: list[tuple[str, list[str]]] = []
    for heading, lines in sections:
        combined = heading + "\n" + "\n".join(lines)
        if any(keyword in combined for keyword in keywords):
            matches.append((heading, lines))
    return matches


def has_structured_comparison_signal(sections: list[tuple[str, list[str]]]) -> bool:
    for heading, lines in find_sections_with_keywords(sections, DUAL_MODE_REQUIRED_MARKERS["设计取舍对比"]):
        nonempty = [line.strip() for line in lines if line.strip()]
        combined = heading + "\n" + "\n".join(nonempty)
        if combined.count("|") >= 6:
            return True
        if any(
            marker in combined
            for marker in ("为什么不选", "本轮不选", "不采用", "不借哪部分", "不直接用", "不能只看")
        ):
            return True
    return False


def has_structured_misconception_signal(sections: list[tuple[str, list[str]]]) -> bool:
    for heading, lines in find_sections_with_keywords(sections, DUAL_MODE_REQUIRED_MARKERS["误区预防"]):
        nonempty = [line.strip() for line in lines if line.strip()]
        combined = heading + "\n" + "\n".join(nonempty)
        if any(marker in combined for marker in ("误区", "误读", "误判")) and any(
            marker in combined for marker in DUAL_MODE_CORRECTION_MARKERS
        ):
            return True
    return False


def has_structured_navigation_signal(sections: list[tuple[str, list[str]]]) -> bool:
    for heading, lines in find_sections_with_keywords(sections, DUAL_MODE_REQUIRED_MARKERS["联读顺序"]):
        nonempty = [line.strip() for line in lines if line.strip()]
        cue_lines = [line for line in nonempty if any(cue in line for cue in DUAL_MODE_NAVIGATION_CUES)]
        if not cue_lines:
            continue
        if sum(count_backticked_spans(line) for line in cue_lines) >= 2:
            return True
    return False


def has_structured_self_check_signal(sections: list[tuple[str, list[str]]]) -> bool:
    for heading, lines in find_sections_with_keywords(sections, DUAL_MODE_REQUIRED_MARKERS["收口自检"]):
        nonempty = [line.strip() for line in lines if line.strip()]
        concrete_lines = 0
        for line in nonempty:
            if not (
                any(keyword in line for keyword in ("自检", "复核"))
                or BULLET_LINE_PATTERN.match(line)
            ):
                continue
            if not any(verb in line for verb in DUAL_MODE_ACTION_VERBS):
                continue
            if count_backticked_spans(line) >= 1 or any(hint in line for hint in DUAL_MODE_EVIDENCE_HINTS):
                concrete_lines += 1
        if concrete_lines >= 2:
            return True
    return False


def build_analysis_text(doc_type: str, text: str) -> str:
    if doc_type.startswith("template_"):
        blocks = [block for block in extract_fenced_blocks(text) if block.strip()]
        if blocks:
            return text + "\n" + "\n".join(blocks)
    return text


def extract_path_anchors(text: str) -> list[str]:
    return [normalize_relpath(value) for value in PATH_ANCHOR_VALUE_PATTERN.findall(text)]


def is_likely_path_anchor(anchor: str) -> bool:
    normalized = normalize_relpath(anchor)
    lowered = normalized.lower()
    basename = Path(normalized).name.lower()
    if not normalized:
        return False
    if "~" in normalized:
        return False
    if normalized.startswith("testA/testB_"):
        return False
    if "/" not in normalized and "\\" not in normalized:
        if basename in SKIP_BARE_FILENAMES:
            return False
        if basename.endswith("_模板.md") or "终极版_part" in basename:
            return False
        if basename not in ALLOWED_BARE_FILENAMES:
            return False
    if re.search(r"\s/\s|\s\\\s", normalized):
        return False
    if normalized in STATE_SPACE_SIGNATURES:
        return False
    if lowered.startswith(("http://", "https://")):
        return False
    if Path(normalized).is_absolute():
        return True
    if normalized.startswith(PATH_LIKE_PREFIXES):
        return True
    return any(lowered.endswith(suffix) for suffix in PATH_LIKE_SUFFIXES)


def should_skip_anchor(anchor: str) -> bool:
    if not anchor:
        return True
    lowered = anchor.lower()
    if lowered.startswith(("http://", "https://")):
        return True
    if not is_likely_path_anchor(anchor):
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
    project_skill_root = project_root / ".trae" / "skills"
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
        candidates.append(project_skill_root / candidate_text)
        if "终极版_part" in candidate_text and "/_archive/" not in candidate_text:
            candidates.append(project_skill_root / "_archive" / Path(candidate_text).name)

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists():
            return candidate.resolve()
    return None


def classify_doc_type(path_value: str) -> str:
    name = Path(path_value).name
    normalized = normalize_relpath(path_value)

    if name == "TCGA原始标杆对齐清单.md":
        return "tcga_benchmark_checklist"
    if name == "学习型说明文人工审稿清单.md":
        return "manual_review_checklist"
    if name in {"SKILL.md", "00_技能体系导航.md", "论文实验项目文档编写规范_完整版.md", "实验执行文档编写规范.md"}:
        return "governance"
    if name.startswith("模板R_"):
        return "template_research_record"
    if name.startswith("模板0_"):
        return "template_stage_card"
    if name == "研究定标记录.md":
        return "research_record"
    if name.startswith("模板1_"):
        return "template_stage_protocol"
    if name.startswith("模板2_"):
        return "template_design"
    if name.startswith("模板3"):
        return "template_acceptance"
    if name.startswith("模板4_"):
        return "template_evidence"
    if re.match(r"模板[5-8]_.*", name):
        return "template_precheck_guard"
    if re.match(r"模板9_.*|模板10_.*", name):
        return "template_post_guard"
    if name == "00_阶段总协议.md" or "阶段总协议" in name:
        return "stage_protocol"
    if "设计依据" in name:
        return "design_basis"
    if "阶段验收" in name:
        return "stage_acceptance"
    if "文献证据" in name or "提取" in name:
        return "literature_evidence"
    if normalized.startswith(".trae/skills/") or "/.trae/skills/" in normalized:
        return "governance"
    return "stage_protocol"


def analyze_sections(path_value: str, text: str, doc_type: str) -> list[Issue]:
    issues: list[Issue] = []
    for group_name, heading_group in SECTION_RULES.get(doc_type, ()):
        if not any(heading in text for heading in heading_group):
            issues.append(
                Issue(
                    "partial",
                    f"文档 `{path_value}` 缺少 `{group_name}` 类关键章节。",
                )
            )
    return issues


def analyze_evidence(path_value: str, text: str, doc_type: str) -> list[Issue]:
    issues: list[Issue] = []
    meaningful_lines = count_meaningful_lines(text)
    minimum = MIN_MEANINGFUL_LINES.get(doc_type)
    if minimum is not None and meaningful_lines < minimum:
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 的有效正文行数为 `{meaningful_lines}`，低于要求 `{minimum}`。",
            )
        )

    minimum_path_anchors = MIN_PATH_ANCHOR_COUNTS.get(doc_type, 2)
    path_anchor_count = sum(
        1 for anchor in extract_path_anchors(text) if is_likely_path_anchor(anchor)
    )
    if path_anchor_count < minimum_path_anchors:
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 的路径锚点数为 `{path_anchor_count}`，低于最小要求 `{minimum_path_anchors}`。",
            )
        )

    if not any(keyword in text for keyword in SOURCE_KEYWORDS):
        issues.append(Issue("partial", f"文档 `{path_value}` 缺少来源/依据痕迹。"))
    if not any(keyword in text for keyword in BOUNDARY_KEYWORDS):
        issues.append(Issue("partial", f"文档 `{path_value}` 缺少边界声明痕迹。"))
    if not any(keyword in text for keyword in CODE_KEYWORDS):
        issues.append(Issue("partial", f"文档 `{path_value}` 缺少代码或工程落点痕迹。"))
    if not any(keyword in text for keyword in VALIDATION_KEYWORDS):
        issues.append(Issue("partial", f"文档 `{path_value}` 缺少验收/回退/质检痕迹。"))

    if doc_type in {"governance", "tcga_benchmark_checklist", "manual_review_checklist"} and not all(signature in text for signature in STATE_SPACE_SIGNATURES):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 未完整覆盖当前正式状态口径（Stage Gate / Diagnostics / implementation_tracking 三套状态空间）。",
            )
        )
    if doc_type == "template_post_guard" and STATE_SPACE_SIGNATURES[1] not in text:
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 未覆盖正式 diagnostics 状态口径 `pass / partial / fail / not_applicable`。",
            )
        )

    if doc_type != "template_guard" and re.search(
        r"(?im)^\s*-\s*[^:\n]+:\s*(?:\[\s*\]\s*pass\s*/\s*\[\s*\]\s*fail|\[\s*pass\s*/\s*fail\s*\]|pass\s*/\s*fail)\s*$",
        text,
    ):
        issues.append(
            Issue(
                "fail",
                f"文档 `{path_value}` 仍残留二元 diagnostics 占位写法（如 `pass / fail`），会把正式状态口径带偏。",
            )
        )

    return issues


def analyze_state_semantics(path_value: str, text: str) -> list[Issue]:
    issues: list[Issue] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if STATE_SPACE_SIGNATURES[1] not in line:
            continue
        if not any(target in line for target in IMPLEMENTATION_TRACKING_ENTRY_TARGETS):
            continue
        if any(guardrail in line for guardrail in STATE_SEMANTIC_GUARDRAILS):
            continue
        issues.append(
            Issue(
                "fail",
                f"文档 `{path_value}` 把 Diagnostics 状态口径 `{STATE_SPACE_SIGNATURES[1]}` "
                "直接挂到了 `implementation_tracking` 阶段入口语义上；"
                "阶段入口只能使用 `not_started / blocked / partial / pass`。",
            )
        )
        break
    return issues


def analyze_anchor_resolution(project_root: Path, doc_path: Path, text: str) -> list[Issue]:
    issues: list[Issue] = []
    anchors = extract_path_anchors(text)
    resolved: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()
    for anchor in anchors:
        if anchor in seen or should_skip_anchor(anchor):
            continue
        seen.add(anchor)
        if resolve_anchor_path(project_root, doc_path, anchor) is not None:
            resolved.append(anchor)
        else:
            missing.append(anchor)

    minimum_existing = MIN_RESOLVED_PATH_ANCHOR_COUNTS.get(
        classify_doc_type(display_path(project_root, doc_path)),
        2,
    )
    if len(resolved) < minimum_existing:
        issues.append(
            Issue(
                "partial",
                f"文档 `{display_path(project_root, doc_path)}` 的真实存在路径锚点数为 `{len(resolved)}`，低于最小要求 `{minimum_existing}`。",
            )
        )
    if missing:
        sample = "`, `".join(missing[:5])
        issues.append(
            Issue(
                "partial",
                f"文档 `{display_path(project_root, doc_path)}` 存在无法解析到真实文件的路径锚点: `{sample}`。",
            )
        )
    return issues


def uses_dual_mode(doc_type: str, text: str) -> bool:
    return doc_type in DUAL_MODE_DOC_TYPES and any(marker in text for marker in DUAL_MODE_TRIGGER_MARKERS)


def analyze_dual_mode_signals(path_value: str, text: str, doc_type: str) -> list[Issue]:
    if not uses_dual_mode(doc_type, text):
        return []

    issues: list[Issue] = []
    if "学习型说明文人工审稿清单.md" not in text:
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但没有回链 `学习型说明文人工审稿清单.md`。",
            )
        )

    sections = extract_sections(text)
    conclusion_section = next(
        (body for heading, body in sections if heading.startswith("## 0. 先给结论")),
        None,
    )
    if conclusion_section is None:
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但缺少 `## 0. 先给结论` 章节。",
            )
        )
    else:
        lead_lines = [line.strip() for line in conclusion_section if line.strip()][:6]
        if not lead_lines or not any(line.startswith(("-", "*", ">")) for line in lead_lines):
            issues.append(
                Issue(
                    "partial",
                    f"文档 `{path_value}` 的 `## 0. 先给结论` 章节没有在开头给出清晰的结论型 bullet。",
                )
            )
        bullet_like_lines = [line for line in lead_lines if BULLET_LINE_PATTERN.match(line) or line.startswith(">")]
        if len(bullet_like_lines) < 3:
            issues.append(
                Issue(
                    "partial",
                    f"文档 `{path_value}` 的 `## 0. 先给结论` 章节结论型 bullet 数为 `{len(bullet_like_lines)}`，低于最小要求 `3`。",
                )
            )

    for signal_name, keywords in DUAL_MODE_REQUIRED_MARKERS.items():
        if not any(keyword in text for keyword in keywords):
            sample = " / ".join(keywords[:3])
            issues.append(
                Issue(
                    "partial",
                    f"文档 `{path_value}` 启用了单文档双达标模式，但缺少 `{signal_name}` 信号（至少应出现 `{sample}` 一类表达）。",
                )
            )

    if "学习型说明文人工审稿清单.md" in text and not any(marker in text for marker in ("人工终审", "人工审稿")):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 虽然回链了 `学习型说明文人工审稿清单.md`，但没有明确写出人工终审/人工审稿动作。",
            )
        )

    if not has_structured_comparison_signal(sections):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但“设计取舍对比”仍不够结构化；至少要有对比表或显式的“为什么不选/本轮不选”说明。",
            )
        )
    if not has_structured_misconception_signal(sections):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但“误区预防”仍不够结构化；至少要同时出现误区描述和纠正/正确理解。",
            )
        )
    if not has_structured_navigation_signal(sections):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但“联读顺序”仍不够具体；至少要给出带顺序词和可定位目标的阅读路径。",
            )
        )
    if not has_structured_self_check_signal(sections):
        issues.append(
            Issue(
                "partial",
                f"文档 `{path_value}` 启用了单文档双达标模式，但“收口自检”仍不够可验证；至少要给出 2 条带动作词和证据对象的自检/复核步骤。",
            )
        )

    return issues


def canonical_governance_paths(project_root: Path) -> dict[str, Path]:
    workspace_root = project_root.parent
    return {
        key: (workspace_root / rel_path).resolve()
        for key, rel_path in CANONICAL_GOVERNANCE_DOCS.items()
    }


def requires_governance_consistency_check(project_root: Path, docs: list[Path]) -> bool:
    canonical_paths = {path.resolve() for path in canonical_governance_paths(project_root).values()}
    governance_doc_types = {"governance", "tcga_benchmark_checklist", "manual_review_checklist"}
    return any(
        doc.resolve() in canonical_paths or classify_doc_type(display_path(project_root, doc)) in governance_doc_types
        for doc in docs
    )


def analyze_governance_consistency(project_root: Path, docs: list[Path]) -> list[Issue]:
    if not requires_governance_consistency_check(project_root, docs):
        return []

    issues: list[Issue] = []
    canonical_paths = canonical_governance_paths(project_root)
    canonical_texts: dict[str, str] = {}

    for key, path in canonical_paths.items():
        if not path.exists():
            issues.append(Issue("fail", f"治理文件缺失: `{display_path(project_root, path)}`"))
            continue
        canonical_texts[key] = read_text(path)

    for key, text in canonical_texts.items():
        for signature in STATE_SPACE_SIGNATURES:
            if signature not in text:
                issues.append(
                    Issue(
                        "partial",
                        f"治理文件 `{display_path(project_root, canonical_paths[key])}` 缺少正式状态口径 `{signature}`。",
                    )
                )
        for marker in GOVERNANCE_REQUIRED_MARKERS[key]:
            if marker not in text:
                issues.append(
                    Issue(
                        "partial",
                        f"治理文件 `{display_path(project_root, canonical_paths[key])}` 缺少共享门禁标记 `{marker}`。",
                    )
                )
        nav_index = text.find("00_技能体系导航.md")
        master_index = text.find("论文实验项目文档编写规范_完整版.md")
        if nav_index != -1 and master_index != -1 and nav_index > master_index:
            issues.append(
                Issue(
                    "partial",
                    f"治理文件 `{display_path(project_root, canonical_paths[key])}` 中导航与总规范的引用顺序发生反转。",
                )
            )

    command_alignment_texts = {
        key: text for key, text in canonical_texts.items() if key in COMMAND_ALIGNMENT_GOVERNANCE_KEYS
    }
    if command_alignment_texts:
        command_presence = {
            command: [key for key, text in command_alignment_texts.items() if command in text]
            for command in COMMAND_SIGNATURES
        }
        for command, holders in command_presence.items():
            if len(holders) != len(command_alignment_texts):
                issues.append(
                    Issue(
                        "partial",
                        f"核心治理文件组没有共同覆盖自动门禁命令 `{command}`，当前命中文件数为 `{len(holders)}`。",
                    )
                )

    return issues


def evaluate_docs(project_root: Path, docs: list[Path]) -> tuple[str, list[str]]:
    issues: list[Issue] = []
    candidate_docs = [doc for doc in docs if is_formal_doc_candidate(display_path(project_root, doc))]

    for doc_path in candidate_docs:
        if not doc_path.exists():
            issues.append(Issue("fail", f"文档不存在: `{display_path(project_root, doc_path)}`"))
            continue
        rel_display = display_path(project_root, doc_path)
        text = read_text(doc_path)
        doc_type = classify_doc_type(rel_display)
        analysis_text = build_analysis_text(doc_type, text)
        issues.extend(analyze_sections(rel_display, analysis_text, doc_type))
        issues.extend(analyze_evidence(rel_display, analysis_text, doc_type))
        issues.extend(analyze_state_semantics(rel_display, analysis_text))
        issues.extend(analyze_anchor_resolution(project_root, doc_path, analysis_text))
        issues.extend(analyze_dual_mode_signals(rel_display, analysis_text, doc_type))

    issues.extend(analyze_governance_consistency(project_root, candidate_docs))

    detail_lines = [f"- [{issue.severity}] {issue.message}" for issue in issues]
    if any(issue.severity == "fail" for issue in issues):
        return "fail", detail_lines
    if any(issue.severity == "partial" for issue in issues):
        return "partial", detail_lines
    if not candidate_docs:
        return "not_applicable", ["- [not_applicable] 本轮没有命中正式模板/规程/协议文档。"]
    return "pass", ["- [pass] 正式模板/规程/协议文档的关键章节、边界、代码落点与质检痕迹检查通过。"]


def build_report(
    project_root: Path,
    docs: list[Path],
    status: str,
    details: Iterable[str],
) -> str:
    detail_list = list(details)
    lines = [
        "# Formal Doc Gate Report",
        "",
        "## 1. 输入文档",
    ]
    for doc in docs:
        lines.append(f"- `{display_path(project_root, doc)}`")
    lines.extend(
        [
            "",
            "## 2. 检查范围",
            "- 检查正式模板/规程/协议文档是否缺少关键章节骨架。",
            "- 检查文档是否同时回答了角色边界、前置依赖、规则或证据、代码或工程落点、验收或回退。",
            "- 检查文档是否保留当前正式状态口径，而不是回退到旧二元写法。",
            "- 检查文档中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。",
            "- 检查治理文件组（中央 SKILL / 导航 / 总规范 / implementation_tracking 规程）是否共同覆盖状态口径、自动门禁命令和调用顺序。",
            "- 检查文档是否留下了最小路径锚点、来源锚点和质检痕迹。",
            "- 对启用了“单文档双达标模式”的正式文档，额外检查下面这些教学信号是否达到最小可执行强度：",
            "- `## 0. 先给结论` 是否存在，且开头至少有 3 条结论型 bullet。",
            "- `设计取舍对比` 是否是结构化对比，而不是只写一句“最后选了什么”。",
            "- `误区预防` 是否同时给出误区/误判和对应的纠正或正确理解。",
            "- `联读顺序` 是否给出带顺序词和可定位目标的真实阅读路径。",
            "- `收口自检` 是否给出至少 2 条带动作词和证据对象的自检/复核步骤。",
            "- `学习型说明文人工审稿清单.md` 是否不仅被回链，还明确出现人工终审/人工审稿动作。",
            "",
            "## 3. 结论",
            f"- `formal_doc_gate_status`: `{status}`",
            "",
            "## 4. 检查摘要",
            "",
        ]
    )
    if status == "pass":
        lines.extend(
            [
                "- `章节与边界`: 未发现 formal gate 异常。",
                "- `证据与锚点`: 未发现 formal gate 异常。",
                "- `状态口径`: 未发现 formal gate 异常。",
                "- `治理一致性`: 未发现 formal gate 异常。",
                "- `双达标模式`: 未发现 formal gate 异常。",
            ]
        )
    elif status == "not_applicable":
        lines.append("- `总体`: 本轮没有命中正式模板/规程/协议文档。")
    else:
        grouped: dict[str, list[str]] = {group_name: [] for group_name, _ in REPORT_GROUP_RULES}
        grouped["其他"] = []
        for detail in detail_list:
            matched = False
            for group_name, keywords in REPORT_GROUP_RULES:
                if any(keyword in detail for keyword in keywords):
                    grouped[group_name].append(detail)
                    matched = True
                    break
            if not matched:
                grouped["其他"].append(detail)

        for group_name in [name for name, _ in REPORT_GROUP_RULES] + ["其他"]:
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
    docs: list[Path] = []

    if args.post_qc_guard:
        post_qc_path = (project_root / normalize_relpath(args.post_qc_guard)).resolve()
        if not post_qc_path.exists():
            raise FileNotFoundError(f"Post-QC guard not found: {post_qc_path}")
        docs.extend(resolve_doc_path(project_root, value) for value in extract_changed_markdown_docs(post_qc_path))

    docs.extend(resolve_doc_path(project_root, value) for value in args.docs)
    unique_docs = list(dict.fromkeys(doc.resolve() for doc in docs))

    status, details = evaluate_docs(project_root, unique_docs)
    if args.output:
        output_path = (project_root / normalize_relpath(args.output)).resolve()
    elif args.post_qc_guard:
        post_qc_path = (project_root / normalize_relpath(args.post_qc_guard)).resolve()
        output_path = post_qc_path.parent / "formal_doc_gate_report.md"
    else:
        output_path = project_root / "formal_doc_gate_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_report(project_root, unique_docs, status, details), encoding="utf-8")

    print(f"formal_doc_gate_status={status}")
    print(f"wrote_report={output_path}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
