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

- `topology-aware gland instance segmentation`
- `multitask learning with MA distance map`
- `watershed-based clustered gland separation`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是近年的腺体任务代表方法，核心是用拓扑骨架而不是 contour 来分离黏连腺体
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`TA-Net: Topology-Aware Network for Gland Segmentation`
- 作者/团队：`Haotian Wang, Min Xian, Aleksandar Vakanski`
- 发表年份/会议/期刊：`2022, IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)`
- DOI / arXiv ID：`10.1109/WACV51458.2022.00330`; `arXiv:2110.14593`
- BibTeX key：`wang2022tanet`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/TA-Net_Topology-Aware_Network_for_Gland_Segmentation_2022.pdf`
- 当前定位：`05` 目录里很重要的“拓扑先验”路线论文，直接对应我们后续是否需要 topology-aware 监督或 skeleton/marker 约束
- 与已提取论文的关系：
  - 继承 `DCAN`、`MILD-Net` 等多任务 instance 分割路线，但明确批评 contour-based separation 在密集黏连腺体上效果有限
  - 与 [04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/04_MILD-Net.md) 互补：后者偏 contour + uncertainty，本篇偏 topology + watershed markers
  - 与 [06_Object-Graphs.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/06_Object-Graphs.md) 在“结构先验”层面相呼应，但 TA-Net 用深度学习学习拓扑骨架

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：contour-based gland separation 在 densely clustered glands 上存在天然缺陷，因为重叠或相邻腺体会共享 contour 段，而且恶性腺体边界本就不规则。
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：gland topology 可用 topological skeleton 表征，相比 contour 对噪声标注更稳，也更适合分离密集簇状腺体。
  - 用途：`方法动机`
  - 页码：`p.2-p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：TA-Net 将 gland instance segmentation 与 gland topology estimation 作为两个任务共享表示学习，并通过 topology loss 逼迫分割结果遵循真实腺体拓扑。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.3-p.4`
- 句子/事实 2：作者明确指出 MA distance map 相比 contour map、Euclidean distance 和 Chessboard distance 更适合 clustered gland separation。
  - 用途：`拓扑监督动机`
  - 页码：`p.5-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| GlaS patch size | `512 x 512` | 实验设置 | `p.5` |
| CRAG patch size | `768 x 768` | 实验设置 | `p.5` |
| GlaS patches | `340 train / 320 test` | 实验设置 | `p.5` |
| CRAG patches | `692 train / 160 test` | 实验设置 | `p.5` |
| 优化器 | `Adam` | 实验设置 | `p.5` |
| 初始学习率 | `1e-4` | 实验设置 | `p.5` |
| 学习率衰减后 | `1e-5 after 100 epochs` | 实验设置 | `p.5` |
| epoch | `200` | 实验设置 | `p.5` |
| batch size | `4` | 实验设置 | `p.5` |
| GlaS 主结果 | `F1 90.5 / Obj-D 90.2 / Obj-H 50.8` | 主表结果 | `p.6` |
| CRAG 主结果 | `F1 84.2 / Obj-D 89.3 / Obj-H 105.2` | 主表结果 | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 现有 contour-based 方法在 densely clustered glands 上很难正确分开相邻腺体，因为相邻腺体会共享或缺失清晰边界。
- contour annotation 本身较粗糙，标注噪声会削弱 contour supervision 的有效性。
- malignant glands 的边界严重变形，局部纹理和颜色信息不可靠。
- 需要一种比 contour 更稳定的结构表征来指导 instance 分割。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- TA-Net 采用 `encoder + two decoders` 的多任务结构，一支输出 gland instance 前景图，另一支输出 gland 的 `Medial Axis (MA) distance map` 作为 topology 表征。训练时总损失由 instance CE loss 和 topology loss 组成，后者又包含 MA distance regression 和 marker Dice loss。推理时将 instance 分支输出作为 watershed 的 filling region，将 MA 分支输出经过阈值化后生成 marker 和 elevation，再结合形态学处理与 watershed 得到最终 instance segmentation。

关键页码：

- `p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`multitask encoder-decoder`
- Backbone：`SegNet encoder + two decoders with densely-connected blocks`
- 输入尺寸：`GlaS 512x512 patch / CRAG 768x768 patch`
- 输出头：
  - `INST`：gland foreground map
  - `TOP`：MA distance map

### 3.2 关键模块详细描述

**模块 1：`Shared Encoder`**

- 位置：`网络主干`
- 操作流程：
  1. 使用 `SegNet` 作为 backbone encoder
  2. 共 `5` 个 downsampling blocks
  3. 每个 block 由卷积层和 max-pooling 组成
  4. 前两个 downsampling blocks 使用 `3` 个卷积层以提取更多基础特征
- 页码：`p.3-p.4`

**模块 2：`Dual Decoder Branches`**

- 位置：`共享编码器之后`
- 操作流程：
  1. 两个 decoder 共享 encoder 特征
  2. `INST decoder` 输出 gland 前景二分类图
  3. `TOP decoder` 输出 MA distance map
  4. decoder 中使用 densely-connected blocks 以扩大 receptive field
  5. 两个 decoder 结构相同，仅最后输出层不同
- 页码：`p.3-p.4`

**模块 3：`MA Distance Map Supervision`**

- 位置：`topology branch`
- 操作流程：
  1. 对每个 gland mask 进行 MA transformation
  2. 得到一像素宽 skeleton
  3. 统计从 contour 到 skeleton 的 erosion iterations
  4. 在 gland 内归一化得到 MA distance map
  5. 以该图作为拓扑 branch 的监督信号
- 页码：`p.4-p.5`

**模块 4：`Topology Loss`**

- 位置：`训练目标`
- 操作流程：
  1. 用 `LMA` 约束预测 distance map 与真值 MA map 一致
  2. 由预测 MA map 阈值化得到 predicted markers
  3. 用 `LMC` 比较 predicted marker map 与 true marker map
  4. 通过 MA + marker 两部分联合抑制 over-/under-segmentation
- 页码：`p.4-p.5`

**模块 5：`Watershed Post-processing`**

- 位置：`推理后处理`
- 操作流程：
  1. 对 `INST` 输出阈值化，生成 gland binary map
  2. 把 `TOP` 输出视为局部 elevation
  3. 对 `TOP` 阈值化，生成 watershed markers
  4. 用 fill holes / remove small objects 等 morphology 操作细化 gland region 和 markers
  5. 将 region、elevation 和 markers 输入 watershed，得到最终实例分割
- 页码：`p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Encoder block 1-5 | conv + pool | `64, 128, 256, 512, 512` | 逐级下采样 | SegNet 风格 |
| INST decoder | upsampling + dense blocks | `512, 512, 256, 128, 64` | 逐级恢复 | 输出 foreground map |
| TOP decoder | upsampling + dense blocks | `512, 512, 256, 128, 64` | 逐级恢复 | 输出 MA distance map |
| INST output | `2x2 conv + softmax` | `2 classes` | patch 尺寸 | gland / background |
| TOP output | `1x1 conv` | `1 channel` | patch 尺寸 | MA distance regression |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L_TA-Net = L_INST + alpha * L_TOP
```

符号说明：
- `L_INST`：instance segmentation 的交叉熵损失
- `L_TOP`：topology loss
- `alpha`：topology loss 权重
- 页码：`Eq.(1), p.4`

公式 2：

```text
L_TOP = L_MA + L_MC
```

符号说明：
- `L_MA`：MA distance map 回归损失
- `L_MC`：marker loss
- 页码：`Eq.(2), p.4`

公式 3：

```text
MA(p_j) =
  ( d(p_j) / (max_{p_k in G_i} d(p_k) - min_{p_k in G_i} d(p_k)) ), if p_j in G_i
  0, otherwise
```

符号说明：
- `G = {G_i}`：图像中的 gland 集合
- `d(p_j)`：点 `p_j` 从 contour 到 skeleton 的 erosion iteration 次数
- 该式把局部几何厚度和 skeleton 拓扑编码进 distance map
- 页码：`Eq.(3), p.4-p.5`

公式 4：

```text
L_MA = (1/m) * sum_{j=1..m} ( MA(p_j) - dMA(p_j) )^2
```

符号说明：
- `dMA`：预测的 MA distance map
- `m`：图像像素数
- 页码：`Eq.(4), p.5`

公式 5：

```text
L_MC = Dice(MC, dMC)
```

符号说明：
- `MC`：真实 marker map
- `dMC`：预测 marker map
- marker 通过阈值化 MA 输出获得
- 页码：`Eq.(5), p.5`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是纯损失论文，但其核心思想是把 contour supervision 替换为更稳的 topology supervision。
- `L_MA` 负责约束 gland 几何和 skeleton，`L_MC` 负责约束实例数和分离位置，避免 watershed 时的 over-/under-segmentation。
- 页码：`p.4-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `L_INST` | cross-entropy | gland foreground segmentation | INST decoder |
| `L_MA` | MSE | MA distance regression | TOP decoder |
| `L_MC` | Dice loss | marker detection | TOP decoder / post-threshold marker |

### 5.2 总损失公式

```text
L_TA-Net = L_INST + alpha * (L_MA + L_MC)
```

### 5.3 权重配置与调度策略

- 各项权重：
  - `alpha`：用于控制 `L_TOP` 贡献
- 是否衰减/动态调整：
  - `正文未给出 alpha 具体数值和动态调度`
- 页码：`p.4`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `85 images / 340 train patches` | `80 images / 320 test patches` | `未单设 val` | `Test A 60, Test B 20` |
| `CRAG` | `173 images / 692 train patches` | `40 images / 160 test patches` | `未单设 val` | `213 images from 38 WSI` |

### 6.2 数据增强

- 增强列表：
  - `random flip`
  - `random rotation`
  - `Gaussian blur`
  - `median blur`
- Patch 提取策略：
  - `GlaS: 512 x 512`
  - `CRAG: 768 x 768`
- 页码：`p.5`

### 6.3 优化器与超参数

- 框架：`正文未明确写 PyTorch/TensorFlow`
- 优化器：`Adam`
- 初始学习率：`1e-4`
- 学习率调度：`100 epochs 后降到 1e-5`
- Batch size：`4`
- Epoch / Steps：`200 epochs`
- 权重初始化：`未说明`
- 预训练策略：`未说明`
- 是否冻结部分层：`否`
- 设备：`NVIDIA Quadro RTX 8000, 512 GB RAM, two 2.4 GHz Intel Xeon 4210R CPUs`
- 页码：`p.5`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未说明 stain normalization`
- 颜色空间转换：`默认 RGB patch 输入`
- resize / crop / pad 策略：`直接按 patch size 切分并在推理后 merge 回原图`
- patch overlap：`未明确`
- 背景过滤策略：`无特别说明`
- 标签生成方式：`instance-level gland labels -> MA distance map / marker map`
- 类别不平衡处理：`未说明`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`未报告独立 val；GlaS 主结果是 Test A/B 平均值，需要与官方 protocol 对齐使用`
- 页码：`p.5-p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：
  - `GlaS 512x512`
  - `CRAG 768x768`
- 概率阈值：`文中说明对 INST 和 MA 输出进行 thresholding，但未给具体阈值`
- 后处理步骤：
  1. 对 `INST` 输出阈值化，得到 gland binary map
  2. 对 `MA` 输出阈值化，得到 watershed markers
  3. 用 morphology 操作填洞、移除小目标
  4. 将 gland region、elevation、markers 输入 watershed
  5. merge patch 结果形成原图大小输出
- TTA / Test-time refinement：`无`
- 页码：`p.5`

---

## 8. 消融实验

### 8.1 消融设计

> 本篇消融较完整，围绕四件事展开：`multitask vs single-task`、`MA map vs contour map`、`with/without marker loss`、`不同 distance metrics`。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | `TA-Net` vs `Ours-CNT` | GlaS/CRAG 上 TA-Net 的 Obj-H 更低 | MA map 比 contour map 更适合黏连腺体分离 |
| 2 | `TA-Net` vs `Ours-INST` / `Ours-MA` | multitask 明显优于单任务 | instance + topology 共享表示有效 |
| 3 | 去掉 marker loss (`Ours-WoM`) | 指标略降 | marker loss 定量增益小，但定性改善 over-/under-segmentation |
| 4 | MA / Euclidean / Chessboard 距离 | MA 最优 | MA distance 最能保留 gland topology |

### 8.2 各模块贡献量化

- `TA-Net` 相比 `Ours-CNT`：
  - `GlaS Obj-H: 54.4 -> 50.8`
  - `CRAG Obj-H: 164.5 -> 105.2`
- `TA-Net` 相比 `Ours-INST`：
  - `GlaS F1: 86.4 -> 90.5`
  - `CRAG F1: 78.9 -> 84.2`
- marker loss 增益：
  - `GlaS Obj-H: 54.4 -> 50.8`
  - `CRAG Obj-H: 108.6 -> 105.2`
- distance metric 对比：
  - `GlaS Obj-H: Euclidean 65.4 / Chessboard 71.2 / MA 54.4`
  - `CRAG Obj-H: Euclidean 257.5 / Chessboard 178.9 / MA 108.6`
- 页码：`Table 2-4, p.6-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS` | `F1 90.5` | `Obj-D 90.2` | `Obj-H 50.8` | `TA-Net` |
| `CRAG` | `F1 84.2` | `Obj-D 89.3` | `Obj-H 105.2` | `TA-Net` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `TA-Net` | `GlaS` | `90.5` | `90.2` | `50.8` |
| `Yan et al. 2020` | `GlaS` | `90.7` | `89.3` | `58.7` |
| `MSFCN` | `GlaS` | `89.3` | `89.9` | `53.1` |
| `TA-Net` | `CRAG` | `84.2` | `89.3` | `105.2` |
| `DSE` | `CRAG` | `83.5` | `88.9` | `120.1` |
| `MILD-Net` | `CRAG` | `82.5` | `87.5` | `160.1` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否`
- 是否统一数据增强：`否，表中大多为原文结果`
- 是否统一后处理：`否`
- 是否统一输入尺寸：`否`
- 结果来源：`SegNet / DeepLab / DCAN 为作者复现，其余多来自原文引用`
- 页码：`p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：
  - `GlaS: 85 train / Test A 60 / Test B 20`
  - `CRAG: 173 train / 40 test`
- 结果汇报层级：
  - `GlaS`：`Test A/B 平均`
  - `CRAG`：test
- 实例匹配规则：`F1 中 overlap > 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`object-level Hausdorff`
- F1 类型：`instance/detection F1`
- 是否含后处理后再报结果：`是，含 watershed 与 morphology`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`GlaS 指标定义对齐 challenge，但主表汇总为 Test A/B 平均`
- 页码：`p.5-p.6`

---

## 10. 计算量与效率

- 参数量（Params）：`未报告`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`未报告`
- 输入尺寸（计算量对应的）：
  - `GlaS 512x512`
  - `CRAG 768x768`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `TA-Net` | `N/A` | `N/A` | `N/A` |

- 页码：`正文未给效率表`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但明确将已有腺体分割路线分为：
  - `传统 morphology / graph-based methods`
  - `contour-based deep multitask methods`
  - `topology-aware method (本文)`

### 11.2 论文指出的研究空白 / Open Problems

1. contour 在 clustered glands 上信息不足，且标注噪声较大。
2. malignant glands 的不规则边界会削弱 contour supervision。
3. 需要比 contour 更稳定、可迁移到 irregular shapes 的 topology representation。

### 11.3 对我们选题的启示

- 如果我们后续想做 boundary 之外的结构先验，TA-Net 是最直接的腺体任务内证据，尤其适合支撑 `skeleton/marker/topology` 类辅助监督。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但明确指出 gland morphology 与 colon / breast / prostate cancer stage 判断相关。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 自动、精确分割 gland 是后续 morphology quantification 的前置步骤，可辅助病理医生降低耗时与主观误差。
- 页码：`p.1`

---

## 13. 开源与复现

- 代码是否开源：`正文未明确提供`
- 代码仓库地址：`未在论文正文中给出`
- 框架/语言：`未说明`
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中`
- 复现障碍：
  - `alpha` 权重未在当前正文片段明确给出
  - INST / MA 阈值和 morphology 参数未写全
  - dense-connected blocks 的完整层级堆叠细节描述略模糊

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集划分 | 否 | 仅记录 train/test 协议 | 中 |
| 推理阈值 | 否 | 只记录存在 thresholding，不脑补数值 | 高 |
| 后处理细节 | 部分 | 记录 watershed + fill holes + remove small objects | 中 |
| 训练轮数停止准则 | 是 | `200 epochs` | 低 |
| 数据预处理 | 部分 | 记录 patch 切分与 augmentation | 中 |

- 不确定但影响较大的点：
  - `alpha` 的具体数值
  - MA/marker threshold 的具体设置
  - dense-connected layers 的精确堆叠配置

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- marker loss 的定量提升有限，虽然定性上可缓解 over-/under-segmentation。
- GlaS 上提升幅度不算特别大，因为其 densely clustered gland 较少。
- 作者后续计划把方法扩展到 nuclei segmentation 等任务。
- 页码：`p.6-p.7`

### 14.2 我们观察到的潜在问题

- 方法最终仍依赖 watershed 和 morphology 后处理，不是纯 end-to-end instance segmentation。
- 主张 contour 不稳，但自身依赖 MA map 阈值和 marker 生成，同样存在一定后处理超参数敏感性。
- 论文没有给效率指标，难以评估 topology 分支与后处理的额外代价。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是，以 clustered glands 对比图展示 DCAN / contour-based 方法失败场景`
- 典型失败场景：
  - contour-based 方法在密集黏连腺体上不能正确分离
  - 无 marker loss 时更容易 over-/under-segmentation
- 页码：`Fig. 2, Fig. 6, Fig. 7`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `instance + topology` 双任务思路
- `MA distance map + marker map` 作为替代 contour supervision 的路线
- `watershed markers` 由学习到的 distance map 生成的思路
- `GlaS + CRAG` 双数据集 protocol 与 `F1 / Obj-D / Obj-H` 指标组合

### 15.2 可以作为候选参数来源的

- `GlaS patch 512x512`
- `CRAG patch 768x768`
- `Adam, 1e-4 -> 1e-5, 200 epochs, batch size 4`
- `5-stage SegNet encoder`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其 watershed 后处理为唯一分离方案
  - 原因：我们需要考虑与主线模型的端到端性和推理复杂度
- 不应把所有 boundary supervision 都替换成 topology supervision
  - 原因：本篇证明 topology 有效，但不等于 contour 完全无价值，二者可能互补

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 拓扑辅助监督 | MA distance + marker loss 能改善 clustered glands 分离 | 强 |
| 多任务解码 | instance 与 topology 共享表示优于单任务 | 强 |
| 后处理讨论 | learned markers + watershed 是一条有效分离路线 | 中 |
| related work 论证 | contour-only 在密集黏连腺体上有限 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`拓扑监督备选方案清单`
- [ ] 需要和哪篇论文交叉验证：`04_MILD-Net.md`, `03_DCAN.md`, `08_Deeplab/DEA 等后续方法`
- [ ] 待确认的问题：`我们是否需要尝试 skeleton/marker 辅助分支，而不是只做 contour/boundary`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 黏连腺体难分离、contour 监督局限 | 任务痛点 |
| related work | contour-based 到 topology-aware 的演化 | 方法脉络 |
| 方法 | MA distance map / marker loss 动机 | 作为结构先验来源 |
| 实验设置 | GlaS + CRAG 协议、patch 和指标 | 作为腺体任务内来源 |
| 讨论 | topology supervision 的收益与后处理代价 | 解释边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.2` | clustered glands 分离失败案例 | 问题动机 |
| `Fig. 3` | `p.2` | contour-based 三类问题示意 | 相关工作批评 |
| `Fig. 4` | `p.4` | TA-Net 总体结构图 | 架构参考 |
| `Fig. 5` | `p.4-p.5` | MA transform 与 distance map 示例 | topology 监督说明 |
| `Table 1` | `p.6` | GlaS / CRAG 主结果对比 | 主表引用 |
| `Table 2` | `p.6` | multitask / contour / MA 消融 | 方法有效性 |
| `Table 3` | `p.7` | marker loss 消融 | 后处理监督分析 |
| `Table 4` | `p.7` | distance metric 对比 | MA 优势说明 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（优化器+lr+bs+epoch+augmentation）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
