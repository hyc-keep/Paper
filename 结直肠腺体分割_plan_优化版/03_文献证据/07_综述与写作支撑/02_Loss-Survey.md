# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [x] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `loss function survey`
- `semantic segmentation`
- `class imbalance`
- `boundary / shape / structure-aware losses`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇用于支撑你后面关于 `为什么选 CE / Dice / Tversky / boundary-aware hybrid loss` 的写法，不是 CRC 专题文，但对方法论说明非常有用
- 本篇至少完成：`1-5, 9, 11, 13-16`

---

## 1. 论文信息

- 论文名：`A survey of loss functions for semantic segmentation`
- 作者/团队：`Shruti Jadon`
- 发表年份/会议/期刊：`2020, arXiv / IEEE preprint`
- DOI / arXiv ID：`arXiv:2006.14822`
- BibTeX key：`jadon2020losssurvey`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/A_Survey_of_Loss_Functions_for_Semantic_Segmentation_2020.pdf`
- 当前定位：`07` 目录中最适合直接服务方法写作的一篇 loss 综述，可作为你解释不同数据分布与边界复杂度下 loss 选择依据的“说明书”
- 与已提取论文的关系：
  - 与 [01_CRC-AI-Review.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/01_CRC-AI-Review.md) 互补：前者解释“为什么做 CRC gland segmentation”，本篇解释“做的时候为什么选这种 loss”
  - 与 [11_Automatic-Mucous-Glands.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/11_Automatic-Mucous-Glands.md)、[14_SkeletonAwareDT.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/14_SkeletonAwareDT.md) 等论文相连：这些论文中的 specialized loss 或 shape term，都能在本篇分类框架下找到位置
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md) 等 benchmark 文献互补：benchmark 告诉你怎么评估，本篇告诉你训练目标为何这样设

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：近几年 semantic segmentation 中出现了大量针对 `biased data`、`sparse segmentation` 等特定情形设计的 objective / loss function。
  - 用途：`方法动机`
  - 页码：`p.1`
- 句子/事实 2：作者将常见 segmentation loss 概括为 `4` 大类：`distribution-based`、`region-based`、`boundary-based` 和 `compounded`
  - 用途：`方法综述结构`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`Binary Cross-Entropy` 更适合相对 balanced 的数据分布，而 `Weighted / Balanced CE` 与 `Focal loss` 更适合 skewed 或 highly-imbalanced segmentation。
  - 用途：`loss 选择依据`
  - 页码：`p.2, p.5`
- 句子/事实 2：`Tversky / Focal Tversky` 更强调 hard examples 或 small ROI；`Shape-aware` 与 `Hausdorff-based` losses 更适用于 hard-to-segment boundaries；`Combo / Exp-Log` 等 compound losses 则尝试同时融合区域和分布信息。
  - 用途：`hybrid / boundary-aware loss 设计依据`
  - 页码：`p.2-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| loss 大类数 | `4` | 综述结构 | `p.1` |
| 总结 loss 数 | `14` 或 `15`（文中两处表述略有差异） | 综述范围 | `p.1, p.2, p.6` |
| experiments dataset | `NBFS Skull-stripping` | 实验说明 | `p.1, p.6` |
| scans | `125` skull CT scans | 实验说明 | `p.6` |
| slices/scan | `120` | 实验说明 | `p.6` |
| annotated examples | `40,000` | 实验说明 | `p.6` |
| batch size | `32` | 训练设置 | `p.6` |
| optimizer | `Adam` | 训练设置 | `p.6` |
| lr | `0.001` | 训练设置 | `p.6` |
| data split | `60/20/20` | 训练设置 | `p.6` |
| best Dice in exp | `0.98` (`Focal Tversky`) | 实验结论 | `p.6` |
| Log-Cosh Dice | `0.975` | 实验结论 | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- segmentation 本质上是 pixel-level classification，但不同任务的数据属性差异很大：
  - class imbalance
  - sparse target
  - boundary ambiguity
  - structure importance
- 单一 objective 往往很难同时兼顾：
  - 数据分布学习
  - 区域 overlap
  - 边界质量
  - 结构一致性
- 因此，loss function 的选择在 segmentation 中不只是训练细节，而是直接决定模型学习目标。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 本文系统总结 semantic segmentation 中常见的 loss function，并按照优化关注点分成四大类：`distribution-based losses` 强调概率分布与类别不平衡，`region-based losses` 强调区域重叠，`boundary-based losses` 强调边界和形状，`compounded losses` 尝试联合多种优势。作者不仅讨论每类 loss 的典型公式和适用情境，还在一个 skull-stripping 数据集上做了统一实验比较，并提出一个 `Log-Cosh Dice Loss` 作为平滑版 Dice 变体。

关键页码：

- `p.1-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇不是单一 segmentation model 论文，而是 loss taxonomy + small experiment
- 核心分类框架：
  - `Distribution-based`
  - `Region-based`
  - `Boundary-based`
  - `Compounded`

### 3.2 关键模块详细描述

**类别 1：`Distribution-based Loss`**

- 关注点：类别分布、概率建模、前景背景不平衡
- 代表：
  - `Binary Cross-Entropy`
  - `Weighted Cross-Entropy`
  - `Balanced Cross-Entropy`
  - `Focal Loss`
  - `Distance map derived penalty term`
- 页码：`p.2-p.4`

**类别 2：`Region-based Loss`**

- 关注点：区域 overlap 和实例/小目标召回
- 代表：
  - `Dice Loss`
  - `Sensitivity-Specificity Loss`
  - `Tversky Loss`
  - `Focal Tversky Loss`
  - `Log-Cosh Dice Loss`
- 页码：`p.2-p.6`

**类别 3：`Boundary-based Loss`**

- 关注点：边界、形状、距离误差
- 代表：
  - `Hausdorff Distance Loss`
  - `Shape-aware Loss`
- 页码：`p.4-p.5`

**类别 4：`Compounded Loss`**

- 关注点：同时编码数据分布与区域/边界信息
- 代表：
  - `Combo Loss`
  - `Exponential Logarithmic Loss`
  - `Correlation Maximized Structural Similarity Loss`
- 页码：`p.4-p.6`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 不适用单一网络架构参数表
- 但可直接复用为你的 loss 选择框架：

| 大类 | 典型 loss | 更适合的场景 |
|------|-----------|-------------|
| Distribution-based | `BCE / WCE / Balanced CE / Focal` | 类别分布不均、hard negatives |
| Region-based | `Dice / Tversky / Focal Tversky` | overlap 优先、小 ROI、class imbalance |
| Boundary-based | `Hausdorff / Shape-aware` | 边界难、形状约束强 |
| Compounded | `Combo / Exp-Log / Structural Similarity` | 需要兼顾分布、区域和结构 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L_BCE(y, yhat) = -( y log(yhat) + (1-y) log(1-yhat) )
```

符号说明：
- `y`：真值
- `yhat`：预测概率
- 含义：最基础的 pixel-wise 二分类损失
- 页码：`Eq.(1), p.2`

公式 2：

```text
L_W-BCE(y, yhat) = -( beta * y log(yhat) + (1-y) log(1-yhat) )
```

符号说明：
- `beta`：正样本权重
- 含义：用权重调节 false negative / false positive 倾向
- 页码：`Eq.(2), p.2`

公式 3：

```text
L_BalCE(y, yhat) = -( beta * y log(yhat) + (1-beta) * (1-y) log(1-yhat) )
```

符号说明：
- `beta`：由前景比例估计的平衡项
- 含义：同时加权正负样本
- 页码：`Eq.(3), p.2`

公式 4：

```text
FL(pt) = - alpha_t (1-pt)^gamma log(pt)
```

符号说明：
- `pt`：真实类别对应的预测概率
- `alpha_t`：类别平衡项
- `gamma`：hard-example focusing 参数
- 含义：抑制 easy examples，聚焦困难样本
- 页码：`Eq.(7), p.2`

公式 5：

```text
DL(y, phat) = 1 - (2 y phat + 1) / (y + phat + 1)
```

符号说明：
- 含义：Dice overlap 的可优化版本
- 页码：`Eq.(8), p.2-p.3`

公式 6：

```text
TI(p, phat) = (p phat) / (p phat + beta (1-p) phat + (1-beta) p (1-phat))
TL(p, phat) = 1 - TI(p, phat)   [文中为平滑形式]
```

符号说明：
- `beta`：FP / FN 权衡参数
- 含义：Dice 的泛化形式，更适合不平衡和不同错误偏好
- 页码：`Eq.(9)-(10), p.3`

公式 7：

```text
FTL = sum_c (1 - TI_c)^gamma
```

符号说明：
- `gamma`：聚焦 hard examples
- 含义：面向 small ROI 和难例的 Tversky 变体
- 页码：`Eq.(11), p.3`

公式 8：

```text
L_shape-aware = - sum_i CE(y, yhat) - sum_i E_i CE(y, yhat)
```

符号说明：
- `E_i`：预测边界到真值曲线的平均点到曲线距离
- 含义：用形状误差调制 CE
- 页码：`Eq.(15)-(16), p.4`

公式 9：

```text
CL(y, yhat) = alpha L_m-bce - (1-alpha) DL(y, yhat)
```

符号说明：
- `alpha`：BCE 与 Dice 的平衡系数
- 含义：Combo loss 融合分布建模与区域重叠
- 页码：`Eq.(18), p.4`

公式 10：

```text
L_lc-dce = log(cosh(DiceLoss))
```

符号说明：
- 含义：对 Dice loss 做平滑，导数为 `tanh`，更连续且有界
- 页码：`Eq.(32), p.6`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- `Focal loss` 通过 `(1-pt)^gamma` 抑制 easy examples，改变梯度集中位置。
- `Tversky` 通过 `beta` 显式控制对 FP 和 FN 的惩罚偏好。
- `Log-Cosh Dice` 的关键论点是：
  - `log(cosh(x))` 的导数为 `tanh(x)`
  - 因此一阶导连续且有界
  - 试图缓解 Dice 非凸带来的优化不稳定

---

## 5. 损失函数

### 5.1 各监督项

- `Binary Cross-Entropy`
- `Weighted Cross-Entropy`
- `Balanced Cross-Entropy`
- `Focal Loss`
- `Distance map derived penalty term`
- `Dice Loss`
- `Sensitivity-Specificity Loss`
- `Tversky Loss`
- `Focal Tversky Loss`
- `Shape-aware Loss`
- `Combo Loss`
- `Exponential Logarithmic Loss`
- `Hausdorff Distance Loss`
- `Correlation Maximized Structural Similarity Loss`
- `Log-Cosh Dice Loss`

### 5.2 总损失公式

- 本篇是多 loss 综述，不存在唯一总损失
- 但对你最有价值的组合结论是：
  - balanced data：`BCE`
  - skewed / highly-imbalanced：`Weighted CE / Balanced CE / Focal / Tversky / Focal Tversky`
  - hard boundaries：`distance map / Hausdorff / shape-aware`
  - hybrid demand：`Combo / Exp-Log`

### 5.3 权重配置与调度策略

- `Focal loss`：`gamma > 0`, `alpha in [0,1]`
- `Tversky loss`：`beta` 用于权衡 FP 与 FN
- `Focal Tversky`：`gamma` 通常在 `[1,3]`
- `Combo loss`：`alpha` 调和 BCE 与 Dice
- 文中重点不是给出统一推荐值，而是强调应随任务属性调整

---

## 6. 训练协议

### 6.1 数据集与划分

- 统一实验数据：
  - `NBFS Skull-stripping dataset`
  - `125` skull CT scans
  - 每个 scan 包含 `120` slices
  - 文中提到约 `40,000` 个 annotated segmented examples
- 数据划分：
  - `60%` train
  - `20%` validation
  - `20%` test

### 6.2 数据增强

- 文中当前抽取片段未展开详细 augmentation

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| model | `simple 2D U-Net` |
| encoder/decoder depth | `10` conv encoder layers, `8` transpose-conv decoder layers |
| batch size | `32` |
| optimizer | `Adam` |
| learning rate | `0.001` |
| lr reduction | `down to 1e-8` |

### 6.4 预处理与数据细节

- 只比较 `9` 个 loss
- 其余 loss 未纳入实验，原因是：
  - 与已选 loss 在该数据集上过于接近
  - 或不适合 NBFS skull 数据

---

## 7. 推理与后处理

- 本篇不聚焦推理后处理
- 更强调训练 objective 如何影响最终 overlap / sensitivity / specificity

---

## 8. 消融实验

### 8.1 消融设计

- 非传统模块消融
- 而是固定 `2D U-Net + NBFS`，只更换 loss function

### 8.2 各模块贡献量化

| Loss | Dice | Sensitivity | Specificity |
|------|------|-------------|-------------|
| `Binary Cross-Entropy` | `0.968` | `0.976` | `0.998` |
| `Weighted Cross-Entropy` | `0.962` | `0.966` | `0.998` |
| `Focal Loss` | `0.936` | `0.952` | `0.999` |
| `Dice Loss` | `0.970` | `0.981` | `0.998` |
| `Tversky Loss` | `0.965` | `0.979` | `0.996` |
| `Focal Tversky Loss` | `0.977` | `0.990` | `0.997` |
| `Sensitivity-Specificity Loss` | `0.957` | `0.980` | `0.996` |
| `Exp-Logarithmic Loss` | `0.972` | `0.982` | `0.997` |
| `Log-Cosh Dice Loss` | `0.989` | `0.975` | `0.997` |

- 文中结论写法存在一处细节不完全一致：
  - 表 3 显示 `Log-Cosh Dice` Dice 最高 (`0.989`)
  - 结论段又写 `Focal Tversky` achieved optimal dice coefficient of `0.98`
- 当前处理：
  - 同时记录表格和文字结论
  - 不擅自替作者统一，只注明存在轻微不一致

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

- loss 选择不存在 universal best
- 高度不平衡数据更适合 `focus-based losses`
- `Focal Tversky` 和 `Log-Cosh Dice` 在作者实验中表现最好
- `Specificity` 在各 loss 之间变化较小，而 `Dice / Sensitivity` 差异更明显

### 9.2 与其他方法的对比

- 本篇的核心不是和某个具体 segmentation 网络比较
- 而是将多种常见 loss 放在统一框架下比较 use-case
- 对写作最有用的是其 `Table II`：
  - loss -> scenario 的直接映射

### 9.3 公平对比条件确认

- 同一数据集
- 同一 U-Net 结构
- 同一优化器和数据划分
- 唯一核心变量是 loss function

### 9.4 评价协议与指标定义

- `Dice Coefficient`
  - `2TP / (2TP + FP + FN)`
- `Sensitivity (TPR)`
  - `TP / (TP + FN)`
- `Specificity (TNR)`
  - `TN / (TN + FP)`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 训练效率相关结论：
  - 作者强调正确 loss 选择可促进更快、更稳定的收敛
  - 但没有系统比较每种 loss 的 wall-clock efficiency

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- `Distribution-based`
- `Region-based`
- `Boundary-based`
- `Compounded`

### 11.2 论文指出的研究空白 / Open Problems

- segmentation objective 不能被单一通用 loss 覆盖
- 不同数据分布、边界复杂度、结构重要性对应不同优化目标
- 传统像素级 loss 容易忽略结构信息和边界性质

### 11.3 对我们选题的启示

- 腺体分割通常同时具备：
  - class imbalance
  - touching glands
  - boundary ambiguity
  - shape / topology importance
- 因此只用单一 `Dice` 或单一 `CE` 很难穷尽需求
- 更合理的写法是：
  - 用本篇解释为什么需要 `hybrid loss`
  - 再用任务论文解释你具体选了哪一种 hybrid

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 不适用

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/shruti-jadon/Semantic-Segmentation-Loss-Functions`
- 框架/语言：`深度学习实现，正文当前片段未显式展开完整框架细节`
- 预训练权重是否提供：`未强调`
- 复现难度评估：`低`
- 复现障碍：
  - 实验数据是 skull-stripping，不是 gland segmentation
  - 结论更适合做 loss 选择参考，而不是直接移植数值

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 完整网络通道配置 | 否 | 仅记录为 simple 2D U-Net | 低 |
| 每种 loss 的具体超参数取值 | 部分 | 只记录范围和角色 | 中 |
| augmentation 细节 | 否 | 不脑补 | 低 |
| 结论段与表格的最佳 Dice 归属 | 轻微不一致 | 同时记录，不强行统一 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 作者并未宣称提出 universal best loss
- 明确强调：
  - loss 选择依赖数据集属性
  - none of the mentioned loss functions have the best performance in all use cases

### 14.2 我们观察到的潜在问题

- 实验数据来自 skull-stripping，而不是病理图像
- 因此其数值结果不能直接等价到 gland segmentation
- 文中“总结 15 类”与“总结 14 类”有轻微表述差异
- 结论段与表格的最佳 Dice 归属也有轻微不一致

### 14.3 失败案例 / 定性分析

- 论文未系统展示失败案例
- 但整体隐含的失败源包括：
  - highly imbalanced foreground
  - hard-to-segment boundaries
  - structurally important outputs
  - 单一 loss 难以兼顾所有维度

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 一个清晰的 loss taxonomy
- loss 与数据属性之间的映射关系
- “没有 universal loss” 这一合理、保守、好写的结论

### 15.2 可以作为候选参数来源的

- `Focal/Tversky` 类思路适合小目标、hard examples
- `distance map / shape-aware / Hausdorff` 适合边界难例
- `Combo / Exp-Log` 适合 hybrid 目标设计

### 15.3 不应照搬的（及原因）

- 不应把本篇实验排名直接当成 gland segmentation 的结论
  - 原因：数据集不是病理腺体
- 不应只根据“某个 loss 在表格最好”就决定方法
  - 原因：作者自己明确说 depends on dataset properties

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 为什么不只用 Dice | 单一 loss 难覆盖分布、边界、结构三类需求 | 强 |
| 为什么考虑 Tversky/Focal Tversky | small ROI / hard examples / imbalance | 强 |
| 为什么考虑边界项 | Hausdorff / shape-aware / distance map loss | 强 |
| 为什么考虑 hybrid loss | Combo / Exp-Log 提供组合范式 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`方法设计_损失函数选择说明`
- [ ] 需要和哪篇论文交叉验证：`11_Automatic-Mucous-Glands.md`, `14_SkeletonAwareDT.md`, `03_Boundary-Loss.md`, `05_clDice.md`
- [ ] 待确认的问题：`我们最终是采用 CE+Dice，还是增加 Tversky / boundary term`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| related work | segmentation loss taxonomy | 方法综述 |
| 方法 | 不同 loss 对应不同数据属性 | loss 设计理由 |
| 实验 | 解释为什么在 imbalance / boundary-hard 任务上选 hybrid loss | 参数与方法说明 |
| 讨论 | 没有 universal loss，需要任务依赖选择 | 谨慎结论 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Table I` | `p.1` | semantic segmentation loss 分类表 | 总体框架 |
| `Table II` | `p.5-p.6` | loss 与 use case 对照表 | 写作支撑 |
| `Table III` | `p.6` | 9 个 loss 的统一实验比较 | 实验结论 |
| `Fig. 3` | `p.4` | Hausdorff distance 示意 | 边界类 loss |
| `Fig. 6` | `p.6` | NBFS skull dataset 示例 | 实验背景 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] loss 分类与适用场景已系统整理
- [x] 关键公式符号都有解释
- [ ] 训练参数足够完全复现（部分 loss 超参数未完整展开）
- [x] 指标定义已确认
- [x] 与我们项目的关联已具体到 loss 设计层面
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补
