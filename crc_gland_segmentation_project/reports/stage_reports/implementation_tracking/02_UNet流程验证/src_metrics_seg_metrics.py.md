# src_metrics_seg_metrics.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/metrics/seg_metrics.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `pixel-level, boundary-level and object-level segmentation evaluation`
- 公式/定义: binary prediction plus binary target -> dice/iou/objdice/boundary_f1/hd95/object_hausdorff

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/metrics/seg_metrics.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `best_selector=val_objdice_max`, `best_metric_name=val_objdice`, `boundary_metric_width=3`, `connected_components_connectivity=8`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/metrics/seg_metrics.py`
- 符号: `dice_score()` / `iou_score()` / `boundary_f1_score()` / `object_dice_score()` / `hd95_score()` / `object_hausdorff_score()` / `compute_batch_segmentation_metrics()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把二值预测 mask 算成 pixel、boundary 和 object 三层正式指标。

答案就是 `../../../../src/metrics/seg_metrics.py`。

你可以把它理解成 stage02 验证链里的“计分规则库”。

用人话说，validation 聚合对象负责把 logits 变成二值预测并把 batch 收齐，但真正决定 `dice`、`iou`、`objdice`、`boundary_f1`、`hd95`、`object_hausdorff` 这些数怎么来的，是这里。

如果没有这份文件，`../../../../src/eval/run_eval.py` 最多只能拿到二值 mask，却没法稳定产出 trainer 后面真正消费的正式指标。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
src/eval/threshold.py
        ↓
src/metrics/seg_metrics.py
        ↓
src/eval/run_eval.py
        ↓
src/engine/trainer.py
        ↓
best checkpoint / scheduler / early stop
```

这里最关键的事实有三条:

1. `../../../../src/eval/run_eval.py` 会把 threshold 之后的二值 mask 交给 `compute_batch_segmentation_metrics()`
2. `../../../../configs/eval/eval_proto_v1.yaml` 已经把 `best_metric_name=val_objdice` 和 `boundary_metric_width=3` 冻结下来
3. `../../../../src/engine/trainer.py` 最后消费的 `val_objdice`，根子就在这里的 `object_dice_score()`

当前最硬的物理证据至少有 5 组:

1. `../../../../src/eval/run_eval.py` 写明 `metrics = compute_batch_segmentation_metrics(...)`
2. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
3. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `boundary_metric_width=3`
4. `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`
5. `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`

说白了，这不是“后面有空再算点指标”，而是当前正式 best-checkpoint 选择链真的建立在这里的对象级指标之上。

## 与项目其他部分的关联

### 上游依赖

- `../../../../src/eval/threshold.py`
- `../../../../src/eval/run_eval.py`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../src/losses/seg_losses.py`

### 下游消费者

- `../../../../src/eval/run_eval.py`
- `../../../../src/engine/trainer.py`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../reports/stage_reports/implementation_tracking/02_UNet流程验证/src_eval_run_eval.py.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义很直接:

1. 当前验证口径不是只看像素 overlap，而是必须覆盖对象级和边界级指标
2. 当前 best selector 明确锁死在 `val_objdice`
3. 当前距离类指标可以在 smoke-check 缩小成本，但正式实现本身不能凭空删掉

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式指标计算层
- 当前冻结字段:
  - `best_metric_name=val_objdice`
  - `boundary_metric_width=3`
  - `connected_components_connectivity=8`
  - `include_distance_metrics=true` 为正式默认链，smoke-check 可局部降级

本轮还要额外记住两个新增变化:

1. `compute_sample_segmentation_metrics()` 已经进入正式实现，用来支撑 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的 sample 行导出
2. `../../../../src/metrics/pixel_metrics.py`、`../../../../src/metrics/object_metrics.py`、`../../../../src/metrics/boundary_metrics.py` 这三个薄门面，当前都只是把这里已经存在的正式实现拆成更稳定的公开入口

换句话说，本轮新增的三个 metrics 子模块没有另起一套算法。
它们真正服务的是“把这里的正式计算口径拆成更清楚的模块边界”。
- 当前最硬证据:
  - `../../../../src/eval/run_eval.py` 写明 `compute_batch_segmentation_metrics(... boundary_width=boundary_width, include_distance_metrics=include_distance_metrics)`
  - `../../../../src/engine/trainer.py` 写明 `val_objdice` 会进入 scheduler 与 best checkpoint
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_selector=val_objdice_max`
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `boundary_metric_width=3`

这里必须诚实说明:

当前证据更强地证明了“指标函数已经进入正式验证决策链”，还没有单独证明“每个指标在完整长程训练里都已经留成独立资产报表”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 4 步:

1. 先对单样本二值 mask 分别算 pixel-level 的 `dice` 和 `iou`
2. 再对边界轮廓算 `boundary_f1`
3. 再基于连通域匹配算 `object_dice` 和 `object_hausdorff`
4. 最后用 `compute_batch_segmentation_metrics()` 把一批样本的分数聚成平均值字典

### 关键对象 1: `object_dice_score()`

这个函数特别值得盯。

因为 stage02 当前冻结的 best selector 不是普通 Dice，而是 `val_objdice`。

说白了，当前不是只关心“像素看起来重没重合”，而是更关心腺体对象层面有没有被分对。

### 关键对象 2: `boundary_f1_score()`

这个函数解决的是另一个常见误区:

“Dice 不错，是不是边界也一定不错？”

答案不一定。

边界指标就是专门把这个问题拆出来看。

### 关键对象 3: `compute_batch_segmentation_metrics()`

这个函数的真正价值不是“帮你少写几行 for 循环”。

它是在把验证输出的字段集合标准化。

这样 validation 聚合对象、训练闭环对象、配置说明文和后面的学习说明文才有同一套口径。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../src/eval/run_eval.py` 被 `../../../../scripts/train.py` 间接调用。

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

“既然 trainer 最终只盯 `val_objdice`，为什么这里还要保留这么多指标？”

用人话说，选优指标和诊断指标不是一回事。

当前 best checkpoint 确实靠 `val_objdice`，但如果没有 dice、boundary_f1、hd95 这些辅助视角，后面很难解释模型到底是哪一层出了问题。

### 设计取舍 1: 为什么 object 指标放在 metrics 层，不放在 trainer

因为 trainer 更像装配层。

对象级匹配、边界匹配和距离统计这些规则放进 trainer，只会把职责边界越写越糊。

### 设计取舍 2: 为什么保留 `include_distance_metrics`

因为 `hd95` 和 `object_hausdorff` 在本地 CPU 上更贵。

当前不是删掉它们，而是允许 smoke-check 只验证主链最关键的 overlap/boundary/object-dice 口径。

### 设计取舍 3: 为什么输入必须是 `[B, 1, H, W]`

因为当前 stage02 明确是单输出二值分割。

如果这里又开始接受任意形状，说明文和验证链就很容易失去边界。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
2. 打开 `../../../../src/eval/run_eval.py`
3. 打开 `../../../../src/engine/trainer.py`
4. 对照 `../../../../src/metrics/seg_metrics.py`

### 当前最关键的核对点

- `best_metric_name=val_objdice` 是否和 `object_dice_score()` 的存在理由对上
- `boundary_metric_width=3` 是否和 `boundary_f1_score(... width=3)` 对上
- `val_objdice` 是否真的继续流向 trainer 的 scheduler/checkpoint 决策

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/metrics/seg_metrics.py`
2. 具体路径已经固定在 `../../../../configs/eval/eval_proto_v1.yaml`
3. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `best_metric_name=val_objdice`
4. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `boundary_metric_width=3`
5. `../../../../src/eval/run_eval.py` 写明 `metrics = compute_batch_segmentation_metrics(...)`
6. `../../../../src/engine/trainer.py` 写明 `scheduler.step(val_row["val_objdice"])`
7. `../../../../src/engine/trainer.py` 写明 `update_best_checkpoint(... metric_value=val_row["val_objdice"])`

## 常见误区

- 误区 1: 以为这里就是“再算个 Dice”
  - 实际上这里同时覆盖 pixel、boundary 和 object 三层指标
- 误区 2: 以为 `val_objdice` 只是日志里好看一点的字段
  - 实际上它是当前正式 best-selector
- 误区 3: 以为当前 eval 包已经全部讲完了
  - 实际上 threshold、run_eval、checkpoint_selector 和这里是四层不同职责

## 建议联读

- `src_eval_run_eval.py.md`
- `src_eval_threshold.py.md`
- `src_eval_checkpoint_selector.py.md`
- `configs_eval_eval_proto_v1.yaml.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_eval_threshold.py.md`，搞清楚二值预测是怎么来的
2. 再去看 `src_eval_run_eval.py.md`，搞清楚这些指标是怎样被聚进 validation epoch 的
3. 最后去看 `src_engine_trainer.py.md` 和 `src_eval_checkpoint_selector.py.md`，搞清楚 `val_objdice` 怎样进入 best checkpoint 决策

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 metrics 对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前 best selector 不是普通 Dice，而是 `val_objdice`
3. boundary 和 distance 指标为什么不能被“反正有 loss 就行”替代
4. 为什么当前不能把这里理解成 eval 包的唯一对象

## 5 分钟自检任务

1. 回到 `../../../../configs/eval/eval_proto_v1.yaml`，找到 `best_metric_name`
2. 回到 `../../../../src/engine/trainer.py`，找到 `scheduler.step(val_row["val_objdice"])`
3. 再回看 `../../../../src/metrics/seg_metrics.py`，说出 `object_dice_score()` 和 `boundary_f1_score()` 各自回答的是哪一类问题

如果这三步你都能顺下来，说明你已经把这份 metrics 说明文真正看懂了。
