# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `error-driven multi-stage instance segmentation`
- `adaptive boosting for dense prediction`
- `multi-attention learning`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体实例分割里的“逐阶段纠错 + 自适应关注 hard pixels”路线代表作
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`AttentionBoost: Learning What to Attend for Gland Segmentation in Histopathological Images by Boosting Fully Convolutional Networks`
- 作者/团队：`Gozde Nur Gunesli, Cenk Sokmensuer, Cigdem Gunduz-Demir`
- 发表年份/会议/期刊：`2020, IEEE Transactions on Medical Imaging`
- DOI / arXiv ID：`10.1109/TMI.2020.3015198`
- BibTeX key：`gunesli2020attentionboost`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/AttentionBoost_Learning_What_to_Attend_for_Gland_Segmentation_2020.pdf`
- 当前定位：`05` 目录里很有特色的一篇实例分割方法论文，不是直接多分支预测 contour 或 topology，而是用 boosting 在多阶段 FCN 中动态重加权 hard-to-learn pixels
- 与已提取论文的关系：
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/03_DCAN.md) 的共同点是都关注 boundary mistakes，但 DCAN 通过 contour branch，AttentionBoost 通过 adaptive loss reweighting
  - 与 [07_TA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/07_TA-Net.md) 不同：TA-Net 预定义 topology supervision，AttentionBoost 不预定义“该关注哪里”，而是由前一阶段错误驱动关注
  - 与 [08_Deep-Multichannel.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/08_Deep-Multichannel.md) 形成对照：后者显式并行多通道，本篇是同任务多阶段 boosting

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：hard-to-learn pixels 的正确分类对 instance segmentation 成败影响很大，而边界像素只是其中一种，噪声和伪影区域也会造成严重 false positives。
  - 用途：`背景 / 痛点`
  - 页码：`p.4262-p.4263`
- 句子/事实 2：已有方法通常预定义“该关注什么”，例如 boundary pixels，但对于其他错误模式，手工定义 attention 既困难也不灵活。
  - 用途：`方法动机`
  - 页码：`p.4262-p.4264`

#### 1.1.2 related work 可引用句

- 句子/事实 1：AttentionBoost 是一个 error-driven、multi-stage 的多注意力学习模型，每个 stage 通过前一阶段像素级错误自适应改变损失权重。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.4263-p.4264`
- 句子/事实 2：作者强调该方法能改进的不只是 boundary pixels，还包括由噪声和 artifacts 导致的 false positives。
  - 用途：`与 contour-only 路线的差异`
  - 页码：`p.4263`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 期刊信息 | `TMI 39(12):4262-4273` | 引用信息 | `paper landing page` |
| 参数量 | `31,387,780` | 计算量/模型规模 | `supp p.5` |
| 训练时间 | `4844 +- 403 s` | 计算量/训练成本 | `supp p.5` |
| stage 数 | `4 stages` | 方法结构 | `supp p.3-p.4, p.5` |
| shared weights 参数量 | `7,846,945` | 消融 | `supp p.5` |
| 2/3/5/6/7 stages 参数量 | `15.69M / 23.54M / 39.23M / 47.08M / 54.93M` | 消融 | `supp p.5` |
| fsize | `3` | 后处理 | `supp p.2` |
| batch size | `1` | 训练设置 | `supp p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 小样本且类别不平衡时，FCN 容易对 minority class 和 hard-to-learn pixels 泛化较差。
- gland instance segmentation 中 boundary pixels 的数量虽少，但错误代价极高，因为它们决定多个 gland 是否被正确分开。
- 手工预定义“该关注边界”只覆盖一种错误模式，不能适应 artifacts、white regions 等其他 hard pixels。
- 需要一种能在训练过程中直接从错误中学习“该关注什么”的机制。

对应原文依据（页码）：

- `p.4262-p.4263`

### 2.2 核心思路（一段话概括解法方向）

- AttentionBoost 构造一个 `multi-stage FCN`，每个 stage 学同一个 gland segmentation 任务，但使用由前一阶段预测误差驱动更新的像素级损失权重，因此后续 stage 会自适应把更多注意力放在前面 stage 没学好的像素上。最终用所有 stage 的平均概率图 `Y_avg` 进行 gland instance 定位，再通过 certain gland/background seeds、生长、面积阈值 `A_thr` 与 majority filter 平滑得到实例结果。

关键页码：

- `p.4263-p.4264`
- `supp p.2-p.3`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`multi-stage FCN with adaptive loss adjustment`
- Backbone：`U-Net like FCN base model` [补充材料还给出 `G-Conv/G-Res` 等替代基模]
- 输入尺寸：`正文当前抽取未明确；补充材料说明 base model 为 U-Net 风格`
- 输出头：`binary gland probability map`

### 3.2 关键模块详细描述

**模块 1：`Multi-stage FCN`**

- 位置：`整体主架构`
- 操作流程：
  1. 串联多个 stage networks
  2. 每个 stage 都执行 gland segmentation
  3. 不同 stage 不共享目标函数，因为损失权重会随前序错误变化
  4. 最终聚合各 stage posterior maps 得到 `Y_avg`
- 页码：`p.4263-p.4264`
- 补充说明：`默认实验核心配置为 4-stage`

**模块 2：`Adaptive Loss Adjustment`**

- 位置：`训练目标层`
- 操作流程：
  1. 统计前一阶段对每个像素的正确/错误及置信度
  2. 按像素分别调整 loss 权重
  3. 错得更明显、却更关键的 hard pixels 在下一 stage 拥有更高权重
  4. 让后续 stage 学不同难度的“子任务”
- 页码：`p.4263-p.4264`

**模块 3：`Average Posterior Aggregation`**

- 位置：`多阶段输出融合`
- 操作流程：
  1. 收集 `Y_1, Y_2, Y_3, Y_4`
  2. 计算 `Y_avg`
  3. 基于 `Y_avg` 而不是单一 stage 进行实例定位
- 页码：`supp p.2-p.4`

**模块 4：`Instance Localization From Y_avg`**

- 位置：`推理/后处理阶段`
- 操作流程：
  1. 在 `Y_avg` 上识别 certain gland 与 certain background pixels
  2. 用这些像素定义 seed regions
  3. 通过区域生长定位 gland instances
  4. 用 `A_thr` 去除过小 seed regions
  5. 用 majority filter 平滑边界
- 页码：`supp p.2`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Stage 1-4 | U-Net like FCN | 未逐层完整展开 | 未明确 | 默认主配置为 `4 stages` |
| Aggregation | average posterior | `1` map | 同输入 | 得到 `Y_avg` |
| Seed extraction | rule-based | `N/A` | 同输入 | 受 `alpha` 控制 |
| Region growing | instance localization | `N/A` | 同输入 | 受 `A_thr` 控制 |
| Boundary smoothing | majority filter | `fsize=3` | 同输入 | 后处理平滑 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
F-score = 2 * precision * recall / (precision + recall)
precision = |TP| / (|TP| + |FP|)
recall = |TP| / (|TP| + |FN|)
```

符号说明：
- 对象级 F-score，沿用 GlaS challenge
- 分割对象与真值对象重叠至少 50% 记为 `TP`
- 页码：`supp Eq.(1), p.1`

公式 2：

```text
Dice(S, G) = 1/2 * [ sum_{s_i in S} w(s_i) * DI(s_i, gamma(s_i))
                   + sum_{g_j in G} w(g_j) * DI(g_j, sigma(g_j)) ]
```

符号说明：
- `S`：分割对象集合
- `G`：真值对象集合
- `gamma` / `sigma`：最大重叠匹配对象
- `DI(x,y) = 2|x∩y| / (|x| + |y|)`
- 页码：`supp Eq.(2), p.1`

公式 3：

```text
Hausdorff(S, G) = 1/2 * [ sum_{s_i in S} w(s_i) * HD(s_i, gamma(s_i))
                        + sum_{g_j in G} w(g_j) * HD(g_j, sigma(g_j)) ]
```

符号说明：
- `HD(x,y)`：对象对之间的 Hausdorff distance
- 无 overlap 时用最小 Hausdorff 的对象匹配
- 页码：`supp Eq.(3), p.1`

公式 4：

```text
Y_avg(I) = { y_avg_hat(p) }_{p in I}
```

符号说明：
- 这是多阶段 posterior aggregation 后的平均概率图
- gland 实例不是直接从某一 stage 输出，而是从 `Y_avg` 上定位
- 页码：`supp p.2`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇最关键的思想不是换 backbone，而是改变 dense prediction 的 loss weighting：每个 pixel 的损失贡献由前序 stage 的错误与置信度决定。
- 这使得 AttentionBoost 虽然所有 stage 学的是同一任务，但由于 objective 被动态改写，等效于每个 stage 关注不同错误模式。
- 页码：`p.4263-p.4264`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| segmentation loss | 二分类像素级损失 | gland/background segmentation | 每个 stage FCN |
| adaptive boosting adjustment | 按像素重加权 | 强化 hard-to-learn pixels | stage-to-stage 之间 |

### 5.2 总损失公式

```text
主文提出的是 stage-wise adaptive loss adjustment，
但当前补充材料未给出完整公式全文；需回主文 Eq.(4) 级核对。
```

### 5.3 权重配置与调度策略

- 各项权重：`不是固定类权重，而是每像素动态权重`
- 是否衰减/动态调整：`是，随 previous stages 的正确/错误和置信度动态调整`
- 页码：`p.4263-p.4264`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `[待确认]` | `[待确认]` | `5-fold early stopping / validation traces appear in supplementary` | 对象级指标沿用 GlaS |
| `fluorescence nuclei task` | `[待确认]` | `[待确认]` | `[待确认]` | 主文提到跨任务泛化 |

### 6.2 数据增强

- 增强列表：`当前抽取未明确`
- Patch 提取策略：`当前抽取未明确`
- 页码：`[待确认]`

### 6.3 优化器与超参数

- 框架：`作者代码公开，主实现为 Python；补充材料未写具体 DL 框架`
- 优化器：`AdaDelta`
- 初始学习率：`AdaDelta 自适应，固定 lr 未单列`
- 学习率调度：`未单独报告`
- Batch size：`1`
- Epoch / Steps：
  - 使用 `early stopping`
  - 4-stage 主模型平均 stopping point 约 `79.4 epochs`
  - shared-weights 变体平均 stopping point 约 `32.2 epochs`
  - shared-weights x2 变体平均 stopping point 约 `184.8 epochs`
- 权重初始化：`from scratch`
- 预训练策略：`无`
- 是否冻结部分层：`否`
- 设备：`补充材料仅给出训练时间，硬件未明确`
- 页码：`supp p.5-p.6`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未明确`
- 颜色空间转换：`未明确`
- resize / crop / pad 策略：`未明确`
- patch overlap：`未明确`
- 背景过滤策略：`实例定位阶段依赖 certain background seeds`
- 标签生成方式：`binary gland masks -> object-level evaluation and stage posteriors`
- 类别不平衡处理：`通过 adaptive pixel-wise loss reweighting 处理，而非仅靠 class weights`
- 随机种子/重复次数：`补充材料多处给平均训练时间，暗示多次/多折实验`
- 数据泄漏风险点：`正文当前未完整抽取，需回主文核对具体 split`
- 页码：`p.4262-p.4264; supp p.2-p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：`未明确`
- 概率阈值：
  - certain pixels 由 `alpha` 控制
  - 当前未抽到 Eq.(4) 的具体阈值形式
- 后处理步骤：
  1. 聚合各 stage posterior 得到 `Y_avg`
  2. 在 `Y_avg` 上提取 certain gland/background seeds
  3. 进行 seed growing 定位 gland instances
  4. 用 `A_thr` 去除过小 seed regions
  5. 用 majority filter 平滑边界，`fsize = 3`
- TTA / Test-time refinement：`无`
- 页码：`supp p.2`

---

## 8. 消融实验

### 8.1 消融设计

> 这篇补充材料的价值很高，核心消融围绕 `shared weights`、`stage 数量`、`base model`、`normalization` 和 `后处理参数`。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | shared weights | 参数量大降，但性能下降 | 不同 stage 用不同权重更有效 |
| 2 | shared weights x2 | 参数量回到同级，但训练时间暴涨 | 性能下降不只是因为参数量少 |
| 3 | 改变 stage 数量 | 2/3/4/5/6/7 stages 对比 | 4 stages 是主配置与成本折中点 |
| 4 | 不同 base model | `U-Net / G-Conv / G-Res` | 方法不依赖单一基模，但成本不同 |
| 5 | 参数分析 `alpha / A_thr` | 过大过小都会伤害实例结果 | 后处理超参数直接影响对象级指标 |

### 8.2 各模块贡献量化

- 主模型参数量与训练时间：
  - `31,387,780 params`
  - `4844 +- 403 s`
- shared weights：
  - `7,846,945 params`
  - `3569 +- 157 s`
  - stopping point 从 `79.4` 降到 `32.2 epochs`
- stage 数量：
  - `2-stage: 15.69M / 1971 s`
  - `3-stage: 23.54M / 3595 s`
  - `4-stage: 31.39M / 4844 s`
  - `5-stage: 39.23M / 5277 s`
  - `6-stage: 47.08M / 6199 s`
  - `7-stage: 54.93M / 6662 s`
- 页码：`supp p.5-p.6`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS` | `[待确认] object-level F-score` | `[待确认] object-level Dice` | `[待确认] object-level Hausdorff` | 主文证明优于 counterparts |
| `nuclei fluorescence task` | `[待确认]` | `[待确认]` | `[待确认]` | 主文提到可迁移性 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `AttentionBoost` | `GlaS` | `[待确认]` | `[待确认]` | `[待确认]` |
| `Boundary-loss-adjustment` | `GlaS` | `[待确认]` | `[待确认]` | `[待确认]` |
| `Multi-task` | `GlaS` | `[待确认]` | `[待确认]` | `[待确认]` |
| `Iterative` | `GlaS` | `[待确认]` | `[待确认]` | `[待确认]` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，补充材料明确为了公平比较将参数量对齐`
- 是否统一数据增强：`[待确认]`
- 是否统一后处理：`实例定位模块共享同类流程，但超参数会影响结果`
- 是否统一输入尺寸：`[待确认]`
- 结果来源：`主文 Tables II-VII + 补充材料 Table I 映射`
- 页码：`supp p.5-p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：`GlaS protocol`
- 结果汇报层级：`对象级`
- 实例匹配规则：`F-score 中 overlap >= 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`object-level Hausdorff`
- F1 类型：`object-level F-score`
- 是否含后处理后再报结果：`是，实例定位阶段含 seed growing 与阈值参数`
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：`补充材料对训练时间有 mean+-std，但主表指标当前未抽到`
- 是否和官方 challenge protocol 一致：`是，指标定义沿用 GlaS`
- 页码：`supp p.1-p.2`

---

## 10. 计算量与效率

- 参数量（Params）：`31,387,780`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`约 4844 +- 403 s` [需注意这是表中 network training time，不一定是完整端到端 wall-clock]
- 输入尺寸（计算量对应的）：`未明确`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `AttentionBoost` | `31.39M` | `N/A` | `N/A` |
| `Boundary-loss-adjustment` | `31.38M` | `N/A` | `N/A` |
| `Multi-task` | `31.26M` | `N/A` | `N/A` |
| `Iterative` | `31.39M` | `N/A` | `N/A` |

- 页码：`supp Table I, p.5`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但从 related work 可抽象出三类 hard-pixel 处理路线：
  - `手工定义 boundary-weighting`
  - `额外任务的 multi-task contour/bbox prediction`
  - `error-driven adaptive attention (本文)`

### 11.2 论文指出的研究空白 / Open Problems

1. 预定义 boundary attention 只解决一种错误模式。
2. 不同 hard pixels 可能来自 artifacts 而非 gland geometry，本质上更难手工定义。
3. 单阶段模型难以同时关注不同难度层级的像素子任务。

### 11.3 对我们选题的启示

- 如果我们后续考虑“哪些像素更值得学”而不想显式多任务分支，AttentionBoost 提供了另一条 loss-level 路线。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但关注 gland instance segmentation 作为后续病理形态量化的基础。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 更准确地区分相邻 gland instances，有助于后续 morphology analysis，尤其在含白色 artifacts 和复杂边界的样本中更重要。
- 页码：`p.4262-p.4263`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://cs.bilkent.edu.tr/~gunduz/downloads/AttentionBoost/AttentionBoost.zip`
- 框架/语言：`Python + Matlab (segmentGlands.m)` [网页说明]
- 预训练权重是否提供：`网页说明未写预训练权重`
- 复现难度评估：`中`
- 复现障碍：
  - 主文核心公式与主表数字需要从正式论文全文逐页核对
  - 实例定位阶段参数 `alpha / A_thr` 会显著影响对象级结果
  - 代码跨 Python + Matlab，复现链路略长

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集划分 | 部分 | 仅记录 5-fold / early stopping 痕迹，不脑补 split | 中 |
| 推理阈值 | 部分 | 记录 `alpha`, `A_thr`, `fsize`，但 `alpha` 最优数值待确认 | 高 |
| 后处理细节 | 部分 | 记录 seed growing + majority filter | 中 |
| 训练轮数停止准则 | 是 | `early stopping` | 低 |
| 数据预处理 | 部分 | 当前仅确认任务与实例定位流程 | 中 |

- 不确定但影响较大的点：
  - 正式主文中 Eq.(4) 的 `alpha` 作用形式与最优值
  - GlaS 主结果表的具体数值
  - 训练/验证 split 细节

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 补充材料显示实例定位阶段的 `alpha` 和 `A_thr` 对对象级结果很敏感。
- shared weights 虽可大幅压缩参数量，但性能下降，说明多阶段注意力学习对 stage-specific capacity 有依赖。
- 更大的 shared-weights x2 变体训练时间显著增长。
- 页码：`supp p.2, p.5-p.6`

### 14.2 我们观察到的潜在问题

- 方法虽然不需要预定义“关注边界”，但仍依赖 hand-tuned 的实例定位后处理。
- 多阶段 FCN 的训练和部署成本高于单阶段方法。
- 主文扩展到 nuclei task 说明泛化潜力，但在腺体主任务上的最佳数字当前需要再回原文核对。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`间接展示，强调 boundary artifacts、white artifacts 与 false positives`
- 典型失败场景：
  - `alpha` 太小会产生 under-segmentation
  - `A_thr` 太小会保留 noisy seed regions，产生 false positives
  - artifacts 区域容易被误认为 glands
- 页码：`p.4262-p.4263; supp p.2`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `error-driven pixel reweighting` 的思路
- 不预定义 contour/topology，而让模型自己学习 hard pixels 的路线
- `alpha + A_thr + seed growing` 明确提醒对象级结果高度依赖实例后处理
- GlaS 对象级指标定义整理

### 15.2 可以作为候选参数来源的

- `4 stages`
- `fsize = 3`
- `batch size = 1`
- `AdaDelta`
- `4b32f` 作为主基模命名与对照口径

### 15.3 不应照搬的（及原因）

- 不应直接照搬其多阶段 FCN + Matlab 后处理链路
  - 原因：工程复杂且现代腺体方法多采用更统一的端到端结构
- 不应把所有难点都转成 boosting loss
  - 原因：对 contour/topology 这类明确先验，显式监督仍可能更稳定

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界困难像素处理 | hard pixels 不止 boundary，可用动态像素加权 | 强 |
| 多阶段纠错 | 后续 stage 专门修复前序错误 | 中 |
| 对象级后处理讨论 | `alpha / A_thr / seed growing` 直接影响对象级指标 | 强 |
| related work 论证 | 手工定义 attention 不一定覆盖所有错误模式 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失设计备选路线表`
- [ ] 需要和哪篇论文交叉验证：`03_DCAN.md`, `07_TA-Net.md`, `08_Deep-Multichannel.md`
- [ ] 待确认的问题：`我们是否需要尝试 pixel-wise hard example reweighting，而不是再加一个分支`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | hard pixels 与 artifacts 的实例分割困难 | 任务痛点 |
| related work | boundary-attention 到 adaptive attention 的演进 | 方法脉络 |
| 方法 | boosting 风格动态重加权思路 | 作为 loss 动机来源 |
| 实验设置 | 对象级指标定义、后处理参数敏感性 | 评价与讨论 |
| 讨论 | 多阶段纠错收益与成本 | 解释边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.4263` | boundary hard pixels 与 white artifacts 示例 | 方法动机 |
| `supp Fig. 1` | `supp p.2` | epoch 对对象级指标影响 | 训练动态 |
| `supp Fig. 4` | `supp p.5` | `alpha` / `A_thr` 参数分析 | 后处理敏感性 |
| `supp Table I` | `supp p.5` | 参数量与训练时间 | 成本分析 |
| `supp Fig. 5` | `supp p.6` | shared weights 收敛曲线 | 消融解释 |
| `supp Fig. 6` | `supp p.7` | `3b32f/3b64f/4b64f` 架构图 | base model 参考 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（主文部分细节仍待确认）
- [x] 预处理与数据细节已检查
- [ ] 结果数字与原文 table 一致（主表具体数值仍待核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
