# Writing Entry Decision

本文件不是“最后决定先写中文还是先写英文”的便签页，也不是把 final_readiness_judgement.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md 再抄一遍的轻量模板。

它在 `11_总验收与止损` 阶段中的唯一职责是：

> 把阶段矩阵、对象级止损、中文起步、英文起步、结果包状态和项目总状态约束，进一步压成唯一的写稿进入执行层输出，正式冻结 `writing_entry_allowed`、`preferred_track`、`remaining_minor_gaps`、`entry_reason` 四个字段；后续正式写稿、结果包说明和复审回看，都只能读取本文件已经冻结的进入结论与轨道边界，不允许再绕开本文件凭主观紧迫感、语言偏好或“先写再补关键实验”的想法重新改判。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面八件事：

1. 把写稿进入结论压成 true / false 的唯一输出值，而不是继续保留“可以考虑开始写”的口头灰区。
2. 把 cn_entry_readiness.md 与 en_entry_readiness.md 的裁决结果进一步映射成 cn_first / cn_first_then_en / en_direct / not_enter_yet 四档轨道之一。
3. 面向下游固定输出 `writing_entry_allowed`、`preferred_track`、`remaining_minor_gaps`、`entry_reason` 四个正式字段。
4. 把 `Gate_11` 中与写稿进入有关的最后一段链路正式落盘为 `writing_entry_fixed`，避免写稿入口停留在口头判断。
5. 明确哪些缺口仍属于“不改变写稿主线的小缺口”，哪些缺口必须把进入结论打回 `not_enter_yet`。
6. 写清当前文件与 stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、final_readiness_judgement.md 的联动边界，防止写稿进入和总状态、止损链互相打架。
7. 写清独立 `回退条件`、固定回退顺序和重新放行条件，防止带着关键阻塞、关键公平性冲突或关键资产缺口进入正式写稿。
8. 保留本文件自己的 `代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- `01-10` 阶段是否过线的底层判定本体；这些以 stage_gate_matrix.md 和 01_阶段门槛总表.md 为准。
- 争议对象的 retain / downgrade / remove / rollback 动作本体；这些以 stop_loss_decision.md 与 02_止损与回退规则.md 为准。
- 中文与英文起步档位本体；这些分别以 cn_entry_readiness.md、en_entry_readiness.md 为准。
- 项目总状态 Pass / Pass with gaps / Not pass 的唯一档位本体；这些以 final_readiness_judgement.md 为准。
- 结果包、表格、图像资产、`package_status` 和论文章节写作本体；当前文件只回答“现在能不能正式进入写稿，以及先走哪条轨道”。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

如果没有一份独立的写稿进入执行层，总验收阶段最容易出现下面这些伪完成状态：

- 中文与英文都各自有结论，但没人把它们压成唯一写稿轨道。
- 总状态看起来不差，于是口头认为“可以先写起来”，但关键止损或关键缺口其实还没收口。
- `cn_ready`、`en_ready`、`tone_down_required`、`major_blockers` 都分别存在，却没有一份文件明确回答“到底现在能不能进入写稿”。
- 结果包大体齐了，于是默认可以边写边补关键实验，重新打开已经冻结的实验判断。
- 总状态文件与写稿进入文件互相引用后，没有一份独立执行层来压住最终进入结论。

因此，当前文件必须独立承担“把多条裁决链压成唯一写稿进入输出”的职责。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件整篇升级为正式执行层，而不是继续保留写稿进入待填模板。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把写稿进入判断写成下游可消费对象，而不是摘要性说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 benchmark、split、阈值来源、后处理、种子和版本冻结边界，是当前文件不能临时放宽写稿口径的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：提供 `run_name`、`result_source_type`、`aggregation`、来源追溯和字段命名要求，是当前文件证据映射与字段链一致性的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束 `best_selector = val_objdice_max`、`GlaS threshold_source = val17`、`CRAG threshold_source = val20` 和对象级口径，是当前文件不能把混合口径结果包装成可写结论的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把写稿进入写成输入资产、字段输出和 handoff 接口，而不是自然语言摘要。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求显式写出 `本轮重写直接依赖的前置文件`、`代码落地接口`、`冲突裁决记录` 和完整收尾闭环。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求差异化 上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环` 不得缩水。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线推进顺序，要求写稿进入只能消费已经冻结的主线，不允许“先写再定实验”。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：要求前序阶段不过线不得进入后续写稿判断，是当前文件必须先消费阶段矩阵的直接路线依据。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求写稿强度服从止损结论、总状态档位和投稿层级边界，是当前文件不能把进入写稿写成“先开写、后降调”的直接依据。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS` benchmark、对象级三指标和 TestA / TestB 分开报告要求，是写稿进入不能依赖混合结果叙事的直接依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供 `GlaS + CRAG` 双 benchmark 语境，是当前文件压住 `CRAG` 只能提供有限增信的关键锚点。
- `结直肠腺体分割_plan_优化版/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md`：提供 `problem-aware metric selection`，要求写稿进入同时参考对象级、边界级和案例级证据，而不是只看单一像素指标。
- `结直肠腺体分割_plan_优化版/03_文献证据/06_我们项目的GlaS_CRAG对照主结果表模板.md`：提供正式主表、联合表和来源标记消费语境，是当前文件判断结果包是否达到可写程度的直接文献支撑。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`：提供各阶段 `stage_pass`、`stage_matrix_ready` 和阶段缺口，是写稿进入最直接的阶段状态上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`：提供争议对象的保留、降级、删除和回退动作，是写稿进入不能绕开的对象级红线上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`：提供中文是否可开写、缺失资产、阻塞项和进入理由，是 `preferred_track` 的直接中文上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`：提供英文是否可起步、是否必须严格降调、缺失资产、阻塞项和进入理由，是 `preferred_track` 的直接英文上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：冻结主表、消融、图像资产、summary 和 `package_status`，是当前文件区分“小缺口”和“硬阻塞”的直接上游。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：负责 `Gate_11` 母协议；当前文件是其中的写稿进入执行层。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`：负责项目总状态唯一输出；当前文件必须与其在 `project_status`、`major_blockers`、`final_stage_pass` 上保持一致，但不重新定义其档位本体。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`：负责阶段门槛细则；当前文件消费它校验“不再依赖补关键实验”的红线。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`：负责止损规则细则；当前文件消费它防止写稿轨道与止损动作打架。

#### 同批模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- 邻接强模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 同层输出模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`

本轮对照后的固定结论是：

- 当前文件必须升级到与 stop_loss_decision.md、final_readiness_judgement.md、en_entry_readiness.md 同等级的前部结构与收尾强度，不能继续停留在写稿进入待填模板层。
- 当前文件必须显式写出 `本轮重写直接依赖的前置文件`、差异化 上游 / 同层 / 下游、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。
- 当前文件虽然以四个字段和轨道判断为核心，但强度不得弱于同层总状态执行层和止损执行层，否则总验收链会出现“上游裁决强、写稿入口弱”的断层。

#### 下游文件 / 消费对象

当前文件在 `11_总验收与止损` 内已经是写稿进入的最终执行层，不再存在继续改判它的同层下游裁决文件。

它的直接下游消费对象固定为：

- 正式中文写稿阶段与英文写稿阶段的启动顺序说明。
- 最终结果包和项目总结中关于“是否已进入写稿”的对外口径。
- 后续任何回审、止损复核和项目收口时的写稿入口基线。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

本文件真正要证明的，不是“现在大概可以开始写了”，而是：

> 在阶段矩阵、止损动作、中英文起步、结果包边界和项目总状态约束都已经由上游压实后，当前项目可以被正式写成一个唯一写稿进入结论，并伴随唯一轨道、剩余小缺口和进入理由，不再留下“靠总体感觉先开写”的灰区。

因此，本文件通过的含义同时包括：

- 写稿进入已经从口头倾向变成正式布尔结论。
- 首选轨道已经唯一化，而不是同时保留多种主观偏好。
- `remaining_minor_gaps` 已经明确限定为不改变总状态、不改变模型身份、不改变止损动作的轻缺口。
- `entry_reason` 已经能解释为什么现在允许进入，或为什么必须继续停在 `not_enter_yet`。

### 3.2 当前文件与 `Gate_11`、`writing_entry_fixed` 和总状态链的关系

本文件不重新定义 `Gate_11`，但它是其中写稿进入子链的正式承接层：

```text
Gate_11 = stage_matrix_ready
          AND project_status_fixed
          AND stop_loss_fixed
          AND cn_ready_fixed
          AND en_ready_fixed
          AND writing_entry_fixed
```

当前文件直接负责落盘的是：

```text
writing_entry_fixed = writing_entry_allowed_fixed
                      AND preferred_track_fixed
                      AND remaining_minor_gap_boundary_fixed
                      AND entry_reason_fixed
```

```text
writing_entry_output_ready = writing_entry_allowed
                             + preferred_track
                             + remaining_minor_gaps
                             + entry_reason
```

这里必须明确区分：

- `writing_entry_fixed` 回答的是“写稿进入执行层是否已经成文并可被下游消费”。
- `writing_entry_allowed` 回答的是“项目当前是否真的允许进入正式写稿”，它不是文件是否完成的同义词。

### 3.3 当前文件与 final_readiness_judgement.md 的互校边界

当前文件与 final_readiness_judgement.md 之间必须保持互校，而不是互相改判：

- 如果 final_readiness_judgement.md 已先定级，当前文件必须继承其 `project_status`、`major_blockers` 和 `final_stage_pass` 边界，不允许写成更乐观的进入结论。
- 如果当前文件先完成，final_readiness_judgement.md 在最终冻结时必须忠实读取当前文件的 `writing_entry_allowed`、`preferred_track` 和 `remaining_minor_gaps`。
- 任何一方如果与另一方在是否允许写稿、是否仍有关键阻塞上互相打架，都按本文件第 `9` 节 `回退条件` 处理。

### 3.4 当前文件不允许用什么替代正式写稿进入执行层

当前明确不允许把下面这些情况当成“写稿进入已完成”：

- 只有中文和英文两个文件的结论，没有唯一 `preferred_track`。
- 只有“建议先写中文”或“英文也可以”，没有 `writing_entry_allowed` 和 `remaining_minor_gaps`。
- 只有总状态档位，没有明确说明是否已经达到正式写稿入口。
- 只有“还差一点图表或表注”的口头说法，没有把它们限定为不影响主结论的小缺口。
- 只有口头说法“先写再补关键实验”，没有把这种情况明确打回 `not_enter_yet`。

---

## 4. 阶段门控表达式

### 4.1 当前文件唯一合法输入

本文件不制造新的实验事实，只消费已经冻结或已要求冻结的正式资产：

```text
writing_entry_inputs = stage_gate_matrix
                       + stop_loss_outputs
                       + cn_entry_outputs
                       + en_entry_outputs
                       + result_package_assets
                       + final_readiness_constraints
```

其中关键来源固定为：

- `stage_gate_matrix`：各阶段 threshold_passed / handoff_assets_ready / next_stage_ready / stage_pass 与 `stage_matrix_ready`。
- `stop_loss_outputs`：`stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 以及对象级动作表。
- `cn_entry_outputs`：`cn_ready`、`cn_ready_reason`、`cn_missing_assets`、`cn_blockers`、`entry_reason`，以及中文是否已把主 `3-seed` 与 supplementary `additional_reporting` 区分清楚。
- `en_entry_outputs`：`en_ready`、`en_ready_reason`、`tone_down_required`、`en_missing_assets`、`en_blockers`、`entry_reason，以及英文是否已把 reviewer / rebuttal 级追加 reporting 和主 3-seed` 结论分开。
- `result_package_assets`：主结果表、消融表、第一批外部对比表、`CRAG` 表、图像资产、summary、`package_status`、seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 的正式记录边界，以及 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 的正式交接记录。
- `final_readiness_constraints`：如果 final_readiness_judgement.md 已先形成正式定级，则必须继承其中的 `project_status`、`status_reason`、`missing_assets`、`major_blockers`、`final_stage_pass` 作为一致性约束；如果该文件尚未最终冻结，则这里只冻结字段链和判断边界，不提前冒写正向结论。

### 4.2 当前文件固定输出字段

本文件至少必须填写下面字段：

- `writing_entry_allowed = [待填]`
- `preferred_track = [待填]`
- `remaining_minor_gaps = [待填]`
- `entry_reason = [待填]`

填写规则如下：

- `writing_entry_allowed` 只能填写 true / false。
- `preferred_track` 只允许填写 cn_first / cn_first_then_en / en_direct / not_enter_yet。
- `remaining_minor_gaps` 只写不改变总状态、不改变最终模型、不改变止损动作、不要求补关键实验的小缺口。
- `entry_reason` 必须同时承接总状态、止损结论、中英文起步和结果包边界，直接回答为何允许或不允许进入写稿。

### 4.3 当前文件固定判定顺序

本文件只允许按下面顺序裁决：

1. 先检查 stage_gate_matrix.md 与 01_阶段门槛总表.md，确认当前项目是否已经不再依赖补关键实验。
2. 再检查 stop_loss_decision.md，确认关键对象是否已经完成保留、降级、删除或回退动作。
3. 再检查 cn_entry_readiness.md，确认中文是否能作为稳定起写入口。
4. 再检查 en_entry_readiness.md，确认英文是否能直接起步，或只能在严格降调下起步。
5. 最后检查 final_readiness_judgement.md 与 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`，确认项目总状态、阻塞项和结果包边界是否允许真正进入写稿。

只要前一层未通过，就不允许越级给出正向写稿进入结论。

---

## 5. 本文件核心规则卡片

### 5.1 写稿进入唯一输出规则

- 当前结论：本文件必须把写稿进入结论输出为 true / false 和唯一轨道，不允许继续停留在口头建议层。
- 规则类型：`写稿进入执行规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`、stage_gate_matrix.md
- 核心公式或定义参考：`writing_entry_allowed in {true, false}` 且 `preferred_track in {cn_first, cn_first_then_en, en_direct, not_enter_yet}`
- 采用原因：下游不能再从中文、英文和总状态文件自行拼接出写稿入口，必须读取唯一执行层结果。
- 不采用的相邻方案：不采用“基本可以开始”；不采用“先写部分章节”；不采用没有正式档位的 `pending`。
- 代码落点：当前文件固定字段区、轨道裁决区
- 运行记录字段：`writing_entry_allowed`, `preferred_track`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查是否存在唯一进入结论和唯一轨道，且理由可回溯到上游正式资产。

### 5.2 不得依赖补关键实验规则

- 当前结论：只要仍依赖补关键实验、补关键止损、补关键公平性说明或补关键结果包资产，当前文件就必须输出 `writing_entry_allowed = false` 和 `preferred_track = not_enter_yet`。
- 规则类型：`阶段放行规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：stage_gate_matrix.md、01_阶段门槛总表.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- 核心公式或定义参考：`entry_ready = no_key_experiment_gap AND no_key_handoff_gap`
- 采用原因：总验收阶段不允许靠“先写起来再补关键证据”回头打开已经冻结的实验判断。
- 不采用的相邻方案：不采用“边写边补关键实验”；不采用“正文先占位，后面再验证”。
- 代码落点：当前文件最后检查区、汇总判断区
- 运行记录字段：`writing_entry_allowed`, `remaining_minor_gaps`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查所有剩余缺口是否都已被限定为非关键缺口。

### 5.3 中文优先轨道规则

- 当前结论：当中文已达到稳定起稿，而英文仍存在严格降调要求或较大支撑缺口时，当前文件应优先输出 `cn_first`。
- 规则类型：`轨道选择规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：cn_entry_readiness.md、en_entry_readiness.md
- 核心公式或定义参考：`preferred_track = cn_first when cn_ready >= startable AND en_ready != stable_direct`
- 采用原因：中文优先轨道用于先稳定收口主叙事和图表，不等于英文已经完全放行。
- 不采用的相邻方案：不采用英文仍卡阻时强行 `en_direct`；不采用同时宣布双轨无差别并行。
- 代码落点：当前文件轨道裁决区
- 运行记录字段：`preferred_track`, `entry_reason`, `remaining_minor_gaps`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查中文、英文和止损边界是否共同支持中文先行。

### 5.4 中英联动轨道规则

- 当前结论：只有当中文和英文都已具备稳定起步条件，且英文主要缺口只剩可控降调或少量整理时，当前文件才允许输出 `cn_first_then_en` 或 `en_direct`。
- 规则类型：`双语联动规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：cn_entry_readiness.md、en_entry_readiness.md、final_readiness_judgement.md
- 核心公式或定义参考：`dual_track_ready = cn_ready_fixed AND en_ready_fixed AND no_major_blockers`
- 采用原因：双语轨道不只是语言偏好问题，还要服从总状态、阻塞项和英文 claim 强度边界。
- 不采用的相邻方案：不采用英文仍需大幅补证时直接 `en_direct`；不采用总状态仍有硬阻塞时写成 `cn_first_then_en`。
- 代码落点：当前文件轨道裁决区、汇总判断区
- 运行记录字段：`preferred_track`, `writing_entry_allowed`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查双语轨道是否与总状态和英文降调边界一致。

### 5.5 小缺口边界规则

- 当前结论：`remaining_minor_gaps` 只能包含不会改变模型身份、止损动作、项目总状态和写稿轨道的小缺口。
- 规则类型：`缺口边界规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、final_readiness_judgement.md
- 核心公式或定义参考：`minor_gap = non_blocking AND non_decision_changing`
- 采用原因：如果小缺口边界不压死，写稿进入会被用来掩盖仍未解决的关键阻塞。
- 不采用的相邻方案：不采用把关键表格、关键公平性说明、关键止损动作写成“小缺口”；不采用把“补关键实验”写进 `remaining_minor_gaps`。
- 代码落点：当前文件固定字段区、证据映射区
- 运行记录字段：`remaining_minor_gaps`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查所有剩余缺口是否都不会改变进入结论。

### 5.6 总状态互校规则

- 当前结论：当前文件的写稿进入结论不得比 final_readiness_judgement.md 的总状态和阻塞项更乐观。
- 规则类型：`总状态互校规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：final_readiness_judgement.md
- 核心公式或定义参考：`entry_claim <= project_status_boundary`
- 采用原因：如果总状态仍有硬阻塞，写稿进入就不能被写成稳定放行。
- 不采用的相邻方案：不采用“总状态还没过，但先进入写稿”；不采用把总状态问题解释成纯语言选择问题。
- 代码落点：当前文件汇总判断区、回退条件区
- 运行记录字段：`writing_entry_allowed`, `preferred_track`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查写稿进入、项目总状态和关键阻塞项是否彼此一致。

### 5.7 主 `3-seed` 与补充 reporting 写稿边界规则

- 当前结论：写稿进入只能以冻结主协议 `seed_reporting_mode = fixed_3_seed_main` 的结论作为正文主入口依据；若已经存在 `additional_reporting，它只能进入 supplementary / rebuttal 级附加材料，不得覆盖主 3-seed` 结论，也不得被静默升级成允许写稿的新前置门槛。
- 规则类型：`统计 reporting 边界规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：02_止损与回退规则.md、cn_entry_readiness.md、en_entry_readiness.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`
- 核心公式或定义参考：`writing_main_basis = fixed_3_seed_main`; `additional_reporting = supplementary_only`
- 采用原因：写稿进入层必须避免两种漂移，一是把补充 seed 统计写成新的主正文事实，二是把“尚未补额外 seed”误写成不能进入写稿的硬阻塞。
- 不采用的相邻方案：不采用“额外 seed 越多越应自动覆盖主结论”；不采用“没有 additional reporting 就不能进入写稿”；不采用把主 `3-seed` 与 `3+n seed` supplementary 统计混成同一入口依据。
- 代码落点：当前文件轨道裁决区、汇总判断区、证据映射区
- 运行记录字段：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`, `writing_entry_allowed`, `preferred_track`, `remaining_minor_gaps`, `entry_reason`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查写稿进入是否明确以主 `3-seed` 为依据；检查若存在 `additional_reporting`，其角色只被写成 supplementary / rebuttal 级附加材料；检查写稿阻塞项没有把额外 seed 缺失写成新的硬阻塞。

---

## 6. 固定填写字段、轨道裁决与汇总判断

### 6.1 固定填写字段

- `writing_entry_allowed = [待填]`
- `preferred_track = [待填]`
- `remaining_minor_gaps = [待填]`
- `entry_reason = [待填]`

### 6.2 轨道允许值与固定定义

#### `cn_first`

只有满足下面条件，当前轨道才允许填写为 `cn_first`：

- 中文已达到 `可直接开写` 或 `可开写但需边补图表`。
- 英文仍存在严格降调要求，或仍有较大支撑缺口但尚未构成中文起写阻塞。
- 总状态允许进入写稿，但更适合先用中文稿收口主叙事、图表和局限性边界。

#### `cn_first_then_en`

只有满足下面条件，当前轨道才允许填写为 `cn_first_then_en`：

- 中文已可稳定起稿。
- 英文也可以起步，或可以在严格降调下同步准备。
- 先中文、后英文能更稳地收口图表、claim 边界和写作节奏。

#### `en_direct`

只有满足下面条件，当前轨道才允许填写为 `en_direct`：

- 中文和英文都已形成稳定起步条件。
- 英文公平性边界、来源边界、task-specific direct comparison 和 `CRAG` 角色都已明确。
- 总状态与阻塞项不再要求先用中文稿消化关键不确定性。
- 若存在 `additional_reporting，也已明确降到 supplementary / rebuttal 层，不覆盖主 3-seed` 写稿入口事实。

#### `not_enter_yet`

下面任意一条成立，当前轨道必须填写为 `not_enter_yet`：

- 总状态未定，或仍存在关键阻塞项。
- 止损动作仍未收口，或仍存在必须回退对象。
- 中文或英文起步状态仍不明确。
- 结果包仍缺关键表格、关键图像、关键来源边界或关键公平性说明。
- 仍依赖补关键实验才能写正文。
- 主 `3-seed` 与 supplementary `additional_reporting` 边界仍未写清，导致写稿入口事实来源不唯一。

### 6.3 固定字段填写要求

#### `writing_entry_allowed`

- 当前填写：`[待填]`
- 固定定义：只有当进入写稿不会重新打开阶段判断、止损动作和总状态边界时，才允许填写为 `true`。

#### `preferred_track`

- 当前填写：`[待填]`
- 允许值：cn_first / cn_first_then_en / en_direct / not_enter_yet

#### `remaining_minor_gaps`

- 当前填写：`[待填]`
- 填写要求：只列非关键缺口，例如排版微调、表注细化、少量图注补写或轻量整理，不得写入关键实验、关键裁决、关键公平性和关键资产缺失。

#### `entry_reason`

- 当前填写：`[待填]`
- 填写要求：必须直接说明当前为何允许或不允许进入写稿，并说明为何选择对应轨道。

### 6.4 汇总判断表

| 字段 | 当前值 | 证据来源 | 备注 |
|------|--------|----------|------|
| `stage_matrix_ready` | `[待填]` | `[待填]` | `[待填]` |
| `project_status` | `[待填]` | `[待填]` | `[待填]` |
| `stop_loss_needed` | `[待填]` | `[待填]` | `[待填]` |
| `cn_ready` | `[待填]` | `[待填]` | `[待填]` |
| `en_ready` | `[待填]` | `[待填]` | `[待填]` |
| `tone_down_required` | `[待填]` | `[待填]` | `[待填]` |
| `writing_entry_allowed` | `[待填]` | `[待填]` | `[待填]` |
| `preferred_track` | `[待填]` | `[待填]` | `[待填]` |
| `remaining_minor_gaps` | `[待填]` | `[待填]` | `[待填]` |

### 6.5 进入写稿前的最后检查

- [ ] 最终模型与模块去留已冻结
- [ ] 所有需止损对象已填入最终动作
- [ ] 中文起步状态已定级
- [ ] 英文起步状态已定级
- [ ] `project_status` 与 `major_blockers` 已与总状态文档对齐
- [ ] 主结果表、消融表、第一批外部对比表、`CRAG` 表和图像资产已可直接调用
- [ ] reproduced / † / *、公平性边界和 `CRAG` 角色已可直接引用
- [ ] 主 `3-seed` 结论与 supplementary `additional_reporting` 边界已可直接引用
- [ ] 不再依赖补关键实验才能写正文

只要上面任一项未完成，就不得把本文件填写为允许进入写稿。

---

## 7. 证据映射与后填规则

### 7.1 证据映射表

| 检查项 | 当前状态 | 证据来源 | 备注 |
|--------|----------|----------|------|
| 阶段矩阵是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 止损动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 中文起步是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 英文起步是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 总状态边界是否一致 | `[待填]` | `[待填]` | `[待填]` |
| 写稿进入是否允许 | `[待填]` | `[待填]` | `[待填]` |
| 首选轨道是否唯一 | `[待填]` | `[待填]` | `[待填]` |
| 剩余小缺口是否非关键 | `[待填]` | `[待填]` | `[待填]` |

### 7.2 现在就要冻结的部分

当前阶段必须先固定下面这些框架：

- 写稿进入布尔结论及其允许值。
- 四档轨道允许值。
- 汇总判断表结构。
- 最后检查项结构。
- 证据映射表结构。
- 与总状态、止损、中英文起步之间的字段联动关系。

### 7.3 必须等真实收口后再回填的部分

下面这些内容必须等阶段矩阵、止损、中英文起步、结果包和项目总状态真实收口后再填写：

- `writing_entry_allowed`
- `preferred_track`
- `remaining_minor_gaps`
- `entry_reason`
- 汇总判断表中的真实状态、来源和备注
- 证据映射表中的真实状态、来源和备注

如果当前仍缺关键阶段过线、关键止损动作、关键中英文边界、关键结果包资产或关键总状态一致性，本文件不能提前写成正向写稿进入。

---

## 8. 代码实现约束、最低交付物与 handoff 资产

### 8.1 本文件必须复用或对齐

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`

### 8.2 本文件禁止修改

- 任何阶段已冻结的实验事实、模型身份和主评估口径。
- retain / downgrade / remove / rollback 的动作本体。
- 中文、英文和项目总状态档位本体。
- `package_status`、正式表格、正式图像资产和来源标记规则本体。
- cn_first / cn_first_then_en / en_direct / not_enter_yet 之外的新轨道。

### 8.3 最低交付物

本文件落地后，至少必须直接支撑下面五类交付物：

1. 写稿进入唯一布尔结论。
2. 写稿首选轨道唯一输出。
3. 写稿剩余小缺口清单。
4. 写稿进入正式理由。
5. 可供正式写稿阶段和复审阶段直接消费的写稿入口基线。

### 8.4 交接给下游消费对象的正式资产

本文件通过后，至少应交接下面这些资产：

- `writing_entry_allowed`
- `preferred_track`
- `remaining_minor_gaps`
- `entry_reason`
- 汇总判断表中的一致性来源
- 证据映射表中可追溯的来源说明

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件就必须先回退修正，而不是继续被下游消费：

- `writing_entry_allowed = true`，但仍依赖补关键实验、补关键止损或补关键结果资产。
- `preferred_track` 已填写，但与 cn_entry_readiness.md 或 en_entry_readiness.md 的正式裁决互相打架。
- `remaining_minor_gaps` 中混入关键实验、关键公平性说明、关键对象动作或关键资产缺失。
- 本文件写成允许进入写稿，但 final_readiness_judgement.md 的 `project_status` 或 `major_blockers` 仍显示存在硬阻塞。
- 本文件比 stop_loss_decision.md 更乐观地保留了已被删除、回退或要求降调的对象或 claim。
- 汇总判断表、证据映射表与正文字段互相打架，导致写稿进入无法唯一解释。
- seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 已进入结果资产，但当前文件仍没有写清主 `3-seed` 与 supplementary `additional_reporting` 的写稿入口边界。

### 9.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查 stage_gate_matrix.md 与 01_阶段门槛总表.md，确认是否仍有关键阶段未过线或仍依赖补关键实验。
2. 再检查 stop_loss_decision.md，确认是否仍有关键对象动作未定、需回退或需降调。
3. 再检查 cn_entry_readiness.md 与 en_entry_readiness.md，确认中英文是否仍存在关键阻塞。
4. 再检查 final_readiness_judgement.md，确认项目总状态、缺失资产和关键阻塞项是否允许写稿进入。
5. 最后才允许重新填写当前文件字段、汇总判断表和证据映射表。

### 9.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已回写到当前文件字段区、汇总判断区或证据映射区。
- 当前文件重新与 stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、final_readiness_judgement.md 完全对齐。
- 当前文件重新满足第 `5` 节规则卡片、第 `6` 节轨道裁决要求和第 `8` 节交接资产要求。

---

## 10. 代码落地接口

### 10.1 写稿进入裁决入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- 入口类/函数：固定字段区、轨道裁决区、汇总判断区
- 输入：阶段矩阵、止损动作、中英文起步结论、结果包状态和总状态约束
- 输出：`writing_entry_allowed`, `preferred_track`, `remaining_minor_gaps`, `entry_reason`
- `dtype`：进入字段为 `bool`；轨道字段与说明字段为 `string`
- 依赖配置：`stage_pass`, `action`, `cn_ready`, `en_ready`, `tone_down_required`, `project_status`, `package_status`, `seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 前置断言：若仍有关键阶段未过线、关键止损未定、关键总状态阻塞、关键写稿边界未定，或主 `3-seed` 与 supplementary `additional_reporting` 的入口边界未写清，不得把进入结论填成 `true`
- 运行产物：写稿进入正式裁决与轨道回填结果

### 10.2 中英文轨道联动入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`、en_entry_readiness.md
- 入口类/函数：轨道判断区与进入理由区
- 输入：`cn_ready`, `cn_blockers`, `en_ready`, `tone_down_required`, `en_blockers`, `entry_reason`
- 输出：`preferred_track`, `remaining_minor_gaps`, `entry_reason`
- `dtype`：全部为 `string`
- 依赖配置：`cn_ready`, `en_ready`, `tone_down_required`, `action`, `package_status`
- 前置断言：若中文或英文任一侧仍存在硬阻塞，不得把对应轨道写成稳定放行
- 运行产物：中文优先、双轨衔接或英文直写的正式联动依据

### 10.3 总状态互校入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 入口类/函数：总状态说明区、阻塞项区、一致性校验区
- 输入：`project_status`, `status_reason`, `missing_assets`, `major_blockers`, `final_stage_pass`
- 输出：`writing_entry_allowed`, `preferred_track`, `entry_reason`
- `dtype`：布尔字段为 `bool`；说明字段为 `string`
- 依赖配置：`project_status`, `final_stage_pass`, `major_blockers`, `remaining_minor_gaps`
- 前置断言：若总状态仍为 `Not pass` 或仍存在硬阻塞，不得把当前文件写成稳定进入写稿
- 运行产物：写稿入口与项目总状态之间的一致性说明

---

## 11. 冲突裁决记录

- 冲突对象：旧版 writing_entry_decision.md 的结构强度、写稿进入语义、上游链路留痕、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版收尾闭环。
- 冲突来源：旧稿虽然保留了四个字段、四档轨道、汇总判断表和最后检查项，但整体仍停留在“写稿进入待填模板”层，缺少与同层强模板一致的前置依赖留痕、差异化 上游 / 同层 / 下游、`writing_entry_fixed` 承接、总状态互校边界、独立回退边界和下游消费语义。
- 裁决结论：本轮将当前文件升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 阶段定位与核心结论 -> 当前文件唯一合法输入、输出与判定流程 -> 规则卡片 -> 固定字段与轨道裁决 -> 证据映射与后填规则 -> 代码实现约束与 handoff 资产 -> 回退条件 -> 代码落地接口 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的正式执行层结构。
- 裁决理由：如果继续保留旧结构，总验收链会出现“止损、中英文和总状态都已强化，但写稿进入仍只是待填表”的断层，下游写稿阶段仍不得不重新主观解释是否已经可以开写。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`、final_readiness_judgement.md、正式中文写稿阶段、正式英文写稿阶段
- 是否需要回流修订：需要；后续任何写稿启动、总状态复核或结果包说明，都必须直接读取本文件冻结的进入结论和轨道，而不是重新主观组织。
- 代码实现影响：影响写稿启动时机、双语轨道选择、总状态与写稿进入的一致性口径。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文
- [x] 已继续补读 `02_路线与投稿`、文献锚点、stage_gate_matrix.md、stop_loss_decision.md、cn_entry_readiness.md、en_entry_readiness.md、final_readiness_judgement.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md` 和同层协议文件，而不是停在总览层
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明为什么这些文件与写稿进入执行层直接相关
- [x] 已完成与 stop_loss_decision.md、final_readiness_judgement.md、en_entry_readiness.md 的模板强度对照，确认当前文件不再弱于同批强模板
- [x] 当前版本按整篇重写执行，不是对旧稿追加少量字段说明
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担写稿进入执行层职责
- [x] 已写清当前文件与 `Gate_11`、`writing_entry_fixed` 和总状态互校链的关系，没有把它写成脱离母协议的孤立模板
- [x] 已把进入唯一输出、不得依赖补关键实验、轨道选择、小缺口边界和总状态互校写成正式规则卡片
- [x] 每条核心规则都保留了 当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式
- [x] 已保留并强化原文件核心四字段、四档轨道、汇总判断表和最后检查项，没有在升级结构时丢失原始实用内容
- [x] 已把 `writing_entry_allowed`、`preferred_track`、`remaining_minor_gaps`、`entry_reason` 扩成可被下游直接消费的正式字段链，而不是只留字段名
- [x] 已把 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 接到写稿进入层，并明确主 `3-seed` 才是正文主入口依据，additional reporting 只能进入 supplementary / rebuttal 级附加材料
- [x] 已写清独立 `回退条件`，没有把回退要求藏在轨道解释或总结句里顺带带过
- [x] 已写清 `代码落地接口`，接口对象细化到写稿进入裁决、中英文轨道联动和总状态互校三条主链
- [x] 已补写 `冲突裁决记录`，说明旧结构与同层强模板如何统一、影响哪些文件以及后续如何回流修订
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、字段链、规则卡片、轨道裁决、回退、接口和收尾闭环
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”
- [x] 当前文件在落盘后继续执行回读与 diagnostics 复核，正文写作不会替代闭环动作
- [x] 当前文件已经达到“可直接指导写稿进入结果回填并支撑双语轨道选择”的最低强度

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成
- 复核范围：至少覆盖标题层级、列表结构、字段命名一致性、上游 / 同层 / 下游 显式落点、`Gate_11 / writing_entry_fixed` 公式书写、四档轨道命名、汇总判断表列名、最后检查项，以及是否存在可见 markdown 诊断问题
- 复核范围补充：额外检查 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 是否与主 `3-seed` 写稿入口边界、supplementary `additional_reporting` 边界和 `remaining_minor_gaps` 写法一致
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核
- 对照要求：本节保持与 stop_loss_decision.md、final_readiness_judgement.md、en_entry_readiness.md 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话

---

## 14. 一句话版本

> 本文件的正式职责已经固定为：把阶段矩阵、对象级止损、中英文起步、结果包边界和项目总状态约束一次压成唯一写稿进入结论，并把首选轨道、剩余小缺口和进入理由一起交接给正式写稿阶段；凡是仍依赖补关键实验、仍和止损或总状态打架、仍缺关键资产或仍无法唯一说明先写哪条轨道的状态，都不得在这里被写成允许进入写稿。
