---
name: "crc-gland-learning-doc"
description: "学习型说明文 skill。只在代码和证据已稳定后调用,负责把已经成立的实现讲清楚。"
---

# CRC Gland Learning Doc

## 正式角色

这个 skill 是学习型说明文阶段入口,只在根目录 `d:\12_Medical_Image_Segmentation\Paper\.trae\skills\crc-gland-coding-guard\SKILL.md` 已裁决到 `说明文档` 时调用。

它负责把已经被研究、实现依据、运行证据和总放行共同证明成立的实现讲清楚,而不是反向替代这些证据。

## 边界/分层

- 本 skill 负责解释已经成立的实现
- 本 skill 不负责补研究定标
- 本 skill 不负责补 `实现依据记录.md`
- 本 skill 不负责补 runtime 三件套或 `workflow_gate_report.md`
- 本 skill 只能消费前面阶段已经成立的正式证据,不能反向制造通过

## 状态口径

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking`: `not_started / blocked / partial / pass`

## 工程落点

学习型说明文阶段的正式工程落点固定为:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\reports\stage_reports\`
- 后续 implementation_tracking 文档组在该目录下按阶段继续展开

## 交付范围裁定

学习型说明文不是给“本轮碰过的所有文件”都补一份。
它只服务 `制度完成定义.md`「文件三分归属」里判定为 **A 类(项目正式对象)** 的文件。

判定口径以 `制度完成定义.md`「文件三分归属」为唯一权威,本 skill 不再自定义主观标准:

- 只有 A 类(项目正式对象)才写逐文件说明文
- B 类(AI 辅助与流程文件)一律不写说明文
- C 类(存疑待清理)在交付前清理裁决前,不写正式交付说明文,只在 `实现依据记录.md` 保留登记

A 类判定不靠“会不会被别人使用”这种主观感觉,而靠客观依据:

- 是当前阶段计划(`结直肠腺体分割_plan_优化版`)的「代码落点 / 代码落地接口 / 正式资产 / 产物清单」明确点名的对象
- 或为满足计划某条明确要求所必需,且能在 `实现依据记录.md` 回链到计划条款号或参考资料出处

固定排除(恒为 B 类,永不写说明文):

- `.trae/skills/**`
- `b_class_auxiliary/coding_guards/**`
- 门禁/治理类 `check_*`、`enforce_*`、`*gate_report*` 等流程脚本
- 计划未点名、仅为生成某个计划产物而临时多造的工具脚本
- 任何只服务本轮治理 / Pre-check / runtime gate / code-quality gate / workflow gate 的内部留痕文件

禁止混合(硬约束):

- 禁止把“计划要求的项目内容”与“AI 辅助检查内容”写进同一个文件
- 若某段 AI 辅助内容确有保留价值,必须单独另存为一个 B 类文件,不允许塞进任何 A 类项目文件
- 出现混合件时,不允许既保留又交付;必须先拆分为纯 A 类和纯 B 类两个文件,再继续

说明文档阶段的强制落盘顺序:

1. 先按 `制度完成定义.md`「文件三分归属」显式列出“本轮 A 类正式对象清单”,逐个标注归 A 的客观依据(计划条款号 或 参考资料出处)
2. 同时列出被判为 B / C 的计划外文件及其归类理由(与 `实现依据记录.md` 登记一致)
3. 再为 A 类清单里的每个对象建立 `正式对象 -> 对应说明文` 映射
4. 再开始写 `README.md`、`implementation_status.md`、`真实对象文件名.md` 或验收说明文
5. 如果某个 A 类对象还没有对应说明文,当前轮次就不能宣称“项目文件说明已覆盖”
6. `README.md` 和 `implementation_status.md` 只能充当入口和阶段状态页,不能替代具体 Python / YAML / CSV / 结果资产的逐文件说明

最小覆盖要求:

- 只要本轮存在新的 A 类 Python 脚本、模块、配置或正式资产,就必须出现对应的逐文件说明文
- 不能只写阶段入口文档,然后把“代码说明”“资产说明”“配置说明”都默认算已完成
- 不能只解释 workflow / gate / guard,却不解释真实项目代码、配置和正式资产
- 逐文件说明的对象优先级,默认按 `scripts/`、`src/`、`configs/`、`splits/`、`datasets/`、计划点名的 `tools/`、A 类 `reports/` 处理

禁止混淆:

- 不要把“和当前工作流有关”误判成“属于项目 A 类”
- 不要把 skill / guard / gate 报告冒充成 A 类项目对象
- 不要因为当前 turn 改过某个 B 类内部文件,就自动要求它进入学习型说明文映射

## 目标

这个 skill 只负责一件事:

> 在代码和证据已经成立后,再把实现写成小白能看懂、又能回链依据的说明文。

全局固定顺序、总放行语义与最终完成定义,以根目录 `crc-gland-coding-guard` 和项目内 `制度完成定义.md` 为准。

## 前置条件

进入本 skill 前至少满足:

- 研究定标记录已存在,且能回查当前阶段为什么这样做
- `research_alignment_gate_report.md = pass`
- 00_阶段实现卡与 `stage_definition_gate_report.md = pass` 已存在
- `实现依据记录.md` 已存在,且能回查本轮正式代码/配置/正式资产到底依据什么实现
- 当前阶段代码或正式资产已经存在
- `runtime_check_report.md` 已存在
- `runtime_evidence.json` 已存在
- `runtime_check.log` 已存在
- `code_quality_gate_report.md` 已有可裁决结论
- `workflow_gate_report.md = pass`
- Diagnostics 和 Post-QC Guard 已回链本轮改动

如果代码还没稳定,先回到 `crc-gland-stage-implementation`。

## 写前必读

正式写文档前,必须先读:

1. 研究定标记录
2. `实现依据记录.md`
3. 00_阶段实现卡
4. `stage_definition_gate_report.md`
5. `crc_gland_segmentation_project/.trae/skills/实验执行文档编写规范.md`
6. `crc_gland_segmentation_project/.trae/skills/TCGA原始标杆对齐清单.md`
7. 至少 2 份真实 TCGA 原始学习说明文
8. `crc_gland_segmentation_project/.trae/skills/示例_学习型说明文_融合版.md`
9. `crc_gland_segmentation_project/.trae/skills/学习型说明文人工审稿清单.md`

## 默认交付物

- README
- implementation_status
- 对应交付对象的逐文件说明文（命名固定为“相对路径扁平化 + 原始后缀 + .md”，例如 `src_data_datasets.py.md`）
- “当前阶段为什么能pass以及下一步怎么看”文档

## 当前边界

这个 skill 只解释已经成立的实现,不负责证明代码正确。
它写进去的每个结论,都应该能同时回链到研究依据、实现依据记录、阶段边界、正式代码和真实运行证据。

## 门禁/审查

写学习型说明文前,至少要回链下面这些正式对象:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\coding_guards\[任务目录]\研究定标记录.md`
- `实现依据记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\coding_guards\[任务目录]\00_阶段实现卡.md`
- `runtime_check_report.md`
- `runtime_evidence.json`
- `code_quality_gate_report.md`
- `workflow_gate_report.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\实验执行文档编写规范.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_learning_docs.py`

## 红线

- 代码证据没出来就先补说明文
- 没有 `workflow_gate_report.md = pass` 就先补“本轮正式任务已通过”的说明文
- 只有口语化,没有来源锚点和物理证据
- 没有 `实现依据记录.md`,却试图在说明文里反向回忆“当时参考了什么”
- 把 Guard 留痕冒充学习型说明文
- 没有先列“本轮交付范围内正式对象清单”,就直接声称“说明文已覆盖本轮代码”
- 只写 `README.md` / `implementation_status.md`,却没有给新增正式 Python / YAML / CSV / 正式资产建立逐文件说明
