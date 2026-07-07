# 结直肠腺体分割 UNet 首轮实验手册

这份文档只服务一个阶段：

> 用 `UNet` 把第一轮真正可用的训练、验证、测试、可视化闭环跑通。

这里不讨论 `LKMA`、边界分支、distance-aware loss，也不讨论投稿层级。

但它并不是“随便先跑一个模型”。

这一阶段的科学定位是：

> 用文献中最经典、最容易复核的最小基线，确认当前实验系统本身是可信的。

---

## 1. 这份文档解决什么问题

它只回答下面这些问题：

1. 第一轮正式实验具体跑哪个 run
2. 跑之前必须准备什么
3. 固定配置该用什么
4. 跑完后先看什么、后看什么
5. 做到什么程度才算“UNet 首轮过线”
6. 过线后下一步做什么，不过线怎么排查

---

## 2. 首轮实验的唯一目标

第一轮 `UNet` 的目标不是高分，也不是写论文主表，而是：

- 数据读取链跑通
- 训练链跑通
- 验证链跑通
- `TestA / TestB` 评估链跑通
- 可视化导出链跑通
- 错误分析链跑通

一句话说：

> 这一轮的任务是证明你的实验系统是真的能用，而不是证明 `UNet` 很强。

### 2.1 直接论文依据

这一阶段主要受下面三类论文约束：

- `U-Net`
  - `U-Net` 把 encoder-decoder + skip connection 作为标准最小基线，并明确强调小样本医学分割依赖强增强与精确定位（`U-Net_2015.pdf`, p.1-p.2, p.6）
- `GlaS Challenge`
  - `GlaS` 已把任务、官方 train / TestA / TestB 划分，以及 `F1 / Object Dice / Object Hausdorff` 评价协议定义清楚（`GlaS_Challenge_Contest_2017.pdf`, p.4, p.8-p.10）
- `Semantic Segmentation of Colon Glands with DCNN and Total Variation Segmentation`
  - 说明在腺体任务中，先建立基本 gland segmentation 流程、再讨论更复杂分离策略，是合理起点

所以这里先跑 `UNet`，不是因为它一定最好，而是因为它最适合承担“流程排雷模型”角色。

---

## 3. 正式开始前的准入条件

只有下面全部满足，才允许启动首轮 `UNet`：

- `7` 个 split CSV 已生成
- `5` 个检查文件已生成
- `GlaS train68 / val17 / testA60 / testB20` 已固定
- 你已经接受 `CRAG` 当前只是后续补充验证，不参与当前调参
- 二值化规则已经写入 `mask_conversion_note.md`
- 你已经看过 `02_结直肠腺体分割_数据准备与检查手册.md`

如果这些不满足，说明你还没到训练阶段。

---

## 4. 第一轮正式 run 只有一个

当前首轮正式实验固定为：

- `A1_UNet_GlaS_v1_seed3407`

这里每一部分都不要改名字：

- `A1`：说明它是阶段 A 第一个正式 run
- `UNet`：说明模型是 `UNet`
- `GlaS`：说明数据集是主数据集
- `v1`：说明这是当前第一版统一协议
- `seed3407`：说明是首轮排雷 seed

第一轮不允许同时再跑：

- `A2`
- `baseline`
- `LKMA`
- `CRAG`

---

## 5. 第一轮固定配置

### 5.1 模型与任务

- 模型：`UNet`
- 任务：二值语义腺体分割
- 输入：`RGB`
- 输入尺寸：`512 x 512`
- 输出：单通道前景概率图

### 5.2 数据输入

训练与验证固定读取：

- `glas_train68.csv`
- `glas_val17.csv`

测试固定读取：

- `glas_testA60.csv`
- `glas_testB20.csv`

### 5.3 标签规则

- 原始实例标注先转换为二值 mask
- 前景定义：`mask > 0`
- 输出阈值：`0.5`

### 5.4 训练设置

- loss：`BCE + Dice`
- optimizer：`AdamW`
- learning rate：`1e-3`
- scheduler：`ReduceLROnPlateau`
- epoch：最大 `120`
- early stopping patience：`20`
- AMP：开启

这套第一版协议的意义不是“最优超参数”，而是：

- 足够常见
- 足够稳定
- 后面容易和主 baseline、公平外部对比保持一致

### 5.4.1 这些配置分别来自哪里

这里必须把“论文直接支持”和“当前工程起点”分开，不然后面很容易把协议写成拍脑袋：

- `UNet + 二值 gland mask`
  - 属于`论文直接固定`
  - 依据：`U-Net` 给出最小基线结构（p.1-p.2），`GlaS Challenge` 给出对象级腺体任务定义（p.2, p.8-p.10）
- 输入尺寸 `512 x 512`
  - 属于`论文支持的候选范围`
  - 依据：`SCAU-Net` 在 gland segmentation 上直接采用 `512x512` 输入（`SCAU-Net_Spatial-Channel_Attention_U-Net_for_Gland_Segmentation_2020.pdf`, p.5）
  - 说明：它不是官方唯一尺寸，而是当前路线层为了统一 `GlaS / CRAG / 外部对比` 而选的稳定尺寸
- `BCE + Dice`
  - 属于`论文支持的固定起点`
  - 依据：`UNet++` 明确采用 `binary cross-entropy + Dice coefficient`（`UNet++_2018.pdf`, p.5）；`SCAU-Net` 也采用 `0.5 * cross-entropy + 0.5 * Dice loss`（p.5）
- 轻量增强包
  - 属于`论文支持的候选范围`
  - 依据：`U-Net` 明确强调强增强，尤其是 `elastic deformation`（p.6）；`MILD-Net` 在腺体任务上使用翻转、旋转、弹性形变、模糊和颜色扰动（`MILD-Net_Minimal_Information_Loss_Dilated_Network_2018.pdf`, p.9）
  - 说明：当前首轮只保留轻量版本，是为了先排查实验链，而不是先做增强搜索
- `AdamW + 1e-3 + ReduceLROnPlateau + max_epoch 120 + early_stop 20 + AMP`
  - 属于`工程默认起点`
  - 依据方式：当前提取文献能证明 gland 任务常见的是 `Adam/AdamW + 1e-4~5e-4 + 100~1000 epochs` 这一量级，而不是唯一固定值，例如 `SCAU-Net` 用 `Adam(1e-4), 100 epochs, batch size 4`（p.5），`DEA-Net` 用 `Adam(5e-4), 1000 epochs, batch size 4`（`Gland_Segmentation_via_Dual_Encoders_and_Boundary-Enhanced_Attention_2024.pdf`, p.3-p.4）
  - 说明：因此当前这组值是为了统一首轮闭环、便于后续公平对比而设的工程起点，不宣称为某一篇论文原样复刻
- `batch size = 当前显存下稳定不溢出的最大值`
  - 属于`工程默认起点`
  - 依据：现有论文的 batch size 差异很大，`U-Net` 偏向大 tile 小 batch（p.4），`SCAU-Net` 与 `DEA-Net` 都用 `batch size 4`（p.5；p.3-p.4）
  - 说明：因此这里不先伪装成“论文固定值”，而是先锁成可复现实验约束
- threshold 初始 `0.5`
  - 属于`工程默认起点`
  - 依据：多篇分割论文与实现默认从 `0.5` 起步，但真正有效的做法仍然是在验证集定阈值后固定到测试集；因此这里把 `0.5` 只作为首轮起点，不作为最终结论值

### 5.5 batch size 如何定

第一轮只按一个原则：

- 用当前显存下稳定且不溢出的最大值

但注意：

- 一旦你正式开始首轮训练，这一轮中途不要再改 batch size
- 如果改了，说明这轮不再是同一个 run，必须重新记 run 名

### 5.6 第一轮允许的基础增强

只允许轻量增强：

- horizontal flip
- vertical flip
- random rotation
- light scale jitter
- light color jitter

第一轮不允许：

- 复杂 stain normalization
- 很强的 elastic distortion
- 多分支增强搜索

原因：

- `U-Net` 原文虽然强调强增强的重要性，但你当前阶段的目标是先验证闭环，不是先做增强搜索
- 当前先用轻量增强，是为了让后面如果出现异常，更容易判断问题来自哪里

### 5.7 第一轮评估规则

- `best checkpoint` 只能按验证集选
- `TestA / TestB` 只做最终评估
- threshold 必须先在 `val17` 确定，再固定用于 `TestA / TestB`
- 第一轮不使用 `TTA`
- 第一轮不使用复杂后处理
- 第一轮 `TestA` 和 `TestB` 必须分开出结果

---

## 6. 训练前必须先准备好的文件

这一轮最少要有下面这些文件路径约定：

- `experiments/A1_UNet_GlaS_v1_seed3407/config.yaml`
- `experiments/A1_UNet_GlaS_v1_seed3407/seed_record.txt`
- `experiments/A1_UNet_GlaS_v1_seed3407/training_log.csv`
- `experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
- `experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
- `experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
- `experiments/A1_UNet_GlaS_v1_seed3407/summary.md`
- `experiments/A1_UNet_GlaS_v1_seed3407/error_cases.md`
- `experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best_checkpoint.pth`
- `experiments/A1_UNet_GlaS_v1_seed3407/predictions/`
- `experiments/A1_UNet_GlaS_v1_seed3407/visualizations/`

如果你训练时根本没有明确这些产物放哪，这一轮最后一定会乱。

---

## 7. 正式执行顺序

第一轮不要边做边跳，严格按下面顺序：

### 步骤 1：写 `config.yaml`

必须写清：

- 模型名
- 数据路径
- 输入尺寸
- batch size
- optimizer
- lr
- scheduler
- loss
- threshold
- seed

合格标准：

- 配置是一个完整文件
- 不是只在脑子里记住

### 步骤 2：启动训练

训练阶段必须生成：

- `training_log.csv`
- 中间 checkpoint
- 验证指标记录

训练时先看三件事：

- loss 是否下降
- 验证指标是否更新
- 是否出现 `nan`

如果一开始就 `nan` 或完全不收敛，不要硬跑满 `120` epoch。

这一步的科学判断标准是：

- 先看训练是否正常
- 再看验证是否正常
- 最后才看测试表现

不能因为想快点看到 `TestA / TestB` 数字，就跳过中间诊断。

### 步骤 3：保存最佳 checkpoint

只按验证集选择：

- `best_checkpoint.pth`

合格标准：

- 能说清最佳 checkpoint 是按什么指标、哪一轮选的

### 步骤 4：跑 `TestA`

必须输出：

- `testA_metrics.csv`
- `TestA` 预测图

### 步骤 5：跑 `TestB`

必须输出：

- `testB_metrics.csv`
- `TestB` 预测图

### 步骤 6：导出可视化

每个 split 至少要导出：

- 原图
- GT
- Pred
- Overlay

建议至少保留：

- `TestA` 中 `6-8` 个样本
- `TestB` 中 `4-6` 个样本

### 步骤 7：写 `summary.md`

这一轮结束必须写：

- 主要结果是什么
- 主要错误是什么
- 当前判断是“通过 / 待排查 / 不通过”
- 当前固定下来的 threshold 是多少

### 步骤 8：写 `error_cases.md`

至少记录：

- 黏连没分开
- 小腺体漏检
- 边界糊
- 过分割
- 欠分割

这样做的原因是：

- 腺体任务后面要讲的是形态完整性、黏连分离和边界质量
- 如果第一轮连错误类型都不记录，后面你根本无法判断 `LKMA` 或 `Boundary Head` 到底解决了什么

### 步骤 9：写首轮交接结论

这一轮结束后，还要额外写清下面四件事，供后面三次重复直接复用：

- 当前 batch size 是多少
- 当前基础增强包是什么
- 当前验证集选模指标是什么
- 当前 threshold 最终固定成多少

如果这四件事还说不清，说明首轮还没有真正交接完成。

---

## 8. 第一轮跑完后先看什么

第一轮跑完后，不要先看“最好看的一个数”，按下面顺序检查：

### 8.1 先看训练曲线

先判断：

- loss 是否在下降
- 验证指标是否在合理变化
- 是否出现明显震荡或崩溃

### 8.2 再看预测图

这是最重要的一步。

你要先肉眼判断：

- 是否大面积全黑
- 是否大面积全白
- 是否系统性偏移
- 是否把多个腺体全粘成一片
- 是否边界严重错位

如果图已经明显不对，不要被某个数字骗过去。

### 8.3 再看指标

第一轮重点先看：

- `Dice`
- `IoU`
- `HD95`

如果对象级指标链已经准备好，再加看：

- `F1`
- `Object Dice`

### 8.4 最后看落盘是否完整

确认下面都存在：

- 配置文件
- 日志
- 最佳权重
- 测试结果
- 预测图
- 错误记录

只要少一样，这一轮都不算完整通过。

---

## 9. 第一轮合格标准

只有下面全部满足，才算 `UNet` 首轮合格：

- 训练、验证、测试全部跑通
- 没有大面积全背景预测
- 没有明显系统性错位
- 预测图和指标大体一致
- 有完整日志
- 有完整结果文件
- 有一组能展示的预测图
- 你能说出主要错误类型

这里的“合格”不是“已经很强”，而是：

> 当前实验链已经能进入重复实验阶段。

这里的“合格”本质上是系统层合格，不是结果层合格。

也就是说：

- 即使分数一般，只要链条可信，依然可以过线
- 即使某个分数看起来不错，但链条不可信，依然不能过线

---

## 10. 第一轮不合格时怎么排查

如果不过线，按下面固定顺序查，不要乱跳：

### 10.1 先查数据

先查：

- 图像和 mask 是否对齐
- CSV 路径是否正确
- split 是否读错
- 二值化逻辑是否一致

### 10.2 再查标签变换

再查：

- mask resize 是否用最近邻
- 是否有地方把 mask 插值坏了
- threshold 前后逻辑是否一致

### 10.3 再查训练设置

再查：

- learning rate 是否过大
- batch size 是否不稳定
- loss 是否实现错误
- 输出激活与损失是否匹配

### 10.4 最后才查模型

如果前面都正常，再考虑：

- `UNet` 实现是否有 bug

大多数第一轮失败问题，通常不是模型结构本身，而是数据和流程。

---

## 11. 第一轮通过后下一步做什么

如果第一轮通过，下一步不是切主 baseline，而是：

> 用 `3407 / 1234 / 2025` 跑 `UNet` 三次重复。

原因很简单：

- 你还不知道当前协议稳不稳
- 现在直接切主 baseline，后面任何波动都没法归因

这一步之后仍然不允许：

- 提前开始第一批外部对比
- 提前开始 `CRAG` 补充验证
- 一边做 `UNet` 三次重复一边改数据协议

---

## 12. 什么时候才允许进入主 baseline

只有下面这些全部满足，才允许进 `ResNet34-U-Net`：

- 首轮 `UNet` 已通过
- 已跑 `3` 个 seed
- 有 `mean +- std`
- 你知道 `UNet` 的主要错误类型
- 结果文件已完整归档
- 当前 threshold、batch size、基础增强包已经固定并写入阶段汇总

如果这些还没做，不要进下一步。

---

## 13. 你如果只记一句话

> `UNet` 首轮的任务不是拿高分，而是证明你的数据、训练、验证、测试、可视化和结果归档这一整条实验链是真的能用。
