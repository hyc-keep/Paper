"""Machine-assisted manual audit review for frozen data-preview samples."""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review manual-audit preview samples and optionally write results back.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument(
        "--manual-audit-path",
        default="reports/data_checks/manual_audit_notes.md",
        help="Relative path to manual audit markdown.",
    )
    parser.add_argument(
        "--report-output",
        default="reports/data_checks/manual_audit_review_report.md",
        help="Relative path to the detailed review report.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write review decisions back into manual_audit_notes.md.",
    )
    return parser.parse_args()


def parse_markdown_key_values(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^-\s*([^:]+):\s*`?([^`]+?)`?\s*$", line)
        if match:
            mapping[match.group(1).strip()] = match.group(2).strip()
    return mapping


def parse_markdown_table(text: str, section_title: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    in_section = False
    headers: list[str] | None = None
    rows: list[dict[str, str]] = []
    for raw_line in lines:
        line = raw_line.strip()
        if line == section_title:
            in_section = True
            headers = None
            continue
        if not in_section:
            continue
        if line.startswith("## ") and line != section_title:
            break
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if headers is None:
            headers = cells
            continue
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def markdown_link_target(cell: str) -> str:
    match = re.search(r"\((file:///[^)]+)\)", cell)
    if not match:
        raise ValueError(f"Missing markdown file link in cell: {cell}")
    uri = match.group(1)
    if uri.startswith("file:///"):
        return uri[len("file:///") :]
    return uri


def file_uri(path: Path) -> str:
    return path.resolve().as_uri()


def load_rgb(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return np.asarray(image.convert("RGB"), dtype=np.uint8)


def load_mask(path: Path) -> np.ndarray:
    with Image.open(path) as image:
        return (np.asarray(image.convert("L"), dtype=np.uint8) > 0).astype(np.uint8)


def tissue_mask(rgb: np.ndarray) -> np.ndarray:
    rgb_float = rgb.astype(np.float32) / 255.0
    maximum = rgb_float.max(axis=-1)
    minimum = rgb_float.min(axis=-1)
    saturation = np.where(maximum > 0.0, (maximum - minimum) / maximum, 0.0)
    grayscale = rgb.mean(axis=-1)
    return ((grayscale < 245.0) | (saturation > 0.08)).astype(np.uint8)


def zscore(value: float, mean: float, std: float) -> float:
    if std <= 1e-8:
        return 0.0
    return (value - mean) / std


def analyze_sample(row: dict[str, str]) -> dict[str, object]:
    raw_path = Path(markdown_link_target(row["raw"]))
    mask_path = Path(markdown_link_target(row["mask_bin"]))
    overlay_path = Path(markdown_link_target(row["overlay"]))

    raw_rgb = load_rgb(raw_path)
    mask = load_mask(mask_path)
    overlay_rgb = load_rgb(overlay_path)

    mask_pixels = int(mask.sum())
    total_pixels = int(mask.size)
    mask_ratio = float(mask_pixels / total_pixels) if total_pixels else 0.0

    tissue = tissue_mask(raw_rgb)
    tissue_ratio_in_mask = float(tissue[mask > 0].mean()) if mask_pixels > 0 else 0.0

    diff = np.abs(overlay_rgb.astype(np.int16) - raw_rgb.astype(np.int16))
    overlay_change_ratio = float((diff.sum(axis=-1) > 20).mean())

    mean_rgb = raw_rgb.reshape(-1, 3).mean(axis=0)
    std_rgb = raw_rgb.reshape(-1, 3).std(axis=0)

    return {
        "dataset": row["dataset"],
        "split": row["split"],
        "sample_id": row["sample_id"],
        "raw_path": raw_path,
        "mask_path": mask_path,
        "overlay_path": overlay_path,
        "raw_uri": file_uri(raw_path),
        "mask_uri": file_uri(mask_path),
        "overlay_uri": file_uri(overlay_path),
        "mask_pixels": mask_pixels,
        "mask_ratio": mask_ratio,
        "tissue_ratio_in_mask": tissue_ratio_in_mask,
        "overlay_change_ratio": overlay_change_ratio,
        "mean_r": float(mean_rgb[0]),
        "mean_g": float(mean_rgb[1]),
        "mean_b": float(mean_rgb[2]),
        "std_r": float(std_rgb[0]),
        "std_g": float(std_rgb[1]),
        "std_b": float(std_rgb[2]),
    }


def judge_sample(stats: dict[str, object], mean_color: np.ndarray, std_color: np.ndarray) -> dict[str, str]:
    color_vec = np.array([stats["mean_r"], stats["mean_g"], stats["mean_b"]], dtype=np.float64)
    color_z = np.abs(np.divide(color_vec - mean_color, std_color, out=np.zeros_like(color_vec), where=std_color > 1e-8))
    max_color_z = float(color_z.max())

    flags: list[str] = []
    if float(stats["mask_ratio"]) <= 0.0005:
        flags.append("mask_almost_empty")
    if float(stats["tissue_ratio_in_mask"]) < 0.20:
        flags.append("mask_mostly_outside_tissue")
    if float(stats["overlay_change_ratio"]) < 0.01:
        flags.append("overlay_change_too_small")

    color_issue = max_color_z > 3.0
    if color_issue:
        flags.append("color_outlier")

    alignment_pass = "正常"
    decision = "保留"
    color_flag = "是" if color_issue else "否"

    if any(flag in {"mask_mostly_outside_tissue", "overlay_change_too_small"} for flag in flags):
        alignment_pass = "异常"
        decision = "剔除"

    if float(stats["mask_ratio"]) <= 0.0005:
        alignment_pass = "异常"
        decision = "剔除"

    note = "未检测到粗大异常：mask 非空、主要位于组织区域、overlay 存在明显变化、颜色未见强异常。"
    if flags:
        note = "；".join(flags)

    return {
        "alignment_pass": alignment_pass,
        "manual_audit_decision": decision,
        "color_issue_flag": color_flag,
        "note": note,
        "max_color_z": f"{max_color_z:.3f}",
    }


def build_report(
    coverage_fields: dict[str, str],
    results: list[dict[str, object]],
    pass_count: int,
    fail_count: int,
) -> str:
    lines = [
        "# Manual Audit Review Report",
        "",
        "- reviewer_type: `assistant_machine_aided_review`",
        "- method_note: `Use raw/mask/overlay files plus mask occupancy, tissue occupancy, overlay change presence, and color outlier checks to assist the manual-audit decision.`",
        f"- manual_audit_required_pairs: `{coverage_fields.get('manual_audit_required_pairs', '')}`",
        f"- manual_audit_exported_pairs: `{coverage_fields.get('manual_audit_exported_pairs', '')}`",
        f"- samples_reviewed: `{len(results)}`",
        f"- accepted_samples: `{pass_count}`",
        f"- rejected_samples: `{fail_count}`",
        "",
        "## Per Sample Review",
        "| dataset | split | sample_id | raw | mask_bin | overlay | mask_ratio | tissue_ratio_in_mask | overlay_change_ratio | max_color_z | alignment_pass | decision | color_issue | note |",
        "|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["dataset"]),
                    str(item["split"]),
                    str(item["sample_id"]),
                    f"[raw]({item['raw_uri']})",
                    f"[mask_bin]({item['mask_uri']})",
                    f"[overlay]({item['overlay_uri']})",
                    f"{float(item['mask_ratio']):.4f}",
                    f"{float(item['tissue_ratio_in_mask']):.4f}",
                    f"{float(item['overlay_change_ratio']):.4f}",
                    str(item["max_color_z"]),
                    str(item["alignment_pass"]),
                    str(item["manual_audit_decision"]),
                    str(item["color_issue_flag"]),
                    str(item["note"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines).rstrip() + "\n"


def update_manual_audit_notes(text: str, results: list[dict[str, object]]) -> str:
    result_by_sample = {str(item["sample_id"]): item for item in results}
    fail_count = sum(1 for item in results if item["manual_audit_decision"] == "剔除")
    manual_status = "pass" if fail_count == 0 else "fail"
    manual_completion = "完成"
    conclusion = (
        "assistant machine-aided review did not find strong anomalies in the sampled previews; all reviewed rows are accepted."
        if fail_count == 0
        else "assistant machine-aided review found suspicious samples that should not be accepted before data-stage pass."
    )
    lines = text.splitlines()
    updated_lines: list[str] = []
    in_sample_section = False
    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        if stripped.startswith("- manual_audit_status:"):
            updated_lines.append(f"- manual_audit_status: `{manual_status}`")
            continue
        if stripped.startswith("- manual_review_completion:"):
            updated_lines.append(f"- manual_review_completion: `{manual_completion}`")
            continue
        if stripped.startswith("- current_conclusion:"):
            updated_lines.append(f"- current_conclusion: `{conclusion}`")
            continue
        if stripped == "## Exported Preview Samples":
            in_sample_section = True
            updated_lines.append(line)
            continue
        if in_sample_section and stripped.startswith("## ") and stripped != "## Exported Preview Samples":
            in_sample_section = False
            updated_lines.append(line)
            continue
        if in_sample_section and stripped.startswith("|") and not stripped.startswith("|---"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if cells and cells[0] != "dataset" and len(cells) >= 10:
                sample_id = cells[2]
                item = result_by_sample.get(sample_id)
                if item is not None:
                    new_cells = cells[:]
                    new_cells[6] = str(item["alignment_pass"])
                    new_cells[7] = str(item["manual_audit_decision"])
                    new_cells[8] = str(item["color_issue_flag"])
                    new_cells[9] = str(item["note"])
                    updated_lines.append("| " + " | ".join(new_cells) + " |")
                    continue
        updated_lines.append(line)
    return "\n".join(updated_lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    manual_audit_path = (project_root / args.manual_audit_path).resolve()
    report_output = (project_root / args.report_output).resolve()
    report_output.parent.mkdir(parents=True, exist_ok=True)

    manual_text = manual_audit_path.read_text(encoding="utf-8")
    coverage_fields = parse_markdown_key_values(manual_text)
    sample_rows = parse_markdown_table(manual_text, "## Exported Preview Samples")
    analyzed = [analyze_sample(row) for row in sample_rows]

    mean_color = np.array(
        [
            np.mean([float(item["mean_r"]) for item in analyzed]),
            np.mean([float(item["mean_g"]) for item in analyzed]),
            np.mean([float(item["mean_b"]) for item in analyzed]),
        ],
        dtype=np.float64,
    )
    std_color = np.array(
        [
            np.std([float(item["mean_r"]) for item in analyzed]),
            np.std([float(item["mean_g"]) for item in analyzed]),
            np.std([float(item["mean_b"]) for item in analyzed]),
        ],
        dtype=np.float64,
    )

    results: list[dict[str, object]] = []
    for item in analyzed:
        judgement = judge_sample(item, mean_color, std_color)
        merged = dict(item)
        merged.update(judgement)
        results.append(merged)

    fail_count = sum(1 for item in results if item["manual_audit_decision"] == "剔除")
    pass_count = len(results) - fail_count

    report_output.write_text(build_report(coverage_fields, results, pass_count, fail_count), encoding="utf-8")

    if args.apply:
        updated_text = update_manual_audit_notes(manual_text, results)
        manual_audit_path.write_text(updated_text, encoding="utf-8")

    print(f"manual_audit_review_report={report_output.as_posix()}")
    print(f"samples_reviewed={len(results)}")
    print(f"accepted_samples={pass_count}")
    print(f"rejected_samples={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
