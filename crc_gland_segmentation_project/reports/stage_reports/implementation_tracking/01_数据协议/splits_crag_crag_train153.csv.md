# splits_crag_crag_train153.csv.md

## 这个文件的作用

- 这不是临时拼出来的训练列表,它是 `CRAG` 在当前项目里唯一正式 `train153` 训练 split 资产
- 它把 `train_sup_16` 和 `train_unsup_137` 合并成后续阶段统一承认的训练池

如果这份表不稳定,后面所有 `CRAG` 补充验证都会失去同一输入层。
所以它是正式项目对象,不是一次性中间文件。

## 结构化溯源卡片

- 正式对象: `splits/crag/crag_train153.csv`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `MILD-Net` / `TA-Net` 中对 `CRAG` 作为腺体任务 benchmark 的使用
- 章节: `cross-dataset benchmark role`
- 公式/定义: `train153 = train_sup_16 union train_unsup_137`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `tools/stage01_data_protocol/prepare_crag_split.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`
- 对应字段: `crag_split_version`, `split_csv_schema_version`, `sample_id_rule_version`, `source_subset`

### 当前实现落点
- 文件: `splits/crag/crag_train153.csv`
- 生成入口: `tools/stage01_data_protocol/prepare_crag_split.py`
- 消费入口: `src/data/csv_loader.py`, `src/data/datasets.py`, `configs/data/crag.yaml`

## 这个文件在整个阶段中的位置

这份 CSV 是 `CRAG` 正式消费链的训练入口资产:

1. 上游是 `tools/stage01_data_protocol/prepare_crag_split.py` 从 `datasets/02_CRAG_reorganized_local_copy` 收集四个子目录
2. 当前文件把 `train_sup_16` 和 `train_unsup_137` 在 CSV 层合成统一 `train153`
3. `src/data/csv_loader.py` 负责校验字段、主键和相对路径
4. `src/data/datasets.py` 再把这些行装成后续正式 sample 列表

所以它锁住的是“`CRAG` 训练到底认哪 `153` 个样本”,而不是“某次实验恰好用了哪些文件”。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `已被正式配置链直接消费`
- 当前样本数: `153`
- 当前字段: `sample_id,image_relpath,mask_relpath,dataset,split,source_subset`

当前真实子集构成是:

- `train_sup_16 = 16`
- `train_unsup_137 = 137`

这和协议里的 `train153 = train_sup_16 union train_unsup_137` 完全一致。

## 这份 CSV 里到底锁了什么

### 1. 训练池合并规则锁定

当前文件里每一行的 `split` 都是 `train153`。

但这不代表来源被抹平了。
相反,它一边把训练职责统一成一个 split,一边保留 `source_subset` 记录原始来源。

### 2. 样本身份锁定

真实样本长这样:

`CRAG_train_sup_16_train_100`

这说明当前主键规则是:

`dataset + "_" + source_subset + "_" + stem(image_filename)`

也就是说,即使两个子集中有重名文件,主键层也能把来源区分开。

### 3. 路径规则锁定

- `image_relpath` 指向 `datasets/02_CRAG_reorganized_local_copy/.../image/*.png`
- `mask_relpath` 指向同一子集下的 `mask/*.png`

这里仍然只保存项目根相对路径。
原因和 `GlaS` 一样: 正式资产必须可交付,不能依赖本地绝对盘符。

### 4. 来源可追溯锁定

`source_subset` 这一列很关键。
它不是装饰字段,而是当前工程里解释 `CRAG train153` 来源结构的正式证据。

没有这列,后面就很难回答:

- 当前样本来自 `train_sup_16` 还是 `train_unsup_137`
- 某个错误案例是不是集中出现在某个来源子集

## 对应代码里的真实协议痕迹

当前仓库里最关键的实现点有三处:

### `tools/stage01_data_protocol/prepare_crag_split.py`

- `collect_subset_pairs(...)`
- `build_row(..., split_name, source_subset)`
- 对 `train153 / val20 / test40` 的固定样本数检查

这说明 `train153` 不是手写表,而是由正式脚本根据固定目录结构生成。

### `src/data/csv_loader.py`

- CRAG 强制要求 `source_subset`
- 禁止绝对路径
- 要求 `sample_id` 唯一

因此当前文件不仅要有 `153` 行,还必须满足 `CRAG` 的正式 schema。

## 如何验证这份文件没读偏

### 验证 1: 看样本总数

直接统计:

- 结果应为 `153`

通过标准:

- 和协议冻结值完全一致

### 验证 2: 看来源子集分布

检查 `source_subset` 分组统计。

通过标准:

- `train_sup_16 = 16`
- `train_unsup_137 = 137`

### 验证 3: 看字段是否完整

检查表头:

`sample_id,image_relpath,mask_relpath,dataset,split,source_subset`

通过标准:

- 六个字段都在
- 没有把 `source_subset` 丢掉

### 验证 4: 看下游是不是只通过正式 CSV 读它

1. 打开 `configs/data/crag.yaml`
2. 看训练 split 是否指向 `splits/crag/crag_train153.csv`
3. 再打开 `src/data/datasets.py`

通过标准:

- 下游不应跳过正式 CSV 直接扫 `train_sup_16` 或 `train_unsup_137`

## 最容易误解的地方

### 误区 1

“既然 `train153` 已经把两个训练子集合并了,那是不是 `source_subset` 可以不要?”

不行。
`source_subset` 是当前项目解释 `CRAG` 训练池来源结构的正式字段。
去掉它,训练池就失去可追溯性。

### 误区 2

“`train153` 既然是正式训练 split,那 `CRAG` 阶段是不是已经跑完了?”

也不是。
它只表示 `01_数据协议` 已经把 `CRAG` 的训练输入层固定好了。
后续真正的 `CRAG` 补充验证仍然属于后面的模型阶段。

## 读完后下一步看什么

读完这份文件后,最应该继续看:

1. `splits_crag_crag_val20.csv.md`
2. `src_data_csv_loader.py.md`
3. `configs_data_crag.yaml.md`

因为 `train153` 只是 `CRAG` 正式 split 的训练部分,它还要和 `val20`、`test40` 以及正式配置一起看,边界才完整。
