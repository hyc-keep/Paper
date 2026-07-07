# tools_convert_masks.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/convert_masks.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: benchmark ground-truth handling and binary foreground protocol
- 公式/定义: 正式数据链不能把 mask 语义留在“默认大家都懂”的口头约定里，必须明确前景判定、磁盘值范围和 resize 规则

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/convert_masks.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `mask_rule_version`、`mask_positive_rule`、`mask_disk_value_rule`、`input_size=512x512`

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/convert_masks.py`
- 符号: `parse_args()` / `safe_relpath()` / `main()`

## 这个脚本的作用

这个脚本负责把“当前项目到底认什么样的 mask 协议”压成正式检查结果。

它不是简单把原始 mask 改写一遍，也不是生成另一套训练资产。
它真正做的事情，是沿着已经冻结的 split CSV，把 GlaS 和 CRAG 的全部正式样本重新过一遍，确认：

- 正前景规则是不是 `mask_gt_0`
- 导出的二值语义是不是稳定
- 当前标签协议有没有漂出 `01_数据协议` 的冻结边界

用人话说，它就是“binary mask 协议总检查器”。
打个类比，它更像标签入库前的总质检员，而不是后厨里顺手做二值化的小工具。

## 这个脚本在整个阶段中的位置

当前标签协议链可以先记成这条线：

```text
../../../../configs/data/glas.yaml
../../../../configs/data/crag.yaml
        ↓
../../../../splits/**/*.csv
        ↓
../../../../tools/stage01_data_protocol/convert_masks.py
        ↓
../../../../reports/data_checks/binary_mask_summary.csv
../../../../reports/data_checks/label_protocol_report.md
        ↓
../../../../tools/stage01_data_protocol/build_boundary_targets.py
../../../../tools/stage01_data_protocol/build_distance_targets.py
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
```

它的上游是正式 config 和正式 split，它像装配线前面的入厂质检口。
先别急着往训练那边想，当前阶段真正要先回答的问题是：这些 mask 到底是不是同一种二值语义；如果这个问题没钉住，后面所有 boundary、distance 和 preflight 讨论都会飘。

所以它的下游不是训练器，而是 `../../../../tools/stage01_data_protocol/build_boundary_targets.py`、`../../../../tools/stage01_data_protocol/build_distance_targets.py` 和 `../../../../tools/stage01_data_protocol/validate_data_assets.py`。
白话一点说，这一步是在给整条数据协议链“定字典”，后面的脚本都默认沿这本字典说话。

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
  - `total_samples_checked: 378`
  - `invalid_binary_masks: 0`
  - `pass_binary_mask: True`
  - `pass_dtype: True`
  - `pass_resize_rule: True`
- 当前物理证据:
  - `../../../../reports/data_checks/binary_mask_summary.csv`
  - `../../../../reports/data_checks/label_protocol_report.md`

这里最重要的不是“脚本跑没跑”，而是它已经把 `378` 个正式样本全部压成了统一标签协议结论。

## 脚本核心逻辑

### 主要流程

这个脚本当前可以拆成 5 步：

1. 读取 `configs/data/glas.yaml` 和 `configs/data/crag.yaml`
2. 顺着 `splits/**/*.csv` 逐行找到全部正式 mask
3. 用 `load_mask_array()` 和 `binarize_mask_gt_zero()` 做二值化
4. 记录每个样本的原始值域、二值结果和前景像素数
5. 写出 `../../../../reports/data_checks/binary_mask_summary.csv` 与 `../../../../reports/data_checks/label_protocol_report.md`

### 关键点 1：它以 split CSV 为唯一入口

这很关键。
它不是直接扫 `datasets/` 目录，而是只检查已经进入正式 split 的样本。

这样做的意义是：
标签协议检查和正式交付对象边界保持一致，不会把计划外样本混进阶段结论。

### 关键点 2：它检查的是“规则是否稳定”，不是“文件是否存在”

`../../../../reports/data_checks/label_protocol_report.md` 里真正值得盯住的字段有：

- `mask_positive_rule = mask_gt_0`
- `mask_disk_value_rule = 0_255`
- `input_size = 512x512`
- `invalid_binary_masks = 0`

这组字段合起来，才是在证明当前标签协议没有漂。

### 关键点 3：它给下游 target 生成链定了输入语义

`../../../../tools/stage01_data_protocol/build_boundary_targets.py` 和 `../../../../tools/stage01_data_protocol/build_distance_targets.py` 都默认上游二值 mask 语义已经成立。

如果这里不先把 binary mask 协议钉住，后面的 boundary/distance 只是“基于某种默认假设生成的 target”，不是正式协议资产。

## 为什么这样设计

最容易出现的误解是：
“既然 `src/data/mask_ops.py` 已经定义了二值化函数，为什么还要单独保留一个工具脚本？”

答案很直接：代码里有函数，不等于阶段里已经有正式证据。
你可以把模块函数理解成“会做这件事的能力”，而这个脚本负责把“这件事已经按当前协议做过并且结果稳定”真正落盘。
你可能会问，既然下游脚本迟早也会读 mask，为什么不让它们顺手检查？因为那样最后只能得到“某处好像不对”，却很难保留一份单独可归档、可复跑、可追责的标签协议结论。

这里的取舍是：

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 只保留 `src/data/mask_ops.py` | 代码更少 | 没有阶段级检查证据 | 否决 |
| 直接全量改写原始 mask | 看起来直接 | 容易污染原始资产边界 | 否决 |
| 用独立工具脚本输出协议检查资产 | 有正式证据、可回查 | 多一份报告 | 采用 |

## 如何运行这个脚本

这里别把它想成一次性的演示命令。它更像一张协议复核单，通常会在数据协议收尾、target 生成前、或者怀疑标签语义漂移时重新跑一遍。
如果你在问“为什么不把这步塞进别的脚本顺手完成”，取舍点就在于可追责性: 单独脚本会多一道执行动作，但换来一份可单查、可单独复跑的正式证据。

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/convert_masks.py --summary-output reports/data_checks/binary_mask_summary.csv --report-output reports/data_checks/label_protocol_report.md
```

运行成功后，至少应得到：

1. `../../../../reports/data_checks/binary_mask_summary.csv`
2. `../../../../reports/data_checks/label_protocol_report.md`

## 如何验证脚本运行结果

### 验证点 1：总样本数是否覆盖正式 split

检查方法：

1. 打开 `../../../../reports/data_checks/label_protocol_report.md`
2. 查看 `total_samples_checked`

通过标准：

- 当前真实值是 `378`
- 和 GlaS/CRAG 全部正式 split 样本总数一致

### 验证点 2：二值协议是否真正通过

检查方法：

1. 继续看 `../../../../reports/data_checks/label_protocol_report.md`
2. 查看 `invalid_binary_masks`、`pass_binary_mask`、`pass_dtype`、`pass_resize_rule`

通过标准：

- `invalid_binary_masks = 0`
- 三个 pass 字段都为 `True`

### 验证点 3：样本级摘要是否真实落盘

检查方法：

1. 打开 `../../../../reports/data_checks/binary_mask_summary.csv`
2. 抽查几行 `binary_unique_values` 与 `binary_positive_pixels`

通过标准：

- `binary_unique_values` 只出现合法二值集合
- `binary_positive_pixels` 不是整列空壳值

## 与项目其他部分的关联

这个脚本直接影响：

- `../../../../src/data/mask_ops.py`
- `../../../../tools/stage01_data_protocol/build_boundary_targets.py`
- `../../../../tools/stage01_data_protocol/build_distance_targets.py`
- `../../../../reports/data_checks/label_protocol_report.md`
- `../../../../reports/data_checks/binary_mask_summary.csv`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

换句话说，它决定了“后续 target 生成到底是在什么标签协议上工作”。

## 容易误解的地方

### 误解 1：它会改写正式训练 mask

不是。
它当前做的是检查和摘要，不是批量覆盖原始数据。

### 误解 2：有标签协议报告就等于 target 也已经通过

也不是。
binary mask 协议通过，只说明 boundary/distance 的输入语义已稳定。

### 误解 3：这个脚本只是 CSV 统计器

不对。
它实际上在给整个标签协议链提供正式放行证据。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事：

1. 打开 `../../../../tools/stage01_data_protocol/convert_masks.py`，确认它是沿 `splits/**/*.csv` 做检查
2. 打开 `../../../../reports/data_checks/label_protocol_report.md`，确认 `total_samples_checked = 378`
3. 打开 `../../../../reports/data_checks/binary_mask_summary.csv`，确认存在样本级 `binary_unique_values`

学完后你应该具备什么能力？

你应该能说清：

- 当前项目到底认什么样的 binary mask 协议
- 为什么这个协议必须有独立正式检查证据
- 它和 boundary/distance target 链是什么关系
