# Stage Gate Check

## 1. 阶段信息
- 当前阶段: `01_数据协议`
- 上一阶段: `阶段锁定`
- 当前任务: `20260703_01_data_protocol_precheck`

## 2. 上一阶段通过证据
- 通过文件: `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_definition_gate_report.md`
- 通过状态: `stage_definition_gate_status = pass`
- 关键交付物:
  - `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md`
  - `b_class_auxiliary/tools/check_stage_definition_gate.py`

## 3. 当前阶段进入条件

| 条件 | 证据文件 | 检查方法 | 结果 |
|------|---------|---------|------|
| 阶段实现卡已存在且已写清当前唯一目标 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md` | 检查第 3 节与第 5 节是否明确写出“恢复并冻结正式输入层”与禁止越界到训练阶段 | `pass` |
| 阶段锁定门禁已通过 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/stage_definition_gate_report.md` | 打开文件确认 `stage_definition_gate_status = pass` | `pass` |
| 上一阶段研究已正式通过 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_research/research_alignment_gate_report.md` | 打开文件确认 `research_alignment_gate_status = pass` | `pass` |
| 当前阶段所需前置边界已经写死 | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/00_阶段实现卡.md` | 检查 `## 4`、`## 7`、`## 9` 是否已经把真实工程阻塞、未来工程落点和未决问题写清楚 | `pass` |
| 本轮任务没有越界到正式编码之后 | `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md` | 对照当前任务只允许写 Pre-check 四件套和运行 precheck gate，不进入正式编码、运行证据和总放行 | `pass` |

## 4. 阻断项

| 阻断项 | 是否触发 | 说明 |
|-------|---------|------|
| `00_阶段实现卡.md` 缺失或仍是空壳 | `否` | 阶段卡已存在且 stage gate 已裁成 `pass` |
| 阶段锁定门禁不是 pass | `否` | 当前门禁报告明确为 `pass` |
| 上一阶段未正式 `pass` | `否` | 研究阶段门禁报告明确为 `pass` |
| 当前任务越界到后续阶段 | `否` | 本轮只做 Pre-check 文档与 gate，不做正式编码 |
| 数据/评估/命名协议仍未冻结 | `否` | 这些内容在研究记录与阶段卡中已锁定为上游约束；当前阻塞不在“协议未读清”，而在工程目录与资产尚未落地 |
| 本轮拟修改文件不属于当前阶段允许范围 | `否` | 本轮只新增 `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/` 下的 Pre-check 文档与 gate 报告 |

## 5. 结论
- Stage Gate Result: `allow`
- 结论说明:
  - 阶段锁定已经正式通过，当前任务边界也已锁死，因此允许进入 Pre-check。
  - 当前允许进入的含义只是“允许做实现前前检”，不等于“允许开始正式编码”。

## 5.1 本轮允许进入的工程落点

| 对象 | 允许动作 | 预期落点 |
|------|---------|---------|
| 正式代码 | `not_applicable` | 本轮不进入源码主链、训练脚本或 `tools/stage01_data_protocol/*.py` 等正式实现层 |
| 配置与正式资产 | `not_applicable` | 本轮不创建数据配置、split 清单、数据检查资产或数据预览资产 |
| 模板与协议文档 | `not_applicable` | 本轮不修改 `.trae/skills/` 和 `结直肠腺体分割_plan_优化版/` 下的正式协议正文 |
| 报告与 guard 产物 | `create` | `b_class_auxiliary/coding_guards/20260703_01_data_protocol_stage_lock/pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`20260703_01_data_protocol_pre_check_guard.md`、`precheck_doc_gate_report.md` |

## 6. 红线提醒
- 当前 `allow` 只表示允许进入 Pre-check，不表示允许进入正式编码。
- 如果 precheck_doc_gate_report 最终不是 `pass`，本轮不能口头宣布 Pre-check 已完成。
- 如果目录扫描证明当前工程区缺少 `datasets/`、`splits/`、`configs/`、`src/`、`scripts/`、`experiments/`、`external/` 等正式工程目录，后续编码前必须先正面处理，而不是跳过。
