# AttUNet适配方案

这份文件不是对 `Attention U-Net` 的通用介绍，也不是“先把注意力门接进来再说”的接入备忘。

它在当前项目里的唯一职责是：

> 把 `Attention U-Net` 在 `08_外部对比` 阶段中的正式比较身份、结构本体、最小必要差异、公平边界、实现入口、结果字段、验收方式和回退条件一次写死。后续代码、实验、主表草稿和论文文字只允许忠实实现这份协议，不允许一边适配一边重新决定 gate 放哪一层、是否扩 decoder、是否加额外监督、是否混入别的注意力技巧。

从现在开始，`Attention U-Net` 的所有正式 run 都必须同时受 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md` 约束；若当前文件与这两个上位协议冲突，以它们为准回改当前文件。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面八件事：

1. `Attention U-Net` 作为首批核心外部对比之一的正式角色、路线意义和主表位置。
2. `Attention U-Net` 在当前工程中的结构身份，也就是 `vanilla U-Net backbone + additive attention gates on skip connections` 的最小可解释集合。
3. `Attention U-Net` 在统一数据、训练、评估和结果记录协议下的唯一合法适配方式。
4. `gate_levels`、`gate_inter_channels`、`gating_source`、`decoder_channels_fixed`、`encoder_pretrained` 等一级解释变量的记录底线。
5. 原文 `3D CT` 背景、器官分割训练设置和当前 `2D gland segmentation` 公平主表协议之间的来源边界。
6. `Attention U-Net` 的代码落地接口、前置断言、运行产物和结果汇总入口。
7. `Attention U-Net` 的最低交付物、主表资格、三 seed 补证触发和下游 handoff 语义。
8. 当前文件自身的独立 `回退条件`、`冲突裁决记录`、`文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- `GlaS` 的数据身份、split、标签口径、输入尺寸和归一化。
- `train_proto_v1 / eval_proto_v1` 的训练与评估协议本体。
- `current_mainline` 的来源；它只能由 `07_Distance` 的正式结论唯一给出。
- `UNet++`、`DeepLabV3+`、增强外部和任务内 direct comparison 的各自适配细则。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md` 的表注规则本体。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md` 的整阶段总裁决。
- `09_CRAG验证`、`10_结果汇总`、`11_总验收与止损` 的下游角色定义。

### 1.3 为什么当前文件必须独立存在

`Attention U-Net` 是首批外部方法里最容易出现“名字对了，实际公平边界已经漂移”的对象，主要风险不是完全跑不起来，而是：

- 只写 `Attention U-Net` 方法名，不记录 gate 接入层级、gating source、通道压缩和 decoder 宽度是否变化。
- 默认沿用第三方仓库的 attention 变体、deep supervision、预训练 encoder 或附加 attention block，却仍声称是在公平复现 `Attention U-Net`。
- 把“在 `U-Net` skip 上加 attention gate”的结构收益和“扩大基础骨干、追加额外注意力、追加额外监督”的收益混写。
- 在正式主表里只留一个数字，却说不清它属于 `reproduced`、`†` 还是 `*`。

如果没有一份独立方法协议，后续 external_main_table_draft.csv、来源标记、同层方法对照和下游结果汇总都会出现“同样叫 `Attention U-Net`，但实际 gate 身份和公平边界不唯一”的灰区。

---

## 2. 前置文件依赖

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件按正式方法协议整篇重写，而不是保留旧版说明文结构。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把 `crc_gland_segmentation_project/external/`、`crc_gland_segmentation_project/configs/`、`crc_gland_segmentation_project/scripts/`、`crc_gland_segmentation_project/reports/` 的路径、产物和交接语义写清。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 `GlaS`、统一训练评估协议、正式种子和结果字段链的冻结边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：约束 `H1_AttUNet_GlaS_v1_seed*`、`run_name`、`aggregation` 与方法级 run_meta.yaml 字段。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：冻结 `best_selector = val_objdice_max`、`threshold_source = val17`、对象级指标优先和 `TestA / TestB` 分开报告。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求当前文件把方法协议落到构建入口、训练入口、结果汇总入口、I/O、前置断言和运行产物。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求规则卡片、代码接口、运行字段、验收方式和冲突裁决显式齐全。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求显式写出前置文件、上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主路线为 `UNet -> ResNet34-U-Net -> LKMA -> Boundary -> Distance -> 外部对比 -> CRAG`。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：明确 `Attention U-Net` 是投稿版第一批外部对比必跑名单之一，且默认只替换网络结构，不顺手改训练口径。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求外部层必须形成可解释、来源边界清楚的主表第一层，而不是为了凑方法数失控扩展。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`：提供 `Attention U-Net` 的核心身份，即 `additive attention gate + skip filtering + coarse gating signal`，并给出注意力门公式、参数增量和原文任务边界。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供当前 benchmark 和对象级评价传统，约束不能把原始语义器官分割评估口径直接搬进腺体对象级主表。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供腺体任务对象级指标和主表解释传统，要求外部方法必须回收到当前对象级评估链。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`：给出 `current_mainline` 的唯一合法来源，因此当前文件不能重新定义主线。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`：给出 `Attention U-Net` 作为 `core_external` 的阶段角色、`Gate_H1` 和三 seed 补证门。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`：给出 `external_run_fair`、`allowed_gap`、`direct_comparison_eligible` 等统一公平边界；当前文件只能细化，不得另起一套公平口径。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/02_UNetPP适配方案.md`：同属首批通用外部方法，和当前文件共享统一训练评估协议与来源边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`：当前同层强模板，用于对照方法协议颗粒度、独立 `回退条件`、`文件质量自检` 和 `Diagnostics 闭环` 是否缩水。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`：定义 `reproduced / † / *` 和直比准入；当前文件要为 `Attention U-Net` 的结果字段提供可直接接入的来源信息。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`：定义整阶段最低交付物；当前文件的最低交付物和通过线必须与其兼容。

#### 同批模板强度对照

- 主结构模板：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 阶段母协议模板：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- 同层方法强模板：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`
- 下游 handoff 模板：`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`

本轮对照后的固定结论是：

- 当前文件虽然是方法级协议，不是阶段母协议，但前部结构、独立 `回退条件`、`文件质量自检` 和独立 `Diagnostics 闭环` 不能弱于同批强模板。
- 当前文件虽然不直接负责下游阶段裁决，但必须提前把 `result_source_type`、`direct_comparison_eligible`、`need_three_seed_followup` 和结果来源边界写成下游可直接消费的字段。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`：会消费 `current_mainline`、外部层来源边界和主表资格，因此当前文件必须保证 `Attention U-Net` 的结果身份可直接读取。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：会把 `Attention U-Net` 汇入外部主表层；当前文件必须保证来源字段和主表资格明确。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：会消费当前方法是否完成、是否需要三 seed、是否具备正式主表资格等结论，因此当前文件不能留下模糊状态。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

当前文件要证明的不是“`Attention U-Net` 可以在工程里跑起来”，而是：

> 在 `current_mainline` 已冻结、统一数据训练评估协议已冻结的前提下，`Attention U-Net` 能否作为“在 `U-Net` skip connection 上引入 additive attention gate”的代表，以最小必要差异接入当前腺体任务并形成可追溯、可解释、可进入外部主表的正式结果。

### 3.2 当前文件唯一允许变化的变量

本文件唯一允许处理的核心变量固定为：

```text
attunet_external_run = unified_protocol + attunet_architecture_identity + documented_minimal_gap_only
```

其中：

- `unified_protocol`：统一数据、训练、评估、结果记录和来源边界协议。
- `attunet_architecture_identity`：`vanilla U-Net encoder-decoder + additive attention gates on skip connections`。
- `documented_minimal_gap_only`：接入当前统一框架不可避免、但已经显式记录的最小必要差异。

### 3.3 `Attention U-Net` 在当前项目中的结构身份

当前 `Attention U-Net v1` 的结构身份固定理解为：

- 基础骨干仍是标准 `U-Net family` 编码器-解码器主干。
- 注意力门只承担 skip feature 过滤职责，而不是替代整个 decoder 或引入新的主分支。
- gate 的输入固定来自 encoder skip feature `x_l` 和更粗尺度 decoder/gating feature `g`。
- 最终输出必须回收到当前工程的单通道二分类 logits 头和统一评估链。

当前文件把下面这些对象全部视为 `Attention U-Net` 结果解释的一部分，而不是隐藏默认值：

- `gate_levels`
- `gating_source`
- `gate_inter_channels`
- `skip_channels`
- `decoder_channels_fixed`
- `encoder_pretrained`
- `extra_attention_block`
- `extra_supervision`

### 3.4 当前 `v1` 的默认正式裁决

当前 `Attention U-Net v1` 的正式裁决固定为：

- 保留 `vanilla U-Net backbone + additive attention gate on skip connections` 这条方法主干。
- 默认使用单输出二分类分割头，不引入额外监督头、边界分支或实例分离支路。
- gate 接入位置允许作为结构级配置项存在，但必须显式暴露并写入配置与记录字段。
- 不允许通过扩大 encoder/decoder 宽度、引入预训练 encoder 或追加其它注意力模块来伪装 `Attention U-Net` 收益。
- 原文 `3D CT` 背景和其训练细节只作为来源说明，不纳入当前 `v1` 主表公平复现协议。

### 3.5 核心公式与方法身份锚点

当前文件把下面三条式子视为 `Attention U-Net` 的身份锚点，而不是可选注释：

```text
q_att^l = ψ^T(σ1(W_x^T x_i^l + W_g^T g_i + b_g)) + b_ψ
```

```text
α_i^l = σ2(q_att^l(x_i^l, g_i; Θ_att))
```

```text
x̂_i,c^l = x_i,c^l · α_i^l
```

它们在本文件里的作用是锁定：

- `Attention U-Net` 的核心改进来自 additive attention gate 对 skip feature 的筛选。
- gate 只改变 skip fusion 的信息选择，不应顺手扩大基础网络容量。
- 只要实现已经失去“skip feature filtering by coarse gating signal”这一本体，即使方法名写成 `AttUNet`，也不再属于本文件意义上的 `Attention U-Net`。

### 3.6 当前文件不允许用什么替代正式定义

当前明确不允许把下面这些情况写成“`Attention U-Net` 适配已完成”：

- 只写方法名，不写 gate 接入层级、gating source 和通道配置。
- 用“额外注意力模块堆叠 + 更宽 decoder”的变体替代原始 gate 结构。
- 直接采用第三方仓库默认训练超参并声称公平复现。
- 把“加入 gate 后 decoder 更大、encoder 换预训练、附带多头监督”的增强结果当成当前主表默认起点。

---

## 4. 阶段门控表达式

### 4.1 当前文件直接继承哪些冻结项

本文件直接继承并不得擅自改动的上位规则如下：

- 主数据集：`GlaS`
- 正式 split：`train68 / val17 / TestA60 / TestB20`
- 标签口径：`mask > 0`
- 输入通道：`RGB`
- 输入尺寸：`512 x 512`
- 归一化：`ImageNet mean/std`
- 主增强包：沿用当前主线已冻结版本
- 主损失：`L_seg = L_BCE + L_Dice`
- 优化协议：`AdamW + lr 1e-3 + weight_decay 1e-4 + ReduceLROnPlateau + epoch_max 120 + early_stopping 20 + AMP on`
- 评估链：`logits -> sigmoid -> threshold -> binary mask -> connected components -> metrics`
- 主指标优先级：`F1 / Object Dice / Object Hausdorff`
- 补充指标：`Dice / IoU / HD95 / Boundary F1`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `postprocess_version = none_in_v1`
- `tta_version = none_in_v1`
- 正式种子集合：`3407 / 1234 / 2025`

### 4.2 当前文件继承的 `current_mainline`

当前文件不重新定义主线，而是严格继承 `07_Distance` 的正式 handoff：

```text
current_mainline = (distance_decision_level == keep) ? distance_kept_base : distance_input_base
```

这意味着：

- `Attention U-Net` 的比较对象固定是唯一合法的 `current_mainline`。
- 当前文件不能通过适配外部方法反向重开主线结构、训练口径或评估口径。
- 每个正式 `Attention U-Net` run 都必须能追溯到同一个 `current_mainline` 字段值。

### 4.3 当前文件禁止重新打开的内容

本文件禁止借“适配 `Attention U-Net`”名义重新打开：

- `GlaS` split、输入尺寸、归一化和标签口径。
- 主增强包、主损失、optimizer、scheduler、训练预算。
- `best checkpoint` 选择器、阈值来源、后处理默认口径和 TTA 默认口径。
- 对象级指标定义和 `TestA / TestB` 分开汇报规则。
- `current_mainline` 的结构组成和来源定义。

---

## 5. `Attention U-Net` 规则卡片

下面所有核心规则都写成最终协议格式。后面写代码、跑实验、汇总表格时，只允许把这些规则实现出来，不允许擅自补新的隐含规则。

### 5.1 比较身份与路线角色规则

- 当前结论：`Attention U-Net` 固定作为首批核心外部对比之一，代表“在 `U-Net` skip connection 上加入 additive attention gate”的路线。
- 规则类型：`路线冻结规则 + 外部基线角色规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`
- 核心公式或定义参考：`model_code = AttUNet`
- 采用原因：它能回答“仅靠 gate 强化 skip 选择，是否足以与当前主线形成高强度公平对照”。
- 不采用的相邻方案：不把 `Attention U-Net` 降级成随手补的普通 baseline；不把它和任务内 gland-specific direct comparison 混成一类证据。
- 代码落点：crc_gland_segmentation_project/external/attention_unet/*、crc_gland_segmentation_project/configs/external/attunet_v1.yaml
- 运行记录字段：`model_code`、`model_name`、`model_version`、`external_group`
- 验收方式：检查 `Attention U-Net` 已作为首批核心外部对比进入外部主表准备层。

### 5.2 统一协议继承规则

- 当前结论：`Attention U-Net` 必须完整继承统一数据、训练、评估和结果记录协议，首轮默认只允许替换网络结构本身。
- 规则类型：`公平比较规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 核心公式或定义参考：`attunet_external_run = unified_data_proto + unified_train_proto + unified_eval_proto + attunet_architecture_only`
- 采用原因：当前阶段比较的是结构路线，不是第三方仓库默认训练流程。
- 不采用的相邻方案：不采用原仓默认器官分割训练流程、默认损失或默认测试链直接横比当前腺体任务结果。
- 代码落点：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/src/eval/run_eval.py
- 运行记录字段：`data_proto_version`、`train_proto_version`、`eval_proto_version`、`eval_cast_policy`、`threshold_source`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`、`fairness_adjustment`
- 验收方式：检查 `best_selector`、`threshold_source`、`TestA / TestB` 和对象级指标链都未被改写。

### 5.3 gate 结构身份规则

- 当前结论：`Attention U-Net` 的正式身份只来自 `additive attention gate on skip connections`，不得扩展成其它注意力堆叠模型。
- 规则类型：`结构身份规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`
- 核心公式或定义参考：`q_att^l -> α_i^l -> x̂_i,c^l = x_i,c^l · α_i^l`
- 采用原因：attention gate 是该方法区别于 plain `U-Net` 的核心结构增量，也是唯一应被解释为方法收益的部分。
- 不采用的相邻方案：不允许只保留方法名却丢掉 gate；不允许把 self-attention、channel attention、transformer block 等额外结构混入同一身份。
- 代码落点：crc_gland_segmentation_project/external/attention_unet/*
- 运行记录字段：`gate_type`、`gate_levels`、`gating_source`、`gate_inter_channels`
- 验收方式：检查实现中确实存在基于 coarse feature 的 skip gate，而不是普通 concat 或其它注意力替代。

### 5.4 gate 层级与通道记录规则

- 当前结论：gate 接入层级、skip 通道和中间压缩通道属于一级结构变量，必须显式记录。
- 规则类型：`结构冻结规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`
- 核心公式或定义参考：`gate_profile = gate_levels + skip_channels + gate_inter_channels + gating_source`
- 采用原因：只要 gate 位置或通道压缩规则不清楚，就无法判断收益来自 gate 还是来自容量变化。
- 不采用的相邻方案：不允许把 gate 放置层级写成“默认全部”却不记录；不允许通道压缩藏在代码默认值中。
- 代码落点：crc_gland_segmentation_project/configs/external/attunet_v1.yaml、crc_gland_segmentation_project/external/attention_unet/*
- 运行记录字段：`gate_levels`、`skip_channels`、`gate_inter_channels`、`gating_source`
- 验收方式：检查正式 run 的配置和 run_meta.yaml 都能还原 gate 放置和通道设置。

### 5.5 基础 `U-Net` 宽度不扩张规则

- 当前结论：加入 gate 后，不允许偷偷扩大基础 encoder 或 decoder 宽度作为隐性收益来源。
- 规则类型：`公平边界规则 + 容量控制规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 核心公式或定义参考：`attunet_v1 = vanilla_unet_backbone + skip_attention_gates_only + single_output_head + unchanged_decoder_width`
- 采用原因：当前要比较的是 gate 筛选效果，而不是更大基础网络的效果。
- 不采用的相邻方案：不允许换更宽 decoder、更深 encoder、额外 context block 后仍笼统记作 `Attention U-Net`。
- 代码落点：crc_gland_segmentation_project/configs/external/attunet_v1.yaml、run_meta.yaml
- 运行记录字段：`encoder_channels`、`decoder_channels`、`decoder_channels_fixed`、`base_unet_changed`
- 验收方式：检查加入 gate 前后的基础通道设置一致，且容量变化被明确禁止或显式记录。

### 5.6 预训练与额外监督边界规则

- 当前结论：`encoder_pretrained`、`extra_attention_block` 和 `extra_supervision` 不属于 `Attention U-Net v1` 的默认公平主表协议。
- 规则类型：`公平边界规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 核心公式或定义参考：`paper_boosted_result = stronger_backbone OR extra_attention OR extra_supervision OR non_unified_test_pipeline`
- 采用原因：这些设置会把 gate 收益和其它增强收益混在一起，破坏当前首版公平比较。
- 不采用的相邻方案：不允许把带预训练 encoder、多输出监督或附加注意力模块的变体直接与当前主线横比。
- 代码落点：run_meta.yaml、crc_gland_segmentation_project/reports/tables/*.csv
- 运行记录字段：`encoder_pretrained`、`extra_attention_block`、`extra_supervision`、`paper_setting_gap`
- 验收方式：检查凡是带这些增强设置的结果，都被降级为说明项、`†` 或 `*`，而不是主表公平复现值。

### 5.7 运行、命名与三 seed 补证规则

- 当前结论：`Attention U-Net` 首轮固定先跑 `seed3407`，满足竞争条件时必须补齐 `3407 / 1234 / 2025`。
- 规则类型：`成本控制规则 + 稳定性补证规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- 核心公式或定义参考：`need_three_seed = (gap_to_mainline <= 1.5pt) OR (rank == 2)`
- 固定命名：`H1_AttUNet_GlaS_v1_seed3407`、`H1_AttUNet_GlaS_v1_seed1234`、`H1_AttUNet_GlaS_v1_seed2025`
- 采用原因：先用单 seed 控制成本，再为关键竞争者补足稳定性证据。
- 不采用的相邻方案：不允许直接跳到额外重复；不允许只跑一次就把 screening 结果写成最终正式结论。
- 代码落点：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/scripts/compare_runs.py
- 运行记录字段：`run_name`、`train_seed`、`need_three_seed_followup`、`aggregation`
- 验收方式：检查命名统一，且补跑触发完全遵守母协议。

### 5.8 主表资格与来源边界规则

- 当前结论：只有在结构身份、统一协议、最小必要差异和来源标记都清楚时，`Attention U-Net` 才具备进入外部主表的资格。
- 规则类型：`结果表资格规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`
- 核心公式或定义参考：`direct_comparison_eligible = same_benchmark AND same_split AND same_metric_protocol AND no_major_test_gap`
- 采用原因：主表承担正文结论，必须区分统一协议复现值、引文值和特殊流程值。
- 不采用的相邻方案：不允许主表里混写 `reproduced`、`†` 和 `*` 却不解释来源边界。
- 代码落点：crc_gland_segmentation_project/scripts/compare_runs.py、crc_gland_segmentation_project/reports/tables/*.csv
- 运行记录字段：`result_source_type`、`direct_comparison_eligible`、`quoted_from_paper`
- 验收方式：检查 `Attention U-Net` 结果能够明确写入来源类型和直比资格。

---

## 6. 代码实现约束

### 6.1 本文件必须对齐的工程位置

- crc_gland_segmentation_project/external/attention_unet/*
- crc_gland_segmentation_project/configs/external/attunet_v1.yaml
- `crc_gland_segmentation_project/scripts/train.py`
- crc_gland_segmentation_project/scripts/compare_runs.py
- crc_gland_segmentation_project/scripts/summarize_stage.py
- crc_gland_segmentation_project/src/eval/run_eval.py
- crc_gland_segmentation_project/src/eval/checkpoint_selector.py
- crc_gland_segmentation_project/src/metrics/object_metrics.py
- crc_gland_segmentation_project/src/metrics/boundary_metrics.py
- crc_gland_segmentation_project/reports/tables/*
- crc_gland_segmentation_project/reports/stage_reports/external_reproduction_note.md

### 6.2 本文件禁止改动的工程对象

- `crc_gland_segmentation_project/splits/glas/*.csv`
- `crc_gland_segmentation_project/configs/data/glas.yaml` 中已冻结的数据协议
- `current_mainline` 的结构和正式配置
- 已冻结的 `train_proto_v1 / eval_proto_v1`
- `TestA / TestB` 分开汇报的评估导出逻辑
- 对象级指标实现和来源标记总规则

### 6.3 `Attention U-Net` 代码落地底线

本文件对应的实现必须同时满足：

- `Attention U-Net` 必须回收到统一训练入口和统一评估导出接口。
- 同一个 `run_name` 只能对应一套固定的 `gate_levels / gating_source / gate_inter_channels / encoder_channels / decoder_channels` 组合。
- `best_selector`、`threshold_source`、后处理与 TTA 状态必须写入 run_meta.yaml。
- gate 层级、通道与基础 `U-Net` 宽度必须从配置层显式暴露。
- 聚合脚本必须能区分单 seed screening 结果、三 seed 聚合结果、原文引用值和特殊流程值。

### 6.4 本文件必须新增的记录字段

`Attention U-Net` 正式 run 至少必须记录：

- `run_name`
- `stage_code`
- `model_code`
- `model_name`
- `model_version`
- `implementation_source`
- `adaptation_note`
- `gate_type`
- `gate_levels`
- `gating_source`
- `skip_channels`
- `gate_inter_channels`
- `encoder_channels`
- `decoder_channels`
- `decoder_channels_fixed`
- `base_unet_changed`
- `encoder_pretrained`
- `extra_attention_block`
- `extra_supervision`
- `paper_setting_gap`
- `fairness_adjustment`
- `data_proto_version`
- `train_proto_version`
- `eval_proto_version`
- `train_seed`
- `best_selector`
- `eval_cast_policy`
- `threshold`
- `threshold_source`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `has_postprocess`
- `has_tta`
- `has_special_test_setting`
- `result_source_type`
- `direct_comparison_eligible`
- `need_three_seed_followup`

### 6.5 代码落地接口

#### 6.5.1 `Attention U-Net` 构建与前向适配入口

- 代码文件：crc_gland_segmentation_project/external/attention_unet/*
- 入口类/函数：`build_attunet(cfg)`、`adapt_attunet_forward(model, x)` 或等价正式入口
- 输入：图像张量 `B x 3 x 512 x 512`，结构配置 `gate_levels`、`gating_source`、`gate_inter_channels`、`encoder_channels`、`decoder_channels`
- 输出：单通道 logits `B x 1 x 512 x 512`
- `dtype`：图像 `float32` 或 AMP 下 `float16 / bfloat16`；logits 为 `float32`
- 前置断言：`model_code = AttUNet`；gate 放置层级和通道均已显式声明；输出尺寸与统一评估链兼容；基础 `U-Net` 宽度未被私自扩张
- 运行产物：可实例化的 `Attention U-Net` 模型对象和完整结构配置快照

#### 6.5.2 统一训练与公平协议校验入口

- 代码文件：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/external/attention_unet/*
- 入口类/函数：`run_external_screening(cfg)`、`validate_external_fairness(cfg)` 或等价正式入口
- 输入：图像张量 `B x 3 x 512 x 512`，mask 张量 `B x 1 x 512 x 512`，外部方法配置 crc_gland_segmentation_project/configs/external/attunet_v1.yaml，公平协议字段 `data_proto_version`、`train_proto_version`、`eval_proto_version`、`best_selector`、`eval_cast_policy`、`threshold_source`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`
- 输出：crc_gland_segmentation_project/experiments/H1_AttUNet_GlaS_v1_seed3407/、config.yaml、run_meta.yaml、train_log.csv、val_metrics.csv、testA_metrics.csv、testB_metrics.csv
- `dtype`：图像 `float32` 或 AMP 浮点；mask `float32`；二值预测 `uint8` 或 `bool`
- 前置断言：`current_mainline` 已唯一确定；`best_selector = val_objdice_max`；`eval_cast_policy = logits/probabilities must be kept or cast to float32 before thresholding`；`threshold_source = val17`；`boundary_metric_width = 3 px`；`boundary_metric_impl = skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`；`connected_components_impl = scipy.ndimage.label`；`connected_components_connectivity = 8`；若存在与论文设置不一致之处，则 `paper_setting_gap` 与 `fairness_adjustment` 必须非空；`has_tta = false` 且 `has_postprocess = false` 作为 `v1` 默认公平口径
- 运行产物：正式 run 目录、`Attention U-Net` 适配记录和 reproduction note 中对应方法条目

#### 6.5.3 `Attention U-Net` 结果汇总与来源边界入口

- 代码文件：crc_gland_segmentation_project/scripts/compare_runs.py、crc_gland_segmentation_project/scripts/summarize_stage.py
- 入口类/函数：`build_external_main_table()`、`summarize_attunet_external_run()` 或等价正式入口
- 输入：`Attention U-Net` 各 run 的 run_meta.yaml、val_metrics.csv、testA_metrics.csv、testB_metrics.csv 和来源标记表
- 输出：external_main_table_draft.csv、quoted_vs_reproduced_rule_note.md、attunet_reproduction_note.md 或等价方法级适配说明
- `dtype`：指标字段 `float`；标记字段 `string / bool`；排名字段 `int`
- 前置断言：`TestA / TestB` 指标已分开导出；`result_source_type` 与 `direct_comparison_eligible` 已显式写入；若结果来自论文增强设置或变体结构，则不得标为 `reproduced`
- 运行产物：`Attention U-Net` 主表草稿条目和方法级来源边界说明

---

## 7. 结果验收与下游 handoff

### 7.1 最低交付物

本文件过线前，至少必须形成：

1. `H1_AttUNet_GlaS_v1_seed3407/`
2. 对应完整的 config.yaml
3. 对应完整的 run_meta.yaml
4. 对应完整的 train_log.csv
5. 对应完整的 val_metrics.csv
6. 对应完整的 testA_metrics.csv
7. 对应完整的 testB_metrics.csv
8. `Attention U-Net` 的方法级适配说明
9. 可进入 external_main_table_draft.csv 的正式条目

### 7.2 通过线

只有同时满足下面条件，本文件才视为闭环：

- `Attention U-Net` 的结构身份已经写成硬规则。
- gate 层级、gating source、通道设置和基础 `U-Net` 宽度边界已经可追溯。
- 原文 `3D CT` 设置与当前统一主表协议的边界已经写清。
- 代码入口、I/O、前置断言和运行产物已经细化到可直接指导实现。
- `seed3407` 首轮结果已经形成，且必要时已按统一规则补三次重复。
- 结果能够明确写入 `result_source_type` 与 `direct_comparison_eligible`。

### 7.3 交接给下游阶段的资产

当前文件向下游至少交接：

- `Attention U-Net` 的正式 run 目录与方法级适配说明。
- `Attention U-Net` 的结构身份字段链和公平差异字段链。
- `result_source_type`、`direct_comparison_eligible`、`need_three_seed_followup` 的明确结论。
- 外部主表草稿中 `Attention U-Net` 的正式条目。

这些资产后续分别承担：

1. 对 `09_CRAG验证`：作为第一批外部层来源边界的上游说明。
2. 对 `10_结果汇总`：作为外部主表层的正式输入。
3. 对 `11_总验收与止损`：作为 `Attention U-Net` 是否真正完成、是否需要补证和是否具备正文主表资格的证据包。

---

## 8. 回退条件

### 8.1 独立回退触发条件

下面任意一条成立，都必须回退修订本文件，而不是继续进入下游细则：

- `Attention U-Net` 的结构本体仍然说不清，只剩方法名描述。
- `gate_levels / gating_source / gate_inter_channels / decoder_channels` 仍可藏在默认值中而不记录。
- 基础 `U-Net` 宽度、额外注意力模块或额外监督边界仍然模糊。
- 代码接口还不能直接指导实现与结果汇总。
- `result_source_type`、`direct_comparison_eligible` 或 `paper_setting_gap` 仍无法与正式结果一一对应。
- 主表草稿、运行记录和方法说明对同一 `Attention U-Net` 结果的来源身份判断不一致。

### 8.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查 `current_mainline` 和统一数据训练评估协议是否被破坏。
2. 再检查 gate 层级、通道、基础 `U-Net` 宽度和结构边界是否完整记录。
3. 再检查额外注意力、额外监督和论文设置差异边界是否写清。
4. 最后检查主表资格、三 seed 状态和下游 handoff 字段是否一致。

### 8.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已写回方法级适配说明或阶段总结。
- run_meta.yaml、主表草稿和文字说明对 `Attention U-Net` 的来源身份重新对齐。
- 当前文件重新满足第 `5-7` 节的规则、交付物和 handoff 要求。

---

## 9. 冲突裁决记录

- 冲突对象：当前文件旧版内容与 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md` 对方法级 formal protocol 强度的要求之间存在明显不一致。
- 冲突来源：旧版虽然已有方法定位、结构变量和结果要求，但仍缺少前置依赖留痕、显式的上游 / 同层 / 下游、与同批强模板一致的回退与 diagnostics 收尾，以及更强的下游 handoff 表达。
- 裁决结论：本轮将当前文件正式升级为 `文件角色与执行边界 -> 本轮重写直接依赖的前置文件 -> 方法定位与唯一变量 -> 上游继承 -> 规则卡片 -> 代码实现约束 -> 结果验收与 handoff -> 回退条件 -> 冲突裁决记录 -> 文件质量自检 -> Diagnostics 闭环 -> 一句话版本` 的完整方法协议结构。
- 裁决理由：`Attention U-Net` 是首批三类核心外部对比之一，也是最容易因为 gate 位置、通道设置、基础骨干宽度和额外注意力变体而被误读的外部方法；如果不把这些边界压成硬协议，后续主表中的 `Attention U-Net` 结果无法证明是在做公平结构比较。
- 对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- 是否需要回流修订：需要；后续阶段验收文件应继承这里固定的结构身份粒度、来源边界与下游 handoff 字段表达。

---

## 10. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文。
- [x] 已继续补读 `02_路线与投稿`、`03_文献证据`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`，而不是停在总览层。
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论。
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明这些文件为什么与 `Attention U-Net` 方法协议直接相关。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 和同层强模板 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md` 的对照，确认前部结构、回退与独立 `Diagnostics 闭环` 没有弱化。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md` 的下游消费对照，确认 handoff 资产与来源字段足以被直接读取。
- [x] 当前版本按整篇重写执行，不是对旧稿追加零散补丁说明。
- [x] 已写清当前文件负责什么、不负责什么，以及为什么 `Attention U-Net` 需要独立方法协议。
- [x] 已把 `attunet_external_run`、gate 公式、`gate_profile`、`attunet_v1`、`paper_boosted_result`、`need_three_seed` 和 `direct_comparison_eligible` 写成正式定义或实现级解释。
- [x] 已写清 `Attention U-Net` 的结构身份、gate 放置边界、基础 `U-Net` 宽度边界、额外注意力边界和论文设置边界，并达到“可直接翻译代码 + 可直接写入论文”的最低深度。
- [x] 已写清为什么不采用相邻方案，包括不让更宽 decoder、更强预训练、额外注意力或额外监督设置偷渡进当前首版主表协议。
- [x] 已把 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 明确写入 `Attention U-Net` 的运行字段、输入配置和前置断言，而不是只抽象成 `eval_proto_version`。
- [x] 已写清代码落点、运行记录字段、最低交付物和下游 handoff 资产。
- [x] 代码落地对象已经细化到构建入口、训练入口、结果汇总入口、I/O、配置字段和运行产物。
- [x] 已写清验收方式与独立 `回退条件`，没有把回退要求藏进通过线或总结句里顺带带过。
- [x] 已补写 `冲突裁决记录`，说明旧口径与同批强模板如何统一、影响哪些文件以及后续如何回流修订。
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、核心定义、规则卡片、接口、回退、handoff 和收尾闭环。
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”。
- [x] 当前文件在落盘后继续执行回读与 diagnostics 复核，正文写作不会替代闭环动作。
- [x] 当前文件已经达到“可直接指导 `Attention U-Net` 接入、结果分层、主表写作和下游 handoff”的最低强度。

---

## 11. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成。
- 复核范围：至少覆盖标题层级、列表结构、字段命名一致性、`上游 / 同层 / 下游` 显式落点、核心公式书写、独立 `回退条件`、`文件质量自检` 和独立 `Diagnostics 闭环` 是否完整。
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核。
- 对照要求：本节保持与 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 和 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md` 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话。

---

## 12. 一句话版本

> `Attention U-Net` 在当前项目中已经被正式固定为“在 `U-Net` skip connection 上加入 additive attention gate”的首批核心外部基线；它进入主表时只能在统一数据、训练、评估协议下做最小结构适配，并且必须把 gate 层级、gating source、通道配置、基础 `U-Net` 宽度边界、额外注意力/监督边界和结果来源边界全部显式记录，否则不能作为公平复现值进入正式外部主表。
