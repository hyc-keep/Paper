"""Formal data package entrypoint for the frozen stage02 pipeline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: dataset protocol and preprocessing utilities exposed behind one stable package facade
- 章节: package-level public API for data config, dataset, mask protocol, and transform helpers
- 公式/定义: `src.data` package -> stable imports consumed by the stage02 train entrypoint
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/data/__init__.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前把 dataset、transform、mask 和最小 yaml/config 入口统一收在 `src.data` 包门面后面，避免训练入口到处散写子模块路径。
- 仍保留 boundary/distance 两类辅助对象的导出，但它们是否进入 learning-doc A 类映射由当前轮次单独裁决，不因为被导出就自动升级。
"""

from .boundary_targets import build_boundary_band
from .datasets import (
    DataConfig,
    build_dataset_from_csv,
    build_segmentation_dataset,
    load_data_config,
    resolve_dataset_root,
    simple_yaml_load,
)
from .distance_targets import euclidean_distance_transform, normalize_distance_map
from .mask_ops import binarize_mask_gt_zero, export_binary_mask_png, load_mask_array, resize_binary_mask
from .transforms import AugmentConfig, build_augment_config, build_eval_transform, build_train_transform

__all__ = [
    "DataConfig",
    "binarize_mask_gt_zero",
    "build_dataset_from_csv",
    "build_segmentation_dataset",
    "build_boundary_band",
    "build_augment_config",
    "build_eval_transform",
    "build_train_transform",
    "euclidean_distance_transform",
    "export_binary_mask_png",
    "load_data_config",
    "load_mask_array",
    "normalize_distance_map",
    "resize_binary_mask",
    "resolve_dataset_root",
    "simple_yaml_load",
    "AugmentConfig",
]
