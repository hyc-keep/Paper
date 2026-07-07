# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [x] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `validation framework`
- `metric recommendation`
- `problem fingerprint`
- `segmentation / detection / classification evaluation writing support`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇不是提出某个单一分割模型，而是提出一套 `problem-aware` 的验证指标选择框架，直接服务你的实验设计、结果表述和 discussion 中的评价协议说明
- 本篇至少完成：`1-3, 9, 11, 13-17`

---

## 1. 论文信息

- 论文名：`Metrics Reloaded: Recommendations for Image Analysis Validation`
- 作者/团队：`Lena Maier-Hein, Annika Reinke, Patrick Godau, Minu D. Tizabi, Florian Buettner, Evangelia Christodoulou, Ben Glocker, Fabian Isensee, Jens Kleesiek, ... , Paul F. Jaeger`
- 发表年份/会议/期刊：`2024, Nature Methods`
- DOI / arXiv ID：`10.1038/s41592-023-02151-z`
- BibTeX key：`maierhein2024metricsreloaded`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/Metrics_Reloaded_Recommendations_for_Image_Analysis_Validation_2024.pdf`
- 当前定位：`07` 目录中专门支撑“实验评价协议与指标选择”的核心文献，可作为你后续写实验 section、metric justification 和 limitation 的总依据
- 与已提取论文的关系：
  - 与 [02_Loss-Survey.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/02_Loss-Survey.md) 形成互补：前者说明 loss 没有 universal best，本篇进一步强调验证 metric 也不能机械跟随训练 loss
  - 与 [01_CRC-AI-Review.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/01_CRC-AI-Review.md)、[03_CRC-Diagnosis-Review-2022.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/03_CRC-Diagnosis-Review-2022.md) 形成“任务地图 + 评估规范”的组合：前两篇定义 CRC 病理任务空间，本篇规定这些任务应如何更规范地验证
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md) 等 benchmark 论文互补：challenge 给出排行榜，本篇解释为什么不同任务不应只看单一分数

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：在生物医学图像分析中，性能指标经常不能真实反映 `domain interest`，这会误导科学进展判断并阻碍方法向实践转化。
  - 用途：`研究动机`
  - 页码：`p.4-p.5`
- 句子/事实 2：指标不是中性的展示数字，而是决定算法是否适合实际应用、并塑造领域研究方向的关键代理量。
  - 用途：`评价协议重要性`
  - 页码：`p.5`

#### 1.1.2 related work 可引用句

- 句子/事实 1：Metrics Reloaded 提出了基于 `problem fingerprint` 的 `problem-aware metric selection` 框架，用结构化方式把 domain interest、target structure、dataset 和 algorithm output 的相关属性编码进指标选择流程。
  - 用途：`评价框架定义`
  - 页码：`p.4, p.7-p.10, p.12-p.13`
- 句子/事实 2：作者明确指出，常见的指标错误主要分为三类：`wrong problem category`、`poor metric selection` 和 `poor metric application`
  - 用途：`评价误用批判`
  - 页码：`p.5-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.1038/s41592-023-02151-z` | 文献信息 | `题录` |
| 期刊卷期页码 | `Nat Methods, 21(2):195-212` | 文献信息 | `题录` |
| 开发方式 | `multi-stage Delphi process` | 框架可信度 | `p.4, p.7, p.12` |
| 国际 workshop 数 | `5` | 共识流程 | `p.9` |
| surveys 数 | `9` | 共识流程 | `p.9` |
| 支持的问题类别 | `4` 类 | 任务分类 | `p.8-p.9` |
| 流程步骤 | `3` 步 | 框架结构 | `p.8-p.9, Fig.2` |
| 主要 pitfall 类别 | `3` 类 | 评价误区框架 | `p.5-p.7, Fig.1` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 自动图像分析领域把大量注意力放在“提出新算法”，却长期低估了“如何正确验证算法”这个问题。
- 在 biomedical image analysis 中，指标经常不能对齐真正的临床/科学目标。
- 同一个问题如果被错误地归类为 segmentation、detection 或 classification，会直接导致验证指标失真。
- 即使问题类别对了，若忽略小目标、边界重要性、层级数据结构、类不平衡、预测分数可用性等属性，也会选错 metric。
- 即使 metric 理论上合适，如果聚合方式、阈值处理、按图像还是按像素统计等应用方式不当，最终结论也会被扭曲。

对应原文依据（页码）：

- `p.4-p.7`

### 2.2 核心思路（一段话概括解法方向）

- 作者提出 `Metrics Reloaded` 这一 problem-aware 验证框架：先把待解决任务映射成一个 `problem fingerprint`，把 domain interest、目标结构特性、数据集属性和算法输出形式等因素结构化编码；再沿着与任务类别匹配的流程，从 image-level classification、object detection、semantic segmentation、instance segmentation 四条路径中选择一组互补指标，并在应用阶段提醒用户避免常见误用。它的核心理念不是“推荐唯一最佳 metric”，而是让指标体系从问题本身出发，而不是从习惯、排行榜或训练 loss 出发。

关键页码：

- `p.4-p.5`
- `p.7-p.10`
- `p.12-p.17`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇不是单一算法，而是一套验证推荐框架
- 从用户视角看，框架分三步：
  1. `Fingerprinting`
  2. `Metric Selection`
  3. `Metric Application`
- 支持四个问题类别：
  - `image-level classification`
  - `object detection`
  - `semantic segmentation`
  - `instance segmentation`

### 3.2 关键模块详细描述

**模块 1：`Problem Fingerprint`**

- 这是全文最重要的新概念
- 它把和 metric 选择相关的属性结构化编码成一组 fingerprint items
- 论文给出的主要 family：
  - `FP1`: problem category
  - `FP2`: domain interest-related properties
  - `FP3`: target structure-related properties
  - `FP4`: dataset-related properties
  - `FP5`: algorithm output-related properties
- 页码：`p.12-p.13`

**模块 2：`Three Pitfall Taxonomy`**

- 作者把常见错误分成三类：
  1. `Inappropriate choice of the problem category`
  2. `Poor metric selection`
  3. `Poor metric application`
- 这是你写实验设计与 limitation 时最容易直接借用的结构
- 页码：`p.5-p.7`

**模块 3：`Semantic Segmentation Recommendation Path`**

- 语义分割不能简单把所有像素展平后套标准分类指标
- 作者建议先按图像计算再聚合，以尊重图像内部像素相关性与层级数据结构
- overlap-based 指标默认可用：
  - `DSC`
  - `IoU`
  - `F_beta`
  - `clDice`（tubular structures）
- 同时通常建议补充 boundary-based 指标，尤其在小结构、形状敏感或边界重要时
- 页码：`p.15-p.16`

**模块 4：`Object Detection Recommendation Path`**

- 检测任务首先要决定 localization criterion 和 assignment strategy
- 由于没有自然定义的 `True Negatives`，`Accuracy / Specificity / AUROC` 这类常见分类指标在 object detection 中可能失效
- 若有连续分数，推荐不要只报单阈值 counting metric，而应补充 multi-threshold metric，如：
  - `AP`
  - `FROC`
- 页码：`p.16-p.17`

**模块 5：`Instance Segmentation Recommendation Path`**

- instance segmentation 同时包含 detection 与 segmentation 两个维度
- 作者建议显式评估 detection performance，并可使用 `Panoptic Quality (PQ)` 作为适合该任务的综合指标
- 若还要评估 matched instances 的 mask 质量，则继续沿 semantic segmentation 流程做 per-instance segmentation metric
- 页码：`p.17`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不适用逐层网络参数表
- 但可直接提炼成“问题类别-推荐关注点”表：

| 问题类别 | 核心风险 | 推荐思路 |
|------|------|---------|
| Image-level classification | 只报单阈值结果或忽略校准 | counting + multi-threshold + calibration 视需求组合 |
| Semantic segmentation | 只看 overlap、忽略边界/小结构 | overlap + boundary，先 per-image 再 aggregate |
| Object detection | 把检测当分割、误用 TN-based metrics | 先 localization，再 assignment，再 detection/classification metrics |
| Instance segmentation | 只看 mask 重叠、忽略 instance awareness | detection metrics + per-instance segmentation metrics，必要时用 `PQ` |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇核心不在新公式，而在 metric selection logic
- 文中提到的重要数学关系与定义层面提醒包括：
  - pixel-level `DSC` 与 `F1 Score` 在数学上等价
  - `IoU` 与 `DSC` 数学上高度相关，很多时候差别更接近 community preference
  - object detection 中缺失 `TN` 会使若干分类指标失效

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不讨论训练损失设计本身
- 但它对 loss 与 metric 的关系给出一个非常重要的原则：
  - 不能因为训练用了 Dice loss，就默认验证也应只用 `DSC`

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 这不是训练论文，因此不报告单一数据集划分
- 它更关注不同 problem fingerprint 对验证协议的影响，例如：
  - class imbalance
  - hierarchical data structure
  - annotation uncertainty
  - target size relative to grid size

### 6.2 数据增强

- 不适用

### 6.3 优化器与超参数

- 不适用

### 6.4 预处理与数据细节

- 论文明确把 `dataset-related properties` 纳入 fingerprint
- 这意味着评估协议不应脱离数据组织方式单独讨论
- 对你来说，最关键的是：
  - 小腺体与大腺体不能假设同一指标敏感性相同
  - patch-level、image-level、WSI-level 结果不能混写成同一种验证

---

## 7. 推理与后处理

- 本篇不讨论模型推理流程
- 但明确强调 metric application 本身也有流程要求：
  - 先确认问题类别
  - 再选 metric pool
  - 再决定 aggregation / thresholding / per-class handling
- 对 segmentation，尤其强调 `per-image -> aggregate` 的应用顺序

---

## 8. 消融实验

### 8.1 消融设计

- 不是单模型论文，不做标准 ablation

### 8.2 各模块贡献量化

- 可量化的不是网络模块增益，而是框架设计决策：
  - 以 `problem fingerprint` 替代经验主义 metric 选择
  - 以多指标互补替代单一指标
  - 以任务类别区分替代把 detection/segmentation/classification 混为一谈

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 核心贡献 | 提出 `Metrics Reloaded` problem-aware metric selection framework | `p.4-p.5` |
| 关键新概念 | `problem fingerprint` 用于编码 metric 选择相关属性 | `p.4, p.12-p.13` |
| 支持任务 | `image-level classification / object detection / semantic segmentation / instance segmentation` | `p.4, p.8-p.9` |
| 核心警告 | 常见错误包括 wrong category、poor selection、poor application | `p.5-p.7` |
| 重要原则 | metric 应由 `domain interest` 决定，而不是由 training loss 倒推 | `p.12` |
| segmentation 建议 | 默认 overlap 指标可用，但通常应补 boundary-based metric | `p.15-p.16` |
| detection 建议 | 无 TN 时不应使用 Accuracy/Specificity/AUROC | `p.16` |
| instance segmentation 建议 | 可使用 `PQ`，同时显式区分 detection 与 segmentation 质量 | `p.17` |

### 9.2 与其他方法的对比

- 这篇不是比较某个新模型，而是在比较“指标选择逻辑”的好坏
- 它对领域常见的坏实践给出直接批评：
  - 把 object detection 当 semantic segmentation 来评估
  - 在 particularly small structures 上仍机械使用 `DSC`
  - 只因为训练用了某个 loss 就验证对应的同名指标
  - 忽略聚合方式导致 metric application 失真

### 9.3 公平对比条件确认

- 本篇的中心思想本身就是“不同问题没有统一单指标公平比较方式”
- 公平对比的前提至少包括：
  - 问题类别一致
  - domain interest 一致
  - target property 与 dataset property 可比
  - aggregation 和 thresholding 规则透明

### 9.4 评价协议与指标定义

- 这是本篇最值得直接复用到你论文里的部分
- 对 gland / lumen / epithelium 这类 semantic segmentation 任务，推荐思路不是只报一个 `Dice`
- 更规范的写法应明确：
  - 任务属于 `semantic segmentation` 还是 `instance segmentation`
  - 是否存在小结构问题
  - 是否关心 boundary quality
  - metric 是按图像统计还是按像素整体统计
  - 是否需要 complementary metrics
- 对你的任务，至少可据此写出：
  - 主要 overlap metric：`Dice` 或 `IoU`
  - 辅助 boundary metric：如有边界质量诉求应补充
  - 若后续做 gland instance analysis，则不能再只用 semantic segmentation 指标

---

## 10. 计算量与效率

- 本篇不以 FLOPs 或 latency 为核心
- 但在 metric pool 的扩展部分明确提到，必要时可加入非 reference-based 指标，例如：
  - speed
  - memory consumption
  - carbon footprint
- 这为后续若要写“方法性能与资源代价平衡”提供了规范依据

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- `Problem category`：
  - image-level classification
  - object detection
  - semantic segmentation
  - instance segmentation
- `Fingerprint family`：
  - FP1 problem category
  - FP2 domain interest
  - FP3 target structure
  - FP4 dataset
  - FP5 algorithm output
- `Pitfall taxonomy`：
  - wrong problem category
  - poor metric selection
  - poor metric application

### 11.2 论文指出的研究空白 / Open Problems

- 领域长期缺乏统一且可解释的 metric selection methodology
- 很多 community 的常用指标沿袭自历史习惯，而非由问题属性严格推出
- 某些有价值的指标在 biomedical image analysis 社区中仍不够常见
- 多类别、层级数据、小结构、噪声标注、复杂临床 trade-off 等场景下，单一指标尤为不足

### 11.3 对我们选题的启示

- 你的工作若是 gland semantic segmentation，就应先明确自己不是 detection，也不是 instance segmentation
- 若论文只报告 Dice，很容易被质疑没有覆盖边界质量、小腺体敏感性和应用相关性
- 如果未来扩展到 gland instance separation、lumen detection 或腺体计数，评价协议必须随任务类型切换
- 这篇文献能让你的实验部分从“报分数”升级为“解释为什么这些分数是合理的”

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 本篇不适用
- 但它提出的 `domain interest` 概念可与病理目标直接对接：
  - 若临床更关心腺体边界完整性，则 boundary metric 更重要
  - 若更关心 gland presence / absence，则 detection-aware metric 更重要
  - 若更关心总体面积重叠，则 overlap metric 更直接

---

## 13. 开源与复现

- 代码是否开源：`提供在线工具`
- 代码仓库地址：`文中提到 Metrics Reloaded online tool`
- 框架/语言：`未在当前提取片段中细述`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`低到中`
- 复现障碍：
  - 真正难点不在代码，而在用户是否能准确完成 problem fingerprint 并理解 trade-off
  - 很多细节依赖 supplementary subprocesses 与 decision guides

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| online tool 具体地址 | 当前抽取片段未保留 | 暂不写入正文主论据 | 低 |
| 所有 subprocess 的完整决策树 | 主文未完整展开 | 以主文原则为主，不脑补细枝末节 | 中 |
| 每种 metric 的统一推荐优先级 | 并非固定唯一排序 | 按任务属性写“推荐思路”而非绝对结论 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 当前主文抽取片段中未见集中列出的“limitations”小节
- 但文中反复暗示：
  - metric selection 需要领域知识
  - 某些场景必须在互补指标之间做 trade-off
  - 框架更像 decision support，而不是一键自动输出唯一答案

### 14.2 我们观察到的潜在问题

- 论文框架很强，但对初学者来说实现门槛不低，因为需要先清楚界定问题类别与 domain interest
- 如果只读主文而不看 supplementary，某些具体 metric 选择路径仍会显得过于抽象
- 对病理图像论文写作来说，最容易复用的是原则层面的规范，而不是完整搬运其全部流程图

### 14.3 失败案例 / 定性分析

- 文中明确举出的典型错误包括：
  - 把 object detection 错当成 semantic segmentation
  - 在 particularly small structures 上仍使用 `DSC` 而忽略其数学局限
  - 用不当 aggregation scheme 应用本来合适的 metric
  - 只根据训练 loss 倒推验证 metric

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `problem-aware metric selection` 的论证框架
- `domain interest should guide metric choice` 这一核心论断
- segmentation / detection / instance segmentation 三类任务不能混用评价协议的写法
- 单一 metric 不足以覆盖复杂 biomedical requirement 的论证

### 15.2 可以作为候选参数来源的

- 本篇不给超参数
- 但给出了 metric 选择时应检查的关键属性：
  - 小结构
  - 边界重要性
  - 类不平衡
  - 预测分数可用性
  - 层级数据结构

### 15.3 不应照搬的（及原因）

- 不应不加区分地把它推荐的所有 metric 都塞进你的实验表
  - 原因：本篇强调的是“问题驱动选择”，不是“指标越多越好”
- 不应把 object detection 或 instance segmentation 的建议直接套到当前 gland semantic segmentation
  - 原因：问题类别不同，metric validity 也不同
- 不应仅用“我们训练用了 Dice loss”作为选择 Dice 的理由
  - 原因：作者明确批评这种从 loss 倒推 validation metric 的习惯

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 实验指标说明 | 指标必须由任务属性和 domain interest 决定 | 强 |
| segmentation 评价 | Dice/IoU 可作为 overlap 指标，但常需补 boundary-aware 视角 | 强 |
| 小腺体分析 | 小结构场景下单独依赖 Dice 可能不稳妥 | 强 |
| loss 与 metric 关系 | 验证指标不应机械跟随训练 loss | 强 |
| discussion | 单指标、错任务类型、错聚合方式都是常见 bad practice | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_实验设置与评价指标`
- [ ] 需要和哪篇论文交叉验证：`02_Loss-Survey.md`, `01_GlaS-Challenge.md`
- [ ] 待确认的问题：`当前主实验是否需要补一个 boundary-based metric 或至少在 discussion 中解释未补的原因`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 指标误用会阻碍临床转化 | 强化“为什么评价协议重要” |
| 方法/实验 | 先定义任务类别，再说明 metric 选择依据 | 规范实验设计 |
| 结果 | 用 complementary metrics 解释不同维度表现 | 避免单分数叙事 |
| 讨论 | 分析小结构、边界、聚合方式与指标局限 | 提升说服力 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.6-p.7` | 三类常见指标 pitfall 与框架如何应对 | 写 bad practice / motivation |
| `Fig. 2` | `p.8-p.9` | 用户视角的三步推荐流程图 | 写方法化叙述 |
| `Fig. 3` | `p.9-p.10` | `problem fingerprint` 结构示意 | 写 metric selection logic |
| `Fig. 4` | `p.11` | 四类问题类别 across modalities/scales | 写任务分类 |
| `Table 1` | `p.17+` | pitfalls 与 recommendation 的对应关系 | discussion / protocol justification |

---

## 17. 提取质量自检

- [x] 所有核心概念都已回到具体原文证据
- [x] 已明确区分本篇是验证框架，不是模型论文
- [x] 四类问题类别与三类 pitfall 已写清
- [x] 与我们项目最相关的 segmentation / small structures / boundary / loss-vs-metric 关系已提炼
- [x] 不确定的在线工具细节没有脑补
- [ ] supplementary 中所有子流程已完整展开（当前未做）
- [x] 已能直接回填实验评价协议写作，而不必再回翻原 PDF
