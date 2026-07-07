"""Formal loss package entrypoint for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: one frozen segmentation loss builder exposed as the public package API
- 章节: package facade for stable BCE+Dice loss construction
- 公式/定义: `src.losses` package -> `build_seg_loss()` and `BCEDiceLoss` as the formal loss-facing API
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/losses/__init__.py, src/losses/seg_losses.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前包门面只公开 `BCEDiceLoss` 与 `build_seg_loss`，保证训练主链在入口层只面对已经冻结的损失对象。
- 训练入口统一从 `src.losses` 取 builder，而不是直接扎到具体实现文件，方便说明文把“正式公开入口”和“底层实现”分层讲清。
"""

from .seg_losses import BCEDiceLoss, build_seg_loss

__all__ = ["BCEDiceLoss", "build_seg_loss"]
