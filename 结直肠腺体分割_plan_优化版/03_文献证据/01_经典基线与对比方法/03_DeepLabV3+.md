# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `大感受野 / 多尺度上下文建模`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇同时也是强上下文建模代表作，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation`
- 作者/团队：`Liang-Chieh Chen, Yukun Zhu, George Papandreou, Florian Schroff, Hartwig Adam`
- 发表年份/会议/期刊：`2018, ECCV 2018`
- DOI / arXiv ID：`10.1007/978-3-030-01234-2_49` / `10.48550/arXiv.1802.02611`
- BibTeX key：`chen2018deeplabv3plus`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/DeepLabV3+_Encoder-Decoder_with_Atrous_Separable_Convolution_2018.pdf`
- 当前定位：`强外部对比基线，代表“大感受野多尺度上下文 + 轻量 decoder 边界修复”路线`
- 与已提取论文的关系：
  - 继承自：`DeepLabv3` 的 `ASPP + image-level features` 编码器
  - 被谁引用/改进：后续大量 `DeepLab` 系列、医学图像 `DeepLabV3+` 迁移版本、轻量语义分割网络
  - 互补论文：`U-Net_2015`、`Attention_U-Net_2018`、`Large_Kernel_Matters_2018`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：`spatial pyramid pooling` 擅长编码多尺度上下文，而 `encoder-decoder` 擅长恢复 sharper object boundaries，两者各有优势
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：`DeepLabv3+` 的核心思想是把 `DeepLabv3` 作为强 encoder，再加一个 simple yet effective decoder 专门修边界
  - 用途：`方法动机`
  - 页码：`p.1-p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`DeepLabv3+` 不是纯 U 形结构，而是“多尺度空洞卷积编码器 + 轻量 decoder”的混合式分割架构
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.6`
- 句子/事实 2：`atrous separable convolution` 被同时用于 `ASPP` 与 decoder，从而在维持性能的同时显著降低计算量
  - 用途：`效率动机`
  - 页码：`p.5-p.6, p.11-p.12`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 初始学习率 | `0.007` | 实验设置 | `p.7` |
| Crop size | `513×513` | 实验设置 | `p.7` |
| train output stride | `16` | 方法/实验设置 | `p.6-p.7, p.9-p.10` |
| decoder 通道压缩 | `[1×1, 48]` | 方法设计 | `p.8-p.9` |
| decoder refine conv | `two [3×3, 256]` | 方法设计 | `p.8-p.9` |
| PASCAL VOC test | `89.0%` | 主结果 | `p.1, p.13` |
| Cityscapes test | `82.1%` | 主结果 | `p.1, p.14` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- `spatial pyramid pooling / ASPP` 路线可以编码强多尺度上下文，但最后的高层特征图在边界处缺少细节
- 单纯依赖空洞卷积提取更稠密特征虽然能改善边界，但在现代大 backbone 上计算代价很高，尤其是 `output stride = 8` 或更密时
- 传统 `encoder-decoder` 路线可以恢复边界，但往往缺少像 `ASPP` 这样的强上下文建模能力
- 目标是在保持 `DeepLabv3` 多尺度语义能力的同时，用一个简单 decoder 修复边界，并用 `atrous separable convolution` 提升速度与强度

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文把 `DeepLabv3` 当作 encoder，利用 `ASPP + image-level features + atrous convolution` 编码多尺度上下文；再将 encoder 输出先上采样 `4x`，与较浅层的 low-level feature 融合，之后用两层 `3×3` 卷积细化边界并再上采样 `4x` 生成预测。同时把 `depthwise separable convolution` 推广到 `ASPP` 和 decoder，从而得到更快更强的 `DeepLabv3+`。

关键页码：

- `p.1-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`encoder-decoder with atrous convolution`
- Backbone：`ResNet-101` 或 `Modified Aligned Xception`
- 输入尺寸：`训练 crop size 513×513`
- 输出头：`像素级语义分割输出；decoder 最终输出 stride = 4 后再双线性上采样到原图`

### 3.2 关键模块详细描述

**模块 1：`DeepLabv3 Encoder / ASPP`**

- 位置：`主干高层语义编码端`
- 操作流程：
  1. backbone 用 `atrous convolution` 提取任意目标分辨率的 dense feature
  2. `ASPP` 用多组不同 rate 的并行空洞卷积探测多尺度上下文
  3. 再加 `image-level features`
  4. 最后得到 `256-channel` 的 encoder 输出特征
- 页码：`p.2-p.6`

**模块 2：`Proposed Decoder`**

- 位置：`encoder 输出之后，最终预测之前`
- 操作流程：
  1. 先把 encoder feature 双线性上采样 `4x`
  2. 取 backbone 中与其同分辨率的 low-level feature
  3. 对 low-level feature 先做 `[1×1, 48]` 降通道，避免其大通道数压制 encoder 语义特征
  4. 拼接后用 `two [3×3, 256]` 细化
  5. 再上采样 `4x` 得到最终预测
- 页码：`p.6-p.9`

**模块 3：`Atrous Separable Convolution`**

- 位置：`用于 ASPP 与 decoder 的卷积替换`
- 操作流程：
  1. 标准卷积分解成 `depthwise convolution + pointwise convolution`
  2. 在 depthwise 阶段加入 atrous rate
  3. 以更低的计算量维持相近或更优性能
- 页码：`p.5-p.6, p.11-p.12`

**模块 4：`Modified Aligned Xception`**

- 位置：`更强 backbone 版本`
- 操作流程：
  1. 采用更深的 `Xception`
  2. 用 stride 的 `depthwise separable convolution` 替换 max pooling
  3. 在每个 `3×3 depthwise conv` 后增加额外的 `BN + ReLU`
  4. 使得分割任务上的 dense feature 提取更适合 `atrous separable convolution`
- 页码：`p.6-p.8`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Backbone encoder | ResNet-101 / Xception | backbone 依赖 | `OS=16 / 8` | 用 atrous conv 控制输出分辨率 |
| ASPP branches | parallel atrous conv + image pooling | `256` 级别输出 | encoder 输出尺度 | 多 rate 多尺度上下文 |
| Encoder output | fused semantic feature | `256` | `input/16` 常用 | 论文明确提到为 256 channels |
| Low-level feature | Conv2 before striding | 原始较高 | `input/4` | 先 `[1×1, 48]` 降维 |
| Decoder refine 1 | `3×3 conv` | `256` | `input/4` | 拼接后细化 |
| Decoder refine 2 | `3×3 conv` | `256` | `input/4` | 拼接后细化 |
| Final prediction | bilinear upsample | `Nc` | 原图大小 | 最终分割图 |

说明：

- 论文不是像 `U-Net` 那样给完整逐层通道尺寸链路，而是重点给 decoder 关键结构选择
- 其中最直接可复用的设计点是：`[1×1, 48] + two [3×3, 256] + Conv2 low-level feature`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
y[i] = \sum_k x[i + r · k] w[k]
```

符号说明：

- `x`：输入特征图
- `y`：输出特征图
- `i`：输出位置
- `w[k]`：卷积核参数
- `r`：atrous rate
- 作用：通过改变 `r` 控制采样间隔，从而扩大感受野并控制输出特征密度
- 页码：`p.5`

公式 2：

```text
output stride = input spatial resolution / final output resolution
```

符号说明：

- `output stride (OS)`：输入分辨率相对最终特征图分辨率的缩放比
- `OS=16 / 8`：论文重点比较的两种 encoder 特征密度设置
- 页码：`p.5-p.6`

### 4.2 推导过程或梯度行为

- 梯度特性：论文未做显式梯度推导，但通过 decoder 设计和 trimap 实验证明，加入 decoder 后边界附近区域的分割精度显著提升
- 适用条件：适合需要更大上下文但又不想完全放弃边界细节的语义分割任务
- 不适用场景：当数据量很小、对象尺度更像病理实例而非自然场景语义区域时，直接照搬整套 `DeepLabV3+` 训练协议不一定合适
- 页码：`p.12-p.14`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| segmentation loss | `正文未显式展开` | 像素级语义分割 | 最终输出 |

### 5.2 总损失公式

```text
L_total = semantic segmentation objective used in DeepLabv3 training protocol
```

说明：

- 这篇论文的重点不在新 loss，而在结构设计
- 正文直接说训练协议沿用 `DeepLabv3`，并未在本文中完整展开损失公式
- 因此这里不能把常见 CE 细节冒充为本文明确写出的原值

### 5.3 权重配置与调度策略

- 各项权重：`正文未单独说明`
- 是否衰减/动态调整：`学习率调度使用 poly policy`
- 页码：`p.7`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| PASCAL VOC 2012 | `train 1464 + val 1449 + test 1456` | 官方 test | `trainaug 10582` 用于训练 | `21` 类 mIOU |
| Cityscapes | `2975 train / 500 val / 1525 test` | 官方 test | 官方 val | 另有约 `20000` coarse annotations |

### 6.2 数据增强

- 增强列表：
  - `random scale data augmentation`
  - `multi-scale inputs during evaluation`
  - `left-right flipped inputs`（推理可选）
- Patch 提取策略：`crop size 513×513`
- 页码：`p.7, p.9-p.12`

### 6.3 优化器与超参数

- 框架：`TensorFlow`
- 优化器：`正文未在分割训练部分明确写出；训练协议说明沿用 DeepLabv3`
- 初始学习率：`0.007`
- 学习率调度：`poly policy`
- Batch size：`正文未在分割训练处明确写出 [待确认]`
- Epoch / Steps：`正文未明确给出 [待确认]`
- 权重初始化：`ResNet-101 / Modified Xception 采用 ImageNet-1k 预训练`
- 预训练策略：`ImageNet-1k`；增强版本进一步使用 `COCO` 与 `JFT-300M`
- 是否冻结部分层：`最佳模型在 test set 训练时使用 frozen batch normalization`
- 设备：`正文未在分割训练处明写；Xception 预训练部分使用 50 GPUs`
- 页码：`p.7, p.10-p.13`

补充：

- Xception ImageNet 预训练参数单独给出：
  - `Nesterov momentum = 0.9`
  - `initial lr = 0.05`
  - `rate decay = 0.94 every 2 epochs`
  - `weight decay = 4e-5`
  - `50 GPUs, batch size 32/GPU, image size 299×299`
- 这些是 backbone 预训练参数，不应和分割主实验训练参数混为一谈
- 页码：`p.10`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用，自然图像语义分割`
- 颜色空间转换：`未提到`
- resize / crop / pad 策略：`crop size 513×513`
- patch overlap：`未提到`
- 背景过滤策略：`不适用`
- 标签生成方式：`官方语义分割像素标签`
- 类别不平衡处理：`未重点讨论`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`采用官方 train/val/test 划分，风险较低`
- 页码：`p.7, p.13-p.14`

---

## 7. 推理与后处理

- 推理时输入尺寸：`按训练 crop 与 output stride 组合推理；常比较 eval OS=16 / 8`
- 概率阈值：`不适用，语义分割 argmax 输出`
- 后处理步骤：
  1. `decoder 输出后双线性上采样回原图`
  2. `可选 multi-scale inference`
  3. `可选 left-right flip inference`
- TTA / Test-time refinement：`multi-scale + flip`
- 页码：`p.9-p.12`

说明：

- 论文特别强调最终 test set 结果 `without any post-processing`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | decoder 的 `1×1` 通道压缩从不同通道数取值 | `48` 通道最好，`mIOU 78.21%` | low-level feature 必须先降维，避免压过高层语义特征 |
| 2 | decoder refine conv 结构不同 | `two [3×3, 256]` 达到 `78.85%`，优于一层或三层 | 两层 `3×3` 是最有效的简单 decoder 结构 |
| 3 | 使用 `Conv2` vs `Conv2+Conv3` | `Conv2 + two [3×3,256]` 最优；加入 `Conv3` 无显著增益 | 不必像 U-Net 那样逐层密集解码 |
| 4 | ResNet-101 上加 decoder | `77.21% -> 78.85%` (`eval OS=16`)；`78.51% -> 79.35%` (`eval OS=8`) | decoder 主要提升边界恢复 |
| 5 | Xception 版中采用 atrous separable conv 于 ASPP+decoder | Multiply-Adds 降低 `33%-41%`，性能相近 | `atrous separable conv` 提升效率非常明显 |

### 8.2 各模块贡献量化

- 模块 A 的独立贡献：`decoder` 在 ResNet-101 上带来约 `+1.64%` 或 `+0.84%` mIOU 提升，取决于 eval OS
- 模块 B 的独立贡献：`atrous separable conv` 把计算量降低 `33%-41%`
- 模块 C 的独立贡献：trimap 边界实验显示在最窄边界带上，decoder 给 `ResNet-101 / Xception` 分别带来 `4.8% / 5.4%` mIOU 提升
- 页码：`p.8-p.12`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| PASCAL VOC 2012 test | `87.8%` | `89.0%` | - | 分别对应 `Xception` / `Xception-JFT` |
| Cityscapes test | `82.1%` | - | - | `DeepLabv3+` |
| PASCAL VOC val (ResNet-101, decoder) | `78.85%` | `79.35%` | - | 分别对应 `eval OS=16 / 8` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `DeepLabv3+ (Xception-JFT)` | PASCAL VOC 2012 test | `mIOU 89.0%` | - | - |
| `DeepLabv3+ (Xception)` | PASCAL VOC 2012 test | `mIOU 87.8%` | - | - |
| `DeepLabv3-JFT` | PASCAL VOC 2012 test | `mIOU 86.9%` | - | - |
| `DeepLabv3` | PASCAL VOC 2012 test | `mIOU 85.7%` | - | - |
| `PSPNet` | PASCAL VOC 2012 test | `mIOU 85.4%` | - | - |
| `DeepLabv3+` | Cityscapes test | `mIOU 82.1%` | - | - |
| `PSPNet` | Cityscapes test | `mIOU 81.2%` | - | - |
| `DeepLabv3` | Cityscapes test | `mIOU 81.3%` | - | - |

### 9.3 公平对比条件确认

- 是否统一 backbone：`部分对比统一，部分是跨 backbone SOTA 对比`
- 是否统一数据增强：`不完全统一，特别是 COCO/JFT 预训练会改变比较基础`
- 是否统一后处理：`是，主结果强调不使用 post-processing`
- 是否统一输入尺寸：`主要在相同 crop size / OS 设置下比较，但跨方法不完全统一`
- 结果来源：`原文数字`
- 页码：`p.9-p.14`

### 9.4 评价协议与指标定义

- 数据划分来源：`官方 PASCAL VOC 2012 / Cityscapes 划分`
- 结果汇报层级：`val / test`
- 实例匹配规则：`不适用，语义分割`
- Dice 类型：`未使用`
- Hausdorff 类型：`未使用`
- F1 类型：`未使用`
- 是否含后处理后再报结果：`否`
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`是`
- 页码：`p.7, p.13-p.14`

---

## 10. 计算量与效率

- 参数量（Params）：`正文未直接给出`
- 计算量（FLOPs / MACs）：`论文使用 Multiply-Adds`
- 推理时间（ms/image）：`未直接给出`
- 训练时间（总 GPU-hours）：`未直接给出`
- 输入尺寸（计算量对应的）：`主要随 VOC val 设置、OS 与 MS/Flip 策略变化`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| ResNet-101, no decoder, OS16 | `未报告` | `81.02B` Multiply-Adds | `未报告` |
| ResNet-101 + decoder, OS16 | `未报告` | `101.28B` Multiply-Adds | `未报告` |
| Xception + decoder + SC, OS16 | `未报告` | `54.17B` Multiply-Adds | `未报告` |

- 页码：`p.9-p.12`

说明：

- 在 Xception 版本中，把 `atrous separable convolution` 用到 ASPP 与 decoder 后，计算复杂度下降 `33%-41%`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/tensorflow/models/tree/master/research/deeplab`
- 框架/语言：`TensorFlow`
- 预训练权重是否提供：`论文配套 reference implementation，权重需结合官方仓库确认`
- 复现难度评估：`中到高`
- 复现障碍：`训练协议部分沿用 DeepLabv3；同时 COCO/JFT 预训练、MS/Flip、不同 OS 选择都会显著影响结果`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不视为论文固定值 | 中 |
| 验证集划分 | 是 | 使用官方划分理解论文结果 | 低 |
| 推理阈值 | 不适用 | 语义分割 argmax | 低 |
| 后处理细节 | 是 | 明确记录为无 post-processing | 低 |
| 训练轮数停止准则 | 否 | 不把 epoch 视作论文固定值 | 高 |
| 数据预处理 | 部分 | 只记录 crop、OS、scale、MS/Flip 等已明确项目 | 中 |

- 不确定但影响较大的点：
  - `分割主训练使用的精确 optimizer / momentum / weight decay`
  - `batch size`
  - `不同实验表的完整超参数一致性`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 当把 encoder 特征提得更密时，计算代价明显增加，所以 `OS=8` 只带来边际提升但成本更高
- 论文不继续追求 `output stride < 4` 的更密 decoder 输出，原因是 GPU 资源有限
- 失败模式主要出现在类别相似、严重遮挡、稀有视角物体
- 页码：`p.6, p.10-p.14`

### 14.2 我们观察到的潜在问题

- 这是自然图像语义分割强基线，不是病理实例分割论文；其指标、数据分布和目标类型与腺体分割差异很大
- `DeepLabV3+` 强项是上下文和边界修复，但对 gland instance separation 未必天然占优
- 它很适合作为“强外部对比”，但不适合直接定义我们主线 protocol

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是，Fig.6 最后一行专门给出 failure mode`
- 典型失败场景：`sofa vs chair` 混淆、严重遮挡、稀有视角物体
- 页码：`p.12-p.14`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 把 `DeepLabV3+` 作为强外部对比，代表“大感受野多尺度上下文”路线
- 如果后续做 decoder 轻量边界修复，可以参考它的 `low-level feature + channel reduction + two 3×3 conv`
- `output stride` 是精度和成本的重要控制旋钮，这个思想可以借

### 15.2 可以作为候选参数来源的

- `crop size 513×513` 可作为接近 `512×512` 的外部候选参考
- `poly lr + random scale augmentation`
- `OS=16` 作为速度和精度平衡的常见起点

### 15.3 不应照搬的（及原因）

- `PASCAL / Cityscapes` 的 mIOU 数字
  - 原因：和腺体分割完全不是同一任务与协议
- `COCO / JFT` 预训练增强策略
  - 原因：当前项目不具备同级别外部预训练条件
- 语义分割整套 decoder 细节直接作为实例腺体主线
  - 原因：腺体任务更需要对象级分离与边界处理，不能只看语义区域

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 是否需要强外部对比 | `DeepLabV3+` 是非常合适的强上下文基线 | 强 |
| 是否要加入轻量 decoder 修边界 | 论文明确证明简单 decoder 能改善边界 | 中 |
| 是否要直接照搬训练协议 | 只能借原则，不适合作为腺体固定值 | 弱 |
| 是否值得关注大感受野 | `ASPP + atrous conv` 明确展示多尺度上下文价值 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`
- [ ] 需要和哪篇论文交叉验证：`Large_Kernel_Matters_2018`、`U-Net_2015`、`MILD-Net_2018`
- [ ] 待确认的问题：`在腺体任务上，是把 DeepLabV3+ 只作为外部对比，还是抽取其 decoder 低层融合思想做模块参考`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 多尺度上下文与边界细化需要兼顾 | 作为大感受野路线动机 |
| related work | `ASPP + decoder` 的经典代表 | 放在强上下文外部对比路线 |
| 方法 | 若后续借用 low-level feature 融合，可引用其 decoder 设计 | 只引用结构思路，不冒充原样复现 |
| 实验设置 | `DeepLabV3+` 作为外部强基线名单之一 | 用于基线角色定义 |
| 讨论 | 可讨论“上下文强不等于实例分离强” | 用于解释外部强基线和腺体任务差异 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig.1` | `p.2` | spatial pyramid / encoder-decoder / DeepLabv3+ 三种结构对比 | 说明方法定位 |
| `Fig.2` | `p.4` | DeepLabv3+ 总体结构图 | 直接参考 encoder-decoder 组合方式 |
| `Fig.3` | `p.5` | depthwise separable / atrous separable conv 示意图 | 解释效率改进来源 |
| `Fig.4` | `p.7` | modified aligned Xception 结构图 | backbone 设计参考 |
| `Fig.5` | `p.13` | trimap 边界提升与 decoder 效果图 | 支撑 decoder 改善边界 |
| `Fig.6` | `p.14` | 可视化结果与 failure mode | 失败场景引用 |
| `Table 1` | `p.9` | decoder 1×1 通道数选择 | decoder 超参数依据 |
| `Table 2` | `p.9` | decoder 结构选择 | `two [3×3, 256]` 依据 |
| `Table 3` | `p.9-p.10` | ResNet-101 版 OS / decoder / MS / Flip 对比 | 外部对比与效率参考 |
| `Table 5` | `p.12` | Xception 版推理策略与 SC/COCO/JFT 对比 | 强版本对比参考 |
| `Table 6` | `p.13` | VOC test SOTA 结果 | 数字引用 |
| `Table 7` | `p.14` | Cityscapes val/test 结果 | 数字引用 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够复现（优化器+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查（stain normalization / patch overlap / label 生成）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认（不是只记指标名字）
- [x] 消融实验的结论已量化（不只是"有效"）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
