# src_data_distance_targets.py.md

## 这个文件的作用

- 这个文件负责从正式二值 mask 生成 Euclidean distance transform，并把结果归一化到 `[0,1]`
- 你可以把它理解成 `05_标签转换与可视化规则.md` 里 `distance_target_version=distance_target_v1` 的核心实现

它不是训练 loss，也不是 signed distance map 实验场。
它只负责把当前项目已经锁定的距离目标协议稳稳落成一份正式可交付资产。

## 结构化溯源卡片

- 正式对象: `src/data/distance_targets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Distance Map Loss Penalty Term for Semantic Segmentation`
- 章节: `distance-transform supervision`
- 公式/定义: `距离监督应从前景/边界几何关系稳定派生，而不是和主标签脱钩`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `src/data/distance_targets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `distance_target_version`, `distance_type`, `distance_norm`

### 当前实现落点
- 文件: `src/data/distance_targets.py`
- 符号: `_edt_1d()`, `euclidean_distance_transform()`, `normalize_distance_map()`

## 这个文件在整个阶段中的位置

它在数据协议里的位置是：

1. `src/data/mask_ops.py` 先生成正式二值 mask
2. 当前文件从二值 mask 生成距离图
3. 下游的距离目标导出工具、预览资产和 `07_Distance` 阶段继续消费这张图

所以它和 `boundary_targets.py` 一样，都属于“主标签之后的派生层”，不是主标签入口。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `可直接被距离目标导出工具调用`
- 测试覆盖: `当前阶段已有正式协议绑定，说明文在本轮补齐`

这份实现的重点不是功能堆得多，而是口径收得住。
当前协议已经明确说了：只认 Euclidean，先做无符号版本，再归一化到 `[0,1]`。

## 主要流程

### 1. 用一维 EDT 做基础积木

`_edt_1d(values)` 是一个一维 squared distance transform。

它的职责很纯：

- 输入一维代价数组
- 输出每个位置到最近零值点的平方距离

这里先算平方距离，是经典做法，后面在二维组合完成后再统一开平方。

### 2. 把二维 mask 拆成按行、按列两轮 EDT

`euclidean_distance_transform(binary_mask)` 的步骤是：

1. 先取 `foreground = binary_mask > 0`
2. 构造一张代价网格：前景点先设成大值，背景点设成 `0`
3. 逐行跑一轮 `_edt_1d`
4. 再逐列跑一轮 `_edt_1d`
5. 最后整体 `sqrt`

用人话说，就是把“到最近背景点的欧氏距离”拆成两轮一维问题来算。

这也正说明当前版本认的是 Euclidean distance transform，不是 Manhattan，也不是 signed distance。

### 3. 再做一次 `[0,1]` 归一化

`normalize_distance_map(distance_map)` 的逻辑很直接：

- 先找全图最大值
- 如果最大值小于等于 `0`，就直接转成 `float32`
- 否则用 `distance_map / maximum`

这一步对应协议里锁死的 `distance_norm=zero_one`。

它的目的不是把数值“变好看”，而是让不同样本生成的距离图保持同一尺度口径，方便下游稳定消费。

## 关键函数说明

### `_edt_1d(values)`

- 作用: 计算一维平方距离变换
- 输入: 一维 `np.ndarray`
- 输出: 一维 `float64` 距离数组
- 核心逻辑: 下包络形式的动态推进

它虽然是内部函数，但其实是整份距离协议最核心的数值基础。

### `euclidean_distance_transform(binary_mask)`

- 作用: 计算二值 mask 的二维欧氏距离变换
- 输入: `{0,1}` 二值 mask
- 输出: `float64` 距离图
- 核心逻辑: 行列两轮 EDT + 开平方

当前这一步明确只认 Euclidean。
如果以后要做 signed distance map，应该在新版本里单独开口子，而不是偷偷改这里。

### `normalize_distance_map(distance_map)`

- 作用: 把距离图归一化到 `[0,1]`
- 输入: 距离图
- 输出: `float32` 归一化结果
- 核心逻辑: 除以全图最大值

它直接对应当前阶段协议里的 `distance_norm: zero_one`。

## 代码里的真实协议痕迹

最关键的协议点有四个：

1. `foreground = binary_mask > 0`
2. `grid = np.where(foreground, inf, 0.0)`
3. `return np.sqrt(grid, dtype=np.float64)`
4. `return (distance_map / maximum).astype(np.float32)`

它们分别对应：

- 正式主标签来源
- 到最近背景/边界的代价初始化
- Euclidean 距离定义
- `[0,1]` 归一化口径

## 为什么这样设计，而不是别的设计

### 取舍 1: 为什么当前只做 Euclidean

因为当前协议的目标是先给后续 distance supervision 提供唯一、可解释、可复现的第一版正式资产。
Euclidean 最直接，也最容易和当前文档、预览和验收链保持一致。

### 取舍 2: 为什么不直接做 signed distance map

因为当前阶段已经明确把 signed distance map 列成相邻方案，而不是主线正式协议。
现在如果直接塞进去，就会把“距离目标是否有效”和“距离定义是不是换了”混到一起。

### 取舍 3: 为什么要统一归一化到 `[0,1]`

因为不同样本、不同腺体大小下的原始距离范围会差很多。
如果不归一化，下游看到的是一堆量纲不统一的 target，训练和可视化都更难稳定解释。

## 如何验证这份代码没跑偏

### 验证 1: 看是不是仍然只认 Euclidean

1. 打开 `src/data/distance_targets.py`
2. 找 `np.sqrt(grid, dtype=np.float64)`

通过标准：

- 最终距离不是 L1
- 没有 signed distance 的正负分支

### 验证 2: 看归一化口径有没有被写死

1. 找 `normalize_distance_map()`
2. 确认是除以 `maximum`
3. 确认输出是 `float32`

通过标准：

- 数值口径对应 `zero_one`
- 输出类型稳定

### 验证 3: 回看阶段协议是否对齐

1. 打开 `05_标签转换与可视化规则.md`
2. 搜 `distance_type=euclidean`
3. 搜 `distance_norm=zero_one`

通过标准：

- 文档和代码是一条线

## 最容易误解的地方

### 误区 1

“距离图就是随便算个 heatmap，反正后面还能调。”

不对。
一旦它进入正式资产链，它就不再是随便试试的热力图，而是下游阶段会继承的正式 supervision target。

### 误区 2

“既然要做距离监督，直接上 signed distance 更先进。”

这个判断放在研究阶段可以讨论，但当前数据协议阶段不成立。
当前阶段要先锁唯一主线，而不是把多个相邻方案揉进一份正式资产里。

## 读完后下一步看什么

建议接着读：

1. `src_data_mask_ops.py.md`
2. `src_data_boundary_targets.py.md`
3. 后续要补的 `tools_build_distance_targets.py.md`

这样更容易把“主标签 -> 边界目标 -> 距离目标”看成同一条派生链，而不是三份散开的脚本说明。
