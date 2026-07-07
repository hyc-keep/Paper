# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `topology-preserving loss`
- `tubular / curvilinear structure segmentation`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为这篇有明确理论保证、算法实现和跨 2D/3D benchmark，所以额外补全：`6, 10, 16`

---

## 1. 论文信息

- 论文名：`clDice - a Novel Topology-Preserving Loss Function for Tubular Structure Segmentation`
- 作者/团队：`Suprosanna Shit, Johannes C. Paetzold, Anjany Sekuboyina, Ivan Ezhov, Bohdan Stier, Bjoern Menze, et al.`
- 发表年份/会议/期刊：`2021, CVPR 2021`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:2003.07311 [待确认版本]`
- BibTeX key：`shit2021cldice`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/clDice_A_Novel_Topology-Preserving_Loss_Function_for_Tubular_Structure_2021.pdf`
- 当前定位：`针对 tubular / curvilinear structure 的拓扑保持损失代表作；核心价值是用 skeleton-mask intersection 构造 connectivity-aware 相似度，并给出 differentiable soft-clDice 训练损失`
- 与已提取论文的关系：
  - 与 `Boundary-Loss_2019`、`Distance-Map-Loss_2019`、`Shape-Aware-SDM_2020` 互补：前三者更偏 boundary/surface 几何，这篇直接强调 connectivity topology
  - 对我们项目的特殊意义在于：如果后续任务涉及腺体骨架、腺腔连通性、细长结构或拓扑保持，这篇是强支撑
  - 与 `Gated-SCNN_2019` 形成“边界质量 vs 拓扑连接性”两个不同目标维度

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：对 vessels / neurons / roads 这类 tubular network，最重要的属性是 topology，尤其是 connectedness
  - 用途：`背景 / 痛点`
  - 页码：`Abstract, p.1; Intro, p.1-p.2`
- 句子/事实 2：传统体积型指标如 Dice、Jaccard 对 network topology 是次优的，因为它们按 voxel 平均，不能正确强调连续连通路径
  - 用途：`指标与损失动机`
  - 页码：`Intro, p.1-p.2`
- 句子/事实 3：soft-clDice 训练得到的分割具有更准确的 connectivity information、更高 graph similarity 和更好 volumetric scores
  - 用途：`结果概述`
  - 页码：`Abstract, p.1; Results, p.5-p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：已有 persistent homology / Betti-based loss 能施加拓扑约束，但训练昂贵且对真实图像大小 patch 容易出错
  - 用途：`related work 对比`
  - 页码：`Sec.1.1, p.2`
- 句子/事实 2：clDice 基于 morphological skeleton，因此强调 network topology，而不是均匀对待所有体素
  - 用途：`方法定位`
  - 页码：`Sec.1.2, p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据集数量 | `5` | benchmark 覆盖 | `p.5` |
| 2D 数据集 | `DRIVE / Roads / CREMI` | 数据集设置 | `p.5` |
| 3D 数据集 | `synthetic vessels / Vessap` | 数据集设置 | `p.5` |
| 网络 | `U-Net / FCN` | baseline 架构 | `p.4-p.5` |
| 联合损失 | `Lc = (1-α)(1-softDice) + α(1-softclDice)` | 训练目标 | `p.4` |
| `α` 范围 | `[0, 0.5]` | 超参数设置 | `p.4-p.5` |
| skeleton iterations `k` | `5...25` | soft-skeleton 设置 | `p.4` |
| 骨架半径条件 | `k >= max observed radius` | 算法约束 | `p.4` |
| 验证协议 | `3-fold cross-validation + held-out test` | 评估协议 | `p.5` |
| 训练时间开销 | `1.35s vs 1.24s` | soft-clDice vs soft-Dice | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 对 tubular / network-like structures，最关键的不是单纯体素重叠，而是 global connectivity
- 传统 Dice/Jaccard 等体积损失会偏向大半径结构，对细小连接、细分支和单像素级位移非常敏感却表达不足
- 对于血管、道路、神经元等网络，漏掉一个连接段会严重改变拓扑意义，但普通体积指标可能仍给出不错的分数
- 现有 topology-preserving 方法要么不可端到端优化，要么计算代价高、难以用于真实规模训练

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`
- `Sec.1.1, p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `clDice`，其核心是将预测 mask 与 GT mask 的 skeleton 与实体 mask 交叉，分别定义 `topology precision` 和 `topology sensitivity`，再取二者的 harmonic mean。为了把它用于神经网络训练，作者提出 differentiable `soft-skeletonization`，用 min/max pooling 近似形态学细化，从而得到 `soft-clDice`。训练时再与 soft-Dice 组合成 `Lc(α)`，在保持体积精度的同时显式提升连通拓扑。

关键页码：

- `Sec.2, p.3`
- `Sec.4, p.4-p.5`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Tprec(SP, VL) = |SP ∩ VL| / |SP|
Tsens(SL, VP) = |SL ∩ VP| / |SL|
```

符号说明：

- `VP`：预测 segmentation mask
- `VL`：GT segmentation mask
- `SP`：预测 mask 的 skeleton
- `SL`：GT mask 的 skeleton
- `Tprec`：topology precision，对 false positives 更敏感
- `Tsens`：topology sensitivity，对 false negatives 更敏感
- 页码：`Eq.(1), p.3`

公式 2：

```text
clDice(VP, VL) = 2 * Tprec(SP, VL) * Tsens(SL, VP) / (Tprec(SP, VL) + Tsens(SL, VP))
```

符号说明：

- 含义：以 skeleton-mask overlap 为基础的 harmonic mean，强调 connectivity 而非单纯体积重叠
- 页码：`Eq.(2), p.3`

公式 3：

```text
Lc = (1 - α)(1 - softDice) + α(1 - softclDice)
```

符号说明：

- `softclDice`：soft-skeletonization 下的 differentiable clDice
- `α ∈ [0, 0.5]`：soft-clDice 权重
- 含义：将体积重叠优化与拓扑保持优化联合
- 页码：`Eq.(3), p.4`

公式 4：

```text
soft-skeleton(I, k):
I0 = maxpool(minpool(I))
S = ReLU(I - I0)
repeat k times:
  I = minpool(I)
  I0 = maxpool(minpool(I))
  S = S + (1 - S) * ReLU(I - I0)
```

符号说明：

- `I`：待 skeletonize 的 real-valued mask
- `k`：迭代次数，应不小于最大观测半径
- 含义：用 min/max pooling 近似形态学 erosion/dilation，实现可微 soft-skeleton
- 页码：`Algorithm 1, p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 理论保证：
  - 在 mild assumptions 下，若前景和背景 skeleton 满足相互包含条件，则 clDice 能保证 up to homotopy equivalence 的 topology preservation
- 梯度/优化意义：
  - soft-clDice 通过 skeletonization 放大连通路径上的错误，尤其是断裂连接和伪连通
  - 与普通 Dice 相比，更倾向于恢复 missed connections，而不是只优化粗大主体体素重叠
- 适用条件：
  - 目标局部呈 tubular / curvilinear，整体形成 connected network
  - 典型如 vessels, roads, neurons
- 不适用场景：
  - 若目标不是 network topology 主导，而是块状器官或不规则实体区域，clDice 可能不是第一主损失
- 页码：
  - `Sec.3, p.3-p.4`
  - `Sec.4, p.4-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `soft-Dice` | `1 - softDice` | 体积重叠 | segmentation output |
| `soft-clDice` | `1 - softclDice` | 拓扑 / 连通性保持 | segmentation output 经 soft-skeletonization |
| `combined loss` | `Lc = (1-α)(1-softDice) + α(1-softclDice)` | 兼顾 volumetric 与 topology | 最终训练目标 |

### 5.2 总损失公式

```text
L_total = (1 - α)(1 - softDice) + α(1 - softclDice)
```

说明：

- 论文不是直接只用 `soft-clDice`
- 而是将其与 `soft-Dice` 联合，保持体积精度不被拓扑优化单独主导

### 5.3 权重配置与调度策略

- `α ∈ [0, 0.5]`
- 文中实验测试 `α = 0.1 ~ 0.5`
- 经验结论：
  - 几乎所有 `α > 0` 都优于纯 `soft-Dice`
  - `α` 可视为 dataset-specific hyper-parameter
- 特殊说明：
  - 对复杂且高度不平衡的数据，只在 underrepresented foreground class 上计算 clDice 也足够
- 页码：
  - `p.4-p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `DRIVE` | `[待确认]` | `[待确认]` | `3-fold CV + held-out test` | 2D retina vessels |
| `Massachusetts Roads` | `[待确认]` | `[待确认]` | `3-fold CV + held-out test` | 2D roads |
| `CREMI` | `[待确认]` | `[待确认]` | `3-fold CV + held-out test` | 2D neuron segmentation |
| `Synthetic vessels` | `[待确认]` | `[待确认]` | `3-fold CV + held-out test` | 3D synthetic |
| `Vessap` | `[待确认]` | `[待确认]` | `3-fold CV + held-out test` | 3D real vessels, 1/2 channel variants |

### 6.2 数据增强

- 增强列表：`[待确认，当前摘录未展开]`
- Patch 提取策略：`held-out, large, highly-variant test sets`
- 页码：`p.5`

### 6.3 优化器与超参数

- 框架：`标准 deep-learning toolbox，可用 pooling 实现 soft-skeleton`
- 优化器：`[待确认]`
- 初始学习率：`[待确认]`
- 学习率调度：`[待确认]`
- Batch size：
  - 计算效率示例中为 `4`
- Epoch / Steps：`[待确认]`
- 权重初始化：`[待确认]`
- 预训练策略：`[待确认]`
- 是否冻结部分层：`否`
- 设备：
  - 运行时开销示例在 `RTX-8000`
- 关键超参数：
  - `k = 5 ... 25`
  - `α = 0.1 ... 0.5`
- 页码：`p.4-p.6`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用`
- 颜色空间转换：`未强调`
- resize / crop / pad 策略：`[待确认]`
- patch overlap：`[待确认]`
- 背景过滤策略：
  - 对 highly imbalanced data，仅在前景类上计算 clDice 即可
- 标签生成方式：
  - 直接使用 segmentation mask
  - skeleton 在训练中通过 soft-skeletonization 从 mask 动态得到
- 类别不平衡处理：
  - 通过前景 clDice 和 connectivity emphasis 自然减轻大结构偏置
- 随机种子/重复次数：
  - `3-fold cross-validation`
- 数据泄漏风险点：
  - 需要保证 fold 与 held-out set 完全分离
- 页码：`p.4-p.5`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | `soft-Dice` vs `Lc(α)` | 几乎所有 `α > 0` 下 topology / graph / volumetric 指标都更好 | soft-clDice 有普适收益 |
| `A2` | 不同 `α = 0.1 ... 0.5` | 最优 `α` 因数据集而异 | `α` 是 dataset-specific 超参数 |
| `A3` | FCN vs U-Net | 两种架构上都成立 | loss 对 backbone 通用 |
| `A4` | 2D vs 3D datasets | 均提升 connectivity / graph similarity | 方法跨模态跨维度有效 |

### 8.2 各模块贡献量化

- Roads, FCN：
  - `soft-dice -> Lc, α=0.4`
  - `Dice 64.84 -> 67.18`
  - `clDice 70.79 -> 76.92`
  - `β0 Error 1.474 -> 0.934`
  - `β1 Error 1.408 -> 1.092`
- Roads, U-Net：
  - `soft-dice -> Lc, α=0.5`
  - `Dice 76.23 -> 76.45`
  - `clDice 86.83 -> 88.17`
  - `β1 Error 1.256 -> 0.953`
- DRIVE, FCN：
  - `soft-Dice -> Lc, α=0.5`
  - `clDice 78.02 -> 80.95`
  - `β0 Error 2.187 -> 1.836`
  - `β1 Error 1.860 -> 1.408`
- Vessap, U-Net 2ch：
  - `soft-dice -> Lc, α=0.4`
  - `Dice 87.98 -> 88.57`
  - `clDice 90.16 -> 93.25`
  - `β0 Error 2.344 -> 2.281`
  - `β1 Error 4.323 -> 4.302`
- 结论：
  - 提升最稳定地体现在 `clDice`、`Betti errors`、`graph similarity` 上
  - volumetric Dice 常常也同步提升，但不是唯一目标
- 页码：`Table 1, p.5-p.6`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Roads / FCN` | `Dice 67.18` | `clDice 76.92` | `β0 Error 0.934` | `α=0.4` |
| `Roads / U-Net` | `Dice 76.45` | `clDice 88.17` | `β1 Error 0.953` | `α=0.5` |
| `CREMI / U-Net` | `Dice 91.78` | `clDice 96.21` | `β1 Error 0.537` | `α=0.3` |
| `DRIVE / FCN` | `Dice 77.76~78.75` | `clDice up to 80.95` | `β1 Error down to 1.332` | `α=0.2~0.5` |
| `Vessap / U-Net 2ch` | `Dice up to 88.57` | `clDice up to 93.25` | `χ error 5.370` | `α=0.4` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `soft-Dice baseline` | `Roads / FCN` | `Dice 64.84` | `clDice 70.79` | `β0 Error 1.474` |
| `Lc(α=0.4)` | `Roads / FCN` | `Dice 67.18` | `clDice 76.92` | `β0 Error 0.934` |
| `soft-Dice baseline` | `DRIVE / FCN` | `clDice 78.02` | `β0 Error 2.187` | `β1 Error 1.860` |
| `Lc(α=0.5)` | `DRIVE / FCN` | `clDice 80.95` | `β0 Error 1.836` | `β1 Error 1.408` |
| `Mosinska et al.` | `Roads / U-Net` | `Accuracy 97.54` | `β1 Error 2.781` | `-` |
| `Hu et al.` | `Roads / U-Net` | `Accuracy 97.28` | `β1 Error 1.275` | `-` |

补充结论：

- 作者指出其方法在 Roads 和 CREMI 上与 Hu 等 topology 方法相比 `Accuracy / Betti Error` 至少持平或更好
- soft-clDice 几乎在所有实验中都优于纯 soft-Dice baseline

### 9.3 公平对比条件确认

- 是否统一 backbone：
  - `是，同一架构下仅替换 loss`
- 是否统一数据增强：
  - `[待确认，当前摘录未展开]`
- 是否统一后处理：
  - 文中重点是 end-to-end loss，对比未依赖额外后处理
- 是否统一输入尺寸：
  - `[待确认]`
- 结果来源：
  - `Table 1` 原文数字
- 页码：`p.5-p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：`3-fold cross-validation + held-out test`
- 结果汇报层级：`held-out test`
- Dice 类型：`volumetric Dice`
- clDice 类型：`centerlineDice / topology-aware similarity`
- 额外拓扑与图指标：
  - `β0 Error`
  - `β1 Error`
  - `SMD`
  - `χ error`
  - `OPT-J F1`
- 是否含后处理后再报结果：`未强调`
- 是否多 seed 平均：`以 cross-validation 为主`
- 是否报告标准差 / 置信区间：`主表未逐项给 std`
- 页码：`p.5-p.6`

---

## 10. 计算量与效率

- soft-skeleton 算法训练复杂度：
  - `O(k n^2)` 对于 `n × n` 2D 图像
- 其中 `k` 是 skeletonization iterations
- 与 persistent homology 类方法相比：
  - 训练计算更简单，避免 critical point matching 的高复杂度
- 实测运行开销：
  - `batch size 4, 1024×1024`
  - `soft-clDice: 1.35s`
  - `soft-Dice: 1.24s`
  - 额外开销 `<10%`
- 页码：`p.6`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/jocpae/clDice`
- 框架/语言：`[待确认，推测为 PyTorch，但当前摘录未直接写明]`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - soft-skeletonization 的 `k` 需要和数据最大半径匹配
  - 非 tubular 任务直接迁移时可能效果不稳定
  - 若要完整对比拓扑指标，需要实现 Betti / graph-based metrics

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定` | `中` |
| 验证集划分 | `是` | `3-fold CV + held-out test` | `低` |
| 推理阈值 | `否` | `需看官方代码` | `中` |
| 后处理细节 | `未突出` | `按 end-to-end 无后处理理解` | `中` |
| 训练轮数停止准则 | `否` | `需查官方实现` | `中` |
| 数据预处理 | `部分明确` | `按各 benchmark 官方设置补充` | `中` |

- 不确定但影响较大的点：
  - optimizer / lr / epoch 在当前主文摘录里未直接展开
  - `k` 的最终最佳值是强数据相关超参数

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 当前 soft-skeletonization 近似不是严格的 topology-preserving operator，只是 practical differentiable proxy
- 最适合 tubular / network-like structures，未来还需扩展到其他结构类型
- 页码：`p.6`

### 14.2 我们观察到的潜在问题

- 对块状器官或一般语义分割，clDice 可能不如 boundary/surface loss 直接
- `k` 需要与最大半径匹配，半径分布很宽的数据集调参成本较高
- 对腺体这种并非天然细长网络的目标，直接作为主损失未必合适，更可能只适合作为辅助正则或在 skeleton-aware 子任务中使用

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`通过 Figure 5 定性展示 soft-Dice 的 missed connections 和 false-positive connections`
- 典型失败场景：
  - `soft-Dice` 在 Roads / DRIVE 上常漏连通
  - `soft-Dice` 在 3D vessel 上可能出现 false-positive connections
- 对我们任务的映射：
  - 如果后续需要保持 gland skeleton / lumen connectivity，可借鉴 clDice
  - 如果只做普通 gland mask 分割，直接引入 clDice 可能会把目标函数带偏到 skeleton consistency
- 页码：`p.5-p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 对细长、分支、连通型目标使用 `soft-clDice` 作为辅助损失
- 用 `skeleton-mask intersection` 替代单纯体积重叠来强调 connectivity
- 用 `soft-skeletonization` 实现可微拓扑约束，而不是昂贵 persistent homology

### 15.2 可以作为候选参数来源的

- `Lc = (1-α)(1-softDice) + α(1-softclDice)`
- `α` 可先从 `0.1 ~ 0.5` 搜索
- `k` 至少要覆盖目标最大半径

### 15.3 不应照搬的（及原因）

- 把 clDice 直接作为腺体整体分割的唯一主损失：
  - 原因：腺体整体更接近区域/边界问题，不一定是 tubular connectivity 主导
- 直接照搬 vessel/road 的 `k`：
  - 原因：目标半径分布完全不同
- 仅根据 Dice 高低判断 clDice 是否有效：
  - 原因：它的主要收益经常体现在 connectivity / Betti / graph similarity 上

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 拓扑保持辅助损失 | soft-clDice 可显式优化 connectivity | `强` |
| skeleton-aware 监督 | soft-skeletonization 提供可微骨架代理 | `强` |
| 细小连通结构保护 | 比普通 Dice 更重视细连接段 | `强` |
| 腺体黏连/腔道结构分析 | 若后续引入 skeleton 或 lumen 连通子任务，可作为直接依据 | `中` |
| 普通 gland mask 分割 | 不是最直接主损失，更多是特定场景补充 | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失函数候选池`、`拓扑保持分支/子任务设计`
- [ ] 需要和哪篇论文交叉验证：`Boundary-Loss_2019`、`Shape-Aware-SDM_2020`
- [ ] 待确认的问题：`腺体任务是否存在值得显式保持的 skeleton / lumen connectivity`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 传统 Dice 对 network topology 次优 | 用于解释拓扑保持需求 |
| related work | topology-preserving differentiable loss 路线 | 放在 topology-aware supervision 小节 |
| 方法 | `soft-clDice` 与 `Lc(α)` 公式 | 作为 skeleton/connectivity 辅助损失依据 |
| 实验设置 | Betti / graph 指标体系 | 若项目涉及拓扑任务可参考 |
| 讨论 | 为什么有时 Dice 相近但 connectivity 差异很大 | 用于解释细连接段恢复 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1` | 两个 Dice 相同但拓扑不同的分割示例 | 写方法动机 |
| `Eq.(1)` | `p.3` | topology precision / sensitivity | 解释 clDice 构成 |
| `Eq.(2)` | `p.3` | clDice 定义 | 回填理论公式 |
| `Theorem 1 / Corollary 1.1` | `p.3-p.4` | homotopy-equivalence 保证 | 作为理论支撑 |
| `Algorithm 1` | `p.4` | soft-skeleton | 回填可微骨架实现 |
| `Algorithm 2` | `p.4` | soft-clDice | 回填损失实现 |
| `Eq.(3)` | `p.4` | `Lc(α)` 联合损失 | 回填训练目标 |
| `Table 1` | `p.5-p.6` | 五个数据集定量对比 | 主结果引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 `α`、`k`、数据集协议与效率
- [x] soft-skeleton 与 clDice 计算逻辑已记录
- [x] 主表关键结果已核对
- [x] 指标定义和评价协议已确认（Dice / clDice / Betti / graph）
- [x] 消融结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
