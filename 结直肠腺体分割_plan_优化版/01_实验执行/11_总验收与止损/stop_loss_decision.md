# Stop Loss Decision

本文件不是把 02_止损与回退规则.md 再抄一遍的待填表，也不是“总状态要写时再临时决定哪些对象保留”的备忘录。

它在 `11_总验收与止损` 阶段中的唯一职责是：

> 把所有争议对象正式压成唯一、可追溯、可被下游直接消费的对象级止损动作执行层，逐项落盘 need_stop_loss / trigger_reason / action / evidence_source / notes，并进一步冻结 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 四个文件级输出；后续 final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md 和 writing_entry_decision.md 只能忠实继承本文件已经填写的动作结论，不允许再绕开本文件凭沉没成本、主观乐观或写稿压力重新改判。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面八件事：

1. 把所有争议对象统一压成 retain / downgrade / remove / rollback 四档之一的唯一动作，而不是继续保留“后面再看”的灰区。
2. 把 02_止损与回退规则.md 的统一触发公式和四档动作边界，落到模块层、外部对比层、`CRAG` 层、写作主张层和工程协议层的真实对象。
3. 面向下游固定输出 `target_name`、`target_type`、`need_stop_loss`、`trigger_reason`、`action`、`evidence_source`、`notes` 七字段，以及文件级 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 四字段。
4. 把 `stop_loss_fixed` 在当前文件中落成真实对象级动作闭环，而不是只保留规则层定义。
5. 明确哪些对象还能保留进正文主线或正式主表，哪些对象只能降到补充层、discussion、局限性说明，哪些对象必须彻底删除或直接回退。
6. 写清主 `3-seed` 冻结结论与 supplementary `additional_reporting` 在对象级止损层的边界，确保额外 seed 既不会覆盖主结论，也不会被误判成新的硬阻塞或强保留理由。
7. 写清当前文件与 `Gate_11`、项目总状态、中英文起步和写稿进入的联动边界，防止止损链和总裁决链脱节。
8. 写清独立 `回退条件`、固定回退顺序和重新放行条件，防止带着来源冲突、公平性冲突或协议分叉的对象进入总状态与写稿文档。
9. 保留本文件自己的 `代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- 止损触发公式和四档动作边界的规则本体；这些以 `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md` 为准。
- `01-10` 各阶段是否真正过线的底层判定；这些以 stage_gate_matrix.md 和 01_阶段门槛总表.md 为准。
- 项目总状态 Pass / Pass with gaps / Not pass 的唯一档位本体；这些以 final_readiness_judgement.md 为准。
- 中文保底、英文起步和写稿进入的档位本体；这些分别以 cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 为准。
- 各模型、外部方法、`CRAG` 实验、结果包和 benchmark 资产的实验事实本体；当前文件只消费它们的正式状态和证据边界。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

如果没有一份独立的对象级止损执行层，总验收阶段最容易出现下面这些伪完成状态：

- 规则层已经写了四档动作，但没有人把真实对象压成唯一动作。
- 模块已经跑过很多轮，于是默认应当保留进主线，但正式证据其实只在波动范围内。
- 外部方法已经接进主表，于是默认继续保留，但公平性边界、来源标记或协议一致性并没有正式写清。
- `CRAG` 已经跑完，于是默认可以写成跨 benchmark 稳定支撑，但真实强度可能只够补充验证甚至只能写局限性。
- 中文或英文准备开写，于是默认删减项、降调项和回退项可以后面再补。

因此，当前文件必须独立承担“把规则层压成对象级唯一动作底表”的职责。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件整篇升级为正式执行层，而不是继续保留对象列表模板。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把止损动作写成下游可消费对象，而不是停在抽象规则说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 benchmark、split、阈值来源、后处理、种子和版本冻结边界，是当前文件不能在总验收层临时放宽口径的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：提供 `run_name`、`result_source_type`、`aggregation`、版本字段和来源追溯要求，是 `evidence_source` 与对象级记录链的一致性依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`：补充冻结 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 的 run 级和 table 级 schema，是对象级止损层必须继续承接主 `3-seed` 与 supplementary reporting 边界的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束 `best_selector = val_objdice_max`、`GlaS threshold_source = val17`、`CRAG threshold_source = val20` 和对象级优先口径，是止损判断不能靠混合口径制造假收益的直接依据。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把止损判断写成字段链、对象映射和下游接口，而不是自然语言摘要。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求显式写出 `本轮重写直接依赖的前置文件`、`代码落地接口`、`冲突裁决记录` 和完整收尾闭环。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求差异化 上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环` 不得缩水。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线推进顺序，要求对象级止损必须覆盖模块、外部对比、`CRAG` 和写作边界，而不是只看某一个子域。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：要求前一阶段不过线不得进入后一阶段，是协议分叉对象必须 `rollback` 的直接路线依据。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求写稿强度服从真实证据和真实止损结论，是当前文件必须联动中文、英文和写稿进入边界的直接依据。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS` benchmark 边界、对象级三指标和 TestA / TestB 分开报告要求，是外部对比和模块止损不能依赖混合口径的直接依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供 `GlaS + CRAG` 双 benchmark 语境，是 `CRAG` 止损时必须压住角色和强度的关键文献锚点。
- `结直肠腺体分割_plan_优化版/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md`：提供 `problem-aware metric selection`，要求止损判断同时考虑对象级、边界级和案例级证据，而不是只看单个像素指标。
- `结直肠腺体分割_plan_优化版/03_文献证据/06_我们项目的GlaS_CRAG对照主结果表模板.md`：提供正式主表、联合表和来源标记消费语境，是外部层和 `CRAG` 层止损动作必须服务的正式表格边界。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`：提供统一触发公式、四档动作和回退边界，是当前文件最直接的规则上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`：提供哪些阶段真实过线、哪些阶段未过线和对应来源，是对象级动作能否放行或必须回退的直接状态上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`：提供阶段门槛、handoff 资产和下一阶段放行要求，是协议分叉、来源不清对象必须止损的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`：冻结外部方法主表准入、公平协议和来源标记，是外部对比对象动作的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`：冻结 `CRAG` 角色、A / B / C 强度和联合 handoff 资产，是 `CRAG` 与写作主张动作的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：冻结主表、消融、图像资产、summary 和 `package_status`，是总动作总结和写作边界的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`：冻结主 `3-seed` 与 supplementary reporting 的字段链，是当前文件判断“额外 reporting 是补充说明而非新动作触发器”的直接 schema 上游。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：负责 `Gate_11` 母协议；当前文件是其中的对象级止损执行层。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`：负责项目总状态唯一输出；当前文件提供其必须消费的止损动作和阻塞来源。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`：负责中文起步判定；当前文件提供其必须继承的保留项、降级项、删除项和回退项。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`：负责英文起步判定；当前文件提供其必须继承的降调项、删除项和 `CRAG` 强度边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`：负责最终写稿进入；当前文件提供其必须继承的剩余红线和对象级动作底表。

#### 同批模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- 邻接强模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- 同层输出模板：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`

本轮对照后的固定结论是：

- 当前文件必须升级到与 stage_gate_matrix.md、final_readiness_judgement.md 和 en_entry_readiness.md 同等级的前部结构与收尾强度，不能继续停留在轻量止损表模板层。
- 当前文件必须显式写出 `本轮重写直接依赖的前置文件`、差异化 上游 / 同层 / 下游、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。
- 当前文件虽然以对象级表格输出为核心，但强度不得弱于同层阶段矩阵与总状态执行层，否则总验收链会出现“规则层强、对象动作层弱”的断层。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`：直接消费 `stop_loss_needed`、关键对象动作和回退目标，决定项目总状态是否还能落到 `Pass` 或只能落到 Pass with gaps / Not pass。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`：直接消费哪些对象仍可保留入中文主线、哪些对象必须降级或删除，决定中文是否可直接开写。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`：直接消费哪些英文主张必须降调、哪些对象必须移出 headline claim，决定英文是否能起步以及是否必须严格降调。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`：综合消费止损动作、总状态和中英文起步边界，决定最终是否进入写稿以及首选轨道。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

本文件真正要证明的，不是“项目里大多数对象看起来都还能留”，而是：

> 所有争议对象都已经被压成唯一动作，不再存在待定项、口头保留项或沉没成本保留项；同时，这些动作已经强到足以直接支撑项目总状态、中英文起步和写稿进入，而不需要下游重新解释“这个对象到底还能不能讲”。

因此，本文件通过的含义同时包括：

- 每个争议对象都能被压成统一字段链，而不是继续保留各说各话的解释。
- `action` 已经从口头倾向变成唯一枚举值。
- `evidence_source` 可以指出真实文件、表格、图像资产或正式 summary，而不是只写“见上游”。
- `notes` 可以忠实解释影响范围、降级边界或删除原因，而不是把一切粉饰成“基本可保留”。
- 文件级 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 已经能被下游直接消费。

### 3.2 当前文件与 `Gate_11`、`stop_loss_fixed` 和下游总裁决的关系

本文件不重新定义 `Gate_11`，但它是其中止损子链的正式承接层：

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
stop_loss_fixed = all_contested_targets_classified
                  AND action_boundary_fixed
                  AND rollback_boundary_fixed
                  AND downstream_stop_loss_schema_fixed
```

```text
stop_loss_output_ready = target_rows
                         + stop_loss_needed
                         + rollback_target
                         + downgrade_target
                         + global_stop_loss_summary
```

这里必须明确区分：

- `stop_loss_fixed` 回答的是“当前止损执行层是否已经成文并可被下游消费”。
- `stop_loss_needed` 回答的是“当前项目是否至少存在一个对象需要执行降级、删除或回退动作”，它不是文件是否完成的同义词。

### 3.3 当前文件不允许用什么替代正式止损执行层

当前明确不允许把下面这些情况当成“止损裁决已完成”：

- 只有统一规则，没有对象级表格。
- 只有对象名和占位，没有唯一动作与证据来源。
- 只有“建议降调”这种口头结论，没有 retain / downgrade / remove / rollback 正式枚举。
- 只有总体印象“需要止损”，没有 `rollback_target`、`downgrade_target` 和 `global_stop_loss_summary`。
- 只有写稿层面的一句“注意保守措辞”，没有对象级删除、降级或回退边界。

---

## 4. 阶段门控表达式

### 4.1 当前文件唯一合法输入

本文件不制造新的实验事实，只消费已经冻结的正式资产：

```text
stop_loss_inputs = stage_gate_matrix
                   + module_results
                   + external_comparison_assets
                   + crag_handoff_assets
                   + result_package_assets
                   + writing_readiness_constraints
                   + seed_reporting_assets
```

其中关键来源固定为：

- `stage_gate_matrix`：`01-10` 的 threshold_passed / handoff_assets_ready / next_stage_ready / stage_pass 与阶段缺口说明。
- `module_results`：`LKMA`、`Boundary Head`、`Distance-aware Loss` 的正式结果、案例证据和阶段 summary。
- `external_comparison_assets`：首批外部主表、来源标记、公平协议和 direct comparison 边界。
- `crag_handoff_assets`：`CRAG` 主表、图像资产、联合表输入和 A / B / C 结论强度。
- `result_package_assets`：`10_结果汇总` 的主表、消融表、失败案例图、summary、`package_status`，以及 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 的正式交接记录。
- `writing_readiness_constraints`：中文保底、英文起步和写稿进入所依赖的正式表述边界与阻塞项。
- `seed_reporting_assets`：seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 的正式 run 级和 table 级记录，以及主 `3-seed` 与 supplementary reporting 的消费边界。

### 4.2 当前文件固定输出字段

本文件至少必须填写下面字段：

- `stop_loss_needed = [待填]`
- `rollback_target = [待填]`
- `downgrade_target = [待填]`
- `global_stop_loss_summary = [待填]`
- `eval_cast_policy = [待填]`
- `boundary_metric_width = [待填]`
- `boundary_metric_impl = [待填]`
- `connected_components_impl = [待填]`
- `connected_components_connectivity = [待填]`
- 所有对象的 `target_name = [待填]`
- 所有对象的 `target_type = [待填]`
- 所有对象的 `need_stop_loss = [待填]`
- 所有对象的 `trigger_reason = [待填]`
- 所有对象的 `action = [待填]`
- 所有对象的 `evidence_source = [待填]`
- 所有对象的 `notes = [待填]`
- `seed_reporting_mode = [待填]`
- `main_seed_set = [待填]`
- `additional_seed_set = [待填]`
- `combined_seed_count = [待填]`

填写规则如下：

- `stop_loss_needed` 只能填写 true / false。
- `rollback_target` 只列必须回退到上一冻结版本的对象，不写一般性待优化项。
- `downgrade_target` 只列必须降到补充层、discussion、局限性说明或弱表述层的对象。
- `global_stop_loss_summary` 必须直接说明哪些对象保留、哪些对象降级、哪些对象删除、哪些对象回退，以及它们如何影响总状态和写稿边界。
- `eval_cast_policy` 必须显式写成 logits/probabilities must be kept or cast to float32 before thresholding，不允许只缩写成“沿用 `eval_proto_v1`”。
- `boundary_metric_width` 必须显式写成 `3 px`，不允许只写“沿用边界主版本宽度”。
- `boundary_metric_impl` 必须显式写成 `skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`，不允许只写“沿用正式边界评估实现”。
- `connected_components_impl` 必须显式写成 `scipy.ndimage.label`。
- `connected_components_connectivity` 必须显式写成 `8` 或 `二维 8-connectivity`，不允许只写“沿用对象级协议”。
- `need_stop_loss` 只能填写 true / false。
- `action` 只允许填写 retain / downgrade / remove / rollback。
- `evidence_source` 必须写明确文件、表格、图像资产、summary 或正式来源链，不允许写成“见上游”。
- `notes` 只写当前对象的缺口、影响范围和下游消费说明，不写空泛总结。
- `seed_reporting_mode` 只允许记录 `fixed_3_seed_main + optional_additional_reporting` 的正式状态，不得把额外 seed 直接升级成 `retain` 证据或新的止损触发器。
- main_seed_set / additional_seed_set / combined_seed_count 只用于说明统计 reporting 边界和下游消费范围，不单独决定对象动作。

### 4.3 当前文件固定判定顺序

本文件只允许按下面顺序裁决：

1. 先检查 stage_gate_matrix.md 与 01_阶段门槛总表.md，确认对象所依附的阶段与结果是否真的成立。
2. 再检查 02_止损与回退规则.md，确认是否触发统一止损公式以及唯一动作边界。
3. 再检查对象对应的正式表格、图像资产、summary、来源标记和公平协议。
4. 再检查该对象会如何影响 final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md 和 writing_entry_decision.md。
5. 最后才填写对象级 `action`、文件级 `stop_loss_needed`、`rollback_target`、`downgrade_target` 与 `global_stop_loss_summary`。

只要前一层未通过，就不允许越级给出正向保留动作。

---

## 5. 本文件核心规则卡片

### 5.1 对象级统一触发规则

- 当前结论：只要收益接近波动范围、跨 benchmark 不稳、来源不清、公平性不清或协议已分叉，当前对象就必须进入正式止损判断。
- 规则类型：`止损执行规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- 核心公式或定义参考：`need_stop_loss = near_variance OR cross_benchmark_unstable OR source_unclear OR fairness_unclear OR protocol_diverged`
- 采用原因：总验收阶段不允许再用沉没成本、单次最好结果或“后面写稿再看”替代正式对象裁决。
- 不采用的相邻方案：不采用“先留着”；不采用“暂定保留”；不采用没有正式触发依据的口头建议。
- 代码落点：当前文件对象级止损表区
- 运行记录字段：`target_name`, `need_stop_loss`, `trigger_reason`, `evidence_source`
- 验收方式：检查每个争议对象都能明确回答是否触发止损，以及触发依据来自哪份正式资产。

### 5.2 四档动作唯一输出规则

- 当前结论：每个争议对象只能落到 retain / downgrade / remove / rollback 四档之一，不允许存在第五档。
- 规则类型：`动作枚举规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- 核心公式或定义参考：`action in {retain, downgrade, remove, rollback}`
- 采用原因：如果动作边界不唯一，下游总状态和写稿文档就会重新陷入口头协商。
- 不采用的相邻方案：不采用 `pending`；不采用“半保留半删除”；不采用“先主表后讨论”这种非枚举动作。
- 代码落点：当前文件对象级止损表区、总结字段区
- 运行记录字段：`action`, `rollback_target`, `downgrade_target`
- 验收方式：检查每个对象只有唯一动作，且文件级汇总能直接对应到对象行。

### 5.3 模块层止损规则

- 当前结论：`LKMA`、`Boundary Head`、`Distance-aware Loss` 只有在对象级、边界级、跨 seed 和跨 benchmark 证据真实成立时才允许保留为主线贡献。
- 规则类型：`模块执行规则`
- 适用阶段：`05_LKMA`、`06_Boundary`、`07_Distance` 的总验收收口
- 直接依据：对应阶段总协议、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- 核心公式或定义参考：`module_keep = stable_gain AND role_explainable AND evidence_traceable`
- 采用原因：模块是否保留必须服务最终结论，而不是因为设计看起来合理就默认继续留在主线。
- 不采用的相邻方案：不采用单 seed 局部最优；不采用只靠少量案例就写主要贡献。
- 代码落点：当前文件模块层止损表区
- 运行记录字段：`target_type=module`, `need_stop_loss`, `action`, `evidence_source`, `notes`
- 验收方式：检查每个模块都有正式保留、降级、删除或回退结论，且与阶段 summary 一致。

### 5.4 外部对比层止损规则

- 当前结论：外部方法只有在公平协议成立、来源标记清楚且确实增强任务内结论时，才允许保留在正式主表或主要叙述中。
- 规则类型：`外部对比执行规则`
- 适用阶段：`08_外部对比` 与总验收写稿前
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- 核心公式或定义参考：`external_keep = fairness_aligned AND source_clear AND contribution_nontrivial`
- 采用原因：外部对比最容易因为“已经接进来了”而被误保留，必须先把公平性和来源边界压死。
- 不采用的相邻方案：不采用协议差异大的横比；不采用来源不清或仅引用值冒充公平对比。
- 代码落点：当前文件外部对比层止损表区
- 运行记录字段：`target_type=external_baseline`, `trigger_reason`, `action`, `evidence_source`, `notes`
- 验收方式：检查每个外部方法都能明确回答是保留主表、降到 `†` / discussion、直接删除，还是因协议分叉而回退。

### 5.5 `CRAG` 与写作主张止损规则

- 当前结论：`CRAG` 只允许作为第二 benchmark 的补充验证层；若方向反转、强度不足或解释失真，`CRAG` 主张和相关中英文主张都必须同步降级甚至删除。
- 规则类型：`跨 benchmark 执行规则`
- 适用阶段：`09_CRAG验证` 与总验收写稿前
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`、04_英文起步条件.md
- 核心公式或定义参考：`crag_keep = direction_consistent AND grade_traceable AND claim_boundary_clear`
- 采用原因：`CRAG` 最容易被误写成主证据来源，必须在对象级止损层先压住角色与强度。
- 不采用的相邻方案：不采用“跑过就算泛化”；不采用方向反转时仍写跨数据集优势。
- 代码落点：当前文件 `CRAG` 与写作主张止损表区
- 运行记录字段：target_type=crag_claim / writing_claim, `action`, `notes`
- 验收方式：检查 `CRAG` 主张与中英文 headline claim 是否被同步压到正式强度边界。

### 5.6 协议分叉回退规则

- 当前结论：只要协议中途分叉、结果无法追溯、评估口径冲突或只对个别方法启用额外流程，就必须优先 `rollback` 到最后一个协议清楚的冻结版本。
- 规则类型：`工程回退规则`
- 适用阶段：总验收全过程
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- 核心公式或定义参考：`protocol_valid = source_traceable AND evaluation_aligned AND fairness_preserved`
- 采用原因：如果工程协议已破坏公平性，再多结果也不能直接进入正式主表和最终裁决。
- 不采用的相邻方案：不采用“后面补表注即可”；不采用把不公平结果继续留在主表里。
- 代码落点：当前文件协议与工程分叉回退表区
- 运行记录字段：`target_type=protocol_branch`, `need_stop_loss`, `action`, `evidence_source`, `notes`
- 验收方式：检查所有协议冲突对象都已明确回退目标和受影响资产，没有带病进入总裁决。

### 5.7 主 `3-seed` 与补充 reporting 止损边界规则

- 当前结论：对象级止损层必须继续以 `seed_reporting_mode = fixed_3_seed_main + optional_additional_reporting` 约束统计 reporting 的消费方式；主保留、降级、删除或回退动作只允许由冻结主 `3-seed` 结论和正式协议边界支撑，`additional_seed_set` 与 `combined_seed_count` 只能作为 supplementary / rebuttal 级补充说明，不得覆盖主结论，也不得被误判成新的硬阻塞或强保留理由。
- 规则类型：`统计 reporting 止损边界规则`
- 适用阶段：`11_总验收与止损`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`
- 核心公式或定义参考：`main_stop_loss_basis = fixed_3_seed_main`; `additional_reporting = supplementary_only`
- 采用原因：对象级止损层最容易在“额外 seed 更稳定”或“还没补额外 seed”这两端发生漂移，因此必须先封死“额外 reporting 覆盖主结论”和“额外 reporting 成为新阻塞”这两类错误动作来源。
- 不采用的相邻方案：不采用把 `3+n seed` 补充统计升级成新的 `retain` 理由；不采用把 supplementary reporting 缺失写成必须 `rollback` 的新理由；不采用把额外 reporting 混成对象级正式主证据。
- 代码落点：当前文件对象级止损表区、文件级汇总区、证据映射区
- 运行记录字段：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`, `trigger_reason`, `action`, `notes`
- 验收方式：检查对象动作是否仍以主 `3-seed` 结论和正式协议边界为主；检查 supplementary `additional_reporting` 只被写成附加说明而非新动作触发器

---

## 6. 固定填写字段、对象级止损表与结果解释

### 6.1 固定填写字段

- `stop_loss_needed = [待填]`
- `rollback_target = [待填]`
- `downgrade_target = [待填]`
- `global_stop_loss_summary = [待填]`
- `eval_cast_policy = [待填]`
- `boundary_metric_width = [待填]`
- `boundary_metric_impl = [待填]`
- `connected_components_impl = [待填]`
- `connected_components_connectivity = [待填]`
- `seed_reporting_mode = [待填]`
- `main_seed_set = [待填]`
- `additional_seed_set = [待填]`
- `combined_seed_count = [待填]`

### 6.2 固定字段填写要求

#### `stop_loss_needed`

- 当前填写：`[待填]`
- 固定定义：只要存在任一对象 `action in {downgrade, remove, rollback}`，或仍存在必须落盘的对象级止损动作，当前字段就应为 `true`。

#### `rollback_target`

- 当前填写：`[待填]`
- 填写要求：只列必须回退到上一冻结版本的对象，不写一般性待优化项。

#### `downgrade_target`

- 当前填写：`[待填]`
- 填写要求：只列必须降到补充层、discussion、局限性说明或弱表述层的对象。

#### `global_stop_loss_summary`

- 当前填写：`[待填]`
- 填写要求：必须直接说明哪些对象进入正文主线、哪些对象移出主线、哪些对象只能弱化叙述，以及这些动作怎样影响总状态与写稿边界。

### 6.3 主线模块止损表

| `target_name` | `target_type` | `need_stop_loss` | `trigger_reason` | `action` | `evidence_source` | `notes` |
|---------------|---------------|------------------|------------------|----------|-------------------|---------|
| `LKMA` | `module` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `Boundary Head` | `module` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `Distance-aware Loss` | `module` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |

### 6.4 外部对比层止损表

| `target_name` | `target_type` | `need_stop_loss` | `trigger_reason` | `action` | `evidence_source` | `notes` |
|---------------|---------------|------------------|------------------|----------|-------------------|---------|
| `UNet++` | `external_baseline` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `DeepLabV3+` | `external_baseline` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `Attention U-Net` | `external_baseline` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `Task-specific direct comparisons` | `task_specific_comparison` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |

### 6.5 `CRAG` 与写作主张止损表

| `target_name` | `target_type` | `need_stop_loss` | `trigger_reason` | `action` | `evidence_source` | `notes` |
|---------------|---------------|------------------|------------------|----------|-------------------|---------|
| `CRAG generalization claim` | `crag_claim` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `English headline claim` | `writing_claim` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `Chinese conclusion strength` | `writing_claim` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |

### 6.6 协议与工程分叉回退表

| `target_name` | `target_type` | `need_stop_loss` | `trigger_reason` | `action` | `evidence_source` | `notes` |
|---------------|---------------|------------------|------------------|----------|-------------------|---------|
| `training protocol branch` | `protocol_branch` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `evaluation protocol branch` | `protocol_branch` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |
| `post-processing mismatch` | `protocol_branch` | `[待填]` | `[待填]` | `[待填]` | `[待填]` | `[待填]` |

### 6.7 对象级结果解释规则

#### `retain`

只有当对象证据稳定、来源清楚、公平性成立且不会与下游总状态或写稿边界冲突时，才允许填写为 `retain`。

#### `downgrade`

当对象仍有局部参考价值，但不足以承担主表、headline claim 或主要贡献时，必须填写为 `downgrade`。

#### `remove`

当对象证据不支持正式保留，且继续保留只会制造误导时，必须填写为 `remove`。

#### `rollback`

当对象的协议、来源链、公平性或评估口径已失效时，必须优先填写为 `rollback`，而不是继续比较它的结果优劣。

---

## 7. 证据映射与后填规则

### 7.1 证据映射表

| 检查项 | 当前状态 | 证据来源 | 备注 |
|--------|----------|----------|------|
| 模块层动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 外部对比动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| `CRAG` 动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 写作主张动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| 协议回退动作是否闭环 | `[待填]` | `[待填]` | `[待填]` |
| `stop_loss_needed` | `[待填]` | `[待填]` | `[待填]` |
| `rollback_target` | `[待填]` | `[待填]` | `[待填]` |
| `downgrade_target` | `[待填]` | `[待填]` | `[待填]` |
| `global_stop_loss_summary` | `[待填]` | `[待填]` | `[待填]` |

### 7.2 现在就要冻结的部分

当前阶段必须先固定下面这些框架：

- 对象级字段集合。
- 四档动作枚举和填写边界。
- 对象分层表结构。
- 文件级四个输出字段语义。
- 主 `3-seed` 与 supplementary reporting 的对象级消费边界。
- 证据映射表结构。
- 与总状态、中英文起步和写稿进入的消费关系。

### 7.3 必须等真实收口后再回填的部分

下面这些内容必须等真实结果、来源链和写作边界收口后再填写：

- 每个对象的 `need_stop_loss`
- 每个对象的 `trigger_reason`
- 每个对象的 `action`
- 每个对象的 `evidence_source`
- 每个对象的 `notes`
- `stop_loss_needed`
- `rollback_target`
- `downgrade_target`
- `global_stop_loss_summary`
- `seed_reporting_mode`
- `main_seed_set`
- `additional_seed_set`
- `combined_seed_count`
- 证据映射表中的真实状态、来源和备注

如果某个对象还没有正式证据或仍有协议冲突，这里只能保留占位或写明未放行原因，不允许提前给出正向保留结论。

---

## 8. 代码实现约束、最低交付物与 handoff 资产

### 8.1 本文件必须复用或对齐

- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/02_止损与回退规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stage_gate_matrix.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/cn_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/en_entry_readiness.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`

### 8.2 本文件禁止修改

- 任何上游已冻结的实验事实、benchmark 身份、split 和阈值来源。
- retain / downgrade / remove / rollback 之外的新动作档位。
- 项目总状态、中英文起步和写稿进入的档位本体。
- 正式结果包、来源标记和 `package_status` 的本体定义。

### 8.3 最低交付物

本文件落地后，至少必须直接支撑下面五类交付物：

1. 全项目争议对象止损清单。
2. 每个对象唯一的四档动作裁决。
3. 文件级 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary`。
4. 可回查的对象级证据来源清单。
5. 面向总状态、中英文起步和写稿进入的正式止损底表。

### 8.4 交接给下游消费对象的正式资产

本文件通过后，至少应交接下面这些资产：

- 所有对象的 `need_stop_loss`
- 所有对象的 `trigger_reason`
- 所有对象的 `action`
- 所有对象的 `evidence_source`
- 所有对象的 `notes`
- `stop_loss_needed`
- `rollback_target`
- `downgrade_target`
- `global_stop_loss_summary`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `seed_reporting_mode`
- `main_seed_set`
- `additional_seed_set`
- `combined_seed_count`

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件就必须先回退修正，而不是继续被下游消费：

- 某个争议对象仍停留在“后面再看”或动作不唯一。
- `need_stop_loss = true`，但对象行仍没有正式 `action`。
- 对象动作与 stage_gate_matrix.md、01_阶段门槛总表.md 的真实阶段状态互相打架。
- 对象动作与 final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md 或 writing_entry_decision.md 的正式边界互相冲突。
- `evidence_source` 仍是抽象指代，无法回溯到明确文件、表格、图像资产或 summary。
- 对象已经被写成 `retain`，但其协议、公平性或来源链其实已经失效。
- seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 已进入结果资产，但当前文件仍没有写清主 `3-seed` 与 supplementary reporting 的动作边界。

### 9.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查 stage_gate_matrix.md 与 01_阶段门槛总表.md，确认对象所在阶段和 handoff 条件是否真的成立。
2. 再检查 02_止损与回退规则.md，确认触发公式和动作边界是否被误读。
3. 再检查 `08_外部对比`、`09_CRAG验证`、`10_结果汇总` 的正式表格、图像资产、summary 和来源标记是否一致。
4. 再检查 final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 是否已经消费了错误动作。
5. 最后才允许重新填写当前文件对象行、文件级字段和证据映射表。

### 9.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已回写到当前文件对象区或证据映射区。
- 当前文件重新与 02_止损与回退规则.md、stage_gate_matrix.md、final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md 对齐。
- 当前文件重新满足第 `5` 节规则卡片、第 `6` 节对象级止损表和第 `8` 节交接资产要求。

---

## 10. 代码落地接口

### 10.1 对象级止损裁决入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- 入口类/函数：模块层止损表区、外部对比层止损表区、`CRAG` 与写作主张止损表区、协议回退表区
- 输入：阶段矩阵、模块结果、外部主表、`CRAG` 表、案例图、来源标记、公平协议和结果包状态
- 输入补充：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 输出：`eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`, `target_name`, `target_type`, `need_stop_loss`, `trigger_reason`, `action`, `evidence_source`, `notes`
- `dtype`：状态字段为 bool / string；动作字段为枚举 retain / downgrade / remove / rollback
- 依赖配置：`stage_pass`, `result_source_type`, `conclusion_grade`, `package_status`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`, `seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 前置断言：任何来源不清、协议分叉或动作未定的对象不得进入最终止损表；不得把 supplementary `additional_reporting` 误写成新的保留理由或新阻塞
- 运行产物：对象级正式止损清单、唯一动作映射、影响范围说明

### 10.2 文件级止损汇总入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`
- 入口类/函数：固定字段区、结果解释区、证据映射区
- 输入：对象级动作表、关键阻塞对象、回退对象、降级对象
- 输入补充：`seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 输出：`stop_loss_needed`, `rollback_target`, `downgrade_target`, `global_stop_loss_summary`
- `dtype`：`stop_loss_needed` 为 `bool`；其余字段为 `string`
- 依赖配置：`action`, `need_stop_loss`, `stage_pass`, `package_status`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`, `seed_reporting_mode`, `main_seed_set`, `additional_seed_set`, `combined_seed_count`
- 前置断言：只有当对象级动作已唯一化后，才允许汇总文件级四字段
- 运行产物：下游总状态、中英文起步和写稿进入可直接消费的止损汇总层

### 10.3 下游总裁决联动入口

- 代码文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md
- 入口类/函数：总状态裁决区、中英文起步判断区、写稿轨道判断区
- 输入：对象级止损动作、降级对象、删除对象、回退对象、止损总摘要
- 输出：`project_status`, `status_reason`, `major_blockers`, `cn_ready`, `en_ready`, `tone_down_required`, `writing_entry_allowed`, `entry_reason`
- `dtype`：状态字段为 bool / string
- 依赖配置：`action`, `stop_loss_needed`, `rollback_target`, `downgrade_target`, `package_status`
- 前置断言：若关键对象尚未完成正式动作裁决，下游文档不得给出稳定正向结论
- 运行产物：项目总状态阻塞项、中英文写稿边界和最终写稿进入结论

---

## 11. 冲突裁决记录

- 冲突对象：旧版 stop_loss_decision.md 的结构强度、对象级执行语义、文件级输出字段、主 `3-seed` 与 supplementary reporting 边界、独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、强版收尾闭环。
- 冲突来源：旧稿虽然保留了四档动作、对象类型和四类表格，但整体仍停留在“待填止损模板”层，缺少与同层强模板一致的前置依赖留痕、差异化 上游 / 同层 / 下游、文件级 `stop_loss_fixed` 承接、下游消费语义、独立回退边界和强版收尾，也没有把 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 纳入对象级动作边界。
- 裁决结论：本轮将当前文件升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 阶段定位与核心结论 -> 当前文件唯一合法输入、输出与判定流程 -> 规则卡片 -> 固定字段与对象级止损表 -> 证据映射与后填规则 -> 代码实现约束与 handoff 资产 -> 回退条件 -> 代码落地接口 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的正式执行层结构。
- 裁决理由：如果继续保留旧结构，总验收链会出现“规则层已强化、阶段矩阵与总状态已强化，但对象动作层仍只是待填模板”的断层，下游文档仍不得不重新主观解释哪些对象还能留。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/stop_loss_decision.md`、final_readiness_judgement.md、cn_entry_readiness.md、en_entry_readiness.md、writing_entry_decision.md
- 是否需要回流修订：需要；后续任何总状态与写稿边界文档都必须直接读取本文件冻结的对象级动作链，而不是重新主观改判。
- 代码实现影响：影响项目总状态阻塞项、中英文降调边界、`CRAG` 话语强度和写稿进入红线的一致性。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文
- [x] 已继续补读 `02_路线与投稿`、文献锚点、02_止损与回退规则.md、stage_gate_matrix.md、final_readiness_judgement.md、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md` 和相关下游文档，而不是停在总览层
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明为什么这些文件与对象级止损执行层直接相关
- [x] 已完成与 stage_gate_matrix.md、final_readiness_judgement.md、en_entry_readiness.md 的模板强度对照，确认当前文件不再弱于同层强模板
- [x] 当前版本按整篇重写执行，不是对旧稿追加少量对象表和字段说明
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担对象级止损执行层职责
- [x] 已写清当前文件与 `Gate_11`、`stop_loss_fixed` 和下游总裁决链的关系，没有把它写成脱离母协议的孤立表格
- [x] 已把对象级统一触发、四档动作、模块层、外部层、`CRAG` 与写作层、协议回退层写成正式规则卡片
- [x] 已把 seed_reporting_mode / main_seed_set / additional_seed_set / combined_seed_count 接入对象级止损字段区、规则卡片和文件级汇总语义，并明确主 `3-seed` 才是冻结动作依据
- [x] 已把 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 接入输入资产、固定字段、填写要求、handoff 资产和接口依赖，避免止损执行层只消费抽象 `eval_proto_version`
- [x] 每条核心规则都保留了 当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式
- [x] 已保留并强化原文件核心对象表、四档动作、对象类型和文件级总结字段，没有在升级结构时丢失原始实用内容
- [x] 已把 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 扩成可被下游直接消费的正式字段链，而不是只留字段名
- [x] 已明确 supplementary `additional_reporting` 只作为补充说明进入止损链，不会被升级成新的保留理由、删除理由或回退理由
- [x] 已写清独立 `回退条件`，没有把回退要求藏在动作解释或总结句里顺带带过
- [x] 已写清 `代码落地接口`，接口对象细化到对象级裁决、文件级汇总和下游总裁决联动三条主链
- [x] 已补写 `冲突裁决记录`，说明旧结构与同层强模板如何统一、影响哪些文件以及后续如何回流修订
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、字段链、规则卡片、回退、交接、接口和收尾闭环
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”
- [x] 当前文件在落盘后继续执行回读与 diagnostics 复核，正文写作不会替代闭环动作
- [x] 当前文件已经达到“可直接指导对象级止损裁决并支撑总状态与写稿边界消费”的最低强度

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成
- 复核范围：至少覆盖标题层级、列表结构、字段命名一致性、上游 / 同层 / 下游 显式落点、`Gate_11 / stop_loss_fixed / 四档动作公式书写、对象表列名、主 3-seed` 与 supplementary reporting 边界、证据映射表结构，以及是否存在可见 markdown 诊断问题
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核
- 对照要求：本节保持与 stage_gate_matrix.md、final_readiness_judgement.md、en_entry_readiness.md 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话

---

## 14. 一句话版本

> 本文件的正式职责已经固定为：把所有争议对象一次压成唯一、可追溯、可被下游直接消费的 retain / downgrade / remove / rollback 动作底表，并把 `stop_loss_needed`、`rollback_target`、`downgrade_target`、`global_stop_loss_summary` 一起交接给项目总状态、中英文起步和写稿进入链；凡是仍无法明确说明来源、公平性、协议一致性或写作边界的对象，都不得在这里被写成正式保留。
