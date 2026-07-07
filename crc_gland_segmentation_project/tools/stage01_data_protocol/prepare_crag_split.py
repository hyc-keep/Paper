"""Build the frozen CRAG split CSV assets from the formal dataset root.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark split contract reused for fixed formal subset organization
- 公式/定义: CRAG 正式输入层需要固定 train153 / val20 / test40 子集协议，并保持 image/mask 配对关系可审计
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/prepare_crag_split.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 直接从 `train_sup_16 / train_unsup_137 / val / test` 四个本地正式子集装配出三份 CSV，并硬检查数量是否为 153 / 20 / 40。
"""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.datasets import load_data_config, resolve_dataset_root


def to_project_relpath(path: Path, project_root: Path) -> str:
    return Path(os.path.relpath(path, project_root)).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate formal CRAG split CSV assets.")
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--config",
        default="configs/data/crag.yaml",
        help="Relative path to the formal CRAG data config.",
    )
    parser.add_argument(
        "--output-dir",
        default="splits/crag",
        help="Relative output directory for the split CSV files.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/crag_split_report.md",
        help="Relative markdown report output path.",
    )
    return parser.parse_args()


def collect_subset_pairs(subset_root: Path) -> list[tuple[Path, Path]]:
    """Collect aligned image/mask pairs from one CRAG subset directory.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark asset integrity and paired annotation preconditions
    - 公式/定义: 正式 split 资产必须来源于真实存在且一一对应的 image/mask 对
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/prepare_crag_split.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 强制要求 subset 下同时存在 `image/` 和 `mask/`，并要求每个 image 都有同名 mask。
    """
    image_root = subset_root / "image"
    mask_root = subset_root / "mask"
    if not image_root.exists() or not mask_root.exists():
        raise FileNotFoundError(f"Missing image/mask directory under {subset_root}")

    image_paths = sorted(path for path in image_root.iterdir() if path.is_file())
    pairs: list[tuple[Path, Path]] = []
    for image_path in image_paths:
        mask_path = mask_root / image_path.name
        if not mask_path.exists():
            raise FileNotFoundError(f"Missing mask for image {image_path.name} under {subset_root}")
        pairs.append((image_path, mask_path))
    return pairs


def build_row(
    project_root: Path,
    image_path: Path,
    mask_path: Path,
    split_name: str,
    source_subset: str,
) -> dict[str, str]:
    return {
        "sample_id": f"CRAG_{source_subset}_{image_path.stem}",
        "image_relpath": to_project_relpath(image_path, project_root),
        "mask_relpath": to_project_relpath(mask_path, project_root),
        "dataset": "CRAG",
        "split": split_name,
        "source_subset": source_subset,
    }


def write_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sample_id", "image_relpath", "mask_relpath", "dataset", "split", "source_subset"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_report(project_root: Path, dataset_root: Path, report_output: Path, counts: dict[str, int]) -> None:
    report_output.parent.mkdir(parents=True, exist_ok=True)
    try:
        dataset_root_display = dataset_root.relative_to(project_root).as_posix()
    except ValueError:
        dataset_root_display = dataset_root.as_posix()
    lines = [
        "# CRAG Split Report",
        "",
        f"- dataset_root: `{dataset_root_display}`",
        f"- train153_count: `{counts['train153']}`",
        f"- val20_count: `{counts['val20']}`",
        f"- test40_count: `{counts['test40']}`",
        "",
        "## Conclusion",
        "- status: `pass`",
        "- note: `formal CRAG split CSV assets were generated from the project-local formal dataset root.`",
        "",
    ]
    report_output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Generate the formal CRAG split CSV assets and split report.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark asset preparation reused for fixed subset export
    - 公式/定义: 当前阶段必须把 CRAG 正式输入层冻结为可交接、可追溯的 split 资产
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/prepare_crag_split.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 读取 `configs/data/crag.yaml` 解析正式数据根目录，把四个子集合并输出为 `train153 / val20 / test40` 三份 CSV。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    config = load_data_config(project_root, project_root / args.config)
    dataset_root = resolve_dataset_root(project_root, config)
    if not dataset_root.exists():
        raise SystemExit(f"Missing dataset_root: {dataset_root}")

    subset_pairs = {
        "train_sup_16": collect_subset_pairs(dataset_root / "train_sup_16"),
        "train_unsup_137": collect_subset_pairs(dataset_root / "train_unsup_137"),
        "val": collect_subset_pairs(dataset_root / "val"),
        "test": collect_subset_pairs(dataset_root / "test"),
    }

    train_rows = [
        build_row(project_root, image, mask, "train153", "train_sup_16")
        for image, mask in subset_pairs["train_sup_16"]
    ] + [
        build_row(project_root, image, mask, "train153", "train_unsup_137")
        for image, mask in subset_pairs["train_unsup_137"]
    ]
    train_rows.sort(key=lambda item: item["sample_id"])
    val_rows = [build_row(project_root, image, mask, "val20", "val") for image, mask in subset_pairs["val"]]
    test_rows = [build_row(project_root, image, mask, "test40", "test") for image, mask in subset_pairs["test"]]

    if len(train_rows) != 153 or len(val_rows) != 20 or len(test_rows) != 40:
        raise SystemExit(
            f"Unexpected CRAG split counts: train={len(train_rows)} val={len(val_rows)} test={len(test_rows)}"
        )

    output_dir = (project_root / args.output_dir).resolve()
    write_rows(output_dir / "crag_train153.csv", train_rows)
    write_rows(output_dir / "crag_val20.csv", val_rows)
    write_rows(output_dir / "crag_test40.csv", test_rows)

    counts = {"train153": len(train_rows), "val20": len(val_rows), "test40": len(test_rows)}
    build_report(project_root, dataset_root, (project_root / args.report_output).resolve(), counts)
    print("crag_split_status=pass")
    for key, value in counts.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
