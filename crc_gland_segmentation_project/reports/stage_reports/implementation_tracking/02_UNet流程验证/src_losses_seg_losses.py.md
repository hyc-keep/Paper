# src_losses_seg_losses.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/losses/seg_losses.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `medical segmentation loss survey`
- 章节: `region supervision and overlap optimization`
- 公式/定义: `BCEWithLogits(logits, targets) + Dice(sigmoid(logits), targets)`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/losses/seg_losses.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `loss_name=bce_dice`, `bce_weight=1.0`, `dice_weight=1.0`, `loss_eps=1.0e-6`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/losses/seg_losses.py`
- 符号: `BCEDiceLoss` / `build_seg_loss()`

## 这个脚本的作用

`../../../../src/losses/seg_losses.py` 负责回答一个很具体的问题:

当前 stage02 的模型输出出来以后，到底用什么目标函数把它拉回“腺体前景 vs 背景”这条任务定义上。

当前答案不是一长串备选 loss，而是很明确的一组冻结选择:

`BCE + Dice`

这份文件的价值就在这里。

用大白话说，它像训练链里的“评分器”。

你可以把它理解成训练链里专门负责“打分并指出该往哪里改”的那个人。

模型就算已经吐出了 logits，如果这里没有一个正式评分器，后面的 backward 根本不知道该往哪个方向推。

它把这个选择从“计划里写过”变成了“训练链里真的有一个固定实现”。

如果没有它，`../../../../src/models/unet.py` 就只能输出 logits，却没有正式方式把 logits 变成可反向传播的监督目标。

## 这个脚本在整个阶段中的位置

你可以先把它理解成“模型和 trainer 之间的正式胶水层”。

链路位置大致是:

```text
src/models/unet.py
        ↓
src/losses/seg_losses.py
        ↓
src/engine/trainer.py
        ↓
runtime_evidence.json
```

这里最关键的事实有两条:

1. 模型输出的是 logits
2. loss 文件把 logits 和二值 mask 对上

当前正式证据同样不是空口判断。

`../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经明确写出了:

- `target_shape=[2, 1, 512, 512]`
- `target_unique_values=[0, 1]`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已写明 `loss_value=1.2771382331848145`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已写明 `loss_is_finite=true`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明 `loss_module=pass`

这些字段至少证明了一件事:

当前损失层并不是“代码里有个类名”，而是真的在正式 runtime-check 里产出了有限损失值。

衔接也先说白:

这份文件一头接 `../../../../src/models/unet.py`，一头接 `../../../../src/engine/trainer.py`。

所以它不是独立存在的小工具，而是模型输出和训练闭环之间那层真正负责“把监督落地”的接口。

## 与项目其他部分的关联

### 上游依赖

- `../../../../src/models/unet.py`
- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/engine/trainer.py`
- `../../../../src/eval/run_eval.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 当前训练配置: `../../../../configs/train/unet_flow_v1.yaml`
- 当前评估配置: `../../../../configs/eval/eval_proto_v1.yaml`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一段回链最重要的作用是把三个边界钉死:

1. 当前训练损失就是 `BCE + Dice`
2. 当前评估 threshold 不在 loss 里做
3. 当前对象只服务二值前景分割
4. 当前路线锁定和正式规则都要求先把这条标准基线闭环讲清楚，而不是提前扩成更多损失变体

直接看 `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md` 和 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`，你会发现当前阶段本来就要求先把标准单头 UNet + `BCE + Dice` 这条最短主链讲清楚。

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式监督目标实现
- 当前冻结参数:
  - `loss_name=bce_dice`
  - `bce_weight=1.0`
  - `dice_weight=1.0`
  - `loss_eps=1.0e-6`
- 当前最硬证据:
  - `../../../../configs/train/unet_flow_v1.yaml` 冻结了 `loss_name=bce_dice`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 明确写明 `loss_module=pass`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 的 `Formal Chain Readiness` 已把对象定位到 `../../../../src/losses/seg_losses.py`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `loss_value=1.2771382331848145`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `loss_is_finite=true`

这里需要诚实说一句:

当前证据证明的是“这份 loss 已经进入正式单步训练闭环”，不是“已经完成所有更复杂 loss 对比实验”。

## 脚本核心逻辑

### 主要流程

如果你把这份文件当成“把 logits 正式接成监督目标的装配脚本”去看，会更好懂。

它的主流程可以先记成 5 步:

1. `build_seg_loss()` 从 `../../../../configs/train/unet_flow_v1.yaml` 取冻结参数
2. `BCEDiceLoss.forward()` 接收 logits 和 target
3. 先算 `BCEWithLogitsLoss`
4. 再对 logits 做 sigmoid 去算 Dice
5. 返回 `loss_total`、`loss_bce`、`loss_dice` 给 `../../../../src/engine/trainer.py`

你可以把它想成一条“既盯像素，又盯区域重叠”的双重监督链。

### 核心 1: `BCEDiceLoss`

`BCEDiceLoss` 做了三件事:

1. 先把 target 转成 `float`
2. 用 `BCEWithLogitsLoss` 约束像素级监督
3. 再用 sigmoid 后的概率图去算 Dice

这三步拼起来以后，最终返回三类结果:

- `loss_total`
- `loss_bce`
- `loss_dice`

这件事很重要，因为 trainer 不只是需要一个总损失，还需要能把 BCE 和 Dice 分量分别写到日志里。

### 核心 2: 为什么 Dice 放在 sigmoid 之后

Dice 要比较的是概率和目标区域的重叠，不是原始 logits 的符号大小。

所以当前实现先 `torch.sigmoid(logits)`，再计算交集和并集，这样语义更稳定，也更符合“前景概率图”的直觉。

### 核心 3: 为什么保留 `eps`

`eps` 的作用很朴素:

避免在分母很小时直接把数值稳定性打穿。

当前阶段不追求花哨技巧，但非常重视“最小正式闭环不要因为数值边缘情况直接炸掉”。

## 如何运行这个脚本

这份对象同样不是独立 CLI。

它的正式运行方式，是经由 `../../../../scripts/train.py` 的 runtime-check 或 smoke-check 间接进入训练链。

### 运行方式 1: formal runtime-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --run-name A1_UNet_GlaS_v1_seed3407 --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1
```

### 运行方式 2: local smoke-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --smoke-check --device cpu
```

你可能会问:

“loss 不是被调用的一层吗，为什么还要写运行方式？”

因为这里真正要解释的是“它怎么进入正式链”，而不是“它能不能单独 import”。

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“既然还有很多分割 loss 变体，为什么当前不顺手一起做？”

说白了，当前阶段先要的是稳定、可回链、可被 runtime 真值验证的正式基线，而不是一口气把所有 loss 花样都堆进来。

### 设计取舍 1: 为什么不是只用 BCE

只用 BCE 的好处是实现更简单。

但它对区域重叠这件事表达得不够直接。

当前任务是腺体分割，区域重叠好不好本来就是核心关注点，所以 Dice 不能缺席。

### 设计取舍 2: 为什么不是只用 Dice

只用 Dice 看起来更贴近分割任务，但在训练早期更容易出现不稳定的梯度信号。

把 BCE 和 Dice 放在一起，可以同时保留像素级监督和区域级重叠约束。

### 设计取舍 3: 为什么不把 sigmoid 写进模型

这件事看上去只是“写在哪一层”的区别，实际上会直接影响职责分层。

当前选择是:

- `../../../../src/models/unet.py` 只负责输出 logits
- `../../../../src/losses/seg_losses.py` 负责在 loss 侧处理 sigmoid
- `../../../../src/eval/run_eval.py` 负责在 eval 侧处理 threshold

这样一来，每层做什么都更清楚。

### 设计取舍 4: 为什么 builder 也要单独保留

`build_seg_loss()` 的作用不是“多此一举包一层”，而是把 config 到对象实例的映射边界固定住。

这样 `../../../../scripts/train.py` 在解出 `configs/train/unet_flow_v1.yaml` 以后，不需要知道 loss 类内部细节，只需要把冻结参数交给 builder。

| 候选方案 | 看起来的好处 | 实际问题 | 当前决策 |
|---|---|---|---|
| 只用 BCE | 实现最简单 | 对区域重叠表达不够直接 | 否决 |
| 只用 Dice | 任务味道更浓 | 训练早期梯度更不稳 | 否决 |
| 当前固定 `BCE + Dice` | 兼顾像素监督和区域重叠 | 需要解释两部分损失 | 采用 |

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 对照 `../../../../src/losses/seg_losses.py`
3. 再看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- `bce_weight=1.0` 和 `dice_weight=1.0` 是否来自配置
- `loss_value=1.2771382331848145` 是否来自正式 runtime-check
- `target_unique_values=[0, 1]` 是否说明当前 loss 面对的是二值监督

### 当前真实结果

当前最关键的物理证据至少有 4 组:

1. `../../../../configs/train/unet_flow_v1.yaml` 冻结了 `loss_name=bce_dice`
2. `../../../../configs/train/unet_flow_v1.yaml` 冻结了 `bce_weight=1.0` 与 `dice_weight=1.0`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_is_finite=true`
5. `../../../../scripts/train.py` 已把 loss builder 串进正式入口
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已把 loss readiness 标成 `pass`
7. 文件路径已经固定在 `../../../../src/losses/seg_losses.py`
8. 关键字段已经固定在 `../../../../configs/train/unet_flow_v1.yaml` 的 `loss_name`、`bce_weight`、`dice_weight`

如果这三项都能说清，你就知道当前 loss 不是凭空拍脑袋定的。

## 常见误区

- 误区 1: 以为 Dice 可以直接吃 logits
  - 实际上当前实现会先做 sigmoid，再算 overlap
- 误区 2: 以为这份文件只返回一个总损失就够了
  - 实际上 trainer 还要记录 `loss_bce` 和 `loss_dice`
- 误区 3: 以为 loss 层顺手就该做 threshold
  - 实际上 threshold 属于 eval 侧，不属于训练损失职责

## 建议联读

- `scripts_train.py.md`
- `src_models_unet.py.md`
- `src_engine_trainer.py.md`
- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先回到 `src_models_unet.py.md`，确认 logits 从哪里来
2. 再去看 `src_engine_trainer.py.md`，确认 `loss_total`、`loss_bce`、`loss_dice` 如何被写进训练闭环
3. 最后回到 `scripts_train.py.md`，重新看入口如何把 model、loss 和 trainer 装到同一条链上

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前 stage02 为什么固定用 `BCE + Dice`
2. `loss_total`、`loss_bce`、`loss_dice` 三个字段分别有什么用
3. 为什么 sigmoid 不放在模型里而放在 loss 侧处理
4. 哪个正式证据最能说明当前 loss 真的跑出了有限值

## 5 分钟自检任务

1. 回到 `../../../../configs/train/unet_flow_v1.yaml`，找到 `bce_weight`
2. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，找到 `loss_is_finite`
3. 再回看 `../../../../src/losses/seg_losses.py`，说出 Dice 分量为什么要先走 sigmoid

如果这三步你都能顺下来，说明你已经把这份损失说明文真正看懂了。
