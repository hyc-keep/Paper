# Data Stage Acceptance

## 1. Inputs
- asset_manifest: `reports/stage_reports/asset_manifest.json`
- split_assets_ready: `True`
- check_assets_ready: `True`
- label_assets_ready: `True`
- preview_assets_ready: `True`
- config_assets_ready: `True`
- source_assets_ready: `True`

## 2. Gate Status
- pass_source: `True`
- pass_split: `True`
- pass_pair: `True`
- pass_label: `True`
- pass_binary_mask: `True`
- pass_dtype: `True`
- pass_resize_rule: `True`
- pass_boundary_target: `True`
- pass_distance_target: `True`
- pass_check: `True`
- pass_preview: `True`
- pass_handoff: `True`
- assets_traceable: `True`
- protocol_explainable: `True`
- red_flag: `False`
- data_stage_pass: `True`
- handoff_ready: `True`
- preflight_pass: `True`
- next_action: `enter_02_unet`

## 3. Blocking Reasons
- none

## 4. Formal Outputs
- reports/data_checks/data_check_report.md
- reports/data_checks/dataset_stats.csv
- reports/data_checks/duplicate_check_report.md
- reports/data_checks/foreground_summary.csv
- reports/data_checks/object_size_summary.csv
- reports/data_checks/manual_audit_notes.md
- reports/data_checks/label_protocol_report.md
- reports/data_checks/boundary_target_report.md
- reports/data_checks/distance_target_report.md
- reports/data_preview/*
- reports/data_targets/*
- reports/stage_reports/asset_manifest.json
- reports/stage_reports/data_stage_acceptance.md

## 5. Conclusion
- truthful_interpretation: this report only grants `pass` when the formal 01_数据协议 handoff chain is fully closed; currently any missing manual audit, missing label-target chain, or missing preflight gate must keep the stage blocked.
