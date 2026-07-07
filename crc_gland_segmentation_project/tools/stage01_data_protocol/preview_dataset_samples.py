"""Export formal split-level preview assets for the frozen data protocol.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark visual audit, qualitative sanity-check and split-level preview evidence
- 公式/定义: 正式数据协议需要最小人工抽查覆盖,因此每个 split 都必须导出可复核的 raw/mask/overlay 预览资产
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/preview_dataset_samples.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 固定 GlaS `5/3/2/2` 与 CRAG `5/3/3` 的抽查覆盖目标,并同步生成 `manual_audit_notes.md`。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - local dependency
    raise SystemExit("Pillow is required for preview_dataset_samples.py") from exc

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.datasets import load_data_config, resolve_split_csv

AUDIT_TARGETS = {
    "glas": {"train68": 5, "val17": 3, "testA60": 2, "testB20": 2},
    "crag": {"train153": 5, "val20": 3, "test40": 3},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export formal preview assets from split CSV files.")
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--num-per-split",
        type=int,
        default=None,
        help="Override how many representative samples to export per split.",
    )
    parser.add_argument(
        "--output-root",
        default="reports/data_preview",
        help="Relative preview output root.",
    )
    parser.add_argument(
        "--manual-audit-output",
        default="reports/data_checks/manual_audit_notes.md",
        help="Relative output path for the formal manual-audit note.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def pick_indices(total: int, count: int) -> list[int]:
    """Pick evenly spread preview samples for one frozen split.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark qualitative sampling for protocol review
    - 公式/定义: 人工抽查样本需要覆盖 split 全段,不能只看前几张或随机一小撮样本
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/preview_dataset_samples.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 用等间距索引为每个 split 选代表样本,并保证目标样本数不足时仍稳定回退。
    """
    if total <= 0:
        return []
    if total <= count:
        return list(range(total))
    if count == 1:
        return [0]
    indices = sorted({round(index * (total - 1) / (count - 1)) for index in range(count)})
    while len(indices) < count:
        candidate = len(indices)
        if candidate not in indices:
            indices.append(candidate)
        indices.sort()
    return indices[:count]


def build_mask_binary(mask_path: Path) -> Image.Image:
    """Convert one formal mask file into a binary preview image.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark mask visualization and foreground sanity check
    - 公式/定义: 预览审阅要求把正式 mask 统一为前景/背景二值图,方便人工快速核对覆盖区域
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/preview_dataset_samples.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 采用 `value > 0 -> 255 else 0` 的二值显示规则,与 `mask_gt_0` 标签协议保持一致。
    """
    with Image.open(mask_path) as mask_image:
        mask = mask_image.convert("L")
        return mask.point(lambda value: 255 if value > 0 else 0)


def build_overlay(raw_path: Path, mask_path: Path) -> Image.Image:
    """Overlay a binary mask on the raw image for manual visual review.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark qualitative verification of annotation alignment
    - 公式/定义: 人工审阅不能只看原图或二值 mask,还要看 overlay 以确认标注是否落在目标组织区域
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/preview_dataset_samples.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 用红色高亮前景区域,输出 `__overlay.png` 作为 `manual_audit_notes.md` 的直接审阅入口。
    """
    with Image.open(raw_path) as raw_image:
        raw = raw_image.convert("RGB")
    mask_bin = build_mask_binary(mask_path).convert("L")
    overlay = raw.copy()
    raw_pixels = raw.load()
    overlay_pixels = overlay.load()
    mask_pixels = mask_bin.load()
    width, height = raw.size
    for y in range(height):
        for x in range(width):
            if mask_pixels[x, y] > 0:
                red, green, blue = raw_pixels[x, y]
                overlay_pixels[x, y] = (
                    min(255, int(red * 0.35 + 255 * 0.65)),
                    int(green * 0.35),
                    int(blue * 0.35),
                )
    return overlay


def required_count(dataset_code: str, split_name: str, override: int | None) -> int:
    """Resolve the formal preview coverage target for one split.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark minimum qualitative evidence coverage
    - 公式/定义: 每个正式 split 都要达到预设最小抽查张数,这样 manual audit 才有协议意义
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/preview_dataset_samples.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 默认沿用 `AUDIT_TARGETS`,但允许通过 CLI 覆盖单次导出数量。
    """
    if override is not None:
        return override
    return AUDIT_TARGETS[dataset_code][split_name]


def main() -> int:
    """Export split-level preview assets and the formal manual-audit note.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark manual audit packaging and preview evidence export
    - 公式/定义: 当前阶段必须把 raw/mask_bin/overlay 三类预览和人工审稿清单一起落盘,才能证明预览链可交接
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/preview_dataset_samples.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 当前真实导出 `23` 对预览样本,并在 `manual_audit_notes.md` 中写出 `manual_audit_status=partial/pass` 所需的全部表格骨架。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    output_root = (project_root / args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    manual_audit_path = (project_root / args.manual_audit_output).resolve()
    manual_audit_path.parent.mkdir(parents=True, exist_ok=True)

    exported_rows: list[dict[str, str]] = []
    coverage_rows: list[dict[str, str]] = []
    total_required = 0
    total_exported = 0
    coverage_pass = True
    for dataset_code in ("glas", "crag"):
        config = load_data_config(project_root, project_root / "configs" / "data" / f"{dataset_code}.yaml")
        for split_name, csv_name in config.csv_files.items():
            csv_path = resolve_split_csv(project_root, config, split_name)
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            split_label = rows[0]["split"] if rows else split_name
            needed = required_count(dataset_code, split_label, args.num_per_split)
            chosen_indices = pick_indices(len(rows), needed)
            total_required += needed
            total_exported += len(chosen_indices)
            split_coverage_pass = len(chosen_indices) >= needed
            coverage_pass = coverage_pass and split_coverage_pass
            coverage_rows.append(
                {
                    "dataset": dataset_code,
                    "split": split_label,
                    "required_pairs": str(needed),
                    "exported_pairs": str(len(chosen_indices)),
                    "coverage_status": "pass" if split_coverage_pass else "fail",
                }
            )
            for index in chosen_indices:
                row = rows[index]
                sample_id = row["sample_id"]
                image_path = (project_root / row["image_relpath"]).resolve()
                mask_path = (project_root / row["mask_relpath"]).resolve()
                split_dir = output_root / dataset_code / row["split"]
                split_dir.mkdir(parents=True, exist_ok=True)

                raw_output = split_dir / f"{sample_id}__raw.png"
                mask_output = split_dir / f"{sample_id}__mask_bin.png"
                overlay_output = split_dir / f"{sample_id}__overlay.png"

                with Image.open(image_path) as raw_image:
                    raw_image.convert("RGB").save(raw_output)
                build_mask_binary(mask_path).save(mask_output)
                build_overlay(image_path, mask_path).save(overlay_output)

                exported_rows.append(
                    {
                        "dataset": dataset_code,
                        "split": row["split"],
                        "sample_id": sample_id,
                        "raw": safe_relpath(raw_output, project_root),
                        "mask_bin": safe_relpath(mask_output, project_root),
                        "overlay": safe_relpath(overlay_output, project_root),
                        "raw_uri": file_uri(raw_output),
                        "mask_bin_uri": file_uri(mask_output),
                        "overlay_uri": file_uri(overlay_output),
                    }
                )

    audit_lines = [
        "# Manual Audit Notes",
        "",
        "- manual_audit_version: `manual_audit_v1`",
        "- manual_audit_status: `partial`",
        "- audit_protocol_target: `GlaS 5/3/2/2; CRAG 5/3/3`",
        f"- manual_audit_required_pairs: `{total_required}`",
        f"- manual_audit_exported_pairs: `{total_exported}`",
        f"- manual_audit_coverage_status: `{'pass' if coverage_pass else 'fail'}`",
        "- manual_review_completion: `pending`",
        "- review_fill_rule_alignment: `pass_or_fail`",
        "- review_fill_rule_decision: `keep_or_reject`",
        "- review_fill_rule_color_issue: `yes_or_no`",
        "- current_conclusion: `formal preview assets now cover the minimum protocol sampling target, but human review decisions are still pending so manual audit is not complete yet.`",
        "",
        "## 简明判断规则",
        "- `alignment_pass`：看红色区域是否大体盖在腺体上。能对上就写 `正常` 或 `pass`；明显错位、盖错目标、空掉主要目标就写 `异常` 或 `fail`。",
        "- `manual_audit_decision`：这张样本是否允许保留进正式数据协议。可接受就写 `保留` 或 `keep`；明显有问题就写 `剔除` 或 `reject`。",
        "- `color_issue_flag`：颜色是否明显离谱。没有明显异常写 `否` 或 `no`；有明显异常写 `是` 或 `yes`。",
        "- 全部 23 条都看完后，把 `manual_review_completion` 改成 `完成` 或 `complete`。",
        "",
        "## Coverage Summary",
        "| dataset | split | required_pairs | exported_pairs | coverage_status |",
        "|---|---|---:|---:|---|",
    ]
    for row in coverage_rows:
        audit_lines.append(
            f"| {row['dataset']} | {row['split']} | {row['required_pairs']} | {row['exported_pairs']} | {row['coverage_status']} |"
        )
    audit_lines.extend(
        [
        "",
        "## Review Instructions",
        "- Set `alignment_pass` to `pass` or `fail`.",
        "- Set `manual_audit_decision` to `keep` or `reject`.",
        "- Set `color_issue_flag` to `yes` or `no`.",
        "- Chinese values are also accepted: `正常/异常`, `保留/剔除`, `是/否`, `完成`.",
        "- If all rows are reviewed and all decisions are acceptable, change `manual_review_completion` to `complete`.",
        "",
        "## Exported Preview Samples",
        "| dataset | split | sample_id | raw | mask_bin | overlay | alignment_pass | manual_audit_decision | color_issue_flag | note |",
        "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in exported_rows:
        audit_lines.append(
            f"| {row['dataset']} | {row['split']} | {row['sample_id']} | [raw]({row['raw_uri']}) | [mask_bin]({row['mask_bin_uri']}) | [overlay]({row['overlay_uri']}) | PENDING_REVIEW | PENDING_REVIEW | UNKNOWN | |"
        )
    manual_audit_path.write_text("\n".join(audit_lines) + "\n", encoding="utf-8")

    print(f"preview_export_status=pass")
    print(f"preview_root={safe_relpath(output_root, project_root)}")
    print(f"manual_audit_notes={safe_relpath(manual_audit_path, project_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
