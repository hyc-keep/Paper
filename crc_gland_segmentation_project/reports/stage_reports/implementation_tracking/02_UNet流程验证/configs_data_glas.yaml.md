# configs_data_glas.yaml.md

## 结构化溯源卡片

- 正式对象: `../../../../configs/data/glas.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `official dataset split and binary gland-mask protocol`
- 公式/定义: `dataset_root + split csv + preprocessing freeze -> formal data protocol`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../configs/data/glas.yaml`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `dataset_root`, `split_dir`, `csv_files`, `input_size`, `normalize_mean`, `normalize_std`, `mask_positive_rule`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 当前这个文件说明了什么

这份配置文件回答的是:

当前 stage02 的正式数据协议到底冻结成什么样。

你可以把它理解成 dataset 侧的“操作说明卡”。

说白了，`src/data/datasets.py` 不是凭感觉去读数据，它要先看这里规定的根目录、split CSV、输入尺寸、归一化和 mask 规则。

## 这张表/这个文件长什么样

这个文件主要有 5 类字段:

1. 数据集身份字段
2. split 与 CSV 资产字段
3. 图像/掩码预处理字段
4. mask 规则字段
5. 可视化与边界/距离相关字段

## 当前真实结果

当前最关键的真实字段有 8 组:

1. `dataset_root` 对应 `../../../../datasets/01_GlaS_official_raw`
2. `split_dir` 对应 `../../../../splits/glas`
3. `csv_files.train` 对应 `../../../../splits/glas/glas_train68.csv`
4. `csv_files.val` 对应 `../../../../splits/glas/glas_val17.csv`
5. `input_size=[512, 512]`
6. `normalize_mean=[0.485, 0.456, 0.406]`
7. `normalize_std=[0.229, 0.224, 0.225]`
8. `mask_positive_rule=mask_gt_0`

当前最关键的真实路径也有 4 组:

1. 数据根目录路径 `../../../../datasets/01_GlaS_official_raw`
2. split 目录路径 `../../../../splits/glas`
3. train split CSV 路径 `../../../../splits/glas/glas_train68.csv`
4. val split CSV 路径 `../../../../splits/glas/glas_val17.csv`

这些结果已经和正式证据对上:

- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `split_csv` 对应 `../../../../splits/glas/glas_train68.csv`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前 data config 继承的是上一阶段已经放行的数据协议
2. 当前路线锁定要求 stage02 先沿用冻结好的 GlaS 输入协议
3. 当前正式规则要求输入尺寸、mask 规则和 split 资产都能回到真实路径

## 这些列/字段分别是什么意思

- `dataset_root`: 原始 GlaS 资产根目录
- `split_dir`: 正式 split CSV 目录
- `csv_files.*`: 各 split 真实 CSV 文件名
- `input_size`: 当前训练与验证统一输入尺寸
- `normalize_mean`: RGB 归一化均值
- `normalize_std`: RGB 归一化标准差
- `mask_positive_rule`: 当前把原始 mask 转成二值监督的规则
- `boundary_width`: 边界指标宽度
- `asset_status`: 当前数据资产状态，这里是 `restored_and_frozen`

## 为什么这样组织

如果没有这份 data config，数据规则就会非常容易漂。

今天有人在 dataset 层改一点，明天有人在 transform 层再改一点，最后谁都说不清现在到底认哪一套输入协议。

当前把关键数据规则全部收在这份文件里，本质上是在保护正式数据协议不被运行时随手改写。

## 这个文件没说明什么

这份文件不负责解释:

- `src/data/datasets.py` 的具体实现细节
- `src/data/transforms.py` 的增强逻辑细节
- `splits/glas/*.csv` 每一行的具体样本内容

这些问题要去看对应对象或资产的逐文件说明文。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../configs/data/glas.yaml`
2. 对照 `../../../../src/data/datasets.py`
3. 对照 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 对照 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

期望结果:

- split CSV 路径能和 runtime 报告里的 `split_csv` 对上
- `input_size` 能和 `input_shape` 对上
- `mask_positive_rule=mask_gt_0` 能和 `target_unique_values=[0, 1]` 对上
- 具体路径 `../../../../datasets/01_GlaS_official_raw` 与 `../../../../splits/glas` 都真实存在

## 与项目其他部分的关联

- 上游: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 下游: `../../../../src/data/datasets.py`
- 结果回链: `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 常见问题

- 容易误解 1: 以为这份配置只影响训练，不影响 runtime-check
  - 实际上 runtime-check 也直接消费这里的数据协议
- 容易误解 2: 以为 `mask_positive_rule` 可以后面再定
  - 实际上当前 data config 已经把它冻结了

## 建议联读

- `src_data_datasets.py.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `scripts_train.py.md`

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答:

1. 当前 stage02 的正式数据协议冻结了哪些字段
2. 为什么 `mask_gt_0` 属于 data config 而不是 loss config
3. runtime 里的 `input_shape` 和 `target_unique_values` 为什么能回到这份配置
