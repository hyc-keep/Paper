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

- `boundary-aware loss`
- `level-set / distance-map based contour loss`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为原文还给出了较完整的训练细节、`α` 调度策略和 benchmark 对比，所以额外补全：`6, 7, 16`

---

## 1. 论文信息

- 论文名：`Boundary loss for highly unbalanced segmentation`
- 作者/团队：`Hoel Kervadec, Jihene Bouchtiba, Christian Desrosiers, Eric Granger, Jose Dolz, Ismail Ben Ayed`
- 发表年份/会议/期刊：`2019, MIDL 2019 / Medical Image Analysis 路线工作`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1812.07032`
- BibTeX key：`kervadec2019boundary`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Boundary_loss_for_highly_unbalanced_segmentation_2019.pdf`
- 当前定位：`边界损失路线的代表论文；核心价值是把 contour-space 的距离转成可与 softmax 输出直接耦合的区域积分形式，从而在 highly unbalanced segmentation 中补足纯区域损失的不足`
- 与已提取论文的关系：
  - 与 `Distance-Map-Loss_2019` 形成近邻对照：二者都用 GT 派生的距离信息，但这篇更强调 contour distance 与 level-set 表达
  - 与 `Gated-SCNN_2019` 互补：`Gated-SCNN` 偏结构边界流，这篇偏损失层边界约束
  - 可作为后续 `Shape-Aware SDM`、`Boundary DoU` 的理论前驱

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：常用 `Dice / cross-entropy` 等分割损失建立在 region integrals 上，而 highly unbalanced segmentation 中不同类别的积分量级会相差多个数量级，影响训练性能与稳定性
  - 用途：`问题背景 / 痛点`
  - 页码：`Abstract, p.1; Sec.1, p.1-p.2`
- 句子/事实 2：boundary loss 在 contour space 上定义距离，而不是在 region space 上求和，因此能缓解极度类别不平衡问题
  - 用途：`方法动机`
  - 页码：`Abstract, p.1; Sec.2, p.4-p.6`
- 句子/事实 3：boundary loss 与 regional losses 是互补关系，而不是替代关系
  - 用途：`方法定位`
  - 页码：`Abstract, p.1; Sec.2, p.6`

#### 1.1.2 related work 可引用句

- 句子/事实 1：论文指出 Hausdorff-based loss 虽能引入边界几何信息，但需要在每个 epoch 重新计算距离图，对 3D 尤其昂贵
  - 用途：`与相关边界损失对比`
  - 页码：`Sec.1, p.2; Sec.3.2, p.8-p.9`
- 句子/事实 2：boundary loss 通过 integral approach 把 contour distance 改写成区域积分，避免直接对 contour points 做局部微分计算
  - 用途：`理论创新点`
  - 页码：`Sec.2, p.5-p.6`
- 句子/事实 3：仅用 boundary loss 会快速塌缩到 empty foreground，必须与 regional loss 联合使用并设计合适的 `α` 调度
  - 用途：`实际训练注意事项`
  - 页码：`Sec.2, p.6; Sec.3.6, p.11`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| ISLES 划分 | `74 train / 20 val` | 数据集设置 | `p.7-p.8` |
| WMH 划分 | `50 train / 10 val` | 数据集设置 | `p.7-p.8` |
| 输入处理 | `3D scan -> independent 2D slices` | 预处理设置 | `p.9-p.10` |
| resize | `256×256 if needed` | 预处理设置 | `p.9-p.10` |
| 数据增强 | `none` | 训练设置 | `p.9-p.10` |
| 架构 | `UNet` | backbone | `p.9-p.10` |
| optimizer | `Adam` | 训练设置 | `p.9-p.10` |
| 学习率 | `0.001` | 训练设置 | `p.9-p.10` |
| batch size | `8` | 训练设置 | `p.9-p.10` |
| lr schedule | `20 epochs 无提升则减半` | 训练设置 | `p.9-p.10` |
| `α` 初值 | `0.01` | loss scheduling | `p.9-p.10` |
| `α` 增量 | `每个 epoch +0.01` | loss scheduling | `p.9-p.10` |
| 评价指标 | `DSC`, `HD95` | 评价协议 | `p.10-p.11` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 传统分割损失大多对区域做积分，foreground 与 background 在极度不平衡时数值量级相差很大
- 这种不平衡会让 CE、Dice 及其加权变体在 very small structures 上训练不稳定，甚至偏向 majority class
- 区域损失没有显式编码 “距离边界多远” 的信息，区域内所有点被一视同仁
- 医学图像中很多 lesion / WMH / stroke segmentation 都属于典型 highly unbalanced segmentation，需要更直接的 contour-space supervision

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.3`
- `WMH may be 500x smaller than background, p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文从 ground-truth region 的边界 `BG` 出发，利用 level-set 函数 `φG` 把 contour-space 上的非对称 `L2` boundary distance 近似改写为对整个图像域的区域积分；再将二值区域指示函数替换为网络 softmax 输出 `sθ(q)`，得到可直接优化的 `boundary loss`。该损失本身只编码 boundary information，因此训练时与任意 regional loss `LR` 组合为 `LR + αLB`，并通过 `α` 的增长或 rebalance 调度，在早期依赖区域监督避免塌缩、后期增强边界约束。

关键页码：

- `Sec.2, p.4-p.6`
- `Sec.3.4, p.9-p.10`

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
1/2 Dist(BG, BS) = ∫S φG(q) dq - ∫G φG(q) dq
                 = ∫Ω φG(q) s(q) dq - ∫Ω φG(q) g(q) dq
```

符号说明：

- `BG`：GT region `G` 的边界
- `BS`：预测区域 `S` 的边界
- `φG(q)`：GT 边界的 level-set representation
- `s(q)`：区域 `S` 的二值指示函数
- `g(q)`：GT 区域 `G` 的二值指示函数
- 含义：把 contour distance 转写成区域积分，避免显式操作 contour points
- 页码：`Eq.(4), p.5-p.6`

公式 2：

```text
φG(q) = -DG(q), if q ∈ G
φG(q) =  DG(q), otherwise
```

符号说明：

- `DG(q)`：点 `q` 到 GT boundary `BG` 最近点的距离
- 含义：GT 内部为负、外部为正的 signed distance / level-set 表达
- 页码：`p.5-p.6`

公式 3：

```text
LB(θ) = ∫Ω φG(q) sθ(q) dq
```

符号说明：

- `sθ(q)`：网络 softmax 概率输出
- `LB`：boundary loss
- 含义：将二值区域指示函数替换为 softmax 后得到可微边界损失
- 页码：`Eq.(5), p.6`

公式 4：

```text
L_total(θ) = LR(θ) + α LB(θ)
```

符号说明：

- `LR`：任意 regional loss，如 `GDL`、`CE`、`focal` 等
- `α`：平衡 regional 与 boundary loss 的权重
- 含义：boundary loss 作为边界几何补充项，与区域损失联合优化
- 页码：`Eq.(6), p.6`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 梯度特性：
  - `LB` 的梯度等于 `φG` 乘以 softmax prediction 的梯度
  - 在 GT 内部，`φG < 0`，推动 `sθ` 增大
  - 在背景区域，`φG > 0`，推动 `sθ` 减小
  - 离 GT boundary 越远，梯度系数绝对值越大
- 理论含义：
  - loss 最优点对应预测与 GT 完全重合
  - 但 empty foreground 也会导致低梯度，形成近似局部最小/鞍点
- 实践结论：
  - 不能只用 boundary loss
  - 必须联合 regional loss，并在训练早期让 regional term 主导
- 页码：
  - `p.6`
  - `p.11`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Boundary Loss` | `LB(θ) = ∫Ω φG(q) sθ(q) dq` | 约束预测边界与 GT 边界距离 | network softmax output |
| `Regional Loss` | `LR(θ)` | 维持区域级分割监督 | softmax output |
| `Joint Loss` | `LR + αLB` | 同时优化区域重叠与边界几何 | 最终训练目标 |

### 5.2 总损失公式

```text
L_total = LR + α LB
```

补充说明：

- 这篇论文不主张用 boundary loss 替代区域损失
- 它的定位是 `complement regional information`
- 可与 `GDL`、`UNet CE`、`focal loss` 等多种区域损失组合

### 5.3 权重配置与调度策略

- `α` 选择策略：
  - `Constant α`
  - `Increase α`
  - `Rebalance α`
- `Increase α`：
  - 从较小 `α > 0` 开始
  - 每个 epoch 末逐步增加
  - `LR` 权重保持不变
- `Rebalance α`：
  - 改写为 `(1 - α) LR + α LB`
  - 随训练推进逐步增加 `α`
  - 保证 `LR` 权重始终不为 `0`
- 默认超参数：
  - `α = 0.01` 起始
  - 每个 epoch `+0.01`
- 页码：
  - `p.9-p.10`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `ISLES` | `74` | `[待确认，当前文中主要报告 val]` | `20 val` | 94 个 ischemic stroke lesion multi-modal scans |
| `WMH challenge` | `50` | `[待确认，当前文中主要报告 val]` | `10 val` | 60 个 scans，来自 3 家医院 |

### 6.2 数据增强

- 增强列表：
  - `none`
- Patch 提取策略：
  - 3D scans 被处理为独立 `2D slices`
- 页码：`p.9-p.10`

### 6.3 优化器与超参数

- 框架：`PyTorch`
- 优化器：`Adam`
- 初始学习率：`0.001`
- 学习率调度：`验证性能 20 epochs 无提升则减半`
- Batch size：`8`
- Epoch / Steps：`[待确认，未在当前摘录中给出总 epoch]`
- 权重初始化：`[待确认]`
- 预训练策略：`未见强调，默认从头训练`
- 是否冻结部分层：`否`
- 设备：`NVIDIA GTX 1080 Ti 11GB`
- 页码：`p.9-p.10`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；MRI`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：
  - 归一化到 `[0, 1]`
  - 必要时 resize 到 `256×256`
- patch overlap：`不适用`
- 背景过滤策略：
  - 对只含背景的 slice，`φG` 使用 zero-distance map，默认 regional loss 已足够
- 标签生成方式：
  - 从 GT segmentation mask 预先计算 level-set function `φG`
  - level-set 由 SciPy distance transform 得到
- 类别不平衡处理：
  - 主要通过 `boundary loss + regional loss` 联合处理，而非单纯 class reweighting
- 随机种子/重复次数：
  - `3 independent runs` 用于表格统计均值和标准差
- 数据泄漏风险点：
  - 以 scan 为单位划分，后续复现要避免 slice-level 泄漏
- 页码：`p.9-p.11`

---

## 7. 推理与后处理

- 论文主要讨论训练损失与验证结果
- 未强调复杂后处理
- 重要实现点：
  - level-set / distance map 从完整初始 3D segmentation mask 计算
  - 训练更新时可只取图像域 `Ω` 的子集，因此允许用 2D mini-batches 配合 3D distance map
- 页码：`p.9-p.10`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | 各种 `LR` 单独使用 vs `LR + LB` | 多数设置下 DSC/HD95 都改善 | boundary loss 对区域损失有互补作用 |
| `A2` | `LB (2D)` vs `LB (3D)` | 3D distance map 通常再带来约 `1% DSC` 提升 | 在切片相关性高的数据上 3D 边界信息更有利 |
| `A3` | `Constant α` / `Increase α` / `Rebalance α` | 调度优于生硬固定常数 | 训练前期应由 regional term 引导 |
| `A4` | 仅用 `LB` | 网络迅速塌缩到 empty foreground | boundary loss 不能单独优化 |

### 8.2 各模块贡献量化

- `ISLES` 上：
  - `GDL`: `DSC 0.511`, `HD95 5.320`
  - `GDL + LB (2D)`: `DSC 0.644`, `HD95 4.795`
  - `GDL + LB (3D)`: `DSC 0.659`, `HD95 2.725`
  - 论文总结为：相对 `GDL` 单独使用，`DSC` 提升约 `13%`
- `WMH` 上：
  - `GDL`: `DSC 0.768`, `HD95 3.634`
  - `GDL + LB (2D)`: `DSC 0.793`, `HD95 2.039`
  - `GDL + LB (3D)`: `DSC 0.818`, `HD95 1.702`
- 与 `Hausdorff loss` 对比：
  - `ISLES` 上 `GDL + LHD` 有提升，但仍低于 `GDL + LB (3D)`
  - 说明 boundary loss 在某些数据集上优于 Hausdorff-based loss
- 页码：`p.10-p.11`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `ISLES` | `DSC 0.659 ± 0.001` | `HD95 2.725 ± 2.196 mm` | `-` | `GDL + LB (3D)` 最优 |
| `WMH` | `DSC 0.818 ± 0.003` | `HD95 1.702 ± 1.982 mm` | `-` | `GDL + LB (3D)` 最优 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `GDL` | `ISLES` | `DSC 0.511` | `HD95 5.320` | baseline |
| `GDL + LB (3D)` | `ISLES` | `DSC 0.659` | `HD95 2.725` | best |
| `UNet CE` | `ISLES` | `DSC 0.608` | `HD95 4.572` | baseline |
| `Focal loss` | `ISLES` | `DSC 0.631` | `HD95 4.989` | baseline |
| `Focal loss + LB (2D)` | `ISLES` | `DSC 0.650` | `HD95 1.770` | strong |
| `GDL` | `WMH` | `DSC 0.768` | `HD95 3.634` | baseline |
| `GDL + LB (3D)` | `WMH` | `DSC 0.818` | `HD95 1.702` | best |
| `UNet CE` | `WMH` | `DSC 0.757` | `HD95 4.355` | baseline |
| `Focal loss` | `WMH` | `DSC 0.808` | `HD95 1.816` | strong baseline |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，统一使用 UNet`
- 是否统一数据增强：`是，均未做 augmentation`
- 是否统一后处理：`文中未强调差异，重点在损失层对比`
- 是否统一输入尺寸：`必要时统一到 256×256`
- 结果来源：`Table 1 原文数字`
- 页码：`p.9-p.11`

### 9.4 评价协议与指标定义

- 数据划分来源：`作者定义的 train/val split`
- 结果汇报层级：`validation subset`
- Dice 类型：`DSC / Dice Similarity Coefficient`
- Hausdorff 类型：`modified HD95`
- 是否含后处理后再报结果：`未明确强调`
- 是否多 seed 平均：
  - `是，3 independent runs`
- 是否报告标准差 / 置信区间：
  - `是，均值后括号内给标准差`
- 页码：`p.10-p.11`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/LIVIAETS/surface-loss`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - `φG` 的 level-set 计算要与原实现一致
  - 需要正确处理 all-background slices
  - `α` 调度对结果影响明显

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `需固定并重复多次` | `中` |
| 验证集划分 | `是` | `按 ISLES 74/20, WMH 50/10` | `低` |
| 推理阈值 | `否` | `后续复现需看官方代码` | `中` |
| 后处理细节 | `未突出` | `暂按原文默认 pipeline 理解` | `中` |
| 训练轮数停止准则 | `部分明确` | `无 early stopping，lr plateau 20 epochs halve` | `中` |
| 数据预处理 | `部分明确` | `0-1 normalization + 256×256 + modality concat` | `中` |

- 不确定但影响较大的点：
  - total epochs 在当前摘录中未直接给出
  - 不同 `α` 策略的完整日程若要严格复现，需参考官方代码

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- boundary loss 单独使用时不能得到有竞争力的结果，网络会快速塌缩到 empty foreground
- 它不是完整替代方案，而是必须依附于 regional supervision
- 页码：`p.6; p.11`

### 14.2 我们观察到的潜在问题

- 虽然它比 Hausdorff loss 更高效，但仍依赖预计算 level-set / distance map，工程上比纯 Dice/CE 更复杂
- boundary loss 与某些本身已引入 boundary-sensitive weighting 的区域损失之间可能有 “toxic interplay”
- 论文主要验证在 lesion / WMH 这类极不平衡病灶分割上，对腺体这种大面积黏连边界任务需要再验证
- 该损失更擅长边界几何对齐，不直接解决拓扑断裂或实例分离

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`未明确作为 failure cases 小节，但讨论了 empty foreground collapse 和 mixed results`
- 典型失败场景：
  - 仅用 `LB` 时塌缩为空前景
  - `UNet CE + LB` 在 WMH 上没有明显提升，说明损失之间可能互相干扰
- 对我们任务的映射：
  - 腺体分割中如果区域损失已强依赖边界距离信息，叠加 boundary loss 需谨慎
  - 更适合和稳健的区域主损失联用，而不是和过于相似的边界加权再重复堆叠
- 页码：`p.10-p.11`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 用 GT 边界的 level-set / distance map 对 softmax 输出做边界几何约束
- 将 boundary loss 作为 `auxiliary term` 与主区域损失联用
- 对极不平衡结构采用 boundary-space supervision，而不是只靠 region reweighting

### 15.2 可以作为候选参数来源的

- `L_total = LR + αLB`
- 默认 `α = 0.01` 起步，每个 epoch `+0.01`
- 若任务前期容易塌缩，优先使用 `rebalance α` 而不是固定常数

### 15.3 不应照搬的（及原因）

- 直接把 `ISLES / WMH` 的 2D-slice pipeline 迁移到腺体任务：
  - 原因：病理图像不是 3D MRI，输入组织结构和边界统计完全不同
- 只靠 boundary loss，不配区域损失：
  - 原因：原文已明确会塌缩到 empty foreground
- 无 augmentation 的训练方案：
  - 原因：病理图像通常需要更强颜色/几何增强

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 边界辅助损失 | `LB` 可直接作为主分割损失外的边界约束项 | `强` |
| GT 派生监督图 | `φG` 来自 GT mask，无需额外人工边界标注 | `强` |
| 边界-区域联合优化 | 必须与 `Dice/CE/GDL` 等区域损失联合 | `强` |
| 极度不平衡场景 | 对 very small structures 尤其有意义 | `强` |
| 训练调度设计 | `α` 需要随训练逐步增强 | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失函数候选池`、`边界监督设计`
- [ ] 需要和哪篇论文交叉验证：`Distance-Map-Loss_2019`、`Shape-Aware SDM 2020`
- [ ] 待确认的问题：`腺体任务中 boundary loss 更适合和 Dice 还是 BCE/CE 联合`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | highly unbalanced segmentation 中区域损失的固有局限 | 作为边界损失动机 |
| related work | contour-space / level-set based boundary supervision 路线 | 放在 boundary-aware loss 小节 |
| 方法 | `LB = ∫ φG sθ` 与 `LR + αLB` 的直接公式依据 | 作为损失设计出处 |
| 实验设置 | `α` scheduling 的经验 | 用于训练策略设计 |
| 讨论 | 为什么 boundary loss 不能单独用、为什么要联合区域监督 | 用于解释实验现象 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1-p.2` | GDL vs GDL + boundary loss 定性对比 | 展示小区域恢复能力 |
| `Figure 2` | `p.4-p.5` | differential vs integral boundary variation | 解释理论推导 |
| `Eq.(4)` | `p.5-p.6` | contour distance 到区域积分的转换 | 回填理论依据 |
| `Eq.(5)` | `p.6` | boundary loss 定义 | 回填损失公式 |
| `Eq.(6)` | `p.6` | 联合损失 `LR + αLB` | 回填训练目标 |
| `Table 1` | `p.10-p.11` | ISLES / WMH 上不同区域损失与 boundary loss 的对比 | 主结果引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 optimizer、lr、batch、resize、α 调度
- [x] `φG` / distance-to-boundary 的生成逻辑已记录
- [x] 结果数字与原文表格关键项已核对
- [x] 指标定义和评价协议已确认（DSC / HD95）
- [x] 消融结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
