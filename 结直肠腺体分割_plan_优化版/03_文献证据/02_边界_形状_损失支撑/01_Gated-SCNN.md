# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `边界分支 + shape stream 结构论文`
- `boundary supervision / dual-task regularization 论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为这篇同时给出明确结构设计、训练协议和主表结果，所以额外补全：`3, 6, 7, 16`

---

## 1. 论文信息

- 论文名：`Gated-SCNN: Gated Shape CNNs for Semantic Segmentation`
- 作者/团队：`Towaki Takikawa, David Acuna, Varun Jampani, Sanja Fidler`
- 发表年份/会议/期刊：`2019, ICCV 2019`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1907.05740`
- BibTeX key：`takikawa2019gated`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Gated-SCNN_Gated_Shape_CNNs_for_Semantic_Segmentation_2019.pdf`
- 当前定位：`显式边界/形状分支的代表性论文；它不是单纯再加一个 edge loss，而是把 boundary information 作为独立 shape stream 建模，并用 gated interaction 和 dual-task regularizer 强化边界对齐`
- 与已提取论文的关系：
  - 可与：`DeepLabV3+_2018` 形成直接 baseline 对照
  - 互补于：`FPN_2017` 的多尺度语义增强；`Gated-SCNN` 更强调边界与 shape 表达
  - 可作为后续：`Boundary loss`、`Distance Map Loss`、`clDice`、`Shape-Aware SDM` 的结构侧支撑

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：论文提出一个 two-stream semantic segmentation architecture，把 shape information 显式作为单独 processing branch 并行建模
  - 用途：`方法动机 / 结构定位`
  - 页码：`Abstract, p.1`
- 句子/事实 2：高层 regular stream 语义用于 gate 低层 shape stream 响应，从而去噪并让浅层全分辨率 shape stream 只关注 boundary-related information
  - 用途：`边界分支设计依据`
  - 页码：`Abstract, p.1; Sec.3, p.3-p.4`
- 句子/事实 3：该设计 produces sharper predictions around object boundaries，并对 thinner and smaller objects 提升尤其明显
  - 用途：`边界与小目标痛点`
  - 页码：`Abstract, p.1; Sec.4, p.6-p.7`

#### 1.1.2 related work 可引用句

- 句子/事实 1：与只在 loss 层面联合 segmentation 和 boundary 的方法不同，Gated-SCNN 把 boundary information 显式注入网络中间处理流
  - 用途：`related work / 方法差异`
  - 页码：`Sec.2, p.2-p.3`
- 句子/事实 2：shape stream 不是简单拼接 regular stream feature，而是由 regular stream 的高层语义门控 shape stream 自身激活，抑制无关噪声
  - 用途：`结构创新点`
  - 页码：`Sec.3.1, p.3-p.4`
- 句子/事实 3：dual-task regularizer 进一步约束预测 segmentation 与 boundary 在边界空间上的一致性
  - 用途：`损失创新点`
  - 页码：`Sec.3.3, p.4-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 训练分辨率 | `800×800` | 训练设置 | `p.6` |
| 框架 | `PyTorch` | 复现设置 | `p.6` |
| batch size | `16 (8 GPUs)` | 训练设置 | `p.6-p.7` |
| 学习率 | `1e-2` | 优化器设置 | `p.6-p.7` |
| 学习率调度 | `polynomial decay` | 训练设置 | `p.6-p.7` |
| 消融训练轮数 | `100 epochs` | 消融设置 | `p.6` |
| 最优结果训练轮数 | `230 epochs` | 主表设置 | `p.6` |
| 联合损失权重 | `λ1=20, λ2=1, λ3=1, λ4=1` | 损失配置 | `p.6` |
| Gumbel softmax 温度 | `τ=1` | 梯度近似 | `p.6` |
| boundary threshold | `0.8` | dual-task regularizer | `p.5` |
| 单尺度验证推理 | `single-scale` | val 对比公平性 | `p.6` |
| 测试时多尺度推理 | `0.5, 1.0, 2.0` | test set 设置 | `p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 现有语义分割网络主要优化区域语义一致性，但对 object boundaries 的刻画不足
- 边界信息与区域语义信息相关但不相同，若只放在单流 dense representation 中，边界细节容易被高层语义吞没
- 小而细的目标更依赖 sharp boundaries，单纯全局 mIoU 不能充分反映这些对象的质量差异
- 仅在 loss 层联合 boundary task 不够，论文认为 boundary information 应在网络结构内部被显式建模并受语义引导

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`
- `Sec.2, p.2-p.3`
- `Sec.4.1, p.6-p.7`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `regular stream + shape stream + fusion module` 的 two-stream 架构：regular stream 负责常规语义表示，shape stream 以 semantic boundaries 为目标在高分辨率下浅层处理边界信息；两流之间通过 `Gated Convolutional Layer (GCL)` 交互，由高层语义门控低层 shape 响应；最后用 fusion module 和 ASPP 融合区域与边界特征，并用 `BCE + CE + dual-task regularizer` 同时约束 boundary prediction 与 segmentation output 的一致性。

关键页码：

- `Abstract, p.1`
- `Sec.3, p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`two-stream semantic segmentation network`
- Backbone：`regular stream 可接任意 segmentation backbone；文中实验使用 ResNet-50 / ResNet-101 / WideResNet`
- 输入尺寸：`训练时 800×800`
- 输出头：
  - `shape stream` 输出 boundary map `s`
  - `fusion module` 输出最终语义分割 `f = p(y|s, r)`

### 3.2 关键模块详细描述

**模块 1：`Regular Stream`**

- 位置：`主语义分支`
- 操作流程：
  1. 输入原始图像 `I`
  2. 用标准 segmentation CNN 提取 dense pixel features
  3. 输出低分辨率但语义强的特征表示 `r`
- 页码：`Sec.3, p.3`

**模块 2：`Shape Stream`**

- 位置：`并行边界/形状分支`
- 操作流程：
  1. 输入图像梯度 `∇I` 和 regular stream 第一层卷积输出
  2. 通过浅层 residual blocks 处理边界信息
  3. 在多个阶段插入 `GCL`，只保留 boundary-relevant responses
  4. 输出全分辨率 boundary map `s`
- 页码：`Sec.3, p.3-p.4`

**模块 3：`Gated Convolutional Layer (GCL)`**

- 位置：`regular stream 与 shape stream 的多处连接位置`
- 操作流程：
  1. 取某一阶段的 `st` 和 `rt`
  2. 拼接后经 `1×1 conv + sigmoid` 得到 attention map `αt`
  3. 用 `αt` 对 `st` 做逐元素门控
  4. 加上 residual 并经 channel weighting 得到更新后的 `ŝt`
- 页码：`Sec.3.1, p.3-p.4`

**模块 4：`Fusion Module`**

- 位置：`两流末端`
- 操作流程：
  1. 将 shape stream 输出的 boundary map 与 regular stream 的语义特征 `r` 融合
  2. 使用 `ASPP` 保留 multi-scale contextual information
  3. 输出最终语义分布 `f = p(y|s, r)`
- 页码：`Sec.3, p.3-p.4`

**模块 5：`Dual Task Regularizer`**

- 位置：`作用于 boundary prediction 与 segmentation prediction 的一致性约束`
- 操作流程：
  1. 从 segmentation output 导出边界潜变量 `ζ`
  2. 与 GT 边界 `ẑ` 比较，形成 `reg→`
  3. 再用 shape stream 的 boundary prediction `s` 约束 segmentation probabilities，形成 `reg←`
  4. 两项相加得到最终 dual-task regularizer
- 页码：`Sec.3.3, p.4-p.5`

### 3.3 结构关键点总结

| 组件 | 作用 | 关键设计 | 页码 |
|------|------|---------|------|
| `regular stream` | 学习区域语义 | 可插在任意标准 backbone 上 | `p.3` |
| `shape stream` | 学习 semantic boundaries | 浅层、全分辨率、局部监督 | `p.3-p.4` |
| `GCL` | 语义引导的边界去噪 | `1×1 conv + sigmoid` 产生门控图 | `p.3-p.4` |
| `fusion module` | 合并区域与边界信息 | 使用 `ASPP` 做多尺度融合 | `p.3-p.4` |
| `dual-task regularizer` | 强化边界与分割一致性 | 双向 consistency 约束 | `p.4-p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
αt = σ(C1×1(st || rt))
```

符号说明：

- `st`：第 `t` 个位置的 shape stream 中间特征
- `rt`：第 `t` 个位置的 regular stream 中间特征
- `||`：特征拼接
- `C1×1`：归一化的 `1×1` 卷积
- `σ`：sigmoid
- 含义：由 regular/shape 双流联合产生 attention map，对 shape stream 做语义引导门控
- 页码：`Eq.(1), p.4`

公式 2：

```text
ŝt(i, j) = ((st(i, j) ⊙ αt(i, j)) + st(i, j))T wt
```

符号说明：

- `⊙`：逐元素乘法
- `wt`：channel-wise weighting kernel
- 含义：先用 attention 抑制无关 shape 响应，再加 residual 保持原始边界信息，最后做通道重加权
- 页码：`Eq.(2), p.4`

公式 3：

```text
L = λ1 LBCE(s, ŝ) + λ2 LCE(ŷ, f)
```

符号说明：

- `s`：shape stream 输出 boundary map
- `ŝ`：GT boundary map
- `f`：fusion module 输出的 segmentation distribution
- `ŷ`：GT semantic labels
- 含义：同时监督 boundary prediction 与 semantic segmentation
- 页码：`Eq.(3), p.4`

公式 4：

```text
ζ = (1 / √2) ||∇(G * arg maxk p(yk | r, s))||
```

符号说明：

- `G`：Gaussian filter
- `p(yk | r, s)`：融合模块输出的第 `k` 类概率
- `ζ`：由 segmentation output 派生出的边界潜变量
- 含义：把 segmentation prediction 映射到 boundary space，为 dual-task regularizer 提供约束对象
- 页码：`Eq.(4), p.4-p.5`

公式 5：

```text
Lreg = Lreg→ + Lreg←
```

补充说明：

- `Lreg→`：约束 segmentation-derived boundary 与 GT boundary 对齐
- `Lreg←`：用高置信度 boundary prediction 约束 segmentation probabilities
- 论文通过 Gumbel softmax 近似 `argmax`，以保证可反向传播
- 页码：`Eq.(5)-(9), p.5`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 梯度特性：
  - dual-task regularizer 需要穿过 `argmax` 回传梯度
  - 论文用 `Gumbel softmax` 近似非可导 `argmax`
  - 温度参数设为 `τ = 1`
- 适用条件：
  - 需要有可从 mask 稳定生成的 GT semantic boundaries
  - 更适合重视边界质量和细小结构的任务
- 不适用场景：
  - 若训练集只有粗糙标注或边界标注不可靠，boundary supervision 质量会明显受限
  - 如果任务只关注粗区域 mIoU、边界不关键，则 dual-task regularizer 的收益可能变小
- 页码：
  - `Sec.3.3.1, p.5`
  - `Sec.4.1, p.6-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Boundary BCE` | `LBCE(s, ŝ)` | 监督 shape stream 输出 boundary map | shape stream 输出端，fusion 前 |
| `Segmentation CE` | `LCE(ŷ, f)` | 监督最终语义分割结果 | fusion module 输出端 |
| `Dual task reg→` | `λ3 Σ|ζ(p+) - ẑ(p+)|` | 约束 segmentation-derived boundary 与 GT boundary 对齐 | segmentation output 导出的 boundary space |
| `Dual task reg←` | `λ4 Σ 1s_p [ŷk_p log p(yk_p | r, s)]` | 用 boundary prediction 反向约束 segmentation | boundary prediction 与 semantic prediction 之间 |

### 5.2 总损失公式

```text
L_total = λ1 LBCE + λ2 LCE + λ3 Lreg→ + λ4 Lreg←
```

说明：

- 论文先给出联合监督 `LBCE + LCE`
- 再把 dual-task regularizer 分解为 `reg→` 与 `reg←`
- 实践上可把整篇方法理解为 `boundary supervision + segmentation supervision + boundary/region consistency regularization`

### 5.3 权重配置与调度策略

- 各项权重：
  - `λ1 = 20`
  - `λ2 = 1`
  - `λ3 = 1`
  - `λ4 = 1`
- 类别不平衡处理：
  - boundary BCE 中使用系数 `β` 处理 boundary / non-boundary 像素极度不平衡
- 阈值设置：
  - `thrs = 0.8`
- 是否衰减/动态调整：
  - 文中未报告动态 loss reweighting
- 页码：
  - `p.4-p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Cityscapes fine` | `2975` | `1525 test` | `500 val` | 主实验数据集 |
| `Cityscapes coarse` | `20,000 additional coarse annotations` | `-` | `-` | 本文 test set 结果不使用 coarse 训练 |

### 6.2 数据增强

- 增强列表：
  - `uniform sampling` 获取 `800×800` crop
  - `multi-scale inference` 使用 `0.5, 1.0, 2.0`
- Patch 提取策略：`800×800` crop，test set 最优模型采用按类别均匀采样
- 页码：`p.6-p.7`

### 6.3 优化器与超参数

- 框架：`PyTorch`
- 优化器：`[待确认，文中此处未在摘录段明确写出 optimizer 名称]`
- 初始学习率：`1e-2`
- 学习率调度：`polynomial decay`
- Batch size：`16 total on 8 GPUs`
- Epoch / Steps：
  - `100 epochs` 用于 ablation
  - `230 epochs` 报告 Table 1 最佳 val 结果
  - `175 epochs` 用于 WideResNet test set 最优模型
- 权重初始化：`ImageNet initialization`（至少在公平消融表中明确说明）
- 预训练策略：`ImageNet 预训练`
- 是否冻结部分层：`未见强调`
- 设备：`NVIDIA DGX Station, 8 GPUs`
- 页码：`p.6-p.7`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；自然场景语义分割`
- 颜色空间转换：`未强调`
- resize / crop / pad 策略：`训练分辨率 800×800`
- patch overlap：`不适用`
- 背景过滤策略：`无`
- 标签生成方式：
  - 语义标签：`Cityscapes semantic labels`
  - 边界标签：`从 GT semantic masks 生成 binary edges / semantic boundaries`
- 类别不平衡处理：`BCE 中使用 β 处理 boundary / non-boundary imbalance`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`按 Cityscapes 官方协议，未见额外风险`
- 页码：`p.4, p.6-p.7`

---

## 7. 推理与后处理

- 验证集主对比：
  - `single-scale inference`
  - 与 DeepLabV3+ 做公平比较时均仅使用 Cityscapes fine set 训练
- 测试集最优模型：
  - `multi-scale inference`，scales 为 `0.5, 1.0, 2.0`
- 概率阈值：
  - `thrs = 0.8` 用于 dual-task regularizer 内部高置信边界指示
- 后处理步骤：
  1. shape stream 先输出 boundary map
  2. 与 regular stream 特征经 fusion module / ASPP 融合
  3. 得到最终 segmentation output
- TTA / Test-time refinement：`有，多尺度测试`
- 页码：`p.5-p.7`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | baseline DeepLabV3+ vs `+ GCL` | mIoU 提升约 `1-2%`，boundary F-score 提升约 `3%` | 单独引入门控 shape stream 已有效 |
| `A2` | `+ GCL` vs `+ Dual Task` | `th=3/5/9/12 px` 的 boundary F-score 均进一步提升 | dual-task regularizer 明显改善边界对齐 |
| `A3` | 是否加入 image gradients | 在多 backbone 下继续带来小幅增益 | 显式梯度信息对边界流有辅助作用 |
| `A4` | 不同 backbone：ResNet-50 / 101 / WideResNet | 不同主干下均保持正向增益 | 方法具有 backbone-agnostic 特性 |

### 8.2 各模块贡献量化

- `GCL` 的独立贡献：
  - 与 baseline 相比，在不同 backbone 上带来约 `1-2%` 的 `mIoU` 提升，以及约 `3%` 的 boundary alignment 提升
- `Dual Task Regularizer` 的独立贡献：
  - `th=3px`：`64.1 -> 65.0 -> 68.0`
  - `th=5px`：`69.8 -> 70.8 -> 73.0`
  - `th=9px`：`74.8 -> 75.9 -> 77.2`
  - `th=12px`：`76.7 -> 77.8 -> 78.8`
  - 解释：从 `Baseline -> GCL -> + Dual Task` 逐步提升，说明一致性正则并不是冗余项
- 参数代价：
  - `ResNet-50`：`Param +0.43%`, `Perf +1.7 mIoU`, `+3.2 mF`
  - `ResNet-101`：`Param +0.29%`, `Perf +2.0 mIoU`, `+3.5 mF`
  - `WideResNet38`：`Param +0.13%`, `Perf +0.9 mIoU`, `+2.1 mF`
- 页码：`p.6-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Cityscapes val` | `mIoU 80.8` | `boundary F-score 73.6 @ 3px` | `boundary F-score 77.6 @ 5px` | 对比 DeepLabV3+ 单尺度、仅 fine set |
| `Cityscapes val` | `boundary F-score 80.7 @ 9px` | `boundary F-score 81.8 @ 12px` | `-` | 边界质量持续优于 baseline |
| `Cityscapes test` | `mIoU 82.8` | `-` | `-` | WideResNet regular stream，多尺度测试 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `GSCNN` | `Cityscapes val` | `mIoU 80.8` | `F-score@3px 73.6` | `F-score@5px 77.6` |
| `DeepLabV3+` | `Cityscapes val` | `mIoU 78.8` | `F-score@3px 69.7` | `F-score@5px 74.7` |
| `PSP-Net` | `Cityscapes val` | `mIoU 78.8` | `-` | `-` |
| `GSCNN` | `Cityscapes test` | `mIoU 82.8` | `published methods without coarse data 中领先` | `-` |

补充观察：

- `Cityscapes val` 上，`GSCNN` 相比 `DeepLabV3+`：
  - `mIoU: 78.8 -> 80.8`
  - `F-score@3px: 69.7 -> 73.6`
  - `F-score@5px: 74.7 -> 77.6`
  - `F-score@9px: 78.7 -> 80.7`
  - `F-score@12px: 80.1 -> 81.8`
- 对 `poles / traffic lights / traffic signs / motorcycles` 等小而细类别提升更明显
- distance-based evaluation 中，crop factor 从 `0` 增加到 `400` 时，与 `DeepLabV3+` 的差距由约 `2%` 扩大到接近 `6%`

### 9.3 公平对比条件确认

- 是否统一 backbone：
  - `Table 3/4` 中与自实现 baseline 使用相同 backbone 与同一套超参数，公平性较强
- 是否统一数据增强：
  - 消融中基本统一；val 比较明确限定为 `Cityscapes fine set`
- 是否统一后处理：
  - 文中未强调额外后处理，重点差异在结构和损失
- 是否统一输入尺寸：
  - 训练使用 `800×800`
- 结果来源：
  - `Table 1/2/3/4/6` 为原文数字
- 页码：`p.6-p.8`

### 9.4 评价协议与指标定义

- 数据划分来源：`Cityscapes 官方 train / val / test`
- 结果汇报层级：
  - `val`：给出 `mIoU` 与 boundary `F-score`
  - `test`：给出 benchmark `mIoU`
- Dice 类型：`不适用`
- Hausdorff 类型：`不适用`
- F1 类型：`boundary F-score`
- boundary 指标细节：
  - 使用 [41] 的 boundary metric
  - 阈值 `0.00088, 0.001875, 0.00375, 0.005`
  - 分别对应 `3, 5, 9, 12 pixels`
- 是否含后处理后再报结果：`未强调`
- 是否多 seed 平均：`未说明`
- 是否报告标准差 / 置信区间：`未说明`
- 是否和官方 challenge protocol 一致：`是（Cityscapes benchmark）`
- 页码：`p.6-p.7`

---

## 13. 开源与复现

- 代码是否开源：`[待确认；论文提供了 project website]`
- 代码仓库地址：`https://nv-tlabs.github.io/GSCNN/`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - dual-task regularizer 涉及 `argmax` 的可导近似
  - boundary GT 的生成方式需要与论文一致
  - regular stream / shape stream 的连接位置需要精确实现

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定多次重复` | `中` |
| 验证集划分 | `是` | `按 Cityscapes 官方 protocol` | `低` |
| 推理阈值 | `部分明确` | `dual-task 内部阈值用 0.8；最终分割阈值不单列` | `中` |
| 后处理细节 | `未突出` | `默认以 fusion output 为最终结果` | `中` |
| 训练轮数停止准则 | `部分明确` | `按 100/175/230 epochs 对应不同实验设置` | `中` |
| 数据预处理 | `部分明确` | `至少保留 800×800 crop 与 boundary 标签生成` | `高` |

- 不确定但影响较大的点：
  - `optimizer` 名称在当前摘录段未直接命中，需要后续若做严格复现再回 PDF 或官方实现确认
  - boundary GT 生成的具体滤波/离散细节若与论文不一致，可能影响 boundary F-score

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 该方法依赖高质量 boundary annotation；因此 test set 最优模型明确不使用 coarse data 训练
- 边界质量提升最明显，但这也意味着方法收益与任务是否重视 boundary strongly 相关
- 页码：`p.6-p.7`

### 14.2 我们观察到的潜在问题

- 这篇论文基于自然场景 Cityscapes，边界统计特征与腺体病理图像不同，不能把绝对超参数直接照搬
- shape stream 依赖图像梯度与语义边界的一致性，病理图像中染色变化、黏连和空腔结构可能导致噪声更复杂
- dual-task regularizer 的收益依赖边界标签质量，若腺体边界本身标注模糊，可能放大监督噪声
- 多尺度 ASPP + 双流结构会增加实现复杂度，不一定适合最轻量 baseline

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未专门以 “failure cases” 命名，但通过定性图说明 baseline 与本文在细目标边界上差异`
- 典型失败场景：
  - baseline 在 `poles` 等细目标上边界更粗糙
  - 远距离小目标更容易受益，反过来也说明这些正是传统单流结构的薄弱点
- 对我们任务的映射：
  - 若腺体黏连严重或边界模糊，shape stream 可能有助于分离
  - 若切片噪声导致假边界很多，则仅加 boundary branch 不一定稳，需要配合更鲁棒 loss
- 页码：`p.7-p.8`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `regular stream + shape stream` 的双流分工思路
- 用高层语义去门控低层边界流，而不是简单拼接边界特征
- 在 segmentation output 与 boundary space 之间增加一致性正则
- 用 boundary-specific metric 而不只看区域指标

### 15.2 可以作为候选参数来源的

- `boundary BCE + segmentation CE + consistency regularizer` 的组合框架
- 权重初值参考：`λ1=20, λ2=1, λ3=1, λ4=1`
- `thrs = 0.8`
- 在需要兼顾上下文和边界时，用 `ASPP` 作为 fusion module

### 15.3 不应照搬的（及原因）

- `Cityscapes 800×800` 的训练裁剪与多尺度测试比例：
  - 原因：病理图像 patch 尺度、显微倍率和目标尺寸分布完全不同
- `Canny / natural image gradients` 的使用方式：
  - 原因：病理纹理噪声更强，颜色与结构变化更复杂，边缘检测器可能不稳定
- 直接用 `mIoU + boundary F-score` 作为唯一评价协议：
  - 原因：腺体任务往往还要看 `Dice`、`HD/HD95`、对象级分割与黏连分离能力

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界分支 | shape stream 显式处理 semantic boundaries | `强` |
| 边界门控融合 | GCL 用高层语义门控低层边界特征，说明边界流不能完全裸跑 | `强` |
| 边界损失组合 | BCE + CE + dual-task regularizer 说明边界监督应与区域监督联动 | `强` |
| 细小结构强化 | 对 thinner and smaller objects 的显著提升，为小腺体/细边界假设提供外部证据 | `强` |
| 多尺度上下文 | fusion module 结合 ASPP，说明边界增强仍需全局语义上下文 | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`边界分支设计`、`损失函数候选池`、`评价指标设计`
- [ ] 需要和哪篇论文交叉验证：`Boundary loss 2019`、`Distance Map Loss 2019`、`Shape-Aware SDM 2020`
- [ ] 待确认的问题：`病理场景中图像梯度是否真的能稳定帮助边界流`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 单流分割网络边界质量不足、细小目标更受损 | 作为边界建模动机 |
| related work | 显式边界/形状分支代表作 | 放在 boundary-aware segmentation 小节 |
| 方法 | GCL、shape stream、boundary-region consistency 的设计依据 | 作为结构与损失来源 |
| 实验设置 | boundary F-score 阈值化评价思路 | 作为补充指标设计参考 |
| 讨论 | 哪些场景更受益于边界建模 | 用于解释小腺体和黏连区域结果 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1` | GSCNN 总览图：gated convolution、dual task regularizer、shape stream | 写方法定位 |
| `Figure 2` | `p.3` | regular stream + shape stream + fusion module 结构图 | 回填结构设计 |
| `Eq.(1)-(2)` | `p.4` | GCL 的 attention 与 gated update 公式 | 回填门控机制 |
| `Eq.(3)-(9)` | `p.4-p.5` | joint loss、dual-task regularizer、Gumbel softmax 梯度近似 | 回填损失设计 |
| `Table 1` | `p.6` | Cityscapes val mIoU 主结果 | 数字引用 |
| `Table 2` | `p.6` | boundary F-score 主结果 | 边界指标引用 |
| `Table 4` | `p.7` | Dual Task loss 消融 | 说明正则项必要性 |
| `Figure 5` | `p.7` | distance-based evaluation | 支撑“小而远目标收益更大” |
| `Table 6` | `p.7-p.8` | Cityscapes test set benchmark | 写 benchmark 结论 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 `lr / batch / epoch / resolution / loss weights`
- [x] 标签与边界监督来源已检查
- [x] 结果数字与原文 table 关键项已核对
- [x] 指标定义和评价协议已确认（含 boundary F-score 阈值）
- [x] 消融实验已量化，不只写“有效”
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
