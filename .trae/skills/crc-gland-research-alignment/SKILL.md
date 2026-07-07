---
name: "crc-gland-research-alignment"
description: "正式编码前的研究定标 skill。先读计划、参考资料、论文和参考代码，再产出研究定标记录。"
---

# CRC Gland Research Alignment

## 正式角色

这个 skill 是正式研究定标入口,只在根目录 `d:\12_Medical_Image_Segmentation\Paper\.trae\skills\crc-gland-coding-guard\SKILL.md` 已裁决到 `研究` 时调用。

它负责把当前阶段进入编码前必须先读透的计划依据、论文依据、官方脚本依据和参考代码依据压成正式研究记录,并为后续阶段实现卡与 `实现依据记录.md` 提供第一批来源锚点。

## 边界/分层

- 本 skill 负责研究定标,不负责阶段锁定、Pre-check、正式编码、运行证据和说明文
- 本 skill 负责提取“为什么现在做这个”和“后续编码时必须继承哪些约束”
- 本 skill 不直接替代阶段实现卡
- 本 skill 不直接替代 `实现依据记录.md`,但必须为后者准备来源锚点和冻结项种子

## 状态口径

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking`: `not_started / blocked / partial / pass`

## 工程落点

研究阶段的正式工程落点固定为:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\coding_guards\[任务目录]\研究定标记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\runtime_checks\research_alignment_gate_report.md`

当前阶段只允许在这些研究产物里沉淀来源锚点和约束提取,不允许提前把工程落点写成正式代码实现。

## 目标

这个 skill 只做一件事:

> 在进入阶段锁定之前,先把当前阶段为什么现在要做、读了什么、提取出了什么硬约束、还有什么不能靠猜说清楚。

没有这一步,后面的阶段锁定和编码一律视为边写边猜。

全局固定顺序、状态口径与最终完成定义,以根目录 `crc-gland-coding-guard` 和项目内 `制度完成定义.md` 为准。

## 前提

- 如果规则体系还在重写,先回到 `crc-gland-skill-governance`
- 如果当前任务已经准备进入阶段锁定,但还没有研究定标记录,也要先回到这里

## 必读材料

### 1. 计划侧

必须先读:

1. `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
2. `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
3. `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
4. `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
5. `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
6. 当前阶段和上一阶段的正式协议与验收文件

### 2. 参考资料侧

必须继续读:

1. `结直肠腺体分割_正式参考资料/README.md`
2. `结直肠腺体分割_正式参考资料/00_文档与官方链接汇总.md`
3. 当前阶段直接相关的论文、官方脚本、参考代码

## 唯一交付物

本 skill 完成时,必须留下 2 类正式产物:

1. 研究定标记录
2. `research_alignment_gate_report.md`

研究定标记录至少回答 9 件事:

1. 当前阶段为什么现在必须先研究
2. 本轮直接依赖的已读文件是什么
3. 这些文件各自回答了什么问题
4. 从计划与协议中提取了哪些硬约束
5. 从参考资料 / 论文 / 官方脚本 / 参考代码中提取了哪些硬约束
6. 当前阶段边界初判是什么
7. 为什么现在不能直接进入下一个阶段
8. 后续阶段锁定必须写清哪些点
9. 当前研究结论到底是 `allow_stage_lock` 还是 `blocked`

另外还必须提前写清 3 类“后续编码种子”:

10. 后续编码时必须继承的冻结参数、split 边界、标签规则和评估前提
11. 后续 `实现依据记录.md` 至少要回链哪些论文、官方脚本、参考代码和计划章节
12. 哪些点只是工程收敛候选,后续不能冒充成论文直接结论

研究阶段不直接产出阶段实现卡,也不直接产出 `stage_definition_gate_report.md`。

这两个对象属于下一步“阶段锁定”,不是研究定标的交付物。

推荐用项目内模板起草:

- `crc_gland_segmentation_project/.trae/skills/模板R_研究定标记录.md`

写完研究定标记录后,必须立刻运行:

- `python b_class_auxiliary/tools/check_research_alignment_gate.py --research-record [研究定标记录相对路径] --output [b_class_auxiliary/runtime_checks/research_alignment_gate_report.md]`

只有当 `research_alignment_gate_report.md = pass`,研究阶段才允许被视为“已完成”。

## 进入阶段锁定的条件

只有同时满足下面条件,才允许从研究定标切到“阶段锁定”:

- 已读完计划和正式参考资料中的相关部分
- 已写清论文依据 / 官方依据 / 代码依据
- 已写清后续编码必须继承的冻结参数与实现依据种子
- 已写清为什么现在做这个,而不是下一个阶段
- 已形成研究定标记录
- `研究结论状态 = allow_stage_lock`
- `research_alignment_gate_report.md = pass`

## 门禁/审查

研究阶段至少要回链下面这些正式对象:

- `d:\12_Medical_Image_Segmentation\Paper\结直肠腺体分割_plan_优化版\01_实验执行\00_总览与规范\00_执行导航.md`
- `d:\12_Medical_Image_Segmentation\Paper\结直肠腺体分割_plan_优化版\01_实验执行\00_总览与规范\02_参数冻结总表.md`
- `d:\12_Medical_Image_Segmentation\Paper\结直肠腺体分割_正式参考资料\00_文档与官方链接汇总.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\模板R_研究定标记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\模板I_实现依据记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_research_alignment_gate.py`

## 进入编码阶段不是本 skill 的职责

研究完成后,下一步应该先进入“阶段锁定”:

1. 用 `模板0_阶段实现卡.md` 起草正式输出名 00_阶段实现卡
2. 运行 `b_class_auxiliary/tools/check_stage_definition_gate.py`
3. 只有当 `stage_definition_gate_report.md = pass`,才允许继续 Pre-check 和正式编码

## 红线

- 还没形成研究定标记录就直接进入阶段锁定
- 没有跑 `check_research_alignment_gate.py`,就把研究阶段口头写成“已完成”
- 把研究定标记录写成阶段实现卡的缩水版,却没有把“读了什么、提取了什么约束”说清
- 在研究阶段直接口头宣布“阶段边界已锁定”
- 只写“参考某论文/某仓库”,但不写章节、公式、commit、文件落点
- 研究阶段顺手开始写说明文或正式代码
