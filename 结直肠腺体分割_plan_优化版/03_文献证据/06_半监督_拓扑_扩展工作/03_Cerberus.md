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

- `multi-task learning`
- `simultaneous histology segmentation and classification`
- `gland + lumen + nuclei + tissue type`
- `transfer learning in CPath`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`06_半监督_拓扑_扩展工作`

- 本篇虽然不只做 gland segmentation，但它把 `gland / lumen / nuclei / tissue type` 统一进一个可同时预测的数字病理框架，是后续写作里非常关键的系统化参考
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`One Model is All You Need: Multi-Task Learning Enables Simultaneous Histology Image Segmentation and Classification`
- 作者/团队：`Simon Graham, Quoc Dang Vu, Mostafa Jahanifar, Shan E Ahmed Raza, Fayyaz Minhas, David Snead, Nasir Rajpoot`
- 发表年份/会议/期刊：`2022, arXiv`
- DOI / arXiv ID：`arXiv:2203.00077`
- BibTeX key：`graham2022one`
- PDF 路径：`结直肠腺体分割_pdf库/06_半监督_拓扑_扩展工作/One_Model_is_All_You_Need_Multi-Task_Learning_Enables_Simultaneous_Histology_Image_Segmentation_and_Classification_2022.pdf`
- 当前定位：`06` 目录里最强的多任务数字病理系统论文之一，说明 gland segmentation 可以自然嵌进更大的组织分析流水线
- 与已提取论文的关系：
  - 与 [01_PRS2.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/01_PRS2.md) 不同：`PRS2` 关注标注效率与半监督，本篇关注多任务共享表示与同时预测
  - 与 [02_MorphologicalConstraints.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/02_MorphologicalConstraints.md) 形成对照：后者依赖结构先验与显式几何约束，本篇强调统一 encoder 下的 shared representation
  - 与 [12_DEA-Net.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/12_DEA-Net.md) 不同：`DEA-Net` 是单任务全监督结构增强，本篇强调多任务泛化和外部数据稳健性

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者指出，传统数字病理工作流通常“一个任务一个网络”，这种方式随着组织学任务数量增加会变得不可扩展。
  - 用途：`研究动机`
  - 页码：`p.1-p.2`
- 句子/事实 2：多任务学习若要支持真正的 simultaneous prediction，前提是不同任务的输入必须在 tissue type、stain 和 resolution 上对齐；否则只能得到通用 encoder，而不能得到有意义的共同输出。
  - 用途：`方法前提 / 写作亮点`
  - 页码：`p.2, p.16`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`Cerberus` 同时处理 `nuclei`、`glands`、`lumina` 和 `tissue regions`，通过共享 encoder 和 task-specific decoders，在多个独立数据源上联合训练。
  - 用途：`多任务相关工作`
  - 页码：`p.1, p.5`
- 句子/事实 2：作者不仅比较 simultaneous prediction 性能，还展示 `Cerberus` 学到的特征可迁移到 patch classification、object subtyping 和 signet ring cell detection。
  - 用途：`扩展价值 / 迁移学习`
  - 页码：`p.5-p.6, p.15`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| arXiv | `2203.00077` | 文献信息 | `p.1` |
| TCGA WSIs | `599` | 数据规模 | `p.1, p.15` |
| total nuclei | `495,179` | 数据规模 | `p.8-p.9` |
| total glands | `51,157` | 数据规模 | `p.8-p.9` |
| total lumina | `56,358` | 数据规模 | `p.8-p.9` |
| tissue patches | `438,362` | 数据规模 | `p.8-p.9` |
| segmentation patch | `448x448` | 训练设置 | `p.16` |
| classification patch | `144x144` | 训练设置 | `p.16` |
| batch size | `9 / GPU`, `27 total` | 训练设置 | `p.16` |
| optimizer | `Adam` | 训练设置 | `p.16` |
| training steps | `90,000` | 训练设置 | `p.16` |
| lr | `1e-3 -> 1e-4 @ 70k steps` | 训练设置 | `p.16` |
| external gland PQ | `0.650` | 主结果 | `p.10` |
| external lumen PQ | `0.530` | 主结果 | `p.10` |
| TCGA output | `377M nuclei / 900K glands / 2.1M lumina` | 下游资源 | `p.1, p.15` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 数字病理中常见做法是“一个任务一个模型”，这会带来：
  - 训练与推理成本高
  - 系统扩展性差
  - 各任务之间不能显式共享特征
- 以往 CPath 多任务学习往往只把 MTL 当作“学通用 encoder”的手段，而不能对单幅输入实现有意义的 simultaneous prediction。
- 作者认为，只有当多个任务在 `tissue type`、`stain` 和 `resolution` 上对齐时，多任务输出才真正可解释且可同时使用。
- 此外，病理标注昂贵，单个任务往往数据不足；共享 encoder 可让不同任务互相补益，提高外部泛化。

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `Cerberus` 多任务框架：使用共享 `ResNet34 encoder` 和多个 task-specific decoders，同步处理 `nuclear segmentation/classification`、`gland segmentation`、`lumen segmentation` 与 `tissue type classification`。训练时通过 `task sampler` 从多个独立但输入假设对齐的数据源中取样，并比较 `fixed batch` 与 `mixed batch` 两种 MTL 采样策略。模型不只追求在各任务输出端达到接近甚至优于单任务模型的结果，还把训练好的 encoder 进一步用于 patch classification、object subtyping、signet ring cell detection 和大规模 TCGA 组织成分解析。

关键页码：

- `p.1-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`shared-encoder multi-task framework`
- 主要模块：
  - `shared encoder Phi`
  - `task-specific decoders Psi_t`
  - `task sampler`
  - `dynamic weight freezing`
  - `transfer learning heads`
- Backbone：
  - `ResNet34` encoder
  - segmentation tasks 使用 `U-Net style decoder`
  - patch classification 使用 `GAP + 2 FC layers`
- 关键机制：
  - aligned tasks only
  - mixed batch / fixed batch sampling
  - task-wise masked loss aggregation
  - 可扩展到 boundary-aware `Cerberus+`

### 3.2 关键模块详细描述

**模块 1：`Shared Encoder + Task-Specific Decoders`**

- 位置：`核心网络`
- 操作流程：
  1. 输入 patch 送入共享 `ResNet34 encoder`
  2. encoder 学到跨任务共享特征
  3. 对每个任务配置一个独立 decoder / prediction head
  4. 在输出端同时产生不同任务的预测
- 页码：`p.5`

**模块 2：`Segmentation Decoder`**

- 位置：`nuclei / glands / lumina segmentation branches`
- 操作流程：
  1. 类 `U-Net` 逐级上采样
  2. 与 encoder 侧特征做 skip connections
  3. 每次上采样后接 `2` 个 `3x3 conv + BN`
  4. 恢复到与输入相同空间尺寸
- 页码：`p.5`

**模块 3：`Patch Classification Head`**

- 位置：`tissue type classification`
- 操作流程：
  1. 对 encoder 输出做 `global average pooling`
  2. 得到 `k=256` 维向量
  3. 通过 `2` 个 FC layers 分类
  4. FC 之间使用 `dropout=0.3`
- 页码：`p.5`

**模块 4：`Task Sampler`**

- 位置：`训练管线`
- 操作流程：
  1. 将任务组织为 task-level datasets `D_t`
  2. 再按输入尺寸将任务分成 super tasks
  3. segmentation super task 使用 `448x448`
  4. tissue classification super task 使用 `144x144`
  5. super task 采样概率分别是 `0.7` 和 `0.3`
  6. 在 super task 内部进一步采用 `fixed batch` 或 `mixed batch`
- 页码：`p.5-p.6`

**模块 5：`Dynamic Training and Loss Aggregation`**

- 位置：`多任务优化`
- 操作流程：
  1. encoder 参数总是更新
  2. 某任务 decoder 只有在 batch 中出现该任务样本时才更新
  3. 通过 masking 将其他任务样本的 loss 置零
  4. 对所有任务损失求和
- 页码：`p.6`

**模块 6：`Cerberus+`**

- 位置：`增强版实例分割输出`
- 操作流程：
  1. 基础 `Cerberus` 预测 eroded instance target
  2. `Cerberus+` 额外预测 object boundary
  3. 在核、gland、lumen 实例任务上均能带来进一步提升，尤其在外部测试上更明显
- 页码：`p.10-p.11`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| encoder | `ResNet34` | `未逐层展开` | 输入依任务而定 | 共享给全部任务 |
| seg decoder | `U-Net style` | `未逐层展开` | `448x448` 输出 | glands / lumina / nuclei |
| cls head | `GAP + 2 FC` | `k=256` | `144x144` 输入 | tissue classification |
| dropout | regularization | `0.3` | `N/A` | classification head |
| super task 1 | segmentation | `N/A` | `448x448` | 采样概率 `0.7` |
| super task 2 | classification | `N/A` | `144x144` | 采样概率 `0.3` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L = sum_(t in [1, T]) sum_(rho in D_t) L_t({Phi, Psi_t}, x_rho, y_rho)
```

符号说明：
- `Phi`：共享 encoder
- `Psi_t`：第 `t` 个任务的 decoder / head
- `D_t`：第 `t` 个任务数据集
- `x_rho, y_rho`：样本与标签
- 含义：Cerberus 的联合多任务训练目标
- 页码：`Eq.(1), p.6`

公式 2：

```text
L_(T+1)(X) = L_alpha(X) + L_beta(X)
```

符号说明：
- `L_alpha`：masked cross-entropy
- `L_beta`：Dice loss
- 含义：对新增 subtyping branch 的损失
- 页码：`Eq.(2), p.6-p.7`

公式 3：

```text
L_alpha(X) = - sum_(k in K) (1 / |nu_k|) * sum_(i in nu_k) y_(i,k)(X) * log(yhat_(i,k)(X))
```

符号说明：
- `K`：类别数
- `nu_k`：属于第 `k` 类的前景像素集合
- 含义：仅在 foreground 内计算的 masked cross-entropy
- 页码：`Eq.(3), p.7`

公式 4：

```text
L_beta(X) = sum_(k in K) 1 - (2 * sum_(i in nu_k)(y_(i,k)(X) + yhat_(i,k)(X)) + eps) /
                       (sum_(i in nu_k) y_(i,k)(X) + sum_(i in nu_k) yhat_(i,k)(X) + eps)
```

符号说明：
- `eps`：平滑项
- 含义：subtyping 分支的 Dice loss
- 页码：`Eq.(4), p.7`

公式 5：

```text
Dice = 2 * (|Y| ∩ |Yhat|) / (|Y| + |Yhat|)
```

符号说明：
- `Y, Yhat`：预测与真值 mask
- 含义：binary segmentation overlap
- 页码：`Eq.(5), p.9`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- Cerberus 的关键不是提出新损失，而是：
  - 使用 task masking 解决不同任务样本不共现问题
  - 让 encoder 始终更新、task decoder 按需更新
  - 借此在多个独立数据集上稳定训练 shared representation
- 对额外 subtyping branch，作者单独冻结原始分支，只训练新增 decoder，避免再去平衡所有任务损失。

---

## 5. 损失函数

### 5.1 各监督项

- joint multi-task loss：对所有任务求和
- segmentation / classification 主训练：`cross-entropy-based loss`
- instance segmentation：使用 `weighted cross-entropy`
- subtyping branch：`masked cross-entropy + Dice`

### 5.2 总损失公式

```text
L = sum_(t in [1, T]) sum_(rho in D_t) L_t({Phi, Psi_t}, x_rho, y_rho)
```

补充：

- 所有任务共享 encoder
- 其他任务样本通过 mask 抑制梯度

### 5.3 权重配置与调度策略

- 文中没有引入显式 task loss 权重平衡公式
- 主要通过：
  - aligned tasks
  - 相同类型损失
  - dynamic weight freezing
  - task sampler
  来降低多任务冲突

---

## 6. 训练协议

### 6.1 数据集与划分

- 任务级数据包含四类：
  - `gland segmentation`
  - `lumen segmentation`
  - `nuclear segmentation & classification`
  - `tissue type classification`
- 数据规模：
  - glands：`51,157`
  - lumina：`56,358`
  - nuclei：`495,179`
  - tissue patches：`438,362`
- gland 数据来源：
  - `GlaS`
  - `CRAG`
  - `DigestPath`
  - `TCGA`
- lumen 数据来源：
  - `GlaS`
  - `CRAG`
  - `DigestPath`
  - `TCGA`
- segmentation 数据划分：
  - `TCGA` 用作 external test set
  - 其余数据做 `3-fold cross-validation`
  - 按 patient level 划分，避免患者重叠
- tissue classification：
  - 也做 `3-fold`，但无独立 external test set

### 6.2 数据增强

- `flip`
- `rotation`
- `Gaussian blur`
- `median blur`
- `colour perturbation`

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| segmentation patch | `448x448` |
| classification patch | `144x144` |
| batch size | `9 / GPU`, `27 total` |
| optimizer | `Adam` |
| training steps | `90,000` |
| initial lr | `1e-3` |
| lr decay | `70,000 steps` 后降到 `1e-4` |
| input normalization | `RGB in [0,1]` |

### 6.4 预处理与数据细节

- 所有任务统一要求：
  - `H&E stained`
  - `colorectal tissue`
  - `20x objective magnification`，约 `0.5 um/pixel`
- task sampler 先按 super task 选择输入尺寸，再按 task dataset 采样
- 采用 pathologist-in-the-loop 迭代标注流程扩充 gland / lumen 数据

---

## 7. 推理与后处理

- Cerberus 推理时可同时输出：
  - nuclei
  - glands
  - lumina
  - tissue type
- `Cerberus+` 在实例任务中额外预测 boundary target
- 迁移学习扩展：
  - patch-level nuclear classification
  - object subtyping
  - RetinaNet signet ring cell detection
- 大规模应用：
  - 处理 `599` 张 TCGA colorectal WSIs
  - 产出 `377M nuclei / 900K glands / 2.1M lumina`

---

## 8. 消融实验

### 8.1 消融设计

- `Cerberus` vs `Cerberus+`
- `STL` vs `MTL`
- `Fixed batch` vs `Mixed batch`
- `U-Net encoder` vs `ResNet34 encoder`
- `Random init` vs `ImageNet pretrained`
- `with / without patch classification auxiliary task`

### 8.2 各模块贡献量化

**gland / lumen 主任务结果**

| 模型 | Gland Cross Val PQ | Gland External PQ | Lumen Cross Val PQ | Lumen External PQ |
|------|--------------------|-------------------|--------------------|-------------------|
| `U-Net` | `0.622 ± 0.030` | `0.459 ± 0.024` | `0.501 ± 0.008` | `0.240 ± 0.109` |
| `MILD-Net` | `0.647 ± 0.046` | `0.526 ± 0.027` | `0.522 ± 0.034` | `0.353 ± 0.088` |
| `Rota-Net` | `0.662 ± 0.048` | `0.573 ± 0.034` | `0.569 ± 0.042` | `0.436 ± 0.054` |
| `Cerberus` | `0.677 ± 0.028` | `0.640 ± 0.012` | `0.589 ± 0.006` | `0.525 ± 0.027` |
| `Cerberus+` | `0.674 ± 0.021` | `0.650 ± 0.004` | `0.590 ± 0.018` | `0.530 ± 0.005` |

- 结论：
  - `Cerberus` 已全面超过 `U-Net / MILD-Net / Rota-Net`
  - `Cerberus+` 在外部测试上进一步提升，说明 boundary target 有助于泛化

**MTL vs STL**

- 在 `ResNet34` 外部测试上：
  - gland `PQ`: `STL 0.566` -> `MTL Mixed 0.617`
  - lumen `PQ`: `STL 0.313` -> `MTL Mixed 0.492`
- 加上 `ImageNet pretraining + patch classification` 后，external test 提升更明显：
  - gland `PQ = 0.640`
  - lumen `PQ = 0.525`
- 论文明确指出：`mixed batch` 在 external test 上优于 `fixed batch`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集/任务 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|-------------|--------|--------|--------|------|
| `Gland external, Cerberus+` | `PQ = 0.650 ± 0.004` | `Dice = 0.908 ± 0.010` | `MTL mixed` | 最强 gland 外测 |
| `Lumen external, Cerberus+` | `PQ = 0.530 ± 0.005` | `Dice = 0.666 ± 0.014` | `MTL mixed` | 最强 lumen 外测 |
| `Nuclei external, Cerberus+` | `Binary PQ = 0.568 ± 0.009` | `mPQ = 0.332 ± 0.011` | `mPQ+ = 0.388 ± 0.003` | 实例 + 分类 |

### 9.2 与其他方法的对比

- gland/lumen 上与三类强基线比较：
  - `U-Net`
  - `MILD-Net`
  - `Rota-Net`
- nuclei 上与：
  - `U-Net`
  - `HoVer-Net`
  对比
- 结果特点：
  - 对所有主任务，优势在 external test 上比 cross validation 更明显
  - 说明 multi-task shared representation 主要收益之一是跨源泛化

### 9.3 公平对比条件确认

- segmentation 统一使用 patient-level split
- `TCGA` 始终保留为 external test
- 对 nuclei、gland、lumen、tissue tasks，作者强调只使用 `aligned` 任务，即：
  - 同 tissue type
  - 同 stain
  - 同分辨率
- 这点是本篇“同时预测可解释”的核心前提

### 9.4 评价协议与指标定义

- segmentation：
  - `Dice`
  - `PQ (Panoptic Quality)`
- nuclei multi-class：
  - `mPQ`
  - `mPQ+`
- classification：
  - `mAP`
  - `mF1`
- signet ring detection：
  - `FROC area`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 训练硬件：
  - `PyTorch 1.9`
  - `3 x NVIDIA V100`
  - `32GB RAM / GPU`
- 效率亮点：
  - 多任务共用一个 encoder，降低“一个任务一个模型”的系统成本
  - 同时预测多个病理对象，适合大规模 WSI 处理
- 实际规模证明：
  - 已处理 `599` 张 TCGA colorectal WSIs

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 论文区分：
  - `single-task learning`
  - `multi-task learning`
  - `multi-label learning`
- 关键点：
  - `MLL` 要求每个样本都有所有标签
  - `MTL` 可以利用多个独立数据集
  - 但若想 simultaneous prediction，任务必须 `aligned`

### 11.2 论文指出的研究空白 / Open Problems

- 过去 CPath 中的 MTL 往往只学通用 encoder，而不是保证输出端各任务都强
- 不对齐的任务会引入 task entanglement 与 gradient conflicts
- 多任务若只追求 representation，不足以形成可部署的一体化数字病理系统

### 11.3 对我们选题的启示

- gland segmentation 不一定必须被孤立处理
- 可以把 gland 放到更大的病理分析框架里，与：
  - lumen
  - nuclei
  - tissue type
  共享表示与先验
- 这对后续论文写作非常有帮助，因为能把你的工作自然放进“from segmentation to explainable CPath pipeline”的叙事里

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本文不直接提出正式 grading system
- 但强调 WSI 上多组织成分定位是后续 biomarker discovery、survival analysis、explainable AI 的基础

### 12.2 涉及的生物标志物

- 未报告单一 biomarker
- 更接近“组织成分与微环境量化平台”

### 12.3 临床意义

- 多任务同时定位 glands、lumina、nuclei 和 tissue regions，可支持可解释数字病理分析
- 作者特别强调：这类资源可用于 downstream biomarker discovery 与 survival analysis

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/TissueImageAnalytics/cerberus`
- 框架/语言：`PyTorch 1.9`
- 预训练权重是否提供：`文中表述代码和 TCGA 结果可获取，权重需以仓库为准`
- 复现难度评估：`中`
- 复现障碍：
  - 数据整合与任务对齐成本高
  - 多源病理数据的 patient-level split 与清洗较复杂
  - 若没有相同规模数据，完整重现 TCGA 资源产出较难

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 每个 decoder 的逐层通道数 | 否 | 只记录为 U-Net style decoder | 低 |
| 各任务 batch 内采样比例细节 | 部分 | 记录 `p_t = 1/T` 与 super task 概率 | 中 |
| boundary-aware `Cerberus+` 的实现细节 | 部分 | 记录“额外预测 boundary” | 中 |
| 大规模 TCGA 后处理细节 | 否 | 仅记录产出规模 | 中 |
| 各单任务基线的复现实装细节 | 部分 | 以文中描述为准 | 中 |

- 不确定但影响较大的点：
  - 多任务标签清洗与 patient-level fold 构建脚本
  - `Cerberus+` 的具体 boundary target 编码方式
  - TCGA 推理与结果汇总的工程细节

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 文章主要强调 aligned tasks 的必要性，这本身也说明方法不是“任意任务都能混合”的通用多任务方案

### 14.2 我们观察到的潜在问题

- 只有当任务在 stain / resolution / tissue type 上对齐时，多任务同时预测才合理；这会限制任务组合自由度
- 构建如此大规模且高质量的多任务数据代价高
- 对当前单一 gland 分割实验而言，这篇更像“系统级上位框架”，不是最直接的可复现 backbone 替代方案

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`有定性展示，但非系统失败集`
- 可从结果推断的典型难点：
  - 外部数据源分布偏移
  - 多任务下的 gradient conflict
  - lumen 这类较弱结构在跨源泛化中的稳定预测

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `shared encoder + 多头输出` 的框架思路
- 把 `gland + lumen` 联合学习而不是完全拆开
- 用 `mixed batch MTL` 提升 external generalization 的实验组织方式

### 15.2 可以作为候选参数来源的

- segmentation 输入 `448x448`
- classification 输入 `144x144`
- `Adam`
- `90k steps`
- `1e-3 -> 1e-4`
- 增强组合：`flip / rotation / blur / colour perturbation`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其四任务全套系统
  - 原因：你的当前主线仍是腺体分割，不一定已有完整 nuclei/tissue labels
- 不应直接把它当作单任务 gland backbone baseline
  - 原因：它的优势来自多任务数据规模与任务对齐，而不是单个 decoder 的局部结构创新

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| gland + lumen 联合学习 | `Cerberus` 在 gland / lumen 同时建模上外测明显优于单任务 | 强 |
| 多任务写作框架 | 说明 gland segmentation 可嵌入 explainable CPath pipeline | 强 |
| 外部泛化论证 | mixed batch MTL 在 external test 上优势更明显 | 强 |
| 迁移学习价值 | encoder 可迁移到 signet ring detection 等新任务 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`多任务联合学习备选方案`
- [ ] 需要和哪篇论文交叉验证：`02_MorphologicalConstraints.md`, `12_DEA-Net.md`, `11_Automatic-Mucous-Glands.md`
- [ ] 待确认的问题：`我们是否需要把 lumen 作为辅助任务加入主模型`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 一个任务一个网络不可扩展 | 研究背景 |
| related work | aligned MTL for simultaneous prediction | 多任务小节 |
| 方法讨论 | shared encoder + task-specific decoders | 系统设计依据 |
| 实验 | mixed batch 对外部泛化更好 | 结果解释 |
| 讨论 | gland segmentation 在 explainable pipeline 中的角色 | 总体价值拔高 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.4-p.5` | Cerberus MTL 训练策略与迁移学习扩展 | 总体框架 |
| `Fig. 3` | `p.8` | pathologist-in-the-loop 标注流程 | 数据构建 |
| `Fig. 4` | `p.8-p.9` | 四类任务数据概览 | 数据规模 |
| `Table 1` | `p.9` | segmentation 对象数量统计 | 数据规模 |
| `Table 3` | `p.10` | gland / lumen 对比结果 | 主结果 |
| `Table 4` | `p.10-p.11` | STL vs MTL 与 mixed/fixed batch 对比 | 方法收益 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够支持主要复现实验
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补
