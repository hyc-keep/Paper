"""Formal train/eval transforms for the stage02 UNet baseline.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: U-Net: Convolutional Networks for Biomedical Image Segmentation
- 章节: preprocessing and augmentation before supervised segmentation
- 公式/定义: raw RGB image plus binary mask -> resize/augment/normalize -> tensor pair
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/data/glas.yaml, configs/train/unet_flow_v1.yaml, src/data/datasets.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 stage02 只冻结 `light_aug_v1` 这一套最小增强协议，目标是先保证训练主链和说明文主链都能回到唯一配置来源。
- 训练与验证共用同一组尺寸、归一化和 mask 二值化语义，但把随机增强限制在 train transform，避免 eval 口径漂移。
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from PIL import Image, ImageEnhance
from torchvision.transforms import InterpolationMode, RandomResizedCrop
from torchvision.transforms import functional as TF

from .datasets import DataConfig


@dataclass(frozen=True)
class AugmentConfig:
    """Frozen augmentation knobs parsed from the formal stage02 train config.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: data augmentation practice for biomedical segmentation
    - 章节: lightweight geometric and photometric perturbations
    - 公式/定义: train_config.light_aug -> typed augmentation profile
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/train/unet_flow_v1.yaml, src/data/transforms.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前把 `light_aug_v1` 展开成显式 dataclass 字段，避免后续运行和说明文继续依赖松散字典取值。
    - eval 路径只复用必要的输入变换，不把随机增强字段带入验证阶段。
    """
    aug_version: str
    random_hflip_prob: float
    random_vflip_prob: float
    rotate90_enable: bool
    rotate90_prob: float
    random_resized_crop_prob: float
    crop_scale_range: tuple[float, float]
    crop_ratio_range: tuple[float, float]
    brightness_prob: float
    brightness_limit: float
    contrast_prob: float
    contrast_limit: float
    eval_aug_enable: bool


def build_augment_config(train_config: dict[str, Any]) -> AugmentConfig:
    """Build the frozen stage02 augmentation profile from train config.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: segmentation augmentation parameterization
    - 章节: config-driven augmentation profile construction
    - 公式/定义: train_config.light_aug -> AugmentConfig
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/train/unet_flow_v1.yaml, src/data/transforms.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前只接受正式训练配置里的 `light_aug` 映射，不引入第二套 augmentation profile 入口。
    - builder 会把数值和布尔字段立即显式化，保证 train transform 后续消费语义固定。
    """
    light_aug = train_config.get("light_aug", {})
    if not isinstance(light_aug, dict):
        raise ValueError("light_aug must be a mapping")
    return AugmentConfig(
        aug_version=str(train_config["aug_version"]),
        random_hflip_prob=float(light_aug["random_hflip_prob"]),
        random_vflip_prob=float(light_aug["random_vflip_prob"]),
        rotate90_enable=bool(light_aug["rotate90_enable"]),
        rotate90_prob=float(light_aug["rotate90_prob"]),
        random_resized_crop_prob=float(light_aug["random_resized_crop_prob"]),
        crop_scale_range=(float(light_aug["crop_scale_min"]), float(light_aug["crop_scale_max"])),
        crop_ratio_range=(float(light_aug["crop_ratio_min"]), float(light_aug["crop_ratio_max"])),
        brightness_prob=float(light_aug["brightness_prob"]),
        brightness_limit=float(light_aug["brightness_limit"]),
        contrast_prob=float(light_aug["contrast_prob"]),
        contrast_limit=float(light_aug["contrast_limit"]),
        eval_aug_enable=bool(train_config["eval_aug_enable"]),
    )


def _resize_pair(image: Image.Image, mask: torch.Tensor, size_hw: tuple[int, int]) -> tuple[Image.Image, torch.Tensor]:
    """Resize image/mask pair with modality-safe interpolation rules.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: dense segmentation preprocessing
    - 章节: image resize with bilinear interpolation and mask resize with nearest interpolation
    - 公式/定义: image, mask, target_size -> resized image, resized mask
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/transforms.py, configs/data/glas.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前显式区分图像和 mask 的插值策略，避免二值监督在 resize 环节被平滑污染。
    - resize 入口统一接受 `H, W` 语义，和 data config 的 `input_size` 保持一致。
    """
    height, width = size_hw
    resized_image = image.resize((width, height), resample=Image.Resampling.BILINEAR)
    resized_mask = TF.resize(mask, [height, width], interpolation=InterpolationMode.NEAREST)
    return resized_image, resized_mask


def _random_resized_crop_pair(
    image: Image.Image,
    mask: torch.Tensor,
    size_hw: tuple[int, int],
    scale_range: tuple[float, float],
    ratio_range: tuple[float, float],
) -> tuple[Image.Image, torch.Tensor]:
    """Apply a synchronized random resized crop to image and mask.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: segmentation augmentation with shared geometric transforms
    - 章节: coupled crop parameters for image-mask pairs
    - 公式/定义: shared crop params + target_size -> aligned cropped pair
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/transforms.py, configs/train/unet_flow_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前随机裁剪只在 `light_aug_v1` 条件下启用，并强制图像与 mask 共享同一组 crop 参数。
    - 图像与 mask 仍分别走 bilinear 和 nearest，保持监督边界不被错误插值。
    """
    height, width = size_hw
    i, j, h, w = RandomResizedCrop.get_params(image, scale=scale_range, ratio=ratio_range)
    cropped_image = TF.resized_crop(image, i, j, h, w, [height, width], interpolation=InterpolationMode.BILINEAR)
    cropped_mask = TF.resized_crop(mask, i, j, h, w, [height, width], interpolation=InterpolationMode.NEAREST)
    return cropped_image, cropped_mask


def _adjust_brightness(image: Image.Image, limit: float) -> Image.Image:
    factor = 1.0 + random.uniform(-limit, limit)
    return ImageEnhance.Brightness(image).enhance(factor)


def _adjust_contrast(image: Image.Image, limit: float) -> Image.Image:
    factor = 1.0 + random.uniform(-limit, limit)
    return ImageEnhance.Contrast(image).enhance(factor)


def _normalize_image(image: Image.Image, data_config: DataConfig) -> torch.Tensor:
    """Convert RGB PIL image into normalized CHW float tensor.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: image normalization before convolutional segmentation
    - 章节: float conversion and channel-wise normalization
    - 公式/定义: uint8 RGB image -> float tensor -> normalize by mean/std
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, src/data/transforms.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前固定使用 data config 中冻结的 `normalize_mean` 和 `normalize_std`，不在运行时切换别的统计口径。
    - 归一化输出统一为 `C,H,W`，方便直接送入 stage02 单头 UNet。
    """
    image_np = np.array(image, dtype=np.float32) / 255.0
    image_tensor = torch.from_numpy(image_np).permute(2, 0, 1)
    mean = torch.tensor(data_config.normalize_mean, dtype=torch.float32).view(3, 1, 1)
    std = torch.tensor(data_config.normalize_std, dtype=torch.float32).view(3, 1, 1)
    return (image_tensor - mean) / std


def build_train_transform(
    data_config: DataConfig,
    augment_config: AugmentConfig,
) -> Any:
    """Build the formal stage02 train transform callable.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: train-time augmentation for dense prediction
    - 章节: resize, random flips, rotation, crop, photometric perturbation and normalization
    - 公式/定义: raw pair + AugmentConfig -> normalized train tensor pair
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/transforms.py, configs/data/glas.yaml, configs/train/unet_flow_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 train transform 只实现 `light_aug_v1` 所需的最小几何与光照增强，不提前引入更重的 albumentations 风格流水线。
    - 输出 mask 会再次压成二值 float tensor，确保和 `mask_gt_0` 数据协议保持一致。
    """
    def transform(image: Image.Image, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        image, mask = _resize_pair(image, mask, data_config.input_size)

        if random.random() < augment_config.random_hflip_prob:
            image = TF.hflip(image)
            mask = TF.hflip(mask)

        if random.random() < augment_config.random_vflip_prob:
            image = TF.vflip(image)
            mask = TF.vflip(mask)

        if augment_config.rotate90_enable and random.random() < augment_config.rotate90_prob:
            angle = random.choice((0, 90, 180, 270))
            image = TF.rotate(image, angle, interpolation=InterpolationMode.BILINEAR)
            mask = TF.rotate(mask, angle, interpolation=InterpolationMode.NEAREST)

        if random.random() < augment_config.random_resized_crop_prob:
            image, mask = _random_resized_crop_pair(
                image=image,
                mask=mask,
                size_hw=data_config.input_size,
                scale_range=augment_config.crop_scale_range,
                ratio_range=augment_config.crop_ratio_range,
            )

        if random.random() < augment_config.brightness_prob:
            image = _adjust_brightness(image, augment_config.brightness_limit)

        if random.random() < augment_config.contrast_prob:
            image = _adjust_contrast(image, augment_config.contrast_limit)

        image_tensor = _normalize_image(image, data_config)
        return image_tensor.float(), (mask > 0.5).float()

    return transform


def build_eval_transform(data_config: DataConfig) -> Any:
    """Build the frozen eval transform without random augmentation.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: validation preprocessing consistency
    - 章节: deterministic resize and normalization for evaluation
    - 公式/定义: raw pair + data_config -> normalized eval tensor pair
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, src/data/transforms.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 eval transform 明确不消费随机增强字段，避免验证结果被非确定性变换污染。
    - 评估侧继续沿用和训练侧一致的尺寸与归一化语义，只去掉随机扰动。
    """
    def transform(image: Image.Image, mask: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        image, mask = _resize_pair(image, mask, data_config.input_size)
        return _normalize_image(image, data_config).float(), (mask > 0.5).float()

    return transform
