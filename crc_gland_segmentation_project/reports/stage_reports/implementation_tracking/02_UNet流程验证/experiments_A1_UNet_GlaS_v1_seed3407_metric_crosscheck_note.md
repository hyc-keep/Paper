# experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md

## 这份文件的定位

这份说明文对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`。

你可以把它理解成“结果口径对账单”。

它不负责生成新的指标，而是负责证明 sample 行和 aggregate 行没有悄悄跑偏。

## 作用

它是当前 run 的内部口径对账页，专门说明 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的 sample 行与 aggregate 行是否一致。

## 这个文件是干什么的

- 负责记录 sample 均值与 aggregate 值的对账结果
- 负责把 `threshold_source`、`threshold_value`、`boundary_metric_width` 一起写进同一页
- 负责给 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 的 `metric_crosscheck_result` 提供直接来源

说白了，这份文件在回答:
“当前项目自己的 split 级聚合有没有把自己算错？”

## 当前这个文件说明了什么

当前 note 已经真实记录:

1. `threshold_source=val17`
2. `threshold_value=0.5`
3. `boundary_metric_width=3`
4. `connected_components_connectivity=8`
5. `metric_crosscheck_result=pass`

这说明当前不是口头说“应该差不多”，而是真把结果重聚合了一次。

## 阶段协议回链卡片

- 当前阶段协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 代码参考: `../../../../scripts/test.py`
- 上游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
- 下游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
- 论文依据: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`

## 这张表/这个文件长什么样

当前文件由 3 层组成:

1. 头部冻结字段
2. `testA` 对账块
3. `testB` 对账块

每个 split 块里至少写出:

1. `sample_count`
2. `sampled_ids`
3. `objdice`
4. `dice`
5. `iou`
6. `f1`
7. `boundary_f1`
8. `hd95`
9. `object_hausdorff`

## 当前真实结果

| 项目 | 当前真实结果 | 说明 |
|---|---|---|
| `metric_crosscheck_result` | `pass` | 当前重聚合没有发现 split 级口径漂移 |
| `testA objdice` | `0.08680183161763688` | 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 的 aggregate 一致 |
| `testB objdice` | `0.25959866009914456` | 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的 aggregate 一致 |
| `hd95` | `nan` | 当前样本下仍保持和 aggregate 一致 |

## 这些列/字段分别是什么意思

这里最关键的字段至少分 3 组:

1. 协议字段: `threshold_source`、`threshold_value`、`boundary_metric_width`
2. 抽样字段: `sample_count`、`sampled_ids`
3. 对账字段: `sample_mean`、`aggregate`、`status`

换句话说:

- 这份文件不是“再抄一遍 CSV”
- 它是把“数值从哪里来、按什么比、结果是否一致”三件事压在一起

## 这个文件没说明什么

这份 note 没有解释:

1. 模型为什么只在当前样本上这样表现
2. 哪些视觉错例最值得看
3. 正式外部官方脚本是否完全一致

这些问题要去联读:

- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`

## 当前最该注意的一点

不要把 `metric_crosscheck_result=pass` 误读成“模型效果 pass”。

它只说明一件事:
当前项目内部的 sample 行和 aggregate 行对得上。

## 和上下游怎么衔接

- 上游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 提供 sample 行和 aggregate 行
- 下游是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 回填 `metric_crosscheck_result`，以及 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 收口“有没有发生 aggregate 漂移”

## 如何手工验证这个文件的正确性

最短验证步骤:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`，读取 sample `objdice` 的均值
2. 对照当前 note 中 `testA` 的 `sample_mean` 与 `aggregate`
3. 再对 `testB` 重复一次
4. 检查头部冻结字段是否和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 一致

通过标准:

- `testA` 所有指标都显示 `status=pass`
- `testB` 所有指标都显示 `status=pass`
- `threshold_source=val17`
- `boundary_metric_width=3`

## 常见问题

- 不要把它当成外部 benchmark 对齐报告，它只是当前项目内部 sanity check
- 不要因为 `hd95` 和 `object_hausdorff` 是 `nan` 就误以为 note 无效；当前关键是 sample 与 aggregate 是否一致
- 不要跳过头部冻结字段，它们决定了这次 crosscheck 属于哪一版协议

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
