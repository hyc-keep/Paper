# Pre-check Extraction

## 1. 本次任务
- 任务名: `20260703_01_data_protocol_precheck`
- 当前阶段: `01_数据协议`
- 上一阶段: `阶段锁定`
- 日期: `2026-07-03`

## 2. 规划约束提取

| 来源文件 | 章节 | 约束内容 | 约束类型 | 对本次实现的影响 |
|---------|------|---------|---------|----------------|
| `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md` | `§1`、`§4`、`§8` | `01_数据协议` 必须先于 `02_UNet流程验证` 完成，且不得把输入层问题拖到训练阶段再处理 | `官方协议固定项` | 本轮 Pre-check 只能围绕正式输入层、前置依据、目录现实和未来工程落点展开，不能越界到模型实现 |
| `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` | `§1`、`§4`、`§6`、`§8` | 数据阶段通过前提是正式输入层可交接、可追溯、可阻断错误训练入口 | `路线层已锁定` | 本轮必须明确当前工程区还缺哪些正式目录和资产，才能判断后续编码是否有合法落点 |
| `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md` | `§1`、`§4`、`§9`、`§10` | 后续必须形成七条链门控、红线回退、最小交接放行和训练前预飞检查 | `论文支持的候选范围` | 本轮需要提前把未来会落到哪些工具、配置、报告与交接对象写清楚，同时诚实记录当前还没有这些资产 |
| `.trae/skills/制度完成定义.md` | `Pre-check 完成` | Pre-check 只有在四件套齐全且 precheck_doc_gate_report 为 pass 时才算正式完成 | `工程冻结规则` | 本轮必须先真实生成四件套并跑 gate；如果 gate 因目录缺失阻断，也要如实保留阻断结论，不能口头放行 |

## 2.1 预期工程落点

| 对象层 | 预期落点 | 为什么现在就要写 |
|------|---------|----------------|
| guard 提取留痕 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md` | Pre-check 的约束提取必须先正式落盘，后面的 Stage Gate 和 Guard 才能回链 |
| 报告与门禁 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_gate_check.md`、`current_codebase_状态.md`、`20260703_01_data_protocol_pre_check_guard.md`、`precheck_doc_gate_report.md` | Pre-check 的真实边界、目录扫描结果和 gate 结论都必须有独立正式产物 |
| 正式代码 | `not_applicable` | 本轮只做 Pre-check，不进入正式编码，因此不应该在本轮伪造源码目录、脚本目录或 `tools/stage01_data_protocol/*.py` 的实现结果 |

## 3. 路线层约束提取

| 来源文件 | 章节 | 当前结论 | 不允许做什么 |
|---------|------|---------|-------------|
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md` | `## 3` 到 `## 10` | 当前唯一目标仍是恢复并冻结正式输入层，Pre-check 只是为后续编码做正式前检，不是提前编码 | 不允许把 Pre-check 写成“正式数据资产已经就位” |
| `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_definition_gate_report.md` | `## 3` 到 `## 4` | 阶段锁定已经通过，因此允许进入 Pre-check 审查代码库现实和未来工程落点 | 不允许跳过 Pre-check 直接开始 `src/`、`configs/`、`splits/` 实现 |
| `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md` | `§6`、`§7`、`§8` | 后续编码阶段会涉及 `tools/stage01_data_protocol/*.py`、数据配置文件、数据检查报告目录和数据预览目录等正式落点 | 不允许在当前工程区目录和资产尚未明确前就假装这些落点已经准备好 |

## 4. 文献/参考实现提取

| 类型 | 来源 | 章节/文件/行号 | 可直接采用内容 | 本项目调整 |
|------|------|---------------|---------------|-----------|
| `项目内正式脚本` | `b_class_auxiliary/tools/check_precheck_docs.py` | `evaluate_task()` | Pre-check 四件套必须与阶段卡、阶段锁定门禁、目录扫描和预期文档映射保持一致 | 本轮直接按脚本的真实目录扫描规则写文档，并用它回头验证当前工程区是否达到进入编码前的最低要求 |
| `项目内正式脚本` | `b_class_auxiliary/tools/check_stage_definition_gate.py` | `analyze_task()` | 阶段实现卡已经把唯一目标、边界、依据、工程落点与最小验证计划锁死 | 本轮 Pre-check 只承接这些已锁定边界，不重新发明新的阶段目标 |
| `参考资料` | `结直肠腺体分割_正式参考资料/00_文档与官方链接汇总.md` | `GlaS Challenge`、MILD-Net 与 CRAG 语义锚点 | benchmark 身份、测试边界和对象级指标背景必须先由数据协议保护 | 本轮只把这些约束提成实现前前置依据，不在 Pre-check 阶段扩写模型或评估实现 |

## 5. 当前阶段唯一允许改动的变量
- 允许改:
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/` 下的 Pre-check 四件套与 `precheck_doc_gate_report.md`
  - 对当前工程区目录、已有门禁脚本、研究与阶段锁定产物的真实扫描和前置依据提取
- 不允许改:
  - 不允许开始正式编码
  - 不允许创建训练代码、模型代码、实验配置或运行资产
  - 不允许伪造正式数据目录、正式 split、正式配置或正式交接资产已经完成
- 如果越界会影响:
  - 会破坏 `01_数据协议` 当前“先审查前置现实，再允许编码”的单变量顺序

## 5.1 本轮最小验证计划

| 验证项 | 计划动作 | 预期证据 |
|------|---------|---------|
| py_compile 与 import | 运行 `b_class_auxiliary/tools/check_precheck_docs.py` 对当前 Pre-check Guard 做正式检查 | 终端输出 precheck_doc_gate_status，并生成正式 gate 报告 |
| `smoke run` | 用同一条命令真实检查四件套与阶段锁定产物的一致性 | `precheck_doc_gate_report.md` 落盘 |
| `dataloader batch` | `not_applicable`；本轮不进入数据加载链实现，只在文档里提前声明未来编码阶段需要什么目录与资产 | Pre-check 文档明确记录“当前还没有合法 dataloader batch 条件” |
| loss 与 backward | `not_applicable`；本轮不进入训练链验证 | 文档显式保留 `not_applicable`，不把前检写成代码已成立 |
