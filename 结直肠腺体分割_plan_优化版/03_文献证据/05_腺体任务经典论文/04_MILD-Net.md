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

- `gland-specific segmentation`
- `minimal information loss`
- `uncertainty quantification with RTS`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体任务内兼顾 `GlaS / CRAG / contour / large receptive field / uncertainty` 的关键方法论文
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`MILD-Net: Minimal Information Loss Dilated Network for Gland Instance Segmentation in Colon Histology Images`
- 作者/团队：`Daniel Graham et al.` [待后续如需 BibTeX 可再精确核对作者全表]
- 发表年份/会议/期刊：`2018, Medical Image Analysis`
- DOI / arXiv ID：`正文已抽取，当前以 PDF 正文内容为准，DOI 可后续补齐`
- BibTeX key：`graham2018mild`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/MILD-Net_Minimal_Information_Loss_Dilated_Network_2018.pdf`
- 当前定位：`05` 目录里最重要的腺体方法论文之一，同时提供 `GlaS + CRAG`、对象级指标、边界分支、感受野设计和不确定性量化证据
- 与已提取论文的关系：
  - 继承自 `DCAN`：同样使用 gland / contour 双分支与 auxiliary loss，并明确说明 `lambda` 衰减策略来自 `DCAN`
  - 在 `DCAN` 基础上更强调“减少 max-pooling 信息损失”与 `ASPP + dilated residual`
  - 与 `TA-Net`、`DEA-Net` 互补：前者拓扑更强，后者边界增强更近；本篇更像结构与协议总入口

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：腺体分割难点包括边界精细描绘、腺体大小形态差异大，以及腺体与非腺体结构相似。
  - 用途：`背景 / 痛点`
  - 页码：`p.3`
- 句子/事实 2：常规 `max-pooling` 会丢失对像素级预测很重要的细节信息，这对小腺体、细轮廓和黏连腺体尤其不利。
  - 用途：`方法动机`
  - 页码：`p.4-p.5`

#### 1.1.2 related work 可引用句

- 句子/事实 1：MILD-Net 用 `MIL unit` 在 pooling 后重新注入原图信息，再结合 dilated residual unit 与 ASPP 扩大感受野。
  - 用途：`方法脉络 / 与我们大感受野路线的关系`
  - 页码：`p.4-p.5`
- 句子/事实 2：作者强调 contour 输出在 MILD-Net 里主要用于 uncertainty map refinement，而不是像早期方法那样直接拿来分离实例。
  - 用途：`与 DCAN 的差异`
  - 页码：`p.4-p.5`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| `GlaS` 数据口径 | `85 train / 80 test` | 实验设置 | `p.8-p.9` |
| `CRAG` 数据口径 | `173 train / 40 test` | 实验设置 | `p.8-p.9` |
| patch 提取 | `500 x 500 -> 464 x 464` | 训练设置 | `p.9` |
| 优化器 | `Adam` | 实验设置 | `p.9` |
| 学习率 | `1e-4` | 实验设置 | `p.9` |
| batch size | `2` | 实验设置 | `p.9` |
| GlaS epochs | `30 (60,000 steps)` | 实验设置 | `p.9` |
| CRAG epochs | `75 (200,000 steps)` | 实验设置 | `p.9` |
| 推理阈值 | `0.5` | 后处理 | `p.11-p.12` |
| morphology opening | `disk radius = 5` | 后处理 | `p.11-p.12` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 腺体分割需要较深网络提取高层语义，但普通 `max-pooling` 会丢失对像素级分割至关重要的局部细节。
- gland size 与 morphology 差异大，尤其 malignant cases 中形态异质性更强。
- 小腺体、细边界与相互黏连的腺体容易在下采样后被破坏。
- 除了分割结果本身，临床应用还需要知道模型对预测的确定性。

对应原文依据（页码）：

- `p.3`
- `p.4-p.5`
- `p.6-p.7`

### 2.2 核心思路（一段话概括解法方向）

- MILD-Net 围绕“最小化信息损失”设计：在编码端用 `MIL unit` 把下采样原图重新注入特征提取路径，在深层用 `dilated residual unit` 与 `ASPP` 提升感受野，再通过 U-Net 式逐级上采样恢复边界，并输出 gland 与 contour 两个分支。训练时同时监督主输出和辅助输出，推理阶段再用 `RTS` 获得 uncertainty map 并改进高不确定区域的预测。

关键页码：

- `p.4-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`encoder-decoder FCN with residual units + MIL unit + dilated residual + ASPP`
- Backbone：`自定义 residual-style network`
- 输入尺寸：`训练 patch 最终裁剪为 464 x 464`
- 输出头：
  - `gland object`
  - `contour`
  - `gland auxiliary`
  - `contour auxiliary`

### 3.2 关键模块详细描述

**模块 1：`MIL unit`**

- 位置：`每次 max-pooling 后的特征提取阶段`
- 操作流程：
  1. 原始图像先下采样到与 pooling 输出同尺寸
  2. 对下采样原图做一个 `3x3 conv`
  3. 与当前特征图拼接
  4. 再过一个 `3x3 conv`
  5. 与普通残差分支结果求和
- 页码：`p.4-p.5`

**模块 2：`Dilated residual unit`**

- 位置：`图像被下采样到 1/8 后`
- 操作流程：
  1. 将普通残差块中的 `3x3 conv` 替换成 `3x3 dilated conv`
  2. 保持较大 receptive field，同时避免原图尺度计算代价
- 页码：`p.5`

**模块 3：`ASPP`**

- 位置：`深层特征输出后`
- 操作流程：
  1. 使用 dilation rate `6 / 12 / 18`
  2. 加入 `global average pooling`
  3. 各分支后接 `1x1 conv`
  4. `dropout = 0.5`
  5. 再以 `1x1 conv` 压缩通道
- 页码：`p.5`

**模块 4：`Decoder + dual branch`**

- 位置：`上采样恢复阶段`
- 操作流程：
  1. 像 U-Net 一样逐级 `x2` 上采样
  2. 与低层特征拼接
  3. 拼接前先对低层特征做 `1x1 conv`
  4. 最终分出 `gland branch` 与 `contour branch`
  5. 在第二个 dilated residual unit 处接 auxiliary loss
- 页码：`p.5-p.6`

**模块 5：`RTS (Random Transformation Sampling)`**

- 位置：`测试时 uncertainty quantification`
- 操作流程：
  1. 对输入图像做随机变换采样
  2. 逐个通过网络推理
  3. 取输出均值作为 refined prediction
  4. 取输出方差作为 uncertainty map
  5. 用 boundary-removed uncertainty 给每个实例计算 uncertainty score
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Encoder stage | residual / MIL | 未完整列通道 | 逐级下采样 | 每次 pooling 后接 MIL |
| Deep stage | dilated residual | 未完整列通道 | `1/8` 尺度 | 扩大感受野 |
| ASPP | dilated conv + GAP | 多分支 | 深层特征尺度 | dilation `6/12/18` |
| Decoder | upsampling + skip | 未完整列通道 | 逐级恢复 | 类 U-Net |
| Output heads | `1x1 conv` | `2` classes each | 原图分辨率 | gland / contour / aux |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
y = F(x, W) + x
```

符号说明：
- 普通 residual unit 的输出
- 页码：`p.4-p.5`

公式 2：

```text
y = F(x, W) + G(x, v, M)
```

符号说明：
- `x`：当前特征
- `v`：下采样后的原始图像
- `G`：把原图信息卷积、拼接再卷积后的函数
- 这是 `MIL unit` 的核心公式
- 页码：`Eq.(2), p.4-p.5`

公式 3：

```text
Ltotal = Lg + Lc + lambda * Lag + lambda * Lac + gamma * ||w||^2_2
```

符号说明：
- `Lg`：gland 主输出交叉熵
- `Lc`：contour 主输出交叉熵
- `Lag`：gland auxiliary 交叉熵
- `Lac`：contour auxiliary 交叉熵
- `lambda`：辅助损失折扣权重
- `gamma`：L2 正则系数
- 页码：`Eq.(4), p.5-p.6`

公式 4：

```text
mu = (1/n) * sum_i f(Phi_i(x); w)
sigma = (1/n) * sum_i (f(Phi_i(x); w) - mu)^2
```

符号说明：
- `mu`：RTS 下的 refined prediction
- `sigma`：uncertainty map
- `Phi_i`：第 `i` 个随机变换
- `n`：采样次数
- 页码：`Eq.(5), p.6-p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是纯损失论文，但 auxiliary loss 通过 `lambda` 衰减，避免训练后期辅助分支持续主导优化。
- `RTS` 不是对结构做改动，而是通过测试时采样近似得到 observation-dependent uncertainty。
- 页码：`p.5-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Lg` | cross-entropy | gland 主输出 | gland branch |
| `Lc` | cross-entropy | contour 主输出 | contour branch |
| `Lag` | cross-entropy | gland 辅助输出 | auxiliary head |
| `Lac` | cross-entropy | contour 辅助输出 | auxiliary head |
| `gamma ||w||^2_2` | L2 regularization | 权重正则 | 全网络 |

### 5.2 总损失公式

```text
Ltotal = Lg + Lc + lambda * Lag + lambda * Lac + gamma * ||w||^2_2
```

### 5.3 权重配置与调度策略

- 各项权重：
  - `lambda = 1` 初始
  - `gamma = 1e-5`
- 是否衰减/动态调整：
  - `lambda` 每 `8` 个 epoch 除以 `10`
- 页码：`p.5-p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `85` | `80` | 从训练集中留 `20%` 评估 | `165` 张总图像 |
| `CRAG` | `173` | `40` | 从训练集中留 `20%` 评估 | `213` 张图像 |

### 6.2 数据增强

- 增强列表：
  - `elastic distortion`
  - `random flip`
  - `random rotation`
  - `Gaussian blur`
  - `median blur`
  - `colour distortion`
- Patch 提取策略：`500 x 500 -> 464 x 464`
- 页码：`p.9`

### 6.3 优化器与超参数

- 框架：`TensorFlow 1.3.0`
- 优化器：`Adam`
- 初始学习率：`1e-4`
- 学习率调度：`正文未单独展开，按固定初始值训练`
- Batch size：`2`
- Epoch / Steps：
  - `GlaS`: `30 epochs (60,000 steps)`
  - `CRAG`: `75 epochs (200,000 steps)`
- 权重初始化：`Xavier initialisation`
- 预训练策略：`未明确说明使用外部预训练`
- 是否冻结部分层：`否`
- 设备：`1 x NVIDIA Titan X GPU`
- 页码：`p.9`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未明确写 stain normalization`
- 颜色空间转换：`默认 RGB`
- resize / crop / pad 策略：`先取 500x500 patch，再随机裁成 464x464`
- patch overlap：`未明确`
- 背景过滤策略：`未明确`
- 标签生成方式：`instance-level gland + contour annotations`
- 类别不平衡处理：`未明确 class weighting`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`GlaS / CRAG 都从 train 中再划 20% 评估集，后续引用时要和官方 test protocol 区分`
- 页码：`p.8-p.9`

---

## 7. 推理与后处理

- 推理时输入尺寸：`原图推理，正文未单独给 patch inference 细节`
- 概率阈值：`0.5`
- 后处理步骤：
  1. 对所有预测概率图以 `0.5` 阈值化
  2. 做 morphology opening
  3. 使用 `disk filter radius = 5`
- TTA / Test-time refinement：
  - `RTS`：对输入做 flip / rotation / blur / Gaussian noise 等随机变换采样
  - 均值作为 refined prediction，方差作为 uncertainty map
- 页码：`p.6-p.7, p.11-p.12`

---

## 8. 消融实验

### 8.1 消融设计

> 本篇最关键的额外分析是 `RTS` 带来的提升，以及与其他方法在 `GlaS / CRAG` 上的对比。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | 不使用 `RTS` | `GlaS B / CRAG` 的 `F1 / ObjDice / ObjHaus` 均略差 | RTS 有助于改进高不确定区域预测 |
| 2 | 使用 `Monte Carlo dropout` 代替 RTS | 提升不明显，甚至训练有负面影响 | 在本结构下 RTS 比 MC dropout 更合适 |

### 8.2 各模块贡献量化

- `RTS` 在 `GlaS B` 上：
  - `F1: 0.809 -> 0.844`
  - `ObjDice: 0.822 -> 0.836`
  - `ObjHaus: 117.91 -> 105.89`
- `RTS` 在 `CRAG` 上：
  - `F1: 0.806 -> 0.825`
  - `ObjDice: 0.867 -> 0.875`
  - `ObjHaus: 162.35 -> 160.14`
- 页码：`Table 3, p.12`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS A` | `F1 0.914` | `ObjDice 0.913` | `ObjHaus 41.54` | `MILD-Net-RTS` |
| `GlaS B` | `F1 0.844` | `ObjDice 0.836` | `ObjHaus 105.89` | `MILD-Net-RTS` |
| `CRAG` | `F1 0.825` | `ObjDice 0.875` | `ObjHaus 160.14` | `MILD-Net-RTS` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `MILD-Net-RTS` | `CRAG` | `0.825` | `0.875` | `160.14` |
| `DCAN` | `CRAG` | `0.736` | `0.794` | `218.76` |
| `U-Net` | `CRAG` | `0.600` | `0.654` | `354.09` |
| `MILD-Net-RTS` | `GlaS A/B` | `0.914 / 0.844` | `0.913 / 0.836` | `41.54 / 105.89` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否`
- 是否统一数据增强：`否`
- 是否统一后处理：`未完全统一`
- 是否统一输入尺寸：`否`
- 结果来源：`原文 Table 1 / 2 / 3`
- 页码：`p.11-p.12`

### 9.4 评价协议与指标定义

- 数据划分来源：
  - `GlaS`：`85 / 80`
  - `CRAG`：`173 / 40`
- 结果汇报层级：`GlaS A / GlaS B / CRAG`
- 实例匹配规则：`沿用 GlaS challenge object-level protocol`
- Dice 类型：`Object Dice`
- Hausdorff 类型：`Object Hausdorff`
- F1 类型：`object/detection F1`
- 是否含后处理后再报结果：`是`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`正文主表未强调`
- 是否和官方 challenge protocol 一致：`GlaS 指标口径一致，但训练中额外从 train 留 20% eval`
- 页码：`p.8-p.12`

---

## 10. 计算量与效率

- 参数量（Params）：`未明确给出`
- 计算量（FLOPs / MACs）：`未明确给出`
- 推理时间（ms/image）：`正文未给单图耗时`
- 训练时间（总 GPU-hours）：`未直接换算，但给了 epoch / steps`
- 输入尺寸（计算量对应的）：`500 -> 464 patch`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `MILD-Net` | `N/A` | `N/A` | `N/A` |

- 页码：`正文主要强调性能，不强调效率`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，本节不适用。

### 11.2 论文指出的研究空白 / Open Problems

1. max-pooling 信息损失会破坏 gland segmentation 的细节恢复
2. 单纯 backbone 预测不够，还需 uncertainty quantification
3. 未来还要把模型扩展到更高效的 WSI 处理与非集成式 uncertainty 建模

### 11.3 对我们选题的启示

- 我们当前的 `大感受野 + Boundary Head` 路线并不是拍脑袋，和腺体任务内有效改进方向一致。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但明确强调不同 cancer grades 带来的 morphological heterogeneity。

### 12.2 涉及的生物标志物

- 无直接 biomarker，但 `MILD-Net+` 进一步引入 lumen segmentation 以增强诊断信息。

### 12.3 临床意义

- uncertainty map 可用于标记高歧义 gland 区域，辅助 pathologist 排查与 annotation prioritisation。
- 页码：`p.6-p.7, p.17`

---

## 13. 开源与复现

- 代码是否开源：`CRAG 数据链接给出，但代码开源情况需后续确认`
- 代码仓库地址：`CRAG dataset URL 见正文，代码仓库未在当前抽取段落明确写出`
- 框架/语言：`TensorFlow 1.3.0`
- 预训练权重是否提供：`未明确`
- 复现难度评估：`中`
- 复现障碍：
  - 通道数与完整层表未完全逐项列出
  - RTS 的采样次数 `n` 在当前抽取片段里未直接给出
  - MILD-Net 与 MILD-Net+ 混在同文，需要小心区分主结果与扩展结果

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不依赖逐点复现 | 中 |
| 验证集划分 | 部分 | 仅记录“从 train 留 20% eval”，不脑补具体分法 | 中 |
| 推理阈值 | 是 | `0.5` | 低 |
| 后处理细节 | 是 | 记录 morphology opening + `r=5` | 低 |
| 训练轮数停止准则 | 部分 | 用 epoch/steps 记录，未补未写早停 | 中 |
| 数据预处理 | 部分 | 记录 patch 与 augmentations，未见 stain normalization | 中 |

- 不确定但影响较大的点：
  - RTS 的采样数量 `n`
  - 部分实验表的完整 baseline 列表和 rank 细节
  - 作者与 DOI 还需最终 BibTeX 级核对

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- `CRAG` 明显比 `GlaS` 更难，尤其 malignant cases 中 gland boundary 非常模糊。
- `Hausdorff` 在 malignant 场景下明显更高，说明 boundary disagreement 仍然严重。
- 现有 RTS 很有用，但若要高效处理 WSI，需要非集成式 uncertainty 方法。
- 页码：`p.12, p.17`

### 14.2 我们观察到的潜在问题

- 虽然输出 contour，但作者强调 contour 主要用于 uncertainty refinement，而不是直接分离实例，这与 `DCAN` 路线不同。
- RTS 会增加测试开销，不适合直接做高效 WSI 推理。
- `MILD-Net+` 是额外扩展，不应和主表结果混为一谈。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是`
- 典型失败场景：
  - `CRAG` 中 boundary ambiguity 更强
  - malignant 腺体边界误差导致 `Hausdorff` 恶化
  - 高 uncertainty 区域更容易出现 false positives / boundary disagreement
- 页码：`Figure 4-5, p.11-p.12; p.17`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `GlaS + CRAG` 双数据集协议
- `F1 / Object Dice / Object Hausdorff` 对象级主指标
- `gland + contour + auxiliary` 四监督结构
- `500 x 500 -> 464 x 464`
- `Adam(1e-4), batch size 2`

### 15.2 可以作为候选参数来源的

- `lambda` 每 `8` epoch 衰减
- `gamma = 1e-5`
- morphology opening `radius = 5`
- `RTS` 作为测试阶段增强与 uncertainty 估计方案

### 15.3 不应照搬的（及原因）

- 不应直接照搬 `RTS` 到主结果协议
  - 原因：会带来推理开销，且和我们主线的公平比较口径可能冲突
- 不应把 contour 的作用简单理解成“就是实例分离”
  - 原因：本篇里 contour 主要用于 uncertainty refinement，不同于 `DCAN`

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| `Boundary Head` | gland/contour 双分支与辅助监督 | 强 |
| `LKMA / 大感受野` | dilated residual + ASPP 对形态异质性有效 | 强 |
| 训练协议 | `GlaS + CRAG`, patch/aug/lr/bs | 强 |
| uncertainty 讨论 | RTS 提供临床可解释性附加信息 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`实验协议表 / 参数来源表 / 边界分支动机说明`
- [ ] 需要和哪篇论文交叉验证：`DCAN 2016`, `TA-Net 2022`, `DEA-Net 2024`
- [ ] 待确认的问题：`我们是否需要把 uncertainty 分析作为附加实验而非主表设置`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 腺体边界、形态异质性与信息损失问题 | 直接引用任务难点 |
| related work | 从 DCAN 到 MILD-Net 的轮廓/感受野演进 | 方法脉络 |
| 方法 | MIL unit / ASPP / dual branch / auxiliary loss 动机 | 作为设计依据 |
| 实验设置 | GlaS + CRAG、patch、增强、优化器 | 作为任务内来源 |
| 讨论 | RTS 提升与 WSI 效率矛盾 | 解释边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.2-p.3` | `GlaS / CRAG` 示例图 | 双数据集说明 |
| `Figure 2` | `p.4-p.5` | MILD-Net 总体结构图 | MIL / ASPP / dual branch 参考 |
| `Eq.(2)` | `p.4-p.5` | MIL unit 公式 | 方法引用 |
| `Eq.(4)` | `p.5-p.6` | 总损失公式 | 损失引用 |
| `Eq.(5)` | `p.6-p.7` | RTS prediction / uncertainty 公式 | uncertainty 分析 |
| `Table 1` | `p.11-p.12` | GlaS 对比表 | 主结果引用 |
| `Table 2` | `p.11-p.12` | CRAG 对比表 | 主结果引用 |
| `Table 3` | `p.12` | RTS 增益表 | 消融引用 |

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
