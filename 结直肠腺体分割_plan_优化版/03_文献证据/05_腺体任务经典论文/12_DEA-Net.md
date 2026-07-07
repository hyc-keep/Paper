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
- [x] G - 基线对比论文（经典架构，重点提取架构参数表）
- [x] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `dual encoder gland segmentation`
- `boundary-enhanced attention`
- `local semantic guidance + feature fusion`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇是当前与你主线最接近的近期腺体分割论文之一，直接围绕恶性腺体形变、相邻腺体黏连和边界恢复展开
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Gland Segmentation via Dual Encoders and Boundary-Enhanced Attention`
- 作者/团队：`Huadeng Wang, Jiejiang Yu, Bingbing Li, Xipeng Pan, Zhenbing Liu, Rushi Lan, Xiaonan Luo`
- 发表年份/会议/期刊：`2024, arXiv`
- DOI / arXiv ID：`arXiv:2401.15990`
- BibTeX key：`wang2024deanet`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Gland_Segmentation_via_Dual_Encoders_and_Boundary-Enhanced_Attention_2024.pdf`
- 当前定位：`05` 目录中较新的 gland-specific 方法，核心是 `dual encoders + FFM + DFB + BEA`，把 local edge semantics 和主干上下文特征结合起来恢复 gland boundaries
- 与已提取论文的关系：
  - 与 [03_DCAN.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/03_DCAN.md) 一样关注 boundary，但从 contour branch 发展到更复杂的 boundary-enhanced attention
  - 与 [07_TA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/07_TA-Net.md) 构成一组很有价值的近期对照：TA-Net 强调 topology，DEA-Net 强调 local boundary recovery
  - 与 [10_SCAU-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/10_SCAU-Net.md) 都使用 attention，但 DEA-Net 的 attention 明确服务于 boundary enhancement

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：作者开篇明确指出 gland segmentation 的三大难点是恶性腺体严重形变、相邻腺体黏连，以及不同腺体在轮廓、大小和形状上的强不一致性。
  - 用途：`任务痛点`
  - 页码：`p.1`
- 句子/事实 2：作者认为现有方法失败的主要原因之一是过多 downsampling 导致局部边缘特征丢失、gland boundary 模糊难辨。
  - 用途：`方法动机`
  - 页码：`p.1-p.2`

#### 1.1.2 related work 可引用句

- 句子/事实 1：DEA-Net 采用双编码器，其中 `pretrained DeepLabv3+` 作为 local semantic-guided encoder，专门补偿主干下采样造成的 edge feature loss。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.1-p.2`
- 句子/事实 2：作者通过 `FFM + DFB + BEA` 逐步加强边界恢复，消融结果表明这些模块都对 `GlaS` 指标有稳定正增益。
  - 用途：`模块有效性论证`
  - 页码：`p.3-p.4`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| GlaS 划分 | `85 train / 60 test A / 20 test B` | 数据集说明 | `p.3` |
| CRAG 划分 | `173 train / 40 test` | 数据集说明 | `p.3` |
| 训练 epoch | `1000` | 训练设置 | `p.3-p.4` |
| optimizer | `Adam` | 训练设置 | `p.3-p.4` |
| initial lr | `5e-4` | 训练设置 | `p.3-p.4` |
| batch size | `4` | 训练设置 | `p.3-p.4` |
| GlaS 输入尺寸 | `416x416` | 训练设置 | `p.3-p.4` |
| CRAG 输入尺寸 | `512x152` [疑似 OCR 异常] | 训练设置 | `p.3-p.4` |
| GlaS 最佳结果 | `F1 89.3 / Dice 89.6 / Hausdorff 60.8` | 主结果 | `Table 1-2, p.4` |
| CRAG 最佳结果 | `F1 86.0 / Dice 89.9 / Hausdorff 129.4` | 主结果 | `Table 2, p.4` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 恶性腺体形态严重变形，使普通网络难以稳定识别。
- 相邻腺体存在黏连，导致 individual gland separation 困难。
- gland outline、size、shape 差异很大，容易发生 under-segmentation。
- 现有方法由于过度下采样，边缘局部特征缺失，边界恢复能力不足。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- DEA-Net 用一个 `dual-encoder` 结构来联合建模全局语义与局部边缘信息：主编码器负责提取上下文语义，`pretrained DeepLabv3+` 组成的 `Local Semantic-Guided Encoder (LD)` 专门提取 gland edge features；之后通过 `Feature Fusion Module (FFM)` 融合双编码器特征，在解码端用 `Deep Feature Decoder Block (DFB)` 恢复空间信息，并在每个 decoder 末端引入 `Boundary-Enhanced Attention (BEA)`，通过自适应阈值增强 gland boundary pixels 的权重，从而改善恶性腺体和黏连腺体的分割。

关键页码：

- `p.2-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`dual-encoder encoder-decoder network`
- 主要组成：
  - `Local Semantic-Guided Encoder (LD)`
  - `main encoder`
  - `Feature Fusion Module (FFM)`
  - `Deep Feature Decoder Block (DFB)`
  - `Boundary-Enhanced Attention (BEA)`
  - `deep supervision`
- 输出方式：`bilinear interpolation upsampling + convolution output`
- 监督方式：`variance-constrained cross-entropy + triple mask supervision`

### 3.2 关键模块详细描述

**模块 1：`Local Semantic-Guided Encoder (LD)`**

- 位置：`第二编码器分支`
- 操作流程：
  1. 使用预训练 `DeepLabv3+`
  2. 仅经历两次下采样
  3. 强化 gland edge 相关低层特征提取
  4. 补偿主网络下采样后的边缘特征损失
- 页码：`p.2`

**模块 2：`Feature Fusion Module (FFM)`**

- 位置：`双编码器输出融合处`
- 操作流程：
  1. 融合 LD 的低层特征 `Fl` 与主编码器特征 `Fh`
  2. 用多尺度提取器处理不同 receptive fields
  3. 用 channel attention 对融合特征加权
  4. 输出更丰富的 fused feature map
- 页码：`p.2-p.3`

**模块 3：`Deep Feature Decoder Block (DFB)`**

- 位置：`decoder`
- 操作流程：
  1. 将低层特征与上采样高层特征双支路结合
  2. 用 bilinear upsampling 恢复空间信息
  3. 提升双编码器融合后的信息恢复能力
- 页码：`p.3`

**模块 4：`Boundary-Enhanced Attention (BEA)`**

- 位置：`每个 decoder 末端`
- 操作流程：
  1. 对 decoder feature `Fs` 做 `3x3` 卷积
  2. 通过 `7x1` 与 `1x7` 卷积构造方向性边界表征
  3. 得到 gland boundary weight map
  4. 用自适应阈值 `delta` 将 boundary pixels 强化
  5. 对 boundary 区域做 feature enhancement
- 页码：`p.3`

**模块 5：`Deep Supervision + Triple Mask`**

- 位置：`训练阶段`
- 操作流程：
  1. 在每个 decoder layer 做 deep supervision
  2. 为每个 gland 构建 `triple mask`
  3. 使用 cross-entropy loss 监督网络学习
- 页码：`p.2-p.4`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| LD encoder | `pretrained DeepLabv3+` | `未逐层明示` | `lower downsampling` | 提取 edge features |
| Main encoder | `3x3 conv blocks + max pooling` | `未逐层明示` | `progressive downsampling` | 提取 context features |
| FFM | `multiscale extractor + channel attention` | `融合后特征` | `多尺度` | 融合双编码器信息 |
| DFB | `dual-branch decoder block` | `未逐层明示` | `upsampled` | 恢复空间信息 |
| BEA | `3x3 + 7x1 + 1x7 + threshold attention` | `boundary map` | `decoder scale` | 强调 gland boundaries |
| 输出层 | `bilinear upsampling + conv` | `triple-mask supervised` | `416x416 / [512x152?]` | CRAG 输入尺寸可能 OCR 异常 |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Fa = F'h ⊗ sigma1(C1(P1(F'h)))
```

符号说明：
- `F'h`：融合前特征
- `P1`：adaptive global pooling
- `C1`：`1x1` convolution
- `sigma1`：sigmoid
- 含义：通过 channel attention 对融合特征重新加权
- 页码：`Eq.(1), p.2`

公式 2：

```text
F'i = Fi, i = 1
F'i = F(i-1) ⊕ Fi, i in [2, 4]
```

符号说明：
- 多尺度提取器在不同 dilation / receptive field 上逐级聚合特征
- `⊕`：文中表示特征融合
- 页码：`Eq.(2)-(3), p.2-p.3`

公式 3：

```text
Fm = sigma2(C1(F'1 © F'2 © F'3 © F'4 © Fa)) ⊕ G(F'h)
```

符号说明：
- `©`：concatenate
- `sigma2`：ReLU
- `G(F'h)`：残差特征融合项
- 含义：多尺度残差融合得到最终 FFM 输出
- 页码：`Eq.(4), p.3`

公式 4：

```text
Fm' = Fm ⊕ sigma1(C(P2(Fm)))
Fc = (Fm' ⊕ Up(Fn)) © Up(Fn)
```

符号说明：
- `P2`：adaptive max pooling
- `Fn`：高层特征
- `Up`：bilinear upsampling
- 含义：DFB 将低层与高层特征结合以恢复空间信息
- 页码：`Eq.(5)-(6), p.3`

公式 5：

```text
Fg = Cv(Cl(C2(Fs))) © Cl(Cv(C2(Fs)))
Mg = sigma1(C1(Fg))
```

符号说明：
- `Fs`：decoder feature map
- `C2`：`3x3` convolution
- `Cl`：`7x1` convolution
- `Cv`：`1x7` convolution
- `Mg`：boundary weight map
- 含义：结合水平与垂直方向卷积构造边界关注图
- 页码：`Eq.(7)-(8), p.3`

公式 6：

```text
Mt[i, j] = 1 if Mg >= delta else 0
delta = C1(P1(Mg))
Fs' = C((Fs ⊗ Mg) ⊕ (Fs ⊗ Mt)) ⊕ Fs
```

符号说明：
- `Mt`：经阈值处理后的 preliminary boundary map
- `delta`：自适应阈值
- `Fs'`：边界增强后的特征
- 含义：用软权重图 `Mg` 和硬阈值图 `Mt` 共同增强 gland boundary
- 页码：`Eq.(9)-(12), p.3`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 论文没有做严格理论推导，更偏工程设计。
- 可直接看到的设计逻辑是：先用 LD 保边缘，再用 FFM 融合多尺度语义，最后用 BEA 做自适应边界强化。

---

## 5. 损失函数

### 5.1 各监督项

- 论文说明使用 `variance-constrained cross-entropy loss`
- 同时为每个 gland 构造 `triple mask`
- 并在每个 decoder layer 进行 deep supervision

### 5.2 总损失公式

```text
主文未给出完整显式总损失展开式；
当前可确认的是：
1) 基础监督为 cross-entropy
2) 监督对象为 triple mask
3) 在每个 decoder layer 做 deep supervision
```

说明：

- 这篇的重点更在结构设计，而非损失公式推导
- `variance-constrained cross-entropy` 的精确写法在当前正文抽取中未展开，需回原 PDF 图文核对

### 5.3 权重配置与调度策略

- 训练 `1000 epochs`
- `Adam`
- `initial lr = 5e-4`
- `batch size = 4`
- 增强包含：
  - horizontal flipping
  - affine transformation
  - random elastic transformation
  - random cropping

---

## 6. 训练协议

### 6.1 数据集与划分

- `GlaS`
  - `165` 张 H&E 图像
  - 来自 `16` 张 WSI
  - 常见尺寸约 `775 x 522`
  - 训练集 `85`
  - 测试集 `60 + 20`
  - 文中所有 GlaS 结果是 test A/B 平均结果
- `CRAG`
  - `213` 张 H&E 图像
  - 来自 `38` 张 WSI
  - 常见尺寸约 `1512 x 1516`
  - 训练集 `173`
  - 测试集 `40`
  - malignant glands 更不规则、更难分割

### 6.2 数据增强

- horizontal flipping
- affine transformation
- random elastic transformation
- random cropping

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| 框架 | `PyTorch` |
| GPU | `2 x NVIDIA GeForce GTX 3090` |
| optimizer | `Adam` |
| initial lr | `5e-4` |
| batch size | `4` |
| epochs | `1000` |
| GlaS input size | `416x416` |
| CRAG input size | `512x152` [疑似 OCR 异常] |

### 6.4 预处理与数据细节

- 文中明确说明为每个 gland 构建 `triple mask`
- 使用 challenge 常见 `F1 / object Dice / object Hausdorff`
- `CRAG 512x152` 很可能是 OCR 问题，需要回 PDF 排版页确认是否应为 `512x512` 或其他尺寸
- 未报告随机种子和验证集切分

---

## 7. 推理与后处理

- 文中未描述复杂后处理，例如 watershed、graph growing 或 morphology filtering
- 推理依赖 decoder 恢复的特征空间信息与 BEA 的边界强化
- 输出目标与评价协议都是 instance-aware 的 gland segmentation 口径

---

## 8. 消融实验

### 8.1 消融设计

- 以 `U-Net as Backbone` 为基础
- 逐步加入：
  - `LD`
  - `FFM`
  - `BEA`
  - `DFB`
- 消融数据集：`GlaS`
- 指标：
  - `F1`
  - `Dice`
  - `Hausdorff`

### 8.2 各模块贡献量化

| 方法 | F1(%) | Dice(%) | Hausdorff |
|------|-------|---------|-----------|
| `Backbone` | `86.1` | `85.1` | `87.318` |
| `Backbone + LD` | `87.4` | `86.9` | `72.181` |
| `Backbone + LD + FFM` | `88.1` | `87.8` | `68.405` |
| `Backbone + LD + FFM + BEA` | `89.1` | `88.8` | `63.786` |
| `DEA-Net` | `89.3` | `89.6` | `60.774` |

- 解读：
  - `LD` 显著改善边缘特征缺失问题
  - `FFM` 继续提升多尺度上下文融合能力
  - `BEA` 再次改善黏连腺体边界恢复
  - 完整 `DEA-Net` 达到最佳结果
- 注意：
  - 正文叙述里有一句 “When we added the DFB module, F1 was 86.1%...” 与表格不一致，明显应以 `Table 1` 为准

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS` | `F1 = 89.3` | `Dice = 89.6` | `Hausdorff = 60.8` | 在文中列出的对比方法中最佳 |
| `CRAG` | `F1 = 86.0` | `Dice = 89.9` | `Hausdorff = 129.4` | `F1 / Dice` 最佳，但 Hausdorff 不是最佳 |

### 9.2 与其他方法的对比

| 数据集 | 方法 | F1(%) | Dice(%) | Hausdorff |
|--------|------|-------|---------|-----------|
| `GlaS` | `DCAN` | `81.4` | `83.9` | `102.9` |
| `GlaS` | `HC-FCN` | `84.5` | `87.0` | `69.1` |
| `GlaS` | `MILD-Net` | `87.9` | `87.5` | `73.7` |
| `GlaS` | `SADL` | `88.9` | `87.3` | `76.7` |
| `GlaS` | `CMD-Net` | `89.0` | `88.1` | `69.2` |
| `GlaS` | `MSFCN` | `88.2` | `88.6` | `66.5` |
| `GlaS` | `GCSBA-Net` | `87.4` | `87.5` | `72.2` |
| `GlaS` | `GAGLVT-Net` | `88.8` | `88.5` | `70.2` |
| `GlaS` | `DEA-Net` | `89.3` | `89.6` | `60.8` |
| `CRAG` | `DCAN` | `73.6` | `79.4` | `218.8` |
| `CRAG` | `DeepLabv3` | `64.8` | `74.5` | `281.4` |
| `CRAG` | `MILD-Net` | `82.5` | `87.5` | `160.1` |
| `CRAG` | `DSE` | `83.5` | `88.9` | `120.1` |
| `CRAG` | `MSFCN` | `82.5` | `89.2` | `130.4` |
| `CRAG` | `TA-Net` | `84.2` | `89.3` | `105.2` |
| `CRAG` | `2D RNN` | `82.6` | `86.5` | `127.2` |
| `CRAG` | `ECGSSL` | `83.6` | `89.3` | `115.2` |
| `CRAG` | `DEA-Net` | `86.0` | `89.9` | `129.4` |

- 任务内解读：
  - `GlaS` 上 DEA-Net 三项都最好
  - `CRAG` 上 DEA-Net 的 `F1 / Dice` 最好，但 `Hausdorff` 仍落后于 `TA-Net`
  - 说明它在 gland detection 与重叠体积一致性上更强，但在边界形状贴合度上并非最优

### 9.3 公平对比条件确认

- 论文使用标准 `GlaS / CRAG` 划分，协议相对清晰
- 采用的是 challenge 常见的对象级三指标，具有较好的任务内可比性
- 但部分细节如 `triple mask` 构造方式、损失完整写法没有完全展开，复现实验仍有门槛

### 9.4 评价协议与指标定义

- 使用三项指标：
  - `F1`
  - `object-level Dice`
  - `object-level Hausdorff distance`
- 论文文字说明：
  - `F1` 评估单个 gland detection accuracy
  - `object-level Dice` 评估 individual glands 的体积重叠精度
  - `object-level Hausdorff` 评估分割结果与真值在形状上的相似性
- 页码：`p.3-p.4`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未报告`
- 训练硬件：`2 x NVIDIA GeForce GTX 3090`
- 间接效率观察：
  - 训练周期长达 `1000 epochs`
  - 双编码器 + 多模块结构意味着工程复杂度与算力成本都不低

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，没有正式提出系统分类框架。

### 11.2 论文指出的研究空白 / Open Problems

- 现有方法在恶性腺体和黏连腺体上的局部边缘建模仍不够强。
- 仅在 gland 数据集上验证仍不足以说明广泛泛化能力。

### 11.3 对我们选题的启示

- 这篇清楚说明：如果你要做边界增强路线，必须同时回答“局部边缘从哪里来”和“融合后如何在 decoder 中恢复”。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 论文提到 benign/malignant glands 与不同 cancer grades，但没有给出临床分级标准表。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- 更准确的 gland segmentation 有助于 colorectal adenocarcinoma 的定量分析与辅助诊断。
- 作者特别强调对 malignant glands 与 adhesive glands 的分割价值。

---

## 13. 开源与复现

- 代码是否开源：`当前正文未提供代码地址`
- 代码仓库地址：`未提供`
- 框架/语言：`PyTorch`
- 预训练权重是否提供：`未说明`
- 复现难度评估：`中到高`
- 复现障碍：
  - `triple mask` 具体构造方法未充分展开
  - `variance-constrained cross-entropy` 公式未完整给出
  - `CRAG input size 512x152` 疑似 OCR 异常
  - 双编码器与多模块的具体通道配置未完整公开

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| `triple mask` 详细生成方式 | 部分 | 只记录其存在，不脑补实现 | 高 |
| `variance-constrained CE` 完整公式 | 部分 | 标记需回原文图式核对 | 高 |
| 各层通道配置 | 否 | 仅记录模块级结构 | 中 |
| 随机种子 | 否 | 不假设固定 seed | 中 |
| 输入尺寸中 CRAG 项 | 部分 | 标记为 `[疑似 OCR 异常]` | 高 |
| 预训练 DeepLabv3+ 具体权重来源 | 否 | 只记录为 `pretrained` | 中 |

- 不确定但影响较大的点：
  - `CRAG 512x152` 的真实输入尺寸
  - `DFB` 在主文叙述中的指标文字错误应如何对应正式版本
  - deep supervision 的具体权重配置

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 论文只在 gland segmentation 数据集上测试，未来还需在更多数据集上验证 generalization。
- 页码：`p.4`

### 14.2 我们观察到的潜在问题

- 方法结构较重，双编码器加多模块，工程成本不低。
- `Hausdorff` 在 `CRAG` 上不如 `TA-Net`，说明边界形状精度仍有提升空间。
- 正文存在明显文字/排版问题，复现时需要以表格和图为准，不宜只信叙述句子。

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`以消融可视化间接展示`
- 定性结论：
  - `LD + FFM` 有助于缓解 small glands 的 under-segmentation 和 sticking
  - `BEA + DFB` 更有利于 adhesive glands 分离
- 页码：`Fig.3, p.4`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `双编码器 + 边界增强` 的模块组合思路
- `DeepLabv3+` 作为 local semantic guided edge encoder 的定位方式
- `F1 + object Dice + object Hausdorff` 的标准对象级评价口径
- `Adam 5e-4, batch size 4, long schedule` 作为近期 gland-specific 训练参考

### 15.2 可以作为候选参数来源的

- `1000 epochs`
- `Adam`
- `lr = 5e-4`
- `batch size = 4`
- `GlaS input 416x416`

### 15.3 不应照搬的（及原因）

- 不应直接照搬其双编码器重结构
  - 原因：和我们方案可能过于同构，且工程复杂度较高
- 不应直接照抄其 `CRAG` 输入尺寸
  - 原因：正文抽取存在 OCR 疑点
- 不应忽视 `Hausdorff` 未占优这一事实
  - 原因：边界增强不必然带来最佳形状相似度

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 局部边缘先验引入 | `LD` 用预训练 DeepLabv3+ 抽边缘特征 | 强 |
| 多尺度特征融合 | `FFM` 解决单感受野局限 | 强 |
| 解码端边界恢复 | `DFB + BEA` 的组合 | 强 |
| 对象级评估选择 | `F1 / object Dice / object Hausdorff` | 强 |
| 恶性腺体泛化论证 | `CRAG` 上强于多种已有方法 | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`主线实验矩阵与边界增强模块对照表`
- [ ] 需要和哪篇论文交叉验证：`07_TA-Net.md`, `10_SCAU-Net.md`, `03_DCAN.md`
- [ ] 待确认的问题：`我们的方案要不要保留一个轻量 local-edge encoder，而不是完整双编码器`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | malignant / adhesive glands 的三大难点 | 任务痛点 |
| related work | dual encoder + boundary enhancement 路线 | 方法脉络 |
| 方法 | local semantic encoder, FFM, BEA | 模块动机 |
| 实验设置 | GlaS / CRAG 协议与训练超参 | 对照设置 |
| 讨论 | F1/Dice 强但 Hausdorff 未最佳 | 结果分析 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.1` | 恶性腺体、黏连腺体与形态差异示例 | 方法动机 |
| `Fig. 2a` | `p.2-p.3` | DEA-Net 总体结构 | 总体架构 |
| `Fig. 2b` | `p.2-p.3` | FFM 模块 | 特征融合 |
| `Fig. 2c` | `p.3` | BEA 模块 | 边界增强 |
| `Fig. 2d` | `p.3` | DFB 模块 | 解码恢复 |
| `Table 1` | `p.4` | GlaS 消融结果 | 模块贡献 |
| `Fig. 3` | `p.4` | Backbone 到 DEA-Net 的分割可视化 | 失败模式与改进 |
| `Table 2` | `p.4` | GlaS 与 CRAG 主表结果 | 横向对比 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（损失与 triple mask 细节仍不足）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已用疑点标记而未脑补
