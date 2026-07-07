# tools_build_distance_targets.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/build_distance_targets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: shape-aware supervision and distance-map target preparation
- 公式/定义: distance target 需要从正式 mask 派生，并以数值 target 与 heatmap 双证据形式回链到具体样本

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/build_distance_targets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `distance_target_version`、`distance_type=euclidean`、`distance_norm=zero_one`

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/build_distance_targets.py`
- 符号: `pick_indices()` / `main()`

## 这个脚本的作用

这个脚本负责把 distance target 这条链真正落成可检查的正式证据。

它不是直接跑训练，也不是直接评估模型。
它做的是：从正式 split 里挑代表样本，导出 distance map 本体和 heatmap，让人能确认“距离监督这条链现在已经有真东西，不是口头说法”。

你可以把它理解成“distance target 抽查导出器”。
打个类比，它像把“离边界多远”这种抽象数值翻译成一张既能算、又能看的体温图。

## 这个脚本在整个阶段中的位置

```text
../../../../splits/**/*.csv
        ↓
../../../../tools/stage01_data_protocol/convert_masks.py
        ↓
../../../../tools/stage01_data_protocol/build_distance_targets.py
        ↓
../../../../reports/data_targets/distance/**
../../../../reports/data_checks/distance_target_report.md
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
```

它和 `../../../../tools/stage01_data_protocol/build_boundary_targets.py` 是平行关系。
但两者不是简单重复劳动，一个讲边界几何，一个讲像素到边界或前景的距离分布。

可以先反问一句：如果距离图最后是给训练用的，为什么数据阶段就要先导出来？
因为这一阶段要先确认“派生 target 协议有没有稳定落地”，而不是等到训练报错了再回头猜。

你现在可能会问：为什么不用等训练阶段顺手验证？
用人话说，`../../../../tools/stage01_data_protocol/convert_masks.py` 先把上游 mask 语言统一，这个脚本再把那套语言翻译成数值距离图和热力图证据，最后交给 `../../../../tools/stage01_data_protocol/validate_data_assets.py` 做总裁决。
这里的取舍也很直接：如果等训练阶段再看，排错会混进模型和 loss；如果现在先把 target 证据单独导出来，问题会更容易定位。
为什么不用别的设计，例如只留 heatmap 不留数值文件？因为人眼能看懂热力图，但只有 `npy` 才能保住正式数值 target 的可回用性。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 数据阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

## 当前实现状态

- 当前状态: `已实现`
- 当前是否首次正式可用: `yes`
- 当前真实结果:
  - `distance_target_version: distance_target_v1`
  - `distance_type: euclidean`
  - `distance_norm: zero_one`
  - `exported_sample_count: 14`
  - `pass_distance_target: True`
- 当前物理证据:
  - `../../../../reports/data_checks/distance_target_report.md`
  - `../../../../reports/data_targets/distance/glas/train68/GlaS_official_train_train_1__distmap.npy`
  - `../../../../reports/data_targets/distance/glas/train68/GlaS_official_train_train_1__distance_heatmap.png`
  - `../../../../reports/data_targets/distance/crag/test40/CRAG_test_test_9__distmap.npy`

## 脚本核心逻辑

### 主要流程

这个脚本现在可以拆成 5 步：

1. 读取正式 config 和 split CSV
2. 为每个 split 选代表样本
3. 读取 mask 并做二值化
4. 用欧氏距离变换生成归一化 distance map
5. 写出 `__distmap.npy`、`__distance_heatmap.png` 和 `../../../../reports/data_checks/distance_target_report.md`

### 关键点 1：它同时保留数值证据和可视证据

这里不是只导图片。
脚本同时导出：

- `__distmap.npy`
- `__distance_heatmap.png`

为什么两者都要？
因为 heatmap 让人能快速看懂，`npy` 则保证这不是“只给人看的截图”，而是真正可回用的数值 target 证据。

### 关键点 2：`distance_max = 1.000000` 是归一化通过的直接信号

`../../../../reports/data_checks/distance_target_report.md` 里最值得盯住的字段之一，就是每个导出样本的 `distance_max`。

当前真实结果里，这些代表样本的 `distance_max` 都是 `1.000000`。
这说明距离图已经被归一化到协议要求的范围。

### 关键点 3：它跟 split 血统一起保存

distance target 不是脱离 split 单独导出的。
它落在：

- `reports/data_targets/distance/glas/train68/**`
- `reports/data_targets/distance/crag/test40/**`

这种目录组织下。

这件事很重要，因为它保证了下游看到 target 证据时，能直接知道它属于哪个正式 split。
取舍也很现实：如果只留一份总表，读者得自己反推样本属于哪个 split；如果把目录血统保留下来，解释成本会低很多。

## 为什么这样设计

最常见的误解是：
“既然训练阶段才真正用 distance target，现在这一步导出它是不是太早了？”

不是。
当前阶段要解决的不是“模型用不用”，而是“输入层和派生 target 协议是否已经有正式证据”。

这里的取舍是：

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 等训练阶段再看 distance target | 工作量后移 | 当前阶段无法证明派生 target 协议成立 | 否决 |
| 当前就全量导出所有 distance target | 看起来完整 | 资产太重，超出当前阶段目标 | 否决 |
| 当前导出代表样本 distance 证据 | 够检查、够解释 | 不是全量资产 | 采用 |

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/build_distance_targets.py --num-per-split 2 --output-root reports/data_targets/distance --report-output reports/data_checks/distance_target_report.md
```

运行成功后，至少应得到：

1. `../../../../reports/data_checks/distance_target_report.md`
2. `../../../../reports/data_targets/distance/glas/train68/GlaS_official_train_train_1__distmap.npy`
3. `../../../../reports/data_targets/distance/glas/train68/GlaS_official_train_train_1__distance_heatmap.png`
4. `../../../../reports/data_targets/distance/crag/test40/CRAG_test_test_9__distmap.npy`

## 如何验证脚本运行结果

### 验证点 1：导出数量和总状态是否正确

检查方法：

1. 打开 `../../../../reports/data_checks/distance_target_report.md`
2. 看 `exported_sample_count` 和 `pass_distance_target`

通过标准：

- `exported_sample_count = 14`
- `pass_distance_target = True`

### 验证点 2：distance map 是否真的归一化

检查方法：

1. 继续看 `../../../../reports/data_checks/distance_target_report.md` 的样本表
2. 查看 `distance_max`

通过标准：

- 当前代表样本的 `distance_max` 显式写成 `1.000000`

### 验证点 3：目录结构是否仍然挂在正式 split 下

检查方法：

1. 打开 `../../../../reports/data_targets/distance/`
2. 看子目录结构

通过标准：

- 能看到 `../../../../reports/data_targets/distance/glas/train68/`、`../../../../reports/data_targets/distance/glas/val17/`、`../../../../reports/data_targets/distance/glas/testA60/`、`../../../../reports/data_targets/distance/glas/testB20/`
- 能看到 `../../../../reports/data_targets/distance/crag/train153/`、`../../../../reports/data_targets/distance/crag/val20/`、`../../../../reports/data_targets/distance/crag/test40/`

## 与项目其他部分的关联

这个脚本直接影响：

- `../../../../src/data/distance_targets.py`
- `../../../../tools/stage01_data_protocol/convert_masks.py`
- `../../../../reports/data_checks/distance_target_report.md`
- `../../../../reports/data_targets/distance/**`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

## 容易误解的地方

### 误解 1：distance heatmap 就是训练真正消费的 target

不是。
heatmap 是给人看的解释证据，不是训练时的唯一正式输入格式。

### 误解 2：有 `pass_distance_target=True` 就等于训练已验证

不对。
这只说明 distance target 协议链有证据，不说明模型已消费它。

### 误解 3：它和 boundary target 完全重复

也不是。
两者都源自 mask，但表达的是不同监督语义。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事：

1. 打开 `../../../../tools/stage01_data_protocol/build_distance_targets.py`，确认它会同时导出 `npy` 和 heatmap
2. 打开 `../../../../reports/data_checks/distance_target_report.md`，确认 `exported_sample_count = 14`
3. 抽看一行样本，确认 `distance_max = 1.000000`

学完后你应该具备什么能力？

你应该能说清：

- distance target 证据是怎么从正式 split 样本导出来的
- 为什么这里要同时保留数值文件和 heatmap
- 它和阶段总验收之间是什么关系
