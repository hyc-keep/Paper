# Run Summary

## Inputs

- run_name: `A1_UNet_GlaS_v1_seed3407`
- stop_reason: `smoke_check_complete`
- smoke_check: `true`
- device: `cpu`
- best_epoch: `1`
- best_metric_name: `val_objdice`
- best_metric_value: `0.2769027040775563`

## Gate Status

- pass_train: `false`
- pass_val: `false`
- pass_test: `false`
- pass_eval: `false`
- pass_visual: `true`
- pass_record: `true`
- stage_pass: `false`
- protocol_error: `true`
- freeze_status: `false`
- handoff_ready_for_a2: `false`
- next_action: `stay_in_02_complete_formal_a1`

## Test Splits

- testA_expected_count: `60`
- testA_actual_count: `2`
- testA_objdice: `0.08680183161763688`
- testB_expected_count: `20`
- testB_actual_count: `2`
- testB_objdice: `0.25959866009914456`

## Findings

- metric_crosscheck_result: `pass`
- major_failure_modes: `adhesion_merge, boundary_over_smooth`
- protocol_abnormal_signs: `formal_run_missing_or_still_smoke; testA_sample_count_mismatch:2!=60; testB_sample_count_mismatch:2!=20; debug_close_status_not_closed:open`
- truthful_interpretation: `Current assets only support local smoke connectivity and partial stage02 closure; formal A1 acceptance remains blocked until a non-smoke full run, full TestA60/TestB20, and frozen evaluation fields are re-exported.`
