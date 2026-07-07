# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| datasets/ | 判断正式工程区内是否已经具备数据资产入口，而不是只在工作区外部有说明文 | 检查 `datasets/DATASETS_README.md`、`datasets/DATASET_SOURCE_NOTES.md`；确认当前只有 `2` 份占位说明文,还没有正式数据资产 |
| splits/ | 判断正式 split 清单目录是否已经在工程区落地 | 检查 `splits/README.md`；确认当前只有 `1` 份占位说明文,还没有正式 split CSV |
| configs/ | 判断正式数据配置目录是否已经在工程区落地 | 检查 `configs/data/README.md`；确认当前只有 `1` 份占位说明文,正式配置仍待后续编码阶段补齐 |
| src/ | 判断正式源码主链目录是否已经在工程区落地 | 检查 `src/README.md`；确认当前只有 `1` 份源码骨架占位说明文 |
| scripts/ | 判断正式训练或评估脚本目录是否已经在工程区落地 | 检查 `scripts/README.md`；确认当前只有 1 份脚本骨架说明文 |
| `tools/` | 判断当前工程区内 A 类正式数据工具链是否已经落地 | 检查 `tools/stage01_data_protocol/convert_masks.py`、`tools/stage01_data_protocol/validate_data_assets.py`、`tools/stage01_data_protocol/prepare_glas_split.py`、`tools/stage01_data_protocol/prepare_crag_split.py` |
| `b_class_auxiliary/` | 判断 B 类门禁脚本、运行留痕和治理产物是否已经按新结构集中隔离 | 检查 `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/runtime_checks/runtime_check_report.md`、`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md` |
| experiments/ | 判断正式运行资产目录是否已经在工程区落地 | 检查 `experiments/README.md`；确认当前只有 `1` 份运行资产骨架占位说明文 |
| external/ | 判断第三方适配层目录是否已经在工程区落地 | 检查 `external/README.md`；确认当前只有 `1` 份第三方对齐骨架占位说明文 |
| reports/ | 判断当前工程区内 A 类正式报告与验收产物是否真实存在,并和 B 类留痕目录分开 | 检查 `reports/data_checks/binary_mask_summary.csv`、`reports/data_checks/boundary_target_report.md`、`reports/stage_reports/data_stage_acceptance.md` |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| datasets/ | `datasets/DATASETS_README.md`、`datasets/DATASET_SOURCE_NOTES.md` | 已有 `2` 份项目内数据说明文件；当前是最小骨架状态，正式 GlaS 与 CRAG 数据资产仍未落地 | `是`; 后续编码前必须把占位说明文替换成正式数据资产链 |
| splits/ | `splits/README.md` | 已有 `1` 份 split 骨架说明文；当前仍未生成正式 split CSV | `是`; 后续编码前必须把占位说明文替换成正式 split 资产 |
| configs/ | `configs/data/README.md` | 已有 `1` 份配置骨架说明文；当前处于最小骨架状态,正式数据配置仍待后续编码阶段补齐 | `是`; 后续编码前必须把占位说明文替换成正式数据配置 |
| src/ | `src/README.md` | 已有 `1` 份源码骨架说明文；当前仍未恢复正式数据、模型和训练主链源码 | `是`; 后续编码前必须按阶段边界恢复正式源码落点 |
| scripts/ | `scripts/README.md` | 已有 1 份脚本骨架说明文；当前仍未恢复正式训练或评估入口脚本 | 是; 后续编码前必须补正式脚本入口 |
| tools/ | `tools/stage01_data_protocol/convert_masks.py`、`tools/stage01_data_protocol/validate_data_assets.py`、`tools/stage01_data_protocol/prepare_glas_split.py`、`tools/stage01_data_protocol/prepare_crag_split.py` | 根目录 `tools/` 已完成阶段化整理: `tools/stage01_data_protocol/` 承载 `01_数据协议` 的 `8` 个 A 类正式工具, `tools/c_pending_review/` 承载 `2` 个 C 类待裁决脚本 | `是`; 当前结构已从单层平铺改成阶段目录 + C 类隔离目录 |
| b_class_auxiliary/ | `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/tools/enforce_workflow_gate.py`、`b_class_auxiliary/runtime_checks/runtime_check_report.md`、`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md` | 已存在 `4` 个固定子目录、至少 `44` 个文件；B 类门禁脚本、运行留痕与治理产物已经从主区隔离出来 | `是`; 本轮继续把路径口径和模板规则统一到这个目录 |
| experiments/ | `experiments/README.md` | 已有 `1` 份运行资产骨架说明文；当前仍未进入正式 run 资产阶段 | `是`; 这符合当前尚未进入编码与运行证据阶段的现实 |
| external/ | `external/README.md` | 已有 `1` 份第三方对齐骨架说明文；当前仍未恢复正式适配层 | `是`; 后续若需要参考实现接入才会处理 |
| reports/ | `reports/data_checks/binary_mask_summary.csv`、`reports/data_checks/boundary_target_report.md`、`reports/stage_reports/data_stage_acceptance.md` | 已存在 4 个正式报告子目录、至少 170 个文件；A 类正式报告继续留在 reports 下，B 类 guard/runtime 留痕已迁到 b_class_auxiliary/ | 是；本轮会核对 `reports/` 是否只保留正式报告链，不再混入 B 类流程留痕 |

## 2. 已实现能力
- 已有研究门禁: `b_class_auxiliary/tools/check_research_alignment_gate.py`
- 已有阶段锁定门禁: `b_class_auxiliary/tools/check_stage_definition_gate.py`
- 已有 Pre-check 门禁: `b_class_auxiliary/tools/check_precheck_docs.py`
- 已有运行证据与总放行脚本: `b_class_auxiliary/tools/run_minimal_runtime_check.py`、`b_class_auxiliary/tools/enforce_workflow_gate.py`
- 已有 A 类正式数据工具: `tools/stage01_data_protocol/convert_masks.py`、`tools/stage01_data_protocol/validate_data_assets.py`、`tools/stage01_data_protocol/prepare_glas_split.py`、`tools/stage01_data_protocol/prepare_crag_split.py`
- 已有 C 类待裁决脚本隔离目录: `tools/c_pending_review/`
- 已有正式研究与阶段锁定留痕: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_research/` 与 `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/`

## 3. 缺口与风险
- 缺口1: project_root 内虽然已经补齐最小目录骨架，但这些目录当前仍只是占位说明文状态，不是正式工程资产
- 缺口2: 当前正式 GlaS 与 CRAG 主数据资产仍未在工程区落地，因此后续没有合法的正式 split、配置、检查资产、预览资产和交接资产入口
- 风险1: `b_class_auxiliary/tools/check_precheck_docs.py` 现在会同时检查 `tools/` 与 `b_class_auxiliary/` 的真实样本路径；如果模板和实例继续混写两者，后续阶段会再次被前检阻断
- 风险2: 如果忽略这些缺口直接进入编码，后续训练无法证明自己读取的是哪一版正式输入层

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md` | `create` | 需要把 Pre-check 的上游约束、路线约束和允许改动变量正式提取落盘 | `否`; 当前任务目录此前没有这份文件 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md` | `create` | 需要把“当前为何允许进入 Pre-check”写成正式门禁检查文件 | `否`; 当前任务目录此前没有这份文件 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/current_codebase_状态.md` | `create` | 需要把工程区当前真实目录状态、缺口和风险写成可审计结果 | `否`; 当前任务目录此前没有这份文件 |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md` | `create` | 需要把 Pre-check 汇总件正式落盘，并为 precheck gate 提供输入 | `否`; 当前任务目录此前没有这份文件 |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 本轮为什么会受影响 |
|------|----------|------------------|
| 代码层 | `not_applicable` | 本轮只做 Pre-check，不进入正式代码实现 |
| 配置层 | `not_applicable` | 本轮不创建正式配置或资产 |
| 运行资产层 | `not_applicable` | 本轮不产生 experiments 运行资产 |
| 报告层 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md`、`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md`、`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/current_codebase_状态.md`、`b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/20260703_01_data_protocol_pre_check_guard.md` | 本轮所有正式新增都属于 Pre-check 文档产物 |
| 治理层 | `not_applicable` | 本轮不再修改 `.trae/skills/` 或计划正文 |
