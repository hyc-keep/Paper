"""Standard single-head UNet for the stage02 baseline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
- 章节: encoder-decoder with skip connections
- 公式/定义: contracting path + expanding path + skip fusion for dense prediction
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/model/unet_v1.yaml, scripts/train.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前只保留标准单头 UNet, 不提前引入预训练 encoder、attention 或多任务分支。
- 通道宽度由 `configs/model/unet_v1.yaml` 冻结在 `base_channels=32`, 方便和 runtime 证据对齐。
"""

from __future__ import annotations

from typing import Any

import torch
from torch import nn


class DoubleConv(nn.Module):
    """Two 3x3 conv blocks used as the basic stage02 feature unit.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
    - 章节: repeated conv blocks in each encoder/decoder stage
    - 公式/定义: local feature extraction before down/up sampling
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/models/unet.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一采用 Conv-BN-ReLU 两次的轻量块，优先保证 stage02 闭环可复现。
    - 不引入 residual、dropout 或 attention 子结构，避免当前阶段解释边界失控。
    """
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class DownBlock(nn.Module):
    """Encoder down-sampling block used by the stage02 UNet.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net
    - 章节: contracting path
    - 公式/定义: max-pool then local convolutional refinement
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/models/unet.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前下采样统一固定为 2x2 max-pool，再进入 `DoubleConv`，保证结构足够标准。
    - 不在这里引入 stride-conv 变体，避免和 frozen `unet_v1` 结构分叉。
    """
    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv = DoubleConv(in_channels, out_channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(self.pool(x))


class UpBlock(nn.Module):
    """Decoder up-sampling block with skip fusion for stage02.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net
    - 章节: expanding path with skip connections
    - 公式/定义: upsample + concatenate skip feature + local refinement
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/models/unet.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前使用 bilinear upsample 并在尺寸不齐时 pad，对齐 histology 输入尺寸上的边界差异。
    - 不使用 transposed convolution，优先减少当前阶段对额外参数和伪影解释负担。
    """
    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
        self.conv = DoubleConv(in_channels + skip_channels, out_channels)

    def forward(self, x: torch.Tensor, skip: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        diff_y = skip.size(2) - x.size(2)
        diff_x = skip.size(3) - x.size(3)
        if diff_y or diff_x:
            x = nn.functional.pad(
                x,
                [diff_x // 2, diff_x - diff_x // 2, diff_y // 2, diff_y - diff_y // 2],
            )
        x = torch.cat([skip, x], dim=1)
        return self.conv(x)


class UNet(nn.Module):
    """Stage02 formal single-output UNet model.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
    - 章节: full encoder-decoder segmentation architecture
    - 公式/定义: RGB image -> feature pyramid -> single-channel gland logit
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/model/unet_v1.yaml, scripts/train.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 输入固定 `in_channels=3`，输出固定 `out_channels=1`，和 GlaS 二值腺体分割协议保持一致。
    - 当前模型只输出单通道 logits，把 sigmoid 与 threshold 留给 loss/eval 支路处理，避免职责混合。
    """
    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 1,
        base_channels: int = 32,
    ) -> None:
        super().__init__()
        self.inc = DoubleConv(in_channels, base_channels)
        self.down1 = DownBlock(base_channels, base_channels * 2)
        self.down2 = DownBlock(base_channels * 2, base_channels * 4)
        self.down3 = DownBlock(base_channels * 4, base_channels * 8)
        self.down4 = DownBlock(base_channels * 8, base_channels * 16)
        self.up1 = UpBlock(base_channels * 16, base_channels * 8, base_channels * 8)
        self.up2 = UpBlock(base_channels * 8, base_channels * 4, base_channels * 4)
        self.up3 = UpBlock(base_channels * 4, base_channels * 2, base_channels * 2)
        self.up4 = UpBlock(base_channels * 2, base_channels, base_channels)
        self.outc = nn.Conv2d(base_channels, out_channels, kernel_size=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.down4(x4)
        x = self.up1(x5, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        return self.outc(x)


def build_unet_model(model_config: dict[str, Any]) -> UNet:
    """Build the formal stage02 UNet from frozen model config.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
    - 章节: architecture instantiation from predefined channel settings
    - 公式/定义: config -> in_channels / out_channels / base_channels -> UNet instance
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/model/unet_v1.yaml, src/models/unet.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前只暴露 `in_channels`、`out_channels`、`base_channels` 三个冻结入口，避免 stage02 早期把模型工厂做成可随意漂移的实验沙盒。
    - 由 experiment config 统一回链到 `configs/model/unet_v1.yaml`，保持 learning-doc 和 runtime 证据的参数来源一致。
    """
    return UNet(
        in_channels=int(model_config["in_channels"]),
        out_channels=int(model_config["out_channels"]),
        base_channels=int(model_config["base_channels"]),
    )
