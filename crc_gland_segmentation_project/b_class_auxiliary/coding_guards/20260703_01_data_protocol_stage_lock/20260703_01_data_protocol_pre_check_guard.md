# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: `01_数据协议`
- 上一阶段: `阶段锁定`
- 当前任务: `20260703_01_data_protocol_precheck`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- `01_数据协议` 必须先把正式输入层恢复成可交接、可追溯、可阻断错误训练入口的唯一数据链，不能直接跳到模型实现 (`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`)
- 当前正式工程区缺少主数据资产与核心工程目录时，Pre-check 必须把这种现实阻塞写清，而不是口头假定“后面补一下就好” (`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md`)
- Pre-check 只有在四件套与 gate 全部成立时才允许进入编码 (`.trae/skills/制度完成定义.md`)

## 3. 来自参考资料的实现依据
- `b_class_auxiliary/tools/check_precheck_docs.py` 已给出 Pre-check 四件套、阶段门禁一致性、目录扫描和真实路径锚点的自动门禁规则
- `b_class_auxiliary/tools/check_stage_definition_gate.py` 已确认当前阶段锁定结论成立，可作为 Pre-check 的直接上游依据
- `b_class_auxiliary/coding_guards/20260703_01_data_protocol_research/研究定标记录.md` 已明确当前最大真实阻塞不是研究不足，而是正式主数据资产和工程区目录尚未落地

## 4. 当前工程已有能力与缺口
- 已有能力:
  - 已有研究记录与研究门禁报告
  - 已有阶段实现卡与阶段锁定门禁报告
  - 已有研究、阶段锁定、Pre-check、运行证据、代码质量、总放行相关 gate 脚本
- 当前缺口:
  - project_root 内还缺少 datasets、splits、configs、src、scripts、experiments、external 等正式工程目录
  - 正式 GlaS 与 CRAG 主数据资产没有在工程区落地，因此当前还不具备进入正式编码前的最小工程现实

## 5. 本次任务边界
- 明确要做:
  - 新建 Pre-check 四件套
  - 运行 `b_class_auxiliary/tools/check_precheck_docs.py`
  - 记录当前工程区真实目录状态和 gate 阻断结论
- 明确不做:
  - 不进入正式编码
  - 不创建训练代码、split 资产、配置资产和运行资产
  - 不伪造正式工程目录已经存在

## 6. 预期代码落点
- 新建文件:
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md`
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md`
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/current_codebase_状态.md`
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md`
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/precheck_doc_gate_report.md`
- 修改文件:
  - `not_applicable`
- 影响的 run / report / external:
  - 只影响 `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/` 下的 Pre-check 文档与 gate 报告

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| `scripts/train.py` | `A` | `01_工程目录框架.md` 与 `01_数据协议/00_阶段总协议.md` 点名正式训练入口 | `reports/stage_reports/implementation_tracking/01_数据协议/scripts_train.py.md` | `not_applicable` | `create` | `scripts/train.py` 属于 A 类正式入口,需要单独说明它在 `01_数据协议` 中只承担 formal preflight 入口职责 |
| `tools/stage01_data_protocol/prepare_glas_split.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md` 明确点名 GlaS split 正式生成工具 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_glas_split.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/prepare_glas_split.py` 属于 A 类正式 split 资产生成器,需要单独说明固定随机种子、grade 分层与 train68/val17/testA60/testB20 的生成规则 |
| `tools/stage01_data_protocol/prepare_crag_split.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md` 明确点名 CRAG split 正式生成工具 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_crag_split.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/prepare_crag_split.py` 属于 A 类正式 split 资产生成器,需要单独说明 train153/val20/test40 的子集装配规则 |
| `tools/stage01_data_protocol/convert_masks.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 明确要求标签协议检查产物 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_convert_masks.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/convert_masks.py` 属于 A 类正式标签协议检查工具,需要单独说明 `mask_gt_0`、binary_mask_summary.csv 与 label_protocol_report.md 的关系 |
| `tools/stage01_data_protocol/build_boundary_targets.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 明确要求 boundary target 证据链 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_boundary_targets.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/build_boundary_targets.py` 属于 A 类正式 boundary target 证据导出工具,需要单独说明 `boundary_width=3` 和 overlay 证据 |
| `tools/stage01_data_protocol/build_distance_targets.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 明确要求 distance target 证据链 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_distance_targets.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/build_distance_targets.py` 属于 A 类正式 distance target 证据导出工具,需要单独说明 distance_target_report.md、`__distmap.npy` 和 heatmap |
| `tools/stage01_data_protocol/check_dataset_pairs.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 明确要求正式数据检查 bundle | `reports/stage_reports/implementation_tracking/01_数据协议/tools_check_dataset_pairs.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/check_dataset_pairs.py` 属于 A 类正式数据检查工具,需要单独说明 pair/readable/duplicate/manual_audit 的统一裁决 |
| `tools/stage01_data_protocol/preview_dataset_samples.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` 明确要求正式 preview 与人工抽查证据 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_preview_dataset_samples.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/preview_dataset_samples.py` 属于 A 类正式 preview 导出工具,需要单独说明 GlaS 5/3/2/2、CRAG 5/3/3 与人工审稿入口 |
| `tools/stage01_data_protocol/validate_data_assets.py` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`、`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` 明确点名数据阶段正式总校验工具 | `reports/stage_reports/implementation_tracking/01_数据协议/tools_validate_data_assets.py.md` | `not_applicable` | `create` | `tools/stage01_data_protocol/validate_data_assets.py` 属于 A 类正式交接裁决工具,需要单独说明 handoff_ready/data_stage_pass/preflight_pass 的汇总逻辑 |
| `reports/stage_reports/data_stage_acceptance.md` | `A` | `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md` 明确点名当前阶段正式验收结果 | `reports/stage_reports/implementation_tracking/01_数据协议/reports_stage_reports_data_stage_acceptance.md.md` | `not_applicable` | `create` | `reports/stage_reports/data_stage_acceptance.md` 属于 A 类正式验收结果,需要单独说明 data_stage_pass/handoff_ready/preflight_pass 的真实判定含义 |
| `b_class_auxiliary/tools/run_minimal_runtime_check.py` | `B` | runtime gate 汇总脚本属于内部流程留痕,不属于计划点名 A 类对象 | `not_applicable` | `not_applicable` | `not_applicable` | 本轮不作为对外交付对象进入学习型说明文 |
| `b_class_auxiliary/tools/check_code_quality_gate.py` | `B` | code-quality gate 脚本属于内部流程留痕,不属于计划点名 A 类对象 | `not_applicable` | `not_applicable` | `not_applicable` | 本轮不作为对外交付对象进入学习型说明文 |
| `scripts/README.md` | `A` | `scripts/` 属于正式工程目录,目录入口说明需要跟随阶段真实能力同步 | `reports/stage_reports/implementation_tracking/01_数据协议/README.md` | `reports/stage_reports/implementation_tracking/01_数据协议/README.md` | `update` | `scripts/README.md` 当前变化属于目录入口说明更新,并入阶段入口文档解释; `reports/stage_reports/implementation_tracking/01_数据协议/implementation_status.md` 会同步更新,但入口同步项保持单值路径 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md` | `B` | Pre-check 提取文件,只服务当前流程留痕 | `not_applicable` | `not_applicable` | `not_applicable` | 不属于 `implementation_tracking` |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md` | `B` | Pre-check 阶段门控检查文件,只服务当前流程留痕 | `not_applicable` | `not_applicable` | `not_applicable` | 不属于学习型说明文 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/current_codebase_状态.md` | `B` | 代码库现实扫描文件,只服务当前流程留痕 | `not_applicable` | `not_applicable` | `not_applicable` | 不属于学习型说明文 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md` | `B` | 当前 Pre-check 汇总件,只服务当前流程留痕 | `not_applicable` | `not_applicable` | `not_applicable` | 不属于学习型说明文 |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 00_阶段实现卡.md: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁报告 stage_definition_gate_report.md: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_definition_gate_report.md`
- `pre_check_extraction.md`: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md`
- `stage_gate_check.md`: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md`
- `current_codebase_状态.md`: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/current_codebase_状态.md`
- `precheck_doc_gate_report.md`: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/precheck_doc_gate_report.md`
