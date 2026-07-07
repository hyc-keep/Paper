"""Formal stage02 acceptance summarizer.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: stage-level closure must aggregate training, validation, testing, evaluation, visuals, and records
- 公式/定义: pass_stage = pass_train and pass_val and pass_test and pass_eval and pass_visual and pass_record
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, scripts/test.py, reports/stage_reports/data_stage_acceptance.md
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前脚本把已有训练、测试、可视化和 debug 资产再聚合成 stage02 的正式验收层。
- 如果当前 run 仍是 smoke、split 样本数不满正式口径或冻结字段未对齐，脚本会如实写成 blocked，而不是包装成通过。
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
import sys
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import train as train_entry

FORMAL_CONNECTIVITY = 8
FORMAL_BOUNDARY_WIDTH = 3
FORMAL_CAST_POLICY = "float32_before_threshold"
FORMAL_BEST_SELECTOR = "val_objdice_max"
FORMAL_THRESHOLD_SOURCE = "val17"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize formal stage02 acceptance state.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional run name override.")
    parser.add_argument(
        "--debug-note",
        default="notes/debug_note.md",
        help="Relative path to the structured debug note.",
    )
    parser.add_argument(
        "--stage-summary-output",
        default="reports/stage_reports/unet_flow_stage_summary.md",
        help="Relative path for the stage summary markdown.",
    )
    parser.add_argument(
        "--manifest-output",
        default="reports/tables/unet_flow_stage_manifest.csv",
        help="Relative path for the stage manifest csv.",
    )
    return parser.parse_args()


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return bool(value)


def _parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_markdown_fields(path: Path) -> dict[str, str]:
    pattern = re.compile(r"^- ([a-zA-Z0-9_]+): `?(.*?)`?$")
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw_line.strip())
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_csv_aggregate_row(path: Path) -> dict[str, str]:
    for row in _load_csv_rows(path):
        if row.get("row_type") == "aggregate":
            return row
    return {}


def _find_expected_split_count(asset_manifest: dict[str, Any], dataset_code: str, split_name: str) -> int:
    split_assets = asset_manifest.get("split_assets", [])
    if not isinstance(split_assets, list):
        return 0
    for item in split_assets:
        if not isinstance(item, dict):
            continue
        if item.get("dataset") == dataset_code and item.get("split_name") == split_name:
            return _parse_int(item.get("row_count"), default=0)
    return 0


def _collect_major_failure_modes(error_cases_path: Path) -> str:
    modes: list[str] = []
    if not error_cases_path.exists():
        return "not_exported"
    for raw_line in error_cases_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        label, value = line[2:].split(":", 1)
        label = label.strip()
        if label in {"adhesion_merge", "boundary_over_smooth", "small_gland_miss", "fragmented_complex_region", "all_background"}:
            modes.append(label)
    return ", ".join(sorted(set(modes))) if modes else "not_exported"


def _write_stage_manifest(
    manifest_output_path: Path,
    asset_rows: list[dict[str, Any]],
) -> None:
    manifest_output_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["asset_key", "relative_path", "exists", "required_for_a2"],
        )
        writer.writeheader()
        for row in asset_rows:
            writer.writerow(row)


def _write_run_summary(
    run_summary_path: Path,
    run_meta: dict[str, Any],
    gate_status: dict[str, Any],
    split_status: dict[str, Any],
    major_failure_modes: str,
    blocking_reasons: list[str],
) -> None:
    if gate_status["stage_pass"]:
        truthful_interpretation = (
            "Current assets complete the formal stage02 closure: non-smoke A1 training ended normally, "
            "full TestA60/TestB20 were exported, evaluation and visual assets are aligned, "
            "and handoff is ready for stage03."
        )
    else:
        truthful_interpretation = (
            "Current assets only support local smoke connectivity and partial stage02 closure; "
            "formal A1 acceptance remains blocked until a non-smoke full run, full TestA60/TestB20, "
            "and frozen evaluation fields are re-exported."
        )
    lines = [
        "# Run Summary",
        "",
        "## Inputs",
        "",
        f"- run_name: `{run_meta.get('run_name', 'unknown')}`",
        f"- stop_reason: `{run_meta.get('stop_reason', 'unknown')}`",
        f"- smoke_check: `{str(_parse_bool(run_meta.get('smoke_check', False))).lower()}`",
        f"- device: `{run_meta.get('device', 'unknown')}`",
        f"- best_epoch: `{run_meta.get('best_epoch', 'unknown')}`",
        f"- best_metric_name: `val_objdice`",
        f"- best_metric_value: `{run_meta.get('best_metric_value', 'unknown')}`",
        "",
        "## Gate Status",
        "",
        f"- pass_train: `{str(gate_status['pass_train']).lower()}`",
        f"- pass_val: `{str(gate_status['pass_val']).lower()}`",
        f"- pass_test: `{str(gate_status['pass_test']).lower()}`",
        f"- pass_eval: `{str(gate_status['pass_eval']).lower()}`",
        f"- pass_visual: `{str(gate_status['pass_visual']).lower()}`",
        f"- pass_record: `{str(gate_status['pass_record']).lower()}`",
        f"- stage_pass: `{str(gate_status['stage_pass']).lower()}`",
        f"- protocol_error: `{str(gate_status['protocol_error']).lower()}`",
        f"- freeze_status: `{str(gate_status['freeze_status']).lower()}`",
        f"- handoff_ready_for_a2: `{str(gate_status['handoff_ready_for_a2']).lower()}`",
        f"- next_action: `{gate_status['next_action']}`",
        "",
        "## Test Splits",
        "",
        f"- testA_expected_count: `{split_status['testA_expected_count']}`",
        f"- testA_actual_count: `{split_status['testA_actual_count']}`",
        f"- testA_objdice: `{split_status['testA_objdice']}`",
        f"- testB_expected_count: `{split_status['testB_expected_count']}`",
        f"- testB_actual_count: `{split_status['testB_actual_count']}`",
        f"- testB_objdice: `{split_status['testB_objdice']}`",
        "",
        "## Findings",
        "",
        f"- metric_crosscheck_result: `{run_meta.get('metric_crosscheck_result', 'unknown')}`",
        f"- major_failure_modes: `{major_failure_modes}`",
        (
            "- protocol_abnormal_signs: `"
            + ("; ".join(blocking_reasons) if blocking_reasons else "none")
            + "`"
        ),
        (
            "- truthful_interpretation: `"
            + truthful_interpretation
            + "`"
        ),
    ]
    run_summary_path.parent.mkdir(parents=True, exist_ok=True)
    run_summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_stage_summary(
    stage_summary_path: Path,
    run_dir: Path,
    debug_note_path: Path,
    gate_status: dict[str, Any],
    split_status: dict[str, Any],
    blocking_reasons: list[str],
) -> None:
    lines = [
        "# UNet Flow Stage Summary",
        "",
        "## 1. Inputs",
        f"- run_dir: `{_relative_path(run_dir)}`",
        f"- run_meta: `{_relative_path(run_dir / 'run_meta.yaml')}`",
        f"- run_summary: `{_relative_path(run_dir / 'summaries' / 'run_summary.md')}`",
        f"- debug_note: `{_relative_path(debug_note_path)}`",
        "",
        "## 2. Gate Status",
        f"- pass_train: `{str(gate_status['pass_train']).lower()}`",
        f"- pass_val: `{str(gate_status['pass_val']).lower()}`",
        f"- pass_test: `{str(gate_status['pass_test']).lower()}`",
        f"- pass_eval: `{str(gate_status['pass_eval']).lower()}`",
        f"- pass_visual: `{str(gate_status['pass_visual']).lower()}`",
        f"- pass_record: `{str(gate_status['pass_record']).lower()}`",
        f"- stage_pass: `{str(gate_status['stage_pass']).lower()}`",
        f"- protocol_error: `{str(gate_status['protocol_error']).lower()}`",
        f"- freeze_status: `{str(gate_status['freeze_status']).lower()}`",
        f"- handoff_ready_for_a2: `{str(gate_status['handoff_ready_for_a2']).lower()}`",
        f"- next_action: `{gate_status['next_action']}`",
        "",
        "## 3. Split Counts",
        f"- testA_expected_count: `{split_status['testA_expected_count']}`",
        f"- testA_actual_count: `{split_status['testA_actual_count']}`",
        f"- testB_expected_count: `{split_status['testB_expected_count']}`",
        f"- testB_actual_count: `{split_status['testB_actual_count']}`",
        "",
        "## 4. Blocking Reasons",
    ]
    if blocking_reasons:
        lines.extend(f"- {item}" for item in blocking_reasons)
    else:
        lines.append("- none")
    if gate_status["stage_pass"]:
        stage_truthful_interpretation = (
            "current stage summary confirms formal stage02 closure: non-smoke A1 training ended normally, "
            "full TestA60/TestB20 are present, evaluation and visual assets are aligned, "
            "and handoff is ready for stage03."
        )
    else:
        stage_truthful_interpretation = (
            "current stage summary does not grant formal stage02 closure yet; "
            "a non-smoke full run, full TestA60/TestB20, aligned evaluation fields, "
            "and closed protocol blockers are still required before handoff."
        )
    lines.extend(
        [
            "",
            "## 5. Conclusion",
            f"- truthful_interpretation: {stage_truthful_interpretation}",
        ]
    )
    stage_summary_path.parent.mkdir(parents=True, exist_ok=True)
    stage_summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    _, experiment_config = train_entry.load_experiment_config(PROJECT_ROOT, args.config)
    run_name = args.run_name or str(experiment_config.get("run_name", "manual_run"))
    run_dir = train_entry.build_output_dir(PROJECT_ROOT, run_name)
    if not run_dir.exists():
        raise FileNotFoundError(f"run directory not found: {run_dir}")

    debug_note_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.debug_note)).resolve()
    stage_summary_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.stage_summary_output)).resolve()
    manifest_output_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.manifest_output)).resolve()

    eval_config_path = train_entry.resolve_config_ref(PROJECT_ROOT, experiment_config, "eval")
    eval_config = train_entry.simple_yaml_load(eval_config_path.read_text(encoding="utf-8"))

    asset_manifest_path = (PROJECT_ROOT / "reports" / "stage_reports" / "asset_manifest.json").resolve()
    asset_manifest = train_entry.load_json_mapping(asset_manifest_path)
    data_acceptance_path = (PROJECT_ROOT / "reports" / "stage_reports" / "data_stage_acceptance.md").resolve()
    data_acceptance_fields = _parse_markdown_fields(data_acceptance_path)

    run_meta_path = run_dir / "run_meta.yaml"
    run_meta = train_entry.simple_yaml_load(run_meta_path.read_text(encoding="utf-8"))

    debug_fields = _parse_markdown_fields(debug_note_path)
    metric_note_fields = _parse_markdown_fields(run_dir / "metric_crosscheck_note.md")
    testa_aggregate = _load_csv_aggregate_row(run_dir / "testA_metrics.csv")
    testb_aggregate = _load_csv_aggregate_row(run_dir / "testB_metrics.csv")

    testA_expected_count = _find_expected_split_count(asset_manifest, str(run_meta.get("dataset_code", "")), "testA")
    testB_expected_count = _find_expected_split_count(asset_manifest, str(run_meta.get("dataset_code", "")), "testB")
    testA_actual_count = _parse_int(testa_aggregate.get("sample_count"), default=_parse_int(run_meta.get("testA_sample_count")))
    testB_actual_count = _parse_int(testb_aggregate.get("sample_count"), default=_parse_int(run_meta.get("testB_sample_count")))

    actual_connectivity = _parse_int(
        metric_note_fields.get("connected_components_connectivity", eval_config.get("connected_components_connectivity")),
        default=0,
    )
    actual_boundary_width = _parse_int(
        metric_note_fields.get("boundary_metric_width", run_meta.get("boundary_metric_width", eval_config.get("boundary_metric_width"))),
        default=0,
    )
    actual_eval_cast_policy = str(eval_config.get("eval_cast_policy", "missing"))

    data_stage_pass = data_acceptance_fields.get("data_stage_pass", "false") == "True"
    handoff_ready = data_acceptance_fields.get("handoff_ready", "false") == "True"
    preflight_pass = data_acceptance_fields.get("preflight_pass", "false") == "True"

    best_ckpt_exists = (run_dir / "checkpoints" / "best.ckpt").exists()
    last_ckpt_exists = (run_dir / "checkpoints" / "last.ckpt").exists()
    train_log_exists = (run_dir / "train_log.csv").exists()
    val_metrics_exists = (run_dir / "val_metrics.csv").exists()
    testA_metrics_exists = (run_dir / "testA_metrics.csv").exists()
    testB_metrics_exists = (run_dir / "testB_metrics.csv").exists()
    metric_note_exists = (run_dir / "metric_crosscheck_note.md").exists()
    error_cases_exists = (run_dir / "summaries" / "error_cases.md").exists()
    visuals_testA_exists = (run_dir / "visuals" / "testA").exists()
    visuals_testB_exists = (run_dir / "visuals" / "testB").exists()
    run_summary_exists = (run_dir / "summaries" / "run_summary.md").exists()

    formal_run_done = not _parse_bool(run_meta.get("smoke_check", False)) and str(run_meta.get("stop_reason", "")) != "smoke_check_complete"
    best_selector_ok = str(run_meta.get("best_selector", "")) == FORMAL_BEST_SELECTOR
    threshold_source_ok = str(run_meta.get("threshold_source", "")) == FORMAL_THRESHOLD_SOURCE
    pass_train = formal_run_done and best_ckpt_exists and last_ckpt_exists and train_log_exists
    pass_val = formal_run_done and val_metrics_exists and best_selector_ok and threshold_source_ok
    pass_test = (
        testA_metrics_exists
        and testB_metrics_exists
        and testA_expected_count > 0
        and testB_expected_count > 0
        and testA_actual_count == testA_expected_count
        and testB_actual_count == testB_expected_count
    )
    pass_eval = (
        pass_test
        and metric_note_exists
        and str(run_meta.get("metric_crosscheck_result", "")) == "pass"
        and actual_boundary_width == FORMAL_BOUNDARY_WIDTH
        and actual_eval_cast_policy == FORMAL_CAST_POLICY
        and actual_connectivity == FORMAL_CONNECTIVITY
    )
    pass_visual = error_cases_exists and visuals_testA_exists and visuals_testB_exists
    debug_note_exists = debug_note_path.exists()
    pass_record = (
        data_stage_pass
        and handoff_ready
        and preflight_pass
        and (run_dir / "config.yaml").exists()
        and run_meta_path.exists()
        and run_summary_exists
        and debug_note_exists
        and asset_manifest_path.exists()
    )

    blocking_reasons: list[str] = []
    if not formal_run_done:
        blocking_reasons.append("formal_run_missing_or_still_smoke")
    if testA_actual_count != testA_expected_count:
        blocking_reasons.append(f"testA_sample_count_mismatch:{testA_actual_count}!={testA_expected_count}")
    if testB_actual_count != testB_expected_count:
        blocking_reasons.append(f"testB_sample_count_mismatch:{testB_actual_count}!={testB_expected_count}")
    if actual_eval_cast_policy != FORMAL_CAST_POLICY:
        blocking_reasons.append(f"eval_cast_policy_mismatch:{actual_eval_cast_policy}!={FORMAL_CAST_POLICY}")
    if actual_boundary_width != FORMAL_BOUNDARY_WIDTH:
        blocking_reasons.append(f"boundary_metric_width_mismatch:{actual_boundary_width}!={FORMAL_BOUNDARY_WIDTH}")
    if actual_connectivity != FORMAL_CONNECTIVITY:
        blocking_reasons.append(f"connected_components_connectivity_mismatch:{actual_connectivity}!={FORMAL_CONNECTIVITY}")
    if debug_fields.get("close_status", "missing") != "closed":
        blocking_reasons.append(f"debug_close_status_not_closed:{debug_fields.get('close_status', 'missing')}")

    protocol_error = bool(blocking_reasons)
    stage_pass = pass_train and pass_val and pass_test and pass_eval and pass_visual and pass_record and not protocol_error
    freeze_status = stage_pass
    handoff_ready_for_a2 = stage_pass
    next_action = "enter_03_unet_stability" if handoff_ready_for_a2 else "stay_in_02_complete_formal_a1"
    rollback_reason = "; ".join(blocking_reasons) if blocking_reasons else "none"

    stage_asset_manifest_relpath = _relative_path(manifest_output_path)
    run_meta.update(
        {
            "asset_manifest": stage_asset_manifest_relpath,
            "data_stage_pass": data_stage_pass,
            "handoff_ready": handoff_ready,
            "preflight_pass": preflight_pass,
            "eval_cast_policy": actual_eval_cast_policy,
            "connected_components_connectivity": actual_connectivity,
            "pass_train": pass_train,
            "pass_val": pass_val,
            "pass_test": pass_test,
            "pass_eval": pass_eval,
            "pass_visual": pass_visual,
            "pass_record": pass_record,
            "stage_pass": stage_pass,
            "protocol_error": protocol_error,
            "rollback_reason": rollback_reason,
            "freeze_status": freeze_status,
            "handoff_ready_for_a2": handoff_ready_for_a2,
            "next_action": next_action,
        }
    )
    run_meta_path.write_text(train_entry.dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    split_status = {
        "testA_expected_count": testA_expected_count,
        "testA_actual_count": testA_actual_count,
        "testA_objdice": testa_aggregate.get("objdice", run_meta.get("testA_objdice", "unknown")),
        "testB_expected_count": testB_expected_count,
        "testB_actual_count": testB_actual_count,
        "testB_objdice": testb_aggregate.get("objdice", run_meta.get("testB_objdice", "unknown")),
    }
    gate_status = {
        "pass_train": pass_train,
        "pass_val": pass_val,
        "pass_test": pass_test,
        "pass_eval": pass_eval,
        "pass_visual": pass_visual,
        "pass_record": pass_record,
        "stage_pass": stage_pass,
        "protocol_error": protocol_error,
        "freeze_status": freeze_status,
        "handoff_ready_for_a2": handoff_ready_for_a2,
        "next_action": next_action,
    }
    major_failure_modes = _collect_major_failure_modes(run_dir / "summaries" / "error_cases.md")

    _write_run_summary(
        run_summary_path=run_dir / "summaries" / "run_summary.md",
        run_meta=run_meta,
        gate_status=gate_status,
        split_status=split_status,
        major_failure_modes=major_failure_modes,
        blocking_reasons=blocking_reasons,
    )

    asset_rows = [
        {"asset_key": "config_yaml", "relative_path": _relative_path(run_dir / "config.yaml"), "exists": (run_dir / "config.yaml").exists(), "required_for_a2": True},
        {"asset_key": "run_meta_yaml", "relative_path": _relative_path(run_meta_path), "exists": run_meta_path.exists(), "required_for_a2": True},
        {"asset_key": "train_log_csv", "relative_path": _relative_path(run_dir / "train_log.csv"), "exists": train_log_exists, "required_for_a2": True},
        {"asset_key": "val_metrics_csv", "relative_path": _relative_path(run_dir / "val_metrics.csv"), "exists": val_metrics_exists, "required_for_a2": True},
        {"asset_key": "testA_metrics_csv", "relative_path": _relative_path(run_dir / "testA_metrics.csv"), "exists": testA_metrics_exists, "required_for_a2": True},
        {"asset_key": "testB_metrics_csv", "relative_path": _relative_path(run_dir / "testB_metrics.csv"), "exists": testB_metrics_exists, "required_for_a2": True},
        {"asset_key": "metric_crosscheck_note", "relative_path": _relative_path(run_dir / "metric_crosscheck_note.md"), "exists": metric_note_exists, "required_for_a2": True},
        {"asset_key": "best_ckpt", "relative_path": _relative_path(run_dir / "checkpoints" / "best.ckpt"), "exists": best_ckpt_exists, "required_for_a2": True},
        {"asset_key": "last_ckpt", "relative_path": _relative_path(run_dir / "checkpoints" / "last.ckpt"), "exists": last_ckpt_exists, "required_for_a2": True},
        {"asset_key": "train_curve_csv", "relative_path": _relative_path(run_dir / "curves" / "train_curve.csv"), "exists": (run_dir / "curves" / "train_curve.csv").exists(), "required_for_a2": True},
        {"asset_key": "val_curve_csv", "relative_path": _relative_path(run_dir / "curves" / "val_curve.csv"), "exists": (run_dir / "curves" / "val_curve.csv").exists(), "required_for_a2": True},
        {"asset_key": "visuals_testA_dir", "relative_path": _relative_path(run_dir / "visuals" / "testA"), "exists": visuals_testA_exists, "required_for_a2": True},
        {"asset_key": "visuals_testB_dir", "relative_path": _relative_path(run_dir / "visuals" / "testB"), "exists": visuals_testB_exists, "required_for_a2": True},
        {"asset_key": "error_cases_md", "relative_path": _relative_path(run_dir / "summaries" / "error_cases.md"), "exists": error_cases_exists, "required_for_a2": True},
        {"asset_key": "run_summary_md", "relative_path": _relative_path(run_dir / "summaries" / "run_summary.md"), "exists": True, "required_for_a2": True},
        {"asset_key": "debug_note_md", "relative_path": _relative_path(debug_note_path), "exists": debug_note_exists, "required_for_a2": True},
        {"asset_key": "stage_summary_md", "relative_path": _relative_path(stage_summary_path), "exists": True, "required_for_a2": False},
        {"asset_key": "stage_manifest_csv", "relative_path": _relative_path(manifest_output_path), "exists": True, "required_for_a2": False},
    ]
    _write_stage_manifest(manifest_output_path, asset_rows)
    _write_stage_summary(stage_summary_path, run_dir, debug_note_path, gate_status, split_status, blocking_reasons)

    print(f"run_name={run_name}")
    print(f"stage_pass={str(stage_pass).lower()}")
    print(f"protocol_error={str(protocol_error).lower()}")
    print(f"next_action={next_action}")
    print(f"stage_summary={_relative_path(stage_summary_path)}")
    print(f"manifest={_relative_path(manifest_output_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
