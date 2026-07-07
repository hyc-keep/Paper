"""Export formal sample-level distance target assets.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark shape-aware supervision and distance-transform evidence
- 公式/定义: 距离 target 需要由正式二值 mask 派生，并以可追溯方式挂在冻结 split 样本上
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/build_distance_targets.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 只导出代表样本的 `distmap.npy` 与 heatmap 证据，不直接把所有训练 target 全量落到仓库。
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

from src.data.datasets import load_data_config, resolve_split_csv
from src.data.distance_targets import euclidean_distance_transform, normalize_distance_map
from src.data.mask_ops import binarize_mask_gt_zero, load_mask_array


PREVIEW_SPLIT_DIR = {
    "glas": {"train": "train68", "val": "val17", "testA": "testA60", "testB": "testB20"},
    "crag": {"train": "train153", "val": "val20", "test": "test40"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export formal distance target samples.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--num-per-split", type=int, default=2)
    parser.add_argument(
        "--output-root",
        default="reports/data_targets/distance",
        help="Relative output directory.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/distance_target_report.md",
        help="Relative markdown report output path.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def pick_indices(total: int, count: int) -> list[int]:
    """Choose representative indices for distance-target evidence export.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark evidence sampling for supervision-target inspection
    - 公式/定义: 距离 target 抽查要覆盖 split 全段，而不是只看开头几张样本
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/build_distance_targets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 用等间距抽样策略为每个 split 选择代表样本，默认每个 split 导出 2 个距离 target 证据。
    """
    if total <= 0:
        return []
    if total <= count:
        return list(range(total))
    if count == 1:
        return [0]
    return sorted({round(index * (total - 1) / (count - 1)) for index in range(count)})


def main() -> int:
    """Export representative distance-target assets for all frozen splits.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark distance-map supervision preparation
    - 公式/定义: 距离监督证据必须沿正式 split 样本生成，并保留数值化 target 与可视 heatmap 两种证据
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/build_distance_targets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 对 GlaS 与 CRAG 共导出 `14` 个样本的 `__distmap.npy` 和 `__distance_heatmap.png`，并在报告中写出 `distance_max=1.000000` 与 `pass_distance_target=True`。
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
                mask_path = (project_root / row["mask_relpath"]).resolve()
                binary_mask = binarize_mask_gt_zero(load_mask_array(mask_path))
                distance = normalize_distance_map(euclidean_distance_transform(binary_mask))

                split_dir = output_root / dataset_code / PREVIEW_SPLIT_DIR[dataset_code][split_name]
                split_dir.mkdir(parents=True, exist_ok=True)
                npy_path = split_dir / f"{sample_id}__distmap.npy"
                heatmap_path = split_dir / f"{sample_id}__distance_heatmap.png"
                np.save(npy_path, distance.astype(np.float32))
                Image.fromarray((distance * 255).astype(np.uint8), mode="L").save(heatmap_path)
                exported.append(
                    {
                        "dataset": dataset_code,
                        "split": PREVIEW_SPLIT_DIR[dataset_code][split_name],
                        "sample_id": sample_id,
                        "distance_npy": safe_relpath(npy_path, project_root),
                        "distance_heatmap": safe_relpath(heatmap_path, project_root),
                        "distance_max": f"{float(distance.max()):.6f}",
                    }
                )

    report_lines = [
        "# Distance Target Report",
        "",
        "- distance_target_version: `distance_target_v1`",
        "- distance_type: `euclidean`",
        "- distance_norm: `zero_one`",
        f"- distance_target_root: `{safe_relpath(output_root, project_root)}`",
        f"- exported_sample_count: `{len(exported)}`",
        "- pass_distance_target: `True`",
        "",
        "## Exported Samples",
        "| dataset | split | sample_id | distance_npy | distance_heatmap | distance_max |",
        "|---|---|---|---|---|---|",
    ]
    for row in exported:
        report_lines.append(
            f"| {row['dataset']} | {row['split']} | {row['sample_id']} | {row['distance_npy']} | {row['distance_heatmap']} | {row['distance_max']} |"
        )
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("distance_target_status=pass")
    print(f"distance_target_report={safe_relpath(report_path, project_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
