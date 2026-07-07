# configs_data_glas.yaml.md

## 这份配置是干什么的

- `configs/data/glas.yaml` 是 GlaS 的正式数据消费配置
- 它定义了项目到底认哪一版 GlaS 数据、哪一组 split、以及哪些数据协议字段被冻结

你可以把它理解成“GlaS 正式输入层的身份证”。

## 当前真实结果

当前文件里的关键信息是:

- `dataset_code: glas`
- `dataset_root: datasets/01_GlaS_official_raw`
- `split_dir: splits/glas`
- `csv_files.train: glas_train68.csv`
- `csv_files.val: glas_val17.csv`
- `csv_files.testA: glas_testA60.csv`
- `csv_files.testB: glas_testB20.csv`
- `mask_interp: nearest`
- `mask_positive_rule: mask_gt_0`
- `asset_status: restored_and_frozen`

换句话说,它已经不是草稿配置,而是一份冻结后的正式配置。

## 结构化溯源卡片

- 正式对象: `configs/data/glas.yaml`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `benchmark split and evaluation setup`
- 公式/定义: `官方 train/test 划分、二值腺体标签和固定输入协议`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `configs/data/glas.yaml`
- commit: `workspace_local_20260704`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `input_size`, `mask_interp`, `normalize_mean`, `normalize_std`, `mask_positive_rule`, `boundary_width`

### 当前实现落点
- 文件: `configs/data/glas.yaml`
- 下游消费者: `src/data/datasets.py`, `scripts/train.py`, 交付型数据工具脚本

## 这份文件长什么样

这份 YAML 可以分成 5 组字段看:

1. 数据集身份: `dataset_code`, `dataset_role`, `dataset_version`
2. 数据根目录与 split: `dataset_root`, `split_dir`, `csv_files`
3. split / sample_id 协议: `split_csv_schema_version`, `sample_id_rule_version`
4. 输入与标签规则: `input_size`, `image_interp`, `mask_interp`, `mask_positive_rule`
5. 边界、距离图和预览协议: `boundary_target_version`, `distance_target_version`, `visual_proto_version`

## 关键字段分别是什么意思

### `dataset_code`

- 含义: 当前配置对应哪个 benchmark
- 当前值: `glas`
- 如何验证: 打开文件首行即可看到

### `dataset_root`

- 含义: 这套配置最终认哪一个数据根目录
- 当前值: `datasets/01_GlaS_official_raw`
- 如何验证: 再联读 `scripts/train.py` 和 `src/data/datasets.py`

这字段很重要,因为它决定后面的相对路径最终落到哪里。

### `split_dir`

- 含义: 当前数据集的 split CSV 放在哪个目录
- 当前值: `splits/glas`

用人话说,它告诉项目去哪里找 GlaS 的正式划分资产。

### `csv_files`

- 含义: 把逻辑 split 名映射成真正文件名
- 当前值:
  - `train -> glas_train68.csv`
  - `val -> glas_val17.csv`
  - `testA -> glas_testA60.csv`
  - `testB -> glas_testB20.csv`

这说明 GlaS 不是只有 train/val/test 三段,而是保留了 challenge 原本的 `testA/testB` 结构。

### `input_size`

- 含义: 当前阶段冻结的输入尺寸
- 当前值: `[512, 512]`

这里说的是配置承诺的尺寸,不是 runtime 报告里原图的原始尺寸。
不要把这两个概念混掉。

### `mask_interp`

- 含义: mask 重采样方式
- 当前值: `nearest`

这条是不能随便改的。
如果你把标签插值改成双线性,二值标签边界就会被污染。

### `mask_positive_rule`

- 含义: 什么样的 mask 像素算正类
- 当前值: `mask_gt_0`

说白了,就是大于 0 的像素都算腺体前景。

### `boundary_width`

- 含义: 边界带宽度
- 当前值: `3`

这会影响 `boundary_targets.py` 和对应导出工具的结果。

### `asset_status`

- 含义: 当前这份配置绑定的数据资产处于什么状态
- 当前值: `restored_and_frozen`

这不是注释,而是状态声明。
它在告诉下游: 当前资产不是临时整理中的半成品。

## 这份文件说明了什么

这份配置至少说明了三件事:

1. 当前项目认的 GlaS 数据根目录是固定的
2. 当前项目认的 GlaS split 文件是固定的
3. 当前项目对输入尺寸、标签插值和二值规则有明确冻结值

如果没有这份文件,后续脚本很容易各自写一套默认值。

## 这份文件没说明什么

它没有直接说明:

- 模型结构
- loss 公式
- 训练 batch 大小
- optimizer

所以不要因为看到了 `input_size` 和 `normalize_mean/std`,就误判成“完整训练配置已经齐了”。

## 如何手工验证这份配置

### 验证步骤 1: 看 split 是否能对上真实文件

1. 打开 `configs/data/glas.yaml`
2. 记录 `split_dir: splits/glas`
3. 记录 `csv_files.train: glas_train68.csv`
4. 到 `splits/glas/` 目录下检查该文件是否存在

期望结果:

- `splits/glas/glas_train68.csv` 真实存在

### 验证步骤 2: 看下游代码是否真实消费它

1. 打开 `src/data/datasets.py`
2. 查看 `load_data_config()` 和 `resolve_split_csv()`
3. 再打开 `scripts/train.py`
4. 确认入口通过 `load_data_config()` 和 `build_dataset_from_csv()` 间接消费这份 YAML

期望结果:

- `scripts/train.py` 不自己写死 GlaS 的 split 文件名

### 验证步骤 3: 看规则是不是和当前阶段协议一致

1. 查看 `mask_interp: nearest`
2. 查看 `mask_positive_rule: mask_gt_0`
3. 再联读 `01_数据协议/05_标签转换与可视化规则.md`

期望结果:

- 标签插值和正类规则与阶段协议不冲突

## 常见误区

### Q: `input_size=[512,512]` 是不是说明原始图像尺寸都是 512?

A: 不是。
这只是正式消费配置里的目标输入尺寸。
当前 runtime 报告里样本原始尺寸仍然可能是 `[522, 775, 3]` 这种真实大小。

### Q: 有了 `glas.yaml` 是不是就等于完整训练实验配置已经存在?

A: 也不是。
它只是数据配置。
完整训练实验配置还要额外包含模型、loss、trainer 等阶段对象。

## 读完后建议联读

建议按这个顺序继续读:

1. `configs_data_crag.yaml.md`
2. `src_data_datasets.py.md`
3. `scripts_train.py.md`

这样你就能把 GlaS 配置、总装配入口和 preflight 入口串成一条线。
