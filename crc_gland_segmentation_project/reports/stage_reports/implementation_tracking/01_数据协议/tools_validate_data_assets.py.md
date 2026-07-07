# tools_validate_data_assets.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: benchmark data integrity and evaluation preconditions
- 公式/定义: 阶段放行不能只看是否有文件，还要看 split / check / preview / label / handoff 是否同时闭环

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `handoff_ready`、`assets_traceable`、`protocol_explainable`、`data_stage_pass`、`preflight_pass`

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- 符号: `inspect_check_assets()` / `inspect_preview_assets()` / `inspect_label_assets()` / `inspect_training_preflight()` / `build_acceptance_report()` / `main()`

## 这个脚本的作用

这个脚本负责把 `01_数据协议` 最后要不要放行，压成一份正式、结构化、可复核的判断。

它不是在生成某一类单独资产，而是在回答一个更大的问题:

“现在这套正式数据资产、split、检查结果、预览结果和 preflight 入口，能不能一起交接给下一个阶段？”

你可以把它理解成“数据阶段总闸门”。

前面的脚本各自只解决一段:

- split 有没有生成
- check 结果有没有落盘
- label 目标有没有通过
- preview 图有没有导出
- 训练入口能不能认到正式样本

而 `../../../../tools/stage01_data_protocol/validate_data_assets.py` 做的，是把这些散点拼成一个统一裁决。

## 这个脚本在整个阶段中的位置

如果你只记一条链，记这个就够了:

```text
../../../../configs/data/*.yaml + ../../../../splits/*.csv + ../../../../reports/data_checks/* + ../../../../reports/data_preview/* + ../../../../scripts/train.py
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
        ↓
../../../../reports/data_checks/data_asset_validation_report.md
../../../../reports/stage_reports/asset_manifest.json
../../../../reports/stage_reports/data_stage_acceptance.md
        ↓
handoff_ready、data_stage_pass、preflight_pass
```

也就是说，它已经不只是“读一些报告再汇总”。
它会直接产出:

1. `reports/data_checks/data_asset_validation_report.md`
2. `reports/stage_reports/asset_manifest.json`
3. `reports/stage_reports/data_stage_acceptance.md`

这三份文件就是当前数据阶段交接的正式出口。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 数据阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 工程目录框架: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

这组回链真正解释的是:
为什么当前阶段需要一份“总校验脚本”，而不是只靠人工看几份 markdown 报告下结论。

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `pass_pair: True`
  - `pass_label: True`
  - `pass_check: True`
  - `pass_preview: True`
  - `pass_config: True`
  - `pass_source: True`
  - `handoff_ready: True`
  - `assets_traceable: True`
  - `protocol_explainable: True`
  - `data_stage_pass: True`
  - `preflight_pass: True`
  - `next_action: enter_02_unet`

这些结果不是口头总结，而是已经落在:

- `../../../../reports/data_checks/data_asset_validation_report.md`
- `../../../../reports/stage_reports/asset_manifest.json`
- `../../../../reports/stage_reports/data_stage_acceptance.md`

## 脚本核心逻辑

### 主要流程

这个脚本现在可以拆成 7 步:

1. 对 GlaS / CRAG 两份正式 config 做 split 存在性检查
2. 检查 `reports/data_checks/*` 里的配对、重复、前景、人工审阅结果
3. 检查标签协议和 boundary / distance target 报告
4. 检查 `reports/data_preview/*` 是否达到最小预览数量
5. 检查 `configs/data/*.yaml` 和 `datasets/*.md` 是否存在
6. 检查 `scripts/train.py` 的 preflight 入口是否可接入
7. 把所有结果压成 manifest、validation report 和 acceptance report

### 关键函数 1: `validate_dataset()`

这个函数负责验证单个数据集配置是否闭环。

它会读取:

- `configs/data/glas.yaml`
- `configs/data/crag.yaml`

然后检查:

- `dataset_root` 是否存在
- 各 split CSV 是否存在
- 每个 split 的 `row_count` 是多少

当前真实结果已经写得很明确:

- GlaS split 行数: 68 / 17 / 60 / 20
- CRAG split 行数: 153 / 20 / 40

这一步回答的是“正式数据根和 split 资产有没有真正落地”。

### 关键函数 2: `inspect_check_assets()`

这个函数负责读检查类产物。

它不会只看文件在不在，还会去读 markdown 里的字段，例如:

- `pair_check_pass`
- `readable_check_pass`
- `foreground_check_pass`
- `duplicate_check_status`
- `manual_audit_coverage_status`

为什么这一步重要？
因为只看 `reports/data_checks/*.md` 文件存在，是会被“空壳报告”骗过去的。

### 关键函数 3: `inspect_preview_assets()`

这个函数负责查 `reports/data_preview/*` 的图片数量。

当前它要求每个 split 目录里至少有:

- `raw`
- `mask_bin`
- `overlay`

三类图，而且每类至少达到最小张数。

从 `asset_manifest.json` 可以直接看到当前真实结果:

- GlaS train68: raw / mask_bin / overlay = 5 / 5 / 5
- GlaS val17: raw / mask_bin / overlay = 3 / 3 / 3
- GlaS testA60: raw / mask_bin / overlay = 2 / 2 / 2
- GlaS testB20: raw / mask_bin / overlay = 2 / 2 / 2
- CRAG train153: raw / mask_bin / overlay = 5 / 5 / 5
- CRAG val20: raw / mask_bin / overlay = 3 / 3 / 3
- CRAG test40: raw / mask_bin / overlay = 3 / 3 / 3

### 关键函数 4: `inspect_label_assets()`

这个函数负责检查标签协议链。

它看的是:

- `../../../../reports/data_checks/label_protocol_report.md`
- `../../../../reports/data_checks/binary_mask_summary.csv`
- `../../../../reports/data_checks/boundary_target_report.md`
- `../../../../reports/data_checks/distance_target_report.md`

并从里面读出:

- `pass_binary_mask`
- `pass_dtype`
- `pass_resize_rule`
- `pass_boundary_target`
- `pass_distance_target`

说白了，它在防止一种很常见的假通过:
表面上 target 文件都在，但实际没有人证明规则正确。

### 关键函数 5: `inspect_training_preflight()`

这个函数把数据阶段和训练入口接起来。

它检查的不是完整训练，而是:

- `scripts/train.py` 是否存在
- `data_stage_pass` 是否为真
- `handoff_ready` 是否为真

然后产出:

- `preflight_pass`
- `blockers`

当前真实结果是:

- `preflight_pass = True`
- `next_action = enter_02_unet`

这一步很关键，因为它把“阶段验收”从纸面状态推进到了“下游真的能接”。

### 关键函数 6: `build_acceptance_report()`

这个函数把最终结论写成 `../../../../reports/stage_reports/data_stage_acceptance.md`。

它会把下面这些字段正式落盘:

- `pass_source`
- `pass_split`
- `pass_pair`
- `pass_label`
- `pass_check`
- `pass_preview`
- `pass_handoff`
- `data_stage_pass`
- `handoff_ready`
- `preflight_pass`
- `next_action`

你可以把它理解成“正式验收口径的印章机”。

## 为什么这样设计

最容易被问的一句是:
“既然前面的报告都已经各自写好了，为什么还要再来一个 `../../../../tools/stage01_data_protocol/validate_data_assets.py`？”

原因很简单:
前面的报告回答的是局部真相，这个脚本回答的是全局裁决。

设计取舍可以概括成:

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 人工打开所有报告自己判断 | 不用再写代码 | 容易漏字段，也不稳定 | 否决 |
| 只看某一份 gate 报告 | 简单 | 无法保证 split、preview、label、preflight 同时成立 | 否决 |
| 用总校验脚本统一汇总并生成正式输出 | 可重复、可审计、可回退 | 代码更长 | 采用 |

所以这个脚本本质上不是“多余的一层”，而是阶段交接的统一裁决器。

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/validate_data_assets.py --dataset all --output reports/data_checks/data_asset_validation_report.md --acceptance-output reports/stage_reports/data_stage_acceptance.md --asset-manifest-output reports/stage_reports/asset_manifest.json
```

运行成功后，应该至少得到:

1. `../../../../reports/data_checks/data_asset_validation_report.md`
2. `../../../../reports/stage_reports/data_stage_acceptance.md`
3. `../../../../reports/stage_reports/asset_manifest.json`

## 如何验证脚本运行结果

### 验证点 1: 全局门状态是否全部落盘

检查方法:

1. 打开 `../../../../reports/data_checks/data_asset_validation_report.md`
2. 找 `## data_stage_gates`

通过标准:

- `pass_pair = True`
- `pass_label = True`
- `pass_check = True`
- `pass_preview = True`
- `data_stage_pass = True`
- `preflight_pass = True`

### 验证点 2: 资产 manifest 是否和真实数量一致

检查方法:

1. 打开 `../../../../reports/stage_reports/asset_manifest.json`
2. 查看 `split_assets`
3. 查看 `preview_assets`

通过标准:

- split 行数分别是 68 / 17 / 60 / 20 / 153 / 20 / 40
- preview 数量和当前目录真实图片数量一致

### 验证点 3: 正式验收结果是否和总校验一致

检查方法:

1. 打开 `../../../../reports/stage_reports/data_stage_acceptance.md`
2. 查看 `data_stage_pass`、`handoff_ready`、`preflight_pass`

通过标准:

- 三个字段都与 validation report 一致
- `next_action = enter_02_unet`

### 验证点 4: preflight 是否真的接到了训练入口

检查方法:

1. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
2. 查看 `runtime_profile`
3. 再回到 `../../../../reports/stage_reports/data_stage_acceptance.md`

通过标准:

- runtime 报告里是 `data_protocol_preflight`
- 验收报告里是 `preflight_pass = True`

## 与项目其他部分的关联

这个脚本和下面这些对象是强耦合的:

- `../../../../configs/data/glas.yaml`
- `../../../../configs/data/crag.yaml`
- `../../../../splits/**/*.csv`
- `../../../../reports/data_checks/*`
- `../../../../reports/data_preview/*`
- `../../../../reports/stage_reports/data_stage_acceptance.md`
- `../../../../reports/stage_reports/asset_manifest.json`
- `../../../../scripts/train.py`

也就是说，它本身不生成图像或 mask，但它决定这些对象能不能被一起视为“当前阶段正式交付包”。

## 容易误解的地方

### 误解 1: 这个脚本只是把已有 markdown 再抄一遍

不是。
它会重新解析字段、计数和状态，再生成结构化输出。

### 误解 2: `data_stage_pass = True` 就说明后续训练也已经完成

不对。
这里的 `True` 只代表 `01_数据协议` 通过。
模型、loss、backward、optimizer 仍然属于 `02_UNet流程验证`。

### 误解 3: 只要 `asset_manifest.json` 在，阶段就算通过

也不是。
manifest 只是一个结构化快照，不是最终裁决本身。
真正的裁决还要看 `../../../../reports/stage_reports/data_stage_acceptance.md` 里的门状态。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事:

1. 打开 `../../../../reports/data_checks/data_asset_validation_report.md`，确认 `data_stage_pass = True`
2. 打开 `../../../../reports/stage_reports/asset_manifest.json`，确认 split 行数是 68 / 17 / 60 / 20 / 153 / 20 / 40
3. 打开 `../../../../reports/stage_reports/data_stage_acceptance.md`，确认 `next_action = enter_02_unet`

学完后你应该具备什么能力？

你应该能一眼分清:

- 哪些脚本是在生成局部资产
- 哪个脚本是在做全局裁决
- 为什么当前阶段已经能交接，但还没有进入完整训练链
