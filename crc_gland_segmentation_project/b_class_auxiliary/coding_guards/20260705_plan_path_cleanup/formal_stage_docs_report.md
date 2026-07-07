# Formal Doc Gate Report

## 1. 输入文档
- `scripts/README.md`
- `b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `b_class_auxiliary/runtime_checks/code_quality_gate_report.md`
- `b_class_auxiliary/runtime_checks/post_qc_guard.md`
- `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/README.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/implementation_status.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/00_交付范围内正式对象清单.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/scripts_train.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_glas_split.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_crag_split.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_convert_masks.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_boundary_targets.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_distance_targets.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_check_dataset_pairs.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_preview_dataset_samples.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/tools_validate_data_assets.py.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/reports_stage_reports_data_stage_acceptance.md.md`
- `reports/stage_reports/implementation_tracking/01_数据协议/当前阶段为什么能pass以及下一步怎么看.md`
- `D:/12_Medical_Image_Segmentation/Paper/结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- `D:/12_Medical_Image_Segmentation/Paper/结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- `D:/12_Medical_Image_Segmentation/Paper/结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- `D:/12_Medical_Image_Segmentation/Paper/结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`

## 2. 检查范围
- 检查正式模板/规程/协议文档是否缺少关键章节骨架。
- 检查文档是否同时回答了角色边界、前置依赖、规则或证据、代码或工程落点、验收或回退。
- 检查文档是否保留当前正式状态口径，而不是回退到旧二元写法。
- 检查文档中的反引号路径是否能解析到真实存在的文件，而不是只写一个看起来像路径的字符串。
- 检查治理文件组（中央 SKILL / 导航 / 总规范 / implementation_tracking 规程）是否共同覆盖状态口径、自动门禁命令和调用顺序。
- 检查文档是否留下了最小路径锚点、来源锚点和质检痕迹。
- 对启用了“单文档双达标模式”的正式文档，额外检查下面这些教学信号是否达到最小可执行强度：
- `## 0. 先给结论` 是否存在，且开头至少有 3 条结论型 bullet。
- `设计取舍对比` 是否是结构化对比，而不是只写一句“最后选了什么”。
- `误区预防` 是否同时给出误区/误判和对应的纠正或正确理解。
- `联读顺序` 是否给出带顺序词和可定位目标的真实阅读路径。
- `收口自检` 是否给出至少 2 条带动作词和证据对象的自检/复核步骤。
- `学习型说明文人工审稿清单.md` 是否不仅被回链，还明确出现人工终审/人工审稿动作。

## 3. 结论
- `formal_doc_gate_status`: `pass`

## 4. 检查摘要

- `章节与边界`: 未发现 formal gate 异常。
- `证据与锚点`: 未发现 formal gate 异常。
- `状态口径`: 未发现 formal gate 异常。
- `治理一致性`: 未发现 formal gate 异常。
- `双达标模式`: 未发现 formal gate 异常。

## 5. 详细结果
- [pass] 正式模板/规程/协议文档的关键章节、边界、代码落点与质检痕迹检查通过。
