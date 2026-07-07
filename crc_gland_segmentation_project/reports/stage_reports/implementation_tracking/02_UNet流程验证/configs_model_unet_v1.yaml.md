# configs_model_unet_v1.yaml.md

## 结构化溯源卡片

- 正式对象: `../../../../configs/model/unet_v1.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 章节: `standard encoder-decoder baseline`
- 公式/定义: `in_channels + out_channels + base_channels -> formal UNet instantiation`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../configs/model/unet_v1.yaml`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/model/unet_v1.yaml`
- 对应字段: `model_name`, `model_version`, `in_channels`, `out_channels`, `base_channels`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 当前这个文件说明了什么

这份配置文件回答的是:

当前 stage02 的正式模型参数到底冻结成什么样。

你可以把它理解成 `src/models/unet.py` 的参数卡。

换句话说，模型代码负责怎么搭结构，这份配置负责明确“当前到底认哪组结构参数”。

## 这张表/这个文件长什么样

这个文件字段不多，主要就是:

1. 模型名与版本
2. 输入通道数
3. 输出通道数
4. 基础通道宽度
5. 架构来源标记

## 当前真实结果

当前最关键的真实字段有 5 组:

1. `model_name=unet`
2. `model_version=unet_v1`
3. `in_channels=3`
4. `out_channels=1`
5. `base_channels=32`

当前最关键的真实路径也有 4 组:

1. 模型配置路径 `../../../../configs/model/unet_v1.yaml`
2. 模型实现路径 `../../../../src/models/unet.py`
3. experiment 索引路径 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
4. runtime 证据路径 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

这些结果已经和正式证据对上:

- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`
- `../../../../src/models/unet.py` 的 builder 会直接消费这里的 3 个核心结构字段

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前 model config 是当前阶段正式协议点名的模型冻结口径
2. 当前路线锁定要求先沿用标准单头 UNet，而不是提前扩成更多 backbone
3. 当前正式规则要求输入输出 shape 与模型参数能直接对账

## 这些列/字段分别是什么意思

- `model_name`: 当前正式模型名
- `model_version`: 当前正式模型版本名
- `in_channels`: 输入通道数，这里固定是 RGB 的 `3`
- `out_channels`: 输出通道数，这里固定是二值 gland logits 的 `1`
- `base_channels`: 当前 U-Net 的基础宽度
- `arch_source`: 当前结构来源标签

## 为什么这样组织

如果没有这份配置，模型结构最容易变成代码里随手改常量。

短期看好像快一点，长期最难回链。

当前把关键结构参数收进这份配置，本质上是在保护模型结构和 runtime 证据能逐项对账。

## 这个文件没说明什么

这份文件不负责解释:

- `src/models/unet.py` 每一层具体怎么前向传播
- skip connection 的实现细节
- 为什么 bilinear upsample 比 transposed conv 更适合当前首轮

这些问题要去看 `src_models_unet.py.md`。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../configs/model/unet_v1.yaml`
2. 对照 `../../../../src/models/unet.py`
3. 再对照 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

期望结果:

- `in_channels=3` 和 `input_shape=[2, 3, 512, 512]` 对得上
- `out_channels=1` 和 `output_shape=[2, 1, 512, 512]` 对得上
- `base_channels=32` 确实不是脚本里临时写死
- 具体路径 `../../../../configs/model/unet_v1.yaml` 与 `../../../../src/models/unet.py` 都真实存在

## 与项目其他部分的关联

- 上游: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 下游: `../../../../src/models/unet.py`
- 证据回链: `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 常见问题

- 容易误解 1: 以为这份配置只是模型名标签
  - 实际上它还冻结了输入/输出通道和宽度
- 容易误解 2: 以为模型 shape 证据只能从代码里看
  - 实际上 runtime-evidence 已经给出真实输入输出 shape

## 建议联读

- `src_models_unet.py.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `scripts_train.py.md`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答:

1. 当前 stage02 的正式模型参数冻结了哪几项
2. 为什么 `in_channels=3` 和 `out_channels=1` 是当前最关键的两个字段
3. runtime 里的输入输出 shape 为什么能回到这份配置
