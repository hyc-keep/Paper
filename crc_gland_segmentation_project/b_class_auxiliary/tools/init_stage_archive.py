"""Initialize a per-stage implementation archive and an optional current-copy stub."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize stage archive scaffolding for 实现依据记录.md."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--stage-name",
        required=True,
        help="Current numbered stage name, for example `02_UNet流程验证`.",
    )
    parser.add_argument(
        "--reconstructed",
        action="store_true",
        help="Create the stage archive as a reconstructed archive instead of a fresh archive.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the stage archive if it already exists.",
    )
    parser.add_argument(
        "--root-copy-mode",
        choices=("skip", "init_if_missing", "sync"),
        default="init_if_missing",
        help=(
            "How to handle b_class_auxiliary/runtime_checks/实现依据记录.md: "
            "`skip` leaves it untouched, `init_if_missing` only creates it when absent, "
            "`sync` rewrites it as the current-stage copy stub."
        ),
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def stage_archive_relpath(stage_name: str) -> str:
    normalized_stage = normalize_relpath(stage_name)
    return f"reports/stage_reports/implementation_tracking/{normalized_stage}/实现依据记录.md"


def extract_template_body(template_text: str) -> str:
    match = re.search(r"(?ms)^## 1\. 角色/入口\s*$.*\Z", template_text)
    if not match:
        raise ValueError("Template is missing `## 1. 角色/入口` section.")
    return match.group(0).rstrip() + "\n"


def fill_stage_placeholders(body: str, stage_name: str) -> str:
    body = body.replace("- 当前阶段:\n", f"- 当前阶段: `{stage_name}`\n", 1)
    body = body.replace("- 当前任务:\n", "- 当前任务: `待填写`\n", 1)
    body = body.replace("- 当前记录只负责:\n", "- 当前记录只负责: `待填写`\n", 1)
    body = body.replace("- 当前记录不负责:\n", "- 当前记录不负责: `待填写`\n", 1)
    return body


def build_stage_archive_text(project_root: Path, template_text: str, stage_name: str, reconstructed: bool) -> str:
    archive_rel = stage_archive_relpath(stage_name)
    archive_kind = "重建归档版" if reconstructed else "阶段归档版"
    title = f"# 实现依据记录（{archive_kind}）"
    intro_lines = [
        title,
        "",
        "## 0. 归档说明",
        "",
        f"- 当前文件角色: `{archive_kind}`",
        f"- 当前对应阶段: `{stage_name}`",
        f"- 当前阶段归档路径: `{archive_rel}`",
    ]
    if reconstructed:
        intro_lines.extend(
            [
                "- 当前归档说明: `这是依据现存正式产物与门禁证据重建的阶段归档版，不是逐字原件。`",
                "- 当前可恢复边界: `需由重建者补充 surviving evidence、可恢复范围与不能宣称成立的边界。`",
            ]
        )
    else:
        intro_lines.extend(
            [
                "- 当前归档说明: `这是当前阶段的独立正式归档，后续阶段不得覆盖。`",
                "- 当前可恢复边界: `not_applicable`",
            ]
        )
    intro_lines.append("")
    body = fill_stage_placeholders(extract_template_body(template_text), stage_name)
    return "\n".join(intro_lines) + body


def list_existing_stage_archives(project_root: Path) -> list[str]:
    root = project_root / "reports" / "stage_reports" / "implementation_tracking"
    archives: list[str] = []
    if not root.exists():
        return archives
    for candidate in sorted(root.glob("*/实现依据记录.md")):
        archives.append(candidate.relative_to(project_root).as_posix())
    return archives


def build_root_copy_text(project_root: Path, template_text: str, stage_name: str) -> str:
    title = "# 实现依据记录"
    archive_rel = stage_archive_relpath(stage_name)
    history_lines = list_existing_stage_archives(project_root)
    intro_lines = [
        title,
        "",
        "## 0. 当前副本说明",
        "",
        "- 当前文件角色: `当前阶段副本`",
        f"- 当前对应阶段: `{stage_name}`",
        f"- 当前阶段归档路径: `{archive_rel}`",
        "- 历史阶段归档路径:",
    ]
    if history_lines:
        intro_lines.extend(f"  - `{item}`" for item in history_lines)
    else:
        intro_lines.append("  - `待创建`")
    intro_lines.extend(
        [
            "- 维护规则:",
            "  - 后续新阶段必须先在对应阶段目录创建独立 `实现依据记录.md`",
            "  - 当前根路径文件只保留为“当前阶段副本”，不再作为跨阶段唯一真本",
            "  - 禁止再用当前文件覆盖旧阶段归档",
            "",
        ]
    )
    body = fill_stage_placeholders(extract_template_body(template_text), stage_name)
    return "\n".join(intro_lines) + body


def write_if_needed(path: Path, text: str, force: bool) -> str:
    existed_before = path.exists()
    if existed_before and not force:
        return "exists"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return "updated" if existed_before else "created"


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    stage_name = normalize_relpath(args.stage_name)
    template_path = project_root / ".trae" / "skills" / "模板I_实现依据记录.md"
    template_text = read_text(template_path)

    archive_path = (project_root / stage_archive_relpath(stage_name)).resolve()
    archive_text = build_stage_archive_text(project_root, template_text, stage_name, args.reconstructed)
    archive_status = write_if_needed(archive_path, archive_text, args.force)

    root_copy_path = (project_root / "b_class_auxiliary" / "runtime_checks" / "实现依据记录.md").resolve()
    root_copy_status = "skipped"
    if args.root_copy_mode == "sync":
        root_copy_text = build_root_copy_text(project_root, template_text, stage_name)
        root_copy_status = write_if_needed(root_copy_path, root_copy_text, True)
    elif args.root_copy_mode == "init_if_missing" and not root_copy_path.exists():
        root_copy_text = build_root_copy_text(project_root, template_text, stage_name)
        root_copy_status = write_if_needed(root_copy_path, root_copy_text, False)

    print(f"stage_archive_status={archive_status}")
    print(f"stage_archive_path={archive_path.as_posix()}")
    print(f"root_copy_status={root_copy_status}")
    print(f"root_copy_path={root_copy_path.as_posix()}")


if __name__ == "__main__":
    main()
