# splits_glas_glas_train68.csv.md

## 这个文件的作用

- 这不是随手导出的中间表,它是 `GlaS` 在当前项目里唯一正式 `train68` 训练 split 资产
- 它把 `official_train85` 里允许进入训练池的那 `68` 个样本冻结成可交付 CSV

如果这份表漂了,后面的训练、验证和结果解释都会跟着漂。
所以它不是“给脚本看的普通输入”,而是 `01_数据协议` 要先锁死的正式对象。

## 结构化溯源卡片

- 正式对象: `splits/glas/glas_train68.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `official train/test organization`
- 公式/定义: `official_train85 -> project_frozen(train68 + val17), TestA60 / TestB20 preserved`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `tools/stage01_data_protocol/prepare_glas_split.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- 对应字段: `glas_split_version`, `split_seed`, `sample_id_rule_version`, `source_partition_rule_version`

### 当前实现落点
- 文件: `splits/glas/glas_train68.csv`
- 生成入口: `tools/stage01_data_protocol/prepare_glas_split.py`
- 消费入口: `src/data/csv_loader.py`, `src/data/datasets.py`, `configs/data/glas.yaml`

## 这个文件在整个阶段中的位置

这份 CSV 处在 `GlaS` 正式消费链的正中间:

1. 上游是 `tools/stage01_data_protocol/prepare_glas_split.py` 按 `split_seed = 3407` 和 `grade` 分层规则生成
2. 当前文件把 `68` 个训练样本冻结成正式表
3. `src/data/csv_loader.py` 负责校验字段和路径
4. `src/data/datasets.py` 再把这些行装成后续入口真正消费的 sample

所以它解决的不是“怎么训练得更好”,而是“训练到底只允许读哪 `68` 个正式样本”。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `已被正式配置链直接消费`
- 当前样本数: `68`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`

这份资产现在已经不是候选 split,而是当前项目承认的正式训练 split。

## 这份 CSV 里到底锁了什么

### 1. 样本身份锁定

表头第一列是 `sample_id`。
真实样本长这样:

`GlaS_official_train_train_1`

这说明样本身份不是只靠文件名猜出来,而是按照:

`dataset + "_" + source_partition + "_" + stem(image_filename)`

拼成正式主键。

### 2. 路径规则锁定

- `image_relpath` 形如 `datasets/01_GlaS_official_raw/train_1.bmp`
- `mask_relpath` 形如 `datasets/01_GlaS_official_raw/train_1_anno.bmp`

这里故意只存项目根相对路径,不存机器绝对路径。
这样这份 CSV 才能跟着项目一起交付,而不是绑定某一台电脑。

### 3. split 身份锁定

这一整份表里 `split` 都固定为 `train68`。

它的含义很明确:

- 当前这些样本只能承担训练职责
- 它们不能在后续流程里被冒充成 `val17`
- 也不能和 `testA60 / testB20` 混起来

### 4. 分层字段锁定

当前真实统计是:

- `malignant = 38`
- `benign = 30`
- `source_partition = official_train`

这正对应 `03_GlaS划分协议.md` 里“从 `official_train85` 一次性分层生成 `train68 / val17`”的要求。

## 对应代码里的真实协议痕迹

当前仓库里最关键的实现点有四处:

### `tools/stage01_data_protocol/prepare_glas_split.py`

- `GLAS_SPLIT_SEED = 3407`
- `stratified_train_val_split(...)`
- `build_row(..., split_name, grade, source_partition)`

这里把随机种子、按 `grade` 分层和 `sample_id/source_partition` 写成了实际代码,不是文档口头约定。

### `src/data/csv_loader.py`

- GlaS 强制要求 `grade,source_partition`
- 禁止绝对路径
- 要求 `sample_id` 唯一

也就是说,这份 CSV 不只是“长得像表格”就能过,它还要满足正式 schema。

## 如何验证这份文件没读偏

### 验证 1: 看样本数

直接统计:

- 结果应为 `68`

通过标准:

- 不能多,也不能少

### 验证 2: 看字段是否完整

检查表头:

`sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`

通过标准:

- 七个字段都在
- 没有把 `grade` 或 `source_partition` 丢掉

### 验证 3: 看样本来源是否仍然是 official train

检查 `source_partition` 列。

通过标准:

- 当前文件里都应是 `official_train`

### 验证 4: 看下游是不是只通过正式 CSV 读它

1. 打开 `configs/data/glas.yaml`
2. 看训练 split 是否指向 `splits/glas/glas_train68.csv`
3. 再打开 `src/data/datasets.py`

通过标准:

- 下游不应绕开正式 CSV 直接扫目录

## 最容易误解的地方

### 误区 1

“既然原始数据里已经有 `train_*.bmp`, 为什么还需要 `glas_train68.csv`?”

因为官方 `train85` 只是原始训练池,不是当前项目后续阶段要直接继承的固定训练 split。
这份 CSV 的作用就是把工程里真正承认的 `68` 个训练样本固定下来。

### 误区 2

“`train68` 既然是正式训练 split,是不是已经代表完整训练阶段完成了?”

不是。
它只说明 `01_数据协议` 已经把数据输入层冻结好了。
完整 UNet 训练链属于后面的 `02_UNet流程验证`。

## 读完后下一步看什么

读完这份文件后,最应该继续看:

1. `splits_glas_glas_val17.csv.md`
2. `src_data_csv_loader.py.md`
3. `configs_data_glas.yaml.md`

因为 `train68` 只是 `GlaS` 正式 split 的一部分,它还需要和 `val17` 以及正式配置一起看,边界才不会读偏。
