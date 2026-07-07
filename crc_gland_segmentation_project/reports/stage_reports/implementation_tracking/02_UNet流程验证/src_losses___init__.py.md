# src_losses___init__.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/losses/__init__.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `one frozen segmentation loss builder exposed as the public package API`
- 章节: `package facade for stable BCE + Dice loss construction`
- 公式/定义: `src.losses` package -> `BCEDiceLoss` + `build_seg_loss()` as the formal loss-facing API

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/losses/__init__.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `loss_name`, `loss_version`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/losses/__init__.py`
- 符号: `BCEDiceLoss` / `build_seg_loss()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 的正式损失入口到底是谁。

答案就是 `../../../../src/losses/__init__.py`。

你可以把它理解成损失层的“统一售票口”。

用人话说，真正的 BCE + Dice 细节在 `../../../../src/losses/seg_losses.py` 里，但训练入口不应该直接和那个实现文件死绑。

它应该面对一层已经冻结好的包级门面。

如果没有这份文件，训练入口只是在“凑巧调用一个实现文件”；有了它，才算真正形成了正式损失公开入口。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/train/unet_flow_v1.yaml
        ↓
scripts/train.py
        ↓
src/losses/__init__.py
        ↓
src/losses/seg_losses.py
        ↓
loss_value / backward / optimizer.step
```

这里最关键的事实有四条:

1. `../../../../scripts/train.py` 当前真实写了 `from src.losses import build_seg_loss`
2. `../../../../src/losses/__init__.py` 只公开 `BCEDiceLoss` 和 `build_seg_loss`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已经写明 `loss_value=1.2771382331848145`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经写明 `backward_executed=true` 和 `optimizer_step_executed=true`

当前最硬的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/losses/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.losses import build_seg_loss`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `loss_value=1.2771382331848145`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `optimizer_step_executed=True`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`

说白了，这里不是“loss 目录里顺手放一个导出文件”，而是正式训练入口到底通过哪个公开接口拿到冻结损失对象。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/losses/seg_losses.py`
- `../../../../src/engine/trainer.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前正式损失已经冻结为 `BCE + Dice`
2. 当前入口层必须能稳定回链到正式损失公开接口
3. 当前说明文可以把“loss 入口层”和“loss 具体公式实现”拆开讲

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式损失包门面
- 当前冻结字段:
  - `loss_name=bce_dice`
  - `loss_version=seg_loss_v1`
- 当前最硬证据:
  - `../../../../scripts/train.py` 通过 `src.losses` 取正式 builder
  - `../../../../src/losses/__init__.py` 用 `__all__` 明确公开 `BCEDiceLoss` 和 `build_seg_loss`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `loss_value=1.2771382331848145`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true` 和 `optimizer_step_executed=true`

这里必须诚实说明:

当前证据更强地证明了“当前训练主链确实通过 `src.losses` 这个门面拿到冻结损失并完成了反向传播”，还没有单独证明将来如果扩成更多损失家族，这个门面已经准备好多策略并存。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 从 `../../../../src/losses/seg_losses.py` 导出 `BCEDiceLoss`
2. 从 `../../../../src/losses/seg_losses.py` 导出 `build_seg_loss()`
3. 用 `__all__` 把正式公开损失 API 清单固定下来

### 关键点 1: 为什么要同时公开类和 builder

因为它们回答的问题不一样。

`BCEDiceLoss` 回答“正式损失对象是什么”；
`build_seg_loss()` 回答“训练入口怎样按冻结配置实例化它”。

### 关键点 2: 为什么包门面值得单独进 A 类

因为当前训练入口真实 import 面就在这里。

只要 `scripts/train.py` 正式通过它取 loss builder，它就已经属于工程公开边界的一部分。

### 关键点 3: 为什么这里不提前暴露别的 loss

因为当前首轮基线只允许 `BCE + Dice`。

如果这里提前把别的候选损失一起公开，说明文和审计边界都会开始变虚。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是由 `../../../../scripts/train.py` 间接消费。

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

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“为什么不让 `../../../../scripts/train.py` 直接从 `src.losses.seg_losses` 导入，不要多一层门面？”

用人话说，短期可以。

但那样训练入口、包级公开接口和具体公式实现会混成一层。

单独保留门面以后，训练入口只面对稳定损失 API，说明文也能清楚分层。

### 设计取舍 1: 为什么这里公开 `BCEDiceLoss`

因为当前冻结口径并不只是一个函数名，它对应的是正式损失对象本身。

### 设计取舍 2: 为什么这里公开 `build_seg_loss()`

因为训练入口真正消费的是 builder，而不是手写实例化细节。

### 设计取舍 3: 为什么这份对象不能被 `src_losses_seg_losses.py.md` 替代

因为二者的职责不同:

1. `src_losses_seg_losses.py.md` 解释损失实现细节
2. 这份门面说明文解释正式公开入口

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../scripts/train.py`
2. 打开 `../../../../src/losses/__init__.py`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- 训练入口是否直接从 `src.losses` 导入 builder
- `loss_value` 是否已经出现真实数值
- `backward_executed` 和 `optimizer_step_executed` 是否都为真
- `__all__` 是否已经把正式损失公开接口钉死

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/losses/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.losses import build_seg_loss`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `loss_value=1.2771382331848145`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `optimizer_step_executed=True`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `optimizer_step_executed=true`

## 常见误区

- 误区 1: 以为解释了 `../../../../src/losses/seg_losses.py` 就等于解释了损失入口层
  - 实际上包门面和具体实现不是一回事
- 误区 2: 以为这里导出一个 builder 只是编码习惯
  - 实际上它已经是训练入口真实依赖的正式公开 API
- 误区 3: 以为门面越宽越灵活
  - 实际上当前阶段更需要冻结，而不是提前扩很多候选损失

## 建议联读

- `src_losses_seg_losses.py.md`
- `configs_train_unet_flow_v1.yaml.md`
- `scripts_train.py.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_train_unet_flow_v1.yaml.md`，确认 `BCE + Dice` 的冻结来源
2. 再去看 `src_losses_seg_losses.py.md`，理解损失具体实现
3. 最后回到 `scripts_train.py.md`，确认入口如何通过 `src.losses` 门面把损失接进主链

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 为什么 `src.losses` 包门面本身应该算正式对象
2. 它和 `../../../../src/losses/seg_losses.py` 的边界分别是什么
3. 为什么当前训练入口必须通过门面取 loss builder
4. 为什么反向传播证据能反过来证明这层入口已经真的被消费

## 5 分钟自检任务

1. 回到 `../../../../scripts/train.py`，找到 `from src.losses import build_seg_loss`
2. 回到 `../../../../src/losses/__init__.py`，说出它公开了哪两个正式符号
3. 再回看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，解释为什么 `backward_executed=true` 能说明这条损失入口链已经真的跑过

如果这三步你都能顺下来，说明你已经把这份 loss package 门面说明文真正看懂了。
