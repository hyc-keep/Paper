# splits_crag_crag_test40.csv.md

## 这个文件的作用

- 这份 CSV 是 `CRAG` 在当前项目里的唯一正式测试 split 资产
- 它固定了 `40` 个测试样本,供后续 `CRAG` 最终结果和案例展示使用

它的核心作用,是把 `CRAG` 的测试职责从训练和验证里彻底分开。

## 结构化溯源卡片

- 正式对象: `splits/crag/crag_test40.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `MILD-Net` / `TA-Net` 的 `CRAG` benchmark 使用背景
- 定义: 当前 `test40` 是项目冻结的正式测试 split

### 代码依据
- 文件: `tools/stage01_data_protocol/prepare_crag_split.py`
- 关键实现: `test_rows = [build_row(..., "test40", "test")]`

### 冻结回链
- 协议文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`
- 对应字段: `test_split_name`, `eval_proto_version`

## 当前实现状态

- 状态: `已实现`
- 当前样本数: `40`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,source_subset`
- 当前真实分布:
  - `source_subset = test`

## 这份 CSV 锁了什么

### 1. 测试职责锁定

整份表里的 `split` 都固定为 `test40`。
它只能进入最终评估和展示链,不能回流做调参。

### 2. 来源边界锁定

`source_subset` 固定为 `test`。
这说明当前测试输入来自本地整理版里专门保留的测试目录。

### 3. 路径与主键锁定

真实路径都指向:

- `datasets/02_CRAG_reorganized_local_copy/test/image/*.png`
- `datasets/02_CRAG_reorganized_local_copy/test/mask/*.png`

主键格式则保持 `CRAG_test_{stem}` 这一类正式可追溯命名。

## 如何验证这份文件没读偏

1. 统计行数,结果应为 `40`
2. 检查 `split` 列,结果应全部为 `test40`
3. 检查 `source_subset`,结果应全部为 `test`
4. 确认后续测试入口只通过正式 CSV 消费它

## 最容易误解的地方

### 误区 1

“`CRAG` 的测试集反正只是补充验证,看完后再微调也问题不大。”

不行。
一旦回调测试集,它就不再是正式测试证据。

### 误区 2

“`val20` 和 `test40` 都来自固定目录,差别主要只是数量。”

也不对。
两者的职责不同,一个服务验证,一个服务最终测试。

## 读完后下一步看什么

1. `splits_crag_crag_val20.csv.md`
2. `splits_crag_crag_train153.csv.md`
3. `configs_data_crag.yaml.md`
