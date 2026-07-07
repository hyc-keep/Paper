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

- `encoder-decoder 改进基线`
- `dense / nested skip 路线`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇是对 `U-Net` 主干的直接结构性改进，所以额外完成：`2, 4, 5, 8, 14`

---

## 1. 论文信息

- 论文名：`UNet++: A Nested U-Net Architecture for Medical Image Segmentation`
- 作者/团队：`Zongwei Zhou, Md Mahfuzur Rahman Siddiquee, Nima Tajbakhsh, Jianming Liang`
- 发表年份/会议/期刊：`2018, DLMIA 2018 / MICCAI workshop`
- DOI / arXiv ID：`10.1007/978-3-030-00889-5_1` / `arXiv:1807.10165`
- BibTeX key：`zhou2018unetpp`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/UNet++_2018.pdf`
- 当前定位：`对 U-Net skip connection 的经典改造基线，代表“通过 nested dense skip pathways 缩小 encoder-decoder semantic gap”的路线`
- 与已提取论文的关系：
  - 继承自：`U-Net_2015` 的 encoder-decoder + skip connection 主结构
  - 被谁引用/改进：后续大量 `UNet++` 医学图像变体、3D 扩展版本、轻量/注意力/残差型 nested U-Net 结构
  - 互补论文：`U-Net_2015`、`Attention_U-Net_2018`、`MILD-Net_2018`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：医疗图像分割对边界和细节的准确性要求比自然图像更高，哪怕是边缘附近的微小误差也可能影响后续诊断
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：普通 `U-Net` 的 plain skip connection 会直接融合语义差异很大的 encoder 与 decoder 特征，这种 semantic gap 可能损害分割性能
  - 用途：`方法动机`
  - 页码：`p.2-p.4`
- 句子/事实 3：`UNet++ with deep supervision` 平均比 `U-Net` 和 `wide U-Net` 分别高 `3.9` 和 `3.4` 个 IoU 点
  - 用途：`结果概述`
  - 页码：`Abstract, p.1, p.7-p.8`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`UNet++` 的关键不是换 backbone，而是重做 skip pathway，让 encoder 高分辨率特征在融合前先逐步语义增强
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.5`
- 句子/事实 2：deep supervision 让 `UNet++` 可以在 accurate mode 和 fast mode 两种推理方式之间切换，并支持 pruning
  - 用途：`结构特点 / 工程价值`
  - 页码：`p.4-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 优化器 | `Adam` | 实验设置 | `p.6` |
| 学习率 | `3e-4` | 实验设置 | `p.6` |
| 基础通道规则 | `k = 32 × 2^i` | 架构设计 | `p.6` |
| U-Net 参数量 | `7.76M` | 外部对比 | `p.7` |
| Wide U-Net 参数量 | `9.13M` | 外部对比 | `p.7` |
| UNet++ 参数量 | `9.04M` | 外部对比 | `p.7` |
| 剪枝速度收益 | `32.2%` | 工程价值 | `p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 医疗图像分割比自然图像分割更强调边缘与细微结构的精确恢复
- 原始 `U-Net` 的 plain skip connection 直接融合浅层高分辨率特征和深层高语义特征，二者语义差距较大
- 这种 semantically dissimilar 的特征融合会让优化更困难，也可能拖累最终分割质量
- 目标是让 encoder 特征在送入 decoder 前先经过渐进式语义增强，使其与 decoder 特征更“语义对齐”

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- `UNet++` 在 `U-Net` 基础上重设计了 skip pathway：不再把 encoder 特征直接跳连给 decoder，而是让它们沿着嵌套的 dense convolution block 逐步演化，并持续接收来自下层上采样特征的输入，从而缩小 encoder-decoder 之间的 semantic gap；同时在多个全分辨率语义层上施加 deep supervision，使模型既可追求更高精度，也可通过选择分支实现推理剪枝。

关键页码：

- `p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`deeply-supervised nested encoder-decoder network`
- Backbone：`U-Net style encoder-decoder backbone`
- 输入尺寸：依数据集而定，文中实验使用 `96×96`、`224×224`、`512×512`、`64×64×64`
- 输出头：在 `{X0,1, X0,2, X0,3, X0,4}` 这些 full-resolution semantic levels 上都可接分割头

### 3.2 关键模块详细描述

**模块 1：`Re-designed Skip Pathways`**

- 位置：`encoder 与 decoder 各级之间的 skip connection`
- 操作流程：
  1. 对于普通 `U-Net`，encoder 特征会直接送入 decoder
  2. 对于 `UNet++`，encoder 特征先进入一个 dense convolution block
  3. 该 dense block 的每一层都接收来自同一路径历史节点的输出和下层 skip pathway 上采样来的特征
  4. 经过多层卷积后，encoder 特征在融合前被逐步“语义对齐”
- 页码：`p.3-p.5`

**模块 2：`Nested Dense Skip Connections`**

- 位置：`每条 skip pathway 内部`
- 操作流程：
  1. 设 `X_{i,j}` 表示第 `i` 个编码层、第 `j` 个 skip dense block 节点
  2. 当 `j=0` 时，节点只接收来自 encoder 上一层的输入
  3. 当 `j>0` 时，节点接收同一 skip pathway 上先前所有节点的输出
  4. 同时再接收来自更低层 skip pathway 上采样后的输出
- 页码：`p.4-p.5`

**模块 3：`Deep Supervision`**

- 位置：`多个 full-resolution decoder semantic levels`
- 操作流程：
  1. 在 `{X0,j | j ∈ {1,2,3,4}}` 上都接 `1×1 conv + sigmoid`
  2. 每个分支都产生一张 segmentation map
  3. `accurate mode` 对所有分支输出求平均
  4. `fast mode` 只选某一条分支输出，以换取剪枝和速度提升
- 页码：`p.4-p.6`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| `X0,0 / X0,4` | encoder/decoder stage 0 | `32` | full resolution | U-Net 基础通道起点 |
| `X1,0 / X1,3` | stage 1 | `64` | `1/2` 分辨率 |  |
| `X2,0 / X2,2` | stage 2 | `128` | `1/4` 分辨率 |  |
| `X3,0 / X3,1` | stage 3 | `256` | `1/8` 分辨率 |  |
| `X4,0 / X4,0` | bottleneck | `512` | `1/16` 分辨率 |  |

对比结构参数量：

| 架构 | 参数量 |
|------|--------|
| `U-Net` | `7.76M` |
| `wide U-Net` | `9.13M` |
| `UNet++` | `9.04M` |

说明：

- `UNet++` 的参数量和 `wide U-Net` 接近，因此作者特地用它来排除“只是参数更多”的解释
- 每条 skip pathway 上的卷积都使用 `k = 32 × 2^i` 个 `3×3` 卷积核；3D lung nodule 任务用 `3×3×3`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
x_{i,j} = H(x_{i-1,j}),               j = 0
x_{i,j} = H([ [x_{i,k}]_{k=0}^{j-1}, U(x_{i+1,j-1}) ]),   j > 0
```

符号说明：

- `x_{i,j}`：节点 `X_{i,j}` 的输出特征
- `i`：encoder 下采样层索引
- `j`：skip pathway 上 dense block 的卷积层索引
- `H(.)`：卷积 + 激活操作
- `U(.)`：上采样操作
- `[ ]`：拼接操作
- 含义：`UNet++` 每个 skip 节点会聚合历史同层特征和下层上采样特征，形成 dense nested pathway
- 页码：`p.4-p.5`

公式 2：

```text
L(Y, Y_hat) = -(1/N) * sum_{b=1}^N ( 1/2 * Y_b * log(Y_hat_b) + (2 * Y_b * Y_hat_b) / (Y_b + Y_hat_b) )
```

符号说明：

- `Y_hat_b`：第 `b` 张图的 flatten 预测概率
- `Y_b`：第 `b` 张图的 flatten 真值
- `N`：batch size
- 含义：每个 deep supervision 分支都用 `binary cross-entropy + dice coefficient` 的组合损失
- 页码：`p.5`

### 4.2 推导过程或梯度行为

- 梯度特性：作者明确指出 dense skip connections 会改善 gradient flow，deep supervision 也让不同语义层都能直接接收监督
- 适用条件：适合需要高精细边界、且 encoder-decoder semantic gap 明显的医学分割任务
- 不适用场景：如果任务本身不需要复杂 skip pathway，或者对推理速度极度敏感，完整 `UNet++` 的 nested 结构可能过重
- 页码：`p.5-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| Binary cross-entropy term | `见公式 2` | 像素级前景监督 | 每个 deep supervision 分支 |
| Dice coefficient term | `见公式 2` | 强化区域重叠与小目标稳定性 | 每个 deep supervision 分支 |

### 5.2 总损失公式

```text
L_total = BCE + Dice coefficient loss at each supervised semantic level
```

说明：

- 论文明确说在四个语义层上都加了 `binary cross-entropy + dice coefficient`
- 但未单独给出“分支间加权总和”的更细权重设定，因此不能编造额外 branch weight

### 5.3 权重配置与调度策略

- 各项权重：`正文未说明 BCE 与 Dice 的单独权重系数`
- 是否衰减/动态调整：`未说明`
- 页码：`p.5-p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| cell nuclei | `670` | `[待确认]` | `有 validation 并 early stop` | `96×96`, microscopy |
| colon polyp | `7379` | `[待确认]` | `有 validation 并 early stop` | `224×224`, RGB video |
| liver | `331` | `[待确认]` | `有 validation 并 early stop` | `512×512`, CT |
| lung nodule | `1012` | `[待确认]` | `有 validation 并 early stop` | `64×64×64`, CT |

### 6.2 数据增强

- 增强列表：`正文未展开，具体预处理与增强被放到 supplementary material`
- Patch 提取策略：`输入尺寸按数据集分别为 96×96 / 224×224 / 512×512 / 64×64×64`
- 页码：`p.5-p.6`

### 6.3 优化器与超参数

- 框架：`正文未明确写框架 [待确认]`
- 优化器：`Adam`
- 初始学习率：`3e-4`
- 学习率调度：`未说明`
- Batch size：`正文未明确 [待确认]`
- Epoch / Steps：`正文未明确 [待确认]`
- 权重初始化：`UNet++ is constructed from original U-Net architecture；具体初始化未写`
- 预训练策略：`未提到外部预训练`
- 是否冻结部分层：`否`
- 设备：`NVIDIA TITAN X (Pascal), 12GB` 用于 speed 测试
- 页码：`p.6-p.7`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未提到`
- 颜色空间转换：`colon polyp 为 RGB；其余为 microscopy/CT`
- resize / crop / pad 策略：`按各任务固定输入尺寸训练`
- patch overlap：`未提到`
- 背景过滤策略：`未提到`
- 标签生成方式：`原始分割标注`
- 类别不平衡处理：`通过 BCE + Dice 组合间接缓解`
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：`正文未展开，具体数据预处理在 supplementary material`
- 页码：`p.5-p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：`按数据集固定尺寸推理`
- 概率阈值：`sigmoid 输出后具体阈值未写 [待确认]`
- 后处理步骤：
  1. `accurate mode`：平均所有 segmentation branches 的输出
  2. `fast mode`：只保留某一 segmentation branch 输出
  3. `可在 inference time 对模型进行 pruning`
- TTA / Test-time refinement：`未提到`
- 页码：`p.4-p.7`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | `U-Net` vs `wide U-Net` | wide U-Net 平均略优，但不是所有任务都明显更好 | 仅加宽通道能带来部分收益，但解释不了 UNet++ 的全部提升 |
| 2 | `UNet++ w/o DS` vs `U-Net` | 平均 `+2.8 IoU` | nested dense skip pathways 本身就有效 |
| 3 | `UNet++ w/o DS` vs `wide U-Net` | 平均 `+3.3 IoU` | 收益不只是“参数更大” |
| 4 | `UNet++ w/ DS` vs `UNet++ w/o DS` | 平均 `+0.6 IoU` | deep supervision 进一步提升整体表现 |
| 5 | pruning at different levels | `UNet++ L3` 平均提速 `32.2%`，IoU 仅降 `0.6` | deep supervision 让结构可剪枝、可切换精度-速度 |

### 8.2 各模块贡献量化

- 模块 A 的独立贡献：nested dense skip pathways 带来相对 `U-Net` 的主要性能提升
- 模块 B 的独立贡献：deep supervision 平均再增加 `0.6 IoU`
- 模块 C 的独立贡献：`UNet++ L3` 在轻微精度下降下换来 `32.2%` 推理时间降低
- 页码：`p.6-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| cell nuclei | `IoU 92.52` | - | - | `UNet++ w/ DS` |
| colon polyp | `IoU 32.12` | - | - | `UNet++ w/ DS` |
| liver | `IoU 82.90` | - | - | `UNet++ w/ DS` |
| lung nodule | `IoU 77.21` | - | - | `UNet++ w/ DS` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `U-Net` | cell nuclei | `IoU 90.77` | - | - |
| `Wide U-Net` | cell nuclei | `IoU 90.92` | - | - |
| `UNet++ w/o DS` | cell nuclei | `IoU 92.63` | - | - |
| `UNet++ w/ DS` | cell nuclei | `IoU 92.52` | - | - |
| `U-Net` | colon polyp | `IoU 30.08` | - | - |
| `Wide U-Net` | colon polyp | `IoU 30.14` | - | - |
| `UNet++ w/o DS` | colon polyp | `IoU 33.45` | - | - |
| `UNet++ w/ DS` | colon polyp | `IoU 32.12` | - | - |
| `U-Net` | liver | `IoU 76.62` | - | - |
| `Wide U-Net` | liver | `IoU 76.58` | - | - |
| `UNet++ w/o DS` | liver | `IoU 79.70` | - | - |
| `UNet++ w/ DS` | liver | `IoU 82.90` | - | - |
| `U-Net` | lung nodule | `IoU 71.47` | - | - |
| `Wide U-Net` | lung nodule | `IoU 73.38` | - | - |
| `UNet++ w/o DS` | lung nodule | `IoU 76.44` | - | - |
| `UNet++ w/ DS` | lung nodule | `IoU 77.21` | - | - |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，基于相同 U-Net family 比较`
- 是否统一数据增强：`正文未展开，但比较在同一实验框架内进行`
- 是否统一后处理：`未见额外后处理描述`
- 是否统一输入尺寸：`同一任务内保持一致`
- 结果来源：`原文数字`
- 页码：`p.6-p.8`

### 9.4 评价协议与指标定义

- 数据划分来源：`作者实验设置，正文未逐一展开 train/val/test 细分`
- 结果汇报层级：`task-level held-out evaluation`
- 实例匹配规则：`不适用，主表用 IoU`
- Dice 类型：`训练监控使用 Dice，但主表主要报 IoU`
- Hausdorff 类型：`未使用`
- F1 类型：`未使用`
- 是否含后处理后再报结果：`未提到`
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`部分数据集来自 challenge / provider，但本文主表未按官方 leaderboard 展示`
- 页码：`p.5-p.8`

---

## 10. 计算量与效率

- 参数量（Params）：`U-Net 7.76M`, `wide U-Net 9.13M`, `UNet++ 9.04M`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`正文未直接给出具体毫秒值`
- 训练时间（总 GPU-hours）：`未报告`
- 输入尺寸（计算量对应的）：`按不同数据集不同`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `U-Net` | `7.76M` | `未报告` | `未报告` |
| `wide U-Net` | `9.13M` | `未报告` | `未报告` |
| `UNet++` | `9.04M` | `未报告` | `见 Fig.3 相对速度对比` |

- 页码：`p.5-p.8`

说明：

- `UNet++ L3` 平均提速 `32.2%`，IoU 仅下降 `0.6`
- 论文用一张 `NVIDIA TITAN X (Pascal), 12GB` 测量 `10k` 测试图的处理时间

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`github.com/Nested-UNet`
- 框架/语言：`正文未明确；仓库需另行确认具体实现`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：`正文把部分预处理和数据细节放在 supplementary material；不同数据集的分割任务设定差异较大`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不视为论文固定值 | 中 |
| 验证集划分 | 部分 | 只确认有 validation 和 early stop | 中 |
| 推理阈值 | 否 | 不把阈值当论文固定值 | 中 |
| 后处理细节 | 否 | 不假设有额外后处理 | 中 |
| 训练轮数停止准则 | 部分 | 只记录 early stop，不补造 epoch | 高 |
| 数据预处理 | 部分 | 标记为需看 supplementary material | 高 |

- 不确定但影响较大的点：
  - `batch size`
  - `具体 augmentation`
  - `不同任务的训练/验证拆分细节`

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 更激进的 pruning 虽然能继续提速，但会带来显著精度下降
- deep supervision 的收益不是所有任务都同样明显，在 cell nuclei 和 polyp 上提升有限甚至略有回落
- 页码：`p.6-p.8`

### 14.2 我们观察到的潜在问题

- 论文是跨多个医学任务证明结构有效，但没有专门针对 gland segmentation 设计
- `UNet++` 的 nested skip 结构会明显增加结构复杂度和实现复杂度
- 对于我们项目来说，它更像“强改进基线”而不是第一优先主线，因为主线还要考虑对象级分离和边界专门建模

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`没有系统化 failure case 表，但有 pruning 后速度-精度权衡图`
- 典型失败场景：`更深层剪枝会导致显著精度下降；deep supervision 对部分任务提升不稳定`
- 页码：`p.7-p.8`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 把 `UNet++` 作为 `U-Net` 的强改进基线之一
- nested dense skip pathway 的动机可直接作为“plain skip connection 不够好”的证据来源
- deep supervision 可作为我们后续多层输出监督的结构依据之一

### 15.2 可以作为候选参数来源的

- `Adam, lr = 3e-4`
- `BCE + Dice` 组合损失
- 基础通道规则 `k = 32 × 2^i`

### 15.3 不应照搬的（及原因）

- 多任务上的 IoU 数字
  - 原因：数据模态、输入尺寸和协议与腺体分割不同
- 直接按原文多分支 accurate/fast mode 做主线
  - 原因：我们当前首先需要稳定、可解释、可回填实验 protocol 的基线
- 所有 supplementary material 中未显式写出的细节
  - 原因：不能把未确认的实现细节当论文固定值

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 是否要把 plain skip 改得更强 | 论文明确指出 semantic gap 是问题根源之一 | 强 |
| 是否值得试 deep supervision | 论文证明 deep supervision 有整体收益并支持 pruning | 中 |
| 是否直接替换 U-Net 基线 | 可作为第二梯队强改进基线 | 强 |
| 是否证明收益只是参数更多 | wide U-Net 对比排除了这个简单解释 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`01_实验执行/08_外部对比/02_UNetPP适配方案.md`
- [ ] 需要和哪篇论文交叉验证：`U-Net_2015`、`Attention_U-Net_2018`、`MILD-Net_2018`
- [ ] 待确认的问题：`在腺体任务上，nested skip 的收益是否主要体现在对象分离边界，还是更多体现在整体区域完整性`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 医疗图像分割对细节恢复要求更高 | 作为 plain U-Net 不足的动机 |
| related work | nested U-Net / dense skip 改进路线的经典代表 | 放在 U-Net family 改进段 |
| 方法 | 如果后续引入更强 skip pathway，可引用其 semantic gap 动机 | 只引用结构设计思想 |
| 实验设置 | `UNet++` 作为强改进基线 | 用于基线名单与对比路线 |
| 讨论 | 可讨论 deep supervision 与 pruning 的精度-速度权衡 | 用于解释工程价值边界 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig.1` | `p.3-p.4` | UNet++ 总体结构、skip pathway 和 pruning 示意 | 直接参考 nested skip 设计 |
| `Eq.1` | `p.4-p.5` | skip pathway 公式 | 解释 nested dense 连接 |
| `Table 1` | `p.5` | 四个实验数据集信息 | 数据背景引用 |
| `Table 2` | `p.5` | U-Net / wide U-Net 通道配置 | 公平对比说明 |
| `Fig.2` | `p.6` | U-Net / wide U-Net / UNet++ 定性比较 | 结果可视化 |
| `Table 3` | `p.7` | 主结果 IoU 对比表 | 数字引用 |
| `Fig.3` | `p.7-p.8` | pruning 后复杂度、速度、准确率关系 | 工程权衡说明 |

---

## 17. 提取质量自检

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
