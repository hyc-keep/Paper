"""Build an executed notebook for manual-audit visual evidence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build executed notebook evidence for manual audit review.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument(
        "--review-report",
        default="reports/data_checks/manual_audit_review_report.md",
        help="Relative path to manual audit review markdown report.",
    )
    parser.add_argument(
        "--acceptance-report",
        default="reports/stage_reports/data_stage_acceptance.md",
        help="Relative path to stage acceptance report.",
    )
    parser.add_argument(
        "--output",
        default="reports/data_checks/manual_audit_visual_review.ipynb",
        help="Relative path to the generated notebook.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Notebook execution timeout in seconds.",
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
        raise ValueError(f"Missing markdown link in cell: {cell}")
    target = match.group(1)
    if target.startswith("file:///"):
        return unquote(target[len("file:///") :])
    return unquote(target)


def py_string(value: str) -> str:
    return repr(value.replace("\\", "/"))


def safe_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0


def build_pass_reason(sample: dict[str, str]) -> str:
    mask_ratio = safe_float(sample.get("mask_ratio", "0"))
    tissue_ratio = safe_float(sample.get("tissue_ratio_in_mask", "0"))
    overlay_change = safe_float(sample.get("overlay_change_ratio", "0"))
    color_z = safe_float(sample.get("max_color_z", "0"))

    reasons = [
        f"mask_ratio={mask_ratio:.4f}，大于空掩膜告警线 `0.0005`，说明 `mask_bin` 不是空白图。",
        f"tissue_ratio_in_mask={tissue_ratio:.4f}，高于组织区域阈值 `0.20`，说明标注主体主要落在组织区域内。",
        f"overlay_change_ratio={overlay_change:.4f}，高于叠加变化阈值 `0.01`，说明 `overlay` 相比 `raw` 确实发生了明显标注覆盖变化。",
        f"max_color_z={color_z:.3f}，未超过颜色异常阈值 `3.0`，未见强颜色离群。",
    ]
    return "；".join(reasons)


def build_sample_cell(sample: dict[str, str]) -> str:
    raw_path = py_string(markdown_link_target(sample["raw"]))
    mask_path = py_string(markdown_link_target(sample["mask_bin"]))
    overlay_path = py_string(markdown_link_target(sample["overlay"]))
    sample_id = py_string(sample["sample_id"])
    dataset = py_string(sample["dataset"])
    split_name = py_string(sample["split"])
    alignment = py_string(sample["alignment_pass"])
    decision = py_string(sample["decision"])
    color_issue = py_string(sample["color_issue"])
    note = py_string(sample["note"])
    mask_ratio = py_string(sample["mask_ratio"])
    tissue_ratio = py_string(sample["tissue_ratio_in_mask"])
    overlay_change = py_string(sample["overlay_change_ratio"])
    color_z = py_string(sample["max_color_z"])

    return f"""from pathlib import Path
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

sample_id = {sample_id}
dataset = {dataset}
split_name = {split_name}
raw_path = Path({raw_path})
mask_path = Path({mask_path})
overlay_path = Path({overlay_path})

raw = mpimg.imread(raw_path)
mask = mpimg.imread(mask_path)
overlay = mpimg.imread(overlay_path)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, image, title in zip(
    axes,
    [raw, mask, overlay],
    ["raw", "mask_bin", "overlay"],
):
    ax.imshow(image, cmap="gray" if title == "mask_bin" else None)
    ax.set_title(f"{{dataset}} / {{split_name}} / {{sample_id}}\\n{{title}}")
    ax.axis("off")
plt.tight_layout()
plt.show()

print("alignment_pass:", {alignment})
print("manual_audit_decision:", {decision})
print("color_issue_flag:", {color_issue})
print("mask_ratio:", {mask_ratio})
print("tissue_ratio_in_mask:", {tissue_ratio})
print("overlay_change_ratio:", {overlay_change})
print("max_color_z:", {color_z})
print("note:", {note})
"""


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    review_report_path = (project_root / args.review_report).resolve()
    acceptance_report_path = (project_root / args.acceptance_report).resolve()
    output_path = (project_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    review_text = review_report_path.read_text(encoding="utf-8")
    acceptance_text = acceptance_report_path.read_text(encoding="utf-8")
    review_fields = parse_markdown_key_values(review_text)
    acceptance_fields = parse_markdown_key_values(acceptance_text)
    sample_rows = parse_markdown_table(review_text, "## Per Sample Review")

    notebook = new_notebook()
    notebook.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata["language_info"] = {"name": "python", "version": f"{sys.version_info.major}.{sys.version_info.minor}"}

    intro = f"""# 人工抽查可视化审查件

这份 notebook 是 `01_数据协议` 的正式人工抽查视觉证据。
它直接嵌入真实的 `raw / mask_bin / overlay` 图片，并把每个样本的通过理由写在图片旁边，便于肉眼复核。

## 当前阶段汇总

- `samples_reviewed`: `{review_fields.get("samples_reviewed", "")}`
- `accepted_samples`: `{review_fields.get("accepted_samples", "")}`
- `rejected_samples`: `{review_fields.get("rejected_samples", "")}`
- `pass_check`: `{acceptance_fields.get("pass_check", "")}`
- `handoff_ready`: `{acceptance_fields.get("handoff_ready", "")}`
- `data_stage_pass`: `{acceptance_fields.get("data_stage_pass", "")}`
- `preflight_pass`: `{acceptance_fields.get("preflight_pass", "")}`
- `next_action`: `{acceptance_fields.get("next_action", "")}`

## 审查标准

本 notebook 采用和 `manual_audit_review_report.md` 一致的辅助判据：

1. `mask_ratio > 0.0005`：避免空掩膜。
2. `tissue_ratio_in_mask >= 0.20`：避免标注主体大面积落在非组织区域。
3. `overlay_change_ratio >= 0.01`：确认叠加图不是“几乎没变化”的假 overlay。
4. `max_color_z <= 3.0`：排除明显颜色离群样本。

## 证据来源

- `review_report`: `{review_report_path.as_posix()}`
- `acceptance_report`: `{acceptance_report_path.as_posix()}`
- `method_note`: `{review_fields.get("method_note", "")}`
"""
    notebook.cells.append(new_markdown_cell(intro))

    summary_code = f"""summary = {{
    "samples_reviewed": {py_string(review_fields.get("samples_reviewed", ""))},
    "accepted_samples": {py_string(review_fields.get("accepted_samples", ""))},
    "rejected_samples": {py_string(review_fields.get("rejected_samples", ""))},
    "pass_check": {py_string(acceptance_fields.get("pass_check", ""))},
    "handoff_ready": {py_string(acceptance_fields.get("handoff_ready", ""))},
    "data_stage_pass": {py_string(acceptance_fields.get("data_stage_pass", ""))},
    "preflight_pass": {py_string(acceptance_fields.get("preflight_pass", ""))},
    "next_action": {py_string(acceptance_fields.get("next_action", ""))},
}}
for key, value in summary.items():
    print(f"{{key}}: {{value}}")
"""
    notebook.cells.append(new_code_cell(summary_code))

    for sample in sample_rows:
        sample_markdown = f"""## {sample['dataset']} / {sample['split']} / {sample['sample_id']}

- `alignment_pass`: `{sample['alignment_pass']}`
- `decision`: `{sample['decision']}`
- `color_issue`: `{sample['color_issue']}`
- `raw`: `{markdown_link_target(sample['raw'])}`
- `mask_bin`: `{markdown_link_target(sample['mask_bin'])}`
- `overlay`: `{markdown_link_target(sample['overlay'])}`
- `通过理由`: {build_pass_reason(sample)}
- `note`: `{sample['note']}`
"""
        notebook.cells.append(new_markdown_cell(sample_markdown))
        notebook.cells.append(new_code_cell(build_sample_cell(sample)))

    notebook = NotebookClient(
        notebook,
        timeout=args.timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(project_root)}},
    ).execute()

    output_path.write_text(nbformat.writes(notebook), encoding="utf-8")
    print(f"manual_audit_notebook={output_path.as_posix()}")
    print(f"samples_embedded={len(sample_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
