# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `WSI tumor grading`
- `gland formation percentage`
- `survival prognostication`
- `deep survival model`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是 `08` 目录里把传统 `WHO gland formation grading` 正式推到 `WSI 级自动评估 + 生存预测` 的关键节点
- 对当前项目最有价值的是：
  - 用自动化方式近似估计 `gland formation percentage`
  - 把病理分级指标从单纯视觉规则扩展到 `survival-oriented` 深度指标
  - 证明 `deep survival grade` 比单纯 `SGFR` 更强
  - 给出从 tissue map / GF heatmap 到 WSI 级风险分层的完整流程
- 本篇至少完成：`1-3, 9, 12, 14-17`

---

## 1. 论文信息

- 论文名：`Automatic Tumor Grading on Colorectal Cancer Whole-Slide Images: Semi-Quantitative Gland Formation Percentage and New Indicator Exploration`
- 作者/团队：`Shenlun Chen, Meng Zhang, Jiazhou Wang, Midie Xu, Weigang Hu, Leonard Wee, Andre Dekker, Weiqi Sheng, Zhen Zhang`
- 发表年份/会议/期刊：`2022, Frontiers in Oncology`
- DOI / arXiv ID：`10.3389/fonc.2022.833978`
- BibTeX key：`chen2022automaticgrading`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/Automatic_Tumor_Grading_on_Colorectal_Cancer_Whole-Slide_Images_2022.pdf`
- 当前定位：`08` 目录中从“局部腺体形态”走向“整张 WSI 的 gland formation 比例与生存预测”的关键文献，重点不再只是 grade 分类本身，而是 grade 作为 prognostic biomarker 的自动化实现
- 与已提取论文的关系：
  - 承接 [01_CRC-Histological-Characteristics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics.md)：前者给出 WHO gland formation 分级口径，本篇尝试在 WSI 上自动近似这一规则
  - 承接 [02_Glandular-Morphometrics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/02_Glandular-Morphometrics.md) 与 [03_Segmentation-and-Grade-Prediction.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/03_Segmentation-and-Grade-Prediction.md)：前两篇侧重图像级/局部级 grading，本篇升级到整张 WSI 与 survival 分层
  - 与 [03_CRC-Diagnosis-Review-2022.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022.md) 呼应：后者指出数字病理已从 diagnosis 走向 prognosis，本篇就是这条线的具体实证

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：WHO 对 CRC 腺癌的组织学分级本质上依赖 `gland-forming regions` 在整张 WSI 中的密度，而人工目测 GF percentage 具有明显主观性。
  - 用途：`病理标准 + 研究动机`
  - 页码：`p.1-p.2`
- 句子/事实 2：WHO grade 本身并不是足够强的个体化治疗 biomarker，因此仅仅机械计算 GF percentage 还不够，可能需要更深层的 WSI 级生存指标。
  - 用途：`研究缺口`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者先训练 tissue classifier 和 gland formation classifier 生成 WSI 级 spatial heatmaps，再从这些 heatmaps 中计算 `SGFR` 或训练 `SPPSN` 得到 `deep survival grade`。
  - 用途：`方法框架`
  - 页码：`p.2-p.4`
- 句子/事实 2：在独立机构测试集中，`deep survival grade` 的 c-index 高于 `SGFR`，并且还能提升基线 Cox 模型的判别力。
  - 用途：`核心结论`
  - 页码：`p.1`, `p.6-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.3389/fonc.2022.833978` | 文献信息 | `p.1` |
| 训练 WSI | `857 COAD + 297 READ` | 训练规模 | `p.3` |
| 本地外测 WSI | `108` | 外部测试 | `p.3` |
| local subjects | `106` | 队列规模 | `p.5` |
| tissue classifier micro/macro AUC | `0.987 / 0.982` | 分类器性能 | `p.5` |
| GF classifier micro/macro AUC | `0.973 / 0.973` | 分类器性能 | `p.5` |
| SGFR TCGA c-index | `0.552` | GF 百分比验证 | `p.5` |
| 独立外测 SGFR c-index | `0.62` | survival | `p.1`, `p.7` |
| 独立外测 deep survival grade c-index | `0.64` | survival | `p.1`, `p.7` |
| baseline Cox -> +SGFR (test) | `0.74 -> 0.76` | 多变量增益 | `p.6-p.7` |
| baseline Cox -> +deep survival grade (val) | `0.75 -> 0.77` | 多变量增益 | `p.6-p.7` |
| baseline Cox -> +deep survival grade (test) | `0.74 -> 0.77` | 多变量增益 | `p.6-p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRC 的 visual histology grading 仍是标准临床实践的重要组成部分。
- 其中最经典的 WHO grading 规则依赖整张 WSI 上 `gland formation percentage`。
- 但现实问题是：
  - pathologist 估计 GF percentage 高度主观
  - 真正的 WSI 级量化工具长期缺失
  - WHO grade 自身对个体化预后并不总是足够强
- 因此本文试图同时回答两个问题：
  - 能否自动计算一个接近 WHO gland formation 百分比的指标
  - 能否从 WSI spatial heatmaps 中直接学习出比 `GF percentage` 更强的 survival biomarker

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 作者先训练两个独立的 supervised CNN classifier：一个做 tissue category segmentation，区分 `epithelium / stroma / immune cells / other / background`；另一个做 gland formation 分类，把上皮区域进一步分为 `GF1 / GF2 / GF3 / X(normal)`。在此基础上，一方面用这些 heatmaps 计算 `SGFR (semi-quantitative gland formation ratio)` 以近似 WHO 的 gland formation 百分比；另一方面把 masked GF maps、tissue masks 和 WSI thumbnail 一起输入 `SPPSN (spatial pyramid pooling survival network)`，学习一个 `deep survival grade`。最后比较 `SGFR` 与 `deep survival grade` 在 Cox survival analysis 中的判别力。

关键页码：

- `p.2-p.4`
- `p.5-p.8`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 总体流程：
  1. WSI 标注与 patch 采样
  2. tissue classifier 生成 tissue masks
  3. gland formation classifier 生成 GF heatmaps
  4. 基于 masks + heatmaps 计算 `SGFR`
  5. 基于同一组输入训练 `SPPSN`
  6. 用 Cox analysis 比较 `SGFR` 与 `deep survival grade`

### 3.2 关键模块详细描述

**模块 1：`Tissue Classifier`**

- 目标类别：
  - `epithelium`
  - `stroma`
  - `immune cells`
  - `other tissues`
  - `background`
- 作用：
  - 在整张 WSI 上生成组织类别 masks
  - 为后续只在上皮/腺体相关区域内分析 GF 提供约束
- 页码：`p.3-p.5`

**模块 2：`Gland Formation Classifier`**

- ROI 标签：
  - `GF1`：simple tubules only
  - `GF2`：complex / irregular tubules with cribriform morphology
  - `GF3`：paucity of gland-forming cells
  - `X`：normal epithelial cells
- 作用：
  - 生成 tumor differentiation spatial heatmaps
- 页码：`p.3-p.4`

**模块 3：`SGFR`**

- 这是一个 semi-quantitative GF ratio，而不是严格的真实 GF 百分比
- 权重设定：
  - `GF1 -> 1`
  - `GF2 -> 0.5`
  - `GF3 -> 0`
  - normal tissues 不参与
- 核心思想：
  - 用 weighted average 近似 WHO gland-forming percentage
- 页码：`p.4`

**模块 4：`SPPSN`**

- 全称：`Spatial Pyramid Pooling Survival Network`
- 设计原因：
  - DeepSurv 需要固定长度一维输入
  - 但 WSI heatmaps 形状可变
  - `SPP layer` 可把任意形状空间图转换为固定长度特征
- 输入：
  - masked GF maps
  - stroma / immune / other / background masks
  - WSI thumbnail
- 结构：
  - `1 SPP layer`
  - `3 linear layers`
  - `1 activation layer`
- 输出：
  - `deep survival grade`
- 页码：`p.4-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| tissue classifier | 组织分割/分类 | `epithelium/stroma/immune/other/background` |
| GF classifier | gland formation 分层 | `GF1/GF2/GF3/X` |
| SGFR | 近似 WHO GF 百分比 | `1 / 0.5 / 0` 加权 |
| SPP layer | 处理可变尺寸 WSI heatmaps | 把空间图变成固定长度 |
| SPPSN | 生存预测 | masked GF maps + tissue masks + WSI thumbnail |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：`SGFR` 的核心思想

```text
SGFR ≈ weighted average of GF1, GF2, GF3 in tumor-containing regions
```

符号说明：
- `GF1`：权重 `1`
- `GF2`：权重 `0.5`
- `GF3`：权重 `0`
- `normal tissue`：排除

公式 2：Cox survival modeling

```text
h(t|x) = h0(t) exp(f(x))
```

符号说明：
- `x`：由 `SGFR` 或 `SPPSN` 学得的 survival grade 等特征
- 本篇更看重模型判别力，如 `c-index`，而不是显式解析形式

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不以损失推导为主
- 关键创新在于：
  - 把 pathologist 的 GF 规则近似成 `SGFR`
  - 再把空间 heatmap 送入 survival network 学习更优 prognostic representation

---

## 5. 损失函数

### 5.1 各监督项

- tissue classifier：
  - 具体损失未在正文展开
- GF classifier：
  - 具体损失未在正文展开
- SPPSN：
  - 基于 `DeepSurv` 风格的 Cox proportional hazards learning

### 5.2 总损失公式

- 正文未给出完整损失式
- 详细训练参数和网络细节主要放在补充材料 `S1.5`

### 5.3 权重配置与调度策略

- 未在正文细报

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `TCGA-COAD` | `857` WSI | 与 `READ` 合并后再划分 | discovery set | `983` 中筛到 `857` |
| `TCGA-READ` | `297` WSI | 与 `COAD` 合并后再划分 | discovery set | `364` 中筛到 `297` |
| `Local institutional set` | 不参与 discovery 训练 | `108` WSI | 独立外部测试 | `FFPE`, `40x` |

补充：

- `COAD + READ` 随机按 `80:20` 切为 training / validation
- log-rank test 显示 train 与 validation 的 OS 分布无显著差异，`p = 0.70`

### 6.2 数据增强

- 正文未详细给出 augmentation 细节
- 标注与训练流程是：
  - pathologists 在原始 WSI 上做 rectangular annotations
  - 从 annotations 中随机采样 trainable patches
  - 训练前平衡标签比例

### 6.3 优化器与超参数

- SPPSN 结构：
  - `1 SPP layer`
  - `3 linear layers`
  - `1 activation layer`
- 详细 architecture / training parameters 在补充材料 `S1.5`
- 正文未报告更具体 optimizer / lr / batch size

### 6.4 预处理与数据细节

- TCGA：
  - 同时包含 `40x (0.25 um/pixel)` 和 `20x (0.5 um/pixel)`
  - 作者选择尽可能高的 magnification 以获得足够细节
- local institutional dataset：
  - `40x`
  - `FFPE`
- 外部测试集纳入标准：
  - 有 follow-up
  - epithelial tissue area 至少 `20%`
  - WSI 足够清晰且无大面积污染

---

## 7. 推理与后处理

- 对整张 WSI 采用 sliding window 生成 tissue masks 和 GF probability maps
- epithelium mask 会特意应用到 GF heatmap 上，因为 GF 只应在 gland-forming regions 内解释
- 推理输出不只是单一标签，而是可视化 composite maps：
  - tissue category overlay
  - gland formation heatmap overlay
- 这使结果更接近 pathologist 的可读工作流

---

## 8. 消融实验

- 本篇没有传统模块消融表，但有实质上的两组关键比较：
  - `SGFR` vs `deep survival grade`
  - baseline Cox vs baseline + `SGFR` vs baseline + `deep survival grade`
- 这类比较比普通 ablation 更贴近临床意义，因为它直接问：
  - 传统 GF 百分比够不够
  - 深度模型是否真的带来额外 prognostic value

---

## 9. 主表结果与对比

### 9.1 tissue / GF classifier 结果

| 模块 | 指标 | 数值 | 页码 |
|------|------|------|------|
| tissue classifier | micro-average AUC | `0.987` | `p.5` |
| tissue classifier | macro-average AUC | `0.982` | `p.5` |
| tissue classifier | epithelium AUC | `0.981` | `p.5` |
| tissue classifier | stroma AUC | `0.977` | `p.5` |
| tissue classifier | immune cells AUC | `0.972` | `p.5` |
| tissue classifier | other AUC | `0.979` | `p.5` |
| tissue classifier | background AUC | `0.999` | `p.5` |
| GF classifier | micro-average AUC | `0.973` | `p.5` |
| GF classifier | macro-average AUC | `0.973` | `p.5` |
| GF classifier | GF1 AUC | `0.983` | `p.5` |
| GF classifier | GF2 AUC | `0.963` | `p.5` |
| GF classifier | GF3 AUC | `0.963` | `p.5` |
| GF classifier | X AUC | `0.981` | `p.5` |

### 9.2 SGFR 对 WHO GF 百分比的近似验证

- 在 TCGA 上，`SGFR` 的 `c-index = 0.552`
- optimized cutoff 得到阈值约 `0.49`
- 这个值与 WHO 的 `0.5` 分界点非常接近
- 但 WHO 的 `0.05` 与 `0.95` 两端阈值在 TCGA 上样本过少，不足以稳定验证
- 这说明：
  - `SGFR` 可以大致贴近 WHO 两级分化界限
  - 但作为纯 prognostic marker 仍偏弱

### 9.3 univariable survival 结果

| 指标 | Validation | Test | 页码 |
|------|------------|------|------|
| SGFR c-index | `0.52` | `0.62` | `p.7` |
| SGFR log HR | `-0.44` | `-7.15` | `p.7` |
| SGFR p-value | `0.66` | `0.07` | `p.7` |
| Deep survival grade c-index | `0.64` | `0.64` | `p.7` |
| Deep survival grade log HR | `1.73` | `3.53` | `p.7` |
| Deep survival grade p-value | `0.008` | `0.02` | `p.7` |

解释：

- `SGFR` 在 validation 上不显著，在外部 test 上也只是边缘性
- `deep survival grade` 在 validation 和 test 上都更稳定、更显著

### 9.4 multivariable Cox 增益

- baseline Cox 由以下显著因素构成：
  - age
  - vascular invasion
  - AJCC stage III / IV
- 加入 `SGFR`
  - validation：c-index 不提升
  - test：`0.74 -> 0.76`
- 加入 `deep survival grade`
  - validation：`0.75 -> 0.77`
  - test：`0.74 -> 0.77`
- 这是本篇最重要的结果：
  - 深度学得的 WSI 级 grade signal 比单纯近似的 GF 百分比更强

### 9.5 Kaplan-Meier 结果

- validation set：
  - `SGFR p = 0.69`
  - `deep survival grade p = 0.02`
- test set：
  - `SGFR p = 0.07`
  - `deep survival grade p = 0.02`
- 结论非常明确：
  - `deep survival grade` 比 `SGFR` 更能稳定分开高低风险组

### 9.6 评价协议与指标定义

- classifier 级别：
  - ROC / AUC
  - confusion matrix
- survival 级别：
  - `c-index`
  - Kaplan-Meier log-rank
  - uni-/multivariable Cox regression
- 这篇的重要性在于，它把“分级”的评价从普通分类准确率推进到“是否真正有生存分层价值”

---

## 10. 计算量与效率

- 正文未系统报告 runtime
- 本篇重点不是部署效率，而是 WSI 级 prognostic discrimination

---

## 11. 分类体系与研究空白

### 11.1 本篇的分类与分级体系

- tissue classes：
  - epithelium
  - stroma
  - immune cells
  - other
  - background
- gland formation classes：
  - `GF1`
  - `GF2`
  - `GF3`
  - `X`
- WHO differentiation cutoffs：
  - `>95%`
  - `50%-95%`
  - `5%-50%`
  - `<5%`

### 11.2 本篇指出的关键空白

- 单纯 GF percentage 对 personalized therapy 还不够强
- pathologist 的人工 GF 估计缺乏标准化
- 过去几乎没有研究把 WHO gland formation grading 和 survival model 正式接起来
- 即便 `SGFR` 自动化了，也仍不一定是最优 prognostic biomarker

---

## 12. 临床/病理标准

- WHO grading 的根基仍是：
  - gland-forming density on WSI
- 具体阈值：
  - well differentiated：`>95%`
  - moderately differentiated：`50%-95%`
  - poorly differentiated：`5%-50%`
  - undifferentiated：`<5%`
- 本篇最有价值的一点是没有脱离病理标准另起炉灶，而是先尽量贴近 WHO 规则，再探索能否超越它

---

## 13. 开源与复现

### 13.1 论文未报告但复现必需的信息

- tissue / GF classifier 的网络 backbone 未在正文完整展开
- 具体 optimizer、batch size、epoch、tile size 等主要在补充材料中
- `SGFR` 的完整公式正文只给原理，完整实现需看 `Supplementary Material S2`
- `SPPSN` 的精确实现细节也主要依赖 `S1.5`

### 13.2 复现风险与偏差源

- TCGA 与 local dataset 在制片质量上差异明显：
  - TCGA 有更多 low-quality / folded / stained WSIs
  - local dataset 质量更稳定
- WHO 极高/极低分化端的样本太少，使四分级验证不稳
- `GF2` 是主要错误来源，容易被错分到正常或高 GF

### 13.3 数据与代码

- 训练集主体基于公开 `TCGA-COAD / TCGA-READ`
- 外部测试集为机构私有数据
- 正文未给出稳定可访问的完整代码仓库

---

## 14. 局限性与失败案例

- `SGFR` 只能近似 WHO GF 百分比，不能精确替代人工真实计量
- 四级 WHO 分级在实际数据上两端样本稀少，更像支持 two-tiered interpretation
- `GF2` 是最难的类别，容易错到 normal 或 high GF
- TCGA WSI 质量波动影响 GF 百分比稳定性
- 这篇证明了 deep survival grade 更强，但其可解释性仍弱于直接的 GF percentage

---

## 15. 对我们项目的落地价值

### 15.1 最可直接借用的结论

- 如果我们的目标不只是像素级分割，而是服务病理分级和预后讨论，那么 `WSI 级 gland formation` 是非常自然的桥梁变量
- 单纯把 gland formation 百分比算出来还不够，空间分布本身也含有额外预后信息
- `deep survival grade` 优于 `SGFR`，说明 morphology 的空间组织方式比单一比例统计更有价值

### 15.2 对方法设计的启发

- 后续若要从腺体分割走向下游任务，可以考虑：
  - 先生成 gland / tissue heatmaps
  - 再做 WSI 级 aggregation
  - 再训练 survival / prognosis model
- 这比只在 patch 层面做三分类更接近临床真正关心的问题

### 15.3 对写作的价值

- 讨论里可以引用本篇说明：
  - WHO gland formation grading 有坚实病理基础，但人工实现主观且粗糙
  - 自动化模型既可以复制传统规则，也有机会提炼出比传统规则更强的 prognostic biomarker
- 这非常适合放在“为什么要保留 gland 结构信息，而不仅仅做语义分割”这一段

### 15.4 在文献链中的位置

- 这是 `08` 目录里从局部形态走向 WSI 级 prognosis 的枢纽篇
- 处理完这篇后，`08` 目录关于病理意义和下游应用的主线已经基本成形

---

## 16. 关键图表索引

- `Figure 1`
  - 内容：从标注、heatmap 生成到 `SGFR / SPPSN` 的总流程
  - 用途：写整个 WSI 级 pipeline
  - 页码：`p.3-p.4`
- `Figure 2`
  - 内容：tissue classifier 和 GF classifier 的 ROC
  - 用途：支撑前端分类器有效
  - 页码：`p.5`
- `Figure 3`
  - 内容：WSI 原图、tissue map、epithelium mask、GF heatmap 可视化
  - 用途：解释模型输出可读性
  - 页码：`p.5-p.6`
- `Figure 4`
  - 内容：`SGFR` 在 WHO / median / optimized cutoff 下的 Kaplan-Meier
  - 用途：验证 SGFR 与 WHO cutoff 关系
  - 页码：`p.6`
- `Figure 5`
  - 内容：`SGFR` 与 `deep survival grade` 在 validation/test 上的 KM 曲线
  - 用途：最关键结果
  - 页码：`p.6-p.7`
- `Figure 6`
  - 内容：baseline / +SGFR / +deep survival grade 的 Cox forest plot
  - 用途：说明 deep survival grade 的增益
  - 页码：`p.7-p.8`
- `Table 1`
  - 内容：三数据集 patient characteristics
  - 用途：说明 discovery vs external test 的 cohort 差异
  - 页码：`p.5`
- `Table 2`
  - 内容：univariable Cox models
  - 用途：比较 `SGFR` 与 `deep survival grade`
  - 页码：`p.7`

---

## 17. 提取质量自检

- 本篇全文已抽取，并重点核对了题录、WHO gland formation 定义、`SGFR`、`SPPSN`、AUC、c-index 以及 Cox 结果。
- 重点保留了对当前项目最有价值的几类证据：
  - WSI 级 gland formation 自动评估
  - `SGFR` 与传统 WHO 规则的关系
  - `deep survival grade` 对 `SGFR` 的增益
  - validation + external test 的生存分层结果
- 正文中部分网络训练细节依赖补充材料，因此 `6`、`13` 节中明确标注了信息缺口。
- 这篇更适合作为“病理结构为什么值得保留到 WSI 级下游模型”的证据，而不是作为单纯分类精度论文来引用。
