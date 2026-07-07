# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [x] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `semi-supervised histopathology segmentation`
- `stain-structure disentanglement`
- `teacher-student + uncertainty weighting`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`04_腺体与病理近期相关工作`

- 本篇是标注稀缺场景下的腺体分割半监督路线代表作
- 本篇至少完成：`1, 2, 3, 4, 5, 6, 8, 9, 13, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Learning Disentangled Stain and Structural Representations for Semi-Supervised Histopathology Segmentation`
- 作者/团队：`Ha-Hieu Pham, Nguyen Lan Vi Vu, Thanh-Huy Nguyen, Ulas Bagci, Min Xu, Trung-Nghia Le, Huy-Hieu Pham`
- 发表年份/会议/期刊：`2025, COMPAYL Workshop @ MICCAI`
- DOI / arXiv ID：`arXiv:2507.03923`
- BibTeX key：`pham2025csds`
- PDF 路径：`结直肠腺体分割_pdf库/04_腺体与病理近期相关工作/Learning_Disentangled_Stain_and_Structural_Representations_2025.pdf`
- 当前定位：`一篇把 stain variation 与 tissue structure variation 显式解耦后做半监督腺体分割的近期方法论文，适合补“标注稀缺 + 病理域偏移”路线`
- 与已提取论文的关系：
  - 与 `IHC glandular epithelium 2018` 互补：前者偏跨染色泛化的监督学习，这篇偏低标注比例下的半监督
  - 与 `MAC-Net` 互补：MAC-Net 解决全监督近期结构设计，这篇解决 low-label regime
  - 与后续拓扑/一致性半监督论文相关：都属于 gland segmentation 在 scarce labels 条件下的扩展路线

说明：

- `pdf` 文件名中写的是 `2026`，但论文正文显示为 `COMPAYL Workshop @ MICCAI (2025)`，并标注 `arXiv:2507.03923v2 [cs.CV] 3 Aug 2025`；正式记录按论文正文年份记为 `2025`。

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：病理 H&E 图像同时存在显著的 stain variation 与 tissue morphology variation，而现有 SSL 方法通常把图像整体处理，没有显式解耦这两类变化来源。
  - 用途：`引言中的方法动机`
  - 页码：`p.1-p.2`
- 句子/事实 2：CSDS 用两个专门 student 网络分别建模 color / structure 变化，再由共享 EMA teacher 提供伪标签监督。
  - 用途：`related work 或方法概括`
  - 页码：`Abstract, p.1; p.2-p.4`
- 句子/事实 3：在 5% 和 10% 标注比例下，CSDS 在 `GlaS` 与 `CRAG` 上都优于文中对比的 SSL 方法。
  - 用途：`结果概括`
  - 页码：`Abstract, p.1; Table 1, p.5-p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：大多数 SSL segmentation 方法缺少针对 histopathology 的 stain-specific 和 structure-specific representation learning。
  - 用途：`半监督 related work 缺口`
  - 页码：`p.1-p.2`
- 句子/事实 2：CSDS 的关键不是简单双分支，而是配合 color-aware 与 structure-aware uncertainty，对 teacher 伪标签的监督强度进行自适应调制。
  - 用途：`方法差异化`
  - 页码：`p.3-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入尺寸 | `256 x 256` | 实验设置 | `p.5` |
| 主干 | `DeepLabV3+ + ResNet-101` | 方法/实验设置 | `p.5` |
| 优化器 | `AdamW` | 实验设置 | `p.5` |
| 学习率 | `1e-4` | 实验设置 | `p.5` |
| batch size | `4` | 实验设置 | `p.5` |
| GlaS epochs | `80` | 实验设置 | `p.5` |
| CRAG epochs | `120` | 实验设置 | `p.5` |
| labeled ratios | `5% / 10%` | SSL 协议 | `Table 1, p.5-p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 腺体分割在癌症诊断与预后分析中重要，但 H&E 图像的 `stain variation` 与 `morphological variation` 会显著削弱自动分割性能。
- 标注代价高，真实场景常处于 `limited-label regime`。
- 现有半监督分割通常只做一般性的 pseudo-labeling / consistency regularization，没有显式建模病理图像中的两类关键变化源：
  - 染色外观变化
  - 组织结构变化

对应原文依据（页码）：

- `Abstract, p.1`
- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `Color-Structure Dual-Student (CSDS)`。整体基于 Mean Teacher 范式，但把单 student 拆成两个专门分支：`Color Student` 通过 histogram matching 与 color jitter 学习染色变化鲁棒性；`Structure Student` 通过 elastic deformation 学习结构形变与腺体形态变化。共享 `EMA Teacher` 汇聚两个 student 的知识并生成伪标签。同时，作者利用 teacher 输出 entropy 构造基础 uncertainty map，并进一步用图像的颜色复杂度与结构边缘强度构造 `color-aware` 与 `structure-aware` uncertainty，对无标注样本上的一致性损失做加权，从而提高伪标签可靠性。

关键页码：

- `p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`semi-supervised teacher-dual-student segmentation framework`
- 主干：`DeepLabV3+ with ResNet-101`
- 输入尺寸：`256 x 256`
- 输出头：`单个 segmentation map`，但训练期有 `teacher / color student / structure student` 三个网络角色

### 3.2 关键模块详细描述

**模块 1：`Color Student`**

- 位置：`student branch 1`
- 操作流程：
  1. 对输入施加 `color jittering` 或 `histogram matching`
  2. 学习对 in-distribution 与 out-of-distribution stain shift 的鲁棒表征
  3. 接受 teacher 生成的 uncertainty-weighted pseudo-label 监督
- 页码：`p.2-p.5`

**模块 2：`Structure Student`**

- 位置：`student branch 2`
- 操作流程：
  1. 对输入施加 `elastic deformation`
  2. 强调组织形变、边界和腺体形态变化
  3. 同样接受 teacher 的 uncertainty-weighted consistency 监督
- 页码：`p.2-p.5`

**模块 3：`EMA Teacher`**

- 位置：`shared teacher`
- 操作流程：
  1. 由两个 student 的参数做 EMA 聚合
  2. 对无标注样本生成伪标签
  3. 输出 logits 后用于 uncertainty estimation
- 作用：
  - 比单 student teacher 更稳定
  - 融合 color / structure 两类知识
- 页码：`p.2-p.5; p.7-p.8`

**模块 4：`Color-aware uncertainty modulation`**

- 位置：`teacher supervision weighting`
- 操作流程：
  1. 从输入 RGB 图像计算 per-pixel inter-channel variance
  2. 经过平滑与归一化得到颜色复杂度图
  3. 高颜色变化区域提升 uncertainty 权重
- 页码：`p.3-p.4`

**模块 5：`Structure-aware uncertainty modulation`**

- 位置：`teacher supervision weighting`
- 操作流程：
  1. 用有限差分估计图像水平/垂直梯度
  2. 构造边缘强度图并归一化
  3. 在结构显著区域进一步增强 uncertainty
- 页码：`p.4`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| segmentation backbone | `DeepLabV3+ + ResNet-101` | teacher / two students 共享架构 | `p.5` |
| color augmentations | `color jittering`, `histogram matching` | stain robustness | `p.2, p.5` |
| structure augmentation | `elastic deformation` | morphology robustness | `p.2, p.5` |
| shared augmentation | `random flips`, `random rotations` | 通用增强 | `p.5` |
| prediction model at inference | `best validation student` | 最终推理 | `p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：teacher softmax probability

```text
p(x) = softmax(z(x))
```

符号说明：

- `z(x)`：teacher 在像素 `x` 的 logits
- `p(x)`：像素级类别概率
- 页码：`Eq.(1), p.3`

公式 2：entropy uncertainty

```text
U(x) = - Σ_c p_c(x) log(p_c(x) + ε)
```

符号说明：

- `U(x)`：teacher 的基础不确定性
- `ε`：数值稳定项
- 页码：`Eq.(2), p.3`

公式 3：color-aware modulation

```text
σ²(x) = Var_c∈{R,G,B}[I_c(x)]
V^(x) = V(x) / (max_x∈Ω V(x) + ε)
M_C(x) = I[V^(x) > τ_color]
Ũ_C(x) = U(x) · (1 + λ_C · M_C(x))
```

符号说明：

- `σ²(x)`：RGB 通道方差，表示局部颜色复杂度
- `M_C(x)`：高颜色变化区域掩码
- `λ_C`：颜色不确定性调制强度
- 页码：`Eq.(3)-(6), p.3-p.4`

公式 4：structure-aware modulation

```text
G_h(x) = |I(x+1, y) - I(x, y)|
G_v(x) = |I(x, y+1) - I(x, y)|
E(x) = (G_h(x) + G_v(x)) / 3
M_S(x) = I[E^(x) > τ_structure]
Ũ_S(x) = Ũ_C(x) · (1 + λ_S · M_S(x))
```

符号说明：

- `E(x)`：边缘强度图
- `M_S(x)`：结构显著区域掩码
- `λ_S`：结构不确定性调制强度
- 页码：`Eq.(7)-(10), p.4`

公式 5：监督与无监督损失

```text
L_sup = L_CE+Dice(C(x_l), y_l) + L_CE+Dice(S(x_l), y_l)

L_unsup = Ũ_C(x_u) · L_CE+Dice(C(A_C(x_u)), T(x_u))
        + Ũ_S(x_u) · L_CE+Dice(S(A_S(x_u)), T(A_S(x_u)))

L_total = L_sup + λ_unsup L_unsup
```

符号说明：

- `C`：Color Student
- `S`：Structure Student
- `T`：Teacher
- `A_C`：color branch augmentation
- `A_S`：structure branch augmentation
- 页码：`Eq.(11)-(13), p.4-p.5`

### 4.2 推导过程或梯度行为

- 论文核心不是复杂数学推导，而是把 `entropy uncertainty + pathology-specific priors` 合并成 teacher 监督权重。
- 直觉上：
  - color-rich 区域更易受 stain shift 影响
  - edge-rich 区域更易出现结构不确定性
  - 因此对这些区域的伪标签监督应当做自适应调制，而不是一刀切
- 页码：`p.3-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `L_CE+Dice` | `Eq.(11)-(12)` | 同时优化像素分类与区域重叠 | teacher-student supervision |
| `L_sup` | `Eq.(11)` | 标注样本上的双 student 监督 | labeled branch |
| `L_unsup` | `Eq.(12)` | 无标注样本上的 uncertainty-weighted consistency | unlabeled branch |
| `L_total` | `Eq.(13)` | 联合优化监督与半监督目标 | overall training |

### 5.2 总损失公式

```text
L_total = L_sup + λ_unsup L_unsup
```

### 5.3 权重配置与调度策略

- `λ_unsup`：控制无监督损失贡献
- `τ_color`, `τ_structure`：控制 uncertainty mask 阈值
- `λ_C`, `λ_S`：控制颜色/结构不确定性调制强度
- 论文没有在正文给出这些超参数的具体数值
- 页码：`p.3-p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `80%` 用于 5-fold CV | `20% fixed test` | five folds | 共 `165` 张 |
| `CRAG` | `80%` 用于 5-fold CV | `20% fixed test` | five folds | 共 `213` 张 |

### 6.2 数据增强

- 共享增强列表：
  - random flips
  - random rotations
- Color Student 专属增强：
  - color jittering
  - histogram matching
- Structure Student 专属增强：
  - elastic deformation
- Patch 提取策略：`未使用 patch 训练；统一 resize 到 256 x 256`
- 页码：`p.5`

### 6.3 优化器与超参数

- 框架：`PyTorch 2.5`
- CUDA：`12.2`
- 优化器：`AdamW`
- 初始学习率：`1e-4`
- Batch size：`4`
- Epoch / Steps：
  - `GlaS`: `80` epochs
  - `CRAG`: `120` epochs
- 权重初始化：`未明确说明`
- 预训练策略：`[待确认]`
- 是否冻结部分层：`否/未提及`
- 设备：`single NVIDIA RTX 3060 GPU, 16GB VRAM`
- 页码：`p.5`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`无传统 stain normalization；改为 color-specific augmentation + histogram matching`
- 颜色空间转换：`RGB`
- resize / crop / pad 策略：`all images resized to 256 x 256`
- patch overlap：`无`
- 背景过滤策略：`未提及`
- 标签生成方式：`标准 gland segmentation mask`
- 类别不平衡处理：`Dice + CE`
- 随机种子/重复次数：
  - 报告了 `five-fold average ± std`
- 数据泄漏风险点：
  - 采用 fixed test + 5-fold cross-validation，但需注意是否 slide-level 独立，正文未更细说明
- 页码：`p.5-p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 只保留 teacher + Color Student | Dice/Jaccard 下降 | 颜色分支单独不够 |
| `A2` | 只保留 teacher + Structure Student | Dice/Jaccard 下降 | 结构分支单独不够 |
| `A3` | Color + Structure + Teacher | 最好 | 两个 student 互补 |
| `A4` | EMA strategy = Alternate | 低于 Mean | 简单轮替更新 teacher 不稳 |
| `A5` | EMA strategy = Best student only | 低于 Mean | 只依赖单 student 会损失互补信息 |
| `A6` | EMA strategy = Mean | 最好 | teacher 聚合双 student 最优 |

### 8.2 各模块贡献量化

- 5% 标注：
  - `teacher + color`：`81.10 Dice / 69.53 Jaccard`
  - `teacher + structure`：`80.35 / 68.75`
  - `full CSDS`：`82.86 / 72.01`
- 10% 标注：
  - `teacher + color`：`84.37 / 74.02`
  - `teacher + structure`：`84.07 / 73.75`
  - `full CSDS`：`85.06 / 74.87`
- EMA 策略：
  - `5%`: `Alternate 81.80`, `Best-student 81.60`, `Mean 82.86`
  - `10%`: `Alternate 84.56`, `Best-student 84.34`, `Mean 85.06`
- 页码：`Table 2-3, p.7-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS, 5% labeled` | `Dice 82.86±1.24` | `Jaccard 72.01±1.81` | `vs full sup Dice 90.84` | 低标注主结果 |
| `CRAG, 5% labeled` | `Dice 75.25±1.54` | `Jaccard 63.00±1.67` | SOTA | 低标注主结果 |
| `GlaS, 10% labeled` | `Dice 85.06±0.57` | `Jaccard 74.87±0.82` | SOTA | 更高标注比例 |
| `CRAG, 10% labeled` | `Dice 79.50±0.88` | `Jaccard 68.14±1.18` | SOTA | 更高标注比例 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Mean Teacher` | `GlaS/CRAG` | 弱于本文 | teacher-student baseline | 对照 |
| `UAMT` | `GlaS/CRAG` | 弱于本文 | uncertainty-aware SSL | 对照 |
| `FixMatch` | `GlaS/CRAG` | 弱于本文 | pseudo-label consistency | 对照 |
| `CPS` | `GlaS/CRAG` | 强基线，但仍弱于本文 | co-training | 对照 |
| `FDCL` | `GlaS/CRAG` | 次优/较强 | histopathology-specific SSL | 最强对照 |
| `CSDS` | `GlaS/CRAG` | best Dice / Jaccard | 两数据集均领先 | 本文 |

### 9.3 公平对比条件确认

- 是否统一 backbone：`正文未逐个声明，需谨慎视为原文报告对比`
- 是否统一数据增强：`否，不同方法原设定可能不同`
- 是否统一后处理：`未明确`
- 是否统一输入尺寸：`本文统一 resize 256 x 256，自他法是否完全一致未逐项说明`
- 结果来源：`原文 Table 1`
- 页码：`p.5-p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：`20% fixed test + 80% five-fold CV`
- 结果汇报层级：`5% / 10% labeled ratio`
- Dice 类型：`pixel Dice`
- Jaccard 类型：`IoU / Jaccard`
- 是否含后处理后再报结果：`未提及`
- 是否多 seed 平均：`报告 five-fold average ± std`
- 是否报告标准差 / 置信区间：`是，报告 ± std`
- 是否和官方 challenge protocol 一致：`不完全是；作者采用自己的 SSL split`
- 页码：`p.5-p.6`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/hieuphamha19/CSDS`
- 框架/语言：`Python 3.11 + PyTorch 2.5`
- 预训练权重是否提供：`论文摘要称 code and pre-trained models are available`
- 复现难度评估：`中`
- 复现障碍：
  - 正文未给出 `λ_unsup`, `τ_color`, `τ_structure`, `λ_C`, `λ_S` 的具体值
  - 某些对比方法的公平复现条件需另查仓库

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `依赖 5-fold 平均降低波动` | `中` |
| 验证集划分 | `部分明确` | `沿用 fixed test + 5-fold` | `中` |
| 推理阈值 | `否` | `需查代码` | `中` |
| 后处理细节 | `否` | `默认无额外后处理，需查代码` | `中` |
| `λ_unsup/τ/λ_C/λ_S` 数值 | `否` | `需查源码` | `高` |
| 预训练细节 | `否` | `需查源码/配置` | `中` |

- 不确定但影响较大的点：
  - `teacher EMA momentum`
  - `labeled/unlabeled batch sampling ratio`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 正文结论没有展开长篇局限性讨论，但从实验设置可看出：
  - 只验证了 `GlaS` 和 `CRAG`
  - 主要考察的是 `5% / 10%` 低标注设置
- 页码：`p.7-p.8`

### 14.2 我们观察到的潜在问题

- 主干使用 `DeepLabV3+ + ResNet-101`，相对不轻，作为 SSL 基线合适，但不一定适合作为你当前项目的高性价比默认主干。
- 方法的新增收益一部分来自较强 backbone，本身并不完全等价于“轻量半监督技巧”。
- 论文没有在正文里给出关键权重超参数，复现仍需强依赖代码仓库。
- 只在 H&E 腺体数据上验证，尚未直接证明对 IHC 或跨器官腺体任务同样稳定。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`以 qualitative comparison 形式间接展示`
- 典型失败场景：
  - clustered glands 边界不清
  - artifacts 残留
  - CRAG 上不规则结构导致 under-segmentation 或 fragmented boundaries
- 页码：`Figure 2, p.6-p.7`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 把 `stain variation` 与 `structure variation` 明确拆开看，而不是把 augmentation 混成一个黑箱。
- 在标注比例低时，可优先考虑 `teacher-student + branch-specific augmentation`。
- 用 `uncertainty-weighted pseudo-labeling` 替代均匀一致性约束，适合腺体这种边界不稳定任务。

### 15.2 可以作为候选参数来源的

- `DeepLabV3+ + ResNet-101`
- `resize = 256 x 256`
- `AdamW, lr = 1e-4`
- `batch size = 4`
- `5% / 10% labeled` 作为低标注实验协议

### 15.3 不应照搬的（及原因）

- 不应直接照搬双 student + ResNet-101 作为默认训练配置
  - 原因：复杂度和显存开销较高，且你当前主线未必以半监督为第一优先级。
- 不应在没有代码细节前直接复刻 uncertainty 模块
  - 原因：关键阈值和权重未在正文明确，容易出现“表面复现、实际失配”。

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 半监督扩展路线 | 低标注比例下的 gland segmentation 方案 | `强` |
| stain-aware augmentation | 将颜色变化单独建模 | `强` |
| morphology-aware augmentation | elastic deformation 单独建模结构变化 | `强` |
| uncertainty-weighted pseudo-labeling | 边界不确定区域的半监督优化 | `中-强` |
| 轻量主干选择 | 并不直接支持 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`半监督路线备选方案`、`数据稀缺实验设计`
- [ ] 需要和哪篇论文交叉验证：`FDCL`、`CPS`、`拓扑约束半监督` 论文
- [ ] 待确认的问题：`如果后面做 5%/10% 标注实验，是否需要把 stain-aware 与 structure-aware augmentation 分开做消融`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 病理 SSL 不能忽视 stain 与 structure 的双重变化 | 作为 low-label 动机 |
| related work | dual-student + uncertainty 半监督路线 | 放在半监督小节 |
| 方法 | branch-specific augmentation / uncertainty weighting | 作为设计参考 |
| 实验设置 | 5%/10% labeled protocol | 作为低标注实验模板 |
| 讨论 | stain 和 morphology 解耦的必要性 | 解释病理任务特殊性 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.2-p.3` | CSDS 总体框架图 | 参考方法结构 |
| `Eq.(1)-(10)` | `p.3-p.4` | uncertainty estimation 与 modulation | 参考公式设计 |
| `Eq.(11)-(13)` | `p.4-p.5` | supervised / unsupervised / total loss | 参考训练目标 |
| `Table 1` | `p.5-p.6` | GlaS / CRAG 主结果 | 引用主结果 |
| `Figure 2` | `p.6-p.7` | 定性比较 | 分析边界与形态质量 |
| `Table 2` | `p.7` | Color/Structure Student 消融 | 引用模块贡献 |
| `Table 3` | `p.7-p.8` | EMA 策略消融 | 引用 teacher 更新策略 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写
- [x] 公式符号都有解释
- [x] 训练参数足够复现（主干+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查（resize / augmentation / split）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`

