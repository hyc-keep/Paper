# src_engine_lr_scheduler.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/engine/lr_scheduler.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `validation-driven learning-rate adaptation`
- 章节: `ReduceLROnPlateau on monitored validation metric`
- 公式/定义: optimizer plus scheduler config -> ReduceLROnPlateau scheduler

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/lr_scheduler.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `scheduler`, `scheduler_monitor`, `scheduler_factor`, `scheduler_patience`, `scheduler_min_lr`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/engine/lr_scheduler.py`
- 符号: `build_scheduler()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把 train config 里的 scheduler 字段变成真正可调用的学习率调度器。

答案就是 `../../../../src/engine/lr_scheduler.py`。

你可以把它理解成 stage02 训练链里的“降速规则装配器”。

用人话说，optimizer 只是负责按当前学习率更新参数，但真正决定“验证指标长期不涨时要不要降学习率、降多少、等几轮再降”的，是这里。

如果没有这份文件，`../../../../scripts/train.py` 最多只能构出 optimizer，却没法稳定得到和正式配置一致的 scheduler 行为。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/train/unet_flow_v1.yaml
        ↓
src/engine/lr_scheduler.py
        ↓
scripts/train.py
        ↓
src/engine/trainer.py
        ↓
scheduler.step(val_objdice)
```

这里最关键的事实有三条:

1. `../../../../configs/train/unet_flow_v1.yaml` 已冻结 `scheduler=ReduceLROnPlateau`
2. `../../../../scripts/train.py` 会调用 `build_scheduler(optimizer, train_config)`
3. `../../../../src/engine/trainer.py` 会在每轮验证后执行 `scheduler.step(val_row["val_objdice"])`

当前最硬的物理证据至少有 5 组:

1. `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler=ReduceLROnPlateau`
2. `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler_monitor=val_objdice`
3. `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler_factor=0.5`
4. `../../../../scripts/train.py` 写明 `scheduler = build_scheduler(optimizer, train_config)`
5. `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`

说白了，这里不是可有可无的小 helper，而是把“什么时候降学习率”这条正式训练规则钉住的地方。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../scripts/train.py`
- `../../../../src/eval/run_eval.py`

### 下游消费者

- `../../../../scripts/train.py`
- `../../../../src/engine/trainer.py`
- `../../../../reports/stage_reports/implementation_tracking/02_UNet流程验证/src_engine_trainer.py.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义很直接:

1. 当前 scheduler 不是随运行现场临时挑的
2. 当前监控指标明确固定为 `val_objdice`
3. 当前降学习率方向和 best checkpoint 方向都要和对象级指标链保持一致

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式学习率调度器构造层
- 当前冻结字段:
  - `scheduler=ReduceLROnPlateau`
  - `scheduler_monitor=val_objdice`
  - `scheduler_factor=0.5`
  - `scheduler_patience=5`
  - `scheduler_min_lr=1.0e-6`
- 当前最硬证据:
  - `../../../../scripts/train.py` 写明 `scheduler = build_scheduler(optimizer, train_config)`
  - `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`
  - `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler_min_lr=1.0e-6`

这里必须诚实说明:

当前证据能证明的是“scheduler 已经进入正式训练闭环”，还没有单独证明“完整长程训练里学习率曲线已经作为正式资产被逐轮审阅”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 从 `train_config` 读取 scheduler 名称
2. 验证当前只允许 `ReduceLROnPlateau`
3. 用冻结的 `factor`、`patience`、`min_lr` 组装出 scheduler 对象

### 关键点 1: 为什么 mode 固定成 `max`

因为当前 monitor 的就是 `val_objdice`。

说白了，当前“更好”意味着指标更大，不是更小。

### 关键点 2: 为什么只支持一种 scheduler

因为当前 stage02 最重要的是把最小正式闭环讲清楚。

如果这里一上来就支持一堆 scheduler，说明文边界会先散掉。

### 关键点 3: 为什么 scheduler builder 单独拆成文件

因为 optimizer 构造、scheduler 规则、trainer 消费是三件事。

拆开后，配置说明文、源码说明文和训练主链更容易对账。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../scripts/train.py` 的正式训练支路间接进入。

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

“为什么不在训练入口里直接把 scheduler 一行写掉？”

用人话说，当然能写，但那样会把训练入口、配置解引用和调度规则揉成一团。

单独拆开以后，哪一层负责“冻结的 scheduler 规则”，就更清楚了。

### 设计取舍 1: 为什么不支持别的 scheduler

因为当前还不是扩实验位点的时候。

现在最优先的是把 `val_objdice` 驱动的单一路径讲透。

### 设计取舍 2: 为什么不在这里消费 monitor 名字

因为当前 scheduler 对象只负责构造，真正把 `val_objdice` 喂进去的是 trainer。

这样职责边界更稳。

### 设计取舍 3: 为什么 `min_lr` 也要显式冻结

因为如果没有下界，学习率退火到哪就会变得很虚。

现在把它写死，后面读配置和看训练行为就更容易对账。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 打开 `../../../../scripts/train.py`
3. 打开 `../../../../src/engine/trainer.py`
4. 对照 `../../../../src/engine/lr_scheduler.py`

### 当前最关键的核对点

- `scheduler=ReduceLROnPlateau` 是否和 builder 里的唯一允许分支对上
- `scheduler_monitor=val_objdice` 是否和 `scheduler.step(val_row["val_objdice"])` 对上
- `scheduler_factor`、`scheduler_patience`、`scheduler_min_lr` 是否都来自正式 train config

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/engine/lr_scheduler.py`
2. 具体路径已经固定在 `../../../../configs/train/unet_flow_v1.yaml`
3. `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler=ReduceLROnPlateau`
4. `../../../../configs/train/unet_flow_v1.yaml` 写明 `scheduler_monitor=val_objdice`
5. `../../../../scripts/train.py` 写明 `scheduler = build_scheduler(optimizer, train_config)`
6. `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`

## 常见误区

- 误区 1: 以为 scheduler 是 trainer 顺手写的一行附属逻辑
  - 实际上它对应的是正式 train config 里一整组冻结字段
- 误区 2: 以为 monitor 什么指标都可以临时换
  - 实际上当前 monitor 已经固定成 `val_objdice`
- 误区 3: 以为说明完 scheduler 就等于整个 engine 包解释完了
  - 实际上 trainer、early_stop 和这里是三层不同职责

## 建议联读

- `src_engine_trainer.py.md`
- `configs_train_unet_flow_v1.yaml.md`
- `src_engine_early_stop.py.md`
- `src_eval_run_eval.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_train_unet_flow_v1.yaml.md`，搞清楚 scheduler 这些字段为什么这么冻结
2. 再去看 `src_engine_trainer.py.md`，搞清楚 `val_objdice` 是怎样被喂进 scheduler 的
3. 最后去看 `src_engine_early_stop.py.md`，比较 scheduler 和 early stop 在训练闭环里各自负责什么

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 scheduler 对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前 scheduler 监控的是 `val_objdice`
3. 为什么 scheduler builder 要和 trainer 分开
4. 为什么当前不能把它理解成“各种 scheduler 都已经开放实验”

## 5 分钟自检任务

1. 回到 `../../../../configs/train/unet_flow_v1.yaml`，找到 `scheduler_factor`
2. 回到 `../../../../src/engine/trainer.py`，找到 `scheduler.step(val_row["val_objdice"])`
3. 再回看 `../../../../src/engine/lr_scheduler.py`，说出这个 builder 现在允许哪一种 scheduler

如果这三步你都能顺下来，说明你已经把这份 scheduler 说明文真正看懂了。
