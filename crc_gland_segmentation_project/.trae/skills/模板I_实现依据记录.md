# 实现依据记录

## 0. 归档/副本说明

- 当前文件角色:
- 当前对应阶段:
- 当前阶段归档路径:
- 如果当前文件是根路径副本,必须显式写:
  - `当前文件角色: 当前阶段副本`
  - `当前阶段归档路径: reports/stage_reports/implementation_tracking/[阶段名]/实现依据记录.md`
  - `历史阶段归档路径:` 列表
- 如果当前文件是阶段目录下的归档版,必须显式写:
  - `当前文件角色: 阶段归档版` 或 `重建归档版`
  - 当前归档为什么存在
  - 如果不是原始首发版本,必须诚实写明“这是重建归档版,不是逐字原件”
- 红线:
  - 不允许只保留根路径单文件并跨阶段滚动覆盖
  - 不允许进入新阶段编码时覆盖旧阶段唯一依据记录
  - 每个编号阶段都必须在 `reports/stage_reports/implementation_tracking/[阶段名]/实现依据记录.md` 留独立归档
  - 根路径 `b_class_auxiliary/runtime_checks/实现依据记录.md` 只能作为当前阶段副本,不能作为跨阶段唯一真本

## 1. 角色/入口
- 当前阶段:
- 当前任务:
- 当前记录只负责:
- 当前记录不负责:

## 2. 边界/分层

- 只有当 `precheck_doc_gate_report.md = pass` 并准备进入正式编码时,才允许创建或更新当前记录
- 当前记录属于编码阶段正式产物,不是学习型说明文
- 只要本轮改了正式代码、配置或正式资产,就必须同步维护当前记录
- 如果本轮没有正式改动,当前记录可以标记为 `not_applicable`,但不能伪造内容

## 3. 状态口径

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking`: `not_started / blocked / partial / pass`

这里要明确写清:

- 当前编码是否允许开始,看 `Stage Gate`
- 当前实现依据留痕是否已经齐全,看 `implementation_tracking`
- 当前 runtime / code quality 是否已经成立,看 `Diagnostics / Post-QC`

## 4. 本轮直接依赖的已读文件

| 类型 | 文件 | 章节/定位 | 提取出的硬约束 | 映射到哪些正式文件 |
| --- | --- | --- | --- | --- |
| 计划 |  |  |  |  |
| 论文/文献 |  |  |  |  |
| 官方脚本/参考代码 |  |  |  |  |
| 工程冻结规则 |  |  |  |  |

## 5. 正式文件到依据的回链

这里按逐文件填写,不要合并:

- 每个被改动的正式 `py / yaml / yml / json / toml / csv / md` 文件都单独占一行
- 同一个模块下改了 3 个 `py`,就写 3 行
- 不要求每个文件再单独建一份 md,但要求当前表逐文件可审计

| 正式文件 | 直接计划依据 | 论文/文献依据 | 官方脚本/参考代码依据 | 本轮采用的实现动作 | 为什么不用相邻方案 |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## 6. 参数与规则冻结回填

| 参数/规则 | 当前值 | 来源文件与章节 | 最终落点 |
| --- | --- | --- | --- |
|  |  |  |  |

## 7. 工程落点

本轮至少要写清下面这些工程落点中的哪些对象被修改:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\scripts`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\src`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\configs`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\reports`

如果本轮引用了模板或规程,也要写清:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\模板I_实现依据记录.md`
- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\制度完成定义.md`

## 8. 门禁/审查回链

当前记录至少要准备回链到:

- `b_class_auxiliary/tools/run_minimal_runtime_check.py`
- `b_class_auxiliary/tools/check_code_quality_gate.py`
- `b_class_auxiliary/tools/enforce_workflow_gate.py`

如果本轮是在治理阶段补规则,还要额外回链:

- `b_class_auxiliary/tools/check_formal_stage_docs.py`

## 9. 诚实边界
- 哪些结论是计划或论文直接规定的:
- 哪些结论是参考代码直接给出的:
- 哪些结论是工程收敛决定,不是论文直接结论:
- 哪些点当前还没有证据,不能宣称已经成立:

## 10. 本轮未采用但需要明确拒绝的方案

| 未采用方案 | 为什么没用 | 对应依据 |
| --- | --- | --- |
|  |  |  |

## 11. 最小自检

- 检查每个正式文件是否都能回链到 `结直肠腺体分割_plan_优化版/01_实验执行` 的具体文件和章节
- 检查每个被改动的正式 `py` 文件是否都在“正式文件到依据的回链”表里单独出现
- 检查每个论文/文献/参考代码条目是否都写清了文件、章节、函数或脚本位置
- 检查所有冻结参数是否都写清了来源与最终落点
- 检查哪些地方只是工程收敛决定,已经诚实标注,没有冒充成论文直接结论
