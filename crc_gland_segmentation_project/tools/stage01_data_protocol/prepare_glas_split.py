"""Build the frozen GlaS split CSV assets from the formal dataset root.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark split and grade-aware train/test protocol
- 公式/定义: train_ / testA_ / testB_ 命名与 grade 分层约束
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/prepare_glas_split.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 固定 `GLAS_SPLIT_SEED = 3407`，输出 train68 / val17 / testA60 / testB20，并强制 image/mask 成对存在。
"""

from __future__ import annotations

import argparse
import csv
import os
import random
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.datasets import load_data_config, resolve_dataset_root


GLAS_SPLIT_SEED = 3407


def to_project_relpath(path: Path, project_root: Path) -> str:
    return Path(os.path.relpath(path, project_root)).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate formal GlaS split CSV assets.")
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--config",
        default="configs/data/glas.yaml",
        help="Relative path to the formal GlaS data config.",
    )
    parser.add_argument(
        "--output-dir",
        default="splits/glas",
        help="Relative output directory for the split CSV files.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/glas_split_report.md",
        help="Relative markdown report output path.",
    )
    return parser.parse_args()


def detect_grade_columns(header: list[str]) -> tuple[str, str]:
    """Resolve the sample/grade columns from Grade.csv.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark split metadata and grade annotation usage
    - 公式/定义: Grade.csv 需要稳定提供样本身份与 grade 分层信息
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/prepare_glas_split.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 兼容 `sample/image/name/filename/id` 与 `grade/class/label/type` 等常见列名写法。
    """
    lowered = {item.strip().lower(): item for item in header}
    sample_key = None
    grade_key = None
    for candidate in ("sample", "image", "name", "filename", "id"):
        if candidate in lowered:
            sample_key = lowered[candidate]
            break
    for normalized, original in lowered.items():
        if normalized == "grade" or normalized.startswith("grade "):
            grade_key = original
            break
    if grade_key is None:
        for candidate in ("class", "label", "type"):
            if candidate in lowered:
                grade_key = lowered[candidate]
                break
    if sample_key is None or grade_key is None:
        raise ValueError(f"Unsupported Grade.csv columns: {header}")
    return sample_key, grade_key


def load_grade_map(grade_csv_path: Path) -> dict[str, str]:
    with grade_csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"Grade.csv has no header: {grade_csv_path}")
        sample_key, grade_key = detect_grade_columns(reader.fieldnames)
        mapping: dict[str, str] = {}
        for row in reader:
            raw_sample = row[sample_key].strip()
            raw_grade = row[grade_key].strip()
            stem = Path(raw_sample).stem
            mapping[stem] = raw_grade
        return mapping


def build_pairs(dataset_root: Path, prefix: str) -> list[tuple[Path, Path]]:
    image_paths = sorted(
        path for path in dataset_root.glob(f"{prefix}*.bmp") if not path.name.endswith("_anno.bmp")
    )
    pairs: list[tuple[Path, Path]] = []
    for image_path in image_paths:
        mask_path = image_path.with_name(f"{image_path.stem}_anno{image_path.suffix}")
        if not mask_path.exists():
            raise FileNotFoundError(f"Missing mask for image: {image_path.name}")
        pairs.append((image_path, mask_path))
    return pairs


def stratified_train_val_split(
    train_pairs: list[tuple[Path, Path]],
    grade_map: dict[str, str],
    seed: int,
) -> tuple[list[tuple[Path, Path]], list[tuple[Path, Path]]]:
    """Split the official GlaS train set into frozen train68/val17 subsets.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark train/test partition and grade-aware split usage
    - 公式/定义: train 集内部需要在 grade 维度上保持稳定分层
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/prepare_glas_split.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 采用固定随机种子 `3407`，按 `17 / 85` 比例在每个 grade 组内切分，并强制校验最终数量为 `68 / 17`。
    """
    groups: dict[str, list[tuple[Path, Path]]] = {}
    for pair in train_pairs:
        grade = grade_map.get(pair[0].stem)
        if grade is None:
            raise KeyError(f"Missing grade entry for {pair[0].stem}")
        groups.setdefault(grade, []).append(pair)

    rng = random.Random(seed)
    train_split: list[tuple[Path, Path]] = []
    val_split: list[tuple[Path, Path]] = []
    for group_pairs in groups.values():
        ordered = list(group_pairs)
        rng.shuffle(ordered)
        val_count = round(len(ordered) * 17 / 85)
        val_split.extend(ordered[:val_count])
        train_split.extend(ordered[val_count:])

    train_split.sort(key=lambda item: item[0].name)
    val_split.sort(key=lambda item: item[0].name)
    if len(train_split) != 68 or len(val_split) != 17:
        raise ValueError(
            f"Unexpected split sizes after stratification: train={len(train_split)} val={len(val_split)}"
        )
    return train_split, val_split


def build_row(
    project_root: Path,
    image_path: Path,
    mask_path: Path,
    split_name: str,
    grade: str,
    source_partition: str,
) -> dict[str, str]:
    return {
        "sample_id": f"GlaS_{source_partition}_{image_path.stem}",
        "image_relpath": to_project_relpath(image_path, project_root),
        "mask_relpath": to_project_relpath(mask_path, project_root),
        "dataset": "GlaS",
        "split": split_name,
        "grade": grade,
        "source_partition": source_partition,
    }


def write_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sample_id", "image_relpath", "mask_relpath", "dataset", "split", "grade", "source_partition"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_report(project_root: Path, dataset_root: Path, report_output: Path, counts: dict[str, int], seed: int) -> None:
    report_output.parent.mkdir(parents=True, exist_ok=True)
    try:
        dataset_root_display = dataset_root.relative_to(project_root).as_posix()
    except ValueError:
        dataset_root_display = dataset_root.as_posix()
    lines = [
        "# GlaS Split Report",
        "",
        f"- dataset_root: `{dataset_root_display}`",
        f"- split_seed: `{seed}`",
        f"- train68_count: `{counts['train68']}`",
        f"- val17_count: `{counts['val17']}`",
        f"- testA60_count: `{counts['testA60']}`",
        f"- testB20_count: `{counts['testB20']}`",
        "",
        "## Conclusion",
        "- status: `pass`",
        "- note: `formal GlaS split CSV assets were generated from the project-local formal dataset root.`",
        "",
    ]
    report_output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    """Generate the formal GlaS split CSV assets and split report.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark asset preparation and official split contract
    - 公式/定义: 正式输入层必须冻结为可交接、可复现、可验证的 split 资产
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/prepare_glas_split.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 从 `configs/data/glas.yaml` 解析正式数据根目录，输出 `splits/glas/*.csv` 和 `reports/data_checks/glas_split_report.md`。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    config = load_data_config(project_root, project_root / args.config)
    dataset_root = resolve_dataset_root(project_root, config)
    grade_csv_path = dataset_root / "Grade.csv"
    if not dataset_root.exists():
        raise SystemExit(f"Missing dataset_root: {dataset_root}")
    if not grade_csv_path.exists():
        raise SystemExit(f"Missing Grade.csv: {grade_csv_path}")

    grade_map = load_grade_map(grade_csv_path)
    official_train = build_pairs(dataset_root, "train_")
    official_test_a = build_pairs(dataset_root, "testA_")
    official_test_b = build_pairs(dataset_root, "testB_")
    if len(official_train) != 85 or len(official_test_a) != 60 or len(official_test_b) != 20:
        raise SystemExit(
            f"Unexpected GlaS asset counts: train={len(official_train)} testA={len(official_test_a)} testB={len(official_test_b)}"
        )
    train_split, val_split = stratified_train_val_split(official_train, grade_map, GLAS_SPLIT_SEED)

    output_dir = (project_root / args.output_dir).resolve()
    train_rows = [
        build_row(project_root, image, mask, "train68", grade_map[image.stem], "official_train")
        for image, mask in train_split
    ]
    val_rows = [
        build_row(project_root, image, mask, "val17", grade_map[image.stem], "official_train")
        for image, mask in val_split
    ]
    test_a_rows = [
        build_row(project_root, image, mask, "testA60", "not_applicable", "official_testA")
        for image, mask in official_test_a
    ]
    test_b_rows = [
        build_row(project_root, image, mask, "testB20", "not_applicable", "official_testB")
        for image, mask in official_test_b
    ]

    write_rows(output_dir / "glas_train68.csv", train_rows)
    write_rows(output_dir / "glas_val17.csv", val_rows)
    write_rows(output_dir / "glas_testA60.csv", test_a_rows)
    write_rows(output_dir / "glas_testB20.csv", test_b_rows)

    counts = {
        "train68": len(train_rows),
        "val17": len(val_rows),
        "testA60": len(test_a_rows),
        "testB20": len(test_b_rows),
    }
    build_report(
        project_root,
        dataset_root,
        (project_root / args.report_output).resolve(),
        counts,
        GLAS_SPLIT_SEED,
    )
    print("glas_split_status=pass")
    for key, value in counts.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
