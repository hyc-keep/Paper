"""Boundary-target helpers for the frozen data protocol."""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter


def build_boundary_band(binary_mask: np.ndarray, width: int = 3) -> np.ndarray:
    if width not in {3, 5}:
        raise ValueError(f"Unsupported boundary width: {width}")
    base = Image.fromarray((binary_mask > 0).astype(np.uint8) * 255, mode="L")
    max_filter = ImageFilter.MaxFilter(size=width)
    min_filter = ImageFilter.MinFilter(size=width)
    dilated = np.array(base.filter(max_filter), dtype=np.uint8)
    eroded = np.array(base.filter(min_filter), dtype=np.uint8)
    return ((dilated > eroded) & (binary_mask > 0)).astype(np.uint8)

