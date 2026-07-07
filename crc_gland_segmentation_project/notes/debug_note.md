# Debug Note

- debug_proto_version: `debug_proto_v1`
- run_name: `A1_UNet_GlaS_v1_seed3407`
- stage_code: `A1`
- config_version: `v1`
- data_proto_version: `01_data_protocol_v1`
- train_proto_version: `train_proto_v1`
- eval_proto_version: `eval_proto_v1`
- model_version: `unet_v1`
- loss_version: `seg_loss_v1`
- postprocess_version: `none_in_v1`
- result_tag: `reproduced`
- aggregation: `single_seed`

## Issue 1

- issue_id: `stage02_acceptance_blocker_001`
- failure_type: `formal_acceptance_blocker`
- suspect_stage: `stage_acceptance`
- evidence_path: `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml; experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv; experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv; experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
- fix_action: `reran the non-smoke formal A1 package, exported full TestA60/TestB20, aligned connected_components_connectivity with the frozen acceptance rule, and regenerated the stage summary`
- verify_result: `formal A1 training ended with early stopping, full TestA60/TestB20 assets were exported, and the remaining stage02 acceptance blocker has been cleared`
- close_status: `closed`
- protocol_error: `false`
- rollback_reason: `none`
