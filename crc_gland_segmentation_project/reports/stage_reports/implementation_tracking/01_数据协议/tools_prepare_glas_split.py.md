# tools_prepare_glas_split.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/prepare_glas_split.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: official train/test partition and benchmark split protocol
- 公式/定义: 官方 `train_` / `testA_` / `testB_` 命名和 grade 分层约束

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/prepare_glas_split.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `GLAS_SPLIT_SEED = 3407`、train68、val17、testA60、testB20、`split_csv_schema_version`

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/prepare_glas_split.py`
- 符号: `load_grade_map()` / `stratified_train_val_split()` / `build_row()` / `main()`

## 这个脚本的作用

这个脚本负责把 GlaS 原始官方目录整理成项目正式认账的 4 份 split CSV:

- `splits/glas/glas_train68.csv`
- `splits/glas/glas_val17.csv`
- `splits/glas/glas_testA60.csv`
- `splits/glas/glas_testB20.csv`

你可以把它理解成“GlaS 正式划分资产生成器”。

它最重要的价值，不是把 CSV 写出来这么简单，而是把 GlaS 的 split 规则从“口头约定”变成“冻结资产”。
如果这一步不固定，后面 `configs/data/glas.yaml`、`src/data/datasets.py`、`scripts/train.py` 就可能各自读到不同的样本边界。

## 这个脚本在整个阶段中的位置

当前阶段里，GlaS 这条正式链可以简化成:

```text
../../../../datasets/01_GlaS_official_raw
        ↓
../../../../datasets/01_GlaS_official_raw/Grade.csv
        ↓
../../../../tools/stage01_data_protocol/prepare_glas_split.py
        ↓
../../../../splits/glas/glas_train68.csv
../../../../splits/glas/glas_val17.csv
../../../../splits/glas/glas_testA60.csv
../../../../splits/glas/glas_testB20.csv
        ↓
../../../../configs/data/glas.yaml
        ↓
../../../../src/data/datasets.py
        ↓
../../../../scripts/train.py
```

上游依赖很明确:

1. `datasets/01_GlaS_official_raw`
2. `datasets/01_GlaS_official_raw/Grade.csv`
3. `configs/data/glas.yaml`

下游消费者也很明确:

1. `src/data/datasets.py`
2. `tools/stage01_data_protocol/check_dataset_pairs.py`
3. `tools/stage01_data_protocol/validate_data_assets.py`
4. `scripts/train.py`

换句话说，这个脚本不属于门禁小工具，而是正式数据资产生成链里的上游锚点。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- GlaS 划分协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- 数据检查与配对规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 工程目录框架: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

这张回链卡片真正要证明的是:
`../../../../tools/stage01_data_protocol/prepare_glas_split.py` 不是“为了方便临时写的脚本”，而是计划明确点名的正式工程落点。

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `split_seed: 3407`
  - `train68_count: 68`
  - `val17_count: 17`
  - `testA60_count: 60`
  - `testB20_count: 20`
  - `dataset_root`: `datasets/01_GlaS_official_raw`
- 当前物理证据:
  - `../../../../reports/data_checks/glas_split_report.md`
  - `../../../../splits/glas/glas_train68.csv`
  - `../../../../splits/glas/glas_val17.csv`
  - `../../../../splits/glas/glas_testA60.csv`
  - `../../../../splits/glas/glas_testB20.csv`

你现在最该盯住的不是“这个脚本能不能跑”，而是“它产出的数量和分层规则是不是稳定”。

## 脚本核心逻辑

### 主要流程

这个脚本现在的主流程可以拆成 6 步:

1. 读取 `configs/data/glas.yaml`
2. 通过 `resolve_dataset_root()` 找到 `datasets/01_GlaS_official_raw`
3. 读取 `datasets/01_GlaS_official_raw/Grade.csv`，建立 `sample -> grade` 映射
4. 扫描 `train_*.bmp`、`testA_*.bmp`、`testB_*.bmp`，并检查对应 `_anno.bmp`
5. 用固定随机种子 `3407` 对官方训练集做 grade 分层拆分
6. 把结果写成 4 份正式 CSV，并回写 `../../../../reports/data_checks/glas_split_report.md`

### 关键函数 1: `load_grade_map()`

这个函数负责把 `datasets/01_GlaS_official_raw/Grade.csv` 读成字典。

它不是死认一个列名，而是先用 `detect_grade_columns()` 识别 header，再把:

- `sample`、`image`、`name`、`filename`、`id`
- grade、class、label、type

这些可能出现的列名归一起来。

为什么这样设计？
因为 GlaS 的原始表头写法可能有轻微差异，但项目需要稳定拿到 `sample -> grade` 这层语义。

### 关键函数 2: `build_pairs()`

这个函数负责把 image 和 mask 成对抓出来。

它会扫描:

- `train_*.bmp`
- `testA_*.bmp`
- `testB_*.bmp`

然后强制要求每个 image 都有对应的 `_anno.bmp`。

如果 mask 不存在，它会直接抛 `FileNotFoundError`。
这一步的意义很实际: split 资产生成不能默默吞掉坏样本。

### 关键函数 3: `stratified_train_val_split()`

这是整个脚本最核心的一步。

它不是随机把 85 张官方训练图硬拆成 68/17，而是按 `grade` 先分组，再在每组内部打乱。
你可以把它理解成“先按类别分桶，再各桶按同一个种子切 val 配额”。

当前冻结逻辑有两条:

1. 随机种子固定为 `GLAS_SPLIT_SEED = 3407`
2. `val_count = round(len(group) * 17 / 85)`

最终脚本还会硬检查:

- `len(train_split) == 68`
- `len(val_split) == 17`

只要数量不对，就直接报错。

### 关键函数 4: `build_row()`

这个函数把单个 pair 变成正式 CSV 行。

当前写出的关键字段有:

- `sample_id`
- `image_relpath`
- `mask_relpath`
- `dataset`
- `split`
- `grade`
- `source_partition`

其中 `sample_id` 不是随手拼的，而是固定成:

`GlaS_{source_partition}_{image_stem}`

这能保证后面 `../../../../scripts/train.py`、`../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`、`../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 用的是同一套样本命名。

### 关键函数 5: `main()`

`main()` 做的是总装配:

1. 加载 config
2. 校验 dataset root 和 `datasets/01_GlaS_official_raw/Grade.csv`
3. 生成官方 train/testA/testB pair
4. 拆 train/val
5. 写 CSV
6. 写 `reports/data_checks/glas_split_report.md`

说白了，`main()` 不是做算法创新，而是把“规则写死并落盘”。

## 为什么这样设计

最容易出现的误解是:
“既然 split 最后只是 4 个 CSV，为什么不用手工整理好直接放仓库里？”

这里真正的设计取舍是:

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 手工维护 CSV | 直观 | 很难审计 seed、grade 分层和配对校验 | 否决 |
| 扫描目录后每次现场随机切 | 灵活 | 结果不稳定，无法冻结 | 否决 |
| 用脚本从正式根目录和 grade 元数据表生成固定 CSV | 可复现、可回溯 | 多了一次生成步骤 | 采用 |

这也是为什么脚本里要把 `3407` 写成常量，而不是每次随机。

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/prepare_glas_split.py --config configs/data/glas.yaml --output-dir splits/glas --report-output reports/data_checks/glas_split_report.md
```

运行成功后，至少应该得到:

1. `splits/glas/glas_train68.csv`
2. `splits/glas/glas_val17.csv`
3. `splits/glas/glas_testA60.csv`
4. `splits/glas/glas_testB20.csv`
5. `reports/data_checks/glas_split_report.md`

## 如何验证脚本运行结果

### 验证点 1: 数量是否对齐

检查方法:

1. 打开 `../../../../reports/data_checks/glas_split_report.md`
2. 看 `train68_count`、`val17_count`、`testA60_count`、`testB20_count`

通过标准:

- `train68 = 68`
- `val17 = 17`
- `testA60 = 60`
- `testB20 = 20`

### 验证点 2: CSV 路径是否真实存在

检查方法:

1. 打开 `../../../../splits/glas/`
2. 检查 4 份 CSV 是否存在
3. 随机打开其中一份，看 `image_relpath` 和 `mask_relpath`

通过标准:

- 路径都在 `datasets/01_GlaS_official_raw/` 下
- 不存在 image 有而 mask 没有的行

### 验证点 3: 下游配置是否真的消费这些 CSV

检查方法:

1. 打开 `../../../../configs/data/glas.yaml`
2. 查看 `csv_files`
3. 再打开 `../../../../src/data/datasets.py`

通过标准:

- `../../../../configs/data/glas.yaml` 里的 `csv_files` 和脚本写出的文件名一致
- `../../../../src/data/datasets.py` 通过相对路径解析这些 CSV

### 验证点 4: 训练入口有没有沿着这条链读取

检查方法:

1. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
2. 查看 `split_csv`

通过标准:

- 报告里出现 `splits/glas/glas_train68.csv`
- 没有绕开正式 split 直接扫原始目录

## 与项目其他部分的关联

这个脚本直接影响下面这些对象:

- `splits_glas_glas_train68.csv.md`
- `splits_glas_glas_val17.csv.md`
- `splits_glas_glas_testA60.csv.md`
- `splits_glas_glas_testB20.csv.md`
- `../../../../configs/data/glas.yaml`
- `../../../../src/data/csv_loader.py`
- `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

换句话说，它既决定 split 资产本身，也决定后面所有校验脚本到底在检查什么。

## 容易误解的地方

### 误解 1: `3407` 只是一个可有可无的随机种子

不是。
它是当前冻结协议的一部分。
如果你改了它，train68 / val17 的成员就可能漂掉。

### 误解 2: `testA60` 和 `testB20` 也要再参与 train/val 划分

不是。
它们本来就是官方测试分区。
脚本对它们做的是直接收集，不是重新切分。

### 误解 3: 有了这 4 份 CSV 就等于整个数据阶段已经自动通过

也不是。
split 只是正式链的一段。
后面还要经过 `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`、`../../../../tools/stage01_data_protocol/preview_dataset_samples.py`、`../../../../tools/stage01_data_protocol/validate_data_assets.py` 和最终验收文档。

## 5 分钟自检任务

你现在可能会问:

“既然 split 最后只是几份 CSV，为什么不直接手工维护？”

答案是：手工文件很难证明 grade 分层、固定随机种子和 image/mask 配对关系一直没漂。

如果你只给自己 5 分钟，建议做这三件事:

1. 打开 `../../../../tools/stage01_data_protocol/prepare_glas_split.py`，确认 `GLAS_SPLIT_SEED = 3407`
2. 打开 `../../../../reports/data_checks/glas_split_report.md`，确认四个数量分别是 68 / 17 / 60 / 20
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`，确认 `split_csv` 字段指向 `../../../../splits/glas/glas_train68.csv`

学完后你应该具备什么能力？

你应该能说清:

- GlaS 的正式 split 是怎么来的
- 为什么它必须由脚本稳定生成而不是手工维护
- 下游入口怎样证明自己真的消费了这套 split 资产
