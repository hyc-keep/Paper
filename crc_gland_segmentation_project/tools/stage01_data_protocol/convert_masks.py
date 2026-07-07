"""Validate and summarize the formal binary-mask protocol.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark ground-truth handling and binary foreground protocol
- 公式/定义: 当前阶段需要把 mask_gt_0 规则、磁盘值范围和 resize 约束写成正式可复核协议
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/convert_masks.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 不直接批量改写原始 mask 文件，只对冻结 split CSV 覆盖到的样本做规则检查，并输出 binary_mask_summary.csv 与 label_protocol_report.md。
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.datasets import load_data_config, resolve_split_csv, simple_yaml_load
from src.data.mask_ops import binarize_mask_gt_zero, load_mask_array, resize_binary_mask


EXPECTED_INPUT_SIZE = [512, 512]
EXPECTED_IMAGE_INTERP = "bilinear"
EXPECTED_MASK_INTERP = "nearest"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate binary-mask protocol summaries.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument(
        "--summary-output",
        default="reports/data_checks/binary_mask_summary.csv",
        help="Relative CSV output path.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/label_protocol_report.md",
        help="Relative markdown report output path.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def main() -> int:
    """Check the formal binary-mask rule across all frozen split samples.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark annotation protocol and pre-training label consistency
    - 公式/定义: 正式输入层要求所有样本都能稳定落到二值 mask 语义，且 resize / dtype 规则不能漂移
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/convert_masks.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 对 GlaS 与 CRAG 全量 `378` 个 split 样本逐行校验，输出 `invalid_binary_masks=0`、`pass_binary_mask=True`、`pass_dtype=True`、`pass_resize_rule=True`。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    summary_path = (project_root / args.summary_output).resolve()
    report_path = (project_root / args.report_output).resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    rows_out: list[dict[str, str]] = []
    total_samples = 0
    bad_binary_count = 0
    bad_dtype_count = 0
    resize_rule_failures: list[str] = []
    config_resize_status: list[dict[str, str]] = []

    for dataset_code in ("glas", "crag"):
        config = load_data_config(project_root, project_root / "configs" / "data" / f"{dataset_code}.yaml")
        config_path = project_root / "configs" / "data" / f"{dataset_code}.yaml"
        raw_config = simple_yaml_load(config_path.read_text(encoding="utf-8"))
        config_resize_ok = (
            raw_config.get("input_size") == EXPECTED_INPUT_SIZE
            and str(raw_config.get("image_interp", "")).strip() == EXPECTED_IMAGE_INTERP
            and str(raw_config.get("mask_interp", "")).strip() == EXPECTED_MASK_INTERP
        )
        config_resize_status.append(
            {
                "dataset": dataset_code,
                "config_path": safe_relpath(config_path, project_root),
                "input_size": str(raw_config.get("input_size")),
                "image_interp": str(raw_config.get("image_interp", "")),
                "mask_interp": str(raw_config.get("mask_interp", "")),
                "status": "pass" if config_resize_ok else "fail",
            }
        )
        if not config_resize_ok:
            resize_rule_failures.append(f"config_mismatch:{dataset_code}")
        for split_name in config.csv_files:
            csv_path = resolve_split_csv(project_root, config, split_name)
            with csv_path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    mask_path = (project_root / row["mask_relpath"]).resolve()
                    raw_mask = load_mask_array(mask_path)
                    binary_mask = binarize_mask_gt_zero(raw_mask)
                    resized_binary_mask = resize_binary_mask(binary_mask, tuple(EXPECTED_INPUT_SIZE))
                    raw_unique = sorted(int(value) for value in set(raw_mask.reshape(-1).tolist()))
                    binary_unique = sorted(int(value) for value in set(binary_mask.reshape(-1).tolist()))
                    resized_unique = sorted(int(value) for value in set(resized_binary_mask.reshape(-1).tolist()))
                    is_binary_valid = binary_unique in ([0], [0, 1], [1])
                    dtype_valid = raw_mask.dtype.name == "uint8" and binary_mask.dtype.name == "uint8"
                    resize_valid = (
                        list(resized_binary_mask.shape) == EXPECTED_INPUT_SIZE
                        and resized_unique in ([0], [0, 1], [1])
                    )
                    total_samples += 1
                    bad_binary_count += 0 if is_binary_valid else 1
                    bad_dtype_count += 0 if dtype_valid else 1
                    if not resize_valid:
                        resize_rule_failures.append(f"resize_invalid:{row['sample_id']}")
                    rows_out.append(
                        {
                            "dataset": dataset_code,
                            "split": split_name,
                            "sample_id": row["sample_id"],
                            "raw_mask_unique_min": str(raw_unique[0] if raw_unique else 0),
                            "raw_mask_unique_max": str(raw_unique[-1] if raw_unique else 0),
                            "binary_unique_values": ",".join(str(value) for value in binary_unique),
                            "binary_positive_pixels": str(int(binary_mask.sum())),
                            "binary_valid": str(is_binary_valid),
                            "dtype_valid": str(dtype_valid),
                            "resized_shape_hw": f"{resized_binary_mask.shape[0]}x{resized_binary_mask.shape[1]}",
                            "resized_unique_values": ",".join(str(value) for value in resized_unique),
                            "resize_valid": str(resize_valid),
                        }
                    )

    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "dataset",
                "split",
                "sample_id",
                "raw_mask_unique_min",
                "raw_mask_unique_max",
                "binary_unique_values",
                "binary_positive_pixels",
                "binary_valid",
                "dtype_valid",
                "resized_shape_hw",
                "resized_unique_values",
                "resize_valid",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    pass_binary_mask = bad_binary_count == 0
    pass_dtype = bad_dtype_count == 0
    pass_resize_rule = len(resize_rule_failures) == 0
    report_lines = [
        "# Label Protocol Report",
        "",
        "- mask_rule_version: `mask_rule_v1`",
        "- mask_positive_rule: `mask_gt_0`",
        "- mask_disk_value_rule: `0_255`",
        "- input_size: `512x512`",
        "- image_interp: `bilinear`",
        "- mask_interp: `nearest`",
        f"- binary_mask_summary_csv: `{safe_relpath(summary_path, project_root)}`",
        f"- total_samples_checked: `{total_samples}`",
        f"- invalid_binary_masks: `{bad_binary_count}`",
        f"- pass_binary_mask: `{pass_binary_mask}`",
        f"- pass_dtype: `{pass_dtype}`",
        f"- invalid_dtype_masks: `{bad_dtype_count}`",
        f"- pass_resize_rule: `{pass_resize_rule}`",
        f"- resize_rule_failure_count: `{len(resize_rule_failures)}`",
        "",
        "## Resize Rule Config Checks",
        "",
    ]
    for item in config_resize_status:
        report_lines.append(
            f"- {item['dataset']}: config=`{item['config_path']}` input_size=`{item['input_size']}` image_interp=`{item['image_interp']}` mask_interp=`{item['mask_interp']}` status=`{item['status']}`"
        )
    report_lines.extend(
        [
            "",
            "## Conclusion",
            "- note: `formal binary-mask protocol has been checked against all split CSV samples, and resize rule status now requires both frozen config alignment and binary-safe nearest-mask resizing.`",
        ]
    )
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    print(f"label_protocol_status={'pass' if pass_binary_mask and pass_dtype and pass_resize_rule else 'fail'}")
    print(f"label_protocol_report={safe_relpath(report_path, project_root)}")
    return 0 if pass_binary_mask and pass_dtype and pass_resize_rule else 1


if __name__ == "__main__":
    raise SystemExit(main())
