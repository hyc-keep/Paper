# src_eval_run_eval.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/eval/run_eval.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `biomedical segmentation validation workflow`
- 章节: `thresholded validation and metric aggregation`
- 公式/定义: logits + target masks -> validation loss plus dice, iou, objdice, boundary_f1, hd95, object_hausdorff

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/eval/run_eval.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `best_selector=val_objdice_max`, `best_metric_name=val_objdice`, `threshold_value=0.5`, `threshold_source=val17`, `boundary_metric_width=3`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/eval/run_eval.py`
- 符号: `run_validation_epoch()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把模型输出的 logits 变成正式验证指标。

答案就是 `../../../../src/eval/run_eval.py` 里的 `run_validation_epoch()`。

你可以把它理解成 stage02 训练链里的“验收计分台”。

用人话说，trainer 负责把模型跑起来，但真正决定这一轮验证结果怎么记、按什么阈值二值化、最后汇成哪些指标的人，是这里。

如果没有这份文件，`../../../../src/engine/trainer.py` 就只能知道“做了一次验证”，却没法稳定拿到 `val_loss`、`val_objdice`、`boundary_f1` 这些正式结果。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
src/models/unet.py
        ↓
src/losses/seg_losses.py
        ↓
src/eval/run_eval.py
        ↓
src/engine/trainer.py
        ↓
best checkpoint / scheduler / early stop
```

这里最关键的事实有三条:

1. 模型先输出 logits
2. `../../../../src/eval/threshold.py` 在这里把 logits 按冻结阈值转成二值 mask
3. `../../../../src/metrics/seg_metrics.py` 在这里把预测和目标汇成正式指标

当前最硬的物理证据主要有 4 组:

1. `../../../../configs/eval/eval_proto_v1.yaml` 冻结了 `best_metric_name=val_objdice`
2. `../../../../configs/eval/eval_proto_v1.yaml` 冻结了 `threshold_value=0.5`
3. `../../../../src/engine/trainer.py` 已把 `run_validation_epoch()` 串进正式训练闭环
4. `../../../../src/engine/trainer.py` 已把 `val_objdice` 继续交给 scheduler、best checkpoint 和 early stop
5. 文件路径已经固定在 `../../../../src/eval/run_eval.py`

说白了，当前虽然还没有单独一份“eval runtime report”，但验证主链已经在正式 trainer 里有明确落点，不是口头设计。

## 与项目其他部分的关联

### 上游依赖

- `../../../../src/models/unet.py`
- `../../../../src/losses/seg_losses.py`
- `../../../../src/eval/threshold.py`
- `../../../../src/metrics/seg_metrics.py`
- `../../../../configs/eval/eval_proto_v1.yaml`

### 下游消费者

- `../../../../src/engine/trainer.py`
- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../reports/stage_reports/implementation_tracking/02_UNet流程验证/src_engine_trainer.py.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链的意义很直接:

1. 当前验证口径不能随意改成别的阈值来源
2. 当前最关键的选优指标已经冻结为 `val_objdice`
3. 当前 validation 不只是算一个 loss，而是服务后面的 checkpoint 和 early stop 决策

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式验证指标聚合层
- 当前冻结字段:
  - `best_selector=val_objdice_max`
  - `best_metric_name=val_objdice`
  - `threshold_value=0.5`
  - `threshold_source=val17`
  - `boundary_metric_width=3`
- 当前最硬证据:
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_value=0.5`
  - `../../../../src/engine/trainer.py` 写明 `run_validation_epoch()` 会回传 `val_loss`、`val_loss_bce`、`val_loss_dice`
  - `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`
  - `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`

这里必须诚实说明:

当前证据更强地证明了“验证函数已经进入正式训练闭环并决定下游口径”，还没有单独证明“完整长程验证结果已经作为正式 run 资产落盘”。

但这条说法在本轮需要补一句新的诚实更新:

当前 `../../../../src/eval/run_eval.py` 已经不只服务训练期 validation。
本轮新增的 `evaluate_split()` 让它同时进入了从 `../../../../scripts/test.py` 到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的正式测试资产链。

当前最直接的新物理证据包括:

1. `../../../../scripts/test.py` 已真实通过 `evaluate_split()` 导出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
2. `../../../../scripts/test.py` 已真实通过 `evaluate_split()` 导出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 已保留 sample 行和 aggregate 行
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 已保留 sample 行和 aggregate 行

## 脚本核心逻辑

### 主要流程

你可以把它想成 5 步:

1. 遍历 validation dataloader
2. 让模型对每个 batch 产出 logits
3. 用 loss 函数聚合 `val_loss`、`val_loss_bce`、`val_loss_dice`
4. 用 `apply_threshold()` 把 logits 转成二值预测
5. 用 `compute_batch_segmentation_metrics()` 聚合 dice、iou、objdice、boundary_f1、hd95、object_hausdorff

### 关键点 1: 为什么这里要先做 threshold

因为 metric 层吃的是二值 mask，不是原始 logits。

如果不在这里把 logits 转成二值预测，后面的对象级指标和边界指标就没有稳定输入。

### 关键点 2: 为什么 trainer 要盯 `val_objdice`

因为 stage02 当前冻结的不是“看起来差不多就行”，而是明确的 `best_selector=val_objdice_max`。

这意味着 validation 不只是辅助看数，而是真正参与训练闭环决策。

### 关键点 3: 为什么 smoke-check 还能走这里

因为 smoke-check 缩小的是规模，不是把验证主链剪掉。

说白了，当前想验证的是“正式验证逻辑存在且能被 trainer 调用”，不是只验证训练前半截。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../scripts/train.py` 的 smoke-check 或正式训练支路间接进入。

### 运行方式 1: local smoke-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --smoke-check --device cpu
```

### 运行方式 2: formal training branch

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --device cpu
```

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“既然 loss 里已经有数值，为什么还要额外搞一层 validation 聚合？”

用人话说，训练损失只能说明这一步算没算出来，不能替代真正的验证口径。

如果不把 threshold、对象级指标和边界指标单独拉出来，后面的 best checkpoint 与 early stop 就会缺少稳定依据。

### 设计取舍 1: 为什么 validation 里同时保留 loss 和 metric

因为 trainer 后面既要记录损失分量，也要做按指标选优。

只留一边都会让后面的说明文和运行资产断链。

### 设计取舍 2: 为什么不在 trainer 里自己手写全部验证细节

因为那样 trainer 会太重。

把验证逻辑单独收在这里，可以让 trainer 更像装配层，validation 更像计分层，职责边界更清楚。

### 设计取舍 3: 为什么还保留 `include_distance_metrics`

因为 `hd95` 和 `object_hausdorff` 这类距离类指标在 smoke-check 里更贵。

当前设计不是把它们删掉，而是在缩小验证规模时给出开关。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
2. 打开 `../../../../src/engine/trainer.py`
3. 打开 `../../../../src/eval/run_eval.py`
4. 对照 `../../../../src/metrics/seg_metrics.py`

### 当前最关键的核对点

- `threshold_value=0.5` 是否和 `apply_threshold(logits, threshold_value)` 对上
- `best_metric_name=val_objdice` 是否和 trainer 后续的 `val_objdice` 消费逻辑对上
- `boundary_metric_width=3` 是否和 `compute_batch_segmentation_metrics(... boundary_width=boundary_width)` 对上

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/eval/run_eval.py`
2. 具体路径已经固定在 `../../../../configs/eval/eval_proto_v1.yaml`
3. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
4. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_source=val17`
5. `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`
6. `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`

## 常见误区

- 误区 1: 以为 validation 只是再算一遍 loss
  - 实际上这里还负责 threshold 和正式指标聚合
- 误区 2: 以为 best checkpoint 是 trainer 随便挑的
  - 实际上 trainer 挑的依据来自这里产出的 `val_objdice`
- 误区 3: 以为当前已经把整个 eval 包都讲完了
  - 实际上当前已经补了 `src/eval/threshold.py` 和 `src/eval/checkpoint_selector.py` 的单独说明文, 但这仍不等于整个 stage02 的所有后续对象包都已经解释完

## 建议联读

- `configs_eval_eval_proto_v1.yaml.md`
- `src_engine_trainer.py.md`
- `src_losses_seg_losses.py.md`
- `../../../../src/metrics/seg_metrics.py`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_eval_eval_proto_v1.yaml.md`，搞清楚这些评估字段为什么这么冻结
2. 再去看 `src_engine_trainer.py.md`，搞清楚 `val_objdice` 怎样进入 scheduler 和 checkpoint 决策
3. 最后回到 `scripts_train.py.md`，重新看正式入口如何把 eval 配置一起接进来

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 validation 聚合对象在 stage02 里到底负责哪一段正式职责
2. 为什么 `val_objdice` 能继续影响 best checkpoint 和 early stop
3. 当前 `threshold_value=0.5` 是从哪份正式配置来的
4. 为什么当前不能把这个 validation 聚合对象的解释等同于整个 eval 包都已经讲完

## 5 分钟自检任务

1. 回到 `../../../../configs/eval/eval_proto_v1.yaml`，找到 `threshold_source`
2. 回到 `../../../../src/engine/trainer.py`，找到 `scheduler.step(val_row["val_objdice"])`
3. 再回看 `../../../../src/eval/run_eval.py`，说出 logits 是在这里的哪一步被变成二值预测的

如果这三步你都能顺下来，说明你已经把这份 eval 说明文真正看懂了。
