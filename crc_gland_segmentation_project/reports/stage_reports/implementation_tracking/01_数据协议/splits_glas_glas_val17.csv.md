# splits_glas_glas_val17.csv.md

## 这个文件的作用

- 这份 CSV 是 `GlaS` 在当前项目里的唯一正式验证 split 资产
- 它把 `official_train85` 中被固定划给验证职责的 `17` 个样本写成可交付表

它的职责不是“额外训练池”,而是后续 checkpoint 选择和阈值冻结的唯一验证输入。

## 结构化溯源卡片

- 正式对象: `splits/glas/glas_val17.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `GlaS Challenge`
- 定义: `official_train85 -> project_frozen(train68 + val17)`

### 代码依据
- 文件: `tools/stage01_data_protocol/prepare_glas_split.py`
- 关键实现: `GLAS_SPLIT_SEED = 3407`, `stratified_train_val_split(...)`

### 冻结回链
- 协议文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- 对应字段: `split_seed`, `best_selector`, `threshold_source`

## 当前实现状态

- 状态: `已实现`
- 当前样本数: `17`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`
- 当前真实分布:
  - `malignant = 10`
  - `benign = 7`
  - `source_partition = official_train`

## 这份 CSV 锁了什么

### 1. 验证职责锁定

整份表里的 `split` 都固定为 `val17`。
这表示它只能承担:

- 验证监控
- checkpoint 选择
- 阈值来源

它不能被回写成正式测试结果。

### 2. 主键与路径锁定

- `sample_id` 仍采用 `GlaS_{source_partition}_{stem}`
- `image_relpath` 和 `mask_relpath` 都是项目根相对路径

这保证验证样本既可追溯,又可交付。

### 3. 分层来源锁定

`val17` 不是临时抽出来的观察集。
它是和 `train68` 同一次分层生成后被冻结下来的正式验证 split。

## 如何验证这份文件没读偏

1. 统计行数,结果应为 `17`
2. 检查 `split` 列,结果应全部为 `val17`
3. 检查 `source_partition`,结果应全部为 `official_train`
4. 在 `configs/data/glas.yaml` 中确认验证入口引用的是这份 CSV

## 最容易误解的地方

### 误区 1

“`val17` 也是从官方 train 里来的,那和 `train68` 混着用也没关系?”

不行。
一旦混用,后面的 checkpoint 选择和阈值来源就不再可解释。

### 误区 2

“既然它不是正式测试集,是不是不重要?”

也不对。
它虽然不进入主结果表,但后续很多正式裁决都会依赖它。

## 读完后下一步看什么

1. `splits_glas_glas_train68.csv.md`
2. `splits_glas_glas_testA60.csv.md`
3. `configs_data_glas.yaml.md`
