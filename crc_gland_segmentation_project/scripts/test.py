"""Formal test entrypoint for stage02 split-wise evaluation assets.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: frozen checkpoint plus fixed threshold evaluated on TestA/TestB
- 公式/定义: best.ckpt + threshold_value + test split dataloaders -> metrics csv + predictions + summaries
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/eval/run_eval.py, src/eval/export_visuals.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 CLI 先服务 `A1` 最小正式评估链, 直接导出 `testA/testB` 指标表、预测掩码、crosscheck note、visuals 和总结。
- `--max-samples-per-split` 只用于本地 CPU 联通检查; 正式评估应保持 `None` 覆盖全量 split。
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
import sys
from typing import Any

import torch
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import train as train_entry
from src.data import build_eval_transform, build_segmentation_dataset, export_binary_mask_png, load_data_config
from src.eval import evaluate_split, export_run_visual_assets
from src.losses import build_seg_loss
from src.models import build_unet_model


def parse_args() -> argparse.Namespace:
    """Parse the formal stage02 test CLI contract.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: frozen checkpoint plus fixed threshold evaluated on TestA/TestB
    - 公式/定义: formal test cli args -> one run directory plus one fixed evaluation/export protocol
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/test.py, configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml, configs/eval/eval_proto_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前参数面只暴露 run 定位、device 提示、checkpoint 覆盖和本地联通检查相关开关，不重新开放阈值与评估口径。
    - `--max-samples-per-split` 与 `--max-visual-samples` 明确服务本地 CPU 联通检查，正式评估仍沿用冻结配置。
    """
    parser = argparse.ArgumentParser(description="Formal stage02 test entrypoint.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional run name override.")
    parser.add_argument("--device", default="cpu", help="Requested device hint.")
    parser.add_argument("--checkpoint", default=None, help="Optional checkpoint path override.")
    parser.add_argument(
        "--max-samples-per-split",
        type=int,
        default=None,
        help="Optional sample cap for local CPU connectivity checks.",
    )
    parser.add_argument(
        "--max-visual-samples",
        type=int,
        default=5,
        help="How many worst-case samples to export per split.",
    )
    parser.add_argument(
        "--skip-visuals",
        action="store_true",
        help="Skip visual export and only write metrics, predictions, note, and summary.",
    )
    return parser.parse_args()


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def _resolve_run_dir(experiment_config: dict[str, Any], run_name_override: str | None) -> Path:
    run_name = run_name_override or str(experiment_config["run_name"])
    return train_entry.build_output_dir(PROJECT_ROOT, run_name)


def _resolve_checkpoint_path(run_dir: Path, checkpoint_override: str | None) -> Path:
    if checkpoint_override:
        candidate = Path(checkpoint_override)
        if not candidate.is_absolute():
            candidate = (PROJECT_ROOT / checkpoint_override).resolve()
        return candidate
    return (run_dir / "checkpoints" / "best.ckpt").resolve()


def _load_checkpoint(model: torch.nn.Module, checkpoint_path: Path, device: torch.device) -> dict[str, Any]:
    checkpoint = torch.load(checkpoint_path, map_location=device)
    if not isinstance(checkpoint, dict) or "model_state_dict" not in checkpoint:
        raise ValueError(f"checkpoint format is invalid: {checkpoint_path}")
    model.load_state_dict(checkpoint["model_state_dict"])
    return checkpoint


def _write_metrics_csv(
    output_path: Path,
    sample_rows: list[dict[str, Any]],
    aggregate_metrics: dict[str, float],
    split_role: str,
) -> None:
    fieldnames = [
        "row_type",
        "sample_id",
        "split_role",
        "sample_count",
        "image_path",
        "mask_path",
        "pred_path",
        "loss",
        "loss_bce",
        "loss_dice",
        "objdice",
        "dice",
        "iou",
        "f1",
        "boundary_f1",
        "hd95",
        "object_hausdorff",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in sample_rows:
            writer.writerow(row)
        writer.writerow(
            {
                "row_type": "aggregate",
                "sample_id": "__aggregate__",
                "split_role": split_role,
                "sample_count": len(sample_rows),
                "image_path": "",
                "mask_path": "",
                "pred_path": "",
                "loss": aggregate_metrics["loss"],
                "loss_bce": aggregate_metrics["loss_bce"],
                "loss_dice": aggregate_metrics["loss_dice"],
                "objdice": aggregate_metrics["objdice"],
                "dice": aggregate_metrics["dice"],
                "iou": aggregate_metrics["iou"],
                "f1": aggregate_metrics["f1"],
                "boundary_f1": aggregate_metrics["boundary_f1"],
                "hd95": aggregate_metrics["hd95"],
                "object_hausdorff": aggregate_metrics["object_hausdorff"],
            }
        )


def _build_sample_rows(run_dir: Path, split_role: str, sample_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    predictions_dir = run_dir / "predictions" / split_role
    for record in sample_records:
        pred_path = predictions_dir / f"{record['sample_id']}_pred.png"
        export_binary_mask_png(record["pred_mask"], pred_path)
        rows.append(
            {
                "row_type": "sample",
                "sample_id": record["sample_id"],
                "split_role": split_role,
                "sample_count": 1,
                "image_path": _relative_path(Path(record["image_path"])),
                "mask_path": _relative_path(Path(record["mask_path"])),
                "pred_path": _relative_path(pred_path),
                "loss": "",
                "loss_bce": "",
                "loss_dice": "",
                "objdice": record["metrics"]["objdice"],
                "dice": record["metrics"]["dice"],
                "iou": record["metrics"]["iou"],
                "f1": record["metrics"]["f1"],
                "boundary_f1": record["metrics"]["boundary_f1"],
                "hd95": record["metrics"]["hd95"],
                "object_hausdorff": record["metrics"]["object_hausdorff"],
            }
        )
    return rows


def _is_close_or_both_nan(left: float, right: float, atol: float = 1.0e-6) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    return abs(left - right) <= atol


def _write_metric_crosscheck_note(
    run_dir: Path,
    sample_rows_by_split: dict[str, list[dict[str, Any]]],
    aggregate_by_split: dict[str, dict[str, float]],
    eval_config: dict[str, Any],
) -> str:
    metric_names = ["objdice", "dice", "iou", "f1", "boundary_f1", "hd95", "object_hausdorff"]
    lines = [
        "# Metric Crosscheck Note",
        "",
        "- crosscheck_scope: `python_reaggregation_from_split_csv`",
        "- official_reference_type: `project_internal_reaggregation_sanity_check`",
        f"- threshold_source: `{eval_config['threshold_source']}`",
        f"- threshold_value: `{eval_config['threshold_value']}`",
        f"- boundary_metric_width: `{eval_config['boundary_metric_width']}`",
        f"- boundary_metric_impl: `binary_erosion_xor_plus_binary_dilation`",
        f"- connected_components_connectivity: `{eval_config.get('connected_components_connectivity', 1)}`",
        "",
        "## Split Checks",
        "",
    ]

    overall_ok = True
    for split_role in ("testA", "testB"):
        sample_rows = sample_rows_by_split[split_role]
        aggregate = aggregate_by_split[split_role]
        lines.append(f"### {split_role}")
        lines.append("")
        lines.append(f"- sample_count: `{len(sample_rows)}`")
        lines.append(
            "- sampled_ids: `"
            + ", ".join(row["sample_id"] for row in sample_rows[: min(5, len(sample_rows))])
            + "`"
        )
        split_ok = True
        for metric_name in metric_names:
            sample_values = [float(row[metric_name]) for row in sample_rows]
            sample_mean = float(sum(sample_values) / len(sample_values)) if sample_values else float("nan")
            aggregate_value = float(aggregate[metric_name])
            is_ok = _is_close_or_both_nan(sample_mean, aggregate_value)
            split_ok = split_ok and is_ok
            lines.append(
                "- "
                + f"`{metric_name}`: sample_mean=`{sample_mean}` / aggregate=`{aggregate_value}` / "
                + f"status=`{'pass' if is_ok else 'fail'}`"
            )
        lines.append("")
        overall_ok = overall_ok and split_ok

    lines.insert(6, f"- metric_crosscheck_result: `{'pass' if overall_ok else 'partial'}`")
    note_path = run_dir / "metric_crosscheck_note.md"
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "pass" if overall_ok else "partial"


def _update_run_meta(
    run_dir: Path,
    run_meta: dict[str, Any],
    aggregate_by_split: dict[str, dict[str, float]],
    crosscheck_result: str,
    visual_info: dict[str, Any] | None,
) -> None:
    run_meta["metric_list"] = [
        "f1",
        "objdice",
        "object_hausdorff",
        "dice",
        "iou",
        "hd95",
        "boundary_f1",
    ]
    run_meta["boundary_metric_width"] = int(run_meta.get("boundary_metric_width", 3))
    run_meta["metric_crosscheck_result"] = crosscheck_result
    run_meta["metric_crosscheck_note_path"] = _relative_path(run_dir / "metric_crosscheck_note.md")
    run_meta["visual_version"] = "visual_proto_v1"
    run_meta["testA_sample_count"] = int(aggregate_by_split["testA"]["sample_count"])
    run_meta["testB_sample_count"] = int(aggregate_by_split["testB"]["sample_count"])
    run_meta["testA_objdice"] = float(aggregate_by_split["testA"]["objdice"])
    run_meta["testB_objdice"] = float(aggregate_by_split["testB"]["objdice"])
    if visual_info is not None:
        run_meta["num_visual_samples_testA"] = int(visual_info["visual_counts"].get("testA", 0))
        run_meta["num_visual_samples_testB"] = int(visual_info["visual_counts"].get("testB", 0))
    (run_dir / "run_meta.yaml").write_text(train_entry.dump_simple_yaml(run_meta) + "\n", encoding="utf-8")


def _write_run_summary(
    run_dir: Path,
    run_meta: dict[str, Any],
    aggregate_by_split: dict[str, dict[str, float]],
    crosscheck_result: str,
    visual_info: dict[str, Any] | None,
) -> None:
    major_failure_modes = []
    if visual_info is not None:
        major_failure_modes = visual_info["major_failure_modes"]
    visuals_ready = visual_info is not None and all(count > 0 for count in visual_info["visual_counts"].values())
    baseline_ready = crosscheck_result == "pass"
    lines = [
        "# Run Summary",
        "",
        f"- stop_reason: `{run_meta.get('stop_reason', 'evaluation_completed')}`",
        f"- best_epoch: `{run_meta.get('best_epoch', 'unknown')}`",
        f"- best_metric_name: `val_objdice`",
        f"- best_metric_value: `{run_meta.get('best_metric_value', 'unknown')}`",
        f"- smoke_check: `{str(run_meta.get('smoke_check', False)).lower()}`",
        f"- amp_active: `{str(run_meta.get('amp_active', False)).lower()}`",
        f"- metric_crosscheck_result: `{crosscheck_result}`",
        f"- visuals_ready: `{str(visuals_ready).lower()}`",
        f"- baseline_ready: `{str(baseline_ready).lower()}`",
        "",
        "## Test Splits",
        "",
        f"- testA_objdice: `{aggregate_by_split['testA']['objdice']:.6f}`",
        f"- testA_dice: `{aggregate_by_split['testA']['dice']:.6f}`",
        f"- testB_objdice: `{aggregate_by_split['testB']['objdice']:.6f}`",
        f"- testB_dice: `{aggregate_by_split['testB']['dice']:.6f}`",
        "",
        "## Findings",
        "",
        "- main_findings: `Split-wise metrics, predictions, and crosscheck note have been exported.`",
        "- protocol_abnormal_signs: `No aggregate-vs-sample reaggregation mismatch was found.`"
        if crosscheck_result == "pass"
        else "- protocol_abnormal_signs: `Aggregate-vs-sample reaggregation mismatch still exists and must be checked.`",
        "- major_failure_modes: `" + (", ".join(major_failure_modes) if major_failure_modes else "not_exported") + "`",
    ]
    (run_dir / "summaries").mkdir(parents=True, exist_ok=True)
    (run_dir / "summaries" / "run_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """Run the frozen stage02 TestA/TestB export pipeline.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: best checkpoint plus validation-derived threshold exported to held-out test splits
    - 公式/定义: best.ckpt + eval protocol + testA/testB dataloaders -> metrics csv + crosscheck note + summaries + visuals
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/test.py, src/eval/run_eval.py, src/eval/export_visuals.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前主函数把 split-wise 指标、prediction png、crosscheck、run_meta 回填和 visual export 固定成一条正式资产链。
    - 当前默认允许本地 CPU 联通检查，但不把抽样模式包装成正式全量测试结论。
    """
    args = parse_args()
    config_path, experiment_config = train_entry.load_experiment_config(PROJECT_ROOT, args.config)
    config_bundle = train_entry.load_training_configs(PROJECT_ROOT, experiment_config)
    run_dir = _resolve_run_dir(experiment_config, args.run_name)
    run_meta_path = run_dir / "run_meta.yaml"
    if not run_meta_path.exists():
        raise FileNotFoundError(f"run_meta.yaml not found: {run_meta_path}")

    data_config_path = (PROJECT_ROOT / config_bundle["paths"]["data"]).resolve()
    data_config = load_data_config(PROJECT_ROOT, data_config_path)
    eval_transform = build_eval_transform(data_config)
    train_config = config_bundle["train"]
    eval_config = config_bundle["eval"]

    test_datasets = {
        "testA": build_segmentation_dataset(PROJECT_ROOT, data_config, "testA", transform=eval_transform),
        "testB": build_segmentation_dataset(PROJECT_ROOT, data_config, "testB", transform=eval_transform),
    }
    test_loaders = {
        split_role: DataLoader(
            dataset,
            batch_size=int(train_config["batch_size"]),
            shuffle=False,
            num_workers=int(train_config["num_workers"]),
        )
        for split_role, dataset in test_datasets.items()
    }

    device = train_entry.resolve_device(args.device)
    model = build_unet_model(config_bundle["model"]).to(device)
    loss_fn = build_seg_loss(train_config)
    checkpoint_path = _resolve_checkpoint_path(run_dir, args.checkpoint)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"checkpoint not found: {checkpoint_path}")
    checkpoint = _load_checkpoint(model, checkpoint_path, device)

    split_results: dict[str, dict[str, Any]] = {}
    sample_rows_by_split: dict[str, list[dict[str, Any]]] = {}
    aggregate_by_split: dict[str, dict[str, float]] = {}
    for split_role in ("testA", "testB"):
        result = evaluate_split(
            model=model,
            dataloader=test_loaders[split_role],
            loss_fn=loss_fn,
            device=device,
            threshold_value=float(eval_config["threshold_value"]),
            boundary_width=int(eval_config["boundary_metric_width"]),
            connected_components_connectivity=int(eval_config["connected_components_connectivity"]),
            split_role=split_role,
            max_samples=args.max_samples_per_split,
            include_distance_metrics=args.max_samples_per_split is None,
        )
        sample_rows = _build_sample_rows(run_dir, split_role, result["sample_records"])
        _write_metrics_csv(run_dir / f"{split_role}_metrics.csv", sample_rows, result["metrics"], split_role)
        split_results[split_role] = result
        sample_rows_by_split[split_role] = sample_rows
        aggregate_by_split[split_role] = dict(result["metrics"])
        aggregate_by_split[split_role]["sample_count"] = float(result["sample_count"])

    crosscheck_result = _write_metric_crosscheck_note(
        run_dir=run_dir,
        sample_rows_by_split=sample_rows_by_split,
        aggregate_by_split=aggregate_by_split,
        eval_config=eval_config,
    )

    visual_info: dict[str, Any] | None = None
    if not args.skip_visuals:
        visual_info = export_run_visual_assets(run_dir=run_dir, max_samples_per_split=args.max_visual_samples)

    run_meta = train_entry.simple_yaml_load(run_meta_path.read_text(encoding="utf-8"))
    run_meta["best_checkpoint_path"] = _relative_path(checkpoint_path)
    run_meta["best_checkpoint_epoch"] = int(checkpoint.get("epoch", run_meta.get("best_epoch", 0)))
    run_meta["boundary_metric_width"] = int(eval_config["boundary_metric_width"])
    _update_run_meta(run_dir, run_meta, aggregate_by_split, crosscheck_result, visual_info)
    _write_run_summary(run_dir, run_meta, aggregate_by_split, crosscheck_result, visual_info)

    print(f"run_dir={_relative_path(run_dir)}")
    print(f"checkpoint={_relative_path(checkpoint_path)}")
    print(f"testA_metrics={_relative_path(run_dir / 'testA_metrics.csv')}")
    print(f"testB_metrics={_relative_path(run_dir / 'testB_metrics.csv')}")
    print(f"metric_crosscheck_result={crosscheck_result}")
    if visual_info is not None:
        print(f"error_cases={visual_info['error_cases_path']}")
        print(f"testA_visual_count={visual_info['visual_counts']['testA']}")
        print(f"testB_visual_count={visual_info['visual_counts']['testB']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
