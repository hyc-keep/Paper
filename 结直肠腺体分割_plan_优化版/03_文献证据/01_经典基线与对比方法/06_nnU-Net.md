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

- `auto-configuring pipeline 论文`
- `baseline protocol / fairness 校准论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇对我们后续 `U-Net / ResNet34-U-Net / 腺体分割公平基线协议` 都很关键，所以额外完成：`2, 4, 5, 8, 14`

---

## 1. 论文信息

- 论文名：`nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation`
- 作者/团队：`Fabian Isensee, Paul F. Jaeger, Simon A. A. Kohl, Jens Petersen, Klaus H. Maier-Hein`
- 发表年份/会议/期刊：`2021, Nature Methods, 18(2): 203-211`
- DOI / arXiv ID：`10.1038/s41592-020-01008-z` / `arXiv:1809.10486`（早期技术报告版本）
- BibTeX key：`isensee2021nnunet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/nnU-Net_a_self-configuring_method_for_deep_learning-based_biomedical_image_segmentation_2021.pdf`
- 当前定位：`强通用医学分割 baseline 与实验规范来源；它的核心价值不只是结构本身，而是把 preprocessing / patch / aug / infer / postprocess / model selection 一起系统化`
- 与已提取论文的关系：
  - 继承自：`U-Net_2015` 的 encoder-decoder 基础范式
  - 互补于：`ResNet_2016`、`UNet++_2018`、`Attention_U-Net_2018`、`DeepLabV3+_2018`
  - 被谁引用/校准：大量医学分割 benchmark、挑战赛方案、后续很多方法论文的 baseline 设计

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：很多 biomedical segmentation 方法的性能差异，来源不只是网络结构，还来自 preprocessing、training、inference 和 postprocessing 的整套配置是否合理
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.3`
- 句子/事实 2：在 pipeline 配置合理时，`U-Net like architectures` 已经能够达到 state-of-the-art，未必需要复杂结构变体
  - 用途：`方法动机 / related work`
  - 页码：`p.3`
- 句子/事实 3：`nnU-Net` 的自动配置覆盖了 preprocessing、network architecture、training 和 postprocessing，而不是只调某一个局部模块
  - 用途：`方法概述`
  - 页码：`p.1-p.4`

#### 1.1.2 related work 可引用句

- 句子/事实 1：`nnU-Net` 把 pipeline design choices 拆成 `fixed parameters`、`rule-based parameters` 和 `empirical parameters`
  - 用途：`方法脉络 / 我们实验协议设计`
  - 页码：`p.3-p.5`
- 句子/事实 2：论文不是否认结构改进有价值，而是强调如果 baseline 协议没配好，就很难公平评估新模块是否真正有效
  - 用途：`实验公平性讨论`
  - 页码：`p.3-p.5`
- 句子/事实 3：推理阶段用与训练相同 patch size 的 sliding-window，并用 `Gaussian importance weighting` 聚合，可显著减少拼接边界伪影
  - 用途：`实验设置 / 推理协议`
  - 页码：`p.4`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| epoch 数 | `1000` | 训练设置 | `p.3-p.4` |
| 每个 epoch 迭代数 | `250` | 训练设置 | `p.3-p.4` |
| 初始学习率 | `0.01` | 优化器设置 | `p.3-p.4` |
| Nesterov momentum | `0.99` | 优化器设置 | `p.3-p.4` |
| inference stride | `patch_size / 2` | 推理协议 | `p.4` |
| batch size 下限 | `2` | patch / batch 配置原则 | `p.5` |
| GPU memory 目标 | `11 GB` | 默认硬件预算 | `Online Methods / Supplementary, p.65` |
| MSD 任务数 | `10` | benchmark 范围 | `Supplementary, p.38-p.39` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- biomedical image segmentation 并不存在一个“只要换更强 backbone 就自然更好”的统一方案
- 不同任务在维度、体素间距、各向异性、图像大小、前景比例、类别数、成像模态上差异极大
- end-to-end segmentation pipeline 的关键决策很多，而且彼此耦合：预处理、target spacing、patch size、batch size、augmentation、训练策略、推理方式、后处理等
- 这些设计如果依赖人工经验，不仅成本高、可迁移性差，而且容易把“工程调参收益”误认为“新模块理论收益”

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- `nnU-Net` 的核心不是提出一个花哨新 block，而是把 U-Net 系列在医学分割里真正起作用的 pipeline 经验系统化，拆成固定参数、规则驱动参数和经验选择参数，并根据数据集 fingerprint 自动生成合适的 `2D U-Net`、`3D full resolution U-Net`、`3D U-Net cascade` 配置，再通过 cross-validation 自动挑选单模型或 ensemble 以及是否启用 postprocessing。

关键页码：

- `p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`self-configuring U-Net-based segmentation pipeline`
- 候选主干：`2D U-Net`、`3D full resolution U-Net`、`3D U-Net cascade`
- 编码器-解码器基本单元：`conv - instance norm - leaky ReLU`
- 每个分辨率阶段：`encoder 与 decoder 都使用两个 computational blocks`
- 下采样：`stride convolution`
- 上采样：`transpose convolution`
- 附加监督：`deep supervision`，加在除最低两层分辨率之外的 segmentation outputs 上

### 3.2 关键模块详细描述

**模块 1：`Dataset Fingerprint -> Pipeline Configuration`**

- 位置：`整个方法入口`
- 操作流程：
  1. 从训练集提取 image size、spacing、anisotropy、类别前景分布、强度统计等 fingerprint
  2. 依据固定规则确定 normalization、target spacing、patch size、batch size、kernel / stride 配置
  3. 自动生成 `2D / 3D fullres / 3D cascade` 候选配置
  4. 用交叉验证结果自动选择最佳单模型或 ensemble
- 页码：`p.3-p.5`

**模块 2：`Plain U-Net Backbone`**

- 位置：`所有候选配置的基础网络`
- 操作流程：
  1. 每个 stage 用两个 `conv - IN - lReLU` block
  2. 用 stride convolution 做下采样
  3. decoder 镜像 encoder，并通过 transpose convolution 上采样
  4. 通过 skip connection 融合高低层信息
- 页码：`p.3-p.5, Supplementary p.37-p.38`

**模块 3：`3D U-Net Cascade`**

- 位置：`大体积数据场景`
- 操作流程：
  1. 先在 low-resolution 数据上训练一个 3D U-Net 获取粗分割
  2. 将粗分割上采样到 full-resolution
  3. 以 one-hot segmentation map 与原图一起输入第二个 full-resolution U-Net 做细化
  4. 用 cross-validation 判断它是否比单个 full-resolution U-Net 更值得保留
- 页码：`p.3-p.5, Supplementary p.32-p.34`

**模块 4：`Model Selection + Ensemble + Postprocessing`**

- 位置：`训练后验证与测试提交阶段`
- 操作流程：
  1. 对每个配置执行五折交叉验证
  2. 聚合 5 个 fold 模型作为 ensemble 预测测试集
  3. 计算所有 foreground classes 上的平均 Dice 形成单个评分
  4. 自动选择最佳单模型或最佳两模型 ensemble
  5. 对候选结果尝试 connected-component postprocessing，若验证集变好则启用
- 页码：`p.4-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 配置 | 适用场景 | 核心特点 | 主要局限 | 论文判断 |
|------|---------|---------|---------|---------|
| `2D U-Net` | 强各向异性数据、按 slice 建模更稳的场景 | full-resolution 逐切片训练，保留高平面内分辨率 | 缺少跨切片 3D 上下文 | 对 anisotropic 数据常是强候选 |
| `3D full resolution U-Net` | 大多数 3D 医学分割任务 | 通常整体表现最好 | patch size 受显存限制，超大体积时上下文可能不足 | `overall the best performing configuration` |
| `3D U-Net cascade` | 大体积、单个 fullres patch 覆盖上下文不够 | low-res 粗分割 + fullres 细化 | 训练和推理更复杂，未必总是需要 | 仅在大数据/上下文不足时启用 |

补充的固定设计原则：

| 项 | 论文默认做法 | 页码 |
|----|-------------|------|
| 基本 block | `conv - IN - lReLU` | `p.3-p.4` |
| 每个 stage block 数 | `2` | `p.3-p.4` |
| 下采样 | `stride conv` | `p.3-p.4` |
| 上采样 | `transpose conv` | `Supplementary p.37-p.38` |
| 深监督 | `除最低两层外加入 auxiliary outputs` | `Supplementary p.38` |
| patch 配置原则 | `在 batch >= 2 前提下尽可能大` | `p.5` |

说明：

- 和 `U-Net_2015` 最大不同不在某个结构块，而在于把整套 pipeline configuration 明确化、自动化、可迁移化

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L_total = 0.5 * (L_Dice + L_CE)
```

符号说明：

- `L_Dice`：Dice loss
- `L_CE`：cross-entropy loss
- 含义：论文文字明确说明两项 loss 采用简单平均，以提升训练稳定性和分割精度
- 说明：`这是按论文文字描述整理出的复现写法，原文此处不是以编号公式给出`
- 页码：`p.4`

公式 2：

```text
stride_inference = patch_size / 2
```

符号说明：

- `patch_size`：训练与推理共用的输入 patch 尺寸
- `stride_inference`：滑窗推理时相邻 patch 的位移
- 含义：相邻预测窗口重叠 50%，以减轻拼接缝伪影
- 说明：`原文为规则描述，不是正式编号公式`
- 页码：`p.4`

### 4.2 推导过程或梯度行为

- 类别极度不平衡时，Dice loss 直接对齐 segmentation metric，但 patch-based training 下它只是近似全局 Dice
- 单独 Dice loss 在实践中不够稳定；再叠加 CE 后稳定性更好，因此论文采用简单平均
- patch 越大，上下文越足，但 batch 过小会导致优化不稳，因此 nnU-Net 把 `patch 大` 与 `batch >= 2` 作为联动约束
- 这篇论文更强调“规则与经验设计的因果逻辑”，不是数学推导型论文

对应页码：

- `p.4-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 监督项 | 作用 | 页码 |
|-------|------|------|
| `Dice loss` | 直接应对 class imbalance，优化 overlap 表现 | `p.4` |
| `Cross-entropy loss` | 提升训练稳定性，补足 Dice 的优化缺陷 | `p.4` |
| `Deep supervision auxiliary losses` | 在 decoder 多尺度输出上提供额外监督 | `Supplementary p.38` |

### 5.2 总损失公式

- 主分割损失：`Dice + Cross-Entropy` 简单平均
- 深监督：`decoder 多个输出分支都参与监督，但最低两层分辨率不加 auxiliary output`
- 原文没有在主文里展开详细权重公式，偏向经验型设计说明

### 5.3 权重配置与调度策略

- `Dice` 与 `CE`：简单平均，没有复杂手工权重搜索
- 深监督具体权重：主文未细写，需进一步看开源实现或 online methods
- 论文强调：比起堆复杂 loss 设计，先把 sampling、patch、augmentation、inference 协议配好更关键

---

## 6. 训练协议

### 6.1 数据集与划分

- 主文与补充材料覆盖 `23` 个公开 biomedical segmentation datasets / challenge datasets，其中核心展示包括 `Medical Segmentation Decathlon` 的 `10` 个任务
- 模型选择基于 `5-fold cross-validation`
- 测试集预测时，使用各 fold 模型聚合形成 ensemble
- 论文核心卖点之一：`without manual intervention` 应用于多个任务，而不是只在单一数据集调优

### 6.2 数据增强

- spatial augmentation 是必须项，论文明确说缺少充分增强会导致性能下降
- 对 3D patch 做旋转、缩放、低分辨率模拟等增强
- 若 patch 强各向异性，则相关 spatial augmentation 会退化到 2D 方式，避免跨层插值伪影
- 还包括 Gaussian noise、Gaussian blur、brightness / contrast、gamma 等常规强度增强
- foreground oversampling 用于缓解 rare classes 被忽略的问题

### 6.3 优化器与超参数

| 项目 | 数值/策略 | 页码 |
|------|-----------|------|
| optimizer | `SGD` | `p.3-p.4` |
| 初始学习率 | `0.01` | `p.3-p.4` |
| momentum | `Nesterov 0.99` | `p.3-p.4` |
| lr schedule | `polyLR` | `p.3-p.4` |
| 训练总长度 | `1000 epochs` | `p.3-p.4` |
| 每个 epoch | `250 iterations` | `p.3-p.4` |
| batch size 原则 | `minimum 2` | `p.5` |
| GPU memory 预算 | `11 GB` 默认配置 | `Supplementary p.65` |

论文原话要点：

- `shorter trainings than this default empirically result in diminished segmentation performance`
- `patch size should be as large as possible while still allowing a batch size of 2`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；本文主要面向通用 biomedical segmentation，不局限病理 RGB`
- 颜色空间转换：`不固定，依任务模态而定`
- resize / crop / pad 策略：
  - 按 target spacing 做 resampling
  - 若 patch 超出图像边界则自动 padding
- patch overlap：`推理时 stride = patch_size / 2`
- 背景过滤策略：`foreground oversampling；CT normalization 用 foreground voxels 统计`
- 标签生成方式：`原始 segmentation masks`
- 类别不平衡处理：
  - `foreground oversampling`
  - `Dice + CE`
- 随机种子/重复次数：`主文未强调固定随机种子；模型层面用 5-fold CV`
- 数据泄漏风险点：
  - 若划分不严格，cross-validation 可能把同患者或强相关样本拆到不同 fold
  - 论文在若干 challenge 设置中会强调按 patient stratification 组织 fold

更细的规则：

- isotropic 数据：target spacing 常取 training cases 的 median spacing
- anisotropic 数据：低分辨率轴常按更保守的 percentile 规则处理，高分辨率轴按 median
- CT 图像：会基于 foreground voxels 统计裁剪到 `0.5 / 99.5 percentile`，再做全局 mean/std normalization
- 非 CT 图像：通常每个 case 独立做 z-score normalization

---

## 7. 推理与后处理

- 推理方式：`patch-based inference`
- patch 尺寸：`与训练时相同`
- 相邻 patch 步长：`patch_size / 2`
- 聚合方式：`Gaussian importance weighting`，中心 voxel 权重更高，边缘更低
- fully convolutional inference：`论文不推荐`，因为会带来 zero-padding 与 normalization 相关问题
- 模型集成：`5 个 fold 模型组成 ensemble`，也会比较不同配置间的最佳两模型 ensemble
- 后处理：`connected component analysis`，若验证集上删除非最大连通域能提升 Dice，则按类别启用

---

## 8. 消融实验

### 8.1 消融设计

- 论文的“消融”更偏向 design principle analysis，而不是单模块删改竞赛
- 主要比较维度：
  - `2D vs 3D full resolution vs 3D cascade`
  - `single model vs ensemble`
  - `with / without postprocessing`
  - `默认设计 vs 去掉 deep supervision / 改 ReLU / 改上采样方式`

### 8.2 各模块贡献量化

- `ACDC`：
  - `2D U-Net`：`0.9165`
  - `3D full resolution`：`0.9181`
  - `ensemble of the two`：`0.9228`
  - 说明：`ensemble` 优于单个配置
- `LiTS`：
  - `2D U-Net`：`0.7625`
  - `3D full resolution`：`0.8044`
  - `3D low resolution`：`0.7796`
  - `full resolution 3D U-Net of cascade`：`0.8017`
  - `best combination of two models`：`0.8111`
  - 说明：大体积数据下 `cascade / ensemble` 更有价值
- 额外分析：
  - 去掉 `deep supervision` 会带来轻微性能下降
  - 把 `transpose conv` 换成三线性上采样也会有下降

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 场景 | 结果 | 页码 |
|------|------|------|
| `Medical Segmentation Decathlon` 开放榜单 | `再次获得 first rank` | `Supplementary p.38-p.39` |
| `ACDC` | `best ensemble = 0.9228` | `Supplementary p.30-p.31` |
| `LiTS` | `best combination = 0.8111`（平均标量） | `Supplementary p.32-p.34` |
| 多数据集整体结论 | `在 23 个公开数据集上超过多数专门设计方法` | `Abstract / p.1-p.2` |

### 9.2 与其他方法的对比

- 和很多“专为某数据集定制”的方法相比，`nnU-Net` 的优势是：不靠人工定制，也能达到很强结果
- 和单纯比较 `U-Net / UNet++ / Attention U-Net` 这类结构论文相比，`nnU-Net` 把“公平 baseline 到底应该怎么配”这件事说清楚了
- 它的论点不是“结构创新不重要”，而是“如果 baseline protocol 没标准化，就很难知道新结构增益是真是假”
- 对我们项目更重要的是：
  - 它可以作为 `U-Net family` 的强工程上限参考
  - 它能校准 patch、大图滑窗、后处理、loss、训练长度这些是否设置充分

### 9.3 公平对比条件确认

- 优势：
  - 多任务、跨数据集验证
  - 自动配置，减少人工调参偏置
  - 明确使用 cross-validation 选择模型和后处理
- 需要注意：
  - 不同任务的最终配置并不相同，因此它更像“自配置系统”而不是单一固定网络
  - 和我们腺体病理 2D RGB patch 任务比时，不能直接把 3D 配置原样照搬

### 9.4 评价协议与指标定义

- 主指标：`Dice score`
- 模型选择：`平均 foreground Dice`，跨所有 foreground classes 与 cases 聚合成单一标量
- challenge test set：通常由在线平台评估，因此个别 test 指标只保留有限有效数字
- postprocessing 触发条件：若某类别在验证集 Dice 因去除非最大连通域而提升，则对该类别启用

---

## 10. 计算量与效率

- 论文没有像分类 backbone 论文那样统一报告 FLOPs 主表
- 它更关注在固定硬件预算下自动确定可行 patch / batch / depth / pooling 结构
- 默认面向 `11 GB` GPU 预算配置
- 效率取舍的核心规则：
  - 优先保证 `patch 尽可能大`
  - 其次确保 `batch >= 2`
  - 若 patch 太小导致上下文不足，再考虑 `3D lowres + cascade`
- 对我们项目的现实意义：
  - 与其盲目堆更复杂模块，不如先在显存预算下把 `input size / overlap / batch / infer` 配到合理上限

---

## 13. 开源与复现

- 开源情况：`是`
- 官方代码：`MIC-DKFZ/nnUNet`
- 复现难度：`中`
- 难点不在核心网络，而在于：
  - 数据 fingerprint 提取
  - target spacing / patch / batch 联动规则
  - five-fold 训练与 ensemble
  - 自动 postprocessing 决策

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否（主文未强调）` | `如果后续自己实现，需显式固定 seed` | `中` |
| 验证集划分 | `是（5-fold CV）` | `保留五折；病理任务需 patient-level 划分` | `高` |
| 推理阈值 | `部分` | `语义分割通常 argmax；具体实现仍需核对代码` | `中` |
| 后处理细节 | `部分` | `先按 largest connected component on validation 改善为准` | `中` |
| 训练轮数停止准则 | `是（固定 1000 epochs）` | `优先照此作为强 baseline 训练上限参考` | `低` |
| 数据预处理 | `是（原则明确）` | `病理 RGB 需映射成对应的 stain / resize / patch 规则` | `高` |
| deep supervision 权重 | `否（主文未细写）` | `后续结合源码核对` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 不是所有任务都由单一配置获胜，仍需在 `2D / 3D fullres / cascade / ensemble` 间做经验选择
- patch 受 GPU memory 限制，超大体积数据中 full-resolution patch 可能上下文不足
- 方法依赖监督数据，不解决 annotation scarcity 本身

### 14.2 我们观察到的潜在问题

- 这篇论文主要针对医学影像通用语义分割，病理 RGB 腺体实例边界问题并不是它的主战场
- `largest connected component` 的后处理假设在多实例腺体任务里往往不成立，不能直接用
- 病理图像的 stain variation、tile overlap、实例分离需求，比文中大多数 CT/MRI 任务更特殊

### 14.3 失败案例 / 定性分析

- 对于大图像、上下文需求高的任务，如果 full-resolution patch 太小，会出现“看得太近”的误判，这正是 cascade 设计的动机
- 对实例分割或边界敏感任务，单纯语义 mask 的后处理未必足够
- 对我们任务来说，它更像 `strong semantic baseline protocol`，不是直接可用的实例级最终方案

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `baseline 先把训练协议配够` 这一思想
- `patch-based inference + overlap + Gaussian weighting`
- `Dice + CE` 作为稳定基础损失
- `patient-level / case-level` 的严格验证观念

### 15.2 可以作为候选参数来源的

- `1000 epochs` 作为“是否训够”的上界参考
- `SGD(lr=0.01, Nesterov=0.99) + polyLR` 作为可试的强基线训练方案
- `patch 尽可能大且 batch 至少为 2` 的资源分配原则
- `5-fold CV + ensemble` 作为最终严谨评估参考

### 15.3 不应照搬的（及原因）

- `3D full resolution / 3D cascade`：我们当前主线是 2D 病理腺体图像，不适合直接照搬
- `largest connected component`：腺体是多实例目标，直接保留最大连通域会破坏任务定义
- `CT foreground intensity clipping`：病理 RGB 不适用，需要单独设计 stain / color 预处理

### 15.4 对我们具体模块的支撑

- 对 `U-Net` 主线：
  - 支撑“先把 baseline 训公平、训充分”而不是过早叠模块
- 对 `ResNet34-U-Net` 主线：
  - 提醒 backbone 改动之外，实验 protocol 一样会大幅影响结果
- 对 `边界/损失` 主线：
  - 可把 `Dice + CE` 作为区域基线，再叠加后续 boundary / shape loss
- 对 `实验执行`：
  - 可以直接反向约束我们的 `patch / overlap / aug / infer / postprocess / cv` 表格设计

### 15.5 后续行动项

- 把 `nnU-Net` 的协议思想回填到 `01_实验执行` 里的 baseline 训练规范
- 为腺体 2D 任务单独写出一个“病理版 nnU-Net 化”配置表
- 后续若做公平对比，可考虑：
  - `U-Net`
  - `ResNet34-U-Net`
  - `UNet++`
  - `Attention U-Net`
  - 再用 `nnU-Net philosophy` 校准训练与推理

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | “pipeline 配置同样决定性能”的核心论点 | 用来解释为什么我们重视公平基线与实验协议 |
| related work | 自动配置 U-Net、强基线方法学 | 放在 `U-Net family` 与 `AutoML / strong baseline` 之间 |
| 方法 | 训练与推理协议设计依据 | 作为实验设计依据，不夸大成“完全复现 nnU-Net” |
| 实验设置 | epoch、optimizer、loss、patch inference、CV、postprocess 依据 | 可直接转成实验表格 |
| 讨论 | 为什么有时工程配置收益大于复杂模块收益 | 用于解释结果波动和公平对比 |

---

## 16. 关键图表索引

| 图/表 | 内容 | 用途 |
|------|------|------|
| `p.3-p.5` | design principles：fixed / rule-based / empirical parameters | 写方法思想、实验规范来源 |
| `Supplementary Figure SN3.1` | ACDC 自动生成 pipeline 示例 | 说明 2D 与 3D fullres 如何自动配置 |
| `Supplementary Figure SN3.2` | LiTS 自动生成 pipeline 示例 | 说明为何需要 cascade |
| `Supplementary Table SN6.2` | ACDC 结果表 | 引用 ensemble 提升 |
| `Supplementary Table SN6.6` | LiTS 结果表 | 引用 large-volume 场景下 cascade / ensemble 收益 |
| `Supplementary Figure 6.2` | 由 stride / kernel 配置还原网络结构 | 对接代码实现时参考 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（优化器+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查（normalization / patch overlap / target spacing / CV）
- [x] 结果数字与原文 table 一致（已核对关键示例）
- [x] 指标定义和评价协议已确认（不是只记指标名字）
- [x] 消融实验的结论已量化（不只是“有效”）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[需结合源码进一步确认]` 或说明来源
