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
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `mucous gland instance-oriented segmentation`
- `contour-aware loss`
- `multiscale + non-local U-Net variant`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是面向 `mucous glands` 的专门分割论文，强调不只是腺体前景分割，还要做 individual gland identification
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Automatic Mucous Glands Segmentation in Histological Images`
- 作者/团队：`A. Khvostikov, A. Krylov, I. Mikhailov, O. Kharlova, N. Oleynikova, P. Malkov`
- 发表年份/会议/期刊：`2019, The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences / Photogrammetric & Computer Vision Techniques for Video Surveillance, Biometrics and Biomedicine Workshop`
- DOI / arXiv ID：`10.5194/isprs-archives-XLII-2-W12-103-2019`
- BibTeX key：`khvostikov2019mucous`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Automatic_Mucous_Glands_Segmentation_in_Histological_Images_2019.pdf`
- 当前定位：`05` 目录里一篇比较特殊但很有价值的实例分离导向论文，面向 colon biopsy 中的 `mucous glands`，兼顾标准 `Warwick-QU` 与作者自建 `PATH-DT-MSU` 数据
- 与已提取论文的关系：
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/03_DCAN.md) 一样都强调 contour 对 gland separation 的作用，但本篇不用双输出分支，而是把 contour 信息写进 loss
  - 与 [06_Object-Graphs.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/06_Object-Graphs.md) 共同点是都把“相邻腺体分开”视为核心目标，但本篇转向 CNN 路线
  - 与 [08_Deep-Multichannel.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/08_Deep-Multichannel.md) 对照鲜明：后者显式 region/edge/location 三路融合，本篇走更轻的 `single-output + contour-aware loss` 路线

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：`mucous glands` 是消化病理里的重要诊断元素，而结肠息肉恶性潜能评估的第一步就是 gland segmentation。
  - 用途：`任务背景 / 临床动机`
  - 页码：`p.1`
- 句子/事实 2：任务不只是把 glands 从背景里分出来，还必须完成 `individual gland identification`，否则无法获得可靠的 morphometric criteria。
  - 用途：`实例分离动机`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者提出的 CNN 基于 U-Net，但通过 `contour-aware loss`、multiscale input 和 deepest-layer non-local block 来增强 stuck glands 的分离能力。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.3`
- 句子/事实 2：与 DCAN 那类双输出 gland/contour 分支不同，本篇通过对网络输出施加 Sobel 获取 contour probability map，并把 contour Dice 直接写进总损失。
  - 用途：`方法差异点`
  - 页码：`p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| Warwick-QU 使用子集 | `37 train / 37 eval, benign only` | 数据集说明 | `p.3` |
| PATH-DT-MSU | `20 images` | 数据集说明 | `p.3` |
| PATH-DT-MSU 组成 | `13 HP + 6 SSA/P + 1 normal` | 数据集说明 | `p.3` |
| 多尺度输入 | `0.5x / 1x / 2x` | 模型结构 | `p.2` |
| 对应 patch 尺寸 | `128x128 / [疑似 256x256] / 512x512` | 模型结构 | `p.2` |
| 数据增强倍率 | `tau = 10` | 数据增强 | `p.4` |
| 第一阶段 optimizer | `RMSProp, lr = 2e-3` | 训练设置 | `p.4` |
| 第一阶段 batch size | `8` | 训练设置 | `p.4` |
| lr 调度 | `plateau 时 x0.1` | 训练设置 | `p.4` |
| early stopping | `metric 10 epochs 内变化 < 1e-4` | 训练设置 | `p.4` |
| 第二阶段 lr | `2e-4` | fine-tuning 设置 | `p.4` |
| Warwick-QU 结果 | `Dice 0.92 / object Dice 0.88` | 主结果 | `p.5` |
| PATH-DT-MSU 结果 | `Dice 0.78 / object Dice 0.77` | 主结果 | `p.5-p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 传统 gland segmentation 方法在某些医疗病例上稳定性不足，精度也不够支持定量诊断。
- 经典语义分割 CNN 很难把 close 或 contiguous 的 gland objects 分开。
- 在病理应用里，若不能单独识别每个 gland，就无法做可靠的 morphometric analysis。
- PATH-DT-MSU 这类全视野活检图像还引入了 `open glands`、近腔面 glands 和全局组织背景等更复杂问题。

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出一个基于 U-Net 的 patch-oriented CNN，用 `multiscale input` 提供不同尺度上下文，在最深层加入 `non-local block` 建模长程依赖，并把 gland contour 信息通过 `contour-aware loss` 直接写进训练目标。网络仍输出单个 gland probability map，但对该输出施加 Sobel 得到 contour probability map，再把 `gland Dice loss` 与 `contour Dice loss` 按动态权重组合。训练上先在 `Warwick-QU` 的 benign subset 上学通用腺体表示，再在作者自建的 `PATH-DT-MSU` 上做 fine-tuning，以适应更真实、更复杂的 mucous gland 场景。

关键页码：

- `p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`U-Net based patch-oriented CNN`
- Backbone：`U-Net variant`
- 关键增强：
  - `multiscale input block`
  - `deepest-layer non-local block`
  - `contour-aware combined Dice loss`
- 输出头：`single gland probability map`
- 目标定位：`semantic output + instance-oriented separation tendency`

### 3.2 关键模块详细描述

**模块 1：`Patch-Oriented U-Net Backbone`**

- 位置：`整体主干`
- 操作流程：
  1. 输入固定大小 patch
  2. 经 encoder-decoder 主干提取并恢复分割特征
  3. 输出 gland segmentation probability map
  4. 测试时对整图切 patch，再把 patch 结果 merge 回去
- 页码：`p.2-p.3`

**模块 2：`Contour-Aware Loss Path`**

- 位置：`训练目标`
- 操作流程：
  1. 对网络输出施加 Sobel filter
  2. 得到 contour probability map
  3. 分别计算 contour Dice loss `Lc` 与 gland Dice loss `Lg`
  4. 用动态权重 `alpha` 组合成总损失
- 设计理由：显式鼓励相邻黏连 glands 的边界分离，但不额外增加第二输出分支
- 页码：`p.2`

**模块 3：`Multiscale Input Block`**

- 位置：`输入端`
- 操作流程：
  1. 原始 patch 作为 `1x`
  2. 同时输入 `0.5x` 和 `2x` 尺度 patch
  3. 让模型同时看到局部细节和更大范围上下文
- 文中给出的尺度示例：
  - `128x128`
  - `[疑似 256x256]`
  - `512x512`
- 页码：`p.2-p.3`

**模块 4：`Non-Local Block`**

- 位置：`最深层`
- 操作流程：
  1. 在 deepest layer 插入一个 non-local block
  2. 建模图像结构的 long-range dependencies
  3. 作者指出它还能正向影响 convergence time
- 约束：只放 `1` 个 non-local block，因为 GPU 显存有限
- 页码：`p.3`

**模块 5：`Patch Merging Strategy`**

- 位置：`推理阶段`
- 操作流程：
  1. 测试图像切成 patches
  2. patch 间采用 `1/4 patch size` overlay
  3. merge 时对重叠区域做 averaging
  4. 只信任 patch 中央区域，以减轻 padding 与多尺度输入带来的边缘伪差
- 页码：`p.3`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 输入 | multiscale patches | `3 scales` | `128 / [256?] / 512` | 正文 OCR 抽取中间尺度异常，疑似 `256x256` |
| 主干 | `U-Net based CNN` | `未逐层明示` | `patch-oriented` | 输出 gland map |
| 轮廓路径 | `Sobel on output` | `1` | 同输出 | 仅用于训练 loss |
| 上下文模块 | `non-local block` | `1 block` | deepest layer | 建模长程依赖 |
| 推理合并 | overlapping patch merge | `N/A` | full image | `1/4 patch overlay + averaging` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L = alpha * Lc + (1 - alpha) * Lg
```

符号说明：
- `Lc`：contour map 上的 Dice loss
- `Lg`：gland map 上的 Dice loss
- `alpha`：动态权重，训练初期从 `0` 开始，逐步升到 `0.5`
- 含义：先让模型更稳定地学 gland map，再逐步加强 contour supervision
- 页码：`p.2`

公式 2：

```text
D(G, S) = 2 * |G ∩ S| / (|G| + |S|)
```

符号说明：
- `G`：ground truth gland pixel set
- `S`：predicted gland pixel set
- 含义：标准 Dice score
- 页码：`p.5`

公式 3：

```text
D_object(G, S) =
  (1 / 2) * [
    sum_{i=1..nS} w_i * D(G_i, S_i) +
    sum_{j=1..nG} w_tilde_j * D(G_tilde_j, S_tilde_j)
  ]
```

符号说明：
- `S_i`：第 `i` 个预测对象
- `G_i`：与 `S_i` 最大重叠的真值对象
- `G_tilde_j`：第 `j` 个真值对象
- `S_tilde_j`：与 `G_tilde_j` 最大重叠的预测对象
- `w_i`、`w_tilde_j`：按对象面积归一化的权重
- `nS`、`nG`：预测对象数与真值对象数
- 含义：对象级 Dice，更适合 instance segmentation 评价
- 页码：`p.5-p.6`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本文没有给出 contour-aware loss 的理论推导。
- 从训练策略看，`alpha` 从 `0` 平滑升至 `0.5`，说明作者希望先稳定学习 gland foreground，再逐步引入 contour 分离压力。

---

## 5. 损失函数

### 5.1 各监督项

- `Lg`：gland segmentation Dice loss
- `Lc`：contour map Dice loss
- contour map 来源：对网络输出施加 `Sobel filter`

### 5.2 总损失公式

```text
L = alpha * Lc + (1 - alpha) * Lg
```

补充说明：

- 本篇与 DCAN 的关键不同是：不是双输出头分别监督，而是单输出后再计算 contour map
- 这种设计减少了显式分支复杂度，但仍把边界信息直接纳入优化目标

### 5.3 权重配置与调度策略

- `alpha` 初始为 `0`
- 在若干 epoch 内平滑增至 `0.5`
- 正文未给出精确升温函数或持续 epoch 数

---

## 6. 训练协议

### 6.1 数据集与划分

- `Warwick-QU`
  - 来自 `MICCAI 2015 Gland Segmentation Challenge`
  - 本文只用 `benign subset`
  - `37 train / 37 evaluation`
  - 分辨率 `0.62 um/pixel`
- `PATH-DT-MSU`
  - 作者自建
  - `20` 张全视野 H&E 结肠活检图像
  - 组成：`13 HP + 6 SSA/P + 1 normal`
  - 标注包含 `open glands`

### 6.2 数据增强

- on-the-fly augmentation
- 随机裁剪
- 随机平移
- 随机旋转
- 随机缩放
- 随机翻转
- 非线性变换
- 随机亮度变化
- 增强倍率参数：`tau = 10`
- 多尺度输入的三个尺度同步做增强

### 6.3 优化器与超参数

| 项目 | 第一阶段 | 第二阶段 |
|------|---------|---------|
| 训练目标 | `Warwick-QU pretrain` | `PATH-DT-MSU fine-tune` |
| optimizer | `RMSProp` | `RMSProp` |
| initial lr | `2e-3` | `2e-4` |
| batch size | `8` | `未单独重写，默认沿用相同设置` |
| lr schedule | `validation plateau 时 x0.1` | `同第一阶段` |
| stopping | `target metric 10 epochs 内变化 < 1e-4` | `同第一阶段` |

### 6.4 预处理与数据细节

- PATH-DT-MSU 在 fine-tuning 前整体下采样 `30%`
- 目的：让 PATH-DT-MSU 与 Warwick-QU 中 histological structures 的尺度更接近
- 输入是固定尺寸 patch，但 OCR 抽取出现 `256 x 2556` 异常，结合多尺度描述更像 `256 x 256`
- 推理时 patch 间有 `1/4` 重叠并做 averaging

---

## 7. 推理与后处理

- 推理是 patch-based full-image inference
- 关键细节：
  - 全图切 patch
  - patch 重叠比例为 `1/4 patch size`
  - merge 时对重叠区取平均
  - 只信任 patch 中央区域，以降低 padding 影响
- 这不是后处理型实例分离方法，没有额外的 watershed 或 graph growing
- 实例分离主要来自 contour-aware 训练目标和近边界区域建模能力

---

## 8. 消融实验

### 8.1 消融设计

- 严格意义上没有像 `SA/CA` 那样的模块化消融表
- 但正文比较了：
  - `Warwick-QU` 预训练结果
  - `PATH-DT-MSU` fine-tuning 且不含 `open glands` 标注
  - `PATH-DT-MSU` fine-tuning 且含 `open glands` 标注
- 这相当于对数据定义与目标类型做了任务级对比分析

### 8.2 各模块贡献量化

- 论文没有分别量化 multiscale、non-local、contour-aware loss 的独立增益
- 可量化的对比主要体现在 `PATH-DT-MSU` 的两种 fine-tuning 标注策略：

| 配置 | Dice | object Dice | 作者解读 |
|------|------|-------------|---------|
| `without open glands` | `0.78` | `0.77` | 容易把 open glands 过分分割 |
| `with open glands` | `0.77` | `0.70` | 更符合医学偏好，但更易把多个 open glands 合并 |

- 额外定性结论：
  - non-local block 被作者认为能改善 convergence time
  - contour-aware loss 被作者认为能帮助 detect and separate stuck glands
  - 但正文缺少逐模块 ablation table，因此这些更多属于作者解释而非严格量化证据

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Warwick-QU benign test` | `Dice = 0.92` | `object Dice = 0.88` | `instance merging remains` | 只使用良性子集 |
| `PATH-DT-MSU without open glands` | `Dice = 0.78` | `object Dice = 0.77` | `near-boundary deviation` | 更高 object Dice |
| `PATH-DT-MSU with open glands` | `Dice = 0.77` | `object Dice = 0.70` | `more medically preferable` | 医学意义上更合理 |

### 9.2 与其他方法的对比

- 正文没有给出完整横向对比表去系统比较 `U-Net / DCAN / Deep Multichannel` 等方法
- 更像是一篇任务型 workshop 论文，重点在提出方法并报告在两个数据源上的表现
- 可做的任务内定位：
  - 相比只做前景分割的普通 U-Net，本篇更强调 contour-aware training
  - 相比更重的多分支或多通道方法，本篇结构更简洁
  - 相比标准 GlaS 挑战集，`PATH-DT-MSU` 更贴近真实活检场景，因此结果更难

### 9.3 公平对比条件确认

- `Warwick-QU` 只使用 `benign subset`，不能直接与使用全 `GlaS` 数据集的论文横比
- `PATH-DT-MSU` 是作者自建数据集，任务难度和图像覆盖范围都与 Warwick-QU 不同
- 因此主结果适合解释“方法在更真实 mucous gland 场景中的迁移性”，不适合直接排 challenge 榜单

### 9.4 评价协议与指标定义

公式 1：

```text
Dice = 2 * |G ∩ S| / (|G| + |S|)
```

公式 2：

```text
object Dice =
  (1 / 2) * [
    sum_i w_i * D(G_i, S_i) +
    sum_j w_tilde_j * D(G_tilde_j, S_tilde_j)
  ]
```

说明：

- `Dice` 评估像素级区域重叠
- `object Dice` 用于 instance-level 评价，更适合衡量 individual gland identification
- 论文明确指出：单纯 Dice 不足以评估 individual objects

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未报告`
- 训练硬件：
  - `Intel i7-6700HQ + GeForce GTX 960M`
  - `FloydHub + Tesla K80`
- 间接效率信息：
  - 作者声称 non-local block 对 convergence time 有正向影响
  - 但没有提供严格 wall-clock 对比

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，没有正式提出分类框架。

### 11.2 论文指出的研究空白 / Open Problems

- close/contiguous glands 的分离仍然困难
- `open glands` 的建模与评价仍然不充分
- 只依赖局部 patch 仍不足以完整理解 colon lumen 与 muscularis mucosae 的全局关系

### 11.3 对我们选题的启示

- 这篇说明“边界建模”不一定非要用额外分支，也可以写进 loss
- 同时也提醒：当数据从 challenge crop 变成 full-slide biopsy 时，open glands 和全局组织结构会显著改变任务难度

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 论文涉及 `HP` 与 `SSA/P` 的差异诊断背景，但没有给出正式病理分级规范表。

### 12.2 涉及的生物标志物

- 结论中提到后续可分析 immunohistochemical markers，但本篇未直接做 biomarker 研究。

### 12.3 临床意义

- 可靠的 individual gland segmentation 是后续 morphometric criteria 建立的前提。
- 论文把 mucous gland 分割直接连接到 colon polyps malignant potential assessment。
- `open glands`、lumen 形态和细胞核-胞浆比等都被视为后续定量分析目标。

---

## 13. 开源与复现

- 代码是否开源：`文中未提供代码`
- 代码仓库地址：`未提供`
- 数据是否可得：
  - `PATH-DT-MSU` 文中称将发布到 `http://imaging.cs.msu.ru/en/research/histology`
- 框架/语言：`Keras + TensorFlow`
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中`
- 复现障碍：
  - 主文 OCR 抽取存在 patch 尺寸异常
  - 没有逐层结构表
  - `alpha` 调度函数未明示
  - PATH-DT-MSU 获取状态需额外核查

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 中间输入 patch 尺寸 | 否 | 标记为 `[疑似 256x256]`，不脑补写死 | 高 |
| `alpha` 具体升温曲线 | 否 | 仅记录 `0 -> 0.5` | 中 |
| 逐层通道/卷积核配置 | 否 | 只记录 `U-Net based` | 中 |
| 验证集划分 | 部分 | 只记录 plateau 与 stopping 规则 | 中 |
| 随机种子 | 否 | 不假设固定 seed | 中 |
| PATH-DT-MSU 下载状态 | 部分 | 记录发布网址，不假设当前可获取 | 中 |
| 测试阈值 | 否 | 仅记录 patch merge 逻辑 | 低 |

- 不确定但影响较大的点：
  - `256 x 2556` 是否确为 OCR 错误
  - batch size 在第二阶段是否完全沿用第一阶段
  - `open glands` 标注准则细节

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 即便在 Warwick-QU 上结果较好，close glands 仍可能 merged together。
- PATH-DT-MSU 上的主要偏差集中在 `near-boundary glands`。
- 只基于局部 patch 的方法不足以充分理解 colon lumen 与 muscularis mucosae 的全局结构。
- 对 `open glands` 的建模仍需更全局的大尺度分析。

### 14.2 我们观察到的潜在问题

- 这篇属于 workshop 短文，消融与横向对比较弱。
- 虽然强调 instance separation，但没有真正输出独立实例标签或对象后处理流程。
- `Warwick-QU` 只用 benign subset，任务设置与常见腺体分割论文并不完全一致。
- 结果段出现 `Warwick-QU object Dice 0.88` 与结论段 `0.87` 的轻微不一致，应以主结果段为主并标记该差异。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`间接展示`
- 典型失败情形：
  - close lying glands 被合并
  - near-boundary glands 偏差较大
  - 不含 `open glands` 标注训练时会出现 over-segmentation
  - 含 `open glands` 标注训练时又可能把多个 open glands 合并
- 页码：`Fig.7-Fig.9, p.5-p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `contour-aware loss` 的思路
- `Warwick-QU pretrain -> 真实数据 fine-tune` 的迁移策略
- patch overlap averaging 的整图推理方式
- 用 `object Dice` 补充普通 Dice 的实例级评价习惯

### 15.2 可以作为候选参数来源的

- `RMSProp`
- `lr = 2e-3 / 2e-4`
- `batch size = 8`
- `tau = 10`
- `1/4 patch overlay`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其 benign-only Warwick 设置
  - 原因：和主流 GlaS 全数据或 challenge 设置不一致
- 不应把它当成完整实例分割方案
  - 原因：方法本质仍是单输出分割 + contour-aware training
- 不应忽略 `open glands` 这类数据定义问题
  - 原因：真实活检场景里的标注边界会直接改变评价结果

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界损失设计 | 通过 `alpha * Lc + (1-alpha) * Lg` 强调 contour | 强 |
| 多尺度输入 | `0.5x / 1x / 2x` 提供上下文 | 中 |
| 全局依赖建模 | deepest non-local block | 中 |
| 真实数据迁移 | challenge 数据到 biopsy 数据的两阶段训练 | 强 |
| 指标选择 | `Dice + object Dice` 双口径 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失设计备选路线表`、`真实数据迁移实验草案`
- [ ] 需要和哪篇论文交叉验证：`03_DCAN.md`, `08_Deep-Multichannel.md`, `09_AttentionBoost.md`
- [ ] 待确认的问题：`我们是否要尝试单输出 + contour-aware loss，而不是再开边界分支`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | mucous glands 与 colon polyps 诊断关联 | 任务背景 |
| related work | contour-aware loss 路线 | 方法脉络 |
| 方法 | 单输出 + Sobel contour supervision | loss 动机 |
| 实验设置 | 两阶段训练与真实数据适配 | 迁移策略 |
| 讨论 | open glands 与全局结构依赖 | 失败模式说明 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.2` | 提出的方法结构图 | 总体架构 |
| `Fig. 3` | `p.2-p.3` | multiscale input block | 多尺度设计 |
| `Fig. 4` | `p.3` | conv / upconv block | 结构细节 |
| `Fig. 5` | `p.5` | PATH-DT-MSU 样例与 open glands 标注 | 数据难点 |
| `Fig. 6` | `p.5` | Warwick-QU 第一阶段结果 | 主结果示例 |
| `Fig. 7` | `p.5-p.6` | PATH-DT-MSU 无 open glands 配置结果 | 失败模式 |
| `Fig. 8` | `p.6` | PATH-DT-MSU 含 open glands 配置结果 | 失败模式 |
| `Fig. 9` | `p.6` | 两种 fine-tuning 配置的 Dice/object Dice 曲线 | 训练动态 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（`alpha` 调度和结构细节仍缺）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table/正文一致（已标出 `0.88` 与 `0.87` 的文内差异）
- [x] 指标定义和评价协议已确认
- [ ] 消融实验的结论已量化（严格模块消融不足）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注为疑点而未脑补
