# Precheck Doc Gate Report

## 1. 输入文件
- `project_root`: `D:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project`
- `precheck_guard`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md`

## 2. 检查范围
- 检查 `00_阶段实现卡.md` 与 `stage_definition_gate_report.md` 是否存在，并确认阶段锁定门禁已经先于 Pre-check 裁成 `pass`。
- 检查 `pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md` 与 `Pre-check Guard` 是否全部存在。
- 检查 `Pre-check Guard` 与 `stage_definition_gate_report.md` 的阶段锁定结论是否一致。
- 检查 `Pre-check Guard` 与 `stage_gate_check.md` 的 `Stage Gate Result` 是否一致。
- 检查 `Pre-check Guard` 是否回链 `00_阶段实现卡.md`、`stage_definition_gate_report.md`、四件套与 `precheck_doc_gate_report.md`，并保留 `6.1 预期文档映射`。
- 检查 `pre_check_extraction.md` 是否覆盖 `官方协议固定项 / 路线层已锁定 / 论文支持的候选范围 / 工程冻结规则` 四类约束。
- 检查 `current_codebase_状态.md` 是否覆盖 `datasets/`、`splits/`、`configs/`、`src/`、`scripts/`、`tools/`、`b_class_auxiliary/`、`experiments/`、`external/`、`reports/` 的最小扫描范围。
- 检查阶段实现卡和 Pre-check 文件中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。

## 3. 结论
- `precheck_doc_gate_status`: `pass`

## 4. 详细结果
- [pass] Pre-check 四件套存在、Stage Gate 一致、约束提取与工程扫描锚点检查均通过。
