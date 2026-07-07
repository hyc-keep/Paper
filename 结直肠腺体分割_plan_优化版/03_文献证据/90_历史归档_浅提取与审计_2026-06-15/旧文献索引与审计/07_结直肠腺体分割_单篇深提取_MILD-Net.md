# `MILD-Net` 单篇深提取

## 1. 论文信息

- 论文名：`MILD-Net: Minimal Information Loss Dilated Network for Gland Instance Segmentation in Colon Histology Images`
- PDF：`结直肠腺体分割_pdf库/05_腺体任务经典论文/MILD-Net_Minimal_Information_Loss_Dilated_Network_2018.pdf`
- 当前定位：`GlaS / CRAG` 双数据集、腺体任务内强基线、形态建模与边界分支的重要参考论文

---

## 2. 这篇论文到底在解决什么问题

### 2.1 论文自己定义的问题

论文明确把问题指向下面几类难点：

- 腺体分割需要足够深的网络做有效特征提取，但常规 `max-pooling` 会丢失对像素级预测很重要的细节信息
- 腺体大小和形态变化很大，尤其是恶性腺体更不规则
- 小腺体、细轮廓、黏连腺体都容易被压缩后的特征破坏

对应原文依据：

- `MILD-Net` 任务难点与腺体形态异质性：p.3
- `max-pooling` 带来细节信息损失：p.4-p.5

### 2.2 这篇论文的核心思路

它不是单纯再堆一个更深 backbone，而是围绕“减少下采样导致的信息丢失”设计整套结构：

1. 用 `MIL unit` 在 pooling 后把原图信息重新引入特征提取流程
2. 在特征被下采样到 `1/8` 后引入 `dilated residual unit`
3. 用 `ASPP` 处理不同癌变等级带来的形态尺度差异
4. 用 `U-Net` 风格逐级上采样和低层特征拼接恢复边界
5. 最终分成 `gland branch` 和 `contour branch`

关键页码：

- 总体结构与任务特异模块：p.4-p.6

---

## 3. 模型是怎么搭的

### 3.1 主体骨架

论文使用的是一个全卷积网络，主干由三类残差单元组成：

- 标准 residual unit
- `MIL unit`
- `dilated residual unit`

原文说明：

- 传统残差单元公式：`y = F(x, W) + x`，见 p.4-p.5
- `MIL unit` 在 pooling 后把下采样原图特征重新送入残差求和路径，见 p.5

### 3.2 `MIL unit` 的具体改进位置

这是这篇论文最值得真正提取的地方，不是简单一句“减少信息丢失”就够了。

原文给出的实现过程是：

1. 原始图像先下采样到和 pooling 输出同尺寸
2. 对下采样原图做一个 `3×3` 卷积
3. 与 pooling 输出做拼接
4. 再过一个 `3×3` 卷积
5. 最终把这个结果用于残差求和

论文明确写到：

- 三个 `MIL units` 被加在特征提取阶段、每次 `max-pooling` 之后，见 p.4

### 3.3 `MIL unit` 的公式

论文把普通残差单元

```text
y = F(x, W) + x
```

改成了：

```text
y = F(x, W) + G(x, v, M)
```

其中：

- `x` 是当前特征
- `v` 是下采样后的原始图像
- `G` 表示把原图信息卷积后与当前特征拼接再卷积的函数

原文页码：

- 普通残差公式：p.4-p.5
- `MIL unit` 公式与符号定义：p.5

### 3.4 dilated residual unit 怎么放

论文没有在全网络到处用空洞卷积，而是：

- 先通过 pooling + `MIL unit` 做下采样
- 当图像已经被下采样到 `1/8` 时，再把每个 `3×3` 卷积换成 `3×3 dilated convolution`

作者还明确解释了为什么不全程用 dilation：

- 否则 GPU 显存放不下
- 在原图尺度直接卷积代价太高

页码：

- p.5

### 3.5 `ASPP` 怎么设

论文在深层输出后使用 `ASPP` 做多尺度聚合，目标是对抗不同癌变等级引起的形态异质性。

具体配置：

- 三个 dilation rate：`6 / 12 / 18`
- 额外加入 `global average pooling`
- 各分支后接 `1×1 conv`
- 使用 `dropout = 0.5`
- 再用一个 `1×1 conv` 压缩通道

页码：

- p.5

### 3.6 decoder 和输出头怎么做

这篇论文不是只在编码端改。

decoder 侧做法：

- 像 `U-Net` 一样逐级 `×2` 上采样
- 与低层特征拼接
- 拼接前先对低层特征做 `1×1 conv`
- 最终分成两个输出分支：
  - `gland object`
  - `contour`

论文还额外加入：

- deep supervision：在第二个 dilated residual unit 处计算 auxiliary loss
- final `1×1 conv` 前加 `dropout = 0.5`

页码：

- 低层特征拼接与双分支：p.5
- auxiliary loss 与 dropout：p.6

---

## 4. 损失函数怎么定义

### 4.1 监督项

论文训练时对四个输出都算交叉熵：

- `Lg`：gland 主输出
- `Lc`：contour 主输出
- `Lag`：gland auxiliary 输出
- `Lac`：contour auxiliary 输出

页码：

- p.6

### 4.2 总损失公式

原文总损失写成：

```text
Ltotal = Lg + Lc + λLag + λLac + γ||w||^2_2
```

这里真正重要的是参数怎么设：

- 初始 `lambda = 1`
- 每 `8` 个 epoch 把 `lambda` 除以 `10`
- `gamma = 1e-5`

页码：

- 总损失公式：p.6
- `lambda` 衰减策略：p.6
- `gamma`：p.6

### 4.3 这对我们有什么启发

这篇论文最值得借的不是“照搬交叉熵”，而是：

- 主任务和边界任务分开监督
- auxiliary supervision 逐步衰减，而不是一直同权

这说明后面我们做 `Boundary Head` 时，不应只写“加个边界分支”，而应明确：

- 监督在哪一层接
- 主输出和辅助输出怎么配权
- 权重是否固定还是衰减

---

## 5. 训练协议与数据处理

### 5.1 数据集协议

论文明确用了两个数据集：

- `GlaS`: `85 train / 80 test`
- `CRAG`: `173 train / 40 test`

并且：

- 对两个数据集都从训练集中留出 `20%` 用于训练过程中的评估

页码：

- p.9

### 5.2 patch 和增强

这部分是之前提取不够的关键内容，原文写得很具体：

- 先提取 `500×500` patch
- 增强包括：
  - `elastic distortion`
  - `random flip`
  - `random rotation`
  - `Gaussian blur`
  - `median blur`
  - `colour distortion`
- 最后随机裁成 `464×464`

页码：

- p.9

### 5.3 实现与训练参数

论文给出的实现细节：

- 框架：`TensorFlow 1.3.0`
- 初始化：`Xavier initialisation`
- 设备：`1 × NVIDIA Titan X GPU`
- `GlaS`: `30 epochs (60,000 steps)`
- `CRAG`: `75 epochs (200,000 steps)`
- 优化器：`Adam`
- 初始学习率：`1e-4`
- `batch size = 2`

页码：

- p.9

### 5.4 推理与后处理

论文不是直接概率图阈值化完就结束，它还做了后处理：

- 对所有预测概率图统一用 `threshold = 0.5`
- 再做一次 morphology opening
- disk filter 半径为 `5`
- 这个半径是作者通过视觉和定量结果经验选出来的

页码：

- p.10

### 5.5 RTS 不确定性 refinement

论文还有一个很重要但容易被忽略的点：

- 通过随机变换采样 `RTS` 做 test-time refinement
- 论文证明 RTS 能提升 `GlaS B` 和 `CRAG` 的结果

这提示我们：

- `MILD-Net` 的最终最好结果，不只是主干结构贡献
- 还包含 test-time uncertainty refinement 的贡献

页码：

- RTS 介绍：p.6-p.8
- RTS 结果：p.12

---

## 6. 结果到底怎么样

### 6.1 `GlaS` 主表结果

Table 1 显示：

- `MILD-Net`
  - `Test A`: `F1 0.914 / ObjDice 0.913 / ObjHaus 41.54`
  - `Test B`: `F1 0.844 / ObjDice 0.836 / ObjHaus 105.89`
  - 综合 rank 最优

页码：

- p.12

### 6.2 `CRAG` 结果

Table 2 显示：

- `MILD-Net`
  - `F1 0.825`
  - `ObjDice 0.875`
  - `ObjHaus 160.14`

对比：

- `DCAN`: `0.736 / 0.794 / 218.76`
- `U-Net`: `0.600 / 0.654 / 354.09`

页码：

- p.12

### 6.3 RTS 带来的增益

Table 3 显示：

- `GlaS B`
  - `F1`: `0.809 -> 0.844`
  - `ObjDice`: `0.822 -> 0.836`
  - `ObjHaus`: `117.91 -> 105.89`
- `CRAG`
  - `F1`: `0.806 -> 0.825`
  - `ObjDice`: `0.867 -> 0.875`
  - `ObjHaus`: `162.35 -> 160.14`

页码：

- p.12

### 6.4 论文结论

论文声称：

- 在 `GlaS` 上达到当时 SOTA
- 在 `CRAG` 上也优于比较方法
- 说明减少信息损失、保留空间细节、结合 contour 与 uncertainty refinement 对腺体任务有效

页码：

- 结论总结：p.12, p.17

---

## 7. 这篇论文里哪些内容可以直接融入我们的实验

### 7.1 可以直接借用的

- `GlaS + CRAG` 双数据集证据链
- `F1 / Object Dice / Object Hausdorff` 主评价协议
- 训练集内部再留 `20%` 评估集的思路
- 形态异质性、大感受野、边界分支这三条动机链
- `gland branch + contour branch` 的多任务监督逻辑
- 小腺体、细轮廓、黏连腺体是重点 error type 的分析框架

### 7.2 可以作为候选范围借用的

- patch 流程：`500 -> 464`
- 增强包：弹性形变、翻转、旋转、模糊、颜色扰动
- `Adam + 1e-4 + batch size 2`
- threshold `0.5` + morphology opening `r=5`

这些不能直接写成“我们就必须一模一样”，但可以作为：

- 参数候选来源
- 协议设计参考
- 后处理上限参考

### 7.3 不应直接照搬的

- `TensorFlow 1.3.0`
- `MILD-Net` 的完整主干与我们当前 `ResNet34-U-Net + LKMA + Boundary Head` 主线
- RTS refinement
- morphology opening 半径 `5`

原因：

- 这些会直接改变公平比较协议
- 如果全部照搬，会把我们的主线和外部对比搞乱

---

## 8. 对我们当前项目最具体的落地价值

### 8.1 对数据协议

它证明我们现在把：

- `GlaS` 作为主 benchmark
- `CRAG` 作为第二 benchmark
- 官方 test 保留为最终评估

是合理的。

### 8.2 对模型路线

它证明腺体任务中的有效改进通常围绕：

- 减少信息丢失
- 增强感受野
- 引入边界/轮廓监督

所以我们当前的：

- `LKMA`
- `Boundary Head`

不是盲目拼装，而是和任务内强论文的动机一致。

### 8.3 对参数和实验步骤

它给了我们真正可引用的参数与步骤来源：

- `20%` 评估集
- `500×500 -> 464×464`
- `Adam(1e-4)`
- `batch size 2`
- `threshold 0.5`
- morphology opening `r=5`

以后如果我们不采用这些值，就必须明确写：

- 为什么不采用
- 是工程统一性原因，还是公平比较原因

### 8.4 对结果解释

它提醒我们：

- 最终效果不只看 backbone
- contour branch、后处理、test-time refinement 都会影响对象级结果

所以以后写我们自己的论文时，必须把：

- 结构贡献
- loss 贡献
- 后处理贡献
- TTA/RTS 贡献

严格拆开。

---

## 9. 用这篇论文反过来看目前 `03_文献证据` 的缺口

如果只写成“`MILD-Net` 支持 `GlaS + CRAG`、支持对象级指标、支持感受野和边界建模”，这还是不够的。

至少还缺：

1. 具体结构改在哪里
2. 公式是什么
3. loss 怎么配
4. patch 怎么取
5. 增强怎么做
6. 优化器、学习率、batch size、epoch 是什么
7. 后处理做了什么
8. 哪些结果来自主干，哪些结果来自 test-time refinement

也就是说，你说得对：

> 之前那种提取方式，更适合“写 related work 的摘要”，不适合“直接拿来融合实验 protocol”。

---

## 10. 这篇论文后续应该怎么继续吸收到执行层

基于这篇论文，后续最值得回填到 `01_实验执行` 的内容是：

- 在 `02_数据准备与检查手册` 中明确：
  - `训练集中留评估集` 的任务内出处来自 `MILD-Net`, p.9
- 在 `03_UNet首轮实验手册` 中明确：
  - 当前轻量增强包是对 `MILD-Net` 增强包的收缩版，而不是凭感觉设的
- 在 `04_主线实验矩阵` 中明确：
  - `Boundary Head` 的任务内强动机，不只是 `DCAN`
  - 大感受野和形态异质性的任务内支持，不只是通用大核论文
- 在后续参数来源表中明确：
  - 哪些参数来自 `MILD-Net` 的直接值
  - 哪些只是被它支持的候选范围

