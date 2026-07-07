# 通用文献深提取模板

> 使用说明：每篇论文新建一个文件，复制本模板，先填第 0 节确定论文类型，再按指引填写对应章节。
> 命名规范：`XX_结直肠腺体分割_单篇深提取_论文简称.md`

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `A - 方法论文`
- `H - 注意力论文`

### 0.2 章节填写指引

| 章节 | A 方法 | B 损失/模块 | C 综述 | D 病理临床 | E 半监督 | F 数据集 | G 基线 | H 大核/注意力 |
|------|--------|------------|--------|-----------|---------|---------|--------|-------------|
| 1. 论文信息 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 |
| 2. 问题定义与动机 | 必填 | 必填 | 选填 | 必填 | 必填 | 必填 | 选填 | 必填 |
| 3. 模型/方法结构 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 跳过 | 必填 | 必填 |
| 4. 公式与推导 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 跳过 | 选填 | 必填 |
| 5. 损失函数 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 跳过 | 选填 | 选填 |
| 6. 训练协议 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 选填 | 必填 | 必填 |
| 7. 推理与后处理 | 必填 | 选填 | 跳过 | 跳过 | 选填 | 跳过 | 选填 | 选填 |
| 8. 消融实验 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 跳过 | 跳过 | 必填 |
| 9. 主表结果与对比 | 必填 | 必填 | 跳过 | 选填 | 必填 | 必填 | 必填 | 必填 |
| 10. 计算量与效率 | 选填 | 选填 | 跳过 | 跳过 | 选填 | 跳过 | 必填 | 必填 |
| 11. 分类体系与研究空白 | 跳过 | 跳过 | 必填 | 选填 | 跳过 | 选填 | 跳过 | 跳过 |
| 12. 临床/病理标准 | 跳过 | 跳过 | 跳过 | 必填 | 跳过 | 跳过 | 跳过 | 跳过 |
| 13. 开源与复现 | 必填 | 必填 | 跳过 | 跳过 | 必填 | 必填 | 必填 | 必填 |
| 14. 局限性与失败案例 | 必填 | 必填 | 选填 | 选填 | 必填 | 选填 | 选填 | 必填 |
| 15. 对我们项目的落地价值 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 | 必填 |
| 16. 关键图表索引 | 必填 | 选填 | 选填 | 选填 | 选填 | 选填 | 选填 | 必填 |

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇同时也是注意力模块代表作，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`Attention U-Net: Learning Where to Look for the Pancreas`
- 作者/团队：`Ozan Oktay, Jo Schlemper, Loic Le Folgoc, Matthew Lee, Mattias Heinrich, Kazunari Misawa, Kensaku Mori, Steven McDonagh, Nils Y Hammerla, Bernhard Kainz, Ben Glocker, Daniel Rueckert`
- 发表年份/会议/期刊：`2018, MIDL 2018, Amsterdam, The Netherlands；同时提供 arXiv 版本`
- DOI / arXiv ID：`10.48550/arXiv.1804.03999` / `arXiv:1804.03999`
- BibTeX key：`oktay2018attentionunet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/Attention_U-Net_2018.pdf`
- 当前定位：`经典注意力增强 U-Net 基线，用于支撑“在 skip connection 上做轻量注意力筛选”这条外部对比路线`
- 与已提取论文的关系：
  - 继承自：`U-Net` 的 encoder-decoder + skip connection 主骨架；注意力形式与 soft attention / additive attention 文献相关
  - 被谁引用/改进：后续大量 `Attention U-Net` 变体、病理图像注意力 U-Net、腺体分割中的 `SCAU-Net`、`AttentionBoost` 等路线
  - 互补论文：`U-Net_2015`、`UNet++_2018`、`DeepLabV3+_2018`、`SCAU-Net_2020`

### 1.1 可直接引用卡片

> 这里专门记录“后面写论文时可以直接拿来用”的内容，避免做完深提取后还得回 PDF 里二次找。

#### 1.1.1 引言可引用句

- 句子/事实 1：`标准 FCN / U-Net 在目标形状和大小变化很大时，常依赖额外的 cascaded localisation model 先找 ROI 再做精分割`
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：`Attention gate 可以在不引入显著计算开销、也不需要多模型级联的情况下，自动聚焦目标区域并提升 sensitivity 与 prediction accuracy`
  - 用途：`方法动机`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`Attention U-Net 的核心不是重做整个主干，而是在 U-Net 的 skip connection 上插入 AG，让 coarse-scale gating signal 过滤低层特征`
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.3-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 优化器 | `Adam` | 实验设置 | `p.6` |
| Batch size | `2-4` | 实验设置 | `p.6` |
| 数据增强 | `affine transformations + axial flips + random crops` | 实验设置 | `p.6` |
| 指标定义 | `DSC / Precision / Recall / S2S distance` | 评价协议说明 | `p.6-p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 标准 `FCN / U-Net` 在目标器官形状、大小、位置变化较大时，常需要额外的 cascaded localisation model 先做 ROI 定位再做精分割
- cascaded 框架会重复提取相似的低层特征，增加计算和参数冗余
- 对于小器官且边界模糊、形态变化大的场景，普通 skip connection 容易把无关背景激活一并传给解码器，导致 false positive 难以抑制
- 目标是让网络在不使用外部定位模型的情况下，自动聚焦目标区域并提升 foreground sensitivity

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 在标准 `U-Net` 的 skip connection 上加入 `attention gate (AG)`，利用来自更粗尺度的 gating signal 过滤低层特征，只把与当前任务更相关的激活送入解码端；这样既保留 U-Net 的多尺度融合框架，又在前向和反向传播中抑制无关背景响应，从而减少对外部 ROI localisation 模块的依赖。

关键页码：

- `p.1`
- `p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`3D encoder-decoder U-Net with attention-gated skip connections`
- Backbone：`3D U-Net`
- 输入尺寸：`论文未固定一个全局训练 patch 尺寸；推理时间统计对应输入 tensor 为 160×160×96`
- 输出头：`分割头；在 CT-150 上为多类腹部器官分割，在 TCIA 上聚焦 pancreas`

### 3.2 关键模块详细描述

> 每个创新模块单独一小节，写清楚：放在哪里、输入输出是什么、具体操作步骤

**模块 1：`Additive Attention Gate (AG)`**

- 位置：`每个需要被筛选的 skip connection 之前，在与 decoder 特征拼接前进行 gating`
- 操作流程：
  1. 从浅层 skip feature `x_l` 取当前尺度特征，同时从更粗尺度取 gating signal `g`
  2. 用 `1×1×1` 线性变换把 `x_l` 与 `g` 映射到同一个中间空间，再经过 `ReLU`
  3. 再通过一个线性映射和 `sigmoid` 生成 attention coefficient `α`
  4. 用 `α` 对输入特征做逐元素缩放，得到过滤后的 `x_hat`
- 页码：`p.4-p.5`

**模块 2：`Grid-based Gating`**

- 位置：`AG 内部，不使用单一全局向量作为 gating，而是使用带空间分辨率的 grid signal`
- 操作流程：
  1. gating signal 不再是全图共享的单个向量，而是保留局部空间信息的 coarse grid
  2. 每个 skip connection 对应的 gating signal 汇聚多个尺度的上下文信息
  3. 由此生成更具局部针对性的 attention coefficient，而不是粗糙的全局 gating
- 页码：`p.2, p.4-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Encoder Stage 1 | conv block | `F1` | `H1×W1×D1` | 标准 U-Net 编码器起点 |
| Encoder Stage 2 | conv block + pool | `F2` | `H2×W2×D2` | 逐层下采样 |
| Encoder Stage 3 | conv block + pool | `F3` | `H3×W3×D3` |  |
| Encoder Stage 4 | conv block + pool | `F4` | `H4×W4×D4` | 最粗尺度上下文 |
| Skip Connections | gated skip | `F1/F2/F3` | 对应各尺度 | 由 AG 过滤后再拼接 |
| Decoder Stages | upsampling + concat + conv | 对应尺度通道 | 逐层恢复分辨率 | AG 放在 concat 前 |
| Output | segmentation map | `Nc` | `H1×W1×D1` | `Nc` 为类别数 |

说明：

- 论文图中给出的是符号级架构示意，而不是精确的每层通道数表
- 精确的 `F1-F4` 数值在正文中未明确列出，属于`[待确认]`
- 该文重点是证明 `AG` 的接入方式与效果，而不是发布一张可直接复刻的完整层配置表

---

## 4. 公式与推导

### 4.1 核心公式

> 列出论文中最重要的 1-3 个公式，写明符号含义

公式 1：

```text
q_att^l = ψ^T(σ1(W_x^T x_i^l + W_g^T g_i + b_g)) + b_ψ
```

符号说明：

- `x_i^l`：第 `l` 层、第 `i` 个位置的输入特征
- `g_i`：来自更粗尺度的 gating signal
- `W_x, W_g`：把输入特征和 gating signal 映射到中间空间的线性变换
- `σ1`：`ReLU`
- `ψ`：把中间表示压成一个 attention logit 的线性映射
- `b_g, b_ψ`：偏置项
- 页码：`p.4`

公式 2：

```text
α_i^l = σ2(q_att^l(x_i^l, g_i; Θ_att))
```

符号说明：

- `α_i^l`：第 `l` 层、第 `i` 个位置的 attention coefficient
- `σ2`：`sigmoid`
- `Θ_att`：attention gate 的参数集合
- 页码：`p.4`

公式 3：

```text
x̂_i,c^l = x_i,c^l · α_i^l
```

符号说明：

- `x̂_i,c^l`：经 attention gate 过滤后的输出特征
- `x_i,c^l`：输入特征
- `α_i^l`：attention coefficient
- 页码：`p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 梯度特性：`AG` 不只在前向传播中筛选特征，也会在反向传播中对来自背景区域的梯度进行 down-weight，使浅层参数更新更聚焦于任务相关区域
- 适用条件：适合需要在 skip connection 上传递低层细节、但又容易引入背景噪声的 encoder-decoder 结构
- 不适用场景：论文未系统讨论 2D 自然图像或病理图像场景；对极大目标或强对比目标的收益可能不如小器官明显
- 页码：`p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| Sorensen-Dice loss | `论文正文未展开公式` | 多类器官分割 | 最终分割输出 |
| Deep supervision | `论文未单独列出公式` | 让中间尺度特征更具语义判别性 | 多尺度中间层 |

### 5.2 总损失公式

```text
L_total = Sorensen-Dice loss over all semantic classes + deep-supervision related auxiliary constraints
```

说明：

- 论文明确写了主损失使用 `Sorensen-Dice loss`
- `deep-supervision` 被用于提升中间特征的语义可分性
- 但完整加权公式和每一项权重在正文中未明确展开，属于`[待确认]`

### 5.3 权重配置与调度策略

- 各项权重：`[待确认]`
- 是否衰减/动态调整：`正文未明确说明`
- 页码：`p.5, p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `CT-150` | `120` | `30` | `正文未单独说明验证集` | 多类腹部 CT，pancreas/liver/spleen |
| `CT-150` | `30` | `120` | `同上` | 用于测试小训练集下的鲁棒性 |
| `TCIA Pancreas-CT (CT-82)` | `61` | `21` | `fine-tune / scratch` | 报告 `BFT/AFT/SCR` 三组结果 |

### 6.2 数据增强

- 增强列表：
  - `affine transformations`
  - `axial flips`
  - `random crops`
- Patch 提取策略：`随机裁剪，但具体 crop size 未明确写出 [待确认]`
- 页码：`p.6`

### 6.3 优化器与超参数

- 框架：`PyTorch`
- 优化器：`Adam`
- 初始学习率：`[待确认]`
- 学习率调度：`正文未明确说明`
- Batch size：`2-4`
- Epoch / Steps：`正文未给出明确 epoch 数`
- 权重初始化：`gating parameters 初始为让 AG 在所有空间位置先近似通过特征`
- 预训练策略：`在 TCIA 上报告了直接迁移(BFT)、微调(AFT)、从头训练(SCR)；结论部分还讨论了可用 pre-trained U-Net 初始化 AG 网络`
- 是否冻结部分层：`未明确说明`
- 设备：`未明确说明`
- 页码：`p.6, p.8`

### 6.4 预处理与数据细节

> 这部分专门防止论文只写了主干训练参数，但遗漏真正影响复现的实现细节。

- stain normalization / color normalization：`不适用，CT 任务`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：`所有图像下采样到 isotropic 2.00 mm resolution；训练中使用 random crops`
- patch overlap：`[待确认]`
- 背景过滤策略：`未明确说明`
- 标签生成方式：`原始器官分割 mask`
- 类别不平衡处理：`采用 Sorensen-Dice loss，作者称其对 class imbalance 不那么敏感`
- 随机种子/重复次数：`未明确说明`
- 数据泄漏风险点：`正文未见同 patient / same scan 泄漏说明；但这里是 CT 腹部公开/内部数据，不是病理 slide 视野问题`
- 页码：`p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：`推理时间统计对应输入 tensor 160×160×96`
- 概率阈值：`正文未明确说明`
- 后处理步骤：
  1. `论文强调其框架不依赖外部 localisation model`
  2. `与文中主要对比实验一致时，不使用额外 post-processing，如 CRF`
- TTA / Test-time refinement：`未提到`
- 页码：`p.6-p.7`

---

## 8. 消融实验

### 8.1 消融设计

> 论文做了哪些消融？每个消融关闭/替换了什么？

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | `Attention U-Net` vs `U-Net` on `CT-150 (120/30)` | `Pancreas DSC 0.814 -> 0.840`，`Recall 0.806 -> 0.841`，`S2S 2.358 -> 1.920` | AG 的主要收益体现在 recall 和边界距离改善 |
| 2 | `Attention U-Net` vs `U-Net` on `CT-150 (30/120)` | `Pancreas DSC 0.741 -> 0.767` | 小训练集下收益仍保持 |
| 3 | `Attention U-Net` vs larger-capacity `U-Net` | `6.40M` 参数的 Attention U-Net 优于 `6.44M / 10.40M` 的普通 U-Net | 收益不只是“加参数”，而是 AG 的结构作用 |
| 4 | `U-Net` vs `Attention U-Net` on `TCIA` 的 `BFT/AFT/SCR` | 三种设置下 Attention U-Net 都略优于 U-Net | AG 具有跨数据集与微调场景的一致增益 |

### 8.2 各模块贡献量化

- 模块 A 的独立贡献：`AG` 在 `CT-150 (120/30)` 上带来 `+0.026 DSC`、`+0.035 recall`、`-0.438 mm S2S`
- 模块 B 的独立贡献：`grid-based gating + skip filtering` 的贡献体现为参数仅从 `5.88M` 增加到 `6.40M`，但优于更大参数量的普通 U-Net
- 页码：`p.6-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `CT-150 (120/30)` | `Pancreas DSC 0.840 ± 0.087` | `Recall 0.841 ± 0.092` | `S2S 1.920 ± 1.284 mm` | Attention U-Net |
| `CT-150 (30/120)` | `Pancreas DSC 0.767 ± 0.132` | `Recall 0.762 ± 0.145` | `S2S 3.507 ± 3.814 mm` | Attention U-Net |
| `TCIA BFT` | `Dice 0.712 ± 0.110` | `Recall 0.751 ± 0.149` | `S2S 5.251 ± 2.551 mm` | 直接迁移 |
| `TCIA AFT` | `Dice 0.831 ± 0.038` | `Recall 0.840 ± 0.053` | `S2S 2.305 ± 0.568 mm` | 微调后 |
| `TCIA SCR` | `Dice 0.821 ± 0.057` | `Recall 0.835 ± 0.057` | `S2S 2.333 ± 0.856 mm` | 从头训练 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| 本文方法 `Attention U-Net` | `CT-150 (120/30)` | `DSC 0.840` | `Recall 0.841` | `S2S 1.920 mm` |
| `U-Net` | `CT-150 (120/30)` | `DSC 0.814` | `Recall 0.806` | `S2S 2.358 mm` |
| 更大参数量 `U-Net` | `CT-150 (120/30)` | `DSC 0.821 / 0.825` | `Recall 0.814 / 0.807` | `S2S 2.383 / 2.202 mm` |
| 本文方法 `Attention U-Net` | `TCIA AFT` | `Dice 0.831` | `Recall 0.840` | `S2S 2.305 mm` |
| `U-Net` | `TCIA AFT` | `Dice 0.820` | `Recall 0.828` | `S2S 2.464 mm` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，主对比是 standard 3D U-Net`
- 是否统一数据增强：`是，主比较基于同一训练流程`
- 是否统一后处理：`是，作者强调未使用额外 post-processing`
- 是否统一输入尺寸：`主比较保持一致；推理时间在相同 160×160×96 输入上统计`
- 结果来源：`原文数字`
- 页码：`p.6-p.7`

### 9.4 评价协议与指标定义

> 腺体分割里“同名指标不同定义”很常见，这一节专门把协议锁死。

- 数据划分来源：`作者自定义训练/测试划分`
- 结果汇报层级：`test set`
- 实例匹配规则：`不适用，本篇不是实例分割协议`
- Dice 类型：`DSC, pixel-wise Dice similarity coefficient`
- Hausdorff 类型：`不是 Hausdorff，而是 mesh surface-to-surface distance (S2S)`
- F1 类型：`未使用`
- 是否含后处理后再报结果：`否，作者强调未用额外 post-processing`
- 是否多 seed 平均：`正文未明确说明`
- 是否报告标准差 / 置信区间：`报告均值 ± 标准差`
- 是否和官方 challenge protocol 一致：`否，本篇不是 GlaS/CRAG/challenge 论文`
- 页码：`p.6-p.7`

---

## 10. 计算量与效率

- 参数量（Params）：`U-Net 5.88M`，`Attention U-Net 6.40M`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`U-Net 0.167 s`，`Attention U-Net 0.179 s`
- 训练时间（总 GPU-hours）：`未报告`
- 输入尺寸（计算量对应的）：`160×160×96`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `U-Net` | `5.88M` | `未报告` | `0.167 s` |
| `Attention U-Net` | `6.40M` | `未报告` | `0.179 s` |
| `Larger U-Net` | `6.44M / 10.40M` | `未报告` | `0.191 s / 0.222 s` |

- 页码：`p.6-p.7`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

跳过。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

跳过。

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/ozan-oktay/Attention-Gated-Networks`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：`这是 3D 腹部 CT 分割任务，不是病理腺体分割；正文未给出完整学习率和精确 patch 尺寸等细节`

### 13.1 论文未报告但复现必需的信息

> 这里不要空着。论文没写清楚的东西，后面最容易被误当成“论文默认值”。

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不视为论文固定值 | 中 |
| 验证集划分 | 否 | 不强行补造验证集规则 | 高 |
| 推理阈值 | 否 | 仅引用结果，不照搬推理细节 | 中 |
| 后处理细节 | 部分 | 记录为“未用额外 post-processing” | 中 |
| 训练轮数停止准则 | 否 | 不把 epoch 当论文固定值 | 高 |
| 数据预处理 | 部分 | 只记录已明确写出的 `2.00 mm isotropic + random crops + intensity scaling` | 中 |

- 不确定但影响较大的点：
  - `学习率`
  - `精确 patch size`
  - `deep supervision 的具体权重`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- `AG` 的训练行为还可以从 transfer learning 和 multi-stage training 中继续受益
- residual connection around gate 在作者实验里尚未带来显著性能提升，后续仍需探索更优 gating architecture
- 由于 GPU 显存限制，当前 3D 模型需要对图像做下采样；如果未来可以用更大 batch 和更高分辨率输入，性能还有提升空间
- 页码：`p.8`

### 14.2 我们观察到的潜在问题

- 这篇不是病理图像论文，数据分布、纹理统计和目标形态与腺体分割差异很大
- 论文证明了 `AG` 结构有用，但没有提供完整层级超参数表，因此作为“可直接复刻基线”的程度不如 `U-Net` 或 `UNet++`
- 主要收益集中在 pancreas 这类小器官定位与 recall 改善，迁移到 gland segmentation 时是否同样显著，需要实证验证

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是，给出 U-Net 与 Attention U-Net 的可视化对比，强调 U-Net 的 missed dense predictions`
- 典型失败场景：`小器官定位不足、边界附近漏检、背景干扰导致召回不足`
- 页码：`p.4, p.6`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- （列出可以直接写入我们实验 protocol 的内容）
  - `把 attention gate 放在 skip connection 上，在拼接前先过滤浅层特征`
  - `把 Attention U-Net 作为外部对比中的“轻量注意力增强 U 形结构”代表`

### 15.2 可以作为候选参数来源的

- （不能照搬但可作为参考范围的参数/策略）
  - `Adam`
  - `小 batch（2-4）+ data augmentation + deep supervision`

### 15.3 不应照搬的（及原因）

- `CT 任务的全部训练设置`
  - 原因：`数据模态、目标类型、类别定义和评价协议与 GlaS/CRAG 完全不同`
- `CT-150 / TCIA 上的 Dice 和 S2S 数字`
  - 原因：`不能作为腺体任务的直接性能预期`
- `2.00 mm isotropic downsampling`
  - 原因：`属于 3D CT 体数据预处理，不适用于 2D 病理图像`

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 是否加入注意力增强对比 | 证明在 U-Net skip connection 上加 AG 是经典且轻量的做法 | 强 |
| 注意力模块放置位置 | 明确应放在 skip connection、concat 前 | 强 |
| 是否能直接照搬训练参数 | 仅提供泛化参考，不能作为腺体任务固定值 | 弱 |
| 讨论 attention 是否只是“加参数” | 表 2 证明收益不只是简单加大模型容量 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`01_实验执行/08_外部对比/04_AttUNet适配方案.md`
- [ ] 需要和哪篇论文交叉验证：`SCAU-Net_2020`、`AttentionBoost_2020`、`U-Net_2015`
- [ ] 待确认的问题：`在腺体任务上，AG 更适合单独作为外部对比，还是适合并入我们主线做轻量注意力变体`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | encoder-decoder 在变形目标上常需更强目标聚焦 | 作为注意力模块动机 |
| related work | 注意力增强 U-Net 的经典代表 | 放在外部对比和经典 attention 路线里 |
| 方法 | 如果后续加入 skip attention，可引用 AG 的放置位置与 gating 机制 | 只引用结构思路，不冒充完全复现 |
| 实验设置 | `Attention U-Net` 可作为第一批外部对比之一 | 用于方法名单和角色定义 |
| 讨论 | 可讨论“收益来自结构筛选而非单纯加参数” | 用于解释注意力模块的价值边界 |

---

## 16. 关键图表索引

> 记录论文中值得引用、重绘或参考的图表，方便后续写论文时快速定位

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig.1` | `p.3` | Attention U-Net 总体结构图 | 参考注意力模块放置位置 |
| `Fig.2` | `p.4` | Additive attention gate 示意图 | 参考 AG 内部计算流程 |
| `Fig.3` | `p.4-p.5` | gated feature activation 与可视化预测对比 | 写方法直觉与失败模式 |
| `Fig.4` | `p.6` | 不同 epoch 下 attention coefficient 演化 | 说明 AG 学到的聚焦行为 |
| `Table 1` | `p.6-p.7` | CT-150 主结果表 | 数字引用 |
| `Table 2` | `p.7` | 与更大 U-Net 容量对比 | 证明不是单纯靠加参数 |
| `Table 3` | `p.7` | TCIA BFT/AFT/SCR 结果 | 迁移与微调表现 |
| `Table 4` | `p.7` | 与 SOTA pancreas segmentation 对比 | related work 参照 |

---

## 17. 提取质量自检

> 提取完成后，对照以下清单确认信息完整度

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够复现（优化器+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查（stain normalization / patch overlap / label 生成）
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认（不是只记指标名字）
- [x] 消融实验的结论已量化（不只是"有效"）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
