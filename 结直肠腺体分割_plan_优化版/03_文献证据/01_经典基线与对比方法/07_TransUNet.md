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
- [ ] H - 大核/感受野/注意力论文（计算量分析、等效感受野）

副类型说明：

- `Transformer 医学分割论文`
- `CNN + Transformer hybrid encoder 论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇是后续 Transformer 外部对比的重要代表，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`TransUNet: Transformers Make Strong Encoders for Medical Image Segmentation`
- 作者/团队：`Jieneng Chen, Yongyi Lu, Qihang Yu, Xiangde Luo, Ehsan Adeli, Yan Wang, Le Lu, Alan L. Yuille, Yuyin Zhou`
- 发表年份/会议/期刊：`2021, arXiv / 医学分割 Transformer 代表工作`
- DOI / arXiv ID：`[待确认 DOI]` / `arXiv:2102.04306`
- BibTeX key：`chen2021transunet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/TransUNet_Transformers_Make_Strong_Encoders_for_Medical_Image_Segmentation_2021.pdf`
- 当前定位：`Transformer 医学分割外部对比的重要代表；核心不是 pure ViT，而是用 CNN + Transformer hybrid encoder 与 U-Net 式 skip decoder 兼顾 global context 和 localization`
- 与已提取论文的关系：
  - 继承自：`U-Net_2015` 的 U-shape + skip connection
  - 借用 backbone：`ResNet_2016`、`ViT`
  - 互补于：`nnU-Net_2021`、`Attention_U-Net_2018`、`Swin-Unet_2022`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：传统 `U-Net` 受卷积局部性的限制，难以显式建模 long-range dependency
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：Transformer 虽然擅长建模 global context，但如果直接做 naive upsampling，会因低层细节不足而导致 coarse segmentation
  - 用途：`方法动机`
  - 页码：`p.2-p.5`
- 句子/事实 3：`TransUNet` 用 tokenized CNN feature map 进入 Transformer 编码，再结合高分辨率 CNN skip features 实现 precise localization
  - 用途：`方法概述`
  - 页码：`Abstract, p.1-p.5`

#### 1.1.2 related work 可引用句

- 句子/事实 1：论文明确说明 pure Transformer encoder 在 segmentation 中的难点，不是语义不足，而是 localized low-level details 缺失
  - 用途：`related work / 结构分析`
  - 页码：`p.2-p.5`
- 句子/事实 2：`CUP` decoder 明显优于 naive upsampling，而在此基础上继续加入 `CNN hybrid encoder` 与 `skip-connections`，性能还能继续提升
  - 用途：`结构设计依据`
  - 页码：`p.6-p.8`
- 句子/事实 3：增加更多 skip-connections 对小器官的提升更明显，说明全局建模必须和细粒度定位恢复结合
  - 用途：`实验分析 / 对腺体边界任务的启发`
  - 页码：`p.8-p.9`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入分辨率 | `224×224` | 默认实验设置 | `p.6` |
| patch size | `16` | Transformer tokenization | `p.6, p.9` |
| Transformer 层数 | `12` | ViT encoder 设置 | `p.6` |
| 优化器 | `SGD` | 训练设置 | `p.6` |
| 学习率 | `0.01` | 训练设置 | `p.6` |
| momentum | `0.9` | 训练设置 | `p.6` |
| weight decay | `1e-4` | 训练设置 | `p.6` |
| batch size | `24` | 训练设置 | `p.6` |
| ACDC iterations | `20k` | 训练设置 | `p.6` |
| Synapse iterations | `14k` | 训练设置 | `p.6` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- `U-Net` 在医学分割中非常成功，但卷积的局部性使它难以显式捕获 long-range relation
- pure Transformer 擅长 global self-attention，但在 dense prediction 中会因为低分辨率 token representation 缺失局部几何与边界细节，导致 segmentation coarse
- 因此单独 “CNN only” 或 “Transformer only” 都不理想：前者 global context 不够，后者 localization 不够
- 论文目标是找到一种同时保留全局建模能力和精细定位能力的 segmentation encoder-decoder 结构

对应原文依据（页码）：

- `p.1-p.5`

### 2.2 核心思路（一段话概括解法方向）

- `TransUNet` 先用 CNN 提取 feature map，再把 feature map tokenized 成 patch sequence 送入 Transformer 编码，以建模 global context；随后通过 cascaded upsampler 将隐藏特征逐步上采样，并与来自 CNN 编码路径的高分辨率特征通过 skip connection 融合，从而在保留 Transformer 全局依赖建模能力的同时恢复细粒度定位信息。

关键页码：

- `Abstract, p.2-p.5`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`CNN + Transformer hybrid U-shape segmentation network`
- Encoder：
  - `CNN feature extractor`
  - `Transformer encoder` for tokenized patch sequence
- Decoder：`CUP (Cascaded Upsampler)`
- Skip 连接：`将高分辨率 CNN features 注入 decoder`
- 默认 backbone 组合：`R50-ViT`

### 3.2 关键模块详细描述

**模块 1：`Patch Tokenization + Transformer Encoder`**

- 位置：`编码路径中后段`
- 操作流程：
  1. 将输入图像或 CNN feature map 切成 non-overlapping patches
  2. 把 patch flatten 后映射到 latent embedding space
  3. 加入 position embedding
  4. 通过多层 `MSA + MLP` Transformer blocks 建模全局上下文
- 页码：`p.3-p.5`

**模块 2：`CNN-Transformer Hybrid Encoder`**

- 位置：`Transformer 前的特征提取部分`
- 操作流程：
  1. 不直接对原图做 pure ViT tokenization
  2. 先经 `ResNet-50` 提取 CNN feature map
  3. 对 feature map 再做 tokenization 并输入 ViT
  4. 保留多尺度 CNN feature 供 decoder skip 使用
- 页码：`p.5-p.6`

**模块 3：`CUP (Cascaded Upsampler)`**

- 位置：`解码路径`
- 操作流程：
  1. 将 Transformer 隐藏表示 reshape 回 feature map
  2. 级联多个 `2× upsampling + 3×3 conv + ReLU` block
  3. 逐步恢复空间分辨率
  4. 与不同尺度的 CNN 特征做融合
- 页码：`p.5-p.6`

**模块 4：`U-Net-like Skip Connections`**

- 位置：`decoder 与 encoder 各中间尺度之间`
- 操作流程：
  1. 从 CNN 编码器提取高分辨率 low-level features
  2. 在 `1/2, 1/4, 1/8` 等尺度注入 decoder
  3. 强化 boundary、shape 和 small structure 的定位能力
- 页码：`p.7-p.9`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| 输入尺寸 | `224×224` | 默认训练与比较设置 | `p.6` |
| patch size | `16×16` | 构造 token sequence | `p.6, p.9` |
| Transformer 层数 | `12` | 全局上下文建模 | `p.6` |
| patch sequence length | `196` | 当 patch=16 时 | `p.9` |
| hybrid encoder | `ResNet-50 + ViT` | 提供 local + global 表征 | `p.6-p.7` |
| decoder | `CUP` | 渐进上采样 | `p.5-p.6` |
| upsampling blocks 数 | `4` | 从 token feature 回到 full resolution | `p.6` |
| skip connections | `3 个中间尺度` | 恢复细节定位 | `p.8-p.9` |

补充：

| 变体 | 说明 |
|------|------|
| `ViT-None` | 纯 Transformer 编码 + naive upsampling |
| `ViT-CUP` | 纯 Transformer 编码 + CUP |
| `R50-ViT-CUP` | hybrid encoder + CUP，但无 U-Net 式 skip |
| `TransUNet` | `R50-ViT-CUP + skip-connections`，完整版本 |

说明：

- 论文的关键结论不是 “Transformer 一上来就赢”，而是 `Transformer + CNN + U-shape decoder + skip` 的组合才真正形成最强版本

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
z0 = [x_p^1 E; x_p^2 E; ...; x_p^N E] + E_pos
```

符号说明：

- `x_p^i`：第 `i` 个 patch 的向量化表示
- `E`：patch embedding projection
- `E_pos`：position embedding
- `z0`：输入 Transformer 的初始 token 序列
- 页码：`p.4`

公式 2：

```text
z'_l = MSA(LN(z_{l-1})) + z_{l-1}
```

符号说明：

- `MSA`：Multi-head Self-Attention
- `LN`：Layer Normalization
- `z'_l`：第 `l` 层注意力块后的中间表示
- 含义：标准 Transformer attention 残差更新
- 页码：`p.4`

公式 3：

```text
z_l = MLP(LN(z'_l)) + z'_l
```

符号说明：

- `MLP`：Transformer feed-forward block
- `z_l`：第 `l` 层输出
- 含义：标准 Transformer MLP 残差更新
- 页码：`p.4`

### 4.2 推导过程或梯度行为

- 论文没有复杂理论推导，重点是结构因果分析
- pure Transformer 把输入看成 1D sequence，能抓 global context，但会损失 low-level localization cues
- CUP 比 naive upsampling 更适合 dense prediction，因为它分层恢复分辨率
- skip connections 进一步把 low-level detail 注回 decoder，尤其改善小器官和边界敏感结构

对应页码：

- `p.5-p.9`

---

## 5. 损失函数

### 5.1 各监督项

- 主文重点不在新 loss，而在结构设计与 encoder-decoder 组合
- 当前全文提取中未看到复杂多项损失设计
- `loss 具体形式 [待确认源码]`；本文更像标准 segmentation supervision

### 5.2 总损失公式

- 主文提取文本中未明确展开总损失公式
- 当前可确定的是论文主卖点不在 loss，而在 `Transformer encoder + CUP + skip` 的结构组合

### 5.3 权重配置与调度策略

- 未见复杂 loss weighting / curriculum / deep supervision 权重调度说明
- 若后续要复现，更应优先核对：
  - 输入分辨率
  - patch size
  - backbone 预训练
  - 训练迭代数

---

## 6. 训练协议

### 6.1 数据集与划分

- `Synapse multi-organ CT`：
  - `30` 个 abdominal CT scans
  - `18` 个训练 case，`12` 个验证 case
  - 共 `8` 个器官
- `ACDC`：
  - `70` 个训练 case
  - `10` 个验证 case
  - `20` 个测试 case
- 3D volume 的评估方式：按 `slice-by-slice` 2D 推理后堆叠回 3D volume

### 6.2 数据增强

- 默认增强：`random rotation / scaling / flipping`
- 论文没有像 `nnU-Net` 那样展开完整 augmentation recipe
- 说明：
  - 本文关注点主要在 encoder-decoder 结构
  - augmentation 是有的，但不是论文本体创新点

### 6.3 优化器与超参数

| 项目 | 数值/策略 | 页码 |
|------|-----------|------|
| optimizer | `SGD` | `p.6` |
| learning rate | `0.01` | `p.6` |
| momentum | `0.9` | `p.6` |
| weight decay | `1e-4` | `p.6` |
| batch size | `24` | `p.6` |
| ACDC 训练迭代数 | `20k` | `p.6` |
| Synapse 训练迭代数 | `14k` | `p.6` |
| GPU | `single Nvidia RTX2080Ti` | `p.6` |

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；本文是 CT / MRI`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：
  - 默认输入 resize 到 `224×224`
  - 也做了 `512×512` 消融
- patch overlap：`未强调 patch overlap 推理；其 patch size 主要用于 tokenization 而不是滑窗训练`
- 背景过滤策略：`未见专门描述`
- 标签生成方式：`标准器官 segmentation mask`
- 类别不平衡处理：`主文未把重点放在 loss reweighting`
- 随机种子/重复次数：`未见固定 seed 说明`
- 数据泄漏风险点：
  - 使用的是 random split，需要注意后续病理任务应切到 patient-level 严格划分

---

## 7. 推理与后处理

- 推理方式：`slice-by-slice` 2D inference
- volume 级评估：把预测 2D slices 堆叠回 3D volume 再评估
- 论文文本中未强调复杂后处理
- 当前重点在：
  - Encoder 是否 hybrid
  - Decoder 是否用 CUP
  - Skip 连接数量如何影响结果

---

## 8. 消融实验

### 8.1 消融设计

- `ViT-None` vs `ViT-CUP`：验证 CUP 是否优于 naive upsampling
- `ViT-CUP` vs `R50-ViT-CUP`：验证 hybrid encoder 是否优于 pure Transformer encoder
- `R50-ViT-CUP` vs `TransUNet`：验证 skip-connections 的增益
- skip 数量消融：`0-skip / 1-skip / 3-skip`
- 输入分辨率消融：`224` vs `512`
- patch size / sequence length 消融：`32 / 16`
- model scale 消融：`Base` vs `Large`

### 8.2 各模块贡献量化

- `Table 1, Synapse`：
  - `ViT-None`：`Average DSC 61.50`, `HD 39.61`
  - `ViT-CUP`：`Average DSC 67.86`, `HD 36.11`
  - `R50-ViT-CUP`：`Average DSC 71.29`, `HD 32.87`
  - `TransUNet`：`Average DSC 77.48`, `HD 31.69`
- 论文直接总结：
  - `ViT-None -> ViT-CUP`：`+6.36% DSC`, `-3.50 mm HD`
  - `ViT-CUP -> R50-ViT-CUP`：`+3.43% DSC`, `-3.24 mm HD`
  - `TransUNet` 相对 `R50-ViT-CUP` 继续提升，并相对 `R50-AttnUNet` 提升 `1.91% DSC`
- skip 消融：
  - `3-skip` 最优
  - 小器官收益比大器官更明显
  - 在 `1/8` 分辨率 skip 中加入轻量 Transformer 可再带来 `+1.4% DSC`
- 输入分辨率消融：
  - `224 -> 512`：Average DSC 从 `77.48` 提升到 `84.36`
  - 但计算开销明显增大
- patch size 消融：
  - `patch=32, seq=49`：`Average DSC 76.99`
  - `patch=16, seq=196`：`Average DSC 77.48`

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 方法 | 结果 | 页码 |
|-------|------|------|------|
| Synapse | `TransUNet` | `Average DSC 77.48`, `HD 31.69` | `p.6-p.8` |
| ACDC | `TransUNet` | `Average DSC 89.71` | `p.10` |
| Synapse | `R50-AttnUNet` | `75.57 / 36.97` | `p.6-p.8` |
| Synapse | `R50-U-Net` | `74.68 / 36.87` | `p.6-p.8` |

### 9.2 与其他方法的对比

- `TransUNet` 在 Synapse 上优于：
  - `V-Net`
  - `DARR`
  - `R50-U-Net`
  - `R50-AttnUNet`
  - `ViT-CUP`
  - `R50-ViT-CUP`
- 关键对比逻辑：
  - pure Transformer baseline 已经可用，但不够强
  - hybrid encoder 能进一步提升
  - 最终还需要 U-Net-like skip connection 才达到最优
- 这说明：
  - global context 不能替代 localization
  - Transformer 医学分割最有效的落地方式之一，是与 CNN/U-shape 做结构融合

### 9.3 公平对比条件确认

- 公平性优势：
  - 多个 Transformer 变体放在同一训练协议下比较
  - 对 `decoder / encoder / skip` 做逐层递进消融
- 需要注意：
  - `R50-U-Net` 与 `R50-AttnUNet` 用了 ImageNet 预训练 `ResNet-50`，属于强化版对比
  - 论文采用 `224×224` 默认分辨率，真实高分辨率潜力更高，但主表为控制计算成本没有全部放大到 `512`

### 9.4 评价协议与指标定义

- `Synapse`：
  - 平均 `DSC`
  - 平均 `Hausdorff Distance (HD)`
- `ACDC`：
  - `DSC`
- 说明：
  - 论文不仅看平均 Dice，也看 HD，因此对边界几何质量有额外约束

---

## 10. 计算量与效率

- 论文明确指出：
  - `512×512` 分辨率会显著提升结果
  - 但计算成本也大幅增加
- patch size 越小，sequence length 越长，global dependency 建模越充分，但 Transformer 计算负担也更高
- 默认采用 `224×224 + patch 16 + base model`，本质上是性能与成本折中
- 对我们项目的含义：
  - 如果未来把 `TransUNet` 放进腺体任务对比，输入分辨率和 patch size 选择会显著影响结论，不能只跑一个默认值就下结论

---

## 13. 开源与复现

- 开源情况：`是`
- 官方代码：`https://github.com/Beckschen/TransUNet`
- 复现难度：`中到高`
- 关键难点：
  - hybrid encoder 细节
  - ViT 预训练权重接入
  - 输入分辨率与 patch size 的显存代价
  - 医学 3D 数据以 2D slice 方式训练/推理的实现细节

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续如复现需手动固定` | `中` |
| 验证集划分 | `部分（给出随机 split）` | `病理任务必须换成 patient-level 划分` | `高` |
| 推理阈值 | `未强调` | `默认多类 argmax [待确认源码]` | `中` |
| 后处理细节 | `未强调` | `暂不视为本方法主贡献` | `中` |
| 训练停止准则 | `部分（固定 iterations）` | `可先按论文迭代数对齐` | `中` |
| 数据预处理 | `部分（输入 resize 明确）` | `病理图像需单独设定颜色/patch 规则` | `高` |
| 具体 loss 形式 | `主文未展开` | `后续结合源码确认` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- pure Transformer 直接上采样不够好
- 高分辨率输入会更强，但计算开销更大
- 小 patch 会带来更好性能，但 sequence length 上升导致开销增加

### 14.2 我们观察到的潜在问题

- 论文验证集中使用的是 CT / MRI，不是病理 RGB 腺体图像，domain gap 很明显
- 使用 `ResNet-50` + ViT 的 hybrid encoder，参数量与训练成本比 U-Net 系列高不少
- 腺体分割里边界细节、实例分离与病理染色变化，比器官分割更复杂；`TransUNet` 的 global context 优势未必自动转成实例分离优势

### 14.3 失败案例 / 定性分析

- pure ViT 变体的结果显示：仅靠 global context，容易丢细粒度结构
- skip 更少时，小器官更受损，说明细节恢复对小目标尤其关键
- 对我们任务的对应关系：
  - 腺体 lumen、薄边界、相邻腺体粘连，都属于不能只靠 coarse semantic token 解决的问题

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `global context + localization` 必须兼顾的设计逻辑
- 用 `hybrid encoder` 替代纯 CNN 的可行路径
- skip connection 数量对小结构的重要性
- `DSC + HD` 组合评价更适合边界敏感任务

### 15.2 可以作为候选参数来源的

- `224×224` 作为最低可跑基线输入
- `patch size = 16`
- `R50-ViT` 作为标准 hybrid 起点
- `SGD(lr=0.01, momentum=0.9, wd=1e-4, bs=24)` 作为原论文训练参考

### 15.3 不应照搬的（及原因）

- `slice-by-slice` 的 3D 医学图像 protocol：我们当前是 2D 病理，不是按体数据堆叠评估
- 直接照搬 `ResNet-50 + ViT + 224`：病理 patch 尺寸、纹理粒度、显存预算都不同
- 论文默认随机 split：对病理任务必须改成严格 patient-level / slide-level 划分

### 15.4 对我们具体模块的支撑

- 对 `外部强对比`：
  - 它很适合代表“Transformer global modeling”路线
- 对 `边界与定位`：
  - 它能支持一个关键判断：global modeling 不能以牺牲 low-level detail 为代价
- 对 `ResNet34-U-Net` 或其他 hybrid 设计：
  - 说明 encoder 强化后，decoder 与 skip 设计仍然是决定性因素

### 15.5 后续行动项

- 若后续把 `TransUNet` 纳入正式对比，需要单独制定病理任务版输入分辨率与 patch size 方案
- 可以把本文与 `Swin-Unet` 连着提取，形成 `hybrid Transformer` vs `pure Transformer` 的成组证据
- 若实验资源有限，可先不实跑，但在 related work 中保留其结构价值

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | 卷积局部性与 long-range dependency 问题 | 作为 Transformer 路线进入医学分割的动机 |
| related work | hybrid Transformer segmentation 路线 | 与 `Swin-Unet`、`SegFormer` 形成一组 |
| 方法 | global + local 融合设计依据 | 支撑是否引入大范围上下文模块 |
| 实验设置 | 输入分辨率、patch size、R50-ViT 默认配置 | 仅作外部参考，不夸大为直接复现 |
| 讨论 | 为什么 pure Transformer 不够、skip 仍关键 | 用来解释边界与细节问题 |

---

## 16. 关键图表索引

| 图/表 | 内容 | 用途 |
|------|------|------|
| `Fig. 1` | Transformer layer 与 TransUNet 总体结构图 | 写模型结构时最关键 |
| `Table 1` | Synapse 主对比结果 | 引用主性能数字 |
| `Fig. 2` | skip-connections 数量消融 | 说明 low-level detail 恢复的重要性 |
| `Table 2` | 输入分辨率消融 | 说明分辨率-性能-成本关系 |
| `Table 3` | patch size / sequence length 消融 | 说明 token granularity 的影响 |
| `Table 5` | ACDC 对比结果 | 证明跨模态泛化 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（优化器+lr+bs+iter+输入尺寸+patch）
- [x] 预处理与数据细节已检查（2D slice inference / resize / split）
- [x] 结果数字与原文 table 一致（已核对主表关键项）
- [x] 指标定义和评价协议已确认（DSC / HD）
- [x] 消融实验的结论已量化（不只是“有效”）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
