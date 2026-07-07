# 模板8: Pre-check Guard

> **使用场景**: 汇总本轮任务的 Pre-check 结论,明确能做什么、不能做什么、准备改哪些文件。
> **调用顺序**: 先看 `00_技能体系导航.md`,并确保阶段卡正式输出名 00_阶段实现卡.md、阶段锁定门禁报告 stage_definition_gate_report.md、`模板5_Pre-check提取.md`、`模板6_阶段门控检查.md`、`模板7_当前代码库状态.md` 已先完成
> **与中央门禁的关系**: 本模板负责生成本轮 Pre-check 的正式汇总件; 它不能跳过前三个 guard 文件直接凭印象填写

---

这份模板不是重复抄一遍 `模板5~7`。

它真正负责的是:
- 把分散的 Pre-check 结果压成“本轮允许做什么 / 禁止做什么”的正式边界
- 让三个月后的自己只看这一份文件,也能知道当时为什么允许进入实现
- 给后面的 `Post-QC Guard` 提供明确的对照基线

```markdown
# Pre-check Guard

## 1. 本次任务归属
- 当前阶段:
- 上一阶段:
- 当前任务:
- 阶段实现卡路径:
- 阶段锁定门禁结论: `pass / partial / fail`
- Stage Gate Result: `allow / blocked`

## 2. 来自规划的硬约束
- [约束1] (`文件 -> 章节`)

## 3. 来自参考资料的实现依据
- [依据1] (`论文 / 仓库 / 脚本来源`)

## 4. 当前工程已有能力与缺口
- 已有能力:
- 当前缺口:

## 5. 本次任务边界
- 明确要做:
- 明确不做:

## 6. 预期代码落点
- 新建文件:
- 修改文件:
- 影响的 run / report / external:

## 6.1 预期最小运行验证
- `py_compile / import`:
- `最小运行验证命令`: `python b_class_auxiliary/tools/run_minimal_runtime_check.py --experiment-config [configs/experiment/*.yaml]`
- `smoke run`:
- `dataloader batch`:
- `loss / backward / optimizer.step`:
- 计划生成的 `runtime_check_report.md`: `b_class_auxiliary/runtime_checks/runtime_check_report.md / not_applicable`
- 计划生成的代码质量门禁报告: `code_quality_gate_report.md / not_applicable`

**怎么写才算合格:**
- 如果本轮存在正式代码改动,这里不能只写“后面再检查”
- 至少要提前写出 1 条最小运行命令或最小运行入口
- 至少要提前写出 1 组 tensor / loss / backward 证据准备怎么留
- 如果本轮没有正式代码改动,允许写 `not_applicable`,但必须说明原因

## 6.2 预期文档映射

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 计划动作 | 备注 |
|-------------|------|---------|-------------|-----------|---------|------|
| `[文件路径]` | `A / B / C` | `[计划条款号 / 参考资料出处 / 归 B 或归 C 的理由]` | `[implementation_tracking/对象说明文路径] / not_applicable` | `[reports/stage_reports/implementation_tracking/阶段名/README.md 或 implementation_status.md 的单个路径] / not_applicable` | `create / update / append_version / not_applicable` | [为什么这样判定] |

补充规则:

- 只有 A 类对象才允许填写真实 `对象级说明文`
- B / C 类对象的 `对象级说明文` 固定写 `not_applicable`
- 如果本轮只是阶段入口变化,`入口同步项` 只能填写一个真实阶段入口文档路径; 如果 `README.md` 和 `implementation_status.md` 都同步了,优先填写主入口路径,并在 `备注` 里说明另一份也已同步
- 这里写的 A / B / C 归类,必须与 `制度完成定义.md` 和后续 `Post-QC Guard` 保持一致

## 7. 上游 guard 文件回链
- 阶段卡正式输出名 00_阶段实现卡.md: [本轮是否已完成 / 关键结论]
- 阶段锁定门禁报告 stage_definition_gate_report.md: [本轮是否已运行 `b_class_auxiliary/tools/check_stage_definition_gate.py` / 关键结论]
- `pre_check_extraction.md`: [本轮是否已完成 / 关键结论]
- `stage_gate_check.md`: [本轮是否已完成 / 关键结论]
- `current_codebase_状态.md`: [本轮是否已完成 / 关键结论]
- `precheck_doc_gate_report.md`: [本轮是否已运行 `b_class_auxiliary/tools/check_precheck_docs.py` / 关键结论]

**红线提醒:**
- 如果阶段锁定门禁报告 stage_definition_gate_report.md 不是 `pass`,这里不能把 `Stage Gate Result` 写成 `allow`
- 如果阶段卡正式输出名 00_阶段实现卡.md 和 `Stage Gate` 的边界说法不一致,必须先回退修正
- 如果 `Stage Gate Result = blocked`,这里不能再写“明确要做”
- 这里写的“预期代码落点”必须能和后面的 `Post-QC Guard` 一一对照
- 这里写的“预期最小运行验证”也必须能和后面的代码质量门禁及 `Post-QC Guard` 一一对照
- 这里写的“预期文档映射”也必须能和后面的 `Post-QC Guard` 一一对照
- 如果 `precheck_doc_gate_report.md` 还是 `partial / fail`,不能声称 Pre-check 已正式通过
- 如果 `模板5~7` 里已经发现阻断项,不能在这里把问题洗掉
```
