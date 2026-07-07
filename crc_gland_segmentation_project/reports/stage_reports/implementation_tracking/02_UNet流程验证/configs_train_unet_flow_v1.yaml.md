# configs_train_unet_flow_v1.yaml.md

## 结构化溯源卡片

- 正式对象: `../../../../configs/train/unet_flow_v1.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `medical segmentation training baseline`
- 章节: `optimizer, scheduler, loss, batch and smoke-check freeze`
- 公式/定义: `loss + optimizer + scheduler + batch protocol -> formal train config`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../configs/train/unet_flow_v1.yaml`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `loss_name`, `bce_weight`, `dice_weight`, `optimizer`, `lr`, `scheduler`, `scheduler_monitor`, `epoch_max`, `batch_size`, `smoke_epochs`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 当前这个文件说明了什么

这份配置文件回答的是:

当前 stage02 的正式训练超参数和 smoke-check 规则到底冻结成什么样。

你可以把它理解成 trainer 的“调度单”。

说白了，`src/engine/trainer.py` 和 `src/losses/seg_losses.py` 不会自己发明超参数，它们先认这份配置。

## 这张表/这个文件长什么样

这个文件主要分成 4 类字段:

1. loss 字段
2. optimizer / scheduler 字段
3. epoch / batch / worker / amp 字段
4. light augmentation 字段

## 当前真实结果

当前最关键的真实字段有 10 组:

1. `loss_name=bce_dice`
2. `bce_weight=1.0`
3. `dice_weight=1.0`
4. `optimizer=AdamW`
5. `lr=0.001`
6. `scheduler=ReduceLROnPlateau`
7. `scheduler_monitor=val_objdice`
8. `epoch_max=120`
9. `batch_size=2`
10. `smoke_epochs=1`

当前最关键的真实路径也有 4 组:

1. 训练配置路径 `../../../../configs/train/unet_flow_v1.yaml`
2. trainer 对象路径 `../../../../src/engine/trainer.py`
3. loss 对象路径 `../../../../src/losses/seg_losses.py`
4. experiment 索引路径 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`

这些结果已经和正式对象对上:

- `../../../../src/losses/seg_losses.py` 消费 `bce_weight`、`dice_weight`
- `../../../../src/engine/trainer.py` 消费 `scheduler_monitor=val_objdice`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前 train config 是当前阶段正式协议点名的训练冻结口径
2. 当前路线锁定要求先把 `BCE + Dice`、`AdamW`、`ReduceLROnPlateau` 这条标准基线讲清楚
3. 当前正式规则要求 smoke-check 与正式训练的关键超参数都能回链到单一来源

## 这些列/字段分别是什么意思

- `loss_name`: 当前正式损失组合名
- `bce_weight` / `dice_weight`: 两部分损失权重
- `optimizer`: 当前优化器类型
- `lr`: 学习率
- `scheduler`: 当前调度器类型
- `scheduler_monitor`: 调度器盯的指标
- `epoch_max`: 最大 epoch
- `batch_size`: 批大小
- `amp`: 是否允许混合精度
- `smoke_epochs` / `smoke_train_batches`: 本地最小验证规模

## 为什么这样组织

如果 loss、optimizer、scheduler、smoke-check 规则散在不同地方，trainer 就会越来越像一堆隐式常量的集合。

当前把它们先收进同一份 train config，本质上是在保护训练闭环的单一来源。

## 这个文件没说明什么

这份文件不负责解释:

- `src/engine/trainer.py` 的具体 epoch 循环
- `src/losses/seg_losses.py` 的具体计算细节
- 每个增强操作在图像空间里怎么实现

这些问题要去看对应对象说明文。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 对照 `../../../../src/losses/seg_losses.py`
3. 对照 `../../../../src/engine/trainer.py`
4. 对照 `../../../../configs/eval/eval_proto_v1.yaml`

期望结果:

- `bce_weight` / `dice_weight` 能和 loss builder 对上
- `scheduler_monitor=val_objdice` 能和 trainer 对上
- smoke-check 字段能和最小验证规模对上
- 具体路径 `../../../../configs/train/unet_flow_v1.yaml`、`../../../../src/engine/trainer.py`、`../../../../src/losses/seg_losses.py` 都真实存在

## 与项目其他部分的关联

- 上游: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 下游: `../../../../src/losses/seg_losses.py`、`../../../../src/engine/trainer.py`
- 联动配置: `../../../../configs/eval/eval_proto_v1.yaml`

## 常见问题

- 容易误解 1: 以为 scheduler 盯哪个指标是 trainer 临时决定的
  - 实际上这里已经冻结为 `val_objdice`
- 容易误解 2: 以为 smoke-check 只是命令行参数问题
  - 实际上它对应的 epoch / batch 规模也在这里冻结

## 建议联读

- `src_losses_seg_losses.py.md`
- `src_engine_trainer.py.md`
- `configs_eval_eval_proto_v1.yaml.md`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答:

1. 当前 stage02 的正式训练超参数冻结了哪些核心项
2. 为什么 `scheduler_monitor=val_objdice` 会影响整个训练闭环
3. smoke-check 规模为什么也属于 train config 的一部分
