# EN Entry Readiness

本文件不是英文写稿备忘录，也不是把 04_英文起步条件.md 简单抄一遍的轻量模板。

它在 `11_总验收与止损` 阶段中的唯一职责是：

> 把上游已经冻结的英文起步规则、阶段门槛、止损动作、正式结果包、公平性边界、task-specific direct comparison、`CRAG` 结论强度和写作降调边界，正式压成可被下游直接消费的英文起步裁决输出；后续 writing_entry_decision.md 与 final_readiness_judgement.md 只能读取本文件已经填写的英文档位、是否必须降调、缺失资产、阻塞项、已删除主张、已降调主张和进入理由，不允许再绕过本文件另行主观改判。

这里的 `EN Entry Readiness` 不是重新定义英文规则，而是把 04_英文起步条件.md 的冻结细则落成真正可填写、可回查、可交接的英文执行层。它关心的是：当前项目到底能不能开始英文写稿，要不要严格降调，缺什么，卡在哪里，哪些 claim 已经不能保留，以及这些判断分别由哪份正式证据支撑。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面八件事：

1. 英文稿起步状态只允许填写为 可以起步 / 可以起步但需严格降调 / 暂不建议起步 三档之一的唯一输出值。
2. 面向下游固定输出 `en_ready`、`en_ready_reason`、`tone_down_required`、`en_missing_assets`、`en_blockers`、`removed_claims`、`downgraded_claims`、`entry_reason` 的字段边界。
3. 把 04_英文起步条件.md 的英文三档、硬门槛、公平性边界、claim 边界和章节最低可写要求，映射成可直接回填的检查表、判定规则和证据映射表。
4. 把 01_阶段门槛总表.md 的阶段状态、02_止损与回退规则.md 的动作边界、`10_结果汇总` 的正式资产，收束成英文起步的唯一判断入口。
5. 明确哪些缺口仍属于 `可以起步但需严格降调` 的可控缺口，哪些缺口必须把结论打回 `暂不建议起步`。
6. 把英文裁决结果正式交接给 writing_entry_decision.md 与 final_readiness_judgement.md，避免下游重复解释英文状态。
7. 写清独立 `回退条件`、固定回退顺序和重新放行条件，防止英文写稿带着不公平横比、过强 claim 或未收口资产进入下游总裁决。
8. 保留本文件自己的 `代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- 英文三档状态本体、公平性边界和英文最低可写条件本体；这些以 04_英文起步条件.md 为准。
- Pass / Pass with gaps / Not pass 的项目总状态本体；这些以 final_readiness_judgement.md 为准。
- 中文保底与中文写稿边界本体；这些以 03_中文保底条件.md 为准。
- 模块级 retain / downgrade / remove / rollback 动作本体；这些以 02_止损与回退规则.md 为准。
- 正式结果包、表格、图像和 `package_status` 本体；这些以 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md` 为准。
- 论文正文表述、语言润色和章节写作风格本体；当前文件只回答“能不能起稿，以及依据是什么”。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/04_英文起步条件.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/03_中文保底条件.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`

### 1.3 为什么当前文件必须独立存在

如果只有 04_英文起步条件.md 而没有当前文件，总验收阶段很容易出现下面这些伪完成状态：

- 英文规则已经写清，但没有真正把唯一档位填出来。
- 主线和结果包大体齐了，就口头认为“英文可以先写”。
- `tone_down_required`、`removed_claims`、`downgraded_claims` 和 `entry_reason` 没有正式落盘，下游只剩模糊印象。
- writing_entry_decision.md 与 final_readiness_judgement.md 需要英文状态时，只能重新人工解释而不是读取正式输出。

因此，当前文件必须独立承担“把英文起步规则变成正式裁决产物”的职责。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件整篇升级为正式裁决文档，而不是保留旧版“字段 + 检查表 + 一句话”的轻量结构。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把英文起步判断写成能被下游交接消费的正式对象，而不是摘要性说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 benchmark、split、阈值、后处理和种子等冻结边界，是当前文件不能擅自改口径的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：提供 `result_source_type`、来源追溯和字段命名要求，是证据映射区与来源边界区的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束对象级主指标、`best_selector = val_objdice_max`、`GlaS threshold_source = val17`、`CRAG threshold_source = val20`，是英文实验可落笔性判断的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把判断规则映射成字段链、输入资产和交接对象，而不是停在自然语言总结。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求显式写出 `本轮重写直接依赖的前置文件`、`代码落地接口`、`冲突裁决记录` 和完整收尾闭环。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求差异化 上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环` 不得缩水。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线推进顺序，要求英文起步只消费已冻结主线，而不是边写边回头改实验叙事。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：要求前序阶段不过线不得进入后续写稿判断，是当前文件必须依赖阶段矩阵的直接依据。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求英文起步服从止损与投稿层级边界，是当前文件不能把英文起稿写成“先写再说”的直接依据。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS` benchmark、对象级三指标和 TestA / TestB 分开报告要求，是英文 experiments 判断是否可落笔的直接依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供 `GlaS + CRAG` 双 benchmark 语境，是当前文件判定 `CRAG` 只能作为补充验证或有限增信的关键锚点。
- `结直肠腺体分割_plan_优化版/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md`：提供 `problem-aware metric selection`，要求英文实验不能只靠单一像素指标判断“可写”。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_GlaS_CRAG_主结果数值速查表.md` 与 06_我们项目的GlaS_CRAG对照主结果表模板.md：提供主结果表和来源标记消费语境，是证据映射区、缺失资产区和公平性区的直接支撑。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/04_英文起步条件.md`：冻结英文三档、公平性边界、claim 强度和下游字段链，是当前文件最直接的规则上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`：提供 `stage_pass` 与 `stage11_pass` 逻辑，是英文状态不能脱离阶段真实通过线单独成立的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`：提供 retain / downgrade / remove / rollback 动作边界，是 `removed_claims`、`downgraded_claims` 和英文降调边界的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：冻结主表、消融表、外部对比表、task-specific direct comparison、`CRAG` 表、图像资产和 `package_status`，是当前文件判断缺失资产和阻塞项的最直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：提供 `Gate_11` 母协议，是当前文件进入总验收裁决链的直接上游。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：负责 `11` 阶段母协议；当前文件是英文起步的实际输出层。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/04_英文起步条件.md`：负责英文规则冻结；当前文件负责把规则落成填写结果。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/03_中文保底条件.md`：负责中文规则冻结；当前文件需要与其保持起步粒度、字段链强度和收尾强度的一致性。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`：负责动作裁决；当前文件消费它防止英文输出与止损结论冲突。

#### 同批模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- 邻接强模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/04_英文起步条件.md`
- 同层细则模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`

本轮对照后的固定结论是：

- 当前文件必须升级到与 cn_entry_readiness.md 和 04_英文起步条件.md 同等级的前部结构与收尾强度，不能继续停留在待填模板。
- 当前文件必须显式写出 `本轮重写直接依赖的前置文件`、差异化 上游 / 同层 / 下游、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。
- 当前文件虽然以字段输出为核心，但强度不得弱于同层规则文件，否则英文链路会出现“规则强、执行弱、交接弱”的断层。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`：直接消费 `en_ready`、`tone_down_required`、`entry_reason`、缺失资产和阻塞项，决定能否进入写稿与首选轨道。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`：间接消费英文状态、阻塞项和缺失资产，作为总状态判断的一部分。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/03_中文保底条件.md` 与 cn_entry_readiness.md：需要与当前文件保持中英文裁决粒度和写稿联动的一致性，避免中文和英文执行层强度不对称。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

本文件真正要证明的，不是“现在看起来差不多能写英文”，而是：

> 在阶段门槛、止损动作、主线冻结、正式结果包、task-specific direct comparison、图像资产、来源边界、公平横比边界、`CRAG` 角色和英文章节可落笔性都已经由上游压实后，当前项目可以被正式写成一个唯一英文状态，并伴随正式理由、降调要求、缺失资产、阻塞项、已删除主张、已降调主张和进入理由，不再留下“靠口头理解继续推进”的灰区。

因此，本文件通过的含义同时包括：

- 英文状态已经从规则层落成结果层。
- 结果层输出已经足以直接交给写稿进入裁决。
- 当前文件可以解释为什么能写、为什么只能严格降调写，或为什么暂时不能写。
- 当前文件可以明确指出哪些 claim 被删、哪些 claim 被降调，而不是让下游自己猜。

### 3.2 当前文件与 `Gate_11`、`Gate_EN` 的关系

本文件不重新定义 `Gate_11` 与 `Gate_EN`，但它是两者落地到英文裁决输出的正式承接层：

```text
Gate_11 = stage_matrix_ready
          AND project_status_fixed
          AND stop_loss_fixed
          AND cn_ready_fixed
          AND en_ready_fixed
          AND writing_entry_fixed
```

```text
Gate_EN = en_state_fixed
          AND en_asset_boundary_fixed
          AND en_claim_boundary_fixed
          AND en_rollback_boundary_fixed
          AND en_downstream_schema_fixed
```

当前文件真正负责消费并落盘的是：

```text
en_entry_output_ready = en_ready
                        + en_ready_reason
                        + tone_down_required
                        + en_missing_assets
                        + en_blockers
                        + removed_claims
                        + downgraded_claims
                        + entry_reason
```

只有当上游 `en_ready_fixed` 已经成立，且当前文件把上述输出字段真实填成可交接资产时，英文链路才算真正闭环。

### 3.3 当前文件不允许用什么替代正式裁决

当前明确不允许把下面这些情况当成“英文起步已完成”：

- 只有检查表，没有最终字段输出。
- 只有英文档位，没有 `en_ready_reason`、`tone_down_required`、`en_missing_assets` 和 `en_blockers`。
- 只有“可以起步”结论，没有 `removed_claims` 与 `downgraded_claims`。
- 只有上游规则复述，没有证据映射和交接对象。
- 只有口头说法“先写英文再降调”，但没有把降调要求和缺口写进正式字段。

---

## 4. 阶段门控表达式

### 4.1 当前文件唯一合法输入

本文件不制造新的实验事实，只消费已经冻结的正式资产：

```text
en_entry_inputs = stage_gate_matrix
                + stop_loss_actions
                + result_package_assets
                + direct_comparison_assets
                + figure_assets
                + source_boundary_assets
                + claim_tone_down_evidence
```

其中关键来源固定为：

- `stage_gate_matrix`：各阶段 threshold_passed / handoff_assets_ready / next_stage_ready / stage_pass 以及 `stage11_pass`。
- `stop_loss_actions`：模块层、外部对比层、`CRAG` 层和写作层的 retain / downgrade / remove / rollback 结论。
- `result_package_assets`：`GlaS` 主结果表、主线消融表、第一批外部对比表、task-specific direct comparison、`CRAG` 表、summary、`package_status`，以及 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 的正式记录边界。
- `direct_comparison_assets`：gland-specific 对照是否可公平直比、哪些只能引用对照、哪些必须显式来源标记。
- `figure_assets`：主线逐步对比图、边界局部放大图、失败案例图、`CRAG` 成功或失败图。
- `source_boundary_assets`：reproduced / † / *、表注边界、direct comparison 边界、`CRAG` 角色和局限性边界，以及主 `3-seed` 结论与 supplementary `additional_reporting` 的英文写作边界。
- `claim_tone_down_evidence`：标题、摘要、experiments 和 conclusion 中允许或禁止出现的结论强度及其理由。

### 4.2 当前文件固定输出字段

本文件至少必须填写下面字段：

- `en_ready = [待填]`
- `en_ready_reason = [待填]`
- `tone_down_required = [待填]`
- `en_missing_assets = [待填]`
- `en_blockers = [待填]`
- `removed_claims = [待填]`
- `downgraded_claims = [待填]`
- `entry_reason = [待填]`

填写规则如下：

- `en_ready` 只能填写 可以起步 / 可以起步但需严格降调 / 暂不建议起步 之一。
- `tone_down_required` 只能填写 true / false。
- `en_ready_reason` 必须直接说明为什么落到当前档位，不能只写“条件基本满足”。
- `en_missing_assets` 只写尚未补齐的真实资产，不能混入已经有但还想优化的项。
- `en_blockers` 只写真正阻止英文起稿的关键阻塞项。
- `removed_claims` 只写已经被止损规则判定删除的英文表述、模块贡献或对照主张。
- `downgraded_claims` 只写仍可保留但必须降调的英文表述。
- `entry_reason` 必须可直接被 writing_entry_decision.md 消费，说明当前英文轨道为何可放行或不可放行。

### 4.3 当前文件固定判定顺序

本文件只允许按下面顺序裁决：

1. 先检查主线冻结是否已定。
2. 再检查正式结果表、task-specific direct comparison 和 `CRAG` 是否齐。
3. 再检查图像资产是否成套。
4. 再检查来源边界、表注边界和公平性边界是否清楚。
5. 最后检查标题、摘要、related work、method、experiments 和 conclusion 能否在不拔高的前提下直接落笔。

只要前一层未通过，就不允许越级给出正向英文判断。

---

## 5. 本文件核心规则卡片

### 5.1 英文档位输出规则

- 当前结论：本文件必须把英文状态输出为 可以起步 / 可以起步但需严格降调 / 暂不建议起步 三档之一。
- 规则类型：`写作进入规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：04_英文起步条件.md、00_阶段总协议.md
- 核心公式或定义参考：`en_ready in {ready_to_start, start_with_tone_down, not_ready}`
- 采用原因：下游写稿进入裁决只能消费唯一档位，不能再从检查表自行推断。
- 不采用的相邻方案：不采用“基本可写”；不采用“先写标题摘要”；不采用没有正式档位的 `pending`。
- 代码落点：当前文件字段区、writing_entry_decision.md
- 运行记录字段：`en_ready`, `en_ready_reason`, `entry_reason`
- 验收方式：检查英文状态是否被唯一填值，且理由能回溯到正式资产。

### 5.2 降调要求输出规则

- 当前结论：本文件必须同时输出 `tone_down_required`、`removed_claims` 和 `downgraded_claims`，不能只给英文档位。
- 规则类型：`止损联动规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：04_英文起步条件.md、02_止损与回退规则.md
- 核心公式或定义参考：`en_claim_boundary = tone_down_required + removed_claims + downgraded_claims`
- 采用原因：英文起步不只是判断能不能写，还要判断哪些 claim 不再能写、哪些只能降调写。
- 不采用的相邻方案：不采用“先按强版本写，后面再删”；不采用只在上游止损文件保留动作结论而当前文件不回填。
- 代码落点：当前文件字段区、writing_entry_decision.md, final_readiness_judgement.md
- 运行记录字段：`tone_down_required`, `removed_claims`, `downgraded_claims`, `entry_reason`
- 验收方式：检查英文输出是否与上游动作结论逐项一致。

### 5.3 结果包与对照资产输出规则

- 当前结论：本文件必须同时输出 `en_missing_assets` 与 `en_blockers`，并明确英文 experiments 依赖的对照资产是否齐备。
- 规则类型：`handoff 规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：04_英文起步条件.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- 核心公式或定义参考：`en_gap_output = missing_assets + blockers`
- 采用原因：下游需要知道哪些是可边补的小缺口，哪些是会阻止英文起步的硬阻塞。
- 不采用的相邻方案：不采用把所有缺口都塞进 `en_ready_reason`；不采用只写一句“还差一些图表和对照”。
- 代码落点：当前文件字段区、证据映射区、writing_entry_decision.md
- 运行记录字段：`en_missing_assets`, `en_blockers`, `entry_reason`
- 验收方式：检查缺失资产与阻塞项能否直接支持下游给出 `preferred_track`。

### 5.4 公平性与来源边界规则

- 当前结论：本文件必须保留正式证据映射表，明确每个英文判断来自哪里，并显式承接公平性边界与来源标记。
- 规则类型：`证据追溯规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`、04_英文起步条件.md
- 核心公式或定义参考：`judgement_trace = state + source + note`
- 采用原因：如果没有映射表，英文裁决只能停留在口头解释，无法回查公平性与来源边界是否真实成立。
- 不采用的相邻方案：不采用只在段落里笼统提“见上游文件”；不采用没有来源列的纯勾选清单。
- 代码落点：当前文件证据映射区
- 运行记录字段：`en_ready_reason`, `tone_down_required`, `en_missing_assets`, `en_blockers`
- 验收方式：检查关键判断是否都能落到表内对应来源。

### 5.5 下游交接规则

- 当前结论：本文件必须直接支撑 writing_entry_decision.md 与 final_readiness_judgement.md 的英文输入字段。
- 规则类型：`handoff 规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：writing_entry_decision.md、final_readiness_judgement.md
- 核心公式或定义参考：`en_handoff_ready = en_state + tone_down + gaps + blockers + claims + entry_reason`
- 采用原因：如果下游仍需重新解释英文状态，说明当前文件不是正式执行层。
- 不采用的相邻方案：不采用只写给人看的摘要版；不采用只有本文件自己能懂的临时表述。
- 代码落点：当前文件字段区、下游写稿判断区、总状态说明区
- 运行记录字段：`en_ready`, `tone_down_required`, `en_blockers`, `entry_reason`
- 验收方式：检查下游是否可以直接读取当前字段而无需补充解释。

### 5.6 主 `3-seed` 与补充 reporting 英文边界规则

- 当前结论：英文起步判断必须继续以冻结主协议 `seed_reporting_mode = fixed_3_seed_main` 为正文主结论依据；若已经存在 `additional_reporting，它只能作为 supplementary / rebuttal 级补充统计，不得覆盖英文主稿的主 3-seed` 结论，也不得被静默升级成英文可起步的新增硬门槛。
- 规则类型：`统计 reporting 边界规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：02_止损与回退规则.md、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`
- 核心公式或定义参考：`en_main_basis = fixed_3_seed_main`; `additional_reporting = supplementary_only`
- 采用原因：英文稿最容易把补充稳定性统计写成新的主证据，必须提前压住“主结论来自冻结 `3-seed`，补充 reporting 只服务 supplementary / rebuttal”的边界。
- 不采用的相邻方案：不采用“有额外 seed 就自动改写主结论”；不采用“没有 additional reporting 就不能起写英文”；不采用把主 `3-seed` 和 `3+n seed` 统计混成同一英文事实。
- 代码落点：当前文件公平性与来源边界区、英文可落笔性区、下游交接区
- 运行记录字段：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`, `en_ready_reason`, `tone_down_required`, `entry_reason`
- 验收方式：检查英文起步是否明确以主 `3-seed` 为依据；检查若存在 `additional_reporting`，其角色只被写成 supplementary / rebuttal 级补充；检查英文阻塞项没有把额外 seed 缺失写成新的硬阻塞。

---

## 6. 固定填写字段、检查表与状态裁决

### 6.1 固定填写字段

- `en_ready = [待填]`
- `en_ready_reason = [待填]`
- `tone_down_required = [待填]`
- `en_missing_assets = [待填]`
- `en_blockers = [待填]`
- `removed_claims = [待填]`
- `downgraded_claims = [待填]`
- `entry_reason = [待填]`

### 6.2 英文起步检查表

#### 主线冻结

- [ ] 正式 baseline 已冻结
- [ ] 正式最终模型已冻结
- [ ] 模块去留已冻结

#### 结果表与对照资产

- [ ] `GlaS` 主结果表已齐
- [ ] 主线消融表已齐
- [ ] 第一批外部对比表已齐
- [ ] task-specific direct comparison 已齐
- [ ] `CRAG` 结果表已齐

#### 图像资产

- [ ] 主线逐步对比图已齐
- [ ] 边界局部放大图已齐
- [ ] 失败案例图已齐
- [ ] `CRAG` 成功或失败图已齐

#### 公平性与来源边界

- [ ] reproduced / † / * 已写清
- [ ] 引用值与复现值未混写
- [ ] 不公平横比对象已降级或移出 direct comparison
- [ ] `CRAG` 角色和局限性边界已写清
- [ ] 主 `3-seed` 结论与 supplementary `additional_reporting` 边界已写清

#### 英文起稿可落笔性

- [ ] English title and abstract 可直接起稿
- [ ] English related work 可直接起稿
- [ ] English method 可直接起稿
- [ ] English experiments 可直接起稿
- [ ] English conclusion 可直接起稿

### 6.3 三档状态裁决

#### `可以起步`

只有同时满足下面条件，当前档位才允许填写为 `可以起步`：

- 检查表不存在关键缺项。
- `en_missing_assets` 只剩表注细化、轻量整理或少量表述微调工作。
- `en_blockers` 为空或只剩不影响主结论的小缺口。
- `tone_down_required = false` 或仅保留轻度措辞克制，不改变标题与摘要主骨架。
- `removed_claims` 与 `downgraded_claims` 已和止损结论完全对齐。
- `entry_reason` 可以直接说明英文已达到稳定起稿入口。

#### `可以起步但需严格降调`

只有满足下面条件，当前档位才允许填写为 `可以起步但需严格降调`：

- 主线结论、正式表格、task-specific direct comparison 和 `CRAG` 最低验证已固定。
- 仍存在少量非致命缺口，例如个别来源说明待整理、部分图像或表注仍待补齐、外部对比覆盖仍需克制表述。
- 这些缺口会进入 `en_missing_assets`，但不会改变英文稿主结构。
- `tone_down_required = true`，且标题、摘要、experiments 或 conclusion 必须显式降调。
- 若存在 `additional_reporting 尚未整理成 supplementary / rebuttal 资产，只能作为可补充缺口处理，前提是主 3-seed` 英文叙事已经独立成立。
- `en_blockers` 不包含最终模型未定、关键对照未定、关键公平性未定或 `CRAG` 角色冲突等硬阻塞。

#### `暂不建议起步`

下面任意一条成立，当前档位必须填写为 `暂不建议起步`：

- 最终模型仍未锁定。
- task-specific direct comparison 或 `CRAG` 尚未收口。
- 图像资产或来源边界仍存在明显缺口。
- 标题、摘要、experiments 或 conclusion 仍依赖放大单点结果、模糊来源或强泛化措辞。
- `removed_claims` 与 `downgraded_claims` 仍未回填，导致英文可写边界不清楚。
- 主 `3-seed` 与 supplementary `additional_reporting` 边界仍未写清，导致英文主结论来源不唯一。

---

## 7. 证据映射与后填规则

### 7.1 证据映射表

| 检查项 | 当前状态 | 证据来源 | 备注 |
|--------|----------|----------|------|
| 主线冻结 | `[待填]` | `[待填]` | `[待填]` |
| 主结果与对照资产 | `[待填]` | `[待填]` | `[待填]` |
| 图像资产 | `[待填]` | `[待填]` | `[待填]` |
| 公平性与来源边界 | `[待填]` | `[待填]` | `[待填]` |
| 英文可落笔性 | `[待填]` | `[待填]` | `[待填]` |
| 已删除主张 | `[待填]` | `[待填]` | `[待填]` |
| 已降调主张 | `[待填]` | `[待填]` | `[待填]` |

### 7.2 现在就要冻结的部分

当前阶段必须先固定下面这些框架：

- 英文档位允许值。
- 固定输出字段集合。
- 检查表结构。
- 三档裁决定义。
- 证据映射表结构。
- 与下游写稿判断的字段联动关系。

### 7.3 必须等真实收口后再回填的部分

下面这些内容必须等主线、外部对比、task-specific direct comparison、`CRAG`、结果包和止损结论真实收口后再填写：

- `en_ready`
- `en_ready_reason`
- `tone_down_required`
- `en_missing_assets`
- `en_blockers`
- `removed_claims`
- `downgraded_claims`
- `entry_reason`
- 检查表真实勾选状态
- 证据映射表中的真实状态、来源和备注

如果当前仍缺关键表、关键图、关键来源边界、关键公平性判断或关键动作结论，本文件不能提前写成英文正向起步。

---

## 8. 代码实现约束、最低交付物与 handoff 资产

### 8.1 本文件必须复用或对齐

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/04_英文起步条件.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`

### 8.2 本文件禁止修改

- 任何阶段已冻结的实验事实、模型身份和主评估口径。
- 英文三档本体、公平性边界和英文起步硬门槛本体。
- retain / downgrade / remove / rollback 的动作本体。
- reproduced / † / * 的来源标记规则本体。
- `package_status` 和结果包正式资产本体。

### 8.3 最低交付物

本文件落地后，至少必须直接支撑下面五类交付物：

1. 英文起步唯一档位。
2. 英文起步理由与是否严格降调。
3. 英文缺失资产清单。
4. 英文关键阻塞项清单。
5. 写稿进入阶段的英文进入理由。

### 8.4 交接给下游文档的正式资产

本文件通过后，至少应交接下面这些资产给下游裁决文档：

- `en_ready`
- `en_ready_reason`
- `tone_down_required`
- `en_missing_assets`
- `en_blockers`
- `removed_claims`
- `downgraded_claims`
- `entry_reason`
- 证据映射表中可追溯的来源说明

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件就必须先回退修正，而不是继续被下游消费：

- 英文档位已经填写，但 `en_ready_reason` 仍是抽象结论，无法回溯到正式资产。
- `tone_down_required`、`removed_claims` 或 `downgraded_claims` 与 02_止损与回退规则.md 的动作结论互相打架。
- `en_missing_assets` 与 `en_blockers` 混写，导致下游无法区分可补缺口和硬阻塞。
- 英文档位与 04_英文起步条件.md 的三档定义不一致。
- 英文输出与 `10_结果汇总` 的正式表格、图像、`package_status` 或公平性边界不一致。
- 当前文件想放行英文起稿，但标题、摘要、experiments 或 conclusion 仍依赖补关键实验或过强 claim。
- seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 已进入结果资产，但当前文件仍没有写清主 `3-seed` 与 supplementary `additional_reporting` 的英文引用边界。

### 9.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查 04_英文起步条件.md，确认三档定义、公平性边界和 claim 边界没有被误改。
2. 再检查 01_阶段门槛总表.md，确认阶段矩阵和 `stage11_pass` 是否真实成立。
3. 再检查 02_止损与回退规则.md，确认 `tone_down_required`、`removed_claims` 与 `downgraded_claims` 的来源。
4. 再检查 `10_结果汇总` 的正式表格、task-specific direct comparison、图像和 `package_status` 是否真正收口。
5. 最后才允许重新填写当前文件字段与证据映射表。

### 9.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已回写到当前文件字段区或证据映射区。
- 当前文件重新与 04_英文起步条件.md、writing_entry_decision.md 和 final_readiness_judgement.md 对齐。
- 当前文件重新满足第 `5` 节规则卡片、第 `6` 节裁决要求和第 `8` 节交接资产要求。

---

## 10. 代码落地接口

### 10.1 英文起步裁决入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- 入口类/函数：英文档位区、理由区、降调要求区、缺失资产区、阻塞项区和证据映射区
- 输入：阶段矩阵、止损动作、主结果表、外部对比表、task-specific direct comparison、`CRAG` 表、图像资产、来源标记、公平边界和章节可写性证据
- 输出：`en_ready`, `en_ready_reason`, `tone_down_required`, `en_missing_assets`, `en_blockers`, `removed_claims`, `downgraded_claims`, `entry_reason`
- `dtype`：档位字段为 `string`；降调字段为 `bool`；缺失资产、阻塞项和原因字段为 `string`
- 依赖配置：`stage_pass`, `action`, `package_status`, `result_source_type`, `conclusion_grade`, `seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 前置断言：若最终模型未定、止损未定、关键资产缺失、核心章节不可落笔，或主 `3-seed` 与 supplementary `additional_reporting` 的英文边界未写清，不得把英文档位填成正向状态
- 运行产物：英文起步正式裁决与证据回填结果

### 10.2 写稿进入联动入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- 入口类/函数：写稿轨道判断区与进入理由区
- 输入：`en_ready`, `en_ready_reason`, `tone_down_required`, `en_missing_assets`, `en_blockers`, `entry_reason`
- 输出：`writing_entry_allowed`, `preferred_track`, `remaining_minor_gaps`, `entry_reason`
- `dtype`：布尔字段为 `bool`；轨道字段与说明字段为 `string`
- 依赖配置：`cn_ready`, `en_ready`, `tone_down_required`, `project_status`, `action`
- 前置断言：若当前文件仍为 `暂不建议起步`，不得把英文轨道写成允许进入
- 运行产物：英文直接起写或延后起写的最终联动依据

### 10.3 总状态说明联动入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 入口类/函数：总状态说明区与缺失资产汇总区
- 输入：`en_ready`, `en_blockers`, `en_missing_assets`, `entry_reason`
- 输出：`status_reason`, `missing_assets`, `major_blockers`
- `dtype`：说明字段为 `string`
- 依赖配置：`en_ready`, `project_status`, `package_status`, `action`
- 前置断言：若英文仍依赖关键实验、关键公平性说明或关键 claim 降调未完成，不得把总状态写成可直接进入稳定英文写稿
- 运行产物：项目总状态中与英文可写性相关的正式说明

---

## 11. 冲突裁决记录

- 冲突对象：旧版 en_entry_readiness.md 的结构强度、交接语义、止损字段承接、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版收尾闭环。
- 冲突来源：旧稿虽然保留了英文三档、检查表和证据映射表，但整体仍停留在“待填模板”层，缺少和同层强模板一致的前置依赖留痕、上下游角色说明、字段链扩展、回退边界和下游交接语义。
- 裁决结论：本轮将当前文件升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 阶段定位与核心结论 -> 输入输出与判定流程 -> 规则卡片 -> 固定字段与状态裁决 -> 证据映射与后填规则 -> 代码实现约束与 handoff 资产 -> 回退条件 -> 代码落地接口 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的正式执行层结构。
- 裁决理由：如果继续保留旧结构，英文链路会出现“上游规则已强化，但执行层仍只是待填表”的断层，下游 writing_entry_decision.md 和 final_readiness_judgement.md 仍无法直接消费英文状态。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`、writing_entry_decision.md、final_readiness_judgement.md
- 是否需要回流修订：需要；后续重写下游文件时，必须直接读取本文件冻结的字段链，而不是重新主观组织英文状态。
- 代码实现影响：影响英文起步字段回填、写稿轨道判断和总状态中的英文阻塞项说明。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文
- [x] 已继续补读 `02_路线与投稿`、文献锚点、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`、01_阶段门槛总表.md、02_止损与回退规则.md、03_中文保底条件.md、04_英文起步条件.md 和直接下游文件，而不是停在总览层
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明为什么这些文件与英文执行层裁决直接相关
- [x] 已完成与 cn_entry_readiness.md、04_英文起步条件.md、01_阶段门槛总表.md 的模板强度对照，确认当前文件不再弱于同批强模板
- [x] 当前版本按整篇重写执行，不是对旧稿追加少量字段说明
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担英文执行层裁决职责
- [x] 已写清当前文件与 `Gate_11`、`Gate_EN` 和 `en_ready_fixed` 的关系，没有把它写成脱离母协议的孤立模板
- [x] 已把固定输出字段、降调要求、缺失资产、阻塞项、止损联动、证据追溯和下游交接写成正式规则卡片
- [x] 每条核心规则都保留了 当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式
- [x] 已保留并强化原文件核心三档定义、检查表、证据映射和一句话目标，没有在升级结构时丢失原始实用内容
- [x] 已补齐 `removed_claims`、`downgraded_claims` 和 `entry_reason`，避免当前文件只给出英文档位而不给出下游需要的正式字段链
- [x] 已把 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 接到英文起步层，并明确主 `3-seed` 是英文主稿唯一冻结依据，additional reporting 只作 supplementary / rebuttal 级补充统计
- [x] 已写清独立 `回退条件`，没有把回退要求藏在状态裁决或总结句里顺带带过
- [x] 已写清 `代码落地接口`，接口对象细化到英文裁决入口、写稿进入联动和总状态说明三条主链
- [x] 已补写 `冲突裁决记录`，说明旧结构与同层强模板如何统一、影响哪些文件以及后续如何回流修订
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、字段链、规则卡片、交接、回退、接口和收尾闭环
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”
- [x] 当前文件在落盘后继续执行回读与 diagnostics 复核，正文写作不会替代闭环动作
- [x] 当前文件已经达到“可直接指导英文起步结果回填并支撑写稿轨道判断”的最低强度

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成
- 复核范围：至少覆盖标题层级、列表结构、字段命名一致性、上游 / 同层 / 下游 显式落点、`Gate_11` 与 `Gate_EN` 公式书写、英文三档命名、字段扩展是否完整，以及是否存在可见 markdown 诊断问题
- 复核范围补充：额外检查 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 是否与英文主 `3-seed` 叙事边界、supplementary `additional_reporting` 边界和 `tone_down_required` 写法一致
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核
- 对照要求：本节保持与 cn_entry_readiness.md、04_英文起步条件.md、01_阶段门槛总表.md 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话

---

## 14. 一句话版本

> 本文件的正式职责已经固定为：把上游已经冻结的英文起步规则落成唯一英文起步结果，并把理由、是否严格降调、缺失资产、关键阻塞项、已删除主张、已降调主张和写稿进入理由一起交接给下游；凡是仍依赖补关键实验、仍和止损结论打架、仍缺关键表图、仍说不清来源边界或仍需要拔高 claim 的状态，都不得在这里被写成英文可正式起稿。
