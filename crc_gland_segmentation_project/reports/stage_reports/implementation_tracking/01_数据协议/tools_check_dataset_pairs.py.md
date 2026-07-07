# tools_check_dataset_pairs.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: pair integrity, readability, duplicate control and manual audit readiness
- 公式/定义: 正式数据链必须证明 image/mask 成对、路径可读、前景非空、重复关系受控且人工抽查闭环

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `data_check_version`、`duplicate_check_status`、`manual_audit_status`、foreground summary

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- 符号: `mask_stats()` / `classify_token()` / `derive_manual_audit_status()` / `main()`

## 这个脚本的作用

这个脚本负责把“正式 split 里的样本到底健不健康”写成一组正式检查资产。

它不是只看 CSV 文件存在，也不是只做简单路径检查。
它会同时检查：

- image / mask 是否成对
- 文件是否可读
- sample_id / 路径是否重复
- mask 是否空壳
- 人工抽查是否真正闭环

你可以把它理解成“数据配对与样本健康总检查器”。

## 这个脚本在整个阶段中的位置

```text
../../../../configs/data/*.yaml
../../../../splits/**/*.csv
        ↓
../../../../tools/stage01_data_protocol/check_dataset_pairs.py
        ↓
../../../../reports/data_checks/dataset_stats.csv
../../../../reports/data_checks/foreground_summary.csv
../../../../reports/data_checks/object_size_summary.csv
../../../../reports/data_checks/duplicate_check_report.md
../../../../reports/data_checks/data_check_report.md
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
```

这里真正重要的是：
它把“split 资产存在”进一步推进成“split 对应的样本质量也经过正式检查”。

再问深一层：为什么当前阶段要单独保留这一层，而不是把这些检查全塞进总验收？
因为一旦 pair、可读性、重复冲突、前景空壳和人工审稿混在一起，总验收只能告诉你“没过”，却很难第一时间说清楚到底是哪一层先坏了。

白话一点说，这个脚本像数据阶段的体检中心。
`../../../../splits/**/*.csv` 只是挂号单，真正的健康结论要靠 `../../../../reports/data_checks/dataset_stats.csv`、`../../../../reports/data_checks/foreground_summary.csv`、`../../../../reports/data_checks/object_size_summary.csv`、`../../../../reports/data_checks/duplicate_check_report.md` 和 `../../../../reports/data_checks/data_check_report.md` 这组资产一起落盘。

如果你只想先抓最关键的证据文件，优先看这几份：

- `../../../../reports/data_checks/data_check_report.md`
- `../../../../reports/data_checks/dataset_stats.csv`
- `../../../../reports/data_checks/foreground_summary.csv`
- `../../../../reports/data_checks/object_size_summary.csv`
- `../../../../reports/data_checks/duplicate_check_report.md`
- `../../../../reports/data_checks/manual_audit_notes.md`

这些都是当前阶段会直接回看的具体路径。
其中 `../../../../reports/data_checks/data_check_report.md` 负责汇总状态字段，另外几份 CSV / Markdown 则保留更细的列、数值和样本数。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 数据检查与配对规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `pair_check_pass: pass`
  - `readable_check_pass: pass`
  - `duplicate_check_pass: pass`
  - `foreground_check_pass: pass`
  - `manual_audit_status: pass`
  - `data_check_bundle_status: pass`
- 当前物理证据:
  - `../../../../reports/data_checks/data_check_report.md`
  - `../../../../reports/data_checks/dataset_stats.csv`
  - `../../../../reports/data_checks/foreground_summary.csv`
  - `../../../../reports/data_checks/object_size_summary.csv`
  - `../../../../reports/data_checks/duplicate_check_report.md`
  - `../../../../reports/data_checks/manual_audit_notes.md`

## 脚本核心逻辑

### 主要流程

这个脚本现在可以拆成 6 步：

1. 读取 GlaS / CRAG 的正式 config 和 split CSV
2. 对每个样本检查 image/mask 路径是否存在且可读
3. 统计 mask 的前景比例、bbox 面积和空壳情况
4. 检查 sample_id、image_relpath、mask_relpath 是否重复
5. 读取 `../../../../reports/data_checks/manual_audit_notes.md` 把人工审稿状态压成统一字段
6. 写出 5 份检查资产和总报告

### 关键点 1：它检查的是“整条数据检查 bundle”

`../../../../reports/data_checks/data_check_report.md` 里不是只有一个 pass。
它把多个子门分开写出来：

- `pair_check_pass`
- `readable_check_pass`
- `duplicate_check_pass`
- `foreground_check_pass`
- `manual_audit_status`

这很重要，因为这样后面出问题时，能直接定位是“路径坏了”还是“人工抽查没闭环”。

### 关键点 2：它把人工审稿也纳入正式结论

很多人会以为人工审稿只是补充说明。
在当前项目里不是这样。

这个脚本会直接读取 `../../../../reports/data_checks/manual_audit_notes.md`，把人工抽查状态压成统一的三级裁决状态。

当前真实结果是：

- `manual_audit_status = pass`
- `manual_audit_reason = manual audit coverage and row-level review decisions are complete and acceptable.`

### 关键点 3：它真的做了数值级样本统计

这不是只有“有无文件”的布尔检查。
脚本会把每个样本的：

- `foreground_pixels`
- `foreground_ratio`
- `foreground_bbox_area`

写入统计资产。

所以 `../../../../reports/data_checks/dataset_stats.csv`、`../../../../reports/data_checks/foreground_summary.csv`、`../../../../reports/data_checks/object_size_summary.csv` 才有阶段价值，不是随手凑的表。

## 为什么这样设计

最容易出现的误解是：
“既然 split CSV 已经是正式资产，为啥还需要再做一次 pair check？”

因为 CSV 只是样本清单，不是样本质量证明。
这里有个很朴素的取舍：把问题拖到训练时才发现，表面上省了一步，实际上会把错误定位成本抬得很高；提前做这层 bundle，会多出几份报告，但每份报告都在回答一个具体问题。

这里的取舍是：

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 只相信 split CSV | 简单 | 无法证明路径可读和样本健康 | 否决 |
| 每次训练时现场发现坏样本 | 不用前置检查 | 错误暴露太晚 | 否决 |
| 先用正式工具输出数据检查 bundle | 可提前阻断问题 | 多几份检查资产 | 采用 |

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/check_dataset_pairs.py --output-dir reports/data_checks
```

运行成功后，至少应得到：

1. `../../../../reports/data_checks/data_check_report.md`
2. `../../../../reports/data_checks/dataset_stats.csv`
3. `../../../../reports/data_checks/foreground_summary.csv`
4. `../../../../reports/data_checks/object_size_summary.csv`
5. `../../../../reports/data_checks/duplicate_check_report.md`
6. `../../../../reports/data_checks/manual_audit_notes.md`

## 如何验证脚本运行结果

### 验证点 1：总状态是否全部通过

检查方法：

1. 打开 `../../../../reports/data_checks/data_check_report.md`
2. 查看 `## Summary`

通过标准：

- `pair_check_pass = pass`
- `readable_check_pass = pass`
- `duplicate_check_pass = pass`
- `foreground_check_pass = pass`
- `manual_audit_status = pass`

### 验证点 2：每个 split 的统计是否真实

检查方法：

1. 继续看 `../../../../reports/data_checks/data_check_report.md` 的 `## Per Split Summary`
2. 对照 `../../../../reports/data_checks/dataset_stats.csv`

通过标准：

- GlaS train68、val17、testA60、testB20
- CRAG train153、val20、test40
- `empty_mask_count` 当前都为 `0`

### 验证点 3：重复检查是否真正落盘

检查方法：

1. 打开 `../../../../reports/data_checks/duplicate_check_report.md`
2. 查看 `duplicate_*_conflicts`

通过标准：

- 冲突计数为 `0`
- `duplicate_check_status = pass`

## 与项目其他部分的关联

这个脚本直接影响：

- `../../../../src/data/csv_loader.py`
- `../../../../splits/**/*.csv`
- `../../../../reports/data_checks/manual_audit_notes.md`
- `../../../../reports/data_checks/data_check_report.md`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

换句话说，它是正式 split 资产和阶段总验收之间最关键的一层数据质量门。

## 容易误解的地方

### 误解 1：它是门禁脚本，所以应该归 B 类

这次不是。
当前计划明确把它当作正式数据检查工程落点，所以它属于 A 类。

### 误解 2：只要总数据检查报告是 pass，人工审稿就不重要

不对。
`manual_audit_status` 本身就是 pass 条件的一部分。

### 误解 3：它和阶段总验收脚本重复

也不是。
`../../../../tools/stage01_data_protocol/check_dataset_pairs.py` 负责局部数据检查 bundle，`../../../../tools/stage01_data_protocol/validate_data_assets.py` 负责阶段总裁决。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事：

1. 打开 `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`，确认它会读取 `../../../../reports/data_checks/manual_audit_notes.md`
2. 打开 `../../../../reports/data_checks/data_check_report.md`，确认 5 个关键子门都是 `pass`
3. 打开 `../../../../reports/data_checks/dataset_stats.csv`，确认 split 计数和正式 CSV 一致

学完后你应该具备什么能力？

你应该能说清：

- 当前正式 split 为什么还需要额外的数据质量检查 bundle
- 人工审稿为什么会被纳入正式数据检查结论
- 这个脚本和阶段总验收脚本是怎样分工的
