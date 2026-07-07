# experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经有 `loss_value` 和 `output_shape` 了，为什么还要单独解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`？”

因为 runtime evidence 更像单次物理打点。
而当前这份文件回答的是“规范 smoke run 的验证侧正式结果表有没有真的落盘”。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 的运行资产说明文。
- 流程: 它位于验证链完成 loss 与 segmentation metric 聚合之后、结果目录需要落下正式验证表的环节。
- 结构: 当前文件按 val loss、pixel 指标、boundary 指标、object 距离指标这四组结果组织。
- 衔接: 它向上回接 `../../../../src/eval/run_eval.py`、`../../../../src/metrics/seg_metrics.py`, 向下衔接 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 的 best 结果记录和阶段验收。
- 解释: 它回答“验证侧到底输出了哪些正式字段, 它们怎样继续影响 best 选择链”。
- 验证: 需要同时对照 `../../../../configs/eval/eval_proto_v1.yaml`、`../../../../src/eval/run_eval.py`、`../../../../src/metrics/seg_metrics.py` 和当前 run 目录。
- 误区: 不能把单行 smoke-check 验证表误读成完整测试和可视化包。
- 自检: 读完后应能说清 `val_objdice`、boundary 指标和 object 距离指标为什么会一起写进这张表。
- 局限: 它只证明正式验证表已经落盘, 不能替代 TestA/TestB 结果、错误分析和最终总结。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里把验证侧 loss、pixel 指标、boundary 指标和 object 距离指标统一落盘的正式资产。
- 它负责回答“当前验证链到底吐出了哪些正式字段”, 让读者能直接回查验证链产出的正式结果列。

当前这份 CSV 同样只有一行。
但这一行已经足够说明:

- 验证链真的跑了
- 指标字段已经成表
- `val_objdice` 已经有真实数值

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `segmentation validation and metric aggregation`
- 章节: `thresholded mask evaluation with pixel, boundary and object metrics`
- 公式/定义: `logits + threshold + target -> one smoke val metric table row`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/eval/run_eval.py`, `../../../../src/metrics/seg_metrics.py`, `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 当前评估配置: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `val_objdice`, `threshold_value`, `threshold_source`, `boundary_metric_width`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段验证测试与可视化协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 把 val loss、pixel 指标、boundary 指标和 object 距离指标放进同一张表，是为了让 best 选择和阶段验收依赖的验证字段一起可审计回查。

路线锁定文件先要求 stage02 建立最小验证资产链。
正式规则文件又要求把 threshold 后的正式验证字段按统一口径落盘。

所以这份资产的组织方式本质上是在服务“规范 smoke 验证链不只给一个 loss, 而要把会影响 best 选择和阶段验收的正式字段一起写成结果表”。

## 当前这个文件说明了什么

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 说明的是:

1. 上游的 `../../../../src/eval/run_eval.py` 和 `../../../../src/metrics/seg_metrics.py` 已经把正式验证字段聚合出来
2. 当前 smoke run 目录已经有一张可审计的验证结果表, 不再只是口头说“验证过了”
3. 下游的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、best 选择链和阶段验收可以继续消费这里的字段

## 这张表/这个文件长什么样

当前文件虽然只有 1 行结果, 但表头已经分成 4 组:

1. epoch 与 val loss
2. pixel 指标
3. boundary 指标
4. object 距离指标

## 这些列/字段分别是什么意思

这里的字段至少分成 4 组:

1. `val_loss`、`val_loss_bce`、`val_loss_dice` 先解释验证侧 loss 是怎样拆开的
2. `val_objdice`、`val_dice`、`val_iou`、`val_f1` 解释 pixel/object 级主指标
3. `val_boundary_f1` 解释 boundary 质量
4. `val_hd95` 与 `val_object_hausdorff` 解释 object 距离层面的几何误差

它不只是告诉你 loss 大小。
它还会把 `val_objdice`、boundary 和 object 距离这些后面真正会影响 best 选择与阶段验收的字段一起写出来。

## 当前实现状态

- 状态: `已存在`
- 当前行数: `1`
- 当前真实结论: `验证指标表已经落盘, 但当前仍只是规范 smoke-check 级别的最小结果`

这里同样要把边界说清楚:
当前文件能证明 `val17` 验证链已经能输出正式字段, 但不能替代 TestA 和 TestB 的正式测试结果。

## 当前真实结果

当前最关键的真实路径至少有 5 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
2. `../../../../src/eval/run_eval.py` 是当前验证指标聚合入口
3. `../../../../src/metrics/seg_metrics.py` 是当前正式指标计算入口
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已继续消费当前表里的 best 结果
5. `../../../../configs/eval/eval_proto_v1.yaml` 已冻结当前验证字段背后的规则来源

当前最关键的真实字段至少有 9 组:

1. `val_loss=1.2901947498321533`
2. `val_loss_bce=0.6876387000083923`
3. `val_loss_dice=0.6025561094284058`
4. `val_objdice=0.26280593599215546`
5. `val_dice=0.49554966074459383`
6. `val_iou=0.3651432910243176`
7. `val_boundary_f1=0.221016372013223`
8. `val_hd95=258.0885375976562`
9. `val_object_hausdorff=292.8710179932626`

这说明当前文件已经是带有真实数值的验证结果表。

## 这份验证结果表里到底写了什么

当前表头是:

`epoch,val_loss,val_loss_bce,val_loss_dice,val_objdice,val_dice,val_iou,val_f1,val_boundary_f1,val_hd95,val_object_hausdorff`

当前唯一一行真实数值包括:

- `epoch=1`
- `val_loss=1.2901947498321533`
- `val_loss_bce=0.6876387000083923`
- `val_loss_dice=0.6025561094284058`
- `val_objdice=0.26280593599215546`
- `val_dice=0.49554966074459383`
- `val_iou=0.3651432910243176`
- `val_f1=0.49554966074459383`
- `val_boundary_f1=0.221016372013223`
- `val_hd95=258.0885375976562`
- `val_object_hausdorff=292.8710179932626`

## 对应代码里的真实协议痕迹

当前最关键的代码痕迹有四处:

1. `../../../../src/eval/run_eval.py` 调 `apply_threshold(...)` 和 `compute_batch_segmentation_metrics(...)`
2. `../../../../src/eval/run_eval.py` 把字段 `val_loss`、`val_loss_bce`、`val_loss_dice` 合并进 metric dict
3. `../../../../src/engine/trainer.py` 把验证结果按 epoch 写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
4. `../../../../configs/eval/eval_proto_v1.yaml` 冻结字段 `best_selector=val_objdice_max`、`threshold_value=0.5`、`threshold_source=val17`

所以当前表里的列不是临时命名, 而是评估协议和 trainer 共同产出的正式字段。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
2. 对照 `../../../../configs/eval/eval_proto_v1.yaml`
3. 再对照 `../../../../src/eval/run_eval.py` 和 `../../../../src/metrics/seg_metrics.py`
4. 最后回看 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`

通过标准:

- `val_objdice` 这一列真实存在
- boundary 和 object 距离指标列没有丢
- 当前 `best_metric_value` 能和 `val_objdice=0.26280593599215546` 对上
- 路径 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 真实存在

## 这个文件没说明什么

当前文件能证明的是:

1. 当前验证结果表已经真实落盘
2. `val_objdice`、boundary 和 object 距离指标已经进入正式结果列
3. 规范 smoke run 不再只有抽象“验证过了”的口头说法

当前文件还不能单独证明的是:

1. TestA 和 TestB 的正式测试结果都已交齐
2. 完整测试、可视化和 metric crosscheck 闭环已经完成
3. 只凭这一份验证表就能代替总结页、错误分析和下游阶段交接

## 常见问题

- 误解 1: 以为这份表只是在记录 `val_loss`
  - 实际上它还记录了 pixel、boundary 和 object 三层指标
- 误解 2: 以为 `val_objdice` 有一行数值就等于完整评估包已经齐全
  - 实际上当前还没有把 TestA 和 TestB 的正式测试结果也一并纳入本轮说明文
- 误解 3: 以为 smoke-check 下的指标就可以直接当成长程正式结论
  - 实际上这里更适合把它理解成“验证表资产链已经成立”

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `src_eval_run_eval.py.md`
- `src_metrics_seg_metrics.py.md`
- `src_eval_threshold.py.md`
- `configs_eval_eval_proto_v1.yaml.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. 当前 smoke 验证结果表到底记录了哪几层指标
2. 为什么 `val_objdice` 会继续影响 best 选择链
3. 为什么这份表能证明验证资产链成立, 但还不能替代完整测试与可视化闭环
