"""Validate the formal data-stage handoff chain for 01_数据协议.

对应阶段: 01_数据协议
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark data integrity, readiness and evaluation preconditions
- 公式/定义: 阶段验收不能只看单个文件是否存在，还要同时验证 split、check、preview、label 与 preflight 入口是否共同闭环
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: tools/stage01_data_protocol/validate_data_assets.py
- commit: workspace_local_20260705
- 许可证: project_internal
本项目调整: 输出 `data_asset_validation_report.md`、`asset_manifest.json` 和 `data_stage_acceptance.md`，并给出 `handoff_ready / data_stage_pass / preflight_pass`。
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.datasets import load_data_config, resolve_dataset_root, resolve_split_csv


EXPECTED_SPLITS: dict[str, tuple[str, ...]] = {
    "glas": ("train", "val", "testA", "testB"),
    "crag": ("train", "val", "test"),
}
PREVIEW_SPLIT_DIR: dict[str, dict[str, str]] = {
    "glas": {"train": "train68", "val": "val17", "testA": "testA60", "testB": "testB20"},
    "crag": {"train": "train153", "val": "val20", "test": "test40"},
}
CHECK_ASSET_PATHS = {
    "data_check_report": "reports/data_checks/data_check_report.md",
    "dataset_stats": "reports/data_checks/dataset_stats.csv",
    "duplicate_check_report": "reports/data_checks/duplicate_check_report.md",
    "foreground_summary": "reports/data_checks/foreground_summary.csv",
    "object_size_summary": "reports/data_checks/object_size_summary.csv",
    "manual_audit_notes": "reports/data_checks/manual_audit_notes.md",
}
LABEL_ASSET_PATHS = {
    "label_protocol_report": "reports/data_checks/label_protocol_report.md",
    "binary_mask_summary": "reports/data_checks/binary_mask_summary.csv",
    "boundary_target_report": "reports/data_checks/boundary_target_report.md",
    "distance_target_report": "reports/data_checks/distance_target_report.md",
}
SOURCE_ASSET_PATHS = (
    "datasets/DATASETS_README.md",
    "datasets/DATASET_SOURCE_NOTES.md",
)
CONFIG_ASSET_PATHS = (
    "configs/data/glas.yaml",
    "configs/data/crag.yaml",
)
POSITIVE_TOKENS = {
    "pass", "true", "yes", "y", "ok", "keep", "accept", "accepted", "complete",
    "正常", "通过", "保留", "完成", "是",
}
NEGATIVE_TOKENS = {
    "fail", "false", "no", "n", "reject", "rejected", "blocked",
    "异常", "不通过", "剔除", "拒绝", "否",
}
PENDING_TOKENS = {"pending_review", "pending", "unknown", "", "todo", "na", "n/a", "待审阅", "待定", "未知"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate formal data-stage assets and handoff gates.")
    parser.add_argument(
        "--project-root",
        default=str(PROJECT_ROOT),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--dataset",
        choices=("glas", "crag", "all"),
        default="all",
        help="Which frozen dataset config to validate.",
    )
    parser.add_argument(
        "--output",
        default="reports/data_checks/data_asset_validation_report.md",
        help="Relative markdown report output path.",
    )
    parser.add_argument(
        "--acceptance-output",
        default="reports/stage_reports/data_stage_acceptance.md",
        help="Relative markdown output path for the formal data-stage acceptance report.",
    )
    parser.add_argument(
        "--asset-manifest-output",
        default="reports/stage_reports/asset_manifest.json",
        help="Relative JSON output path for the formal asset manifest.",
    )
    return parser.parse_args()


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_markdown_key_values(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = re.match(r"^-\s*([^:]+):\s*`?([^`]+?)`?\s*$", line)
        if match:
            mapping[match.group(1).strip()] = normalize_relpath(match.group(2))
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


def classify_token(value: str) -> str:
    """Normalize review/status tokens into positive/negative/pending buckets.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark review and readiness state normalization
    - 公式/定义: 阶段验收字段需要被稳定归一，避免人工审稿和 markdown 写法差异影响正式裁决
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 同时兼容英文和中文状态词，例如 `pass / fail / 待定 / 通过 / 不通过`。
    """
    token = value.strip().lower()
    if token in POSITIVE_TOKENS:
        return "positive"
    if token in NEGATIVE_TOKENS:
        return "negative"
    if token in PENDING_TOKENS:
        return "pending"
    return "unknown"


def derive_manual_audit_status(manual_text: str) -> tuple[str, bool]:
    """Summarize the manual audit markdown into a stage-level audit status.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark manual review and visual audit preconditions
    - 公式/定义: 人工抽查既要看覆盖率，也要看每个样本的对齐结论和人工决策是否真实闭环
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 将 `manual_audit_coverage_status`、`manual_review_completion` 与导出表逐行结果压成 `pass / partial / fail`。
    """
    manual_fields = parse_markdown_key_values(manual_text)
    coverage_pass = manual_fields.get("manual_audit_coverage_status") == "pass"
    completion_done = classify_token(manual_fields.get("manual_review_completion", "")) == "positive"
    rows = parse_markdown_table(manual_text, "## Exported Preview Samples")
    if not rows:
        return "partial", False

    has_pending = False
    has_failure = False
    for row in rows:
        alignment_state = classify_token(row.get("alignment_pass", ""))
        decision_state = classify_token(row.get("manual_audit_decision", ""))
        color_state = classify_token(row.get("color_issue_flag", ""))
        if alignment_state != "positive" or decision_state != "positive":
            if alignment_state == "negative" or decision_state == "negative":
                has_failure = True
            else:
                has_pending = True
        if color_state in {"pending", "unknown"}:
            has_pending = True

    if coverage_pass and completion_done and not has_pending and not has_failure:
        return "pass", True
    if has_failure:
        return "fail", False
    return "partial", False


def count_preview_files(split_dir: Path) -> dict[str, int]:
    """Count raw/mask/overlay preview images under one split preview directory.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark visual audit and preview evidence requirements
    - 公式/定义: 预览资产必须具备最小可视复核强度，不能只有目录存在却没有足够样本图
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 将文件名后缀归一为 `__raw.png`、`__mask_bin.png`、`__overlay.png` 三类计数。
    """
    counters = {"raw": 0, "mask_bin": 0, "overlay": 0}
    if not split_dir.exists():
        return counters
    for path in split_dir.glob("*.png"):
        name = path.name
        if "__raw.png" in name:
            counters["raw"] += 1
        elif "__mask_bin.png" in name:
            counters["mask_bin"] += 1
        elif "__overlay.png" in name:
            counters["overlay"] += 1
    return counters


def load_csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def validate_dataset(project_root: Path, dataset_code: str) -> tuple[str, list[str], dict[str, Any]]:
    """Validate one frozen dataset config and its split asset availability.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark dataset-root and split-asset readiness constraints
    - 公式/定义: 每个正式数据集都必须证明 dataset root 和 split CSV 真实存在，才能进入数据阶段交接
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 对 GlaS / CRAG 统一输出 dataset role、dataset root、split row_count 和 pass/blocked 结论。
    """
    config_path = project_root / "configs" / "data" / f"{dataset_code}.yaml"
    config = load_data_config(project_root, config_path)
    dataset_root = resolve_dataset_root(project_root, config)
    details: list[str] = [
        f"- dataset_code: `{config.dataset_code}`",
        f"- dataset_role: `{config.dataset_role}`",
        f"- dataset_root: `{safe_relpath(dataset_root, project_root)}`",
        f"- dataset_root_exists: `{dataset_root.exists()}`",
        f"- dataset_source_note: `{config.dataset_source_note}`",
        f"- asset_status: `{config.asset_status}`",
    ]
    failures = 0
    split_assets: list[dict[str, Any]] = []
    if not dataset_root.exists():
        failures += 1
        details.append("- missing_reason: `dataset_root_not_restored`")

    for split_name in EXPECTED_SPLITS[dataset_code]:
        split_path = resolve_split_csv(project_root, config, split_name)
        exists = split_path.exists()
        row_count = load_csv_row_count(split_path) if exists else 0
        split_assets.append(
            {
                "dataset": dataset_code,
                "split_name": split_name,
                "relative_path": safe_relpath(split_path, project_root),
                "exists": exists,
                "row_count": row_count,
            }
        )
        details.append(
            f"- split_{split_name}: `{safe_relpath(split_path, project_root)}` exists=`{exists}` rows=`{row_count}`"
        )
        if not exists:
            failures += 1

    status = "pass" if failures == 0 else "blocked"
    details.append(
        "- conclusion: `all frozen dataset assets required by this config exist`"
        if status == "pass"
        else "- conclusion: `formal config exists but dataset root and/or split assets are still blocked`"
    )
    payload = {
        "dataset_code": config.dataset_code,
        "dataset_role": config.dataset_role,
        "dataset_root": safe_relpath(dataset_root, project_root),
        "dataset_root_exists": dataset_root.exists(),
        "dataset_source_note": config.dataset_source_note,
        "asset_status": config.asset_status,
        "split_assets": split_assets,
    }
    return status, details, payload


def inspect_check_assets(project_root: Path) -> dict[str, Any]:
    """Inspect formal check assets and derive pair/check/manual-audit status.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark data integrity, duplicate check and manual audit requirements
    - 公式/定义: 配对检查、重复检查、前景检查和人工审稿必须一起成立，才能说明数据检查链闭环
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 将 `reports/data_checks/*` 中的关键字段统一汇总为 `pass_pair / pass_check / red_flag`。
    """
    report_path = project_root / CHECK_ASSET_PATHS["data_check_report"]
    duplicate_path = project_root / CHECK_ASSET_PATHS["duplicate_check_report"]
    manual_path = project_root / CHECK_ASSET_PATHS["manual_audit_notes"]
    asset_entries: list[dict[str, Any]] = []
    missing: list[str] = []
    for key, relpath in CHECK_ASSET_PATHS.items():
        path = project_root / relpath
        exists = path.exists()
        asset_entries.append({"key": key, "relative_path": relpath, "exists": exists})
        if key != "manual_audit_notes" and not exists:
            missing.append(key)

    report_fields = parse_markdown_key_values(read_text(report_path)) if report_path.exists() else {}
    duplicate_fields = parse_markdown_key_values(read_text(duplicate_path)) if duplicate_path.exists() else {}
    manual_text = read_text(manual_path) if manual_path.exists() else ""
    manual_fields = parse_markdown_key_values(manual_text) if manual_text else {}

    pair_pass = report_fields.get("pair_check_pass") == "pass"
    readable_pass = report_fields.get("readable_check_pass") == "pass"
    duplicate_pass = duplicate_fields.get("duplicate_check_status") == "pass"
    foreground_pass = report_fields.get("foreground_check_pass") == "pass"
    if manual_text:
        manual_status, manual_pass = derive_manual_audit_status(manual_text)
    else:
        manual_status, manual_pass = ("missing", False)
    pass_pair = pair_pass and readable_pass and duplicate_pass
    pass_check = pair_pass and readable_pass and duplicate_pass and foreground_pass and manual_pass and not missing
    red_flag = not pair_pass or not readable_pass or not duplicate_pass or not foreground_pass

    return {
        "assets": asset_entries,
        "missing": missing,
        "report_fields": report_fields,
        "duplicate_fields": duplicate_fields,
        "manual_fields": manual_fields,
        "pass_pair": pass_pair,
        "pass_check": pass_check,
        "red_flag": red_flag,
        "manual_audit_status": manual_status,
    }


def inspect_preview_assets(project_root: Path) -> dict[str, Any]:
    preview_root = project_root / "reports" / "data_preview"
    entries: list[dict[str, Any]] = []
    failures = 0
    for dataset_code, split_map in PREVIEW_SPLIT_DIR.items():
        for split_name, split_dir_name in split_map.items():
            split_dir = preview_root / dataset_code / split_dir_name
            counters = count_preview_files(split_dir)
            ok = all(counters[key] >= 2 for key in ("raw", "mask_bin", "overlay"))
            entries.append(
                {
                    "dataset": dataset_code,
                    "split_name": split_name,
                    "relative_dir": safe_relpath(split_dir, project_root),
                    "exists": split_dir.exists(),
                    "raw_count": counters["raw"],
                    "mask_bin_count": counters["mask_bin"],
                    "overlay_count": counters["overlay"],
                    "status": "pass" if ok else "fail",
                }
            )
            if not ok:
                failures += 1
    return {
        "preview_root": safe_relpath(preview_root, project_root),
        "entries": entries,
        "pass_preview": failures == 0,
    }


def inspect_label_assets(project_root: Path) -> dict[str, Any]:
    """Inspect label protocol outputs and derive label-stage pass signals.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: label protocol, binary-mask conversion and derived target readiness
    - 公式/定义: binary mask、boundary target 和 distance target 必须同时通过，标签协议链才算成立
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 汇总为 `pass_binary_mask / pass_dtype / pass_resize_rule / pass_boundary_target / pass_distance_target / pass_label`。
    """
    asset_entries: list[dict[str, Any]] = []
    missing: list[str] = []
    for key, relpath in LABEL_ASSET_PATHS.items():
        path = project_root / relpath
        exists = path.exists()
        asset_entries.append({"key": key, "relative_path": relpath, "exists": exists})
        if not exists:
            missing.append(key)

    label_report_path = project_root / LABEL_ASSET_PATHS["label_protocol_report"]
    boundary_report_path = project_root / LABEL_ASSET_PATHS["boundary_target_report"]
    distance_report_path = project_root / LABEL_ASSET_PATHS["distance_target_report"]

    label_fields = parse_markdown_key_values(read_text(label_report_path)) if label_report_path.exists() else {}
    boundary_fields = parse_markdown_key_values(read_text(boundary_report_path)) if boundary_report_path.exists() else {}
    distance_fields = parse_markdown_key_values(read_text(distance_report_path)) if distance_report_path.exists() else {}

    pass_binary_mask = label_fields.get("pass_binary_mask") == "True"
    pass_dtype = label_fields.get("pass_dtype") == "True"
    pass_resize_rule = label_fields.get("pass_resize_rule") == "True"
    pass_boundary_target = boundary_fields.get("pass_boundary_target") == "True"
    pass_distance_target = distance_fields.get("pass_distance_target") == "True"
    pass_label = (
        not missing
        and pass_binary_mask
        and pass_dtype
        and pass_resize_rule
        and pass_boundary_target
        and pass_distance_target
    )

    return {
        "assets": asset_entries,
        "missing": missing,
        "label_fields": label_fields,
        "boundary_fields": boundary_fields,
        "distance_fields": distance_fields,
        "pass_binary_mask": pass_binary_mask,
        "pass_dtype": pass_dtype,
        "pass_resize_rule": pass_resize_rule,
        "pass_boundary_target": pass_boundary_target,
        "pass_distance_target": pass_distance_target,
        "pass_label": pass_label,
    }


def inspect_config_source_assets(project_root: Path) -> dict[str, Any]:
    """Inspect frozen config files and dataset source notes for handoff readiness.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: dataset provenance and frozen-config traceability requirements
    - 公式/定义: 正式数据配置和数据来源说明都是交接包的一部分，缺任一项都不能宣称输入层可追溯
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 将配置资产和数据源说明分别汇总成 `pass_config` 与 `pass_source` 两个门状态。
    """
    entries: list[dict[str, Any]] = []
    missing_config: list[str] = []
    missing_source: list[str] = []
    for relpath in CONFIG_ASSET_PATHS:
        path = project_root / relpath
        exists = path.exists()
        entries.append({"type": "config", "relative_path": relpath, "exists": exists})
        if not exists:
            missing_config.append(relpath)
    for relpath in SOURCE_ASSET_PATHS:
        path = project_root / relpath
        exists = path.exists()
        entries.append({"type": "source", "relative_path": relpath, "exists": exists})
        if not exists:
            missing_source.append(relpath)
    return {
        "entries": entries,
        "missing_config": missing_config,
        "missing_source": missing_source,
        "pass_config": not missing_config,
        "pass_source": not missing_source,
    }


def inspect_training_preflight(
    project_root: Path,
    data_stage_pass: bool,
    handoff_ready: bool,
    manifest_relpath: str,
    dataset_codes: tuple[str, ...],
) -> dict[str, Any]:
    """Check whether the formal data-stage package can hand off to train-entry preflight.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark handoff and entrypoint readiness constraints
    - 公式/定义: 当前阶段通过后，还必须证明 `scripts/train.py` 至少能接住冻结后的输入层
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 通过一次最小 `scripts/train.py --runtime-check` probe 真实验证入口是否继承 `asset_manifest` 里的 handoff gate。
    """
    train_entry = project_root / "scripts" / "train.py"
    blockers: list[str] = []
    if not data_stage_pass:
        blockers.append("data_stage_pass_false")
    if not handoff_ready:
        blockers.append("handoff_ready_false")
    if not train_entry.exists():
        blockers.append("missing_train_entrypoint")
    dataset_code = "glas" if "glas" in dataset_codes else (dataset_codes[0] if dataset_codes else "")
    if not dataset_code:
        blockers.append("no_dataset_available_for_preflight_probe")
    if blockers:
        return {
            "train_entrypoint": safe_relpath(train_entry, project_root),
            "train_entrypoint_exists": train_entry.exists(),
            "probe_dataset": dataset_code,
            "probe_mode": "runtime_check_probe",
            "blockers": blockers,
            "preflight_pass": False,
        }

    runtime_root = project_root / "reports" / "runtime_checks"
    runtime_root.mkdir(parents=True, exist_ok=True)
    probe_config_path = runtime_root / "_tmp_validate_data_assets_preflight.yaml"
    probe_output_path = runtime_root / "_tmp_validate_data_assets_preflight.json"
    probe_log_path = runtime_root / "_tmp_validate_data_assets_preflight.log"
    probe_config_relpath = safe_relpath(probe_config_path, project_root)
    probe_output_relpath = safe_relpath(probe_output_path, project_root)

    probe_config_lines = [
        "run_name: data_stage_preflight_probe",
        "stage_code: 01_data_protocol_preflight",
        f"dataset_code: {dataset_code}",
        "model_code: train_entrypoint_preflight_only",
        "runtime_split: train",
        "config_refs:",
        f"  data: configs/data/{dataset_code}.yaml",
        f"  asset_manifest: {manifest_relpath}",
    ]
    probe_config_path.write_text("\n".join(probe_config_lines) + "\n", encoding="utf-8")

    command = [
        sys.executable,
        str(train_entry),
        "--config",
        probe_config_relpath,
        "--run-name",
        "data_stage_preflight_probe",
        "--runtime-check",
        "--runtime-check-output",
        probe_output_relpath,
        "--device",
        "cpu",
        "--max-steps",
        "1",
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        probe_log_path.write_text(
            "[preflight_probe] stdout\n"
            + completed.stdout
            + "\n[preflight_probe] stderr\n"
            + completed.stderr,
            encoding="utf-8",
        )
        if completed.returncode != 0:
            blockers.append(f"preflight_probe_exit_{completed.returncode}")
        elif not probe_output_path.exists():
            blockers.append("preflight_probe_payload_missing")
        else:
            payload = json.loads(probe_output_path.read_text(encoding="utf-8"))
            if payload.get("entrypoint_check_pass") is not True:
                blockers.append("entrypoint_check_pass_false")
            if payload.get("data_stage_pass") is not True:
                blockers.append("payload_data_stage_pass_false")
            if payload.get("handoff_ready") is not True:
                blockers.append("payload_handoff_ready_false")
            if normalize_relpath(str(payload.get("asset_manifest", ""))) != normalize_relpath(manifest_relpath):
                blockers.append("payload_asset_manifest_mismatch")
            if payload.get("split_asset_exists") is not True:
                blockers.append("payload_split_asset_missing")
            if payload.get("data_config_registered") is not True:
                blockers.append("payload_data_config_not_registered")
    except subprocess.TimeoutExpired:
        blockers.append("preflight_probe_timeout")
        probe_log_path.write_text("[preflight_probe] timeout\n", encoding="utf-8")
    finally:
        for temp_path in (probe_config_path, probe_output_path, probe_log_path):
            if temp_path.exists():
                temp_path.unlink()

    return {
        "train_entrypoint": safe_relpath(train_entry, project_root),
        "train_entrypoint_exists": train_entry.exists(),
        "probe_dataset": dataset_code,
        "probe_mode": "runtime_check_probe",
        "blockers": blockers,
        "preflight_pass": not blockers,
    }


def build_asset_manifest(
    project_root: Path,
    dataset_results: dict[str, dict[str, Any]],
    check_info: dict[str, Any],
    label_info: dict[str, Any],
    preview_info: dict[str, Any],
    config_source_info: dict[str, Any],
    handoff_ready: bool,
    assets_traceable: bool,
    protocol_explainable: bool,
    data_stage_pass: bool,
    preflight_pass: bool,
    next_action: str,
) -> dict[str, Any]:
    return {
        "asset_manifest_version": "asset_manifest_v1",
        "data_protocol_package_version": "01_data_protocol_v1",
        "split_assets": [
            split
            for payload in dataset_results.values()
            for split in payload["split_assets"]
        ],
        "check_assets": check_info["assets"],
        "label_assets": label_info["assets"],
        "preview_assets": preview_info["entries"],
        "config_source_assets": config_source_info["entries"],
        "handoff_ready": handoff_ready,
        "assets_traceable": assets_traceable,
        "protocol_explainable": protocol_explainable,
        "data_stage_pass": data_stage_pass,
        "preflight_pass": preflight_pass,
        "next_action": next_action,
        "project_root": project_root.as_posix(),
    }


def build_validation_report(
    project_root: Path,
    dataset_sections: list[tuple[str, str, list[str]]],
    check_info: dict[str, Any],
    label_info: dict[str, Any],
    preview_info: dict[str, Any],
    config_source_info: dict[str, Any],
    handoff_ready: bool,
    assets_traceable: bool,
    protocol_explainable: bool,
    data_stage_pass: bool,
    preflight_info: dict[str, Any],
    next_action: str,
) -> str:
    lines = ["# Data Asset Validation Report", "", f"- project_root: `{project_root.as_posix()}`", ""]
    for dataset_code, status, details in dataset_sections:
        lines.append(f"## {dataset_code}")
        lines.append(f"- status: `{status}`")
        lines.extend(details)
        lines.append("")
    lines.extend(
        [
            "## data_stage_gates",
            f"- pass_pair: `{check_info['pass_pair']}`",
            f"- pass_label: `{label_info['pass_label']}`",
            f"- pass_binary_mask: `{label_info['pass_binary_mask']}`",
            f"- pass_dtype: `{label_info['pass_dtype']}`",
            f"- pass_resize_rule: `{label_info['pass_resize_rule']}`",
            f"- pass_boundary_target: `{label_info['pass_boundary_target']}`",
            f"- pass_distance_target: `{label_info['pass_distance_target']}`",
            f"- pass_check: `{check_info['pass_check']}`",
            f"- manual_audit_status: `{check_info['manual_audit_status']}`",
            f"- pass_preview: `{preview_info['pass_preview']}`",
            f"- pass_config: `{config_source_info['pass_config']}`",
            f"- pass_source: `{config_source_info['pass_source']}`",
            f"- handoff_ready: `{handoff_ready}`",
            f"- assets_traceable: `{assets_traceable}`",
            f"- protocol_explainable: `{protocol_explainable}`",
            f"- data_stage_pass: `{data_stage_pass}`",
            f"- preflight_pass: `{preflight_info['preflight_pass']}`",
            f"- next_action: `{next_action}`",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_acceptance_report(
    project_root: Path,
    manifest_relpath: str,
    dataset_results: dict[str, dict[str, Any]],
    check_info: dict[str, Any],
    label_info: dict[str, Any],
    preview_info: dict[str, Any],
    config_source_info: dict[str, Any],
    handoff_ready: bool,
    assets_traceable: bool,
    protocol_explainable: bool,
    data_stage_pass: bool,
    preflight_info: dict[str, Any],
    next_action: str,
) -> str:
    """Build the formal data-stage acceptance markdown report.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark acceptance and handoff reporting requirements
    - 公式/定义: 数据阶段需要一份正式验收结果，把 split、check、preview、handoff 和 preflight 结论统一写成可交接文档
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 生成 `reports/stage_reports/data_stage_acceptance.md`，显式写出 `data_stage_pass / handoff_ready / preflight_pass / next_action`。
    """
    lines = [
        "# Data Stage Acceptance",
        "",
        "## 1. Inputs",
        f"- asset_manifest: `{manifest_relpath}`",
        f"- split_assets_ready: `{all(payload['dataset_root_exists'] for payload in dataset_results.values())}`",
        f"- check_assets_ready: `{check_info['pass_check']}`",
        f"- label_assets_ready: `{label_info['pass_label']}`",
        f"- preview_assets_ready: `{preview_info['pass_preview']}`",
        f"- config_assets_ready: `{config_source_info['pass_config']}`",
        f"- source_assets_ready: `{config_source_info['pass_source']}`",
        "",
        "## 2. Gate Status",
        f"- pass_source: `{config_source_info['pass_source']}`",
        f"- pass_split: `{all(payload['dataset_root_exists'] and all(item['exists'] for item in payload['split_assets']) for payload in dataset_results.values())}`",
        f"- pass_pair: `{check_info['pass_pair']}`",
        f"- pass_label: `{label_info['pass_label']}`",
        f"- pass_binary_mask: `{label_info['pass_binary_mask']}`",
        f"- pass_dtype: `{label_info['pass_dtype']}`",
        f"- pass_resize_rule: `{label_info['pass_resize_rule']}`",
        f"- pass_boundary_target: `{label_info['pass_boundary_target']}`",
        f"- pass_distance_target: `{label_info['pass_distance_target']}`",
        f"- pass_check: `{check_info['pass_check']}`",
        f"- pass_preview: `{preview_info['pass_preview']}`",
        f"- pass_handoff: `{handoff_ready}`",
        f"- assets_traceable: `{assets_traceable}`",
        f"- protocol_explainable: `{protocol_explainable}`",
        f"- red_flag: `{check_info['red_flag']}`",
        f"- data_stage_pass: `{data_stage_pass}`",
        f"- handoff_ready: `{handoff_ready}`",
        f"- preflight_pass: `{preflight_info['preflight_pass']}`",
        f"- next_action: `{next_action}`",
        "",
        "## 3. Blocking Reasons",
    ]
    blockers: list[str] = []
    if not label_info["pass_label"]:
        blockers.append("label protocol or derived target chain is not fully closed")
    if not check_info["pass_check"]:
        blockers.append("manual audit not complete, so check gate is not fully closed")
    if not handoff_ready:
        blockers.append("minimum handoff package is incomplete under the formal protocol")
    if not data_stage_pass:
        blockers.append("data_stage_pass cannot be granted until label/check/preview/handoff chain is fully closed")
    if not preflight_info["preflight_pass"]:
        blockers.append(f"preflight blockers: {', '.join(preflight_info['blockers'])}")
    if not blockers:
        blockers.append("none")
    for item in blockers:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## 4. Formal Outputs",
            f"- reports/data_checks/data_check_report.md",
            f"- reports/data_checks/dataset_stats.csv",
            f"- reports/data_checks/duplicate_check_report.md",
            f"- reports/data_checks/foreground_summary.csv",
            f"- reports/data_checks/object_size_summary.csv",
            f"- reports/data_checks/manual_audit_notes.md",
            f"- reports/data_checks/label_protocol_report.md",
            f"- reports/data_checks/boundary_target_report.md",
            f"- reports/data_checks/distance_target_report.md",
            f"- reports/data_preview/*",
            f"- reports/data_targets/*",
            f"- {manifest_relpath}",
            f"- reports/stage_reports/data_stage_acceptance.md",
            "",
            "## 5. Conclusion",
            "- truthful_interpretation: this report only grants `pass` when the formal 01_数据协议 handoff chain is fully closed; currently any missing manual audit, missing label-target chain, or missing preflight gate must keep the stage blocked.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Run the formal 01_数据协议 handoff validation and write stage outputs.

    对应阶段: 01_数据协议
    理论依据:
    - 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
    - 章节: benchmark readiness aggregation and formal stage handoff
    - 公式/定义: 当前阶段收口时必须把局部资产、局部检查和交接结论统一成正式输出，而不是只保留散落报告
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: tools/stage01_data_protocol/validate_data_assets.py
    - commit: workspace_local_20260705
    - 许可证: project_internal
    本项目调整: 同时写出 validation report、asset manifest 和 acceptance report，并输出总体状态到 CLI。
    """
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    dataset_codes = ("glas", "crag") if args.dataset == "all" else (args.dataset,)

    dataset_sections: list[tuple[str, str, list[str]]] = []
    dataset_results: dict[str, dict[str, Any]] = {}
    for dataset_code in dataset_codes:
        status, details, payload = validate_dataset(project_root, dataset_code)
        dataset_sections.append((dataset_code, status, details))
        dataset_results[dataset_code] = payload

    check_info = inspect_check_assets(project_root)
    label_info = inspect_label_assets(project_root)
    preview_info = inspect_preview_assets(project_root)
    config_source_info = inspect_config_source_assets(project_root)

    pass_split = all(payload["dataset_root_exists"] and all(item["exists"] for item in payload["split_assets"]) for payload in dataset_results.values())
    pass_source = config_source_info["pass_source"]
    pass_config = config_source_info["pass_config"]
    pass_preview = preview_info["pass_preview"]
    pass_pair = check_info["pass_pair"]
    pass_check = check_info["pass_check"]
    pass_label = label_info["pass_label"]

    assets_traceable = pass_split and pass_config and pass_source
    protocol_explainable = pass_preview and pass_config and pass_source and check_info["manual_audit_status"] in {"partial", "pass"}
    handoff_ready = pass_split and pass_check and pass_preview and pass_config and pass_source and assets_traceable and protocol_explainable and not check_info["red_flag"]
    data_stage_pass = handoff_ready and pass_pair and pass_label and pass_check and not check_info["red_flag"]

    output_path = (project_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    acceptance_output_path = (project_root / args.acceptance_output).resolve()
    acceptance_output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_output_path = (project_root / args.asset_manifest_output).resolve()
    manifest_output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_relpath = safe_relpath(manifest_output_path, project_root)

    provisional_manifest = build_asset_manifest(
        project_root,
        dataset_results,
        check_info,
        label_info,
        preview_info,
        config_source_info,
        handoff_ready,
        assets_traceable,
        protocol_explainable,
        data_stage_pass,
        False,
        "pending_preflight",
    )
    manifest_output_path.write_text(
        json.dumps(provisional_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    preflight_info = inspect_training_preflight(
        project_root,
        data_stage_pass,
        handoff_ready,
        manifest_relpath,
        tuple(dataset_results.keys()),
    )
    next_action = "enter_02_unet" if preflight_info["preflight_pass"] else "rollback"

    manifest = build_asset_manifest(
        project_root,
        dataset_results,
        check_info,
        label_info,
        preview_info,
        config_source_info,
        handoff_ready,
        assets_traceable,
        protocol_explainable,
        data_stage_pass,
        preflight_info["preflight_pass"],
        next_action,
    )
    manifest_output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    output_path.write_text(
        build_validation_report(
            project_root,
            dataset_sections,
            check_info,
            label_info,
            preview_info,
            config_source_info,
            handoff_ready,
            assets_traceable,
            protocol_explainable,
            data_stage_pass,
            preflight_info,
            next_action,
        ),
        encoding="utf-8",
    )
    acceptance_output_path.write_text(
        build_acceptance_report(
            project_root,
            manifest_relpath,
            dataset_results,
            check_info,
            label_info,
            preview_info,
            config_source_info,
            handoff_ready,
            assets_traceable,
            protocol_explainable,
            data_stage_pass,
            preflight_info,
            next_action,
        ),
        encoding="utf-8",
    )

    overall = "pass" if data_stage_pass and preflight_info["preflight_pass"] else "blocked"
    print(f"report_path={output_path.as_posix()}")
    print(f"acceptance_report_path={acceptance_output_path.as_posix()}")
    print(f"asset_manifest_path={manifest_output_path.as_posix()}")
    print(f"data_asset_validation_status={overall}")
    for dataset_code, status, _ in dataset_sections:
        print(f"{dataset_code}_status={status}")
    print(f"pass_pair={pass_pair}")
    print(f"pass_label={pass_label}")
    print(f"pass_check={pass_check}")
    print(f"pass_preview={pass_preview}")
    print(f"pass_config={pass_config}")
    print(f"pass_source={pass_source}")
    print(f"handoff_ready={handoff_ready}")
    print(f"assets_traceable={assets_traceable}")
    print(f"protocol_explainable={protocol_explainable}")
    print(f"data_stage_pass={data_stage_pass}")
    print(f"preflight_pass={preflight_info['preflight_pass']}")
    print(f"next_action={next_action}")
    return 0 if overall == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
