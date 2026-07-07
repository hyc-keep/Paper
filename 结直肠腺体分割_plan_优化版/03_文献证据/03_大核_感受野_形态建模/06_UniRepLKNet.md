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

- `universal large-kernel convnet`
- `dilated structural re-parameterization`
- `cross-modality backbone`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是这一组里“现代大核 ConvNet 通用化”的最后一篇
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`UniRepLKNet: A Universal Perception Large-Kernel ConvNet for Audio, Video, Point Cloud, Time-Series and Image Recognition`
- 作者/团队：`Xiaohan Ding et al.`
- 发表年份/会议/期刊：`2024, CVPR`
- DOI / arXiv ID：`[待确认 DOI]` / `[待确认 arXiv]`
- BibTeX key：`ding2024unireplknet`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/UniRepLKNet_A_Universal_Perception_Large-Kernel_ConvNet_CVPR_2024.pdf`
- 当前定位：`现代大核 ConvNet 的通用化代表；在 RepLKNet 基础上总结大核设计准则，并把大核 backbone 无缝泛化到图像、时间序列、音频、视频、点云`
- 与已提取论文的关系：
  - 与 `Scaling-Up-Kernels_2022` 是直接延续关系：从 RepLKNet 的单一图像大核 backbone 发展到通用感知骨干
  - 与 `VAN_2023` 互补：VAN 强调 large kernel attention，UniRepLKNet 强调大核卷积主干的通用性与速度
  - 对你当前项目的意义在于，它证明“大核不仅是某个单任务 trick，而是一种强通用结构偏置”

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者发现 large kernels 是释放 ConvNet 潜力的关键
  - 用途：`方法动机`
  - 页码：`p.1`
- 句子/事实 2：UniRepLKNet 在图像识别、分割、检测以及多模态任务上都取得领先结果
  - 用途：`总结果概括`
  - 页码：`Abstract, p.1`
- 句子/事实 3：论文指出大核设计不能只看 ImageNet，必须结合下游 dense prediction 任务评估
  - 用途：`为什么要看分割结果`
  - 页码：`Sec.3.2, p.4-p.5`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者总结了四条大核结构设计准则，涵盖 block 设计、re-parameterization、kernel size 分配和 scaling rule
  - 用途：`现代大核设计总纲`
  - 页码：`Sec.3, p.4`
- 句子/事实 2：UniRepLKNet 可以不改结构本体而泛化到音频、时间序列、视频、点云等模态
  - 用途：`通用 backbone 论据`
  - 页码：`Sec.3.4, p.5-p.6; Sec.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| default large kernel | `13x13` | stage 2-4 默认大核 | `p.4-p.5` |
| default stage config | `C=96, N=(3,3,9,3)` | vanilla backbone | `p.4-p.5` |
| default parallel branches | `k=(5,7,3,3,3), r=(1,2,3,4,5)` | `K=13` re-param | `p.4` |
| ImageNet best | `88.0%` | UniRepLKNet-XL | `Table 6` |
| COCO best | `56.4 / 49.0` | APbox / APmask | `Table 7` |
| ADE20K best | `55.2 / 55.6` | SS / MS mIoU | `Table 8` |
| Audio | `98.5%` | Speech Commands V2 | `Table 10` |
| Point cloud | `90.3 / 93.2` | mAcc / OA | `Table 12` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- RepLKNet 等大核 ConvNet 已证明在图像上很强，但仍存在几个未解决问题：
  - 怎样系统化总结大核设计准则
  - 怎样让大核 ConvNet 兼顾速度和精度
  - 怎样证明大核结构不是只适用于图像分类，而是通用于多模态感知
- 需要一个既高效、又可扩展、又具有跨模态泛化能力的大核 backbone

对应原文依据（页码）：

- `p.1-p.2`
- `Sec.3, p.4`

### 2.2 核心思路（一段话概括解法方向）

- 论文基于对大核 ConvNet 的进一步分析，总结出四条架构准则：`高效 block design`、`用 dilated small kernels re-parameterize large kernel`、`依据下游任务决定 kernel size 并重点放在中高层`、`扩深时新增 block 应优先用小核`。据此，作者提出 `UniRepLKNet`，核心单元是 `Dilated Reparam Block`，训练时用多个带不同 dilation 的小核并联增强大核，推理时再等价合并回单个非膨胀大核卷积，从而兼顾高 ERF、表达力与实际吞吐。

关键页码：

- `Sec.3.1-Sec.3.2, p.4-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`hierarchical large-kernel ConvNet`
- 基本结构：
  - 4 个 stage
  - 4 个 stage 的通道数为 `C, 2C, 4C, 8C`
  - stage 之间通过 stride-2 `3x3` conv 下采样
- 基本 block：
  - `LarK Block`：使用 large kernel 的 block
  - `SmaK Block`：使用 small kernel 的 block
- 默认配置：
  - `C=96`
  - `N=(3,3,9,3)`
  - stage 2-4 默认用 `13x13` large kernel

### 3.2 关键模块详细描述

**模块 1：`Dilated Reparam Block`**

- 位置：`stage 中的 DW conv 部分`
- 操作流程：
  1. 主分支使用一个非膨胀 large kernel conv
  2. 并联多个带不同 dilation 的 small-kernel conv
  3. 各分支输出经 BN 后相加
  4. 推理时把这些分支等价合并回单个非膨胀大核卷积
- 页码：`Sec.3.1, p.4`

**模块 2：`LarK / SmaK Blocks`**

- 位置：`主干 block 级别`
- 作用：
  - `LarK Block` 用大核提供大 ERF 与空间聚合
  - `SmaK Block` 在扩深时提供更高性价比和更好速度
- 页码：`Sec.3.2, p.4-p.5`

**模块 3：`Cross-Modality Adaptation`**

- 位置：`输入嵌入层`
- 操作方式：
  - 对不同模态只调整首层输入通道或嵌入方式
  - backbone 主体基本保持不变
- 页码：`Sec.3.4, p.5-p.6`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| large kernel `K` | `13` | 中高层大核建模 | `p.4-p.5` |
| re-param branches | `k=(5,7,3,3,3)` | small kernels | `p.4` |
| dilation rates | `r=(1,2,3,4,5)` | sparse pattern capture | `p.4` |
| vanilla width | `C=96` | 基础宽度 | `p.4-p.5` |
| depth config | `N=(3,3,9,3)` | 四阶段 block 数 | `p.4-p.5` |
| model family | `A/F/P/N/T/S/B/L/XL` | 多尺度实例 | `Table 5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：dilated kernel 到非膨胀稀疏大核的等价变换

```text
W' = conv_transpose2d(W, I, stride = r)
```

符号说明：

- `W`：小核膨胀卷积权重
- `I`：单位核
- `r`：dilation rate
- `W'`：等价的非膨胀稀疏大核
- 页码：`Eq.(1), p.4`

公式 2：等价 kernel size

```text
K_equiv = (k - 1) * r + 1
```

符号说明：

- `k`：膨胀小核尺寸
- `r`：dilation rate
- 用于说明为什么 dilated small kernels 可以增强大核
- 页码：`Sec.3.1, p.4`

### 4.2 推导过程或梯度行为

- 核心推导：
  - 膨胀卷积忽略输入中的部分位置，等价于在卷积核中插入零
  - 因此多个不同 dilation 的小核分支，可以在训练时补充大核对 sparse patterns 的建模
  - 推理时再统一合并成单大核，避免额外分支开销
- 设计含义：
  - 小核分支帮助捕获小尺度与稀疏模式
  - 大核主分支保证大 ERF
- 页码：`p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `classification loss` | `[标准分类损失]` | ImageNet | classifier |
| `detection/segmentation loss` | `[对应框架默认损失]` | COCO / ADE20K | task heads |
| `modality-specific loss` | `[各任务默认目标]` | time-series / audio / point cloud / video | task heads |

### 5.2 总损失公式

```text
L_total = L_task
```

说明：

- 本文主要创新在 backbone 结构和 re-parameterization
- 下游各任务仍用标准训练目标

### 5.3 权重配置与调度策略

- ImageNet-1K：
  - `300-epoch recipe`
- ImageNet-22K：
  - `90-epoch pretrain + 30-epoch 1K finetune`
- COCO：
  - `Cascade Mask R-CNN`
  - `3x (36 epochs)`
- ADE20K：
  - `UPerNet`
  - `160k iterations`
- 页码：`p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ImageNet-1K` | `标准 train` | `val` | `validation` | 分类 |
| `ImageNet-22K` | `大规模预训练集` | `finetune on 1K` | `validation` | 大模型 |
| `COCO` | `train` | `val` | `validation` | Cascade Mask R-CNN |
| `ADE20K` | `train` | `val` | `validation` | UPerNet |
| `Speech Commands V2` | `105,829 clips` | `标准评估` | `validation/test` | 音频 |
| `ModelNet-40` | `9843 / 2468` | `val` | `validation` | 点云 |

### 6.2 数据增强

- 图像任务：
  - 采用 ConvNeXt / MMSeg / MMDetection 默认成熟配置
- 其他模态：
  - 采用相应任务标准预处理，但 backbone 主体不改
- 页码：`p.5-p.8`

### 6.3 优化器与超参数

- ImageNet throughput 评估：
  - `A100 GPU`
  - `batch size = 128`
- ADE20K：
  - `UPerNet`
  - `MMSegmentation`
  - `160k iterations`
- COCO：
  - `Cascade Mask R-CNN`
  - `MMDetection`
  - `36 epochs`
- 页码：`p.4-p.6`

### 6.4 预处理与数据细节

- 为不同模态调整首层输入通道或嵌入方式
- backbone 主体保持一致，强调通用性
- 模态泛化结论：
  - image / time-series / audio / video / point cloud 均可用
- 页码：`Sec.3.4, p.5-p.6; Sec.5`

---

## 7. 推理与后处理

- 推理时将 Dilated Reparam Block 的所有分支合并为单个非膨胀大核卷积
- 因此不会保留训练时的并联分支结构
- 目标是保证实际部署速度，而不只是理论 FLOPs 漂亮
- 页码：`p.4; p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 不同 extra structures 增深 | `SE/Bottleneck` 有增益但不如完整设计平衡 | 需要高效深度结构 |
| `A2` | 不同 structural re-param 形式 | parallel dilated small kernels 最优 | 大核需要稀疏模式增强 |
| `A3` | 不同 stage 的 kernel size 分配 | 中高层用大核最优 | 大核不应平均铺满全网 |
| `A4` | Stage 3 中 LarK / SmaK 比例 | 增深时小核块更有利于速度-精度平衡 | scaling 不能只堆大核 |
| `A5` | 跨模态 smaller kernels 对比 | `K=13` 普遍优于 `K=11/7/3` | 大核在多模态依然关键 |

### 8.2 各模块贡献量化

- Table 1：
  - `None`: `81.2 / 45.1`
  - `Bottleneck`: `81.5 / 46.3`
  - `Two 1x1`: `81.3 / 46.2`
  - `Two DW 3x3`: `81.3 / 45.4`
  - `SE Block`: `81.6 / 46.5`
- Table 3 / 4 结论：
  - 在中高层保留 large kernels 对 ADE20K 更关键
  - 扩深时新增 SmaK blocks 速度更优，mIoU 也不吃亏
- Table 13：
  - `ResNet-101 (K=3)`: time-series `7.846`, point cloud `92.6`, audio `73.6`, video `41.3`
  - `ConvNeXt-S (K=7)`: `7.641 / 92.7 / 94.3 / 48.5`
  - `UniRepLKNet-S (K=11)`: `7.751 / 92.9 / 94.7 / 51.7`
  - `UniRepLKNet-S (K=13)`: `7.602 / 93.2 / 98.5 / 54.8`
- 页码：`p.4-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ImageNet-1K` | `UniRepLKNet-T 83.2` | `S 83.9` | `XL 88.0` | 大模型带 22K pretrain |
| `COCO` | `T 51.8 / 44.9` | `S 53.0 / 45.9` | `XL 56.4 / 49.0` | APbox / APmask |
| `ADE20K` | `T 48.6 / 49.1` | `S 50.5 / 51.0` | `XL 55.2 / 55.6` | SS / MS mIoU |
| `Speech Commands V2` | `98.5%` | fewer params than Audio-MAE | no pretraining | 通用性结果 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `UniRepLKNet-T` | `COCO` | `51.8 / 44.9` | 优于 `Swin-T 50.4 / 43.7` | 优于 `ConvNeXt-T 50.4 / 43.7` |
| `UniRepLKNet-S` | `ADE20K` | `50.5 / 51.0` | 优于 `Swin-S 47.6 / 49.5` | 优于 `ConvNeXt-S 48.7 / 49.6` |
| `UniRepLKNet-B‡` | `ADE20K` | `53.5 / 53.9` | 优于 `Swin-B‡ 50.0 / 51.7` | 优于 `RepLKNet-31B‡ 51.5 / 52.3` |
| `UniRepLKNet-XL‡` | `COCO` | `56.4 / 49.0` | 优于 `ConvNeXt-XL‡ 55.2 / 47.7` | 略优于 `InternImage-XL‡ 56.2 / 48.8` |

### 9.3 公平对比条件确认

- 是否统一任务头：`是，COCO 统一用 Cascade Mask R-CNN，ADE20K 统一用 UPerNet`
- 是否统一训练策略：`是，采用标准 MMDetection / MMSegmentation 配置`
- 是否统一硬件吞吐评估：`是，在 A100 上报告 throughput`
- 页码：`p.5-p.6`

### 9.4 评价协议与指标定义

- 分类：`Top-1 accuracy`
- 检测/实例分割：`APbox / APmask`
- 语义分割：`single-scale / multi-scale mIoU`
- 其他模态：
  - time-series：`MSE / MAE`
  - audio：`accuracy`
  - point cloud：`mAcc / OA`
- 页码：`Table 6-13`

---

## 10. 计算量与效率

- 论文强调实际吞吐而不只看 FLOPs
- 典型结果：
  - `UniRepLKNet-S`: `83.9%` at `1265 img/s`
  - `RepLKNet-31B`: `83.5%` at `859 img/s`
  - `UniRepLKNet-S‡` 准确率接近 `RepLKNet-31L‡`，但速度约为其 `3x`
- 结论：
  - Dilated small-kernel re-param 能增强大核表达力
  - 但推理时仍可保持单大核结构和较好吞吐
- 页码：`p.6, Table 6`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/AILab-CVC/UniRepLKNet`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`仓库待确认`
- 复现难度评估：`中`
- 复现障碍：
  - 多分支 re-param 训练与单分支推理合并需要正确实现
  - 跨模态实验虽结构统一，但各模态前处理仍需单独适配

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 具体优化器与学习率细节 | `主文有限` | `以后查附录/仓库` | `中` |
| 各模态完整训练脚本 | `需仓库确认` | `优先看官方实现` | `中` |
| 权重下载口径 | `待仓库确认` | `后续补查` | `低` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文虽强调通用性，但视频等任务上并未达到该模态最强专用方法
- 这说明 UniRepLKNet 更像“强通用主干”，不一定在每个模态上都是绝对专精解

### 14.2 我们观察到的潜在问题

- 对腺体分割而言，UniRepLKNet 很强于 backbone 层面，但并不直接提供 boundary/topology 机制
- 其价值更适合用来支撑“大核主干可行、且值得做”，而不是直接作为边界方法证据
- 若直接整套引入，工程和算力成本会显著高于只抽其中的大核 block 设计

### 14.3 失败案例 / 定性分析

- 从跨模态结果可见：
  - 在音频、时间序列、点云上很强
  - 在视频上虽优于其他 generalist，但仍落后于专门视频模型
- 这提示我们：
  - 通用 backbone 的优势在于稳定和迁移性
  - 真正落到腺体分割，还需结合任务特定边界/实例设计

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- “large kernels are the key to unlocking ConvNet strength” 这类总动机表述
- 四条大核设计准则
- Dilated small-kernel re-parameterization 增强大核的工程方案

### 15.2 可以作为候选参数来源的

- 中高层默认 `13x13`
- 默认 re-param 支路：
  - `k=(5,7,3,3,3)`
  - `r=(1,2,3,4,5)`
- 扩深时新增 block 优先用小核，而不是继续堆大核

### 15.3 不应照搬的（及原因）

- 直接把完整 `UniRepLKNet-B/L/XL` 整套替换腺体分割 backbone：
  - 原因：工程和显存成本高
- 把多模态通用性直接等同于病理任务最优：
  - 原因：通用强不等于腺体分割最优，仍需边界与实例特定设计

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 大核 backbone 路线 | 直接的现代总证据 | `强` |
| 大核 block 设计 | 给出具体 re-param 方案 | `强` |
| 感受野增强 | 证明对分割任务尤其有效 | `强` |
| 边界监督 / 拓扑约束 | 不直接提供 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`大核主干改造依据`、`LKMA 结构细化`
- [ ] 需要和哪篇论文交叉验证：`Scaling-Up-Kernels_2022`、`VAN_2023`、`Wavelet-Convolutions_2024`
- [ ] 待确认的问题：`你更想借鉴其 backbone 全局设计，还是只抽 Dilated Reparam Block`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 大核是释放 ConvNet 潜力的关键 | 作为大核路线总括 |
| related work | RepLKNet -> UniRepLKNet 的发展脉络 | 放在大核 ConvNet 小节 |
| 方法 | Dilated Reparam Block | 作为结构设计来源 |
| 实验分析 | 大核对分割任务比 ImageNet 更敏感 | 解释为何要看 ADE20K |
| 讨论 | 大核 backbone 是通用强结构，但不是边界方法替代 | 连接到边界支撑文献 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1-p.2` | UniRepLKNet 总体结构 | 回填框架 |
| `Figure 2` | `p.4` | Dilated Reparam Block | 回填核心机制 |
| `Eq.(1)` | `p.4` | dilated kernel 到非膨胀大核的等价变换 | 公式引用 |
| `Table 1-4` | `p.4-p.5` | 大核设计准则相关消融 | 写设计原则 |
| `Table 5` | `p.5` | A/F/P/N/T/S/B/L/XL 配置 | 参数来源 |
| `Table 6` | `p.6` | ImageNet 结果与吞吐 | 分类与速度引用 |
| `Table 7` | `p.6` | COCO 结果 | 检测引用 |
| `Table 8` | `p.6-p.7` | ADE20K 结果 | 分割引用 |
| `Table 9-13` | `p.7-p.8` | 多模态结果 | 通用性引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 大核四条设计准则已记录
- [x] Dilated Reparam Block 公式和结构已覆盖
- [x] ImageNet / COCO / ADE20K 主结果已覆盖
- [x] 多模态泛化结果已单独记录
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`
