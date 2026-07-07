# Run Summary

## Inputs

- run_name: `A1_UNet_GlaS_v1_seed3407`
- stop_reason: `early_stopping`
- smoke_check: `false`
- device: `cpu`
- best_epoch: `48`
- best_metric_name: `val_objdice`
- best_metric_value: `0.7626771700880477`

## Gate Status

- pass_train: `true`
- pass_val: `true`
- pass_test: `true`
- pass_eval: `true`
- pass_visual: `true`
- pass_record: `true`
- stage_pass: `true`
- protocol_error: `false`
- freeze_status: `true`
- handoff_ready_for_a2: `true`
- next_action: `enter_03_unet_stability`

## Test Splits

- testA_expected_count: `60`
- testA_actual_count: `60`
- testA_objdice: `0.6941893856375373`
- testB_expected_count: `20`
- testB_actual_count: `20`
- testB_objdice: `0.7619798771629787`

## Findings

- metric_crosscheck_result: `pass`
- major_failure_modes: `adhesion_merge, boundary_over_smooth, fragmented_complex_region, small_gland_miss`
- protocol_abnormal_signs: `none`
- truthful_interpretation: `Current assets complete the formal stage02 closure: non-smoke A1 training ended normally, full TestA60/TestB20 were exported, evaluation and visual assets are aligned, and handoff is ready for stage03.`
