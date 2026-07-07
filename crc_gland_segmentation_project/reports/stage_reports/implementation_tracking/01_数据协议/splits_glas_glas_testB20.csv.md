# splits_glas_glas_testB20.csv.md

## 这个文件的作用

- 这份 CSV 是 `GlaS` 官方 `TestB` 子集在当前项目里的唯一正式测试资产
- 它固定了 `20` 个 `testB` 样本,供后续正式结果单独汇报

它最重要的作用,是防止 `TestB` 被平均值吞掉。

## 结构化溯源卡片

- 正式对象: `splits/glas/glas_testB20.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `GlaS Challenge`
- 定义: `TestB20` 必须保留独立测试身份

### 代码依据
- 文件: `tools/stage01_data_protocol/prepare_glas_split.py`
- 关键实现: `official_test_b = build_pairs(dataset_root, "testB_")`

### 冻结回链
- 协议文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- 对应字段: `test_split_name`, `difficulty_note`

## 当前实现状态

- 状态: `已实现`
- 当前样本数: `20`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`
- 当前真实分布:
  - `source_partition = official_testB`
  - `grade = not_applicable`

## 这份 CSV 锁了什么

### 1. 困难测试子集身份锁定

整份表里的 `split` 都固定为 `testB20`。
这意味着它必须和 `testA60` 分开保留、分开汇报、分开解释。

### 2. 官方来源锁定

当前真实路径都回指:

- `datasets/01_GlaS_official_raw/testB_*.bmp`
- `datasets/01_GlaS_official_raw/testB_*_anno.bmp`

这说明它不是工程内重划出来的测试集,而是官方测试子集的正式映射。

### 3. 不回流规则锁定

`testB20` 只能用于最终测试与案例分析。
它不能被拿回去做阈值搜索或 checkpoint 调整。

## 如何验证这份文件没读偏

1. 统计行数,结果应为 `20`
2. 检查 `split` 列,结果应全部为 `testB20`
3. 检查 `source_partition`,结果应全部为 `official_testB`
4. 检查 `grade`,结果应全部为 `not_applicable`

## 最容易误解的地方

### 误区 1

“`TestB` 只有 20 个样本,单独留着意义不大。”

不对。
它正是当前 benchmark 里最不能被合并吞掉的那部分证据。

### 误区 2

“既然 `TestA`、`TestB` 字段结构一样,那只保留一个说明文就够了。”

也不对。
结构相同不等于职责相同。

## 读完后下一步看什么

1. `splits_glas_glas_testA60.csv.md`
2. `splits_glas_glas_val17.csv.md`
3. `configs_data_glas.yaml.md`
