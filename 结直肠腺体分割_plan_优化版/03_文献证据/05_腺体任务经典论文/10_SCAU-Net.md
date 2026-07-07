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
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland semantic segmentation`
- `spatial attention + channel attention`
- `attention U-Net variant for GlaS/CRAG`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体任务里较直接的 attention U-Net 路线代表作，强调在 U-Net 骨架上插入空间注意力与通道注意力
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`SCAU-Net: Spatial-Channel Attention U-Net for Gland Segmentation`
- 作者/团队：`Peng Zhao, Jindi Zhang, Weijia Fang, Shuiguang Deng`
- 发表年份/会议/期刊：`2020, Frontiers in Bioengineering and Biotechnology`
- DOI / arXiv ID：`10.3389/fbioe.2020.00670`
- BibTeX key：`zhao2020scau`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/SCAU-Net_Spatial-Channel_Attention_U-Net_for_Gland_Segmentation_2020.pdf`
- 当前定位：`05` 目录中一篇很典型的 gland-specific attention 方法，重点不在实例级后处理，而在用 `SA + CA` 提升语义分割质量、边界辨识和 gland connectivity
- 与已提取论文的关系：
  - 与 [04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/04_MILD-Net.md) 一样都强调边界与多尺度特征，但本篇把重点放在显式 attention recalibration
  - 与 [09_AttentionBoost.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/09_AttentionBoost.md) 形成对照：SCAU-Net 预定义“在哪里/哪些通道更重要”，AttentionBoost 则由错误驱动动态关注 hard pixels
  - 与 [07_TA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/07_TA-Net.md) 不同：本篇仍是语义分割口径，不显式建模 topology、markers 或实例后处理

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：腺体在 H&E 病理中与腺癌分级密切相关，而 size、shape、location 等 gland information 对诊断和治疗前后评估都有价值。
  - 用途：`任务背景 / 临床动机`
  - 页码：`p.1`
- 句子/事实 2：SCAU-Net 的核心动机是增强 local related features、抑制 irrelevant features，尤其让模型更多关注 gland 的模糊边界。
  - 用途：`方法动机`
  - 页码：`p.1-p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者把 spatial attention 与 channel attention 设计为 plug-and-play 模块，可嵌入基本 encoder-decoder 结构。
  - 用途：`模块定位 / related work`
  - 页码：`p.2-p.4`
- 句子/事实 2：SCAU-Net 相比经典 U-Net 在 `GlaS` 和 `CRAG` 上都有提升，且可视化表明其更有利于保持 gland object connectivity、抑制背景噪声与减少 sticking。
  - 用途：`任务内有效性论证`
  - 页码：`p.1, p.6-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入尺寸 | `512 x 512` | 训练设置 | `p.5` |
| GlaS 官方规模 | `85 train / 80 test` | 数据集说明 | `p.5` |
| CRAG 划分 | `173 train / 40 test` | 数据集说明 | `p.5` |
| 损失 | `0.5 * CE + 0.5 * Dice` | 训练设置 | `p.5` |
| 优化器 | `Adam, lr = 1e-4` | 训练设置 | `p.5` |
| batch size | `4` | 训练设置 | `p.5` |
| epoch | `100` | 训练设置 | `p.5` |
| lr decay | `every 30 epochs x0.1` | 学习率调度 | `p.5` |
| SA 隐藏通道 | `16` | 模块参数 | `p.5` |
| CA 隐藏神经元 | `32` | 模块参数 | `p.5` |
| 最佳 GlaS Dice | `0.9063` | 主结果 | `Table 1, p.5` |
| 最佳 CRAG Dice | `0.9100` | 主结果 | `Table 1, p.5` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 腺体形态在不同分化等级下变化复杂，texture 与 size 也存在明显个体差异，因此自动分割仍然困难。
- U-Net 这类 encoder-decoder 骨架虽有效，但没有显式区分“哪些位置”和“哪些通道”更重要。
- 对 gland slices 而言，模糊边界、背景噪声和多腺体相邻粘连是主要误差来源。
- 作者认为 attention 应重点帮助模型强化相关局部特征，并抑制杂乱背景。

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- SCAU-Net 以 U-Net 式 encoder-decoder 为骨架，在低层特征图上加入 `Spatial Attention (SA)`，在 encoder 最后层加入 `Channel Attention (CA)`，通过全局聚合 + 小型自学习映射生成空间权重图与通道权重向量，再对原特征做 recalibration。作者认为浅层更适合做边缘/轮廓级空间关注，深层更适合做语义级通道筛选；最终输出仍是二分类 gland mask，并在 `GlaS` 与 `CRAG` 上用 `Dice / Jaccard / RVD` 评估。

关键页码：

- `p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`encoder-decoder symmetric U-Net with SA and CA modules`
- Backbone：`U-Net style CNN`
- 基本块：`Block(x) = Conv(3x3) + BN + ReLU` 重复两次
- 下采样：`2x2 max-pooling`
- 上采样：`bilinear interpolation`
- 输出头：`1x1 conv -> 2 classes`
- attention 插入位置：
  - `SA` 放在低层特征图
  - `CA` 放在 encoder 最后层高层特征图

### 3.2 关键模块详细描述

**模块 1：`Encoder-Decoder Backbone`**

- 位置：`整体主干`
- 操作流程：
  1. encoder 逐层提取特征并在每次下采样后减小空间尺寸、增加通道数
  2. decoder 对应恢复空间分辨率
  3. 通过 copy/skip connection 融合对应层高低级特征
  4. 最终用 `1x1` 卷积预测二类 mask
- 页码：`p.3-p.4`

**模块 2：`Spatial Attention (SA)`**

- 位置：`低层 feature map`
- 操作流程：
  1. 对输入特征 `U in R^(C x H x W)` 在通道维做全局平均池化，得到空间描述子 `p in R^(H x W)`
  2. 用两层 `3x3` 卷积 + `ReLU` + `sigmoid` 生成空间权重图 `t`
  3. 将每个空间位置的原特征乘以对应权重，实现 spatial-wise recalibration
- 设计理由：低层特征更强调 contour、edge 等空间信息
- 页码：`p.3-p.4`

**模块 3：`Channel Attention (CA)`**

- 位置：`encoder 最后一层高层 feature map`
- 操作流程：
  1. 对输入特征 `U` 在空间维做全局平均池化，得到通道描述子 `q in R^C`
  2. 用两层全连接层 + `ReLU` + `sigmoid` 生成通道权重 `v`
  3. 将每个通道特征乘以对应权重，实现 channel-wise recalibration
- 设计理由：高层特征具有更大感受野和更丰富语义信息，适合做通道选择
- 页码：`p.4`

**模块 4：`Attention Placement Strategy`**

- 位置：`模块配置逻辑`
- 操作流程：
  1. SA 不与 CA 并联到所有层
  2. SA 只用于 low-level spatial feature
  3. CA 只用于 encoder 末端的 high-level semantic feature
  4. 最终主模型是 `SA + CA` 联合配置
- 页码：`p.3-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 输入 | RGB image | `3` | `512x512` | 训练与推理都统一到固定尺寸 |
| Encoder block | `Block(x)` + pooling | `逐层翻倍` | `逐层减半` | 正文未逐层列出精确通道表 |
| SA module | `avg over channel + 3x3 conv + 3x3 conv` | `hidden m = 16` | `H x W` | 作用于低层特征 |
| Bottleneck / high-level encoder | feature map | `未逐层明示` | `低分辨率` | 接 CA |
| CA module | `avg over spatial + FC + FC` | `hidden K = 32` | `C` | 作用于高层特征 |
| Decoder block | upsample + skip fusion | `逐层减半` | `逐层放大` | bilinear interpolation |
| 输出层 | `1x1 conv` | `2 classes` | `512x512` | gland vs background |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
p_hw = F_ac(u_hw) = (1 / C) * sum_{i=1..C} u_hw(i)
```

符号说明：
- `U in R^(C x H x W)`：输入特征图
- `u_hw`：位置 `(h, w)` 上的通道向量
- `p_hw`：空间描述子
- 含义：在通道维做全局平均池化，得到每个空间位置的总体响应
- 页码：`Eq.(1), p.3`

公式 2：

```text
t = F_l(p, f) = sigma(g(p, f)) = sigma(f2 * delta(f1 * p))
```

符号说明：
- `t in R^(H x W)`：空间权重图
- `f1`：`Conv(3x3, m)`
- `f2`：`Conv(3x3, 1)`
- `delta`：`ReLU`
- `sigma`：`sigmoid`
- 含义：两层卷积学习空间相关性，生成 `0-1` 之间的位置权重
- 页码：`Eq.(2), p.3`

公式 3：

```text
u'_hw = F_re(u_hw, t_hw) = u_hw * t_hw
```

符号说明：
- `u'_hw`：SA 之后的位置特征
- 含义：对不同位置赋不同权重，强化关键区域、抑制无关区域
- 页码：`Eq.(3), p.3`

公式 4：

```text
q_c = F_as(u_c) = (1 / (H * W)) * sum_i sum_j u_c(i, j)
```

符号说明：
- `u_c`：第 `c` 个通道的二维特征图
- `q_c`：通道描述子
- 含义：在空间维做全局平均池化，得到每个通道的全局响应
- 页码：`Eq.(4), p.4`

公式 5：

```text
v = F_l(q, w) = sigma(g(q, w)) = sigma(w2 * delta(w1 * q))
```

符号说明：
- `v in R^C`：通道权重向量
- `w1 in R^(K x C), w2 in R^(C x K)`
- `K`：隐藏层神经元数
- 含义：通过两层全连接学习通道间非线性依赖
- 页码：`Eq.(5), p.4`

公式 6：

```text
u'_c = F_re(u_c, v_c) = u_c * v_c
```

符号说明：
- `u'_c`：CA 之后的通道特征
- 含义：对重要通道增强、对无关通道抑制
- 页码：`Eq.(6), p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇没有展开严格的梯度推导，核心是 attention-based feature recalibration，而非新损失的理论证明。
- 从实现角度看，`sigmoid` 产生的空间/通道权重直接参与逐点乘法，因此梯度可同时回传到主干特征与 attention 生成分支。

---

## 5. 损失函数

### 5.1 各监督项

- `CELoss`：像素级二分类交叉熵
- `DiceLoss`：基于 Dice coefficient 的区域重叠项
- 任务类型：`binary semantic segmentation`

### 5.2 总损失公式

```text
CELoss = -(1 / n) * sum [ y * log(y') + (1 - y) * log(1 - y') ]

DiceLoss = 2 * sum(y' * y) / (sum y' + sum y)

Loss = lambda * CELoss + (1 - lambda) * DiceLoss
```

说明：

- `y`：ground truth
- `y'`：prediction
- 论文正文按上式书写；其中 `DiceLoss` 更接近 Dice 系数形式，正文没有再显式写 `1 - Dice`
- 页码：`Eq.(7)-(9), p.5`

### 5.3 权重配置与调度策略

- `lambda = 0.5`
- 等价于 `0.5 * CE + 0.5 * Dice`
- 学习率从 `1e-4` 开始，每 `30 epochs` 衰减为前一值的 `1/10`

---

## 6. 训练协议

### 6.1 数据集与划分

- `GlaS`
  - 文中先写官方划分：`85 train / 80 test`
  - 但紧接着又写“from 165 images using 80% for training and 20% for testing”
  - 这意味着正文对 `GlaS` 的最终实际划分存在表述冲突
- `CRAG`
  - `173 train / 40 test`
- 图像属性：
  - `GlaS` 多数尺寸约 `780 x 520`
  - `CRAG` 多数尺寸约 `1510 x 1510`
- 标注提供者：`expert pathologists`

### 6.2 数据增强

- 随机旋转
- 随机缩放
- 随机裁剪
- 目的：提升鲁棒性、减轻小数据集过拟合

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| 框架 | `PyTorch` |
| 系统 | `Ubuntu 16.04` |
| GPU | `NVIDIA Tesla K80` |
| CUDA | `10.1` |
| optimizer | `Adam` |
| initial lr | `1e-4` |
| batch size | `4` |
| total epochs | `100` |
| lr schedule | `every 30 epochs x0.1` |
| SA hidden channels | `16` |
| CA hidden neurons | `32` |

### 6.4 预处理与数据细节

- 所有输入统一 resize 或处理为 `512 x 512`
- 论文只概括写了 augmentation 类型，没有给出精确概率、缩放范围、裁剪策略顺序
- 未明确颜色归一化、 stain normalization、像素归一化均值方差
- 未报告随机种子、验证集构造方式

---

## 7. 推理与后处理

- 推理输出是二值语义分割 mask，而非实例级标签图
- 论文未描述额外后处理，例如 watershed、morphology、connected components 策略
- 训练过程中以 `Dice` 作为保存最佳模型的主评价指标
- 推理阶段的阈值选择未明示，正文默认是标准二分类分割输出

---

## 8. 消融实验

### 8.1 消融设计

- 主消融围绕 attention 模块配置展开：
  - `U-Net` baseline
  - `SCAU-Net(CA)` 仅通道注意力
  - `SCAU-Net(SA)` 仅空间注意力
  - `SCAU-Net(SA+CA)` 空间与通道联合
- 消融数据集：
  - `GlaS`
  - `CRAG`
- 评价指标：
  - `Dice`
  - `Jaccard`
  - `RVD`

### 8.2 各模块贡献量化

| 配置 | GlaS Dice | GlaS Jaccard | CRAG Dice | CRAG Jaccard | 结论 |
|------|-----------|--------------|-----------|--------------|------|
| `U-Net` | `0.8963` | `0.8175` | `0.9003` | `0.8243` | baseline |
| `CA` | `0.9004` | `0.8242` | `0.9069` | `0.8333` | 单独 CA 有稳定增益 |
| `SA` | `0.9054` | `0.8322` | `0.9067` | `0.8330` | 单独 SA 在 GlaS 上略优于 CA |
| `SA+CA` | `0.9063` | `0.8332` | `0.9100` | `0.8381` | 联合配置最佳 |

- 相对 `U-Net`：
  - `GlaS` 上 `SA+CA` 的 Dice 提升约 `+1.0%`
  - `GlaS` 上 Jaccard 提升约 `+1.6%`
  - `CRAG` 上 Dice 提升约 `+1.0%`
  - `CRAG` 上 Jaccard 提升约 `+1.4%`
- 训练动态：
  - `SA+CA` 在验证集上达到最高准确率
  - `GlaS` 上约 `60th epoch` 后出现轻微过拟合
  - 作者认为 attention 增加参数量后，在小数据集上更易过拟合

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS` | `Dice = 0.9063` | `Jaccard = 0.8332` | `RVD = 0.0197` | 最佳模型为 `SA+CA` |
| `CRAG` | `Dice = 0.9100` | `Jaccard = 0.8381` | `RVD = -0.0074` | 最佳模型为 `SA+CA` |

### 9.2 与其他方法的对比

| 方法 | GlaS Dice | GlaS Jaccard | CRAG Dice | CRAG Jaccard |
|------|-----------|--------------|-----------|--------------|
| `SegNet` | `0.7930` | `0.6643` | `0.8990` | `0.8209` |
| `U-Net` | `0.8963` | `0.8175` | `0.9003` | `0.8243` |
| `U-Net++` | `0.8952` | `0.8166` | `0.8870` | `0.8010` |
| `DeepLabv3+` | `0.8866` | `0.7994` | `0.8672` | `0.7691` |
| `SCAU-Net(SA+CA)` | `0.9063` | `0.8332` | `0.9100` | `0.8381` |

- 任务内解读：
  - SCAU-Net 在两套数据上都优于文中列出的 `U-Net / U-Net++ / DeepLabv3+ / SegNet`
  - 其提升主要体现为语义分割口径下的 overlap 指标改善
  - 论文没有报告对象级 `F1 / object-Dice / Hausdorff`，因此不能与 GlaS challenge 口径论文直接一一对齐

### 9.3 公平对比条件确认

- 正文没有详细说明对比方法是否全部按同一数据划分、同一增强与同一训练轮数重新训练
- `GlaS` 划分存在“官方 split”与“80/20 random split”两种写法，影响横向公平性判断
- 指标使用 `Dice / Jaccard / RVD`，而非腺体任务更常见的 object-level 三指标
- 因此本篇更适合用来证明 attention 模块对 gland semantic segmentation 的有效性，而不是用作 challenge 榜单级严格横向比较

### 9.4 评价协议与指标定义

公式 1：

```text
Dice = 2 * (A ∩ B) / (A + B)
```

公式 2：

```text
Jaccard = (A ∩ B) / (A ∪ B)
```

公式 3：

```text
RVD = (|B| - |A|) / |A|
```

说明：

- `A`：ground truth gland pixel set
- `B`：predicted gland pixel set
- 只按二值语义分割计算，前景为 glands，其他全部视为 background
- 页码：`Eq.(10)-(12), p.5`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未报告`
- 显存占用：`未报告`
- 间接效率信息：
  - 训练环境为 `Tesla K80`
  - 作者提到 attention 增加了参数量，使小数据集上更易过拟合
- 对复现的意义：
  - 这篇可提供 attention placement 思路，但几乎不能提供可复现实验成本预算

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，没有提出系统性的任务分类框架。

### 11.2 论文指出的研究空白 / Open Problems

- 传统 encoder-decoder 结构未显式区分空间与通道的重要性。
- 小型医学数据集下，如何在不显著破坏 U-Net 简洁性的前提下提升相关特征选择能力，仍是开放问题。

### 11.3 对我们选题的启示

- 即使不做复杂实例图建模，仅通过“浅层看空间、深层看通道”的 attention placement，也能在 gland 任务上带来稳定收益。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 论文提到腺体分化等级与 morphology 相关，但没有给出正式病理分级标准表。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 更好的 gland segmentation 可帮助病理医生更快获得与疾病过程相关的数字化形态信息。
- 论文明确把 gland 的 `size / shape / location` 与后续治疗评估联系起来。
- 页码：`p.1`

---

## 13. 开源与复现

- 代码是否开源：`文中未说明，当前未见代码地址`
- 代码仓库地址：`未提供`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中`
- 复现障碍：
  - `GlaS` 划分表述冲突
  - 未报告随机种子、验证集、阈值与完整预处理
  - 未给出参数量、速度和逐层通道配置

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| `GlaS` 最终使用哪种划分 | 否 | 记录为“官方 split 与 80/20 split 存在冲突” | 高 |
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集构造 | 否 | 仅记录“以 Dice 保存最佳模型” | 中 |
| 归一化/染色预处理 | 否 | 仅确认固定输入尺寸 `512x512` | 中 |
| 推理阈值 | 否 | 视为标准二分类输出，但不脑补阈值 | 中 |
| 逐层通道表 | 否 | 只保留 `Block(x)` 与“通道逐层翻倍”的文字描述 | 低 |
| baseline 重训练协议 | 否 | 不假设完全同训同增广 | 高 |

- 不确定但影响较大的点：
  - `GlaS` 是否真的用了官方 `85/80` 划分
  - 所有对比方法是否共享同一训练协议
  - 训练时是否存在额外阈值选择或验证集 early model selection 细节

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- `GlaS` 上 `SA+CA` 在约 `60 epoch` 后出现轻微过拟合。
- 作者认为 attention 增加参数量，使模型在小数据集上更容易过拟合。
- 作者在结论中明确表示，未来仍需探索：
  - 卷积层数量
  - 全连接层数量
  - 模块嵌入位置
- 页码：`p.6-p.7`

### 14.2 我们观察到的潜在问题

- 方法仍是语义分割，不直接解决 gland instance separation。
- 指标体系不是 gland challenge 常见的 object-level 口径，因此对“真正的腺体分离能力”反映有限。
- 论文对公平对比条件、数据划分和复现细节交代不足。
- attention 收益存在，但增益幅度总体属于小幅稳定改善，不是范式级跳变。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未以“failure cases”专节呈现，但给出可视化对比`
- 定性结论：
  - `U-Net` 容易把 gland 内白色区域误判为背景
  - 在复杂背景下，SCAU-Net 更能压制噪声
  - 在多个 gland 相邻时，SCAU-Net 更能防止 “sticking”
- 页码：`Fig.5, p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `浅层加 SA、深层加 CA` 的模块放置思路
- `0.5 * CE + 0.5 * Dice` 这组 gland 任务内常见损失配比
- `512x512`, `Adam 1e-4`, `batch size 4`, `100 epochs` 这一组可作为首轮实验参数参考
- attention weights 可视化的解释方式

### 15.2 可以作为候选参数来源的

- `SA hidden channels = 16`
- `CA hidden neurons = 32`
- `lr decay every 30 epochs x0.1`
- `Dice` 作为模型选择指标

### 15.3 不应照搬的（及原因）

- 不应直接照搬其结果表做横向结论
  - 原因：`GlaS` 划分与公平对比条件不清晰
- 不应把本篇结果当作 instance segmentation 证据
  - 原因：它只报告语义分割指标
- 不应忽略对象级指标
  - 原因：我们的任务重点仍然是 gland separation 与 morphology-level usefulness

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 浅层边缘增强分支 | SA 放低层特征、强调模糊边界 | 强 |
| 深层语义筛选 | CA 放高层特征、做通道重标定 | 强 |
| 训练首参选择 | `512x512 + Adam 1e-4 + batch 4 + 100 epochs` | 中 |
| 结果解释 | 更好 connectivity、噪声抑制与 anti-sticking | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`主线实验矩阵与注意力模块候选表`
- [ ] 需要和哪篇论文交叉验证：`04_MILD-Net.md`, `07_TA-Net.md`, `09_AttentionBoost.md`
- [ ] 待确认的问题：`我们是否需要在自己的 U-Net 基线上加一个轻量 SA/CA 版本作为 attention baseline`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland morphology 与 H&E 场景重要性 | 任务背景 |
| related work | gland-specific attention U-Net 路线 | 方法脉络 |
| 方法 | `SA at low-level, CA at high-level` | 模块动机 |
| 实验设置 | `512x512`, `Adam`, `CE+Dice` | 超参数依据 |
| 讨论 | semantic 指标提升但 instance 能力有限 | 边界说明 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.4` | SCAU-Net 总体结构 | 主架构引用 |
| `Fig. 2` | `p.4` | Spatial Attention 模块 | SA 公式对应 |
| `Fig. 3` | `p.4` | Channel Attention 模块 | CA 公式对应 |
| `Table 1` | `p.5` | GlaS/CRAG 主结果与消融 | 主表结果 |
| `Fig. 4` | `p.6` | U-Net 与各 attention 配置训练曲线 | 过拟合与收敛解释 |
| `Fig. 5` | `p.6` | 可视化分割对比 | connectivity / anti-sticking |
| `Fig. 6` | `p.7` | SA 权重与特征图可视化 | attention 解释性 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（仍缺验证集、seed、预处理等）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已明确标出而未脑补
