"""Segmentation losses for the stage02 UNet baseline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: Loss-Survey for medical segmentation
- 章节: BCE-like region supervision and Dice overlap optimization
- 公式/定义: BCEWithLogits + Dice as the first stable binary segmentation objective
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/train/unet_flow_v1.yaml, scripts/train.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前首轮只冻结 `BCE + Dice` 组合，目标是先证明 stage02 训练链能稳定给出 finite loss。
- sigmoid 不放进模型头，而是保留在 loss/eval 侧各自处理，避免训练和评估职责混写。
"""

from __future__ import annotations

from typing import Any

import torch
from torch import nn


class BCEDiceLoss(nn.Module):
    """Formal stage02 binary segmentation loss.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: medical segmentation loss survey
    - 章节: region loss and overlap loss combination
    - 公式/定义: BCEWithLogits(logits, targets) + Dice(probs, targets)
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/train/unet_flow_v1.yaml, src/losses/seg_losses.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 直接返回 `loss_total`、`loss_bce`、`loss_dice` 三个字段，方便 trainer 写日志和 runtime 证据对账。
    - 当前只服务单通道前景分割，不扩到多类或 topology-aware loss。
    """
    def __init__(self, bce_weight: float = 1.0, dice_weight: float = 1.0, eps: float = 1e-6) -> None:
        super().__init__()
        self.bce_weight = bce_weight
        self.dice_weight = dice_weight
        self.eps = eps
        self.bce = nn.BCEWithLogitsLoss()

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> dict[str, torch.Tensor]:
        targets = targets.float()
        loss_bce = self.bce(logits, targets)
        probs = torch.sigmoid(logits)
        dims = tuple(range(1, probs.ndim))
        intersection = torch.sum(probs * targets, dim=dims)
        denom = torch.sum(probs, dim=dims) + torch.sum(targets, dim=dims)
        loss_dice = 1.0 - ((2.0 * intersection + self.eps) / (denom + self.eps))
        loss_dice = loss_dice.mean()
        loss_total = self.bce_weight * loss_bce + self.dice_weight * loss_dice
        return {
            "loss_total": loss_total,
            "loss_bce": loss_bce,
            "loss_dice": loss_dice,
        }


def build_seg_loss(train_config: dict[str, Any]) -> BCEDiceLoss:
    """Build the frozen stage02 BCE+Dice loss from training config.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: medical segmentation loss survey
    - 章节: weighted composition of region and overlap losses
    - 公式/定义: bce_weight * BCE + dice_weight * Dice
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/train/unet_flow_v1.yaml, src/losses/seg_losses.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 参数入口只接受当前训练配置冻结的 `bce_weight`、`dice_weight`、`loss_eps`，不在 builder 里额外引入别名或隐式默认值。
    - 保持 loss 构造和 `scripts/train.py` 的配置解引用语义一致，方便说明文逐层回链。
    """
    return BCEDiceLoss(
        bce_weight=float(train_config["bce_weight"]),
        dice_weight=float(train_config["dice_weight"]),
        eps=float(train_config["loss_eps"]),
    )
