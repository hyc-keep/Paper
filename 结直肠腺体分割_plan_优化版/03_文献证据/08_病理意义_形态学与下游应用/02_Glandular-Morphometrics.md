# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland morphometrics`
- `objective grading`
- `segmentation + handcrafted shape features`
- `CRC pathology downstream application`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是把“腺体分割”真正接到“客观分级”的关键中间节点
- 对当前项目最有价值的是：
  - 明确 gland segmentation 是 grading 的前置步骤
  - 用 `BAM` 把 gland shape aberrance 量化为可分类特征
  - 说明正常 / 低级别 / 高级别之间可通过 gland morphology 区分
  - 同时暴露 image-level split 的潜在乐观偏差风险
- 本篇至少完成：`1-9, 13-17`

---

## 1. 论文信息

- 论文名：`Glandular Morphometrics for Objective Grading of Colorectal Adenocarcinoma Histology Images`
- 作者/团队：`Ruqayya Awan, Korsuk Sirinukunwattana, David Epstein, Samuel Jefferyes, Uvais Qidwai, Zia Aftab, Imaad Mujeeb, David Snead, Nasir Rajpoot`
- 发表年份/会议/期刊：`2017, Scientific Reports`
- DOI / arXiv ID：`10.1038/s41598-017-16516-w`
- BibTeX key：`awan2017glandmorphometrics`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/Glandular_Morphometrics_for_Objective_Grading_of_Colorectal_Adenocarcinoma_Histology_Images_2017.pdf`
- 当前定位：`08` 目录中“腺体形态 -> 客观分级”链条的关键方法论文，说明分割结果可以进一步转成病理上有解释力的 grading feature
- 与已提取论文的关系：
  - 直接承接 [01_CRC-Histological-Characteristics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/08_病理意义_形态学与下游应用/01_CRC-Histological-Characteristics.md)：前者定义 gland formation 与 grade，本篇尝试把这种病理判断算法化
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md) 密切相关：作者显式用 gland segmentation 作为 morphometric grading 的前置条件，并用 GlaS 口径做补充评估
  - 与 [04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md) 等后续腺体方法互补：这些方法提升分割质量后，可进一步服务下游 grading / morphometrics

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：在 colorectal adenocarcinoma 中，grading 部分取决于 morphology 与 glandular structure formation 的程度，而 pathologist 间一致性受主观性影响较大。
  - 用途：`研究动机`
  - 页码：`p.1`
- 句子/事实 2：常用 two-tiered grading 以 gland formation 为核心，`>=50%` glandular 判为 low grade，`<50%` 判为 high grade。
  - 用途：`病理标准`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者提出 `Best Alignment Metric (BAM)` 来量化 gland shape 与正常近圆/近椭圆形态的偏离程度，并证明其与 tumour grade 强相关。
  - 用途：`方法定位`
  - 页码：`p.1-p.3`
- 句子/事实 2：论文明确指出，automatic grading based on gland morphology 的非平凡前提是高质量 gland segmentation。
  - 用途：`为什么分割重要`
  - 页码：`p.2-p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.1038/s41598-017-16516-w` | 文献信息 | `p.1` |
| 期刊卷号/文章号 | `Scientific Reports 7:16852` | 文献信息 | `p.1` |
| WSI 数 | `38` | 数据规模 | `p.6` |
| 扫描分辨率 | `0.275 um/pixel` | 数字病理设置 | `p.6` |
| 图像尺寸 | `4548 x 7548` | patch/field size | `p.6` |
| 放大倍率 | `20x` | 实验设置 | `p.6` |
| 总图像数 | `139` | 数据规模 | `p.6` |
| 类别分布 | `71 normal / 33 low grade / 35 high grade` | 数据分布 | `p.6` |
| two-class accuracy | `97.12 +- 1.27%` | 主结果 | `p.5` |
| three-class accuracy | `90.66 +- 2.45%` | 主结果 | `p.5` |
| High grade F1 | `86.71 +- 4.54%` | 3类细分结果 | `p.6-p.7` |
| Cancer F1 | `97.78 +- 2.27%` | 3类细分结果 | `p.6-p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRA 的 grade 对临床管理有意义，但 pathologist 视觉 grading 具有主观性且耗时。
- 两级分级系统虽然降低了观察者差异，但仍然依赖人工估计 gland formation 比例。
- 如果要把 grading 做成更稳定的计算流程，核心难点有两个：
  - 如何可靠分割 gland boundaries
  - 如何把 gland shape irregularity 量化成与 grade 相关的数值
- 因此本文试图构建一条完整链路：
  - gland segmentation
  - gland shape aberrance computation
  - image-level normal/low-grade/high-grade classification

对应原文依据（页码）：

- `p.1-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文先用改造版 U-Net 对 H&E 结直肠组织图像中的 gland 进行分割，再对每个 gland boundary 计算其与最佳拟合椭圆之间的 `Best Alignment Metric (BAM)`，并在图像层面构造三个 morphometric 特征：平均 BAM、BAM entropy 和 `Regularity Index`。最后用 SVM 做 `normal vs cancer` 和 `normal vs low grade vs high grade` 分类。其核心思想不是端到端直接分级，而是把“病理上依赖 gland formation 的 grading”显式拆成“可解释的分割 + 形态测量 + 分类器”三步。

关键页码：

- `p.1-p.4`
- `p.6-p.10`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 总体流程：
  1. gland segmentation
  2. gland boundary extraction
  3. BAM-based gland aberrance computation
  4. image-level feature aggregation
  5. SVM classification
- 输入：
  - H&E WSI 中抽取的 `4548 x 7548` 视野图像
- 输出：
  - 二分类：`normal vs cancer`
  - 三分类：`normal vs low grade vs high grade`

### 3.2 关键模块详细描述

**模块 1：`Modified U-Net for Gland Segmentation`**

- 位置：整个流程的第一步
- 操作流程：
  1. 对输入图像做 stain normalization 和 patch 切分
  2. 用改造版 U-Net 输出 gland / background probability map
  3. 通过 thresholding 和形态学后处理得到 segmentation mask
- 相比原始 U-Net 的主要改动：
  - 加 batch normalization
  - 去掉 dropout
  - 每层增加 `1 x 1 conv`
  - 用 `Adadelta`
  - 用 weighted cross entropy
- 页码：`p.6-p.9`

**模块 2：`BAM-based Gland Aberrance`**

- 位置：在得到 gland boundary 之后
- 操作流程：
  1. 对每个 gland boundary curve 提取封闭曲线
  2. 计算最小包围椭圆
  3. 将椭圆归一化为圆，并对 gland curve 做对应变换
  4. 在 shape space 上计算 gland 与参考椭圆/圆之间的 `BAM distance`
- 含义：
  - BAM 越大，说明 gland 偏离正常近规则形态越明显
- 页码：`p.9-p.10`

**模块 3：`Image-level Morphometric Features`**

- 三个核心特征：
  - `average BAM`
  - `BAM entropy`
  - `Regularity Index`
- `Regularity Index` 定义：
  - BAM histogram 前两 bins 的 gland 数量占总 gland 数量的比例
- 直觉解释：
  - 正常图像中更多 glands 落在较小 BAM bins
  - 随 tumour 从 low grade 到 high grade 进展，BAM 分布整体右移
- 页码：`p.5`, `p.10`

**模块 4：`SVM Classifier`**

- 位置：最终分类器
- 任务：
  - `normal vs cancer`
  - `normal vs low grade vs high grade`
- 特征集：
  - `Feature Set 1 = average BAM + BAM entropy`
  - `Feature Set 2 = Regularity Index + Feature Set 1`
- 页码：`p.4-p.6`, `p.10`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| modified U-Net | gland segmentation | BN, no dropout, extra `1x1 conv`, Adadelta |
| threshold + morphology | mask clean-up | 去小物体、填孔、分离轻微粘连 gland |
| BAM | gland shape distance | 对 shape space 中曲线与参考椭圆/圆做距离计算 |
| image-level features | morphometric summarization | average BAM, entropy, Regularity Index |
| SVM | grade classification | 2类与3类分类 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：`BAM` 的连续形式

```text
d_BAM([u], [v]) = min_{(r, theta)} ∫ |u(s) - p_theta(v(s + r))| ds
```

符号说明：
- `[u], [v]`：shape equivalence class
- `r`：循环位移
- `theta`：旋转参数
- `p_theta`：平面旋转
- 核心目标：在平移、旋转、重参数化不变条件下比较两条闭合曲线的形状差异

公式 2：离散曲线情况下的 `BAM`

```text
d_BAM([u], [v]) = (1/N) min_{(r, theta)} Σ |u_j - e^(i theta) v_{j+r}|
```

符号说明：
- `N`：曲线离散采样点数
- `u_j, v_j`：离散边界点

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇重点不是梯度推导，而是形状空间上的可解释距离构造
- 关键思想是：
  - 先把 gland 与其最小包围椭圆放到同一“公平比较”坐标系
  - 再比较标准化曲线之间的最优对齐距离
- 这样能弱化切片角度差异，对正常 gland 的近圆/近椭圆结构更稳健

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| weighted cross entropy | 文中未展开完整式 | gland vs background | segmentation network |

### 5.2 总损失公式

```text
L_seg = weighted cross entropy
```

### 5.3 权重配置与调度策略

- 未报告具体 class weight 数值
- 优化器为 `Adadelta`
- 页码：`p.7-p.9`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| UHCW 自建 CRA WSI 视野集 | 共 `139` 张图像 | 通过 `3-fold CV` 轮换 | `3-fold cross-validation` | `71 normal / 33 low grade / 35 high grade` |
| 额外 gland segmentation 训练集 | 初始 `37 normal + 48 tumour` | 未单列 | 用于先训练分割网络 | 后续又从自家 WSI 追加标注 |

### 6.2 数据增强

- 增强列表：
  - flip
  - rotation
  - elastic distortion
- Patch 提取策略：训练与推理均使用 `428 x 428` patch
- 页码：`p.7-p.8`

### 6.3 优化器与超参数

- 优化器：`Adadelta`
- 损失：`weighted cross entropy`
- 训练 patch：`428 x 428`, non-overlapping
- 推理 patch：`428 x 428`, overlapping
- 推理额外 overlap：`25%`
- 分类器：`SVM`
- 页码：`p.6-p.9`

### 6.4 预处理与数据细节

- stain normalization：
  - 使用 `Reinhard stain normalization`
  - 在 `Lab` color space 中匹配均值和标准差
- mean subtraction / scale normalization：
  - 生成 zero mean / unit norm patches
- 扫描器：`Omnyx VL120`
- 扫描分辨率：`0.275 um/pixel`
- magnification：`20x`
- 图像级切分：从 `38` 张 WSI 中抽取非重叠大视野
- 数据泄漏风险点：
  - `3-fold` 划分基于 extracted images，而不是 patient level
  - 同一 WSI 的不同非重叠图像可能同时进入训练和测试
- 页码：`p.6-p.8`

---

## 7. 推理与后处理

- 推理时从大图中抽取重叠 `428 x 428` patches
- 为减少 patch 边界伪影，测试时使用 `25%` 额外 overlap
- patch 输出用 `alpha blending` 融合为整图 segmentation mask
- segmentation postprocessing 包括：
  - thresholding
  - 去除小物体
  - 填孔
  - 分离轻微 merged glands
- 正常图像还额外做 `feature postprocessing`：
  - 去除图像边缘 tangential crypt sections 带来的异常高 BAM

---

## 8. 消融实验

### 8.1 特征集比较

- `Feature Set 1`：`average BAM + BAM entropy`
- `Feature Set 2`：`Regularity Index + Feature Set 1`
- 结果显示加入 `Regularity Index` 后，2类和3类分类都提升

### 8.2 postprocessing 的作用

- feature postprocessing 后：
  - `normal vs cancer` 从 `94.97%` 提升到 `97.12%`
  - `normal vs low grade vs high grade` 从 `88.53%` 提升到 `90.66%`
- 说明边缘 tangential crypt sections 是一个真实且会污染 morphometrics 的误差源

### 8.3 BAM 与普通形状特征比较

- 作者比较了：
  - roundness
  - aspect ratio
  - elongation
  - solidity
  - convexity
- 结论是这些标准形状特征组合都不如 BAM 特征

---

## 9. 主表结果与对比

### 9.1 主结果

| 任务 | 指标 | 数值 | 页码 |
|------|------|------|------|
| `Normal vs Cancer` | accuracy | `97.12 +- 1.27%` | `p.5` |
| `Normal vs Low grade vs High grade` | accuracy | `90.66 +- 2.45%` | `p.5` |
| `High grade` | accuracy | `92.83 +- 3.19%` | `p.6-p.7` |
| `High grade` | precision | `84.08 +- 11.72%` | `p.6-p.7` |
| `High grade` | recall | `91.16 +- 9.10%` | `p.6-p.7` |
| `High grade` | specificity | `93.31 +- 6.57%` | `p.6-p.7` |
| `High grade` | F1-score | `86.71 +- 4.54%` | `p.6-p.7` |
| `Cancer` | accuracy | `97.83 +- 2.17%` | `p.6-p.7` |
| `Cancer` | precision | `97.10 +- 2.52%` | `p.6-p.7` |
| `Cancer` | recall | `98.48 +- 2.62%` | `p.6-p.7` |
| `Cancer` | specificity | `97.16 +- 2.46%` | `p.6-p.7` |
| `Cancer` | F1-score | `97.78 +- 2.27%` | `p.6-p.7` |

### 9.2 统计结论

- `Regularity Index`、average BAM、BAM entropy 在 `normal / low grade / high grade` 三群之间的 Kruskal-Wallis 检验均 `p < 0.001`
- 但 low grade 与 high grade 仍存在明显 overlap，因此三分类比二分类更难

### 9.3 结果解释

- 正常组织中更多 glands 落在小 BAM 值区间
- 从 normal 到 low grade 再到 high grade，BAM histogram 明显向更高 bin 移动
- 这与病理上“gland 形成度下降、结构更不规则”的理解一致

### 9.4 评价协议与指标定义

- 分类任务主要报告：
  - accuracy
  - precision
  - recall
  - specificity
  - F1-score
  - ROC / AUC
- segmentation 不是主表任务，但它是 morphometric 分级的 prerequisite
- 作者还补充将自家分割结果与 `GlaS challenge` top methods 做对照，并指出其对 malignant 图像表现更好

---

## 10. 计算量与效率

- BAM 的一个优点是比许多形状空间 metric 计算更快
- 但文中没有系统报告整条流程的推理时间
- 因此本篇主要价值仍在可解释性，而不是部署效率

---

## 11. 分类体系与研究空白

### 11.1 本篇的方法学定位

- 不是纯 end-to-end grading
- 也不是单纯 segmentation
- 它是：
  - segmentation-driven
  - shape-based
  - interpretable pathology classification

### 11.2 对后续研究的空白提示

- 单靠 gland shape 对 `low grade vs high grade` 的区分仍不够稳，需要额外：
  - lumen features
  - nuclear morphology
  - mitotic rate
  - necrosis extent
- 单张 WSI 往往混有多个 grade，单 patch 分类只是第一步
- 真正的 slide-level grading 还需要 spatial aggregation 与 heterogeneous tumour mapping

---

## 12. 临床/病理标准

- 本篇直接沿用病理上的 two-tiered grading 口径：
  - `>=50%` glandular -> low grade
  - `<50%` glandular -> high grade
- 正常 gland 被视为近圆/近椭圆的规则 tubular structure
- 随 tumour 去分化，gland boundary 更 diffuse、更 irregular
- 因而 gland morphology 的数值化并不是随意设计，而是与病理 grading 标准同源

---

## 13. 开源与复现

### 13.1 论文未报告但复现必需的信息

- 未给出：
  - segmentation 训练 epoch
  - batch size
  - Adadelta 具体参数
  - weighted cross entropy 的权重
  - SVM 核函数与超参数
  - thresholding 的具体阈值
  - 形态学后处理的结构元素参数
- 这些都会显著影响最终 morphometric feature 的稳定性

### 13.2 复现风险与偏差源

- 最大风险是数据划分基于 image 而非 patient：
  - 同一 WSI 不同 non-overlapping regions 可同时进入 train/test
  - 这会引入 slide-level appearance leakage 风险
- 类别数量较少，且 low/high grade 分布接近，统计稳定性有限
- 结果对 segmentation quality 高度敏感；一旦正常 glands 被 merged，就会人为抬高 BAM

### 13.3 数据与代码

- 文中写明：`Data and code will be made available if the paper is accepted`
- 就已发表版本来看，不应默认已稳定公开可得

---

## 14. 局限性与失败案例

- 三分类比二分类明显更难，low grade 与 high grade 特征分布有重叠
- 正常图像中的 tangential crypt sections 会产生异常高 BAM，需要额外后处理
- segmentation 对 benign/normal gland 的处理仍需改进
- 方法 heavily depends on segmentation quality，因此前端误差会直接传导到 grading
- patch/image-level 分级未必等价于真正 slide-level 或 patient-level grading

---

## 15. 对我们项目的落地价值

### 15.1 最直接的启发

- 这篇是“腺体分割不仅能做 mask，还能做病理 grading”的强证据
- 它支持我们在论文中写：
  - gland segmentation 是下游客观形态测量的基础
  - 边界质量和 gland instance separation 直接影响病理可用性

### 15.2 对特征工程和下游任务的启发

- 从分割结果中可进一步提取：
  - gland regularity
  - shape entropy
  - gland formation ratio
  - lumen-related features
  - gland size / elongation / convexity
- 如果后续做 gland grading / morphology-aware classification，可把本篇作为经典可解释基线

### 15.3 对实验设计的提醒

- 若我们以后复现或扩展这条路线，应优先避免：
  - image-level split leakage
  - 仅看二分类高精度而忽略 low/high grade 区分难点
- 更合理的评估应尽量用：
  - patient-level split
  - slide-level aggregation
  - segmentation + grading 联合报告

### 15.4 在整套文献链中的位置

- 这是 `08` 目录里最关键的“形态测量型下游应用”起点
- 后续最自然的承接是：
  - `Segmentation_and_Grade_Prediction_of_Colon_Cancer_Digital_Pathology_Images_Across_Multiple_Institutions_2019`
  - `Automatic_Tumor_Grading_on_Colorectal_Cancer_Whole-Slide_Images_2022`

---

## 16. 关键图表索引

- `Figure 1`
  - 内容：normal / low grade / high grade 示例及正常 gland 结构
  - 用途：写 grade 与 gland 形态关系
  - 页码：`p.2`
- `Figure 2`
  - 内容：segmentation mask 叠加 BAM histogram
  - 用途：最直观展示 BAM 随 grade 增大
  - 页码：`p.5`
- `Figure 4`
  - 内容：Regularity Index、average BAM、BAM entropy 的 boxplots
  - 用途：支撑统计显著性
  - 页码：`p.7`
- `Figure 5`
  - 内容：整体流程图
  - 用途：写 methodology pipeline
  - 页码：`p.7`
- `Figure 6`
  - 内容：modified U-Net architecture
  - 用途：写分割前端
  - 页码：`p.7`
- `Figure 7`
  - 内容：gland aberrance 计算示意
  - 用途：解释 BAM
  - 页码：`p.8`
- `Table 1`
  - 内容：with/without feature postprocessing 的分类准确率
  - 用途：主结果
  - 页码：`p.5`
- `Table 2`
  - 内容：3类分类中 Cancer / High grade 的 precision-recall-F1
  - 用途：补充高等级识别效果
  - 页码：`p.6-p.7`

---

## 17. 提取质量自检

- 本篇全文已抽取并结合关键词、表格数字与方法段落核对，主结果与方法链较完整。
- 重点保留了对当前项目最有价值的几类证据：
  - gland formation 与 grade 的病理对应
  - segmentation -> morphometrics -> grading 的完整路线
  - BAM/Regularity Index 的可解释特征设计
  - image-level split 的潜在偏差风险
- 受 PDF 文本抽取限制，`BAM` 的数学公式排版有轻微噪声，因此这里只保留核心含义与可读形式，不逐字符校对所有数学符号。
- 这篇非常适合作为病理下游应用链的经典节点，但若要复现，仍需补充原始代码或附录参数。
