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
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `large-kernel CNN`
- `RepLKNet`
- `effective receptive field`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是现代大核 CNN 路线的代表论文，负责把 `GCN` 的早期大核动机延伸到 `31x31` 级别的现代纯 CNN 架构
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Scaling Up Your Kernels to 31x31: Revisiting Large Kernel Design in CNNs`
- 作者/团队：`Xiaohan Ding et al.`
- 发表年份/会议/期刊：`2022, CVPR`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:2203.06717`
- BibTeX key：`ding2022replknet`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/Scaling_Up_Your_Kernels_to_31x31_Revisiting_Large_Kernel_Design_in_CNNs_2022.pdf`
- 当前定位：`现代大核卷积代表作；提出 RepLKNet，并系统总结大核 CNN 的五条设计准则，直接支撑你后续大核模块的理论和工程路线`
- 与已提取论文的关系：
  - 与 `Large-Kernel-Matters_2017` 构成“早期大核动机 -> 现代大核架构”的连续证据链
  - 与 `Wavelet_Convolutions_2024` 互补：这篇强调直接大核卷积与 re-parameterization，后者更强调频域/小波形式的大感受野
  - 对你自己的 `LKMA` 模块最有价值的是：大核不仅扩大 ERF，还带来更高的 shape bias，并且对下游分割增益更大

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者重新审视现代 CNN 中的大核设计，提出 `RepLKNet`，卷积核最大可达 `31x31`
  - 用途：`方法动机`
  - 页码：`Abstract, p.1`
- 句子/事实 2：大核 CNN 能显著缩小 CNN 和 ViT 的差距，并在多个下游任务上具有竞争力
  - 用途：`为何现代阶段仍要做大核`
  - 页码：`Abstract, p.1`
- 句子/事实 3：`RepLKNet-XL` 达到 `87.8%` ImageNet top-1 和 `56.0%` ADE20K mIoU
  - 用途：`结果概括`
  - 页码：`Abstract, p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者总结了五条 large-kernel design guidelines，其中包括 `large depth-wise conv`、`identity shortcut` 和 `small-kernel re-parameterization`
  - 用途：`工程设计出处`
  - 页码：`p.1, p.3-p.4`
- 句子/事实 2：大核显著扩大 effective receptive field，并提高 shape bias，而这两点被认为是其下游迁移优势的重要原因
  - 用途：`大核对结构建模的理论支撑`
  - 页码：`p.2, p.7-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 最大 kernel size | `31x31` | RepLKNet 核心卖点 | `p.1` |
| kernel schedule | `[31, 29, 27, 13]` | RepLKNet-31 | `p.5-p.6` |
| baseline kernel schedule | `[3, 3, 3, 3]` | 小核对照 | `p.5` |
| ImageNet training | `120 epochs, AdamW` | 主实验设置 | `p.5-p.6` |
| ADE20K setting | `UperNet, 80K iterations` | 分割设置 | `p.5-p.6` |
| Cityscapes setting | `UperNet, 80K iterations` | 分割设置 | `p.6` |
| ADE20K best | `56.0 mIoU` | RepLKNet-XL | `p.6` |
| ImageNet best | `87.8 top-1` | RepLKNet-XL | `p.1, p.6` |
| RepLKNet-31B vs Swin-B | `84.8 vs 84.5`, 且更快 | ImageNet-1K | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 在 ViT 兴起后，CNN 被认为在大模型和高复杂度预算下落后于 Transformer
- 传统 CNN 多采用小核堆叠，但这未必是最优设计范式
- 需要重新回答两个问题：
  - 大核卷积在现代 CNN 中是否仍然有效
  - 如何把大核做到既高性能又可训练、可部署

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文先通过一系列实验总结五条大核设计准则，再据此构建纯 CNN 架构 `RepLKNet`。核心是使用 `large depth-wise convolutions`、保留 `identity shortcuts`、用小核分支做 `re-parameterization` 来缓解优化困难，并证明大核会显著扩大 effective receptive field、增强 shape bias，且这种收益在 `semantic segmentation` 等下游任务上比在 ImageNet 分类上更明显。

关键页码：

- `p.1-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`pure CNN large-kernel architecture`
- 总体组成：
  - `Stem`
  - `Stage 1-4`
  - `Transition Blocks`
  - `RepLK Block + ConvFFN` 交替堆叠
- 关键设计：
  - RepLK Block 内部使用 `DW large kernel conv`
  - 其前后用 `1x1 conv`
  - 每个大核层训练时带一个 `5x5` re-parameterization 分支
- 页码：`Sec.4.1, p.5`

### 3.2 关键模块详细描述

**模块 1：`RepLK Block`**

- 位置：`各 stage 的核心空间建模单元`
- 操作流程：
  1. 输入先经过 `1x1 conv`
  2. 再经过 `K x K depth-wise large conv`
  3. 训练时并联一个 `5x5` 小核分支用于 re-parameterization
  4. 输出与 shortcut 相加
- 核心意义：
  - 用超大核直接扩大感受野
  - 保留 shortcut 以稳定优化
- 页码：`p.5`

**模块 2：`ConvFFN Block`**

- 位置：`每个 RepLK Block 后`
- 操作流程：
  1. shortcut
  2. BN
  3. 两层 `1x1 conv`
  4. `GELU`
- 核心意义：
  - 增加深度、非线性与通道间信息交互
  - 类似 Transformer 中 attention 后接 FFN
- 页码：`p.5`

**模块 3：`Transition Block`**

- 位置：`相邻 stages 之间`
- 操作流程：
  1. `1x1 conv` 提升通道数
  2. `DW 3x3` 做下采样
- 页码：`p.5`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| kernel schedule | `[31,29,27,13]` | RepLKNet-31 主配置 | `p.5-p.6` |
| blocks per stage | `[2,2,18,2]` | RepLKNet-13/25/31 评估配置 | `p.5` |
| channels per stage | `[128,256,512,1024]` | Base 配置 | `p.5` |
| internal ConvFFN ratio | `4x` | 扩展通道容量 | `p.5` |
| activation | `ReLU / GELU` | conv-BN 序列与 ConvFFN | `p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
RepLKNet = Stem + [RepLK Block, ConvFFN] x Stages + Transition Blocks
```

符号说明：

- `RepLK Block`：大核深度卷积空间建模
- `ConvFFN`：两层 `1x1` 卷积的通道混合块
- 核心思想：以大核替代 attention 或大量小核堆叠
- 页码：`Sec.4.1, p.5`

公式 2：

```text
training-time large kernel = KxK DW conv + parallel 5x5 branch
inference-time large kernel = re-parameterized single KxK DW conv
```

符号说明：

- 训练时：并联小核分支缓解优化困难
- 推理时：把小核与 BN 参数合并进大核，不增加部署分支
- 页码：`Guideline 3, p.3-p.4; Fig.2`

### 4.2 推导过程或梯度行为

- Guideline 1：
  - `large depth-wise conv` 在实践中可高效，不必机械地把 FLOPs 增长等同于 latency 灾难
- Guideline 2：
  - very large kernels 必须配 identity shortcut，否则精度会显著崩溃
- Guideline 3：
  - re-parameterization 用小核辅助训练，再合并回大核，能明显改善优化
- Guideline 4：
  - 大核对下游任务提升大于对 ImageNet 分类提升，说明其价值更多体现在迁移与 dense prediction
- Guideline 5：
  - 即便 feature map 很小，大核仍然有用，不应仅凭“核接近特征图尺寸”就停止放大
- 页码：`p.3-p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `classification loss` | `[标准分类损失]` | ImageNet 预训练 | classifier |
| `segmentation loss` | `[UperNet 默认分割损失]` | ADE20K / Cityscapes 分割 | segmentation head |

### 5.2 总损失公式

```text
L_total = L_task
```

说明：

- 本文贡献不在新 loss，而在大核 CNN 的结构与设计准则
- 训练目标沿用任务默认配置

### 5.3 权重配置与调度策略

- ImageNet：
  - `AdamW`
  - `120 epochs`
  - 使用 `RandAugment / mixup / CutMix / Random Erasing / Stochastic Depth`
- ADE20K：
  - `UperNet`
  - `80K iterations`
- Cityscapes：
  - `UperNet`
  - `80K iterations`
- 页码：`p.5-p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ImageNet-1K` | `标准训练集` | `标准验证` | `val` | 主预训练 |
| `ADE20K` | `20K train` | `2K val` | `validation` | 150 classes |
| `Cityscapes` | `官方 train` | `官方 test` | `val` | 语义分割基准 |
| `COCO` | `检测 benchmark` | `val/test` | `标准协议` | 用于下游证明 |

### 6.2 数据增强

- ImageNet：
  - `RandAugment`
  - `mixup`
  - `CutMix`
  - `Random Erasing`
  - `Stochastic Depth`
- segmentation：
  - 沿用 `MMSegmentation / UperNet` 默认训练设置
- 页码：`p.5-p.6`

### 6.3 优化器与超参数

- ImageNet 框架风格：`AdamW`
- ImageNet 训练时长：`120 epochs`，后续公平对比扩展到 `300 + 30` epochs / finetune
- segmentation head：`UperNet`
- Cityscapes schedule：`80K iterations`
- ADE20K schedule：`80K iterations` 用于 kernel-size study；后续 state-of-the-art 对比为 `160K`
- 框架：
  - `MMSegmentation`
  - 推理速度在 `2080Ti` 上报告
- 页码：`p.5-p.6`

### 6.4 预处理与数据细节

- 预训练输入：
  - `224 x 224`
  - 进一步对比时使用 `384 x 384`
- FLOPs 计算：
  - `ADE20K` 对齐 `2048 x 512`
  - `Cityscapes` 对齐 `1024 x 2048`
- 预训练扩展：
  - `ImageNet-22K`
  - `MegData73M` 半监督额外数据
- 页码：`p.5-p.6`

---

## 7. 推理与后处理

- 推理阶段将训练时的小核辅助分支 re-parameterize 进大核主分支
- 因此部署时仍然是单一路径的大核 DW conv，不引入额外结构分叉
- segmentation 评估使用：
  - `single-scale`
  - `multi-scale`
- 页码：`p.3-p.4, p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | `[3,3,3,3] -> [31,29,27,13]` | ImageNet `82.11 -> 83.07`, ADE20K `46.05 -> 49.17` | 大核对分割提升更明显 |
| `A2` | 去 shortcut | MobileNetV2 `68.67 -> 53.98` | 超大核必须保留 identity shortcut |
| `A3` | 不用 re-param | `13x13` 在 ImageNet/Cityscapes 更差 | 小核辅助训练有效 |
| `A4` | 小 feature map 不再放大核 | `7x7/13x13` 仍继续提升 | 大核在小特征图上也有价值 |
| `A5` | ERF 与 shape bias 分析 | RepLKNet ERF 更广、shape bias 更强 | 解释为何下游迁移更强 |

### 8.2 各模块贡献量化

- Table 5：
  - `[3,3,3,3]`: `82.11 / 46.05`
  - `[7,7,7,7]`: `82.73 / 48.05`
  - `[13,13,13,13]`: `83.02 / 48.35`
  - `[25,25,25,13]`: `83.00 / 48.68`
  - `[31,29,27,13]`: `83.07 / 49.17`
- Guideline 4 的关键结论：
  - 从 `3x3 -> 9x9`，ImageNet 只提升 `1.33%`
  - 但 Cityscapes mIoU 提升 `3.99%`
- ERF：
  - `ResNet-101` 在 `t=99%` 时面积比 `22.4%`
  - `RepLKNet-31` 达 `98.6%`
- 页码：`p.3-p.4, p.7-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ImageNet` | `RepLKNet-31B 84.8` | `Swin-B 84.5` | `RepLKNet 更快` | `384x384, 1K pretrain` |
| `Cityscapes` | `83.1 ss / 83.5 ms` | `Swin-B 80.4 / 81.5` | `RepLKNet-31B 更强` | `UperNet` |
| `ADE20K` | `49.9 ss / 50.6 ms` | `Swin-B 48.1 / 49.7` | `RepLKNet-31B 更强` | `1K pretrain` |
| `ADE20K` | `55.2 ss / 56.0 ms` | `RepLKNet-XL` | `competitive SOTA` | extra data |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `RepLKNet-31B` | `ImageNet` | `84.8` | `79M params` | faster than Swin-B |
| `Swin-B` | `ImageNet` | `84.5` | `88M params` | slower |
| `RepLKNet-31B + UperNet` | `Cityscapes` | `83.1 ss` | `83.5 ms` | 优于 Swin-B / Swin-L |
| `RepLKNet-31B + UperNet` | `ADE20K` | `49.9 ss` | `50.6 ms` | 优于 Swin-B |
| `RepLKNet-XL + UperNet` | `ADE20K` | `55.2 ss` | `56.0 ms` | 大模型结果 |

### 9.3 公平对比条件确认

- 是否统一 head：`是，分割统一使用 UperNet`
- 是否统一训练框架：`是，采用 MMSegmentation 设定`
- 是否统一输入/FLOPs 统计：`是，按 Swin 相同口径统计`
- 是否强调 backbone-only 对比：`是，作者明确不加额外 tricks/custom algorithms`
- 页码：`p.6`

### 9.4 评价协议与指标定义

- 分类：`top-1 accuracy`
- 分割：
  - `single-scale mIoU`
  - `multi-scale mIoU`
- 额外分析：
  - `ERF high-contribution area ratio`
  - `shape bias`
- 页码：`p.6-p.8`

---

## 10. 计算量与效率

- Guideline 1 明确指出：
  - 大核 FLOPs 上升不必然等于 latency 等比例变差
  - `DW large conv` 让大核在实践中可接受
- 从 `[3,3,3,3]` 到 `[31,29,27,13]`：
  - FLOPs 只增约 `18.6%`
  - 参数只增约 `10.4%`
- 推理效率：
  - `RepLKNet-31B 384x384` 比 `Swin-B` 更快
  - 虽然 `RepLKNet-XL` FLOPs 更高，仍可快于 `Swin-L`
- 对我们项目的意义：
  - 若要做大核模块，不应只看理论 FLOPs，还要看实际 latency 与是否可 re-parameterize
- 页码：`p.3, p.6`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`github.com/DingXiaoH/RepLKNet-pytorch`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`论文中给出 code & models available`
- 复现难度评估：`中`
- 复现障碍：
  - 大核 DW conv 的高效实现依赖优化过的 CUDA kernel
  - 若只用默认框架实现，速度可能明显偏慢
  - extra data 版本（MegData73M）难完整复现

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 具体学习率细节 | `正文未完整展开` | `后续看附录/仓库` | `中` |
| 各模型完整训练脚本 | `需查代码` | `仓库复现` | `低` |
| MegData73M 细节 | `非公开标准数据` | `不作为主复现目标` | `高` |
| kernel CUDA 优化细节 | `正文略写` | `优先用官方实现` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 大核卷积虽有效，但基础框架若未优化，对默认工具链并不友好
- 随着模型和数据规模继续扩大，RepLKNet 在部分 ImageNet 指标上仍可能落后于大规模 Swin

### 14.2 我们观察到的潜在问题

- 这篇主要解决 backbone 感受野与形状偏置，不直接处理腺体实例分离或边界黏连
- 对病理图像来说，大核可能更利于整体形态建模，但仍需要与 boundary/topology 路线结合
- 若你的算力有限，完整 RepLKNet 式替换 backbone 成本较高，更现实的是抽取其 guideline 和模块思想

### 14.3 失败案例 / 定性分析

- 论文最关键的“失败风险”不是定性图，而是训练与部署层面：
  - 无 shortcut 时精度显著崩塌
  - 无 re-param 时更大的核未必更好
  - 默认深度学习框架对大 DW conv 支持较差
- 这说明：
  - 大核设计必须配套优化策略
  - 不能只把 kernel 变大而不改训练结构

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `large kernel -> larger ERF -> better downstream dense prediction` 的完整证据链
- `identity shortcut + re-parameterization + DW large conv` 这套大核工程规范
- `shape bias` 这一非常适合病理形态建模的论证语言

### 15.2 可以作为候选参数来源的

- 大核尺寸可优先尝试 `13 / 25 / 31` 这一梯度
- 如果你做轻量版 LKMA，可用“训练时小核并联，推理时重参数化”的策略
- 大核不必只放高分辨率阶段，小 feature map 阶段也可继续放大

### 15.3 不应照搬的（及原因）

- 直接整套照搬 `RepLKNet-31B/31L/XL` 到腺体分割：
  - 原因：工程成本高，且你的任务还需要边界与实例层面的补充
- 只依据 ImageNet 指标判断大核价值：
  - 原因：本文明确说明大核对下游分割的增益更大

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 大核模块 `LKMA` | 给出最直接的现代大核设计准则 | `强` |
| 感受野增强 | ERF 分析与表格证据完整 | `强` |
| 形态建模 / shape bias | 说明大核更偏 shape 而非 texture | `强` |
| 边界分支设计 | 本文不直接提供 | `弱-中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`大核模块设计动机`、`backbone 改造依据`
- [ ] 需要和哪篇论文交叉验证：`Large-Kernel-Matters_2017`、`Wavelet_Convolutions_2024`
- [ ] 待确认的问题：`你的模块是做纯 backbone 替换，还是做可插拔大核块`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 现代 CNN 中为何重新重视大核 | 作为大核路线总动机 |
| related work | RepLKNet 代表的大核 CNN 路线 | 放在 receptive field / backbone 设计部分 |
| 方法 | re-parameterized large DW conv | 作为 LKMA 工程来源 |
| 讨论 | 大核更偏 shape bias | 引到病理形态结构建模 |
| 实验分析 | 大核对下游分割提升更大 | 用于解释为什么要在腺体分割中尝试 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1-p.2` | ERF 可视化 | 写大核感受野动机 |
| `Table 2-4` | `p.3-p.4` | 五条 guideline 的关键消融 | 回填设计原则 |
| `Figure 2` | `p.4` | re-parameterization 示意 | 回填训练/部署逻辑 |
| `Figure 3` | `p.4` | 大核与小 feature map 关系 | 解释 guideline 5 |
| `Figure 4` | `p.5` | RepLKNet 架构图 | 方法结构 |
| `Table 5-8` | `p.5-p.6` | ImageNet / Cityscapes / ADE20K 主结果 | 数字引用 |
| `Table 10` | `p.7-p.8` | ERF 定量分析 | 强化感受野证据 |
| `Figure 5` | `p.8` | shape bias 分析 | 形态偏置证据 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 五条 guideline 已逐条记录
- [x] RepLKNet 架构与 re-param 逻辑已写清
- [x] ImageNet / Cityscapes / ADE20K 主结果已覆盖
- [x] ERF 与 shape bias 证据已单独保留
- [x] 与我们项目的关联已具体到大核模块级别
- [x] 不确定内容已标注 `[待确认]`
