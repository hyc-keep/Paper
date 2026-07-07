"""Seed helpers for reproducible stage02 runs.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: reproducible deep-learning experiment setup
- 章节: align Python, NumPy and PyTorch random states
- 公式/定义: one frozen train_seed -> synchronized random generators
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml, scripts/train.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前正式 run 先把 `train_seed` 对齐到 Python、NumPy 和 Torch，再进入 dataset/model/training 构图，避免运行元数据和真实行为断链。
- worker 级种子逻辑单独保留在同一文件里，方便后续 dataloader 扩 worker 时沿用同一口径。
"""

from __future__ import annotations

import random

import numpy as np
import torch


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy and Torch RNGs with the frozen stage02 train seed.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: experiment reproducibility across software RNG backends
    - 章节: global seeding before data/model/training construction
    - 公式/定义: train_seed -> random.seed, np.random.seed, torch.manual_seed
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/train.py, src/utils/seed.py, configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前训练入口会在构造 transform、dataset、model 和 optimizer 之前调用这里，保证正式 run 元信息和随机行为一起冻结。
    - 若 CUDA 可用，会同步补 `torch.cuda.manual_seed_all()`，避免 GPU 路径落到另一套随机状态。
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def seed_worker(worker_id: int) -> None:
    """Derive a per-worker RNG seed from the active Torch worker seed base.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: dataloader worker reproducibility
    - 章节: propagate deterministic worker-local seeds to Python and NumPy
    - 公式/定义: torch.initial_seed modulo 2**32 plus worker_id -> Python/NumPy worker seeds
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/utils/seed.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 stage02 正式 DataLoader 仍使用 `num_workers=0`，但保留 worker seeding helper，方便后续扩 worker 时不另起一套口径。
    - 只同步 Python 和 NumPy worker 随机源，保持 helper 轻量且和当前工程使用面一致。
    """
    worker_seed = torch.initial_seed() % 2**32
    random.seed(worker_seed + worker_id)
    np.random.seed(worker_seed + worker_id)
