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
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `complex gland segmentation`
- `morphological constraints`
- `lumen-guided contour selection`
- `stain separation + classical contour optimization`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`06_半监督_拓扑_扩展工作`

- 本篇聚焦复杂、低分化、粘连腺体的分割，不走纯端到端 mask 预测，而是把 `stain separation`、`lumen segmentation`、`nuclear detection`、`morphological constraints` 串成一条混合流程
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Multiple Morphological Constraints-Based Complex Gland Segmentation in Colorectal Cancer Pathology Image Analysis`
- 作者/团队：`Kun Zhang, JunHong Fu, Liang Hua, Peijian Zhang, Yeqin Shao, Sheng Xu, Huiyu Zhou, Li Chen, Jing Wang`
- 发表年份/会议/期刊：`2020, Complexity`
- DOI / arXiv ID：`10.1155/2020/6180457`
- BibTeX key：`zhang2020multiple`
- PDF 路径：`结直肠腺体分割_pdf库/06_半监督_拓扑_扩展工作/Multiple_Morphological_Constraints-Based_Complex_Gland_Segmentation_in_Colorectal_Cancer_Pathology_Image_Analysis_2020.pdf`
- 当前定位：`06` 目录中最典型的“复杂 gland 形态约束”路线，尤其适合支撑 `poorly differentiated / adherent glands` 为什么不能只靠普通像素分割
- 与已提取论文的关系：
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/03_DCAN.md) 不同：`DCAN` 通过 gland/contour 双分支学习边界，本篇则显式利用 `lumen + rough boundary + epithelial nucleus` 形态约束选 contour
  - 与 [11_Automatic-Mucous-Glands.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/11_Automatic-Mucous-Glands.md) 相通：都强调实例分离和 contour，但本篇更偏“深度学习 + 几何/传统图像分析”混合框架
  - 与 [14_SkeletonAwareDT.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/14_SkeletonAwareDT.md) 互补：后者把结构信息编码进 dense prediction 表示，本篇则在后端 contour 选择时显式加入形态先验

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者明确指出，`poorly differentiated colorectal glands` 难以被准确分割，尤其在 malignant 场景下 epithelial nuclei 容易与 stroma 混杂，且 glands 常相互粘连。
  - 用途：`任务痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者认为 `lumen` 是 gland 中更稳定、可定义的结构，其存在及形态还能反映癌症分级，因此可以作为复杂 gland 分割的重要内轮廓线索。
  - 用途：`方法动机 / 病理意义`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者提出的主线不是直接 end-to-end 分 gland，而是先做 `U-Net` stain separation，再在 `background channel` 上分 lumen，并借助 epithelial nucleus 与 rough gland boundary 选出最优 gland contour。
  - 用途：`方法脉络`
  - 页码：`p.1-p.3`
- 句子/事实 2：作者将核心创新概括为两点：一是用深度学习预测 stain coefficient interval 完成 stain separation；二是结合内轮廓 `lumen` 与外轮廓 `epithelium` 的多重形态约束，得到更精确的 gland contour。
  - 用途：`方法亮点`
  - 页码：`p.1, p.3, p.14`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 期刊 DOI | `10.1155/2020/6180457` | 文献信息 | `p.1` |
| 自建数据集 | `100` 张 colon adenocarcinoma 图像 | 数据集说明 | `p.7` |
| 自建数据患者数 | `34` 例 | 数据集说明 | `p.7` |
| 切片 stage | `T3 / T4` | 数据集说明 | `p.7` |
| 自建图像像素精度 | `0.465 um` | 扫描设置 | `p.7` |
| 重采样后精度 | `0.620 um` (`20x`) | 扫描设置 | `p.7` |
| patch size | `128x128` | 训练设置 | `p.7-p.8` |
| patch 数 | `22000` | 训练设置 | `p.7-p.8` |
| optimizer | `Adam` | stain separation 训练 | `p.8` |
| initial lr | `1e-3` | stain separation 训练 | `p.8` |
| GlaS reported split | `100 train / 65 test (45A + 20B)` | 评价协议 | `p.12-p.13` |
| GlaS best result | `F1 0.901 / 0.851; Obj-D 0.893 / 0.842; Obj-H 44.125 / 94.528` | 主结果 | `p.11-p.12` |
| independent dataset result | `Accuracy mean 86.91, Dice mean 0.869` | 主结果 | `p.12` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 传统基于颜色、纹理、阈值或显式 gland model 的方法难以处理：
  - 粘连腺体
  - malignant / poorly differentiated glands
  - stain 分布变化与边界不完整
- 在 malignant 场景下，epithelial nuclei 往往与 stroma 混杂，单靠 nuclei 或普通 contour model 难以恢复完整 gland 外轮廓。
- 作者认为 lumen 较 gland 其他组成部分更稳定、更容易被准确分出，因此可作为 complex gland segmentation 的内在锚点。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 本文提出一条混合式复杂腺体分割流程：先用 `Gaussian U-net Stain Separation (GUSS)` 将原始 H&E 图像分解成 `H-stain / E-stain / background` 三个 intensity maps；随后在 `background channel` 上用改进 `SPF level set` 分割 lumen，在 `H-stain` 上做 epithelial nucleus detection / sorting，并从这些 nucleus 获得 rough gland boundary；最后以 lumen 与 rough boundary 的几何对应关系为核心，利用 `axis of least inertia (ALI)`、`12-direction chain code`、`similar triangles` 与距离约束，在候选 contour 中选出最优 gland contour，从而改善复杂、粘连、低分化 gland 的分割。

关键页码：

- `p.1-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`deep learning + classical morphology / level set hybrid pipeline`
- 主要模块：
  - `GUSS stain separation`
  - `SPF-level set lumen segmentation`
  - `SC-CNN + softmax CNN nuclear detection/sorting`
  - `ALI-based feature representation`
  - `similar-triangle + distance-constrained contour selection`
- Backbone：
  - stain separation 主网络为 `U-shaped encoder-decoder`
  - 共 `10` 个 residual branches
- 关键机制：
  - 预测 stain coefficient interval，而不是单一 stain matrix
  - lumen 作为内轮廓先验
  - rough gland boundary 与 candidate contour 的双重几何约束

### 3.2 关键模块详细描述

**模块 1：`GUSS (Gaussian U-net Stain Separation)`**

- 位置：`整条流程的前端`
- 操作流程：
  1. 输入原始 H&E histopathology image
  2. 通过 `contracting path + bridge + expanding path` 提取多尺度特征
  3. 同时输出 `H / E / Background` 三个 stain intensity maps
  4. 利用 bridge 处最紧凑特征预测 `stain color matrix`
  5. 通过高斯分布的 `mean + variance` 建模 stain coefficient interval
- 设计理由：应对 stain intensity 不均匀与不同实验来源之间的 stain shift
- 页码：`p.3-p.5`

**模块 2：`Lumen Segmentation on Background Channel`**

- 位置：`GUSS 之后`
- 操作流程：
  1. 在 `background intensity map` 上应用改进的 `SPF level set`
  2. 通过内外区域的高斯统计构造 `SPF`
  3. 迭代演化 level set function
  4. 移除 small background targets 得到 lumen contour
- 设计理由：作者认为 lumen 既相对稳定，又与 gland boundary 形状相关
- 页码：`p.5-p.6`

**模块 3：`Nuclear Detection + Rough Gland Boundary`**

- 位置：`与 lumen 分割并行`
- 操作流程：
  1. 使用 `SC-CNN` 在 `H-stain map` 上定位 nucleus
  2. 再用 `softmax CNN` 进行 nucleus sorting
  3. 区分 epithelial nucleus 与 stromal nucleus
  4. 从 epithelial nucleus 集合中构造 rough gland boundary `L`
- 页码：`p.5-p.6`

**模块 4：`ALI + 12-direction Chain Representation`**

- 位置：`precise contour selection`
- 操作流程：
  1. 对 lumen contour 求 `axis of least inertia`
  2. 以 lumen centroid 为原点建立坐标系
  3. 沿 `12` 个方向提取 lumen contour 的交点，形成 chain code
  4. 对 candidate epithelial contours 也做同样编码
- 设计理由：把 lumen 和 candidate contour 变成可比较的几何特征序列
- 页码：`p.6-p.7`

**模块 5：`Similar-Triangle Membership + Distance Constraint`**

- 位置：`candidate contour selection`
- 操作流程：
  1. 以相邻两个方向的交点与 centroid 形成 characteristic triangle
  2. 计算 lumen triangle 与 candidate triangle 的 membership similarity
  3. 同时约束 candidate contour 与 rough gland boundary 的距离
  4. 在 `J` 条候选 contour chains 中选最优 contour，再用 cubic spline 平滑
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| F1 | residual branch | `8` | `128` | encoder 起始层 |
| F2 | residual branch | `16` | `64` | encoder |
| F3 | residual branch | `32` | `32` | encoder |
| F4 | residual branch | `64` | `16` | encoder |
| F5 | bridge | `128` | `8` | 同时预测 stain color matrix |
| F6 | residual branch | `64` | `16` | decoder |
| F7 | residual branch | `32` | `32` | decoder |
| F8 | residual branch | `16` | `64` | decoder |
| F9 | residual branch | `8` | `128` | decoder |
| F10 | output | `3` | `128` | 输出 `H / E / Background` intensity maps |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
loss = (1 / MN) * sum_m sum_n (x_(n,m) - x'_(n,m))^2
```

符号说明：
- `x_(n,m)`：第 `m` 张图像的第 `n` 个像素
- `x'_(n,m)`：预测重建像素
- 含义：GUSS stain separation 的 reconstruction loss
- 页码：`Eq.(1), p.3`

公式 2：

```text
P1(I; u1, sigma1), P2(I; u2, sigma2)
```

符号说明：
- `P1, P2`：level set 内外区域的高斯分布
- `u, sigma`：对应区域 stain intensity 的均值与标准差
- 含义：用高斯统计建模 lumen segmentation 的区域强度分布
- 页码：`Eq.(2), p.5`

公式 3：

```text
spf(I(x)) = (ln p1 - ln p2) / max |ln p1 - ln p2|
```

符号说明：
- `spf(I(x))`：symbol pressure function
- 含义：构造 level set 的演化驱动力
- 页码：`Eq.(3), p.5`

公式 4：

```text
dphi / dt = spf(I(x)) * alpha * |grad(phi)|
```

符号说明：
- `phi`：level set function
- `alpha`：演化参数
- 含义：lumen contour 的迭代演化方程
- 页码：`Eq.(4), p.5`

公式 5：

```text
min sum_(xi, yi in phi) ((xi + B*yi + C)^2 / (1 + B^2))
```

符号说明：
- `x + By + C = 0`：候选直线
- `phi`：边界点集合
- 含义：求目标轮廓的 `axis of least inertia`
- 页码：`Eq.(5), p.6`

公式 6：

```text
mu(theta1, theta2, theta3) = 1 - (1/180) * (theta1 - theta3)
```

符号说明：
- `theta1, theta2, theta3`：feature triangle 三个内角
- 含义：triangle membership，用于度量 lumen triangle 与 candidate triangle 的形状相似性
- 页码：`Eq.(6), p.6`

公式 7：

```text
Sim(c, v) = mu_n / mu'_n
TotalSim(c, v) = (1 / n) * sum_i Sim(mu_i, mu'_i)
```

符号说明：
- `c`：lumen contour 特征
- `v`：candidate contour 特征
- `TotalSim`：跨全部 characteristic triangles 的平均相似度
- 含义：评估 lumen 与候选 contour 的整体形状一致性
- 页码：`Eq.(8)-(9), p.6`

公式 8：

```text
alpha <= TotalSim(l, v) <= 1
beta  <= TotalSim(c, v) <= 1
```

符号说明：
- `l`：rough gland boundary 特征
- `c`：lumen contour 特征
- `v`：candidate contour 特征
- 含义：通过双重相似度约束筛 candidate contour
- 页码：`Eq.(10), p.6`

公式 9：

```text
s_j = argmin_(s_j in v) sum_i ||l_i - v_(i,j)||^2
```

符号说明：
- `l_i`：第 `i` 个方向上 rough gland boundary 的交点
- `v_(i,j)`：第 `j` 条候选 contour 在第 `i` 个方向上的交点
- 含义：距离约束，要求目标 contour 靠近 rough gland boundary
- 页码：`Eq.(11), p.6-p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本文不是典型端到端梯度式 segmentation loss 设计，而是先训练 stain separation 网络，再把后续 contour optimization 作为显式几何搜索问题处理。
- `Eq.(12)-(15)` 在当前 PDF 文本抽取中存在 OCR 丢失，尤其是 candidate contour 递推与最终最优 contour 选择部分；正式记录到此，不自行补公式。

---

## 5. 损失函数

### 5.1 各监督项

- `reconstruction loss`：用于 GUSS stain separation
- lumen segmentation 与 contour selection 主要依赖统计建模、level set 与几何约束，不是单一神经网络 loss 主导

### 5.2 总损失公式

```text
loss = (1 / MN) * sum_m sum_n (x_(n,m) - x'_(n,m))^2
```

说明：

- 该 loss 对应 stain separation 子任务
- gland segmentation 主体更多由后续 `SPF + ALI + membership + distance constraint` 决定

### 5.3 权重配置与调度策略

- stain separation 训练使用 `Adam`
- initial learning rate 为 `1e-3`
- 文中只说明“每个 epoch 结束时逐渐降低 learning rate”，未给出完整衰减公式

---

## 6. 训练协议

### 6.1 数据集与划分

- 公共数据集：
  - `GlaS Challenge dataset`
- 自建数据集：
  - `100` 张 benign / malignant colon adenocarcinoma 图像
  - 来源于 `34` 名患者
  - stage 为 `T3 / T4`
- 自建图像采集设置：
  - 原始像素精度 `0.465 um`
  - 调整后 `0.620 um`，约等于 `20x magnification`
- GlaS 评测设置：
  - 文中写为 `100 train / 65 test`
  - test 进一步写为 `45` 张 `Test A` + `20` 张 `Test B`
  - 该写法与常见官方 `85 train / 80 test` 描述不一致，需要保留为协议疑点

### 6.2 数据增强

- 自建数据被随机裁成 `128x128`
- 扩增到 `22000` 个 patches 用于 training and verification
- 文中未详细列出 rotation / flip / color jitter 等增强项

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| optimizer | `Adam` |
| initial lr | `1e-3` |
| lr schedule | `每个 epoch 结束逐渐降低` |
| patch size | `128x128` |
| patch count | `22000` |
| stain separation output | `H / E / Background` |

### 6.4 预处理与数据细节

- 先做 H&E stain separation，再分别在不同 stain maps 上处理下游结构
- `H-stain` 用于 nuclear detection / sorting
- `Background channel` 用于 lumen segmentation
- 对包含完整 gland structure 的图像做无间隔裁剪；边缘不足区域用零填充
- nucleus annotations 由 experienced pathologist 手工标注，并细分为 epithelial nucleus 与其他类型

---

## 7. 推理与后处理

- 推理流程：
  1. 原始 H&E 输入 GUSS
  2. 得到 `H / E / Background` intensity maps
  3. `Background` 上做 improved `SPF-level set` lumen segmentation
  4. `H-stain` 上做 nuclear detection / sorting
  5. 由 epithelial nucleus 得到 rough gland boundary
  6. 用 `ALI + 12-direction chain + similar triangles + distance constraint` 搜索最优 contour
  7. 用 `cubic spline interpolation` 平滑 gland contour
- 后处理：
  - 删除 lumen segmentation 中的小目标
  - spline smoothing
- 速度信息：
  - 文中报告 lumen segmentation 阶段计算时间约 `21s`
  - 该比较对象是其他 active contour models

---

## 8. 消融实验

### 8.1 消融设计

- 论文没有标准的深度模块消融表，而是主要做：
  - stain separation 质性对比
  - lumen segmentation 对比传统 contour / level set 方法
  - gland segmentation 上 `Proposed-N` 与 `Proposed-N+L` 比较
  - 与多个公开方法、独立数据集方法的主表比较

### 8.2 各模块贡献量化

**`Proposed-N` vs `Proposed-N+L`**

| 方法 | Test A F1 | Test B F1 | Test A Obj-D | Test B Obj-D | Test A Obj-H | Test B Obj-H |
|------|-----------|-----------|--------------|--------------|--------------|--------------|
| `Proposed-N` | `0.886` | `0.816` | `0.886` | `0.823` | `45.236` | `103.686` |
| `Proposed-N+L` | `0.901` | `0.851` | `0.893` | `0.842` | `44.125` | `94.528` |

- 结论：
  - 加入 `lumen contour` 后三项指标都提升
  - 在 `Test B`（更偏 malignant）上的 `Obj-H` 改善尤其明显
  - 这直接支持“复杂 gland 需要内轮廓形态约束”的论点

**lumen segmentation 对比**

- 对比 `DRLSE / LBF / LGDF / LIF`
- 作者结论：
  - `DRLSE` 会产生不完整分割
  - `LGDF` 可把 cavity 与其他区域分开
  - `LIF` 与 `LBF` 不适合 gland cavity
  - 新的 `SPF-level set` 更易实现，且运行时间约 `21s`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS, Proposed-N+L, Test A` | `F1 = 0.901` | `Obj-D = 0.893` | `Obj-H = 44.125` | 公开 benchmark |
| `GlaS, Proposed-N+L, Test B` | `F1 = 0.851` | `Obj-D = 0.842` | `Obj-H = 94.528` | malignant 更有代表性 |
| `Independent dataset` | `Accuracy mean = 86.91%` | `Dice mean = 0.869` | `Dice std = 0.047` | 自建数据 |

### 9.2 与其他方法的对比

- GlaS competition 对比中：
  - `Test A` 的 `F1` 不是最高，`CUMedVision2` 达到 `0.912`
  - 但 `Proposed-N+L` 在 `Test B` 的 `Obj-D = 0.842` 与 `Obj-H = 94.528` 表现更有竞争力
- 自建独立数据集上：
  - `Proposed` 的 `Accuracy mean = 86.91`
  - 相比次优 `Guannan et al. [47]` 的 `83.60`，提升约 `3.31`
  - `Dice mean = 0.869`，相比次优 `0.832` 提升 `0.037`
- 作者自己的表述是：
  - average pixel precision 至少提升 `3%`
  - Dice 至少提升 `0.033`

### 9.3 公平对比条件确认

- 公共数据上对比的是 `GlaS competition` 已有方法
- 但需注意：
  - 文中报告的 `GlaS split` 与常见官方描述不一致
  - 若后续引用 benchmark 结果，必须保留这点作为协议风险
- 自建数据集对比只在其内部数据上成立，不能直接等价为公共 benchmark SOTA 结论

### 9.4 评价协议与指标定义

- `F1 score`
  - gland detection / segmentation 的综合准确度
- `Object Dice`
  - gland 实例级 overlap
- `Object Hausdorff`
  - 形状相似度，越低越好
- `Accuracy`
  - `(TP + TN) / (TP + TN + FP + FN)`
- `Dice`
  - `2TP / (2TP + FN + FP)`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未完整报告`
- 间接效率信息：
  - stain separation 是一个 `10-branch` U-Net 风格网络
  - 后续还包含 level set、candidate contour 搜索与 spline smoothing
  - lumen segmentation 文中给出的运行时间约 `21s`
- 效率判断：
  - 这篇更偏“准确恢复复杂 gland contour”，不是轻量实时路线

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但隐含区分了三类 gland segmentation 思路：
  - 基于颜色/阈值/手工特征的传统方法
  - 直接基于 contour / nuclei 的模型
  - 融合 stain separation 与多重形态约束的混合方法

### 11.2 论文指出的研究空白 / Open Problems

- 复杂 gland，尤其 malignant / adherent glands，不能只靠 appearance characteristics
- 传统 gland model 或基于 nuclei 的方法在边界不完整、stain 变化大时不稳
- 自动 gland segmentation 需要显式编码 gland 内外结构之间的关系，而不是只做像素分类

### 11.3 对我们选题的启示

- 如果你的主线是“复杂腺体分割要保结构”，这篇可以作为非常强的论据
- lumen 作为内部稳定结构，可以被视为：
  - 辅助分支 supervision
  - prompt / prior
  - 后处理拓扑约束

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 文中未采用正式分级系统条目化展开
- 但明确指出 gland histological assessment 是 colon cancer grading 的关键环节

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告
- 主要讨论的组织形态学结构是：
  - lumen
  - epithelial nucleus
  - gland boundary

### 12.3 临床意义

- 自动 gland segmentation 可辅助 pathologists 抽取形态学特征，用于 prognosis 与 treatment planning
- 文中尤其强调 lumen 的存在与形态可以反映癌症 grade，这为“为什么要单独建模 lumen”提供病理学支撑

---

## 13. 开源与复现

- 代码是否开源：`正文未提供`
- 代码仓库地址：`未提供`
- 框架/语言：`正文未显式说明，至少 stain separation 部分为深度学习实现`
- 预训练权重是否提供：`未提供`
- 复现难度评估：`中-高`
- 复现障碍：
  - 混合流程较长，包含多个互相依赖的子模块
  - `Eq.(12)-(15)` 文本抽取不完整
  - GlaS 的具体划分与官方协议存在不一致
  - SC-CNN / nuclear sorting 的训练细节未完整展开

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 完整学习率衰减公式 | 否 | 仅记录 `1e-3` 且每个 epoch 逐渐降低 | 中 |
| epoch 数 / stopping criterion | 否 | 不脑补 | 中 |
| 22000 patches 的 train/val 精确拆分 | 否 | 仅记录 `training and verification` | 中 |
| SC-CNN / softmax CNN 训练细节 | 部分 | 仅记录其功能位置 | 中 |
| `Eq.(12)-(15)` 精确表达式 | 当前 OCR 不完整 | 明确标注缺失 | 高 |
| GlaS split 解释 | 写法存在冲突 | 保留原文，不替作者修正 | 高 |

- 不确定但影响较大的点：
  - `GlaS 100/65` 是否为作者自行重组后的实验协议
  - stain separation 与 contour selection 的具体串联代码
  - candidate contour 递推条件阈值

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文结尾主要强调方法贡献，没有系统性罗列失败案例
- 但作者已隐含承认：复杂 gland segmentation 仍然依赖多个子模块都足够稳定

### 14.2 我们观察到的潜在问题

- 该方法工程链路较长，不像纯 CNN/Transformer 那样易于端到端训练
- 对 nucleus detection 与 stain separation 的质量依赖很强，前面任一环节失误都可能传导到最终 contour
- benchmark 协议写法存在疑点，影响结果可比性
- 方法对 today 的大规模训练范式不够友好，更像结构先验很强的专用 pipeline

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未系统展示`
- 可从结果推断的典型难点：
  - epithelial nuclei 与 stromal nuclei 混杂
  - gland boundary 不完整
  - 黏连 glands
  - stain variation 明显的数据源迁移

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `lumen` 作为复杂 gland 分割的结构先验
- “内部稳定结构 + 外部 rough boundary” 联合约束思路
- 在写作中用来论证：复杂 gland segmentation 需要显式形态约束，而不只是普通 semantic mask

### 15.2 可以作为候选参数来源的

- `128x128` patch
- `Adam`
- `1e-3` initial learning rate
- `20x` 量级扫描精度参考

### 15.3 不应照搬的（及原因）

- 不应直接复刻整条传统-深度混合 pipeline
  - 原因：工程复杂，且和你当前主线的端到端模型开发不完全同轨
- 不应直接把其 `GlaS` 数值当作严格可对齐 benchmark
  - 原因：split 写法和官方协议不一致

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 复杂 gland 需要结构先验 | lumen 与 rough boundary 联合约束明显优于只看 nucleus | 强 |
| 多分支辅助监督设计 | 可引入 lumen / boundary 辅助头 | 强 |
| 病理意义阐释 | lumen 形态与 grade 相关 | 中 |
| 粘连 gland 分离 | 通过内部外部双轮廓关系改进 contour 恢复 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`结构先验与复杂腺体分离设计`
- [ ] 需要和哪篇论文交叉验证：`03_DCAN.md`, `11_Automatic-Mucous-Glands.md`, `14_SkeletonAwareDT.md`
- [ ] 待确认的问题：`我们是否要把 lumen 作为辅助监督目标，而不是后处理约束`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 复杂/低分化/粘连 glands 难分 | 任务痛点 |
| related work | morphology-constrained gland segmentation | 结构先验小节 |
| 方法 | lumen 作为内部先验、boundary 作为外部先验 | 模块动机 |
| 实验讨论 | malignant glands 上形状相似度改善更明显 | 结果解释 |
| 讨论 | 纯像素分割不足以描述复杂 gland | 局限与改进方向 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.4` | 整体框架图 | 总体方法 |
| `Fig. 3` | `p.4-p.5` | GUSS stain separation 结构 | stain separation |
| `Fig. 5` | `p.6` | lumen extraction 过程 | lumen segmentation |
| `Fig. 6` | `p.7` | `ALI + characteristic triangle` 表示 | 几何约束 |
| `Table 1` | `p.11-p.12` | GlaS 对比结果 | benchmark |
| `Table 2` | `p.12` | 自建独立数据结果 | 泛化 / 外部验证 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（`epoch`、`schedule`、`Eq.(12)-(15)` 仍不完整）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融/模块贡献已尽可能量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补
