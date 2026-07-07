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
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `representation learning for instance segmentation`
- `skeleton-aware distance transform`
- `watershed-based gland instance extraction`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇虽然方法更通用，但主实验直接放在 histopathology gland instance segmentation 上，且非常贴合“连通性保持 + 复杂形状实例分离”主线
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Structure-Preserving Instance Segmentation via Skeleton-Aware Distance Transform`
- 作者/团队：`Zudi Lin, Donglai Wei, Aarush Gupta, Xingyu Liu, Deqing Sun, Hanspeter Pfister`
- 发表年份/会议/期刊：`2023, MICCAI / arXiv`
- DOI / arXiv ID：`arXiv:2310.05262`
- BibTeX key：`lin2023sdt`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Structure-Preserving_Instance_Segmentation_via_Skeleton-Aware_Distance_Transform_MICCAI_2023.pdf`
- 当前定位：`05` 目录里一篇很值得保留的表示学习论文，不直接换 backbone，而是提出新的实例表示 `SDT`，解决 boundary map 和普通 DT 在复杂腺体结构上的连通性问题
- 与已提取论文的关系：
  - 与 [07_TA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/07_TA-Net.md) 一样都关心 topology / connectivity，但 TA-Net 走多任务监督，本篇直接改实例表示
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/03_DCAN.md) 构成鲜明对照：DCAN 直接预测 boundary，本篇认为 boundary map 很脆弱
  - 与 [12_DEA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/12_DEA-Net.md) 对照：DEA-Net 用结构与注意力救边界，本篇用 representation + watershed 解决 touching instances

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：gland tissues 的结构在显微图像中对癌症诊断和治疗评估非常关键，但它们常常彼此接触且具有非凸、宽度变化大的复杂形状。
  - 用途：`任务背景 / 结构难点`
  - 页码：`p.1-p.2`
- 句子/事实 2：boundary map 容易在 contacting pixels 处因小错误造成明显 connectivity change，而传统 DT 又会在细连接处产生过分割。
  - 用途：`方法动机`
  - 页码：`p.1-p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：SDT 同时融合了 skeleton 在 preserving connectivity 上的优势和 DT 在几何建模上的优势，从而让 boundary 和 topology 同时可辨。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.2-p.4`
- 句子/事实 2：作者强调，相比 FullNet 等基于 boundary 的方法，SDT 从更全局的结构角度推断 instance energy，因此在 Hausdorff 上提升更明显。
  - 用途：`结构表示优势`
  - 页码：`p.7-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据集 | `GlaS, 85 train / 80 test` | 数据集说明 | `p.6-p.7` |
| 评估划分 | `60 normal / 20 abnormal` | 评价协议 | `p.6-p.7` |
| F1 匹配阈值 | `IoU > 0.5` | 评价协议 | `p.6-p.7` |
| alpha | `0.8` | SDT 曲率 | `p.7-p.9` |
| 学习策略 | `classification mode, K=10 bins` | 训练设置 | `p.4-p.7` |
| 输出通道 | `11` | 训练设置 | `p.7` |
| 训练迭代 | `20k` | 训练设置 | `p.7` |
| lr | `5e-4` | 训练设置 | `p.7` |
| momentum | `0.9` | 训练设置 | `p.7` |
| 最佳结果 | `F1 0.931/0.866, Dice 0.919/0.851, Haus 32.29/82.40` | 主结果 | `Table 1, p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- boundary map 是局部二分类表示，对接触像素的小错误非常敏感，容易破坏实例连通性。
- 普通 Euclidean distance transform 虽能区分 interior 和 boundary，但在非凸、细连接、宽度变化大的对象上会出现多个局部极值，导致 over-segmentation。
- histopathology 里的 glands 往往既复杂又紧密接触，因此需要一种同时保边界精度和拓扑连通性的实例表示。

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出 `Skeleton-Aware Distance Transform (SDT)`，把对象 skeleton 引入传统 boundary-based DT 中，形成一张新的 energy map：边界值为 `0`，skeleton 值为 `1`，中间区域平滑插值，从而为每个实例构造一个同时具备明确边界和单峰内部结构的表示。网络直接学习这张 SDT energy map，推理时先对 SDT threshold 得到 skeleton segments，再用 connected component labeling 生成 seeds，最后在反向 SDT 上做 watershed 得到实例 mask，并辅以 hole-filling 与小伪目标去除。

关键页码：

- `p.3-p.6`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`representation learning + watershed-based extraction`
- Backbone：`DeepLabV3 with ResNet backbone`
- 关键设计：
  - `Skeleton-Aware Distance Transform (SDT)`
  - `classification-mode energy prediction`
  - `skeleton-aware instance extraction`
  - `CoordConv`
- 后处理核心：
  - thresholding
  - connected components as seeds
  - watershed on reversed SDT

### 3.2 关键模块详细描述

**模块 1：`SDT Energy Representation`**

- 位置：`核心表示`
- 操作流程：
  1. 计算像素到 boundary 的距离 `d(x, Γb)`
  2. 计算像素到 skeleton 的距离 `d(x, Γs)`
  3. 构造新的 SDT energy
  4. 保证 boundary 为最低值、skeleton 为全局最高值
- 设计目标：同时拥有 precise geometric boundary 和 robust topological connectivity
- 页码：`p.3-p.4`

**模块 2：`Learning Strategy`**

- 位置：`监督方式`
- 操作流程：
  1. 可选回归模式：`L1 / L2`
  2. 可选分类模式：把 `[0,1]` energy 量化到 `K=10` 个 bins
  3. 分类模式加一个背景通道
  4. 用 softmax + cross-entropy 训练
- 作者结论：分类模式更稳、更优
- 页码：`p.4-p.5, p.8-p.9`

**模块 3：`SDT Network`**

- 位置：`主网络`
- 操作流程：
  1. 使用 `DeepLabV3 + ResNet`
  2. 端到端直接预测 SDT energy map
  3. 在 backbone 第 3 stage 前加入 `CoordConv` 注入空间信息
- 页码：`p.4-p.5`

**模块 4：`On-the-Fly Local Skeleton Generation`**

- 位置：`target generation`
- 操作流程：
  1. 所有空间变换之后再计算 local skeleton
  2. 避免 global skeleton 被 crop 后与局部 mask 不一致
  3. 使用 Lee 等人的 skeletonization algorithm
- 设计理由：防止模型 hallucinate 当前视野外的结构
- 页码：`p.5-p.6`

**模块 5：`Skeleton-Aware Instance Extraction`**

- 位置：`推理阶段`
- 操作流程：
  1. threshold SDT，得到 skeleton pixels
  2. 对 skeleton pixels 做 connected component labeling，生成 seeds
  3. 在 reversed SDT energy map 上做 watershed
  4. 最后做 hole-filling 和 small object removal
- 页码：`p.5-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 主干 | `DeepLabV3 + ResNet` | `未逐层明示` | `全图/patch` | 直接学习 energy map |
| CoordConv | spatial encoding layer | `未报告` | backbone stage 3 前 | 注入坐标信息 |
| 输出层 | classification mode | `11 channels` | 同输出 | `10` bins + `1` background |
| 实例提取 | `threshold + CCL + watershed` | `N/A` | 实例级 | reversed SDT 上做 watershed |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
0 = E|Γb < E|Ω\(Γb∪Γs) < E|Γs = 1
```

符号说明：
- `Ω`：实例 mask
- `Γb`：实例 boundary
- `Γs`：实例 skeleton
- 含义：定义理想 energy map 的排序关系，边界最低、骨架最高
- 页码：`Eq.(1), p.3`

公式 2：

```text
E_SDT(x) = ( d(x, Γb) / ( d(x, Γs) + d(x, Γb) ) )^alpha, alpha > 0
```

符号说明：
- `d(x, Γb)`：像素到 boundary 的距离
- `d(x, Γs)`：像素到 skeleton 的距离
- `alpha`：控制 energy surface curvature
- 含义：在 boundary 到 skeleton 之间构造平滑 energy landscape，并确保 skeleton 为唯一全局最大值
- 页码：`Eq.(2), p.3-p.4`

公式 3：

```text
Regression mode:
  predict single-channel energy with L1/L2

Classification mode:
  quantize [0,1] into K bins, add one background channel,
  apply softmax + cross-entropy
```

符号说明：
- `K = 10`
- 作者最终采用 classification mode
- 页码：`p.4-p.5`

公式 4：

```text
Regression background transform:
  y'_i = (1 + b) * sigma(y_hat_i) - b
```

符号说明：
- `b = 0.1`
- 用于让 regression 输出覆盖 `(-b, 1)` 范围，从而与背景区分
- 页码：`p.8-p.9`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 论文没有做严格梯度证明，但给出了非常明确的表示设计逻辑：
  - boundary 的几何辨识能力来自 DT
  - connectivity-preserving 来自 skeleton
- 分类模式优于回归模式，说明把 energy 离散化后再用 cross-entropy 学习更稳健。

---

## 5. 损失函数

### 5.1 各监督项

- 回归模式：
  - `L1`
  - `L2`
- 分类模式：
  - `cross-entropy`

### 5.2 总损失公式

```text
SDT 本身不是传统 segmentation loss，
而是先把实例 mask 映射到 SDT energy space，
再在该空间里用：
1) L1/L2 回归，或
2) cross-entropy 分类
去学习目标表示。
```

说明：

- 最优配置是 quantized energy + `cross-entropy`
- 输出为 `11` 通道：`10` 个能量 bin + `1` 个背景通道

### 5.3 权重配置与调度策略

- `alpha = 0.8`
- `K = 10`
- `b = 0.1` 仅用于 regression mode 的背景偏移

---

## 6. 训练协议

### 6.1 数据集与划分

- 数据集：`GlaS`
- 划分：
  - `85` train
  - `80` test
  - challenge 协议下再分为：
    - `60 normal`
    - `20 abnormal`
- 标注来源：`pathologists`

### 6.2 数据增强

- random brightness
- random contrast
- random rotation
- random crop
- elastic transformation

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| backbone | `DeepLabV3 + ResNet` |
| learning strategy | `classification mode` |
| output channels | `11` |
| iterations | `20k` |
| initial lr | `5e-4` |
| momentum | `0.9` |
| alpha | `0.8` |

### 6.4 预处理与数据细节

- skeleton 在所有空间变换后 on-the-fly 计算，不预先离线缓存
- 为了避免 skeleton 分支过多，先对 mask 做 Gaussian smoothing + thresholding
- 推理时始终在 whole images 上预测，避免局部 skeleton 不一致

---

## 7. 推理与后处理

- 对 SDT energy map 做 threshold
- 得到 skeleton pixels
- connected component labeling 生成 seeds
- 在 reversed SDT 上做 watershed
- 后续做：
  - hole-filling
  - removing small spurious objects

---

## 8. 消融实验

### 8.1 消融设计

- loss / learning mode：
  - `L1`
  - `L2`
  - `CE`
- 曲率参数：
  - `alpha = 0.6`
  - `alpha = 0.8`
  - `alpha = 1.0`
- skeleton 生成策略：
  - `partial`
  - `local`

### 8.2 各模块贡献量化

| 设置 | F1 A | F1 B | Dice A | Dice B | Haus A | Haus B |
|------|------|------|--------|--------|--------|--------|
| `L1` | `0.916` | `0.842` | `0.903` | `0.850` | `39.76` | `94.83` |
| `L2` | `0.896` | `0.833` | `0.885` | `0.837` | `49.11` | `110.24` |
| `CE` | `0.931` | `0.866` | `0.919` | `0.851` | `32.29` | `82.40` |
| `alpha = 0.6` | `0.912` | `0.845` | `0.914` | `0.855` | `36.25` | `91.24` |
| `alpha = 0.8` | `0.931` | `0.866` | `0.919` | `0.851` | `32.29` | `82.40` |
| `alpha = 1.0` | `0.926` | `0.858` | `0.907` | `0.849` | `35.73` | `86.73` |
| `partial skeleton` | `0.899` | `0.831` | `0.896` | `0.837` | `47.50` | `105.19` |
| `local skeleton` | `0.931` | `0.866` | `0.919` | `0.851` | `32.29` | `82.40` |

- 结论：
  - `CE` 优于 `L1/L2`
  - `alpha = 0.8` 整体最优
  - `local skeleton` 明显优于 `partial skeleton`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS Part A` | `F1 = 0.931` | `Dice = 0.919` | `Hausdorff = 32.29` | 最佳或并列最佳 |
| `GlaS Part B` | `F1 = 0.866` | `Dice = 0.851` | `Hausdorff = 82.40` | 最佳 F1 / Hausdorff |

### 9.2 与其他方法的对比

| 方法 | F1 A | F1 B | Dice A | Dice B | Haus A | Haus B |
|------|------|------|--------|--------|--------|--------|
| `DCAN` | `0.912` | `0.716` | `0.897` | `0.781` | `45.42` | `160.35` |
| `MCN` | `0.893` | `0.843` | `0.908` | `0.833` | `44.13` | `116.82` |
| `SPL` | `0.924` | `0.844` | `0.902` | `0.840` | `49.88` | `106.08` |
| `SA` | `0.921` | `0.855` | `0.904` | `0.858` | `44.74` | `96.98` |
| `FullNet` | `0.924` | `0.853` | `0.914` | `0.856` | `37.28` | `88.75` |
| `QSA` | `0.930` | `0.862` | `0.914` | `0.859` | `41.78` | `97.39` |
| `SS` | `0.872` | `0.765` | `0.853` | `0.797` | `54.86` | `116.33` |
| `DT` | `0.918` | `0.846` | `0.896` | `0.848` | `41.84` | `90.86` |
| `SDT` | `0.931` | `0.866` | `0.919` | `0.851` | `32.29` | `82.40` |

- 任务内解读：
  - SDT 在 `5/6` 个指标上达到 SOTA
  - 尤其在 `Hausdorff` 上优势最明显，平均分从 `FullNet 50.15` 降到 `44.82`
  - 作者据此报告对前 SOTA 相对提升 `10.6%`

### 9.3 公平对比条件确认

- 使用标准 `GlaS challenge` 划分与对象级指标
- 对比对象覆盖 boundary map、distance transform、full-resolution 和 suggestive annotation 路线
- 论文还在相同训练设置下额外报告了 `DT` 与 `SS`，使 representation-level 比较更公平

### 9.4 评价协议与指标定义

- 使用 challenge 三指标：
  - `instance-level F1`
  - `Dice index`
  - `Hausdorff distance`
- 解释：
  - `F1`：目标检测正确性
  - `Dice`：实例分割体积重叠
  - `Hausdorff`：形状相似性
- `F1` 的匹配阈值为 `IoU > 0.5`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未报告`
- 间接效率信息：
  - 单模型直接预测 SDT energy，再用简单 watershed 后处理
  - 不需要额外多任务目标
  - classification mode 输出 `11` 通道，代价较可控

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述，但隐含区分了三类实例表示路线：
  - `boundary map`
  - `distance transform`
  - `skeleton-aware distance transform`

### 11.2 论文指出的研究空白 / Open Problems

- 现有实例表示要么几何边界强、要么连通性强，很难兼得
- skeleton 在直接 instance segmentation 中仍未被充分利用
- 后续仍需扩展到更难的 `3D instance segmentation`

### 11.3 对我们选题的启示

- 这篇最重要的启发不是“再加一个分支”，而是“重新定义监督目标本身”，这对你的 shape / topology 设计很有参考价值

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 数据来自 `GlaS`，覆盖 benign 到 malignant 的不同 histological levels，但本文不单独展开病理标准。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 作者明确指出 gland instance segmentation 对临床分析尤其癌症诊断很重要。
- 结构形态的更准确恢复，可提升后续 pathology-oriented morphometrics 的可靠性。

---

## 13. 开源与复现

- 代码是否开源：`正文未提供代码链接`
- 代码仓库地址：`未提供`
- 框架/语言：`CNN segmentation pipeline`，正文未显式写框架
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中`
- 复现障碍：
  - SDT target generation 要自己实现
  - local skeleton 必须在所有空间变换后 on-the-fly 生成
  - watershed extraction 和阈值设置需和文中一致

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 阈值 `theta` | 否 | 仅记录 thresholding，不脑补具体值 | 高 |
| DeepLabV3 具体变体 | 部分 | 记录为 `DeepLabV3 + ResNet` | 中 |
| batch size | 否 | 不假设固定 batch size | 中 |
| 训练框架 | 否 | 不写死实现框架 | 低 |
| watershed 参数 | 否 | 仅记录标准 pipeline | 中 |
| Gaussian smoothing / threshold 参数 | 否 | 只记录有该步骤 | 中 |

- 不确定但影响较大的点：
  - skeleton threshold 与 watershed 细参数
  - CoordConv 插入后的具体通道配置
  - 训练 crop 尺寸

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 当前仅在 2D histopathology instance segmentation 上验证
- 未来计划扩展到更难的 3D instance segmentation

### 14.2 我们观察到的潜在问题

- 方法虽强，但依赖较重的 target engineering 和 on-the-fly skeleton generation
- 对工程实现而言，比直接预测 binary mask 更复杂
- Dice 并非所有子集都绝对最优，例如 Part B Dice 低于 `QSA` 的 `0.859`

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`通过可视化间接展示`
- 定性结论：
  - SDT 更能分离 closely touching objects
  - 对复杂非凸 mask 的 morphology 恢复更准确
  - 相比 FullNet，Hausdorff 明显更低
- 页码：`Fig.5, p.7-p.8`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `shape/topology` 不一定只能做辅助分支，也可以做主监督表示
- `local skeleton + DT` 组合思路
- `threshold + seeds + watershed` 的实例提取流程
- `CE on quantized energy bins` 这一替代回归的训练策略

### 15.2 可以作为候选参数来源的

- `alpha = 0.8`
- `K = 10`
- `20k iterations`
- `lr = 5e-4`
- `momentum = 0.9`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其完整 target generation pipeline
  - 原因：工程链路较复杂，且需要可靠 skeletonization 实现
- 不应只看 Dice 判定优劣
  - 原因：本篇真正优势更体现在 `Hausdorff` 和 morphology preservation
- 不应忽略后处理
  - 原因：watershed-based extraction 是方法有效性的重要组成部分

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 拓扑/骨架监督 | skeleton-aware 表示优于纯 boundary / DT | 强 |
| 复杂形状实例分离 | non-convex, varying width 对象更适合 SDT | 强 |
| 损失设计 | quantized energy + CE 可替代直接回归 | 强 |
| 后处理设计 | skeleton seeds + watershed | 中 |
| 结果解释 | Hausdorff 更能反映结构保真 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`边界_形状_损失支撑`、`主线实验矩阵`
- [ ] 需要和哪篇论文交叉验证：`07_TA-Net.md`, `03_DCAN.md`, `12_DEA-Net.md`
- [ ] 待确认的问题：`我们是否值得尝试把骨架感知目标做成辅助 energy map，而非直接 mask`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | touching glands 与复杂形状实例难点 | 任务痛点 |
| related work | boundary / DT / SDT 表示演进 | 方法脉络 |
| 方法 | skeleton-aware energy representation | 形状监督动机 |
| 实验 | Hausdorff 提升解释 | 指标讨论 |
| 讨论 | topology vs geometry 的平衡 | 结果分析 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.2` | boundary map / DT / SDT 对比 | 方法动机 |
| `Fig. 2` | `p.4` | SDT energy function 示意 | 公式解释 |
| `Fig. 3` | `p.5` | SDT 训练与推理总流程 | 总体架构 |
| `Fig. 4` | `p.5-p.6` | global vs local skeleton 差异 | target generation |
| `Fig. 5` | `p.7` | gland segmentation 可视化对比 | 定性结果 |
| `Table 1` | `p.8` | 与现有方法比较 | 主结果 |
| `Table 2` | `p.8` | loss / alpha / skeleton 消融 | 消融实验 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（阈值与部分后处理参数仍缺）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标出而未脑补
