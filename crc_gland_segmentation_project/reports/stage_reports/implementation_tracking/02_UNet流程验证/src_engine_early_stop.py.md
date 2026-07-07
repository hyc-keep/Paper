# src_engine_early_stop.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/engine/early_stop.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `early stopping by monitored validation metric`
- 章节: `stop when validation no longer improves for a fixed patience`
- 公式/定义: metric stream plus patience -> improved flag plus should_stop flag

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/early_stop.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `early_stop_patience`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/engine/early_stop.py`
- 符号: `EarlyStopper` / `update()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁决定“训练是不是该停了”。

答案就是 `../../../../src/engine/early_stop.py`。

你可以把它理解成 stage02 训练链里的“耐心值裁判”。

用人话说，训练不是每次都跑满 `epoch_max`。真正负责判断“验证指标已经连续好多轮没变好，要不要停”的，是这里。

如果没有这份文件，`../../../../src/engine/trainer.py` 只能机械地把 epoch 跑到上限，却没法按正式 patience 规则决定何时早停。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/train/unet_flow_v1.yaml
        ↓
src/engine/early_stop.py
        ↓
scripts/train.py
        ↓
src/engine/trainer.py
        ↓
stop_reason
```

这里最关键的事实有三条:

1. `../../../../configs/train/unet_flow_v1.yaml` 已冻结 `early_stop_patience=20`
2. `../../../../scripts/train.py` 会调用 `EarlyStopper(patience=int(train_config["early_stop_patience"]), mode="max")`
3. `../../../../src/engine/trainer.py` 会在每轮验证后执行 `improved, should_stop = early_stopper.update(val_row["val_objdice"])`

当前最硬的物理证据至少有 5 组:

1. `../../../../configs/train/unet_flow_v1.yaml` 写明 `early_stop_patience=20`
2. `../../../../scripts/train.py` 写明 `mode="max"`
3. `../../../../src/engine/trainer.py` 写明 `early_stopper.update(val_row["val_objdice"])`
4. `../../../../src/engine/trainer.py` 写明 `if should_stop:`
5. `../../../../src/engine/trainer.py` 的 run summary 会写出 `stop_reason`

说白了，这里不是顺手写的计数器，而是把“什么时候该停”这条正式训练规则单独锁住的地方。

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

1. 当前 early stop 不是拍脑袋停
2. 当前比较方向和 best checkpoint 一样，都跟着 `val_objdice` 变大这条口径走
3. 当前 patience 来自正式 train config，而不是运行现场临时改写

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式早停判定层
- 当前冻结字段:
  - `early_stop_patience=20`
  - `mode=max`
- 当前最硬证据:
  - `../../../../scripts/train.py` 写明 `EarlyStopper(patience=int(train_config["early_stop_patience"]), mode="max")`
  - `../../../../src/engine/trainer.py` 写明 `early_stopper.update(val_row["val_objdice"])`
  - `../../../../configs/train/unet_flow_v1.yaml` 写明 `early_stop_patience=20`

这里必须诚实说明:

当前证据能证明的是“早停规则已经进入正式训练闭环”，还没有单独证明“完整长程训练已经真的因为 early stop 触发而提前结束”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 4 步:

1. 保存 `best_value`
2. 保存连续未改进轮数 `num_bad_epochs`
3. 每次 `update()` 时比较当前值和历史最好值
4. 达到 `patience` 就返回 `should_stop=true`

### 关键点 1: 为什么当前走 `mode=max`

因为当前训练链盯的是 `val_objdice`。

说白了，当前更好就是数值更大，不是更小。

### 关键点 2: 为什么这里不做复杂 stop 策略

因为 stage02 当前最重要的是最小正式闭环。

先把“连续多少轮不涨就停”这条规则钉死，比提前造复杂策略更重要。

### 关键点 3: 为什么 early stop 要和 scheduler 分开

因为这两者都看验证指标，但回答的是两件不同的问题。

scheduler 回答“该不该降学习率”，这里回答“该不该停训练”。

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

“为什么不把早停逻辑直接写在 trainer 的 for 循环里？”

用人话说，当然能写，但那样 trainer 会同时背日志、checkpoint、scheduler、stop rule 四套职责。

单独拆开后，读者更容易看清“停训规则”到底是什么。

### 设计取舍 1: 为什么状态只留 `best_value` 和 `num_bad_epochs`

因为当前正式规则只需要这两个量。

如果现在就引入 delta、窗口平均、复杂容忍区，说明文边界会先失控。

### 设计取舍 2: 为什么仍保留“向上比较/向下比较”方向参数

因为对象本身是一个通用比较器外壳，但 stage02 正式调用只走 `max`。

这也是说明文里必须诚实写清楚的边界。

### 设计取舍 3: 为什么 `update()` 返回两个布尔值

因为 trainer 后面既要知道这次有没有改进，也要知道该不该停。

把两个结论一起返回，外层就不用重复推断。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 打开 `../../../../scripts/train.py`
3. 打开 `../../../../src/engine/trainer.py`
4. 对照 `../../../../src/engine/early_stop.py`

### 当前最关键的核对点

- `early_stop_patience=20` 是否和构造 `EarlyStopper(...)` 时的 patience 对上
- `mode=max` 是否和 `val_objdice` 的方向对上
- `should_stop` 是否真的在 trainer 里控制停训分支

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/engine/early_stop.py`
2. 具体路径已经固定在 `../../../../configs/train/unet_flow_v1.yaml`
3. `../../../../configs/train/unet_flow_v1.yaml` 写明 `early_stop_patience=20`
4. `../../../../scripts/train.py` 写明 `mode="max"`
5. `../../../../src/engine/trainer.py` 写明 `early_stopper.update(val_row["val_objdice"])`
6. `../../../../src/engine/trainer.py` 会把最终 `stop_reason` 写入 run summary

## 常见误区

- 误区 1: 以为 early stop 就是 scheduler 的另一种写法
  - 实际上一个回答“降不降学习率”，一个回答“停不停训练”
- 误区 2: 以为当前停训方向可以现场改成 `min`
  - 实际上正式调用已经固定跟着 `val_objdice` 走 `max`
- 误区 3: 以为讲完它就等于整个 engine 包都讲完了
  - 实际上 trainer、lr_scheduler 和这里是三层不同职责

## 建议联读

- `src_engine_trainer.py.md`
- `src_engine_lr_scheduler.py.md`
- `configs_train_unet_flow_v1.yaml.md`
- `src_eval_run_eval.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_engine_trainer.py.md`，搞清楚 `should_stop` 是在哪一步被 trainer 消费的
2. 再去看 `src_engine_lr_scheduler.py.md`，比较 scheduler 和 early stop 的边界
3. 最后去看 `configs_train_unet_flow_v1.yaml.md`，回到 patience 的冻结来源

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 early-stop 对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前 early stop 盯的是 `val_objdice`
3. 为什么它要和 scheduler、trainer 分开
4. 为什么当前不能把它理解成完整的复杂 stop 策略框架

## 5 分钟自检任务

1. 回到 `../../../../configs/train/unet_flow_v1.yaml`，找到 `early_stop_patience`
2. 回到 `../../../../src/engine/trainer.py`，找到 `early_stopper.update(val_row["val_objdice"])`
3. 再回看 `../../../../src/engine/early_stop.py`，说出 `update()` 到底返回了哪两个判断结果

如果这三步你都能顺下来，说明你已经把这份 early stop 说明文真正看懂了。
