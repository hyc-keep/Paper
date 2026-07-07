# configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md

## 结构化溯源卡片

- 正式对象: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 章节: `baseline experiment entry and reproducible training setup`
- 公式/定义: experiment config -> data, model, train, eval config refs plus run metadata

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 对应字段: `run_name`, `stage_code`, `dataset_code`, `model_name`, `config_refs`, `train_seed`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 当前这个文件说明了什么

这个文件不是训练逻辑本身，它更像一张“总索引卡”。

你可以把它理解成 stage02 配置链里的总入口。

说白了，当前正式训练到底认哪一套 data/model/train/eval 配置，不是靠人脑记忆，而是先看这份 experiment config。

## 这张表/这个文件长什么样

当前文件结构很短，但非常关键:

1. run 元信息
2. stage / dataset / model 基本标识
3. `config_refs.data`
4. `config_refs.model`
5. `config_refs.train`
6. `config_refs.eval`

## 当前真实结果

当前最关键的真实字段有 6 组:

1. `run_name=A1_UNet_GlaS_v1_seed3407`
2. `stage_code=A1`
3. `dataset_code=glas`
4. data 配置真实路径 `../../../../configs/data/glas.yaml`
5. model 配置真实路径 `../../../../configs/model/unet_v1.yaml`
6. train 配置真实路径 `../../../../configs/train/unet_flow_v1.yaml`
7. eval 配置真实路径 `../../../../configs/eval/eval_proto_v1.yaml`

`../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 也已经写明:

- `experiment_config` 对应 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- data/model/train/eval 四份配置都存在且通过解析

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链的意义很直接:

1. 当前 experiment 配置不是孤立文件，而是当前阶段协议明牌点名的正式索引入口
2. 当前路线锁定要求先把这套单头 UNet 基线的正式配置链讲清楚
3. 当前正式规则文件要求 run 名、配置链和结果链都能对账

## 这些列/字段分别是什么意思

- `run_name`: 当前正式实验运行名，也是 runtime-check 使用的正式 run 名
- `stage_code`: 当前阶段代码，帮助区分 stage02 内部子位点
- `dataset_code`: 当前实验绑定的数据集代码，这里固定是 `glas`
- `model_name`: 当前实验绑定的模型名，这里固定是 `unet`
- `train_seed`: 当前随机种子冻结值
- `config_refs.*`: 这才是最关键的部分，表示当前实验显式指向哪四份正式配置

## 为什么这样组织

如果没有这份 experiment config，训练入口就很容易走向另一种坏状态:

1. data 路径写死一点
2. model 参数写死一点
3. train 超参数再写死一点
4. eval 阈值又藏在别处

这样短期看很省事，长期最难回链。

当前把它们先收进一份总索引卡，本质上是在保护配置链。

## 这个文件没说明什么

这份文件不负责解释:

- `configs/data/glas.yaml` 每个字段为什么这么定
- `configs/model/unet_v1.yaml` 的模型结构细节
- `configs/train/unet_flow_v1.yaml` 的训练超参数取舍
- `configs/eval/eval_proto_v1.yaml` 的评估口径细节

这些问题要去看对应的逐文件资产说明文。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. 确认 `config_refs` 指向 4 份真实存在的配置
3. 对照 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 的 `Config Resolution`
4. 对照 `../../../../scripts/train.py` 的 experiment config 解引用逻辑

期望结果:

- 四份配置路径都真实存在
- runtime 报告里的解析结果和这份文件一致
- `scripts/train.py` 不需要额外猜测配置位置
- 文件路径 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 能和 runtime 报告里的 `experiment_config` 对上

## 与项目其他部分的关联

- 上游: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 下游: `../../../../configs/data/glas.yaml`、`../../../../configs/model/unet_v1.yaml`、`../../../../configs/train/unet_flow_v1.yaml`、`../../../../configs/eval/eval_proto_v1.yaml`
- 消费方: `../../../../scripts/train.py`

## 常见问题

- 容易误解 1: 以为这份文件就是“所有配置内容”
  - 实际上它只是一张总索引卡
- 容易误解 2: 以为 `config_refs` 只是装饰字段
  - 实际上正式入口就是靠它解引用四份配置

## 建议联读

- `configs_data_glas.yaml.md`
- `configs_model_unet_v1.yaml.md`
- `configs_train_unet_flow_v1.yaml.md`
- `configs_eval_eval_proto_v1.yaml.md`
- `scripts_train.py.md`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答:

1. 当前 stage02 正式实验到底认哪四份配置
2. 为什么 experiment config 必须先于其他配置被解释
3. runtime 报告里的配置解析结果为什么能回到这份文件
