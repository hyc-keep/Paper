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
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `adaptive receptive field`
- `deformable convolution`
- `deformable RoI pooling`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`03_大核_感受野_形态建模`

- 本篇是“通过自适应采样位置学习感受野”的经典来源，和“大核”“小波域大感受野”是并列路线
- 本篇至少完成：`1, 2, 3, 4, 6, 8, 9, 10, 14, 15, 16`

---

## 1. 论文信息

- 论文名：`Deformable Convolutional Networks`
- 作者/团队：`Jifeng Dai, Haozhi Qi, Yuwen Xiong, Yi Li, Guodong Zhang, Han Hu, Yichen Wei`
- 发表年份/会议/期刊：`2017, ICCV`
- DOI / arXiv ID：`[待确认 DOI]` / `[待确认 arXiv]`
- BibTeX key：`dai2017deformable`
- PDF 路径：`结直肠腺体分割_pdf库/03_大核_感受野_形态建模/Deformable_Convolutional_Networks_2017.pdf`
- 当前定位：`自适应采样/形变感受野的代表论文；核心不是直接扩大 kernel，而是让卷积和 RoI pooling 的采样网格带可学习 offset`
- 与已提取论文的关系：
  - 与 `Large-Kernel-Matters_2017` 互补：GCN 用固定大核扩大覆盖，这篇让采样位置可变形
  - 与 `Wavelet-Convolutions_2024` 互补：那篇做频域大感受野，这篇做几何自适应感受野
  - 对腺体任务有潜在启发，因为腺体边界和腺腔形状常呈现非刚性变形

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CNN 的基础模块具有固定几何结构，因此天然不擅长建模几何变形
  - 用途：`方法动机`
  - 页码：`Abstract, p.1`
- 句子/事实 2：论文提出 `deformable convolution` 与 `deformable RoI pooling`，通过为采样位置引入可学习 offsets 来增强变换建模能力
  - 用途：`核心贡献`
  - 页码：`Abstract, p.1; Sec.2, p.2-p.4`
- 句子/事实 3：这些模块不需要额外监督，可直接替换原始模块并端到端训练
  - 用途：`模块可插拔性`
  - 页码：`Abstract, p.1; Sec.2.3, p.4`

#### 1.1.2 related work 可引用句

- 句子/事实 1：本文的重点不是学习滤波器权重的自由形状，而是学习采样位置
  - 用途：`与 atrous / 大核 / 形状滤波路线区分`
  - 页码：`p.6-p.7`
- 句子/事实 2：学习到的 offsets 会明显随图像内容自适应变化，能覆盖非刚性目标区域
  - 用途：`几何自适应证据`
  - 页码：`p.7-p.8`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| DeepLab best deformable layers | `3` | 分割默认配置 | `p.7` |
| RPN/Faster/R-FCN best deformable layers | `6` 或接近饱和 | 检测消融 | `p.7` |
| RoI pooling gamma | `0.1` | offset normalization | `p.3` |
| VOC training images | `10582` | 分割训练集 | `p.6` |
| Cityscapes split | `2975 train / 500 val` | 分割设置 | `p.6` |
| PASCAL VOC DeepLab baseline -> deformable | `69.7 -> 75.2` | mIoU@V | `p.6-p.7` |
| Cityscapes DeepLab baseline -> deformable | `70.4 -> 75.2` | mIoU@C | `p.6-p.7` |
| COCO R-FCN baseline -> deformable | `30.8 -> 34.5` | mAP@[0.5:0.95] | `p.8` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 传统卷积和 RoI pooling 的采样网格是固定规则网格
- 当目标存在尺度变化、姿态变化、视角变化、局部非刚性变形时，固定网格难以对齐真实几何结构
- 需要一种既保持 CNN 端到端训练优点、又能自适应几何变形的模块

对应原文依据（页码）：

- `Abstract, p.1`
- `Sec.1, p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出在标准卷积和 RoI pooling 的规则采样位置上加入可学习偏移量 `offsets`。在 `deformable convolution` 中，每个卷积采样点都从规则网格位置移动到新的分数坐标，再用双线性插值取值；在 `deformable RoI pooling` 中，每个 bin 的采样位置也由网络预测偏移。这些 offset 由目标任务驱动自动学习，因此卷积感受野和 RoI 对齐区域都能适应目标几何形变。

关键页码：

- `Sec.2.1-Sec.2.3, p.2-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`plain CNN module + learnable offsets`
- 两个核心模块：
  - `deformable convolution`
  - `deformable RoI pooling / deformable PS RoI pooling`
- 模块特征：
  - 输入输出张量维度与原模块兼容
  - 可直接替换现有网络中的 plain counterparts

### 3.2 关键模块详细描述

**模块 1：`Deformable Convolution`**

- 位置：`feature extraction stages`
- 操作流程：
  1. 先用一个卷积层预测 offset fields
  2. 每个卷积核采样位置从规则网格 `p_n` 变为 `p_n + Δp_n`
  3. 对分数位置采用双线性插值采样
  4. 与标准卷积权重相乘求和
- 核心意义：
  - 让 receptive field 自适应图像内容
  - 不是固定 dilation，也不是固定大核
- 页码：`Sec.2.1, p.2-p.3`

**模块 2：`Deformable RoI Pooling`**

- 位置：`region-based detection heads`
- 操作流程：
  1. 对原始 RoI pooling 输出再预测归一化 offsets
  2. 每个 bin 的采样位置加入 `Δp_ij`
  3. 用双线性插值在新的位置上池化
- 特别设置：
  - `γ = 0.1` 用于调节 offset 大小
  - offset 按 RoI 宽高归一化，保证尺度不变性
- 页码：`Sec.2.2, p.3-p.4`

**模块 3：`Deformable PS RoI Pooling`**

- 位置：`R-FCN fully convolutional detection head`
- 操作流程：
  1. 用卷积层生成全分辨率 offset fields
  2. 对每个 RoI 应用 PS RoI pooling 得到归一化 offsets
  3. 再映射回真实偏移位置进行可变形池化
- 页码：`Sec.2.2, p.3-p.4`

### 3.3 架构参数表

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| offset channels | `2N` | 对应 `N` 个 2D offsets | `p.3` |
| interpolation | `bilinear` | 处理分数采样位置 | `p.2-p.3` |
| RoI bins | `7 x 7` | detection 设置 | `p.6` |
| deformable conv layers | `1/2/3/6` 消融 | 感受野自适应范围 | `p.6-p.7` |
| offset init | `zero weights` | 稳定训练 | `p.4` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：标准卷积

```text
y(p0) = Σ_{pn∈R} w(pn) · x(p0 + pn)
```

符号说明：

- `R`：规则卷积采样网格
- `p0`：输出位置
- `pn`：卷积核中的规则采样点
- 页码：`Eq.(1), p.2`

公式 2：deformable convolution

```text
y(p0) = Σ_{pn∈R} w(pn) · x(p0 + pn + Δpn)
```

符号说明：

- `Δpn`：每个采样点对应的可学习 offset
- 感受野不再受固定规则网格限制
- 页码：`Eq.(2), p.2`

公式 3：分数位置的双线性插值

```text
x(p) = Σ_q G(q, p) · x(q)
G(q, p) = g(qx, px) · g(qy, py)
g(a, b) = max(0, 1 - |a - b|)
```

符号说明：

- `p`：分数采样位置
- `q`：整数网格位置
- `G`：双线性插值核
- 页码：`Eq.(3)-(4), p.2-p.3`

公式 4：标准 RoI pooling

```text
y(i, j) = Σ_{p∈bin(i,j)} x(p0 + p) / nij
```

符号说明：

- `(i, j)`：RoI 中第 `i,j` 个 bin
- `nij`：该 bin 内像素数
- 页码：`Eq.(5), p.3`

公式 5：deformable RoI pooling

```text
y(i, j) = Σ_{p∈bin(i,j)} x(p0 + p + Δpij) / nij
```

符号说明：

- `Δpij`：bin 级别的可学习 offset
- 页码：`Eq.(6), p.3`

### 4.2 推导过程或梯度行为

- offset 学习机制：
  - offsets 由额外 conv 或 fc layer 预测
  - 因使用双线性插值，梯度可通过采样操作回传到 offset 分支
- 与 atrous convolution 的区别：
  - atrous 只改变固定 dilation
  - deformable conv 按内容自适应移动采样位置
- 论文实证结论：
  - deformable conv 学到的“有效 dilation”会随目标大小变化，小中大目标分布不同
- 页码：`p.3-p.4; p.6-p.7`

---

## 5. 损失函数

### 5.1 各监督项

| 损失项名称 | 公式 | 监督目标 | 接入位置 |
|-----------|------|---------|---------|
| `task loss` | `[原任务默认损失]` | 分割 / 检测 / proposal 监督 | original task heads |

### 5.2 总损失公式

```text
L_total = L_task
```

说明：

- offsets 不需要额外监督
- 其学习完全由目标任务损失驱动

### 5.3 权重配置与调度策略

- offset learning layer 初始化为 `0`
- 学习率为原网络学习率的 `β` 倍：
  - 默认 `β = 1`
  - Faster R-CNN 的 fc offset layer 用 `β = 0.01`
- 页码：`p.4`

---

## 6. 训练协议

### 6.1 数据集与划分

| 数据集 | 训练量 | 测试量 | 验证集策略 | 备注 |
|--------|--------|--------|-----------|------|
| `PASCAL VOC 2012` | `10582 train` | `1449 val` | `validation` | segmentation |
| `Cityscapes` | `2975 train` | `500 val` | `validation` | segmentation |
| `PASCAL VOC 2007+2012` | `trainval union` | `VOC 2007 test` | `test` | detection |
| `COCO` | `120k trainval` | `20k test-dev` | `test-dev` | detection |

### 6.2 数据增强

- segmentation：
  - 图像短边 resize 到 `360`（VOC）或 `1024`（Cityscapes）
- detection：
  - 图像短边 resize 到 `600`
- mini-batch：
  - 每 GPU `1 image`
- 页码：`p.6`

### 6.3 优化器与超参数

- 优化器：`SGD`
- GPU 数：`8`
- segmentation 迭代数：
  - `VOC 30k`
  - `Cityscapes 45k`
- detection 迭代数：
  - `VOC 30k`
  - `COCO 240k`
- 学习率：
  - 前 `2/3` 为 `1e-3`
  - 后 `1/3` 为 `1e-4`
- detection 额外设置：
  - class-aware RPN 采样 `256 RoIs`
  - Faster R-CNN / R-FCN 分别采样 `256 / 128 RoIs`
  - `7 x 7` RoI bins
- 页码：`p.6`

### 6.4 预处理与数据细节

- backbone：`ResNet-101`
- 用于消融的 deformable conv 层数：
  - `1 / 2 / 3 / 6`
- 默认后续实验：
  - feature extraction networks 用 `3` 个 deformable conv layers
- 页码：`p.6-p.7`

---

## 7. 推理与后处理

- 推理阶段与训练阶段结构一致，不需要额外后处理来修正 offsets
- detection 中仍包含常规后处理，如 `NMS`
- 页码：`p.6-p.7`

---

## 8. 消融实验

### 8.1 消融设计

| 实验编号 | 去掉/替换的组件 | 结果变化 | 结论 |
|---------|---------------|---------|------|
| `A1` | deformable conv 层数从 `1 -> 6` | 分割和检测持续提升后趋于饱和 | 自适应感受野有效 |
| `A2` | atrous conv vs deformable conv | deformable 更优 | 固定 dilation 不如内容自适应采样 |
| `A3` | deformable RoI pooling | 检测进一步提升 | feature alignment 也重要 |
| `A4` | deformable conv + RoI pooling 同时使用 | gains 可叠加 | 两模块互补 |
| `A5` | effective dilation 统计 | offset 分布随目标尺度变化 | offsets 真在学几何适配 |

### 8.2 各模块贡献量化

- Table 1：
  - DeepLab `69.7 -> 73.9 -> 74.8 -> 75.2`
  - class-aware RPN `68.0 -> 73.5 -> 74.3 -> 74.5`
  - Faster R-CNN `78.1/62.1 -> 78.6/63.8 -> 78.5/63.3 -> 78.6/63.3`
  - R-FCN `80.0/61.8 -> 80.6/63.0 -> 81.0/63.8 -> 81.4/64.7`
- Table 3：
  - `deformable conv` 明显优于 `(2,2,2)/(4,4,4)/(6,6,6)/(8,8,8)` atrous conv
  - `deformable conv + deformable RoI pooling` 最强
- 页码：`p.6-p.7`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `PASCAL VOC` | `75.2 mIoU@V` | baseline `69.7` | `+5.5` | DeepLab + deformable conv |
| `Cityscapes` | `75.2 mIoU@C` | baseline `70.4` | `+4.8` | DeepLab + deformable conv |
| `VOC 2007` | `R-FCN 81.4 / 64.7` | baseline `80.0 / 61.8` | improved | mAP@0.5 / @0.7 |
| `COCO test-dev` | `R-FCN 34.5` | baseline `30.8` | `+3.7` | mAP@[0.5:0.95] |

### 9.2 与其他方法的对比

| 方法 | 数据集 | 指标 1 | 指标 2 | 指标 3 |
|------|--------|--------|--------|--------|
| `atrous conv (6,6,6)` | `VOC / Cityscapes` | `73.6 / 72.7` | 固定 dilation | 对照 |
| `deformable conv` | `VOC / Cityscapes` | `75.3 / 75.2` | 内容自适应 | 更优 |
| `R-FCN baseline` | `COCO` | `30.8` | `52.6 AP@0.5` | 对照 |
| `R-FCN + deformable` | `COCO` | `34.5` | `55.0 AP@0.5` | 明显提升 |

### 9.3 公平对比条件确认

- 是否统一 backbone：`是，主要基于 ResNet-101`
- 是否统一任务框架：`是，只替换 plain conv / RoI pooling 模块`
- 是否统一数据与训练设置：`是`
- 结果来源：`VOC/Cityscapes val 与 COCO test-dev`
- 页码：`p.6-p.8`

### 9.4 评价协议与指标定义

- segmentation：`mIoU`
- detection：
  - `VOC`: `mAP@0.5 / mAP@0.7`
  - `COCO`: `mAP@[0.5:0.95]` 与 `mAP@0.5`
- 页码：`p.6`

---

## 10. 计算量与效率

- 参数量几乎不增加太多：
  - `DeepLab 46.0M -> 46.1M`
  - `R-FCN 47.1M -> 49.5M`
- 运行代价有上升但可接受：
  - `DeepLab@V runtime 0.094s -> 0.098s`
  - `R-FCN runtime 0.170s -> 0.193s`
- 含义：
  - 几何适应能力提升不是靠大量堆参数得到的
  - 更像高性价比的可插拔感受野改造
- 页码：`Table 4, p.7`

---

## 13. 开源与复现

- 代码是否开源：`是`
- 代码仓库地址：`https://github.com/msracver/Deformable-ConvNets`
- 框架/语言：`[待确认原始实现框架，倾向 Caffe/CUDA 扩展]`
- 预训练权重是否提供：`仓库待确认`
- 复现难度评估：`中`
- 复现障碍：
  - 需要实现可微分双线性插值和 offset sampling
  - 旧版检测/分割框架与现代实现接口差异较大

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 原始代码框架细节 | `正文未细写` | `后续查仓库` | `中` |
| 各任务完整训练脚本 | `需代码确认` | `优先参考官方实现` | `中` |
| 现代框架迁移细节 | `否` | `参考 mmcv 中 DCN 实现` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文主要针对自然图像检测与语义分割，不是病理图像
- 模块虽轻量，但实现比普通卷积复杂，需要插值与 offset 分支

### 14.2 我们观察到的潜在问题

- 对腺体分割来说，deformable conv 可能有助于非刚性形态建模，但未必直接解决实例黏连
- 若 offset 过于自由，也可能让边界细节变得不稳定，尤其在小目标密集场景
- 因此更适合作为 backbone/encoder 增强，而不是单独替代 boundary/topology 约束

### 14.3 失败案例 / 定性分析

- 论文展示的 offset 可视化说明：
  - 对大目标和复杂几何结构，offset 会明显扩展或偏移
  - 这能覆盖非刚性区域，但也说明模块对数据分布较敏感
- 对我们任务的映射：
  - 腺体边界复杂且形状变化大，理论上适合这类模块
  - 但最好与边界损失或形态约束联用，而不是单独依赖

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- “感受野增强不一定只能靠大核，也可以靠可学习采样位置” 这条论证
- 对非刚性几何结构的建模思路
- 可插拔、端到端、无需额外监督的 offset learning 设计

### 15.2 可以作为候选参数来源的

- deformable conv 可优先放在高层语义特征阶段
- 初始 offset 用零初始化
- 若做 RoI/instance 支线，可参考 `γ = 0.1` 的归一化方式

### 15.3 不应照搬的（及原因）

- 直接把检测用 deformable RoI pooling 搬到当前主线腺体语义分割：
  - 原因：你的主线不是 region-based detector
- 只依靠 deformable conv 解决边界质量：
  - 原因：它更偏几何适应，而不是显式边界监督

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 自适应感受野 | 直接来源论文 | `强` |
| 形态变形建模 | 非刚性结构适配逻辑 | `强` |
| 大核替代路线 | 提供“offset 代替固定大核”的另一条路线 | `中-强` |
| 边界监督 | 间接支持 | `弱` |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`encoder 感受野增强方案`、`非刚性形态建模依据`
- [ ] 需要和哪篇论文交叉验证：`Large-Kernel-Matters_2017`、`Wavelet-Convolutions_2024`
- [ ] 待确认的问题：`是否值得在腺体主干中测试 deformable block 替换部分 3x3 conv`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | CNN 固定几何结构难处理形变 | 作为自适应感受野动机 |
| related work | deformable sampling 路线 | 放在 receptive field / geometry-aware 模块部分 |
| 方法 | offset-based sampling | 作为可选模块设计来源 |
| 实验分析 | 与 atrous conv 的对比逻辑 | 解释为什么固定 dilation 不够 |
| 讨论 | 非刚性结构建模与边界问题不同 | 连接到边界/形态文献 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Figure 2` | `p.2-p.3` | deformable convolution 示意 | 回填核心机制 |
| `Figure 3-4` | `p.3-p.4` | deformable RoI / PS RoI pooling | 回填 detection 分支 |
| `Eq.(1)-(6)` | `p.2-p.3` | 标准/可变形卷积与池化公式 | 回填公式 |
| `Table 1` | `p.6-p.7` | deformable conv 层数消融 | 参数参考 |
| `Table 2` | `p.6-p.7` | effective dilation 统计 | 解释 offsets 行为 |
| `Table 3` | `p.7` | 与 atrous conv 对比 | 对照论据 |
| `Table 4` | `p.7` | 参数量与运行时间 | 效率引用 |
| `Table 5` | `p.8` | COCO 主结果 | 数字引用 |

---

## 17. 提取质量自检

- [x] 关键数字都标注了来源页码
- [x] 可直接引用卡片已填写
- [x] deformable conv / RoI pooling 公式已覆盖
- [x] offset 学习机制与 bilinear interpolation 已记录
- [x] VOC / Cityscapes / COCO 主结果已覆盖
- [x] 与 atrous conv 的对比已写清
- [x] 参数量与运行时代价已补充
- [x] 与我们项目的关联已具体到模块级别
- [x] 不确定内容已标注 `[待确认]`
