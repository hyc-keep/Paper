# src_eval_threshold.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/eval/threshold.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `binary segmentation probability thresholding`
- 章节: `sigmoid and fixed cutoff before metric computation`
- 公式/定义: logits(float32) -> sigmoid -> threshold -> binary mask

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/eval/threshold.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `threshold_value=0.5`, `threshold_source=val17`, `eval_cast_policy=float32_before_threshold`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

### 当前实现落点

- 文件: `../../../../src/eval/threshold.py`
- 符号: `apply_threshold()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把模型输出的浮点 logits 变成给指标层消费的二值预测 mask。

答案就是 `../../../../src/eval/threshold.py`。

你可以把它理解成 stage02 验证链里的“闸门开关”。

用人话说，模型输出的是连续数值，不是最终的 0/1 预测。真正决定“多大算前景、多小算背景”的，就是这里。

如果没有这份文件，`../../../../src/metrics/seg_metrics.py` 只能拿到浮点 logits，后面的对象级和边界级指标口径就会变得很飘。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
src/models/unet.py
        ↓
src/eval/threshold.py
        ↓
src/metrics/seg_metrics.py
        ↓
src/eval/run_eval.py
        ↓
src/engine/trainer.py
```

这里最关键的事实有三条:

1. `../../../../src/eval/run_eval.py` 会直接调用 `apply_threshold(logits, threshold_value)`
2. `../../../../configs/eval/eval_proto_v1.yaml` 已把 `threshold_value=0.5` 与 `threshold_source=val17` 冻结下来
3. 阈值前显式转成 `float32`，和正式评估协议中的 `float32_before_threshold` 口径一致

当前最硬的物理证据至少有 5 组:

1. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_value=0.5`
2. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_source=val17`
3. `../../../../src/eval/run_eval.py` 写明 `pred_masks.append(apply_threshold(logits, threshold_value).cpu().numpy())`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_dtype=float32`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`

说白了，这一步不是可有可无的后处理细节，而是把模型连续输出变成正式评估输入的硬边界。

## 与项目其他部分的关联

### 上游依赖

- `../../../../src/models/unet.py`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../src/eval/run_eval.py`

### 下游消费者

- `../../../../src/eval/run_eval.py`
- `../../../../src/metrics/seg_metrics.py`
- `../../../../src/engine/trainer.py`
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

1. 当前阈值来源不是现场临时调的，而是 `val17`
2. 当前 threshold 不是自适应实验位点，而是冻结的 `0.5`
3. 当前阈值逻辑必须先于 metric 逻辑完成，不能让指标层重新猜预测语义

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式阈值化层
- 当前冻结字段:
  - `threshold_value=0.5`
  - `threshold_source=val17`
  - `eval_cast_policy=float32_before_threshold`
- 当前最硬证据:
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_value=0.5`
  - `../../../../configs/eval/eval_proto_v1.yaml` 写明 `eval_cast_policy=float32_before_threshold`
  - `../../../../src/eval/run_eval.py` 写明 `apply_threshold(logits, threshold_value)`

这里必须诚实说明:

当前证据能证明的是“正式验证链已经固定了阈值化动作”，不是“当前项目已经进入多阈值或自适应阈值实验阶段”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 先把 logits 转成 `float32`
2. 再用 `sigmoid()` 变成概率
3. 最后按固定的 `threshold_value` 压成 `torch.uint8` 二值 mask

### 关键点 1: 为什么阈值前要先转 `float32`

因为当前正式评估规则已经把这件事写死了。

说白了，当前想要的是稳定、可解释的阈值输入，而不是让半精度或别的 dtype 差异偷偷影响最终预测。

### 关键点 2: 为什么输出是 `uint8`

因为下游 metric 链吃的是离散二值预测。

如果这里还继续保留浮点概率，后面的 object/boundary 指标就会开始混淆“连续置信度”和“离散前景语义”。

### 关键点 3: 为什么阈值逻辑单独拆成一个文件

因为它是正式评估链里的独立规则位点。

把它单独拆开后，validation 聚合对象负责聚合，metrics 对象负责计分，边界更清楚。

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

“为什么不把 threshold 直接写死在 validation 聚合对象里？”

用人话说，写死当然也能跑，但那样会把“阈值规则”和“验证聚合逻辑”揉成一团。

单独拆开后，后面无论解释配置、解释验证函数，还是对账 formal rule，都更清楚。

### 设计取舍 1: 为什么不在这里做 connected components

因为这里的职责只到“连续值 -> 二值 mask”。

连通域和对象级指标应该交给 metrics 层去做。

### 设计取舍 2: 为什么不支持一堆阈值 mode

因为当前 stage02 只需要一个冻结过的正式阈值。

如果现在就把 mode 做成大而全，说明文边界会先漂掉。

### 设计取舍 3: 为什么不直接输出 bool

因为当前下游既要进 numpy，也要和现有 metric 实现对齐，`uint8` 更稳，也更接近当前项目里“二值 mask 资产”的语义。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/eval/eval_proto_v1.yaml`
2. 打开 `../../../../src/eval/run_eval.py`
3. 打开 `../../../../src/eval/threshold.py`
4. 对照 `../../../../src/metrics/seg_metrics.py`

### 当前最关键的核对点

- `threshold_value=0.5` 是否和 `apply_threshold(logits, threshold_value)` 对上
- `float32_before_threshold` 是否和 `logits.float()` 对上
- 二值输出是否真的进入了 metrics 层

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/eval/threshold.py`
2. 具体路径已经固定在 `../../../../configs/eval/eval_proto_v1.yaml`
3. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `threshold_value=0.5`
4. `../../../../configs/eval/eval_proto_v1.yaml` 写明 `eval_cast_policy=float32_before_threshold`
5. `../../../../src/eval/run_eval.py` 写明 `apply_threshold(logits, threshold_value)`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_dtype=float32`

## 常见误区

- 误区 1: 以为 threshold 只是一个无关紧要的小 helper
  - 实际上它是把 logits 变成正式预测语义的边界点
- 误区 2: 以为 `0.5` 可以训练时随便改
  - 实际上当前阈值来源和阈值值都已冻结
- 误区 3: 以为 threshold 一讲完，整个 eval 包也就讲完了
  - 实际上 run_eval、metrics 和 checkpoint selector 还是不同层

## 建议联读

- `src_eval_run_eval.py.md`
- `src_metrics_seg_metrics.py.md`
- `configs_eval_eval_proto_v1.yaml.md`
- `src_eval_checkpoint_selector.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_eval_run_eval.py.md`，搞清楚 threshold 是在 validation epoch 的哪一步被调用的
2. 再去看 `src_metrics_seg_metrics.py.md`，搞清楚二值预测怎样被算成正式指标
3. 最后去看 `src_eval_checkpoint_selector.py.md`，搞清楚 `val_objdice` 怎样影响 best checkpoint 决策

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 threshold 对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前 threshold 不能藏在 validation 聚合对象里不解释
3. `threshold_value=0.5` 和 `threshold_source=val17` 到底是从哪份正式配置来的
4. 为什么这里的输出必须是离散二值预测而不是继续保留概率

## 5 分钟自检任务

1. 回到 `../../../../configs/eval/eval_proto_v1.yaml`，找到 `threshold_source`
2. 回到 `../../../../src/eval/run_eval.py`，找到 `apply_threshold(logits, threshold_value)`
3. 再回看 `../../../../src/eval/threshold.py`，说出这里在 sigmoid 前后各做了什么

如果这三步你都能顺下来，说明你已经把这份 threshold 说明文真正看懂了。
