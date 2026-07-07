"""Distance-target helpers for the frozen data protocol."""

from __future__ import annotations

import math

import numpy as np


def _edt_1d(values: np.ndarray) -> np.ndarray:
    length = len(values)
    v = np.zeros(length, dtype=np.int32)
    z = np.zeros(length + 1, dtype=np.float64)
    output = np.zeros(length, dtype=np.float64)
    k = 0
    v[0] = 0
    z[0] = -math.inf
    z[1] = math.inf
    for q in range(1, length):
        s = ((values[q] + q * q) - (values[v[k]] + v[k] * v[k])) / (2.0 * (q - v[k]))
        while s <= z[k]:
            k -= 1
            s = ((values[q] + q * q) - (values[v[k]] + v[k] * v[k])) / (2.0 * (q - v[k]))
        k += 1
        v[k] = q
        z[k] = s
        z[k + 1] = math.inf
    k = 0
    for q in range(length):
        while z[k + 1] < q:
            k += 1
        output[q] = (q - v[k]) * (q - v[k]) + values[v[k]]
    return output


def euclidean_distance_transform(binary_mask: np.ndarray) -> np.ndarray:
    foreground = binary_mask > 0
    height, width = foreground.shape
    inf = float(height * height + width * width + 1)
    grid = np.where(foreground, inf, 0.0).astype(np.float64)
    for y in range(height):
        grid[y, :] = _edt_1d(grid[y, :])
    for x in range(width):
        grid[:, x] = _edt_1d(grid[:, x])
    return np.sqrt(grid, dtype=np.float64)


def normalize_distance_map(distance_map: np.ndarray) -> np.ndarray:
    maximum = float(distance_map.max())
    if maximum <= 0.0:
        return distance_map.astype(np.float32)
    return (distance_map / maximum).astype(np.float32)
