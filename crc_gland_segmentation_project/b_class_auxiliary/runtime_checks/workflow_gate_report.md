# Workflow Gate Report

## 1. 固定执行顺序
- `research_alignment_record` -> `stage_definition_gate` -> `precheck_doc_gate` -> `runtime_check` -> `code_quality_gate` -> `workflow_gate`

## 2. 本轮正式产物要求
- required_artifact: `b_class_auxiliary/coding_guards/20260705_02_unet_flow_research/研究定标记录.md`
- required_artifact: `b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`
- required_artifact: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md`
- required_artifact: `b_class_auxiliary/runtime_checks/stage_definition_gate_report.md`
- required_artifact: `b_class_auxiliary/runtime_checks/precheck_doc_gate_report.md`
- required_artifact: `b_class_auxiliary/runtime_checks/workflow_gate_report.md`
- required_artifact: `b_class_auxiliary/runtime_checks/实现依据记录.md`
- required_artifact: `b_class_auxiliary/runtime_checks/runtime_check_report.md`
- required_artifact: `b_class_auxiliary/runtime_checks/runtime_evidence.json`
- required_artifact: `b_class_auxiliary/runtime_checks/runtime_check.log`
- required_artifact: `b_class_auxiliary/runtime_checks/code_quality_gate_report.md`
- required_artifact: `reports/stage_reports/implementation_tracking/02_UNet流程验证/实现依据记录.md`
- missing_artifacts: `none`

## 3. 各步结果
### research_alignment_gate
- status: `pass`
- reason: `completed`
- output_path: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project/b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`
- return_code: `0`
- command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_research_alignment_gate.py --project-root D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project --research-record b_class_auxiliary/coding_guards/20260705_02_unet_flow_research/研究定标记录.md --output b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`

### stage_definition_gate
- status: `pass`
- reason: `completed`
- output_path: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project/b_class_auxiliary/runtime_checks/stage_definition_gate_report.md`
- return_code: `0`
- command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_stage_definition_gate.py --project-root D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project --stage-card b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md --output b_class_auxiliary/runtime_checks/stage_definition_gate_report.md`

### precheck_doc_gate
- status: `pass`
- reason: `completed`
- output_path: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project/b_class_auxiliary/runtime_checks/precheck_doc_gate_report.md`
- return_code: `0`
- command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_precheck_docs.py --project-root D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project --precheck-guard b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md --output b_class_auxiliary/runtime_checks/precheck_doc_gate_report.md`

### runtime_check
- status: `pass`
- reason: `completed`
- output_path: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project/b_class_auxiliary/runtime_checks/runtime_check_report.md`
- return_code: `0`
- command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\run_minimal_runtime_check.py --project-root D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project --experiment-config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --split train --sample-index 0 --output b_class_auxiliary/runtime_checks/runtime_check_report.md --evidence-output b_class_auxiliary/runtime_checks/runtime_evidence.json --log-output b_class_auxiliary/runtime_checks/runtime_check.log --train-runtime-output b_class_auxiliary/runtime_checks/train_runtime_payload.json`

### code_quality_gate
- status: `pass`
- reason: `completed`
- output_path: `D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project/b_class_auxiliary/runtime_checks/code_quality_gate_report.md`
- return_code: `0`
- command: `D:\conda_envs\sd\python.exe D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_code_quality_gate.py --project-root D:/12_Medical_Image_Segmentation/Paper/crc_gland_segmentation_project --post-qc-guard b_class_auxiliary/runtime_checks/post_qc_guard.md --output b_class_auxiliary/runtime_checks/code_quality_gate_report.md`

## 4. 结论
- workflow_gate_status: `pass`
- 规则: 任一步不是 `pass`，后续依赖步骤一律 `blocked`，不允许跳步放行。
- 规则: 缺少任何本轮必需正式产物，也不允许宣称“正式任务已通过”。
- 说明: `learning_doc_gate` 与 `formal_doc_gate` 属于后续 `说明文档` 或治理阶段检查，不属于当前 `workflow_gate_report.md` 的前置条件。
