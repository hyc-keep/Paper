"""Learning-rate scheduler helpers for stage02 training.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: validation-driven learning-rate adaptation
- 章节: ReduceLROnPlateau on monitored validation metric
- 公式/定义: optimizer + train_config scheduler fields -> ReduceLROnPlateau scheduler
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/train/unet_flow_v1.yaml, src/engine/trainer.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 stage02 只冻结 `ReduceLROnPlateau` 这一种 scheduler，目标是先把 `val_objdice` 驱动的最小闭环讲清楚。
- scheduler mode 被显式钉成 `max`，和当前 `best_selector=val_objdice_max` 保持一致，不再让调用方二次猜测。
"""

from __future__ import annotations

from typing import Any

from torch.optim import Optimizer
from torch.optim.lr_scheduler import ReduceLROnPlateau


def build_scheduler(optimizer: Optimizer, train_config: dict[str, Any]) -> ReduceLROnPlateau:
    """Build the frozen stage02 ReduceLROnPlateau scheduler from train config.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: plateau-based learning-rate decay
    - 章节: reduce learning rate when monitored validation metric stalls
    - 公式/定义: scheduler config + optimizer -> ReduceLROnPlateau(mode=max)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/train/unet_flow_v1.yaml, src/engine/lr_scheduler.py, scripts/train.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 builder 只接受正式训练配置里的 `scheduler=ReduceLROnPlateau`，不支持多 scheduler 分支。
    - `factor`、`patience`、`min_lr` 全部从冻结配置显式解引用，便于说明文和运行结果逐项对账。
    """
    scheduler_name = str(train_config["scheduler"]).strip()
    if scheduler_name != "ReduceLROnPlateau":
        raise ValueError(f"Unsupported scheduler: {scheduler_name}")
    return ReduceLROnPlateau(
        optimizer=optimizer,
        mode="max",
        factor=float(train_config["scheduler_factor"]),
        patience=int(train_config["scheduler_patience"]),
        min_lr=float(train_config["scheduler_min_lr"]),
    )
