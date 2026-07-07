# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [ ] A - 方法论文（提出新模型/新架构）
- [x] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `boundary-region loss`
- `Boundary IoU inspired loss`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为这篇给出了 boundary-aware 区域损失公式、adaptive size strategy 和成体系 benchmark，所以额外补全：`6, 16`

---

## 1. 论文信息

- 论文名：`Boundary Difference over Union Loss for Medical Image Segmentation`
- 作者/团队：`Sun Fan, Luo Zhiming, et al. [待确认完整作者列表]`
- 发表年份/会议/期刊：`2023, arXiv preprint / 医学图像分割损失论文`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:2308.00220`
- BibTeX key：`sun2023boundarydou`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Boundary_Difference_Over_Union_Loss_For_Medical_Image_Segmentation_2023.pdf`
- 当前定位：`Boundary IoU 启发下的简洁边界区域损失；核心价值是不用显式距离图、也不依赖与其他损失组合，仅通过 difference set 与 partial union 的区域运算就增强边界监督`
- 与已提取论文的关系：
  - 与 `Boundary-Loss_2019`、`Distance-Map-Loss_2019` 相比，它更偏 region-like computation，不依赖 point-to-boundary distance
  - 与 `Shape-Aware-SDM_2020` 相比，它不显式回归距离图，而是直接在 segmentation 集合关系上强化 boundary region
  - 可视作 `Dice` 的 boundary-aware 变体，适合与你当前已有 `Dice / Dice+CE` 体系直接对照

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：现有医学图像分割损失主要关注 overall segmentation，专门引导 boundary segmentation 的损失较少
  - 用途：`背景 / 痛点`
  - 页码：`Abstract, p.1`
- 句子/事实 2：已有 boundary losses 往往需要和其他损失组合使用，且训练效果不稳定
  - 用途：`相关工作缺陷`
  - 页码：`Abstract, p.1; Intro, p.1-p.2`
- 句子/事实 3：Boundary DoU Loss 只依赖 region calculation，易于实现、训练稳定，而且不需要额外 losses
  - 用途：`方法定位`
  - 页码：`Abstract, p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：Boundary IoU 很关注 boundary quality，但其 boundary area 依赖 erode operation，不可微，难以直接作为训练损失
  - 用途：`方法动机`
  - 页码：`Sec.2.1, p.2-p.3`
- 句子/事实 2：Boundary DoU Loss 用 difference region 近似 mismatched boundary，并用 partial union 替代难以微分的 boundary IoU 计算
  - 用途：`公式设计依据`
  - 页码：`Sec.2.2, p.3-p.4`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 数据集 | `Synapse / ACDC` | benchmark 设置 | `p.5-p.6` |
| Synapse 划分 | `18 train / 12 test` | 数据集设置 | `p.5-p.6` |
| ACDC 划分 | `7:1:2 train/val/test` | 数据集设置 | `p.5-p.6` |
| 输入分辨率 | `224×224` | 训练设置 | `p.6` |
| optimizer | `SGD` | 训练设置 | `p.6` |
| 学习率 | `0.01` | 训练设置 | `p.6` |
| weight decay | `1e-4` | 训练设置 | `p.6` |
| batch size | `24` | 训练设置 | `p.6` |
| momentum | `0.9` | 训练设置 | `p.6` |
| epochs | `150` | 训练设置 | `p.6` |
| backbone for UNet | `ResNet50 + ImageNet pretrained` | 基线设置 | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 医学图像分割常用损失多偏向整体区域重叠，缺少针对边界区域的显式优化
- 现有 boundary-oriented losses 常常需要和 Dice/CE 等损失组合，且训练可能不稳定
- Boundary IoU 作为指标很适合评价边界质量，但由于 erode operation 不可微，不能直接拿来训练
- 小目标和复杂器官的难点往往集中在 boundary region，因此需要一个既像 Dice 一样易训练、又更聚焦边界的损失

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`
- `Sec.2.1, p.2-p.3`

### 2.2 核心思路（一段话概括解法方向）

- 论文从 `Boundary IoU` 出发，把 prediction 与 GT 的 difference set 视作 mismatched boundary 区域，并把交集的中间部分去掉，用 `α * (G ∩ P)` 构造 partial union，最终定义 `Boundary DoU Loss = (difference set) / (partial union)`。同时，作者通过目标的 boundary-length-to-size 比例 `C/S` 自适应设定 `α = 1 - 2C/S`，使大目标更强调 boundary、小目标同时兼顾内部与边界。这样得到一个无需额外距离图、无需额外辅助损失、但仍显式强化 boundary region 的简单区域型损失。

关键页码：

- `Sec.2.2, p.3-p.4`
- `Sec.2.3, p.4`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Boundary IoU = |(Gd ∩ G) ∩ (Pd ∩ P)| / |(Gd ∩ G) ∪ (Pd ∩ P)|
```

符号说明：

- `G`：ground-truth binary mask
- `P`：predicted binary mask
- `Gd, Pd`：对应 inner boundary region
- 作用：作为方法设计的启发来源，不直接用于训练
- 页码：`Eq.(1), p.3`

公式 2：

```text
LDoU = (G ∪ P - G ∩ P) / (G ∪ P - α * G ∩ P)
```

符号说明：

- `G ∪ P - G ∩ P`：prediction 与 GT 的 difference set
- `α * (G ∩ P)`：对交集内部区域的折减，保留 boundary-focused partial union
- `α < 1`：控制 partial union 中 intersection 的保留比例
- 含义：用区域型集合运算近似边界错配程度
- 页码：`Eq.(2), p.3`

公式 3：

```text
α = 1 - 2 * C / S,   α ∈ [0, 1)
```

符号说明：

- `C`：目标的 boundary length
- `S`：目标面积/大小
- 含义：
  - 大目标 `C/S` 小，`α` 大，更聚焦 boundary
  - 小目标 `C/S` 大，`α` 小，同时兼顾 interior 与 boundary
- 页码：`Eq.(3), p.3-p.4`

公式 4：

```text
LDoU = SD / (SD + SI - α SI)
     = 1 - α' * SI / (SD + α' * SI),   α' = 1 - α
```

符号说明：

- `SD`：difference set 面积
- `SI`：intersection 面积
- 含义：将 Boundary DoU 与 Dice 放在统一集合量框架下比较
- 页码：`Eq.(4), p.4`

公式 5：

```text
LDice = 1 - 2 * SI / (2 * SI + SD)
```

符号说明：

- `SI`：intersection area
- `SD`：difference set area
- 对比意义：Dice 关注整个 intersection，而 Boundary DoU 只部分保留 intersection，更强调 boundary contribution
- 页码：`Eq.(5), p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 关键对比：
  - `Dice` 对整个交集一视同仁
  - `Boundary DoU` 因为 `α < 1`，只对 intersection 的一部分起缓冲作用，因此更强调 boundary-adjacent mismatch
- 行为差异：
  - 最小化 `LDoU` 同样会鼓励 `SI ↑, SD ↓`
  - 但它对 `SD/SI` 比例惩罚更强
  - 当 `SI` 已较高时，`LDoU` 比 `Dice` 下降更快
- 适用条件：
  - 想在保持 Dice 类区域训练稳定性的同时，增强 boundary segmentation
- 不适用场景：
  - 若任务完全由 topology 或 skeleton 决定，`clDice` 类方法可能更直接
- 页码：
  - `Sec.2.3, p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Boundary DoU Loss` | `(G ∪ P - G ∩ P) / (G ∪ P - α * G ∩ P)` | 强化 boundary-adjacent mismatch 的惩罚 | segmentation output |
| `Adaptive α` | `1 - 2C/S` | 依据目标大小调节 boundary emphasis | loss 内部 |

### 5.2 总损失公式

```text
L_total = LDoU
```

说明：

- 这是这篇论文最重要的点之一：
  - 它不依赖额外辅助损失
  - 可以单独训练
  - 目标是比现有 boundary losses 更稳定、更简洁

### 5.3 权重配置与调度策略

- 无额外手工 loss 混合权重
- 唯一核心超参数由自适应策略给出：
  - `α = 1 - 2C/S`
- 对比实验中的其他 loss 设置：
  - `Dice + CE`：
    - UNet / TransUNet: `(0.5, 0.5)`
    - Swin-UNet: `(0.6, 0.4)`
  - `Tversky`: `α = 0.7`, `β = 0.3`
  - `Boundary Loss`：从 `α = 1` 开始，每 epoch 减 `0.01`，直到 `0.01`
- 页码：
  - `p.3-p.4`
  - `p.6`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Synapse` | `18 scans` | `12 scans` | `按 TransUNet 设置` | 30 abdominal 3D CT scans |
| `ACDC` | `7/1/2 split` | `test from original 100 scans split` | `train/val/test = 7:1:2` | cardiac MRI, 100 scans used |

### 6.2 数据增强

- 增强列表：`[待确认，当前摘录未展开 augmentation 细节]`
- Patch 提取策略：`统一输入分辨率 224×224`
- 页码：`p.6`

### 6.3 优化器与超参数

- 框架：`PyTorch`
- 优化器：`SGD`
- 初始学习率：`0.01`
- 学习率调度：`沿用 Swin-UNet / TransUNet 源码默认设置 [待确认具体 schedule]`
- Batch size：`24`
- Epoch / Steps：`150 epochs`
- 权重初始化：
  - `UNet` 采用 `ResNet50` backbone
  - encoder 用 `ImageNet pretrained weights`
- 预训练策略：
  - `TransUNet / Swin-UNet` 按原始源码设置
  - `UNet` 用 `ImageNet` 预训练
- 是否冻结部分层：`否`
- 设备：`NVIDIA GTX A4000`
- 页码：`p.6`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；CT/MRI`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：`输入统一到 224×224`
- patch overlap：`未强调`
- 背景过滤策略：`未强调`
- 标签生成方式：
  - 直接用 segmentation masks
  - `α` 通过 target 的 `C/S` 动态计算
- 类别不平衡处理：
  - 通过 target size 自适应边界关注，而不是单独 class re-weighting
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：
  - 应严格保持 scan-level split
- 页码：`p.5-p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | `Dice / CE / Dice+CE / Tversky / Boundary` vs `Ours` | `Ours` 在 Synapse/ACDC 上整体更稳 | Boundary DoU 可单独替代常见 loss 作为主损失 |
| `A2` | 大目标 vs 小目标 | `Ours` 在 large/small 都提升，尤其 small 更明显 | adaptive α 有效 |
| `A3` | UNet / TransUNet / Swin-UNet | 三种 backbone 全部受益 | loss 跨架构有效 |

### 8.2 各模块贡献量化

- Synapse：
  - `UNet`：`Dice 76.38 -> 78.68`, `HD 31.45 -> 26.29`, `B-IoU 86.26 -> 87.08`
  - `TransUNet`：`Dice 78.52 -> 79.53`, `HD 28.84 -> 27.28`, `B-IoU 87.34 -> 88.11`
  - `Swin-UNet`：`Dice 77.98 -> 79.87`, `HD 25.95 -> 19.80`, `B-IoU 86.19 -> 87.78`
- ACDC：
  - `UNet`：`Dice 90.17 -> 90.84`, `B-IoU 75.20 -> 76.44`
  - `TransUNet`：`Dice 90.69 -> 91.29`, `B-IoU 76.66 -> 78.45`
  - `Swin-UNet`：`Dice 90.17 -> 91.02`, `HD 1.34 -> 1.28`, `B-IoU 75.20 -> 77.00`
- 按目标大小分组：
  - ACDC, `UNet`：large `92.60 -> 93.73`, small `84.11 -> 86.04`
  - Synapse, `Swin-UNet`：large `79.97 -> 81.83`, small `41.67 -> 44.08`
- 页码：`Table 1-3, p.5-p.6`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Synapse / UNet` | `DSC 78.68` | `HD 26.29±2.35` | `B-IoU 87.08` | best |
| `Synapse / TransUNet` | `DSC 79.53` | `HD 27.28±0.51` | `B-IoU 88.11` | best |
| `Synapse / Swin-UNet` | `DSC 79.87` | `HD 19.80±2.34` | `B-IoU 87.78` | best |
| `ACDC / UNet` | `DSC 90.84` | `HD 1.54±0.33` | `B-IoU 76.44` | best B-IoU |
| `ACDC / TransUNet` | `DSC 91.29` | `HD 2.16±0.02` | `B-IoU 78.45` | best B-IoU |
| `ACDC / Swin-UNet` | `DSC 91.02` | `HD 1.28±0.00` | `B-IoU 77.00` | strong overall |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Dice` | `Synapse / UNet` | `76.38` | `31.45` | `86.26` |
| `Boundary DoU` | `Synapse / UNet` | `78.68` | `26.29` | `87.08` |
| `Dice` | `Synapse / Swin-UNet` | `77.98` | `25.95` | `86.19` |
| `Boundary DoU` | `Synapse / Swin-UNet` | `79.87` | `19.80` | `87.78` |
| `Dice` | `ACDC / TransUNet` | `90.69` | `2.03` | `76.66` |
| `Boundary DoU` | `ACDC / TransUNet` | `91.29` | `2.16` | `78.45` |

补充文字结论：

- Synapse 上，相比 Dice：
  - `UNet +2.30% DSC`
  - `TransUNet +1.20% DSC`
  - `Swin-UNet +1.89% DSC`
- ACDC 上，相比 Dice：
  - `UNet +0.62% DSC`
  - `TransUNet +0.60% DSC`
  - `Swin-UNet +0.85% DSC`
- 在两套数据上，作者都强调 `Boundary IoU` 指标显著更优，说明方法确实更聚焦 boundary regions

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，UNet / TransUNet / Swin-UNet 上仅替换 loss`
- 是否统一数据增强：`沿用原始源码设置 [待确认细节]`
- 是否统一后处理：`文中未强调额外后处理差异`
- 是否统一输入尺寸：`224×224`
- 结果来源：`原文 Table 1-3`
- 页码：`p.5-p.6`

### 9.4 评价协议与指标定义

- 数据划分来源：
  - Synapse：`18 train / 12 test`
  - ACDC：`7:1:2`
- 结果汇报层级：`test set`
- Dice 类型：`DSC`
- Hausdorff 类型：`HD`
- boundary 指标：
  - `Boundary IoU / B-IoU`
- 是否含后处理后再报结果：`未说明`
- 是否多 seed 平均：`未说明`
- 是否报告标准差 / 置信区间：`表中对 HD 给出 ±`
- 页码：`p.5-p.6`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/sunfan-bvb/BoundaryDoULoss`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - `α = 1 - 2C/S` 中 boundary length `C` 的具体实现需与作者一致
  - 不同数据集上 small / large target 划分阈值需明确复现
  - 仍依赖 backbone 原始训练配置

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定` | `中` |
| 验证集划分 | `是` | `Synapse 18/12；ACDC 7:1:2` | `低` |
| 推理阈值 | `否` | `需查看源码` | `中` |
| 后处理细节 | `否` | `按无额外后处理理解` | `中` |
| 训练轮数停止准则 | `是` | `150 epochs` | `低` |
| 数据预处理 | `部分明确` | `224×224；其他跟原始源码` | `中` |

- 不确定但影响较大的点：
  - `C` 的计算若与作者实现不一致，`α` 会变化
  - Synapse/ACDC 的具体 augmentation 策略在当前摘录中未展开

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 文中主要强调其方法对 boundary region 更有效，但并未主打拓扑保持或距离几何理论
- 方法设计更偏针对医学 segmentation boundary，而非所有结构类型的统一最优损失
- 页码：`Conclusion, p.8-p.9`

### 14.2 我们观察到的潜在问题

- 它依赖 `C/S` 来定义边界重要性，这对目标边界质量和 size estimation 的稳定性有要求
- 对极不规则、细碎或多实例目标，单个目标的 `C/S` 统计可能不够稳
- 虽然 B-IoU 一致提升，但在 ACDC 的部分 HD 上并非始终最优，说明它更直接优化 boundary overlap 而不一定同时最优所有几何距离指标

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`通过 Fig.3 / Fig.4 展示其他 losses 在小目标和难边界上的失败`
- 典型失败场景：
  - Synapse 上复杂器官如 `stomach / pancreas` 容易出现 boundary localization 不准
  - ACDC 中 `RV` 形状变化大，容易 under-/mis-segmentation
- 对我们任务的映射：
  - 腺体任务中的黏连边界、细小腺体和轮廓不清区域，与本文强调的 boundary region 难点高度一致
  - 但如果未来更关注 topology 或 instance separation，仅靠 Boundary DoU 可能还不够
- 页码：`p.6-p.8`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 用 `difference set / partial union` 形式构建 boundary-aware 区域损失
- 用 `C/S` 自适应控制边界关注强度
- 在保持 Dice 类稳定训练特性的同时，显式提高对 boundary segmentation 的重视

### 15.2 可以作为候选参数来源的

- `α = 1 - 2C/S`
- 如果需要做对照，可与：
  - `Dice`
  - `Dice + CE`
  - `Boundary loss`
  - `Tversky`
  组成同组实验

### 15.3 不应照搬的（及原因）

- 不加检查地直接替代所有主损失：
  - 原因：如果任务目标不仅是 boundary，还包含 topology、instance split 或 region calibration，可能需要联合其他 loss
- 直接照搬 small/large target 划分阈值：
  - 原因：作者的 `C/S < 0.2` 针对 ACDC/Synapse，不一定适用于腺体数据

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界区域损失 | Boundary DoU 直接强化 boundary-adjacent mismatch | `强` |
| 自适应小目标/大目标边界关注 | `α = 1 - 2C/S` 给出简单可落地策略 | `强` |
| Dice 替代/补充实验 | 它本质上是更 boundary-aware 的 Dice-like loss | `强` |
| 黏连腺体边界优化 | 可作为难边界专门损失候选 | `中` |
| topology/骨架任务 | 不是直接针对 connectivity 的损失 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失函数候选池`、`边界优化实验设计`
- [ ] 需要和哪篇论文交叉验证：`Boundary-Loss_2019`、`Distance-Map-Loss_2019`
- [ ] 待确认的问题：`腺体任务中 Boundary DoU 更适合单独用还是与 Dice/CE 组合`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 现有损失更关注 overall segmentation，边界优化不足 | 作为 boundary-focused loss 动机 |
| related work | Boundary IoU inspired differentiable loss 路线 | 放在 boundary-aware loss 小节 |
| 方法 | `LDoU` 与 `α = 1 - 2C/S` 公式 | 作为自适应边界损失出处 |
| 实验设置 | ACDC / Synapse 上与 Dice、Boundary、Tversky 的对照范式 | 作为实验设计参考 |
| 讨论 | 为什么 small target 更受益于 boundary-aware 自适应策略 | 用于解释结果差异 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.2-p.3` | Boundary IoU 与 Boundary DoU 关系示意 | 写方法动机 |
| `Eq.(2)` | `p.3` | Boundary DoU Loss 定义 | 回填主公式 |
| `Eq.(3)` | `p.3-p.4` | adaptive `α` 策略 | 回填 size-aware 设计 |
| `Eq.(4)-(5)` | `p.4` | Boundary DoU 与 Dice 的统一表达对比 | 解释差异 |
| `Table 1` | `p.5` | Synapse 实验结果 | 数字引用 |
| `Table 2` | `p.5-p.6` | ACDC 实验结果 | 数字引用 |
| `Table 3` | `p.6` | large/small target 对比 | 支撑 adaptive strategy |
| `Figure 3-4` | `p.6-p.8` | Synapse / ACDC 定性结果 | 说明复杂边界优势 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 optimizer、lr、batch、epoch、input size
- [x] `difference set / partial union / adaptive α` 逻辑已完整记录
- [x] 结果数字与原文表格关键项已核对
- [x] 指标定义和评价协议已确认（DSC / HD / B-IoU）
- [x] 消融实验结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
