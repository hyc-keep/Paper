# tools_prepare_crag_split.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/prepare_crag_split.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: benchmark split thinking reused for fixed formal subset contracts
- 公式/定义: 本项目对 CRAG 采用固定的 train153 / val20 / test40 子集协议

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/prepare_crag_split.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: train153 / val20 / test40, `split_csv_schema_version`, `CRAG 数据根目录`

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/prepare_crag_split.py`
- 符号: `collect_subset_pairs()` / `build_row()` / `main()`

## 这个脚本的作用

这个脚本负责把 CRAG 的本地正式目录写成项目真正认账的 3 份 split CSV:

- `../../../../splits/crag/crag_train153.csv`
- `../../../../splits/crag/crag_val20.csv`
- `../../../../splits/crag/crag_test40.csv`

你可以把它理解成“CRAG 正式子集清单导出器”。

和 GlaS 不一样，CRAG 这里不是先从一个官方 train 集里再抽 val，而是直接认项目已经整理好的:

- `train_sup_16`
- `train_unsup_137`
- `val`
- `test`

然后把它们按正式协议合并成最终 3 份 CSV。

## 这个脚本在整个阶段中的位置

CRAG 这条链可以先记成:

```text
../../../../datasets/02_CRAG_reorganized_local_copy
        ↓
train_sup_16 / train_unsup_137 / val / test
        ↓
../../../../tools/stage01_data_protocol/prepare_crag_split.py
        ↓
../../../../splits/crag/crag_train153.csv
../../../../splits/crag/crag_val20.csv
../../../../splits/crag/crag_test40.csv
        ↓
../../../../configs/data/crag.yaml
        ↓
../../../../src/data/datasets.py
        ↓
../../../../scripts/train.py
```

上游依赖:

1. `datasets/02_CRAG_reorganized_local_copy`
2. `datasets/02_CRAG_reorganized_local_copy/train_sup_16/image` 与 `datasets/02_CRAG_reorganized_local_copy/train_sup_16/mask`
3. `datasets/02_CRAG_reorganized_local_copy/train_unsup_137/image` 与 `datasets/02_CRAG_reorganized_local_copy/train_unsup_137/mask`
4. `datasets/02_CRAG_reorganized_local_copy/val/image` 与 `datasets/02_CRAG_reorganized_local_copy/val/mask`
5. `datasets/02_CRAG_reorganized_local_copy/test/image` 与 `datasets/02_CRAG_reorganized_local_copy/test/mask`

下游消费者:

1. `src/data/datasets.py`
2. `tools/stage01_data_protocol/check_dataset_pairs.py`
3. `tools/stage01_data_protocol/validate_data_assets.py`
4. `scripts/train.py`

所以它同样不是“只服务本轮治理的工具脚本”，而是正式 split 资产生成器。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- CRAG 划分协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 工程目录框架: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

这组回链要说明的是:
CRAG 的 split 不是“仓库里碰巧有三份 CSV”，而是计划要求必须有稳定工程落点的正式资产。

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `dataset_root`: `datasets/02_CRAG_reorganized_local_copy`
  - `train153_count: 153`
  - `val20_count: 20`
  - `test40_count: 40`
- 当前物理证据:
  - `../../../../reports/data_checks/crag_split_report.md`
  - `../../../../splits/crag/crag_train153.csv`
  - `../../../../splits/crag/crag_val20.csv`
  - `../../../../splits/crag/crag_test40.csv`

和 GlaS 那条链不同，这里最该检查的是“子集目录组织有没有被正确翻译成正式 CSV”。

## 脚本核心逻辑

### 主要流程

这个脚本当前可以拆成 5 步:

1. 读取 `configs/data/crag.yaml`
2. 解析 `dataset_root`，当前真实路径是 `datasets/02_CRAG_reorganized_local_copy`
3. 分别扫描 `train_sup_16`、`train_unsup_137`、`val`、`test`
4. 把前两个子集并成 `train153`
5. 写 3 份 CSV 并回写 `../../../../reports/data_checks/crag_split_report.md`

### 关键函数 1: `collect_subset_pairs()`

这个函数负责把某个 subset 下的图像和 mask 成对收出来。

它强制要求目录结构是:

- `subset_root` 下存在 image 子目录
- `subset_root` 下存在 mask 子目录

然后逐个检查:

- `image_root` 是否存在
- `mask_root` 是否存在
- 每个 image 是否有同名 mask

如果任何一步不对，它直接抛错，不会默默跳过坏样本。

这一步很重要，因为 CRAG 的风险不在随机切分，而在“目录重组后有没有丢对齐关系”。

### 关键函数 2: `build_row()`

这个函数把 pair 写成正式 CSV 行。

关键字段有:

- `sample_id`
- `image_relpath`
- `mask_relpath`
- `dataset`
- `split`
- `source_subset`

其中 `sample_id` 的规则是:

`CRAG_{source_subset}_{image_stem}`

你可以把 `source_subset` 理解成“样本血统标签”。
它的价值在于，后面别人看到一行 train153 数据时，还能回溯它究竟来自 `train_sup_16` 还是 `train_unsup_137`。

### 关键函数 3: `main()`

`main()` 做的不是复杂算法，而是把协议装配成稳定资产:

1. 校验 `dataset_root`
2. 读取 4 个子集
3. 把两个训练子集合并成 `train153`
4. 硬检查数量必须等于 153 / 20 / 40
5. 写 CSV
6. 生成 `../../../../reports/data_checks/crag_split_report.md`

这里的数量检查不是装饰。
它直接回答“当前正式资产到底有没有完整恢复”。

## 为什么这样设计

最容易被低估的一点是:
CRAG 这里看起来不像 GlaS 那样有随机划分，所以很多人会以为“那就手动整理三份 CSV 就完了”。

你现在可能会问:

“既然没有随机种子，这个脚本为什么还是 A 类正式对象？”

用人话说，这里真正容易漂掉的不是随机性，而是目录重组之后的 image/mask 对齐和 `source_subset` 血统。

实际不是这样。
CRAG 的主要风险在于目录重组和子集归属，如果不用脚本固化，很快就会出现:

- subset 名写错
- image/mask 对不齐
- 训练子集缺一块
- 相对路径漂移

这里的取舍可以概括成:

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 手动维护 train153、val20、test40 三份 CRAG CSV | 省代码 | 难以证明来自哪个 subset，也不易审计 | 否决 |
| 每次动态扫目录直接训练 | 少一层资产 | 破坏“先冻结 split 再消费”的协议 | 否决 |
| 用脚本把子集目录导出成稳定 CSV | 路径和数量都可验证 | 多一次导出动作 | 采用 |

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/prepare_crag_split.py --config configs/data/crag.yaml --output-dir splits/crag --report-output reports/data_checks/crag_split_report.md
```

运行成功后，应该看到:

1. `../../../../splits/crag/crag_train153.csv`
2. `../../../../splits/crag/crag_val20.csv`
3. `../../../../splits/crag/crag_test40.csv`
4. `../../../../reports/data_checks/crag_split_report.md`

## 如何验证脚本运行结果

### 验证点 1: 数量是否对齐

检查方法:

1. 打开 `../../../../reports/data_checks/crag_split_report.md`
2. 查看三个数量字段

通过标准:

- `train153 = 153`
- `val20 = 20`
- `test40 = 40`

### 验证点 2: 训练集是否真的由两个子集合并而成

检查方法:

1. 打开 `../../../../splits/crag/crag_train153.csv`
2. 查看 `source_subset` 列

通过标准:

- 只能出现 `train_sup_16` 和 `train_unsup_137`
- 不能出现 `val` 或 `test`

### 验证点 3: 路径是否还落在正式数据根目录下

检查方法:

1. 随机抽几行 `image_relpath` 和 `mask_relpath`
2. 回到 `datasets/02_CRAG_reorganized_local_copy` 下检查

通过标准:

- 路径真实存在
- image 和 mask 文件名同名

### 验证点 4: 下游配置和数据装配是否真的消费这些 CSV

检查方法:

1. 打开 `../../../../configs/data/crag.yaml`
2. 查看 `csv_files`
3. 再打开 `../../../../src/data/datasets.py`

通过标准:

- `../../../../configs/data/crag.yaml` 写的是 train153、val20、test40 这 3 份 CRAG CSV
- `../../../../src/data/datasets.py` 没有跳过 CSV 直接扫目录

## 与项目其他部分的关联

这个脚本直接影响:

- `splits_crag_crag_train153.csv.md`
- `splits_crag_crag_val20.csv.md`
- `splits_crag_crag_test40.csv.md`
- `../../../../configs/data/crag.yaml`
- `../../../../src/data/csv_loader.py`
- `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

也就是说，它既决定了 CRAG split 资产怎么生成，也决定了后面所有验证动作到底在验证什么。

## 容易误解的地方

### 误解 1: `train153` 就是一个原生单独目录

不是。
它是 `train_sup_16 + train_unsup_137` 合并后的正式训练 split。

### 误解 2: 既然没有随机种子，这个脚本就不重要

也不是。
这里的关键风险换成了“子集对齐和目录组织”，不是随机性。

### 误解 3: 这份 CSV 只给训练入口看，和验收无关

不对。
`../../../../tools/stage01_data_protocol/validate_data_assets.py` 和 `../../data_stage_acceptance.md` 也要基于这些 CSV 判断 `pass_split` 和 `handoff_ready`。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事:

1. 打开 `../../../../tools/stage01_data_protocol/prepare_crag_split.py`，确认 `train153` 是由两个训练子集合并而来
2. 打开 `../../../../reports/data_checks/crag_split_report.md`，确认数量是 153 / 20 / 40
3. 打开 `../../../../configs/data/crag.yaml`，确认 `csv_files` 指向这 3 份 CSV

学完后你应该具备什么能力？

你应该能说清:

- CRAG 的 split 资产为什么不是手写清单
- `train153` 到底由哪两部分组成
- 下游脚本为什么必须沿着这套正式 CSV 继续走
