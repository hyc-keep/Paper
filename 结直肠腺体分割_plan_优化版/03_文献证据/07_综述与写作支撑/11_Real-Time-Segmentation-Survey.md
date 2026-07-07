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
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `real-time segmentation survey`
- `efficiency vs accuracy`
- `lightweight architecture background`
- `deployment-oriented writing support`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`07_综述与写作支撑`

- 本篇主要用于补“高效/实时/低内存语义分割”的方法背景，而不是病理专文
- 对当前项目最有价值的是：
  - 系统解释轻量化分割的常见设计手段
  - 明确 `latency-accuracy trade-off`
  - 支撑为什么边界细节任务不一定适合极端压缩模型
- 本篇至少完成：`1-3, 10-11, 15-17`

---

## 1. 论文信息

- 论文名：`On Efficient Real-Time Semantic Segmentation: A Survey`
- 作者/团队：`Christopher J. Holder, Muhammad Shafique`
- 发表年份/会议/期刊：`2022, arXiv survey`
- DOI / arXiv ID：`10.48550/arXiv.2206.08605`, `arXiv:2206.08605`
- BibTeX key：`holder2022realtimesegsurvey`
- PDF 路径：`结直肠腺体分割_pdf库/07_综述与写作支撑/On_Efficient_Real-Time_Semantic_Segmentation_A_Survey_2022.pdf`
- 当前定位：`07` 目录中补“轻量化与部署约束”背景的综述，适合为后续若涉及效率、延迟、内存占用、嵌入式部署等讨论提供依据
- 与已提取论文的关系：
  - 与 [10_ViT-Segmentation-Survey.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/10_ViT-Segmentation-Survey.md) 形成互补：前者补现代 Transformer 路线，本篇补高效/实时 CNN segmentation 路线与部署约束
  - 与 [04_Metrics-Reloaded.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/04_Metrics-Reloaded.md) 互补：前者强调评价应服务任务需求，本篇提醒效率本身也是实际部署的重要维度
  - 与 [09_Region-Boundary-Integration-Survey.md](file:///D:/12_Medical_Image_Segmentation/图像分类学习/结直肠腺体分割_plan/03_文献证据/07_综述与写作支撑/09_Region-Boundary-Integration-Survey.md) 有方法论呼应：两篇都强调全局语义与局部边界之间存在长期张力

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：许多高性能 semantic segmentation 模型过于复杂笨重，不适合在低内存、低时延的嵌入式平台上部署。
  - 用途：`研究动机`
  - 页码：`p.1`
- 句子/事实 2：作者在统一硬件和软件条件下比较 2015-2021 年的代表模型，强调 quoted runtime 若来自不同实验环境，往往无法直接客观比较。
  - 用途：`效率比较规范`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：综述将实时语义分割方法归纳为五类：`encoder-decoder`、`multi-branch`、`meta-learning`、`attention` 和 `training pipeline`
  - 用途：`分类框架`
  - 页码：`p.6-p.7`
- 句子/事实 2：高效 segmentation 最核心的张力在于如何提取 `high-level global context` 的同时保留 `fine-grained detail`
  - 用途：`方法难点`
  - 页码：`p.2-p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| arXiv | `2206.08605` | 文献信息 | `题录` |
| 实时定义 | `>= 30 fps` | 术语定义 | `p.1` |
| 统一比较模型数 | `24` 个 notable works | 综述规模 | `p.1` |
| 时间范围 | `2015-2021` | 综述范围 | `p.1` |
| taxonomy 类别数 | `5` 类 | 方法分类 | `p.6-p.7` |
| 常用 driving benchmark 例子 | `CamVid`, `KITTI`, `Cityscapes`, `BDD`, `A2D2` | 数据集背景 | `p.3-p.4` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- semantic segmentation 在自动驾驶、机器人、无人机等场景中必须满足低时延要求
- 但大量高精度模型追求的是多 GPU 环境下的最高精度，而忽略嵌入式部署现实
- 真正落地时，平台往往同时受限于：
  - latency
  - memory
  - compute budget
- 因此需要专门研究：
  - 更紧凑的模型
  - 更低的推理延迟
  - 在资源受限硬件上仍能运行的 segmentation architectures

对应原文依据（页码）：

- `p.1`

### 2.2 核心思路（一段话概括解法方向）

- 本综述聚焦低时延或低内存推理目标下的 semantic segmentation 架构，先回顾 semantic segmentation 的背景、挑战、应用和常见数据集，再系统总结提高 CNN 效率的通用技巧，如 downsampling、efficient convolution、residual connection 与轻量 backbone，随后将实时 segmentation 模型分为 `encoder-decoder`、`multi-branch`、`meta-learning`、`attention` 和 `training pipeline` 五类，并在统一高端 GPU 与嵌入式 GPU 条件下对代表模型的推理速度做横向比较。它最重要的结论是：很多模型确实可在资源受限硬件上实现 real-time inference，但 `latency-accuracy trade-off` 始终存在。

关键页码：

- `p.1-p.2`
- `p.6-p.16`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 本篇是综述，不是单一模型论文
- 结构可概括为三层：
  1. semantic segmentation 背景与部署挑战
  2. 提升效率的通用结构技巧
  3. 五类实时分割方法 taxonomy

### 3.2 关键模块详细描述

**模块 1：`Challenges and Trade-Offs`**

- 语义分割需要输出与输入同尺寸的 dense prediction
- FCN 路线虽然保留了空间结构，但多次 downsampling 会丢失细粒度边界信息
- 高层全局语义与低层局部细节之间的平衡，是整个领域的长期主题
- 页码：`p.2-p.3`

**模块 2：`General Efficiency Techniques`**

- 综述系统列出常见提速/压缩手段：
  - `downsampling and upsampling`
  - `depthwise-separable convolution`
  - `grouped convolution`
  - `asymmetric convolution`
  - `bottleneck residual blocks`
  - `efficient backbones`
- 这些是你后面解释“轻量化怎么做”的最直接素材
- 页码：`p.4-p.6`

**模块 3：`Encoder-Decoder`**

- 典型路线包括：
  - `SegNet`
  - `U-Net`
  - `ENet`
  - `ERFNet`
  - `EDANet`
  - `ESPNet`
- 核心思想是：
  - 编码阶段提取语义
  - 解码阶段恢复空间细节
- 页码：`p.7-p.11`

**模块 4：`Multi-Branch`**

- 使用多个分辨率或多个语义层级并行处理，再融合高低层特征
- 这种设计对“兼顾 global context 和 fine detail”尤其重要
- 是速度与边界保真折中的常见路线
- 页码：`taxonomy`, `p.6+`

**模块 5：`Attention / Meta-Learning / Training Pipeline`**

- `Attention`：用注意力显式聚合全局上下文
- `Meta-learning`：由另一学习模块设定结构或权重
- `Training pipeline`：不一定改结构，而是通过更好的训练/蒸馏/优化策略提升实时模型表现
- 这说明“高效模型”不一定只来自轻量 backbone，也可能来自训练方案改进
- 页码：`p.6-p.7`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

- 本篇不做统一参数表
- 但可提炼为“策略-目的”表：

| 策略 | 主要目的 | 对你写作的价值 |
|------|---------|---------------|
| `early downsampling` | 降低计算量 | 解释为何轻量模型快 |
| `lightweight decoder` | 降低恢复阶段代价 | 解释速度来源 |
| `depthwise/grouped conv` | 减参数减 FLOPs | 轻量结构关键词 |
| `multi-branch fusion` | 兼顾低层细节与高层语义 | 解释精度保真手段 |
| `attention` | 聚合全局上下文 | 解释为何不是只靠卷积 |

---

## 4. 公式与推导

### 4.1 核心公式

- 本篇不是公式论文
- 更重要的是其结构性结论：
  - downsampling 减少计算，但也更容易丢失边界与小目标细节
  - 轻量卷积块与高效 backbone 是实时分割的常见工程基础

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 不适用

---

## 5. 损失函数

### 5.1 各监督项

- 本篇不以 loss 设计为主
- 但提到某些高效模型的表现也可能受训练 pipeline 和任务特定 loss 影响

### 5.2 总损失公式

- 不适用

### 5.3 权重配置与调度策略

- 不适用

---

## 6. 训练协议

### 6.1 数据集与划分

- 本篇主要围绕 driving scene benchmarks 展开
- 代表数据集包括：
  - `CamVid`
  - `KITTI`
  - `Cityscapes`
  - `Berkeley DeepDrive`
  - `A2D2`
- 这些是实时分割路线最常见的 benchmark 背景

### 6.2 数据增强

- 不是当前提取重点

### 6.3 优化器与超参数

- 综述不集中报告统一超参数

### 6.4 预处理与数据细节

- 作者特别强调 runtime 必须在统一条件下比较
- 这是本篇非常有价值的 methodological reminder

---

## 7. 推理与后处理

- 本篇核心在推理延迟而不是后处理
- 明确把“在嵌入式 GPU 上的 inference latency”作为主要考察对象
- 对部署写作最有用的一句是：
  - 模型 quoted runtime 若来自不同硬件/软件环境，并不能公平比较

---

## 8. 消融实验

### 8.1 消融设计

- 综述不做单模型 ablation
- 但通过统一环境下比较 `24` 个代表模型，形成一种更可信的横向分析

### 8.2 各模块贡献量化

- 作者最重要的综合观察是：
  - 许多模型确实能在嵌入式设备上达到实时
  - 但 latency 和 accuracy 的 trade-off 一直存在
  - 提速最容易牺牲的是边界与细节保真

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 项目 | 结论 | 页码 |
|------|------|------|
| 核心问题 | 高精度模型过于复杂，不适合低资源部署 | `p.1` |
| 实时定义 | `>= 30 fps` | `p.1` |
| 比较规模 | `24` 个 notable works, `2015-2021` | `p.1` |
| taxonomy | `encoder-decoder / multi-branch / meta-learning / attention / training pipeline` | `p.6-p.7` |
| 效率技巧 | early downsampling, efficient conv, bottleneck 等 | `p.4-p.6` |
| 总结结论 | 多数模型可在受限硬件实时运行，但存在稳定的 `latency-accuracy trade-off` | `p.1, p.15-p.16` |

### 9.2 与其他方法的对比

- 本篇不是强调单一 SOTA，而是强调部署情境下的对比逻辑
- 关键对照不是“谁在大 GPU 上最准”，而是：
  - 谁更适合低内存嵌入式设备
  - 谁的速度代价更合理
  - 谁在降延迟时保留了更多精度

### 9.3 公平对比条件确认

- 作者自己重新在统一环境下测 latency
- 同时包含：
  - 高端 GPU research scenario
  - low-memory embedded GPU deployed scenario
- 这是本篇最可靠的部分之一

### 9.4 评价协议与指标定义

- 本篇不是专门 metrics 综述
- 但它扩展了“评价”的含义：
  - 对实际部署任务，仅看精度不够
  - latency 与 memory 也是必须报告的指标
- 对你的项目，这篇很适合支持这样一种讨论：
  - 若后续考虑部署或资源约束，就不能只看 Dice/mIoU
  - 还要看模型是否在合理内存和时延下可运行

---

## 10. 计算量与效率

- 这是本篇最核心的部分
- 作者系统总结了轻量化语义分割的工程策略：
  - 早期下采样
  - 轻量 decoder
  - depthwise-separable convolution
  - grouped convolution
  - asymmetric convolution
  - bottleneck residual design
- 结论上最值得直接借用的是：
  - 高效模型最难兼顾 `global context` 与 `fine-grained spatial detail`
  - 边界和小结构细节往往是压缩模型时最先受损的部分

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- `encoder-decoder`
- `multi-branch`
- `meta-learning`
- `attention`
- `training pipeline`

### 11.2 论文指出的研究空白 / Open Problems

- 精度与时延之间仍存在稳定 trade-off
- 统一、可复现的 latency benchmarking 仍然缺乏
- 高效模型最难保住的是边界和细节
- 真正适合嵌入式部署的分割模型仍需要继续优化

### 11.3 对我们选题的启示

- 如果你的腺体分割后续考虑轻量化或设备侧部署，这篇是很好的上位支撑
- 即使暂时不做部署，它也能帮你说明：
  - 过度压缩模型可能损伤 gland boundary 细节
  - 小结构、细边界任务对轻量化特别敏感
- 因此在论文里完全可以写出：
  - 轻量化不是无代价的
  - boundary-sensitive tasks 更需谨慎看待速度提升

---

## 12. 临床/病理标准（病理临床 D 类型专用）

- 本篇不是病理或临床标准文献
- 但它明确提到：
  - 在 medical diagnosis 中，latency 不像自动驾驶那样绝对关键
  - 但若模型要直接部署在诊断设备上，memory constraints 依然重要
- 这句很适合回填到你后面“医学场景中的部署讨论”

---

## 13. 开源与复现

- 代码是否开源：`不适用（综述）`
- 代码仓库地址：`不适用`
- 框架/语言：`不适用`
- 预训练权重是否提供：`不适用`
- 复现难度评估：`低`
- 复现障碍：
  - 不是单一模型
  - 真正的难点在于不同原始论文的运行环境不统一

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 各模型统一训练脚本 | 否 | 只提综述结论 | 低 |
| 每个模型完整部署配置 | 非统一公开 | 不做直接复现 | 中 |
| 医学图像专门的实时 benchmark | 否 | 只作部署动机支撑 | 低 |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 作者本身就承认高效模型通常需要接受一定精度折损
- 统一 runtime benchmarking 很难彻底做到完全公平，因为实现细节和软件栈仍有差异

### 14.2 我们观察到的潜在问题

- 这篇主要围绕 driving / robotics deployment 场景
- 对病理图像最适合借用的是“效率约束思路”，不是具体 benchmark 排名
- 如果你当前论文不讨论部署，则它更适合出现在展望、discussion 或 related work 的轻量化背景里

### 14.3 失败案例 / 定性分析

- 文中持续强调的失败模式是：
  - 追求更快推理时，边界细节和小区域最容易退化
- 这与你的 gland boundary 任务高度相关

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 轻量化 segmentation 的五类 taxonomy
- 常见提速手段的标准表述
- `latency-accuracy trade-off` 的规范说法
- “边界细节最容易在轻量化中受损”的论证

### 15.2 可以作为候选参数来源的

- 本篇不给具体超参数
- 但能帮你确定：
  - 若要写轻量化 related work，该怎么分类
  - 若要讨论部署，该强调哪些工程维度

### 15.3 不应照搬的（及原因）

- 不应把 driving benchmark 上的实时排名直接套到病理任务
  - 原因：任务和硬件环境不同
- 不应把“更快”直接等同于“更适合腺体分割”
  - 原因：边界与细节可能先受损
- 不应只引用本篇就下结论说你的模型必须实时
  - 原因：医疗任务的 latency 优先级不一定与自动驾驶相同

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 轻量化 related work | 五类实时分割方法 taxonomy | 强 |
| discussion | 速度与精度/边界保真的权衡 | 强 |
| 部署展望 | medical device 上的 memory constraints | 中 |
| 方法取舍说明 | 为什么不一味追求最小模型 | 强 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`论文写作_轻量化与部署相关工作`
- [ ] 需要和哪篇论文交叉验证：`10_ViT-Segmentation-Survey.md`, `04_Metrics-Reloaded.md`
- [ ] 待确认的问题：`你后续是否真的要把轻量化作为一条副线写进正文，还是只保留在讨论与展望`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| related work | 高效/实时分割方法 taxonomy | 轻量化背景 |
| discussion | latency-accuracy trade-off | 结果分析 |
| 展望 | 低资源部署与边界保真冲突 | 未来工作 |
| 方法动机 | 为什么不盲目压缩模型 | 设计解释 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.1-p.2` | 论文结构总览 | 阅读导航 |
| `Fig. 2` | `p.2-p.3` | semantic segmentation pipeline | 基本概念 |
| `Fig. 5` | `p.5-p.6` | ResNet / ShuffleNet / MobileNetV2 典型高效卷积块 | 轻量结构说明 |
| `Table III` | `p.6-p.7` | 五类 taxonomy 总表 | 方法分类 |
| `Fig. 6` | `p.7` | SegNet encoder-decoder architecture | 经典高效路线 |

---

## 17. 提取质量自检

- [x] 已写清本篇服务于“效率/部署/轻量化”背景
- [x] 已记录 `>=30fps` 的实时定义
- [x] 已提炼五类 taxonomy
- [x] 已记录常见高效卷积与轻量化设计手段
- [x] 已保留 medical diagnosis 场景下 `memory constraints` 的表述
- [x] 已明确边界细节在轻量化中容易受损
- [ ] 各代表模型具体 latency 数字逐项核对（当前不需要）
