"""Formal epoch trainer for the stage02 UNet baseline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
- 章节: supervised training loop for dense segmentation
- 公式/定义: train epoch -> validation epoch -> scheduler/best-checkpoint/early-stop feedback loop
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/eval/run_eval.py, src/eval/checkpoint_selector.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 trainer 只服务单输出 UNet 基线，把训练日志、验证指标、checkpoint 和 summary 固定在一个最小可审计闭环里。
- smoke-check 会强制缩短 epoch/batch 数量，但仍保留完整的 train -> val -> scheduler -> checkpoint 主链。
"""

from __future__ import annotations

import csv
from contextlib import nullcontext
from pathlib import Path
from time import perf_counter
from typing import Any

import torch
from torch.utils.data import DataLoader

from src.eval.checkpoint_selector import BestCheckpointState, update_best_checkpoint
from src.eval.run_eval import run_validation_epoch

from .early_stop import EarlyStopper


def _append_csv_row(path: Path, fieldnames: list[str], row: dict[str, Any]) -> None:
    """Append one structured metrics row to the formal CSV artifact.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: experiment reproducibility practice
    - 章节: persistent epoch-level metric recording
    - 公式/定义: one epoch/step result -> one CSV row
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/engine/trainer.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一在写入前自动创建父目录，并在首行缺失时补 header，避免 stage02 首轮实验因为空目录或无表头而留下不可读资产。
    - 写入接口只接受显式 `fieldnames` 和 `row`，不在内部偷偷重排字段，方便和 learning-doc 说明文逐项对账。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def _save_checkpoint(
    path: Path,
    epoch: int,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    metric_value: float,
) -> None:
    """Persist a minimal checkpoint snapshot for the formal training loop.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: supervised model selection workflow
    - 章节: checkpoint persistence for best/last model recovery
    - 公式/定义: epoch + model_state + optimizer_state + metric_value -> checkpoint artifact
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/engine/trainer.py, src/eval/checkpoint_selector.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 checkpoint 只冻结最小恢复必需字段，不提前引入 scaler、EMA 或复杂训练态，保持 stage02 首轮闭环可解释。
    - `best.ckpt` 与 `last.ckpt` 共用同一保存结构，方便后续评估链按统一格式消费。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "metric_value": metric_value,
        },
        path,
    )


def _as_int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _as_float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _build_autocast_context(device: torch.device, amp_enabled: bool):
    """Return the runtime autocast context that matches the current device.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: mixed-precision runtime practice
    - 章节: autocast only on supported CUDA execution
    - 公式/定义: cuda and amp_enabled -> autocast, otherwise -> nullcontext
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/engine/trainer.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前明确禁止在 CPU 路径伪造 AMP，上下文会直接退化为 `nullcontext()`，和本地无 GPU 环境保持一致。
    - 把 autocast 判定集中在一个 helper，避免 train loop 内散落条件分支，降低说明文解释成本。
    """
    if amp_enabled and device.type == "cuda":
        return torch.autocast(device_type="cuda", dtype=torch.float16)
    return nullcontext()


def train_model(
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: torch.optim.lr_scheduler.ReduceLROnPlateau,
    early_stopper: EarlyStopper,
    train_loader: DataLoader[dict[str, Any]],
    val_loader: DataLoader[dict[str, Any]],
    device: torch.device,
    output_dir: Path,
    train_config: dict[str, Any],
    eval_config: dict[str, Any],
    smoke_check: bool,
    resume_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the formal stage02 train/val loop and materialize training artifacts.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: biomedical segmentation training workflow
    - 章节: epoch training, validation feedback, checkpoint selection and early stopping
    - 公式/定义: train_loader + val_loader + loss + optimizer -> epoch metrics + best checkpoint + run summary
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/train.py, src/eval/run_eval.py, src/eval/checkpoint_selector.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前最佳模型唯一由 `val_objdice` 决定，并同步驱动 scheduler 与 early stopper，保持和冻结配置 `best_selector=val_objdice_max` 一致。
    - smoke-check 只缩小 epoch/batch 与验证项范围，不绕过日志、验证、checkpoint 和 run summary 这些正式资产输出。
    """
    model.to(device)
    amp_enabled = bool(train_config["amp"]) and device.type == "cuda"
    max_epochs = 2 if smoke_check else int(train_config["epoch_max"])
    boundary_width = int(eval_config["boundary_metric_width"])
    connected_components_connectivity = int(eval_config["connected_components_connectivity"])
    threshold_value = float(eval_config["threshold_value"])
    smoke_val_batches = int(train_config.get("smoke_val_batches", 1))

    train_log_path = output_dir / "train_log.csv"
    val_metrics_path = output_dir / "val_metrics.csv"
    curves_dir = output_dir / "curves"
    checkpoints_dir = output_dir / "checkpoints"
    summary_dir = output_dir / "summaries"

    start_epoch = 1
    train_rows: list[dict[str, Any]] = []
    val_rows: list[dict[str, Any]] = []
    best_state: BestCheckpointState | None = None
    if resume_state is not None:
        start_epoch = int(resume_state["next_epoch"])
        train_rows = list(resume_state["train_rows"])
        val_rows = list(resume_state["val_rows"])
        best_state = resume_state["best_state"]
    stop_reason = "epoch_max_reached"

    for epoch in range(start_epoch, max_epochs + 1):
        model.train()
        epoch_start = perf_counter()
        total_loss = 0.0
        total_bce = 0.0
        total_dice = 0.0
        total_batches = 0

        for batch_index, batch in enumerate(train_loader, start=1):
            images = batch["image"].to(device=device, dtype=torch.float32)
            targets = batch["mask"].to(device=device, dtype=torch.float32)

            optimizer.zero_grad(set_to_none=True)
            with _build_autocast_context(device, amp_enabled):
                logits = model(images)
                loss_dict = loss_fn(logits, targets)
                loss_total = loss_dict["loss_total"]

            loss_total.backward()
            optimizer.step()

            total_loss += float(loss_total.item())
            total_bce += float(loss_dict["loss_bce"].item())
            total_dice += float(loss_dict["loss_dice"].item())
            total_batches += 1

            if smoke_check and batch_index >= int(train_config["smoke_train_batches"]):
                break

        if total_batches == 0:
            raise RuntimeError("train dataloader produced zero batches")

        train_row = {
            "epoch": epoch,
            "epoch_train_loss": total_loss / total_batches,
            "epoch_loss_bce": total_bce / total_batches,
            "epoch_loss_dice": total_dice / total_batches,
            "lr": optimizer.param_groups[0]["lr"],
            "batch_size": int(train_config["batch_size"]),
            "amp": str(bool(train_config["amp"])).lower(),
            "epoch_time_sec": round(perf_counter() - epoch_start, 4),
        }
        train_rows.append(train_row)
        _append_csv_row(train_log_path, list(train_row.keys()), train_row)

        val_metrics = run_validation_epoch(
            model=model,
            dataloader=val_loader,
            loss_fn=loss_fn,
            device=device,
            threshold_value=threshold_value,
            boundary_width=boundary_width,
            connected_components_connectivity=connected_components_connectivity,
            max_batches=smoke_val_batches if smoke_check else None,
            include_distance_metrics=not smoke_check,
        )
        val_row = {
            "epoch": epoch,
            "val_loss": val_metrics["val_loss"],
            "val_loss_bce": val_metrics["val_loss_bce"],
            "val_loss_dice": val_metrics["val_loss_dice"],
            "val_objdice": val_metrics["objdice"],
            "val_dice": val_metrics["dice"],
            "val_iou": val_metrics["iou"],
            "val_f1": val_metrics["f1"],
            "val_boundary_f1": val_metrics["boundary_f1"],
            "val_hd95": val_metrics["hd95"],
            "val_object_hausdorff": val_metrics["object_hausdorff"],
        }
        val_rows.append(val_row)
        _append_csv_row(val_metrics_path, list(val_row.keys()), val_row)

        scheduler.step(val_row["val_objdice"])
        best_state, is_best = update_best_checkpoint(best_state, epoch=epoch, metric_value=val_row["val_objdice"])
        improved, should_stop = early_stopper.update(val_row["val_objdice"])

        _save_checkpoint(
            path=checkpoints_dir / "last.ckpt",
            epoch=epoch,
            model=model,
            optimizer=optimizer,
            metric_value=val_row["val_objdice"],
        )
        if is_best:
            _save_checkpoint(
                path=checkpoints_dir / "best.ckpt",
                epoch=epoch,
                model=model,
                optimizer=optimizer,
                metric_value=val_row["val_objdice"],
            )

        if smoke_check and epoch >= int(train_config["smoke_epochs"]):
            stop_reason = "smoke_check_complete"
            break

        if should_stop:
            stop_reason = "early_stopping"
            break

    curves_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)
    with (curves_dir / "train_curve.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epoch", "epoch_train_loss", "epoch_loss_bce", "epoch_loss_dice", "lr"])
        writer.writeheader()
        for row in train_rows:
            writer.writerow({key: row[key] for key in writer.fieldnames})
    with (curves_dir / "val_curve.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epoch", "val_loss", "val_objdice", "val_dice", "val_iou"])
        writer.writeheader()
        for row in val_rows:
            writer.writerow({key: row[key] for key in writer.fieldnames})

    best_epoch = best_state.best_epoch if best_state is not None else 0
    best_metric_value = best_state.best_metric_value if best_state is not None else 0.0
    summary_text = "\n".join(
        [
            "# Run Summary",
            "",
            f"- stop_reason: `{stop_reason}`",
            f"- best_epoch: `{best_epoch}`",
            f"- best_metric_name: `val_objdice`",
            f"- best_metric_value: `{best_metric_value:.6f}`",
            f"- smoke_check: `{str(smoke_check).lower()}`",
            f"- amp_active: `{str(amp_enabled).lower()}`",
        ]
    )
    (summary_dir / "run_summary.md").write_text(summary_text + "\n", encoding="utf-8")

    return {
        "stop_reason": stop_reason,
        "best_epoch": best_epoch,
        "best_metric_value": best_metric_value,
        "amp_active": amp_enabled,
        "epoch_count": len(train_rows),
        "last_val_metrics": val_rows[-1],
    }
