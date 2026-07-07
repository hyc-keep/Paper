# src_eval_checkpoint_selector.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/eval/checkpoint_selector.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `supervised model selection workflow`
- 章节: `keep best checkpoint by monitored validation metric`
- 公式/定义: current best state plus current metric -> updated best state plus save flag

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/eval/checkpoint_selector.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `best_selector=val_objdice_max`, `best_metric_name=val_objdice`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

### 当前实现落点

- 文件: `../../../../src/eval/checkpoint_selector.py`
- 符号: `BestCheckpointState` / `update_best_checkpoint()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁决定“这一轮验证结果算不算新的 best checkpoint”。

答案就是 `../../../../src/eval/checkpoint_selector.py`。

你可以把它理解成 stage02 训练链里的“最好成绩裁判”。

用人话说，训练闭环对象每个 epoch 都能拿到一堆验证结果，但真正负责比较“这次 `val_objdice` 有没有超过历史最好值”的，是这里。

如果没有这份文件，`../../../../src/engine/trainer.py` 只能每轮都保存 checkpoint，却没法稳定知道哪一个才应该叫 `best.ckpt`。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
src/metrics/seg_metrics.py
        ↓
src/eval/run_eval.py
        ↓
src/eval/checkpoint_selector.py
        ↓
src/engine/trainer.py
        ↓
checkpoints/best.ckpt
```

这里最关键的事实有三条:

1. `../../../../src/eval/run_eval.py` 负责产出 `val_objdice`
2. `../../../../configs/eval/eval_proto_v1.yaml` 已把 `best_selector=val_objdice_max` 冻结下来
3. `../../../../src/engine/trainer.py` 会在每个 epoch 里调 `update_best_checkpoint(best_state, epoch=epoch, metric_value=val_row["val_objdice"])`

当前最硬的物理证据至少有 5 组:

1. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_selector=val_objdice_max`
2. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
3. `../../../../src/engine/trainer.py` 写明 `best_state, is_best = update_best_checkpoint(...)`
4. `../../../../src/engine/trainer.py` 写明只有在 `is_best=true` 时才会写 `best.ckpt`
5. `../../../../src/engine/trainer.py` 写明 `metric_value=val_row["val_objdice"]`

说白了，这里不是随手写的比较函数，而是把“哪一轮才算最好”这条正式裁决规则单独钉住的地方。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../src/eval/run_eval.py`
- `../../../../src/metrics/seg_metrics.py`
- `../../../../src/engine/trainer.py`

### 下游消费者

- `../../../../src/engine/trainer.py`
- `../../../../experiments`
- `../../../../reports/stage_reports/implementation_tracking/02_UNet流程验证/src_engine_trainer.py.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义很直接:

1. 当前 best checkpoint 不是按 `val_loss` 选，也不是按人工目测选
2. 当前“更好”这一件事的定义已经被 `val_objdice_max` 冻结
3. 当前 checkpoint 选择逻辑必须和 trainer 的保存逻辑、eval 的输出逻辑同时对上

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式 best-checkpoint 选择层
- 当前冻结字段:
  - `best_selector=val_objdice_max`
  - `best_metric_name=val_objdice`
- 当前最硬证据:
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_selector=val_objdice_max`
  - `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`
  - `../../../../src/engine/trainer.py` 写明 `best.ckpt` 只在 `is_best` 时落盘

这里必须诚实说明:

当前证据更强地证明了“best checkpoint 选择逻辑已经被 trainer 正式消费”，还没有单独证明“完整长程训练已经产生了最终 best.ckpt 资产并在实验目录被人工验收”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 保存一个冻结的 `BestCheckpointState`
2. 每轮拿当前 `metric_value` 和历史最好值做比较
3. 如果更好，就返回新的 best 状态和 `is_best=true`

### 关键对象 1: `BestCheckpointState`

这个 dataclass 的价值不是“看起来整洁”。

它真正解决的是: best checkpoint 状态不要散落在 trainer 的临时变量里。

这样 `best_epoch` 和 `best_metric_value` 都有稳定落点。

### 关键对象 2: `update_best_checkpoint()`

这个函数看起来很短，但它回答的是正式规则问题:

“什么才叫更好？”

当前答案非常明确，就是:

`metric_value > current_best_metric_value`

### 关键点 3: 为什么这里不支持一堆 mode

因为当前 stage02 没有冻结别的 selector。

现在如果把“最大化/最小化 mode”、多指标、复合裁决一股脑塞进去，只会让说明文边界先失控。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../src/engine/trainer.py` 被 `../../../../scripts/train.py` 间接调用。

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

“为什么不直接在 trainer 里写一个 `if current > best` 就完了？”

用人话说，当然能写，但那样会把“验证聚合”“best 规则”“checkpoint 保存”三件事揉成一坨。

单独拆开后，哪个文件负责产指标，哪个文件负责比大小，哪个文件负责落盘，就更清楚了。

### 设计取舍 1: 为什么状态对象只留两个字段

因为当前只需要知道“最好发生在哪个 epoch”和“最好值是多少”。

先把最小正式闭环钉住，比提前造复杂状态对象更重要。

### 设计取舍 2: 为什么这里明确只支持 `>` 比较

因为当前 frozen rule 就是 `val_objdice_max`。

如果这里开始做一套通用策略框架，反而会让当前配置口径失去唯一性。

### 设计取舍 3: 为什么不自己保存 checkpoint

因为这里的职责是裁决，不是 I/O。

真正写 `best.ckpt` 还是交给 trainer，那样文件职责和状态职责分得更开。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
2. 打开 `../../../../src/engine/trainer.py`
3. 打开 `../../../../src/eval/checkpoint_selector.py`
4. 对照 `../../../../src/eval/run_eval.py`

### 当前最关键的核对点

- `best_selector=val_objdice_max` 是否和 `metric_value > current_state.best_metric_value` 对上
- `best_metric_name=val_objdice` 是否和 trainer 传进来的字段对上
- `is_best` 是否真的控制 `best.ckpt` 落盘

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/eval/checkpoint_selector.py`
2. 具体路径已经固定在 `../../../../configs/eval/eval_proto_v1.yaml`
3. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_selector=val_objdice_max`
4. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
5. `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`
6. `../../../../src/engine/trainer.py` 写明只有在 `is_best=true` 时才会写 `best.ckpt`

## 常见误区

- 误区 1: 以为这里就是个不重要的小比较器
  - 实际上它在正式定义“什么叫 best checkpoint”
- 误区 2: 以为 current best 可以随便换成别的指标
  - 实际上当前 selector 已经被配置冻结
- 误区 3: 以为解释完它就等于把 trainer 都解释完了
  - 实际上 trainer 还负责日志、scheduler、early stop 和 checkpoint I/O

## 建议联读

- `src_eval_run_eval.py.md`
- `src_metrics_seg_metrics.py.md`
- `src_engine_trainer.py.md`
- `configs_eval_eval_proto_v1.yaml.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_eval_run_eval.py.md`，搞清楚 `val_objdice` 是怎么来的
2. 再去看 `src_engine_trainer.py.md`，搞清楚这个 best 状态怎样和 `best.ckpt` 保存逻辑衔接
3. 最后去看 `当前阶段为什么能pass以及下一步怎么看.md`，重新理解当前为什么还是“阶段 pass，但说明文分批推进”

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 best-checkpoint 选择对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前 best checkpoint 必须由 `val_objdice` 决定
3. 为什么这里要和 trainer 的 `_save_checkpoint()` 分开
4. 为什么当前不能把它理解成“将来任意 selector 框架已经做好了”

## 5 分钟自检任务

1. 回到 `../../../../configs/eval/eval_proto_v1.yaml`，找到 `best_selector`
2. 回到 `../../../../src/engine/trainer.py`，找到 `if is_best:`
3. 再回看 `../../../../src/eval/checkpoint_selector.py`，说出这个文件到底返回了哪两个东西

如果这三步你都能顺下来，说明你已经把这份 checkpoint selector 说明文真正看懂了。
