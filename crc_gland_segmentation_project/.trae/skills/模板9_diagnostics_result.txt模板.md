# 模板9: diagnostics_result.txt 模板

> **使用场景**: 编码后或模板修订后记录最小 diagnostics 与协议级质检结果。
> **调用顺序**: 先看 `00_技能体系导航.md`,并在本轮实际修改完成后填写
> **与中央门禁的关系**: 本模板负责把 Post-QC 的最小检查结果压成一份可复查的纯文本记录; 它不是一句“已检查”备注,也不能脱离 `Post-QC Guard` 单独充当最终结论
> **来源/依据**: 继承中央 `crc-gland-coding-guard` 的 Post-QC 最小检查清单,并服务 `模板10_Post-QC Guard.md` 的协议级质检表
> **工程落点**: 正式输出到 `b_class_auxiliary/coding_guards/[任务目录]/diagnostics_result.txt`,供 `Post-QC Guard`、`learning_doc_gate_report.md` 和 `formal_doc_gate_report.md` 回链
> **职责边界**: 这里只记录 diagnostics 最小结果,不替代 `Post-QC Guard` 的最终裁决

---

这份模板最容易出现两个问题:
- 明明本轮只是文档/模板治理任务,却被迫把所有协议项都写成 `pass/fail`
- 明明某项检查根本没做,却为了看起来完整硬写 `pass`

更科学的写法是:
- 做了且通过: 写 `pass`
- 做了但有缺口: 写 `partial` 或 `fail`
- 本轮任务天然不涉及: 写 `not_applicable`

这样后面的 `Post-QC Guard` 才能如实解释本轮任务到底检查到了哪一层

```text
[Code Syntax]
- py_compile: pass / partial / fail / not_applicable
- import_check: pass / partial / fail / not_applicable

[Config Check]
- yaml_valid: pass / partial / fail / not_applicable
- path_exists: pass / partial / fail / not_applicable

[Runtime Check]
- smoke_run_pass: pass / partial / fail / not_applicable
- dataloader_batch_check_pass: pass / partial / fail / not_applicable
- tensor_shape_dtype_pass: pass / partial / fail / not_applicable
- loss_finite_pass: pass / partial / fail / not_applicable
- grad_step_pass: pass / partial / fail / not_applicable

[Protocol Check]
- version_chain_complete: pass / partial / fail / not_applicable
- naming_rule_pass: pass / partial / fail / not_applicable
- stage_boundary_pass: pass / partial / fail / not_applicable
- code_quality_gate_pass: pass / partial / fail / not_applicable
- learning_doc_gate_pass: pass / partial / fail / not_applicable
- formal_doc_gate_pass: pass / partial / fail / not_applicable
- traceability_card_complete: pass / partial / fail / not_applicable
- best_selector_unique: pass / partial / fail / not_applicable
- threshold_source_valid: pass / partial / fail / not_applicable
- glas_split_export_pass: pass / partial / fail / not_applicable
- crag_export_pass: pass / partial / fail / not_applicable
- metric_crosscheck_status: pass / partial / fail / not_applicable
- result_tag_aggregation_pass: pass / partial / fail / not_applicable
- external_adaptation_record_pass: pass / partial / fail / not_applicable

[Conclusion]
- diagnostics_result: pass / partial / fail / not_applicable
- blocker:
```

**红线提醒:**
- `not_applicable` 不是偷懒,而是“本轮任务客观不涉及这一项”
- 只要写了 `partial / fail`, `blocker` 就不能空着
- 如果本轮新增/修改了正式代码对象,`[Runtime Check]` 里的 5 个运行项和 `code_quality_gate_pass` 都不能写 `not_applicable`
- 如果本轮新增/修改了正式代码、配置或正式资产对象,`learning_doc_gate_pass` 就不能写 `not_applicable`
- 如果本轮新增/修改了 `.trae/skills/*.md` 正式模板/规程,或修改了 `01_实验执行` 下的正式协议文档,`formal_doc_gate_pass` 就不能写 `not_applicable`
- 如果本轮新增/修改了正式脚本说明文,`traceability_card_complete` 不能写 `not_applicable`
- 如果本轮改了评估链、结果表或 external 适配层,对应检查项就不能再写 `not_applicable`
