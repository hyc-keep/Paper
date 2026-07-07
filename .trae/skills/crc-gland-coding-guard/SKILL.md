---
name: "crc-gland-coding-guard"
description: "结直肠腺体分割项目的唯一总入口。只负责判断当前该进哪个阶段。"
---

# CRC Gland Coding Guard

## 正式角色

这个 skill 只负责一件事:

> 用唯一状态机判断当前任务应该停在 `治理 / 研究 / 阶段锁定 / Pre-check / 编码 / 运行证据 / 代码质量 / 总放行 / 说明文档 / 交付前清理` 的哪一步。

它不负责展开模板正文,也不负责替代 gate report。

## 边界/分层

根目录总入口只负责路由,不直接替代下面这些对象:

- 项目内导航: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\00_技能体系导航.md`
- 完成定义: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\制度完成定义.md`
- 模板总规范: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\论文实验项目文档编写规范_完整版.md`
- 学习型说明文规程: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\实验执行文档编写规范.md`
- TCGA 对齐清单: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\TCGA原始标杆对齐清单.md`
- 人工审稿清单: `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\.trae\skills\学习型说明文人工审稿清单.md`

这些文件必须和总入口同向协同,但都没有独立放行权。

必须始终分清 3 层对象:

- `skill 路由层`: 只决定当前该去哪一步
- `非 skill 门禁层`: `research / stage definition / precheck / runtime / code quality`
- `任务总放行件`: `workflow_gate_report.md`

还必须额外分清:

- `编号阶段`: `01_数据协议 / 02_UNet流程验证 / ...`
- `skill 工作流阶段`: `治理 / 研究 / 阶段锁定 / Pre-check / 编码 / 运行证据 / 代码质量 / 总放行 / 说明文档 / 交付前清理`

禁止把“编号阶段下一步是什么”和“当前 turn 在 skill 工作流里下一步必须补什么”混成一句话。

凡涉及什么叫 `pass / partial / fail` 以及什么时候允许进入下一步,以项目内 `制度完成定义.md` 为准; 本 skill 只负责状态机路由裁决。

## 根目录 skill 分工

根目录只有本 skill 是路由总入口。其余 skill 都从属于本 skill 的裁决，不得自封为并列入口:

- `crc-gland-research-alignment`: 研究定标阶段被调用
- `crc-gland-stage-implementation`: 编码阶段被调用
- `crc-gland-learning-doc`: 说明文阶段被调用
- `crc-gland-skill-governance`: 仅在改规则体系本身时被调用
- `standard-md-rewrite`: 仅负责 `结直肠腺体分割_plan_优化版/01_实验执行` 下 plan 正文的严格重写协议,属于计划文档重写工具,不参与代码工作流路由,也不替代本 skill 判断当前该去哪一步

## 状态口径

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking`: `not_started / blocked / partial / pass`

禁止把这三套状态混成一个总状态。

## 唯一裁决顺序

| 当前状态 | 进入条件 | 阻断条件 | 必需产物 | 必跑脚本 | 下一状态 |
| --- | --- | --- | --- | --- | --- |
| `治理` | 当前正在改 `.trae/skills`、导航、模板总规范或规程 | 还说不清哪个文件说了算 | 无 | `b_class_auxiliary/tools/check_formal_stage_docs.py` | `研究` |
| `研究` | 已确定规则体系稳定,准备进入某个正式阶段 | 还没读透 `结直肠腺体分割_plan_优化版` 与 `结直肠腺体分割_正式参考资料` | 研究定标记录、`research_alignment_gate_report.md` | `b_class_auxiliary/tools/check_research_alignment_gate.py` | `阶段锁定` |
| `阶段锁定` | `research_alignment_gate_report.md = pass` 且 `研究结论状态 = allow_stage_lock` | 还没有正式阶段边界 | 阶段实现卡、`stage_definition_gate_report.md` | `b_class_auxiliary/tools/check_stage_definition_gate.py` | `Pre-check` |
| `Pre-check` | `stage_definition_gate_report.md = pass` | 还没写清前置依据、阶段门控、代码库现状和工程落点 | `pre_check_extraction.md`、`stage_gate_check.md`、`current_codebase_状态.md`、`Pre-check Guard`、`precheck_doc_gate_report.md` | `b_class_auxiliary/tools/check_precheck_docs.py` | `编码` |
| `编码` | `precheck_doc_gate_report.md = pass` | 阶段边界未锁定或 Pre-check 未通过 | 正式代码、配置、正式资产改动、`实现依据记录.md` | 无 | `运行证据` |
| `运行证据` | 本轮存在正式代码、配置或正式资产改动 | 还没有真实运行画像物理证据 | `runtime_check_report.md`、`runtime_evidence.json`、`runtime_check.log` | `b_class_auxiliary/tools/run_minimal_runtime_check.py` | `代码质量` |
| `代码质量` | 已拿到 runtime 三件套 | 若当前是完整训练画像, runtime 仍未给出 `shape / dtype / loss / finite / backward / optimizer.step`; 若当前编号阶段=`01_数据协议` 且本轮目标仅是 `train entrypoint preflight`, 则必须显式声明 `runtime_profile = data_protocol_preflight`, 并证明正式数据链与入口预飞成立,同时明确这不等于完整训练链成立 | `code_quality_gate_report.md` | `b_class_auxiliary/tools/check_code_quality_gate.py` | `总放行` |
| `总放行` | 已确认代码、runtime、code quality 都成立,准备裁决本轮正式任务是否通过 | 任一前置阶段仍不是 `pass` | `workflow_gate_report.md` | `b_class_auxiliary/tools/enforce_workflow_gate.py` | `说明文档` |
| `说明文档` | `workflow_gate_report.md = pass` 且代码、runtime、code quality 已稳定 | `workflow_gate_report.md` 还不是 `pass` | 学习型说明文产物 | `b_class_auxiliary/tools/check_learning_docs.py` | `交付前清理` |
| `交付前清理` | 仅在准备把项目打包交付给别人时进入; 全部编号阶段说明文已成立 | 尚未准备交付,或仍有未收口阶段 | A/B/C 三分清理结论留痕 | 无 | 完成 |

## 六问路由法

每次进入任务只问下面 6 个问题:

1. 现在是不是还在改 skill、导航、模板或规程本身?
2. 如果不是,研究定标记录和 `research_alignment_gate_report.md` 是否已经成立?
3. 如果研究已成立,阶段实现卡和 `stage_definition_gate_report.md` 是否已经成立?
4. 如果准备编码,`precheck_doc_gate_report.md` 是否已经是 `pass`?
5. 如果准备宣称本轮正式任务通过,是否已经完成总放行裁决并生成 `workflow_gate_report.md`?
6. 如果准备写学习型说明文,`workflow_gate_report.md` 是否已经是 `pass`?

只要某一问回答为否,就必须停在更早状态。

## 进入任务前的显式遍历

每次开始任务、恢复任务或用户只说“继续”时,必须先显式给出“本轮已遍历文件清单”,再做阶段判断。

最小清单规则:

- 如果当前在 `治理`,至少列出: `crc-gland-skill-governance`、`crc-gland-coding-guard`、`00_技能体系导航.md`、`制度完成定义.md`、`项目阶段推进指令使用手册.md`
- 如果当前在正式阶段工作流,除根目录总入口外,还必须列出当前阶段对应的 skill、当前阶段协议/计划文件、当前阶段最近一次 gate report
- 如果某个关键文件还没读,就先读,不要先下阶段结论

路由输出必须把下面两件事分开写清:

- `当前编号阶段`
- `当前 skill 工作流阶段`

只要当前仍在 `治理`,或当前编号阶段的 formal artifact / gate 还没收口,就禁止在结论里提“下一编号阶段现在可以开始”。

## 强制规则

- 研究未通过,不允许进入阶段锁定
- 阶段锁定未通过,不允许进入 Pre-check
- Pre-check 未通过,不允许进入正式编码
- 没有先显式展示“本轮已遍历文件清单”,不允许给出阶段路由结论
- 编号阶段允许进入下一阶段,不等于当前 turn 可以跳过 `运行证据 -> 代码质量`
- 没有真实 runtime 三件套,不允许宣称代码成立
- 如果当前编号阶段=`01_数据协议`,且本轮正式改动只服务 `train entrypoint preflight`,则 `运行证据 -> 代码质量` 允许按 `data_protocol_preflight` 画像裁决; 这类 `pass` 只代表正式数据链与训练入口预飞成立,不代表完整训练链已经成立
- 如果本轮新增或修改了正式代码、配置或正式资产,必须同时留下 `实现依据记录.md`,把每个正式文件对应的计划条款、论文/参考代码、冻结参数和工程收敛决定写清
- 这里的“每个正式文件”按逐文件口径执行: 每个被改动的正式 `py / yaml / yml / json / toml / csv / md` 文件都必须在 `实现依据记录.md` 里单独回链
- 没有 `code_quality_gate_report.md = pass`,不允许进入总放行
- 没有 `workflow_gate_report.md = pass`,不允许进入学习型说明文
- 没有 `workflow_gate_report.md = pass`,不允许宣称本轮正式任务整体通过
- `raw asset 可读` 不等于 `正式训练链已成立`
- `模板层` 不允许反向充当总入口
- 如果本轮新增或修改了正式代码、配置或正式资产,即使编号阶段 gate 已显示 `next_action = enter_next_stage`,当前 turn 也必须先补完 `运行证据 -> 代码质量`,再汇报“可进入下一编号阶段”
- 如果当前仍在 `01_数据协议`,且 `data_stage_pass / handoff_ready / preflight_pass` 任一不是 `True`,禁止提议进入 `02_UNet流程验证`
- 如果当前仍在 `01_数据协议`,即使 `data_protocol_preflight` 已经 `pass`,也不允许把这个结论扩写成完整训练链 `forward / loss / backward / optimizer.step` 已成立

## 门禁/审查

治理层至少要能回链下面这些共享门禁标记:

- `00_技能体系导航.md`
- `制度完成定义.md`
- `论文实验项目文档编写规范_完整版.md`
- `实验执行文档编写规范.md`
- `TCGA原始标杆对齐清单.md`
- `学习型说明文人工审稿清单.md`
- `Guard 留痕`
- `模板R_研究定标记录.md`
- `模板0_阶段实现卡.md`

如果当前正在修改 skill / 导航 / 模板总规范 / 规程,必须额外运行:

- `d:\12_Medical_Image_Segmentation\Paper\crc_gland_segmentation_project\b_class_auxiliary\tools\check_formal_stage_docs.py`

## 红线

- 不允许跳过研究定标直接写正式代码
- 不允许把阶段实现卡冒充成“阶段已锁定”
- 不允许在 `stage_definition_gate_report.md` 不是 `pass` 时进入正式编码
- 不允许在 `precheck_doc_gate_report.md` 不是 `pass` 时进入正式编码
- 不允许未显式展示本轮已遍历的 skill / 导航 / 规程 / 当前阶段文件,就直接说“现在到哪一步了”
- 不允许正式代码已经改了,却没有同步留下 `实现依据记录.md`
- 不允许改了多个正式 `py` 文件,却把它们合并成一条无法逐文件审计的依据记录
- 不允许只有 markdown 报告、没有 `runtime_evidence.json` 就宣称代码证据成立
- 不允许把原始样本可读性冒充成 `forward / loss / backward / optimizer.step` 已成立
- 不允许把“实现依据留痕”拖到学习型说明文阶段才补
- 不允许在代码证据没出来前先补长文
- 不允许没有 `workflow_gate_report.md` 就宣称本轮正式任务整体通过
- 不允许用“`01` 已结束 / `02` 可进入”掩盖当前 turn 仍未补齐 runtime/code-quality 的事实
- 不允许在 `治理` 未结束,或当前编号阶段的 formal artifact / gate 未收口时,顺嘴提下一编号阶段
- 不允许把“计划要求的项目内容”和“AI 辅助检查内容”写进同一个文件; 出现混合件必须先拆成纯 A 类和纯 B 类两个文件
- 不允许把计划未点名、未在 `实现依据记录.md` 登记归类(A/B/C)的文件当成项目正式交付对象
