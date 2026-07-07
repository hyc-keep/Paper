# configs_data_crag.yaml.md

## 这份配置的作用

- `configs/data/crag.yaml` 是 CRAG 的正式数据消费配置
- 它负责声明: 当前项目到底认哪一版 CRAG 数据、哪几份 split、以及与标签和目标资产相关的冻结字段

如果把它说得更直白一点,这就是 CRAG 这条输入链的正式合同。

## 当前真实结果

当前文件里的关键字段是:

- `dataset_code: crag`
- `dataset_root: datasets/02_CRAG_reorganized_local_copy`
- `split_dir: splits/crag`
- `csv_files.train: crag_train153.csv`
- `csv_files.val: crag_val20.csv`
- `csv_files.test: crag_test40.csv`
- `train_pool_rule: train_sup_16_plus_train_unsup_137`
- `mask_interp: nearest`
- `mask_positive_rule: mask_gt_0`
- `asset_status: restored_and_frozen`

这里最值得注意的是 `train_pool_rule`。
它在提醒你: CRAG 训练池不是随便切出来的,而是按当前协议整理过的组合。

## 结构化溯源卡片

- 正式对象: `configs/data/crag.yaml`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Colorectal Adenocarcinoma Gland (CRAG) Dataset` 相关数据集说明与当前阶段冻结协议
- 章节: `dataset organization and train/val/test identity`
- 公式/定义: `正式 split 身份、标签二值化规则和固定数据根目录`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `configs/data/crag.yaml`
- commit: `workspace_local_20260704`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `dataset_root`, `split_dir`, `train_pool_rule`, `mask_interp`, `mask_positive_rule`, `distance_norm`

### 当前实现落点
- 文件: `configs/data/crag.yaml`
- 下游消费者: `src/data/datasets.py`, `scripts/train.py`, 交付型数据处理工具

## 这份文件长什么样

和 `glas.yaml` 类似,它也可以拆成几块:

1. 数据集身份和版本
2. 数据根目录与 split 定位
3. split/schema/sample_id 版本字段
4. 输入和标签规则
5. boundary / distance / visual 相关冻结字段

不同点在于:

- CRAG 没有 `testA/testB`
- CRAG 多了 `train_pool_rule`

## 关键字段怎么理解

### `dataset_root`

- 含义: CRAG 正式数据根目录
- 当前值: `datasets/02_CRAG_reorganized_local_copy`

这意味着项目下游不会去原始散乱目录里猜路径,而是只认当前整理后的正式根目录。

### `csv_files`

- 含义: 逻辑 split 到真实 CSV 文件名的映射
- 当前值:
  - `train -> crag_train153.csv`
  - `val -> crag_val20.csv`
  - `test -> crag_test40.csv`

这里没有 `testA/testB`,这正是 CRAG 和 GlaS 的结构差异。

### `train_pool_rule`

- 含义: CRAG 当前训练池如何构成
- 当前值: `train_sup_16_plus_train_unsup_137`

这不是装饰字段。
它告诉你 `crag_train153.csv` 背后的来源组成,后面解释 split 时要回到这里。

### `input_size`

- 含义: 当前冻结输入尺寸
- 当前值: `[512, 512]`

和 GlaS 一样,它是目标输入尺寸,不是原始图像天然尺寸。

### `mask_interp`

- 含义: 标签重采样方式
- 当前值: `nearest`

这里同样不能乱改。
标签图一旦插值污染,后面 boundary 和 distance target 都会跟着偏。

### `distance_norm`

- 含义: 距离图归一化方式
- 当前值: `zero_one`

这意味着后续 distance target 输出默认要落在 0 到 1 的范围内。

### `asset_status`

- 含义: 当前绑定的 CRAG 资产状态
- 当前值: `restored_and_frozen`

说白了,当前不是在讨论“准备怎么整理 CRAG”,而是在说明“当前已经正式认哪一版 CRAG”。

## 这份配置说明了什么

它至少说明了下面三件事:

1. CRAG 有自己独立的数据根目录和 split 目录
2. CRAG 的训练池组成被显式写进了配置,不是只在脚本里暗含
3. 输入尺寸、mask 规则、distance 规则都已经冻结

这能避免一个很常见的问题:
不同脚本对 CRAG 的理解各写一套,最后谁都说自己是“默认”。

## 这份配置没说明什么

它没有解释:

- `crag_train153.csv` 里每一列具体长什么样
- `source_subset` 字段的逐行含义
- distance target 代码实现细节
- 模型训练逻辑

所以你不能只看这份 YAML,就认为 CRAG 全链条说明已经齐了。

## 如何手工验证

### 验证步骤 1: split 映射是否真实存在

1. 打开 `configs/data/crag.yaml`
2. 记录 `split_dir: splits/crag`
3. 记录 `train/val/test` 三个 CSV 文件名
4. 到 `splits/crag/` 下核对这些文件

期望结果:

- `crag_train153.csv`、`crag_val20.csv`、`crag_test40.csv` 都真实存在

### 验证步骤 2: 下游代码是否走统一入口

1. 打开 `src/data/datasets.py`
2. 看 `load_data_config()` 是否能把这份 YAML 读进 `DataConfig`
3. 看 `resolve_split_csv()` 是否通过 `csv_files` 找 split

期望结果:

- CRAG split 文件名来自配置映射,不是脚本里写死

### 验证步骤 3: 训练池规则是否有现实痕迹

1. 观察 `train_pool_rule: train_sup_16_plus_train_unsup_137`
2. 再看 `splits/crag/crag_train153.csv` 前几行里的 `source_subset`

期望结果:

- 你能看出当前训练集确实保留了来源子集这个概念,不是纯黑箱

## 常见误区

### Q: CRAG 和 GlaS 的数据配置是不是只是文件名不同,本质完全一样?

A: 不是。
两者共享一部分冻结字段,但 split 结构和来源字段不同。
CRAG 有 `train_pool_rule` 和 `source_subset`,GlaS 有 `grade` 和 `source_partition`。

### Q: 既然 `asset_status=restored_and_frozen`,是不是说明所有下游 target 资产都已经讲清楚了?

A: 也不是。
它只说明当前绑定的数据资产已经冻结。
对应的 boundary / distance 输出说明文还需要单独补。

## 读完后下一步看什么

建议接着看:

1. `src_data_datasets.py.md`
2. `src_data_csv_loader.py.md`
3. 后续的 `splits_crag_crag_train153.csv.md`

这样你才能把 CRAG 配置、CSV schema 和正式训练池组成串起来。
