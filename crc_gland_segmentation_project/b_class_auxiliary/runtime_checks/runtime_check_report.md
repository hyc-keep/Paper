# Runtime Check Report

## 1. Inputs
- project_root: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project`
- experiment_config: `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- run_name: `A1_UNet_GlaS_v1_seed3407`
- stage_code: `A1`
- dataset_code: `glas`
- model_code: `unknown`
- runtime_profile: `full_training_runtime`

## 2. Config Resolution
- data_config_exists: `pass` -> `configs/data/glas.yaml`
- model_config_exists: `pass` -> `configs/model/unet_v1.yaml`
- train_config_exists: `pass` -> `configs/train/unet_flow_v1.yaml`
- eval_config_exists: `pass` -> `configs/eval/eval_proto_v1.yaml`
- missing_configs: `none`

## 3. Formal Chain Readiness
- train_entrypoint: `pass` -> `scripts/train.py` (implemented)
- dataset_module: `pass` -> `src/data/datasets.py` (implemented)
- trainer: `pass` -> `src/engine/trainer.py` (implemented)
- model_registry: `pass` -> `src/models/__init__.py` (implemented)
- model_module: `pass` -> `src/models/unet.py` (implemented)
- loss_module: `pass` -> `src/losses/seg_losses.py` (implemented)

## 4. Raw Sample Evidence
- sample_source: `split_csv`
- sample_status: `pass`
- sample_reason: `split_csv_sample_readable`
- split_name: `train`
- split_csv: `splits/glas/glas_train68.csv`
- sample_id: `GlaS_official_train_train_1`
- image_path: `datasets/01_GlaS_official_raw/train_1.bmp`
- mask_path: `datasets/01_GlaS_official_raw/train_1_anno.bmp`
- image_shape_hw: `[522, 775]`
- image_dtype: `uint8`
- mask_shape_hw: `[522, 775]`
- mask_dtype: `uint8`
- mask_unique_values: `['0', '1', '2', '3', '4', '5', '6', '7']`

## 5. Formal Runtime Execution
- runtime_execution_attempted: `True`
- runtime_execution_status: `pass`
- runtime_execution_reason: `runtime_payload_loaded`
- runtime_execution_exit_code: `0`
- runtime_blocking_reasons: `[]`
- runtime_command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\scripts\train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --run-name A1_UNet_GlaS_v1_seed3407 --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1`
- runtime_log: `b_class_auxiliary/runtime_checks/runtime_check.log`
- runtime_evidence_json: `b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 6. Runtime Fields
- sample_path: `datasets/01_GlaS_official_raw/train_42.bmp`
- sample_id: `GlaS_official_train_train_42`
- input_shape: `[2, 3, 512, 512]`
- input_dtype: `float32`
- target_shape: `[2, 1, 512, 512]`
- target_dtype: `float32`
- target_unique_values: `[0, 1]`
- output_shape: `[2, 1, 512, 512]`
- output_dtype: `float32`
- loss_value: `1.2771382331848145`
- loss_is_finite: `True`
- backward_executed: `True`
- optimizer_step_executed: `True`

## 7. Runtime Check Status
- smoke_run_pass: pass (formal runtime-check subprocess completed and confirmed formal asset entrypoint checks)
- dataloader_batch_check_pass: pass (formal runtime payload contains sample path/id and input/target tensor metadata)
- tensor_shape_dtype_pass: pass (formal runtime payload contains input/target/output tensor shape and dtype)
- loss_finite_pass: pass (loss_value=1.2771382331848145 and loss_is_finite=True)
- grad_step_pass: pass (formal runtime payload confirms backward and optimizer.step)

## 8. Conclusion
- runtime_check_status: `pass`
- truthful_interpretation: only evidence produced by the formal runtime subprocess may upgrade this report to `pass`; supporting raw-asset inspection alone cannot do that.
