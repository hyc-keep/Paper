# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [x] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `backbone 论文`
- `residual block / shortcut 论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇是后续 `ResNet34-U-Net` 的 backbone 来源，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`Deep Residual Learning for Image Recognition`
- 作者/团队：`Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun`
- 发表年份/会议/期刊：`2016, CVPR 2016`
- DOI / arXiv ID：`10.1109/CVPR.2016.90` / `arXiv:1512.03385`
- BibTeX key：`he2016resnet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/Deep_Residual_Learning_for_Image_Recognition_2016.pdf`
- 当前定位：`为后续 `ResNet34-U-Net` 这类 encoder backbone 提供最核心的结构来源和 residual block 理论依据`
- 与已提取论文的关系：
  - 继承自：`VGG` 风格深层卷积网络
  - 被谁引用/改进：`ResUNet`、`ResNet34-U-Net`、`DeepLab` 系列、几乎所有残差型视觉 backbone
  - 互补论文：`U-Net_2015`、`DeepLabV3+_2018`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：随着网络深度增加，准确率会先饱和后下降，而且这种 degradation 不是由 overfitting 引起的
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：如果最优映射接近 identity，那么让网络学习 residual 会比直接学习原映射更容易优化
  - 用途：`方法动机`
  - 页码：`p.2-p.3`
- 句子/事实 3：`152-layer ResNet` 在 `ImageNet` 上比 `VGG` 更深但复杂度更低，证明 residual learning 能稳定支撑极深网络
  - 用途：`结果概述`
  - 页码：`Abstract, p.1, p.6-p.7`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`ResNet` 的核心不是简单堆深度，而是通过 identity shortcut 把若干层改写成 `F(x)+x`
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.3`
- 句子/事实 2：projection shortcut 主要在维度变化时使用，但解决 degradation 问题本身并不依赖所有 shortcut 都做 projection
  - 用途：`结构细节`
  - 页码：`p.3-p.6`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| mini-batch size | `256` | 训练设置 | `p.4` |
| 初始学习率 | `0.1` | 训练设置 | `p.4` |
| weight decay | `1e-4` | 训练设置 | `p.4` |
| momentum | `0.9` | 训练设置 | `p.4` |
| 训练 crop | `224×224` | 训练设置 | `p.4` |
| 34-layer FLOPs | `3.6e9` | 效率/结构对比 | `p.3-p.5` |
| 152-layer FLOPs | `11.3e9` | 效率/结构对比 | `p.5` |
| Ensemble top-5 error | `3.57%` | 主结果 | `Abstract, p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 深网络虽然理论上表示能力更强，但实际训练时随着深度增加会出现 degradation problem，即训练误差本身也变差
- 这个问题并不是简单的 overfitting，因为更深网络连训练集都拟合得更差
- 如果更深网络的新增层能学成 identity mapping，它本不应比浅层网络更差；但现有求解器难以找到这样的解
- 因此需要一种让深层网络更易优化的结构重参数化方式

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 不再让若干堆叠层直接学习原始映射 `H(x)`，而是改为学习 residual function `F(x)=H(x)-x`，使输出写成 `F(x)+x`。这个改写通过 parameter-free identity shortcut 实现，不增加额外参数和复杂度，但能显著缓解深层网络的优化困难，从而让 34、50、101、152 层网络都能稳定训练并获得更高精度。

关键页码：

- `p.2-p.3`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`residual CNN backbone`
- Backbone：`ResNet-18 / 34 / 50 / 101 / 152`
- 输入尺寸：`训练时随机裁 `224×224``
- 输出头：`global average pooling + 1000-d fc + softmax`（ImageNet 分类设置）

### 3.2 关键模块详细描述

**模块 1：`Basic Residual Block`**

- 位置：`ResNet-18 / 34` 的主干块`
- 操作流程：
  1. 堆叠两层 `3×3` 卷积
  2. shortcut 直接传递输入 `x`
  3. 主分支输出 `F(x)` 与 shortcut 做逐元素相加
  4. 再经过非线性激活
- 页码：`p.2-p.3, p.6`

**模块 2：`Identity Shortcut / Projection Shortcut`**

- 位置：`每个 residual block 的旁路`
- 操作流程：
  1. 若输入输出维度一致，直接使用 identity shortcut
  2. 若通道数或空间尺寸变化，可用零填充或 `1×1` projection shortcut 匹配维度
  3. 作者实验表明解决 degradation 问题不一定需要所有 shortcut 都带参数
- 页码：`p.3, p.5-p.6`

**模块 3：`Bottleneck Block`**

- 位置：`ResNet-50 / 101 / 152`
- 操作流程：
  1. 先用 `1×1` 降维
  2. 再用 `3×3` 处理
  3. 最后用 `1×1` 升维
  4. shortcut 与主支路相加形成 bottleneck residual block
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 输出尺寸 | ResNet-18 | ResNet-34 | ResNet-50 | 备注 |
|---------|---------|-----------|-----------|-----------|------|
| `conv1` | `112×112` | `7×7,64,stride2` | `7×7,64,stride2` | `7×7,64,stride2` | 后接 max pool |
| `conv2_x` | `56×56` | `[3×3,64; 3×3,64] ×2` | `[3×3,64; 3×3,64] ×3` | `[1×1,64; 3×3,64; 1×1,256] ×3` | |
| `conv3_x` | `28×28` | `[3×3,128; 3×3,128] ×2` | `[3×3,128; 3×3,128] ×4` | `[1×1,128; 3×3,128; 1×1,512] ×4` | 首块降采样 |
| `conv4_x` | `14×14` | `[3×3,256; 3×3,256] ×2` | `[3×3,256; 3×3,256] ×6` | `[1×1,256; 3×3,256; 1×1,1024] ×6` | 首块降采样 |
| `conv5_x` | `7×7` | `[3×3,512; 3×3,512] ×2` | `[3×3,512; 3×3,512] ×3` | `[1×1,512; 3×3,512; 1×1,2048] ×3` | 首块降采样 |
| head | `1×1` | avg pool + fc | avg pool + fc | avg pool + fc | |

补充：

| 模型 | FLOPs |
|------|-------|
| ResNet-18 | `1.8e9` |
| ResNet-34 | `3.6e9` |
| ResNet-50 | `3.8e9` |
| ResNet-101 | `7.6e9` |
| ResNet-152 | `11.3e9` |

说明：

- 对我们项目最关键的是 `ResNet-34`：它仍然使用两层 `3×3` 的 basic block，更适合后续对接 `U-Net` 式 decoder

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
F(x) := H(x) - x
```

符号说明：

- `H(x)`：希望若干堆叠层学习到的原始目标映射
- `F(x)`：改写后的 residual mapping
- 含义：把“直接学目标函数”改成“学相对输入的残差”
- 页码：`p.2-p.3`

公式 2：

```text
y = F(x, {W_i}) + x
```

符号说明：

- `x`：block 输入
- `y`：block 输出
- `F(x, {W_i})`：主支路要学习的残差函数
- 含义：basic residual block 的标准形式
- 页码：`p.3`

公式 3：

```text
y = F(x, {W_i}) + W_s x
```

符号说明：

- `W_s`：shortcut 上的线性 projection
- 作用：当输入输出维度不匹配时，用于匹配通道或尺寸
- 页码：`p.3`

### 4.2 推导过程或梯度行为

- 梯度特性：identity shortcut 让信息和梯度都能更直接穿过深层网络，降低深度增加带来的优化难度
- 适用条件：适合构建更深的 backbone，并作为其他视觉任务的特征提取器
- 不适用场景：如果任务本身不需要这么深的 encoder，完整 ResNet 的深度可能带来冗余
- 页码：`p.2-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| 分类损失 | `正文未显式写出公式` | 1000 类 ImageNet 分类 | 最终 fc + softmax 输出 |

### 5.2 总损失公式

```text
L_total = ImageNet classification objective
```

说明：

- 这篇论文的重点完全不在新 loss，而在 residual architecture
- 因此这里不能过度扩写不存在的损失细节

### 5.3 权重配置与调度策略

- 各项权重：`不适用`
- 是否衰减/动态调整：`learning rate plateau 时除以 10`
- 页码：`p.4`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| ImageNet 2012 | `1.28M` | `100k test` | `50k val` | 1000 类 |
| CIFAR-10 | 标准训练集 | 标准测试集 | 标准划分 | 用于超深网络分析 |

### 6.2 数据增强

- 增强列表：
  - `shorter side` 随机采样在 `[256, 480]`
  - `224×224` random crop
  - `horizontal flip`
  - `standard color augmentation`
- Patch 提取策略：`224×224 crop`
- 页码：`p.4`

### 6.3 优化器与超参数

- 框架：`Caffe`
- 优化器：`SGD`
- 初始学习率：`0.1`
- 学习率调度：`error plateau 时 /10`
- Batch size：`256`
- Epoch / Steps：`up to 60×10^4 iterations`
- 权重初始化：`as in [13]`
- 预训练策略：`从头训练`
- 是否冻结部分层：`否`
- 设备：`正文未显式写训练硬件`
- 页码：`p.4`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用`
- 颜色空间转换：`未提到`
- resize / crop / pad 策略：`shorter side 256-480 + random 224 crop`
- patch overlap：`不适用`
- 背景过滤策略：`不适用`
- 标签生成方式：`ImageNet 分类标签`
- 类别不平衡处理：`未重点讨论`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`采用标准 ImageNet / CIFAR 划分`
- 页码：`p.4`

---

## 7. 推理与后处理

- 推理时输入尺寸：`10-crop testing`；最佳结果还会采用 fully-convolutional multi-scale 测试
- 概率阈值：`不适用`
- 后处理步骤：
  1. `10-crop testing` 用于常规比较
  2. `fully-convolutional form`
  3. 多尺度平均，短边取 `{224, 256, 384, 480, 640}`
- TTA / Test-time refinement：`multi-scale testing`
- 页码：`p.4`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | plain-18 vs plain-34 | `27.94 -> 28.54 top-1 error` 变差 | 直接加深 plain net 会出现 degradation |
| 2 | ResNet-18 vs ResNet-34 | `27.88 -> 25.03 top-1 error` 改善 | residual learning 让加深真正带来收益 |
| 3 | ResNet-34 A/B/C | `25.03 / 24.52 / 24.19 top-1 error` | projection shortcut 略有帮助，但 identity shortcut 已足够解决核心问题 |
| 4 | ResNet-34 vs 50 / 101 / 152 | `25.03 -> 22.85 -> 21.75 -> 21.43` | 更深 residual net 持续获益 |

### 8.2 各模块贡献量化

- 模块 A 的独立贡献：`34-layer ResNet` 相比 `34-layer plain net` 降低约 `3.5` 个 top-1 error 点
- 模块 B 的独立贡献：加深到 `50 / 101 / 152` 层继续带来明显精度提升
- 模块 C 的独立贡献：identity shortcut 几乎不增加参数和复杂度，却显著降低优化难度
- 页码：`p.5-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| ImageNet val | `ResNet-34 top-1 25.03` | `top-5 7.76` | - | option A |
| ImageNet val | `ResNet-50 top-1 22.85` | `top-5 6.71` | - | |
| ImageNet val | `ResNet-101 top-1 21.75` | `top-5 6.05` | - | |
| ImageNet val | `ResNet-152 top-1 21.43` | `top-5 5.71` | - | |
| ImageNet test ensemble | `top-5 3.57` | - | - | ILSVRC 2015 1st place |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `plain-34` | ImageNet val | `top-1 28.54` | `top-5 10.02` | - |
| `ResNet-34 A` | ImageNet val | `top-1 25.03` | `top-5 7.76` | - |
| `ResNet-34 B` | ImageNet val | `top-1 24.52` | `top-5 7.46` | - |
| `ResNet-34 C` | ImageNet val | `top-1 24.19` | `top-5 7.40` | - |
| `ResNet-50` | ImageNet val | `top-1 22.85` | `top-5 6.71` | - |
| `ResNet-101` | ImageNet val | `top-1 21.75` | `top-5 6.05` | - |
| `ResNet-152` | ImageNet val | `top-1 21.43` | `top-5 5.71` | - |
| `BN-Inception` | ImageNet val | `top-1 21.99` | `top-5 5.81` | - |
| `PReLU-net` | ImageNet val | `top-1 21.59` | `top-5 5.71` | - |

### 9.3 公平对比条件确认

- 是否统一 backbone：`plain/residual 对比基本统一，只改 shortcut 形式`
- 是否统一数据增强：`是，主比较在同一 ImageNet 训练协议下完成`
- 是否统一后处理：`是，10-crop testing`
- 是否统一输入尺寸：`是，224 crop`
- 结果来源：`原文数字`
- 页码：`p.4-p.7`

### 9.4 评价协议与指标定义

- 数据划分来源：`标准 ImageNet 2012 / CIFAR-10`
- 结果汇报层级：`val / test`
- 实例匹配规则：`不适用`
- Dice 类型：`未使用`
- Hausdorff 类型：`未使用`
- F1 类型：`未使用`
- 是否含后处理后再报结果：`不适用`
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`是`
- 页码：`p.4-p.7`

---

## 10. 计算量与效率

- 参数量（Params）：`正文更强调 FLOPs，未系统列出参数量`
- 计算量（FLOPs / MACs）：`18: 1.8e9, 34: 3.6e9, 50: 3.8e9, 101: 7.6e9, 152: 11.3e9`
- 推理时间（ms/image）：`未直接给出`
- 训练时间（总 GPU-hours）：`未直接给出`
- 输入尺寸（计算量对应的）：`224×224`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `VGG-19` | `未报告` | `19.6e9` | `未报告` |
| `ResNet-34` | `未报告` | `3.6e9` | `未报告` |
| `ResNet-50` | `未报告` | `3.8e9` | `未报告` |
| `ResNet-152` | `未报告` | `11.3e9` | `未报告` |

- 页码：`p.3-p.7`

---

## 13. 开源与复现

- 代码是否开源：`正文未直接给出仓库链接`
- 代码仓库地址：`[待确认]`
- 框架/语言：`Caffe`
- 预训练权重是否提供：`正文未明确`
- 复现难度评估：`中`
- 复现障碍：`原始实现是分类 backbone 论文，不是直接医学分割代码；但结构和训练协议描述比较清楚`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不视为论文固定值 | 中 |
| 验证集划分 | 是 | 采用官方划分理解结果 | 低 |
| 推理阈值 | 不适用 | 分类 argmax | 低 |
| 后处理细节 | 部分 | 记录 10-crop / multi-scale testing | 低 |
| 训练轮数停止准则 | 部分 | 记录为 60×10^4 iterations 上限 | 中 |
| 数据预处理 | 是 | 已记录 scale jitter / crop / color aug | 低 |

- 不确定但影响较大的点：
  - `原始代码/预训练权重可得性`
  - `如果迁移到医学分割时，哪些 stem/stride 该保持，哪些该改`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文主要解决分类 backbone 的优化问题，并不直接讨论医学分割 decoder 或对象级边界问题
- projection shortcut 虽然略有提升，但在更深 bottleneck 模型里也要考虑效率与复杂度
- 页码：`p.5-p.7`

### 14.2 我们观察到的潜在问题

- 这篇不能直接告诉我们 `ResNet34-U-Net` 在腺体分割上的具体训练参数
- `ResNet` 的 ImageNet stem、stride 与下采样设置迁移到病理分割时，常需要工程改动
- 但它非常适合作为“为什么选 ResNet34 当 encoder”的理论来源

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`没有视觉失败案例，主要通过 degradation 曲线展示 plain net 的失败现象`
- 典型失败场景：`plain network 随深度增加出现更高训练误差和更差验证误差`
- 页码：`p.1-p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `ResNet34` 作为 encoder backbone 的结构来源
- residual block 与 shortcut 设计的理论依据
- 用 `ResNet34` 而不是更浅 plain CNN 的优化动机

### 15.2 可以作为候选参数来源的

- `224 crop`、`SGD + momentum 0.9 + weight decay 1e-4` 只可作为自然图像分类训练的背景参考
- `projection shortcut` 只在维度变化时使用的设计原则

### 15.3 不应照搬的（及原因）

- ImageNet 分类训练超参数直接照搬到腺体分割
  - 原因：任务、损失、输入尺寸和数据分布都不同
- 用分类 top-1/top-5 结果推断腺体分割性能
  - 原因：这只是 backbone 论文，不是 segmentation benchmark
- 直接套用 `fc + softmax` 头部结构
  - 原因：我们只借 encoder 主干，不借分类头

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 为什么选 `ResNet34` 当 encoder | 原始 basic residual block 与 34-layer 结构直接来自本文 | 强 |
| 为什么不用 plain CNN encoder | degradation problem 是直接理论依据 | 强 |
| 是否要把 50/101/152 都拉进主线 | 不必，34 已是更适合 U-Net decoder 对接的平衡点 | 中 |
| 是否能直接拿到 segmentation 参数 | 不能，这篇只提供 backbone 依据 | 弱 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`01_实验执行/04_Baseline/01_R34UNet结构与来源.md`
- [ ] 需要和哪篇论文交叉验证：`U-Net_2015`、`Attention_U-Net_2018`
- [ ] 待确认的问题：`在当前项目里，ResNet34 encoder 是保留 ImageNet-style stem，还是做更适合病理图像的小改动`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 深网络优化中的 degradation problem | 作为残差 backbone 动机 |
| related work | residual learning 的原始出处 | 放在 backbone 演化段 |
| 方法 | `ResNet34` encoder 的结构来源 | 只引用 encoder backbone，不夸大为完整复现 |
| 实验设置 | `ResNet34-U-Net` 的 backbone 来源 | 作为结构依据而非训练参数依据 |
| 讨论 | 为什么残差 encoder 比 plain encoder 更稳 | 用于解释 backbone 选择 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig.1` | `p.1` | CIFAR plain net degradation 曲线 | 解释为什么需要 residual learning |
| `Fig.2` | `p.2` | residual block 示意图 | shortcut 结构依据 |
| `Fig.3` | `p.3-p.4` | VGG / plain-34 / ResNet-34 架构对比 | backbone 结构引用 |
| `Table 1` | `p.5` | ImageNet 各层 ResNet 架构表 | `ResNet34` 结构直接依据 |
| `Fig.4` | `p.5` | ImageNet 上 plain vs ResNet 训练曲线 | 说明 residual learning 解决 degradation |
| `Table 2` | `p.5` | 18/34 plain vs residual 对比 | 关键数字引用 |
| `Table 3` | `p.6` | shortcut A/B/C 与 50/101/152 结果 | shortcut 细节和更深网络效果 |
| `Fig.5` | `p.6` | basic block 与 bottleneck 对比 | 解释 34 与 50+ 的差别 |
| `Table 5` | `p.7` | ensemble ImageNet test 结果 | 经典引用数字 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（作为分类 backbone 论文层面）
- [x] 预处理与数据细节已检查（scale jitter / crop / BN / SGD）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认（不是只记指标名字）
- [x] 消融实验的结论已量化（不只是"有效"）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
