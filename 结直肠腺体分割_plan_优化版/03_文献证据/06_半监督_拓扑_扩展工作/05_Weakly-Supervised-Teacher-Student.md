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

- `weakly supervised gland segmentation`
- `teacher-student`
- `progressive pseudo-mask refinement`
- `sparse annotation`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`06_半监督_拓扑_扩展工作`

- 本篇是当前文献库里最贴近“弱监督 gland segmentation + teacher-student 自训练”的任务内新论文。
- 对当前项目最有价值的是：
  - 把 sparse pathologist annotations 和 `EMA teacher` 结合起来；
  - 用 `confidence-based filtering + adaptive fusion + curriculum` 逐步修正 pseudo-mask；
  - 在 `GlaS` 上给出与多种弱监督/全监督方法可比的 `mIoU / mDice`；
  - 补上当前 `06` 目录里原来缺少的 `teacher-student` 路线代表稿。
- 本篇至少完成：`1-9, 13-17`

---

## 1. 论文信息

- 论文名：`Weakly Supervised Teacher-Student Framework with Progressive Pseudo-mask Refinement for Gland Segmentation`
- 作者/团队：`Hikmat Khan, Wei Chen, Muhammad Khalid Khan Niazi`
- 发表年份/会议/期刊：`2026, Original Article / 期刊入口待正式出版信息确认`
- DOI / arXiv ID：`当前抽取正文未见稳定 DOI 或 arXiv 编号`
- BibTeX key：`khan2026wsts`
- PDF 路径：`结直肠腺体分割_pdf库/06_半监督_拓扑_扩展工作/Weakly_Supervised_Teacher-Student_Framework_with_Progressive_Pseudo-mask_Refinement_for_Gland_Segmentation_2026.pdf`
- 当前定位：`06` 目录中最直接的弱监督 gland segmentation 新路线，强调在极少标注条件下，用 `EMA teacher` 持续修正未标注 gland 区域的 dense supervision。
- 与已提取论文的关系：
  - 与 `01_PRS2.md` 不同：`PRS2` 走的是 pairwise relation consistency，本篇走的是更典型也更容易工程化的 `teacher-student + pseudo-mask refinement`。
  - 与 `03_Cerberus.md` 互补：`Cerberus` 偏多任务共享表示，本篇聚焦 sparse-annotation segmentation 本身。
  - 与 `03_CSDS.md` 互补：`CSDS` 更偏 stain/structure disentanglement 与半监督表征，本篇更强调伪标签质量控制。
  - 与 `12_DEA-Net.md` 形成对照：`DEA-Net` 是全监督结构增强，本篇说明在标注稀缺时，监督范式本身也能成为主要增量来源。

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CRC 组织病理分级依赖 gland formation，而像素级 gland 标注成本高、难以适配真实临床流程。
  - 用途：`研究动机`
  - 页码：`p.2`
- 句子/事实 2：现有 CAM-based WSSS 往往只覆盖最具判别性的局部区域，导致 pseudo-mask 边界模糊、结构不连续，难以支撑 dense gland segmentation。
  - 用途：`现有方法缺口`
  - 页码：`p.2-p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者把 gland 弱监督分割的关键矛盾明确写成“如何从 sparse annotations 生成足够完整、可用于 dense segmentation 的 pseudo-masks”。
  - 用途：`问题重述`
  - 页码：`p.3`
- 句子/事实 2：本篇的核心贡献不是单纯加 `Mean Teacher`，而是把 `confidence filtering`、`adaptive fusion` 和 `curriculum-guided refinement` 组合成可逐步扩张监督区域的训练机制。
  - 用途：`方法增量`
  - 页码：`p.3`, `p.6-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| OSUWMC WSI 数 | `60` | 自建弱监督数据说明 | `p.2, p.4` |
| OSUWMC patch 数 | `74,179` | 数据规模 | `p.5` |
| OSUWMC 划分 | `63,191 train / 5,460 val / 5,528 test` | 数据划分 | `p.5` |
| GlaS 划分 | `85 train / 80 test` | benchmark 说明 | `p.5` |
| GlaS 训练再划分 | `70 train / 15 val` | 开发集设置 | `p.5` |
| patch size | `512 x 512` | 训练设置 | `p.5, p.8` |
| 类别数 | `4` | benign / malignant / PDC/G / stroma | `p.4, p.6` |
| EMA decay | `0.999` | teacher 更新 | `p.7` |
| warm-up 比例 | `20% - 25% epochs` | 训练策略 | `p.6` |
| optimizer | `AdamW` | 训练设置 | `p.8` |
| init lr | `0.01` | 训练设置 | `p.8` |
| min lr | `1e-5` | cosine annealing | `p.8` |
| batch size | `16` | 训练设置 | `p.8` |
| max epochs | `250` | 训练设置 | `p.8` |
| early stop patience | `50` | 训练设置 | `p.8` |
| GlaS 结果 | `mIoU 80.10 +- 1.52 / mDice 89.10 +- 2.10` | 主结果 | `p.9` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- gland segmentation 对 grading、risk stratification 和形态量化都很重要，但 dense mask 制作极其昂贵。
- CAM-based WSSS 在自然图像里可行，但在 gland 任务里容易出现：
  - 只激活判别区域；
  - 边界破碎；
  - 邻近 gland 分离失败；
  - 未标注 gland 完全缺监督。
- 任务内真正缺的是一种可以利用 sparse pathologist annotations，同时在未标注区域不断扩张可靠监督的弱监督框架。

对应原文依据（页码）：

- `p.2-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 作者基于 `nnUNet` 构建两个同构网络：学生网络通过监督损失和一致性损失学习，教师网络不直接反向传播，而是用学生权重的 `EMA` 更新。训练先经过一个只看 sparse labels 的 warm-up，再进入 teacher-student 协同阶段。此时教师在全图生成 pseudo-mask，但只有高置信区域会被保留，并和稀疏人工标注做像素级自适应融合；同时通过 `cosine-decayed threshold` 与动态 loss 权重，让模型逐步从“只信最稳的伪标签”过渡到“扩张到更多未标注 gland 区域”。最终在弱监督条件下得到接近强监督上限的 gland segmentation。

关键页码：

- `p.3-p.8`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`EMA teacher-student weakly supervised multi-class gland segmentation`
- backbone：`nnUNet`
- 类别定义：
  - `background stroma`
  - `benign glands`
  - `malignant glands`
  - `poorly differentiated clusters/glands (PDC/G)`
- 总体流程：
  1. sparse-label supervised warm-up
  2. 用学生参数初始化教师
  3. 教师生成 pseudo-mask
  4. confidence filtering
  5. adaptive fusion with sparse GT
  6. consistency regularization + supervised learning
  7. EMA 更新教师

### 3.2 关键模块详细描述

**模块 1：`Student Network`**

- 位置：主训练网络
- 作用：
  - 接收 sparse annotations 的显式监督；
  - 通过 teacher guidance 学会未标注 gland 的 dense segmentation。
- 页码：`p.3-p.8`

**模块 2：`EMA Teacher`**

- 位置：伪标签生成器
- 更新方式：
  - `theta_T <- beta * theta_T + (1 - beta) * theta_S`
  - `beta = 0.999`
- 设计原因：
  - 平滑学生短期波动；
  - 降低 noisy pseudo-label 的确认偏差。
- 页码：`p.6-p.7`

**模块 3：`Confidence-based Filtering`**

- 位置：teacher prediction 到 pseudo-mask 的中间阶段
- 作用：
  - 过滤低置信和模糊区域；
  - 优先保留高可信 gland 区域做自训练监督。
- 页码：`p.7`

**模块 4：`Adaptive Fusion with Sparse GT`**

- 位置：最终 supervision 形成阶段
- 作用：
  - 始终保留 pathologist 给出的 sparse annotations；
  - 在未标注区域用 teacher pseudo-mask 补监督；
  - 避免伪标签覆盖可靠人工标注。
- 页码：`p.3, p.7`

**模块 5：`Curriculum-guided Refinement`**

- 位置：teacher-student co-training 全过程
- 作用：
  - 用动态阈值和 loss 权重，控制从高置信区域向难区域逐步扩张；
  - 让模型避免过早依赖噪声伪标签。
- 页码：`p.3, p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| `nnUNet` student | 主分割器 | 4 类 gland/stroma segmentation |
| `nnUNet` teacher | 伪标签生成 | 仅 EMA 更新，不直接梯度优化 |
| confidence filter | 控制伪标签可信度 | 过滤 early noisy regions |
| adaptive fusion | 合并 sparse GT 和 pseudo-mask | 保证人工标注优先 |
| curriculum schedule | 稳定训练 | 监督权重与阈值随 epoch 变化 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：监督损失

```text
L_supervised = L_dice + L_cce
```

符号说明：
- `L_dice`：Dice loss
- `L_cce`：categorical cross-entropy
- 含义：warm-up 阶段只依赖 sparse GT 学到基础表征
- 页码：`Eq.(1-3), p.6`

公式 2：EMA 更新

```text
theta_T <- beta * theta_T + (1 - beta) * theta_S
```

符号说明：
- `theta_T`：teacher 参数
- `theta_S`：student 参数
- `beta`：EMA decay，文中设为 `0.999`
- 含义：生成更稳定的 teacher pseudo-label
- 页码：`Eq.(4), p.7`

公式 3：总损失

```text
L_total = alpha(t) * L_supervised + (1 - alpha(t)) * L_consistency
```

符号说明：
- `alpha(t)`：随 epoch 变化的动态权重
- `L_consistency`：student 向 teacher 对齐的一致性项
- 含义：从早期更信人工标注，逐步过渡到更依赖 teacher guidance
- 页码：`Eq.(5), p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇重点不在复杂梯度推导，而在训练日程和监督源的组织。
- 最核心的稳定性设计有三个：
  - `EMA teacher` 抑制预测抖动；
  - `confidence filtering` 避免把噪声伪标签直接灌给学生；
  - `alpha(t)` 与阈值的课程式调度，避免训练早期发生确认偏差。

---

## 5. 损失函数

### 5.1 各监督项

- `L_dice`
- `L_cce`
- `L_consistency`

### 5.2 总损失公式

```text
L_supervised = L_dice + L_cce
L_total = alpha(t) * L_supervised + (1 - alpha(t)) * L_consistency
```

### 5.3 权重配置与调度策略

- `alpha(t)` 在 warm-up 后从 `0.9` 逐步衰减到 `0.01`
- 调度方式：`cosine decay`
- warm-up 占总 epoch 的 `20% - 25%`
- 一致性项使用 `logit-level mean squared error`
- 目的：
  - 训练早期更多依赖 sparse GT；
  - 训练后期更多吸收 teacher 伪标签。

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 验证量 | 测试量 | 备注 |
|--------|--------|--------|--------|------|
| OSUWMC | `63,191 patches` | `5,460 patches` | `5,528 patches` | 来自 `60` 张 WSI，弱监督主场景 |
| GlaS | `70` | `15` | `80` | 原始 `85 train / 80 test` |
| TCGA-COAD / READ / SPIDER | 无 GT | 无 GT | 仅外部推理 | 做跨域定性泛化 |

### 6.2 数据增强

- random discrete rotation：`0 / 90 / 180 / 270`
- horizontal flip：`P = 0.5`
- hue-saturation-value jitter
- Gaussian noise
- Gaussian blur
- standard ImageNet normalization

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| framework | `PyTorch 1.13.1` |
| CUDA | `11.7` |
| Python | `3.10` |
| GPU | `NVIDIA A100` |
| optimizer | `AdamW` |
| init lr | `0.01` |
| min lr | `1e-5` |
| weight decay | `0.001` |
| batch size | `16` |
| patch size | `512 x 512` |
| max epochs | `250` |
| early stop patience | `50 epochs` |
| gradient clipping | `max norm 1.0` |
| seed | `42` |
| repeated runs | `5` |

### 6.4 预处理与数据细节

- OSUWMC patch 在 `5x` magnification 下从 `40x` 扫描 WSI 中切出。
- GlaS 原图多数为 `775 x 522`，统一 resize 到 `512 x 512`。
- OSUWMC patch 级类别比例大致为：
  - `45%` benign
  - `35%` malignant
  - `15%` stroma
  - `5%` PDC/G

---

## 7. 推理与后处理

- GlaS 上做定量评估时，直接输出像素级分割结果，主指标是 `mIoU / mDice`。
- OSUWMC 和外部队列更强调定性展示：
  - benign glands
  - malignant glands
  - PDC/G
  - background stroma
- 论文当前抽取正文没有报告复杂的形态学后处理，重点在 teacher-generated pseudo-mask 的训练阶段修正，而不是 test-time 手工修补。

---

## 8. 消融实验

### 8.1 消融设计

- 论文显式强调的模块贡献主要来自：
  - `EMA teacher`
  - `confidence filtering`
  - `adaptive fusion`
  - `curriculum-guided weighting`
- 但当前可抽取正文未给出完整分项表格数值。

### 8.2 各模块贡献量化

- 已可明确的量化结论：
  - 相比最强弱监督 `MAA`，本篇 `mIoU` 略低，但方差更小；
  - 训练稳定性提升是作者重点强调的卖点之一。
- 当前无法严格回填的原因：
  - 分模块 ablation table 在现有正文抽取片段中未完整展开。

### 8.3 稳定性结论

- 本篇最值得保留的不是“绝对第一”，而是：
  - `80.10 +- 1.52` 的 `mIoU` 波动低于 `MAA` 的 `+- 2.26`
  - `89.10 +- 2.10` 的 `mDice` 波动低于 `MAA` 的 `+- 3.31`
- 这说明 `EMA + progressive pseudo-mask refinement` 的价值主要体现在可重复性和更稳的训练过程。

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 备注 |
|--------|--------|--------|------|
| `GlaS` | `mIoU = 80.10 +- 1.52` | `mDice = 89.10 +- 2.10` | `5` 次独立运行均值 |

### 9.2 与其他方法的对比

- 弱监督对比：
  - `MAA 2025`：`81.99 +- 2.26 / 90.10 +- 3.31`
  - `MPFP 2025`：`80.44 +- 0.05 / -`
  - `HAMIL 2023`：`77.37 +- 0.73 / -`
  - `OEEM 2022`：`76.48 +- 0.10 / 83.40 +- 5.36`
- 全监督对比：
  - `EWASwin UNet 2025`：`81.5 / 89.4`
  - `TransAttUNet 2023`：`77.7 / 86.7`
  - `UNet++ 2018`：`70.2 / 81.9`
- 结论：
  - 本篇以弱监督代价达到接近强监督 SOTA 的区间；
  - 并在方差上体现出更好的稳定性。

### 9.3 公平对比条件确认

- GlaS 上与弱监督/全监督方法均按公开 benchmark 做比较。
- 外部队列 `TCGA-COAD / TCGA-READ / SPIDER` 只做定性泛化，不与强监督有标注结果混报。
- 本篇的公平性优势在于：
  - 同任务；
  - 同数据域；
  - 同分辨率级 patch；
  - 明确报告 `mean +- std`。

### 9.4 评价协议与指标定义

- `mIoU = TP / (TP + FP + FN)`
- `mDice = 2TP / (2TP + FP + FN)`
- 两者都基于 pixel-level 分类结果。
- 论文没有在主表使用 `Object Dice / Object F1 / Hausdorff`，因此不能直接替代 `GlaS` 官方对象级协议，只能作为弱监督语义分割口径补充。

---

## 10. 计算量与效率

- 训练硬件：`NVIDIA A100`
- 最大训练轮数：`250`
- 双网络带来额外训练成本，但 teacher 不参与反向传播。
- 相比 CAM + refinement + 二阶段噪声学习的复杂管线，本篇的工程链条更统一，更接近可直接复现的 `teacher-student segmentation` 框架。
- 文中未系统报告：
  - 参数量
  - FLOPs
  - 单张推理时间

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文隐含的方法分类

- gland segmentation 的低标注路线可粗分为：
  - `CAM-based WSSS`
  - `teacher-student self-training`
  - `semi-supervised consistency / relation learning`
- 本篇属于第二类，并且显式讨论了 CAM 伪标签为何不足。

### 11.2 论文指出的研究空白 / Open Problems

- CAM 产生的 pseudo-mask 不完整，不适合 dense gland delineation。
- 弱监督方法在 histopathology 中还要额外面对：
  - 高形态相似性；
  - 邻近 gland 紧贴；
  - 稀疏标注覆盖不足；
  - 明显 domain shift。
- SPIDER 上性能下滑提示：仅靠更好的 pseudo-mask 还不够，跨中心泛化仍需 domain adaptation。

### 11.3 对我们选题的启示

- 若后续做低标注扩展，本篇比单纯 CAM 论文更适合落地参考。
- 如果我们不想上完整半监督新分支，也可以保留其中两点：
  - `EMA teacher`
  - `confidence-based pseudo-label filtering`

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇把 gland formation 与 CRC histopathologic grading 直接挂钩：
  - 低级别肿瘤保留较完整 glandular architecture；
  - 差分化肿瘤表现为复杂、残缺或缺失的 gland formation。

### 12.2 涉及的生物标志物

- 本篇未把核心结果建立在分子 biomarker 上，重点是结构形态学。

### 12.3 临床意义

- 其临床价值主张是：
  - 显著降低 dense annotation 负担；
  - 在 sparse-annotation 场景维持高质量 gland segmentation；
  - 为后续 grading、risk stratification 和 computational pathology workflow 提供更可扩展的前端分割器。

---

## 13. 开源与复现

- 代码是否开源：`正文写明将公开`
- 代码仓库地址：`https://github.com/hikmatkhan/gland-segmentation-teacher-student`
- 框架/语言：`Python + PyTorch`
- 预训练权重是否提供：`正文未确认`
- 复现难度评估：`中`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| pseudo-label 具体阈值初值 | 部分 | 只记录有动态阈值，不脑补初值 | 高 |
| adaptive fusion 精确像素规则 | 部分 | 记录思想，不伪造细节 | 高 |
| 外部队列推理阈值 | 否 | 仅记定性泛化 | 中 |
| backbone 改动细节 | 部分 | 记录为 `nnUNet backbone` | 中 |

- 不确定但影响较大的点：
  - curriculum threshold 的具体数值日程；
  - 伪标签融合的逐像素覆盖规则；
  - 弱监督 OSUWMC 训练是否还包含额外类别采样平衡细节。

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- SPIDER 上存在明显性能下降，说明 severe domain shift 尚未解决。
- 外部多中心队列缺少 GT，因此泛化结论主要是定性而非定量。

### 14.2 我们观察到的潜在问题

- 当前主结果只报告 `mIoU / mDice`，不足以直接对齐 `GlaS` challenge 的对象级口径。
- OSUWMC 是机构内数据，虽然更贴近临床，但和标准 benchmark 的评估语义并不完全一致。
- 方法虽然弱监督，但仍需要 sparse expert annotations，不是纯 image-level 弱标签。

### 14.3 失败案例 / 定性分析

- 作者明确指出 SPIDER 上出现：
  - fragmented gland boundaries
  - stromal false positives
  - 对 PDC/G 灵敏度下降
- 这说明 extreme stain/domain shift 仍是现阶段主要失败来源。

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `EMA teacher` 的稳定更新框架
- sparse labels 与 pseudo-mask 的分区融合思路
- `Dice + CCE + consistency` 的弱监督分割训练结构
- 用 `mean +- std` 报告多随机种子稳定性的结果呈现方式

### 15.2 可以作为候选参数来源的

- `patch 512 x 512`
- `AdamW`
- `weight decay 0.001`
- `max epochs 250`
- `early stop 50`
- `EMA decay 0.999`

### 15.3 不应照搬的（及原因）

- 不应直接把 `mIoU / mDice` 当成我们主表唯一评价口径
  - 原因：我们必须优先对齐 `GlaS` 对象级指标。
- 不应直接把 OSUWMC 的四类标签体系搬到当前主线
  - 原因：当前主任务仍是 `GlaS + CRAG` 的腺体分割，不是 benign/malignant/PDC/G 多类病理体系。

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 少标注扩展路线 | `teacher-student` gland segmentation | 强 |
| 伪标签质量控制 | confidence filtering + adaptive fusion | 强 |
| 稳定性汇报方式 | `5` 次独立运行均值和方差 | 中 |
| 跨中心风险讨论 | SPIDER failure modes | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`08_外部对比` 或未来的弱监督扩展方案说明
- [ ] 需要和哪篇论文交叉验证：`01_PRS2.md`, `03_CSDS.md`, `12_DEA-Net.md`
- [ ] 待确认的问题：`我们是否只吸收 teacher-student 训练框架，而不引入完整弱监督新主线`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | dense annotation 代价高与 CAM 伪标签不足 | 任务缺口 |
| related work | gland weakly supervised segmentation 新路线 | 半监督小节 |
| 方法讨论 | EMA teacher 与渐进伪标签修正 | 设计借鉴 |
| 实验 | 多随机种子稳定性汇报 | 结果可信度 |
| 讨论 | domain shift 下的失败模式 | 风险说明 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.4-p.5` | OSUWMC sparse annotation 示例 | 解释弱监督输入形态 |
| `Fig. 2` | `p.6` | teacher-student 总体框架图 | 主架构 |
| `Table 1` | `p.9` | 与弱监督方法主表对比 | 横向对比 |
| `Table 2` | `p.9-p.10` | 与全监督方法主表对比 | 强监督差距评估 |
| `Fig. 4-5` | `p.10-p.12` | OSUWMC / TCGA / READ / SPIDER 可视化 | 泛化与失败模式 |
| `Fig. 6` | `p.13` | GlaS 测试集定性结果 | benchmark 质感展示 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（部分阈值和融合细节仍缺）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [ ] 消融实验的结论已量化（缺完整分项表）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补
