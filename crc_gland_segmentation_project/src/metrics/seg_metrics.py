"""Pixel-, boundary-, and object-level metrics for binary gland masks.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: pixel-level, boundary-level and object-level segmentation evaluation
- 公式/定义: binary prediction plus binary target -> dice/iou/objdice/boundary_f1/hd95/object_hausdorff
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: src/eval/run_eval.py, configs/eval/eval_proto_v1.yaml, 结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 stage02 只保留正式验证链所需的核心指标集合，先服务 `val_objdice` 选优和对象/边界指标对账。
- 批量聚合入口固定接收 `[B, 1, H, W]` 二值 mask，避免在 metric 层重新解释多头、多类语义。
"""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator <= 0.0:
        return 1.0
    return float(numerator / denominator)


def _resolve_connectivity_structure(connectivity: int) -> np.ndarray:
    if connectivity == 8:
        return ndimage.generate_binary_structure(2, 2)
    if connectivity == 4:
        return ndimage.generate_binary_structure(2, 1)
    raise ValueError(f"Unsupported connected-components connectivity: {connectivity}")


def dice_score(pred_mask: np.ndarray, target_mask: np.ndarray, eps: float = 1e-6) -> float:
    """Compute pixel-level Dice score for one binary prediction-target pair.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: binary segmentation overlap metric
    - 章节: Sørensen-Dice overlap for foreground masks
    - 公式/定义: (2 * intersection + eps) / (pred_sum + target_sum + eps)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, src/eval/run_eval.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前空预测且空标注直接记为 `1.0`，和 stage02 的空前景一致性处理保持统一。
    - 输入会先强制转成 bool，避免上游 uint8/float mask 在这里继续分叉。
    """
    pred = pred_mask.astype(bool)
    target = target_mask.astype(bool)
    intersection = float(np.logical_and(pred, target).sum())
    denom = float(pred.sum() + target.sum())
    if denom == 0.0:
        return 1.0
    return float((2.0 * intersection + eps) / (denom + eps))


def iou_score(pred_mask: np.ndarray, target_mask: np.ndarray, eps: float = 1e-6) -> float:
    """Compute pixel-level IoU score for one binary prediction-target pair.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: binary segmentation intersection-over-union
    - 章节: foreground overlap by intersection divided by union
    - 公式/定义: (intersection + eps) / (union + eps)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, src/eval/run_eval.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前和 Dice 一样把空预测且空标注记为 `1.0`，保证 batch 聚合时语义一致。
    - IoU 在 stage02 主要作为辅助验证指标，不直接驱动 best checkpoint 选择。
    """
    pred = pred_mask.astype(bool)
    target = target_mask.astype(bool)
    intersection = float(np.logical_and(pred, target).sum())
    union = float(np.logical_or(pred, target).sum())
    if union == 0.0:
        return 1.0
    return float((intersection + eps) / (union + eps))


def boundary_f1_score(
    pred_mask: np.ndarray,
    target_mask: np.ndarray,
    width: int = 3,
    connectivity: int = 8,
) -> float:
    """Compute boundary F1 for one binary mask pair with fixed dilation width.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: contour-aware segmentation evaluation
    - 章节: boundary precision/recall inside tolerance band
    - 公式/定义: F1(boundary precision, boundary recall) with width-based matching band
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, configs/eval/eval_proto_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 `width` 由 eval config 冻结为 `3`，不在 metric 调用点随意改口径。
    - 边界提取统一使用二值腐蚀异或逻辑，先保证 stage02 基线实现可解释。
    """
    pred = pred_mask.astype(bool)
    target = target_mask.astype(bool)
    if not pred.any() and not target.any():
        return 1.0

    structure = _resolve_connectivity_structure(connectivity)
    pred_edge = np.logical_xor(pred, ndimage.binary_erosion(pred, structure=structure, border_value=0))
    target_edge = np.logical_xor(target, ndimage.binary_erosion(target, structure=structure, border_value=0))

    pred_band = ndimage.binary_dilation(pred_edge, structure=structure, iterations=width)
    target_band = ndimage.binary_dilation(target_edge, structure=structure, iterations=width)

    precision = _safe_divide(np.logical_and(pred_edge, target_band).sum(), pred_edge.sum())
    recall = _safe_divide(np.logical_and(target_edge, pred_band).sum(), target_edge.sum())
    if precision + recall == 0.0:
        return 0.0
    return float(2.0 * precision * recall / (precision + recall))


def _surface_distances(source_mask: np.ndarray, target_mask: np.ndarray, connectivity: int = 8) -> np.ndarray:
    source = source_mask.astype(bool)
    target = target_mask.astype(bool)
    if not source.any() and not target.any():
        return np.zeros(1, dtype=np.float32)

    structure = _resolve_connectivity_structure(connectivity)
    source_edge = np.logical_xor(source, ndimage.binary_erosion(source, structure=structure, border_value=0))
    target_edge = np.logical_xor(target, ndimage.binary_erosion(target, structure=structure, border_value=0))

    if not source_edge.any() and not target_edge.any():
        return np.zeros(1, dtype=np.float32)

    if not source_edge.any() or not target_edge.any():
        diagonal = float(np.hypot(*source_mask.shape))
        return np.array([diagonal], dtype=np.float32)

    target_distance = ndimage.distance_transform_edt(~target_edge)
    return target_distance[source_edge].astype(np.float32)


def hd95_score(pred_mask: np.ndarray, target_mask: np.ndarray, connectivity: int = 8) -> float:
    """Compute symmetric 95th percentile Hausdorff distance for one mask pair.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: medical segmentation distance metrics
    - 章节: symmetric surface distance percentile summary
    - 公式/定义: percentile_95(concat(surface_distance(pred,target), surface_distance(target,pred)))
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, src/eval/run_eval.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前把距离类指标保留在正式实现里，但允许 smoke-check 通过上游开关跳过，降低本地 CPU 成本。
    - surface distance 的空边界退化逻辑统一收在 helper 中，避免各指标分头处理。
    """
    forward = _surface_distances(pred_mask, target_mask, connectivity=connectivity)
    backward = _surface_distances(target_mask, pred_mask, connectivity=connectivity)
    distances = np.concatenate([forward, backward])
    return float(np.percentile(distances, 95))


def hausdorff_score(pred_mask: np.ndarray, target_mask: np.ndarray, connectivity: int = 8) -> float:
    forward = _surface_distances(pred_mask, target_mask, connectivity=connectivity)
    backward = _surface_distances(target_mask, pred_mask, connectivity=connectivity)
    return float(max(float(forward.max()), float(backward.max())))


def _object_dice_one_way(source_labels: np.ndarray, target_labels: np.ndarray) -> float:
    source_ids = [label_id for label_id in np.unique(source_labels) if label_id != 0]
    if not source_ids:
        return 1.0

    total_area = sum(int((source_labels == label_id).sum()) for label_id in source_ids)
    score = 0.0

    for label_id in source_ids:
        source_object = source_labels == label_id
        source_area = int(source_object.sum())
        overlapping_ids = np.unique(target_labels[source_object])
        overlapping_ids = [target_id for target_id in overlapping_ids if target_id != 0]
        best = 0.0
        for target_id in overlapping_ids:
            target_object = target_labels == target_id
            best = max(best, dice_score(source_object, target_object))
        score += (source_area / total_area) * best

    return float(score)


def object_dice_score(pred_mask: np.ndarray, target_mask: np.ndarray, connectivity: int = 8) -> float:
    """Compute bidirectional object-level Dice for connected gland instances.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS object-level evaluation
    - 章节: object-wise overlap matched by connected components
    - 公式/定义: 0.5 * (GT->Pred object dice + Pred->GT object dice)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, configs/eval/eval_proto_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 `val_objdice` 是 stage02 的唯一 best-selector 指标，因此对象级 Dice 被明确放进正式验证主链。
    - 连接域分解固定使用 scipy label 的默认二维连通逻辑，先和当前基线口径保持一致。
    """
    pred = pred_mask.astype(bool)
    target = target_mask.astype(bool)
    if not pred.any() and not target.any():
        return 1.0
    if not pred.any() or not target.any():
        return 0.0

    structure = _resolve_connectivity_structure(connectivity)
    pred_labels, _ = ndimage.label(pred, structure=structure)
    target_labels, _ = ndimage.label(target, structure=structure)
    gt_to_pred = _object_dice_one_way(target_labels, pred_labels)
    pred_to_gt = _object_dice_one_way(pred_labels, target_labels)
    return float(0.5 * (gt_to_pred + pred_to_gt))


def _object_hausdorff_one_way(source_labels: np.ndarray, target_labels: np.ndarray) -> float:
    source_ids = [label_id for label_id in np.unique(source_labels) if label_id != 0]
    if not source_ids:
        return 0.0

    total_area = sum(int((source_labels == label_id).sum()) for label_id in source_ids)
    score = 0.0
    for label_id in source_ids:
        source_object = source_labels == label_id
        source_area = int(source_object.sum())
        overlapping_ids = np.unique(target_labels[source_object])
        overlapping_ids = [target_id for target_id in overlapping_ids if target_id != 0]
        if overlapping_ids:
            candidates = [hausdorff_score(source_object, target_labels == target_id) for target_id in overlapping_ids]
            best = min(candidates)
        else:
            best = hausdorff_score(source_object, np.zeros_like(target_labels, dtype=bool))
        score += (source_area / total_area) * best
    return float(score)


def object_hausdorff_score(pred_mask: np.ndarray, target_mask: np.ndarray, connectivity: int = 8) -> float:
    """Compute bidirectional object-level Hausdorff distance for connected components.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: object-aware boundary distance in gland evaluation
    - 章节: object matching followed by Hausdorff summary
    - 公式/定义: 0.5 * (GT->Pred object Hausdorff + Pred->GT object Hausdorff)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, src/eval/run_eval.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前对象级 Hausdorff 仍作为正式验证输出保留，但不直接驱动 best checkpoint 选择。
    - 当一侧完全缺失对象时，退化值固定回到图像对角线长度，保证结果可解释。
    """
    pred = pred_mask.astype(bool)
    target = target_mask.astype(bool)
    if not pred.any() and not target.any():
        return 0.0
    if not pred.any() or not target.any():
        return float(np.hypot(*pred_mask.shape))

    structure = _resolve_connectivity_structure(connectivity)
    pred_labels, _ = ndimage.label(pred, structure=structure)
    target_labels, _ = ndimage.label(target, structure=structure)
    gt_to_pred = _object_hausdorff_one_way(target_labels, pred_labels)
    pred_to_gt = _object_hausdorff_one_way(pred_labels, target_labels)
    return float(0.5 * (gt_to_pred + pred_to_gt))


def compute_sample_segmentation_metrics(
    pred_mask: np.ndarray,
    target_mask: np.ndarray,
    boundary_width: int = 3,
    connectivity: int = 8,
    include_distance_metrics: bool = True,
) -> dict[str, float]:
    """Compute the formal metric row for one binary gland-mask pair.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: per-sample segmentation metric accounting before split-level aggregation
    - 章节: one prediction-target pair -> pixel/boundary/object metric summary
    - 公式/定义: sample binary masks -> one formal metric dictionary
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/metrics/seg_metrics.py, src/eval/run_eval.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前把单样本指标字典单独抽出来，方便 testA/testB 结果导出、可视化错误整理和交叉核对共用同一套口径。
    - 距离类指标仍允许通过 `include_distance_metrics` 在本地 CPU smoke 检查时降级，但字段名保持不变。
    """
    pred_2d = pred_mask.astype(np.uint8)
    target_2d = target_mask.astype(np.uint8)
    metrics = {
        "dice": dice_score(pred_2d, target_2d),
        "iou": iou_score(pred_2d, target_2d),
        "objdice": object_dice_score(pred_2d, target_2d, connectivity=connectivity),
        "boundary_f1": boundary_f1_score(pred_2d, target_2d, width=boundary_width, connectivity=connectivity),
        "f1": dice_score(pred_2d, target_2d),
        "hd95": float("nan"),
        "object_hausdorff": float("nan"),
    }
    if include_distance_metrics:
        metrics["hd95"] = hd95_score(pred_2d, target_2d, connectivity=connectivity)
        metrics["object_hausdorff"] = object_hausdorff_score(pred_2d, target_2d, connectivity=connectivity)
    return metrics


def compute_batch_segmentation_metrics(
    pred_masks: np.ndarray,
    target_masks: np.ndarray,
    boundary_width: int = 3,
    connectivity: int = 8,
    include_distance_metrics: bool = True,
) -> dict[str, float]:
    """Aggregate formal stage02 segmentation metrics over one validation batch set.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: batch-wise aggregation of pixel, boundary and object metrics
    - 章节: per-sample metrics averaged into epoch validation summary
    - 公式/定义: batch binary masks -> per-sample metrics -> mean metric dictionary
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/run_eval.py, src/metrics/seg_metrics.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前批量入口只接受 `[B,1,H,W]` 掩码张量布局，和 `run_validation_epoch()` 的输出契约严格对齐。
    - `include_distance_metrics` 允许 smoke-check 跳过 `hd95` 与 `object_hausdorff`，但不会移除 Dice、IoU、ObjDice 和 Boundary F1 主链。
    """
    if pred_masks.ndim != 4 or target_masks.ndim != 4:
        raise ValueError("pred_masks and target_masks must be shaped as [B, 1, H, W]")

    dice_values: list[float] = []
    iou_values: list[float] = []
    objdice_values: list[float] = []
    boundary_f1_values: list[float] = []
    hd95_values: list[float] = []
    object_hausdorff_values: list[float] = []

    for pred_mask, target_mask in zip(pred_masks, target_masks, strict=True):
        sample_metrics = compute_sample_segmentation_metrics(
            pred_mask=pred_mask[0],
            target_mask=target_mask[0],
            boundary_width=boundary_width,
            connectivity=connectivity,
            include_distance_metrics=include_distance_metrics,
        )
        dice_values.append(sample_metrics["dice"])
        iou_values.append(sample_metrics["iou"])
        objdice_values.append(sample_metrics["objdice"])
        boundary_f1_values.append(sample_metrics["boundary_f1"])
        if include_distance_metrics:
            hd95_values.append(sample_metrics["hd95"])
            object_hausdorff_values.append(sample_metrics["object_hausdorff"])

    return {
        "dice": float(np.mean(dice_values)),
        "iou": float(np.mean(iou_values)),
        "objdice": float(np.mean(objdice_values)),
        "boundary_f1": float(np.mean(boundary_f1_values)),
        "f1": float(np.mean(dice_values)),
        "hd95": float(np.mean(hd95_values)) if hd95_values else float("nan"),
        "object_hausdorff": float(np.mean(object_hausdorff_values)) if object_hausdorff_values else float("nan"),
    }
