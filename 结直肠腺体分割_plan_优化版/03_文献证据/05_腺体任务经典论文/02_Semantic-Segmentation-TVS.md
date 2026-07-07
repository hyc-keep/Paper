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

- `early gland segmentation`
- `dual CNN + separator`
- `variational post-processing`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是早期直接针对 `GlaS@MICCAI2015` 的腺体方法论文
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Semantic Segmentation of Colon Glands with Deep Convolutional Neural Networks and Total Variation Segmentation`
- 作者/团队：`Philipp Kainz, Michael Pfeiffer, Martin Urschler`
- 发表年份/会议/期刊：`2015, arXiv / GlaS@MICCAI2015 challenge method paper`
- DOI / arXiv ID：`arXiv:1511.06919`
- BibTeX key：`kainz2015semantic`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Semantic_Segmentation_of_Colon_Glands_with_Deep_Convolutional_Neural_Networks_and_Total_Variation_Segmentation_2015.pdf`
- 当前定位：早期 `GlaS` 参赛方法里非常典型的一篇，核心在 `Object-Net + Separator-Net + weighted TV` 的三段式实例分离思路
- 与已提取论文的关系：
  - 是后续 `DCAN`、`MILD-Net`、`TA-Net` 这类“显式分离相邻腺体”路线的早期前身之一
  - 与 `GlaS Challenge 2017` 互补：后者给官方协议，这篇给早期实现细节
  - 与 `U-Net`、`DeepLabV3+` 等通用基线不同，这篇是 gland-specific 任务内方案

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：colon gland segmentation 是 quantitative morphology assessment 与 cancer grading 的关键前提，而 pathological cases 下 gland 的形态变化会显著加剧分割难度。
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者不是直接做单一 gland/background 分割，而是引入专门的 gland-separating refinement classifier 来处理 touching glands。
  - 用途：`方法动机`
  - 页码：`p.2, p.5-p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：不同于只靠像素分类，这篇把 `separator` 预测和 `weighted total variation` 正则化联合起来，以减少 close objects merging。
  - 用途：`边界/分离路线的早期代表`
  - 页码：`p.2, p.6-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据规模 | `161` 张 | 早期 Warwick-QU 数据口径 | `p.2` |
| 输入 patch | `101 x 101` | 方法/训练设置 | `p.4-p.5, p.7` |
| 训练采样 | `125,000 patches per class` | 训练设置 | `p.8` |
| 学习率 | `0.0025` | 训练设置 | `p.8-p.9` |
| dropout | `0.5` | 训练设置 | `p.8-p.9` |
| 小 blob 去除阈值 | `< 500 pixels` | 后处理 | `p.10` |
| 运行时间 | `5 min / 577 x 522 image` | 效率 | `p.10` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 腺体在 benign 与 malignant 组织中的 `shape / size / location / texture / staining` 变化都很大。
- 仅靠普通图像处理或单一路径像素分类，难以同时稳健处理 benign 和 malignant 腺体。
- 非常接近甚至 touching 的腺体容易在分割时被粘连，需要显式 separator 建模。

对应原文依据（页码）：

- `p.1-p.2`
- `p.5-p.6`

### 2.2 核心思路（一段话概括解法方向）

- 作者先对 H&E 图像做 `color deconvolution + CLAHE` 预处理，然后训练两个 sliding-window CNN：`Object-Net` 负责 gland/background 相关分类，`Separator-Net` 负责 gland-separating structures。随后把两个网络的概率图组合成前景/背景权重图，再用 `weighted total variation` 的 figure-ground segmentation 做全局正则化，最终降低 touching glands 的合并错误。

关键页码：

- `p.2-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`dual CNN pixel classification + variational segmentation`
- Backbone：`LeNet-5 style CNNs`
- 输入尺寸：`101 x 101 patch`
- 输出头：`Object-Net 4-class`, `Separator-Net 2-class`, 最终输出为 gland segmentation mask

### 3.2 关键模块详细描述

**模块 1：`H&E preprocessing`**

- 位置：`输入端`
- 操作流程：
  1. 对原始 RGB 图像做 `color deconvolution`
  2. 仅保留 deconvolved image 的 red channel
  3. 对该通道做 `CLAHE`
- 页码：`p.3`

**模块 2：`Object-Net`**

- 位置：`主像素分类器`
- 操作流程：
  1. 输入 `101 x 101` patch
  2. 四个卷积层后接三个全连接层
  3. 将中心像素分成 `benign background / benign gland / malignant background / malignant gland` 四类
- 页码：`p.4-p.5`

**模块 3：`Separator-Net`**

- 位置：`gland separation refinement classifier`
- 操作流程：
  1. 输入 `101 x 101` patch
  2. 用与 Object-Net 类似的 CNN 预测 separator structures
  3. 输出二分类概率图 `S(x)` 强化 gland border
- 页码：`p.5-p.6`

**模块 4：`Refinement + weighted TV segmentation`**

- 位置：`后端正则化`
- 操作流程：
  1. 用 `Object-Net` 的 gland/background 概率构造 `p_fg` 与 `p_bg`
  2. 用 `Separator-Net` 概率调制二者，避免相邻腺体合并
  3. 对组合后的概率图求解 weighted TV 能量，得到最终连续分割 `u`
  4. 对 `u` 以 `0.5` 阈值化得到最终 mask
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| `Object-Net Conv1` | conv `11x11` | `80` | `101 -> 91` | `p.4-p.5` |
| `Object-Net Conv2` | conv `7x7` | `96` | `46 -> 40` | `p.4-p.5` |
| `Object-Net Conv3` | conv `5x5` | `128` | `20 -> 16` | `p.4-p.5` |
| `Object-Net Conv4` | conv `3x3` | `160` | `8 -> 6` | `p.4-p.5` |
| `Object-Net FC` | FC | `1024 -> 512 -> 4` | N/A | 四分类 |
| `Separator-Net Conv1` | conv `9x9` | `64` | `101 -> 93` | `p.5-p.6` |
| `Separator-Net Conv2` | conv `7x7` | `96` | `47 -> 41` | `p.5-p.6` |
| `Separator-Net Conv3` | conv `5x5` | `128` | `21 -> 17` | `p.5-p.6` |
| `Separator-Net Conv4` | conv `3x3` | `160` | `7 -> 6` | `p.5-p.6` |
| `Separator-Net FC` | FC | `1024 -> 512 -> 2` | N/A | 二分类 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
pfg(x) = max( sum_{l in {1,3}} ICl(x) - rho * S(x), 0 )
```

符号说明：
- `ICl(x)`：Object-Net 在像素 `x` 对第 `l` 类的概率
- `S(x)`：Separator-Net 的 separator 概率
- `rho`：separator refinement 强度
- 页码：`Eq.(1), p.6`

公式 2：

```text
pbg(x) = min( sum_{l in {0,2}} ICl(x) + rho * S(x), 1 )
```

符号说明：
- `pbg(x)`：背景概率图
- gland 类概率被减，background 类概率被加，以增强边界分离
- 页码：`Eq.(2), p.6`

公式 3：

```text
min_u Eseg(u) = ∫ g(x)|∇u(x)|dx + lambda ∫ u(x) * w(x)dx
subject to u(x) in [0,1]
```

符号说明：
- 第一项是 `g`-weighted TV semi-norm
- 第二项是 data term
- `w(x)` 由 `pfg / pbg` 经 logit transform 得到
- 最终对连续 `u` 以 `0.5` 阈值化
- 页码：`Eq.(3)-(6), p.6-p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是专门的损失论文，但后端优化采用 convex weighted TV，可以用 primal-dual algorithm 求全局最优。
- 页码：`p.6-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `negative log-likelihood` | 原文未展开公式 | CNN pixel classification | `Object-Net / Separator-Net` |

### 5.2 总损失公式

```text
CNNs are trained with negative log-likelihood; final segmentation is produced by weighted TV minimization rather than a joint end-to-end loss.
```

### 5.3 权重配置与调度策略

- 各项权重：
  - CNN 分类阶段未给出额外多项加权
  - TV 阶段使用 `rho`, `alpha`, `beta`, `lambda`, `tau`
- 是否衰减/动态调整：
  - CNN 学习率线性衰减
  - TV 参数通过 grid search 选定
- 页码：`p.6-p.9`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Warwick-QU / GlaS@MICCAI2015` | `85` | `60 + 16` | 使用 held-out test set 监控 CNN 早停 | 论文口径为早期 `161` 张 |

### 6.2 数据增强

- 增强列表：
  - `Separator-Net` 前景样本做旋转扩增
  - 每 `36` 度旋转一次，共额外 `9` 个版本
- Patch 提取策略：`101 x 101`
- 页码：`p.7-p.8`

### 6.3 优化器与超参数

- 框架：`Pylearn2 + Theano`
- 优化器：`MBSGD`
- 初始学习率：`0.0025`
- 学习率调度：`线性衰减，在 100 epochs 后饱和到 0.2 * eta0`
- Batch size：`200`
- Epoch / Steps：
  - `Object-Net` 最佳约 `43 epochs`
  - `Separator-Net` 最佳约 `119 epochs`
- 权重初始化：`论文未明确`
- 预训练策略：`从头训练`
- 是否冻结部分层：`否`
- 设备：`NVIDIA GeForce Titan Black 6GB GPU`
- 页码：`p.8-p.10`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`color deconvolution + CLAHE`
- 颜色空间转换：`RGB -> deconvolved red channel`
- resize / crop / pad 策略：`先缩小到一半分辨率，再分类后上采样回原尺寸`
- patch overlap：`sliding-window pixel classification，中心像素预测`
- 背景过滤策略：`未单独说明`
- 标签生成方式：
  - `Object-Net`：四分类标签来自 gland mask + benign/malignant 标签
  - `Separator-Net`：额外人工标注 gland-separating structures
- 类别不平衡处理：`balanced training set of 125,000 patches per class`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：
  - 论文使用的是早期 `Warwick-QU` 口径
  - 训练中提到 held-out test set 监控误差，未细说内部切分细节
- 页码：`p.3-p.9`

---

## 7. 推理与后处理

- 推理时输入尺寸：`half-resolution image + 101 x 101 sliding-window classification`
- 概率阈值：
  - `tau = 0.65` 用于构造 TV 权重图
  - 最终 `u` 以 `0.5` 阈值化
- 后处理步骤：
  1. `Object-Net` 与 `Separator-Net` 输出合成 `pfg / pbg`
  2. 求解 weighted TV segmentation
  3. 去除面积 `< 500 pixels` 的 blobs
  4. 为剩余 blobs 赋 unique identifiers 后计算指标
- TTA / Test-time refinement：`无`
- 页码：`p.6-p.10`

---

## 8. 消融实验

### 8.1 消融设计

> 论文最核心的对照就是“加不加 separator refinement”。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | 去掉 `separator refinement` | `Test A ObjDice 0.70 -> 0.75`, `Test B ObjDice 0.58 -> 0.61`, `Hausdorff` 也明显下降 | separator 对 object separation 与边界质量有效 |
| 2 | 仅保留 `Object-Net` | `F1 / Dice / Hausdorff` 整体较差 | 单一路径像素分类不足以稳定分开 close glands |

### 8.2 各模块贡献量化

- `Separator-Net` 的独立贡献：
  - `Test A`: `F1 0.67 -> 0.68`, `ObjDice 0.70 -> 0.75`, `Hausdorff 137.44 -> 103.49`
  - `Test B`: `F1 0.50 -> 0.55`, `ObjDice 0.58 -> 0.61`, `Hausdorff 249.37 -> 213.58`
- 页码：`Table 1, p.9-p.10`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Training (with separator)` | `F1 0.87` | `ObjDice 0.88` | `Hausdorff 61.36` | 均值 |
| `Test A (with separator)` | `F1 0.68` | `ObjDice 0.75` | `Hausdorff 103.49` | 均值 |
| `Test B (with separator)` | `F1 0.55` | `ObjDice 0.61` | `Hausdorff 213.58` | 均值 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| 本文方法（with separator） | `Test A` | `F1 0.68` | `ObjDice 0.75` | `Hausdorff 103.49` |
| 本文方法（without separator） | `Test A` | `F1 0.67` | `ObjDice 0.70` | `Hausdorff 137.44` |
| 本文方法（with separator） | `Test B` | `F1 0.55` | `ObjDice 0.61` | `Hausdorff 213.58` |
| 本文方法（without separator） | `Test B` | `F1 0.50` | `ObjDice 0.58` | `Hausdorff 249.37` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否，文中没有系统外部主表对比`
- 是否统一数据增强：`不适用`
- 是否统一后处理：`不适用`
- 是否统一输入尺寸：`不适用`
- 结果来源：`原文 Table 1`
- 页码：`p.9-p.10`

### 9.4 评价协议与指标定义

- 数据划分来源：`GlaS@MICCAI2015 contest 口径`
- 结果汇报层级：`Training / Test A / Test B`
- 实例匹配规则：`沿用 challenge evaluation scripts`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`Hausdorff distance`
- F1 类型：`detection F1`
- 是否含后处理后再报结果：`是，TV segmentation + blob filtering 后`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`是，表中给均值和 SD`
- 是否和官方 challenge protocol 一致：`基本一致，但数据总量口径是早期 `161/16` 版本`
- 页码：`p.2, p.9-p.10`

---

## 10. 计算量与效率

- 参数量（Params）：`未报告`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`未报告`
- 输入尺寸（计算量对应的）：`577 x 522` 单图示例
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| 本文方法 | `N/A` | `N/A` | `5 min / image` |

- 页码：`p.10`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，本节不适用。

### 11.2 论文指出的研究空白 / Open Problems

1. 普通 gland/background 分类不足以处理 close glands
2. benign 与 malignant 组织差异值得显式建模
3. 像素分类结果需要更强的结构化后端约束

### 11.3 对我们选题的启示

- 对 gland task 来说，separator / contour / topology 分支并不是后来才有的附加项，而是从早期方法开始就存在的核心需求。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但明确把 gland segmentation 与 cancer grading 联系起来。

### 12.2 涉及的生物标志物

- 无。

### 12.3 临床意义

- automated gland segmentation 可服务 morphology assessment，并支持 benign / malignant 区分。
- 页码：`p.1-p.2, p.11-p.13`

---

## 13. 开源与复现

- 代码是否开源：`否`
- 代码仓库地址：`无`
- 框架/语言：`Pylearn2 / Theano`
- 预训练权重是否提供：`否`
- 复现难度评估：`高`
- 复现障碍：
  - 依赖较老的 `Theano / Pylearn2`
  - `Separator-Net` 需要额外人工 separator 标注
  - sliding-window + TV 后端工程成本高
  - 数据口径与后来的 `GlaS 2017` 最终版存在差异

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不依赖其随机种子做逐点复现 | 中 |
| 验证集划分 | 否 | 只引用其 held-out test 早停描述，不自行脑补比例 | 高 |
| 推理阈值 | 是 | `tau = 0.65`, 最终阈值 `0.5` | 低 |
| 后处理细节 | 是 | 按 TV + small blob removal 记录 | 低 |
| 训练轮数停止准则 | 是 | 记录 `20 epochs no improvement` | 低 |
| 数据预处理 | 是 | 记录 deconvolution + red channel + CLAHE | 低 |

- 不确定但影响较大的点：
  - held-out test set 的具体抽取方式
  - separator 人工标注的精确规则与厚度
  - 旧框架下数值细节对复现稳定性的影响

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 不能区分比 benign / malignant 更细的 histologic grades
- sliding-window + TV 流程较重
- malignant 腺体因为形态不规则和病理变化更难分割
- 页码：`p.10-p.13`

### 14.2 我们观察到的潜在问题

- 额外 separator 标注会增加数据准备成本
- 变分后端与当前端到端分割主线不一致
- 运行时间较长，不适合作为现代快速基线
- 论文使用的早期数据口径与后续官方 `165 / 20` 不一致，写作时容易混淆

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是`
- 典型失败场景：
  - malignant glands 分割更差
  - false negatives 与 false positives 在复杂腺体结构上更常见
  - touching glands 若不加 separator 更易 merge
- 页码：`Fig. 8-10, p.10-p.12`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `separator` 作为独立建模对象的任务内动机
- `color deconvolution + CLAHE` 作为 H&E 预处理候选方案
- 对象级指标口径：`F1 / Object-Dice / Hausdorff`

### 15.2 可以作为候选参数来源的

- `101 x 101` patch 的早期上下文设计思路
- `125,000/class` 的平衡采样策略
- `tau = 0.65`, `alpha = 10`, `beta = 0.95`, `lambda = 0.1` 的 TV 参数可作为历史参考

### 15.3 不应照搬的（及原因）

- 不应直接照搬 `Theano + Pylearn2 + sliding-window + TV`
  - 原因：工程代价大，和我们当前主线不一致
- 不应把 `161 / Test B=16` 当作最终官方 `GlaS` 口径
  - 原因：后续 challenge 总结版已更新为 `165 / 20`

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| `Boundary Head` | separator 学习用于分开 close glands | 强 |
| 对象级结果解释 | separator 对 `ObjDice / Hausdorff` 提升更明显 | 强 |
| 预处理候选 | H&E deconvolution + CLAHE | 中 |
| 失败模式分析 | malignant harder, close glands merging | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`后续边界分支动机说明 / 预处理候选表`
- [ ] 需要和哪篇论文交叉验证：`DCAN 2016`, `MILD-Net 2018`
- [ ] 待确认的问题：`我们是否需要做一个不带 separator 的对照消融来继承这条证据链`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland segmentation 难点与 morphology 价值 | 作为早期任务定义引用 |
| related work | separator/边界分离早期路线 | 用于方法脉络 |
| 方法 | `Boundary Head` 的任务内动机 | 说明不是凭空设计 |
| 实验设置 | object-level metrics, preprocessing 候选 | 谨慎引用，不夸大为复现 |
| 讨论 | 历史方案的局限与工程代价 | 对照我们主线优势 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 2` | `p.3` | H&E 预处理流程 | 预处理引用 |
| `Fig. 3` | `p.4-p.5` | `Object-Net / Separator-Net` 架构图 | separator 双网络设计参考 |
| `Fig. 5` | `p.7-p.8` | separator 人工标注与 patch 采样示意 | 数据准备说明 |
| `Table 1` | `p.9-p.10` | with / without separator 的结果对比 | 消融与结果引用 |
| `Fig. 8-10` | `p.10-p.12` | 定性结果和失败案例 | 误差分析 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现到主要流程级别
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
