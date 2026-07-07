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
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `signed distance map learning`
- `shape-aware joint training`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`02_边界_形状_损失支撑`

- 按模板要求，本篇至少完成：`1, 2, 4, 5, 8, 9, 13, 14, 15`
- 因为这篇同时提出 joint training 机制和完整 3D organ segmentation backbone，所以额外补全：`3, 6, 7, 16`

---

## 1. 论文信息

- 论文名：`Shape-Aware Organ Segmentation by Predicting Signed Distance Maps`
- 作者/团队：`[待确认作者全名，当前摘录未完整显示]`
- 发表年份/会议/期刊：`2020, AAAI 2020`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:1912.03849`
- BibTeX key：`shapeaware2020sdm`
- PDF 路径：`结直肠腺体分割_pdf库/02_边界_形状_损失支撑/Shape-Aware_Organ_Segmentation_by_Predicting_Signed_Distance_Maps_2020.pdf`
- 当前定位：`shape-aware segmentation 的代表工作；核心不是只在边界附近加权，而是把 segmentation task 显式扩展为 SDM regression + segmentation supervision 的联合学习，并通过 differentiable Heaviside 将两者绑定`
- 与已提取论文的关系：
  - 与 `Boundary-Loss_2019` 互补：`Boundary loss` 约束 contour distance，这篇直接学习全局 `signed distance map`
  - 与 `Distance-Map-Loss_2019` 同属距离图路线，但这篇不是给 CE 做加权，而是把 SDM 本身作为预测目标
  - 可与 `Gated-SCNN_2019` 组成“结构显式边界流 vs shape-aware regression target”对照

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：当前 organ segmentation 常能得到较高区域重叠，但往往不 capture overall shape，且缺乏 smoothness
  - 用途：`背景 / 痛点`
  - 页码：`Abstract, p.1; Intro, p.1-p.2`
- 句子/事实 2：由于从 object boundary contours 计算得到的 SDM 与 binary segmentation map 之间存在严格映射，因此可以直接学习 SDM
  - 用途：`方法动机`
  - 页码：`Abstract, p.1; Method, p.3-p.4`
- 句子/事实 3：joint training 的 SDM learning 产生更 smooth、continuous 的结果，并显著减小 Hausdorff distance 和 ASD
  - 用途：`结果总结`
  - 页码：`Abstract, p.1; Experiments, p.5-p.7`

#### 1.1.2 related work 可引用句

- 句子/事实 1：相比把 distance map 作为 regularizer 且在不同 branch 预测 segmentation / distance 的方法，这篇工作通过 differentiable Heaviside 保证 segmentation map 与 SDM 输出的一致性
  - 用途：`related work / 与近邻工作差异`
  - 页码：`Related work, p.2-p.3`
- 句子/事实 2：learning a global SDM 的优势在于更好地捕捉 voxels 间空间关系，并为分割结果提供 confidence / shape representation
  - 用途：`形状表征价值`
  - 页码：`Related work, p.2-p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| Hippocampus 数据量 | `72 CT scans` | 数据集设置 | `p.5` |
| Hippocampus 划分 | `60 train / 12 test` | 数据集设置 | `p.5` |
| MICCAI 2015 H&N | `38 train / 10 test` | 数据集设置 | `p.6` |
| backbone | `3D UNet variant` | 架构设置 | `p.3-p.4; p.6` |
| downsampling 次数 | `6` | backbone 设计 | `p.3` |
| 初始通道数 | `24` | 架构设置 | `p.6` |
| 最大通道数 | `384` | 架构设置 | `p.6` |
| optimizer | `Adam` | 训练设置 | `p.6` |
| 初始学习率 | `5e-4` | 训练设置 | `p.6` |
| lr schedule | `每 25 epochs ×0.8` | 训练设置 | `p.6` |
| epoch | `200 / 600` | Hippocampus / MICCAI 2015 | `p.6` |
| batch size | `1` | 训练设置 | `p.6` |
| GPU | `Tesla P40 24GB` | 训练设置 | `p.6` |
| `λ` | `10` | joint loss 权重 | `p.4-p.5` |
| Heaviside 参数 `k` | `1500` | SDM-to-mask 映射 | `p.4` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 深度学习器官分割结果往往缺少对整体 anatomical shape 的感知，输出不够 smooth / continuous
- binary mask 监督主要强调局部区域分类，缺乏显式全局形状表示
- 对器官这类位置、大小和形状相对稳定的目标，仅靠普通 segmentation loss 不足以约束 shape prior
- 后处理如 morphological operations、CRF、curvature flow 虽可缓解问题，但不是最理想的 end-to-end 方案

对应原文依据（页码）：

- `Abstract, p.1`
- `Intro, p.1-p.2`
- `Related Work, p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文将 organ segmentation 扩展为 `SDM prediction + segmentation map prediction` 的联合学习问题。具体做法是：以 3D UNet backbone 提取体素级表示，直接回归 target organ 的 `signed distance map`，并通过 differentiable approximated Heaviside function 将 SDM 转成 segmentation map，使两种输出在训练阶段保持耦合；联合损失为 `Dice + λ (Lproduct + L1)`，其中 `Lproduct` 专门强调 SDM 符号和 boundary-near 区域的梯度，从而提升边界平滑性、连续性和整体形状保持。

关键页码：

- `Abstract, p.1`
- `Method, p.3-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`3D UNet variant + SDM regression + segmentation joint training`
- Backbone：`deep 3D UNet`
- 输入尺寸：`whole 3D scans / crop 后的 3D head area`
- 输出头：
  - `segmentation map`
  - `signed distance map`

### 3.2 关键模块详细描述

**模块 1：`Deep 3D UNet Backbone`**

- 位置：`主干特征提取`
- 操作流程：
  1. 使用更深的 3D UNet 结构处理体数据
  2. 采用 `6` 次 downsampling 扩大感受野
  3. 用 `group normalization` 替代 batch normalization 以适配小 batch
- 页码：`p.3; p.6`

**模块 2：`SDM Prediction Head`**

- 位置：`主干输出端`
- 操作流程：
  1. 从 GT segmentation map 生成 ground-truth SDM
  2. 将 SDM 归一化到 `[-1, 1]`
  3. 网络输出经过 `tanh` 作为预测 SDM
- 页码：`p.4-p.5`

**模块 3：`Differentiable Heaviside Mapping`**

- 位置：`连接 SDM 输出和 segmentation 输出`
- 操作流程：
  1. 将 predicted SDM 输入平滑 Heaviside 近似函数
  2. 得到 differentiable segmentation representation
  3. 用于 joint training，使 SDM 和 segmentation branch 不再分离
- 页码：`p.4`

**模块 4：`SDM Regression Loss`**

- 位置：`SDM 输出监督`
- 操作流程：
  1. 计算传统 `L1`
  2. 计算新提出的 `Lproduct`
  3. 将二者相加形成 `LSDM`
  4. 再与 Dice segmentation loss 联合
- 页码：`p.4-p.5`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| backbone | `3D UNet variant` | 主体分割网络 | `p.3-p.6` |
| downsampling ops | `6` | 扩大 receptive field | `p.3` |
| initial channels | `24` | 通道起点 | `p.6` |
| max channels | `384` | 容量上限 | `p.6` |
| normalization | `group normalization` | 适配 batch size 1 | `p.3; p.6` |
| output activation for SDM | `tanh` | 归一化 SDM 回归 | `p.4` |
| Heaviside parameter | `k = 1500` | 近似阶跃映射 | `p.4` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
LSeg = LDice = N - Σ_t 2 Σ(y_t p_t + ε) / (Σ y_t + Σ p_t + ε)
```

符号说明：

- `N`：类别数
- `yt`：第 `t` 类 GT
- `pt`：第 `t` 类预测
- `ε`：数值稳定项
- 含义：segmentation branch 的基础 Dice 监督
- 页码：`Eq.(1), p.3-p.4`

公式 2：

```text
φ(x) = 0, x ∈ S
φ(x) = - inf_y∈S ||x-y||_2, x ∈ Ωin
φ(x) = + inf_y∈S ||x-y||_2, x ∈ Ωout
```

符号说明：

- `S`：目标器官表面
- `Ωin` / `Ωout`：器官内部 / 外部区域
- 含义：SDM 在器官内部为负、外部为正、边界为零
- 页码：`Eq.(2), p.4`

公式 3：

```text
f(z) = 1 / (1 + e^(-z / k))
```

符号说明：

- `f(z)`：Heaviside 的平滑近似
- `k`：控制曲线陡峭程度
- 含义：把 SDM 转成 differentiable segmentation map，使联合训练成为可能
- 页码：`Eq.(3), p.4`

公式 4：

```text
Lproduct = - Σ_t y_t p_t / (y_t p_t + p_t^2 + y_t^2)
```

符号说明：

- `yt`：ground-truth SDM
- `pt`：predicted SDM
- 含义：强调预测和 GT 的符号一致性，并在 boundary-near 区域提供更强梯度
- 页码：`Eq.(4), p.4-p.5`

公式 5：

```text
L = LSeg + λ LSDM = LDice + λ (Lproduct + L1)
```

符号说明：

- `LSDM`：SDM branch 的联合回归损失
- `λ`：SDM loss 权重，文中取 `10`
- 含义：segmentation mask 与 SDM 共同训练
- 页码：`Eq.(5), p.5`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 梯度特性：
  - 单独 `L1` 对 multi-organ SDM training 有时不稳定
  - `Lproduct + L1` 在零附近，即 boundary-representing SDM values 附近，具有更大梯度幅值
- 设计意图：
  - 不仅拟合距离值，还惩罚错误符号
  - 让网络更关注 shape sign consistency 和 boundary region
- 适用条件：
  - 目标具有相对稳定的整体形状、位置和大小
  - 任务重视平滑连续边界和整体器官形状
- 不适用场景：
  - 多器官极小结构上，SDM 本身可能学得不够理想
  - 若不同器官之间需要显式关系建模，仅独立预测各器官 SDM 可能不够
- 页码：
  - `p.4-p.5`
  - `Discussion, p.6-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `Dice loss` | `LDice` | segmentation map 重叠 | segmentation output |
| `L1 loss` | `L1` | SDM 数值回归 | SDM output |
| `Product loss` | `Lproduct` | 强化符号正确性与边界附近梯度 | SDM output |
| `Joint SDM loss` | `LSDM = Lproduct + L1` | 稳定 SDM 学习 | SDM branch |
| `Final joint loss` | `LDice + λ(Lproduct + L1)` | segmentation + shape-aware regression | 总损失 |

### 5.2 总损失公式

```text
L_total = LDice + λ (Lproduct + L1)
```

说明：

- 论文明确表明 `SDM-only` 虽更平滑，但单独训练会在小器官上不稳定
- 因此最佳做法是 `SDM + Dice` 联合训练

### 5.3 权重配置与调度策略

- `λ = 10`
- 由 `grid search` 决定
- `k = 1500` 用于近似 Heaviside
- ground-truth SDM 先归一化到 `[-1, 1]`
- 页码：
  - `p.4-p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `Hippocampus CT` | `60` | `12` | `随机划分` | 共 `72` 个病人，1 mm isotropic spacing |
| `MICCAI 2015 Head and Neck` | `38` | `10` | `官方 train/test` | 多器官 CT 分割 |

### 6.2 数据增强

- 增强列表：
  - `[待确认，当前摘录未见显式 augmentation]`
- Patch 提取策略：
  - `MICCAI 2015` 先 crop head area
- 页码：`p.5-p.6`

### 6.3 优化器与超参数

- 框架：`[待确认框架名，文中当前摘录未显式给出，但整体实现是深度学习 3D segmentation training]`
- 优化器：`Adam`
- 初始学习率：`5e-4`
- 学习率调度：`每 25 epochs 衰减为 0.8 倍`
- Batch size：`1`
- Epoch / Steps：
  - `Hippocampus: 200 epochs`
  - `MICCAI 2015: 600 epochs`
- 权重初始化：`[待确认]`
- 预训练策略：`从头训练`
- 是否冻结部分层：`否`
- 设备：`single NVIDIA Tesla P40 24GB`
- 页码：`p.6`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；CT`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：
  - `MICCAI 2015` 裁出 head area
  - Hippocampus scans 为 `1 mm isotropic spacing`
- patch overlap：`未强调`
- 背景过滤策略：`未强调`
- 标签生成方式：
  - 从 GT segmentation map 用 `Danielsson’s algorithm` 计算 GT SDM
  - SDM 归一化到 `[-1, 1]`
- 类别不平衡处理：
  - 依靠 shape-aware joint training，而不是单纯重加权
- 随机种子/重复次数：`未明确`
- 数据泄漏风险点：
  - Hippocampus 需以 patient-level split 保持独立
- 页码：`p.4-p.6`

---

## 7. 推理与后处理

- 推理时输出：
  - 先得到 predicted SDM
  - 再通过 Heaviside function 转为 segmentation result
- 后处理步骤：
  - 无需额外形态学后处理即可减少 isolated false positives
- TTA / Test-time refinement：`未提及`
- 页码：`p.5-p.6`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | `Dice` only vs `SDM` only vs `SDM + Dice` | joint training 在 hippocampus 上四项指标都最好 | segmentation 与 SDM 互补 |
| `A2` | `L1 + Dice` vs `proposed SDM + Dice` | `L1` 版在多器官上不稳定，甚至部分器官失效 | product loss 对稳定训练很关键 |
| `A3` | separate branches vs Heaviside-connected joint prediction | 分支分离时 correspondence 无法保证 | differentiable coupling 有必要 |
| `A4` | single-organ vs multi-organ | 小器官 SDM 更难学习 | shape prior 在 tiny organs 上仍有限制 |

### 8.2 各模块贡献量化

- Hippocampus：
  - `Dice only`: `Dice 0.840±0.025`, `HD 23.568`, `HD95 1.989`, `ASD 0.414`
  - `SDM only`: `Dice 0.757±0.065`, `HD 8.076`, `HD95 3.393`, `ASD 0.714`
  - `SDM + Dice`: `Dice 0.843±0.032`, `HD 5.400`, `HD95 1.747`, `ASD 0.345`
- 结论：
  - `SDM only` 更平滑但整体 Dice 不够
  - `joint training` 同时保住 Dice 并显著降低 HD / ASD
- MICCAI 2015：
  - `Ours w/ Dice` 平均 Dice `0.859`
  - `Ours w/ SDM + Dice` 平均 Dice `0.845`
  - 但 `HD95 average: 3.32 -> 1.98`
  - `Avg HD: 10.95 -> 5.07`
  - `Avg ASD: 0.44 -> 0.39`
- 说明：
  - joint training 在多器官上未必总提升 Dice，但在几何边界指标上明显更好
- 页码：`p.5-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Hippocampus` | `Dice 0.843±0.032` | `HD95 1.747±1.270` | `ASD 0.345±0.130` | `SDM + Dice` 最优 |
| `MICCAI 2015 H&N` | `Average Dice 0.845` | `Average HD95 1.98` | `Avg HD 5.07 / Avg ASD 0.39` | `SDM + Dice` 在几何指标上最优 |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `Dice only` | `Hippocampus` | `Dice 0.840` | `HD95 1.989` | `ASD 0.414` |
| `SDM only` | `Hippocampus` | `Dice 0.757` | `HD95 3.393` | `ASD 0.714` |
| `SDM + Dice` | `Hippocampus` | `Dice 0.843` | `HD95 1.747` | `ASD 0.345` |
| `AnatomyNet` | `MICCAI 2015` | `Average Dice 0.793` | `Average HD95 6.72` | `-` |
| `FocusNet` | `MICCAI 2015` | `Average Dice 0.803` | `Average HD95 2.62` | `-` |
| `Ours w/ Dice` | `MICCAI 2015` | `Average Dice 0.859` | `Average HD95 3.32` | `Avg HD 10.95 / ASD 0.44` |
| `Ours w/ SDM + Dice` | `MICCAI 2015` | `Average Dice 0.845` | `Average HD95 1.98` | `Avg HD 5.07 / ASD 0.39` |

补充结论：

- 小器官提升尤为明显：
  - `Chiasm Dice`: `0.557 -> 0.658`
  - `Optic Nerve L Dice`: `0.644 -> 0.841`
  - `Optic Nerve R Dice`: `0.639 -> 0.825`
- `HD95 average` 比当时 state of the art 再降低约 `0.64`

### 9.3 公平对比条件确认

- 是否统一 backbone：
  - ablation 内部统一使用相同 backbone
- 是否统一数据增强：
  - 当前摘录未强调 augmentation，默认对比设置一致
- 是否统一后处理：
  - joint training 结果强调无需额外 post-processing
- 是否统一输入尺寸：
  - MICCAI 2015 统一 crop 到 head area
- 结果来源：
  - `Table 1-4` 原文数字
- 页码：`p.5-p.7`

### 9.4 评价协议与指标定义

- 数据划分来源：
  - Hippocampus：随机 train/test split
  - MICCAI 2015：challenge testing set
- 结果汇报层级：`test set`
- Dice 类型：`Dice coefficient`
- Hausdorff 类型：
  - `HD`
  - `HD95`
- 其他指标：
  - `ASD = Average Symmetric Surface Distance`
- 是否含后处理后再报结果：
  - 论文重点恰恰是减少对 post-processing 的依赖
- 是否多 seed 平均：`未明确`
- 是否报告标准差 / 置信区间：
  - 单器官表和多器官表中提供若干均值 ± 标准差
- 页码：`p.5-p.7`

---

## 13. 开源与复现

- 代码是否开源：`[待确认]`
- 代码仓库地址：`[待确认]`
- 框架/语言：`[待确认]`
- 预训练权重是否提供：`[待确认]`
- 复现难度评估：`中`
- 复现障碍：
  - SDM 构造、归一化和 Heaviside 近似参数要与原文一致
  - 3D batch size 为 `1`，资源需求较高
  - 多器官情况下各器官 SDM 独立预测，容易在小器官上不稳定

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需固定` | `中` |
| 验证集划分 | `部分明确` | `Hippocampus 60/12；MICCAI 用官方 train/test` | `中` |
| 推理阈值 | `部分明确` | `通过 Heaviside from predicted SDM` | `中` |
| 后处理细节 | `是` | `强调无需额外后处理` | `低` |
| 训练轮数停止准则 | `是` | `200 / 600 epochs` | `低` |
| 数据预处理 | `部分明确` | `crop head area + SDM normalize` | `中` |

- 不确定但影响较大的点：
  - 框架实现细节和 patch/inference crop 策略在当前摘录中未完全展开
  - 多器官输出层的具体组织方式若不一致，可能影响小器官性能

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 多器官任务中 learned SDMs 并非理想 SDM，尤其在最小器官如 `Chiasm` 上保持形状仍有困难
- 当前 multi-SDM 模型中，各器官 SDM 在最后一层独立预测，器官间缺少显式连接
- 由于 GPU memory 限制，单器官和多器官实验使用了同样网络容量，可能限制了多器官上限
- 页码：`Discussion, p.6-p.7`

### 14.2 我们观察到的潜在问题

- 这篇方法更适合器官这类 shape consistency 强的目标；腺体病理图像的形态变异度通常更大
- `SDM only` 虽平滑，但在小目标上容易不收敛，说明 shape-aware 回归不能完全替代区域监督
- joint training 在多器官上有时会轻微牺牲 Dice 换取更好的几何指标，需要根据任务目标取舍

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是，通过 Figure 6 讨论多器官上的小器官和假阳性问题`
- 典型失败场景：
  - `Dice only` 会产生远离真实器官的 isolated false positives
  - `SDM only` 在 `Chiasm / optic nerves` 等小器官上不收敛
  - `L1 + Dice` 在 `right Submandibular` 上也可能失败
- 对我们任务的映射：
  - 若腺体任务追求边界连续和平滑，可借鉴 joint SDM
  - 但如果目标拓扑变化大、形状多样，SDM 先验过强时可能反而不利
- 页码：`p.5-p.7`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 用 GT mask 生成 `signed distance map` 作为 shape-aware 辅助监督
- 通过 differentiable Heaviside 将 SDM prediction 和 segmentation output 绑定
- 使用 `Dice + λ(Lproduct + L1)` 这种区域监督与形状回归联合训练框架

### 15.2 可以作为候选参数来源的

- `λ = 10`
- `k = 1500`
- SDM 归一化到 `[-1, 1]`
- `group normalization` 适配 3D 小 batch

### 15.3 不应照搬的（及原因）

- 直接把 organ-shape 假设照搬到腺体实例：
  - 原因：腺体形状和大小变异更大，且黏连更复杂
- 直接使用 `batch size 1` 的 3D 训练策略：
  - 原因：我们的任务和资源条件未必相同
- 只关注 `HD / ASD` 而轻视 Dice：
  - 原因：腺体分割通常仍需要兼顾区域重叠和对象分离

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 距离图辅助监督 | SDM 作为全局 shape representation 直接监督网络 | `强` |
| 边界连续性约束 | SDM joint training 可显著降低 HD / ASD 和孤立假阳性 | `强` |
| 边界/形状联合训练 | segmentation map 与 distance map 不应完全分支分离 | `强` |
| 小结构处理 | 结果提示小器官仍是难点，说明 shape prior 需要与区域监督联合 | `中` |
| 3D 小 batch normalization 选择 | `group normalization` 的工程经验可迁移 | `中` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`损失函数候选池`、`shape-aware supervision 设计`
- [ ] 需要和哪篇论文交叉验证：`Distance-Map-Loss_2019`、`Boundary-Loss_2019`、`clDice_2021`
- [ ] 待确认的问题：`腺体分割更适合直接回归 SDM，还是把 SDM 作为辅助 branch`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 普通 segmentation output 缺乏整体形状与平滑性 | 作为 shape-aware 训练动机 |
| related work | global SDM learning 路线 | 放在 distance/surface-based supervision 小节 |
| 方法 | `SDM + Dice` 联合训练公式与 Heaviside 连接方式 | 作为损失与结构设计依据 |
| 实验设置 | `HD / HD95 / ASD` 的完整几何指标框架 | 用于补充评估协议 |
| 讨论 | 为什么 shape prior 能减少 isolated false positives | 用于解释边界和平滑性结果 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 1` | `p.1` | segmentation-only vs SDM 结果的平滑性对比 | 写方法动机 |
| `Figure 2` | `p.3` | SDM learning model 总流程 | 回填结构设计 |
| `Eq.(2)` | `p.4` | signed distance map 定义 | 回填理论定义 |
| `Eq.(3)` | `p.4` | approximated Heaviside function | 回填 differentiable coupling |
| `Eq.(4)` | `p.4-p.5` | proposed product regression loss | 回填损失设计 |
| `Eq.(5)` | `p.5` | final joint loss | 训练目标依据 |
| `Table 1` | `p.5` | hippocampus 结果 | 单器官实验引用 |
| `Table 2-4` | `p.6-p.7` | MICCAI 2015 多器官 Dice / HD95 / HD / ASD 比较 | 多器官结果引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] 公式符号都有解释
- [x] 训练参数已覆盖 optimizer、lr、epoch、batch、λ、k
- [x] SDM 构造与归一化逻辑已记录
- [x] 结果数字与原文表格关键项已核对
- [x] 指标定义和评价协议已确认（Dice / HD / HD95 / ASD）
- [x] 消融实验结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
