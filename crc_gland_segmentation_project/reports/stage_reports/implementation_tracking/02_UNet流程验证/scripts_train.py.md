# scripts_train.py.md

## 结构化溯源卡片

- 正式对象: `../../../../scripts/train.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 章节: `encoder-decoder supervised segmentation pipeline`
- 公式/定义: `image -> logits -> supervised loss -> backward -> optimizer.step`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../scripts/train.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `input_size=512x512`, `BCE + Dice`, `AdamW`, `ReduceLROnPlateau`, `best_selector=val_objdice_max`, `threshold_source=val17`

### 当前实现落点

- 文件: `../../../../scripts/train.py`
- 符号: `parse_args()` / `load_experiment_config()` / `resolve_data_config_path()` / `validate_formal_handoff()` / `run_stage02_runtime_check()` / `run_stage02_training()` / `main()`

## 这个脚本的作用

这个脚本负责一件非常核心的事: 把 stage02 的“正式训练入口”真正落成项目里可执行、可回链、可产证据的那一个入口。

你可以把它理解成“stage02 的总闸门”。

后面的 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`、`../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`、`../../../../b_class_auxiliary/runtime_checks/code_quality_gate_report.md` 和 `../../../../b_class_auxiliary/runtime_checks/workflow_gate_report.md` 之所以能成立，不是因为大家口头同意 `../../../../scripts/train.py` 应该能跑，而是因为这个脚本真的把正式配置、正式数据链和最小训练步接起来了。

用人话说，这个文件最重要的价值不是“它名字叫 train”，而是“它真的让训练入口从概念变成了物理证据”。

## 这个脚本在整个阶段中的位置

如果你现在还不熟 stage02，可以先记住一句话:

`../../../../scripts/train.py` 不是某个辅助工具，它就是当前阶段最正式的入口文件。

它在链路里的位置可以画成这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
configs/data/glas.yaml
configs/model/unet_v1.yaml
configs/train/unet_flow_v1.yaml
configs/eval/eval_proto_v1.yaml
        ↓
src/data/* + src/models/unet.py + src/losses/seg_losses.py
        ↓
scripts/train.py
        ↓
b_class_auxiliary/runtime_checks/runtime_check_report.md
b_class_auxiliary/runtime_checks/runtime_evidence.json
b_class_auxiliary/runtime_checks/code_quality_gate_report.md
```

上游依赖有 5 层:

1. experiment config
2. data / model / train / eval 四类正式配置
3. `src/data/*` 的数据消费链
4. `src/models/unet.py` 和 `src/losses/seg_losses.py`
5. `src/engine/*` 与 `src/eval/*`

下游消费者同样很明确:

1. `../../../../b_class_auxiliary/tools/run_minimal_runtime_check.py`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`
4. `../../../../b_class_auxiliary/runtime_checks/code_quality_gate_report.md`
5. `../../../../b_class_auxiliary/runtime_checks/workflow_gate_report.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 0: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一段回链不是为了把路径堆满，而是为了证明:

1. 这个入口为什么属于 `02_UNet流程验证`
2. 它为什么必须消费这 4 份配置
3. 它为什么要把 `best_selector`、`threshold_source`、`run_name` 这些字段写进 run meta

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式训练入口，同时承担 `runtime-check` 真值出口
- 当前真实边界: `主 run 已经完成 full run 收口；同一入口也支持 runtime-check 的最小单步真值采样，但当前还没有为所有 stage02 对象建立逐文件说明文`
- 当前最硬的物理证据:
  - `runtime_profile=full_training_runtime`
  - `sample_id=GlaS_official_train_train_42`
  - `input_shape=[2, 3, 512, 512]`
  - `target_shape=[2, 1, 512, 512]`
  - `output_shape=[2, 1, 512, 512]`
  - `loss_value=1.2771382331848145`
  - `backward_executed=true`
  - `optimizer_step_executed=true`

你现在可能会问:

“既然它已经能做这些事，为什么状态页写的是当前说明文覆盖 `pass（当前锁定范围）`，却又还说不是 stage02 全量说明文完工？”

因为这里在区分两件不同的事:

1. 脚本本身有没有真正实现
2. stage02 的所有对象说明文有没有全部补齐

第 1 件已经成立；当前锁定范围内的说明文也已经收口。
但整个 stage02 仓库里的全量正式对象说明文，还不能在这份入口说明文里被过度宣称成“全部完成”。

## 脚本核心逻辑

### 主要流程

这个脚本当前的核心主链可以拆成 7 步:

1. 读取 `--config` 指向的 experiment config
2. 判断当前是走 stage01 preflight 还是 stage02 训练支路
3. 解析 experiment config 里的 data、model、train、eval 四类 config 引用
4. 检查 train / val 的 formal handoff 是否成立
5. 构建 dataset、dataloader、UNet、loss 和 optimizer
6. 如果启用 `--runtime-check`，直接执行一个最小 train step
7. 如果走正常支路，则进入 `train -> val -> scheduler -> checkpoint` 闭环

### 关键函数 1：`load_experiment_config()`

这个函数负责把“当前到底认哪一套实验配置”变成显式输入。

为什么这一步重要？

因为 stage02 最容易漂移的地方，就是有人直接在脚本里写死数据配置或模型配置。

当前这里坚持先读 experiment config，再去解引用其他配置，本质上是在保护配置链。

换句话说，它让 `run_name`、`dataset_code`、`config_refs` 这些字段都有唯一来源，不会飘成脚本里的隐式常量。

### 关键函数 2：`resolve_data_config_path()` 与 `resolve_config_ref()`

这两个函数解决的是同一个问题:

“训练入口到底应该认哪份 data / model / train / eval 配置？”

当前正式 experiment config 是 `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`。
它会把配置解析到:

- `configs/data/glas.yaml`
- `configs/model/unet_v1.yaml`
- `configs/train/unet_flow_v1.yaml`
- `configs/eval/eval_proto_v1.yaml`

如果你把这几层关系写死在脚本里，短期看像是省事，长期最容易出两个问题:

1. 版本链丢失
2. learning doc 根本没法回链到真实配置来源

### 关键函数 3：`validate_formal_handoff()`

这个函数特别值得盯。

它检查的不是“目录里好像有文件”，而是正式数据阶段交接有没有真的成立。

当前它至少会核对:

- `data_stage_pass`
- `handoff_ready`
- `preflight_pass`
- split 资产是否存在
- data config 是否已经在 manifest 里登记

说白了，这一步就是在防止训练入口绕开 stage01 已经冻结好的输入层。

### 关键函数 4：`run_stage02_runtime_check()`

这是当前最关键的真值出口。

它会真实执行下面这条链:

1. 从 `train_loader` 取 batch
2. `images -> model`
3. `logits -> loss`
4. `loss.backward()`
5. `optimizer.step()`
6. 把结构化 payload 写到 `b_class_auxiliary/runtime_checks/train_runtime_payload.json`

当前真实产出的关键信息包括:

- `input_shape=[2, 3, 512, 512]`
- `target_shape=[2, 1, 512, 512]`
- `output_shape=[2, 1, 512, 512]`
- `loss_value=1.2771382331848145`
- `loss_is_finite=true`
- `backward_executed=true`
- `optimizer_step_executed=true`

这一步为什么这么重要？

因为没有它，`../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 的 `pass` 就只能停留在“原始样本可读”那一层。

### 关键函数 5：`run_stage02_training()`

这个函数是正常训练支路的总装配器。

它会:

1. 读取 train / val 两套 handoff 检查
2. 构造 `build_augment_config()`、`build_train_transform()`、`build_eval_transform()`
3. 构造 train / val dataset 与 dataloader
4. 构造 UNet、loss、optimizer、scheduler、early stopper
5. 在不是 runtime-check 的情况下把训练过程交给 `train_model()`

你可以先把它想成“把 stage02 散落组件装成同一条正式执行链的人”。

### 为什么不用别的设计？

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 另起一个临时 runtime 脚本 | 改起来快 | 真值链和正式入口分家, 后续门禁会失真 | 否决 |
| 在 `../../../../b_class_auxiliary/tools/run_minimal_runtime_check.py` 里自己拼模型和 loss | 不用改入口 | 绕开正式训练入口, learning doc 也没法解释真实主链 | 否决 |
| 让 `scripts/train.py` 同时承担训练入口和 runtime 真值出口 | 一个入口可审计 | 结构更复杂 | 采用 |

## 如何运行这个脚本

### 运行方式 1：stage02 runtime-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --run-name A1_UNet_GlaS_v1_seed3407 --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1
```

### 运行方式 2：本地 smoke-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --smoke-check --device cpu
```

### 运行参数里最值得盯的项

- `--config`: 锁定当前 experiment config
- `--runtime-check`: 触发真实单步训练真值
- `--runtime-check-output`: 指定 payload 输出位置
- `--smoke-check`: 切到最小本地训练闭环
- `--device`: 当前一般是 `cpu`

## 如何验证脚本运行结果

### 检查方法

1. 先运行 runtime-check 命令
2. 打开 `b_class_auxiliary/runtime_checks/runtime_check.log`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前真实结果

当前最关键的日志信号有:

- `run_name=A1_UNet_GlaS_v1_seed3407`
- `device=cpu`
- `steps_executed=1`
- `sample_id=GlaS_official_train_train_42`
- `loss_value=1.277138`

当前最关键的通过标准有:

1. `runtime_check_status=pass`
2. `runtime_execution_status=pass`
3. `tensor_shape_dtype_pass=pass`
4. `loss_finite_pass=pass`
5. `grad_step_pass=pass`

### 为什么不能只看脚本有没有报错

如果你只看“命令退出码是不是 0”，最容易漏掉三件事:

1. 有没有真的拿到 batch
2. 有没有真的算出 loss
3. 有没有真的完成 backward 和 optimizer.step

所以更稳的检查方法，必须同时看 report、json 和 log。

## 常见误区

- 误区 1: 以为 `../../../../scripts/train.py` 只是 shell 入口
  - 实际上它是当前 stage02 的正式主入口
- 误区 2: 以为 runtime-check 只是读个样本看看
  - 实际上它已经真实执行了一次 train step
- 误区 3: 以为当前已经把 stage02 全部对象解释完了
  - 实际上当前只是先把入口对象讲透

## 建议联读

- `README.md`
- `implementation_status.md`
- `当前阶段为什么能pass以及下一步怎么看.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. `../../../../scripts/train.py` 在 stage02 里到底承担什么角色
2. runtime-check 为什么必须放在正式入口里跑
3. 当前 `pass` 的证据到底来自哪些真实字段
4. 为什么现在还不能说 stage02 全量说明文已经完成

## 5 分钟自检任务

1. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`，找到 `loss_value`
2. 回到 `runtime_evidence.json`，找到 `backward_executed`
3. 再看 `implementation_status.md`，说出“当前锁定范围已 pass”和“stage02 全量说明文未宣称全部完成”为什么可以同时成立

如果这三步你都能顺下来，说明你已经真正看懂这份入口说明文，不只是把文件名记住了。
