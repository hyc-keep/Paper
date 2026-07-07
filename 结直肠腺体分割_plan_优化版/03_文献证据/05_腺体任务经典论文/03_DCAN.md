# 通用文献深提取模板

---

## 0. 论文类型与章节填写指引

### 0.1 类型标记（勾选一个主类型，可标注副类型）

- [x] A - 方法论文（提出新模型/新架构）
- [ ] B - 损失/模块论文（提出新 loss 或即插即用模块）
- [ ] C - 综述论文（Survey / Review）
- [ ] D - 病理/临床论文（形态学定义、分级标准、预后分析）
- [ ] E - 半监督/弱监督论文（标注量假设、伪标签、一致性约束）
- [ ] F - 数据集/竞赛论文（benchmark 定义、评价协议）
- [ ] G - 基线对比论文（经典架构，重点提取架构参数表）
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `gland-specific segmentation`
- `object + contour multi-task learning`
- `deep supervision`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是腺体任务里最关键的 contour-aware 早期深度方法之一
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`DCAN: Deep Contour-Aware Networks for Accurate Gland Segmentation`
- 作者/团队：`Hao Chen, Xiaojuan Qi, Lequan Yu, Pheng-Ann Heng`
- 发表年份/会议/期刊：`2016, arXiv / MICCAI Gland Segmentation Challenge method paper`
- DOI / arXiv ID：`arXiv:1604.02677`
- BibTeX key：`chen2016dcan`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/DCAN_Deep_Contour-Aware_Networks_for_Accurate_Gland_Segmentation_2016.pdf`
- 当前定位：`Boundary Head` 最直接的任务内早期出处之一，也是 `GlaS` challenge 冠军方法的正式技术说明
- 与已提取论文的关系：
  - 继承/发展了更早的 `Semantic Segmentation + Separator` 思路，但改成端到端 FCN + contour multi-task
  - 是后续 `MILD-Net`、`TA-Net`、`DEA-Net` 等腺体边界/拓扑路线的重要前驱
  - 与 `GlaS Challenge 2017` 互补：后者给 benchmark 协议，这篇给冠军方法实现细节

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：腺体形态是 adenocarcinoma 恶性程度评估的重要依据，准确的 gland segmentation 是 reliable morphological statistics 的前提。
  - 用途：`背景 / 临床意义`
  - 页码：`p.1`
- 句子/事实 2：腺体分割的三个主要难点是 gland morphology 大幅变化、touching glands 难以分开，以及 malignant cases 中 gland structure 严重退化。
  - 用途：`问题定义 / 任务难点`
  - 页码：`p.1-p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：DCAN 把 gland objects 与 contours 放到统一 multi-task framework 中同时预测，用 complementary contour information 处理 clustered objects。
  - 用途：`边界分支 / 多任务路线`
  - 页码：`p.2-p.4`
- 句子/事实 2：多层上下文特征配合 auxiliary supervision 可缓解 vanishing gradients，并提升 intermediate features 的 discriminative capability。
  - 用途：`deep supervision 动机`
  - 页码：`p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入尺寸 | `480 x 480` | 方法/实验设置 | `p.5` |
| 优化器 | `SGD` | 实验设置 | `p.4-p.5` |
| 初始学习率 | `0.001` | 实验设置 | `p.5` |
| contour 阈值 | `0.5` | 推理融合 | `p.4` |
| object 阈值 | `0.5` | 推理融合 | `p.4` |
| contour label dilation | `disk filter radius = 3` | 标签生成 | `p.5` |
| 训练增强 | `translation / rotation / elastic distortion` | 数据增强 | `p.5` |
| 训练时间 | `~4 hours` | 计算量/效率 | `p.8` |
| 推理时间 | `~1.5 s / 755 x 522 image` | 计算量/效率 | `p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- benign 与 malignant 的 gland morphology 差异极大，尤其 malignant cases 中 gland structure 会严重退化。
- touching glands 会让实例分离变得困难，单纯依赖 gland object likelihood 容易 merge。
- 以规则结构先验为核心的方法在严重形变的 malignant 情况下容易失败。
- 医学数据标注有限，需要利用 transfer learning 缓解小样本训练问题。

对应原文依据（页码）：

- `p.1-p.2`
- `p.4-p.5`

### 2.2 核心思路（一段话概括解法方向）

- DCAN 以 FCN 为基础，引入 multi-level contextual features 与 auxiliary supervision 提升 gland object 概率图质量，再把 gland object 与 contour 作为两个相关任务放进共享下采样路径的 multi-task network 中联合优化。推理时利用 `object prob >= to` 且 `contour prob < tc` 的融合规则，再配合轻量后处理，把相邻腺体分开并提升对象级分割质量。

关键页码：

- `p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`FCN + multi-level contextual features + dual-branch multi-task segmentation`
- Backbone：`FCN-style encoder-decoder`
- 输入尺寸：`480 x 480`
- 输出头：`双头输出`
  - `gland object mask`
  - `contour mask`

### 3.2 关键模块详细描述

**模块 1：`FCN with multi-level contextual features`**

- 位置：`主干基础网络`
- 操作流程：
  1. 用 5 个 max-pooling 层做下采样、3 个 deconvolution 层做上采样
  2. 从不同层级的 receptive field 生成预测
  3. 通过 summation 融合 multi-level contextual predictions
- 页码：`p.2-p.3`

**模块 2：`Auxiliary supervision`**

- 位置：`中间层辅助分类器 C1-C3`
- 操作流程：
  1. 在中间层加入 `C1-C3` 辅助分类器
  2. 通过辅助监督鼓励梯度反传
  3. 在训练早期加强深层网络优化，后期逐步减小其影响
- 页码：`p.3-p.4`

**模块 3：`Deep contour-aware dual-branch network`**

- 位置：`FCN 上层输出分支`
- 操作流程：
  1. 共享下采样路径参数 `Ws`
  2. 分成 object branch 与 contour branch 两个上采样路径
  3. 分别输出 gland object probability 与 contour probability
  4. 通过 joint multi-task learning 同时优化两任务
- 页码：`p.3-p.4`

**模块 4：`Object-contour fusion`**

- 位置：`推理后处理前`
- 操作流程：
  1. 读取 gland object 概率 `po`
  2. 读取 contour 概率 `pc`
  3. 当 `po >= to` 且 `pc < tc` 时保留为 gland mask
  4. 再做 smoothing、fill holes 和 remove small areas
- 页码：`p.4-p.5`

**模块 5：`Transfer learning from DeepLab`**

- 位置：`下采样路径初始化`
- 操作流程：
  1. 用 `PASCAL VOC 2012` 上训练的 `DeepLab` 模型初始化 downsampling path
  2. 其余层随机高斯初始化
  3. 在 gland 数据上 end-to-end fine-tune
- 页码：`p.4-p.5`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| Input | image | `3` | `480 x 480` | 原文 Figure 3 |
| Downsampling | conv + pool | 未完整列通道 | 逐级降采样 | 与 FCN 类似 |
| Upsampling U1-U3 | deconv | `512 / 512 / 1024` 等 | 逐级恢复 | multi-level context |
| Branch 1 | classifier | object mask | 与输入同尺度输出 | gland segmentation |
| Branch 2 | classifier | contour mask | 与输入同尺度输出 | contour prediction |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
L(I; W) = lambda * psi(W) + sum_a w_a * L_a(I; W) + L_e(I; W)
```

符号说明：
- `psi(W)`：正则项
- `L_a`：auxiliary loss
- `w_a`：各辅助分类器折扣权重
- `L_e`：主数据误差项
- 页码：`Eq.(1), p.3`

公式 2：

```text
L_total(x; theta) = lambda * psi(theta)
                    - sum_{x in X} log p_o(x, l_o(x); W_o, W_s)
                    - sum_{x in X} log p_c(x, l_c(x); W_c, W_s)
```

符号说明：
- `theta = {W_s, W_o, W_c}`
- `W_s`：共享下采样路径参数
- `W_o`：object branch 参数
- `W_c`：contour branch 参数
- `p_o`、`p_c`：object / contour softmax 概率
- 页码：`Eq.(2), p.4`

公式 3：

```text
m(x) = 1, if p_o(x; W_o, W_s) >= t_o and p_c(x; W_c, W_s) < t_c
       0, otherwise
```

符号说明：
- `m(x)`：最终 gland segmentation mask
- `t_o`、`t_c`：阈值，实验中均设为 `0.5`
- object 高且 contour 低时保留目标像素
- 页码：`Eq.(3), p.4`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 辅助分类器通过 deep supervision 缓解 vanishing gradients。
- 辅助项权重 `w_a` 随训练迭代逐渐减小，最后在最终损失中近似忽略。
- 页码：`p.3-p.4`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `L_a` | 辅助分类损失 | 加强中间层训练 | `C1-C3` |
| `L_e` | 数据误差项 | gland 主任务预测 | 主输出 |
| `contour data loss` | `-log p_c(...)` | contour 预测 | contour branch |
| `L2 regularization` | `lambda * psi(theta)` | 参数正则化 | 全网络 |

### 5.2 总损失公式

```text
L_total(x; theta) = lambda * psi(theta)
                    - sum log p_o(...)
                    - sum log p_c(...)
```

### 5.3 权重配置与调度策略

- 各项权重：
  - `lambda`：正则化权重
  - `w_a`：辅助分类器权重
- 是否衰减/动态调整：
  - `w_a` 初值为 `1`
  - 每 `10,000` iterations 除以 `10`
  - 直到边际值 `1e-3`
- 页码：`p.3-p.5`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `GlaS / Warwick-QU` | `85` | `60 + 20` | 官方 challenge test A/B | `37/48` benign/malignant in train |

### 6.2 数据增强

- 增强列表：
  - `translation`
  - `rotation`
  - `elastic distortion`
  - `pincushion / barrel distortions`
- Patch 提取策略：`随机裁剪 480 x 480`
- 页码：`p.5`

### 6.3 优化器与超参数

- 框架：`Caffe`
- 优化器：`SGD`
- 初始学习率：`0.001`
- 学习率调度：`当 loss 停止下降时除以 10，直到 1e-7`
- Batch size：`原文未明确写出`
- Epoch / Steps：`原文未明确写 epoch，总体训练约 4 小时`
- 权重初始化：
  - downsampling path：`DeepLab on PASCAL VOC 2012` 预训练
  - 其余层：`Gaussian initialization`
- 预训练策略：`cross-domain transfer learning`
- 是否冻结部分层：`否，整体 fine-tune`
- 设备：`2.50 GHz Intel Xeon E5-1620 CPU + NVIDIA GeForce GTX Titan X GPU`
- 页码：`p.4-p.5, p.8`

### 6.4 预处理与数据细节

- stain normalization / color normalization：`未说明`
- 颜色空间转换：`默认 RGB`
- resize / crop / pad 策略：`随机 crop 480 x 480`
- patch overlap：`测试阶段使用 overlap-tile strategy`
- 背景过滤策略：`未说明`
- 标签生成方式：
  - gland object：来自病理学家 gland annotations
  - contour：由 connected components 的 boundary 提取后，再用 `disk filter radius=3` 膨胀
- 类别不平衡处理：`未明确说明 class reweighting`
- 随机种子/重复次数：`未说明`
- 数据泄漏风险点：`沿用 GlaS 官方 split，Part A / Part B 等权计分`
- 页码：`p.5`

---

## 7. 推理与后处理

- 推理时输入尺寸：`whole image via overlap-tile strategy`
- 概率阈值：
  - `t_o = 0.5`
  - `t_c = 0.5`
- 后处理步骤：
  1. 融合 object 与 contour probability
  2. `disk filter radius = 3` smoothing
  3. fill holes
  4. remove small areas
  5. connected components 唯一编号
- TTA / Test-time refinement：`无`
- 页码：`p.4-p.5`

---

## 8. 消融实验

### 8.1 消融设计

> 论文最核心的消融是是否融合 contour-aware component。

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| 1 | 去掉 contour-aware 分支，只保留 object prediction (`CUMedVision1`) | `Part A` 低于 `CUMedVision2`，但 `Part B` 某些指标更高 | contour 对 benign/touching glands 更有利，但在部分 malignant 情况可能过分裂 |
| 2 | 保留 contour-aware 分支 (`CUMedVision2`) | `Part A` 多数指标第一，总排名第一 | contour multi-task 对整体结果最优 |

### 8.2 各模块贡献量化

- `F1`：
  - `Part A`: `0.8680 -> 0.9116`
  - `Part B`: `0.7692 -> 0.7158`
- `Object Dice`：
  - `Part A`: `0.8666 -> 0.8974`
  - `Part B`: `0.8001 -> 0.7810`
- 结论：
  - contour-aware 在 `Part A` 明显提升
  - 在 malignant 占比更高的 `Part B` 可能因 interior contour 不准导致过分裂
- 页码：`p.6-p.8`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `Part A` | `F1 0.9116` | `Object Dice 0.8974` | `Hausdorff 45.4182` | `CUMedVision2` |
| `Part B` | `F1 0.7158` | `Object Dice 0.7810` | `Hausdorff 160.3469` | `CUMedVision2` |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `CUMedVision2` | `Part A / Part B` | `0.9116 / 0.7158` | `0.8974 / 0.7810` | `45.4182 / 160.3469` |
| `CUMedVision1` | `Part A / Part B` | `0.8680 / 0.7692` | `0.8666 / 0.8001` | `74.5955 / 153.6457` |
| `ExB1` | `Part A / Part B` | `0.8912 / 0.7027` | `0.8823 / 0.7860` | `57.4126 / 145.5748` |
| `ExB3` | `Part A / Part B` | `0.8958 / 0.7191` | `0.8860 / 0.7647` | `57.3500 / 159.8730` |

### 9.3 公平对比条件确认

- 是否统一 backbone：`否`
- 是否统一数据增强：`否`
- 是否统一后处理：`否`
- 是否统一输入尺寸：`否`
- 结果来源：`原文 challenge tables`
- 页码：`p.6-p.8`

### 9.4 评价协议与指标定义

- 数据划分来源：`GlaS challenge official split`
- 结果汇报层级：`Test Part A / Test Part B`
- 实例匹配规则：`与真值重叠至少 50% 记为 TP`
- Dice 类型：`object-level Dice`
- Hausdorff 类型：`object-level Hausdorff distance`
- F1 类型：`gland detection F1`
- 是否含后处理后再报结果：`是`
- 是否多 seed 平均：`否`
- 是否报告标准差 / 置信区间：`否`
- 是否和官方 challenge protocol 一致：`是`
- 页码：`p.5-p.8`

---

## 10. 计算量与效率

- 参数量（Params）：`未报告`
- 计算量（FLOPs / MACs）：`未报告`
- 推理时间（ms/image）：`约 1.5 s / 755 x 522 image`
- 训练时间（总 GPU-hours）：`约 4 hours`
- 输入尺寸（计算量对应的）：`755 x 522` 测试图像
- 对比方法的效率数据：

| 方法 | Params | FLOPs | 推理时间 |
|------|--------|-------|---------|
| `DCAN` | `N/A` | `N/A` | `~1.5 s / image` |

- 页码：`p.8`

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，但把既有 gland segmentation 方法分成：
  - pixel-based methods
  - structure-based methods

### 11.2 论文指出的研究空白 / Open Problems

1. 结构先验方法在 malignant 严重变形时容易失败
2. 仅 object likelihood 难以处理 touching glands
3. 医学数据有限，需要 transfer learning

### 11.3 对我们选题的启示

- 后面做腺体分割不能只看普通 semantic mask，还要重视 clustered gland separation。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 本篇不是病理标准论文，但多次强调 gland morphology 与 malignancy assessment 的关系。

### 12.2 涉及的生物标志物

- 无。

### 12.3 临床意义

- 可靠 gland segmentation 是提取 morphology statistics、辅助 quantitative diagnosis 的前提。
- 页码：`p.1`

---

## 13. 开源与复现

- 代码是否开源：`否`
- 代码仓库地址：`无`
- 框架/语言：`Caffe`
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中`
- 复现障碍：
  - 辅助分类器结构细节未完全列全
  - 未给 batch size
  - 未给 small area 的具体面积阈值
  - 使用较老的 Caffe / DeepLab 版本

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | 否 | 不依赖逐点复现 | 中 |
| 验证集划分 | 否 | 按官方 train/test 理解，不补脑内 val 比例 | 中 |
| 推理阈值 | 是 | `t_o = 0.5`, `t_c = 0.5` | 低 |
| 后处理细节 | 部分 | 记录了 smoothing / fill holes / remove small areas，但缺具体 small area 阈值 | 中 |
| 训练轮数停止准则 | 否 | 仅记录 learning rate schedule 和总训练时长 | 中 |
| 数据预处理 | 是 | 记录 contour label 生成和 overlap-tile inference | 低 |

- 不确定但影响较大的点：
  - 辅助分类器 `C1-C3` 的具体结构和接入层
  - object / contour 分支的完整通道设置
  - remove small areas 的阈值

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- contour-aware component 在部分 malignant cases 存在副作用
- interior structure 中不准确 contour 可能导致 deformed glands fragmented
- 页码：`p.7-p.8`

### 14.2 我们观察到的潜在问题

- contour 对 benign / touching glands 很有效，但未必对严重退化 malignant 腺体稳定
- 仍需后处理，不是完全“网络输出即实例结果”
- challenge `Part A / Part B` 分布差异会放大不同方法的优势/劣势

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`是`
- 典型失败场景：
  - clustered touching glands 在无 contour 时无法分开
  - malignant cases 中 interior contours 可能导致 over-splitting
  - Part B 因 malignant 占比高而整体更难
- 页码：`Figure 4-5, p.6-p.8`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `object + contour` 双分支的任务内强动机
- `F1 / Object Dice / Object Hausdorff` 作为主结果表指标
- `480 x 480` patch、translation/rotation/elastic distortion 作为腺体任务训练参考

### 15.2 可以作为候选参数来源的

- `disk filter radius = 3` 的 contour label dilation
- `dropout = 0.5`
- `SGD + lr 0.001`
- overlap-tile inference

### 15.3 不应照搬的（及原因）

- 不应无条件照搬 contour-aware 分支到所有 malignant 情况
  - 原因：原文已明确存在 over-splitting 副作用
- 不应把冠军结果简单归因于 contour 分支本身
  - 原因：还叠加了 multi-level contextual features、deep supervision、transfer learning 和后处理

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| `Boundary Head` | 直接输出 contour 并用于 object separation | 强 |
| 多任务监督 | object/contour joint learning 提高中间特征判别性 | 强 |
| deep supervision | `C1-C3` 辅助监督缓解深层优化困难 | 中 |
| transfer learning | DeepLab 预训练缓解小样本问题 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`边界分支动机说明 / 训练协议参考`
- [ ] 需要和哪篇论文交叉验证：`MILD-Net 2018`, `TA-Net 2022`
- [ ] 待确认的问题：`我们的 Boundary Head 是否需要像 DCAN 一样显式参与最终实例融合`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | touching glands 与 malignant deformation 难点 | 任务背景引用 |
| related work | contour-aware gland segmentation 经典路线 | 作为强基线前驱 |
| 方法 | `Boundary Head` 动机与 object+contour 多任务依据 | 直接支撑 |
| 实验设置 | patch / augmentation / inference 候选 | 作为任务内经验来源 |
| 讨论 | contour 在 malignant 上的副作用 | 解释边界分支边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 2` | `p.2-p.3` | multi-level contextual FCN 示意图 | deep supervision / context 参考 |
| `Figure 3` | `p.3` | DCAN 总体结构图 | 双分支结构参考 |
| `Table 1` | `p.6-p.7` | F1 检测结果 | 主结果表引用 |
| `Table 2` | `p.7` | object-level Dice 结果 | 主结果表引用 |
| `Table 3` | `p.8` | Hausdorff 结果 | 边界结果引用 |
| `Table 4` | `p.8` | 最终总排名 | challenge 冠军证明 |
| `Figure 4-5` | `p.6-p.7` | benign / malignant 定性结果 | 失败案例与副作用分析 |

---

## 17. 提取质量自检

- [x] 所有关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数已提取到可复现的主要级别
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致（已核对）
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注
