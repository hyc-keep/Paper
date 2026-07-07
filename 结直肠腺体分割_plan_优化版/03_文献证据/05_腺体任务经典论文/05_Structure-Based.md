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

- `classical morphology-based gland segmentation`
- `structure prior from nuclei spatial arrangement`
- `pre-GlaS deep learning baseline`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体任务中的经典传统方法，代表“基于核空间分布和数学形态学”的非深度学习路线
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`A structure-based approach for colon gland segmentation in digital pathology`
- 作者/团队：`Bassem Ben Cheikh, Philippe Bertheau, Daniel Racoceanu`
- 发表年份/会议/期刊：`2016, Proc. SPIE 9791, Medical Imaging 2016: Digital Pathology`
- DOI / arXiv ID：`10.1117/12.2216545`
- BibTeX key：`cheikh2016structure`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/A_Structure-Based_Approach_for_Colon_Gland_Segmentation_in_Digital_Pathology_2016.pdf`
- 当前定位：`05` 目录里重要的传统基线之一，用“核空间排列 + 数学形态学”替代深网络特征学习，为后续 DCAN/MILD-Net 等深度方法提供对比参照
- 与已提取论文的关系：
  - 早于 `DCAN 2016` 与 `MILD-Net 2018`，属于经典非深度学习腺体分割路线
  - 与 `Automatic Segmentation of Colon Glands Using Object-Graphs 2010` 同属结构先验方法，但本篇更强调 nuclei density / solidity / girth 三类形态学映射
  - 与 `Semantic Segmentation + TV 2015` 互补：后者是早期 CNN 像素分类路线，本篇是纯形态学规则路线

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：肠腺形态既是炎症性肠病严重程度的重要指标，也被病理医生常规用于评估结直肠腺癌的恶性程度和预后。
  - 用途：`背景 / 临床意义`
  - 页码：`p.1`
- 句子/事实 2：该方法只依赖细胞核的空间位置关系而非纹理和颜色，因此在理论上更容易扩展到不同染色方式。
  - 用途：`方法动机 / 泛化性`
  - 页码：`p.1-p.2, p.7`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者将已有工作概括为 active contour、superpixel + random forest、stochastic polygon model 和 object-graphs 等路线，并提出只利用 nuclei spatial positioning 的结构化方案。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.1-p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 图像分辨率 1 | `0.62 um/pixel` | 数据设置 | `p.2-p.3, p.5` |
| 图像分辨率 2 | `0.94 um/pixel` | 数据设置 | `p.5` |
| Warwick 数据量 | `17 images, 255 glands` | 实验设置 | `p.5` |
| APHP 数据量 | `64 images, 1824 glands` | 实验设置 | `p.5` |
| 背景去除 closing 半径 | `r0 = 40 pixels` | 预处理 | `p.2` |
| `RD` | `24 um` | 形态学参数 | `p.5` |
| `RG` | `2.4 um` | 形态学参数 | `p.5` |
| `RS` | `30 um` | 形态学参数 | `p.5` |
| `smax` | `120 um^2` | 形态学参数 | `p.5` |
| solid gland 面积阈值 | `3000 um^2` | 后处理 | `p.4-p.5` |
| 评价协议 | `F1 with >= 50% overlap + object-level Dice` | 评价协议 | `p.5-p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 病理图像中腺体形态变化大，不同病程、不同切割角度和切割位置都会导致外观差异明显。
- 现有方法常依赖特定 stain 的颜色或纹理信息，跨染色和跨数据条件下稳定性有限。
- 腺体既可能表现为中空结构，也可能表现为细胞密集的实性结构，单一规则难以统一处理。
- 需要在不依赖复杂学习器的前提下，仅凭 nuclei spatial arrangement 完成 gland segmentation。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文把腺体分为 `hallow gland` 和 `solid gland` 两类：前者由“无核中心区 + 周围厚上皮层”定义，后者由“核密集簇”定义。方法先做 stain normalization 和 nuclei identification，再从 nuclei binary map 上构建 density map、solidity map 和 girth map，用这些形态学映射分别定位 central-region candidates 与 epithelial layers，最后用形态学重建、closing/opening 和 flood-fill 得到腺体边界，并单独识别 solid glands。

关键页码：

- `p.1-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`classical morphology pipeline`
- Backbone：`无深度网络；基于 k-means + mathematical morphology`
- 输入尺寸：`原始病理图像，文中实验分辨率为 0.62 / 0.94 um/pixel`
- 输出头：`单输出腺体分割掩膜`

### 3.2 关键模块详细描述

**模块 1：`Nuclei objects identification`**

- 位置：`输入预处理与前景提取阶段`
- 操作流程：
  1. 采用 `Reinhard` 方法做 stain normalization
  2. 用白色阈值掩膜和 disk closing 去除大面积背景
  3. 将图像在 `Lab` 空间用 `k-means` 量化为 3 类
  4. 取最蓝的 cluster 作为 nuclei objects
  5. 再根据红色占比阈值去除红细胞和伪影
- 页码：`p.2-p.3`

**模块 2：`Density map for CRC detection`**

- 位置：`gland seed determination`
- 操作流程：
  1. 对 nuclei binary map `IN` 进行多尺度 closing
  2. 将不同半径 closing 结果累加平均，形成 `Dmap`
  3. 对 `Dmap` 像素做 `k-means` 三分类
  4. 将均值最低的类别作为 hallow glands 的 central-region candidates
- 页码：`p.3`

**模块 3：`Solidity map`**

- 位置：`epithelial layer determination`
- 操作流程：
  1. 对 `IN` 进行 opening、geodesic reconstruction 和小连通域移除
  2. 在不同半径 `r` 与不同面积阈值 `s` 上累积
  3. 得到刻画 nuclei objects connectedness / solidity 的 `Smap`
  4. 用于突出厚而实的 epithelial layers
- 页码：`p.3-p.4`

**模块 4：`Girth map`**

- 位置：`epithelial layer determination`
- 操作流程：
  1. 以 CRC mask `L` 为起点做多尺度 dilation
  2. 通过 geodesic reconstruction 衡量 nuclei 对 CRC 的包围关系
  3. 与 `IN` 做 Hadamard product
  4. 累积平均得到 `Gmap`
  5. 与 `Smap` 融合后分类出真正环绕 CRC 的 epithelial layers
- 页码：`p.4`

**模块 5：`Boundary delineation for hallow and solid glands`**

- 位置：`最终分割与后处理阶段`
- 操作流程：
  1. 对 hallow glands：把 epithelial layer 通过 morphological reconstruction 赋予对应 CRC 标签
  2. 对结果做 closing、opening 和 flood-fill，补齐上皮层与中心区间的空隙
  3. 对 solid glands：从 `Smap` 中排除已属于 hallow gland 的上皮层对象
  4. 去除小于 `3000 um^2` 的 nuclei objects
  5. 再做 closing + opening 改善边界
- 页码：`p.4-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 颜色归一化 | `Reinhard in Lab` | `N/A` | 原图 | 跨 stain 稳定化 |
| nuclei 提取 | `k-means (3 clusters)` | `N/A` | 原图 | 最蓝 cluster 作为 nuclei |
| seed 检测 | `density map Dmap` | `N/A` | 原图 | 多尺度 closing 累积 |
| 上皮层检测 | `Smap + Gmap` | `N/A` | 原图 | solidity 与 girth 融合 |
| hallow 分割 | `reconstruction + morphology` | `N/A` | 原图 | closing / opening / flood-fill |
| solid 分割 | `threshold + morphology` | `N/A` | 原图 | 去掉 `< 3000 um^2` 小对象 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Dmap = (1 / RD) * sum_{r=1..RD} Cr(IN)
```

符号说明：
- `IN`：nuclei binary image
- `Cr`：半径为 `r` 的 disk closing
- `RD`：density map 的最大 closing 半径
- 该式用于刻画核空间分布密度，低密度区域更可能对应 hallow gland 中心区
- 页码：`Eq.(1), p.3`

公式 2：

```text
Smap = (1 / (RS * smax)) * sum_{r=1..RS} sum_{s=1..smax} Js(rho_IN(Or(IN)))
```

符号说明：
- `Or(X)`：半径为 `r` 的 opening
- `rho_Y(X)`：图像 `X` 在图像 `Y` 下的 geodesic reconstruction
- `Js`：移除小于面积 `s` 的连通域操作
- `RS`：最大 opening 半径
- `smax`：最大连通域面积阈值
- 该式用于突出厚实、相互连接的 epithelial layer objects
- 页码：`Eq.(2), p.3-p.4`

公式 3：

```text
Gmap = (1 / RG) * sum_{r=1..RG} (rho_IN(delta_r(L)) * IN)
```

符号说明：
- `L`：由 `Dmap` 分类得到的 CRC mask
- `delta_r`：半径为 `r` 的 morphological dilation
- `*`：Hadamard product
- `RG`：girth map 的最大 dilation 半径
- 该式用于衡量 nuclei objects 是否环绕 CRC 分布，从而区分真正上皮层与普通核簇
- 页码：`Eq.(3), p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是损失论文，也没有梯度推导；核心是把 nuclei spatial arrangement 映射为 `density / solidity / girth` 三类形态学表征，再基于规则组合完成分割。
- 多尺度操作的目的在于适配不同大小的 glandular regions 与 epithelial layers。
- 页码：`p.3-p.5`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `N/A` | `N/A` | 本篇不涉及学习型损失 | `N/A` |

### 5.2 总损失公式

```text
N/A
```

### 5.3 权重配置与调度策略

- 各项权重：`N/A`
- 是否衰减/动态调整：`N/A`
- 页码：`本篇为规则方法，无训练损失`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Warwick University / GlaS context` | `未报告训练集` | `17 images, 255 glands` | `未单独设置` | `0.62 um/pixel` |
| `APHP-Sorbonne Univ` | `未报告训练集` | `64 images, 1824 glands` | `未单独设置` | `0.94 um/pixel` |

### 6.2 数据增强

- 增强列表：
  - `未报告`
  - `本篇不是学习型训练框架`
- Patch 提取策略：`未报告，直接在整图分辨率上处理`
- 页码：`p.5`

### 6.3 优化器与超参数

- 框架：`未给实现框架；方法本体为 mathematical morphology + k-means`
- 优化器：`N/A`
- 初始学习率：`N/A`
- 学习率调度：`N/A`
- Batch size：`N/A`
- Epoch / Steps：`N/A`
- 权重初始化：`N/A`
- 预训练策略：`N/A`
- 是否冻结部分层：`N/A`
- 设备：`未报告`
- 页码：`本篇不适用训练型超参数`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`使用 Reinhard stain normalization`
- 颜色空间转换：`Lab color space`
- resize / crop / pad 策略：`未报告 resize；参数以物理尺度 um 给出`
- patch overlap：`N/A`
- 背景过滤策略：`对白色背景阈值化后做 disk closing，r0 = 40 pixels`
- 标签生成方式：`使用已有 gland annotations 做评估，但未展开标注生成流程`
- 类别不平衡处理：`N/A`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`两套数据集都只报告用于评估的图像数，没有提供明确 train/val/test 划分协议`
- 页码：`p.2, p.5`

---

## 7. 推理与后处理

- 推理时输入尺寸：`原始病理图像`
- 概率阈值：`无概率输出`
- 后处理步骤：
  1. 由 `Dmap` 分类得到 CRCs
  2. 由 `(Smap + Gmap) / 2` 分类得到 epithelial layers
  3. 对 hallow glands 做 morphological reconstruction 关联 CRC 与 epithelial layer
  4. 对结果做 closing、opening、flood-fill
  5. 对 solid glands 去除 `< 3000 um^2` 对象后再做 closing + opening
- TTA / Test-time refinement：`无`
- 页码：`p.3-p.5`

---

## 8. 消融实验

### 8.1 消融设计

> 本篇没有标准深度学习式 ablation，主要是通过 map 设计和与其他传统方法的对比来说明方案有效性。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `N/A` | `未报告正式消融` | `N/A` | 论文重点是方法描述与基线比较 |

### 8.2 各模块贡献量化

- `Dmap`：用于定位 hallow glands 的低核密度中心区，文中称 CRC 像素中约 `83%` 位于真正的 hallow gland 区域内。
- `Smap + Gmap`：用于把“实心且厚”的 nuclei objects 和“环绕 CRC”的 nuclei objects 结合，过滤掉 connective tissue nuclei。
- 页码：`p.3-p.4`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `APHP-Sorbonne Univ` | `F1 0.8239` | `Object-Dice 0.8841` | `-` | `Table 1` |
| `Warwick University` | `F1 0.8663` | `Object-Dice 0.9113` | `-` | `Table 1` |
| `Total` | `F1 0.8328` | `Object-Dice 0.8898` | `-` | `Table 1` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Mathematical Morphology` | `literature comparison setting` | `PPV 0.86` | `TPR 0.84` | `ACC 0.74` |
| `active contour [1]` | `literature comparison setting` | `PPV 0.88` | `TPR 0.78` | `ACC 0.70` |
| `superpixel-based approach [2]` | `literature comparison setting` | `n.a.` | `n.a.` | `ACC 0.72` |
| `object-graphs [5]` | `literature comparison setting` | `PPV 0.91` | `TPR 0.85` | `ACC 0.78` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`不适用；均为传统方法`
- 是否统一数据增强：`未说明`
- 是否统一后处理：`否，各方法原始协议不同`
- 是否统一输入尺寸：`未明确`
- 结果来源：`原文 Table 1 / Table 2`
- 页码：`p.5-p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：`作者自有两套健康/良性 H&E 数据，未给出标准 train/test split；更像直接评估口径`
- 结果汇报层级：`dataset-level`
- 实例匹配规则：`F1 采用与 ground truth overlap >= 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`未报告`
- F1 类型：`detection F1`
- 是否含后处理后再报结果：`是`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`Warwick 数据引用了 GlaS challenge 来源，但这里不是官方 2017 challenge 完整测试协议`
- 页码：`p.5-p.6`

---

## 10. 计算量与效率

- 参数量（Params）：`N/A`
- 计算量（FLOPs / MACs）：`N/A`
- 推理时间（ms/image）：`未报告`
- 训练时间（总 GPU-hours）：`N/A`
- 输入尺寸（计算量对应的）：`原始图像`
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `Mathematical Morphology` | `N/A` | `N/A` | `N/A` |

- 页码：`正文未报告效率`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，但可从 related work 中抽象出四类传统路线：`active contour`、`superpixel classification`、`stochastic polygon prior`、`object-graphs / morphology-based structure prior`。

### 11.2 论文指出的研究空白 / Open Problems

1. 依赖颜色和纹理的腺体分割方法往往难以跨 stain 泛化。
2. 单一 gland appearance 假设不足以同时覆盖 hallow glands 与 solid glands。
3. 传统方法在健康/良性组织上可行，但对 cancerous tissues 仍需更强拓扑与空间建模。

### 11.3 对我们选题的启示

- 在深度学习之前，研究者已经明确把“核空间排列”视为 gland segmentation 的核心线索，这对我们后续讨论 boundary / topology / morphology 约束很有价值。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理分级标准论文，但明确把 gland morphology 与 inflammatory bowel disease severity、结直肠腺癌恶性程度和预后联系起来。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 腺体形态的定量分割是后续 morphology analysis、肿瘤分级和预后评估的前提。
- 页码：`p.1`

---

## 13. 开源与复现

- 代码是否开源：`否 / 文中未提供`
- 代码仓库地址：`未提供`
- 框架/语言：`未报告`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中`
- 复现障碍：
  - 多个形态学操作虽然给了公式，但具体实现顺序和边界条件需要自己补齐
  - `k-means` 的初始化、重复次数和终止条件未报告
  - 两套数据集的精确 train/test 协议没有展开，尤其 Warwick 只给了 17 张评估图像

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 验证集划分 | 否 | 仅记录 dataset-level 评估口径 | 高 |
| 推理阈值 | 否 | 不适用，规则方法 | 低 |
| 后处理细节 | 部分 | 记录 closing/opening/flood-fill，但结构元素具体次数未脑补 | 中 |
| 训练轮数停止准则 | 否 | 不适用 | 低 |
| 数据预处理 | 部分 | 记录 `Reinhard + Lab + k-means + background closing` | 中 |

- 不确定但影响较大的点：
  - Warwick 数据是否与后续 `GlaS 2017` 官方 challenge 协议完全同口径
  - `k-means` 与形态学重建的具体实现细节
  - APHP-Sorbonne 数据是否可公开获得

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 方法目前只在健康和良性 H&E colon tissue images 上测试。
- 作者把未来工作指向 graph theory 与 sparse sets mathematical morphology，以便处理 cancerous glandular tissues、不同器官和不同 stains。
- 页码：`p.7`

### 14.2 我们观察到的潜在问题

- 该方法强依赖“无核中心区”与“厚上皮层”假设，对高度破坏、黏连、低分化恶性腺体可能不稳。
- 规则管线可解释，但参数较多，且需要按物理尺度重新标定到不同分辨率。
- 没有官方 GlaS challenge 的 `testA / testB / object-HD` 完整协议，因此与后续深度方法不可直接横比。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未单独做失败案例版块，但给了分割可视化结果`
- 典型失败场景：
  - false positive CRC 在后续上皮层检查前会出现
  - solid glands 与 connective tissue nuclei 的区分依赖 solidity 假设
  - 对复杂癌变组织的泛化尚未验证
- 页码：`p.3-p.7`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 用 `nuclei spatial distribution` 解释腺体结构先验
- 用“中空腺体 / 实性腺体”二分法描述传统 morphology-based segmentation 假设
- 引用 `>= 50% overlap` 的 detection F1 口径作为早期传统方法评价方式
- 把物理尺度参数写成 `um` 而不是固定像素值的思路

### 15.2 可以作为候选参数来源的

- `RD = 24 um`
- `RG = 2.4 um`
- `RS = 30 um`
- `smax = 120 um^2`
- solid gland 去噪阈值 `3000 um^2`

### 15.3 不应照搬的（及原因）

- 不应直接照搬这套规则管线作为主方法
  - 原因：对恶性和复杂场景适应性不足，且与我们当前深度学习路线不一致
- 不应把该文的 Warwick 结果直接与 `GlaS 2017` challenge 主榜单对齐
  - 原因：数据口径和评价协议不完全一致

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界先验讨论 | 腺体可理解为中心区与上皮层的组合结构 | 中 |
| 形态学后处理 | closing / opening / flood-fill 的经典使用方式 | 中 |
| 病理结构动机 | nuclei arrangement 与 gland morphology 强相关 | 强 |
| 指标整理 | 早期传统方法采用 `F1 + object Dice` | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`related work 传统方法脉络表`
- [ ] 需要和哪篇论文交叉验证：`Object-Graphs 2010`, `Semantic Segmentation + TV 2015`, `DCAN 2016`
- [ ] 待确认的问题：`Warwick 17-image 口径与 GlaS 官方拆分的关系`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 腺体形态的临床意义 | 直接用作病理任务背景 |
| related work | 传统 morphology-based / structure-based 路线 | 与 CNN 路线形成前后对照 |
| 方法 | 中心区 + 上皮层的结构先验 | 作为形态学动机来源 |
| 实验设置 | 传统方法的 F1 / object Dice 协议 | 用于整理指标演进 |
| 讨论 | 规则方法对复杂恶性样本的局限 | 解释为何需要深度模型 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.3` | hallow / solid glands 与 nuclei image `IN` | 结构先验说明 |
| `Figure 2` | `p.3` | `Dmap` 与 CRC 示例 | 中心区检测解释 |
| `Figure 3` | `p.4` | `Smap` 与 `Gmap` | 上皮层识别说明 |
| `Figure 4` | `p.4-p.5` | epithelial layers 与最终分割示例 | 后处理流程说明 |
| `Table 1` | `p.6` | 两数据集的 `F1 / Object-Dice` | 主结果引用 |
| `Table 2` | `p.6` | 与 active contour / object-graphs 对比 | 基线对比 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（对本篇而言已转化为算法参数与预处理参数）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [ ] 消融实验的结论已量化（原文无正式消融，已如实标注）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]` 或文字说明
