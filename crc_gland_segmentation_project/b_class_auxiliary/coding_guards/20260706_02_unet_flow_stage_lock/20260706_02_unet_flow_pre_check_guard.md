# Pre-check Guard

## 1. 本次任务归属
- 当前阶段: `02_UNet流程验证`
- 上一阶段: `01_数据协议`
- 当前任务: `20260706_02_unet_flow_precheck`
- 阶段实现卡路径: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁结论: `pass`
- Stage Gate Result: `allow`

## 2. 来自规划的硬约束
- `02_UNet流程验证` 只能在 `01_数据协议` 正式放行后启动，且 A1 首版闭环必须先于 A2 稳定性和后续 baseline (`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`)
- 上一阶段正式放行依据: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 当前阶段只允许标准单输出 `UNet`，唯一正式起点是 `A1_UNet_GlaS_v1_seed3407`，后续代码必须补齐模型、loss、engine、eval、metrics 与实验配置链 (`结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`)
- instance_to_binary、mask_gt_0、RGB、ImageNet mean/std、512x512、BCE + Dice、best_selector = val_objdice_max、threshold_source = val17 已被默认配置冻结，后续编码只能继承不能重开 (`结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`)
- Pre-check 只有在四件套与 gate 全部成立时才允许进入编码 (`crc_gland_segmentation_project/.trae/skills/制度完成定义.md`)

## 3. 来自参考资料的实现依据
- `b_class_auxiliary/tools/check_precheck_docs.py` 已给出 Pre-check 四件套、阶段门禁一致性、十目录最小扫描范围与真实路径锚点的自动门禁规则
- `b_class_auxiliary/tools/check_stage_definition_gate.py` 已确认当前阶段锁定结论成立，可作为本轮 Pre-check 的直接上游依据
- `结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py` 已明确对象级三指标是后续 stage02 正式闭环不可绕开的主证据链
- `结直肠腺体分割_正式参考资料/04_正式工程代码映射清单.md` 已明确正式工程应自建 src/models、src/losses、src/metrics、src/engine、src/data 与 configs，而不是整仓继承外部训练框架

## 4. 当前工程已有能力与缺口
- 已有能力:
  - 已有研究记录与研究门禁报告
  - 已有阶段实现卡与阶段锁定门禁报告
  - 已有正式数据资产、正式 split CSV、正式 data 配置与 data 层源码
  - 已有 stage01 formal preflight 入口 `scripts/train.py`
  - 已有 A 类 `tools/stage01_data_protocol/*.py` 工具链与 data stage 正式报告链
  - 已有 B 类门禁脚本、runtime 留痕与 coding guards 集中目录
- 当前缺口:
  - src/models、src/losses、src/metrics、src/engine、src/eval 仍未落地 stage02 正式主链
  - configs/model、configs/train、configs/eval、configs/experiment 仍未落地 stage02 正式配置
  - scripts/test.py、scripts/export_visuals.py、scripts/summarize_stage.py 仍未形成正式入口
  - `experiments/` 当前已经有 `A1_UNet_GlaS_v1_seed3407` 与 `A1_UNet_GlaS_v1_seed3407_smoke` 的真实运行资产；当前 learning-doc 轮次只把配置冻结名对应的规范 smoke 目录继续纳入说明文映射

## 5. 本次任务边界
- 明确要做:
  - 更新 `pre_check_extraction.md`
  - 新建 `stage_gate_check.md`
  - 新建 `current_codebase_状态.md`
  - 新建当前 Pre-check Guard
  - 运行 `b_class_auxiliary/tools/check_precheck_docs.py`
- 明确不做:
  - 不进入正式编码
  - 不创建 stage02 模型、loss、engine、eval、metrics、配置或运行资产
  - 不把 `scripts/train.py` 口头升级成 stage02 完整训练入口

## 6. 预期代码落点
- 新建文件:
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_gate_check.md`
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md`
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md`
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/precheck_doc_gate_report.md`
- 修改文件:
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md`
- 影响的 run / report / external:
  - 只影响 `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/` 下的 Pre-check 文档与 gate 报告；不影响 `experiments/`、`external/` 与 A 类正式报告链

## 6.0 预期最小运行验证
- py_compile / import: 本轮没有正式代码改动，因此运行级 import 与 py_compile 仍记为 not_applicable；当前最小验证只针对 Pre-check 文档门禁
- `最小运行验证命令`: 当前只运行 b_class_auxiliary/tools/check_precheck_docs.py 对本轮 Pre-check Guard 做正式检查
- `smoke run`: 当前只检查四件套、阶段卡与阶段锁定门禁的一致性，不进入训练链
- `dataloader batch`: not_applicable；本轮只声明后续编码阶段必须基于 configs/data/glas.yaml 与 splits/glas/*.csv 留下 batch 级物理证据
- loss / backward / optimizer.step: not_applicable；本轮不进入训练与反向链
- 计划生成的 runtime_check_report.md: `not_applicable`
- 计划生成的代码质量门禁报告: `not_applicable`

## 6.1 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| scripts/test.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 明确点名正式测试入口, 且本轮真实导出了 `experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`、`experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`、预测掩码、crosscheck note 与结果摘要 | reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_test.py.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增正式测试入口对象说明文 |
| scripts/export_visuals.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 明确点名正式可视化重导入口, 且本轮真实导出了 `experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/`、`experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/` 与 `experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` | reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_export_visuals.py.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增正式可视化重导入口说明文 |
| src/eval/export_visuals.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 明确点名正式可视化模块, 且原图、真值、预测与叠加图四件套及错误类型摘要都由它导出 | reports/stage_reports/implementation_tracking/02_UNet流程验证/src_eval_export_visuals.py.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增正式可视化模块说明文 |
| src/eval/run_eval.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 对正式测试资产链要求 split-wise metrics，当前 `scripts/test.py` 已真实通过它导出 TestA 与 TestB 指标表 | reports/stage_reports/implementation_tracking/02_UNet流程验证/src_eval_run_eval.py.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | update | 当前 learning-doc 本轮继续回填 `evaluate_split()` 与 split-wise assets 出口 |
| src/eval/__init__.py | A-薄门面 | 当前只负责把 `evaluate_split`、`export_run_visual_assets` 等正式 eval 入口统一暴露给 CLI, 真实行为已由下游对象说明文覆盖 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 当前作为薄门面处理, 不单列对象级说明文 |
| src/metrics/__init__.py | A-薄门面 | 当前只负责把像素级、对象级、边界级与 sample/batch 聚合入口统一暴露, 真实行为已由下游对象说明文覆盖 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 当前作为薄门面处理, 不单列对象级说明文 |
| src/metrics/pixel_metrics.py | A-薄门面 | 当前只负责把 `dice`、`iou`、`hd95` 门面化导出, 计算逻辑仍回到 `src/metrics/seg_metrics.py` | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 当前作为薄门面处理, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/src_metrics_seg_metrics.py.md` |
| src/metrics/object_metrics.py | A-薄门面 | 当前只负责把 `object_dice_score` 与 `object_hausdorff_score` 门面化导出, 计算逻辑仍回到 `src/metrics/seg_metrics.py` | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 当前作为薄门面处理, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/src_metrics_seg_metrics.py.md` |
| src/metrics/boundary_metrics.py | A-薄门面 | 当前只负责把 `boundary_f1_score` 门面化导出, 计算逻辑仍回到 `src/metrics/seg_metrics.py` | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 当前作为薄门面处理, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/src_metrics_seg_metrics.py.md` |
| src/metrics/seg_metrics.py | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 点名 pixel/object/boundary 三层指标口径，当前 `compute_sample_segmentation_metrics()` 已进入 split-wise 导出链 | reports/stage_reports/implementation_tracking/02_UNet流程验证/src_metrics_seg_metrics.py.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | update | 当前 learning-doc 本轮继续回填 sample rows 与三类薄门面并回主实现的说明 |
| experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求 `TestA` 分开正式落盘, 且当前文件已保留 sample 行与 aggregate 行 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增 TestA 指标资产说明文 |
| experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求 `TestB` 分开正式落盘, 且当前文件已保留 sample 行与 aggregate 行 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增 TestB 指标资产说明文 |
| experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求最少一次口径交叉核对且不能只口头说明, 当前文件已真实记录 split 级重聚合结果 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增 crosscheck 资产说明文 |
| experiments/A1_UNet_GlaS_v1_seed3407/predictions/testA/ | A-目录容器 | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求保留 split-wise prediction 掩码, 当前目录只承载由 `scripts/test.py` 导出的正式 png 结果容器 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 目录容器本身不单列说明文, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_test.py.md` 与 `reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md` |
| experiments/A1_UNet_GlaS_v1_seed3407/predictions/testB/ | A-目录容器 | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求保留 split-wise prediction 掩码, 当前目录只承载由 `scripts/test.py` 导出的正式 png 结果容器 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 目录容器本身不单列说明文, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_test.py.md` 与 `reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md` |
| experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/ | A-目录容器 | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求保留 split-wise visual 四件套, 当前目录只承载 `src/eval/export_visuals.py` 导出的可视化资产容器 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 目录容器本身不单列说明文, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_export_visuals.py.md` 与 `reports/stage_reports/implementation_tracking/02_UNet流程验证/src_eval_export_visuals.py.md` |
| experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/ | A-目录容器 | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求保留 split-wise visual 四件套, 当前目录只承载 `src/eval/export_visuals.py` 导出的可视化资产容器 | - | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | not_applicable | 目录容器本身不单列说明文, 说明义务并入 `reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_export_visuals.py.md` 与 `reports/stage_reports/implementation_tracking/02_UNet流程验证/src_eval_export_visuals.py.md` |
| experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求错误类型整理与可视化回指, 当前文件已真实记录主要失败模式与 overlay 路径 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | create | 当前 learning-doc 本轮新增 error-cases 资产说明文 |
| experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求最终摘要页汇总 split 结果、crosscheck 与主要失败模式, 当前文件已真实回填对应字段 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | update | 当前 learning-doc 本轮继续回填 TestA 与 TestB、`major_failure_modes` 与 `baseline_ready` 结论 |
| experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml | A | `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 要求评估与可视化结果能回填到运行索引页, 当前文件已真实写入 crosscheck 与 visual 计数字段 | reports/stage_reports/implementation_tracking/02_UNet流程验证/experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md | reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md | update | 当前 learning-doc 本轮继续回填 `metric_crosscheck_result`、split 级 objdice 与 visual 字段 |
| b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md | B | Pre-check 提取文件，只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_gate_check.md | B | Pre-check 阶段门控检查文件，只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md | B | 代码库现实扫描文件，只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |
| b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md | B | 当前 Pre-check 汇总件，只服务当前流程留痕 | not_applicable | not_applicable | not_applicable | 不属于 implementation_tracking |

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 `00_阶段实现卡.md`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md`
- 阶段锁定门禁报告 `stage_definition_gate_report.md`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_definition_gate_report.md`
- `pre_check_extraction.md`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md`
- `stage_gate_check.md`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_gate_check.md`
- `current_codebase_状态.md`: `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md`
- `precheck_doc_gate_report.md`: b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/precheck_doc_gate_report.md
