# src_data_transforms.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/data/transforms.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net: Convolutional Networks for Biomedical Image Segmentation`
- 章节: `preprocessing and train-time augmentation before segmentation supervision`
- 公式/定义: raw RGB image and binary mask -> resize/augment/normalize -> tensor pair

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/transforms.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `input_size`, `normalize_mean`, `normalize_std`, `mask_positive_rule`
- 训练冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `aug_version`, `eval_aug_enable`, `light_aug.random_hflip_prob`, `light_aug.random_vflip_prob`, `light_aug.rotate90_prob`, `light_aug.random_resized_crop_prob`, `light_aug.brightness_prob`, `light_aug.contrast_prob`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/data/transforms.py`
- 符号: `AugmentConfig` / `build_augment_config()` / `build_train_transform()` / `build_eval_transform()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把原始 dataset 样本变成真正送进模型的 tensor。

答案就是 `../../../../src/data/transforms.py`。

你可以把它理解成 stage02 数据链里的“精加工工位”。

用人话说，dataset 装配对象负责把图片、mask 和 sample_id 找出来，但真正把图像 resize、归一化、做轻量增强、把 mask 压成训练主链认得的二值 tensor，这一步是这里做的。

如果没有这份文件，`../../../../scripts/train.py` 虽然能拿到 dataset 对象，也没法稳定得到 `float32` 的 `image`、`mask` 和固定的 `512x512` 输入。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/data/glas.yaml + configs/train/unet_flow_v1.yaml
        ↓
src/data/datasets.py
        ↓
src/data/transforms.py
        ↓
scripts/train.py
        ↓
src/models/unet.py / src/losses/seg_losses.py
```

这里最关键的事实有三条:

1. `../../../../scripts/train.py` 会先用 `build_augment_config()` 解析 `../../../../configs/train/unet_flow_v1.yaml`
2. 然后 `build_train_transform()` 和 `build_eval_transform()` 会把 data config 与 aug config 合成正式 transform
3. runtime 真值里的 `input_shape=[2, 3, 512, 512]`、`target_shape=[2, 1, 512, 512]` 只有经过这里的 resize/normalize 才能稳定出现

当前最硬的物理证据至少有 5 组:

1. `../../../../scripts/train.py` 写明 `train_transform = build_train_transform(data_config_obj, augment_config)`
2. `../../../../scripts/train.py` 写明 `eval_transform = build_eval_transform(data_config_obj)`
3. `../../../../configs/train/unet_flow_v1.yaml` 写明 `aug_version=light_aug_v1`
4. `../../../../configs/data/glas.yaml` 写明 `input_size=[512, 512]`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]` 与 `target_shape=[2, 1, 512, 512]`

说白了，这里不是“好像有个 transform 概念”，而是当前正式主链真的从这里拿到了固定形状和固定归一化语义的 batch。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/data/glas.yaml`
- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../src/data/datasets.py`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../scripts/train.py`
- `../../../../src/models/unet.py`
- `../../../../src/losses/seg_losses.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是把 transform 链的边界钉死:

1. 当前不是任意增强实验期，而是 `light_aug_v1` 冻结期
2. 当前验证 transform 不能偷偷带随机增强
3. 当前 resize、normalize 和 mask 二值化语义都必须和正式 data config 对齐

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式 train/eval transform 层
- 当前冻结字段:
  - `aug_version=light_aug_v1`
  - `input_size=[512, 512]`
  - `normalize_mean=[0.485, 0.456, 0.406]`
  - `normalize_std=[0.229, 0.224, 0.225]`
  - `eval_aug_enable=false`
- 当前最硬证据:
  - `../../../../configs/train/unet_flow_v1.yaml` 写明 `random_hflip_prob=0.5`
  - `../../../../configs/train/unet_flow_v1.yaml` 写明 `random_resized_crop_prob=0.3`
  - `../../../../scripts/train.py` 写明 `build_augment_config()`、`build_train_transform()`、`build_eval_transform()` 被正式入口消费
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_dtype=float32`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`

这里顺手纠正一个容易读偏的点:

当前证据能证明的是“transform 已经进入正式训练主链”，不是“更复杂的增强策略已经被批准进入当前基线”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 5 步:

1. 用 `build_augment_config()` 把 `light_aug` 映射装成冻结的 `AugmentConfig`
2. 用 `_resize_pair()` 先把图像和 mask 对齐到 `input_size`
3. train transform 视概率执行翻转、90 度旋转、随机裁剪、亮度和对比度扰动
4. 用 `_normalize_image()` 把 RGB 图像转成 `C,H,W` 的标准化 tensor
5. 最后把 mask 压成 `(mask > 0.5).float()` 的二值监督

### 关键对象 1: `AugmentConfig`

`AugmentConfig` 的作用不是“字典换个壳”。

它真正解决的是: 增强规则不要散落在训练入口的临时字段里。

这样一来，`random_hflip_prob`、`rotate90_prob`、`brightness_limit` 这些字段都有唯一来源。

### 关键对象 2: `build_train_transform()`

这个函数特别值得盯。

因为它不是单纯 resize 一下，而是把:

1. 固定尺寸
2. 轻量几何增强
3. 轻量光照增强
4. 固定归一化
5. mask 二值化

这 5 层正式规则装成一个可调用对象。

### 关键对象 3: `build_eval_transform()`

这个函数看起来更简单，但恰恰是评估口径稳定的关键。

它保留 resize 和 normalize，却故意不保留随机增强。

说白了，当前 validation 只允许比较模型，不允许比较“这一轮随机抖没抖到好位置”。

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

“既然有更重的增强库，为什么这里先只做一套轻量 transform？”

用人话说，当前阶段最怕的是把最小正式闭环搞得太花。

如果主链还在学习说明文阶段，就先把最小增强协议固定下来，出了问题也更容易回链。

### 设计取舍 1: 为什么 train 和 eval 分两个 builder

因为当前训练和验证的共性是 resize/normalize，不共性是随机增强。

如果硬塞在一个 builder 里，后面最容易让 eval 口径漂掉。

### 设计取舍 2: 为什么 mask 在这里再次二值化

因为当前 stage02 认的是二值腺体监督，不是原始多值实例编码。

如果把这个动作拖到更后面，loss 和 metric 的职责会越来越混。

### 设计取舍 3: 为什么先 resize 再增强

因为当前最先要保证的是输入尺寸稳定。

先把尺寸钉死，再做轻量扰动，整个 batch 形状和 runtime 真值更容易对账。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/train/unet_flow_v1.yaml`
2. 打开 `../../../../configs/data/glas.yaml`
3. 打开 `../../../../scripts/train.py`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- `input_size=[512, 512]` 是否和 `input_shape=[2, 3, 512, 512]` 对上
- `normalize_mean`、`normalize_std` 是否来自 `../../../../configs/data/glas.yaml`
- `eval_aug_enable=false` 是否和 eval transform 不带随机增强这件事对上

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/data/transforms.py`
2. 具体路径已经固定在 `../../../../configs/train/unet_flow_v1.yaml`
3. `../../../../configs/train/unet_flow_v1.yaml` 写明 `rotate90_enable=true`
4. `../../../../configs/train/unet_flow_v1.yaml` 写明 `brightness_limit=0.1`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_shape=[2, 3, 512, 512]`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_shape=[2, 1, 512, 512]`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `input_dtype=float32`

## 常见误区

- 误区 1: 以为 transform 只是图像美化
  - 实际上这里决定了 resize、归一化和 mask 二值化这几条正式输入语义
- 误区 2: 以为 eval 也应该走同样的随机增强
  - 实际上 eval 只保留确定性变换
- 误区 3: 以为当前 data 包已经全部讲完了
  - 实际上 dataset 装配层和这里的 transform 层讲的是两层不同职责

## 建议联读

- `src_data_datasets.py.md`
- `configs_train_unet_flow_v1.yaml.md`
- `configs_data_glas.yaml.md`
- `scripts_train.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_data_datasets.py.md`，搞清楚样本是怎么被组织出来的
2. 再去看 `scripts_train.py.md`，搞清楚 transform 是怎么被入口正式挂上的
3. 最后去看 `src_models_unet.py.md` 和 `src_losses_seg_losses.py.md`，搞清楚这些 tensor 进入模型和损失后发生了什么

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 transform 对象在 stage02 里到底负责哪一段正式职责
2. 为什么 train transform 和 eval transform 必须分开
3. 当前哪组真实字段最能证明 resize 和 normalize 已经进入主链
4. 为什么当前不能把 transform 解释成“可随便换的增强实验区”

## 5 分钟自检任务

1. 回到 `../../../../configs/train/unet_flow_v1.yaml`，找到 `light_aug.random_resized_crop_prob`
2. 回到 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，找到 `input_shape`
3. 再回看 `../../../../src/data/transforms.py`，说出 train transform 和 eval transform 到底差在哪一步

如果这三步你都能顺下来，说明你已经把这份 transform 说明文真正看懂了。
