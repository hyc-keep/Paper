# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [x] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland segmentation challenge`
- `benchmark definition`
- `evaluation protocol`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是 `GlaS` benchmark 的官方协议来源
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 作者/团队：`Korsuk Sirinukunwattana et al.`
- 发表年份/会议/期刊：`2017, Medical Image Analysis`
- DOI / arXiv ID：`arXiv:1603.00275`
- BibTeX key：`sirinukunwattana2017glas`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/GlaS_Challenge_Contest_2017.pdf`
- 当前定位：`GlaS` 数据来源、官方划分、对象级评价协议与 challenge 排名规则的直接出处
- 与已提取论文的关系：
  - 后续 `Semantic Segmentation 2015`、`DCAN 2016`、`MILD-Net 2018` 的 `GlaS` 实验协议都要回到这篇核对 benchmark 口径
  - 与 `TA-Net`、`DEA-Net` 等后续腺体方法互补：它定义 protocol，后者体现方法演进
  - 与早期 `04_结直肠腺体分割_核心25篇文献提取与页码索引.md` 对应：本篇是旧索引里 `GlaS` 卡片的正式模板版展开；当前以本文件为准，旧索引已归档

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：结直肠癌分级依赖 intestinal gland 的形态与 gland formation，但病理判读存在明显观察者间和观察者内一致性问题，自动腺体分割可作为量化 morphology 的解决方案。
  - 用途：`背景 / 临床意义`
  - 页码：`p.1-p.2`
- 句子/事实 2：`GlaS` challenge 的目的是为 routine H&E colon histology 中的 gland segmentation 提供一个 standardized comparison platform。
  - 用途：`数据集意义 / benchmark 动机`
  - 页码：`p.3-p.4`

#### 1.1.2 related work 可引用句

- 句子/事实 1：官方评价强调 gland-level detection、volume-based segmentation accuracy 和 boundary-based similarity，而不是仅看 pixel-level overlap。
  - 用途：`评价协议 / 与普通语义分割的区别`
  - 页码：`p.7-p.10`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 训练量 | `85` | 数据集说明 | `Table 1, p.4` |
| Test Part A | `60` | 数据集说明 | `Table 1, p.4` |
| Test Part B | `20` | 数据集说明 | `Table 1, p.4` |
| 采集倍率 | `20x`, `0.620 um` | 数据集说明 | `p.5-p.6` |
| F1 匹配规则 | overlap `>= 50%` 记为 TP | 评价协议 | `p.8` |
| 排名规则 | `3 metrics x 2 test parts = 6 ranking scores`, 最终取 `rank sum` 最小 | 评价协议 | `p.10` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 结直肠癌病理分级高度依赖腺体形态，但人工分割和人工 grading 一致性有限。
- 不同腺体分割方法长期使用不同数据集和不同评价标准，导致结果不可直接比较。
- 真实腺体任务不仅要求 pixel overlap，还要求实例检测、单个腺体体积接近和边界形状相似。

对应原文依据（页码）：

- `p.1-p.2`
- `p.3-p.4`
- `p.7`

### 2.2 核心思路（一段话概括解法方向）

- 这篇论文的核心不是提出单个新模型，而是通过 `GlaS` challenge 统一数据来源、训练/测试拆分、盲评流程、对象级指标和排名规则，从而给腺体分割提供一个可以复用的 benchmark 基线。

关键页码：

- `p.3-p.4`
- `p.6-p.10`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`benchmark / challenge paper`
- Backbone：`不适用，本篇不是单一方法论文`
- 输入尺寸：`数据集中以 775 x 522 为主，也有 574 x 433、589 x 453、581 x 442 等尺寸`
- 输出头：`不适用`

### 3.2 关键模块详细描述

**模块 1：`Dataset and Split Protocol`**

- 位置：`Section 3`
- 操作流程：
  1. 从 16 张 H&E 染色切片中选取 52 个 visual fields
  2. 标注 benign / malignant，并由专家勾画每个 gland object
  3. 按 histologic grade 和 visual field 分层后拆分为 `Training / Test Part A / Test Part B`
- 页码：`p.4-p.6`

**模块 2：`Evaluation Protocol`**

- 位置：`Section 5-6`
- 操作流程：
  1. 用 `F1` 做 gland detection 评估
  2. 用 `object-level Dice` 做对象级体积评估
  3. 用 `object-level Hausdorff` 做边界相似性评估
  4. 以 `rank sum` 汇总 6 个 ranking scores 得到最终排名
- 页码：`p.7-p.10`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| N/A | N/A | N/A | N/A | 本篇为 challenge / benchmark 论文 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
F1score = 2 * Precision * Recall / (Precision + Recall)
```

符号说明：
- `Precision = TP / (TP + FP)`
- `Recall = TP / (TP + FN)`
- gland 实例与真值重叠至少 `50%` 记为 `TP`
- 页码：`Eq.(1)-(2), p.8`

公式 2：

```text
Diceobj(G, S) = 1/2 * [sum_i gamma_i Dice(G_i, S*(G_i)) + sum_j sigma_j Dice(G*(S_j), S_j)]
```

符号说明：
- `G_i`：第 `i` 个 ground-truth gland
- `S_j`：第 `j` 个 segmented gland
- `gamma_i` 与 `sigma_j`：按对象面积加权
- 页码：`Eq.(4)-(5), p.8-p.9`

公式 3：

```text
Hobj(G, S) = 1/2 * [sum_i gamma_i H(G_i, S*(G_i)) + sum_j sigma_j H(G*(S_j), S_j)]
```

符号说明：
- `H`：对象边界间的 Hausdorff distance
- 未匹配对象会与图中最近对象计算距离
- 页码：`Eq.(8)-(9), p.9-p.10`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不属于损失论文，本节不适用。

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| N/A | N/A | 本篇不定义统一训练损失 | N/A |

### 5.2 总损失公式

```text
N/A
```

### 5.3 权重配置与调度策略

- 本篇为 challenge 协议论文，不提供统一训练损失和权重调度。

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS` | `85` | `60 + 20` | 官方 challenge 不单独给验证集 | `Test Part A` 为 off-site，`Test Part B` 为 on-site |

### 6.2 数据增强

- 增强列表：
  - 本篇不规定统一增强
  - 由各参赛方法自行设计
- Patch 提取策略：`官方不统一规定`
- 页码：`challenge paper 不提供统一训练 recipe`

### 6.3 优化器与超参数

- 框架：`各方法不同`
- 优化器：`各方法不同`
- 初始学习率：`未统一`
- 学习率调度：`未统一`
- Batch size：`未统一`
- Epoch / Steps：`未统一`
- 权重初始化：`未统一`
- 预训练策略：`未统一`
- 是否冻结部分层：`未统一`
- 设备：`Part B 要求在 45 分钟内完成现场测试`
- 页码：`p.6-p.7, p.20-p.21`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`challenge 不统一规定`
- 颜色空间转换：`原始数据为 H&E histology images`
- resize / crop / pad 策略：`由各团队自行设计`
- patch overlap：`不统一`
- 背景过滤策略：`不统一`
- 标签生成方式：`专家逐腺体实例描画边界`
- 类别不平衡处理：`challenge paper 未统一规定`
- 随机种子/重复次数：`未统一`
- 数据泄漏风险点：`同一 visual field 不跨 split，但不是严格 patient-level split，同一 slide 的不同 visual fields 可能进入不同子集`
- 页码：`p.4-p.6`

---

## 7. 推理与后处理

- 推理时输入尺寸：`各团队不同`
- 概率阈值：`官方不统一`
- 后处理步骤：
  1. challenge paper 仅总结常见做法，如 small object removal、fill holes、morphological separation
  2. 具体后处理因方法不同而异
- TTA / Test-time refinement：`未统一规定`
- 页码：`p.15, p.18-p.19`

---

## 8. 消融实验

### 8.1 消融设计

> challenge 论文没有像方法论文那样做模块消融，但做了额外评估与协议偏差分析。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | 将 `Part A / Part B` 分开计分改为合并重评估 | 排名顺序仅局部交换，前三仍为 `CUMedVision2 / ExB1 / ExB3` | 原 challenge 排名总体稳定，但存在 split bias |
| 2 | 用 `ARI` 替代 `object-level Dice` | 排名仅轻微变化 | 对象级评价结论较稳，不依赖单一体积指标 |

### 8.2 各模块贡献量化

- 本篇无单一模型模块消融。
- challenge 层面最有价值的额外分析是：边界分离策略可明显减少 gland merging，`CUMedVision2` 相比 `CUMedVision1` 在 benign / malignant 上都更好。
- 页码：`p.16-p.19`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Test Part A/B` | `F1` | `Object Dice` | `Object Hausdorff` | 最终以 6 个 ranking scores 汇总 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `CUMedVision2` | `Part A / Part B` | `0.912 / 0.716` | `0.897 / 0.781` | `45.418 / 160.347` |
| `ExB1` | `Part A / Part B` | `0.891 / 0.703` | `0.882 / 0.786` | `57.413 / 145.575` |
| `ExB3` | `Part A / Part B` | `0.896 / 0.719` | `0.886 / 0.765` | `57.350 / 159.873` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否`
- 是否统一数据增强：`否`
- 是否统一后处理：`否`
- 是否统一输入尺寸：`否`
- 结果来源：`原文 Table 2`
- 页码：`p.15-p.16`

### 9.4 评价协议与指标定义

- 数据划分来源：`官方 challenge 划分`
- 结果汇报层级：`Training / Test Part A / Test Part B`, 以及合并测试重评估
- 实例匹配规则：`预测 gland 与真值重叠至少 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`object-level Hausdorff distance`
- F1 类型：`gland detection F1`
- 是否含后处理后再报结果：`是，各方法可使用各自后处理`
- 是否多 seed 平均：`未统一规定`
- 是否报告标准差 / 置信区间：`challenge 总表不报标准差`
- 是否和官方 challenge protocol 一致：`是，本篇即官方出处`
- 页码：`p.7-p.10, p.15-p.16`

---

## 10. 计算量与效率

- 参数量（Params）：`未统一报告`
- 计算量（FLOPs / MACs）：`未统一报告`
- 推理时间（ms/image）：`未统一报告`
- 训练时间（总 GPU-hours）：`未统一报告`
- 输入尺寸（计算量对应的）：`各方法不同`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `Challenge entries` | `N/A` | `N/A` | 只要求在 `Part B` 现场测试时间内完成 |

- 页码：`p.6-p.7, p.20-p.21`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，本节不适用。

### 11.2 论文指出的研究空白 / Open Problems

1. 缺少多病理学家标注，未纳入 `inter-observer variability`
2. 缺少多扫描仪数据，未纳入 `inter-scanner variability`
3. 临床部署前还需要多中心大规模验证

### 11.3 对我们选题的启示

- 后续如果要强调泛化与临床可用性，需要把多中心、多扫描仪、多标注者验证当作长期目标。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是分级标准论文，但明确指出 colorectal cancer grading 依赖 gland morphology 和 gland formation。

### 12.2 涉及的生物标志物

- 无直接生物标志物定义。

### 12.3 临床意义

- 分割结果可用于 quantifying gland size、shape 以及定位 gland-specific texture / spatial information。
- 页码：`p.1-p.2, p.20-p.22`

---

## 13. 开源与复现

- 代码是否开源：`否，challenge paper 本身不提供统一代码`
- 代码仓库地址：`无`
- 框架/语言：`各方法不同`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中`
- 复现障碍：
  - 单篇 challenge paper 不给统一训练 recipe
  - 不同参赛方法细节分散在各自论文/补充材料中
  - 若只复现 benchmark protocol 较容易，若想复现冠军方法需转向对应方法论文

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不依赖本篇设定随机种子 | 中 |
| 验证集划分 | 否 | 按官方 train/test 口径引用，本篇不推断内部 val | 中 |
| 推理阈值 | 否 | 不从本篇提具体阈值 | 中 |
| 后处理细节 | 否 | 转向各参赛方法原论文 | 高 |
| 训练轮数停止准则 | 否 | 不把本篇当实现 recipe 来源 | 高 |
| 数据预处理 | 否 | 仅引用官方数据来源与 split，不补写方法级预处理 | 中 |

- 不确定但影响较大的点：
  - `Part A / Part B` 上各方法的具体资源限制并不完全一致
  - 单篇 challenge 总结不足以支撑冠军方法的精确复现

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- ground truth 由单一专家生成，未考虑 `inter-observer variability`
- 未考虑不同扫描设备导致的 `digitization variability`
- object-level Dice 和 object-level Hausdorff 相对严格
- 当前算法尚未准备好直接临床部署
- 页码：`p.20-p.22`

### 14.2 我们观察到的潜在问题

- `Part A (60)` 与 `Part B (20)` 等权计分会引入评价偏差
- challenge 汇总结果不适合拿来推断统一训练 recipe
- 同一 slide 的不同 visual fields 可进入不同 split，存在 patient-level leakage 风险

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是`
- 典型失败场景：
  - lumen 大片白区被误判
  - sub-mucosa 或 dense nuclei 区域与 gland tissue 混淆
  - small glands 漏检
  - touching glands 合并
- 页码：`Figure 4, p.19-p.20`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `GlaS` 数据口径：`85 train / 60 test A / 20 test B`
- 官方主指标：`F1 / Object Dice / Object Hausdorff`
- `20x`、`0.620 um`、按 visual field 分层而非严格按 patient 分层

### 15.2 可以作为候选参数来源的

- `Part A / Part B` 分开汇报的习惯可作为结果表拆分参考
- 合并测试重评估与 `ARI` 补充评估可作为我们讨论阶段的分析思路

### 15.3 不应照搬的（及原因）

- 不应把 challenge 总表当成单模型训练 recipe
  - 原因：本篇不提供统一优化器、增强、阈值和后处理细节
- 不应把官方 split 描述成严格 patient-level split
  - 原因：原文明确否认这一点

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 对象级主指标 | 官方协议直接要求 `F1 / ObjDice / ObjHaus` | 强 |
| `Boundary Head` | challenge 讨论显示 border separation 对 clumped glands 有帮助 | 中 |
| 数据协议说明 | `20x`、visual field stratification、非 patient-level split | 强 |
| 结果解释方式 | 多指标 rank sum 比单指标更稳 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`后续实验设置与结果表说明`
- [ ] 需要和哪篇论文交叉验证：`DCAN 2016`, `MILD-Net 2018`
- [ ] 待确认的问题：`如果后续复现实验采用官方测试集，是否还要补充合并测试重评估`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 腺体分割与 CRC grading 的关系 | 直接引用 benchmark 动机 |
| related work | 为什么对象级指标比像素级指标更重要 | 用于说明任务特殊性 |
| 方法 | 不适合直接支持某个模块公式 | 只作 benchmark 依据 |
| 实验设置 | 数据口径、split、指标定义 | 作为第一出处 |
| 讨论 | split bias、clinical relevance、deployment gap | 用于解释结果边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Table 1` | `p.4` | 官方数据拆分与图像尺寸 | 数据集说明 |
| `Section 5` | `p.7-p.10` | `F1 / Object Dice / Object Hausdorff` 定义 | 指标协议引用 |
| `Table 2` | `p.15` | challenge 主结果与 rank sum | 结果对比 |
| `Figure 4` | `p.19-p.20` | 典型困难样本 | 失败场景讨论 |
| `Figure 5 / Table A` | `p.22-p.23` | 完整 contest 排名 | 补充排名引用 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数无法由本篇统一给出，已明确标注“不适用/未统一”
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 额外分析结论已量化到 split bias 和排名变化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
