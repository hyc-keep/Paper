# src_data_datasets.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/data/datasets.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `official split protocol and binary gland-mask supervision`
- 公式/定义: data config + split csv + raw image and raw mask -> formal dataset samples

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/datasets.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `dataset_root`, `split_dir`, `csv_files`, `input_size`, `normalize_mean`, `normalize_std`, `mask_positive_rule`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/data/datasets.py`
- 符号: `DataConfig` / `load_data_config()` / `resolve_split_csv()` / `build_dataset_from_csv()` / `FormalSegmentationDataset` / `build_segmentation_dataset()`

## 这个脚本的作用

这份对象说明文回答的是一个很基础、但非常关键的问题:

当前 stage02 到底是谁把 `configs/data/glas.yaml`、`splits/glas/*.csv` 和 `datasets/01_GlaS_official_raw/*` 真正接成训练能吃的 dataset。

答案就是 `../../../../src/data/datasets.py`。

你可以把它理解成 stage02 数据链里的“装箱工位”。

用人话说，原始图片、mask、split CSV 和配置都在不同地方放着，真正把它们装成 PyTorch dataset 这一步，就是这里做的。

如果没有这份文件，`../../../../scripts/train.py` 就算已经知道 experiment config 是哪一份，也没法稳定拿到 `image`、`mask`、`sample_id` 这组正式输入。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
configs/data/glas.yaml
        ↓
splits/glas/*.csv + datasets/01_GlaS_official_raw/*
        ↓
src/data/datasets.py
        ↓
scripts/train.py / runtime-check / trainer
```

这里最关键的事实有三条:

1. `../../../../scripts/train.py` 会先解析 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. 然后数据配置会落到 `../../../../configs/data/glas.yaml`
3. 再由这里把 split CSV 和真实图像路径装成正式样本列表与 dataset 对象

当前最硬的物理证据已经在 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 和 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 里落下来了:

1. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明 `dataset_module=pass`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已把对应对象指向 `../../../../src/data/datasets.py`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明 split CSV 文件路径 `../../../../splits/glas/glas_train68.csv`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已写明原始图像文件路径 `../../../../datasets/01_GlaS_official_raw/train_1.bmp`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已写明样本文件路径 `../../../../datasets/01_GlaS_official_raw/train_42.bmp`

说白了，这不是“理论上应该能读数据”，而是当前正式主链真的已经从这里拿到了可用样本。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../configs/data/glas.yaml`
- `../../../../splits/glas/glas_train68.csv`
- `../../../../datasets/01_GlaS_official_raw/train_42.bmp`
- 文件路径基线: `../../../../src/data/datasets.py`

### 下游消费者

- `../../../../scripts/train.py`
- `../../../../src/engine/trainer.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是把数据链的边界钉死:

1. 当前数据协议来自上一阶段正式放行，不是 stage02 临时重定义
2. 当前输入尺寸固定为 `512x512`，图像按 RGB 三通道读取，归一化均值与标准差采用 ImageNet 预设，mask 规则固定为 `mask_gt_0`
3. 当前只能沿用正式 split CSV，不允许训练时私下重排样本

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式数据装配层
- 当前冻结字段:
  - `dataset_code=glas`
  - `split_dir` 对应真实目录 `../../../../splits/glas`
  - `input_size=[512, 512]`
  - `normalize_mean=[0.485, 0.456, 0.406]`
  - `normalize_std=[0.229, 0.224, 0.225]`
  - `mask_positive_rule=mask_gt_0`
- 当前最硬证据:
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `dataset_module=pass`，并把对象落点指向 `../../../../src/data/datasets.py`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_source=split_csv`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明当前 `split_csv` 对应 `../../../../splits/glas/glas_train68.csv`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `sample_id=GlaS_official_train_train_42`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`

这里顺手纠正一个容易读偏的点:

当前证据能证明的是“dataset 模块已经进入正式训练链并产出 batch”，不是“所有数据增强和所有 split 资产都已经逐对象解释完”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 6 步:

1. 用 `simple_yaml_load()` 和 `parse_scalar()` 读取 `../../../../configs/data/glas.yaml`
2. 用 `load_data_config()` 把配置装成冻结的 `DataConfig`
3. 用 `resolve_split_csv()` 找到当前 split CSV
4. 用 `build_dataset_from_csv()` 校验 schema 和 sample_id，再解析 image/mask 路径
5. 用 `FormalSegmentationDataset.__getitem__()` 读取 RGB 图像和二值 mask
6. 最后把 `image`、`mask`、`sample_id`、路径元信息交给训练主链

### 关键对象 1: `DataConfig`

`DataConfig` 的作用不是“把字段搬运一下”。

它真正解决的是: 数据协议不要再散落在脚本常量里。

这样一来，`dataset_root`、`split_dir`、`csv_files`、`input_size`、`mask_positive_rule` 这些关键字段都有唯一来源。

### 关键对象 2: `build_dataset_from_csv()`

这个函数特别值得盯。

因为它不是直接读 CSV 就完事，而是先做:

1. schema 校验
2. sample_id 唯一性校验
3. image/mask 路径解析

你可能会问:

“为什么不把坏 CSV 留到训练时报错？”

因为那样太晚了。

当前阶段更稳的做法，是在样本真正进入 Dataset 之前就把问题挡住。

### 关键对象 3: `FormalSegmentationDataset`

这个类负责真正把磁盘上的样本变成 tensor。

这里有两个冻结动作最重要:

1. 图像强制转成 RGB
2. mask 强制走 `mask_gt_0` 二值化

说白了，当前 stage02 的训练主链只认这套输入语义，不在 dataset 层继续保留多值 mask。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

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

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“既然有完整 YAML 库，为什么这里还保留一个最小解析器？”

用人话说，当前阶段最怕的是把配置解析这件事也变成外部依赖变量。

如果最小正式闭环还没跑稳，就先引进更多解析层差异，后面出了问题更难回链。

### 设计取舍 1: 为什么 dataset 层就做 `mask_gt_0`

因为当前数据协议已经冻结为二值腺体分割。

如果把多值 mask 一直拖到训练后面再决定怎么转，职责就会开始漂。

### 设计取舍 2: 为什么返回元信息

因为 runtime-check 和说明文都要回到真实样本。

如果 dataset 只返回 tensor，不返回 `sample_id` 和路径，后面的证据链就会变得很虚。

### 设计取舍 3: 为什么 split CSV 要先校验

因为 schema 不对、sample_id 重复，本质上都不是训练期问题，而是数据资产问题。

当前应该在更早的位置暴露。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/data/glas.yaml`
2. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`
4. 对照 `../../../../src/data/datasets.py`

### 当前最关键的核对点

- `split_dir` 对应的真实目录 `../../../../splits/glas` 是否和 `split_csv` 对应的真实文件 `../../../../splits/glas/glas_train68.csv` 对上
- `input_size=[512, 512]` 是否和 `input_shape=[2, 3, 512, 512]` 对上
- `mask_positive_rule=mask_gt_0` 是否和 `target_unique_values=[0, 1]` 对上

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/data/datasets.py`
2. 具体路径已经固定在 `../../../../configs/data/glas.yaml`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `split_csv` 对应 `../../../../splits/glas/glas_train68.csv`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `image_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1.bmp`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `sample_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_42.bmp`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`
7. 字段 `dataset_root` 对应真实目录 `../../../../datasets/01_GlaS_official_raw`
8. 字段 `split_dir` 对应真实目录 `../../../../splits/glas`

## 常见误区

- 误区 1: 以为这个文件只是读 CSV
  - 实际上它还负责 schema 校验、路径解析、mask 二值化和 dataset 输出结构冻结
- 误区 2: 以为二值 mask 是 loss 层才决定的
  - 实际上 dataset 层已经按 `mask_gt_0` 做了正式规则落地
- 误区 3: 以为当前已经把所有 data 对象都讲完了
  - 实际上 `src/data/transforms.py` 还没进入当前这一批对象说明文

## 建议联读

- `configs_data_glas.yaml.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `scripts_train.py.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_data_glas.yaml.md`，搞清楚这些字段为什么这么冻结
2. 再去看 `scripts_train.py.md`，搞清楚 dataset 怎么被正式入口消费
3. 最后去看 `src_engine_trainer.py.md`，搞清楚 batch 进入训练闭环以后发生了什么

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. `src/data/datasets.py` 在 stage02 里到底负责哪一段正式职责
2. 为什么 `mask_gt_0` 要在 dataset 层落地
3. 当前哪个真实 split CSV 和真实样本最能证明它已经进入主链
4. 为什么当前不能把这个 dataset 装配对象的解释等同于整个 data 包都解释完了

## 5 分钟自检任务

1. 回到 `../../../../configs/data/glas.yaml`，找到 `mask_positive_rule`
2. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，找到 `target_unique_values`
3. 再回看 `../../../../src/data/datasets.py`，说出 `build_dataset_from_csv()` 在 Dataset 实例化之前先挡掉了哪两类问题

如果这三步你都能顺下来，说明你已经把这份 dataset 说明文真正看懂了。
