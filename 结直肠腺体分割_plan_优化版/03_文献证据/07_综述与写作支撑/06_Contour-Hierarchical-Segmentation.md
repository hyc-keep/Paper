# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [x] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `boundary benchmark`
- `precision-recall / F-measure`
- `gPb / OWT-UCM`
- `contour-to-segmentation bridge`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇既是经典 contour detection / segmentation benchmark 论文，也是边界评价口径的重要来源之一
- 对当前项目最重要的价值有两层：
  1. 为 `Boundary F1 / precision-recall` 提供稳固出处
  2. 说明 segmentation 的 region boundaries 可以在 contour benchmark 框架下统一评价
- 本篇至少完成：`1-3, 9, 13-17`

---

## 1. 论文信息

- 论文名：`Contour Detection and Hierarchical Image Segmentation`
- 作者/团队：`Pablo Arbelaez, Michael Maire, Charless Fowlkes, Jitendra Malik`
- 发表年份/会议/期刊：`2011, IEEE Transactions on Pattern Analysis and Machine Intelligence`
- DOI / arXiv ID：`10.1109/TPAMI.2010.161`
- BibTeX key：`arbelaez2011contour`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/Contour_Detection_and_Hierarchical_Image_Segmentation_2011.pdf`
- 当前定位：`07` 目录中最关键的 boundary benchmark 文献之一，适合为 `Boundary F-score / precision-recall / ODS / OIS / AP` 的实验写法提供依据
- 与已提取论文的关系：
  - 与 [04_Metrics-Reloaded.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md) 互补：前者给出现代 problem-aware metric 选择原则，本篇给出边界评价的经典 benchmark 实践
  - 与 [05_Active-Contour-Metrics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/05_Active-Contour-Metrics.md) 形成边界评价链条：前者补 `BDE`，本篇补 `precision-recall / maximum F-measure`
  - 与 [01_GlaS-Challenge.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md) 互补：GlaS 更偏 gland segmentation challenge，本篇更偏 boundary benchmark 方法学与评价口径

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者将 `contour detection` 与 `image segmentation` 统一到同一框架下研究，并强调 segmentation 可被视为由 contour detection 派生而来。
  - 用途：`任务关系定义`
  - 页码：`p.1`
- 句子/事实 2：BSDS benchmark 通过比较 `machine generated contours` 与 `human ground-truth` 来评价算法，并允许把 segmentation 的 region boundaries 也按 contours 进行评价。
  - 用途：`边界评价协议`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：在 `BSDS300` 上，contour detection 与 segmentation 都采用 `precision-recall framework`，并用 `maximum F-measure` 对方法排序。
  - 用途：`benchmark 口径`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者进一步把 `PRI`、`Variation of Information (VI)` 和 `Segmentation Covering` 作为 region quality 的补充指标，说明 segmentation 评价不能只看 boundary PR。
  - 用途：`多维评价`
  - 页码：`p.1, p.12`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DOI | `10.1109/TPAMI.2010.161` | 文献信息 | `题录` |
| 数据集 | `BSDS300`, `BSDS500` | benchmark 设置 | `p.1-p.2, p.12` |
| BSDS300 组成 | `200` train + `100` test | 数据集说明 | `p.2` |
| BSDS500 扩展 | 在 BSDS300 基础上新增 `200` test | 数据集说明 | `p.2` |
| contour benchmark 最佳 `F` | `gPb = 0.70` on BSDS300 | contour 结果 | `p.2` |
| segmentation benchmark 最佳 `F` | `gPb-owt-ucm = 0.71` on BSDS300 | segmentation 结果 | `p.2` |
| BSDS500 boundary ODS/OIS/AP | `0.73 / 0.76 / 0.73` for `gPb-owt-ucm` | boundary 结果 | `p.12-p.15` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- contour detection 与 image segmentation 是计算机视觉中的两个基础问题，但历史上常被分开研究
- contour detector 不保证输出闭合边界，因此不一定天然形成 region partition
- segmentation 则需要闭合区域，但其边界质量又强烈依赖 contour 信号
- 作者试图把两者统一起来：先做好 contour detection，再把 contour signal 变成 hierarchical segmentation
- 论文同时强调：evaluation 也应统一，尤其是 region boundaries 可以放回 contour benchmark 中评价

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 作者提出一个统一框架：用 `gPb` 做高性能 contour detection，再通过 `OWT-UCM` 将 contour signal 转成 hierarchical region tree，从而把 image segmentation 归约为 contour detection 的后续 grouping 问题。在评价上，论文使用 `BSDS300/500` 上的 `precision-recall` 框架，对 contours 和 segment boundaries 做统一 benchmark，并补充 `PRI`、`VI`、`covering` 等 region-level 指标。这使本篇同时成为经典方法论文和边界评价协议文献。

关键页码：

- `p.1-p.2`
- `p.8-p.15`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 论文包含两个核心部分：
  1. `gPb` contour detector
  2. `gPb-owt-ucm` hierarchical segmentation
- 统一思想：
  - contour detection 负责找高质量边界
  - grouping / hierarchy 负责把这些边界变成闭合 region

### 3.2 关键模块详细描述

**模块 1：`gPb`**

- `gPb` 结合多尺度局部 cue 与全局化信息
- 局部 cue 包括：
  - brightness
  - color
  - texture
- 全局化框架基于 spectral clustering
- 作者通过学习方式组合多尺度 cue 与 spectral signal，并以 `F-measure` 为优化目标
- 页码：`p.1, p.6-p.9`

**模块 2：`OWT-UCM`**

- `OWT` 表示 `Oriented Watershed Transform`
- `UCM` 表示 `Ultrametric Contour Map`
- 它把 contour signal 转成 hierarchical region tree
- 对任一阈值，`UCM` 阈值化后都能产生一组闭合 contours，并对应一套 segmentation
- 页码：`p.1, p.9-p.11`

**模块 3：`Boundary Benchmark`**

- 在 BSDS 上，用 `precision-recall` 比较 machine contours 与 human ground-truth
- 论文直接用 `maximum F-measure = 2PR / (P + R)` 排名 contour detectors
- 同一框架也可以评价 segmentation 的 region boundaries
- 页码：`p.1-p.2, p.12`

**模块 4：`Region Benchmarks`**

- 为避免只看 boundary 造成偏差，作者进一步引入：
  - `Probabilistic Rand Index (PRI)`
  - `Variation of Information (VI)`
  - `Segmentation Covering`
- 这说明 segmentation quality 至少要区分 boundary quality 与 region quality
- 页码：`p.1, p.4, p.12`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不适合做逐层网络参数表
- 但可以提炼成“模块-作用”表：

| 模块 | 作用 | 对你写作的价值 |
|------|------|---------------|
| `gPb` | 做 contour detection | 边界 benchmark 主体 |
| `OWT` | 从 contour 生成初始 region | contours -> regions 过渡 |
| `UCM` | 用单张加权边界图编码整个层级分割 | hierarchical segmentation 表达 |
| `PR / F-measure` | 评价 contour 与 region boundaries | `Boundary F1` 来源 |
| `PRI / VI / Covering` | 评价 region quality | 防止只看边界分数 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇最值得直接引用的公式级定义是：
  - `F-measure = 2 * Precision * Recall / (Precision + Recall)`
- 论文还反复使用以下 summary quantities：
  - `ODS`：optimal dataset scale
  - `OIS`：optimal image scale
  - `AP`：average precision，即 PR 曲线下面积
- 对当前项目最有用的不是重推全部 spectral / watershed 公式，而是把这些 benchmark quantity 的含义写清

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不是现代深度学习训练论文
- 但作者提到 cue combination 的权重通过在 BSDS training images 上以 `F-measure` 为目标学习

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 核心 benchmark 是 `BSDS300`
  - `200` training images
  - `100` test images
  - 每张图有多个人工 ground-truth segmentation
- 论文同时发布 `BSDS500`
  - 在 BSDS300 基础上新增 `200` test images
- 多重 human annotation 使其适合作为 contour 与 segmentation 的 benchmark

### 6.2 数据增强

- 未涉及现代数据增强

### 6.3 优化器与超参数

- 未按现代 DL 方式报告 optimizer / lr / batch size

### 6.4 预处理与数据细节

- 多尺度计算是该方法的重要组成部分
- 论文也强调多分辨率计算有助于连接 recognition application

---

## 7. 推理与后处理

- contour detector 输出的是实值 contour signal
- `OWT-UCM` 将其转成 hierarchy
- 通过对 `UCM` 设定不同阈值，可得到不同尺度的 segmentation
- 这正是 `ODS / OIS` 能成立的原因：同一 hierarchy 可以在不同 threshold 下导出不同 segmentation

---

## 8. 消融实验

### 8.1 消融设计

- 本篇不按现代术语做系统 ablation table
- 但明确比较了：
  - local vs multiscale vs spectral globalization
  - contour detector output vs OWT-UCM segmentation output

### 8.2 各模块贡献量化

- `globalization` 提升 contour detection，减少 clutter 并补全 contours
- `OWT-UCM` 把 contours 转成 hierarchical segmentation，同时几乎不损失 boundary benchmark 质量
- 多尺度 cue 对 contour performance 明显优于单尺度

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| contour benchmark | `gPb` 在 BSDS300 上 `F = 0.70`，优于当时主要方法 | `p.2` |
| segmentation benchmark | `gPb-owt-ucm` 在 BSDS300 上 `F = 0.71` | `p.2` |
| BSDS500 boundary | `gPb-owt-ucm` `ODS/OIS/AP = 0.73/0.76/0.73` | `p.12-p.15` |
| region benchmarks | `gPb-owt-ucm` 在 `Covering / PRI / VI` 上也 across-the-board 改善 | `p.1, p.12` |
| 关键结论 | contours 可被转化为 hierarchical segmentations，而不损失 boundary benchmark 表现 | `p.15` |

### 9.2 与其他方法的对比

- contour detection 上，`gPb` 优于：
  - `Pb`
  - `BEL`
  - `Multiscale-Ren`
  - 以及更早的 `Canny / Sobel / Roberts`
- segmentation 上，`gPb-owt-ucm` 优于：
  - `Mean Shift`
  - `NCuts`
  - `Felz-Hutt`
  - `Canny-owt-ucm`
- 这篇的重要意义在于：它不仅给出一个强方法，还顺便确立了边界 benchmark 的经典比较口径

### 9.3 公平对比条件确认

- 使用统一 BSDS ground-truth
- 对 contours 与 segmentation 共享 boundary PR framework
- 同时增加 region metrics，避免只靠单一 benchmark 得出偏结论
- 对 hierarchical segmentation，分别报告：
  - `ODS`
  - `OIS`
  - `AP`

### 9.4 评价协议与指标定义

- 这是本篇对你最直接的价值
- 论文明确支持以下写法：
  - boundary evaluation 用 `precision-recall`
  - summary score 用 `maximum F-measure`
  - `AP` 表示 PR 曲线面积
  - `ODS` 是 dataset-wide 固定阈值下的最优表现
  - `OIS` 是 per-image oracle threshold 下的最优表现
- 更重要的是，它明确说明：
  - segmentation 的 `region boundaries` 可以按 contours 来评价
- 对你当前任务，这意味着如果后面需要解释 `Boundary F1 / Boundary F-score` 的来源，这篇是最稳的经典出处之一

---

## 10. 计算量与效率

- 本篇不是以实时性为主的论文
- 但多分辨率计算与 spectral globalization 说明该方法具有较重计算代价
- 对你来说更重要的是它在 benchmark protocol 上的价值，而不是部署效率

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

- 本篇不是综述
- 但它隐含给出了一套评价层次：
  - contour quality
  - boundary quality of segmentation
  - region quality
  - hierarchical scalability
- 这对你写实验部分非常有用，因为它说明“边界质量好”与“区域划分好”并非完全同一回事

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 本篇不涉及病理标准
- 但其 boundary-centric evaluation 思想可以迁移到病理图像：
  - 当 gland boundary 清晰度很重要时，单一区域 overlap 可能不足
  - 应补充 boundary-aware 视角

---

## 13. 开源与复现

- 代码是否开源：`文中强调 benchmark 和方法实现具有广泛使用价值，但当前抽取片段未单独记录仓库地址`
- 代码仓库地址：`当前未记录`
- 框架/语言：`未单列`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中`
- 复现障碍：
  - 依赖 BSDS 数据与其官方 benchmark 口径
  - 包含 contour detection、spectral clustering、OWT-UCM 等多个组成部分
  - 更适合复用其评价协议和 benchmark 解释，而非在当前项目里完整重现实验

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 当前可直接运行的官方代码入口 | 当前抽取片段未保留 | 不作为立即复现目标 | 中 |
| 所有实现细节与运行配置 | 主文非完整工程手册 | 只提取协议与结果 | 中 |
| 病理分割任务的直接迁移设置 | 否 | 仅把它作为 benchmark 口径来源 | 低 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文并未把局限性集中写成现代格式的小节
- 但全文其实承认：
  - contour detection 与 segmentation 并不完全等价
  - boundary benchmark 不能覆盖所有 region error
  - 因此必须引入 region-based metrics 补充

### 14.2 我们观察到的潜在问题

- 这篇主要基于自然图像 benchmark，不是病理图像专文
- `Boundary F-measure` 来源很强，但不能直接替代 gland segmentation 的医学任务-specific 指标
- 若在你的论文中引用，应注意把它放在“指标来源/评价口径”层，而不是“病理任务直接证据”层

### 14.3 失败案例 / 定性分析

- 论文指出，只看 boundary benchmark 可能漏掉 region-level 的严重错误，例如边界缺一个像素也可能导致大区域错误合并
- 这正是为什么它同时报告 `PRI / VI / covering`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `Boundary F1 / precision-recall / maximum F-measure` 的经典出处
- `ODS / OIS / AP` 三个 benchmark quantity 的清晰定义
- “region boundaries can be evaluated as contours” 这一桥接论断

### 15.2 可以作为候选参数来源的

- 本篇不提供深度模型超参数
- 它给的是 benchmark protocol，而不是训练参数

### 15.3 不应照搬的（及原因）

- 不应把 BSDS 上的自然图像 benchmark 分数直接拿来类比病理分割表现
  - 原因：任务分布与标注属性不同
- 不应只引用这篇就宣称你的 segmentation 评价已经充分
  - 原因：它本身也强调 region metrics 需要补充
- 不应把 `Boundary F1` 当成唯一指标
  - 原因：这篇明确展示 boundary quality 与 region quality 需要分开看

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界指标出处 | `precision-recall / max F-measure / AP` 的 benchmark 口径 | 强 |
| 边界分数解释 | `Boundary F1` 来自经典 BSDS contour benchmark 传统 | 强 |
| 结果分析 | boundary quality 不等同于 region quality | 强 |
| discussion | 为什么还需搭配 region metrics 或 overlap metrics | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_实验指标与边界评价`
- [ ] 需要和哪篇论文交叉验证：`04_Metrics-Reloaded.md`, `05_Active-Contour-Metrics.md`, `01_GlaS-Challenge.md`
- [ ] 待确认的问题：`正文是否需要显式报告 ODS/OIS/AP 风格，还是只保留 Boundary F1 的经典来源说明`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 方法/实验 | `Boundary F1` 的定义来源 | 指标说明 |
| 结果 | `AP / ODS / OIS` 的解释模板 | 结果表注释 |
| 讨论 | boundary 与 region quality 不完全等价 | 指标局限性分析 |
| related work | classic contour benchmark 发展线 | 背景补充 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.2` | BSDS300 contour detector PR benchmark，按 max F 排序 | `Boundary F1` 来源 |
| `Fig. 2` | `p.2` | BSDS300 segmentation algorithm PR benchmark | segmentation boundary 评价 |
| `Fig. 3` | `p.2` | BSDS dataset 与多人工标注示意 | 数据集说明 |
| `Table 1` | `p.12` | BSDS300/500 boundary benchmark，含 `ODS / OIS / AP` | 边界评价协议 |
| `Table 2` | `p.12` | BSDS region benchmark，含 `Covering / PRI / VI` | region 评价补充 |
| `Fig. 17` | `p.15` | BSDS500 boundary benchmark，对比 contour 与 segmentation curves | contours -> segmentation 不失边界质量 |

---

## 17. 提取质量自检

- [x] 已提取 `Boundary F1 / precision-recall / max F-measure` 的核心出处
- [x] 已写清 `ODS / OIS / AP` 的含义
- [x] 已写清本篇既是方法论文也是 benchmark/评价协议文献
- [x] 已明确 `region boundaries` 可在 contour framework 下评价
- [x] 已补充 `PRI / VI / covering` 以避免把本篇误写成“只看边界”
- [x] 与我们项目的引用边界已说明，不会误当病理专文
- [ ] 所有方法细节已完整重建（当前不需要）
