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

- `foundation model for gland segmentation`
- `SAM adaptation`
- `grade prompt with Grad-CAM++`

### 0.3 对应 `pdf库` 文件夹与最小必填集

当前所属文件夹：`05_腺体任务经典论文`

- 本篇代表 `SAM / prompt-based` 路线进入 gland segmentation 的直接工作
- 本篇至少完成：`1-9, 13-16`

---

## 1. 论文信息

- 论文名：`Gland Segmentation Using SAM with Cancer Grade as a Prompt`
- 作者/团队：`Yijie Zhu, Shan E Ahmed Raza`
- 发表年份/会议/期刊：`2025, arXiv`
- DOI / arXiv ID：`arXiv:2501.14718`
- BibTeX key：`zhu2025samgradeprompt`
- PDF 路径：`结直肠腺体分割_pdf库/05_腺体任务经典论文/Gland_Segmentation_Using_SAM_with_Cancer_Grade_as_a_Prompt_2025.pdf`
- 当前定位：`05` 目录里一篇把 foundation model 直接引入腺体分割的论文，关键创新不是只 fine-tune `SAM`，而是把 `cancer grade` 通过 `ViT + Grad-CAM++` 转成 prompt
- 与已提取论文的关系：
  - 与 [10_SCAU-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/10_SCAU-Net.md) 的对照点在于：后者是 CNN attention 内部重标定，本篇则把外部分类语义作为 prompt 注入
  - 与 [09_AttentionBoost.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/09_AttentionBoost.md) 都属于“告诉模型该关注什么”的路线，但本篇的注意力来自 grade prompt，而不是 error-driven reweighting
  - 与 [12_DEA-Net.md](file:///D:/12_Medical_Image_Segmentation/%E5%9B%BE%E5%83%8F%E5%88%86%E7%B1%BB%E5%AD%A6%E4%B9%A0/%E7%BB%93%E7%9B%B4%E8%82%A0%E8%85%BA%E4%BD%93%E5%88%86%E5%89%B2_plan/03_%E6%96%87%E7%8C%AE%E8%AF%81%E6%8D%AE/05_%E8%85%BA%E4%BD%93%E4%BB%BB%E5%8A%A1%E7%BB%8F%E5%85%B8%E8%AE%BA%E6%96%87/12_DEA-Net.md) 形成“近期两条路线”的对照：DEA-Net 仍是任务内结构设计，本篇转向 foundation model adaptation

### 1.1 可直接引用卡片

#### 1.1.1 引言可引用句

- 句子/事实 1：cancer grade 与 gland morphology / gland formation 密切相关，因此如果模型预先知道 gland 更偏 benign 还是 malignant，就可能更好完成分割。
  - 用途：`任务背景 / 方法动机`
  - 页码：`p.1`
- 句子/事实 2：SAM 在医学图像上零样本性能会下降，但其强泛化和 prompt 机制为 gland segmentation adaptation 提供了可行基础。
  - 用途：`foundation model 引入动机`
  - 页码：`p.1`

#### 1.1.2 related work 可引用句

- 句子/事实 1：作者提出用 `Grad-CAM++` 从 ViT 分类分支生成 heat map，并把它作为 `grade prompt` 输入到分割分支。
  - 用途：`方法脉络 / 与我们路线关系`
  - 页码：`p.1-p.2`
- 句子/事实 2：分割分支基于 SAM，同时预测 `gland` 与 `contour`，再通过去除两者重叠区域来分离相邻腺体。
  - 用途：`结构创新点`
  - 页码：`p.2-p.3`

#### 1.1.3 实验设置可引用数字

| 可引用数字/设置 | 数值 | 用于哪里 | 页码 |
|----------------|------|---------|------|
| GlaS 划分 | `85 train / 60 test A / 20 test B` | 数据集说明 | `p.3` |
| 输入尺寸 | `400x400` | 训练设置 | `p.3` |
| 分类模型 | `deit-base-patch16-224` | 分类分支 | `p.3` |
| 分类准确率 | `97.1% / 98.7%` | test A / B | `p.2-p.3` |
| SAM 规模 | `SAM-B / SAM-L / SAM-H` | 主对比 | `p.3-p.4` |
| Prompted SAM-H | `F1 0.929 / 0.841` | 主结果 | `Table 1-2, p.4` |
| Prompted SAM-H | `Object Dice 0.921 / 0.881` | 主结果 | `Table 1-2, p.4` |
| Prompted SAM-H | `Object Hausdorff 41.189 / 74.300` | 主结果 | `Table 1-2, p.4` |
| 阈值 | `0.5` | 后处理 | `p.2-p.3` |

---

## 2. 问题定义与动机

### 2.1 论文自己定义的问题

- gland morphology 在 benign 与 malignant 情况下差异明显，这种差异既带来分割难度，也蕴含可利用的先验。
- SAM 在自然图像上的强能力迁移到医学图像时会退化，直接 zero-shot 不够。
- 相邻 glands 容易被连接，因此 contour prediction 仍然重要。
- 作者希望把“病理分级语义”反过来用于分割，而不是只把分割用于 grading。

对应原文依据（页码）：

- `p.1-p.2`

### 2.2 核心思路（一段话概括解法方向）

- 论文提出一个双分支框架：分类分支用预训练 `ViT` 判断 gland 更偏 benign 还是 malignant，并通过 `Grad-CAM++` 生成 heat map；该 heat map 经 `prompt adapter` 处理后，作为 `grade prompt` 输入到基于 `SAM` 的分割分支。分割分支共享一个 image encoder，同时分出 `gland prediction branch` 与 `contour prediction branch`，其中 gland branch 使用 heat-map prompt，contour branch 不使用 prompt；最终通过去除 gland 与 contour 的重叠区域、median filter 和阈值化来提升相邻腺体分离效果。

关键页码：

- `p.1-p.4`

---

## 3. 模型/方法结构

### 3.1 总体架构

- 骨架类型：`classification branch + prompted SAM segmentation branch`
- 分类分支：`ViT`
- prompt 生成：`Grad-CAM++ heat map`
- prompt 适配：`prompt adapter`
- 分割主干：`SAM`
- 分割输出：
  - `gland mask`
  - `contour mask`

### 3.2 关键模块详细描述

**模块 1：`Classification Branch`**

- 位置：`前置病理语义分支`
- 操作流程：
  1. 使用预训练 `ViT`
  2. 微调 benign / malignant 二分类
  3. 输出分类结果
  4. 为后续 prompt 生成提供依据
- 页码：`p.2-p.3`

**模块 2：`Grade Prompt via Grad-CAM++`**

- 位置：`分类分支到分割分支之间`
- 操作流程：
  1. 对 ViT 分类结果做 `Grad-CAM++`
  2. 生成与原图同尺寸的一通道 heat map
  3. 该 heat map 反映 classification branch 认为重要的区域
  4. 将其作为 grade prompt 输入分割分支
- 设计理由：热图包含 benign / malignant 相关模式，可让分割模型“提前知道” gland 更可能长什么样
- 页码：`p.2`

**模块 3：`Prompt Adapter`**

- 位置：`prompt 预处理层`
- 操作流程：
  1. 将热图与原始图像拼接
  2. 得到四通道特征
  3. 通过两层卷积把四通道降到一通道
  4. 每层卷积后接 `BatchNorm + ReLU`
  5. 将处理后的输出与原热图相加，送入 segmentation branch
- 页码：`p.2`

**模块 4：`SAM-based Segmentation Branch`**

- 位置：`主分割分支`
- 操作流程：
  1. 共享一个 image encoder
  2. 分成 gland prediction branch 与 contour prediction branch
  3. 两个分支各自有 prompt encoder 和 mask decoder
  4. gland branch 接 grade prompt
  5. contour branch 不输入 prompt
  6. 同时预测 gland 与 contour
- 页码：`p.2`

**模块 5：`Overlap Removal Postprocessing`**

- 位置：`推理与后处理`
- 操作流程：
  1. 对 patch overlap 区域取平均
  2. 经过 sigmoid 输出概率
  3. 用 `0.5` 阈值得到二值 mask
  4. 找出 gland 与 contour 的重叠区域并消除
  5. 用 median filter 平滑边界
  6. 去除背景小噪点和前景小孔洞
- 页码：`p.2-p.3`

### 3.3 架构参数表（适用于基线对比论文 G 类型）

| 层/阶段 | 类型 | 通道数 | 空间尺寸 | 备注 |
|---------|------|--------|---------|------|
| 分类分支 | `ViT (deit-base-patch16-224)` | `未展开` | `224` 分类输入 | benign / malignant |
| 热图生成 | `Grad-CAM++` | `1` | 与原图同尺寸 | 生成 grade prompt |
| Prompt Adapter | `concat + conv + conv` | `4 -> 1` | 与输入对齐 | `BN + ReLU` |
| SAM image encoder | shared encoder | `SAM-B/L/H` | `400x400` patch | 共享特征抽取 |
| Gland branch | `prompt encoder + mask decoder` | `1 mask` | 同输入 | 使用 grade prompt |
| Contour branch | `prompt encoder + mask decoder` | `1 mask` | 同输入 | 不输入 prompt |

---

## 4. 公式与推导

### 4.1 核心公式

公式 1：

```text
Weighted MSE = sum( W ⊙ (Y_hat - Y)^2 )
```

符号说明：
- `W`：来自 gland annotation 的 weight map
- `Y_hat`：预测结果
- `Y`：ground truth
- `⊙`：逐元素乘法
- 含义：把 U-Net 风格的 weight map 乘到每个像素的 MSE 上，以更强调关键区域
- 页码：`p.2-p.3`

公式 2：

```text
Prompt = HeatMap + Adapter( concat(Image, HeatMap) )
```

符号说明：
- `HeatMap`：由 `Grad-CAM++` 生成
- `Adapter(.)`：两层卷积的 prompt adapter
- 含义：对原始热图做可学习适配，再作为 gland branch 的 prompt
- 页码：`p.2`

### 4.2 推导过程或梯度行为（适用于 B 类损失论文）

- 论文不以新损失理论推导为重点，核心创新是 prompt 设计和 SAM 结构改造。
- 训练上采用分步式 transfer learning，先分离地把分类与 gland branch 训稳，再冻结 image encoder 去训练 contour branch。

---

## 5. 损失函数

### 5.1 各监督项

- `MSE loss`
- `weighted MSE loss`
- 监督对象：
  - gland branch
  - contour branch

### 5.2 总损失公式

```text
论文明确说明：
1) fine-tuning SAM 时使用 MSE loss
2) 对 gland annotation 引入 U-Net 风格 weight map
3) 最终对每个像素的 MSE 做加权并求和，得到 weighted MSE loss
```

说明：

- 当前正文没有给出更完整的闭式总损失写法
- 但监督核心已经明确：`weighted MSE` 而不是 `Dice / CE`

### 5.3 权重配置与调度策略

- 未报告显式 loss weights
- 训练策略采用逐阶段：
  1. 先微调分类分支
  2. 加载 fine-tuned SAM 初始化 gland branch
  3. 先训练共享 image encoder + gland branch 的 prompt encoder / adapter / decoder
  4. 冻结 image encoder
  5. 最后训练 contour branch 的 prompt encoder / decoder

---

## 6. 训练协议

### 6.1 数据集与划分

- 数据集：`GlaS`
- 划分：
  - `85` train
  - `60` test A
  - `20` test B
- 输入 patch：
  - `400 x 400`
- 原图均大于该尺寸，因此可从四角提取四张部分重叠 patch
- contour annotation 通过 `dilated gland annotation - eroded gland annotation` 构造

### 6.2 数据增强

- 从每张原图四个角提取部分重叠 patch
- 按 `90 degrees` 的不同倍数旋转
- 目的：提升数据多样性和训练鲁棒性

### 6.3 优化器与超参数

| 项目 | 设置 |
|------|------|
| 分类模型 | `deit-base-patch16-224` |
| 分割主干 | `SAM-B / SAM-L / SAM-H` |
| 输入尺寸 | `400x400` |
| 分类准确率 | `97.1% (Test A) / 98.7% (Test B)` |
| 分支训练策略 | `stepwise` |

### 6.4 预处理与数据细节

- prompt 是一通道 heat map
- prompt adapter 先把原图与热图拼接成四通道再降到一通道
- gland / contour 两个分支共享同一个 image encoder
- contour branch 不接 prompt，这个设计是为了将 prompt 的影响主要集中在 gland coverage 上

---

## 7. 推理与后处理

- 对 patch overlap 区域取平均
- 经过 sigmoid 得到概率图
- `threshold = 0.5`
- 去除 gland 与 contour 的 overlap 区域
- median filter 平滑边界
- 去除小背景噪点与前景小孔洞

---

## 8. 消融实验

### 8.1 消融设计

- 以不同规模的 fine-tuned SAM 为 baseline：
  - `SAM-B`
  - `SAM-L`
  - `SAM-H`
- 对每个规模再加入 `grade prompt` 形成：
  - `Prompted SAM-B`
  - `Prompted SAM-L`
  - `Prompted SAM-H`
- 指标：
  - `F1 Score`
  - `Object Dice`
  - `Object Hausdorff`
- 数据集：
  - `GlaS Test A`
  - `GlaS Test B`

### 8.2 各模块贡献量化

| 方法 | F1 A | F1 B | ObjDice A | ObjDice B | Haus A | Haus B |
|------|------|------|-----------|-----------|--------|--------|
| `SAM-B` | `0.880` | `0.764` | `0.884` | `0.813` | `61.384` | `121.047` |
| `Prompted SAM-B` | `0.882` | `0.777` | `0.890` | `0.827` | `58.464` | `114.469` |
| `SAM-L` | `0.925` | `0.810` | `0.914` | `0.846` | `43.380` | `103.227` |
| `Prompted SAM-L` | `0.927` | `0.813` | `0.919` | `0.846` | `37.052` | `98.605` |
| `SAM-H` | `0.932` | `0.820` | `0.917` | `0.879` | `42.441` | `77.158` |
| `Prompted SAM-H` | `0.929` | `0.841` | `0.921` | `0.881` | `41.189` | `74.300` |

- 结论：
  - 对三个 SAM 尺度，加入 grade prompt 后整体都有改进
  - `Test B` 上的增益更明显，尤其 `Prompted SAM-H` 的 `F1 B` 从 `0.820` 提升到 `0.841`
  - `Prompted SAM-H` 虽然在 `Test A F1` 上略低于原 `SAM-H`，但整体 object Dice 和 Hausdorff 更优，且在 `Test B` 上明显更强

---

## 9. 主表结果与对比

### 9.1 论文报告的主要结果

| 数据集 | 指标 1 | 指标 2 | 指标 3 | 备注 |
|--------|--------|--------|--------|------|
| `GlaS Test A` | `F1 = 0.929` | `Object Dice = 0.921` | `Object Hausdorff = 41.189` | `Prompted SAM-H` |
| `GlaS Test B` | `F1 = 0.841` | `Object Dice = 0.881` | `Object Hausdorff = 74.300` | `Prompted SAM-H` |

### 9.2 与其他方法的对比

| 方法 | F1 A | F1 B | ObjDice A | ObjDice B | Haus A | Haus B |
|------|------|------|-----------|-----------|--------|--------|
| `Prompted SAM-H` | `0.929` | `0.841` | `0.921` | `0.881` | `41.189` | `74.300` |
| `CUMedVision2` | `0.912` | `0.716` | `0.897` | `0.781` | `45.418` | `160.347` |
| `ExB1` | `0.891` | `0.703` | `0.882` | `0.786` | `57.413` | `145.575` |
| `ExB3` | `0.896` | `0.719` | `0.886` | `0.765` | `57.350` | `159.873` |
| `Freiburg2` | `0.870` | `0.695` | `0.876` | `0.786` | `57.093` | `148.463` |
| `CUMedVision1` | `0.868` | `0.769` | `0.867` | `0.800` | `74.596` | `153.646` |
| `ExB2` | `0.892` | `0.686` | `0.884` | `0.754` | `54.785` | `187.442` |
| `Freiburg1` | `0.834` | `0.605` | `0.875` | `0.783` | `57.194` | `146.607` |

- 任务内解读：
  - 相比 challenge benchmark，`Prompted SAM-H` 在 A/B 两个子集上都取得很强结果
  - 但当前主表对比的更多是 challenge 时代方法，而不是所有最新 gland-specific 方法
  - 因此这篇更适合作为“foundation model 路线可行且有竞争力”的证据，而不是现代全量 SOTA 清单

### 9.3 公平对比条件确认

- 与 `SAM-B/L/H` 的比较较公平，因为都在同一工作中按同一训练策略评估
- 与 `GlaS` benchmark 的经典方法比较具有历史可读性
- 但它没有和 `DEA-Net / TA-Net` 这类近期强基线在同表直接横向比较
- 因此在写 related work 时最好把它定位为“prompted foundation model evidence”，而非唯一最强现代方法

### 9.4 评价协议与指标定义

- 使用 `GlaS Challenge` 的三项指标：
  - `F1 Score`
  - `Object-level Dice`
  - `Object-level Hausdorff`
- 这些指标分别评估：
  - 单个 gland detection 的准确性
  - individual glands 的重叠质量
  - 形状边界相似性
- 页码：`p.3-p.4`

---

## 10. 计算量与效率

- 参数量：`未报告`
- FLOPs：`未报告`
- 推理时间：`未报告`
- 间接效率信息：
  - 同时试验了 `SAM-B / SAM-L / SAM-H`
  - 较大模型整体性能更好
  - `Prompted SAM-H` 是最佳配置，但也很可能是成本最高配置

---

## 11. 分类体系与研究空白（综述论文 C 类型专用）

### 11.1 论文提出的分类框架

- 本篇不是综述论文，没有提出正式分类框架。

### 11.2 论文指出的研究空白 / Open Problems

- SAM 在医学图像上需要 adaptation，零样本不够。
- 如何把更高层病理语义稳定地转成对分割有帮助的 prompt，仍是开放问题。
- 论文结尾还指出后续可尝试不同损失函数，以及 generative model 路线。

### 11.3 对我们选题的启示

- 如果你的上游信息不仅有图像，还有分级/分类语义，那么这些信息完全可以不只做多任务，而可以直接变成 prompt 去调控分割。

---

## 12. 临床/病理标准（病理临床 D 类型专用）

### 12.1 涉及的病理分级标准

- 论文围绕 benign / malignant 二分类展开，但没有给出病理分级体系细表。

### 12.2 涉及的生物标志物

- 无直接 biomarker 报告。

### 12.3 临床意义

- gland segmentation 被明确连接到 automated and objective grading of cancer
- 作者强调 gland morphology 与 gland formation 是 pathologists 评估 tumor differentiation 的关键因素

---

## 13. 开源与复现

- 代码是否开源：`正文未提供代码地址`
- 代码仓库地址：`未提供`
- 框架/语言：`未在正文显式写明，按模型生态推测为 Python 深度学习实现，但不写死`
- 预训练权重是否提供：`使用公开预训练 ViT 与 SAM`
- 复现难度评估：`中到高`
- 复现障碍：
  - 分类分支、prompt adapter、双分支 SAM 的训练顺序较复杂
  - weighted MSE 的完整实现细节未完全展开
  - 没有报告完整优化器、epoch、lr 等训练超参

### 13.1 论文未报告但复现必需的信息

| 缺失项 | 论文是否明确写出 | 我们当前处理方式 | 风险等级 |
|-------|------------------|----------------|---------|
| optimizer / lr / epochs | 否 | 仅记录 stepwise training，不脑补数值 | 高 |
| weighted MSE 精确公式 | 部分 | 记录其机制，不扩展为未报告细节 | 中 |
| prompt adapter 通道数与卷积核 | 部分 | 仅记录“两层卷积，4->1” | 中 |
| contour branch 初始化细节 | 部分 | 记录来源于 SAM 参数 | 中 |
| 随机种子 | 否 | 不假设固定 seed | 中 |
| patch overlap 具体比例 | 否 | 只记录存在 overlap averaging | 中 |

- 不确定但影响较大的点：
  - fine-tuned SAM 的具体预训练/微调来源
  - 分类分支和分割分支各阶段训练轮数
  - weight map 的具体生成公式

---

## 14. 局限性与失败案例

### 14.1 论文自述的局限性

- 后续计划尝试不同损失函数，如 `Cross Entropy`, `Dice`, `AC Loss`
- 作者还指出 generative model 路线值得进一步探索
- 目前只在 `GlaS` 上验证

### 14.2 我们观察到的潜在问题

- 虽然对 benchmark 很强，但没有和近期 `DEA-Net / TA-Net` 这类方法直接同表比较
- 分类 prompt 的收益在不同测试子集上不完全一致，例如 `Test A` 上 `Prompted SAM-H` 的 F1 略低于 `SAM-H`
- 结构复杂度较高：分类分支、prompt adapter、双 decoder / dual branch、分步训练全部叠加

### 14.3 失败案例 / 定性分析

- 论文是否展示失败案例：`主要展示正例可视化`
- 定性结论：
  - benign 与 malignant 样本上都表现稳定
  - 相邻 glands 很近时仍可被分开
  - contour prediction 对防止 gland 黏连仍然关键
- 页码：`Fig.3-Fig.4, p.2-p.4`

---

## 15. 对我们项目的落地价值

### 15.1 可以直接借用的

- 把上游病理语义转成 segmentation prompt 的思路
- `ViT -> Grad-CAM++ -> prompt adapter -> segmentation` 这一信息桥接范式
- 同时预测 `gland + contour` 再做 overlap removal 的分离策略
- `GlaS` challenge 三指标作为 prompt 路线评价口径

### 15.2 可以作为候选参数来源的

- `400x400` 输入
- `0.5` threshold
- `deit-base-patch16-224`
- `SAM-B / L / H` 多规模比较框架

### 15.3 不应照搬的（及原因）

- 不应直接照搬其整套 foundation model 双分支重结构
  - 原因：训练链路长，复现成本高
- 不应只拿它与 challenge benchmark 的比较就下“全面 SOTA”结论
  - 原因：缺少与若干近期强基线的同表对照
- 不应默认 grade prompt 一定总是提高所有指标
  - 原因：至少在 `SAM-H / Test A / F1` 上并非单调提升

### 15.4 对我们具体模块的支撑

| 我们的模块/决策 | 本论文提供的支撑 | 支撑强度 |
|---------------|----------------|---------|
| 上游语义融入分割 | grade information 可作为 prompt | 强 |
| contour 辅助分离 | gland + contour 双预测仍然有效 | 强 |
| foundation model 路线可行性 | fine-tuned + prompted SAM 在 GlaS 上很强 | 强 |
| prompt 设计 | 热图型 prompt 比直接分类标签更细粒度 | 中 |
| patch 推理后处理 | overlap averaging + threshold + overlap removal | 中 |

### 15.5 后续行动项

- [ ] 需要回填到哪个执行文档：`foundation model / prompt 路线备选表`
- [ ] 需要和哪篇论文交叉验证：`09_AttentionBoost.md`, `12_DEA-Net.md`, `03_DCAN.md`
- [ ] 待确认的问题：`我们是否要尝试把病理先验变成 prompt，而不是简单作为附加通道或多任务标签`

### 15.6 可回填到写作各部分的位置

| 可回填位置 | 本论文可提供什么 | 建议使用方式 |
|-----------|----------------|-------------|
| 引言 | gland morphology 与 grading 的关系 | 临床动机 |
| related work | SAM adaptation 与 prompt-based segmentation | 方法脉络 |
| 方法 | grade prompt / prompt adapter | 模块灵感 |
| 实验 | fine-tuned SAM 多规模对照 | foundation baseline |
| 讨论 | prompt 不是所有子集都单调增益 | 边界条件 |

---

## 16. 关键图表索引

| 图表编号 | 页码 | 内容描述 | 用途 |
|---------|------|---------|------|
| `Fig. 1` | `p.2` | 分类分支、prompt adapter、分割分支整体框架 | 总体结构 |
| `Fig. 2` | `p.2` | Grad-CAM++ heat maps | grade prompt 依据 |
| `Fig. 3` | `p.2-p.3` | gland / contour overlap removal 过程 | 后处理解释 |
| `Table 1` | `p.4` | fine-tuned SAM 与 prompted SAM 各尺度对比 | 消融主表 |
| `Fig. 4` | `p.4` | Prompted SAM-H 可视化结果 | 定性结果 |
| `Table 2` | `p.4` | 与 GlaS benchmark 的对比 | 历史横向对照 |

---

## 17. 提取质量自检

- [x] 所有已确认的关键数字都标注了来源页码
- [x] 可直接引用卡片已经填写，不需要二次回翻 PDF 才能写作
- [x] 公式符号都有解释
- [ ] 训练参数足够完全复现（优化器、轮数等仍缺）
- [x] 预处理与数据细节已检查
- [x] 结果数字与原文 table 一致
- [x] 指标定义和评价协议已确认
- [x] 消融实验的结论已量化
- [x] 与我们项目的关联已具体到模块级别
- [x] 论文未报告但复现必需的信息已单独列出
- [x] 不确定的内容已标明而未脑补
