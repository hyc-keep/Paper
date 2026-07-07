"""Formal validation loop for the stage02 UNet baseline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: biomedical segmentation validation workflow
- 章节: validation loss aggregation, thresholded mask generation, and metric reporting
- 公式/定义: logits + target masks -> validation losses + segmentation metrics
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/eval/eval_proto_v1.yaml, src/metrics/seg_metrics.py, src/eval/run_eval.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前验证支路统一输出 `val_loss/val_loss_bce/val_loss_dice/dice/iou/objdice/boundary_f1/hd95/object_hausdorff`，方便 trainer 和说明文共用一套指标口径。
- smoke-check 允许缩小验证 batch 与距离类指标范围，但不绕开正式阈值化和指标聚合主链。
"""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader

from src.metrics.seg_metrics import compute_batch_segmentation_metrics, compute_sample_segmentation_metrics

from .threshold import apply_threshold


def run_validation_epoch(
    model: torch.nn.Module,
    dataloader: DataLoader[dict[str, Any]],
    loss_fn: torch.nn.Module,
    device: torch.device,
    threshold_value: float,
    boundary_width: int,
    connected_components_connectivity: int,
    max_batches: int | None = None,
    include_distance_metrics: bool = True,
) -> dict[str, float]:
    """Run one frozen validation epoch and aggregate formal stage02 metrics.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: validation-time thresholding and segmentation metric aggregation
    - 章节: loss accumulation plus pixel/boundary/object metric reporting
    - 公式/定义: dataloader + logits + threshold -> validation metric dict
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/eval/eval_proto_v1.yaml, src/eval/threshold.py, src/metrics/seg_metrics.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前阈值固定走 `threshold_value`，并把 `target >= 0.5` 作为二值监督基准，保持和训练损失、runtime 真值口径一致。
    - `include_distance_metrics=False` 仅用于 smoke-check 缩小代价，不改变正式验证函数的输出字段集合。
    """
    model.eval()

    total_loss = 0.0
    total_bce = 0.0
    total_dice = 0.0
    total_batches = 0

    pred_masks: list[np.ndarray] = []
    target_masks: list[np.ndarray] = []

    with torch.no_grad():
        for batch_index, batch in enumerate(dataloader, start=1):
            images = batch["image"].to(device=device, dtype=torch.float32)
            targets = batch["mask"].to(device=device, dtype=torch.float32)

            logits = model(images)
            loss_dict = loss_fn(logits, targets)

            total_loss += float(loss_dict["loss_total"].item())
            total_bce += float(loss_dict["loss_bce"].item())
            total_dice += float(loss_dict["loss_dice"].item())
            total_batches += 1

            pred_masks.append(apply_threshold(logits, threshold_value).cpu().numpy())
            target_masks.append((targets >= 0.5).to(dtype=torch.uint8).cpu().numpy())

            if max_batches is not None and batch_index >= max_batches:
                break

    if total_batches == 0:
        raise RuntimeError("validation dataloader produced zero batches")

    metrics = compute_batch_segmentation_metrics(
        pred_masks=np.concatenate(pred_masks, axis=0),
        target_masks=np.concatenate(target_masks, axis=0),
        boundary_width=boundary_width,
        connectivity=connected_components_connectivity,
        include_distance_metrics=include_distance_metrics,
    )
    metrics.update(
        {
            "val_loss": total_loss / total_batches,
            "val_loss_bce": total_bce / total_batches,
            "val_loss_dice": total_dice / total_batches,
        }
    )
    return metrics


def evaluate_split(
    model: torch.nn.Module,
    dataloader: DataLoader[dict[str, Any]],
    loss_fn: torch.nn.Module,
    device: torch.device,
    threshold_value: float,
    boundary_width: int,
    connected_components_connectivity: int,
    split_role: str,
    max_samples: int | None = None,
    include_distance_metrics: bool = True,
) -> dict[str, Any]:
    """Evaluate one split and retain per-sample outputs for stage02 test assets.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: split-wise evaluation after checkpoint freezing
    - 章节: one split -> per-sample predictions -> aggregate metric file
    - 公式/定义: dataloader + frozen checkpoint -> split summary plus sample records
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/run_eval.py, src/metrics/seg_metrics.py, src/eval/threshold.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前返回值同时保留 split 级均值和样本级记录，方便 `scripts/test.py`、可视化导出与错误整理共用同一条评估主链。
    - `max_samples` 只服务本地 CPU 级联通检查，正式评估时应保持为 `None` 以覆盖完整 split。
    """
    model.eval()

    total_loss = 0.0
    total_bce = 0.0
    total_dice = 0.0
    total_samples = 0
    sample_records: list[dict[str, Any]] = []

    with torch.no_grad():
        for batch in dataloader:
            images = batch["image"].to(device=device, dtype=torch.float32)
            targets = batch["mask"].to(device=device, dtype=torch.float32)

            logits = model(images)
            loss_dict = loss_fn(logits, targets)
            pred_masks = apply_threshold(logits, threshold_value).cpu().numpy()
            target_masks = (targets >= 0.5).to(dtype=torch.uint8).cpu().numpy()

            sample_ids = [str(item) for item in batch["sample_id"]]
            image_paths = [str(item) for item in batch["image_path"]]
            mask_paths = [str(item) for item in batch["mask_path"]]

            batch_size = pred_masks.shape[0]
            total_loss += float(loss_dict["loss_total"].item()) * batch_size
            total_bce += float(loss_dict["loss_bce"].item()) * batch_size
            total_dice += float(loss_dict["loss_dice"].item()) * batch_size

            for sample_index in range(batch_size):
                sample_metrics = compute_sample_segmentation_metrics(
                    pred_mask=pred_masks[sample_index, 0],
                    target_mask=target_masks[sample_index, 0],
                    boundary_width=boundary_width,
                    connectivity=connected_components_connectivity,
                    include_distance_metrics=include_distance_metrics,
                )
                sample_records.append(
                    {
                        "sample_id": sample_ids[sample_index],
                        "split_role": split_role,
                        "image_path": image_paths[sample_index],
                        "mask_path": mask_paths[sample_index],
                        "pred_mask": pred_masks[sample_index, 0].astype(np.uint8),
                        "target_mask": target_masks[sample_index, 0].astype(np.uint8),
                        "metrics": sample_metrics,
                    }
                )
                total_samples += 1
                if max_samples is not None and total_samples >= max_samples:
                    break

            if max_samples is not None and total_samples >= max_samples:
                break

    if total_samples == 0:
        raise RuntimeError(f"{split_role} dataloader produced zero samples")

    aggregate = {
        "loss": total_loss / total_samples,
        "loss_bce": total_bce / total_samples,
        "loss_dice": total_dice / total_samples,
        "objdice": float(np.mean([record["metrics"]["objdice"] for record in sample_records])),
        "dice": float(np.mean([record["metrics"]["dice"] for record in sample_records])),
        "iou": float(np.mean([record["metrics"]["iou"] for record in sample_records])),
        "f1": float(np.mean([record["metrics"]["f1"] for record in sample_records])),
        "boundary_f1": float(np.mean([record["metrics"]["boundary_f1"] for record in sample_records])),
        "hd95": float(np.mean([record["metrics"]["hd95"] for record in sample_records])),
        "object_hausdorff": float(np.mean([record["metrics"]["object_hausdorff"] for record in sample_records])),
    }
    return {
        "split_role": split_role,
        "sample_count": total_samples,
        "metrics": aggregate,
        "sample_records": sample_records,
    }
