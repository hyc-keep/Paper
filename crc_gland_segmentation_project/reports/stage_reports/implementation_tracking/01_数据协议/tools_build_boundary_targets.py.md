# tools_build_boundary_targets.py.md

## 结构化溯源卡片

- 正式对象: `../../../../tools/stage01_data_protocol/build_boundary_targets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: contour-sensitive supervision and boundary-aware target preparation
- 公式/定义: boundary target 必须从正式二值 mask 派生，并且要能回到具体 split 样本做人工核对

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/build_boundary_targets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `boundary_target_version`、`boundary_width=3`、preview evidence coverage

### 当前实现落点
- 文件: `../../../../tools/stage01_data_protocol/build_boundary_targets.py`
- 符号: `pick_indices()` / `build_overlay()` / `main()`

## 这个脚本的作用

这个脚本负责导出“边界监督证据”。

注意，这里说的是证据，不是完整训练时会消费的全部 target 包。
它当前做的是：从正式 split 样本里抽代表样本，把 boundary target 和 overlay 图真正落盘，让人能检查 boundary 逻辑是不是贴在正确位置。

你可以把它理解成“boundary target 抽查导出器”。
打个类比，它像把抽象的边界监督规则洗成几张能直接贴在病例旁边看的胶片。

## 这个脚本在整个阶段中的位置

当前 boundary target 链可以简化成：

```text
../../../../splits/**/*.csv
        ↓
../../../../tools/stage01_data_protocol/convert_masks.py
        ↓
../../../../tools/stage01_data_protocol/build_boundary_targets.py
        ↓
../../../../reports/data_targets/boundary/**
../../../../reports/data_checks/boundary_target_report.md
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
```

它不负责决定正式 split，也不负责总放行。
它负责的是把 boundary target 这条子链讲成有物理证据的一段，而且这段证据得让人肉眼就能复核。

可以先问自己一句：如果只说“代码里能算 boundary”，为什么还要在当前阶段单独导图？
因为数据协议阶段要确认的不是抽象能力，而是当前冻结数据上，边界带是不是确实贴在目标轮廓附近。

你现在可能会问：为什么不用全量导出，反而只留代表样本？
用人话说，这个脚本像是在给后续监督信号拍 X 光片。
`../../../../tools/stage01_data_protocol/convert_masks.py` 先把上游二值语义钉住，这里再把 `../../../../src/data/boundary_targets.py` 的几何结果翻成 `../../../../reports/data_targets/boundary/**` 下能看见的证据，最后再由 `../../../../tools/stage01_data_protocol/validate_data_assets.py` 把它并入总放行。
这里还有个很实际的取舍：全量导出会更“全”，但资产会立刻膨胀；只保留代表样本，解释成本低，而且足够支撑当前阶段的人工复核。
为什么不用别的设计，例如把所有 target 都一口气塞进仓库？因为当前阶段要的是可复核证据，不是把仓库变成大体积样本仓。

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
  - `boundary_target_version: boundary_target_v1`
  - `boundary_width: 3`
  - `exported_sample_count: 14`
  - `pass_boundary_target: True`
- 当前物理证据:
  - `../../../../reports/data_checks/boundary_target_report.md`
  - `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_w3.png`
  - `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_overlay.png`
  - `../../../../reports/data_targets/boundary/crag/test40/CRAG_test_test_9__boundary_w3.png`

这里最值得看的不是“导出了多少张图”，而是这些图已经能把 boundary target 的几何位置讲成可复核证据。

## 脚本核心逻辑

### 主要流程

这个脚本现在的主流程可以拆成 6 步：

1. 读取 GlaS / CRAG 两份正式 config
2. 顺着正式 split CSV 取代表样本
3. 读取 raw image 和 mask
4. 用 `build_boundary_band(..., width=3)` 生成边界带
5. 导出 `__boundary_w3.png` 和 `__boundary_overlay.png`
6. 写出 `../../../../reports/data_checks/boundary_target_report.md`

### 关键点 1：它只抽代表样本，不全量导出

当前脚本不是在仓库里保存所有 boundary target。
它保存的是“足够解释规则是否成立”的代表样本证据。

当前真实输出数是 `14`，覆盖：

- GlaS 的 `../../../../reports/data_targets/boundary/glas/train68/`、`../../../../reports/data_targets/boundary/glas/val17/`、`../../../../reports/data_targets/boundary/glas/testA60/`、`../../../../reports/data_targets/boundary/glas/testB20/`
- CRAG 的 `../../../../reports/data_targets/boundary/crag/train153/`、`../../../../reports/data_targets/boundary/crag/val20/`、`../../../../reports/data_targets/boundary/crag/test40/`

如果你只想先看最硬的物理证据，直接开下面这几份就够了：

- `../../../../reports/data_checks/boundary_target_report.md`
- `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_w3.png`
- `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_overlay.png`
- `../../../../reports/data_targets/boundary/crag/test40/CRAG_test_test_9__boundary_w3.png`
- `../../../../reports/data_targets/boundary/crag/test40/CRAG_test_test_9__boundary_overlay.png`

这些文件路径就是当前最直接的物理证据路径。
如果要核对具体路径、目录组织和样本数，先看 `../../../../reports/data_checks/boundary_target_report.md` 的字段，再回到上面几张图逐个对照。

### 关键点 2：`boundary_width = 3` 是冻结协议的一部分

这不是随手写的魔法数。
它直接出现在 `../../../../reports/data_checks/boundary_target_report.md` 里，并且和当前 target 命名 `__boundary_w3.png` 对齐。

如果以后这里改成别的宽度，当前阶段的 target 解释就会整体漂掉。

### 关键点 3：overlay 图是为了让人工一眼看懂

只有二值边界图，不够。
人看 `__boundary_w3.png` 很容易只知道“导出来了”，但看不出它是不是贴在腺体轮廓上。

所以脚本还会导出 `__boundary_overlay.png`。
这一步是为了让人工终审能直接看见边界是否覆盖在目标边缘，而不是只看纯 target 图猜。

## 为什么这样设计

最容易被问的一句是：
“既然 `src/data/boundary_targets.py` 已经能算 boundary，为啥还要单独有这个工具？”

因为能算出来，不等于已经有正式证据。
这里有个很实际的取舍: 全量导出最“保险”，但仓库资产会立刻膨胀；完全不导出最“省事”，但人工又没法复核。
所以当前选的是中间方案，只导正式 split 的代表样本，让解释成本和证据强度保持平衡。

这里的取舍是：

| 方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 只留 `src/data/boundary_targets.py` | 模块更纯 | 没有落盘证据，人工无法复核 | 否决 |
| 全量导出全部 boundary target | 看起来最完整 | 资产膨胀，超出当前阶段需求 | 否决 |
| 只导出正式 split 的代表样本 target 证据 | 够解释、够复核 | 不是全量资产 | 采用 |

## 如何运行这个脚本

```bash
cd crc_gland_segmentation_project
python tools/stage01_data_protocol/build_boundary_targets.py --num-per-split 2 --output-root reports/data_targets/boundary --report-output reports/data_checks/boundary_target_report.md
```

运行成功后，至少应得到：

1. `../../../../reports/data_checks/boundary_target_report.md`
2. `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_w3.png`
3. `../../../../reports/data_targets/boundary/glas/train68/GlaS_official_train_train_1__boundary_overlay.png`
4. `../../../../reports/data_targets/boundary/crag/test40/CRAG_test_test_9__boundary_w3.png`

## 如何验证脚本运行结果

### 验证点 1：总导出数量是否正确

检查方法：

1. 打开 `../../../../reports/data_checks/boundary_target_report.md`
2. 查看 `exported_sample_count`

通过标准：

- 当前真实值是 `14`
- `pass_boundary_target = True`

### 验证点 2：导出样本是否覆盖主要 split

检查方法：

1. 继续看 `../../../../reports/data_checks/boundary_target_report.md` 的 `## Exported Samples`
2. 确认同时出现 GlaS 和 CRAG 的多个 split

通过标准：

- 至少覆盖 `../../../../reports/data_targets/boundary/glas/train68/`、`../../../../reports/data_targets/boundary/glas/val17/`、`../../../../reports/data_targets/boundary/glas/testA60/`、`../../../../reports/data_targets/boundary/glas/testB20/`、`../../../../reports/data_targets/boundary/crag/train153/`、`../../../../reports/data_targets/boundary/crag/val20/`、`../../../../reports/data_targets/boundary/crag/test40/`

### 验证点 3：overlay 是否真能辅助人工判断

检查方法：

1. 打开一对 `__boundary_w3.png` 和 `__boundary_overlay.png`
2. 对照 raw image 看边界高亮区域

通过标准：

- overlay 不是纯黑或纯白空壳
- 边界大体贴在腺体轮廓附近

## 与项目其他部分的关联

这个脚本直接影响：

- `../../../../src/data/boundary_targets.py`
- `../../../../tools/stage01_data_protocol/convert_masks.py`
- `../../../../reports/data_checks/boundary_target_report.md`
- `../../../../reports/data_targets/boundary/**`
- `../../../../tools/stage01_data_protocol/validate_data_assets.py`

也就是说，它是标签协议链和阶段总验收之间的一段正式证据桥梁。

## 容易误解的地方

### 误解 1：它导出的 14 个样本就是完整 boundary 训练资产

不是。
这 14 个是证据样本，不是全量训练 target 包。

### 误解 2：只要有 boundary 图就说明距离 target 也成立

不对。
boundary 和 distance 是两条平行证据链。

### 误解 3：这个脚本只是做可视化

也不是。
它实际上在把 boundary target 协议写成正式可验的落盘证据。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事：

1. 打开 `../../../../tools/stage01_data_protocol/build_boundary_targets.py`，确认 `build_boundary_band(..., width=3)`
2. 打开 `../../../../reports/data_checks/boundary_target_report.md`，确认 `exported_sample_count = 14`
3. 随机打开一张 `__boundary_overlay.png`，确认边界确实叠到了 raw image 上

学完后你应该具备什么能力？

你应该能说清：

- boundary target 证据是怎么从正式 split 样本导出来的
- 为什么当前阶段只导出代表样本而不是全量 target
- overlay 图在人工复核里到底起什么作用
