# src_data_datasets.py.md

## 这个文件的作用

- 这份代码是当前数据消费链的总装配入口
- 它把 `configs/data/*.yaml`、`splits/*/*.csv` 和 `datasets/...` 这三层正式资产接起来

换句话说,`csv_loader.py` 负责守表结构,而 `datasets.py` 负责把“配置 + split + 路径”拼成可消费样本。

## 结构化溯源卡片

- 正式对象: `src/data/datasets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `benchmark data split and evaluation setup`
- 公式/定义: `正式评估必须绑定确定的数据配置、固定 split 和稳定标签身份`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `src/data/datasets.py`
- commit: `workspace_local_20260704`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `dataset_root`, `split_dir`, `csv_files`, `mask_interp`, `normalize_mean`, `normalize_std`

### 当前实现落点
- 文件: `src/data/datasets.py`
- 符号: `simple_yaml_load()`, `DataConfig`, `load_data_config()`, `resolve_split_csv()`, `build_dataset_from_csv()`

## 它在整个阶段中的位置

当前正式消费链可以直接写成一条线:

1. `configs/data/glas.yaml` 或 `configs/data/crag.yaml`
2. `load_data_config()`
3. `resolve_split_csv()`
4. `build_dataset_from_csv()`
5. `scripts/train.py`

这条链条的意义很明确:

- 不让 `scripts/train.py` 自己到处猜路径
- 不让 split 文件绕开数据配置直接被乱读
- 不让 dataset root 在不同脚本里各写一套

## 当前实现状态

- 状态: `已实现`
- 可运行性: `已被 scripts/train.py 和多个工具脚本消费`
- 当前阶段作用: `formal data_protocol_preflight 的统一配置入口`

这里真正重要的不是“功能多”,而是“所有正式入口都走同一条路”。

## 主要流程

### 1. 解析最小 YAML

`parse_scalar()` 和 `simple_yaml_load()` 实现的是当前项目自己的轻量 YAML 解析。

用人话说,它没有追求通用 YAML 全覆盖。
它只支持当前数据配置文件真正用到的标量、列表和嵌套 mapping。

### 2. 把配置装成 `DataConfig`

`DataConfig` 明确列出了当前阶段真正需要冻结的字段,比如:

- `dataset_code`
- `dataset_root`
- `split_dir`
- `csv_files`
- `split_csv_schema_version`
- `sample_id_rule_version`
- `asset_status`

这一步的价值在于: 配置不再只是松散字典,而是一个明确字段集合。

### 3. 解析数据根目录和 split CSV

`resolve_dataset_root()` 负责得到数据根目录。

`resolve_split_csv()` 负责根据 `split_name` 从 `csv_files` 里找到真正的 split 文件。

这两个函数一起把“配置里写的对象”变成“工程里能打开的对象”。

### 4. 把 split CSV 真正装成样本列表

`build_dataset_from_csv()` 会:

1. 找到目标 CSV
2. 调 `csv_loader.py` 读取和校验
3. 把每一行解析成 sample dict
4. 把 `image_path`、`mask_path` 和原始 `meta` 一起保留下来

所以后面的 `scripts/train.py` 并不是直接碰 CSV。
它拿到的是这一步已经装好的 sample 列表。

## 关键函数怎么看

### `simple_yaml_load(text)`

- 作用: 解析当前项目实际在用的简化 YAML
- 输入: 原始 YAML 文本
- 输出: Python dict

这里最重要的不是解析器多强,而是它够不够稳定地解析当前两份正式数据配置。

### `DataConfig`

- 作用: 把 data config 从“散字典”收敛成明确字段
- 当前关键字段: `dataset_root`, `split_dir`, `csv_files`, `asset_status`

这能减少两个风险:

1. 调用方自己拼错 key
2. 配置文件里塞了无关字段,却没人知道哪些是正式必需字段

### `load_data_config(project_root, config_path)`

- 作用: 读取 YAML 并构造 `DataConfig`
- 输出: 已经结构化的数据配置对象

这一步后,下游不用再每次自己做类型转换。

### `resolve_split_csv(project_root, config, split_name)`

- 作用: 根据 `split_name` 定位正式 CSV
- 核心逻辑: 从 `config.csv_files` 查当前 split 对应的文件名

这一步把“train/val/testA/testB/test”这些逻辑名字,变成了真正的磁盘文件。

### `build_dataset_from_csv(project_root, config, split_name)`

- 作用: 把 data config 和 split CSV 组合成样本列表
- 输出: `list[dict[str, Any]]`

这一步是当前阶段最关键的总装配函数。
因为后续 preflight 能不能老老实实吃到正式资产,就看它。

## 当前代码里最关键的设计取舍

### 取舍 1: 自己写最小 YAML 解析,而不是引入更重依赖

当前阶段这么做是保守选择。

原因不是“通用解析器不好”,而是:

- 现在正式数据配置结构很简单
- 项目更需要稳定和可控
- 当前阶段重点是冻结正式协议,不是扩展配置语言能力

### 取舍 2: 先校验 split,再装 sample

`build_dataset_from_csv()` 没有边读边糊里糊涂地往下跑。
它先把 schema 问题和唯一性问题收集出来,确认没问题再生成 samples。

这比“先跑起来再看哪里炸”更适合正式协议阶段。

### 取舍 3: sample 里保留 `meta`

当前 sample dict 不只留路径,还把原始 row 放到 `meta` 里。

这意味着后续如果要追 `grade`、`source_partition`、`source_subset`,还有回查入口。

## 和真实文件怎么对上

### GlaS 配置

- `configs/data/glas.yaml` 里写了:
  - `dataset_root: datasets/01_GlaS_official_raw`
  - `split_dir: splits/glas`
  - `csv_files.train: glas_train68.csv`

所以 `resolve_split_csv(..., "train")` 最终会对到:

- `splits/glas/glas_train68.csv`

### CRAG 配置

- `configs/data/crag.yaml` 里写了:
  - `dataset_root: datasets/02_CRAG_reorganized_local_copy`
  - `split_dir: splits/crag`
  - `csv_files.train: crag_train153.csv`

所以 CRAG train 会对到:

- `splits/crag/crag_train153.csv`

## 如何手工验证这份代码

### 验证 1: 看配置字段是不是和 `DataConfig` 对齐

1. 打开 `configs/data/glas.yaml`
2. 再看 `DataConfig` 字段列表

通过标准:

- 你能逐项对上 `dataset_code`、`dataset_root`、`split_dir`、`csv_files`、`asset_status`

### 验证 2: 看 split 名字是不是从配置里解析出来

1. 在 `glas.yaml` 里找到 `csv_files.train: glas_train68.csv`
2. 在 `crag.yaml` 里找到 `csv_files.train: crag_train153.csv`
3. 再看 `resolve_split_csv()`

通过标准:

- 你能明确说明 train split 并不是写死在代码里,而是从配置映射出来

### 验证 3: 看 `scripts/train.py` 是否真实消费它

1. 打开 `scripts/train.py`
2. 查看是否调用了 `load_data_config()` 与 `build_dataset_from_csv()`

通过标准:

- 训练前 preflight 入口没有绕开 `datasets.py` 自己乱拼路径

## 最容易掉坑的地方

### 误区 1

“`datasets.py` 是不是已经等于 DataLoader 了?”

不是。
它当前只负责把 formal 配置和 split 资产装成样本描述。
真正的张量化 DataLoader 还不在 `01_数据协议` 的完成范围里。

### 误区 2

“既然 `simple_yaml_load()` 很简单,是不是以后想加什么都能随便往 YAML 里塞?”

也不是。
当前阶段强调的是冻结协议。
如果你往 YAML 里加字段,还得同步确认它是不是正式字段,是不是要进 `DataConfig` 和冻结表。

## 这份说明文没在说什么

这份文档没有声称下面这些内容已经成立:

- 图像增强流水线
- PyTorch Dataset / DataLoader 完整实现
- batch 级训练输入
- 模型前向或 loss 计算

说白了,它只是在解释“正式样本描述怎么被稳定装出来”。

## 读完后建议联读

按最短路径继续看:

1. `configs_data_glas.yaml.md`
2. `configs_data_crag.yaml.md`
3. `scripts_train.py.md`

如果你下一步要补 split 说明文,再接着去看 `splits/glas/*.csv` 和 `splits/crag/*.csv` 对应文档。
