# splits_crag_crag_val20.csv.md

## 这个文件的作用

- 这份 CSV 是 `CRAG` 在当前项目里的唯一正式验证 split 资产
- 它固定了 `20` 个验证样本,供后续 `CRAG` checkpoint 选择和阈值来源使用

它不是训练池的补充,而是训练和测试之间的正式边界。

## 结构化溯源卡片

- 正式对象: `splits/crag/crag_val20.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `MILD-Net` / `TA-Net` 的 `CRAG` benchmark 使用背景
- 定义: `CRAG` 需要稳定验证集,但当前 `val20` 是项目冻结的工程 split

### 代码依据
- 文件: `tools/stage01_data_protocol/prepare_crag_split.py`
- 关键实现: `val_rows = [build_row(..., "val20", "val")]`

### 冻结回链
- 协议文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`
- 对应字段: `val_split_name`, `threshold_source`

## 当前实现状态

- 状态: `已实现`
- 当前样本数: `20`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,source_subset`
- 当前真实分布:
  - `source_subset = val`

## 这份 CSV 锁了什么

### 1. 验证职责锁定

整份表里的 `split` 都固定为 `val20`。
这表示它只承担验证监控、checkpoint 选择和阈值来源职责。

### 2. 来源边界锁定

`source_subset` 固定为 `val`。
这说明它来自本地整理版里已经分出的验证目录,而不是从 `train153` 里临时再抽。

### 3. 可追溯路径锁定

当前真实路径都指向:

- `datasets/02_CRAG_reorganized_local_copy/val/image/*.png`
- `datasets/02_CRAG_reorganized_local_copy/val/mask/*.png`

这让后续验证输入保持稳定可交付。

## 如何验证这份文件没读偏

1. 统计行数,结果应为 `20`
2. 检查 `split` 列,结果应全部为 `val20`
3. 检查 `source_subset`,结果应全部为 `val`
4. 在 `configs/data/crag.yaml` 中确认验证入口引用的是这份 CSV

## 最容易误解的地方

### 误区 1

“`CRAG` 只是补充 benchmark,那验证集要求可以松一点。”

不行。
补充 benchmark 也必须有稳定验证边界。

### 误区 2

“既然 `val20` 来自固定目录,那就不用单独写 CSV 了。”

也不对。
正式消费链要求下游只认配置和 CSV,不能靠直接扫目录替代。

## 读完后下一步看什么

1. `splits_crag_crag_test40.csv.md`
2. `splits_crag_crag_train153.csv.md`
3. `configs_data_crag.yaml.md`
