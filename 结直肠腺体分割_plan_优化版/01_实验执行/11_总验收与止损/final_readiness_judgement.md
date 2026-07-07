# Final Readiness Judgement

本文件不是“最后看一眼项目大概怎么样”的总结页，也不是把 stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md 和 writing_entry_decision.md 再抄一遍的待填模板。

它在 `11_总验收与止损` 阶段中的唯一职责是：

> 把阶段矩阵、止损动作、中文起步、英文起步和写稿进入五条正式裁决链，进一步压成项目唯一总状态输出，强制项目只能落到 Pass / Pass with gaps / Not pass 三档之一；后续任何正式写稿、对外结果包使用或总状态复核，都只能读取本文件已经冻结的总状态、理由、缺失资产、关键阻塞项和最终阶段通过标志，不允许再绕过本文件重新主观改判。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面八件事：

1. 项目总状态只允许输出 Pass / Pass with gaps / Not pass 三档之一的唯一结果。
2. 把 stage_gate_matrix.md 的逐阶段通过状态、stop_loss_decision.md 的止损动作、cn_entry_readiness.md 与 en_entry_readiness.md 的起步结论、writing_entry_decision.md 的写稿进入结论，压成单一总状态说明。
3. 面向下游固定输出 `project_status`、`status_reason`、`missing_assets`、`major_blockers`、`final_stage_pass` 五个正式字段。
4. 明确 `project_status_fixed`、`Gate_11` 和 `Final_stage_pass` 在本文件中的落盘方式，防止总状态停留在口头判断。
5. 给出总状态三档的固定映射边界，明确哪些缺口仍属于 `Pass with gaps`，哪些缺口必须把项目打回 `Not pass`。
6. 保留本文件自己的逐阶段总裁决矩阵、证据映射表、后填规则和下游消费语义。
7. 写清独立 `回退条件`、固定回退顺序和重新放行条件，防止项目带着未收口冲突进入正式写稿。
8. 保留本文件自己的 `代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- `01-10` 阶段是否过线的底层判定本体；这些以 stage_gate_matrix.md 与 01_阶段门槛总表.md 为准。
- 争议对象的 retain / downgrade / remove / rollback 动作本体；这些以 stop_loss_decision.md 与 02_止损与回退规则.md 为准。
- 中文保底、英文起步和写稿进入的档位本体；这些分别以 cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 为准。
- `10_结果汇总` 的主表、消融表、图像资产、失败案例和 `package_status` 本体；当前文件只消费它们的正式结论。
- 正式写稿阶段的章节组织、摘要措辞和论文文本；当前文件只回答“项目现在整体到底到哪一档”。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

如果没有一份独立的项目总状态执行层，总验收阶段最容易出现下面这些伪完成状态：

- 阶段矩阵已经做了，但没人把它正式压成唯一 `project_status`。
- 止损、中文、英文和写稿进入都分别有结论，但这些结论并没有被统一成总状态理由和阻塞项。
- 结果包看起来差不多够了，于是口头认为项目“基本通过”。
- 中文和英文都能开始写一部分，于是默认项目已经 `Pass`。
- writing_entry_decision.md 已经允许进入某个轨道，但项目总状态仍没有正式成文。

因此，当前文件必须独立承担“把五条总裁决链压成项目唯一总状态”的职责。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件整篇升级为正式裁决文档，而不是继续保留旧版“总状态 + 矩阵 + 一句话”的轻模板。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把总状态判断写成可被下游直接消费的正式对象，而不是摘要性说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 benchmark、split、阈值来源、后处理和种子等冻结边界，是本文件不能擅改总状态口径的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：提供 `result_source_type`、来源追溯和字段命名要求，是本文件证据映射区和字段区的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束对象级主指标、`best_selector = val_objdice_max`、`GlaS threshold_source = val17`、`CRAG threshold_source = val20`，是本文件判定项目是否真正收口的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把总状态判断落到字段链、输入资产和下游 handoff，而不是停在自然语言总结。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求显式写出 `本轮重写直接依赖的前置文件`、`代码落地接口`、`冲突裁决记录` 和完整收尾闭环。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求差异化 上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环` 不得缩水。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线推进顺序，要求总状态只能消费已经冻结的整条主线，而不是边写边回头改路线叙事。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：要求前序阶段不过线不得进入后续裁决，是本文件必须先消费阶段矩阵的直接依据。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求项目总状态诚实服从止损边界和写稿边界，是本文件不能把项目状态写成“先过再补”的直接依据。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS` benchmark、对象级三指标和 TestA / TestB 分开报告要求，是本文件判断主结果是否真正成立的直接依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供 `GlaS + CRAG` 双 benchmark 语境，是本文件理解 `CRAG` 只能作为补充验证或有限增信的关键锚点。
- `结直肠腺体分割_plan_优化版/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md`：提供 `problem-aware metric selection`，要求总状态不能只看单一像素指标而忽略对象级、边界级和案例级证据。
- `结直肠腺体分割_plan_优化版/03_文献证据/06_我们项目的GlaS_CRAG对照主结果表模板.md`：提供正式主表、联合表和来源标记消费语境，是本文件判断项目是否达到稳定结果包状态的直接文献支撑。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`：提供 `01-10` 各阶段 threshold_passed / handoff_assets_ready / next_stage_ready / stage_pass 的真实状态，是本文件最直接的阶段状态上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`：提供争议对象的正式止损动作和关键阻塞项，是本文件判定项目是否还能落到 `Pass` 的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`：提供中文起步档位、缺失资产和阻塞项，是本文件判断整体写稿 readiness 的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`：提供英文起步档位、是否严格降调、缺失资产和阻塞项，是本文件判断英文是否仍构成总状态阻塞的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`：提供是否进入写稿、首选轨道和剩余小缺口，是本文件判断 `final_stage_pass` 是否能成立的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：冻结主表、消融表、图像资产、summary 和 `package_status`，是本文件判断总状态理由和缺失资产的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：提供 `Gate_11` 与 `Final_stage_pass` 母协议，是本文件的直接上位协议。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：负责 `11` 阶段母协议；当前文件是其中的项目总状态唯一输出层。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`：负责阶段通过线细则；当前文件消费它确认总状态不能脱离阶段真实过线状态。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`：负责止损规则细则；当前文件消费它确认总状态不能和止损结论打架。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`、en_entry_readiness.md、writing_entry_decision.md：分别负责中文、英文和写稿进入的执行层裁决；当前文件负责把这些执行层输出进一步汇总成唯一项目总状态。

#### 同批模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- 邻接强模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- 同层规则模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`

本轮对照后的固定结论是：

- 当前文件必须升级到与 cn_entry_readiness.md、en_entry_readiness.md 和 00_阶段总协议.md 同等级的前部结构与收尾强度，不能继续停留在总状态待填模板层。
- 当前文件必须显式写出 `本轮重写直接依赖的前置文件`、差异化 上游 / 同层 / 下游、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。
- 当前文件虽然以总字段输出为核心，但强度不得弱于同层中英文执行层，否则总验收链会出现“专项裁决强、总状态执行层弱”的断层。

#### 下游文件 / 消费对象

当前文件在 `11_总验收与止损` 目录内已经是项目总状态唯一输出层，不再存在继续负责改判它的同层下游裁决文件。

它的直接下游消费对象固定为：

- 正式写稿阶段对项目总状态的引用说明。
- 最终结果包对外口径、缺失资产和阻塞项说明。
- 后续任何回审、降调、止损复核时的项目总状态基线。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

本文件真正要证明的，不是“项目大体已经做完”，而是：

> 在阶段矩阵、止损动作、中文起步、英文起步和写稿进入五条裁决链都已经由上游压实后，当前项目可以被正式写成一个唯一总状态，并伴随正式理由、缺失资产、关键阻塞项和最终阶段通过标志，不再留下“靠总体感觉继续推进”的灰区。

因此，本文件通过的含义同时包括：

- 项目总状态已经从多份裁决文件汇总成单一输出。
- 总状态理由已经能解释为什么是 `Pass`、为什么只能是 `Pass with gaps`，或为什么必须是 `Not pass`。
- 缺失资产与关键阻塞项已经正式区分，而不是混成一句“还有些问题”。
- `final_stage_pass` 已经能明确说明 `11` 阶段是否真的闭环。

### 3.2 当前文件与 `Gate_11`、`Final_stage_pass`、`project_status_fixed` 的关系

本文件不重新定义 `Gate_11` 与 `Final_stage_pass`，但它是二者落地到总状态输出的正式承接层：

```text
Gate_11 = stage_matrix_ready
          AND project_status_fixed
          AND stop_loss_fixed
          AND cn_ready_fixed
          AND en_ready_fixed
          AND writing_entry_fixed
```

```text
Final_stage_pass = stage_matrix_ready
                   AND project_status_fixed
                   AND stop_loss_fixed
                   AND cn_ready_fixed
                   AND en_ready_fixed
                   AND writing_entry_fixed
```

其中当前文件直接负责落盘的是：

```text
project_status_fixed = project_status_unique
                       AND status_reason_fixed
                       AND blocker_boundary_fixed
                       AND downstream_total_schema_fixed
```

```text
final_readiness_output_ready = project_status
                               + status_reason
                               + missing_assets
                               + major_blockers
                               + final_stage_pass
```

只有当上游五条裁决链已经各自成文，且当前文件把上述五个字段真实填成可交接资产时，项目总状态链路才算真正闭环。

### 3.3 当前文件不允许用什么替代正式总裁决

当前明确不允许把下面这些情况当成“总状态已完成”：

- 只有逐阶段矩阵，没有唯一 `project_status`。
- 只有 Pass / Pass with gaps / Not pass 档位，没有 `status_reason`、`missing_assets` 和 `major_blockers`。
- 只有“可以写中文或英文”的结论，没有把这些结论压成项目总状态。
- 只有写稿进入轨道，没有项目总状态为何能进入或为何不能进入的正式说明。
- 只有口头说法“项目大致通过”，但没有 `final_stage_pass` 的正式落盘。

---

## 4. 阶段门控表达式

### 4.1 当前文件唯一合法输入

本文件不制造新的实验事实，只消费已经冻结的正式裁决资产：

```text
final_readiness_inputs = stage_gate_matrix
                         + stop_loss_actions
                         + cn_entry_outputs
                         + en_entry_outputs
                         + writing_entry_outputs
                         + result_package_assets
```

其中关键来源固定为：

- `stage_gate_matrix`：`01-10` 的 threshold_passed / handoff_assets_ready / next_stage_ready / stage_pass 与 `stage11_pass`。
- `stop_loss_actions`：模块层、外部对比层、`CRAG` 层和写作层的 retain / downgrade / remove / rollback 结论。
- `cn_entry_outputs`：`cn_ready`、`cn_ready_reason`、`cn_missing_assets`、`cn_blockers`、`entry_reason`，以及中文是否已把 `fixed_3_seed_main` 与 supplementary `additional_reporting` 边界写清。
- `en_entry_outputs`：`en_ready`、`en_ready_reason`、`tone_down_required`、`en_missing_assets`、`en_blockers`、`entry_reason，以及英文是否已把 reviewer / rebuttal 级追加 reporting 和主 3-seed` 结论分开。
- `writing_entry_outputs`：`writing_entry_allowed`、`preferred_track`、`remaining_minor_gaps`、`entry_reason`，以及写稿进入是否仍坚持主协议统计口径不被 additional reporting 覆盖。
- `result_package_assets`：`GlaS` 主表、主线消融表、第一批外部对比表、task-specific direct comparison、`CRAG` 表、图像资产、summary、`package_status`、seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 的正式记录边界，以及 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 的正式交接记录。

### 4.2 当前文件固定输出字段

本文件至少必须填写下面字段：

- `project_status = [待填]`
- `status_reason = [待填]`
- `missing_assets = [待填]`
- `major_blockers = [待填]`
- `final_stage_pass = [待填]`

填写规则如下：

- `project_status` 只能填写 Pass / Pass with gaps / Not pass 之一。
- `status_reason` 必须直接说明为什么落到当前档位，不能只写“整体条件较好”。
- `missing_assets` 只写真实缺失且仍需补齐的正式资产，不能混入已具备但还想优化的项。
- `major_blockers` 只写真正阻止项目进入稳定写稿或稳定总状态的关键阻塞项。
- `final_stage_pass` 只能填写 true / false，且必须与五条上游裁决链是否都已固定完全一致。

### 4.3 当前文件固定判定顺序

本文件只允许按下面顺序裁决：

1. 先检查 stage_gate_matrix.md，确认 `01-10` 是否已经形成统一阶段矩阵。
2. 再检查 stop_loss_decision.md，确认所有争议对象是否已经完成唯一动作裁决。
3. 再检查 cn_entry_readiness.md，确认中文写稿是否仍存在关键阻塞。
4. 再检查 en_entry_readiness.md，确认英文写稿是否仍存在关键阻塞或必须严格降调。
5. 最后检查 writing_entry_decision.md，确认是否已经形成正式写稿进入结论和剩余小缺口说明。

只要前一层未通过，就不允许越级给出正向总状态判断。

---

## 5. 本文件核心规则卡片

### 5.1 项目总状态唯一输出规则

- 当前结论：本文件必须把项目总状态输出为 Pass / Pass with gaps / Not pass 三档之一。
- 规则类型：`写作进入前置规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`、stage_gate_matrix.md
- 核心公式或定义参考：`project_status in {Pass, Pass_with_gaps, Not_pass}`
- 采用原因：下游不能再从五条上游裁决链自行拼接出总状态，必须读取唯一档位。
- 不采用的相邻方案：不采用“基本通过”；不采用“接近通过”；不采用没有正式档位的 `pending`。
- 代码落点：当前文件字段区、总状态定级区
- 运行记录字段：`project_status`, `status_reason`
- 验收方式：检查总状态是否被唯一填值，且理由能追溯到上游正式裁决。

### 5.2 三档总状态映射规则

- 当前结论：总状态三档必须同时参考阶段矩阵、止损动作、中英文起步和写稿进入，不允许只看其中单一维度。
- 规则类型：`总裁决映射规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md
- 核心公式或定义参考：`project_status = f(stage_matrix, stop_loss, cn_ready, en_ready, writing_entry)`
- 采用原因：项目总状态本质上是五条裁决链的汇总，而不是某一条链的别名。
- 不采用的相邻方案：不采用“阶段都过了就一定 Pass”；不采用“英文还卡着也能直接 Pass”。
- 代码落点：当前文件总状态定级区
- 运行记录字段：`project_status`, `status_reason`, `major_blockers`, `final_stage_pass`
- 验收方式：检查三档定义是否同时约束阶段通过、止损收口和写稿进入。

### 5.3 缺失资产与阻塞项输出规则

- 当前结论：本文件必须同时输出 `missing_assets` 与 `major_blockers`，不能只给总状态档位。
- 规则类型：`handoff 规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、writing_entry_decision.md
- 核心公式或定义参考：`gap_output = missing_assets + major_blockers`
- 采用原因：下游需要区分哪些只是待补正式资产，哪些是会阻断项目放行的硬问题。
- 不采用的相邻方案：不采用把所有缺口都塞进 `status_reason`；不采用只写一句“还差一些材料”。
- 代码落点：当前文件字段区、证据映射区
- 运行记录字段：`missing_assets`, `major_blockers`, `status_reason`
- 验收方式：检查缺失资产与阻塞项是否能直接支撑下游判断为何不是 `Pass`。

### 5.4 `final_stage_pass` 联动规则

- 当前结论：本文件必须显式输出 `final_stage_pass`，并与 `Gate_11 / Final_stage_pass` 一致。
- 规则类型：`阶段门联动规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- 核心公式或定义参考：`final_stage_pass = stage_matrix_ready AND project_status_fixed AND stop_loss_fixed AND cn_ready_fixed AND en_ready_fixed AND writing_entry_fixed`
- 采用原因：如果没有显式 `final_stage_pass`，总状态就无法正式说明 `11` 是否已经完全闭环。
- 不采用的相邻方案：不采用“总状态已写好就默认阶段通过”；不采用“只要能写中文就算阶段通过”。
- 代码落点：当前文件字段区、总状态定级区
- 运行记录字段：`final_stage_pass`, `project_status`, `status_reason`
- 验收方式：检查 `final_stage_pass` 是否能被逐项回溯到五条上游裁决链。

### 5.5 下游总状态消费规则

- 当前结论：当前文件必须直接支撑正式写稿阶段、结果包对外口径和后续回审使用，不允许让下游再主观改判总状态。
- 规则类型：`terminal handoff 规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：当前文件字段链与 writing_entry_decision.md
- 核心公式或定义参考：`terminal_status_ready = project_status + blockers + missing_assets + final_stage_pass`
- 采用原因：当前文件是 `11` 目录内项目总状态唯一输出层，不能把最终解释职责继续推给下游。
- 不采用的相邻方案：不采用只有给人看的摘要版；不采用没有正式阻塞项和缺失资产的口头总述。
- 代码落点：当前文件字段区、证据映射区、后续写稿状态说明
- 运行记录字段：`project_status`, `status_reason`, `missing_assets`, `major_blockers`, `final_stage_pass`
- 验收方式：检查下游是否可以直接读取当前五个字段而无需额外解释。

### 5.6 主 `3-seed` 与补充 reporting 边界规则

- 当前结论：项目总状态必须继续以冻结主协议 `seed_reporting_mode = fixed_3_seed_main` 为主结论依据；若已经存在 `additional_reporting，它只能作为 supplementary / rebuttal 级附加证据，不得覆盖主 3-seed` 结论，也不得被静默升级成 `Pass` 的新前置门槛。
- 规则类型：`统计 reporting 边界规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：02_止损与回退规则.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`
- 核心公式或定义参考：`main_status_basis = fixed_3_seed_main`; `additional_reporting = supplementary_only`
- 采用原因：总状态层必须同时守住两条线，一是主协议结论不能被事后追加 seed 改写，二是若已有额外 reporting，也不能被误写成进入 `Pass` 的必备条件。
- 不采用的相邻方案：不采用“额外 seed 越多越应自动覆盖主结论”；不采用“没有追加 reporting 就不能算最终通过”；不采用把 `3-seed` 主表与 `3+n seed` supplementary 统计混成同一总状态事实。
- 代码落点：当前文件总状态定级区、证据映射区、总状态说明区
- 运行记录字段：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`, `status_reason`, `major_blockers`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查总状态是否明确以主 `3-seed` 为依据；检查若存在 `additional_reporting`，其角色只被写成补充证据；检查总状态没有把额外 seed 缺失写成新的硬阻塞。

---

## 6. 固定填写字段、逐阶段总裁决矩阵与状态定级

### 6.1 固定填写字段

- `project_status = [待填]`
- `status_reason = [待填]`
- `missing_assets = [待填]`
- `major_blockers = [待填]`
- `final_stage_pass = [待填]`

### 6.2 逐阶段总裁决矩阵

| 阶段 | `threshold_passed` | `handoff_assets_ready` | `next_stage_ready` | `stage_pass` | `evidence_source` | `notes` |
|------|--------------------|------------------------|--------------------|--------------|-------------------|---------|
| `01_数据协议` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `02_UNet流程验证` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `03_UNet稳定性` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `04_Baseline` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `05_LKMA` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `06_Boundary` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `07_Distance` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `08_外部对比` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `09_CRAG验证` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `10_结果汇总` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |

### 6.3 总状态三档固定定义

#### `Pass`

只有同时满足下面条件，当前档位才允许填写为 `Pass`：

- `01-10` 各阶段已形成统一阶段矩阵，且不存在关键阶段 `stage_pass = false`。
- 关键争议对象已全部完成唯一止损动作，不存在待定项。
- 中文起步、英文起步和写稿进入都已形成正式裁决，且不存在关键阻塞项。
- `missing_assets` 只剩不会改变总结论的小型整理项，或为空。
- `major_blockers` 为空。
- 若存在 `additional_reporting`，也只被写成补充说明，不改变主 `3-seed` 总状态依据。
- `final_stage_pass = true`。

#### `Pass with gaps`

只有满足下面条件，当前档位才允许填写为 `Pass with gaps`：

- 阶段矩阵、止损动作、中英文起步和写稿进入已经基本收口。
- 仍存在少量真实缺口，例如个别图像、表注、来源说明或结果包整理待补。
- 这些缺口会进入 `missing_assets`，但不会改变最终模型身份、止损动作或写稿轨道。
- 若 additional reporting 尚未整理成 supplementary / rebuttal 资产，只能作为可选附加缺口处理，前提是主 `3-seed` 结论已经独立成立。
- `major_blockers` 不包含最终模型未定、阶段关键未过线、关键止损未定、中文或英文仍不可起步这类硬阻塞。
- `final_stage_pass` 只能在五条上游裁决链都已经正式成文时为 `true`；若仍有一条未形成正式裁决，则必须为 `false`。

#### `Not pass`

下面任意一条成立，当前档位必须填写为 `Not pass`：

- 仍有关键阶段 `stage_pass = false` 或阶段矩阵本身尚未固定。
- 仍有关键争议对象止损未定、动作冲突或需要回退。
- 中文起步或英文起步仍存在关键阻塞，导致写稿不能稳定进入。
- writing_entry_decision.md 仍只能给出 `not_enter_yet` 或仍依赖后续补关键实验。
- 主 `3-seed` 结论与 additional reporting 边界仍未写清，导致总状态事实来源不唯一。
- `status_reason` 仍无法把项目状态唯一压成一档。

### 6.4 固定字段填写要求

#### `project_status`

- 当前填写：`[待填]`
- 允许值：Pass / Pass with gaps / Not pass

#### `status_reason`

- 当前填写：`[待填]`
- 填写要求：必须直接说明总状态为何落到当前档位，并且同时承接阶段矩阵、止损、中英文和写稿进入结论。

#### `missing_assets`

- 当前填写：`[待填]`
- 填写要求：如果当前不是完全稳定放行，必须列出仍缺失的正式资产。

#### `major_blockers`

- 当前填写：`[待填]`
- 填写要求：只写真正阻止项目进入稳定写稿或稳定总状态的关键阻塞项。

#### `final_stage_pass`

- 当前填写：`[待填]`
- 固定定义：`final_stage_pass = true` 仅当阶段矩阵、总状态、止损、中文起步、英文起步和写稿进入都已形成正式裁决并彼此一致。

---

## 7. 证据映射与后填规则

### 7.1 证据映射表

| 检查项 | 当前状态 | 证据来源 | 备注 |
|--------|----------|----------|------|
| 阶段矩阵是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 止损动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 中文起步是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 英文起步是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 写稿进入是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 项目总状态 | `[待填]` | `[待填]` | `[待填]` |
| 缺失资产 | `[待填]` | `[待填]` | `[待填]` |
| 关键阻塞项 | `[待填]` | `[待填]` | `[待填]` |

### 7.2 现在就要冻结的部分

当前阶段必须先固定下面这些框架：

- 项目总状态允许档位。
- 固定输出字段集合。
- 逐阶段总裁决矩阵结构。
- 三档总状态定义。
- 证据映射表结构。
- 与 `Gate_11`、`Final_stage_pass` 的联动关系。

### 7.3 必须等真实收口后再回填的部分

下面这些内容必须等阶段矩阵、止损、中英文起步和写稿进入真实收口后再填写：

- `project_status`
- `status_reason`
- `missing_assets`
- `major_blockers`
- `final_stage_pass`
- 逐阶段矩阵中的真实状态、来源和备注
- 证据映射表中的真实状态、来源和备注

如果当前仍缺关键阶段过线、关键止损动作、关键中英文写稿边界或关键写稿进入结论，本文件不能提前写成正向总状态。

---

## 8. 代码实现约束、最低交付物与 handoff 资产

### 8.1 本文件必须复用或对齐

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`

### 8.2 本文件禁止修改

- 任何阶段已冻结的实验事实、模型身份和主评估口径。
- retain / downgrade / remove / rollback 的动作本体。
- 中文、英文和写稿进入的档位定义本体。
- `package_status` 和结果包正式资产本体。
- Pass / Pass with gaps / Not pass 之外的新总状态档位。

### 8.3 最低交付物

本文件落地后，至少必须直接支撑下面五类交付物：

1. 项目总状态唯一档位。
2. 项目总状态正式理由。
3. 项目缺失资产清单。
4. 项目关键阻塞项清单。
5. `11` 阶段最终是否真正通过的正式标志。

### 8.4 交接给下游消费对象的正式资产

本文件通过后，至少应交接下面这些资产：

- `project_status`
- `status_reason`
- `missing_assets`
- `major_blockers`
- `final_stage_pass`
- 证据映射表中可追溯的来源说明

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件就必须先回退修正，而不是继续作为项目总状态被消费：

- `project_status` 已经填写，但 `status_reason` 仍是抽象结论，无法回溯到五条上游裁决链。
- `missing_assets` 与 `major_blockers` 混写，导致下游无法区分可补缺口和硬阻塞。
- 总状态与 stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 中任意一个正式结论互相打架。
- `final_stage_pass` 的布尔值与 `Gate_11 / Final_stage_pass` 的定义不一致。
- 项目被写成 `Pass`，但仍依赖补关键实验、补关键止损、补关键中英文边界或补关键写稿进入结论。
- seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 已进入结果资产，但当前文件仍没有写清主 `3-seed` 与 supplementary `additional_reporting` 的边界。

### 9.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查 stage_gate_matrix.md，确认是否仍有关键阶段未过线或矩阵未定。
2. 再检查 stop_loss_decision.md，确认是否仍有争议对象动作未定或动作冲突。
3. 再检查 cn_entry_readiness.md 与 en_entry_readiness.md，确认中英文是否仍存在关键阻塞。
4. 再检查 writing_entry_decision.md，确认是否仍依赖后续补关键实验或仍未形成正式轨道。
5. 最后才允许重新填写当前文件字段与证据映射表。

### 9.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已回写到当前文件字段区或证据映射区。
- 当前文件重新与 stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 完全对齐。
- 当前文件重新满足第 `5` 节规则卡片、第 `6` 节状态裁决要求和第 `8` 节交接资产要求。

---

## 10. 代码落地接口

### 10.1 项目总状态裁决入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 入口类/函数：总状态档位区、理由区、缺失资产区、阻塞项区和阶段通过区
- 输入：阶段矩阵、止损动作、中英文起步裁决、写稿进入裁决、结果包状态
- 输出：`project_status`, `status_reason`, `missing_assets`, `major_blockers`, `final_stage_pass`
- `dtype`：总状态字段为 `string`；阶段通过字段为 `bool`；说明字段为 `string`
- 依赖配置：`stage_pass`, `action`, `cn_ready`, `en_ready`, `writing_entry_allowed`, `package_status`, `seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 前置断言：若仍有关键阶段未过线、关键止损未定、关键写稿边界未定，或主 `3-seed` 与 supplementary `additional_reporting` 边界未写清，不得把项目状态填成 `Pass`
- 运行产物：项目唯一总状态裁决与证据回填结果

### 10.2 上游总裁决一致性校验入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md
- 入口类/函数：字段一致性区、阻塞项汇总区、证据映射区
- 输入：五条上游裁决链的正式字段输出
- 输出：`status_reason`, `missing_assets`, `major_blockers`, `final_stage_pass`
- `dtype`：说明字段为 `string`；通过字段为 `bool`
- 依赖配置：`stage_pass`, `need_stop_loss`, `cn_blockers`, `en_blockers`, `remaining_minor_gaps`
- 前置断言：若上游字段仍互相打架，当前文件不得形成最终版
- 运行产物：总状态与五条上游裁决链之间的一致性说明

### 10.3 正式写稿阶段状态说明入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 入口类/函数：总状态说明区与阻塞项总结区
- 输入：`project_status`, `status_reason`, `missing_assets`, `major_blockers`, `final_stage_pass`
- 输出：正式写稿阶段所需的项目状态说明、缺失资产说明和阻塞项说明
- `dtype`：全部为 string / bool
- 依赖配置：`project_status`, `final_stage_pass`, `preferred_track`, `package_status`
- 前置断言：若总状态仍为 `Not pass` 或关键阻塞未清除，不得把项目描述为已稳定进入正式写稿
- 运行产物：项目总状态的最终对外和对下游解释口径

---

## 11. 冲突裁决记录

- 冲突对象：旧版 final_readiness_judgement.md 的结构强度、交接语义、`Gate_11` 承接、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版收尾闭环。
- 冲突来源：旧稿虽然保留了三档总状态、固定字段和逐阶段矩阵，但整体仍停留在“总状态待填模板”层，缺少和同层强模板一致的前置依赖留痕、差异化 上游 / 同层 / 下游、总状态五链汇总语义、独立回退边界和下游消费语义。
- 裁决结论：本轮将当前文件升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 阶段定位与核心结论 -> 当前文件唯一合法输入、输出与判定流程 -> 规则卡片 -> 固定字段与状态定级 -> 证据映射与后填规则 -> 代码实现约束与 handoff 资产 -> 回退条件 -> 代码落地接口 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的正式执行层结构。
- 裁决理由：如果继续保留旧结构，总验收链会出现“阶段矩阵、止损、中英文和写稿进入都已强化，但总状态执行层仍只是待填模板”的断层。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`、writing_entry_decision.md、正式写稿阶段的项目状态说明
- 是否需要回流修订：需要；后续任何正式写稿阶段都必须直接读取本文件冻结的总状态五字段，而不是重新主观组织项目状态。
- 代码实现影响：影响项目总状态定级、总阻塞项说明和最终阶段通过标志的统一口径。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文
- [x] 已继续补读 `02_路线与投稿`、文献锚点、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`、01_阶段门槛总表.md、02_止损与回退规则.md、stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md，而不是停在总览层
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明为什么这些文件与项目总状态唯一输出层直接相关
- [x] 已完成与 cn_entry_readiness.md、en_entry_readiness.md、00_阶段总协议.md 的模板强度对照，确认当前文件不再弱于同批强模板
- [x] 当前版本按整篇重写执行，不是对旧稿追加少量字段说明
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担项目总状态唯一裁决职责
- [x] 已写清当前文件与 `Gate_11`、`Final_stage_pass` 和 `project_status_fixed` 的关系，没有把它写成脱离母协议的孤立模板
- [x] 已把总状态唯一输出、三档映射、缺失资产与阻塞项、最终阶段通过和下游消费语义写成正式规则卡片
- [x] 每条核心规则都保留了 当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式
- [x] 已保留并强化原文件核心三档定义、固定字段、逐阶段矩阵和一句话目标，没有在升级结构时丢失原始实用内容
- [x] 已把 `project_status`、`status_reason`、`missing_assets`、`major_blockers`、`final_stage_pass` 扩成可被下游直接消费的正式字段链，而不是只留名字不留边界
- [x] 已把 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 接到总状态层，并明确主 `3-seed` 才是冻结结论依据，additional reporting 只能作为 supplementary / rebuttal 级附加证据
- [x] 已写清独立 `回退条件`，没有把回退要求藏在状态定级或总结句里顺带带过
- [x] 已写清 `代码落地接口`，接口对象细化到总状态裁决、一致性校验和正式写稿状态说明三条主链
- [x] 已补写 `冲突裁决记录`，说明旧结构与同层强模板如何统一、影响哪些文件以及后续如何回流修订
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、字段链、规则卡片、交接、回退、接口和收尾闭环
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”
- [x] 当前文件在落盘后继续执行回读与 diagnostics 复核，正文写作不会替代闭环动作
- [x] 当前文件已经达到“可直接指导项目总状态定级并支撑正式写稿阶段状态说明”的最低强度

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成
- 复核范围：至少覆盖标题层级、列表结构、字段命名一致性、上游 / 同层 / 下游 显式落点、`Gate_11 / Final_stage_pass / project_status_fixed` 公式书写、三档总状态命名、固定字段是否完整，以及是否存在可见 markdown 诊断问题
- 复核范围补充：额外检查 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 是否与主 `3-seed` 边界、supplementary `additional_reporting` 边界和总状态定级保持一致
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核
- 对照要求：本节保持与 cn_entry_readiness.md、en_entry_readiness.md、00_阶段总协议.md 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话

---

## 14. 一句话版本

> 本文件的正式职责已经固定为：把阶段矩阵、止损动作、中文起步、英文起步和写稿进入五条裁决链一次压成唯一项目总状态，并把总状态理由、缺失资产、关键阻塞项和 `final_stage_pass` 一起交接给下游；凡是仍有关键阶段未过线、关键止损未定、中英文仍有硬阻塞或写稿进入仍依赖补关键实验的状态，都不得在这里被写成项目已正式通过。
