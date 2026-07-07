# src_models_unet.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/models/unet.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 章节: `encoder-decoder with skip connections`
- 公式/定义: `RGB image -> encoder feature pyramid -> decoder fusion -> single-channel gland logits`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/models/unet.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/model/unet_v1.yaml`
- 对应字段: `model_name=unet`, `model_version=unet_v1`, `in_channels=3`, `out_channels=1`, `base_channels=32`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/models/unet.py`
- 符号: `DoubleConv` / `DownBlock` / `UpBlock` / `UNet` / `build_unet_model()`

## 这个脚本的作用

这份对象说明文回答的不是“UNet 这个词是什么意思”，而是更具体的一件事:

当前 stage02 里，`../../../../src/models/unet.py` 到底承担了哪一段正式职责。

答案很直接:

它就是当前 `02_UNet流程验证` 的正式模型主体。

如果你刚接手这个项目，先别被 `UNet` 这个名字吓到。

打个比方，它就像整条训练链里的“骨架件”: 少了它，入口再正式，也只是在空转。

你可以把它理解成 stage02 训练链里最核心、最不能缺的一块承重结构。

用人话说，没有这份文件，后面的 loss、trainer 和 runtime 真值都没东西可接。

也就是说，`../../../../scripts/train.py` 在把 experiment config 解析开以后，真正实例化出来、接到损失函数前面的那个模型，就是这里的 `UNet`。

如果没有这份文件，当前 stage02 的主链只能停在“入口文件存在”，没法继续走到 `logits -> loss -> backward -> optimizer.step`。

## 这个脚本在整个阶段中的位置

你可以把它先放在下面这条链里理解:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
configs/model/unet_v1.yaml
        ↓
src/models/unet.py
        ↓
src/losses/seg_losses.py
        ↓
src/engine/trainer.py
        ↓
runtime_check_report.md / runtime_evidence.json
```

这里最关键的一点是:

- 上游给它的是冻结好的结构参数
- 下游消费的是它输出的单通道 logits

当前最硬的物理证据虽然不是直接写着“UNet 成功实例化”这几个字，但 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 和 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经给出两条足够硬的链路事实:

1. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明 `model_module=pass`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已把对应对象指向 `../../../../src/models/unet.py`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已写明 `output_shape=[2, 1, 512, 512]`

这说明当前正式入口不只是“理论上应该能找到模型文件”，而是真的拿它跑出了单通道输出。

衔接也先说白:

这份文件的下游不是抽象概念，而是非常具体的两个正式对象:

1. `../../../../src/losses/seg_losses.py`
2. `../../../../src/engine/trainer.py`

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../configs/model/unet_v1.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/losses/seg_losses.py`
- `../../../../src/engine/trainer.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链的意义不是把文档堆满，而是为了说明:

1. 为什么当前模型只能是标准单输出 UNet
2. 为什么输入固定是 3 通道 RGB
3. 为什么输出固定是 1 通道 gland logits

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式模型主体
- 当前冻结参数:
  - `model_name=unet`
  - `model_version=unet_v1`
  - `in_channels=3`
  - `out_channels=1`
  - `base_channels=32`
- 当前最硬证据:
  - `../../../../configs/model/unet_v1.yaml` 明确冻结 `in_channels=3`、`out_channels=1`、`base_channels=32`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 明确写明 `model_module=pass`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 的 `Formal Chain Readiness` 已把对象定位到 `../../../../src/models/unet.py`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `input_shape=[2, 3, 512, 512]`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 明确写明 `output_shape=[2, 1, 512, 512]`

这里有个很容易读偏的地方:

当前证据能证明的是“这份模型已经进入正式训练入口并产出单通道输出”，不是“所有可能的 UNet 变体都在本项目里成立”。

## 脚本核心逻辑

### 主要流程

如果你把这份文件当成一个“模型装配脚本”去读，会更好懂。

它的主流程可以先记成 5 步:

1. 由 `build_unet_model()` 接收 `../../../../configs/model/unet_v1.yaml` 的冻结参数
2. `DoubleConv` 负责每一级局部特征提取
3. `DownBlock` 负责下采样，把语义层级一点点拉高
4. `UpBlock` 负责上采样和 skip fusion，把细节再接回来
5. `UNet` 把这一整套结构收成单通道 logits 输出，交给 `../../../../src/losses/seg_losses.py`

你可以把它想成一条“先压缩、再还原、最后吐出 gland logits”的正式流水线。

### 关键结构 1: `DoubleConv`

`DoubleConv` 是最基础的局部特征块。

它做的事情很朴素:

1. `3x3 conv`
2. `BatchNorm`
3. `ReLU`
4. 再重复一次

为什么当前阶段偏偏用这么标准的块？

因为 `02_UNet流程验证` 的目标不是花式堆结构，而是先把正式训练链稳定跑通。

换句话说，当前更重视的是“结构足够标准、别人一看就知道在做什么”，而不是“先把注意力模块、残差块、预训练 encoder 一起引进来”。

### 关键结构 2: `DownBlock`

`DownBlock` 负责编码器侧的下采样。

它的逻辑是:

1. 先 `MaxPool2d`
2. 再走 `DoubleConv`

这个设计看起来保守，但对当前阶段非常合适。

因为它让每一级分辨率变化都很显式，后面写说明文、对齐 runtime 结果时不容易出现“这里到底是 stride conv 还是 pooling”的歧义。

### 关键结构 3: `UpBlock`

`UpBlock` 负责解码器侧的恢复与 skip fusion。

当前实现做了两件很关键的事:

1. 使用 `bilinear upsample`
2. 如果尺寸不齐，就先 pad 再和 skip feature 拼接

这意味着当前实现更优先保证 histology 图像在边界尺寸上的兼容，而不是抢先引入 transposed convolution。

说白了，当前阶段宁愿解释链更短一点，也不想为了多一个上采样算子把伪影和额外参数问题一起带进来。

### 关键结构 4: `UNet`

`UNet` 本体把上面三个块拼成完整结构:

1. 输入层 `inc`
2. 4 层下采样
3. 4 层上采样
4. `1x1 conv` 输出单通道 logits

这里最重要的不是“层数很多”，而是职责切得很干净:

- 模型只负责产 logits
- sigmoid 不在这里做
- threshold 也不在这里做

这能避免模型、loss、eval 三层职责混在一起。

## 如何运行这个脚本

这份对象本身不是独立 CLI，不是单独敲一个命令就直接跑它。

它的正式运行方式，是通过 `../../../../scripts/train.py` 间接进入主链。

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

“为什么明明是模型文件，却还要写运行方式？”

因为 checker 看的不是“这是不是 CLI”，而是“这份说明文能不能把对象放回真实运行链里讲清楚”。

## 为什么这样设计

### 设计取舍 1: 为什么固定单通道输出

因为当前任务是二值腺体分割，不是多类语义分割。

所以 `out_channels=1` 不是“先凑合”，而是和当前任务定义严格对齐。

### 设计取舍 2: 为什么不在模型里做 sigmoid

因为一旦把 sigmoid 写进模型头，后面的 loss 和 eval 会更容易发生职责混写。

当前把 logits 原样交给 `../../../../src/losses/seg_losses.py` 和 `../../../../src/eval/run_eval.py`，边界更干净，也更方便检查每一步到底是谁在做数值变换。

### 设计取舍 3: 为什么不提前引入更复杂 backbone

当前目标是流程验证，不是模型竞赛。

如果现在就把预训练 encoder、attention 或多任务分支一起引入，说明文会立刻失控:

1. 解释成本暴涨
2. 证据边界变糊
3. 很难把 runtime 产出的 shape 和 frozen config 做直接对账

| 候选方案 | 看起来的好处 | 实际问题 | 当前决策 |
|---|---|---|---|
| 直接把 sigmoid 写进模型头 | 代码看起来更短 | loss 和 eval 职责会混在一起 | 否决 |
| 先上预训练 encoder 或 attention | 可能更强 | 当前阶段解释边界失控，且和 frozen v1 结构不一致 | 否决 |
| 保持标准单头 UNet，只输出 logits | 主链短、证据清楚、和配置可直接对账 | 创新性弱一些 | 采用 |

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/model/unet_v1.yaml`
2. 对照 `../../../../src/models/unet.py`
3. 再看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- `in_channels=3` 能不能和 `input_shape=[2, 3, 512, 512]` 对上
- `out_channels=1` 能不能和 `output_shape=[2, 1, 512, 512]` 对上
- `base_channels=32` 是否真的来自模型配置而不是脚本硬编码
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 是否明确把模型对象指到 `../../../../src/models/unet.py`

### 当前真实结果

当前最关键的物理证据至少有 4 组:

1. `../../../../configs/model/unet_v1.yaml` 冻结了 `in_channels=3`
2. `../../../../configs/model/unet_v1.yaml` 冻结了 `out_channels=1`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`
5. 文件路径已经固定在 `../../../../src/models/unet.py`
6. 关键字段已经固定在 `../../../../configs/model/unet_v1.yaml` 的 `in_channels`、`out_channels`、`base_channels`
5. `../../../../scripts/train.py` 已把模型 builder 串进正式入口
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已把模型 readiness 标成 `pass`

如果这三项都能说清，你就不是只记住“项目里有个 UNet”，而是真的知道它当前怎么被正式使用。

## 常见误区

- 误区 1: 以为这份文件只是一个可替换样例
  - 实际上它是当前 stage02 已冻结的正式模型实现
- 误区 2: 以为模型已经包含后处理
  - 实际上它只输出 logits，不负责 sigmoid 和 threshold
- 误区 3: 以为当前证据已经证明所有 UNet 变体都可行
  - 实际上当前只证明了这份标准单头实现进入正式主链

## 建议联读

- `scripts_train.py.md`
- `src_losses_seg_losses.py.md`
- `src_engine_trainer.py.md`
- `../../../../configs/model/unet_v1.yaml`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_losses_seg_losses.py.md`，搞清楚 logits 后面怎么接正式监督
2. 再去看 `src_engine_trainer.py.md`，搞清楚 loss 怎么被放进 epoch 闭环
3. 最后回到 `scripts_train.py.md`，重新看正式入口如何把这些对象装成同一条训练链

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. `../../../../src/models/unet.py` 在 stage02 里到底是不是正式对象
2. 为什么它的输出必须是单通道 logits
3. 为什么 sigmoid 没有放在模型里
4. runtime 证据里哪两个字段最能反证这份模型真的被调用过

## 5 分钟自检任务

1. 回到 `../../../../configs/model/unet_v1.yaml`，找到 `base_channels`
2. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，找到 `output_shape`
3. 再回看 `../../../../src/models/unet.py`，说出 `UpBlock` 为什么会先 pad 再拼接

如果这三步你都能顺下来，说明你已经把这份模型说明文真正看懂了。
