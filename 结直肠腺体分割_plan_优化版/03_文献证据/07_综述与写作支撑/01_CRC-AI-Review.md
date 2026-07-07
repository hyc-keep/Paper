# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [x] C - 综述论文（Survey / Review）
- [x] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `systematic review`
- `CRC pathology AI`
- `gland segmentation writing support`
- `clinical/pathology motivation`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇是写 `引言 / related work / 任务价值 / 局限性讨论` 的高价值总览文献，不是单一模型复现对象
- 本篇至少完成：`1-3, 9, 11-16`

---

## 1. 论文信息

- 论文名：`Current Trends of Artificial Intelligence for Colorectal Cancer Pathology Image Analysis: A Systematic Review`
- 作者/团队：`Nishant Thakur, Hongjun Yoon, Yosep Chong`
- 发表年份/会议/期刊：`2020, Cancers`
- DOI / arXiv ID：`10.3390/cancers12071884`
- BibTeX key：`thakur2020crcai`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/Current_Trends_of_Artificial_Intelligence_for_Colorectal_Cancer_Pathology_Image_Analysis_A_Systematic_Review_2020.pdf`
- 当前定位：`07` 目录里最适合率先提取的 CRC 病理 AI 综述，用于给你的论文提供上位背景、任务分类框架和临床价值支撑
- 与已提取论文的关系：
  - 与 [01_PRS2.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/01_PRS2.md) 等任务论文不同：本篇不提供新方法，而是说明为什么 `gland segmentation` 在 CRC pathology AI 中长期占主导
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/03_DCAN.md)、[04_MILD-Net.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md) 和 [08_Deep-Multichannel.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/05_腺体任务经典论文/08_Deep-Multichannel.md) 的关系：这些方法论文都可被本篇纳入 `post-GlaS` 演化脉络中
  - 与 [03_Cerberus.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/06_半监督_拓扑_扩展工作/03_Cerberus.md) 互补：本篇提示 CRC AI 不仅有 gland segmentation，还有 tumor classification、TME 和 prognosis，方便把你的工作挂接到更大病理分析链路中

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CRC 病理诊断存在明显的 `inter-observer / intra-observer variation`，且 Western 与 Eastern pathologists 在诊断标准上仍有差异，因此需要更标准化的辅助工具。
  - 用途：`临床动机`
  - 页码：`p.1-p.2`
- 句子/事实 2：截至 2020 年，CRC pathology AI 研究中最主要的任务仍是 `gland segmentation`，占纳入模型的 `62%`。
  - 用途：`任务定位 / related work 总述`
  - 页码：`p.1, p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：纳入的 40 个模型中，任务分布为 gland segmentation `25` 个、tumor classification `8` 个、TME characterization `4` 个、prognosis prediction `3` 个。
  - 用途：`研究版图`
  - 页码：`p.1, p.3`
- 句子/事实 2：作者明确指出，虽然多数研究结果“看起来很好”，但数据规模、标注质量和外部验证普遍不足，因此距离 routine clinical application 仍有距离。
  - 用途：`局限性 / 讨论`
  - 页码：`p.1, p.9, p.15`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 检索时间范围 | `2000.01 - 2020.01` | 系统综述方法 | `p.1, p.15` |
| 初始检索记录 | `9000` | 综述方法 | `p.1, p.3` |
| 最终纳入记录 | `30` 篇, `40` 个模型 | 综述方法 | `p.1, p.3` |
| gland segmentation | `25` 个模型, `62%` | 任务分布 | `p.1, p.3` |
| tumor classification | `8` 个模型, `20%` | 任务分布 | `p.1, p.3` |
| TME | `4` 个模型, `10%` | 任务分布 | `p.1, p.3` |
| prognosis | `3` 个模型, `8%` | 任务分布 | `p.1, p.3` |
| quantitative gland analysis | `20` 个模型 | 定量比较 | `p.1, p.6-p.7` |
| GlaS challenge teams | `110` | 基准背景 | `p.6, p.10` |
| GlaS 数据 | `165` patches / `16` CRC WSIs | 数据集说明 | `p.10` |
| Ding 2019 rank-sum | `overall rank 1` | 主结论 | `p.1, p.7` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRC 是全球高负担癌种，早期病理诊断对降低死亡率非常关键。
- 结直肠活检病理诊断存在：
  - 组织样本小
  - cauterization artifacts
  - regenerative atypia
  - pathologist 之间标准不一致
- Western 与 Eastern 的病理诊断体系存在差异，尤其在 carcinoma 定义上一个更依赖 invasion，一个更依赖 glandular / nuclear atypia。
- 因此，需要系统回顾 AI 在 CRC pathology 中到底走到了哪一步、最成熟的任务是什么、距离临床应用还差什么。

对应原文依据（页码）：

- `p.1-p.2, p.9-p.10`

### 2.2 核心思路（一段话概括解法方向）

- 本文通过系统综述的方式回顾 2000 到 2020 年间 CRC pathology image analysis 中的 AI 研究，对任务进行分层归纳，并重点对 gland segmentation 进行定量比较。作者将现有工作分成 `gland segmentation`、`tumor classification`、`tumor microenvironment analysis` 和 `prognosis prediction` 四类，指出当前最成熟的是 gland segmentation，尤其是围绕 `GlaS challenge` 及其后续工作的演进；但整体来看，绝大多数研究仍受限于数据量、标注质量、标准不统一以及外部验证不足。

关键页码：

- `p.1-p.3, p.6-p.15`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇不是单一模型论文，而是任务分层综述
- 核心分类框架：
  - `gland segmentation`
  - `tumor classification`
  - `tumor microenvironment characterization`
  - `prognosis prediction`
- 对 gland segmentation 还做了定量 rank-sum 比较

### 3.2 关键模块详细描述

**模块 1：`Gland Segmentation`**

- 在纳入模型中占比最高
- 被作者视为 CRC pathology AI 中最成熟的方向
- 主要 benchmark 围绕 `GlaS challenge`
- 页码：`p.3, p.6-p.7, p.10-p.11`

**模块 2：`Tumor Classification`**

- 主要针对正常/腺瘤/腺癌或多种 polyp / carcinoma 子型分类
- 但作者认为不同研究的分类体系并不统一，导致横向比较意义有限
- 页码：`p.5, p.7, p.11-p.12`

**模块 3：`Tumor Microenvironment Analysis`**

- 关注细胞类型分类、免疫细胞检测和微环境量化
- 代表意义在于与 prognosis、免疫治疗和 precision medicine 相关
- 页码：`p.5, p.8-p.9, p.13`

**模块 4：`Prognosis Prediction`**

- 仍属早期阶段
- 直接从 H&E 图像预测生存、MSI 或复发风险
- 页码：`p.5, p.9, p.13-p.14`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇为综述，不适用统一的逐层架构参数表
- 但其提供了一个可用于写作的任务层级框架：

| 任务类别 | 模型数 | 占比 | 综述结论 |
|---------|--------|------|---------|
| gland segmentation | `25` | `62%` | 最成熟，已有可量化 benchmark |
| tumor classification | `8` | `20%` | 结果看似高，但证据等级不足 |
| TME characterization | `4` | `10%` | 有潜力，但指标和任务不统一 |
| prognosis prediction | `3` | `8%` | 早期探索，数据与泛化仍有限 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇为系统综述，无方法公式推导
- 但明确总结了 gland segmentation 常用评价指标：
  - `F1-score`
  - `Object Dice`
  - `Object Hausdorff`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不讨论统一 loss 设计
- 重点在任务分布、数据质量与评价协议

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 综述提到：
  - gland segmentation 基本围绕 `GlaS`，后续部分工作引入 `CRAG`
  - tumor classification 数据集规模变化极大，从几十图到十余万 patches
  - TME 与 prognosis 数据更异质
- 对 gland segmentation，作者明确写到：
  - `GlaS` 包含 `165` 张 patch 图像
  - 来自 `16` 张 CRC WSIs
  - 训练部分：`37 benign + 48 malignant`
  - test A：`33 benign + 27 malignant`
  - test B：`4 benign + 16 malignant`

### 6.2 数据增强

- 综述文未统一总结 augmentation 细节

### 6.3 优化器与超参数

- 综述文未统一总结优化器与超参数

### 6.4 预处理与数据细节

- 写作上最有用的不是超参数，而是作者对数据问题的总结：
  - patch 数量大不等于 WSI 数量足够
  - 注释过程常缺少 pathologist 数量与一致性说明
  - 外部验证普遍不足

---

## 7. 推理与后处理

- 本篇不适用单一推理流程描述

---

## 8. 消融实验

### 8.1 消融设计

- 本篇不做消融
- 但对 `GlaS` 与 `post-GlaS` 工作做了横向比较

### 8.2 各模块贡献量化

- 作者总结：
  - `post-GlaS` 模型整体优于 challenge 时期模型
  - 在 `20` 个 gland segmentation 模型的 rank-sum 对比中，`Ding et al. 2019` 总体表现最好
- 对 individual metrics：
  - best `F1` 主要由 `Yan / Yang / Zhang`
  - best `Object Dice` 主要由 `Yang / Ding / Graham`
  - best `Object Hausdorff` 主要由 `Ding / Manivannan`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 任务占比 | `gland segmentation` 是最主流方向 (`62%`) | `p.1, p.3` |
| gland benchmark | `post-GlaS` 工作整体优于 challenge 时期 | `p.6-p.7` |
| gland overall best | `Ding et al. 2019` rank-sum 最优 | `p.1, p.7, p.10-p.11` |
| 全局结论 | 结果有希望，但数据规模与质量不足以支持 routine clinical use | `p.1, p.9, p.15` |

### 9.2 与其他方法的对比

- 综述中最可直接回填的是 gland segmentation 主表：
  - `DCAN`
  - `MILD-Net`
  - `Ding 2019 TCC-MSFCN`
  - `MIMO-Net`
  等都被放入同一比较框架
- 文中对 non-gland 任务则明确提醒：
  - 由于数据、类别体系和指标差异过大，直接横向比较 often `meaningless and impossible`

### 9.3 公平对比条件确认

- 对 gland segmentation，作者沿用共同 benchmark 做相对公平比较
- 对 tumor classification / TME / prognosis，作者明确认为：
  - 缺少 standardized dataset
  - 缺少统一 classification system
  - 缺少外部验证
  所以证据等级整体偏低

### 9.4 评价协议与指标定义

- gland segmentation：
  - `F1-score`：individual gland detection accuracy
  - `Object Dice`：对象级相似性
  - `Object Hausdorff`：boundary-based similarity
- tumor classification：
  - 常见为 `accuracy`, `sensitivity`, `specificity`, `AUC`
- 综述作者还特别指出：
  - 单一经典指标可能只反映模型的一维性能
  - 未来需要更综合的新评价参数

---

## 10. 计算量与效率

- 本篇不报告统一计算量
- 但从综述角度提示：
  - 当前很多工作仅证明“能做”，并未充分证明临床部署层面的稳健性与可推广性

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 任务分类框架：
  - `gland segmentation`
  - `tumor classification`
  - `tumor microenvironment characterization`
  - `prognosis prediction`
- 这是本篇最适合直接用于你论文 related work 结构的地方

### 11.2 论文指出的研究空白 / Open Problems

- 数据集规模和质量整体不足
- 外部交叉验证不足，尤其在 tumor classification 中最明显
- 标注流程往往缺少足够细节，难以判断 ground truth 质量
- Western / Eastern 诊断标准差异导致类别定义和标签体系并不完全统一
- patch 数量多不代表模型具有真正的跨患者/跨机构泛化能力

### 11.3 对我们选题的启示

- 你的 gland segmentation 选题是 CRC pathology AI 中最成熟、最核心的子方向之一
- 但论文写作不能只强调性能，还要强调：
  - 数据质量
  - 标注质量
  - 外部验证
  - 病理诊断标准差异
- 这篇还能帮你把工作从“单个 segmentation 模型”提升到“CRC pathological diagnosis pipeline”的叙事层面

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- Western pathologists 常以 invasion 作为 carcinoma 的关键诊断依据
- Eastern pathologists 更依赖 glandular 与 nuclear features
- 文中提到国际上为缓解差异提出了 colorectal neoplasia 五分类体系

### 12.2 涉及的生物标志物

- TME 部分提到：
  - `TILs`
  - `MSI`
  - `CIMP`
  - `PD-L1` 相关免疫治疗背景
- 这些内容可用于支撑“腺体分割不是孤立任务，而与免疫微环境和预后分析有关”

### 12.3 临床意义

- gland 结构的形状、大小和组织关系对 grading 很重要
- 小活检样本中的 artifacts、regenerative atypia 和标准差异会增加误判风险
- 因此自动化、可重复的 gland / tissue analysis software 有明确病理价值

---

## 13. 开源与复现

- 代码是否开源：`不适用（综述）`
- 代码仓库地址：`不适用`
- 框架/语言：`不适用`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`低`
- 复现障碍：
  - 作为综述，不涉及复现具体模型
  - 真正难点在于其比较结论依赖被综述研究的协议差异

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 各模型统一超参数 | 否 | 不强行汇总 | 低 |
| 各分类任务的统一标签体系 | 否，作者反而明确指出不统一 | 记录为局限性 | 高 |
| 外部验证协议细节 | 部分 | 仅按综述结论引用 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 作者明确提醒：
  - GlaS/post-GlaS 排名对评价指标细节敏感
  - 略微变化都可能改变 competition 排名
  - 经典指标不能完整反映模型的多维性能

### 14.2 我们观察到的潜在问题

- 由于发表年份只到 `2020`，本篇不覆盖：
  - foundation models
  - prompt-based methods
  - 更新的多任务、半监督和预训练研究
- 但它对于 `2020` 以前的主线脉络总结仍然很有价值

### 14.3 失败案例 / 定性分析

- 综述没有统一失败案例集
- 但明确指出真实 CRC path diagnosis 的关键困难：
  - small tissue artifacts
  - cauterization
  - regenerative atypia
  - inter-observer variation
  - class system discrepancy

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- CRC pathology AI 的任务分类框架
- gland segmentation 在整个领域中的主导地位证据
- 临床和病理标准差异的写作支撑
- “结果 promising 但数据/验证不足”的谨慎总结

### 15.2 可以作为候选参数来源的

- `GlaS` 的任务地位和评价指标定义
- `GlaS + CRAG` 的演化脉络

### 15.3 不应照搬的（及原因）

- 不应把 `2020` 综述中的“最佳模型”结论直接当作你当前时间点的 SOTA
  - 原因：后续已经有很多新方法
- 不应把 classification 子任务中 reported 高 accuracy 直接当成强证据
  - 原因：作者已明确指出缺少统一标准和高质量外部验证

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 任务选题合理性 | gland segmentation 占 CRC pathology AI 的 `62%` | 强 |
| 引言临床动机 | 诊断标准差异、样本伪影、observer variation | 强 |
| 相关工作结构 | 四大任务框架可直接借用 | 强 |
| 讨论部分 | 数据量、标注质量、外部验证不足 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_引言与相关工作素材`
- [ ] 需要和哪篇论文交叉验证：`03_DCAN.md`, `04_MILD-Net.md`, `08_Deep-Multichannel.md`, `03_Cerberus.md`
- [ ] 待确认的问题：`后续是否再补一篇更新到 2022 的 CRC systematic review 作时间线延伸`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | CRC 负担、observer variation、标准差异 | 临床背景 |
| related work | CRC pathology AI 四类任务结构 | 综述框架 |
| 任务定义 | gland 在 diagnosis/grading 中的基础地位 | 任务价值 |
| 讨论 | 数据质量与外部验证不足 | 局限性讨论 |
| 展望 | 从 gland 分割扩展到 TME / prognosis | 工作意义拔高 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.3` | 系统综述筛选流程 | 综述方法 |
| `Fig. 2` | `p.6` | CRC pathology AI 任务分布与年份趋势 | 研究版图 |
| `Table 1` | `p.4-p.5` | gland segmentation 主表 | 主线方法脉络 |
| `Table 2` | `p.5` | classification / TME / prognosis 模型摘要 | 扩展任务支撑 |
| `Table 3` | `p.7` | gland segmentation rank-sum 排名 | 定量总结 |
| `Fig. 4` | `p.10-p.11` | Ding 2019 的 TCC-MSFCN 流程图 | 主结果代表模型 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 综述框架与任务分类已明确
- [x] 指标定义和评价协议已确认
- [x] 与我们项目的关联已具体到写作模块
- [x] 不确定的内容已标注而未脑补
- [x] 病理和临床背景已单独提炼
- [x] 局限性与时间边界已注明
