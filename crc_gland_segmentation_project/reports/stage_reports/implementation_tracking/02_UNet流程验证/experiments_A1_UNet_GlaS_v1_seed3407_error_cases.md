# experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md

## 这份文件的定位

这份说明文对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`。

如果 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 是数值入口，那么这份文件就是“错例观察入口”。

你可以把它理解成“当前 run 的坏例子索引页”。

## 这个文件是干什么的

- 负责把失败类型写成可读摘要
- 负责把 worst cases 回指到 overlay 路径
- 负责给 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 的 `major_failure_modes` 提供上游依据

## 作用

它是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 与 overlay 目录之间的错例索引页。

说白了，它在回答:
当前这次 run 最值得警惕的失败模式是什么。

## 当前这个文件说明了什么

当前文件已经真实记录:

1. `failure_taxonomy_version=failure_taxonomy_v1`
2. `testA` 里当前主要是 `adhesion_merge`
3. `testB` 里已经出现 `boundary_over_smooth`
4. worst cases 都保留了 overlay 回指

这说明当前阶段不是只有表格，没有肉眼入口。

## 阶段协议回链卡片

- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 代码参考: `../../../../src/eval/export_visuals.py`
- 上游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
- 下游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
- 论文依据: `Metrics Reloaded: recommendations for image analysis validation`

## 这张表/这个文件长什么样

当前文件主要分成 3 层:

1. 头部元信息
2. `Split Summary`
3. `Worst Cases`

`Worst Cases` 一行里当前至少保留:

1. `split_role`
2. `sample_id`
3. `failure_type`
4. `objdice`
5. `dice`
6. `boundary_f1`
7. `overlay`

## 这个文件长什么样

它由头部元信息、`Split Summary` 和 `Worst Cases` 三层组成。
前两层负责回答“整体哪里错得多”，最后一层负责把人工复查直接带回具体 overlay 文件。

## 当前真实结果

| 项目 | 当前真实结果 | 说明 |
|---|---|---|
| `analyzed_sample_count` | `4` | 当前本地联通检查分析了 4 个样本 |
| `testA` 主失败模式 | `adhesion_merge` | 说明预测连通域有黏连风险 |
| `testB` 新失败模式 | `boundary_over_smooth` | 说明边界层面仍有明显问题 |
| overlay 回指 | 已真实回到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/` | 让人工复查不断链 |

## 这些列/字段分别是什么意思

这里最关键的字段可以分成 3 组:

1. 头部字段: `failure_taxonomy_version`、`source_assets`、`analyzed_sample_count`
2. split 统计字段: 每种 `failure_type` 的计数
3. worst-case 字段: `sample_id`、`objdice`、`dice`、`boundary_f1`、`overlay`

换句话说，这份文件既给了全局概览，也给了具体入口。

## 这个文件没说明什么

它没有直接说明:

1. 为什么这些错误会发生在某个 epoch
2. 模型结构是否需要调整
3. 外部 benchmark 下是否也会出现同样问题

这些问题要去联读:

- `src_models_unet.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`
- `当前阶段为什么能pass以及下一步怎么看.md`

## 和上下游怎么衔接

- 上游是 `../../../../src/eval/export_visuals.py` 结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 生成失败类型与 overlay 回指
- 下游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 直接消费 `major_failure_modes`，人工复核再沿 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/` 继续看图

## 当前最该注意的一点

不要把 `failure_type` 当成最终科研结论。

当前它只是 stage02 首轮流程排雷用的工程观察标签。
但这不代表它不重要，因为下游排查和人工审阅都会先看这里。

## 如何手工验证这个文件的正确性

最短验证步骤:

1. 检查 `Split Summary` 的计数是否和 sample 数量一致
2. 检查 `Worst Cases` 的 `sample_id` 能否在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 或 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 里找到
3. 检查每一条 `overlay` 路径是否真实存在
4. 检查 `major_failure_modes` 是否能和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 对上

通过标准:

- `analyzed_sample_count=4`
- 至少回填 `adhesion_merge` 和 `boundary_over_smooth`
- `overlay` 路径真实存在
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 的 `major_failure_modes` 不和这里冲突

## 常见问题

- 不要把 `Worst Cases` 误读成全部失败样本；它只列最差的一小批
- 不要因为当前标签是启发式，就把这份文件当成可删除辅助页
- 不要跳过 overlay 路径，真正的人工复核都要回到图上

## 建议联读

- `src_eval_export_visuals.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
