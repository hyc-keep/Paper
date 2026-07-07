# 模板10: Post-QC Guard

> **使用场景**: 编码或正式模板修订结束后,把 Diagnostics、协议级质检和实际改动与 Pre-check 对照起来。
> **调用顺序**: 先看 `00_技能体系导航.md`,并确保 `diagnostics_result.txt` 已先填写
> **与中央门禁的关系**: 本模板负责形成本轮任务的最终质检结论; 它必须回链 `Pre-check Guard` 与 `diagnostics_result.txt`,不能脱离前后文单独宣告 `pass`
> **来源/依据**: 继承中央 `crc-gland-coding-guard` 的 Post-QC 结构要求,并消费 `模板9_diagnostics_result.txt模板.md`、`learning_doc_gate_report.md` 与 `formal_doc_gate_report.md`
> **工程落点**: 正式输出到 `b_class_auxiliary/coding_guards/[任务目录]/YYYYMMDD_[任务]_post_qc_guard.md`,作为每轮任务的最终质检汇总件
> **职责边界**: 这里负责最终回链、最终边界和最终状态,但不替代 `Pre-check Guard` 或两个门禁报告本身

---

这份模板不是“改完以后写个总结”。

它真正要回答的是:
- 本轮实际做的事有没有偏离 Pre-check 承诺
- 哪些协议级检查做了,哪些本轮天然不适用
- 每个变更对象到底对应哪份学习型说明文
- 最终为什么是 `pass / partial / fail / not_applicable`
- 后面的人只看这份文件,能不能快速回溯本轮真实改动和剩余风险

```markdown
# Post-QC Guard

## 1. 本次任务与 Pre-check 对照
- 任务名:
- 当前阶段:
- 阶段实现卡路径:
- 阶段锁定门禁结论:
- Pre-check 预期:
- 实际完成:

## 2. 实际创建/修改文件

| 文件 | 动作 | 是否符合预期 | 备注 |
|------|------|-------------|------|

## 3. 协议级质检结果

| 检查项 | 结果 | 物理证据 |
|-------|------|---------|
| 最小 smoke run | pass / partial / fail / not_applicable | [运行命令 + `runtime_check_report.md` 路径 + 输出日志路径 + 关键结果] |
| dataloader batch 检查 | pass / partial / fail / not_applicable | [`runtime_check_report.md` 路径 + batch 样本路径/索引 + tensor shape / dtype / unique 值] |
| tensor shape / dtype 检查 | pass / partial / fail / not_applicable | [`runtime_check_report.md` 路径 + 输入/标签/logits 的 shape / dtype / 数值范围] |
| loss finite 检查 | pass / partial / fail / not_applicable | [`runtime_check_report.md` 路径 + loss 值 + 是否 finite + 日志路径] |
| backward / optimizer.step 检查 | pass / partial / fail / not_applicable | [`runtime_check_report.md` 路径 + 梯度反传或单步优化的物理证据] |
| 代码质量门禁 | pass / partial / fail / not_applicable | [`code_quality_gate_report.md` 路径 + 关键结论] |
| 版本链完整 | pass / partial / fail / not_applicable | [文件/字段] |
| 学习型说明文门禁 | pass / partial / fail / not_applicable | [`learning_doc_gate_report.md` 路径 + 关键结论] |
| 正式模板文档门禁 | pass / partial / fail / not_applicable | [`formal_doc_gate_report.md` 路径 + 关键结论] |
| 学习型说明文人工审稿 | pass / partial / fail / not_applicable | [`学习型说明文人工审稿清单.md` + `TCGA原始标杆对齐清单.md` 路径 + 审稿对象 + 关键结论] |
| 结构化溯源卡片完整 | pass / partial / fail / not_applicable | [说明文路径 + 缺失字段或通过证据] |
| `best_selector` 唯一 | pass / partial / fail / not_applicable | [文件/字段] |
| `threshold_source` 合法 | pass / partial / fail / not_applicable | [文件/字段] |
| `GlaS TestA/TestB` 分开导出 | pass / partial / fail / not_applicable | [文件/字段] |
| `result_tag / aggregation` 一致 | pass / partial / fail / not_applicable | [文件/字段] |
| `metric_crosscheck` 状态 | pass / partial / fail / not_applicable | [文件/字段] |

## 4. 阶段说明文档更新清单
- 更新了哪些文档:
- 每份文档回答的核心对象:

## 4.1 对象-说明文映射回填

| 本轮变更对象 | 归类 | 归类依据 | 对象级说明文 | 入口同步项 | 实际动作 | 结果 |
|-------------|------|---------|-------------|-----------|---------|------|
| `[文件路径]` | `A / B / C` | `[计划条款号 / 参考资料出处 / 归 B 或归 C 的理由]` | `[implementation_tracking/对象说明文路径] / not_applicable` | `[reports/stage_reports/implementation_tracking/阶段名/README.md 或 implementation_status.md 的单个路径] / not_applicable` | `create / update / append_version / not_applicable` | [物理证据或原因] |

补充规则:

- 只有 A 类对象才允许填写真实 `对象级说明文`
- B / C 类对象的 `对象级说明文` 固定写 `not_applicable`
- `README.md` / `implementation_status.md` 只允许以真实阶段入口文档路径的形式出现在 `入口同步项`,不能冒充对象级说明文
- 若某对象本轮只触发阶段入口同步,`对象级说明文` 可写 `not_applicable`,但必须在 `结果` 里写清为什么只需要入口同步
- `入口同步项` 一行只能填一个路径; 如果两个入口文档都改了,优先填写主入口路径,并在 `结果` 里说明另一份也已同步
- 这里的 A / B / C 归类必须与 `Pre-check Guard`、`制度完成定义.md` 和 `实现依据记录.md` 一致

## 4.2 与 Pre-check 的差异说明
- 预期中但未完成:
- 实际新增但 Pre-check 未写到:
- 是否越界:

## 4.3 学习型说明文人工审稿回填
- 审稿清单: `.trae/skills/学习型说明文人工审稿清单.md`
- TCGA原始标杆清单: `.trae/skills/TCGA原始标杆对齐清单.md`
- 对照示范稿: `.trae/skills/示例_学习型说明文_融合版.md`
- 审稿对象:
  - `[implementation_tracking/文档路径]`
- 审稿结论: `pass / partial / fail / not_applicable`
- 本轮最关键的通过证据:
  - [具体章节 + 具体表述 + 为什么说明已经讲透]
- 本轮仍需补强的问题:
  - [若为 `partial / fail`,写最严重缺口; 若为 `pass / not_applicable`,写 `无` 或原因]

## 5. Diagnostics 结果
- 结论:
- 剩余问题:

## 5.1 关键回链
- 阶段卡正式输出名 00_阶段实现卡.md 路径:
- 阶段锁定门禁报告 stage_definition_gate_report.md 路径:
- `Pre-check Guard` 路径:
- `实现依据记录.md` 路径:
- `diagnostics_result.txt` 路径:
- `runtime_check_report.md` 路径:
- `code_quality_gate_report.md` 路径:
- `learning_doc_gate_report.md` 路径:
- `formal_doc_gate_report.md` 路径:
- `学习型说明文人工审稿清单.md` 路径:
- 如有 `metric_crosscheck` 或额外 note,路径:

## 6. 最终状态
- Final Status: `pass / partial / fail / not_applicable`
- 原因:
```

**怎么判 `not_applicable`:**
- 本轮是文档/模板治理任务,没有修改评估链、结果汇总表或 external 适配层时,相关协议检查允许写 `not_applicable`
- 只有当本轮没有新增/修改 `src/`、`scripts/`、`tools/`、`configs/`、`external/` 下的正式对象时,代码质量相关检查项才允许写 `not_applicable`
- 如果本轮没有新增正式对象,且已有学习型说明文也无需追加版本记录,对象-说明文映射表里的对应行也允许写 `not_applicable`
- 只有当本轮不存在需要进入学习型说明文映射的正式对象时,`学习型说明文门禁` 才允许写 `not_applicable`
- 只有当本轮不存在正式模板/规程/协议文档改动时,`正式模板文档门禁` 才允许写 `not_applicable`
- 只有当本轮没有新建/重写学习型说明文主体,或本轮根本没有需要进入 `implementation_tracking` 的正式对象时,`学习型说明文人工审稿` 才允许写 `not_applicable`
- 但必须把“不适用的原因”写进 `物理证据` 一列,不能只留下空白
- 如果某对象被判为 B / C 类,对象映射表里也要保留该行,并把 `对象级说明文` 写成 `not_applicable`

**红线提醒:**
- 如果本轮实际改动已经超出阶段卡正式输出名 00_阶段实现卡.md 或阶段锁定门禁报告 stage_definition_gate_report.md 的锁定边界,这里必须显式写成越界
- 如果实际改动超出了 `Pre-check Guard` 的边界,这里必须显式写出,不能伪装成“符合预期”
- 如果本轮存在正式代码、配置或正式资产改动,`实现依据记录.md` 不能缺失,也不能只留空壳
- 如果本轮存在正式代码改动,`最小 smoke run / batch / tensor / loss / backward / 代码质量门禁` 这些行不能缺失,也不能集体写成 `not_applicable`
- 如果 `diagnostics_result.txt` 里存在 `partial / fail`,这里的最终状态通常不能直接写 `pass`
- 如果 `学习型说明文人工审稿` 还是 `partial / fail`,这里的最终状态通常也不能直接写 `pass`
- `Final Status` 不能只靠主观判断,必须由表格里的实际检查结果支撑
