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

- `PTEN`
- `glandular morphogenesis`
- `3D CRC model`
- `aPKC / NHERF-1`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`08_病理意义_形态学与下游应用`

- 本篇是当前文献库中最偏机制层的 gland morphology 论文，解释“为什么 gland architecture 失稳会与高等级 CRC 同步出现”。
- 对当前项目最有价值的是：
  - 给出 `PTEN -> cdc42 -> aPKC -> apical membrane orientation -> gland formation` 的机制链；
  - 证明 PTEN 的 `C2 domain` 即使在催化失活时仍有促形态发生作用；
  - 将 3D Caco-2 模型与人类 CRC 标本中的 gland grade、NHERF-1/apical readout 联系起来；
  - 为“边界/结构保持为什么重要”提供生物学与病理学机制支撑。
- 本篇至少完成：`1-4, 9, 12, 14-17`

---

## 1. 论文信息

- 论文名：`PTEN Phosphatase-Independent Maintenance of Glandular Morphology in a Predictive Colorectal Cancer Model System`
- 作者/团队：`Ishaan C. Jagan, Ravi K. Deevi, Aliya Fatehullah, Rebecca Topley, Joshua Eves, Michael Stevenson, Maurice Loughrey, Kenneth Arthur, Frederick Charles Campbell`
- 发表年份/会议/期刊：`2013, Neoplasia`
- DOI / arXiv ID：`10.1593/neo.121516`
- BibTeX key：`jagan2013pten`
- PDF 路径：`结直肠腺体分割_pdf库/08_病理意义_形态学与下游应用/PTEN_Phosphatase-Independent_Maintenance_of_Glandular_Morphology_in_a_Predictive_Colorectal_Cancer_Model_System_2013.pdf`
- 当前定位：`08` 目录里最核心的“gland morphology 机制起点”论文之一，解释高等级 CRC 中 glandular dysmorphogenesis 的细胞极性与 apical domain 生物学基础。
- 与已提取论文的关系：
  - 与 `01_CRC-Histological-Characteristics.md` 互补：后者给出病理描述口径，本篇解释其背后的极性与形态机制。
  - 与 `02_Glandular-Morphometrics.md` 形成纵向链条：后者量化 gland aberrance，本篇解释 gland aberrance 可能从何而来。
  - 与 `04_Automatic-Tumor-Grading-WSI.md` 的关系是“机制基础 -> 下游自动量化”，从细胞极性失序一路连到 WSI 级 grading。

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：从 benign adenoma 到 invasive CRC 的演进伴随着 glandular architecture 的动态破坏，从围绕中央腔的极化上皮组织逐步走向完全 gland disruption。
  - 用途：`病理背景`
  - 页码：`p.2`
- 句子/事实 2：histologic grading 对这些 glandular morphology 变化具有重要预后意义，因此研究 gland morphogenesis 的机制并非纯基础问题，而有临床相关性。
  - 用途：`临床意义`
  - 页码：`p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：PTEN deficiency 与 adenoma 和 dysmorphic high-grade CRC 的异常 gland morphology 相关。
  - 用途：`机制入口`
  - 页码：`p.2`
- 句子/事实 2：作者并非只讨论 PI3K/AKT 抑癌通路，而是强调 PTEN 通过 `cdc42 / aPKC` 调控 apical membrane orientation 与 3D gland morphogenesis。
  - 用途：`为什么这篇对腺体结构重要`
  - 页码：`p.2`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 期刊页码 | `Neoplasia 15(11):1218-1230` | 文献信息 | `p.1` |
| DOI | `10.1593/neo.121516` | 文献信息 | `p.1` |
| 单腔形成率（Caco-2 vs ShPTEN） | `65.5 +- 2.75% vs 38 +- 2.68%` | 形态缺陷量化 | `p.5` |
| 人体 CRC 样本数 | `40` | translational validation | `p.6` |
| 人体样本分层 | `good / intermediate / poor differentiation` | 组织学验证 | `p.6` |
| NaBt 剂量 | `1 mM` | rescue experiment | `p.3` |
| C2 vs C2 M-CBR3 membrane densitometry | `221 +- 4.8 vs 122 +- 7.2` | membrane localization | `p.3` |
| C2 vs C2 M-CBR3 cytosol densitometry | `137 +- 8.5 vs 236 +- 8.7` | membrane localization | `p.3` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- CRC 进展过程中 gland morphology 会从规则单腔结构走向多腔、空泡化和结构解体。
- 这些变化不仅是病理现象，也可能直接促进 tumor cell escape 与侵袭。
- 作者此前已观察到 PTEN knockdown 会让 3D Caco-2 模型出现多腔、极性错位的高等级癌样 phenotype。
- 但仍不清楚：
  - PTEN 的哪一部分功能在主导 gland morphogenesis；
  - 这一机制是否能在人类 CRC 组织里找到对应 readout。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文通过 `PTEN-wt / PTEN-deficient` 的 isogenic 3D colorectal culture 比较不同 PTEN 结构域对 gland morphogenesis 的作用，重点测试催化活性与 `C2 domain` 膜结合功能是否决定 apical membrane 组装和单腔形成。作者进一步用 `aPKC` 与 `NHERF-1` 作为 apical readout，把 3D 模型中的极性/单腔结果与人类 CRC 标本中的 gland grade、淋巴结转移和 apical marker 强度联系起来，从而建立“机制 -> 形态 -> 病理分级”的跨层证据链。

关键页码：

- `p.1-p.3`
- `p.5-p.12`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 研究由两部分组成：
  1. `3D organotypic CRC model`
  2. `human CRC translational validation`
- 核心链条：
  - `PTEN / PTEN C2 domain`
  - `cdc42 activation`
  - `aPKC apical activity`
  - `apical membrane orientation`
  - `single lumen gland formation`
  - `human CRC gland grade / metastasis association`

### 3.2 关键模块详细描述

**模块 1：`Caco-2 / Caco-2 ShPTEN 3D Morphogenesis Model`**

- 作用：
  - 用等基因背景的 3D 结直肠上皮模型观察 gland formation。
- 关键现象：
  - 正常 Caco-2 更容易形成单腔；
  - `ShPTEN` 出现 aPKC 错位与多腔/空泡 phenotype。
- 页码：`p.2-p.5`

**模块 2：`PTEN Domain Perturbation`**

- 研究对象：
  - wt PTEN
  - catalytically active / inactive mutants
  - isolated `C2 domain`
  - `C2 M-CBR3` membrane-binding mutant
- 目标：
  - 区分 PTEN 的 phosphatase-dependent 与 phosphatase-independent morphogenic function。
- 页码：`p.2-p.4`

**模块 3：`cdc42 / aPKC / NHERF-1 Readout`**

- 作用：
  - 把分子层变化和 apical membrane orientation 连接起来。
- 论文结论：
  - intact `C2 domain` 可增强 `cdc42`；
  - `NHERF-1` 可作为 apical aPKC activity 的 readout；
  - 低 apical `NHERF-1` 与更差 gland morphology 和更高 grade 相关。
- 页码：`p.1-p.3`, `p.8-p.12`

**模块 4：`Human CRC Histomorphic Validation`**

- 样本：
  - `40` 例非连续手术 CRC
- 验证内容：
  - gland formation grade
  - apical `aPKC / p-aPKC / NHERF-1`
  - lymph node metastasis association
- 页码：`p.6-p.12`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 作用 | 关键细节 |
|------|------|---------|
| Caco-2 3D culture | 正常 gland morphogenesis 对照 | 单腔形成 |
| Caco-2 ShPTEN | PTEN 缺失模型 | 多腔/空泡 phenotype |
| C2 domain transfection | 机制干预 | 检查 membrane-binding 功能 |
| aPKC / p-aPKC / NHERF-1 | apical readout | 连接极性与形态 |
| human CRC cohort | 临床转化验证 | gland grade + metastasis |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：本文隐含机制链

```text
PTEN C2 domain integrity -> cdc42 activation -> apical aPKC signaling
-> correct apical membrane orientation -> single-lumen gland morphogenesis
```

公式 2：实验逻辑

```text
if C2 intact:
    rescue membrane localization and gland morphogenesis
else if C2 M-CBR3 mutated:
    fail to rescue
```

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 本篇不是 loss / network 论文。
- 但它的机制推理非常清楚：
  - 若只是 PTEN 的 phosphatase 活性重要，那么催化失活构建体不该保留促形态发生效应；
  - 结果却显示只要 `C2 domain` 完整，催化失活 PTEN 仍能增强 `cdc42` 与 morphogenesis；
  - 因而说明 membrane-binding related 的 phosphatase-independent 功能才是关键。

---

## 5. 损失函数

### 5.1 各监督项

- 不适用。
- 本篇是机制与病理验证论文，不是神经网络训练论文。

### 5.2 总损失公式

```text
不适用
```

### 5.3 权重配置与调度策略

- 不适用。

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据/模型 | 数量 | 备注 |
|----------|------|------|
| Caco-2 3D culture | 多时点观察 | `2 / 4 / 12 days` |
| Caco-2 ShPTEN | 对照缺失模型 | 观察 PTEN 缺失后形态 |
| human CRC | `40` | good/intermediate/poor differentiation |

### 6.2 数据增强

- 不适用。
- 研究核心是 3D 培养、免疫荧光和组织病理 readout。

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| 3D culture observation points | `2 / 4 / 12 days` |
| NaBt treatment | `1 mM` |
| Caco-2 embedding | `40% Matrigel` |
| 细胞数 | `6 x 10^4` per well | 

### 6.4 预处理与数据细节

- `ShPTEN` 通过 retroviral vector + puromycin selection 建立。
- `C2` 与 `C2 M-CBR3` 用 GFP-tagged constructs 稳定转染。
- 人类 CRC 由病理医师按 gland formation 组织学等级评分。

---

## 7. 推理与后处理

- 本篇的“输出”不是 segmentation mask，而是：
  - 单腔形成率
  - apical marker localization
  - gland grade 相关性
- 关键 readout：
  - `single lumen formation`
  - `p-aPKC intensity`
  - `NHERF-1 apical intensity`

---

## 8. 消融实验

### 8.1 结构域功能比较

- 作者实际上做的是功能消融：
  - wt PTEN
  - catalytic mutants
  - isolated `C2`
  - `C2 M-CBR3`

### 8.2 各模块贡献量化

- `C2` 可 rescue morphogenesis；
- `C2 M-CBR3` 不可 rescue；
- 说明 membrane-binding loop 完整性比单纯 phosphatase catalytic activity 更关键。

### 8.3 关键量化结果

- `Caco-2` 与 `Caco-2 ShPTEN` 的单腔形成率：
  - `65.5 +- 2.75% vs 38 +- 2.68%`
- 这直接把 PTEN 缺失与 gland architecture 破坏联系起来。

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 结果 | 数值/结论 | 页码 |
|------|-----------|------|
| single lumen formation | `65.5 +- 2.75% vs 38 +- 2.68%` | `p.5` |
| C2 membrane localization | `221 +- 4.8` vs mutant `122 +- 7.2` | `p.3` |
| NHERF-1 与 CRC grade 关系 | 负相关 | `p.10-p.12` |
| NHERF-1 与 lymph node metastasis | 负相关 | `p.8-p.12` |

### 9.2 结果解释

- PTEN 缺失会扰乱 apical domain positioning，导致多腔/空泡化 gland phenotype。
- 只要 `C2 domain` 完整，即便 PTEN 催化活性不工作，仍能部分 rescue gland morphogenesis。
- 因而高等级 CRC 中的 gland architecture 失序，至少一部分可追溯到 apical polarity machinery 失稳。

### 9.3 公平对比条件确认

- 本篇不是 benchmark 对比文，不做常规分割公平表。
- 它的“公平性”来自：
  - isogenic model control
  - wild-type 与 mutant domain 对照
  - 人体样本转化验证

### 9.4 评价协议与指标定义

- 主要是：
  - single lumen proportion
  - apical signal intensity
  - semiquantitative IHC scores
  - histologic gland grade

---

## 10. 计算量与效率

- 不适用。
- 本篇主要提供机制解释，不提供工程效率结论。

---

## 11. 分类体系与研究空白

### 11.1 本篇的方法学定位

- 这是典型的：
  - `mechanistic pathology paper`
  - `3D model + translational validation`
- 它不属于直接的 gland segmentation 算法文，但对“为什么 gland 结构保持重要”有极高解释价值。

### 11.2 论文指出的研究空白 / Open Problems

- 高等级 CRC 中 gland dysmorphogenesis 的 PTEN 具体功能域机制不清；
- 3D organotypic findings 与 human CRC 病理 readout 缺少直接桥接；
- 仅从 PI3K/AKT 解释 PTEN 并不足以解释 gland morphology。

### 11.3 对后续研究的启示

- 若我们写边界/结构保持的重要性，不能只从经验误差讲，也可以从 apical polarity 和 gland morphogenesis 的生物学机制讲。
- `NHERF-1 / aPKC` 这一链路很适合写在更深的病理机制讨论中。

---

## 12. 临床/病理标准

### 12.1 涉及的病理分级标准

- 论文采用基于 gland formation 的 Grade I/II/III 口径：
  - Grade III：poorly organized region 占满 `x40` 视野
  - Grade II：无腺结构的肿瘤细胞簇 `>=10`
  - Grade I：无腺结构簇 `<10`
- 这与 gland formation 为核心的 CRC 组织学分级传统高度一致。

### 12.2 涉及的生物标志物

- `PTEN`
- `cdc42`
- `aPKC / p-aPKC`
- `NHERF-1`

### 12.3 临床意义

- 本篇说明 gland morphology 并非单纯视觉现象，而对应可测的 apical polarity signal 失稳。
- 这让“结构保持型分割”在写作上更容易获得病理学正当性。

---

## 13. 开源与复现

- 代码是否开源：`未提供`
- 代码仓库地址：`未提供`
- 复现难度评估：`高`

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 每个 3D 实验的精确重复次数 | 部分 | 仅保留已见 `n=3` 结果 | 中 |
| 全部构建体序列细节 | 部分 | 记录到结构域级 | 中 |
| 人体样本完整分层统计表 | 部分 | 只记录核心病理关联 | 中 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 主要是 3D 模型和有限人体样本，不是大规模临床队列。
- 虽然与人类 CRC 病理吻合，但不能直接替代大样本预后研究。

### 14.2 我们观察到的潜在问题

- 与当代数字病理大数据研究相比，样本量较小。
- 其价值更偏“机制支撑”，而不是直接作为现代临床风险模型。
- 不能把这篇当成 segmentation benchmark 论文使用。

### 14.3 失败案例 / 定性分析

- 作者最主要展示的是：
  - PTEN 缺失导致的多腔/空泡 phenotype；
  - 以及 rescue / non-rescue 的鲜明差异。
- 真正的失败场景是：
  - `C2 M-CBR3` 无法 rescue；
  - 提示膜结合失败就会使 apical morphogenesis 路线失效。

---

## 15. 对我们项目的落地价值

### 15.1 最直接的启发

- 这篇是“为什么 gland 结构完整性重要”的机制级证据。
- 它让我们在论文里可以更有底气地写：
  - 结构边界不是纯视觉美学问题；
  - gland lumen 和 apical orientation 的保存与病理等级相关。

### 15.2 对模块设计和写作的启发

- 若我们强调：
  - boundary head
  - topology preserving loss
  - skeleton / lumen aware design
- 本篇可以作为“保持 gland architecture 具有病理意义”的底层支撑。

### 15.3 对实验设计的提醒

- 仅报告 Dice 可能不足以说明病理可用性；
- 若能补一些 lumen integrity、gland separation、shape regularity 相关分析，写作会更强。

### 15.4 在整套文献链中的位置

- 这是 `08` 目录里最偏机制解释的一篇；
- 与 `02_Glandular-Morphometrics.md`、`05_Gland-Orientation-Aggressive-Tumor.md`、`04_Automatic-Tumor-Grading-WSI.md` 共同构成：
  - `机制 -> 形态测量 -> 风险分层 -> WSI 级 prognostic modeling`

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`引言/讨论中的病理机制小段`
- [ ] 需要和哪篇论文交叉验证：`02_Glandular-Morphometrics.md`, `14_SkeletonAwareDT.md`
- [ ] 待确认的问题：`我们是否要在结果讨论里加入 lumen integrity 或 gland regularity 的定性分析`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland architecture 与 CRC progression 的机制联系 | 背景加强 |
| related work | gland morphogenesis mechanism | 病理机制补充 |
| 讨论 | 结构保持为何与 grade / metastasis 相关 | 深层解释 |
| 展望 | 形态感知指标设计 | 后续扩展 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.3-p.4` | PTEN 构建体与 cdc42 activation / membrane localization | 机制主图 |
| `Fig. 2` | `p.5` | Caco-2 与 ShPTEN 的单腔形成对比 | 形态缺陷直观证据 |
| `Fig. 3` | `p.6-p.7` | C2 rescue vs mutant non-rescue | C2 domain 关键作用 |
| `Fig. 6` | `p.10-p.12` | human CRC 中 NHERF-1 / grade / metastasis 关系 | 转化验证 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（这是机制论文，不追求工程级复现）
- [x] 预处理与数据细节已检查
- [x] 结果数字与正文结果段一致
- [x] 指标定义和评价协议已确认
- [ ] 消融实验的结论已量化（主要是机制干预，不是现代 ablation table）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注而未脑补
