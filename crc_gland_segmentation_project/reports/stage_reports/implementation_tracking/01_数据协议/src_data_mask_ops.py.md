# src_data_mask_ops.py.md

## 这个文件的作用

- 这个文件负责把原始 mask 读成数组、按正式规则二值化、导出标准化 PNG，并在需要时做离散 resize
- 你可以把它理解成 `05_标签转换与可视化规则.md` 在工程代码里的最小执行落点

它不负责 split 划分，也不负责训练。
它只回答一件事：当前项目到底用什么方式把原始标注变成后续所有阶段都能继承的正式二值标签。

如果这里的口径漂了，后面的 `boundary_targets.py`、`distance_targets.py`、`preview_dataset_samples.py` 和训练入口就会吃到不同版本的标签。

## 结构化溯源卡片

- 正式对象: `src/data/mask_ops.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `benchmark masks and gland foreground definition`
- 公式/定义: `前景区域必须对应 gland mask 的稳定语义，而不是临时阈值猜测`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `src/data/mask_ops.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `mask_positive_rule`, `mask_interp`, `input_size`

### 当前实现落点
- 文件: `src/data/mask_ops.py`
- 符号: `load_mask_array()`, `binarize_mask_gt_zero()`, `export_binary_mask_png()`, `resize_binary_mask()`

## 这个文件在整个阶段中的位置

当前数据协议里，标签主链可以简化成下面这条：

1. `datasets/...` 里的原始 mask 文件
2. `load_mask_array()`
3. `binarize_mask_gt_zero()`
4. `export_binary_mask_png()` 或 `resize_binary_mask()`
5. 下游的 `boundary_targets.py`、`distance_targets.py`、预览导出和训练入口

用人话说，`mask_ops.py` 解决的是“正式标签长什么样”。
`csv_loader.py` 解决的是“样本表合法不合法”。
`datasets.py` 解决的是“配置和 split 怎么拼成样本列表”。

这三者不要混。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `可直接被数据阶段工具和下游数据装配逻辑调用`
- 测试覆盖: `已具备真实资产消费价值，但当前阶段说明文仍在继续补齐`

它现在代码量很小，但这不是问题。
这里本来就不该塞太多业务判断。
标签协议如果写得花，反而更容易让不同脚本偷偷走出不同分支。

## 主要流程

### 1. 先把磁盘上的 mask 读成单通道数组

`load_mask_array(mask_path)` 的动作很直接：

- 打开原始 mask
- 强制转成 `L` 单通道
- 返回 `uint8` 数组

这一步的重点不是“读图片”本身，而是把输入口径先压成统一形态。
否则上游如果混进 RGB mask、调色板 mask 或别的模式，下游就会在不知情的情况下继续跑。

### 2. 用唯一规则做二值化

`binarize_mask_gt_zero(mask_array)` 只保留一条规则：

- `mask > 0` 记为前景 `1`
- 其他都记为背景 `0`

这正是 `05_标签转换与可视化规则.md` 已经锁死的 `mask_positive_rule: mask_gt_0`。

这里没有给 `GlaS` 一套规则、`CRAG` 一套规则，也没有留“必要时手动调阈值”的口子。
这是故意的。
当前阶段要的不是灵活，而是唯一正式口径。

### 3. 把二值 mask 导出成可交付 PNG

`export_binary_mask_png(binary_mask, output_path)` 会：

- 自动创建输出目录
- 把 `{0,1}` 的数组映射成 `{0,255}`
- 以单通道 `L` 模式保存 PNG

这里一定要分清两层：

- 内存里的正式语义口径是 `{0,1}`
- 磁盘上的可视化/交付口径是 `{0,255}`

如果你把这两层混成一层，后面最容易出现的错就是：
训练前直接拿 `0/255` 的 `uint8` 去做 loss，或者导出 preview 时又以为磁盘文件里的值已经是训练张量口径。

### 4. resize 时只允许离散插值

`resize_binary_mask(binary_mask, size_hw)` 的核心点只有一个：

- `Image.Resampling.NEAREST`

说白了，mask 是离散标签，不是自然图像。
image 可以用连续插值，mask 不行。
如果这里偷用了双线性，边界会被软化，二值标签会在 resize 过程中被污染。

函数最后又做了一次 `> 0`，就是为了把 resize 后的结果重新压回 `{0,1}`。

## 关键函数说明

### `load_mask_array(mask_path)`

- 作用: 读取原始 mask，并统一成单通道 `uint8` 数组
- 输入: `mask_path`
- 输出: `np.ndarray`
- 核心逻辑: `Image.open(...).convert("L") -> np.uint8`

它的协议意义在于先消掉图像模式差异。
不然不同来源的 mask 会在最前面就分叉。

### `binarize_mask_gt_zero(mask_array)`

- 作用: 按正式前景规则生成二值 mask
- 输入: 原始灰度 mask
- 输出: `{0,1}` 的 `uint8` 数组
- 核心逻辑: `(mask_array > 0).astype(np.uint8)`

这个函数很短，但它其实就是当前标签协议最核心的工程锚点。

### `export_binary_mask_png(binary_mask, output_path)`

- 作用: 导出正式二值 mask 的磁盘口径文件
- 输入: `{0,1}` 数组与输出路径
- 输出: `*.png`
- 核心逻辑: 乘 `255` 后按 `L` 模式保存

这里解决的是“怎么留正式资产”，不是“怎么喂模型”。

### `resize_binary_mask(binary_mask, size_hw)`

- 作用: 用离散插值把二值 mask 调整到冻结尺寸
- 输入: 二值 mask 与 `(height, width)`
- 输出: resize 后仍保持 `{0,1}` 的数组
- 核心逻辑: 最近邻 resize + 再次二值化

它直接对应当前冻结表里的 `input_size` 和 `mask_interp: nearest`。

## 代码里的真实协议痕迹

这个文件里最值得盯住的协议痕迹有四个：

1. `convert("L")`
2. `mask_array > 0`
3. `binary_mask * 255`
4. `Image.Resampling.NEAREST`

这四个点分别对应：

- 单通道正式入口
- 唯一前景定义
- 磁盘口径
- 离散 resize 规则

如果后面某个阶段标签看起来不对，先回来看这四个点，通常就能快速判断问题是不是从数据协议层开始的。

## 为什么这样设计，而不是别的设计

### 取舍 1: 为什么不用“按数据集分别定阈值”

因为当前路线要保证 `GlaS` 和 `CRAG` 先共用一条语义标签主线。
如果这里按数据集分裂，后面你就很难再说训练、评估、边界派生和距离派生是在同一协议上比较。

### 取舍 2: 为什么不直接把磁盘文件保留成 `{0,1}`

可以这么做，但当前工程里 PNG 预览、人工抽查和其他工具更容易把 `0/255` 视为稳定视觉口径。
所以这里把“训练张量口径”和“磁盘口径”明确拆开，反而更不容易误用。

### 取舍 3: 为什么 resize 后还要再做一次 `> 0`

因为这个函数的职责不是“差不多还是 mask 就行”，而是“输出必须继续是正式二值标签”。
只要输出口径还可能漂，就应该在函数内部收干净，而不是把这个责任推给下游。

## 如何验证这份代码没跑偏

### 验证 1: 看正式前景规则有没有被写死

1. 打开 `src/data/mask_ops.py`
2. 找 `binarize_mask_gt_zero()`
3. 确认核心表达式是 `mask_array > 0`

通过标准：

- 没有别的阈值分支
- 没有按数据集切换规则

### 验证 2: 看 resize 是否仍是离散插值

1. 找 `resize_binary_mask()`
2. 确认 `resample=Image.Resampling.NEAREST`

通过标准：

- 没有双线性或其它连续插值

### 验证 3: 看磁盘口径和训练口径有没有分开

1. 找 `export_binary_mask_png()`
2. 确认导出前乘了 `255`
3. 再看 `resize_binary_mask()` 的返回值是否重新压回 `{0,1}`

通过标准：

- 导出文件适合人工检查
- 内存结果仍适合后续训练链

### 验证 4: 回看阶段协议是否对得上

1. 打开 `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/05_标签转换与可视化规则.md`
2. 搜 `mask > 0`
3. 搜 `mask_interp: nearest`

通过标准：

- 协议文件和代码里的规则完全同向

## 最容易误解的地方

### 误区 1

“这几个函数太简单了，不值得单独写说明文。”

不对。
它们简单，正说明它们承载的是被冻结后的正式协议，而不是待探索的复杂策略。
越是这种全链路都会继承的基础规则，越不能含糊。

### 误区 2

“反正 boundary 和 distance 都会再派生，主 mask 规则松一点也没关系。”

也不对。
边界图和距离图就是从主 mask 派生出来的。
源头不稳，派生资产只会把问题放大，不会把问题修好。

### 误区 3

“只要最后显示成黑白图，插值方式无所谓。”

这是很常见的坑。
mask 不是拿来好看的，它是监督信号。
只要插值错了，边界就已经被你改写了。

## 读完后下一步看什么

建议按下面顺序继续：

1. `configs_data_glas.yaml.md`
2. `configs_data_crag.yaml.md`
3. 后续要补的 `src_data_boundary_targets.py.md`
4. 后续要补的 `src_data_distance_targets.py.md`

这样你会更容易把“基础 mask 协议”和“派生标签协议”连成一条线，而不是把它们看成几份互不相干的小工具。
