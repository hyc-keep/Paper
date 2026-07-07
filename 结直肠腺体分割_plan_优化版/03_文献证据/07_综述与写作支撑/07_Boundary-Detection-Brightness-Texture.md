# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [x] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [x] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `boundary detection`
- `brightness + texture`
- `precision-recall / F-measure`
- `local cue combination`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇是自然图像边界检测的经典早期学习式方法，最适合补 `brightness + texture` 联合建模与 `precision-recall / F-measure` 评价链条
- 对当前项目最重要的意义不是方法本身可直接迁移到腺体分割，而是为边界评价与 boundary-aware 叙述提供历史来源
- 本篇至少完成：`1-3, 9, 13-17`

---

## 1. 论文信息

- 论文名：`Learning to Detect Natural Image Boundaries Using Brightness and Texture`
- 作者/团队：`David R. Martin, Charless C. Fowlkes, Jitendra Malik`
- 发表年份/会议/期刊：`2002, NeurIPS`
- DOI / arXiv ID：`未见 DOI`
- BibTeX key：`martin2002boundary`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/Learning_to_Detect_Natural_Image_Boundaries_Using_Brightness_and_Texture_2002.pdf`
- 当前定位：`07` 目录中边界检测发展线的更早节点，适合作为 `Boundary F1 / precision-recall` 与 `brightness + texture` cue combination 的经典来源
- 与已提取论文的关系：
  - 与 [06_Contour-Hierarchical-Segmentation.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/06_Contour-Hierarchical-Segmentation.md) 形成前后衔接：本篇提供早期学习式 boundary detector，后者则将该类 contour benchmark 进一步发展为 `gPb` 与 hierarchical segmentation
  - 与 [05_Active-Contour-Metrics.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/05_Active-Contour-Metrics.md) 互补：本篇偏边界检测与 PR/F-measure，前者偏 segmentation boundary displacement 等指标
  - 与 [04_Metrics-Reloaded.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md) 互补：前者给出现代评价选择原则，本篇提供经典 boundary benchmark 的更早实践背景

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者的目标是仅用局部图像测量，估计某个像素中心是否有 boundary 穿过的 `posterior probability`
  - 用途：`任务定义`
  - 页码：`p.1`
- 句子/事实 2：传统仅依赖 brightness discontinuity 的模型不足以刻画自然图像边界，因为纹理区域内部会产生大量伪响应，而纹理间真实边界又可能在平均亮度上变化很小
  - 用途：`研究动机`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者将 cue combination 明确写成 supervised learning 问题，用多个人工分割自然图像给每个像素打 `on-boundary / off-boundary` 标签
  - 用途：`学习式边界检测`
  - 页码：`p.1-p.2`
- 句子/事实 2：论文通过 `precision-recall curves` 评价 boundary detector，并用 `maximum F-measure` 总结性能
  - 用途：`边界 benchmark 口径`
  - 页码：`p.6-p.7`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 训练图像 | `200` | 数据设置 | `p.5-p.6` |
| 测试图像 | `100` | 数据设置 | `p.5-p.6` |
| 每图人工分割数 | `5-6` | ground-truth 说明 | `p.5-p.6` |
| 方向数 | `12` | OE/TG 计算设置 | `p.2-p.3` |
| 半八度尺度数 | `3` | 多尺度设置 | `p.2-p.3` |
| on-boundary 容差 | `2` pixels + `30` degrees | 标注规则 | `p.5-p.6` |
| 代表结果 | `Human F=.75`, `Us F=.67`, `Nitzberg F=.65`, `Canny F=.57` | detector comparison | `p.6-p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 自然图像中的 boundary detection 不能只理解为亮度突变检测
- 真实边界往往同时体现 brightness 和 texture 的变化
- 传统 `Canny` 式 brightness edge detector 在高纹理区域内部会产生很多假边界
- 反过来，当两个纹理区域平均亮度差异很小时，单看 brightness 又会漏掉真实边界
- 因此作者要做的是：从局部图像 patch 中估计边界后验概率，并以学习方式最优结合多种 cue

对应原文依据（页码）：

- `p.1`

### 2.2 核心思路（一段话概括解法方向）

- 本文提出一种学习式 boundary detector：先分别计算响应 brightness 变化的 `oriented energy (OE)` 与响应 texture 变化的 `texture gradient (TG)`，再通过 localization 过程把这些空间上较宽的响应变成更尖锐的局部峰值，最终将多尺度、多方向的局部特征送入分类器，预测像素为 `on-boundary` 的后验概率。作者以人工分割自然图像构造 ground truth，并用 `precision-recall / F-measure` 证明亮度与纹理联合建模优于经典方法。

关键页码：

- `p.1-p.3`
- `p.5-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 方法由三部分组成：
  1. `OE`：brightness-oriented cue
  2. `TG`：texture-oriented cue
  3. classifier-based cue combination
- 核心输出不是硬分割，而是 boundary posterior probability map

### 3.2 关键模块详细描述

**模块 1：`Oriented Energy (OE)`**

- 用于捕捉 brightness edges
- 作者指出自然图像中的 brightness edge 不只是简单 step，还可能包含 peaks 与 roofs
- OE 用 quadrature pair filters 进行建模，并在多尺度上计算
- 页码：`p.2`

**模块 2：`Texture Gradient (TG)`**

- 用于捕捉纹理差异带来的边界
- 基本做法是在边界方向两侧的半圆盘中统计 texton histogram，并计算二者差异
- 这是相对传统 edge detector 的关键增量
- 页码：`p.2-p.3`

**模块 3：`Localization`**

- 原始 OE/TG 响应在边界附近通常较宽、甚至出现 plateau 或 double peaks
- 作者引入 localization 变换，强调局部最大值，从而提升边界定位质量
- 文中明确说明：localization 对 `TG` 的提升尤其明显
- 页码：`p.3-p.5`

**模块 4：`Cue Combination by Classifiers`**

- 论文把 boundary detection 转成 supervised classification
- 输入是多尺度 OE/TG 特征
- 输出是 boundary posterior probability
- 试验了多种分类器：
  - density estimation
  - classification tree
  - logistic regression
  - quadratic LR
  - boosted LR
  - HME
  - SVM
- 最终作者偏好 logistic regression 及其变体，因为性能接近最好且计算代价低
- 页码：`p.4-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不适合逐层参数表
- 但可整理为“模块-作用”表：

| 模块 | 作用 | 写作价值 |
|------|------|---------|
| `OE` | 捕捉 brightness 结构 | 解释仅靠灰度边缘不够 |
| `TG` | 捕捉 texture 差异 | 支撑 boundary-aware 叙事 |
| `Localization` | 提升边界定位精度 | 解释为何 raw cue 不够 |
| `Classifier` | 学习组合 OE 与 TG | 学习式 cue fusion 早期代表 |
| `PR / F-measure` | 统一评价 detector quality | `Boundary F1` 历史来源 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇最重要的不是完整抄写卷积与距离公式，而是把以下定义讲清：
  - boundary posterior probability
  - `F-measure`
  - PR 曲线下不同 detector 的比较方式
- 论文还明确：
  - `precision` 是检测中真正例的比例
  - `recall` 是所有真实边界中被检测出的比例
  - 用 `2 pixel` 的距离容差允许机器与人工边界间的小定位误差

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不是现代神经网络训练论文
- 但实质上使用 supervised learning 去拟合像素为 `on-boundary` 的概率

### 5.2 总损失公式

- 当前抽取片段未聚焦具体分类器目标函数
- 对当前用途不是重点

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 使用由多名 human subjects 手工分割的自然图像数据
- 文中写明：
  - `200` 张图用于训练与算法开发
  - `100` 张图用于最终结果
  - 每图约 `5-6` 个 human segmentations
- 像素被标为 `on-boundary` 的规则是：
  - 位于任一 human boundary 的 `2 pixels` 内
  - 且方向差在 `30 degrees` 内

### 6.2 数据增强

- 未涉及现代数据增强

### 6.3 优化器与超参数

- 论文测试多种分类器，但不是现代 optimizer/lr 设定写法

### 6.4 预处理与数据细节

- OE 与 TG 在多尺度、多方向上计算
- localization 是关键预处理步骤
- 多个 cue 的联合明显优于单一 cue

---

## 7. 推理与后处理

- 模型在每个像素和方向上估计 boundary posterior probability
- 评价时对所有方向取最大响应
- 最终通过调节 detector threshold 形成 PR 曲线

---

## 8. 消融实验

### 8.1 消融设计

- 文中做了相当清楚的 early-style ablation：
  - raw features vs localized features
  - OE only vs TG only vs OE+TG
  - 不同分类器之间比较

### 8.2 各模块贡献量化

- localization 显著提高 individual features 的质量，尤其对 `TG`
- 多尺度有帮助，但最大增益来自 `OE` 与 `TG` 联合
- 分类器之间差距不大，说明主要收益来自 feature design 与 cue combination 本身

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 任务定义 | 估计像素为 boundary 的 posterior probability | `p.1` |
| 关键方法 | `OE + TG + localization + classifier` | `p.2-p.5` |
| localized 特征效果 | `all F=.67`，优于 raw feature 组合 `all F=.65` | `p.5-p.6` |
| detector comparison | `Human F=.75`, `Us F=.67`, `Nitzberg F=.65`, `Canny F=.57` | `p.6-p.7` |
| 主要结论 | 亮度与纹理联合学习式 detector 明显优于经典亮度边缘方法，但仍低于 human performance | `p.6-p.8` |

### 9.2 与其他方法的对比

- 相比 `Canny`：
  - 本文方法明显更能处理 texture-rich 场景
- 相比 `Nitzberg`：
  - 也获得更高 `F-measure`
- 相比 human：
  - 仍存在显著差距，作者据此指出还需要更高层、全局信息

### 9.3 公平对比条件确认

- 文中明确说对 `Canny` 与 `Nitzberg` 都用 training data 做了公平参数优化
- `Canny` 的主要自由度是 scale
- `Nitzberg` 也在同一数据上重新训练分类器
- 这保证了 Figure 4 的比较不是随意挑参数得出的

### 9.4 评价协议与指标定义

- 本篇是你当前边界评价支撑链里很关键的一环
- 论文明确使用：
  - `precision-recall`
  - `maximum F-measure`
  - distance tolerance for boundary matching
- 这意味着如果你后面要写 `Boundary F1` 的历史来源，可以把它放回：
  - 早期学习式 boundary detection
  - PR / F-measure benchmark
  这条脉络中
- 但也要注意：
  - 本篇是 boundary detection 论文，不是 gland semantic segmentation benchmark
  - 因此它更适合作为指标脉络来源，而不是你主实验分数的直接比较对象

---

## 10. 计算量与效率

- 文中提到作者偏好 logistic regression 及其变体，部分原因是计算成本较低
- 相比之下，SVM 被认为性能略低且计算代价更高、鲁棒性更差
- 对当前项目而言，这一部分只是辅助信息，不是核心价值

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

- 本篇不是综述
- 但它实际上奠定了一条经典 boundary detection 路线：
  - brightness cue alone 不够
  - texture cue 必须进入模型
  - cue combination 应由学习而非手工规则完成
  - PR/F-measure 成为客观评价主口径

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 本篇不涉及病理标准
- 但它对病理图像写作仍有启发：
  - 边界不应只被当作灰度突变
  - 组织纹理、局部结构变化同样是边界证据

---

## 13. 开源与复现

- 代码是否开源：`当前抽取片段未记录`
- 代码仓库地址：`未记录`
- 框架/语言：`未记录`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`中`
- 复现障碍：
  - 需要原始数据集与边界标注
  - 需要完整复现实验中的 OE/TG/filter bank/localization 细节
  - 当前项目不需要完整复现其 detector，只需吸收其指标与方法思想

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 现成代码入口 | 当前抽取片段未保留 | 不做直接复现 | 中 |
| 全部实现超参数 | 部分有，部分未系统整理 | 仅提方法和评价思想 | 中 |
| 与病理分割的直接映射 | 否 | 仅作边界评价链条文献 | 低 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 作者明确承认：
  - 当前方法虽优于已有算法，但与 human performance 仍有显著 gap
  - 要进一步缩小差距，需要加入更高层、全局信息

### 14.2 我们观察到的潜在问题

- 这是自然图像 boundary detection 论文，不是医学图像或病理图像专文
- 其最适合被引用的是：
  - cue combination 的思想
  - PR / F-measure 的评价口径
- 不适合直接拿它来支撑 gland segmentation 的主 benchmark 结论

### 14.3 失败案例 / 定性分析

- 文中最核心的失败分析就是：
  - `Canny` 在纹理区域内部会产生错误响应
  - 单看 texture 又可能在 brightness edge 附近出现 halo-like artifact
  - 因而必须联合 brightness 与 texture，并做 localization

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `Boundary F1 / precision-recall` 的更早历史来源
- brightness 与 texture 联合建模的经典论证
- 边界响应应被理解为 posterior probability map 的早期表述

### 15.2 可以作为候选参数来源的

- 本篇不提供深度分割超参数
- 主要提供 boundary modeling 与 benchmark 思路

### 15.3 不应照搬的（及原因）

- 不应把自然图像 boundary detector 的结果直接映射为病理分割优劣
  - 原因：任务与标注对象不同
- 不应把 `F=.67` 一类结果直接拿来和现代医学分割模型比较
  - 原因：benchmark、数据、任务都不一致
- 不应只引用这篇就宣称边界评价已足够
  - 原因：它本身聚焦的是 boundary detection，不覆盖 region-level segmentation quality

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界评价来源 | `precision-recall / max F-measure` 的早期学习式来源 | 强 |
| boundary-aware 论证 | 边界不能只看亮度，纹理也重要 | 强 |
| discussion | 单一 brightness edge 模型会漏检/误检 | 强 |
| related work | 边界检测从 hand-crafted edge 到 learned cue fusion 的演化 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_实验指标与边界相关工作`
- [ ] 需要和哪篇论文交叉验证：`06_Contour-Hierarchical-Segmentation.md`, `04_Metrics-Reloaded.md`
- [ ] 待确认的问题：`正文是否需要展开 brightness+texture 这条历史线，还是只保留为边界指标的补充依据`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| related work | 早期学习式 boundary detection 路线 | 方法背景 |
| 方法/实验 | `PR / F-measure` 的历史口径 | 指标出处 |
| discussion | 为什么边界不应被简化为纯灰度突变 | 机制解释 |
| 附录 | `Boundary F1` 发展线索 | 辅助证据 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.2-p.3` | raw intensity / OE / TG / localized feature 对比 | cue intuition |
| `Figure 2` | `p.5-p.6` | raw vs localized features 的 PR 曲线 | localization 作用 |
| `Figure 3` | `p.6` | feature combinations 与不同 classifiers 对比 | cue fusion 作用 |
| `Figure 4` | `p.6-p.7` | `Human / Us / Nitzberg / Canny` 的 detector comparison | 代表 benchmark 结果 |

---

## 17. 提取质量自检

- [x] 已提取 `brightness + texture` 联合建模的核心动机
- [x] 已写清 boundary posterior probability 的任务定义
- [x] 已记录 `precision-recall / max F-measure` 的评价口径
- [x] 已记录 `Human / Us / Nitzberg / Canny` 的代表结果
- [x] 已明确它在我们项目中是“边界评价脉络文献”，不是主实验 benchmark
- [x] 与后续 `Contour Detection and Hierarchical Segmentation` 的关系已说明
- [ ] 全部公式逐项校对（当前不需要）
