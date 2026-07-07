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

- `wavelet-domain large receptive field`
- `WTConv`
- `multi-frequency spatial mixing`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是“如何不靠暴力增大卷积核也能获得超大感受野”的关键方法支撑
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Wavelet Convolutions for Large Receptive Fields`
- 作者/团队：`Shahaf E. Finder, Roy Amoyal, Eran Treister, Oren Freifeld`
- 发表年份/会议/期刊：`2024, ECCV 2024 / arXiv v2`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:2407.05848`
- BibTeX key：`finder2024wtconv`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/Wavelet_Convolutions_for_Large_Receptive_Fields_2024.pdf`
- 当前定位：`通过小波域卷积实现超大感受野的现代模块论文；核心不在直接增大 kernel，而在用 wavelet decomposition 让小核在原图上对应更大 receptive field`
- 与已提取论文的关系：
  - 与 `Large-Kernel-Matters_2017` 互补：那篇强调“大核为何有用”，这篇强调“如何更高效地实现大感受野”
  - 与 `Scaling-Up-Kernels_2022` 互补：RepLKNet 走“直接大核 + re-param”路线，这篇走“wavelet-domain + small kernel”路线
  - 对你的 `LKMA` 或形态建模模块很有价值，因为它同时给出了 `ERF`、`shape bias`、`robustness` 的证据

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：利用 `Wavelet Transform` 可以在不过度参数化的前提下实现非常大的感受野
  - 用途：`方法动机`
  - 页码：`Abstract, p.1; Sec.1, p.1-p.2`
- 句子/事实 2：对于 `k x k` receptive field，本文方法的可训练参数量只随 `k` 对数级增长
  - 用途：`效率论据`
  - 页码：`Abstract, p.1`
- 句子/事实 3：`WTConv` 可以作为现有网络中 depth-wise convolution 的 `drop-in replacement`
  - 用途：`模块可插拔性`
  - 页码：`Abstract, p.1; Sec.1, p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`WTConv` 获得更大的 `effective receptive field`，并更强调低频与形状信息
  - 用途：`大感受野与形态偏置支撑`
  - 页码：`p.2-p.3; p.12-p.13`
- 句子/事实 2：作者不仅在分类中验证 `WTConv`，还把它接入 `UperNet` 做语义分割、接入 `Cascade Mask R-CNN` 做检测
  - 用途：`说明这是通用 backbone 模块`
  - 页码：`p.2-p.3; p.10-p.11`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| ConvNeXt stage WT levels | `[5,4,3,2]` | WTConvNeXt 默认配置 | `p.9-p.10` |
| kernel size | `5 x 5` | 主配置 | `p.9-p.10` |
| ImageNet 120e | `81.7 top-1` | WTConv on ConvNeXt-T | `p.10` |
| ImageNet 300e WTConvNeXt-B | `84.1 top-1` | 分类结果 | `p.10` |
| ADE20K WTConvNeXt-T | `45.4 / 46.6 mIoU` | 120e / 300e 预训练 | `p.10` |
| ADE20K WTConvNeXt-S | `49.0 mIoU` | 300e 预训练 | `p.10` |
| COCO WTConvNeXt-T | `51.0 APbox / 44.4 APmask` | 300e pretrain + 3x finetune | `p.10-p.11` |
| shape bias gain | `+8% ~ +12%` | 相比 ConvNeXt | `p.12-p.13` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CNN 为了逼近 ViT 的全局混合能力，通常需要更大感受野
- 直接增大卷积核很快遇到参数量、计算量和优化稳定性的上限
- 即便现代大核 CNN 有效果，继续靠暴力堆大 kernel 并不总是最优
- 需要一种让小核也能对应大范围空间交互、同时保留卷积局部归纳偏置的方法

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `WTConv`。它先对输入做多级 Haar wavelet transform，把输入分解为低频和高频分量；然后在 wavelet domain 里对这些多频带特征使用小核 depth-wise convolution；最后再通过 inverse wavelet transform 聚合回原空间。这样，小核在原图上能对应更大的有效感受野，同时更强调低频和形状信息，因此既能提升 `ERF`，又能带来更强 `shape bias`、更好的 corruption robustness，并可直接替换现有网络里的 depth-wise conv。

关键页码：

- `Sec.3.1-Sec.3.3, p.5-p.8`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`wavelet transform + small-kernel depth-wise conv + inverse wavelet transform`
- 模块定位：`drop-in replacement for depth-wise convolution`
- 默认验证 backbone：
  - `ConvNeXt`
  - `MobileNetV2`
- 下游验证：
  - `UperNet` on `ADE20K`
  - `Cascade Mask R-CNN` on `COCO`

### 3.2 关键模块详细描述

**模块 1：`One-Level Haar WT`**

- 位置：`WTConv 前端`
- 操作流程：
  1. 用 Haar filters 对输入做二维小波分解
  2. 得到 `LL / LH / HL / HH` 四个频带
  3. 低频保留全局结构，高频保留方向性细节
- 页码：`Sec.3.1, p.5-p.6`

**模块 2：`Multi-Level Wavelet-Domain Convolution`**

- 位置：`WTConv 主体`
- 操作流程：
  1. 递归分解低频分量 `LL`
  2. 在每一级 wavelet-domain 的频带特征上做小核 depth-wise convolution
  3. 通过不同 level 的卷积形成多尺度空间混合
- 核心意义：
  - 用固定小核获得更大的原空间 receptive field
  - 在多频带上建模，形成 multi-frequency response
- 页码：`Sec.3.2, p.6-p.7`

**模块 3：`IWT Aggregation`**

- 位置：`WTConv 后端`
- 操作流程：
  1. 将各级卷积结果通过 IWT 逐级聚合
  2. 恢复到原空间分辨率
  3. 输出最终特征图
- 页码：`Sec.3.2, p.6-p.7`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| wavelet basis | `Haar` | 高效、简单 | `p.5` |
| ConvNeXt levels | `[5,4,3,2]` | 逐 stage 分解深度 | `p.9-p.10` |
| default kernel | `5 x 5` | wavelet-domain 小核 | `p.9-p.10` |
| example receptive fields | `[160,80,40,20]` | 各 stage 感受野 | `p.10, Table 1` |
| task compatibility | `UperNet / Cascade Mask R-CNN` | 下游验证 | `p.10-p.11` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：二维 Haar WT 滤波器

```text
fLL = 1/2 [[1,  1],
           [1,  1]]
fLH = 1/2 [[1, -1],
           [1, -1]]
fHL = 1/2 [[ 1,  1],
           [-1, -1]]
fHH = 1/2 [[ 1, -1],
           [-1,  1]]
```

符号说明：

- `LL`：低频分量
- `LH / HL / HH`：高频分量
- 页码：`Eq.(1), p.5-p.6`

公式 2：一层小波分解

```text
[XLL, XLH, XHL, XHH] = Conv([fLL, fLH, fHL, fHH], X)
```

符号说明：

- `X`：输入图像/特征图
- 输出四个频带，分辨率各减半
- 页码：`Eq.(2), p.6`

公式 3：逆小波变换

```text
X = Conv-transposed([fLL, fLH, fHL, fHH],
                    [XLL, XLH, XHL, XHH])
```

符号说明：

- 用转置卷积形式实现 IWT
- 页码：`Eq.(3), p.6`

公式 4：级联分解

```text
XLL(i), XLH(i), XHL(i), XHH(i) = WT(XLL(i-1))
```

符号说明：

- 每一级只继续分解低频 `LL`
- 级联后频率分辨率提高、空间分辨率降低
- 页码：`Eq.(4), p.6`

公式 5：WTConv 主操作

```text
Y = IWT(Conv(W, WT(X)))
```

符号说明：

- `W`：wavelet-domain 小核卷积权重
- 含义：先 WT，再卷积，最后 IWT
- 页码：`Eq.(5), p.6`

公式 6：多级 WTConv 聚合

```text
XLL(i), XH(i) = WT(XLL(i-1))
YLL(i), YH(i) = Conv(W(i), (XLL(i), XH(i)))
Z(i) = IWT(YLL(i) + Z(i+1), YH(i))
```

符号说明：

- `XH(i)`：第 `i` 级全部高频分量
- `Z(i)`：从第 `i` 级开始聚合后的输出
- 页码：`Eq.(6)-(8), p.6-p.7`

### 4.2 推导过程或梯度行为

- 参数与感受野关系：
  - `l` 级 WT、固定核大小 `k` 时，参数量按 `l * 4 * c * k^2` 线性增长
  - receptive field 按 `2^l * k` 指数增长
- 这意味着：
  - 若以 receptive field `k x k` 为目标，参数量可近似只随 `log k` 增长
- 频率解释：
  - 重复分解低频会增强低频响应
  - 因而 WTConv 更偏向形状而非纹理
- 页码：`p.7-p.8`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `classification loss` | `[标准分类损失]` | ImageNet-1K 分类 | classifier |
| `segmentation loss` | `[UperNet 默认分割损失]` | ADE20K 分割 | segmentation head |
| `detection loss` | `[Cascade Mask R-CNN 默认损失]` | COCO 检测/实例分割 | detector head |

### 5.2 总损失公式

```text
L_total = L_task
```

说明：

- 本文贡献在模块设计与频域空间混合，而不是新损失
- 下游任务均沿用原框架默认训练目标

### 5.3 权重配置与调度策略

- 不引入特殊 loss 权重
- 直接在原有框架里把 depth-wise conv 替换为 WTConv
- 页码：`p.9-p.11`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ImageNet-1K` | `标准训练集` | `标准验证` | `val` | 分类主实验 |
| `ADE20K` | `标准 train` | `标准 val` | `validation` | UperNet |
| `COCO` | `标准 train` | `标准 val` | `validation` | Cascade Mask R-CNN |
| `ImageNet-C/A/R/Sketch` | `benchmark` | `benchmark` | `标准协议` | robustness 分析 |

### 6.2 数据增强

- 分类使用：
  - `120-epoch`
  - `300-epoch`
  - 具体增广细节在附录
- segmentation / detection：
  - 完全沿用 `ConvNeXt` 原始配置
  - 作者强调 `without parameter tuning`
- 页码：`p.9-p.11`

### 6.3 优化器与超参数

- 主分类 backbone：`ConvNeXt`
- stage-wise WT levels：`[5,4,3,2]`
- wavelet-domain kernel：`5 x 5`
- ADE20K：
  - `MMSegmentation`
  - `80K / 160K` finetune
  - `single-scale mIoU`
- COCO：
  - `MMDetection`
  - `1x / 3x` finetune
- 输入与 FLOPs 口径：
  - `ADE20K`: `2048 x 512`
  - `COCO`: `1280 x 800`
- 页码：`p.9-p.11`

### 6.4 预处理与数据细节

- wavelet basis：`Haar`
- 频带配置：
  - 同时使用低频和高频
  - ablation 显示单独用 low 或 high 都有提升，但两者一起最好
- 其他 wavelet bases：
  - `db2`, `db3` 也可用
  - 但 Haar 已足够有效
- 页码：`p.12-p.14`

---

## 7. 推理与后处理

- 推理流程：
  1. 对输入/特征图做多级 WT
  2. 在各频带做小核 depth-wise conv
  3. 通过 IWT 聚合回原空间
- 结构特征：
  - 纯卷积式 spatial mixing
  - 不依赖 self-attention
- 页码：`p.6-p.7`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 改 WT levels / kernel size | levels 和 kernel 增大多数情况下更好 | 更大感受野总体有益 |
| `A2` | 只用 lows 或只用 highs | 都优于 baseline，但不如一起用 | 低高频互补 |
| `A3` | Haar vs `db2/db3` | Haar 已足够强 | 简单基底已可用 |
| `A4` | WTConv vs RepLK / SLaK / GFNet | WTConv 更省参数且结果更强或相近 | 频域大感受野更高效 |
| `A5` | ERF / shape bias / robustness 分析 | WTConv 更全局、更形状化、更稳健 | 解释收益来源 |

### 8.2 各模块贡献量化

- ImageNet-1K 120e, ConvNeXt-T：
  - baseline `81.0`
  - `+VAN 81.1`
  - `+GFNet 81.2`
  - `+RepLK 81.5`
  - `+SLaK 81.5`
  - `+WTConv 81.7`
- ADE20K：
  - `ConvNeXt-T 44.6 -> WTConvNeXt-T 45.4`
  - `ConvNeXt-T 46.0 -> WTConvNeXt-T 46.6`
  - `ConvNeXt-S 48.7 -> WTConvNeXt-S 49.0`
- COCO：
  - `ConvNeXt-T 50.4/43.7 -> WTConvNeXt-T 51.0/44.4`
  - `ConvNeXt-S 51.9/45.0 -> WTConvNeXt-S 52.6/45.6`
- shape bias：
  - 相比 ConvNeXt 提升 `8% ~ 12%`
- 页码：`p.10-p.13`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ImageNet-1K` | `WTConvNeXt-T 82.5` | `WTConvNeXt-S 83.6` | `WTConvNeXt-B 84.1` | 300e |
| `ADE20K` | `WTConvNeXt-T 45.4 / 46.6 mIoU` | `WTConvNeXt-S 49.0 mIoU` | `+0.3 ~ +0.6 over ConvNeXt` | UperNet |
| `COCO` | `WTConvNeXt-T 51.0 APbox / 44.4 APmask` | `WTConvNeXt-S 52.6 / 45.6` | `+0.6 ~ +0.7` | Cascade Mask R-CNN |
| `Robustness / Shape Bias` | `higher corruption robustness` | `shape decisions +8%~12%` | `nearly-global ERF` | 分析结果 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `ConvNeXt-T` | `ImageNet-1K` | `81.0 / 82.1` | baseline | 对照 |
| `RepLK` | `ImageNet-1K` | `81.5` | more D-W params | 大核对照 |
| `SLaK` | `ImageNet-1K` | `81.5` | larger RF | 大核对照 |
| `WTConv` | `ImageNet-1K` | `81.7 / 82.5` | 更省参数 | wavelet 路线 |
| `WTConvNeXt-T` | `ADE20K` | `45.4 / 46.6` | 优于 ConvNeXt-T | segmentation |
| `WTConvNeXt-T` | `COCO` | `51.0 / 44.4` | 优于 ConvNeXt-T | detection |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，在 ConvNeXt/MobileNetV2 框架内替换 depth-wise conv`
- 是否统一 head：`是，ADE20K 用 UperNet，COCO 用 Cascade Mask R-CNN`
- 是否统一训练设置：`是，作者强调使用原 ConvNeXt 配置且不调参`
- 是否统一 FLOPs 统计口径：`是`
- 页码：`p.9-p.11`

### 9.4 评价协议与指标定义

- 分类：`top-1 accuracy`
- 语义分割：`single-scale mIoU`
- 检测/实例分割：`APbox / APmask`
- 额外分析：
  - `ImageNet-C/A/R/Sketch`
  - `shape bias`
  - `ERF`
- 页码：`p.10-p.13`

---

## 10. 计算量与效率

- 核心公式：
  - 参数量约为 `l * 4 * c * k^2`
  - receptive field 约为 `2^l * k`
- 例子：
  - 单通道 `512 x 512` 输入上，`7 x 7` DW conv 为 `12.8M FLOPs`
  - `31 x 31` DW conv 为 `252M FLOPs`
  - 3-level WTConv + `5 x 5` kernel、覆盖 `40 x 40` RF 时约 `17.9M FLOPs`
- 优势：
  - 用较小参数量实现更大 RF
  - 在主表里通常不增加或几乎不增加 backbone FLOPs
- 代价：
  - 现有框架下运行时可能偏慢，因为 `WT-conv-IWT` 是多步串行操作
- 页码：`p.7-p.8; p.14`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/BGU-CS-VIL/WTConv`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`代码仓库可用，权重情况待仓库确认`
- 复现难度评估：`中`
- 复现障碍：
  - 多级 `WT-conv-IWT` 的实现效率依赖工程优化
  - 现有通用框架下吞吐可能低于理论优势
  - 下游任务需接 `MMSegmentation / MMDetection`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 详细优化器/学习率 | `主文部分有限` | `后续查附录/仓库` | `中` |
| 预训练权重下载口径 | `待仓库确认` | `后续补查` | `低` |
| 高效 CUDA 实现细节 | `未完全展开` | `优先使用官方实现` | `中` |
| 运行时优化方案 | `仅概述` | `必要时自行实现并行 WT` | `中-高` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- WTConv 虽然 FLOPs 不高，但在现有框架中运行时间可能偏高
- 原因是 `WT-conv-IWT` 的多次顺序操作带来额外内存访问与调度开销

### 14.2 我们观察到的潜在问题

- 这篇主要解决大感受野与形状偏置问题，不直接解决腺体实例分离或边界黏连
- wavelet-domain 实现复杂度高于普通卷积替换
- 若你的目标是快速迭代实验，直接复现完整 WTConv backbone 成本高于简单的大核块

### 14.3 失败案例 / 定性分析

- 论文的“风险点”主要体现在工程实现而非性能崩溃：
  - 理论 FLOPs 低，但吞吐不一定理想
  - 需要更专门的实现来真正发挥效率
- 这对我们的启示是：
  - 可以先借其设计思想做轻量近似版
  - 不一定一开始就完整照搬 WT + IWT 全链路

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- “扩大感受野不一定只能靠更大卷积核，也可以靠 wavelet-domain spatial mixing” 这条论证
- `低频更对应形状、纹理更偏高频` 的解释框架
- `ERF / shape bias / corruption robustness` 三位一体的分析口径

### 15.2 可以作为候选参数来源的

- `levels = [5,4,3,2]`
- `kernel = 5 x 5`
- `Haar` 作为默认 wavelet basis
- 同时使用 low/high 频带，而不是只保留一个频带

### 15.3 不应照搬的（及原因）

- 直接把完整 WTConvNeXt backbone 整套移植到腺体分割：
  - 原因：工程复杂度高，且你当前更需要高性价比可控改造
- 把 robustness / corruption 收益直接等同于病理泛化收益：
  - 原因：自然图像 corruption 与病理 stain/shape 变化并不完全同构

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 大感受野模块 | 证明可不靠暴力大核而获得超大 RF | `强` |
| 形态建模 | 低频/shape bias 论证很适合腺体结构 | `强` |
| 轻量化改造 | 提供“参数增长慢于 RF 增长”的路线 | `中-强` |
| 边界/拓扑监督 | 不是本文重点 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`LKMA 设计动机`、`形态感受野增强依据`
- [ ] 需要和哪篇论文交叉验证：`Scaling-Up-Kernels_2022`、`Large-Kernel-Matters_2017`
- [ ] 待确认的问题：`是否值得做 WT 的轻量近似版，而不是完整 WTConv`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 不靠暴力大核也能获得超大感受野 | 作为现代大感受野动机 |
| related work | wavelet-based receptive field enlargement | 放在大核/频域模块相关工作 |
| 方法 | WTConv 的频带分解与聚合思路 | 作为可借鉴结构来源 |
| 实验分析 | ERF / shape bias / robustness 框架 | 用于解释模块收益来源 |
| 讨论 | 大感受野与形状偏置的关系 | 引向病理形态建模 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.2, p.12-p.13` | ERF 可视化 | 写大感受野证据 |
| `Eq.(1)-(4)` | `p.5-p.6` | Haar WT / IWT / cascade decomposition | 回填公式 |
| `Eq.(5)-(8)` | `p.6-p.7` | WTConv 主操作与多级聚合 | 回填方法 |
| `Eq.(9)-(11)` | `p.7-p.8` | FLOPs 计算 | 回填效率分析 |
| `Figure 2-3` | `p.6-p.7` | wavelet-domain 卷积示意 | 写机制 |
| `Table 1-4` | `p.10-p.11` | 分类/分割/检测主结果 | 数字引用 |
| `Figure 4` | `p.12-p.13` | shape bias 分析 | 形态偏置证据 |
| `Table 8` | `p.13-p.14` | ablation study | 参数与 levels 参考 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] Haar WT / IWT / WTConv 公式已覆盖
- [x] 参数增长与感受野增长关系已写清
- [x] 分类 / 分割 / 检测主结果已覆盖
- [x] ERF / shape bias / robustness 已单独记录
- [x] 局限性与工程代价已补充
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`
