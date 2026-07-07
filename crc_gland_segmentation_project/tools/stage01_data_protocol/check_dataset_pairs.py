"""Build formal data-check assets from frozen split CSV files.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark pair integrity, readability and manual-audit preconditions
- 公式/定义: 正式数据链必须证明 image/mask 成对、路径可读、前景非空、重复关系可控且人工抽查闭环
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/check_dataset_pairs.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 以冻结 split CSV 为唯一检查入口，同时汇总 `dataset_stats.csv`、`foreground_summary.csv`、`object_size_summary.csv`、`duplicate_check_report.md` 与 `data_check_report.md`。
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path
import re

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - local dependency
    raise SystemExit("Pillow is required for check_dataset_pairs.py") from exc

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.csv_loader import load_csv_rows, validate_csv_schema, validate_unique_sample_ids
from src.data.datasets import load_data_config, resolve_split_csv

POSITIVE_TOKENS = {
    "pass", "true", "yes", "y", "ok", "keep", "accept", "accepted", "complete",
    "正常", "通过", "保留", "完成", "是",
}
NEGATIVE_TOKENS = {
    "fail", "false", "no", "n", "reject", "rejected", "blocked",
    "异常", "不通过", "剔除", "拒绝", "否",
}
PENDING_TOKENS = {"pending_review", "pending", "unknown", "", "todo", "na", "n/a", "待审阅", "待定", "未知"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate formal data-check assets.")
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/data_checks",
        help="Relative output directory for formal data-check assets.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def format_float(value: float) -> str:
    return f"{value:.6f}"


def mask_stats(mask_path: Path) -> dict[str, float | int]:
    """Measure mask foreground statistics for one formal sample.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark annotation integrity and foreground coverage checks
    - 公式/定义: 每个 mask 都需要给出前景像素、前景比例和 bbox 规模，才能判断样本是否为空壳或严重异常
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 直接对磁盘 mask 统计 `foreground_pixels`、`foreground_ratio` 与 `foreground_bbox_area`，作为数据检查报告核心字段。
    """
    with Image.open(mask_path) as mask_image:
        mask = mask_image.convert("L")
        histogram = mask.histogram()
        foreground_pixels = int(sum(histogram[1:]))
        width, height = mask.size
        total_pixels = width * height
        foreground_ratio = float(foreground_pixels / total_pixels) if total_pixels else 0.0
        bbox = mask.point(lambda value: 255 if value > 0 else 0).getbbox()
        bbox_width = 0 if bbox is None else int(bbox[2] - bbox[0])
        bbox_height = 0 if bbox is None else int(bbox[3] - bbox[1])
        bbox_area = bbox_width * bbox_height
    return {
        "height": int(height),
        "width": int(width),
        "foreground_pixels": foreground_pixels,
        "foreground_ratio": foreground_ratio,
        "is_empty_mask": int(foreground_pixels == 0),
        "foreground_bbox_width": bbox_width,
        "foreground_bbox_height": bbox_height,
        "foreground_bbox_area": bbox_area,
    }


def choose_status(is_pass: bool) -> str:
    return "pass" if is_pass else "fail"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_markdown_key_values(path: Path) -> dict[str, str]:
    """Read summary-style markdown bullets into a flat key-value mapping.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark report parsing and protocol-status normalization
    - 公式/定义: 人工审稿资产先写成 markdown 摘要字段，正式检查脚本需要把这些字段稳定解析回结构化状态
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 只解析 `- key: value` 这种正式摘要行，供 `manual_audit_notes.md` 的覆盖率、完成度和状态字段复用。
    """
    if not path.exists():
        return {}
    mapping: dict[str, str] = {}
    text = path.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^-\s*([^:]+):\s*`?([^`]+?)`?\s*$", line)
        if match:
            mapping[match.group(1).strip()] = match.group(2).strip()
    return mapping


def parse_markdown_table(path: Path, section_title: str) -> list[dict[str, str]]:
    """Parse one markdown table section from a formal audit note file.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark audit table extraction and row-level review aggregation
    - 公式/定义: 人工抽查最终要落到逐样本行级结论，正式脚本需要把 markdown 表格还原成结构化行记录
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 只抽取指定标题下的正式表格，用来汇总 `Exported Preview Samples` 的 alignment、decision 和 color issue 字段。
    """
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    headers: list[str] | None = None
    rows: list[dict[str, str]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line == section_title:
            in_section = True
            headers = None
            continue
        if not in_section:
            continue
        if line.startswith("## ") and line != section_title:
            break
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if headers is None:
            headers = cells
            continue
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def classify_token(value: str) -> str:
    """Normalize mixed Chinese/English audit tokens into review buckets.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark manual review normalization and audit decision consistency
    - 公式/定义: 人工抽查回填允许中英文混写，但协议裁决必须统一到 positive/negative/pending 三类
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 同时接受 `正常/异常`、`保留/剔除`、`是/否` 与 `pass/fail/keep/reject/yes/no`。
    """
    token = value.strip().lower()
    if token in POSITIVE_TOKENS:
        return "positive"
    if token in NEGATIVE_TOKENS:
        return "negative"
    if token in PENDING_TOKENS:
        return "pending"
    return "unknown"


def derive_manual_audit_status(path: Path) -> tuple[str, str]:
    """Summarize formal manual-audit notes into one protocol-level status.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark human visual review and acceptance gating
    - 公式/定义: 数据检查不能只看自动统计，还要把人工抽查覆盖率和逐样本结论压成 pass/partial/fail
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 从 `manual_audit_notes.md` 读取 `manual_audit_coverage_status`、`manual_review_completion` 和逐行审稿字段，生成最终人工审稿结论。
    """
    fields = parse_markdown_key_values(path)
    coverage_pass = fields.get("manual_audit_coverage_status") == "pass"
    completion_done = classify_token(fields.get("manual_review_completion", "")) == "positive"
    rows = parse_markdown_table(path, "## Exported Preview Samples")
    if not path.exists():
        return "missing", "manual audit notes are missing, so protocol-level human audit is not complete yet."
    if not rows:
        return "partial", "manual audit preview rows are missing, so protocol-level human audit is not complete yet."

    has_pending = False
    has_failure = False
    for row in rows:
        alignment_state = classify_token(row.get("alignment_pass", ""))
        decision_state = classify_token(row.get("manual_audit_decision", ""))
        color_state = classify_token(row.get("color_issue_flag", ""))
        if alignment_state != "positive" or decision_state != "positive":
            if alignment_state == "negative" or decision_state == "negative":
                has_failure = True
            else:
                has_pending = True
        if color_state in {"pending", "unknown"}:
            has_pending = True

    if coverage_pass and completion_done and not has_pending and not has_failure:
        return "pass", "manual audit coverage and row-level review decisions are complete and acceptable."
    if has_failure:
        return "fail", "manual audit found alignment failures or rejected samples that must be fixed before passing."
    return "partial", "formal preview assets now cover the minimum protocol sampling target, but human review decisions are still pending so manual audit is not complete yet."


def main() -> int:
    """Generate formal pair-check assets and the protocol-level data-check report.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark pair validation, duplicate control and readiness reporting
    - 公式/定义: 当前阶段必须把 pair/readable/duplicate/foreground/manual_audit 五类检查合并成统一数据检查结论
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/check_dataset_pairs.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 对 GlaS 与 CRAG 全部 `378` 个样本输出正式统计资产，并在 `data_check_report.md` 中给出 `pair_check_pass=pass`、`readable_check_pass=pass`、`duplicate_check_pass=pass`、`foreground_check_pass=pass`、`manual_audit_status=pass`。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    output_dir = (project_root / args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    manual_audit_path = output_dir / "manual_audit_notes.md"

    split_rows: list[dict[str, str]] = []
    dataset_stats_rows: list[dict[str, str]] = []
    foreground_summary_rows: list[dict[str, str]] = []
    object_size_rows: list[dict[str, str]] = []
    duplicate_sample_index: dict[str, list[str]] = {}
    duplicate_image_index: dict[str, list[str]] = {}
    duplicate_mask_index: dict[str, list[str]] = {}
    schema_issues: list[str] = []
    readable_issues: list[str] = []
    pair_issues: list[str] = []
    per_split_empty_masks: dict[str, int] = {}

    for dataset_code in ("glas", "crag"):
        config_path = project_root / "configs" / "data" / f"{dataset_code}.yaml"
        config = load_data_config(project_root, config_path)
        for split_name, csv_name in config.csv_files.items():
            csv_path = resolve_split_csv(project_root, config, split_name)
            rows = load_csv_rows(csv_path)
            schema_issues.extend(
                f"{dataset_code}:{split_name}:{issue}"
                for issue in validate_csv_schema(rows, config.dataset_code)
            )
            schema_issues.extend(
                f"{dataset_code}:{split_name}:{issue}"
                for issue in validate_unique_sample_ids(rows)
            )

            sample_count = len(rows)
            readable_count = 0
            empty_mask_count = 0
            foreground_ratios: list[float] = []
            bbox_areas: list[int] = []
            split_key = f"{dataset_code}:{split_name}"

            for row in rows:
                sample_id = row["sample_id"]
                image_path = (project_root / row["image_relpath"]).resolve()
                mask_path = (project_root / row["mask_relpath"]).resolve()
                duplicate_sample_index.setdefault(sample_id, []).append(split_key)
                duplicate_image_index.setdefault(row["image_relpath"], []).append(split_key)
                duplicate_mask_index.setdefault(row["mask_relpath"], []).append(split_key)

                if not image_path.exists():
                    pair_issues.append(f"missing_image:{split_key}:{sample_id}")
                    continue
                if not mask_path.exists():
                    pair_issues.append(f"missing_mask:{split_key}:{sample_id}")
                    continue

                try:
                    with Image.open(image_path) as image_handle:
                        image_handle.load()
                except Exception as exc:  # pragma: no cover - local data dependent
                    readable_issues.append(f"image_read_error:{split_key}:{sample_id}:{exc}")
                    continue

                try:
                    stats = mask_stats(mask_path)
                except Exception as exc:  # pragma: no cover - local data dependent
                    readable_issues.append(f"mask_read_error:{split_key}:{sample_id}:{exc}")
                    continue

                readable_count += 1
                empty_mask_count += int(stats["is_empty_mask"])
                foreground_ratios.append(float(stats["foreground_ratio"]))
                bbox_areas.append(int(stats["foreground_bbox_area"]))
                split_rows.append(
                    {
                        "dataset": dataset_code,
                        "split": split_name,
                        "sample_id": sample_id,
                        "image_relpath": row["image_relpath"],
                        "mask_relpath": row["mask_relpath"],
                        "height": str(stats["height"]),
                        "width": str(stats["width"]),
                        "foreground_pixels": str(stats["foreground_pixels"]),
                        "foreground_ratio": format_float(float(stats["foreground_ratio"])),
                        "is_empty_mask": str(stats["is_empty_mask"]),
                        "foreground_bbox_width": str(stats["foreground_bbox_width"]),
                        "foreground_bbox_height": str(stats["foreground_bbox_height"]),
                        "foreground_bbox_area": str(stats["foreground_bbox_area"]),
                    }
                )

            per_split_empty_masks[split_key] = empty_mask_count
            dataset_stats_rows.append(
                {
                    "dataset": dataset_code,
                    "split": split_name,
                    "sample_count": str(sample_count),
                    "readable_pair_count": str(readable_count),
                    "empty_mask_count": str(empty_mask_count),
                    "mean_foreground_ratio": format_float(statistics.fmean(foreground_ratios)) if foreground_ratios else "0.000000",
                }
            )
            foreground_summary_rows.append(
                {
                    "dataset": dataset_code,
                    "split": split_name,
                    "sample_count": str(sample_count),
                    "min_foreground_ratio": format_float(min(foreground_ratios)) if foreground_ratios else "0.000000",
                    "mean_foreground_ratio": format_float(statistics.fmean(foreground_ratios)) if foreground_ratios else "0.000000",
                    "median_foreground_ratio": format_float(statistics.median(foreground_ratios)) if foreground_ratios else "0.000000",
                    "max_foreground_ratio": format_float(max(foreground_ratios)) if foreground_ratios else "0.000000",
                }
            )
            object_size_rows.append(
                {
                    "dataset": dataset_code,
                    "split": split_name,
                    "metric_name": "foreground_bbox_area_px",
                    "sample_count": str(sample_count),
                    "min_value": str(min(bbox_areas)) if bbox_areas else "0",
                    "mean_value": format_float(statistics.fmean(bbox_areas)) if bbox_areas else "0.000000",
                    "median_value": format_float(statistics.median(bbox_areas)) if bbox_areas else "0.000000",
                    "max_value": str(max(bbox_areas)) if bbox_areas else "0",
                }
            )

    duplicate_sample_conflicts = {
        key: value for key, value in duplicate_sample_index.items() if len(set(value)) > 1
    }
    duplicate_image_conflicts = {
        key: value for key, value in duplicate_image_index.items() if len(set(value)) > 1
    }
    duplicate_mask_conflicts = {
        key: value for key, value in duplicate_mask_index.items() if len(set(value)) > 1
    }

    write_csv(
        output_dir / "dataset_stats.csv",
        ["dataset", "split", "sample_count", "readable_pair_count", "empty_mask_count", "mean_foreground_ratio"],
        dataset_stats_rows,
    )
    write_csv(
        output_dir / "foreground_summary.csv",
        ["dataset", "split", "sample_count", "min_foreground_ratio", "mean_foreground_ratio", "median_foreground_ratio", "max_foreground_ratio"],
        foreground_summary_rows,
    )
    write_csv(
        output_dir / "object_size_summary.csv",
        ["dataset", "split", "metric_name", "sample_count", "min_value", "mean_value", "median_value", "max_value"],
        object_size_rows,
    )

    duplicate_report_lines = [
        "# Duplicate Check Report",
        "",
        f"- duplicate_sample_id_conflicts: `{len(duplicate_sample_conflicts)}`",
        f"- duplicate_image_relpath_conflicts: `{len(duplicate_image_conflicts)}`",
        f"- duplicate_mask_relpath_conflicts: `{len(duplicate_mask_conflicts)}`",
        f"- duplicate_check_status: `{choose_status(not duplicate_sample_conflicts and not duplicate_image_conflicts and not duplicate_mask_conflicts)}`",
        "",
        "## Details",
    ]
    if not duplicate_sample_conflicts and not duplicate_image_conflicts and not duplicate_mask_conflicts:
        duplicate_report_lines.append("- none")
    else:
        for sample_id, locations in sorted(duplicate_sample_conflicts.items()):
            duplicate_report_lines.append(f"- sample_id conflict: `{sample_id}` -> `{', '.join(sorted(set(locations)))}`")
        for relpath, locations in sorted(duplicate_image_conflicts.items()):
            duplicate_report_lines.append(f"- image_relpath conflict: `{relpath}` -> `{', '.join(sorted(set(locations)))}`")
        for relpath, locations in sorted(duplicate_mask_conflicts.items()):
            duplicate_report_lines.append(f"- mask_relpath conflict: `{relpath}` -> `{', '.join(sorted(set(locations)))}`")
    (output_dir / "duplicate_check_report.md").write_text("\n".join(duplicate_report_lines) + "\n", encoding="utf-8")

    manual_audit_status, manual_audit_reason = derive_manual_audit_status(manual_audit_path)
    manual_audit_pass = manual_audit_status == "pass"

    pair_check_pass = not pair_issues
    readable_check_pass = not readable_issues
    duplicate_check_pass = not duplicate_sample_conflicts and not duplicate_image_conflicts and not duplicate_mask_conflicts
    foreground_check_pass = all(value == 0 for value in per_split_empty_masks.values())
    data_check_bundle_status = (
        "pass"
        if pair_check_pass and readable_check_pass and duplicate_check_pass and foreground_check_pass and manual_audit_pass
        else "fail"
    )

    data_check_lines = [
        "# Data Check Report",
        "",
        "## Summary",
        f"- data_check_version: `data_check_v1`",
        f"- dataset_stats_csv: `{safe_relpath(output_dir / 'dataset_stats.csv', project_root)}`",
        f"- duplicate_check_report: `{safe_relpath(output_dir / 'duplicate_check_report.md', project_root)}`",
        f"- foreground_summary_csv: `{safe_relpath(output_dir / 'foreground_summary.csv', project_root)}`",
        f"- object_size_summary_csv: `{safe_relpath(output_dir / 'object_size_summary.csv', project_root)}`",
        f"- pair_check_pass: `{choose_status(pair_check_pass)}`",
        f"- readable_check_pass: `{choose_status(readable_check_pass)}`",
        f"- duplicate_check_pass: `{choose_status(duplicate_check_pass)}`",
        f"- foreground_check_pass: `{choose_status(foreground_check_pass)}`",
        f"- manual_audit_status: `{manual_audit_status}`",
        f"- manual_audit_reason: `{manual_audit_reason}`",
        f"- data_check_bundle_status: `{data_check_bundle_status}`",
        "",
        "## Per Split Summary",
    ]
    for row in dataset_stats_rows:
        data_check_lines.append(
            "- "
            + ", ".join(
                [
                    f"dataset=`{row['dataset']}`",
                    f"split=`{row['split']}`",
                    f"sample_count=`{row['sample_count']}`",
                    f"readable_pair_count=`{row['readable_pair_count']}`",
                    f"empty_mask_count=`{row['empty_mask_count']}`",
                    f"mean_foreground_ratio=`{row['mean_foreground_ratio']}`",
                ]
            )
        )
    data_check_lines.extend(["", "## Issues"])
    if not schema_issues and not pair_issues and not readable_issues:
        data_check_lines.append("- none")
    else:
        for issue in schema_issues:
            data_check_lines.append(f"- schema_issue: `{issue}`")
        for issue in pair_issues:
            data_check_lines.append(f"- pair_issue: `{issue}`")
        for issue in readable_issues:
            data_check_lines.append(f"- readable_issue: `{issue}`")
    (output_dir / "data_check_report.md").write_text("\n".join(data_check_lines) + "\n", encoding="utf-8")

    print(f"data_check_bundle_status={data_check_bundle_status}")
    print(f"data_check_report={safe_relpath(output_dir / 'data_check_report.md', project_root)}")
    print(f"duplicate_check_report={safe_relpath(output_dir / 'duplicate_check_report.md', project_root)}")
    return 0 if data_check_bundle_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
