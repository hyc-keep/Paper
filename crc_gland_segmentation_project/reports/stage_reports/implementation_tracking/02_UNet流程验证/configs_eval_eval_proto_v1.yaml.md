# configs_eval_eval_proto_v1.yaml.md

## 结构化溯源卡片

- 正式对象: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `medical segmentation evaluation protocol`
- 章节: `thresholded prediction and validation metric selection`
- 公式/定义: `threshold + metric name + boundary width -> formal eval protocol`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../configs/eval/eval_proto_v1.yaml`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `best_selector`, `best_metric_name`, `threshold_value`, `threshold_source`, `boundary_metric_width`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 当前这个文件说明了什么

这份配置文件回答的是:

当前 stage02 的正式评估口径到底冻结成什么样。

你可以把它理解成 validation 侧的“判分规则卡”。

说白了，trainer 后面为什么看 `val_objdice`，threshold 为什么是 `0.5`，都不是运行时临时想到的，而是这里先写死的。

## 这张表/这个文件长什么样

这个文件字段很集中，主要是:

1. best selector 相关字段
2. threshold 相关字段
3. cast policy / postprocess 字段
4. boundary 与 connected-components 字段

## 当前真实结果

当前最关键的真实字段有 6 组:

1. `best_selector=val_objdice_max`
2. `best_metric_name=val_objdice`
3. `threshold_value=0.5`
4. `threshold_source=val17`
5. `boundary_metric_width=3`
6. `connected_components_connectivity=8`

当前最关键的真实路径也有 4 组:

1. 评估配置路径 `../../../../configs/eval/eval_proto_v1.yaml`
2. eval 对象路径 `../../../../src/eval/run_eval.py`
3. trainer 对象路径 `../../../../src/engine/trainer.py`
4. experiment 索引路径 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`

这些结果已经和正式对象对上:

- `../../../../src/eval/run_eval.py` 会消费 `threshold_value` 和 `boundary_width`
- `../../../../src/engine/trainer.py` 会继续消费 `val_objdice`
- `../../../../configs/train/unet_flow_v1.yaml` 也和它一起把监控指标固定为 `val_objdice`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前 eval config 是当前阶段正式协议点名的评估冻结口径
2. 当前路线锁定要求先把 `val_objdice`、threshold 和 boundary 口径讲清楚
3. 当前正式规则要求选优指标与阈值来源都能回到单一来源配置

## 这些列/字段分别是什么意思

- `best_selector`: 当前最优 checkpoint 的选取方式
- `best_metric_name`: 当前训练/验证主监控指标
- `threshold_value`: logits 转二值预测时的阈值
- `threshold_source`: 阈值来源说明
- `eval_cast_policy`: threshold 前的数值转换策略
- `boundary_metric_width`: 边界指标宽度
- `connected_components_connectivity`: 连通组件口径

## 为什么这样组织

如果 best checkpoint 规则、threshold 规则和 boundary 规则分散在 trainer、eval、metrics 多个对象里，最后最容易出现“每个人都说自己那边才是正式口径”。

当前把它们先收进一份 eval config，本质上是在保护评估口径只有一个来源。

## 这个文件没说明什么

这份文件不负责解释:

- `run_validation_epoch()` 的具体实现流程
- `compute_batch_segmentation_metrics()` 每个指标怎么算
- checkpoint selector 内部如何比较 best state

这些问题要去看对应对象说明文。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
2. 对照 `../../../../src/eval/run_eval.py`
3. 对照 `../../../../src/engine/trainer.py`
4. 对照 `../../../../configs/train/unet_flow_v1.yaml`

期望结果:

- `threshold_value=0.5` 能和 `apply_threshold(logits, threshold_value)` 对上
- `best_metric_name=val_objdice` 能和 trainer 的下游消费逻辑对上
- `boundary_metric_width=3` 能和 metric 聚合逻辑对上
- 具体路径 `../../../../configs/eval/eval_proto_v1.yaml`、`../../../../src/eval/run_eval.py`、`../../../../src/engine/trainer.py` 都真实存在

## 与项目其他部分的关联

- 上游: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 下游: `../../../../src/eval/run_eval.py`、`../../../../src/engine/trainer.py`
- 联动配置: `../../../../configs/train/unet_flow_v1.yaml`

## 常见问题

- 容易误解 1: 以为 best checkpoint 看哪个指标是 trainer 决定的
  - 实际上 trainer 只是执行这里冻结的评估口径
- 容易误解 2: 以为 `threshold_source=val17` 只是备注
  - 实际上它是在说明当前阈值来源口径

## 建议联读

- `src_eval_run_eval.py.md`
- `src_engine_trainer.py.md`
- `configs_train_unet_flow_v1.yaml.md`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答:

1. 当前 stage02 的正式评估口径冻结了哪几项
2. 为什么 `best_metric_name=val_objdice` 会影响 best checkpoint 与 early stop
3. 当前 threshold 与 boundary 口径为什么要单独收在这份配置里
