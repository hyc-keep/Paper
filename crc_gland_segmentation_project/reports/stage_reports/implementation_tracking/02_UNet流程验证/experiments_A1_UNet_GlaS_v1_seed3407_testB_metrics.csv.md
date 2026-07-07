# experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md

## 这份文件的定位

这份说明文对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`。

如果说 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 是 `TestA` 的正式分账单，那么这一份就是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的正式分账单。

你可以把它理解成“TestB split 的原始成绩表”。

## 这个文件是干什么的

- 负责保留 `TestB` 的 sample 行和 aggregate 行
- 负责把 `pred_path` 与真实预测 png 连起来
- 负责给 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 提供上游数值

说白了，这张表是在回答:
`TestB` 到底测出了什么，而不是只给一个摘要结论。

## 当前这个文件说明了什么

当前文件最关键的现实信息有 4 组:

1. `TestB` 逐样本指标
2. `TestB` aggregate 指标
3. 对应原图、GT、预测路径
4. 后续错例总结所需的 `sample_id`

当前最硬的路径锚点包括:

- `datasets/01_GlaS_official_raw/testB_1.bmp`
- `datasets/01_GlaS_official_raw/testB_10.bmp`
- `experiments/A1_UNet_GlaS_v1_seed3407/predictions/testB/GlaS_official_testB_testB_1_pred.png`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 代码参考: `../../../../scripts/test.py`
- 上游实现: `../../../../src/eval/run_eval.py`
- 关联资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
- 论文依据: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`

## 这张表/这个文件长什么样

这张表和 `TestA` 版使用完全一致的 schema。

关键列仍然是:

1. `row_type`
2. `sample_id`
3. `split_role`
4. `image_path`
5. `mask_path`
6. `pred_path`
7. `objdice`
8. `dice`
9. `iou`
10. `boundary_f1`

当前真实样例里:

- `GlaS_official_testB_testB_1` 的 `objdice=0.20466293329979884`
- `GlaS_official_testB_testB_10` 的 `objdice=0.3145343868984902`
- aggregate `objdice=0.25959866009914456`

## 当前真实结果

| 项目 | 当前真实结果 | 说明 |
|---|---|---|
| `sample_count` | `2` | 当前本地联通检查抽样导出 2 个 TestB 样本 |
| `aggregate objdice` | `0.25959866009914456` | 已回填到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` |
| `aggregate dice` | `0.5824385066317761` | 说明在当前抽样联通检查里 TestB 的像素级结果高于 TestA |
| `aggregate boundary_f1` | `0.27078208585927027` | 解释了为什么当前会出现 `boundary_over_smooth` |
| `pred_path` | 已真实回指 `predictions/testB/*` | 让 visual 和错例回溯不断链 |

## 这些列/字段分别是什么意思

这里的列仍然可以分成 4 组:

1. 身份列: `row_type`、`sample_id`、`split_role`
2. 路径列: `image_path`、`mask_path`、`pred_path`
3. 损失列: `loss`、`loss_bce`、`loss_dice`
4. 指标列: `objdice`、`dice`、`iou`、`f1`、`boundary_f1`、`hd95`、`object_hausdorff`

最值得记的一点是:
这张表不是只给人工看的，它同时也是后续 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 的结构化输入。

## 这个文件没说明什么

这张表没有单独解释:

1. 为什么 `boundary_f1` 会更低
2. 为什么当前 `TestB` 会出现 `boundary_over_smooth`
3. 阈值和 best checkpoint 是怎么来的

这些问题要去联读:

- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_eval_run_eval.py.md`

## 和上下游怎么衔接

- 上游是 `../../../../scripts/test.py` 调 `../../../../src/eval/run_eval.py` 生成 `TestB` sample 行与 aggregate 行，并把 `pred_path` 指回 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/testB/`
- 下游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 继续做口径对账，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 继续挑坏例子，`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 继续汇总 split 级结论

## 当前最该注意的一点

不要因为 `TestB` 的 `objdice` 高于 `TestA`，就直接写成“模型已经稳定”。

当前这里只能诚实地说:
在当前 CPU 联通检查样本里，`TestB` 的对象级结果高于 `TestA`，但错例总结仍提示边界过平滑问题。

## 如何手工验证这个文件的正确性

最短验证步骤:

1. 检查 `sample` 行和 `aggregate` 行都存在
2. 检查 `split_role` 全部是 `testB`
3. 检查 aggregate `objdice` 是否等于 `0.25959866009914456`
4. 检查 `pred_path` 是否真实存在于 `predictions/testB/*`

通过标准:

- sample 行数为 `2`
- aggregate `objdice = 0.25959866009914456`
- aggregate `boundary_f1 = 0.27078208585927027`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 里 `testB` 段返回 `pass`

## 常见问题

- 不要把 `TestB` 的较高 `dice` 误读成错误已经消失；边界问题仍在
- 不要把当前抽样行数当成正式 split 总样本数
- 不要跳过 `sample_id` 和 `pred_path`，后面 visual 回指都靠它们

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
- `scripts_test.py.md`
