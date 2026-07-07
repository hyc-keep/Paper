# tools_preview_dataset_samples.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/preview_dataset_samples.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: qualitative review, split-level preview evidence and human audit coverage
- 公式/定义: 正式数据协议不能只靠自动统计，还要给出可视化抽查证据，让人工能复核 raw、mask_bin、overlay 是否一致

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/preview_dataset_samples.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `manual_audit_version`、GlaS 5/3/2/2、CRAG 5/3/3、preview coverage

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/preview_dataset_samples.py`
- 符号: `pick_indices()` / `build_mask_binary()` / `build_overlay()` / `required_count()` / `main()`

## 这个脚本的作用

这个脚本负责把“当前正式 split 抽出来给人看的样本”真正导出来。

它不是训练工具，也不是统计汇总器。
它做的是：

- 从正式 split 里挑代表样本
- 导出 raw 图
- 导出二值 mask 图
- 导出 overlay 图
- 生成人工审稿清单

你可以把它理解成“正式人工抽查入口生成器”。

## 这个脚本在整个阶段中的位置

```text
../../../../splits/**/*.csv
        ↓
../../../../tools/stage01_data_protocol/preview_dataset_samples.py
        ↓
../../../../reports/data_preview/**
../../../../reports/data_checks/manual_audit_notes.md
        ↓
../../../../tools/stage01_data_protocol/check_dataset_pairs.py
../../../../tools/stage01_data_protocol/validate_data_assets.py
```

换句话说，它负责把“机器能检查的东西”进一步变成“人也能直接复核的东西”。
如果你只留自动统计，不留这一步，很多明显的边缘错位、遮罩贴合问题其实很难被数字一眼说清。

所以它在阶段里的角色很明确：先沿正式 split 把代表样本挑出来，再把 `../../../../reports/data_preview/**` 里的三联图和 `../../../../reports/data_checks/manual_audit_notes.md` 一起铺好，让人工抽查能落到真实资产上。
白话一点说，这一步是在给机器检查结果补“人眼复核窗口”。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 数据检查与配对规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 数据阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `manual_audit_version: manual_audit_v1`
  - `manual_audit_status: pass`
  - `manual_audit_required_pairs: 23`
  - `manual_audit_exported_pairs: 23`
  - `manual_audit_coverage_status: pass`
- 当前物理证据:
  - `../../../../reports/data_checks/manual_audit_notes.md`
  - `../../../../reports/data_preview/glas/train68/GlaS_official_train_train_1__raw.png`
  - `../../../../reports/data_preview/glas/train68/GlaS_official_train_train_1__mask_bin.png`
  - `../../../../reports/data_preview/glas/train68/GlaS_official_train_train_1__overlay.png`
  - `../../../../reports/data_preview/crag/test40/CRAG_test_test_9__overlay.png`

## 脚本核心逻辑

### 主要流程

这个脚本现在的主流程可以拆成 6 步：

1. 读取正式 config 和 split CSV
2. 按 `AUDIT_TARGETS` 计算每个 split 的最小抽查数量
3. 用等间距索引挑代表样本
4. 导出 `raw`、`mask_bin`、`overlay` 三类图片
5. 生成 `../../../../reports/data_checks/manual_audit_notes.md` 的覆盖表和审稿表
6. 把人工终审需要填写的列预先铺好

### 关键点 1：抽查数量不是临时拍脑袋

当前抽查覆盖目标是冻结的：

- GlaS: 5 / 3 / 2 / 2
- CRAG: 5 / 3 / 3

这组数直接决定了为什么当前 `manual_audit_required_pairs = 23`。

### 关键点 2：它不是只导 overlay

人工复核需要三种视角一起看：

- `raw`
- `mask_bin`
- `overlay`

如果只给 overlay，人看得快，但很难确定二值 mask 本体有没有问题。
如果只给 raw 和 mask_bin，又不容易快速判断贴合度。

所以三类图必须一起保留。

### 关键点 3：它会直接生成正式人工审稿表

`../../../../reports/data_checks/manual_audit_notes.md` 不是另一个人手工从零写出来的。
它的表格骨架、覆盖统计和审稿列，都是这个脚本生成的。

当前真实结果里，人工审稿表已经从最初的 `partial` 收口到：

- `manual_audit_status = pass`
- `manual_review_completion = 完成`

这说明预览链现在不只是“图导出来了”，而是“人工也真的看过了”。

## 为什么这样设计

最容易被低估的一点是：
“既然已经有 `../../../../tools/stage01_data_protocol/check_dataset_pairs.py` 了，为什么还要单独留一个 preview 工具？”

因为自动统计和人眼复核不是一回事。

这里的取舍是：

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 只做自动统计 | 快 | 很难发现明显视觉错位 | 否决 |
| 人工手工随便截几张图 | 灵活 | 无法保证 split 覆盖一致 | 否决 |
| 用正式脚本按协议导出 preview 并附带审稿表 | 可复核、可回填 | 多一层资产 | 采用 |

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/preview_dataset_samples.py --output-root reports/data_preview --manual-audit-output reports/data_checks/manual_audit_notes.md
```

运行成功后，至少应得到：

1. `../../../../reports/data_checks/manual_audit_notes.md`
2. `../../../../reports/data_preview/**/__raw.png`
3. `../../../../reports/data_preview/**/__mask_bin.png`
4. `../../../../reports/data_preview/**/__overlay.png`

## 如何验证脚本运行结果

### 验证点 1：覆盖数量是否符合协议

检查方法：

1. 打开 `../../../../reports/data_checks/manual_audit_notes.md`
2. 查看顶部字段和 `## Coverage Summary`

通过标准：

- `manual_audit_required_pairs = 23`
- `manual_audit_exported_pairs = 23`
- `manual_audit_coverage_status = pass`

### 验证点 2：人工审稿是否真的闭环

检查方法：

1. 继续看 `../../../../reports/data_checks/manual_audit_notes.md`
2. 查看 `manual_audit_status` 和 `manual_review_completion`

通过标准：

- `manual_audit_status = pass`
- `manual_review_completion = 完成`

### 验证点 3：预览目录是否真的包含三类图

检查方法：

1. 打开 `../../../../reports/data_preview/glas/train68/`
2. 随机挑一个样本

通过标准：

- 同时存在 `__raw.png`
- 同时存在 `__mask_bin.png`
- 同时存在 `__overlay.png`

## 与项目其他部分的关联

这个脚本直接影响：

- `../../../../reports/data_preview/**`
- `../../../../reports/data_checks/manual_audit_notes.md`
- `../../../../tools/stage01_data_protocol/check_dataset_pairs.py`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- `../../../../reports/stage_reports/asset_manifest.json`

也就是说，它是正式数据链里“人工复核入口”这一段的唯一工程落点。

## 容易误解的地方

### 误解 1：有预览图就等于人工已经看过

不是。
图导出来只是前半步，还要看 `../../../../reports/data_checks/manual_audit_notes.md` 的回填状态。

### 误解 2：这个脚本只服务内部流程，所以应该排除

这次不对。
当前计划明确需要正式 preview 资产和人工抽查证据，所以它属于 A 类。

### 误解 3：人工审稿记录是 B 类，所以这个脚本也该是 B 类

也不是。
这里要分清脚本和产物边界：
脚本是正式工程落点，`../../../../reports/data_checks/manual_audit_notes.md` 是它导出的正式检查资产。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事：

1. 打开 `../../../../tools/stage01_data_protocol/preview_dataset_samples.py`，确认 `AUDIT_TARGETS`
2. 打开 `../../../../reports/data_checks/manual_audit_notes.md`，确认 23 / 23 已覆盖且状态为 `pass`
3. 打开一组三联图，确认 raw、mask_bin、overlay 都存在

学完后你应该具备什么能力？

你应该能说清：

- 当前人工抽查资产是怎么按协议生成出来的
- 为什么 preview 证据不能只靠自动统计替代
- `../../../../reports/data_checks/manual_audit_notes.md` 在阶段总验收里到底扮演什么角色
