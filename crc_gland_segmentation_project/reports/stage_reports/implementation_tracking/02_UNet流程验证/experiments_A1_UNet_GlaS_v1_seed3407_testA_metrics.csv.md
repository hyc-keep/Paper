# experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 已经写了 `testA_objdice`，为什么还要单独解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`？”

因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 只给摘要。
当前这份文件才是 `TestA` split 的正式原始结果表。

## 这个文件是干什么的

- 这份资产对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`。
- 它负责把 `TestA60` 的 sample 行和 aggregate 行一起落盘。
- 它回答的问题不是“这次 run 大概怎么样”，而是“TestA 每个样本和整体现实结果分别是多少”。

你可以先把它想成 `TestA` 的正式分账单。

## 当前这个文件说明了什么

当前这张表最关键的现实信息有 4 层:

1. `row_type=sample` 的逐样本结果
2. `row_type=aggregate` 的 split 汇总结果
3. `image_path`、`mask_path`、`pred_path` 的物理回指
4. `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff` 这一组正式指标列

说白了，没有这张表，后面的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 都会缺少最硬的上游依据。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 代码参考: `../../../../scripts/test.py`
- 上游实现: `../../../../src/eval/run_eval.py`
- 关联资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
- 论文依据: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`

## 这张表/这个文件长什么样

当前表头固定为:

1. `row_type`
2. `sample_id`
3. `split_role`
4. `sample_count`
5. `image_path`
6. `mask_path`
7. `pred_path`
8. `loss`
9. `loss_bce`
10. `loss_dice`
11. `objdice`
12. `dice`
13. `iou`
14. `f1`
15. `boundary_f1`
16. `hd95`
17. `object_hausdorff`

当前真实样例里:

- `GlaS_official_testA_testA_1` 的 `objdice=0.04433418558851121`
- `GlaS_official_testA_testA_10` 的 `objdice=0.12926947764676255`
- aggregate `objdice=0.08680183161763688`

## 当前真实结果

最值得直接记住的结果有 5 条:

| 项目 | 当前真实结果 | 为什么重要 |
|---|---|---|
| `sample_count` | `2` | 当前本地 CPU 联通检查只抽样导出 2 个 TestA 样本 |
| `aggregate objdice` | `0.08680183161763688` | 后续 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 都回填这个值 |
| `aggregate dice` | `0.32716668323024445` | 说明像素级和对象级结果不能混看 |
| `aggregate boundary_f1` | `0.5096702201939791` | 给边界观察面提供正式数值入口 |
| `pred_path` | 已真实回指 `predictions/testA/*` | 让可视化和错例回溯不断链 |

## 这些列/字段分别是什么意思

这里的列至少分成 4 组职责:

1. 身份列: `row_type`、`sample_id`、`split_role`
2. 路径列: `image_path`、`mask_path`、`pred_path`
3. 损失列: `loss`、`loss_bce`、`loss_dice`
4. 指标列: `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`

换句话说:

- 这不是只给人看的表
- 它也是后续 crosscheck 和 visual 导出的结构化输入

## 这个文件没说明什么

这张表没有单独解释:

1. `best.ckpt` 是怎么来的
2. `threshold_value` 是怎么冻结的
3. 为什么出现 `adhesion_merge`

这些问题要分别去看:

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_eval_run_eval.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`

## 和上下游怎么衔接

- 上游是 `../../../../scripts/test.py` 调 `../../../../src/eval/run_eval.py` 生成 sample 行与 aggregate 行，再把 `pred_path` 指回 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/testA/`
- 下游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 用它做重聚合对账，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 用它挑 worst cases，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 用它收口 split 级结果

## 当前最该注意的一点

最容易读偏的地方只有一个:

不要把 `aggregate` 一行当成整张表的全部价值。

真正支撑后续错例定位和人工审稿的，是 sample 行保留下来的路径与指标。

## 如何手工验证这个文件的正确性

最短验证步骤可以按 4 步走:

1. 检查表里是否既有 `sample` 行又有 `aggregate` 行
2. 检查两条 `sample` 行的 `split_role` 都是 `testA`
3. 检查 `pred_path` 是否真实存在于 `predictions/testA/*`
4. 检查 aggregate `objdice` 是否与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 一致

通过标准:

- `aggregate objdice = 0.08680183161763688`
- `sample_count = 2`
- `pred_path` 能回到真实 png
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 的 `testA` 段返回 `pass`

## 常见问题

- 不要把 `loss` 列为空误读成脚本坏了；sample 行当前只保留指标，aggregate 行才有 loss
- 不要把当前 `sample_count=2` 误读成正式 TestA 只应该评估 2 个样本；这是当前本地联通检查结果
- 不要跳过 `sample_id`，后面 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 都靠它回指

## 建议联读

- `scripts_test.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
