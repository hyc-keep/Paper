# stage summary 模板

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

这份文件不是“阶段总结写法提示页”，而是 `10_结果汇总` 阶段里专门负责 `summaries_ready` 子门的协议文件。

它当前只负责把下面八件事写死：

1. 什么样的 `stage summary` 才算正式阶段收口文档，而不是阶段日志摘要或临时复盘。
2. `02_UNet流程验证` 到 `10_结果汇总` 各关键阶段必须交出的 summary 结构、最少字段和唯一合法粒度。
3. `stage summary = goal + execution + results + decision + handoff` 这条总定义在本项目里的唯一展开方式。
4. `official_result_record`、正式表格层、正式图像层、阶段通过结论和结果包状态如何被 summary 消费并重新组织成下游可读的 handoff 文档。
5. `final_decision`、`handoff_assets`、`next_stage_boundary`、`supports_mainline`、`rollback_needed` 等关键字段在 summary 层里的唯一合法写法。
6. 各阶段 summary 如何统一服务 `11_总验收与止损`、结果包检查和正式写稿进入判断，而不是让下游重新翻日志猜结论。
7. 当前文件自己的独立 `回退条件`、`代码落地接口`、`冲突裁决记录`、`文件质量自检` 和独立 `Diagnostics 闭环`。
8. 当前文件作为 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md` 中 `summaries_ready` 子门展开协议的正式职责。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- 哪些 run 先算正式记录；这些由 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md` 冻结。
- 哪些结果有资格进入主表、消融表和联合表；这些由 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md` 冻结。
- 哪些图像资产算正式证据、失败案例和正文候选图如何分层；这些由 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md` 冻结。
- 最终结果包落到 ready / ready_with_minor_gaps / not_ready 的哪一档；这些由 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md` 和 11_总验收与止损/* 裁决。
- 各阶段主协议中的训练、模型、评估和来源边界定义；summary 只能消费这些已冻结结论，不能借收口文档回头改协议。

### 1.3 为什么当前文件必须独立存在

结果汇总阶段最容易出现的伪完成状态不是“没有总结”，而是：

- 每个阶段都写过很多文字，但说不清最终保留了什么、删除了什么、为什么这么裁决。
- 有表格和图片，却没有一份能让下游直接读懂“本阶段如何收口、资产怎么交接、下一阶段还能改什么”的正式 handoff。
- 阶段已经进入下一步，但上一阶段的结论、风险和边界仍散落在日志、表格注释和口头解释里。
- `CRAG` 已有结果，外部对比也已完成，但 summary 没把“支持主线到什么强度”压成统一口径。
- `10_结果汇总` 形成了 run、表格、图像和结果包状态，却没有一份对总验收友好的阶段收口索引。

如果 summary 层不独立冻结，后面的 05_投稿结果包检查表.md 和 11_总验收与止损/* 都会再次面对“资产很多，但阶段结论和交接边界并没有正式成文”的灰区。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求 `10_结果汇总` 只能在前序阶段真实收口后执行，summary 层不能替代阶段协议本身。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求 summary 资产映射到正式 `crc_gland_segmentation_project/reports/stage_reports/`、结果包层和总验收层，而不是停留在任意笔记目录。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：要求 summary 只能引用已冻结的 benchmark、split、seed、阈值来源、后处理和 TTA 边界，不能在收口文档里重新发明协议。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：要求 summary 能对齐 `run_name`、`result_tag`、`aggregation`、版本链和正式资产命名。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：要求 summary 的主结论围绕正式对象级三指标与固定 split 身份，而不是写模糊“效果不错”。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求阶段收口、summary 索引和下游 handoff 都落到明确脚本入口、I/O 和前置断言。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求把 summary 规则写成规则卡片、代码落点、运行字段和验收方式，而不是仅保留一个空模板。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求显式写出 `本轮重写直接依赖的前置文件`、差异化 上游 / 同层 / 下游、独立 `回退条件`、不缩水的 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线由 `GlaS` 主 benchmark、`CRAG` 补充 benchmark、主线模块链和外部对比链组成，summary 必须服务这条冻结主线的阶段收口。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：明确每个阶段都要形成可交接结论，summary 不能变成重复阶段协议或继续扩变量的入口。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求中文保底和英文起步判断建立在完整的阶段结论、表格、图像、来源边界和 `CRAG` 强度判断之上，因此 summary 必须成为总验收可直接读取的阶段收口层。

### 2.3 文献依据

本轮重写直接继承以下文献层与结果模板层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/05_GlaS_CRAG_主结果数值速查表.md`：提供任务内锚点方法、benchmark 身份和特殊设置差异，决定 summary 不能把引文值和复现值写成同一种阶段证据。
- `结直肠腺体分割_plan_优化版/03_文献证据/06_我们项目的GlaS_CRAG对照主结果表模板.md`：提供主表、`CRAG` 表和联合表的正式写作框架，决定 summary 必须能直接解释这些表为什么成立。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：把 `summaries_ready` 写成 `Gate_J1` 的正式子门，当前文件就是这个子门的展开协议。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`：提供 run 级正式记录、版本链、失败说明、来源边界和表格资格字段，是 summary 引用正式结果的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`：提供五类正式表、保留 / 降级 / 删除结论和 benchmark 角色边界，是 summary 中“阶段结论如何落到正式表格”的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`：提供成功图、失败图、局部放大图、正文候选图和图像追溯字段，是 summary 中图像证据与局限性段落的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`：提供 reproduced / † / *、公平比较和 `direct_comparison_eligible` 的来源边界，是外部对比阶段 summary 的直接上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/03_结果解释规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/04_阶段验收.md`：提供 `CRAG` 的 A / B / C 结论等级、允许 / 禁止写法和阶段放行边界，是 `CRAG` 阶段与总结果阶段 summary 的直接上游。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md`：会直接消费 summary 中的阶段结论、handoff 资产和缺口说明，用于判断结果包是否真的可用。

#### 同批模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`
- 邻接强模板：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`
- 最近同层强模板：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`
- 下游消费对照：`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`

本轮对照后的固定结论是：

- 当前文件不能继续停留在“通用结构 + 几条禁止写法”的弱模板页强度。
- 当前文件必须补齐显式前置依赖、差异化 上游 / 同层 / 下游、独立 `回退条件`、summary 子门定义、阶段字段链、代码接口和独立 `Diagnostics 闭环`。
- 当前文件的 `文件质量自检` 和 `Diagnostics 闭环` 不得弱于 10_结果汇总/01-03 三份已完成文件的收尾强度。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md`：会根据 summary 中的阶段收口状态、handoff 资产和缺口说明判断 `summaries_ready` 与结果包状态。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：会消费每个阶段 summary 的正式结论，用于项目总状态、止损边界和写稿进入裁决。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`：会把阶段 summary 视为 `handoff_assets_ready` 和 `next_stage_ready` 的直接证据之一。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 阶段收口层的统一定义

从现在开始，正式阶段收口文档固定理解为：

```text
stage_summary
= goal
+ execution
+ results
+ decision
+ handoff
```

并且：

```text
stage_summary_record
= stage_identity
+ upstream_gate
+ executed_scope
+ formal_evidence
+ final_decision
+ handoff_assets
+ next_stage_boundary
```

其中：

- `goal`：本阶段目标、入口条件和上一阶段交接条件。
- `execution`：本阶段真实跑了什么、冻结了什么、明确没有继续扩什么。
- `results`：只引用正式 run、正式表格和正式图像层的结果摘要，不搬原始日志。
- `decision`：把保留、降级、删除、支持主线程度和风险点写成正式裁决。
- `handoff`：把配置、checkpoint、表格、图像、总结索引和下一阶段边界写成可交接资产。

### 3.2 当前文件唯一合法输入资产

当前文件只允许消费下面这些正式资产：

- `official_result_record`
- `formal_tables`
- `figure_evidence`
- `stage_pass`
- retain / backup / delete
- conclusion_grade = A / B / C
- package_status = ready / ready_with_minor_gaps / not_ready

当前文件明确不允许：

- 把阶段日志、调参笔记或临时讨论直接贴成正式 summary。
- 先写结论，再倒推去补 run、表格或图像证据。
- 只引用单次最好结果，不交代 single_seed / mean +- std 身份。
- 把 reproduced / † / *、GlaS / CRAG、TestA / TestB / test40 的来源边界在 summary 层写糊。

### 3.3 当前文件在 `Gate_J1` 中的角色

`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md` 把 `summaries_ready` 写成正式子门。

当前文件就是这个子门的展开协议：

```text
summaries_ready
= per_stage_summary_present
AND decision_trace_clear
AND handoff_assets_ready
AND next_stage_boundary_ready
AND downstream_consumable
```

如果 `summaries_ready = false`，后面的结果包检查和总验收都默认不得宣称正式完成。

---

## 4. 阶段门控表达式

后面统一只承认下面九条总原则：

1. 先有正式 run、正式表格和正式图像，再允许写正式 summary。
2. 先写阶段目标与入口条件，再写结果和结论。
3. 先写真实执行范围，再写“没有继续扩展什么”。
4. 先写保留 / 降级 / 删除结论，再写下一阶段动作。
5. 先写 handoff 资产，再写“继续下一阶段”。
6. 先区分 single_seed / mean +- std、reproduced / † / *、GlaS / CRAG 和 split 身份，再写总结句。
7. 先把风险点和回退边界写清，再允许 summary 成为下游放行证据。
8. 先让 summary 服务总验收与结果包，再考虑它的措辞简洁度。
9. `stage summary` 只能做阶段收口与交接，不得退化为完整实验日志副本。

如果一份 summary 只能告诉读者“本阶段大概不错”，却不能说明结果依据、决策理由、交接资产和下一阶段边界，这份 summary 默认不具备正式 handoff 资格。

---

## 5. 核心规则卡片

### 5.1 正式 summary 准入规则

- 当前结论：每个关键阶段都必须形成一份正式 `stage summary`，且 summary 必须建立在正式 run、正式表格和正式图像证据之上
- 规则类型：`工程冻结规则 + 交接放行规则`
- 适用阶段：`02_UNet流程验证` 到 `10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- 核心公式或定义参考：`formal_summary = identity + evidence + decision + handoff`
- 采用原因：没有正式收口文档，下游就只能重新翻阶段协议、日志和表格去猜结论
- 不采用的相邻方案：不采用“阶段协议本身当 summary”；不采用“日志末尾写几句总结”；不采用“只在总验收时统一回忆”
- 代码落点：reports/stage_reports/*.md
- 运行记录字段：`stage_code`, `stage_name`, `stage_pass`, `final_decision`, `handoff_assets`, `next_stage_boundary`
- 验收方式：检查每个关键阶段都存在独立 summary，且下游不需要回翻原始日志才能读懂结论

### 5.2 summary 证据来源规则

- 当前结论：summary 只允许引用正式结果记录、正式表格和正式图像证据，不允许把临时调试信息直接写成阶段结论
- 规则类型：`来源边界规则`
- 适用阶段：`02_UNet流程验证` 到 `10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`
- 核心公式或定义参考：`summary_evidence = official_result_record + formal_tables + figure_evidence`
- 采用原因：summary 是下游裁决层，不是重新试图解释尚未冻结的中间结果
- 不采用的相邻方案：不采用只贴训练曲线截图；不采用引用未入表的临时筛查值；不采用仅凭主观观察写收益
- 代码落点：reports/stage_reports/*.md，scripts/summarize_stage.py
- 运行记录字段：`linked_run_name`, `linked_table_row`, `linked_figure_asset`, `aggregation`, `result_source_type`
- 验收方式：检查 summary 中每个关键结论都能回指正式 run、表格行或图像资产

### 5.3 决策字段固定规则

- 当前结论：每份 summary 都必须显式写出 `final_decision`、`backup_decision`、`delete_decision`、`supports_mainline` 和 `rollback_needed`
- 规则类型：`工程冻结规则`
- 适用阶段：`02_UNet流程验证` 到 `10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`，`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- 核心公式或定义参考：`decision_trace = keep + backup + delete + support + rollback`
- 采用原因：阶段收口的核心不是“写过了什么”，而是“最终保留什么、为什么、风险是什么”
- 不采用的相邻方案：不采用只写“继续下一阶段”；不采用把删除和降级合并成一句模糊话；不采用省略回退边界
- 代码落点：reports/stage_reports/*.md，reports/stage_reports/stage_summary_index.md
- 运行记录字段：`final_decision`, `backup_decision`, `delete_decision`, `supports_mainline`, `rollback_needed`
- 验收方式：检查 summary 能直接回答“下一阶段到底承接哪个版本、哪些内容已放弃”

### 5.4 handoff 资产规则

- 当前结论：summary 必须把配置、checkpoint、正式表格、正式图像、备注与缺口说明写成明确 handoff 资产，不允许只写“见附件”
- 规则类型：`交接放行规则`
- 适用阶段：`02_UNet流程验证` 到 `10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`，`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- 核心公式或定义参考：`handoff_assets = config + checkpoint + tables + figures + notes`
- 采用原因：下游 `next_stage_ready` 的判断依赖是否真的交出了能消费的正式资产
- 不采用的相邻方案：不采用“资产都在实验目录里”；不采用只写结论不写资产路径；不采用把 checkpoint 和图像交接留到口头说明
- 代码落点：reports/stage_reports/*.md，scripts/summarize_stage.py
- 运行记录字段：`config_path`, `checkpoint_path`, `table_refs`, `figure_refs`, `note_refs`
- 验收方式：检查每份 summary 都能列出下一阶段或总验收真正要消费的资产清单

### 5.5 下一阶段边界规则

- 当前结论：每份 summary 都必须同时写清“下一阶段允许改什么”和“下一阶段不允许改什么”
- 规则类型：`路线冻结规则`
- 适用阶段：`02_UNet流程验证` 到 `10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 核心公式或定义参考：`next_stage_boundary = allowed_changes + forbidden_changes`
- 采用原因：如果不把边界写死，后面的阶段很容易借“继续推进”回头改旧结论
- 不采用的相邻方案：不采用只写“继续下一阶段”；不采用允许多变量同时重开；不采用让下一阶段自己猜还能改什么
- 代码落点：reports/stage_reports/*.md
- 运行记录字段：`allowed_changes`, `forbidden_changes`, `next_stage_name`
- 验收方式：检查下游阶段是否能直接从上一阶段 summary 获取边界，而不需要重新询问

### 5.6 `UNet` 类阶段 summary 规则

- 当前结论：`02_UNet流程验证` 和 `03_UNet稳定性` 的 summary 必须额外写清流程是否跑通、波动是否可控、是否形成首版稳定协议
- 规则类型：`阶段特定规则`
- 适用阶段：`02_UNet流程验证`，`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`
- 核心公式或定义参考：`unet_summary = pipeline_status + stability_status + baseline_readiness`
- 采用原因：后续 baseline 和模块实验都建立在稳定主流程之上，早期 summary 不能只写一个最好值
- 不采用的相邻方案：不采用只报单次最优结果；不采用省略三次重复结论；不采用不写流程排错收口
- 代码落点：reports/stage_reports/02_unet_summary.md，reports/stage_reports/03_unet_stability_summary.md
- 运行记录字段：`pipeline_status`, `stability_status`, `mean_std_ready`, `baseline_ready`
- 验收方式：检查 early stage summary 能直接回答“流程能否作为后续正式基线继续使用”

### 5.7 模块阶段 summary 规则

- 当前结论：`04_Baseline`、`05_LKMA`、`06_Boundary`、`07_Distance` 的 summary 必须额外写清模块是否保留、保留的是哪个正式版本、删除或降级的理由是什么
- 规则类型：`阶段特定规则`
- 适用阶段：`04_Baseline` 到 `07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`
- 核心公式或定义参考：`module_summary = kept_version + dropped_version + reason + mainline_support`
- 采用原因：模块阶段的核心不是“模块试过了”，而是“主线到底留下了什么”
- 不采用的相邻方案：不采用模块都写进主线；不采用只写收益不写成本和波动；不采用把删除理由留到总验收才补
- 代码落点：reports/stage_reports/04_baseline_summary.md 到 reports/stage_reports/07_distance_summary.md
- 运行记录字段：`module_name`, `kept_version`, `drop_reason`, `supports_mainline`, `cost_note`
- 验收方式：检查 summary 是否能直接支持消融表顺序和总验收中的模块去留判断

### 5.8 外部对比与 `CRAG` 阶段 summary 规则

- 当前结论：`08_外部对比` summary 必须写清哪些方法进入主表、哪些只保留引用值、哪些降级为补充层；`09_CRAG验证` summary 必须写清 `CRAG` 对主线的支撑强度和任务内对照位置
- 规则类型：`阶段特定规则 + 来源边界规则`
- 适用阶段：`08_外部对比`，`09_CRAG验证`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/03_结果解释规则.md`
- 核心公式或定义参考：`external_or_crag_summary = source_boundary + comparison_role + conclusion_grade`
- 采用原因：这两个阶段最容易在收口时把来源边界和结论强度写糊，必须单独冻结
- 不采用的相邻方案：不把 `†`、`*` 写成公平主结果；不把 `CRAG` 写成超过其真实证据强度的泛化结论
- 代码落点：reports/stage_reports/08_external_summary.md，reports/stage_reports/09_crag_summary.md
- 运行记录字段：`result_source_type`, `direct_comparison_eligible`, `conclusion_grade`, `supports_mainline`
- 验收方式：检查这两份 summary 能直接支撑主表表注、联合表和总验收中的语气边界

### 5.9 `10_结果汇总` summary 规则

- 当前结论：`10_结果汇总` 自身也必须有 summary，且必须把 registry_ready / tables_ready / figures_ready / summaries_ready / package_status_fixed / downstream_ready 的收口状态写清，并显式交接 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 五个评估实现硬字段
- 规则类型：`阶段特定规则 + 子门汇总规则`
- 适用阶段：`10_结果汇总`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md`
- 核心公式或定义参考：`result_summary = subgates + package_status + handoff_to_final_gate + eval_implementation_chain`
- 采用原因：如果 `10_结果汇总` 自己没有正式 summary，总验收仍需要逐个子文件重新拼接本阶段状态
- 不采用的相邻方案：不采用只把子门状态留在分文件里；不采用结果包状态未定就直接交给 `11_总验收与止损`
- 代码落点：reports/stage_reports/10_result_summary.md
- 运行记录字段：`registry_ready`, `tables_ready`, `figures_ready`, `summaries_ready`, `package_status`, `downstream_ready`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 验收方式：检查 `10_结果汇总` summary 能直接服务总验收，不需要重新回读 `01-05` 五个文件才能理解本阶段状态

---

## 6. 正式模板、固定字段与落盘位置

### 6.1 统一适用范围

正式 `stage summary` 至少覆盖下面这些阶段：

- `02_UNet流程验证`
- `03_UNet稳定性`
- `04_Baseline`
- `05_LKMA`
- `06_Boundary`
- `07_Distance`
- `08_外部对比`
- `09_CRAG验证`
- `10_结果汇总`

`01_数据协议` 和 `11_总验收与止损` 分别由更上游的数据交接文档和最终总裁决文档承接，不使用本页的阶段收口模板替代。

### 6.2 正式 summary 最少字段

每份正式 summary 至少要覆盖下面这些字段：

| 字段 | 固定要求 |
|------|----------|
| `stage_code` | 固定阶段码 |
| `stage_name` | 正式阶段名 |
| `summary_status` | draft / final，正式交接时必须为 `final` |
| `upstream_gate` | 上一阶段交接条件或当前阶段入口条件 |
| `executed_scope` | 本阶段真实跑了哪些版本、冻结了哪些变量 |
| `not_extended_scope` | 明确没有继续扩展的内容 |
| `formal_result_refs` | 对应 run、表格、图像证据引用 |
| `final_decision` | 当前正式保留结论 |
| `backup_decision` | 当前降级保留结论 |
| `delete_decision` | 当前删除结论 |
| `supports_mainline` | 当前阶段对主线的支持强度 |
| `risk_note` | 当前剩余风险点 |
| `handoff_assets` | 配置、checkpoint、表格、图像、备注 |
| `next_stage_boundary` | 下一阶段允许改什么 / 不允许改什么 |
| `rollback_needed` | 是否需要回退 |
| `eval_cast_policy` | 阈值前 `float32` 评估约束 |
| `boundary_metric_width` | `Boundary F1` 正式评估宽度 |
| `boundary_metric_impl` | 正式边界评估实现 |
| `connected_components_impl` | 正式连通域实现 |
| `connected_components_connectivity` | 正式连通域连通性 |

### 6.3 通用正式模板

后面每个阶段结束后，都必须至少生成一份如下结构的文档：

```md
# [阶段名] stage summary

- stage_code:
- stage_name:
- summary_status: `final`

## 1. 阶段目标与入口条件
- 本阶段目标：
- 上一阶段交接条件：
- 本阶段唯一允许变化的变量：

## 2. 实际执行与冻结范围
- 实际跑了哪些正式版本：
- 实际固定了哪些参数或边界：
- 明确没有继续扩展什么：

## 3. 正式结果与证据摘要
- run 级证据：
- 表格层证据：
- 图像层证据：
- 主指标结论：
- 补充指标或稳定性结论：

## 4. 最终决策
- final_decision:
- backup_decision:
- delete_decision:
- supports_mainline:
- rollback_needed:

## 5. 主要理由与风险点
- 支持保留的证据：
- 不支持继续扩展的证据：
- 当前风险点：

## 6. 交接给下一阶段或总验收的资产
- 配置：
- checkpoint：
- 表格：
- 图像：
- 备注：

## 7. 下一阶段执行边界
- 下一阶段允许改什么：
- 下一阶段不允许改什么：
```

固定要求：

- `第 3 节` 只能引用正式 run、正式表格和正式图像证据。
- `第 4 节` 不得省略 `final_decision`、`backup_decision`、`delete_decision`、`supports_mainline`、`rollback_needed`。
- `第 6 节` 不得只写“见目录”或“同上”，必须给出可交接资产类别。
- `第 7 节` 不得只写“继续下一阶段”，必须同时写允许边界和禁止边界。

### 6.4 各阶段必须补充的专属字段

#### `UNet` 类阶段

必须特别补：

- `pipeline_status`
- `stability_status`
- `mean_std_ready`
- `baseline_ready`

#### 模块阶段

必须特别补：

- `kept_version`
- `drop_reason`
- `cost_note`
- `supports_mainline`

#### 外部对比阶段

必须特别补：

- `main_table_methods`
- `citation_only_methods`
- `supplement_only_methods`
- `source_boundary_note`

#### `CRAG` 阶段

必须特别补：

- `conclusion_grade`
- `allowed_claim`
- `task_internal_position`

#### `10_结果汇总` 阶段

必须特别补：

- `registry_ready`
- `tables_ready`
- `figures_ready`
- `summaries_ready`
- `package_status`
- `downstream_ready`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`

### 6.5 输出粒度规则

每个 `stage summary` 必须控制在下面范围：

- 能清楚交代决策链和 handoff 资产。
- 不重复整份阶段协议。
- 不把原始实验日志全文搬进来。
- 不跳过正式证据直接写结论。

一句话理解：

- 它是“阶段收口与交接文档”。
- 不是“完整实验日志副本”。

### 6.6 固定落盘位置

正式 handoff 一律以 `crc_gland_segmentation_project/reports/stage_reports/` 为准，推荐最少形成下面这些文件：

- reports/stage_reports/02_unet_summary.md
- reports/stage_reports/03_unet_stability_summary.md
- reports/stage_reports/04_baseline_summary.md
- reports/stage_reports/05_lkma_summary.md
- reports/stage_reports/06_boundary_summary.md
- reports/stage_reports/07_distance_summary.md
- reports/stage_reports/08_external_summary.md
- reports/stage_reports/09_crag_summary.md
- reports/stage_reports/10_result_summary.md
- reports/stage_reports/stage_summary_index.md

如果历史目录中仍存在 summaries/ 路径，允许作为兼容中间目录继续保留，但正式结果包和总验收消费一律以 `crc_gland_segmentation_project/reports/stage_reports/` 为准。

### 6.7 高频漏写项

summary 层最容易漏掉的不是标题结构，而是：

- 当前结论到底基于单次结果还是 `mean +- std`。
- 当前引用的是正式 run、正式表格还是正式图像层。
- 当前保留的是哪个正式版本，而不是泛泛的模块名。
- 下一阶段到底允许改什么，哪些东西已经冻结。
- 当前阶段有哪些资产已经能交接，哪些仍是缺口。

这些字段一旦漏掉，下游总验收和结果包检查就会整体返工。

---

## 7. 代码实现约束与代码落地接口

### 7.1 本文件必须直接服务的资产

当前文件最终必须稳定服务下面这些资产：

- reports/stage_reports/*.md
- reports/stage_reports/stage_summary_index.md
- submission_package_check.md
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/final_readiness_judgement.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/writing_entry_decision.md`

### 7.2 本文件必须复用或对齐

- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/01_阶段门槛总表.md`

### 7.3 本文件禁止放宽的边界

当前文件明确禁止：

- 把 stage summary 写成自由发挥的复盘散文。
- 把 summary 证据来源从正式 run、表格、图像层降级为临时日志。
- 只写“继续下一阶段”，不写 handoff 资产和边界。
- 只写“删除”或“保留”，不写为什么以及风险点。
- 把 `10_结果汇总` summary 省掉，要求总验收自己去拼各子门状态。

### 7.4 代码落地接口

#### 7.4.1 单阶段 summary 构建入口

- 代码文件：scripts/summarize_stage.py
- 入口类/函数：`build_stage_summary()`、`render_stage_summary()` 或等价正式入口
- 输入：阶段代码、正式 run 记录、正式表格、正式图像索引、阶段结论、handoff 资产
- 输出：单阶段 summary markdown
- `dtype`：状态与结论字段为 string / bool；指标字段为 `float`；资产计数字段为 `int`
- 依赖配置：`stage_code`, `stage_name`, `final_decision`, `supports_mainline`, `rollback_needed`, `package_status`
- 前置断言：缺正式证据引用、缺 final decision、缺 handoff 资产或缺下一阶段边界的阶段，不得生成 `final` summary
- 运行产物：reports/stage_reports/[stage]_summary.md

#### 7.4.2 summary 索引与下游校验入口

- 代码文件：scripts/validate_sources.py
- 入口类/函数：`validate_stage_summary_fields()`、`build_stage_summary_index()` 或等价正式入口
- 输入：各阶段 summary、必要字段 schema、阶段顺序表
- 输出：summary 字段校验结果、阶段 summary 索引、缺口清单
- `dtype`：字段状态为 `bool`；缺口说明为 `string`；阶段顺序为 `string list`
- 依赖配置：`summary_status`, `final_decision`, `handoff_assets`, `next_stage_boundary`, `stage_pass`
- 前置断言：缺少关键字段、阶段顺序不连贯或 handoff 资产无法映射的 summary，不得进入总验收索引
- 运行产物：reports/stage_reports/stage_summary_index.md、summary 校验日志

#### 7.4.3 结果包与总验收交接入口

- 代码文件：scripts/summarize_stage.py
- 入口类/函数：`finalize_submission_package_check()`、`build_final_handoff_summary()` 或等价正式入口
- 输入：summary 索引、结果包状态、表格层状态、图像层状态、总验收状态
- 输出：结果包 summary 状态、最终 handoff 摘要、下游总验收输入
- `dtype`：状态字段为 bool / string；缺口计数字段为 `int`
- 依赖配置：`summaries_ready`, `package_status`, `downstream_ready`, `missing_assets`, `eval_cast_policy`, `boundary_metric_width`, `boundary_metric_impl`, `connected_components_impl`, `connected_components_connectivity`
- 前置断言：缺关键阶段 summary、缺 `10_结果汇总` summary 或 summary 与结果包状态打架时，不得宣称 `summaries_ready = true`
- 运行产物：结果包检查摘要、总验收 handoff 摘要

---

## 8. 回退条件

### 8.1 独立回退触发条件

只要出现下面任意一条，当前文件就必须先回退修正，而不是直接进入结果包层或总验收：

- 某阶段没有独立 `stage summary`，或 summary 仍停留在草稿状态。
- summary 中的关键结论无法回指正式 run、正式表格或正式图像证据。
- summary 只有结论，没有 final_decision / handoff_assets / next_stage_boundary 等关键字段。
- summary 把 single_seed / mean +- std、reproduced / † / *、GlaS / CRAG 或 split 身份写糊。
- summary 只写抽象 `eval_proto_version`，没有把 eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity 作为 handoff 资产显式交给下游。
- `10_结果汇总` 没有单独 summary，导致总验收仍需逐个子文件重拼本阶段状态。
- summary 与下游阶段门槛、结果包状态或总验收结论互相打架。

### 8.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查是否每个关键阶段都已有独立 summary。
2. 再检查 summary 的正式证据引用是否完整。
3. 再检查保留 / 降级 / 删除结论和风险点是否写清。
4. 再检查 handoff 资产与下一阶段边界是否能被下游直接消费。
5. 最后检查 `10_结果汇总` summary、结果包状态和总验收输入是否一致。

### 8.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明 `summaries_ready = true`：

- 各关键阶段 summary 已全部补齐并标记为 `final`。
- 每份 summary 的证据来源、决策字段、handoff 资产和下一阶段边界重新对齐。
- `10_结果汇总` summary 已能直接总结各子门与结果包状态。
- 当前文件重新满足第 `5` 节全部规则卡片和第 `6-7` 节全部模板、字段和接口要求。

---

## 9. 冲突裁决记录

- 冲突对象：旧版 04_stage_summary模板.md 的结构强度、`summaries_ready` 子门职责、字段链完整性和收尾闭环强度
- 冲突来源：旧稿虽然已经列出通用模板、阶段差异字段、禁止写法和落盘位置，但仍停留在“如何写总结”的弱模板页层，缺少显式前置文件、差异化 上游 / 同层 / 下游、`summaries_ready 正式子门定义、与 run / 表格 / 图像层的输入映射、独立 回退条件`、正式 `代码落地接口`、`冲突裁决记录`、不缩水的 `文件质量自检` 和独立 `Diagnostics 闭环`
- 裁决结论：本轮将当前文件升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 核心问题 -> summary 层总原则 -> 规则卡片 -> 正式模板与字段链 -> 代码实现约束与代码落地接口 -> 回退条件 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的完整阶段收口协议结构
- 裁决理由：如果继续保留旧版弱结构，summary 仍然无法承担 `summaries_ready` 子门职责，结果包检查和总验收也无法把阶段结论当作正式 handoff 资产直接消费
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/04_stage_summary模板.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`，`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/05_投稿结果包检查表.md`，`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- 是否需要回流修订：需要；后续若任何阶段 summary 仍沿用旧版弱模板、缺 handoff 字段或缺独立边界，必须按本文件补齐
- 代码实现影响：影响 stage summary 生成脚本、summary 索引校验、结果包检查脚本和总验收 handoff 输入

---

## 10. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把适用于 summary 层的硬性约束真实落到正文
- [x] 已继续补读 `02_路线与投稿`、`03_文献证据`、10_结果汇总/00-03、10_结果汇总/05、11_总验收与止损/00-01
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论
- [x] 已按当前文件真实角色区分 上游 / 同层 / 下游，并说明这些文件为什么会直接约束或消费 summary 层
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/01_结果记录模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/02_主表与消融表回填规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/03_可视化与失败案例清单.md`、`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md` 的模板强度对照，确认收尾部分未缩水
- [x] 当前版本按整篇重写执行，不是对旧稿追加零散补丁说明
- [x] 已把当前文件职责提升为 `summaries_ready` 子门协议，而不是停留在“如何写总结”的说明页
- [x] 已写清 `stage_summary` 与 `stage_summary_record` 的统一定义、唯一合法输入资产和 `summaries_ready` 正式子门公式
- [x] 已把正式 summary 准入、证据来源、决策字段、handoff 资产、下一阶段边界、`UNet` 类阶段、模块阶段、外部对比与 `CRAG` 阶段、`10_结果汇总` 阶段全部写成正式规则卡片
- [x] 已保留并强化旧稿中“统一结构”“阶段差异字段”“不是完整日志副本”“禁止模糊结论”“必须交代交接资产和下一阶段边界”等可继承内容
- [x] 已把 summary 中必须写清 single_seed / mean +- std、reproduced / † / *、GlaS / CRAG、split 身份和正式证据引用的边界写清
- [x] 已写清正式模板、最少字段、专属字段、固定落盘位置和兼容目录规则，不再停留在“给一个框架自己填”的粒度
- [x] 已写清 summary 层与正式 run 记录、正式表格层、正式图像层、结果包层和总验收层之间的消费关系
- [x] 已写清代码落点和运行记录字段，不再停留在“人工写总结”粒度
- [x] 代码落地对象已经细化到单阶段 summary 构建、summary 索引校验、结果包与总验收交接三个入口
- [x] 已写清独立 `回退条件`，没有把回退边界藏进验收或总结句里顺带带过
- [x] 已补写标准化 `冲突裁决记录`，说明旧版弱结构与当前强模板之间如何统一
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、核心定义、规则卡片、字段链、接口、回退和下游 handoff
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“已检查”
- [x] 当前文件在落盘后仍要求继续执行回读与 diagnostics 复核，正文重写不会替代闭环动作
- [x] 当前文件已经达到“可直接指导阶段收口、summary 索引、结果包检查和总验收 handoff”的最低强度

---

## 11. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成
- 复核范围：至少覆盖标题层级、列表结构、规则卡片字段完整性、`summaries_ready` 子门公式、正式模板 fenced 结构、上游 / 同层 / 下游 显式落点、独立 `回退条件`、固定落盘位置、`文件质量自检` 和独立 `Diagnostics 闭环` 是否完整
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核
- 对照要求：本节保持与 10_结果汇总/01-03 三份同层强模板同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话

---

## 12. 一句话版本

> `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/04_stage_summary模板.md` 的正式职责已经固定为：把 `02-10` 各关键阶段的收口文档写成 `summaries_ready` 的唯一合法协议层，要求每份 `stage summary` 都必须基于正式 run、正式表格和正式图像证据，明确写清阶段目标、真实执行、正式结果、保留 / 降级 / 删除决策、handoff 资产和下一阶段边界；任何没有独立 summary、没有正式证据引用、没有 handoff 资产或没有边界说明的阶段，都不能被视为真正完成交接。
