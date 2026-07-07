"""Formal binary-mask helpers for the frozen stage02 data protocol.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: binary gland-mask supervision under frozen segmentation protocol
- 章节: mask reading, positive-pixel binarization, and nearest-neighbor resizing
- 公式/定义: raw mask asset -> binary gland mask -> export or resized binary target
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/data/glas.yaml, src/data/mask_ops.py, src/data/datasets.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 mask 协议固定为 `mask_gt_0`，不在数据层保留多值实例编码语义，避免训练主链再做二次解释。
- resize 始终使用最近邻，保证二值边界不会因为插值方式被偷偷软化。
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def load_mask_array(mask_path: Path) -> np.ndarray:
    """Load one raw mask asset as a uint8 grayscale array.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: grayscale mask asset loading before binary supervision conversion
    - 章节: raw annotation image -> in-memory mask array
    - 公式/定义: mask file path -> uint8 grayscale array
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: datasets/01_GlaS_official_raw/*.bmp, src/data/mask_ops.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一转成 `L` 通道再读成 `uint8`，保证后续二值化动作只面对一种确定输入格式。
    - 这里只负责把磁盘资产读出来，不在这里混入 transform 或 tensor 语义。
    """
    with Image.open(mask_path) as mask_image:
        return np.array(mask_image.convert("L"), dtype=np.uint8)


def binarize_mask_gt_zero(mask_array: np.ndarray) -> np.ndarray:
    """Apply the frozen `mask_gt_0` positive rule to one mask array.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: binary foreground supervision derived from positive-valued mask pixels
    - 章节: positive pixel thresholding for gland-vs-background labels
    - 公式/定义: mask_array > 0 -> binary uint8 mask
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, src/data/mask_ops.py, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前正样本判定固定写死为大于零，和正式 data config 的 `mask_positive_rule=mask_gt_0` 保持完全一致。
    - 返回值固定为 `uint8` 二值阵列，方便后续 dataset 层再统一转成 float tensor。
    """
    return (mask_array > 0).astype(np.uint8)


def export_binary_mask_png(binary_mask: np.ndarray, output_path: Path) -> None:
    """Export one binary mask array as a formal grayscale PNG file.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: binary segmentation targets serialized as grayscale foreground maps
    - 章节: binary mask export for inspection or downstream reuse
    - 公式/定义: binary uint8 mask -> 0/255 png asset
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/mask_ops.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前导出时固定把二值 mask 放大成 `0/255` 灰度图，方便人工检查时直接看清前景背景。
    - 先保证父目录存在，再写文件，避免辅助导出动作因为目录不存在而额外失败。
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((binary_mask * 255).astype(np.uint8), mode="L").save(output_path)


def resize_binary_mask(binary_mask: np.ndarray, size_hw: tuple[int, int]) -> np.ndarray:
    """Resize one binary mask with nearest-neighbor semantics.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: discrete label maps should preserve hard class boundaries when resized
    - 章节: nearest-neighbor interpolation for categorical targets
    - 公式/定义: binary mask + target size -> resized binary mask
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/mask_ops.py, src/data/transforms.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前显式使用最近邻插值，避免腺体边界在 resize 过程中被线性插值弄成灰度软标签。
    - resize 后再次做大于零二值化，保证输出仍然回到干净的二值监督格式。
    """
    target_height, target_width = size_hw
    image = Image.fromarray((binary_mask * 255).astype(np.uint8), mode="L")
    resized = image.resize((target_width, target_height), resample=Image.Resampling.NEAREST)
    return (np.array(resized, dtype=np.uint8) > 0).astype(np.uint8)
