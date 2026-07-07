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

- `classical object-based gland segmentation`
- `attributed graph / object-graph prior`
- `pre-deep-learning baseline`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体任务中很早期的经典传统基线，用 object-graph 显式编码 nucleus / lumen 的组织关系
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Automatic segmentation of colon glands using object-graphs`
- 作者/团队：`Cigdem Gunduz-Demir, Melih Kandemir, Akif Burak Tosun, Cenk Sokmensuer`
- 发表年份/会议/期刊：`2010, Medical Image Analysis`
- DOI / arXiv ID：`10.1016/j.media.2009.09.001`
- BibTeX key：`gunduzdemir2010objectgraphs`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Automatic_Segmentation_of_Colon_Glands_Using_Object-Graphs_2010.pdf`
- 当前定位：`05` 目录里最重要的传统非深度学习基线之一，代表“对象级结构建模优于纯像素阈值/区域生长”的早期路线
- 与已提取论文的关系：
  - 早于 `Semantic Segmentation + TV 2015`、`DCAN 2016`、`MILD-Net 2018`，是典型 pre-deep-learning baseline
  - 与 [05_Structure-Based.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/05_Structure-Based.md) 互补：后者用 morphology maps，本篇用 object-graphs + region growing + decision tree
  - 是后续深度学习方法需要超越的传统参照物，尤其在“抗 stain / sectioning artifact”论证上很有代表性

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：腺体分割是自动分析含腺体结构活检样本的重要第一步，而结直肠腺癌会改变腺体结构本身，因此分割是后续量化分析的前提。
  - 用途：`背景 / 临床意义`
  - 页码：`p.1-p.2`
- 句子/事实 2：相比只使用 pixel-based information，object-based structure 对 staining、fixation 和 sectioning 带来的噪声与伪影更鲁棒。
  - 用途：`方法动机 / 传统方法脉络`
  - 页码：`p.2-p.3, p.11`

#### 1.1.2 related work 可引用句

- 句子/事实 1：本文把早期 gland segmentation 概括为 nucleus-identification、lumina-identification 等 pixel-based 路线，并指出单一阈值和像素级规则难以覆盖不同大小腺体、白色伪影和强烈染色变化。
  - 用途：`方法脉络 / 为什么要引入 object-graph`
  - 页码：`p.1-p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据规模 | `72 images from 36 patients` | 实验设置 | `p.7` |
| 训练/测试 | `24 images (12 patients) / 48 images (24 patients)` | 划分协议 | `p.7` |
| 切片厚度 | `5 um` | 数据细节 | `p.7` |
| 放大倍率 | `20x` | 数据细节 | `p.7` |
| 图像分辨率 | `480 x 640` | 实验设置 | `p.7` |
| 颜色空间 | `RGB -> Lab` | 预处理 | `p.7` |
| area threshold | `10 pixels` | 参数设置 | `p.7` |
| lumen neighbor no. `N` | `5` | 参数设置 | `p.7` |
| nuclei neighbor no. `M` | `10` | 参数设置 | `p.7` |
| small object threshold `P` | `5%` | 参数设置 | `p.7` |
| simplification factor `k` | `5` | 参数设置 | `p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 仅靠 pixel-based nucleus / lumen 阈值和区域生长，难以稳定处理不同大小的腺体。
- fixation 和 sectioning 会在腺体边界附近产生大块白色伪影，容易与真正 luminal regions 混淆。
- stain variation、切片厚度和染料衰减会导致强烈强度分布漂移，无法用单一阈值稳定找到 nucleus pixels。
- 围绕腺体的 nucleus pixels 往往不是闭合链，直接基于像素停止区域生长会漏掉小腺体或产生 flooding。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文先把组织图像分解为 nucleus objects 和 lumen objects 两类圆形 primitive，再围绕这些 object 构建两层 graph：第一层 graph 用于基于局部 object-graph 特征把 lumen objects 分为 gland / non-gland，从而得到初始 gland seeds；第二层 graph 只在 nucleus objects 上建图，用 graph edges 作为 region growing 的停止屏障；随后根据邻近 nuclei 质心构造并简化 polygon 得到 gland boundary，最后再用 outer/inner 区域的 cluster composition 特征训练 decision tree 去除 false glands。

关键页码：

- `p.2-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`object-based graph construction + region growing + decision tree filtering`
- Backbone：`无深度网络；基于 k-means, circle-fit, object-graphs, polygon refinement`
- 输入尺寸：`480 x 640 RGB microscopy image`
- 输出头：`单输出 gland segmentation mask`

### 3.2 关键模块详细描述

**模块 1：`Image decomposition with circular primitives`**

- 位置：`输入预处理阶段`
- 操作流程：
  1. 将图像从 `RGB` 转为 `Lab`
  2. 用 `k-means` 量化为 3 类：`nucleus / stroma / lumen`
  3. 对 nucleus cluster 和 lumen cluster 分别做形态学去噪
  4. 用 `circle-fit algorithm` 把像素集合转成圆形原语
  5. 形成 nucleus objects 与 lumen objects
- 页码：`p.3-p.4`

**模块 2：`Initial gland seed determination`**

- 位置：`第一阶段 graph reasoning`
- 操作流程：
  1. 以所有 nucleus / lumen objects 为节点
  2. 对每个 lumen object，连接其 `N` 个最近的 lumen neighbors 和 `N` 个最近的 nucleus neighbors
  3. 提取本体面积、邻居面积、边长、边夹角等局部 graph features
  4. 用 `k-means` 将 lumen objects 分成两类
  5. 用“平均面积更大的一类更可能在 gland 内部”的规则把两类映射成 `gland / non-gland`
- 页码：`p.4-p.5`

**模块 3：`Gland seed growing with nucleus object-graph`**

- 位置：`第二阶段 region growing`
- 操作流程：
  1. 只在 nucleus objects 上建第二层 graph
  2. 每个 nucleus node 连到其 `M` 个最近邻
  3. 从 initial seeds 开始做 region growing
  4. 当遇到 graph edge 对应的像素时停止生长
  5. 再用基于最大区域面积的比例阈值 `P` 去除过小区域
- 页码：`p.5`

**模块 4：`Boundary detection by nucleus centroids`**

- 位置：`边界重建阶段`
- 操作流程：
  1. 找到 inner region 附近的 nucleus objects
  2. 按与 inner region centroid 的极角对 nuclei centroids 排序
  3. 连接这些点形成 simple polygon
  4. 让每个质心连接其前后 `k` 个邻居，做 polygon simplification 以消除不自然凹陷
  5. 再以最大 nucleus circle 的一半做 dilation，补偿 polygon 只连接质心而未覆盖完整 nuclei 的问题
- 页码：`p.6`

**模块 5：`False gland elimination`**

- 位置：`最终后处理阶段`
- 操作流程：
  1. 将每个候选 gland 分为 outer part 和 inner part
  2. 计算两部分面积以及 nucleus / stroma / lumen 三类 cluster 百分比
  3. 用这些特征训练 supervised decision tree
  4. 在测试图像上应用 learned rules，删除 false glands
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 颜色量化 | `k-means (3 clusters)` | `N/A` | `480 x 640` | nucleus / stroma / lumen |
| primitive extraction | `circle-fit` | `N/A` | 原图 | nucleus objects + lumen objects |
| graph 1 | `lumen+nucleus object-graph` | `N/A` | 原图 | 提取局部 graph features 做 seed 分类 |
| graph 2 | `nucleus object-graph` | `N/A` | 原图 | graph edges 作为生长屏障 |
| boundary detection | `polygon + simplification + dilation` | `N/A` | 原图 | nucleus centroids 重建外边界 |
| false gland filter | `decision tree` | `N/A` | gland-level | 基于 inner/outer cluster features |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
small_region_threshold = P * area(largest_region_in_image)
```

符号说明：
- `P`：gland seed growing 中去除小区域的比例阈值
- 作者选用较小 `P`，因为更大的 false glands 会在后续 decision tree 阶段处理
- 页码：`p.5, p.7`

公式 2：

```text
outer_boundary = dilate(simplified_polygon, 0.5 * largest_nucleus_circle)
```

符号说明：
- `simplified_polygon`：连接按极角排序后的 nuclei centroids 并经过 `k` 邻接简化后的 polygon
- 之所以再做 dilation，是因为 polygon 连接的是 nuclei centroid 而非 nuclei 精确边界
- 页码：`p.6`

公式 3：

```text
features_false_gland = [area_outer, %nucleus_outer, %stroma_outer, %lumen_outer,
                        area_inner, %nucleus_inner, %stroma_inner, %lumen_inner]
```

符号说明：
- 这是 decision tree 的 gland-level 特征集合
- outer part 期望更多 epithelial nuclei，inner part 期望更多 lumina 和 epithelial cytoplasms
- 页码：`p.6-p.7`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇没有深度学习损失或梯度推导，核心是把组织结构知识编码为 object 节点、邻接关系和 gland-level composition features。
- 方法上的关键判断是：object relations 比 raw pixels 更能容忍 stain / sectioning / fixation 噪声。
- 页码：`p.2-p.3, p.11`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `N/A` | `N/A` | 本篇无端到端训练损失 | `N/A` |

### 5.2 总损失公式

```text
N/A
```

### 5.3 权重配置与调度策略

- 各项权重：`N/A`
- 是否衰减/动态调整：`N/A`
- 页码：`本篇为传统规则方法，仅 false gland elimination 使用 decision tree`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Hacettepe colon biopsy dataset` | `24 images, 12 patients` | `48 images, 24 patients` | `未单设验证集` | `72 images from 36 patients` |

### 6.2 数据增强

- 增强列表：
  - `未报告`
  - `本篇无深度学习式 augmentation`
- Patch 提取策略：`无；直接处理整张 480 x 640 图像`
- 页码：`p.7`

### 6.3 优化器与超参数

- 框架：`未报告具体代码框架`
- 优化器：`N/A`
- 初始学习率：`N/A`
- 学习率调度：`N/A`
- Batch size：`N/A`
- Epoch / Steps：`N/A`
- 权重初始化：`N/A`
- 预训练策略：`N/A`
- 是否冻结部分层：`N/A`
- 设备：`Nikon Coolscope Digital Microscope 采图；计算硬件未说明`
- 页码：`p.7`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未做 stain normalization，但将 RGB 转到 Lab 进行后续处理`
- 颜色空间转换：`RGB -> Lab`
- resize / crop / pad 策略：`未报告`
- patch overlap：`N/A`
- 背景过滤策略：`通过 k-means 颜色量化和后续 object reasoning 间接处理`
- 标签生成方式：`manual segmentation as gold standard；false gland labeling 用 gold standard centroid 半自动标注`
- 类别不平衡处理：`未报告`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`按 patient-level 划分 train/test，这是优点；但没有独立 validation set`
- 页码：`p.6-p.7`

---

## 7. 推理与后处理

- 推理时输入尺寸：`480 x 640`
- 概率阈值：`无概率输出`
- 后处理步骤：
  1. 用 object-graph 把 lumen objects 选成 initial gland seeds
  2. 用 nucleus graph edges 阻挡 region growing
  3. 删除过小 grown regions
  4. 根据 nuclei centroids 生成并简化 polygon
  5. 用 decision tree 去除 false glands
- TTA / Test-time refinement：`无`
- 页码：`p.4-p.7`

---

## 8. 消融实验

### 8.1 消融设计

> 本篇没有现代意义上的模块 ablation，但做了两类非常有价值的分析：`false gland elimination` 前后对比，以及 5 个自由参数的系统参数分析。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | 去掉 `false gland elimination` | test `Accuracy 87.59% -> 82.57%`; test `Dice 88.91% -> 84.31%`; sensitivity 上升但 specificity 下降 | decision tree 去假阳性是关键步骤 |
| 2 | 参数扫描 `area threshold / N / M / P / k` | 不同参数影响 sensitivity / specificity 平衡 | object-graph 流程对参数有依赖，但比 pixel-based baseline 更稳 |

### 8.2 各模块贡献量化

- `false gland elimination` 在 test set 上：
  - `Sensitivity: 90.62 -> 85.80`
  - `Specificity: 72.80 -> 89.14`
  - `Accuracy: 82.57 -> 87.59`
  - `Dice: 84.31 -> 88.91`
- 参数敏感性结论：
  - 较小 `M` 会导致 flooding，明显拉低 specificity
  - 较大 `P` 会抬高 specificity 但损害 sensitivity
  - `k` 的影响相对小于其他参数
- 页码：`p.7-p.10`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Training set` | `Sensitivity 83.43 +- 7.73` | `Specificity 92.30 +- 5.78` | `Accuracy 88.00 +- 4.16` | `after FGE` |
| `Training set` | `Dice 88.46 +- 4.62` | `-` | `-` | `after FGE` |
| `Test set` | `Sensitivity 85.80 +- 6.71` | `Specificity 89.14 +- 10.40` | `Accuracy 87.59 +- 5.01` | `after FGE` |
| `Test set` | `Dice 88.91 +- 4.63` | `-` | `-` | `after FGE` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Object-graphs (after FGE)` | `Test set` | `Sensitivity 85.80` | `Accuracy 87.59` | `Dice 88.91` |
| `Object-graphs (before FGE)` | `Test set` | `Sensitivity 90.62` | `Accuracy 82.57` | `Dice 84.31` |
| `Nuclei-identification` | `Test set` | `Sensitivity 53.77` | `Accuracy 53.24` | `Dice 54.33` |
| `Lumina-identification` | `Test set` | `Sensitivity 52.59` | `Accuracy 67.62` | `Dice 59.04` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`不适用，均为传统方法`
- 是否统一数据增强：`不适用`
- 是否统一后处理：`否，三种方法各自有自己的后处理`
- 是否统一输入尺寸：`是，均在相同分辨率图像上评估`
- 结果来源：`原文 Table 1-4`
- 页码：`p.8-p.10`

### 9.4 评价协议与指标定义

- 数据划分来源：`作者自建 patient-level train/test split`
- 结果汇报层级：`training set / test set`
- 实例匹配规则：`无实例匹配；完全 pixel-based evaluation`
- Dice 类型：`pixel-level Dice similarity index`
- Hausdorff 类型：`未报告`
- F1 类型：`未报告 F1`
- 是否含后处理后再报结果：`是，主结果含 false gland elimination`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`是，报告 mean +- std`
- 是否和官方 challenge protocol 一致：`否，早于 GlaS，使用自建数据和像素级指标`
- 页码：`p.7-p.10`

---

## 10. 计算量与效率

- 参数量（Params）：`N/A`
- 计算量（FLOPs / MACs）：`N/A`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`N/A`
- 输入尺寸（计算量对应的）：`480 x 640`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `Object-graphs` | `N/A` | `N/A` | `N/A` |

- 页码：`正文未报告效率`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但文中可抽象出早期 gland segmentation 的三类路线：
  - `nuclei-identification based`
  - `lumina-identification based`
  - `object-based / object-graph based`

### 11.2 论文指出的研究空白 / Open Problems

1. 单纯 pixel-based information 对白色伪影、染色变化和断裂 nuclei chains 不够鲁棒。
2. 需要能表达 object organization 的表示，而不是只看单像素类别。
3. 即使在 object-based 框架下，false gland elimination 依然是必要步骤。

### 11.3 对我们选题的启示

- 这篇很适合在 related work 里作为“结构先验早于深度学习就已证明有效”的证据，说明后续 contour / topology / boundary head 并非凭空出现。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理分级标准论文，但明确指出 adenocarcinomas 会改变 gland architecture，因此 gland segmentation 是疾病量化的前置步骤。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 提供后续 gland-level feature extraction 和 gland classification 的基础设施，可服务于病理客观化分析。
- 页码：`p.1-p.2, p.11`

---

## 13. 开源与复现

- 代码是否开源：`否 / 文中未提供`
- 代码仓库地址：`未提供`
- 框架/语言：`未报告`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中`
- 复现障碍：
  - `circle-fit algorithm` 依赖作者 2009 年前作实现
  - decision tree 的具体规则未逐条列出
  - 多个参数需要在训练集上联合调优
  - 数据集不是公开标准 benchmark

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集划分 | 否 | 仅记录 train/test split | 中 |
| 推理阈值 | 否 | 不适用，规则方法 | 低 |
| 后处理细节 | 部分 | 记录 polygon simplification 与 dilation 思路，不脑补未写半径细节 | 中 |
| 训练轮数停止准则 | 否 | 不适用 | 低 |
| 数据预处理 | 部分 | 记录 `RGB->Lab`, k-means, morphology, circle-fit | 中 |

- 不确定但影响较大的点：
  - `circle-fit` 的细节实现与形态学算子参数
  - decision tree 学到的具体分裂规则
  - 自建数据的获取与复现实验难度

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 虽然 object-based representation 更鲁棒，但仍然需要 false gland elimination 才能获得较高最终精度。
- pixel-based baselines 很难找到一组对所有图像都稳定的参数，而 object-graph 方法虽更稳，但仍依赖参数选择。
- 作者把未来工作指向 gland-level feature extraction、graph / Voronoi-based structural analysis 和 gland classification。
- 页码：`p.8-p.11`

### 14.2 我们观察到的潜在问题

- 方法仍较依赖手工参数和启发式图构建，对更复杂 malignant morphology 的泛化不确定。
- 所有评价都在私有小规模数据上完成，不能直接与后续 `GlaS/CRAG` 时代方法横比。
- decision tree 用 supervised filtering，说明整个 pipeline 并非完全“无监督”。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`间接展示，给出了 pixel-based baselines 的失败可视化和跨图像参数不稳现象`
- 典型失败场景：
  - 纯 pixel-based 方法在白色伪影、断裂 nuclei chains 和大小变化大的 gland 上不稳
  - object-graph 若没有 FGE，容易保留 false glands，specificity 明显下降
- 页码：`Fig. 7-10, p.7-p.11`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 用 object organization 而非 raw pixels 解释腺体结构建模动机
- 用 patient-level split 作为早期病理实验设计的正面例子
- 用 `Accuracy + Dice + Sensitivity + Specificity` 的像素级报告形式整理传统方法对比表
- 用“先生成候选 gland，再做 false positive elimination”的 pipeline 思路组织 related work

### 15.2 可以作为候选参数来源的

- `N = 5`
- `M = 10`
- `P = 5%`
- `k = 5`
- `area threshold = 10 pixels`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其私有数据结果到我们的主比较框架
  - 原因：数据集、指标和任务难度与 `GlaS/CRAG` 不同
- 不应把 decision tree + 手工图规则作为主方法
  - 原因：现代复杂恶性场景下表达能力不足，且参数工程负担大

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 结构先验动机 | nucleus / lumen 组织关系对腺体识别有效 | 强 |
| 边界后处理 | 通过 nuclei centroids + polygon 重建 gland 外边界 | 中 |
| 候选筛除思路 | false gland elimination 显著提高 specificity | 中 |
| related work 写法 | 证明传统 pixel-based baseline 明显弱于结构建模 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`传统方法 related work 对比表`
- [ ] 需要和哪篇论文交叉验证：`05_Structure-Based.md`, `02_Semantic-Segmentation-TVS.md`, `03_DCAN.md`
- [ ] 待确认的问题：`是否要专门整理一节“pre-GlaS 传统方法脉络”`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland architecture 改变需要先做 gland segmentation | 任务背景 |
| related work | pixel-based 到 object-based 的传统演进 | 作为深度学习前史 |
| 方法 | 结构先验与 false positive elimination 的动机 | 只作思想来源，不宣称复现 |
| 实验设置 | patient-level split、像素级指标 | 用于传统方法对比说明 |
| 讨论 | object-based 对 artifact 更鲁棒但仍参数敏感 | 说明传统方法边界 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 3` | `p.4` | 方法总流程示意图 | 整体 pipeline 参考 |
| `Fig. 4` | `p.4` | `circle-fit algorithm` 结果示意 | primitive 定义说明 |
| `Fig. 6` | `p.6` | 单个 lumen object 的 local object-graph features | 图特征说明 |
| `Table 1` | `p.8` | object-graph + FGE 的训练/测试结果 | 主结果引用 |
| `Table 2` | `p.8` | FGE 前结果 | 消融引用 |
| `Table 3` | `p.10` | 训练集与 pixel-based baseline 对比 | 传统方法对比 |
| `Table 4` | `p.10` | 测试集与 pixel-based baseline 对比 | 传统方法对比 |
| `Fig. 8` | `p.9` | 五个自由参数的参数分析 | 参数敏感性说明 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（对本篇而言已转化为算法参数与规则参数）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
