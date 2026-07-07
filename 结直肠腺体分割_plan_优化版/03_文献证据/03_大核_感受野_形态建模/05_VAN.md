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

- `large kernel attention`
- `visual attention`
- `hierarchical backbone`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是“大核注意力 / LKA”路线的代表论文，和前面的大核卷积、自适应采样、小波域感受野共同构成这一组的完整谱系
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Visual Attention Network`
- 作者/团队：`Meng-Hao Guo, Cheng-Ze Lu, Zheng-Ning Liu, Ming-Ming Cheng, Shi-Min Hu`
- 发表年份/会议/期刊：`2023, Computational Visual Media / arXiv 2022`
- DOI / arXiv ID：`[待确认 DOI]` / `[待确认 arXiv]`
- BibTeX key：`guo2023van`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/Visual_Attention_Network_VAN_2023.pdf`
- 当前定位：`通过 Large Kernel Attention (LKA) 实现线性复杂度的长程相关建模；本质是“大核分解 + 注意力门控”的纯 CNN/Conv-style backbone`
- 与已提取论文的关系：
  - 与 `Scaling-Up-Kernels_2022` 互补：RepLKNet 是直接大核卷积，VAN 是大核注意力
  - 与 `Wavelet-Convolutions_2024` 互补：WTConv 更偏频域分解，LKA 更偏空间大核注意力
  - 对你后续 `LKMA` 这类命名或思路尤其有参考价值，因为它明确把 large kernel 与 attention 合并成统一模块

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：self-attention 直接用于视觉有三类问题，分别是忽略 2D 结构、二次复杂度过高、只关注空间适应而忽略通道适应
  - 用途：`方法动机`
  - 页码：`Abstract, p.1`
- 句子/事实 2：作者提出线性注意力 `Large Kernel Attention (LKA)`，用来同时获得自适应性和长程依赖
  - 用途：`核心贡献`
  - 页码：`Abstract, p.1; Sec.3.1, p.3-p.4`
- 句子/事实 3：`VAN-B2` 在 ADE20K 上达到 `50.1 mIoU`，比 `Swin-T` 高 `4.0`
  - 用途：`主结果概括`
  - 页码：`Abstract, p.1; Tab.12`

#### 1.1.2 related work 可引用句

- 句子/事实 1：LKA 结合了卷积和 self-attention 的优点，具有 local receptive field、long-range dependence、spatial adaptability、channel adaptability，且复杂度为 `O(n)`
  - 用途：`大核注意力优势总结`
  - 页码：`Tab.1, p.3-p.4`
- 句子/事实 2：标准大核卷积可分解为 `DW-Conv + DW-D-Conv + 1x1 Conv`
  - 用途：`工程实现出处`
  - 页码：`Fig.2; Sec.3.1, p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| default kernel `K` | `21` | LKA 默认大核 | `p.4` |
| best default dilation `d` | `3` | `K=21` 时默认 | `p.4` |
| ImageNet training | `300 epochs, AdamW` | 分类设置 | `p.5` |
| initial LR | `5e-4` | 训练设置 | `p.5` |
| batch size | `1024` | 分类设置 | `p.5` |
| VAN-B2 | `26.6M / 5.0G / 82.8%` | ImageNet | `Tab.7` |
| VAN-B2 + UperNet | `50.1 mIoU` | ADE20K | `Tab.12` |
| VAN-B2 + Mask R-CNN | `46.4 APb / 41.8 APm` | COCO | `Tab.10` |
| VAN-B6 | `87.8%` | ImageNet-22K pretrain 后 | `p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- self-attention 在视觉中虽然强大，但直接移植存在明显代价
- 把图像当作 1D token 序列会弱化二维局部结构
- 全局 self-attention 二次复杂度高，不适合高分辨率视觉任务
- 常规卷积又缺乏长程依赖和动态适应性
- 需要一种同时兼顾局部性、长程建模、动态响应和线性复杂度的视觉注意力

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `Large Kernel Attention (LKA)`。它把一个大核卷积分解为 `DW-Conv + DW-D-Conv + 1x1 Conv`，先用 depth-wise conv 抽局部上下文，再用 depth-wise dilated conv 捕获长程依赖，最后用 `1x1` 做通道混合并生成 attention map，再与输入逐元素相乘得到输出。基于 LKA，作者构建层次化 backbone `VAN`，在分类、检测、分割、全景分割等任务上都优于同量级 CNN/ViT backbone。

关键页码：

- `Sec.3.1-Sec.3.2, p.3-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`hierarchical backbone with LKA`
- stage 结构：
  - 共 `4` 个 stage
  - 输出分辨率依次为 `H/4, H/8, H/16, H/32`
- 每个 stage 的基本单元：
  - `BN`
  - `1x1 Conv`
  - `GELU`
  - `LKA`
  - `FFN`
- 论文构建了 `VAN-B0` 到 `VAN-B6` 七个规模版本

### 3.2 关键模块详细描述

**模块 1：`Large Kernel Attention (LKA)`**

- 位置：`每个 stage 的核心空间建模模块`
- 操作流程：
  1. `DW-Conv` 捕获局部上下文
  2. `DW-D-Conv` 扩大感受野并捕获长程依赖
  3. `1x1 Conv` 做通道混合并形成 attention map
  4. attention map 与输入逐元素相乘
- 核心意义：
  - 用线性复杂度获得长程依赖
  - 同时具备空间与通道适应性
- 页码：`Sec.3.1, p.3-p.4`

**模块 2：`Hierarchical VAN Stage`**

- 位置：`backbone 四个层级`
- 操作流程：
  1. 先下采样
  2. 堆叠 `L` 个 `BN + 1x1 + GELU + LKA + FFN` 单元
  3. 逐 stage 提高通道数、降低分辨率
- 页码：`Sec.3.2, p.4`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| default `K` | `21` | LKA 默认核大小 | `p.4` |
| default `d` | `3` | 默认 dilation | `p.4` |
| `K=21` decomposition | `5x5 DW-Conv + 7x7 DW-D-Conv(d=3) + 1x1` | 低成本近似大核注意力 | `p.3-p.4` |
| VAN-B2 | `26.6M / 5.0G` | 中型主力模型 | `Tab.5, p.5` |
| VAN-B6 | `200M / 38.4G` | 大模型 | `Tab.5, p.5` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：LKA 模块

```text
Attention = Conv1x1(DW-D-Conv(DW-Conv(F)))
Output = Attention ⊗ F
```

符号说明：

- `F ∈ R^(C×H×W)`：输入特征
- `Attention`：由大核分解生成的 attention map
- `⊗`：逐元素乘法
- 页码：`Eq.(1)-(2), p.3`

公式 2：大核分解

```text
K x K conv
≈ ceil(K/d) x ceil(K/d) DW-D-Conv(d)
 + (2d-1) x (2d-1) DW-Conv
 + 1x1 Conv
```

符号说明：

- `K`：目标大核尺寸
- `d`：dilation rate
- 含义：用更小代价近似一个大核空间建模过程
- 页码：`Sec.3.1, p.3`

公式 3：参数与 FLOPs

```text
P(K, d) = C( ceil(K/d)^2 × C + (2d-1)^2 ) + C^2
F(K, d) = P(K, d) × H × W
```

符号说明：

- `C`：通道数
- `H, W`：特征图尺寸
- 用于说明 LKA 分解后的预算优势
- 页码：`Eq.(3)-(4), p.4`

### 4.2 推导过程或梯度行为

- 核心思想：
  - 用 depth-wise local conv 保留局部结构
  - 用 dilated depth-wise conv 建模 long-range dependence
  - 用 `1x1 conv` 引入通道交互和适应性
- 与 self-attention 的差异：
  - 不做 token-to-token 二次关系矩阵
  - 不需要 softmax / sigmoid 形式的 attention normalization
- 与纯卷积的差异：
  - 最终是 attention map 门控，而不只是单纯卷积输出
- 页码：`p.3-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `classification loss` | `[标准分类损失]` | ImageNet 训练 | classifier |
| `detection/segmentation loss` | `[对应框架默认损失]` | COCO / ADE20K 等 | task heads |

### 5.2 总损失公式

```text
L_total = L_task
```

说明：

- 本文创新点在 backbone 和 attention 结构
- 沿用下游框架原生训练目标

### 5.3 权重配置与调度策略

- 分类训练：
  - `AdamW`
  - `300 epochs`
  - `weight decay = 5e-2`
  - `initial LR = 5e-4`
  - `cosine schedule + warmup`
- 训练技巧：
  - `label smoothing`
  - `mixup`
  - `cutmix`
  - `random erasing`
  - `EMA`
- 页码：`p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ImageNet-1K` | `1.28M train` | `50K val` | `validation` | 分类 |
| `ImageNet-22K` | `14M images, 21841 classes` | `finetune on 1K` | `validation` | 大模型预训练 |
| `COCO 2017` | `118K train` | `5K val` | `validation` | detection / instance seg |
| `ADE20K` | `20K train / 2K val / 3K test` | `val/test` | `validation` | semantic segmentation |

### 6.2 数据增强

- ImageNet：
  - `random crop`
  - `random horizontal flip`
  - `label smoothing`
  - `mixup`
  - `cutmix`
  - `random erasing`
- detection / segmentation：
  - 与 Swin / ConvNeXt 使用相同训练验证策略
- 页码：`p.5-p.8`

### 6.3 优化器与超参数

- 分类：
  - `AdamW`
  - `momentum = 0.9`
  - `weight decay = 5e-2`
  - `batch size = 1024`
  - `LR = 5e-4`
- ImageNet-22K 预训练：
  - `90 epochs`
  - `batch size = 8196`
- segmentation：
  - 框架：`MMSEG`
  - heads：`Semantic FPN`, `UperNet`
- detection：
  - 框架：`MMDetection`
  - heads：`RetinaNet`, `Mask R-CNN`, `Cascade Mask R-CNN`, `Sparse R-CNN`
- 页码：`p.5-p.8`

### 6.4 预处理与数据细节

- 所有 backbone 先在 ImageNet 预训练
- ADE20K 采用两套比较协议：
  - `Semantic FPN`
  - `UperNet`
- COCO 检测主要以：
  - `RetinaNet 1x`
  - `Mask R-CNN 1x`
  - `36 epochs` 的更强对比
- 页码：`p.7-p.8`

---

## 7. 推理与后处理

- backbone 推理过程：
  1. stage-wise 下采样
  2. 在每个 stage 堆叠 `LKA + FFN`
  3. 输出供检测/分割 head 使用
- 本文主要贡献集中在 backbone，不依赖特殊后处理
- 页码：`p.4-p.8`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 改 kernel size `7/14/21/28` | `21` 起基本最好 | 大核有效，但过大收益趋缓 |
| `A2` | 去掉 DW-Conv | Top-1 降 `0.5` | 局部上下文仍关键 |
| `A3` | 去掉 attention 或把乘法换加法 | 性能下降 | 真正的注意力门控有效 |
| `A4` | normalization in attention | 不需要额外 sigmoid/softmax | LKA 设计更简洁 |
| `A5` | 与 Swin/ConvNeXt 比较 | 同规模下多任务更强 | LKA backbone 有竞争力 |

### 8.2 各模块贡献量化

- kernel size 消融：
  - `K=7`: `74.8`
  - `K=14`: `75.3`
  - `K=21`: `75.4`
  - `K=28`: `75.4`
- ImageNet-1K：
  - `VAN-B2 82.8`
  - `VAN-B3 83.9`
- ADE20K UperNet：
  - `Swin-T 46.1`
  - `ConvNeXt-T 46.7`
  - `VAN-B2 50.1`
- COCO Mask R-CNN：
  - `Swin-T 46.2 APb`（来自摘要对比口径）
  - `VAN-B2 48.8 AP` 量级更强
- 页码：`p.5-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ImageNet-1K` | `VAN-B2 82.8` | `VAN-B3 83.9` | `VAN-B6 87.8 (22K pretrain chain)` | classification |
| `ADE20K` | `VAN-B2 50.1 mIoU` | `VAN-B3 50.6` | `VAN-B4 52.2` | UperNet |
| `COCO RetinaNet 1x` | `VAN-B2 44.9 AP` | `VAN-B3 47.5 AP` | 强于同级 PVT/ResNet | detection |
| `COCO Mask R-CNN 1x` | `VAN-B2 46.4 APb / 41.8 APm` | `VAN-B3 48.3 / 43.4` | 强于同级 baseline | detection + instance seg |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Swin-T + UperNet` | `ADE20K` | `46.1` | 对照 | transformer baseline |
| `ConvNeXt-T + UperNet` | `ADE20K` | `46.7` | 对照 | CNN baseline |
| `VAN-B2 + UperNet` | `ADE20K` | `50.1` | `+4.0 vs Swin-T` | 主结果 |
| `PVTv2-B2 + Semantic FPN` | `ADE20K` | `45.2` | 对照 | transformer baseline |
| `VAN-B2 + Semantic FPN` | `ADE20K` | `46.7` | 更优 | 同级 backbone |
| `Swin-B + UperNet` | `ADE20K` | `49.7` | 对照 | large baseline |
| `VAN-B4 + UperNet` | `ADE20K` | `52.2` | 更优 | stronger model |

### 9.3 公平对比条件确认

- 是否统一任务头：`是，ADE20K 用 Semantic FPN / UperNet，COCO 用标准检测头`
- 是否统一训练策略：`是，作者强调沿用 Swin / ConvNeXt 设置`
- 是否统一预训练：`是，按 ImageNet-1K 或 22K 分组比较`
- 页码：`p.5-p.8`

### 9.4 评价协议与指标定义

- 分类：`Top-1 accuracy`
- 语义分割：`mIoU`
- 检测：`AP`
- 实例分割：`APb / APm`
- 全景分割：`PQ`
- 页码：`p.1, p.7-p.9`

---

## 10. 计算量与效率

- LKA 的核心卖点：
  - 保持 `O(n)` 复杂度
  - 同时获得 large receptive field 与 dynamic response
- 参数优势示例，`21x21` convolution：
  - `C=32` 时，standard conv `451,584`
  - MobileNet-style decomposition `15,136`
  - LKA decomposition `3,392`
- 实验层面：
  - `VAN-B2` 仅 `26.6M / 5.0G` 即达到 `82.8%`
  - 在 accuracy-throughput 图中 trade-off 优于 Swin
- 页码：`Tab.2, p.3-p.4; Fig.5, p.5`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/Visual-Attention-Network`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`仓库待确认`
- 复现难度评估：`中`
- 复现障碍：
  - 需要正确实现 LKA 的大核分解
  - 多任务结果依赖 MMDetection / MMSEG 等成熟工具链

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| arXiv/DOI 精确信息 | `未在当前抽取块确认` | `后续补查` | `低` |
| 各下游任务完整 schedule 细节 | `正文有限` | `以官方仓库为准` | `中` |
| 预训练权重链接 | `需仓库确认` | `后续补查` | `低` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 文中主张 LKA 优于 self-attention 的某些缺点，但本质上仍是 backbone 层面方法，不直接解决实例边界或拓扑问题
- 模型规模增大后，仍需大规模预训练支持最强性能

### 14.2 我们观察到的潜在问题

- 对腺体分割而言，LKA 更像 backbone/attention 增强，并非直接的 boundary-aware 机制
- 如果只引入 LKA，不配合边界监督或实例分离设计，可能更偏“区域表达提升”而非“边界拆分”
- 但其大核注意力与形态建模的思路，对复杂腺体轮廓仍很有启发

### 14.3 失败案例 / 定性分析

- 论文通过 CAM 可视化说明：
  - VAN 能更聚焦判别区域
  - 表明长程依赖确实被捕获
- 对我们任务的映射：
  - 可期待它更好覆盖腺体整体结构
  - 但仍不能替代显式 boundary/topology 方法

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `Large Kernel Attention` 这一命名和思想框架
- “large kernel + attention + linear complexity” 的论证逻辑
- hierarchical backbone + LKA 的组合方式

### 15.2 可以作为候选参数来源的

- 默认 `K = 21`
- 默认 `d = 3`
- 大核分解：`5x5 DW-Conv + 7x7 DW-D-Conv(d=3) + 1x1`

### 15.3 不应照搬的（及原因）

- 直接整套照搬大规模 `VAN-B4/B5/B6` 到腺体实验：
  - 原因：工程成本和算力压力较大
- 把 LKA 当成边界监督替代品：
  - 原因：它是表示增强模块，不是显式边界/拓扑约束

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| `LKMA` / 大核注意力模块 | 直接来源 | `强` |
| 感受野增强 | 证明长程依赖可由大核注意力高效实现 | `强` |
| 形态建模 | 更大 receptive field + adaptive gating 对结构理解有益 | `中-强` |
| 边界监督 | 间接支持 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`LKMA 模块定义`、`backbone 改造动机`
- [ ] 需要和哪篇论文交叉验证：`Scaling-Up-Kernels_2022`、`Wavelet-Convolutions_2024`
- [ ] 待确认的问题：`你要的是完整 LKA block，还是只借其大核分解形式`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | self-attention 在视觉中的三类不足 | 作为提出 LKA 的动机 |
| related work | 大核注意力路线代表方法 | 放在 receptive field / attention 模块综述 |
| 方法 | LKA 的分解式实现 | 作为 LKMA 的核心来源 |
| 实验分析 | ADE20K/COCO 的大幅提升 | 证明模块普适性 |
| 讨论 | 大核注意力不同于显式边界监督 | 连接到边界方法组 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 2` | `p.3` | 大核卷积分解图 | 回填 LKA 机制 |
| `Eq.(1)-(4)` | `p.3-p.4` | LKA 与参数/FLOPs 公式 | 回填公式 |
| `Figure 3` | `p.4` | LKA 与其他模块对比 | 解释 attention 结构 |
| `Figure 4` | `p.4` | VAN stage 结构 | 回填 backbone |
| `Table 2` | `p.3-p.4` | 21x21 卷积参数对比 | 写效率优势 |
| `Table 5-7` | `p.5-p.6` | VAN 配置、kernel 消融、ImageNet 结果 | 数字引用 |
| `Table 12-13` | `p.7-p.8` | ADE20K 结果 | 语义分割引用 |
| `Table 9-11/14` | `p.6-p.9` | COCO detection / panoptic 结果 | 下游任务引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] LKA 公式与大核分解已覆盖
- [x] 参数/FLOPs 分析已记录
- [x] ImageNet / ADE20K / COCO 主结果已覆盖
- [x] 与 self-attention 的差异已写清
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`
