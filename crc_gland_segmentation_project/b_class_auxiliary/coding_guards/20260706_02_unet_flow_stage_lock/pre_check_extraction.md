# Pre-check Extraction

## 1. 本次任务
- 任务名: `20260706_02_unet_flow_precheck`
- 当前阶段: `02_UNet流程验证`
- 上一阶段: `阶段锁定`
- 日期: `2026-07-06`

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---------|------|---------|---------|----------------|
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md` | `§3`、`§4`、`§8`、`§10` | `02_UNet流程验证` 只能在 `01_数据协议` 正式放行之后启动，且必须先完成 A1 首版闭环，再谈 A2 稳定性或后续 baseline | `官方协议固定项` | 本轮只能做实现前前检，不能把 `03_UNet稳定性`、`04_Baseline` 或更后面的模块阶段提前并入 |
| `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md` | `§1`、`§3`、`§4`、`§7`、`§8` | 当前阶段只允许标准单输出 `UNet`，唯一正式起点是 `A1_UNet_GlaS_v1_seed3407`，并且后续代码必须补齐模型、loss、metrics、engine、eval 与实验配置链 | `路线层已锁定` | 本轮必须把未来工程边界锁在标准 `UNet` 主链，不允许把 `ResNet34-U-Net`、`LKMA`、`Boundary`、`Distance` 或 `CRAG` 扩进来 |
| `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md` | §4.2 到 §4.10 | instance_to_binary、mask_gt_0、RGB、ImageNet mean/std、512x512、light_aug_v1、BCE + Dice、best_selector = val_objdice_max、threshold_source = val17 已形成正式字段链 | 论文支持的候选范围 | 本轮必须提前确认后续代码和配置只能继承这条字段链，不能在编码时临时改字段名或重开默认值 |
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` | `§2` 到 `§6`、`§9` | best checkpoint 只能来自验证集，对象级三指标必须真正落地，TestA 与 TestB 必须分开记录，阈值只能来自 `val17` | `官方协议固定项` | 本轮必须确认后续工程落点包含 object metrics、metric crosscheck、TestA/TestB 分开导出与评估链 |
| `crc_gland_segmentation_project/.trae/skills/制度完成定义.md` | `3. Pre-check 完成` | Pre-check 只有在 `pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、Pre-check Guard 与 `precheck_doc_gate_report.md` 全部成立时才算通过 | `工程冻结规则` | 本轮必须真实生成四件套并运行 precheck gate；如果任何一件与阶段卡、阶段锁定门禁或目录现实不一致，就必须如实阻断 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|------|---------|----------------|
| guard 提取留痕 | `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md` | Pre-check 的约束提取必须正式落盘，后面的 Stage Gate、Current Codebase 与 Pre-check Guard 才有统一上游 |
| 未来正式代码 | src/models/unet.py、src/losses/seg_losses.py、src/metrics/object_metrics.py、src/engine/trainer.py、src/eval/run_eval.py、scripts/train.py、scripts/test.py、scripts/export_visuals.py、scripts/summarize_stage.py | 现在先写清，后续编码时才能判断是否越界到错误目录，或继续把 stage01 的 preflight 入口误当成 stage02 完整训练入口 |
| 未来配置与结果资产 | configs/model/unet_v1.yaml、configs/train/unet_flow_v1.yaml、configs/eval/eval_proto_v1.yaml、configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml、experiments/A1_UNet_GlaS_v1_seed3407/、reports/stage_reports/unet_flow_stage_summary.md | 现在就写清，后续才能审计版本字段、run meta、metrics csv、可视化和阶段总结应该落到哪里 |

## 3. 路线层约束提取

| 来源文件 | 章节 | 当前结论 | 不允许做什么 |
|---------|------|---------|-------------|
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md` | `## 3` 到 `## 10` | 当前唯一目标已经锁定为 `A1_UNet_GlaS_v1_seed3407` 的标准 `UNet` 首版闭环，Pre-check 只是在编码前核对现实工程落点、已有能力与未决问题 | 不允许把 Pre-check 写成正式编码完成证明 |
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_definition_gate_report.md` | `## 3` 到 `## 4` | 阶段锁定门禁已经通过，因此当前工作流允许进入 Pre-check | 不允许跳过 Pre-check 直接开始正式编码 |
| `b_class_auxiliary/runtime_checks/research_alignment_gate_report.md` | `## 2` 到 `## 4` | 研究结论已经明确当前工程并非空壳，而是“数据与 split 已存在，stage02 的模型、loss、engine、eval、metrics 主链尚未落地” | 不允许把当前工程现实误写成“什么都没有”或“训练链已齐全” |
| `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md` | `§7`、`§8` | 当前阶段未来必须新增的正式对象和接口已经被协议点名 | 不允许把 Pre-check 的结论扩写成“后面顺便把 A2 / baseline 一起做了” |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|------|------|---------------|---------------|-----------|
| `项目内正式脚本` | `b_class_auxiliary/tools/check_precheck_docs.py` | `evaluate_task()` | Pre-check 四件套必须与阶段卡、阶段锁定门禁、目录扫描和文档映射保持一致；`current_codebase_状态.md` 还必须覆盖 `datasets/`、`splits/`、`configs/`、`src/`、`scripts/`、`tools/`、`b_class_auxiliary/`、`experiments/`、`external/`、`reports/` 十个目录 | 本轮直接按脚本的真实目录扫描规则、锚点规则和状态一致性规则写文档，并用同一脚本回头验证 |
| `项目内正式脚本` | `b_class_auxiliary/tools/check_stage_definition_gate.py` | `analyze_task()` | 阶段实现卡已经把唯一目标、允许改/禁止改、工程落点和最小运行验证计划锁死 | 本轮只承接这些已锁定边界，不重新发明新的阶段目标 |
| `参考资料` | `结直肠腺体分割_正式参考资料/04_task_specific_benchmarks/GlandSegBenchmarks-master/DCAN/metrics.py` | `ObjectF1score`、`ObjectDice`、`ObjectHausdorff` | 对象级三指标是本任务正式闭环的一部分，不是可选补充 | 本轮把后续 object metrics 模块、TestA/TestB 分开评估和 metric crosscheck 写成必须落地的工程项 |
| `参考资料` | `结直肠腺体分割_正式参考资料/04_正式工程代码映射清单.md` | `## 1` 到 `## 4` | 正式工程应自建 src/models、src/losses、src/metrics、src/engine、src/data、configs 等模块，不直接继承外部仓库的完整训练框架 | 本轮把 stage02 的未来工程落点收敛到现有项目骨架，而不是继续堆叠外部脚本入口 |

## 5. 当前阶段唯一允许改动的变量
- 允许改:
  - `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/` 下的 Pre-check 四件套与 `precheck_doc_gate_report.md`
  - 对当前工程区目录、已放行 stage01 数据能力、已有阶段锁定产物以及 stage02 未来工程落点的真实扫描和前置依据提取
- 不允许改:
  - 不允许开始正式编码
  - 不允许创建 stage02 的模型、loss、engine、eval、metrics、experiment 配置或运行资产
  - 不允许口头假定 `scripts/train.py` 已经等于 stage02 的完整训练入口
- 如果越界会影响:
  - 会破坏 `02_UNet流程验证` 当前“先做实现前前检，再允许编码”的单变量顺序，也会把 stage01 的数据预飞职责和 stage02 的训练闭环职责重新混在一起

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|------|---------|---------|
| py_compile / import | 运行 `b_class_auxiliary/tools/check_precheck_docs.py` 对当前 Pre-check Guard 做正式检查 | 终端输出 `precheck_doc_gate_status`，并生成正式 gate 报告 |
| `smoke run` | 用同一条命令真实检查四件套、阶段卡和阶段锁定门禁的一致性 | `precheck_doc_gate_report.md` 落盘 |
| `dataloader batch` | `not_applicable`；本轮不进入 dataloader 或训练主链实现，只在文档里声明后续编码阶段必须用 `configs/data/glas.yaml` 与 `splits/glas/*.csv` 产出 batch 级证据 | Pre-check 文档明确保留“当前还没有合法 dataloader batch 运行证据” |
| loss / backward | `not_applicable`；本轮不进入训练链验证 | 文档显式保留 `not_applicable`，不把前检写成代码已成立 |
