# R34UNet结构与来源

本文件不是对 `ResNet34-U-Net` 的概念介绍，也不是给 `04_Baseline` 补一段“结构大概长什么样”的说明。

它在当前项目中的唯一职责是：

> 作为 `04_Baseline` 阶段的结构协议细则，把 `ResNet34-U-Net` 为什么被固定为正式 baseline、它的最小结构定义是什么、哪些结构差异允许进入 `UNet -> R34UNet` 比较、哪些改动必须被判为越界、以及这些规则在代码与运行记录里如何落地，一次写死。

从现在开始，只要讨论 `04_Baseline` 的结构身份、encoder 初始化、skip 边界、结构记录字段和向下游模块交接的主干定义，都以本文件为准；若与同层其他文件冲突，以 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` 为总口径，本文件负责把结构层细化到可直接落代码的程度。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面六件事：

1. `ResNet34-U-Net` 作为全文唯一正式 baseline 的结构身份。
2. baseline 的最小结构定义，即 `ResNet34 encoder + U-Net style decoder + single-channel segmentation logit`。
3. `UNet -> R34UNet` 迁移时唯一允许变化的结构变量与禁止越界项。
4. encoder 预训练初始化、skip 来源、输入输出接口与结构记录字段。
5. baseline 结构层与同层训练、比较、验收文件之间的职责边界。
6. 后续 `LKMA / Boundary` 只能在这份已冻结主干上追加单变量模块的交接前提。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- 数据身份、split、标签规则、输入尺寸与归一化。
- `train_proto_v1 / eval_proto_v1` 的完整训练与评估 protocol。
- `UNet vs R34UNet` 的正式比较门、阶段总放行门和汇总表 schema。
- `LKMA`、`Boundary Head`、`Distance-aware Loss` 等后续模块设计。

这些职责分别由下列文件承担：

- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

因为 `Baseline` 阶段最容易发生的偷换，不是“模型没搭起来”，而是把：

- `plain encoder -> residual encoder`
- `U-Net style decoder`
- `official ImageNet-1K supervised weights`

这几个本应冻结的结构层定义，混成：

- 顺手改 decoder
- 顺手加 attention
- 顺手改多分支输出
- 顺手引入后续模块

如果没有一份独立结构协议，后面的 `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\02_训练协议.md`、`结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\03_对比与判断规则.md` 和 `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\04_阶段验收.md` 就无法判断当前比较到底是不是“只差结构升级”。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求本文件按正式协议整篇重写，而不是沿用旧稿局部补丁。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把 `crc_gland_segmentation_project/configs/`、`crc_gland_segmentation_project/src/`、`crc_gland_segmentation_project/scripts/`、`crc_gland_segmentation_project/experiments/`、`crc_gland_segmentation_project/reports/` 的结构落点写清。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 `512 x 512`、`light_aug_v1`、`BCE + Dice`、固定三 seed 和 baseline 阶段不得重开的全局边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：约束 `run_name`、版本字段链、`result_tag`、`aggregation` 和 run_meta.yaml 字段命名。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束 `best_selector = val_objdice_max`、`threshold_source = val17`、`TestA / TestB` 分开报告和对象级指标优先级。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求结构规则必须落到入口函数、I/O、配置字段、前置断言和运行产物。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求本文件保留规则卡片、代码落地接口、冲突裁决、验收与回退说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求显式写明前置文件、上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线顺序为 `UNet -> ResNet34-U-Net -> LKMA -> Boundary -> Distance`。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：明确 `B1` 是正式 baseline 定义阶段，不是临时过渡阶段。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求当前文件只把 baseline 结构基座冻结到位，不能越级写成最终方法结论。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md`：提供 `U-Net` 的 decoder 组织原则、skip connection 语义和最小分割基线身份。
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/05_ResNet.md`：提供 `ResNet34` 作为经典 residual encoder 的结构与预训练合理性依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS` benchmark、对象级指标和 `TestA / TestB` 分开统计的任务背景。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供腺体任务里边界模糊、黏连分离和对象级评价优先的结构动机。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`：冻结数据身份、split、标签规则和输入规格，是本文件不能重开数据接口的最上游约束。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`：冻结 `A2` 的三 seed 稳定基线、独立 `回退条件` 和独立 `Diagnostics 闭环`，是本文件最直接的模板强度上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`：提供固定三 seed 身份和正式 run 命名边界，确保 `R34UNet` 继续沿用同一 seed 体系。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`：提供 `single_seed / mean+-std` 的结果身份写法，决定结构文件中的运行记录字段必须与统计层兼容。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`：提供 `UNet` 放行到 baseline 的上游门槛，保证本文件只在稳定基线已成立的前提下定义结构升级。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`：负责 baseline 总身份、唯一变量、门控与交接；本文件是它的结构细则。
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`：负责 `train_proto_v1 / eval_proto_v1` 继承、batch 政策与阈值边界；本文件必须与其保持单变量比较一致。
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md`：负责 `UNet vs R34UNet` 的正式比较对象和 `Gate_B1_compare`；本文件提供其所需的结构层公平比较前提。
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`：负责 `Gate_B1`、冻结清单和 handoff 资产；本文件提供结构冻结项和结构回退边界。

#### 同批模板强度对照

- 主结构模板：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 收尾强度模板：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 同层对齐模板：`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`

本轮对照的固定结论是：

- 当前文件虽然是结构细则，不是阶段总协议，但 `文件质量自检` 和 `Diagnostics 闭环` 的标题独立性、条目颗粒度和闭环写法，不得弱于 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`。
- 当前文件虽然不直接做阶段总放行，但仍必须保留独立 `回退条件`，因为结构初始化失败、skip 越界或结构变量污染会直接破坏 baseline 身份。
- 当前文件必须与 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` 在 baseline 身份、唯一变量和下游交接语义上完全对齐，不能另写一套更松的结构解释。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/00_阶段总协议.md`：直接消费 baseline 主干、初始化和 batch 政策，只允许在冻结主干上追加 `LKMA`。
- `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`：直接消费 baseline 或 `baseline + kept LKMA` 的主干定义，要求本文件先把 encoder/decoder 主干和输出接口写死。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前阶段真正要证明什么

`04_Baseline` 阶段不是继续证明流程能跑，而是要把“全文唯一正式比较基座”的结构协议压实。

当前文件真正要证明的是：

1. 在 `UNet` 三次稳定基线已经成立的前提下，当前项目唯一正式结构升级版本固定为 `ResNet34-U-Net`。
2. `UNet -> R34UNet` 这一步唯一允许变化的主变量是 `plain encoder -> residual encoder`。
3. baseline 的结构身份、skip 边界、初始化口径、接口形状和记录字段已经冻结到可直接指导实现。
4. 后续 `LKMA / Boundary` 只能建立在这份主干定义之上，而不能反向重新选择 baseline。

### 3.2 为什么正式 baseline 固定为 `ResNet34-U-Net`

固定它为正式 baseline 的原因是：

- `UNet` 已完成流程验证和三次稳定，当前最需要的是“更强但仍可解释”的正式结构基座。
- `ResNet34` 是经典 residual encoder，结构成熟、工程稳定、复现成本可控。
- `ResNet34-U-Net` 足够强，能承担后续模块比较基座，但又没有强到把后续单变量模块空间全部吃掉。
- 相比 `ResNet50/101` 或更复杂的 attention / multi-scale 结构，它更适合承载“唯一新增变量是 encoder 升级”的公平比较。

### 3.3 当前不采用的相邻方案

当前明确不采用：

- 继续把 plain `UNet` 直接当全文唯一正式 baseline。
- 在 baseline 首版直接上 `ResNet50/101`。
- 在 baseline 首版混入 attention、多尺度复杂头、边界分支或距离约束。
- 直接拿外部封装模型替代当前项目内的正式 baseline 协议。

---

## 4. 阶段门控表达式

### 4.1 当前阶段直接继承哪些冻结项

本文件直接继承并不得擅自改动的上位规则如下：

- 主任务：`2D gland segmentation`
- 主数据集：`GlaS`
- 正式 split：`train68 / val17 / testA60 / testB20`
- 标签口径：`mask > 0`
- 输入通道：`RGB`
- 输入尺寸：`512 x 512`
- 归一化：`ImageNet mean/std`
- 增强版本：`light_aug_v1`
- 主损失：`L_seg = L_BCE + L_Dice`
- 优化协议：`AdamW + lr 1e-3 + weight_decay 1e-4 + ReduceLROnPlateau + epoch_max 120 + early_stopping 20 + AMP on`
- 主指标优先级：`F1 / Object Dice / Object Hausdorff`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `eval_cast_policy = logits/probabilities must be kept or cast to float32 before thresholding`
- `boundary_metric_width = 3 px`
- `boundary_metric_impl = skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`
- `connected_components_impl = scipy.ndimage.label`
- `connected_components_connectivity = 8`
- `train_proto_version = train_proto_v1`
- `eval_proto_version = eval_proto_v1`
- `postprocess_version = none_in_v1`
- 固定三 seed：`3407 / 1234 / 2025`

### 4.2 当前阶段禁止重新打开哪些问题

本文件禁止借结构说明之名重新打开：

- 数据 split、标签定义、输入尺寸和归一化。
- 主增强包、主损失、optimizer、lr、scheduler、epoch 与 early stopping。
- `best_selector`、阈值来源、`threshold` 前 `float32` 边界、`Boundary F1` 宽度/实现和连通域实现/连接性定义。
- 对象级指标实现与 `TestA / TestB` 分开统计规则。
- `LKMA`、边界分支、距离约束或其它后续模块。

### 4.3 为什么当前阶段只能继承不能重开

因为 `B1` 结构文件要回答的不是“还有哪些结构也可以试”，而是：

> 在完全相同的数据、训练和评估 protocol 下，单独把 encoder 从 plain 升级为 residual，是否足以建立正式 baseline。

如果这里同时夹带：

- 改 decoder 主体
- 改训练协议
- 改评估链
- 加后续模块

后面就无法判断提升到底来自 encoder 升级，还是来自额外协议漂移。

---

## 5. 本阶段规则卡片

下面所有核心规则都写成正式协议格式；后续实现时，只允许把这些规则忠实落地，不允许再擅自补新的隐含结构变量。

### 5.1 正式 baseline 身份与最小结构定义

- 当前结论：`04_Baseline` 阶段的正式主 baseline 固定为 `ResNet34-U-Net`，其最小定义固定为 `encoder = ResNet34`、`decoder = U-Net style decoder`、输出为单通道腺体前景 `logit`。
- 规则类型：`路线层已锁定 + 论文直接支持 + 工程冻结规则`
- 适用阶段：`04_Baseline` 开始生效，后续 `LKMA / Boundary` 全部继承。
- 直接依据：02_U-Net.md、05_ResNet.md、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：残差单元满足 `y = F(x, {W_i}) + x`；整体分割主干固定为 `logits = Dec_theta_d(Enc_theta_e(x))`
- 采用原因：把 backbone 升级与 decoder 语义恢复解耦，保持结构解释清晰、工程复用稳定。
- 不采用的相邻方案：不把 baseline 定义成“残差 encoder + 新头 + 新分支”的组合体。
- 代码落点：src/models/r34_unet.py、src/models/encoders/resnet34.py、src/models/decoders/unet_decoder.py、configs/model/r34_unet_v1.yaml
- 运行记录字段：`model_name`、`model_version`、`encoder_name`、`decoder_name`、`out_channels`
- 验收方式：检查模型摘要明确为 `ResNet34 encoder + U-Net style decoder`；检查输出尺寸与标签一致；检查没有额外结构模块。

### 5.2 skip connection 与 decoder 边界

- 当前结论：skip connection 只允许来自 `ResNet34` 的固定阶段特征，decoder 继续按标准 `U-Net` 的逐级上采样与拼接逻辑恢复空间分辨率。
- 规则类型：`论文直接支持 + 工程冻结规则`
- 适用阶段：`04_Baseline`
- 直接依据：02_U-Net.md、05_ResNet.md、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：每一级恢复逻辑固定为 `F_l^dec = Phi([Up(F_{l+1}^dec), F_l^enc])`
- 采用原因：只有保留标准 `U-Net` skip 语义，`UNet -> R34UNet` 才仍然是同类 encoder-decoder 结构比较。
- 不采用的相邻方案：不改成 feature pyramid、多头融合、跨级密集连接或多主干恢复。
- 代码落点：src/models/r34_unet.py、src/models/decoders/unet_decoder.py
- 运行记录字段：`encoder_feature_stages`、`skip_levels`、`decoder_channels`
- 验收方式：检查 skip 来源固定且可追溯；检查 decoder 仍是单主干逐级恢复结构。

### 5.3 输入输出与任务接口

- 当前结论：baseline 结构接口必须与上游 `UNet` 保持同任务定义，即输入为 `B x 3 x 512 x 512`，输出为 `B x 1 x 512 x 512`。
- 规则类型：`上游继承规则 + 工程冻结规则`
- 适用阶段：`04_Baseline`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：预测链固定为 `p = sigmoid(logits)`，二值输出为 `y_hat = 1[p >= threshold]`
- 采用原因：只有保持任务接口一致，训练、评估、可视化和下游模块接口才能统一复用。
- 不采用的相邻方案：不改成多类别头；不在 baseline 阶段新增边界输出或距离输出。
- 代码落点：src/models/r34_unet.py、`crc_gland_segmentation_project/scripts/train.py`、scripts/test.py
- 运行记录字段：`input_size`、`in_channels`、`out_channels`、`threshold_value`、`eval_proto_version`、`eval_cast_policy`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`
- 验收方式：检查训练和测试脚本继续消费同一类 tensor 形状；检查预测 mask 与评估脚本接口兼容；检查 run_meta.yaml 与阶段结构总结继续显式记录 `threshold` 前 `float32` 边界、`Boundary F1` 宽度/实现和连通域实现/连接性字段。

### 5.4 encoder 初始化与预训练规则

- 当前结论：`ResNet34` encoder 初始化固定为 `official ImageNet-1K supervised weights`；若未正确加载，该 run 不得记为正式 baseline run。
- 规则类型：`工程冻结规则`
- 适用阶段：`04_Baseline` 开始生效，后续模块阶段继承。
- 直接依据：05_ResNet.md、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- 核心公式或定义参考：初始化协议固定为 `theta_e^0 <- theta_resnet34_imagenet`
- 采用原因：统一、可追溯的官方预训练权重更稳定，也更符合 residual encoder 的常见工程使用方式。
- 不采用的相邻方案：不混用预训练与随机初始化；不使用来源不明的第三方权重；不在后续模块阶段偷偷改回随机初始化。
- 代码落点：src/models/encoders/resnet34.py、configs/model/r34_unet_v1.yaml
- 运行记录字段：`encoder_pretrained`、`encoder_weight_source`、`encoder_weight_version`、`encoder_weight_hash`、`encoder_load_status`
- 验收方式：检查 run_meta.yaml 与日志明确记录权重来源和加载状态；检查三次正式 run 保持一致。

### 5.5 `UNet -> R34UNet` 的唯一允许差异

- 当前结论：`UNet -> R34UNet` 迁移时，只允许修改结构相关内容，包括 encoder 接入、skip 特征抽取、decoder 对接和通道匹配。
- 规则类型：`上游继承规则 + 工程冻结规则`
- 适用阶段：`04_Baseline`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：`diff(B1, A2) in {encoder_upgrade, encoder_init, skip_alignment, decoder_alignment}`
- 采用原因：保证 `UNet vs R34UNet` 的比较真正只差结构。
- 不采用的相邻方案：不在迁移时顺手改训练协议、评估协议、阈值规则或后处理。
- 代码落点：src/models/r34_unet.py、src/models/encoders/resnet34.py、src/models/decoders/unet_decoder.py
- 运行记录字段：`model_version`、`encoder_feature_stages`、`decoder_channels`
- 验收方式：检查结构差异只集中在结构文件；检查 train/eval 协议版本继续继承上游冻结口径。

### 5.6 baseline 阶段明确禁止的结构扩展

- 当前结论：baseline 阶段严禁顺手加入 `LKMA`、边界分支、距离约束、attention、多尺度复杂头或其它增强分支。
- 规则类型：`路线层已锁定 + 工程冻结规则`
- 适用阶段：`04_Baseline`
- 直接依据：02_结直肠腺体分割_分阶段实验路线与执行标准.md、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 采用原因：这一阶段唯一新增变量应该是 encoder 升级，否则后续无法判断 baseline 增益究竟来自哪里。
- 不采用的相邻方案：不做“先顺手加一个模块以后再说”的混合 baseline。
- 代码落点：src/models/r34_unet.py、configs/model/r34_unet_v1.yaml
- 运行记录字段：`model_version`、`extra_module_flags`
- 验收方式：检查 `model_version` 与结构图中没有额外模块；检查配置中相关模块开关全部关闭或不存在。

### 5.7 正式必须记录的结构字段

- 当前结论：只要 baseline 进入正式实验，至少必须记录 `model_name / model_version / encoder_name / encoder_pretrained / encoder_weight_source / decoder_name / skip_levels / out_channels / params_m`。
- 规则类型：`工程冻结规则`
- 适用阶段：`04_Baseline`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：结构记录层必须与统计层共用同一 run_meta.yaml 与阶段汇总字段链
- 采用原因：如果结构字段不显式落盘，后续阶段无法确认自己继承的是哪一个正式主干。
- 不采用的相邻方案：不把结构信息藏在自然语言总结里；不只记录 `model_name` 不记录初始化来源。
- 代码落点：run_meta.yaml、scripts/summarize_stage.py、reports/stage_reports/baseline_structure_report.md
- 运行记录字段：`model_name`、`model_version`、`encoder_name`、`encoder_pretrained`、`encoder_weight_source`、`decoder_name`、`skip_levels`、`out_channels`、`params_m`、`flops_g`、`latency_ms`
- 验收方式：检查三次正式 run 和阶段结构总结中结构字段齐全且取值一致。

---

## 6. 代码实现约束

### 6.1 本阶段必须新增或正式存在的对象

- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/01_R34UNet结构与来源.md`
- src/models/r34_unet.py
- src/models/encoders/resnet34.py
- src/models/decoders/unet_decoder.py
- configs/model/r34_unet_v1.yaml
- reports/stage_reports/baseline_structure_report.md

### 6.2 本阶段必须复用或对齐的对象

- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
- `crc_gland_segmentation_project/scripts/train.py`
- scripts/test.py
- scripts/summarize_stage.py

### 6.3 本阶段禁止修改的对象

- `splits/glas/*.csv`
- `crc_gland_segmentation_project/configs/data/glas.yaml` 中的数据身份、标签口径和输入尺寸
- configs/train/unet_flow_v1.yaml 的正式优化协议
- src/metrics/object_metrics.py 的对象级评估口径
- `train_proto_v1 / eval_proto_v1` 的正式定义
- `LKMA`、边界分支和距离约束的结构定义

### 6.4 本阶段必须新增的结构记录字段

后续所有正式 baseline run 与汇总结果中，至少要记录：

- `run_name`
- `stage_name`
- `model_name`
- `model_version`
- `encoder_name`
- `encoder_pretrained`
- `encoder_weight_source`
- `encoder_weight_version`
- `encoder_weight_hash`
- `decoder_name`
- `encoder_feature_stages`
- `skip_levels`
- `decoder_channels`
- `out_channels`
- `train_proto_version`
- `eval_proto_version`
- `best_selector`
- `threshold_source`
- `threshold_value`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `result_tag`
- `aggregation`
- `params_m`
- `flops_g`
- `latency_ms`

### 6.5 本阶段代码落地底线

本阶段任何脚本都必须满足：

- baseline 结构只能通过固定的 `r34_unet_v1` 配置启动。
- encoder 初始化来源必须可追溯，且三次正式 run 一致。
- skip 层级与 decoder 通道必须显式记录，不能藏在代码默认值里。
- `LKMA / Boundary / Distance` 不得以任何隐式默认值混入 baseline 结构。
- 结构字段必须进入 run_meta.yaml 和阶段汇总，而不是只留在代码注释或 README 中。
- `threshold` 前的 `logits / probabilities` 必须保持为或显式转换为 `float32`，不得因 `AMP` 或结构接线差异静默漂移。
- `Boundary F1` 必须继续使用 `3 px` 主宽度、冻结实现和 `8-connectivity` 连通域口径。

---

## 7. 回退条件

### 7.1 独立回退触发条件

只要出现下面任意一条，本文件负责的结构协议就必须先回退修正，而不是直接进入后续训练、比较或下游模块阶段：

- `ResNet34` encoder 预训练权重未正确加载或来源不可追溯。
- skip 抽取层级、通道匹配或输出尺寸错误，导致主干接口不再等价于 baseline 定义。
- baseline 结构混入 `LKMA`、边界分支、距离约束或其它额外模块。
- `UNet -> R34UNet` 比较被非结构变量污染，却仍试图写成纯结构升级。
- run_meta.yaml 中的结构字段缺失，或 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity / result_tag / aggregation` 没有继续落盘，导致后续无法确认继承的是哪一个正式主干和哪一版正式结果身份。

### 7.2 固定回退顺序

回退时统一按下面顺序排查：

1. 检查 `ResNet34` encoder 接入与预训练加载是否正确。
2. 检查 skip 抽取层级、通道匹配和输出尺寸是否正确。
3. 检查 decoder 是否仍为 `U-Net style decoder`，而非其它复杂恢复结构。
4. 检查结构字段是否已正确写入 `config.yaml / run_meta.yaml / stage report`。
5. 只有确认前面都无问题后，才允许把差异解释为真实结构比较结果。

### 7.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件对应的结构协议已恢复可用：

- 结构问题来源已经按固定顺序定位并修复。
- 修复动作、影响范围和复验结果已写入 notes/debug_note.md、逐 run 总结或阶段总结。
- config.yaml、run_meta.yaml、结构摘要和阶段汇总字段重新对齐。
- 当前结构重新满足第 `5` 节全部规则卡片与第 `6` 节代码实现约束。

---

## 8. 代码落地接口

### 8.1 结构构建入口

- 代码文件：src/models/r34_unet.py、src/models/encoders/resnet34.py、src/models/decoders/unet_decoder.py
- 入口类/函数：`build_r34_unet()`、`build_resnet34_encoder()`、`build_unet_decoder()`
- 输入：图像张量 `B x 3 x 512 x 512`、结构配置对象 `model_cfg`
- 输出：分割 `logits` 张量 `B x 1 x 512 x 512`
- `dtype`：输入图像为 `float32` 或 AMP 下的 `float16/bfloat16`；输出 `logits` 为浮点型
- 依赖配置：`model_name`、`model_version`、`encoder_name`、`encoder_pretrained`、`decoder_channels`、`out_channels`
- 前置断言：`encoder_name = resnet34`；预训练来源可追溯；不得混入 `LKMA / Boundary / Distance` 额外模块
- 运行产物：模型摘要、结构日志、参数量记录写入 run_meta.yaml 与 reports/stage_reports/baseline_structure_report.md

### 8.2 正式训练与评估绑定入口

- 代码文件：`crc_gland_segmentation_project/scripts/train.py`、scripts/test.py
- 入口类/函数：`main(cfg)`、`run_eval()`
- 输入：`configs/experiment/B1_R34UNet_GlaS_v1_seed*.yaml`、固定 split、冻结阈值与 checkpoint 选择规则
- 输出：baseline 正式 run 目录下的 config.yaml、run_meta.yaml、val_metrics.csv、testA_metrics.csv、testB_metrics.csv
- `dtype`：图像为 `float32` 或 AMP 浮点；mask 为 `float32`；二值预测为 `uint8/bool`
- 依赖配置：`train_proto_version`、`eval_proto_version`、`best_selector`、`threshold_source`、`threshold_value`、`eval_cast_policy`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`、`result_tag`、`aggregation`
- 前置断言：结构版本、初始化策略和结构字段必须在三次 seed 中保持一致；结构层不得反向改写训练与评估协议；`threshold` 前必须保持 `float32`；`Boundary F1 = 3 px` 与 `8-connectivity` 连通域口径必须继续与 `UNet` 稳定基线完全一致
- 运行产物：三次 baseline 正式 run 目录、split 级指标、可视化与结构元数据

### 8.3 结构汇总入口

- 代码文件：scripts/summarize_stage.py
- 入口类/函数：`summarize_baseline_stage()`
- 输入：三次 baseline run 目录、结构字段、复杂度统计项
- 输出：reports/stage_reports/baseline_structure_report.md 与阶段汇总中的结构冻结结论
- `dtype`：结构字段以字符串、整数和浮点统计项为主
- 依赖配置：`encoder_pretrained`、`encoder_weight_source`、`skip_levels`、`params_m`、`flops_g`、`latency_ms`、`eval_cast_policy`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`、`result_tag`、`aggregation`
- 前置断言：结构版本在三次正式 run 中保持一致；复杂度统计口径一致；结构总结必须把评估实现硬字段与结果身份字段一起写入正式冻结记录，不能只保留结构字段
- 运行产物：结构摘要、复杂度说明和对下游可继承字段清单

---

## 9. 冲突裁决记录

- 冲突对象：旧版文件的“结构说明文”写法与当前批次要求的“可直接落代码的结构协议细则”之间的不一致。
- 冲突来源：旧版已经说明了 `ResNet34-U-Net` 的 baseline 身份和大致结构，但缺少显式前置依赖、完整上游 / 同层 / 下游、独立 `回退条件`、与同批模板对齐的收尾强度，以及与同层训练 / 比较 / 验收文件完全打通的字段链。
- 裁决结论：本文件本轮正式按结构协议细则整篇重写，并把结构身份、skip 边界、初始化规则、结构记录字段、代码接口、回退条件、`文件质量自检` 和独立 `Diagnostics 闭环` 一次补齐。
- 裁决理由：如果 `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\01_R34UNet结构与来源.md` 继续停留在结构概述层，后续 `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\02_训练协议.md`、`结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\03_对比与判断规则.md` 和 `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\04_阶段验收.md` 仍会出现“知道大概怎么做，但不知道什么算结构越界”的问题。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/01_R34UNet结构与来源.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/03_对比与判断规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/05_LKMA/00_阶段总协议.md`
- 是否需要回流修订：需要；后续若同层或下游文件仍弱化 `ResNet34-U-Net` 的正式主干身份、初始化来源或结构字段链，必须按本文件口径回改。
- 代码实现影响：影响 src/models/r34_unet.py 的正式接口定义、configs/model/r34_unet_v1.yaml 的字段集合、run_meta.yaml 的结构记录字段，以及后续阶段判断“什么算纯结构升级”的边界。

---

## 10. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文。
- [x] 已继续补读 `02_路线与投稿`、`03_文献证据`、`01_数据协议`、`03_UNet稳定性` 全套相关上游，以及 04_Baseline/00/02/03/04 同层文件和 05_LKMA/00、06_Boundary/00 下游文件，而不是停在总览层。
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论。
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明这些文件为什么与“结构协议细则”直接相关。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` 的模板强度对照，确认当前文件的 `文件质量自检` 与 `Diagnostics 闭环` 没有缩水。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` 的同层语义对齐，确保 baseline 身份、唯一变量和交接语义不冲突。
- [x] 当前版本按整篇重写执行，不是对旧稿追加零散补丁说明。
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担 baseline 结构冻结职责。
- [x] 已写清为什么正式 baseline 固定为 `ResNet34-U-Net`，而不是更重 backbone、复杂新头或外部封装结构。
- [x] 已把 baseline 身份、最小结构定义、skip 边界、输入输出接口、初始化规则、唯一允许差异、禁止扩展和结构记录字段写成正式规则卡片。
- [x] 每条核心规则都保留了 `当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式`。
- [x] 涉及结构定义、残差单元、decoder 恢复逻辑和预测链的地方，已补充公式、定义或实现级解释，并达到“可直接翻译代码 + 可直接写入论文”的最低深度。
- [x] 关键术语、版本名、run 字段和代码字段已与 `01_数据协议`、`03_UNet稳定性`、04_Baseline/00-04 和下游阶段保持一致。
- [x] 已写清结构文件不能重开的训练、评估与后续模块变量，避免把结构升级写成协议漂移。
- [x] 已写清独立 `回退条件`，没有把回退要求藏进总结句或验收句里顺带带过。
- [x] 已写清代码实现约束和代码落地接口，接口对象细化到入口函数、I/O、依赖配置、前置断言和运行产物。
- [x] 已补写 `冲突裁决记录`，说明旧口径与新口径如何统一、影响哪些文件以及后续如何回流修订。
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、规则卡片、回退、接口和收尾闭环。
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“已检查”。
- [x] 当前文件在落盘后仍需执行回读和 diagnostics 复核，闭环动作不会被正文写作替代。
- [x] 当前文件已经达到“可直接指导结构实现、训练对齐、阶段验收、下游继承和论文写作”的最低强度。

---

## 11. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成。
- 复核范围：至少覆盖标题层级、列表结构、术语一致性、字段命名一致性、`上游 / 同层 / 下游` 显式落点，以及是否存在可见 markdown 诊断问题。
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核。
- 对照要求：本节保持与 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话。

---

## 12. 一句话版本

> `结直肠腺体分割_plan_优化版\01_实验执行\04_Baseline\01_R34UNet结构与来源.md` 的正式职责已经固定为：在 `UNet` 稳定基线和 `train_proto_v1 / eval_proto_v1` 已冻结的前提下，只把 baseline 的结构变量升级为 `ResNet34 encoder + U-Net style decoder`，并用统一的官方预训练初始化、固定的 skip 边界、固定的输入输出接口和可追溯的结构字段，把 `ResNet34-U-Net` 冻结为后续 `LKMA / Boundary` 只能继承、不能反向重开的唯一正式主基座。
