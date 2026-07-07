---
name: "crc-gland-stage-implementation"
description: "正式代码实现 skill。只在阶段实现卡已锁定后调用,并把代码质量证据放在第一优先级。"
---

# CRC Gland Stage Implementation

## 角色/入口

这个 skill 是正式编码阶段入口,只在根目录 `d:\12_Medical_Image_Segmentation\Paper\.trae\skills\crc-gland-coding-guard\SKILL.md` 已裁决到 `编码` 时调用。

项目内被动导航与规程层位于:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\00_技能体系导航.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\制度完成定义.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\模板I_实现依据记录.md`

## 目标

这个 skill 只负责一件事:

> 按当前阶段边界实现正式代码,并用真实运行证据证明代码质量。

## 边界/分层

- 本 skill 负责正式代码、配置、正式资产改动与其编码期证据留痕
- 本 skill 不负责根目录路由裁决
- 本 skill 不负责把 `workflow_gate_report.md` 提前写出来
- 本 skill 不负责提前写学习型说明文
- 本 skill 产生的“实现依据记录”属于编码期正式证据,不是后置说明文

## 状态口径

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking`: `not_started / blocked / partial / pass`

编码阶段至少要同时分清:

- 当前是否允许编码,看 `Stage Gate`
- 本轮 runtime / code quality 证据是否成立,看 `Diagnostics / Post-QC`
- 当前任务整体推进到哪,看 `implementation_tracking`

## 前置条件

进入本 skill 之前,必须已经先完成“研究定标”和“阶段锁定”。

正式研究记录至少已经说明:

- 当前阶段为什么现在必须先做
- 本轮直接依赖的已读文件
- 从计划 / 论文 / 官方脚本 / 参考代码里提取出的硬约束
- 为什么现在不能直接进入下一个阶段
- `研究结论状态 = allow_stage_lock`

正式阶段实现卡至少包含:

- 当前阶段唯一目标
- 允许改动 / 禁止改动
- 论文依据 / 代码依据 / 官方口径依据
- 工程落点
- 最小验证计划

并且必须同时满足:

- 正式研究记录已存在
- `研究结论状态 = allow_stage_lock`
- `research_alignment_gate_report.md = pass`
- 正式阶段实现卡已存在
- `stage_definition_gate_report.md = pass`
- `precheck_doc_gate_report.md = pass`
- `Pre-check Guard` 已回链 `stage_definition_gate_report.md`

如果研究定标记录还不成立,先回到 `d:\12_Medical_Image_Segmentation\Paper\.trae\skills\crc-gland-research-alignment\SKILL.md`。
如果研究已完成但阶段锁定或 Pre-check 还没成立,不要直接写代码。

## 本阶段工作顺序

### 1. 编码前

必须先做:

1. 读取当前阶段和上一阶段正式协议
2. 确认正式研究记录、正式阶段实现卡与 `stage_definition_gate_report.md` 没有冲突
3. 完成 `Pre-check` 相关留痕
4. 确认 `Pre-check Guard` 与 `stage_definition_gate_report.md` 回链一致
5. 明确本轮最小运行验证计划
6. 建立或更新 `实现依据记录.md`，先把本轮要改动的正式文件、计划依据、论文依据、官方脚本/参考代码依据、冻结参数来源写进去
7. 同时创建或更新当前编号阶段的独立归档:
   - `reports/stage_reports/implementation_tracking/[当前阶段名]/实现依据记录.md`
   - 根路径 `b_class_auxiliary/runtime_checks/实现依据记录.md` 只允许作为“当前阶段副本”
   - 禁止用根路径单文件覆盖旧阶段唯一依据记录
8. 如果当前阶段归档不是首次原始版本，而是事后重建,必须显式写明“重建归档版”与可恢复边界
9. 如果某个改动只有工程冻结规则、没有直接论文或参考代码支撑，也必须在 `实现依据记录.md` 里诚实写明“这是工程收敛决定，不是论文直接结论”

这里的“正式文件”不是一句总称,而是逐文件对象:

- 每个被改动的正式 `py / yaml / yml / json / toml / csv / md` 文件,都必须在 `实现依据记录.md` 里单独占一行
- 不允许只写“本轮改了训练入口和数据模块”,却不把具体文件逐个列出来
- 不要求每个文件单独再写一份 md,但要求同一份 `实现依据记录.md` 对每个正式文件逐文件回链
- 除了根路径当前副本外,还必须在当前阶段目录保留一份不可被后续阶段覆盖的独立归档

### 2. 正式编码

编码时只允许做当前阶段已批准的改动,不允许顺手改下一阶段变量。

编码阶段还必须满足下面 4 条:

1. 每个正式代码/配置/正式资产文件都必须能回链到 `结直肠腺体分割_plan_优化版/01_实验执行` 的具体文件和章节
2. 只要引用了 `结直肠腺体分割_正式参考资料`、`03_文献证据`、论文、官方脚本或参考代码,就必须把对应文件、章节、函数或脚本路径写入 `实现依据记录.md`
3. 当前阶段采用了哪些冻结参数、阈值、split 边界、loss 组合或训练规则,必须写清“参数值是什么、依据来自哪里、最后落到哪个正式文件”
4. 这些依据留痕属于编码阶段正式产物,不能等到学习型说明文阶段才事后回忆
5. 只要本轮改了多个正式 `py` 文件,就必须把每个 `py` 文件分别映射到各自的计划依据、论文/文献依据、参考代码依据和工程收敛说明,不能合并成一条笼统叙述

### 3. 先验证代码质量

只要本轮改了正式代码、配置或正式资产,必须先产出:

1. `runtime_check_report.md`
2. `runtime_evidence.json`
3. `runtime_check.log`
4. `code_quality_gate_report.md`

最低物理证据必须包含:

- smoke run 命令和日志路径
- dataloader batch 的样本来源、shape、dtype、unique 值或数值范围
- 输入、标签、logits 的 shape / dtype
- loss 数值和 finite 结果
- backward 或 optimizer.step 的真实证据

唯一例外只允许出现在当前编号阶段=`01_数据协议`,且本轮正式改动的唯一目标是 `train entrypoint preflight` 时:

- 当前 runtime 必须显式声明 `runtime_profile = data_protocol_preflight`
- 必须真实证明 `configs/data -> splits/*.csv -> dataset_root + relpath -> train.py` 这条正式消费链已被入口脚本接住
- 必须在 `runtime_evidence.json` 里留下 `asset_manifest / data_stage_pass / handoff_ready / split_asset_exists / data_config_registered / entrypoint_check_pass`
- 此时 `loss / backward / optimizer.step` 允许为 `not_applicable` 或 `null`,但必须在报告里明写“这不等于完整训练链成立”
- 这类 preflight 画像只允许支持 `01_数据协议` 的 `preflight_pass`,不允许拿来宣称后续模型阶段的完整训练链代码质量已经成立

推荐命令固定为:

- `python b_class_auxiliary/tools/run_minimal_runtime_check.py --experiment-config [configs/experiment/*.yaml]`
- `python b_class_auxiliary/tools/check_code_quality_gate.py --post-qc-guard [Post-QC Guard相对路径]`

### 4. 本阶段到此为止

本 skill 到 `code_quality_gate_report.md` 为止。
`workflow_gate_report.md` 与学习型说明文属于后续阶段,由根目录 `crc-gland-coding-guard` 继续裁决是否进入。

## 门禁/审查

编码阶段至少要回链下面这些真实对象:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\模板I_实现依据记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\run_minimal_runtime_check.py`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_code_quality_gate.py`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\制度完成定义.md`

如果当前阶段同时改了 skill / 导航 / 模板总规范,必须额外回到治理阶段并运行:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_formal_stage_docs.py`

## 最小交付物

- 已实现的代码改动
- 研究定标记录
- `research_alignment_gate_report.md`
- 阶段实现卡
- Pre-check 留痕
- `实现依据记录.md`
- `runtime_check_report.md`
- `runtime_evidence.json`
- `runtime_check.log`
- `code_quality_gate_report.md`
- Diagnostics
- Post-QC Guard

## 红线

- 没有阶段实现卡就开写
- 没有研究定标记录或 `研究结论状态` 还不是 `allow_stage_lock` 就开写
- `stage_definition_gate_report.md` 还是 `partial / fail`,却继续开写
- `precheck_doc_gate_report.md` 不是 `pass`,却继续开写
- Stage Gate 是 `blocked` 还继续改正式代码
- 没有 `实现依据记录.md`,就开始或继续正式编码
- 没有当前阶段独立归档,却只维护根路径单文件
- 进入新阶段时覆盖旧阶段唯一 `实现依据记录.md`
- 写了正式代码,却不记录对应的计划条款、论文/参考代码来源和冻结参数
- 改了多个正式 `py` 文件,却只留一条合并后的模糊依据说明
- 把“我大概参考过某论文/某仓库”当成已经完成编码依据留痕
- 代码证据没出来就先宣称完成
- 等到学习型说明文阶段才回忆“当时参考了什么”
- 试图用 Guard 或说明文替代真实运行验证
