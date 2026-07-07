# src_data_mask_ops.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/data/mask_ops.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `binary foreground supervision under frozen segmentation protocol`
- 章节: `mask reading, positive-pixel binarization, and nearest-neighbor resizing`
- 公式/定义: raw mask asset -> binary gland mask -> resized or exported binary target

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/mask_ops.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `mask_positive_rule`, `input_size`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/data/mask_ops.py`
- 符号: `load_mask_array()` / `binarize_mask_gt_zero()` / `export_binary_mask_png()` / `resize_binary_mask()`

## 这个脚本的作用

这份对象说明文回答的是另一个非常基础的问题:

当前 stage02 到底是谁把磁盘上的腺体标注 mask，变成训练主链真正认得的二值监督。

答案就是 `../../../../src/data/mask_ops.py`。

你可以把它理解成 stage02 标签链里的“标签定尺和定性工位”。

用人话说，原始标注文件在磁盘上只是灰度图。真正决定“哪些像素算腺体前景、resize 时怎样不把边界弄糊、导出时怎样保持二值语义”的，是这里。

如果没有这份文件，dataset 主对象虽然能读到 mask 文件路径，但没法稳定把它变成 `target_unique_values=[0, 1]` 的正式监督张量。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/data/glas.yaml
        ↓
datasets/01_GlaS_official_raw/train_1_anno.bmp
        ↓
src/data/mask_ops.py
        ↓
src/data/datasets.py
        ↓
src/data/transforms.py
        ↓
scripts/train.py / runtime-check / trainer
```

这里最关键的事实有三条:

1. `../../../../configs/data/glas.yaml` 已冻结 `mask_positive_rule=mask_gt_0`
2. `../../../../src/data/datasets.py` 会在 `__getitem__()` 里直接调用 `load_mask_array()` 和 `binarize_mask_gt_zero()`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经写明 `target_unique_values=[0, 1]`

当前最硬的物理证据至少有 6 组:

1. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_shape=[2, 1, 512, 512]`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`
5. `../../../../src/data/datasets.py` 写明 `binarize_mask_gt_zero(load_mask_array(Path(sample["mask_path"])))`
6. `../../../../src/data/transforms.py` 写明输出 mask 会再次压成二值 float tensor

说白了，这里不是“有几个 mask helper 备用”，而是当前正式监督语义真的从这里开始被钉死。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/data/glas.yaml`
- `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
- `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
- `../../../../src/data/datasets.py`

### 下游消费者

- `../../../../src/data/datasets.py`
- `../../../../src/data/transforms.py`
- `../../../../scripts/train.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是把标签协议边界钉死:

1. 当前监督语义不是 loss 层临时决定的，而是 data protocol 先冻结的
2. 当前正样本判定固定跟着 `mask_gt_0`
3. 当前 mask resize 只能走离散标签安全的最近邻口径

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式二值 mask 协议层
- 当前冻结字段:
  - `mask_positive_rule=mask_gt_0`
  - `input_size=[512, 512]`
- 当前最硬证据:
  - `../../../../src/data/datasets.py` 写明 `load_mask_array()` 被 dataset 主对象直接消费
  - `../../../../src/data/datasets.py` 写明 `binarize_mask_gt_zero()` 被 dataset 主对象直接消费
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`

这里必须诚实说明:

当前证据更强地证明了“mask 读取和 `mask_gt_0` 二值化已经进入正式训练主链”，还没有单独证明“`export_binary_mask_png()` 已作为当前 stage02 正式运行资产的一部分被专门执行过”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 4 步:

1. 用 `load_mask_array()` 把原始标注文件读成灰度 `uint8` 数组
2. 用 `binarize_mask_gt_zero()` 把大于零的像素压成前景
3. 需要导出时，用 `export_binary_mask_png()` 把二值结果写成前景为 255、背景为 0 的灰度图
4. 需要对齐尺寸时，用 `resize_binary_mask()` 按最近邻重采样，并再次回到二值数组

### 关键点 1: 为什么 `mask_gt_0` 在这里就固定

因为当前 stage02 的监督协议已经冻结成“二值腺体 vs 背景”。

说白了，这不是留给 loss 或 metric 临时选择的自由项，而是数据协议先定死的。

### 关键点 2: 为什么 resize 必须走最近邻

因为 mask 不是自然图像。

如果这里改成双线性之类的平滑插值，前景边界会被弄成灰度软标签，后面再二值化时就会偷偷改掉标签形状。

### 关键点 3: 为什么 resize 后还要再次二值化

因为哪怕输入本来是前景 255、背景 0 的灰度 mask，resize 之后也需要重新保证输出只回到干净的二值集合。

当前更在意的是监督语义稳定，而不是保留中间插值痕迹。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是先由 dataset 主对象消费，再由 `../../../../scripts/train.py` 间接进入主链。

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

“为什么不在 dataset 主对象里直接写几行 `(mask > 0)`，非要单独拆一个文件？”

用人话说，如果把 mask 读取、二值化、导出、resize 都藏在 dataset 类内部，读者很难看清“标签协议到底在哪里被冻结”。

单独拆出来以后，数据协议、dataset 主对象和 transform 主对象的边界就更清楚了。

### 设计取舍 1: 为什么 `load_mask_array()` 先转成灰度

因为当前正式 mask 语义只需要一个离散标签通道。

先压成 `L` 通道以后，后续二值化动作就不会再面对多种输入格式。

### 设计取舍 2: 为什么导出时用前景 255、背景 0

因为人工检查时最容易直接看清前景和背景。

如果只把数组原样落盘，很多查看器里并不好读。

### 设计取舍 3: 为什么这份对象仍然保留导出和 resize helper

因为它们虽然不是当前 runtime-check 的主证据，但都属于同一条“正式二值 mask 协议”的辅助动作。

和读取、二值化放在一起讲，边界更干净。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/data/glas.yaml`
2. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`
4. 对照 `../../../../src/data/mask_ops.py`

### 当前最关键的核对点

- `mask_positive_rule=mask_gt_0` 是否和 `target_unique_values=[0, 1]` 对上
- `mask_path` 是否真的指向 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp` 或 `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
- 最近邻 resize 和二值化规则是否都在同一对象里被显式写死

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/data/mask_ops.py`
2. 具体路径已经固定在 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_shape=[2, 1, 512, 512]`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `target_unique_values=[0, 1]`
7. 字段 `mask_positive_rule` 对应 `mask_gt_0`

## 常见误区

- 误区 1: 以为 mask 二值化是 loss 层才决定的事
  - 实际上正式协议在数据层就已经把正样本判定冻住了
- 误区 2: 以为 mask resize 和图像 resize 可以随便共用同一插值策略
  - 实际上标签图一旦被平滑插值，监督语义就会变形
- 误区 3: 以为这里只有读取函数算正式对象
  - 实际上读取、二值化、导出和 resize 一起构成了当前二值 mask 协议层

## 建议联读

- `src_data_datasets.py.md`
- `src_data_transforms.py.md`
- `configs_data_glas.yaml.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_data_datasets.py.md`，搞清楚 `mask_ops` 的结果是怎样进入 dataset 主对象的
2. 再去看 `src_data_transforms.py.md`，比较 dataset 层二值化和 transform 层再次压实二值 tensor 的边界
3. 最后去看 `configs_data_glas.yaml.md`，回到 `mask_positive_rule` 的冻结来源

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前二值监督语义是在哪里真正被固定下来的
2. 为什么 `mask_gt_0` 应该归到 data protocol，而不是归到 loss 层
3. 为什么 mask resize 必须强调最近邻
4. 为什么这个 mask 协议对象值得单独从 dataset 主对象里拆出来讲

## 5 分钟自检任务

1. 回到 `../../../../configs/data/glas.yaml`，找到 `mask_positive_rule`
2. 回到 `../../../../src/data/datasets.py`，找到 `binarize_mask_gt_zero(load_mask_array(...))`
3. 再回看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，确认 `target_unique_values` 为什么会是 `[0, 1]`

如果这三步你都能顺下来，说明你已经把这份 mask protocol 说明文真正看懂了。
