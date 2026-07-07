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

- `deep multichannel instance segmentation`
- `region + edge + location fusion`
- `post-GlaS classic deep baseline`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是 GlaS 时代的经典深度方法，代表 contour/bbox/location 三线索融合的实例分割路线
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Gland Instance Segmentation Using Deep Multichannel Neural Networks`
- 作者/团队：`Yan Xu, Yang Li, Yipei Wang, Mingyuan Liu, Yubo Fan, Maode Lai, Eric I-Chao Chang`
- 发表年份/会议/期刊：`2017, IEEE Transactions on Biomedical Engineering`
- DOI / arXiv ID：`10.1109/TBME.2017.2686418`; `arXiv:1611.06661`
- BibTeX key：`xu2017multichannel`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Gland_Instance_Segmentation_Using_Deep_Multichannel_Neural_Networks_2017.pdf`
- 当前定位：`05` 目录里介于 `DCAN` 和 `MILD-Net/TA-Net` 之间的重要深度实例分割方法，把 region、edge、location 三类线索并行融合
- 与已提取论文的关系：
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/03_DCAN.md) 同属多任务/边界辅助路线，但本篇额外引入 object detection channel
  - 早于 [04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/04_MILD-Net.md)，后者可视为对本篇 `edge/location` 思路的更现代化替代
  - 与 [07_TA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/07_TA-Net.md) 形成鲜明对照：本篇用 contour + box，TA-Net 改为 topology + markers

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：gland instance segmentation 不仅要把 gland 从背景中分出来，还必须给每个前景像素分配 gland ID，因此仅做前景分割是不够的。
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：在 gland instance recognition 中，即便只错一个像素把两个腺体连在一起，也会导致两个实例被当成一个。
  - 用途：`实例分割难点`
  - 页码：`p.2-p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者把 gland instance segmentation 拆成 `foreground segmentation + instance recognition` 两个子问题，并用 `edge detection + object detection` 近似不可微的实例识别目标。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.4`
- 句子/事实 2：edge information 与 location information 在 gland separation 中是互补的，仅靠其中一类都不如三通道联合。
  - 用途：`边界/定位双线索论证`
  - 页码：`p.5-p.10`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据集 | `MICCAI 2015 GlaS, 165 images` | 实验设置 | `p.7` |
| 划分 | `85 train / 80 test` | 实验设置 | `p.7` |
| 测试细分 | `Test A 60 / Test B 20` | 评价协议 | `p.7-p.8` |
| 分辨率 | `~0.62 um/pixel` | 数据设置 | `p.7` |
| 常见尺寸 | `775 x 522` | 数据设置 | `p.7` |
| crop | `400 x 400` | 训练设置 | `p.7` |
| 策略 I | `flip + rotation(0/90/180/270)` | 数据增强 | `p.7-p.10` |
| 策略 II | `策略 I + elastic transformations` | 数据增强 | `p.7-p.10` |
| weight decay | `0.002` | 训练设置 | `p.7` |
| momentum | `0.9` | 训练设置 | `p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- gland segmentation 只解决前景/背景问题，但 morphology analysis 需要每个 gland instance 被单独识别。
- gland 的异质形状、染色差异和背景噪声使纯形状模型或纯像素分类都不稳定。
- 两个腺体黏连时，即使只有一个像素相连，也会让实例识别完全失败。
- 传统自然图像实例分割先检测再框内分割的套路不适合不规则 gland。

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 论文把 gland instance segmentation 分解为 `foreground segmentation` 和 `instance recognition` 两个子任务，并用三通道深度框架联合建模：foreground segmentation channel 用改造的 FCN 预测 gland 区域，edge detection channel 用 HED 预测 gland 边界，object detection channel 用 Faster R-CNN 提供 gland 位置框；随后用一个浅层 fusion CNN 融合 `region + edge + location` 三类线索，得到最终 instance segmentation 结果。

关键页码：

- `p.4-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`three-channel parallel framework + shallow fusion CNN`
- Backbone：`VGG16-based FCN / HED / Faster R-CNN`
- 输入尺寸：`训练时随机 crop 400 x 400；测试时 FCN 支持任意尺寸输入`
- 输出头：
  - `foreground segmentation`
  - `edge map`
  - `object location map from boxes`
  - `fusion output instance mask`

### 3.2 关键模块详细描述

**模块 1：`Foreground Segmentation Channel`**

- 位置：`region cue branch`
- 操作流程：
  1. 基于 `FCN-32s`
  2. 将 `pool4` 和 `pool5` 的 stride 改为 `1`
  3. 后续卷积采用 dilated convolution 以扩大 receptive field
  4. 输出 gland/background 二分类概率图
- 页码：`p.5-p.6`

**模块 2：`Edge Detection Channel`**

- 位置：`boundary cue branch`
- 操作流程：
  1. 基于 `HED`
  2. 设置 `5` 个 side supervisions
  3. 通过多尺度 side outputs 的加权和得到最终 edge result
  4. 训练时使用 sigmoid cross entropy loss
- 页码：`p.5-p.6`

**模块 3：`Object Detection Channel`**

- 位置：`location cue branch`
- 操作流程：
  1. 基于 `Faster R-CNN`
  2. 检测 gland bounding boxes
  3. 将 bounding box 结果做 filling
  4. 每个像素的值表示它被多少个 box 覆盖
  5. 作为 location feature map 输入 fusion stage
- 页码：`p.6`

**模块 4：`Fusion Network`**

- 位置：`三通道输出之后`
- 操作流程：
  1. 输入 `Ps, Pd, Pe` 三类通道结果
  2. 采用浅层 `7-layer CNN`
  3. 为减少信息损失，使用 dilated convolution 替代 downsampling
  4. 通过交叉验证逐步增加层数和 filters
  5. 输出最终 instance segmentation
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Region branch | modified `FCN-32s` | `2 classes` | `400x400` crop / 任意测试尺寸 | `pool4/pool5 stride=1 + dilated conv` |
| Edge branch | `HED` | `1` | 同输入 | `5 side supervisions` |
| Location branch | `Faster R-CNN` | `box count map` | 同输入 | box filling 表示位置上下文 |
| Fusion stage | `7-layer CNN` | `2 classes` | 同输入 | 融合 region/edge/location |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Dist(Y, Y_hat) = (1 / |Y|) * sum_j delta(y_j != y_hat_j)
```

符号说明：
- `Y`：前景分割真值
- `Y_hat`：前景分割预测
- 该式刻画 foreground labeling/segmentation 子问题
- 页码：`Eq.(3), p.3`

公式 2：

```text
Dist(Z, Z_hat) = 1 - (1 / K) * sum_{k'=0..K'} L(R_hat_{k'}, Z)
```

符号说明：
- `Z`：instance label
- `Z_hat`：instance prediction
- `L`：基于 overlap 阈值的实例匹配函数
- 作者指出该目标不可微，因此用 edge detection 与 object detection 去近似
- 页码：`Eq.(5)-(6), p.3`

公式 3：

```text
P_s(Y* = k | X; w_s) = mu_k(h_s(X, w_s))
```

符号说明：
- `P_s`：foreground segmentation channel 输出
- `mu`：softmax
- `h_s`：隐藏层特征
- 页码：`Eq.(7), p.5`

公式 4：

```text
P_e(E* = 1 | X; w_e, alpha) = sigma( sum_{m=1..M} alpha^(m) * h_e^(m)(X, w_e) )
```

符号说明：
- `P_e`：edge channel 输出
- `alpha^(m)`：第 `m` 个 side supervision 的加权系数
- `h_e^(m)`：第 `m` 个 side output
- 页码：`Eq.(8)-(9), p.6`

公式 5：

```text
P(Y_I* = k | P_s, P_d, P_e; w_f) = mu_k(h_f(P_s, P_d, P_e, w_f))
```

符号说明：
- `P_d`：object detection channel 输出
- `w_f`：fusion network 参数
- `Y_I*`：最终 instance segmentation 预测
- 页码：`Eq.(11), p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是纯损失论文，但方法论上最重要的是把不可微的 instance recognition cost 用两个可学习子任务近似：`edge detection + object detection`。
- 论文明确区分了“前景分割错误少量像素影响较小”与“实例识别少量像素黏连会造成严重错误”这两种代价差异。
- 页码：`p.2-p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| Region loss | softmax cross entropy | gland/background segmentation | FCN branch |
| Edge loss | sigmoid cross entropy | gland boundary detection | HED branch |
| Detection loss | classification + regression loss | gland bounding boxes | Faster R-CNN branch |
| Fusion loss | softmax cross entropy | final instance segmentation | fusion CNN |

### 5.2 总损失公式

```text
本篇没有给出统一总损失加权式；各通道分别训练，再由 fusion 网络学习整合。
```

### 5.3 权重配置与调度策略

- 各项权重：`edge side outputs 有 alpha 加权，但正文未列具体数值`
- 是否衰减/动态调整：`未报告`
- 页码：`p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `85` | `80` | `未单设 val` | `Test A 60 / Test B 20` |

### 6.2 数据增强

- 增强列表：
  - `horizontal flipping`
  - `rotation 0/90/180/270`
  - `pin cushion transformation`
  - `barrel transformation`
- Patch 提取策略：`从原图随机裁 400x400`
- 页码：`p.7`

### 6.3 优化器与超参数

- 框架：`CAFFE`
- 优化器：`SGD-style setup implied by momentum/weight decay`
- 初始学习率：
  - foreground channel：`10^-3`
  - edge channel：`10^-9`
  - object detection channel：`10^-3`
  - fusion：`10^-3`
- 学习率调度：`未明确报告`
- Batch size：`未说明`
- Epoch / Steps：`未说明`
- 权重初始化：
  - foreground：`pretrained FCN32s`
  - edge：`Xavier`
  - detection：`pretrained Faster R-CNN`
  - fusion：`Xavier`
- 预训练策略：`FCN32s / Faster R-CNN 预训练`
- 是否冻结部分层：`未说明`
- 设备：`K40 GPU, CUDA 7.0`
- 页码：`p.7`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`per-channel zero mean`
- 颜色空间转换：`默认 RGB`
- resize / crop / pad 策略：`随机 crop 400x400`
- patch overlap：`未说明`
- 背景过滤策略：`无特别说明`
- 标签生成方式：
  - edge label 由 region label 生成并做 dilation
  - box label 为包围 gland 的最小矩形
- 类别不平衡处理：`edge 像素过少，通过 deep supervision + edge dilation 缓解`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`GlaS 官方 train/test 使用，但文中未单独设验证集`
- 页码：`p.7, p.10-p.11`

---

## 7. 推理与后处理

- 推理时输入尺寸：`FCN 支持任意尺寸；训练 crop 为 400x400`
- 概率阈值：`实例匹配阈值 thre = 0.5`
- 后处理步骤：
  1. 三个通道各自产出 region / edge / location map
  2. fusion CNN 融合三者得到最终 instance mask
  3. 重叠 box 区域归属最近 gland
- TTA / Test-time refinement：`未报告`
- 页码：`p.3, p.6-p.10`

---

## 8. 消融实验

### 8.1 消融设计

> 本篇消融集中在三类：`数据增强策略`、`dilated convolution`、`三通道设计合理性`。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | Strategy I vs Strategy II | FCN/dilated FCN 在三指标上均提升 | elastic augmentation 有效 |
| 2 | FCN vs dilated FCN | dilated FCN 明显优于 FCN | 减少下采样 + 扩大 receptive field 有益 |
| 3 | 去掉 `BOX` 或 `EDGE` | 三通道联合最好 | edge 与 location 互补 |
| 4 | fusion 使用/不使用 dilated conv | DMC 优于 MC | fusion 阶段也需要较大 receptive field 与较少信息损失 |

### 8.2 各模块贡献量化

- 数据增强 `Strategy II` 相比 `Strategy I`：
  - `FCN Part A F1: 0.709 -> 0.788`
  - `dilated FCN Part A F1: 0.820 -> 0.854`
- 三通道消融最佳配置：
  - `DMC: dilated FCN + EDGE3 + BOX`
  - `Part A/B F1: 0.893 / 0.843`
  - `Part A/B ObjDice: 0.908 / 0.833`
  - `Part A/B ObjHaus: 44.129 / 116.821`
- 去掉 object detection：
  - `DMC: dilated FCN + EDGE3`
  - `Part B F1: 0.816`，低于完整模型 `0.843`
- 页码：`Table III-IV, p.10-p.11`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS Test A` | `F1 0.893` | `ObjDice 0.908` | `ObjHaus 44.129` | `Ours` |
| `GlaS Test B` | `F1 0.843` | `ObjDice 0.833` | `ObjHaus 116.821` | `Ours` |
| `Overall rank` | `RS 8` | `WRS 4.5` | `-` | `competition protocol` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Ours` | `Test A/B` | `0.893 / 0.843` | `0.908 / 0.833` | `44.129 / 116.821` |
| `FCN` | `Test A/B` | `0.788 / 0.764` | `0.813 / 0.796` | `95.054 / 146.248` |
| `dilated FCN` | `Test A/B` | `0.854 / 0.798` | `0.879 / 0.825` | `62.216 / 118.734` |
| `CUMedVision2 (DCAN)` | `Test A/B` | `0.912 / 0.716` | `0.897 / 0.781` | `45.418 / 160.347` |
| `ExB3` | `Test A/B` | `0.896 / 0.719` | `0.886 / 0.765` | `57.350 / 159.873` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否`
- 是否统一数据增强：`否`
- 是否统一后处理：`否`
- 是否统一输入尺寸：`否`
- 结果来源：`competition leaderboard + 作者复现实验`
- 页码：`p.8-p.10`

### 9.4 评价协议与指标定义

- 数据划分来源：`MICCAI 2015 GlaS official split`
- 结果汇报层级：`Test A / Test B`
- 实例匹配规则：`F1 中 overlap > 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`object-level Hausdorff`
- F1 类型：`detection F1`
- 是否含后处理后再报结果：`含 fusion 后最终实例结果`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`是，同时额外报告 WRS`
- 页码：`p.7-p.9`

---

## 10. 计算量与效率

- 参数量（Params）：`未报告`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`未报告`
- 输入尺寸（计算量对应的）：`400x400 train crop`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `deep multichannel` | `N/A` | `N/A` | `N/A` |

- 页码：`正文未给效率`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但可从文中归纳三类 gland instance 路线：
  - `传统 morphology / graph-based`
  - `contour-aware multitask segmentation`
  - `region + edge + location multichannel fusion (本文)`

### 11.2 论文指出的研究空白 / Open Problems

1. 仅 foreground segmentation 无法解决 gland ID 分配问题。
2. contour 线索虽然有用，但单独使用仍会被 coalescence 破坏。
3. 自然图像中“先检测再框内分割”的实例分割框架不适合不规则 gland。

### 11.3 对我们选题的启示

- 这篇很适合作为 related work 中“边界与位置双线索融合”的代表，说明 gland 任务比自然图像实例分割更依赖结构先验和上下文。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但明确指出 gland morphology 与 benign/malignant 判别和 severity assessment 相关。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- gland instance segmentation 是 morphology assessment 和 cancer grading 的前置步骤。
- 页码：`p.1-p.2`

---

## 13. 开源与复现

- 代码是否开源：`未在正文中提供`
- 代码仓库地址：`未提供`
- 框架/语言：`CAFFE`
- 预训练权重是否提供：`基于 pretrained FCN32s / Faster R-CNN，但未提供作者权重`
- 复现难度评估：`中-高`
- 复现障碍：
  - 三通道独立训练再 fusion，工程链路较长
  - HED side output 权重 `alpha` 未明确
  - batch size / 训练轮数 / 测试细节未写全

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集划分 | 否 | 仅使用官方 train/test 口径记录 | 中 |
| 推理阈值 | 部分 | 仅记录实例匹配阈值 `0.5` | 中 |
| 后处理细节 | 部分 | 记录 overlapping box 像素归到最近 gland | 中 |
| 训练轮数停止准则 | 否 | 不脑补 epoch | 高 |
| 数据预处理 | 是/部分 | 记录 zero mean、edge dilation、box generation、crop | 低 |

- 不确定但影响较大的点：
  - 各分支的训练 iteration 数
  - HED 中 `alpha` 权重
  - fusion 网络完整层宽配置

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- Test B 明显比 Test A 更难，因为恶性样本更多、形状更复杂、尺寸更大。
- 仍有 broken glands 或特殊白色背景区域会误判。
- 论文指出 natural image cascade instance segmentation 在 gland 任务上存在明显缺陷。
- 页码：`p.9-p.10`

### 14.2 我们观察到的潜在问题

- 虽然三通道有效，但工程复杂度高，且依赖 `Faster R-CNN + HED + FCN + fusion` 四段系统。
- 仍以 contour 和 bounding box 为主线索，对更极端黏连腺体可能不如后来的 topology-aware 方法。
- 没有 CRAG 等更难数据集验证，方法时代局限明显。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是`
- 典型失败场景：
  - white area 可能是 cytoplasm 也可能是 background，容易混淆
  - gland 被切开时，cytoplasm 可能被误判成 background
  - broken glands 会逃逸检测
- 页码：`Fig. 6-7, p.9-p.10`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 把 gland instance segmentation 明确拆成 `foreground + instance recognition`
- `region + edge + location` 三线索互补的论证
- `GlaS` challenge 指标协议与 `WRS` 的补充汇报方式
- 说明 dilated convolution 在 gland 任务里早期就已被用于减少下采样信息损失

### 15.2 可以作为候选参数来源的

- `400x400` crop
- `Strategy II` 增强：flip + rotations + elastic transforms
- `weight decay 0.002`
- `momentum 0.9`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其三模型加一融合网络的工程管线
  - 原因：维护成本高，且现代 encoder-decoder 多任务网络可更简洁地吸收同类思想
- 不应把 box-based location channel 当成唯一实例分割路径
  - 原因：后续腺体论文已显示 contour/topology/skeleton 路线更适配不规则 gland

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界辅助监督 | edge channel 明显改善实例分离 | 强 |
| 多任务融合 | region/edge/location 联合优于单线索 | 强 |
| 大感受野动机 | dilated conv 减少 pooling 信息损失 | 中 |
| related work 写法 | gland 实例分割不同于自然图像 box-first 范式 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`related work 中深度实例分割演化表`
- [ ] 需要和哪篇论文交叉验证：`03_DCAN.md`, `04_MILD-Net.md`, `07_TA-Net.md`
- [ ] 待确认的问题：`我们是否需要保留 location cue，还是改由 topology/skeleton 替代`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland instance segmentation 比普通前景分割更难 | 任务定义 |
| related work | contour/location 多线索融合路线 | 方法脉络 |
| 方法 | edge 与 location 互补动机 | 作为设计参考 |
| 实验设置 | GlaS 指标与排名口径 | 评价协议说明 |
| 讨论 | 三通道复杂但有效，后续方法如何简化它 | 演进分析 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.2` | 三通道简图 | 总体方法说明 |
| `Fig. 3` | `p.3` | foreground vs instance recognition 两子问题 | 任务定义引用 |
| `Fig. 5` | `p.6` | 完整三通道结构图 | 架构参考 |
| `Table I` | `p.8-p.9` | 与 GlaS 参赛/基线方法对比 | 主结果引用 |
| `Table II` | `p.10` | 与 SDS/Hypercolumn/MNC 对比 | 跨领域实例分割比较 |
| `Table III` | `p.10` | 数据增强策略对比 | augmentation 参考 |
| `Table IV` | `p.11` | 通道合理性消融 | 组件贡献分析 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（在论文已报告范围内）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
