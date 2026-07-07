# src_engine_trainer.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/engine/trainer.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `biomedical segmentation training workflow`
- 章节: `epoch training, validation feedback and checkpoint selection`
- 公式/定义: train epoch -> validation epoch -> scheduler / best-checkpoint / early-stop feedback

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `optimizer=AdamW`, `scheduler=ReduceLROnPlateau`, `scheduler_monitor=val_objdice`, `epoch_max=120`, `early_stop_patience=20`, `batch_size=2`
- 评估冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 评估字段: `best_selector=val_objdice_max`, `best_metric_name=val_objdice`, `threshold_value=0.5`, `threshold_source=val17`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/engine/trainer.py`
- 符号: `_append_csv_row()` / `_save_checkpoint()` / `_build_autocast_context()` / `train_model()`

## 这个脚本的作用

如果说 `../../../../scripts/train.py` 是 stage02 的总入口，`../../../../src/engine/trainer.py` 就是“真正把训练循环跑起来”的那一层。

它负责回答一个非常现实的问题:

当模型、loss、optimizer、scheduler、early stopper 都准备好以后，到底是谁来把它们按 epoch 串成正式执行链。

当前答案就是 `train_model()`。

这份文件的职责不是做配置解析，也不是决定模型结构，而是把下面这些动作稳定串起来:

1. train loader 迭代
2. forward
3. loss
4. backward
5. optimizer step
6. validation
7. scheduler step
8. best checkpoint 更新
9. early stopping 判断
10. 训练日志与 summary 资产落盘

打个比方，这个文件像整条训练链里的“总装配车间”。

模型、loss、评估和选优各自有零件感，但真正把它们装成一台能跑的机器的人，是这里。

你可以把它理解成 stage02 训练链里那个真正负责“把零件装成机器并让机器跑起来”的岗位。

用人话说，前面对象负责提供零件，这里负责让整条训练线开始转起来。

## 这个脚本在整个阶段中的位置

你可以先把它放在这条链里理解:

```text
scripts/train.py
        ↓
src/models/unet.py + src/losses/seg_losses.py
        ↓
src/engine/trainer.py
        ↓
val metrics / checkpoints / summaries
```

这里要特别注意两个事实:

1. `../../../../scripts/train.py` 会把训练正常支路交给 `train_model()`
2. `train_model()` 不是独立小世界，它还要依赖 `../../../../src/eval/run_eval.py`、`../../../../src/eval/checkpoint_selector.py` 和 `../../../../src/engine/early_stop.py`

所以这份对象说明文不能只盯着一个 for-loop，而要看它如何把整个 epoch 级反馈闭环装起来。

衔接也先说白:

它的上游核心对象是 `../../../../src/models/unet.py` 和 `../../../../src/losses/seg_losses.py`；
它的下游核心对象是 `../../../../src/eval/run_eval.py`、`../../../../src/eval/checkpoint_selector.py` 和 `../../../../src/engine/early_stop.py`。

## 与项目其他部分的关联

### 上游依赖

- `../../../../scripts/train.py`
- `../../../../src/models/unet.py`
- `../../../../src/losses/seg_losses.py`
- `../../../../configs/train/unet_flow_v1.yaml`

### 下游消费者

- `../../../../src/eval/run_eval.py`
- `../../../../src/eval/checkpoint_selector.py`
- `../../../../src/engine/early_stop.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 当前训练配置: `../../../../configs/train/unet_flow_v1.yaml`
- 当前评估配置: `../../../../configs/eval/eval_proto_v1.yaml`
- 相关评估对象: `../../../../src/eval/run_eval.py`
- 相关选优对象: `../../../../src/eval/checkpoint_selector.py`
- 相关早停对象: `../../../../src/engine/early_stop.py`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是把 trainer 的判定口径钉死:

1. scheduler 监控的是 `val_objdice`
2. best checkpoint 依据的是 `val_objdice`
3. early stop 的判断也跟着同一条指标链走
4. 当前路线锁定和正式规则要求先把这条标准基线闭环讲清楚，再考虑后续更复杂扩展

直接看 `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md` 和 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`，你会发现当前 trainer 的任务就是先把单头 UNet 基线的正式训练闭环讲清楚，而不是提前把更多实验分支揉进来。

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式 epoch 训练闭环
- 当前冻结训练参数:
  - `optimizer=AdamW`
  - `lr=0.001`
  - `weight_decay=0.0001`
  - `scheduler=ReduceLROnPlateau`
  - `scheduler_monitor=val_objdice`
  - `scheduler_factor=0.5`
  - `scheduler_patience=5`
  - `early_stop_patience=20`
  - `batch_size=2`
  - `epoch_max=120`
- 当前冻结评估参数:
  - `best_selector=val_objdice_max`
  - `best_metric_name=val_objdice`
  - `threshold_value=0.5`
  - `threshold_source=val17`
  - `boundary_metric_width=3`

当前最硬的正式证据有三层:

1. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 明确写明 `trainer=pass`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 的 `Formal Chain Readiness` 已把对象定位到 `../../../../src/engine/trainer.py`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `backward_executed=true`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `optimizer_step_executed=true`

这里必须诚实说明:

当前最硬证据并不是“120 个 epoch 已经在本地完整执行完”，而是“trainer 模块已经进入正式主链，且它所依赖的 train step 关键闭环已经被 runtime-check 证明成立”。

## 脚本核心逻辑

### 主要流程

如果你把这份文件当成“把训练中所有关键动作装成一条正式流水线的总装配脚本”去看，会更好懂。

它的主流程可以先记成 6 步:

1. 从 `../../../../configs/train/unet_flow_v1.yaml` 和 `../../../../configs/eval/eval_proto_v1.yaml` 接收冻结参数
2. 在 train loop 里完成 forward、loss、backward、optimizer step
3. 写入训练侧与验证侧结构化日志
4. 调 `../../../../src/eval/run_eval.py` 回收验证指标
5. 用 `val_objdice` 驱动 scheduler、best checkpoint 和 early stop
6. 写出 run summary，给下游阅读入口和结果资产解释层使用

你可以把它想成 stage02 正式训练闭环里的“总装配车间”。

### 核心 1: `_append_csv_row()`

这个 helper 的作用很朴素，但很关键:

把训练过程中的结构化结果持续写进 CSV。

为什么这个小函数值得单独讲？

因为很多训练脚本会把日志写得很散，最后只能靠 print 回忆发生了什么。

当前这里统一把训练日志 CSV 和验证指标 CSV 的写入逻辑收在一个 helper 里，能减少很多重复代码，也让“每一轮到底留下了什么资产”更稳定。

### 核心 2: `_save_checkpoint()`

这个 helper 把 checkpoint 保存格式固定下来。

当前保存的字段不多，但都是正式恢复链真正需要的:

- epoch
- model_state_dict
- optimizer_state_dict
- metric_value

这样做的好处是边界很清楚。

当前阶段不提前引入 scaler、EMA 或额外训练状态，避免把 stage02 首轮闭环解释得过重。

### 核心 3: `_build_autocast_context()`

这个 helper 看起来很小，实际上是在保护本地 CPU 环境的诚实边界。

它明确规定:

- 只有 `amp_enabled` 且设备是 `cuda`，才会进入 autocast
- 否则就退回 `nullcontext()`

这件事很重要，因为当前项目环境明确是本地无 GPU。

如果这里还去假装 AMP 生效，说明文和真实运行环境就会直接脱节。

### 核心 4: `train_model()`

`train_model()` 是这份文件的真正中心。

它每个 epoch 会做下面这些事:

1. 进入 `model.train()`
2. 遍历 `train_loader`
3. 取出 `image` 和 `mask`
4. `optimizer.zero_grad()`
5. `model(images)` 得到 logits
6. `loss_fn(logits, targets)` 得到 `loss_total`、`loss_bce`、`loss_dice`
7. `loss_total.backward()`
8. `optimizer.step()`
9. 累积训练损失
10. 写训练日志 CSV
11. 调 `run_validation_epoch()` 做验证
12. 写验证指标 CSV
13. 用 `val_objdice` 驱动 scheduler
14. 用 `val_objdice` 更新 best checkpoint
15. 用 `val_objdice` 驱动 early stopper
16. 保存 `last.ckpt`
17. 必要时保存 `best.ckpt`
18. 最后写 run summary

这里最关键的一点不是步骤多，而是全部围绕同一条指标主线:

`val_objdice`

## 如何运行这个脚本

这份对象也不是独立 CLI。

它的正式运行方式，是通过 `../../../../scripts/train.py` 间接进入主链。

### 运行方式 1: local smoke-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --smoke-check --device cpu
```

### 运行方式 2: formal runtime-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --run-name A1_UNet_GlaS_v1_seed3407 --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1
```

你可能会问:

“trainer 不是被入口调用的吗，为什么这里还要写运行方式？”

因为这里真正要解释的是“它怎么进入正式训练链”，而不是“它能不能被 import”。

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“既然 trainer 可以玩出很多花样，为什么当前不把多套监控指标、多套 checkpoint 规则一起加上？”

说白了，当前阶段最怕的是口径分叉。

一旦 scheduler、best checkpoint、early stop 各看各的指标，后面的说明文、report 和结果资产就很难继续对账。

### 设计取舍 1: 为什么 scheduler / best / early stop 都跟 `val_objdice`

因为当前评估配置已经冻结:

- `best_selector=val_objdice_max`
- `best_metric_name=val_objdice`

如果 trainer 在这里偷偷改成别的指标，比如 `val_loss`，整个阶段的解释链会立刻分叉。

所以当前统一用 `val_objdice`，其实是在保护口径一致性。

### 设计取舍 2: 为什么 smoke-check 不绕过主链

当前 `smoke_check` 只会缩短 epoch 和 batch 数量，不会绕开主流程。

这意味着即使是最小本地验证，也仍然能走到:

- train
- val
- scheduler
- checkpoint
- summary

这样留下来的不是“一个特别版的测试分支”，而是正式训练主链的缩小版。

### 设计取舍 3: 为什么 checkpoint 同时保留 `best.ckpt` 和 `last.ckpt`

这两个文件回答的是不同问题:

- `last.ckpt`: 当前循环实际跑到了哪里
- `best.ckpt`: 当前按冻结指标看最优的是哪一轮

如果只留一个，后续说明文就很难同时解释“过程进度”和“最优选择”。

### 设计取舍 4: 为什么 summary 文本单独写成 run summary

因为 CSV 适合机器和精细对账，不适合人快速看结论。

把 `stop_reason`、`best_epoch`、`best_metric_value` 单独收成一份文本 summary，后续读者会更容易先抓住这次 run 的结果轮廓。

| 候选方案 | 看起来的好处 | 实际问题 | 当前决策 |
|---|---|---|---|
| scheduler 看 `val_loss`，best checkpoint 看别的指标 | 每个模块都能自选指标 | 口径分叉，后续说明文很难对账 | 否决 |
| smoke-check 直接绕过 validation / checkpoint | 本地更快 | 和正式主链脱节，证据价值下降 | 否决 |
| 当前统一围绕 `val_objdice`，且 smoke-check 只缩小规模 | 口径一致、证据连续、容易回链 | 解释细节更多一些 | 采用 |

## 当前最真实的边界

这一节特别重要。

当前这份对象说明文不能夸大到“trainer 的所有正式资产都已经在本地完整跑出”。

当前真正能稳稳说成立的，是下面这些点:

1. `../../../../src/engine/trainer.py` 已经是正式对象，并被 formal chain readiness 标成 `implemented`
2. 它的核心 train step 依赖链已经在 runtime-check 中走通
3. `backward` 和 `optimizer.step` 已经有真实字段证据
4. 它的 epoch 级日志、checkpoint 和 summary 输出结构已经在代码中固定好

当前还不能夸大说的，是下面这些点:

1. 不能因为 trainer 已实现，就说 120 epoch 本地全量训练已完成
2. 不能因为有 runtime-check，就说所有验证指标都已经在正式长程训练中稳定复现
3. 不能把代码里的“会生成哪些资产”误写成“这些资产当前都已经有真实产物”

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
3. 对照 `../../../../src/engine/trainer.py`
4. 再看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- `scheduler_monitor=val_objdice` 是否和 `scheduler.step(val_row["val_objdice"])` 对上
- `best_selector=val_objdice_max` 是否和 `update_best_checkpoint(... metric_value=val_row["val_objdice"])` 对上
- `backward_executed=true` 与 `optimizer_step_executed=true` 是否说明 train loop 关键一步真的成立

### 当前真实结果

当前最关键的物理证据至少有 4 组:

1. `../../../../configs/train/unet_flow_v1.yaml` 冻结了 `scheduler_monitor=val_objdice`
2. `../../../../configs/eval/eval_proto_v1.yaml` 冻结了 `best_selector=val_objdice_max`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `optimizer_step_executed=true`
5. `../../../../scripts/train.py` 已把 `train_model()` 串进正式训练入口
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已把 trainer readiness 标成 `pass`
7. 文件路径已经固定在 `../../../../src/engine/trainer.py`
8. 关键字段已经固定在 `../../../../configs/train/unet_flow_v1.yaml` 和 `../../../../configs/eval/eval_proto_v1.yaml`

如果这三项都能说清，你就已经抓住 trainer 的主脊梁了。

## 常见误区

- 误区 1: 以为 trainer 只是负责 backward
  - 实际上它还负责 validation、checkpoint、scheduler 和 summary
- 误区 2: 以为 smoke-check 会走另一套逻辑
  - 实际上它只是缩小正式主链，不是另起炉灶
- 误区 3: 以为 scheduler、best checkpoint 和 early stop 可以各看各的指标
  - 实际上当前冻结口径要求它们统一围绕 `val_objdice`

## 建议联读

- `scripts_train.py.md`
- `src_models_unet.py.md`
- `src_losses_seg_losses.py.md`
- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先回到 `src_models_unet.py.md`，确认 trainer 前面的模型主体是什么
2. 再去看 `src_losses_seg_losses.py.md`，确认 trainer 里记到日志的损失分量从哪里来
3. 最后回到 `scripts_train.py.md`，重新看正式入口如何把 trainer 放进整条执行链

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. `train_model()` 在 stage02 里到底负责哪些正式资产输出
2. 为什么 scheduler、best checkpoint 和 early stop 都围绕 `val_objdice`
3. 当前最硬的 trainer 运行证据到底来自哪里
4. 为什么当前不能把 trainer 的实现和“全量训练已完成”画等号

## 5 分钟自检任务

1. 回到 `../../../../configs/eval/eval_proto_v1.yaml`，找到 `best_metric_name`
2. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，找到 `optimizer_step_executed`
3. 再回看 `../../../../src/engine/trainer.py`，说出 `best.ckpt` 和 `last.ckpt` 分别回答什么问题

如果这三步你都能顺下来，说明你已经把这份 trainer 说明文真正看懂了。
