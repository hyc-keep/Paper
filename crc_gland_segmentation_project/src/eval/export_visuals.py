"""Formal visual-export helpers for stage02 test assets.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: gland segmentation evaluation needs visual evidence besides numeric metrics
- 章节: raw / gt / pred / overlay export and error-type summarization
- 公式/定义: evaluated sample rows -> visual bundle png files + error_cases summary
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/test.py, scripts/export_visuals.py, src/eval/export_visuals.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前可视化模块只服务 `TestA/TestB` 正式导出链, 先把四件套和错误归纳做成可重复调用的稳定模块。
- 错误类型采用可解释的启发式归类, 目标是给 stage02 首轮流程排雷提供最小正式观察面, 不把它包装成最终论文级 taxonomy。
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image
from scipy import ndimage


def _parse_float(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return float("nan")
    if text.lower() == "nan":
        return float("nan")
    return float(text)


def _resolve_project_path(project_root: Path, path_value: Any) -> Path:
    path = Path(str(path_value))
    if path.is_absolute():
        return path.resolve()
    return (project_root / path).resolve()


def _load_rgb_image(image_path: Path) -> np.ndarray:
    with Image.open(image_path) as image:
        return np.array(image.convert("RGB"), dtype=np.uint8)


def _load_binary_mask(mask_path: Path) -> np.ndarray:
    with Image.open(mask_path) as mask:
        return (np.array(mask.convert("L"), dtype=np.uint8) > 0).astype(np.uint8)


def _resize_rgb_image(image: np.ndarray, size_hw: tuple[int, int]) -> np.ndarray:
    target_height, target_width = size_hw
    pil_image = Image.fromarray(image.astype(np.uint8), mode="RGB")
    return np.array(pil_image.resize((target_width, target_height), resample=Image.Resampling.BILINEAR), dtype=np.uint8)


def _resize_binary_mask(mask: np.ndarray, size_hw: tuple[int, int]) -> np.ndarray:
    target_height, target_width = size_hw
    pil_mask = Image.fromarray((mask.astype(np.uint8) * 255), mode="L")
    resized = pil_mask.resize((target_width, target_height), resample=Image.Resampling.NEAREST)
    return (np.array(resized, dtype=np.uint8) > 0).astype(np.uint8)


def _save_rgb_image(image: np.ndarray, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image.astype(np.uint8), mode="RGB").save(output_path)


def _save_mask_image(mask: np.ndarray, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((mask.astype(np.uint8) * 255), mode="L").save(output_path)


def load_metrics_rows(metrics_csv_path: Path) -> list[dict[str, str]]:
    """Load the per-sample metric rows from one split-level CSV asset."""
    with metrics_csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def build_overlay_panel(raw_image: np.ndarray, target_mask: np.ndarray, pred_mask: np.ndarray) -> np.ndarray:
    """Build one RGB overlay panel for raw image plus GT/pred masks.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: visual verification for segmentation consistency
    - 章节: overlay inspection of prediction vs target boundary/location
    - 公式/定义: raw_rgb + gt_mask + pred_mask -> overlay_rgb
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/export_visuals.py, scripts/export_visuals.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - GT 统一着色为绿色, prediction 统一着色为红色, 交叠区域自然形成黄色, 方便快速肉眼对账。
    - 输出只保留简单单张 overlay, 不引入额外 plotting 依赖或论文级排版组件。
    """
    overlay = raw_image.astype(np.float32).copy()
    target_bool = target_mask.astype(bool)
    pred_bool = pred_mask.astype(bool)
    overlay[target_bool] = overlay[target_bool] * 0.45 + np.array([0, 255, 0], dtype=np.float32) * 0.55
    overlay[pred_bool] = overlay[pred_bool] * 0.45 + np.array([255, 0, 0], dtype=np.float32) * 0.55
    overlap = np.logical_and(target_bool, pred_bool)
    overlay[overlap] = overlay[overlap] * 0.35 + np.array([255, 255, 0], dtype=np.float32) * 0.65
    return np.clip(overlay, 0, 255).astype(np.uint8)


def _has_merged_prediction(pred_labels: np.ndarray, target_labels: np.ndarray) -> bool:
    pred_ids = [label_id for label_id in np.unique(pred_labels) if label_id != 0]
    for pred_id in pred_ids:
        overlapped = np.unique(target_labels[pred_labels == pred_id])
        overlapped = [target_id for target_id in overlapped if target_id != 0]
        if len(overlapped) >= 2:
            return True
    return False


def _count_missed_small_objects(pred_mask: np.ndarray, target_labels: np.ndarray, target_area: int) -> int:
    missed = 0
    target_ids = [label_id for label_id in np.unique(target_labels) if label_id != 0]
    small_area_threshold = max(128, int(target_area * 0.1))
    for target_id in target_ids:
        target_object = target_labels == target_id
        if int(target_object.sum()) > small_area_threshold:
            continue
        if not np.logical_and(pred_mask.astype(bool), target_object).any():
            missed += 1
    return missed


def classify_failure_type(sample_row: dict[str, Any], pred_mask: np.ndarray, target_mask: np.ndarray) -> str:
    """Classify one evaluated sample into the frozen stage02 failure taxonomy.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: qualitative error review should explain failure modes beyond one aggregate score
    - 章节: case-level failure categorization from mask overlap, connected components and boundary quality
    - 公式/定义: sample metrics + pred_mask + target_mask -> one interpretable failure_type label
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/export_visuals.py, experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 taxonomy 先服务 stage02 首轮流程排雷，只保留 `all_background`、`adhesion_merge`、`small_gland_miss`、`boundary_over_smooth`、`fragmented_complex_region` 五类工程标签。
    - 当前规则优先保持可解释和可复查，不包装成最终论文级错误分类体系。
    """
    pred_bool = pred_mask.astype(bool)
    target_bool = target_mask.astype(bool)
    pred_area = int(pred_bool.sum())
    target_area = int(target_bool.sum())
    if pred_area == 0 and target_area > 0:
        return "all_background"
    if target_area == 0:
        return "fragmented_complex_region"

    pred_labels, pred_count = ndimage.label(pred_bool)
    target_labels, target_count = ndimage.label(target_bool)
    if pred_count > 0 and target_count > 0 and _has_merged_prediction(pred_labels, target_labels):
        return "adhesion_merge"

    missed_small = _count_missed_small_objects(pred_bool.astype(np.uint8), target_labels, target_area)
    if missed_small > 0:
        return "small_gland_miss"

    boundary_f1 = _parse_float(sample_row.get("boundary_f1", "nan"))
    dice = _parse_float(sample_row.get("dice", "nan"))
    if not np.isnan(boundary_f1) and boundary_f1 < 0.4 and (np.isnan(dice) or dice >= 0.35):
        return "boundary_over_smooth"

    if pred_count >= max(target_count + 2, target_count * 2):
        return "fragmented_complex_region"
    return "fragmented_complex_region"


def _prepare_visual_entry(project_root: Path, sample_row: dict[str, Any]) -> dict[str, Any]:
    image_path = _resolve_project_path(project_root, sample_row["image_path"])
    mask_path = _resolve_project_path(project_root, sample_row["mask_path"])
    pred_path = _resolve_project_path(project_root, sample_row["pred_path"])
    raw_image = _load_rgb_image(image_path)
    target_mask = _load_binary_mask(mask_path)
    pred_mask = _load_binary_mask(pred_path)
    if raw_image.shape[:2] != pred_mask.shape:
        raw_image = _resize_rgb_image(raw_image, pred_mask.shape)
    if target_mask.shape != pred_mask.shape:
        target_mask = _resize_binary_mask(target_mask, pred_mask.shape)
    failure_type = classify_failure_type(sample_row, pred_mask, target_mask)
    return {
        "sample_id": str(sample_row["sample_id"]),
        "split_role": str(sample_row["split_role"]),
        "image_path": image_path,
        "mask_path": mask_path,
        "pred_path": pred_path,
        "raw_image": raw_image,
        "target_mask": target_mask,
        "pred_mask": pred_mask,
        "overlay": build_overlay_panel(raw_image, target_mask, pred_mask),
        "failure_type": failure_type,
        "objdice": _parse_float(sample_row.get("objdice", "nan")),
        "dice": _parse_float(sample_row.get("dice", "nan")),
        "boundary_f1": _parse_float(sample_row.get("boundary_f1", "nan")),
    }


def export_prediction_visuals(
    project_root: Path,
    sample_rows: list[dict[str, Any]],
    output_dir: Path,
    max_samples: int = 5,
) -> list[dict[str, Any]]:
    """Export raw / gt / pred / overlay bundles for one split.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: worst-case visual inspection should complement split-level segmentation metrics
    - 章节: low-performing evaluated samples are exported as reproducible raw/gt/pred/overlay bundles
    - 公式/定义: ranked sample_rows + project assets -> visuals/{split}/raw+gt+pred+overlay png files
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/export_visuals.py, scripts/export_visuals.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前按 `objdice` 从低到高挑最差样本，优先保障首轮流程验证先看到真正的坏例子。
    - 当前导出格式固定为四件套 png，避免引入额外 plotting 依赖或不可重导的临时图层。
    """
    if max_samples <= 0:
        return []

    ranked_rows = sorted(sample_rows, key=lambda row: _parse_float(row.get("objdice", "nan")))
    selected_rows = ranked_rows[: min(max_samples, len(ranked_rows))]
    exported_entries: list[dict[str, Any]] = []
    for row in selected_rows:
        entry = _prepare_visual_entry(project_root, row)
        sample_prefix = entry["sample_id"]
        raw_output = output_dir / f"{sample_prefix}_raw.png"
        gt_output = output_dir / f"{sample_prefix}_gt.png"
        pred_output = output_dir / f"{sample_prefix}_pred.png"
        overlay_output = output_dir / f"{sample_prefix}_overlay.png"
        _save_rgb_image(entry["raw_image"], raw_output)
        _save_mask_image(entry["target_mask"], gt_output)
        _save_mask_image(entry["pred_mask"], pred_output)
        _save_rgb_image(entry["overlay"], overlay_output)
        entry["visual_paths"] = {
            "raw": raw_output,
            "gt": gt_output,
            "pred": pred_output,
            "overlay": overlay_output,
        }
        exported_entries.append(entry)
    return exported_entries


def write_error_cases_summary(
    project_root: Path,
    sample_rows: list[dict[str, Any]],
    exported_entries: list[dict[str, Any]],
    output_path: Path,
) -> dict[str, Any]:
    """Write the formal stage02 error-case summary markdown.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: visual error review should keep both split-level counts and concrete hard-case references
    - 章节: aggregate failure summary plus worst-case index page for manual inspection
    - 公式/定义: analyzed sample_rows + exported overlays -> summaries/error_cases.md
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/export_visuals.py, experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 summary 同时保留 split 计数和 worst-case overlay 回指，保证人工复查不用再手工翻全量目录。
    - 当前 `major_failure_modes` 只服务 run_summary 与排查入口，不夸大成最终研究结论。
    """
    analyzed_entries = [_prepare_visual_entry(project_root, row) for row in sample_rows]
    split_counters: dict[str, Counter[str]] = {}
    for entry in analyzed_entries:
        split_counter = split_counters.setdefault(entry["split_role"], Counter())
        split_counter.update([entry["failure_type"]])

    major_failure_modes: list[str] = []
    for counter in split_counters.values():
        for failure_type, _ in counter.most_common(2):
            if failure_type not in major_failure_modes:
                major_failure_modes.append(failure_type)

    exported_map = {entry["sample_id"]: entry for entry in exported_entries}
    lines = [
        "# Error Cases",
        "",
        "- failure_taxonomy_version: `failure_taxonomy_v1`",
        "- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`",
        f"- analyzed_sample_count: `{len(analyzed_entries)}`",
        "",
        "## Split Summary",
        "",
    ]
    for split_role in sorted(split_counters):
        counter = split_counters[split_role]
        lines.append(f"### {split_role}")
        lines.append("")
        lines.append(f"- sample_count: `{sum(counter.values())}`")
        for failure_type, count in counter.most_common():
            lines.append(f"- {failure_type}: `{count}`")
        lines.append("")

    lines.extend(
        [
            "## Worst Cases",
            "",
        ]
    )
    worst_entries = sorted(analyzed_entries, key=lambda entry: entry["objdice"])[: min(6, len(analyzed_entries))]
    for entry in worst_entries:
        overlay_note = "not_exported"
        exported = exported_map.get(entry["sample_id"])
        if exported is not None:
            overlay_note = exported["visual_paths"]["overlay"].relative_to(project_root).as_posix()
        lines.append(
            "- "
            + f"`{entry['split_role']}` / `{entry['sample_id']}` / "
            + f"`failure_type={entry['failure_type']}` / "
            + f"`objdice={entry['objdice']:.6f}` / "
            + f"`dice={entry['dice']:.6f}` / "
            + f"`boundary_f1={entry['boundary_f1']:.6f}` / "
            + f"`overlay={overlay_note}`"
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "major_failure_modes": major_failure_modes,
        "analyzed_sample_count": len(analyzed_entries),
    }


def export_run_visual_assets(run_dir: Path, max_samples_per_split: int = 5) -> dict[str, Any]:
    """Export visuals and error summary for one evaluated run directory.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: evaluated runs should preserve both numeric split tables and reproducible qualitative evidence
    - 章节: split-wise metrics csv plus prediction masks are sufficient to rebuild visual assets
    - 公式/定义: run_dir/testA_metrics.csv + run_dir/testB_metrics.csv + predictions -> visuals + error_cases summary
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/export_visuals.py, scripts/test.py, scripts/export_visuals.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一从 run 目录重建 `visuals/testA`、`visuals/testB` 和 `summaries/error_cases.md`，让完整测试链和重导链共享同一套实现。
    - 当前返回值额外带回 `visual_counts` 和 `major_failure_modes`，便于 `run_meta.yaml` 与 `run_summary.md` 同步回填。
    """
    project_root = run_dir.parents[1]
    exported_entries: list[dict[str, Any]] = []
    visual_counts: dict[str, int] = {}
    all_sample_rows: list[dict[str, Any]] = []
    for split_role in ("testA", "testB"):
        metrics_rows = load_metrics_rows(run_dir / f"{split_role}_metrics.csv")
        sample_rows = [row for row in metrics_rows if row.get("row_type") == "sample"]
        all_sample_rows.extend(sample_rows)
        exported = export_prediction_visuals(
            project_root=project_root,
            sample_rows=sample_rows,
            output_dir=run_dir / "visuals" / split_role,
            max_samples=max_samples_per_split,
        )
        visual_counts[split_role] = len(exported)
        exported_entries.extend(exported)

    error_summary = write_error_cases_summary(
        project_root=project_root,
        sample_rows=all_sample_rows,
        exported_entries=exported_entries,
        output_path=run_dir / "summaries" / "error_cases.md",
    )
    return {
        "visual_counts": visual_counts,
        "major_failure_modes": error_summary["major_failure_modes"],
        "error_cases_path": (run_dir / "summaries" / "error_cases.md").relative_to(project_root).as_posix(),
    }
