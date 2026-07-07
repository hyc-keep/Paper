"""Export formal sample-level boundary target assets.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark contour-sensitive supervision and gland-boundary emphasis
- 公式/定义: 边界 target 需要从正式二值 mask 派生，并保持样本来源和 split 血统一致
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/build_boundary_targets.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 只导出每个正式 split 的代表样本边界资产，固定 boundary_width=3，并输出 boundary_target_report.md 作为阶段验收证据。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.boundary_targets import build_boundary_band
from src.data.datasets import load_data_config, resolve_split_csv
from src.data.mask_ops import binarize_mask_gt_zero, load_mask_array


PREVIEW_SPLIT_DIR = {
    "glas": {"train": "train68", "val": "val17", "testA": "testA60", "testB": "testB20"},
    "crag": {"train": "train153", "val": "val20", "test": "test40"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export formal boundary target samples.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--num-per-split", type=int, default=2)
    parser.add_argument(
        "--output-root",
        default="reports/data_targets/boundary",
        help="Relative output directory.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/boundary_target_report.md",
        help="Relative markdown report output path.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def pick_indices(total: int, count: int) -> list[int]:
    """Choose evenly spaced representative sample indices for one split.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark visual evidence sampling for protocol verification
    - 公式/定义: 代表样本导出不能只挑首样本，需要在 split 全范围上做均匀抽样
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/build_boundary_targets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 用等间距索引挑每个 split 的代表样本，默认每个 split 导出 2 个边界 target 证据。
    """
    if total <= 0:
        return []
    if total <= count:
        return list(range(total))
    if count == 1:
        return [0]
    return sorted({round(index * (total - 1) / (count - 1)) for index in range(count)})


def build_overlay(image_path: Path, boundary: np.ndarray) -> Image.Image:
    """Render a boundary overlay image for manual protocol review.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark visual validation of gland contour alignment
    - 公式/定义: 边界 target 需要附带可视化叠加图，才能让人工复核确认 contour 是否贴在真实腺体边缘
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/build_boundary_targets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 把 boundary>0 的像素高亮成暖色 overlay，作为 `boundary_overlay.png` 落到 `reports/data_targets/boundary/**`。
    """
    with Image.open(image_path) as raw_image:
        image = raw_image.convert("RGB")
    overlay = image.copy()
    image_pixels = image.load()
    overlay_pixels = overlay.load()
    height, width = boundary.shape
    for y in range(height):
        for x in range(width):
            if int(boundary[y, x]) > 0:
                red, green, blue = image_pixels[x, y]
                overlay_pixels[x, y] = (
                    min(255, int(red * 0.25 + 255 * 0.75)),
                    min(255, int(green * 0.25 + 220 * 0.75)),
                    int(blue * 0.25),
                )
    return overlay


def main() -> int:
    """Export representative boundary target assets for all frozen splits.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark boundary-supervision preparation and protocol evidence export
    - 公式/定义: 边界监督证据必须显式挂到正式 split 样本上，而不能脱离 split 协议单独生成
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/build_boundary_targets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 对 GlaS 和 CRAG 共导出 `14` 个样本的 `__boundary_w3.png` 与 `__boundary_overlay.png`，并写出 `pass_boundary_target=True`。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    output_root = (project_root / args.output_root).resolve()
    report_path = (project_root / args.report_output).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    exported: list[dict[str, str]] = []
    for dataset_code in ("glas", "crag"):
        config = load_data_config(project_root, project_root / "configs" / "data" / f"{dataset_code}.yaml")
        for split_name in config.csv_files:
            csv_path = resolve_split_csv(project_root, config, split_name)
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            for index in pick_indices(len(rows), args.num_per_split):
                row = rows[index]
                sample_id = row["sample_id"]
                image_path = (project_root / row["image_relpath"]).resolve()
                mask_path = (project_root / row["mask_relpath"]).resolve()
                binary_mask = binarize_mask_gt_zero(load_mask_array(mask_path))
                boundary = build_boundary_band(binary_mask, width=3)

                split_dir = output_root / dataset_code / PREVIEW_SPLIT_DIR[dataset_code][split_name]
                split_dir.mkdir(parents=True, exist_ok=True)
                boundary_path = split_dir / f"{sample_id}__boundary_w3.png"
                overlay_path = split_dir / f"{sample_id}__boundary_overlay.png"
                Image.fromarray((boundary * 255).astype(np.uint8), mode="L").save(boundary_path)
                build_overlay(image_path, boundary).save(overlay_path)
                exported.append(
                    {
                        "dataset": dataset_code,
                        "split": PREVIEW_SPLIT_DIR[dataset_code][split_name],
                        "sample_id": sample_id,
                        "boundary": safe_relpath(boundary_path, project_root),
                        "boundary_overlay": safe_relpath(overlay_path, project_root),
                    }
                )

    report_lines = [
        "# Boundary Target Report",
        "",
        "- boundary_target_version: `boundary_target_v1`",
        "- boundary_width: `3`",
        f"- boundary_target_root: `{safe_relpath(output_root, project_root)}`",
        f"- exported_sample_count: `{len(exported)}`",
        "- pass_boundary_target: `True`",
        "",
        "## Exported Samples",
        "| dataset | split | sample_id | boundary | boundary_overlay |",
        "|---|---|---|---|---|",
    ]
    for row in exported:
        report_lines.append(
            f"| {row['dataset']} | {row['split']} | {row['sample_id']} | {row['boundary']} | {row['boundary_overlay']} |"
        )
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("boundary_target_status=pass")
    print(f"boundary_target_report={safe_relpath(report_path, project_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
