# src_data_boundary_targets.py.md

## 这个文件的作用

- 这个文件负责从正式二值 mask 派生边界带目标
- 你可以把它理解成 `05_标签转换与可视化规则.md` 里 `boundary_target_version` 的最小工程实现

它不重新定义主标签，也不碰训练 loss。
它只回答一件事：当前项目到底如何从已经冻结的 `{0,1}` 语义 mask 稳定长出一张可交付、可复算的 boundary target。

如果这里的规则漂了，后面的 boundary 预览、边界监督和数据阶段验收就会一起漂。

## 结构化溯源卡片

- 正式对象: `src/data/boundary_targets.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Deep Contour-Aware Networks for Accurate Gland Segmentation`
- 章节: `gland contour supervision`
- 公式/定义: `边界监督必须从 gland 区域边缘稳定派生，而不是临时手工描一圈`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `src/data/boundary_targets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `boundary_target_version`, `boundary_width`, `mask_positive_rule`

### 当前实现落点
- 文件: `src/data/boundary_targets.py`
- 符号: `build_boundary_band()`

## 这个文件在整个阶段中的位置

当前派生标签链路里，它的位置是：

1. `src/data/mask_ops.py` 先产出正式二值 mask
2. 当前文件再从二值 mask 派生边界带
3. 后续的 boundary 预览、数据资产检查和 `06_Boundary` 阶段继续消费这张图

换句话说，`boundary_targets.py` 不是主标签入口，而是主标签之后的第一层派生目标。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `可直接被边界目标导出工具和预览工具调用`
- 测试覆盖: `当前阶段已有正式协议回链，但说明文刚在本轮补上`

这里代码很薄是合理的。
数据阶段需要的不是一套复杂 contour 框架，而是一条唯一、可复算、不会偷偷分叉的 boundary 生成规则。

## 主要流程

### 1. 先校验边界宽度是不是正式允许值

`build_boundary_band(binary_mask, width=3)` 一上来先卡：

- 只允许 `3`
- 或 `5`

这直接对应当前协议里“首轮默认 `3 px`，唯一备选 `5 px`”的冻结边界。
如果有人在别处随手改成 `7`，这里会直接报错，而不是默默生成另一套资产。

### 2. 把二值 mask 转成可做形态学操作的灰度图

函数内部先把 `binary_mask > 0` 压成 `0/255` 的 `L` 图像。

这么做不是在重定义标签，而是在借 `PIL` 的滤波器做稳定的最大值/最小值形态学近似。

### 3. 用膨胀和腐蚀拿到边界带

核心操作是：

- `MaxFilter(size=width)` 近似膨胀
- `MinFilter(size=width)` 近似腐蚀
- 再比较 `dilated > eroded`

用人话说，就是把腺体区域先向外撑一下、再向里收一下，中间那层变化区当成边界候选。

### 4. 再和前景区域做一次相交

最终返回值是：

- `(dilated > eroded)`
- 并且 `binary_mask > 0`

第二个条件很关键。
它把边界带限制在当前前景内部，避免把背景侧也一起涂成边界监督区域。

## 关键函数说明

### `build_boundary_band(binary_mask, width=3)`

- 作用: 从正式二值 mask 生成固定宽度的边界带
- 输入: `{0,1}` 二值 mask 与边界宽度
- 输出: `{0,1}` 边界带数组
- 核心逻辑: 形态学膨胀/腐蚀差异 + 前景约束

这个函数其实就把当前 boundary 协议收成了三条硬规则：

1. 源头必须是正式二值 mask
2. 宽度只能是正式允许值
3. 输出必须继续是离散边界标签

## 代码里的真实协议痕迹

当前代码里最值得盯住的协议点有四个：

1. `width not in {3, 5}`
2. `(binary_mask > 0)`
3. `ImageFilter.MaxFilter(size=width)`
4. `((dilated > eroded) & (binary_mask > 0)).astype(np.uint8)`

它们分别对应：

- 冻结宽度集合
- 唯一前景来源
- 形态学膨胀
- 最终边界带的离散化与前景约束

## 为什么这样设计，而不是别的设计

### 取舍 1: 为什么边界图必须从正式二值 mask 派生

因为当前路线要求所有派生标签都继承同一主标签口径。
如果 boundary 在别处自己从原始 mask 或别的预处理结果再算一遍，就等于偷偷开了第二条标签主线。

### 取舍 2: 为什么只允许 `3` 和 `5`

因为当前数据协议不是开放试验场。
这里要先把资产版本冻结住，让后续阶段讨论的是“边界监督有没有用”，而不是“是不是 width 又换了一版”。

### 取舍 3: 为什么要和 `binary_mask > 0` 再做一次相交

因为单纯看膨胀/腐蚀差异，容易把边缘变化扩到背景侧。
当前版本要的是 gland 边缘监督，不是整条背景-前景分界外扩成一大片模糊区域。

## 如何验证这份代码没跑偏

### 验证 1: 看宽度冻结有没有被写死

1. 打开 `src/data/boundary_targets.py`
2. 找 `if width not in {3, 5}`

通过标准：

- 没有更宽的默认集合
- 非法宽度会直接报错

### 验证 2: 看源头是不是仍然只认正式二值 mask

1. 看函数开头是否统一用了 `binary_mask > 0`
2. 看返回值是否仍然和 `binary_mask > 0` 做相交

通过标准：

- 没有第二份主标签来源
- 边界带仍绑定当前前景语义

### 验证 3: 回看阶段协议是否一致

1. 打开 `05_标签转换与可视化规则.md`
2. 搜 `boundary_width`
3. 搜 `boundary_target_version`

通过标准：

- 代码和协议都只认 `3/5`
- boundary target 被明确定义为正式派生资产

## 最容易误解的地方

### 误区 1

“边界图不就是把 mask 描边吗，随便做都差不多。”

不对。
边界图是监督目标，不是装饰线。
只要来源、宽度或前景约束变了，下游监督的物理意义就已经变了。

### 误区 2

“既然以后还会做 Boundary Head，现在数据阶段先随便出一版也没关系。”

也不对。
正因为后面还要做 Boundary Head，数据阶段才更要把基础资产版本锁死。
不然你后面比较到的，可能不是 head 的差异，而是边界目标定义本身的差异。

## 读完后下一步看什么

建议接着读：

1. `src_data_mask_ops.py.md`
2. `src_data_distance_targets.py.md`
3. 后续要补的 `tools_build_boundary_targets.py.md`

这样能把“主标签 -> 边界派生 -> 工具导出”连成一条线。
