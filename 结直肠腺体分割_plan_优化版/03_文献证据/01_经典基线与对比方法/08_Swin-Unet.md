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

- `pure Transformer 医学分割论文`
- `Swin Transformer U-shape 论文`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`01_经典基线与对比方法`

- 按模板要求，本篇至少完成：`1, 3, 6, 7, 9, 10, 13, 15, 16`
- 因为这篇和 `TransUNet` 构成成组对比，所以额外完成：`2, 4, 8, 14`

---

## 1. 论文信息

- 论文名：`Swin-Unet: Unet-like Pure Transformer for Medical Image Segmentation`
- 作者/团队：`Hu Cao, Yueyue Wang, Joy Chen, Dongsheng Jiang, Xiaopeng Zhang, Qi Tian, Manning Wang`
- 发表年份/会议/期刊：`2022, ECCVW 2022 / 医学分割 pure Transformer 代表工作`
- DOI / arXiv ID：`[待确认 DOI]` / `[待确认 arXiv]`
- BibTeX key：`cao2022swinunet`
- PDF 路径：`结直肠腺体分割_pdf库/01_经典基线与对比方法/Swin-Unet_Unet-like_Pure_Transformer_for_Medical_Image_Segmentation_2022.pdf`
- 当前定位：`pure Transformer 医学分割的重要代表；用于和 `TransUNet` 形成成组对比：一个是 CNN+Transformer hybrid，一个是 Swin Transformer 纯 U-shape`
- 与已提取论文的关系：
  - 继承自：`U-Net_2015` 的 encoder-decoder + skip
  - 对比于：`TransUNet_2021`
  - 结构来源：`Swin Transformer`

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：CNN 由于卷积局部性，难以充分学习 local-global 和 long-range semantic interaction
  - 用途：`背景 / 痛点`
  - 页码：`p.1-p.2`
- 句子/事实 2：`Swin-Unet` 被明确提出为 `Unet-like pure Transformer for medical image segmentation`
  - 用途：`方法定位`
  - 页码：`p.1`
- 句子/事实 3：论文明确指出 `skip connection is also effective for Transformer`
  - 用途：`结构分析 / 方法设计依据`
  - 页码：`p.3`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者采用 hierarchical `Swin Transformer with shifted windows` 作为 encoder 提取 context features
  - 用途：`related work / 结构脉络`
  - 页码：`p.1-p.4`
- 句子/事实 2：decoder 采用 `patch expanding layer` 恢复空间分辨率，而不是卷积或插值
  - 用途：`结构亮点`
  - 页码：`p.1, p.4-p.7`
- 句子/事实 3：在 Synapse 上，`Swin-Unet` 相比 `TransUNet` 的 Dice 提升不大，但 HD 从 `31.69` 降到 `21.55`
  - 用途：`实验分析 / 边界质量讨论`
  - 页码：`p.8-p.9`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| 输入分辨率 | `224×224` | 默认实验设置 | `p.8, p.11` |
| 输入分辨率消融 | `384×384` | 输入尺度消融 | `p.11` |
| patch size | `4×4` | tokenization | `p.4, p.8` |
| batch size | `24` | 训练设置 | `p.8` |
| optimizer | `SGD` | 训练设置 | `p.8` |
| momentum | `0.9` | 训练设置 | `p.8` |
| weight decay | `1e-4` | 训练设置 | `p.8` |
| GPU | `Nvidia V100 32GB` | 训练硬件 | `p.8` |
| Synapse 主结果 | `DSC 79.13 / HD 21.55` | 主结果 | `p.8-p.9` |
| ACDC 主结果 | `DSC 90.00` | 泛化结果 | `p.9-p.10` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- 传统 U-Net 及其 CNN 变体虽然强，但卷积局部性限制了 long-range semantic interaction
- `TransUNet` 之类 hybrid 方法已经证明 Transformer 对 segmentation 有价值，但仍然混用了 CNN
- 作者希望验证：在医学图像分割里，是否能构建一个真正的 `pure Transformer-based U-shaped Encoder-Decoder`
- 论文的目标是回答：
  - Transformer 能否单独承担 encoder、bottleneck、decoder 全流程
  - skip connection 对 Transformer 是否仍然有效
  - patch expanding 是否能成为比插值/反卷积更好的上采样方式

对应原文依据（页码）：

- `p.1-p.4`

### 2.2 核心思路（一段话概括解法方向）

- `Swin-Unet` 用 hierarchical Swin Transformer block 构建对称的 U-shape encoder-decoder，输入图像先被切成 `4×4` non-overlapping patches，再通过 patch merging 完成下采样，通过 patch expanding 完成上采样，并结合多尺度 skip connection 恢复空间细节，从而在不依赖 CNN 的情况下，同时学习 local-global 语义交互与像素级分割表示。

关键页码：

- `p.1-p.7`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`Unet-like pure Transformer encoder-decoder`
- Encoder：`Swin Transformer blocks + patch merging`
- Bottleneck：`Swin Transformer blocks`
- Decoder：`Swin Transformer blocks + patch expanding`
- Skip 连接：`encoder 多尺度特征与 decoder 对称融合`
- 输入 tokenization：`patch size = 4×4`

### 3.2 关键模块详细描述

**模块 1：`Hierarchical Swin Transformer Encoder`**

- 位置：`编码路径`
- 操作流程：
  1. 将输入切成 non-overlapping `4×4` patches
  2. 线性映射成 token embeddings
  3. 通过多层 Swin Transformer block 做特征学习
  4. 通过 patch merging 下采样并增加通道维
- 页码：`p.4-p.7`

**模块 2：`Patch Expanding Decoder`**

- 位置：`解码路径`
- 操作流程：
  1. 使用 patch expanding 代替传统插值或转置卷积
  2. 把相邻维度的 feature 重新排列为更高分辨率 feature map
  3. 每次实现 `2×` 上采样
  4. 最后一层执行 `4×` 上采样恢复输出分辨率
- 页码：`p.4-p.7`

**模块 3：`Skip Connections for Transformer`**

- 位置：`encoder-decoder 对应尺度之间`
- 操作流程：
  1. 将 encoder 多尺度 shallow features 与 decoder upsampled features 拼接
  2. 缓解 down-sampling 带来的空间细节损失
  3. 经线性层压回与 decoder 一致的通道维
- 页码：`p.7, p.10-p.11`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 组件 | 默认设置 | 作用 | 页码 |
|------|---------|------|------|
| 输入尺寸 | `224×224` | 主实验设置 | `p.8, p.11` |
| patch size | `4×4` | 图像 tokenization | `p.4, p.8` |
| encoder 基本单元 | `Swin Transformer block` | 层次化语义建模 | `p.4-p.6` |
| downsampling | `patch merging` | 降采样 + 增维 | `p.6` |
| decoder 基本单元 | `Swin Transformer block` | 逐步恢复特征 | `p.6-p.7` |
| upsampling | `patch expanding` | 上采样 + 重排特征 | `p.6-p.7` |
| skip 数量 | `3` | 默认最优设置 | `p.10-p.11` |

补充：

| 上采样方式消融 | DSC |
|---------------|-----|
| `Bilinear interpolation` | `76.15` |
| `Transposed convolution` | `77.63` |
| `Patch expand` | `79.13` |

| skip connection 数量 | DSC |
|---------------------|-----|
| `0` | `72.46` |
| `1` | `77.14` |
| `2` | `78.93` |
| `3` | `79.13` |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
ẑ_l = W-MSA(LN(z_{l-1})) + z_{l-1}
```

符号说明：

- `W-MSA`：window-based multi-head self-attention
- `LN`：LayerNorm
- `z_{l-1}`：上一层输入特征
- `ẑ_l`：当前注意力子层输出
- 页码：`p.6`

公式 2：

```text
z_l = MLP(LN(ẑ_l)) + ẑ_l
```

符号说明：

- `MLP`：两层前馈网络
- `z_l`：当前 Swin Transformer block 输出
- 含义：标准 attention + MLP 残差结构
- 页码：`p.6`

### 4.2 推导过程或梯度行为

- 论文重心仍然是结构设计，不是数学推导
- 关键机制在于：
  - encoder 通过 hierarchical Swin 实现从 local 到 global 的语义交互
  - decoder 通过 patch expanding 恢复分辨率
  - skip connection 将 shallow spatial cues 注回 decoder
- 这篇论文的实质性结论是：Transformer 也需要 U-shape 的多尺度恢复机制，而不是只靠 attention 自然解决 dense prediction

---

## 5. 损失函数

### 5.1 各监督项

- 当前主文提取里没有突出复杂 loss 设计
- 论文重点在结构设计与上采样 / skip 的作用
- `loss 具体形式 [待结合源码确认]`

### 5.2 总损失公式

- 主文提取文本中未见明确展开总损失公式
- 对复现最重要的不是 loss 创新，而是：
  - patch size
  - patch expanding
  - skip 数量
  - 预训练初始化

### 5.3 权重配置与调度策略

- 未见复杂多项 loss weighting 设计
- 论文把主要精力放在结构消融，而不是 loss engineering

---

## 6. 训练协议

### 6.1 数据集与划分

- `Synapse`：
  - `30` 个 case
  - 按已有协议：`18` 个训练，`12` 个测试
  - 指标：平均 `DSC` 与平均 `HD`
- `ACDC`：
  - MRI cardiac segmentation 数据
  - 用于验证跨模态泛化

### 6.2 数据增强

- 使用 `flips` 与 `rotations` 提升数据多样性
- 论文没有像 `nnU-Net` 一样详述完整增强策略

### 6.3 优化器与超参数

| 项目 | 数值/策略 | 页码 |
|------|-----------|------|
| input size | `224×224` | `p.8` |
| patch size | `4` | `p.8` |
| batch size | `24` | `p.8` |
| optimizer | `SGD` | `p.8` |
| momentum | `0.9` | `p.8` |
| weight decay | `1e-4` | `p.8` |
| 预训练 | `ImageNet pretrained weights` | `p.8` |
| GPU | `Nvidia V100 32GB` | `p.8` |

### 6.4 预处理与数据细节

- stain normalization / color normalization：`不适用；本文是 CT / MRI`
- 颜色空间转换：`不适用`
- resize / crop / pad 策略：
  - 默认输入 resize 到 `224×224`
  - 另做 `384×384` 输入消融
- patch overlap：`无；这里的 patch 是 Transformer tokenization，不是滑窗推理 patch`
- 背景过滤策略：`未见单独强调`
- 标签生成方式：`标准医学分割 mask`
- 类别不平衡处理：`主文未强调`
- 随机种子/重复次数：`未见说明`
- 数据泄漏风险点：
  - 沿用既有 split protocol，但对病理任务不能机械照搬 random split

---

## 7. 推理与后处理

- 论文重点不在后处理，而在结构本身
- 关键推理相关因素：
  - 输入分辨率
  - patch size
  - skip 数量
  - 上采样方式
- 从结果解读看，`patch expanding` 带来的边界质量提升是实际有效的

---

## 8. 消融实验

### 8.1 消融设计

- 上采样方式：
  - `bilinear interpolation`
  - `transposed convolution`
  - `patch expanding`
- skip 数量：
  - `0 / 1 / 2 / 3`
- 输入尺寸：
  - `224`
  - `384`
- 模型规模：
  - `tiny`
  - `base`

### 8.2 各模块贡献量化

- `Table 3`：
  - `Bilinear interpolation`：`DSC 76.15`
  - `Transposed convolution`：`DSC 77.63`
  - `Patch expand`：`DSC 79.13`
- `Table 4`：
  - `0 skip`：`72.46`
  - `1 skip`：`77.14`
  - `2 skip`：`78.93`
  - `3 skip`：`79.13`
- `Table 5`：
  - `224×224`：`79.13`
  - `384×384`：`81.12`
- 结论：
  - `patch expanding` 优于传统上采样方式
  - skip 越多性能越高
  - 更高分辨率输入能继续提升，但计算成本更大

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 方法 | 结果 | 页码 |
|-------|------|------|------|
| Synapse | `SwinUnet` | `DSC 79.13`, `HD 21.55` | `p.8-p.9` |
| Synapse | `TransUnet` | `DSC 77.48`, `HD 31.69` | `p.8-p.9` |
| ACDC | `SwinUnet` | `DSC 90.00` | `p.9-p.10` |
| ACDC | `TransUnet` | `DSC 89.71` | `p.9-p.10` |

### 9.2 与其他方法的对比

- Synapse 上：
  - `SwinUnet` 的 DSC 仅比 `TransUnet` 高约 `1.65`
  - 但 HD 从 `31.69` 明显改善到 `21.55`
- 论文据此强调：
  - pure Transformer U-shape 在边界质量和过分割抑制上更有优势
- 同时也优于：
  - `V-Net`
  - `DARR`
  - `U-Net`
  - `Att-UNet`
  - `R50 ViT`
  - `TransUnet`

### 9.3 公平对比条件确认

- 优势：
  - 与 `TransUnet`、`Att-UNet`、`U-Net` 等放在统一 benchmark 下比较
  - 不仅比 Dice，也比 HD
  - 对上采样方式与 skip 数量做了清晰消融
- 注意：
  - 默认输入是 `224×224`，不是最高可能性能设置
  - 作为 pure Transformer 方案，其显存和训练稳定性条件与 CNN 基线并不完全一致

### 9.4 评价协议与指标定义

- `Synapse`：
  - 平均 `DSC`
  - 平均 `HD`
- `ACDC`：
  - `DSC`
- 论文特别强调：HD 改善更能说明边界质量和过分割控制能力

---

## 10. 计算量与效率

- 更高输入分辨率 `384×384` 会继续提升精度，但也显著增加计算量
- patch size 固定为 `4` 时，输入增大意味着 token 序列更长，Transformer 代价更高
- 对我们项目的含义：
  - 如果未来真跑 `Swin-Unet`，输入分辨率设置会显著影响结论
  - 不能用低分辨率结果就断言 pure Transformer 不适合病理图像

---

## 13. 开源与复现

- 开源情况：`是`
- 官方代码：论文声明 `codes and trained models will be publicly available`
- 复现难度：`中到高`
- 难点：
  - Swin Transformer medical adaptation
  - patch expanding 实现
  - 预训练权重初始化
  - 显存开销与分辨率权衡

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| 随机种子 | `否` | `后续复现需显式固定` | `中` |
| 验证集划分 | `部分（沿用既有 split 协议）` | `病理任务必须改 patient-level` | `高` |
| 推理阈值 | `未强调` | `默认 segmentation argmax [待确认源码]` | `中` |
| 后处理细节 | `未强调` | `不作为本方法主贡献` | `低` |
| 训练停止准则 | `未详写` | `需结合代码/日志确认` | `中` |
| 数据预处理 | `部分（输入大小、patch size 明确）` | `病理 RGB 需单独映射` | `高` |
| 损失具体形式 | `未在主文突出` | `后续结合源码确认` | `中` |

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 更高输入分辨率虽然效果更好，但计算成本明显增加
- 纯 Transformer 路线对训练资源更敏感

### 14.2 我们观察到的潜在问题

- 论文验证的是器官/心脏医学分割，不是病理腺体实例级边界任务
- pure Transformer 缺少 CNN inductive bias，在病理纹理细粒度模式上未必稳定
- 虽然 HD 改善很好，但 Dice 提升并不大，说明其优势更偏边界和形状质量，而不是全面碾压

### 14.3 失败案例 / 定性分析

- 论文用可视化说明 CNN-based 方法更易 over-segmentation
- `Swin-Unet` 借助 pure Transformer + U-shape skip 改善了边界预测
- 对我们任务的映射：
  - 若后续关注腺体边界、腺体间粘连和过分割问题，这篇的 HD 改善现象很值得保留

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- `pure Transformer` 也需要 skip connection
- 上采样设计会直接影响边界质量
- 评价时不只看 Dice，还应关注 HD 或边界类指标

### 15.2 可以作为候选参数来源的

- `input size 224` 作为基础跑法
- `patch size 4`
- `ImageNet pretrained initialization`
- `SGD + momentum 0.9 + wd 1e-4 + bs 24`

### 15.3 不应照搬的（及原因）

- 直接把 `Swin-Unet` 原配置搬到病理腺体任务：
  - 成像模态不同
  - patch 语义粒度不同
  - 病理纹理与器官形状先验不同
- 直接用 random split 评价：
  - 会高估病理任务泛化能力

### 15.4 对我们具体模块的支撑

- 对 `Transformer 外部强对比`：
  - 它是比 `TransUNet` 更纯的 Transformer 代表
- 对 `边界质量分析`：
  - 它能支撑“边界与过分割质量不能只看 Dice”的论点
- 对 `结构设计`：
  - 说明 skip connection 对 Transformer 同样关键

### 15.5 后续行动项

- 后续可把 `Swin-Unet` 与 `TransUNet` 一起写进 related work 的 Transformer 小节
- 如果后面要做 Transformer 对比，优先先定：
  - 输入分辨率
  - patch 粒度
  - 是否沿用 patch expanding 风格 decoder
- 若资源有限，可先把它作为文献对比基线，不必立刻实跑

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | CNN 局部性与 Transformer 全局建模动机 | 用作 Transformer 医学分割路线背景 |
| related work | pure Transformer U-shape 代表方法 | 与 `TransUNet` 对照书写 |
| 方法 | patch expanding 与 Transformer skip 的设计依据 | 作为结构启发，不夸大为复现 |
| 实验设置 | 输入分辨率、patch size、预训练初始化 | 作为外部参数参考 |
| 讨论 | Dice 小升但 HD 大幅改善的现象 | 用来说明边界质量的重要性 |

---

## 16. 关键图表索引

| 图/表 | 内容 | 用途 |
|------|------|------|
| `Fig. 1` | Swin-Unet 总体架构图 | 理解 pure Transformer U-shape |
| `Fig. 2` | Swin Transformer block | 结构细节说明 |
| `Table 1` | Synapse 主结果 | 引用 `79.13 / 21.55` |
| `Table 2` | ACDC 结果 | 说明泛化能力 |
| `Table 3` | 上采样方式消融 | 证明 patch expanding 优势 |
| `Table 4` | skip 数量消融 | 证明 Transformer 也需要 skip |
| `Table 5` | 输入尺寸消融 | 说明分辨率影响 |

---

## 17. 提取质量自检

- [x] 所有数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [x] 训练参数足够复现（优化器+bs+输入尺寸+patch+预训练）
- [x] 预处理与数据细节已检查（输入尺寸 / patch / split）
- [x] 结果数字与原文 table 一致（已核对关键项）
- [x] 指标定义和评价协议已确认（DSC / HD）
- [x] 消融实验的结论已量化（不只是“有效”）
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标注 `[待确认]`
