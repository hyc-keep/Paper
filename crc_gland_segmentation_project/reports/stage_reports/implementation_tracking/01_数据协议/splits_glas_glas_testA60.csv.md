# splits_glas_glas_testA60.csv.md

## 这个文件的作用

- 这份 CSV 是 `GlaS` 官方 `TestA` 子集在当前项目里的唯一正式测试资产
- 它固定了 `60` 个 `testA` 样本,供后续正式测试链单独汇报

它的意义不是“普通测试表”,而是保住 `TestA / TestB` 分开报告这条 benchmark 边界。

## 结构化溯源卡片

- 正式对象: `splits/glas/glas_testA60.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `GlaS Challenge`
- 定义: `TestA60` 必须保留独立身份

### 代码依据
- 文件: `tools/stage01_data_protocol/prepare_glas_split.py`
- 关键实现: `official_test_a = build_pairs(dataset_root, "testA_")`

### 冻结回链
- 协议文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- 对应字段: `test_split_name`, `source_partition_rule_version`

## 当前实现状态

- 状态: `已实现`
- 当前样本数: `60`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`
- 当前真实分布:
  - `source_partition = official_testA`
  - `grade = not_applicable`

## 这份 CSV 锁了什么

### 1. 官方测试子集身份锁定

整份表里的 `split` 都固定为 `testA60`。
这表示:

- 它只能进入正式测试链
- 不能回流训练或验证
- 也不能和 `testB20` 合成一个不分子集的单值来替代正式记录

### 2. 路径与配对锁定

当前真实路径形如:

- `datasets/01_GlaS_official_raw/testA_1.bmp`
- `datasets/01_GlaS_official_raw/testA_1_anno.bmp`

这说明它直接回指官方 `TestA` 资产,而不是工程里额外拼出来的集合。

### 3. `grade` 字段边界锁定

这里的 `grade` 固定写成 `not_applicable`。
这不是缺信息,而是在明确表达:

- `TestA60` 的正式职责是测试
- 当前 split 资产不依赖训练期 `grade` 分层逻辑

## 如何验证这份文件没读偏

1. 统计行数,结果应为 `60`
2. 检查 `split` 列,结果应全部为 `testA60`
3. 检查 `source_partition`,结果应全部为 `official_testA`
4. 检查 `grade`,结果应全部为 `not_applicable`

## 最容易误解的地方

### 误区 1

“`TestA` 和 `TestB` 最后反正都要算指标,先合起来也没关系。”

不行。
当前协议明确要求两者分开保留。

### 误区 2

“`grade = not_applicable` 是不是表示这份表不完整?”

不是。
这里是在说明 `TestA60` 的正式测试身份,不是训练分层身份。

## 读完后下一步看什么

1. `splits_glas_glas_testB20.csv.md`
2. `splits_glas_glas_val17.csv.md`
3. `configs_data_glas.yaml.md`
