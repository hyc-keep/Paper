# UNetPP适配方案

这份文件不是 `UNet++` 的泛化介绍，也不是“先接进工程再补边界”的实现备忘录。

它的正式职责只有一个：

> 把 `UNet++` 在 `08_外部对比` 中的结构身份、统一协议继承方式、最小必要适配、正式运行链、主表资格、下游交接方式和独立回退条件一次写死，让后续实现、运行、汇总和论文写作都只能按同一口径执行。

从现在开始，`UNet++` 进入 `08_外部对比` 主表准备层时，必须同时受 `结直肠腺体分割_plan_优化版\01_实验执行\08_外部对比\00_阶段总协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md` 约束；如果当前文件和上位协议冲突，以上位协议为准并回改本文件。

---

## 1. 文件角色与执行边界

### 1.1 本文件要固定什么

本文件固定的不是“把一个常见 `U-Net family` 模型跑起来”，而是把 `UNet++` 在当前项目中的正式比较身份压成可执行协议：

1. 它是 `08_外部对比` 首批核心外部方法之一。
2. 它代表“通过 nested dense skip pathways 缩小 encoder-decoder semantic gap”的结构路线。
3. 它只允许在统一数据、训练、评估和结果记录协议不动的前提下替换结构本体。
4. 它必须把 `deep supervision`、`accurate mode`、`fast mode`、`pruning`、编码器替换和预训练状态写成正式裁决。
5. 它必须把正式运行顺序、命名、结果来源标记、主表资格和下游 handoff 规则写死。
6. 它必须有独立 `回退条件`、独立 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 1.2 它在外部对比执行链中的角色

本文件对应 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 中 `External_core` 的 `UNet++` 方法级执行协议，并直接服务以下阶段门控：

- `core_external_runs_complete`
- `source_boundary_ready`
- `external_table_ready`
- `handoff_ready`

原因是 `UNet++` 很容易出现“方法名正确、结果也有，但结构边界和公平边界都没写死”的伪完成状态。只要这一层没有先固定，后面的 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`、`09_CRAG验证`、`10_结果汇总` 和 `11_总验收与止损` 就都会被迫重新解释同一个方法到底代表什么。

### 1.3 为什么必须现在写死

当前阶段已经满足下面三个前提：

- `current_mainline` 已由 `07_Distance` 唯一化。
- `UNet++` 已被路线层锁定为首批核心外部对比之一。
- `08_外部对比` 当前要交付的是“可进入主表准备层的公平复现协议”，不是方法介绍。

因此，当前文件必须提前把 `UNet++` 的结构本体、允许差异、最小接入式和结果资格写成硬规则，而不能把关键判断推迟到代码接入或表格汇总时临场决定。

---

## 2. 前置文件依赖

### 2.1 `00_总览与规范`

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求处理执行层 `md` 时先重读总规范，再做整篇重写，不能只做局部补丁。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把 `crc_gland_segmentation_project/external/`、`crc_gland_segmentation_project/configs/`、`crc_gland_segmentation_project/scripts/`、`crc_gland_segmentation_project/reports/` 和正式产物路径写成可执行接口。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供统一数据、训练、评估和版本边界，防止 `UNet++` 接入时单独漂移。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：要求 `run_name`、`config_version`、`train_seed`、`aggregation` 和 run_meta.yaml 字段可回查。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：冻结 `best_selector = val_objdice_max`、`threshold_source = val17`、对象级主指标和 `TestA / TestB` 分开汇报规则。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求正文落到具体代码入口、I/O、依赖配置、前置断言和运行产物。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求规则卡片、代码落地接口、运行记录字段和验收方式齐全。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求独立 `回退条件`、独立 `Diagnostics 闭环`，并要求与同层强模板做收尾强度对照。

### 2.2 路线依据

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定 `UNet++` 是首批核心外部对比，不是新主线，也不是可随意扩写的增强方法。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：锁定 `08_外部对比` 处在 `07_Distance` 之后、`09_CRAG验证` 之前，且首批名单包含 `UNet++`。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：要求外部层结果既服务投稿主表，又必须清楚区分公平复现值、引用值和特殊设置值。

### 2.3 文献依据

- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/04_UNet++.md`：提供 nested dense skip pathways、deep supervision、accurate mode、fast mode、pruning 和核心公式来源。
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/03_DeepLabV3+.md`：作为同层强方法对照，帮助校准当前文件的协议颗粒度与工程深度。
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/01_Attention_U-Net.md`：作为同层 `U-Net family` 对照，帮助明确 `UNet++` 不应混入 attention gate 身份。
- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/06_nnU-Net.md`、`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/07_TransUNet.md`、`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/08_Swin-Unet.md`：提供增强外部候选的边界参照，防止把 `UNet++` 写成增强外部入口。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`、`结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/07_TA-Net.md`、12_DEA-Net.md：提供 task-specific 直接对照写作边界，提醒当前文件只负责通用核心外部方法身份。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`：给出 `current_mainline` 的唯一合法来源，是 `UNet++` 比较起点，不允许当前文件自行换基线。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`：定义 `UNet++` 属于 `External_core`，并把 `core_external_runs_complete` 与本文件是否写清方法协议直接绑定。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`：给出 `external_run_fair`、`allowed_gap`、`need_three_seed`、`direct_comparison_eligible` 等统一边界，是本文件的直接上位协议。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`：当前同层强模板，用于对照 `文件质量自检`、`Diagnostics 闭环` 和代码接口颗粒度是否缩水。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/04_AttUNet适配方案.md`：当前同层相对较弱文件，反向提醒本文件不能退回成“轻说明文”。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/05_增强对比进入条件.md`：规定在首批核心外部闭环前不得扩展增强外部，限制 `UNet++` 不得越权承担增强对比入口。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`：要求 `UNet++` 结果显式标记 `reproduced / † / *`，并写清直比资格。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`：要求 `UNet++` 的适配说明、结果产物、来源边界和补跑状态进入阶段最低交付物。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`：只允许资源允许时把首批外部中的最强方法下放到 `CRAG`，因此本文件必须先固定 `UNet++` 的结构身份和结果身份。
- `结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`：直接消费 `run_name`、`result_source_type`、`direct_comparison_eligible`、`aggregation` 等字段，本文件必须先把这些字段写死。
- `结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`：读取 `UNet++` 是公平复现值、引用值还是特殊流程值，并据此做最终放行或止损裁决。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 本文件继承的当前主线定义

本文件不重新定义主模型，只继承 `07_Distance` 已唯一化的正式主线：

```text
current_mainline = (distance_decision_level == keep) ? distance_kept_base : distance_input_base
```

这意味着：

- `UNet++` 只能与唯一的 `current_mainline` 比，不能和多个候选主线混比。
- 当前文件只能回答“nested skip 结构路线相对当前主线的表现”，不能借机重开主线选择。
- 任何正式 `UNet++` run 都必须能追溯到同一个 `current_mainline` 字段值。

### 3.2 本文件继承的统一公平协议

`UNet++` 的正式运行必须完整继承：

```text
external_run_fair = unified_data_proto + unified_train_proto + unified_eval_proto + documented_minimal_gap_only
```

同时保留：

```text
allowed_gap = minimal_necessary_gap(external_architecture)
```

这两条式子的含义是：

- 允许的只有“结构本体接入当前框架不可避免的最小差异”。
- 任何训练、评估、阈值、后处理、TTA 或 checkpoint 选择器的漂移，都不能伪装成 `UNet++` 结构收益。
- 一切额外设置都必须被记录为 `paper_setting_gap` 或 `fairness_adjustment`，而不是埋在实现默认值中。

### 3.3 `UNet++` 在当前项目中的正式方法身份

`UNet++` 在当前项目中固定作为首批核心外部方法中的“更强 U 型密集跳连结构”代表。它要回答的问题固定为：

> 在统一数据、统一训练、统一评估协议全部不动的前提下，只通过 nested dense skip pathways 这一结构改造，是否足以形成有解释力的外部比较结果。

因此，本文件不把 `UNet++` 写成：

- attention 方法
- Transformer 方法
- auto-configure 方法
- gland-specific 方法
- 任意 encoder 替换壳

### 3.4 `UNet++` 的结构本体定义

当前文件把下面这条文献公式视为 `UNet++` 的结构身份锚点，而不是可选注释：

```text
x_{i,j} = H(x_{i-1,j}),               j = 0
x_{i,j} = H([[x_{i,k}]_{k=0}^{j-1}, U(x_{i+1,j-1})]),   j > 0
```

它在本文件里的作用是锁定：

- `UNet++` 的核心改进来自 nested dense skip pathways。
- 该结构通过多级跳连缩小 encoder-decoder semantic gap，而不是通过额外监督头或特殊推理策略获得身份。
- 只要实现已经失去上述 nested skip 关系，即使方法名写成 `UnetPlusPlus`，也不再属于本文件意义上的 `UNet++`。

### 3.5 本文件唯一变量

本文件唯一允许处理的变量固定为：

```text
unetpp_external_run = unified_protocol + unetpp_nested_skip_architecture + minimal_framework_adaptation
```

其中：

- `unified_protocol` 指统一数据、训练、评估与结果记录协议。
- `unetpp_nested_skip_architecture` 指 `UNet++` 的 nested dense skip 结构本体。
- `minimal_framework_adaptation` 指接入当前工程所必需的最小输入输出与配置适配。

### 3.6 `UNet++ v1` 的正式裁决

当前 `v1` 主表协议固定裁决为：

```text
unetpp_v1 = nested_skip_only + single_output_head
```

它的固定含义是：

- `v1` 主表协议只保留 nested skip 这一结构本体。
- `v1` 默认使用 `deep_supervision = false` 的单输出版本。
- `v1` 不把 `accurate mode`、`fast mode`、`pruning` 和多分支输出平均纳入统一协议主表。
- `v1` 不把 encoder 替换或更强外部预训练伪装成 `UNet++` 本体收益。

---

## 4. 阶段门控表达式

当前文件的正式执行链固定为：

```text
identity_check -> build_unetpp_v1 -> seed3407_screening -> need_three_seed_followup -> source_tag_and_table_entry
```

### 4.1 节点一：`identity_check`

这个节点必须同时确认：

1. 实现仍然保留 nested dense skip 关系，而不是退化为 plain `U-Net` 或任意 encoder 替换壳。
2. `deep_supervision`、`accurate_mode`、`fast_mode`、`pruning`、`encoder_name`、`encoder_pretrained` 的边界已经在配置与记录字段中写死。
3. 当前方法完全继承统一公平协议，没有单独改动 loss、checkpoint selector、阈值来源、后处理或 TTA。

只要这一步不过，后续不允许开跑。

### 4.2 节点二：`build_unetpp_v1`

这个节点把 `UNet++` 压成统一工程中的正式 `v1`：

- `model_code = UNetPP`
- `model_version = v1`
- `deep_supervision = false`
- `output_head_mode = single`
- `encoder_pretrained = false`
- `input_channels = 3`
- `num_classes = 1`

这个节点允许做的只是最小接入，不允许顺手引入：

- 更强 encoder
- 额外监督头
- 多分支平均
- 特殊推理逻辑

### 4.3 节点三：`seed3407_screening`

首轮固定先跑：

```text
H1_UNetPP_GlaS_v1_seed3407
```

这个节点承担的职责只有两件事：

1. 验证 `UNet++ v1` 在统一协议下可以完整训练、验证、测试和导出结果。
2. 形成首个正式可审计结果，供排名、差距和补跑判断使用。

它不承担最终统计结论。

### 4.4 节点四：`need_three_seed_followup`

只有在下面条件成立时，才允许继续补 `seed1234 / seed2025`：

```text
need_three_seed = (gap_to_mainline <= 1.5pt) OR (rank == 2)
```

这一步与 `07_Distance` 主链的成本控制逻辑一致：先用单 seed 控制成本，再为关键竞争者补齐稳定性证据。

### 4.5 节点五：`source_tag_and_table_entry`

这个节点固定完成四件事：

1. 标记当前结果属于 `reproduced / † / *` 中哪一类。
2. 计算 `direct_comparison_eligible`。
3. 生成 `single_seed` 或 `mean +- std` 身份。
4. 将结果写入 external_main_table_draft.csv 的候选层。

只要来源边界没写清，结果就不能进入正式主表准备层。

### 4.6 与阶段总门控的关系

本文件不是孤立说明文，而是 `Gate_H1` 的组成部分之一：

```text
Gate_H1 = current_mainline_ready
          AND fairness_protocol_fixed
          AND core_external_runs_complete
          AND source_boundary_ready
          AND external_table_ready
          AND handoff_ready
```

当前文件直接支撑：

- `core_external_runs_complete`
- `source_boundary_ready`
- `handoff_ready`

因此，只要本文件在结构身份、来源边界或回退条件上含糊，`Gate_H1` 就不允许视为完成。

---

## 5. 规则卡片

### 5.1 方法角色固定规则

- 当前结论：`UNet++` 固定作为首批核心外部方法中的“更强 U 型密集跳连结构”代表。
- 规则类型：`路线冻结规则 + 外部基线角色规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/04_UNet++.md`
- 核心公式或定义参考：`UNetPP_role = stronger_skip_path_u_family_baseline`
- 采用原因：它最适合回答“只通过更强 skip topology，是否就足以逼近或挑战当前主线”。
- 不采用的相邻方案：不把 `UNet++` 改写成 attention、Transformer、gland-specific 或增强外部方法。
- 代码落点：crc_gland_segmentation_project/external/unetpp/*、crc_gland_segmentation_project/configs/external/unetpp_v1.yaml
- 运行记录字段：`external_group`、`model_code`、`model_name`
- 验收方式：检查 `UNetPP` 在主表草稿、适配记录和阶段说明中都被固定归类为 `core_external`。

### 5.2 核心结构保留规则

- 当前结论：`UNet++` 正式适配时必须保留 nested dense skip pathways 这一结构本体。
- 规则类型：`文献直接支持 + 结构冻结规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/04_UNet++.md`
- 核心公式或定义参考：`x_{i,j} = H(x_{i-1,j}), j=0; x_{i,j} = H([[x_{i,k}]_{k=0}^{j-1}, U(x_{i+1,j-1})]), j>0`
- 采用原因：这是 `UNet++` 相比 plain `U-Net` 的核心身份，也是唯一应被解释为主表结构收益的部分。
- 不采用的相邻方案：不把 `UNet++` 简化成 plain `U-Net`；不只保留方法名却丢掉 nested skip 路径。
- 代码落点：crc_gland_segmentation_project/external/unetpp/*
- 运行记录字段：`model_version`、`skip_topology`、`dense_skip_depth`
- 验收方式：检查实现中确实存在多级 nested skip 路径，而不是普通单层 skip。

### 5.3 深监督与模式裁决规则

- 当前结论：`UNet++ v1` 默认使用 `deep_supervision = false` 的单输出版本，不把 `accurate mode`、`fast mode`、`pruning` 和多分支平均纳入正式比较结果。
- 规则类型：`公平边界规则 + 工程冻结规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/04_UNet++.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 核心公式或定义参考：`unetpp_v1 = nested_skip_only + single_output_head`
- 采用原因：deep supervision 和多分支推理会把“只替换结构”扩展成“额外监督策略 + 额外推理策略”，削弱首版公平解释。
- 不采用的相邻方案：不默认启用 multi-head averaging；不把 fast mode 或 pruning 结果直接放入统一协议主表。
- 代码落点：crc_gland_segmentation_project/external/unetpp/*、crc_gland_segmentation_project/configs/external/unetpp_v1.yaml
- 运行记录字段：`deep_supervision`、`output_head_mode`、`accurate_mode`、`fast_mode`、`pruning_mode`、`paper_setting_gap`、`fairness_adjustment`
- 验收方式：检查 run_meta.yaml 中显式记录 `deep_supervision = false`，且正式输出为单一二值分割头。

### 5.4 编码器与预训练边界规则

- 当前结论：`UNet++ v1` 默认保持 plain `U-Net family` 结构身份，不额外引入 backbone 替换或预训练 encoder 作为隐性收益来源。
- 规则类型：`结构边界规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/04_UNet++.md`
- 核心公式或定义参考：原文基础通道规则参考 `k = 32 x 2^i`
- 采用原因：一旦把 `UNet++` 改成带预训练 encoder 的变体，就会把 nested skip 收益和 encoder 收益混在一起。
- 不采用的相邻方案：不采用 `smp.UnetPlusPlus + ResNet34 encoder pretrained` 作为 `v1` 正式协议；不把 encoder 替换伪装成 `UNet++` 本体。
- 代码落点：crc_gland_segmentation_project/configs/external/unetpp_v1.yaml、crc_gland_segmentation_project/external/unetpp/*
- 运行记录字段：`encoder_name`、`encoder_pretrained`、`decoder_channels`、`model_version`
- 验收方式：检查 `encoder_pretrained = false` 或等价记录，且没有额外 backbone 替换。

### 5.5 统一协议继承规则

- 当前结论：`UNet++` 只允许替换结构本身，其余数据、训练、评估与结果记录规则必须与统一公平协议完全对齐。
- 规则类型：`公平比较规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`
- 核心公式或定义参考：`external_run_fair = unified_data_proto + unified_train_proto + unified_eval_proto + documented_minimal_gap_only`
- 采用原因：这样才能把 `UNet++` 的收益解释为结构收益，而不是协议收益。
- 不采用的相邻方案：不直接沿用第三方仓库默认训练口径；不允许单独改 threshold、checkpoint selector、后处理或 TTA。
- 代码落点：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/src/eval/run_eval.py、crc_gland_segmentation_project/src/eval/checkpoint_selector.py
- 运行记录字段：`data_proto_version`、`train_proto_version`、`eval_proto_version`、`best_selector`、`eval_cast_policy`、`threshold_source`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`、`has_postprocess`、`has_tta`
- 验收方式：检查 `UNetPP` run 使用和主线一致的协议版本链。

### 5.6 最小必要差异记录规则

- 当前结论：`UNet++` 必须优先接入成熟实现，但只能做最小协议适配，且所有差异都必须结构化记录。
- 规则类型：`适配冻结规则 + 来源记录规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
- 核心公式或定义参考：`allowed_gap = minimal_necessary_gap(unetpp_impl)`
- 采用原因：`UNet++` 常见实现分叉较多，如果不显式记录，最容易把库默认值混成论文本体。
- 不采用的相邻方案：不允许只写“来自某仓库”而不说明修改点；不允许把真实差异藏在默认参数中。
- 代码落点：external_reproduction_note.md、run_meta.yaml、crc_gland_segmentation_project/reports/tables/*.csv
- 运行记录字段：`implementation_source`、`adaptation_note`、`paper_setting_gap`、`fairness_adjustment`、`input_adapter_changed`、`output_head_changed`、`decoder_config_changed`
- 验收方式：检查每个正式 run 都可追溯到具体实现来源、适配说明和公平修正说明。

### 5.7 命名与输入输出规则

- 当前结论：`UNet++` 正式 run 命名固定为 `H1_UNetPP_GlaS_v1_seed*`，输入输出接口统一成当前框架的单输入单输出分割接口。
- 规则类型：`命名冻结规则 + 工程冻结规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 核心公式或定义参考：`run_name = "H1_UNetPP_GlaS_" + config_version + "_" + seed_tag`
- 采用原因：阶段码、模型短名、协议版本和 seed 必须能被聚合脚本稳定解析。
- 不采用的相邻方案：不采用 `unet++`、`nested_unet` 等多写法；不采用多输出头直接裸露给汇总脚本。
- 代码落点：crc_gland_segmentation_project/configs/external/unetpp_v1.yaml、crc_gland_segmentation_project/scripts/compare_runs.py
- 运行记录字段：`run_name`、`stage_code`、`model_code`、`config_version`、`train_seed`
- 验收方式：检查 run 目录、汇总表和主表草稿均使用统一命名。

### 5.8 补跑与来源资格规则

- 当前结论：`UNet++` 首轮固定先跑 `seed3407`；若与 `current_mainline` 差距 `<= 1.5` 个百分点，或为当前第二强方法，则必须补三次重复；结果必须同时完成来源标记和直比资格判定。
- 规则类型：`成本控制规则 + 稳定性补证规则 + 写作边界规则`
- 适用阶段：`08_外部对比`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`
- 核心公式或定义参考：`need_three_seed = (gap_to_mainline <= 1.5pt) OR (rank == 2)`；`direct_comparison_eligible = same_benchmark AND same_split AND same_metric_protocol AND no_major_test_gap`
- 采用原因：先控制成本，再为关键竞争者补齐稳定性证据，并在进入主表前把来源身份写清。
- 不采用的相邻方案：不只报单个总测试值；不临时为了好看补跑或跳过补跑；不把引用值与复现值混写成同一层主表。
- 代码落点：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/scripts/compare_runs.py、crc_gland_segmentation_project/reports/tables/*.csv
- 运行记录字段：`train_seed`、`need_three_seed_followup`、`aggregation`、`rank_in_external_group`、`result_source_type`、`direct_comparison_eligible`
- 验收方式：检查 `UNetPP` 的单 seed 或三 seed 身份、来源边界和直比资格都可追溯。

---

## 6. 代码落地接口

### 6.1 必须对齐的工程位置

- crc_gland_segmentation_project/external/unetpp/*
- crc_gland_segmentation_project/configs/external/unetpp_v1.yaml
- `crc_gland_segmentation_project/scripts/train.py`
- crc_gland_segmentation_project/scripts/compare_runs.py
- crc_gland_segmentation_project/scripts/summarize_stage.py
- crc_gland_segmentation_project/src/eval/run_eval.py
- crc_gland_segmentation_project/src/eval/checkpoint_selector.py
- crc_gland_segmentation_project/src/metrics/object_metrics.py
- crc_gland_segmentation_project/src/metrics/boundary_metrics.py
- crc_gland_segmentation_project/reports/tables/*
- external_reproduction_note.md

### 6.2 本文件禁止改动的工程对象

- `crc_gland_segmentation_project/splits/glas/*.csv`
- `crc_gland_segmentation_project/configs/data/glas.yaml` 中已冻结的数据协议
- 当前主线模型结构与其正式配置
- 已冻结的 `train_proto_v1 / eval_proto_v1`
- `TestA / TestB` 分开汇报的评估导出逻辑

### 6.3 `UNet++` 构建与前向适配入口

- 代码文件：crc_gland_segmentation_project/external/unetpp/*
- 入口类/函数：`build_unetpp(cfg)`、`adapt_unetpp_forward(model, x)`
- 输入：
  - 图像张量：`B x 3 x 512 x 512`
  - 结构配置：`model_version`、`deep_supervision`、`encoder_name`、`encoder_pretrained`、`decoder_channels`
- 输出：
  - 单通道 logits：`B x 1 x 512 x 512`
- `dtype`：
  - 图像为 `float32` 或 AMP 下 `float16 / bfloat16`
  - logits 为 `float32`
- 依赖配置：`model_code = UNetPP`、`model_version`、`deep_supervision`、`encoder_name`、`encoder_pretrained`、`input_channels = 3`、`num_classes = 1`
- 前置断言：
  - nested skip 结构未被改写成 plain `U-Net`
  - `deep_supervision = false` 时不返回多分支监督头
  - 输出空间尺寸与输入保持一致
- 运行产物：
  - 结构摘要
  - run_meta.yaml 中的结构与适配字段

### 6.4 统一训练与公平协议校验入口

- 代码文件：`crc_gland_segmentation_project/scripts/train.py`、crc_gland_segmentation_project/src/eval/run_eval.py
- 入口类/函数：`validate_external_fairness(cfg)`、`run_external_screening(cfg)`
- 输入：
  - 图像张量：`B x 3 x 512 x 512`
  - mask 张量：`B x 1 x 512 x 512`
  - 外部方法配置：crc_gland_segmentation_project/configs/external/unetpp_v1.yaml
- 公平协议字段：`data_proto_version`、`train_proto_version`、`eval_proto_version`、`best_selector`、`eval_cast_policy`、`threshold_source`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`
- 输出：
  - crc_gland_segmentation_project/experiments/H1_UNetPP_GlaS_v1_seed3407/
  - config.yaml
  - run_meta.yaml
  - train_log.csv
  - val_metrics.csv
  - testA_metrics.csv
  - testB_metrics.csv
- `dtype`：
  - 图像为 `float32` 或 AMP 下 `float16 / bfloat16`
  - mask 为 `float32`
  - 二值预测为 `uint8 / bool`
- 依赖配置：`implementation_source`、`adaptation_note`、`paper_setting_gap`、`fairness_adjustment`、`best_selector`、`threshold_source`
- 前置断言：
  - `current_mainline` 已由 `07_Distance` 正式结论唯一确定
  - `best_selector = val_objdice_max`
  - `threshold_source = val17`
  - `eval_cast_policy = logits/probabilities must be kept or cast to float32 before thresholding`
  - `boundary_metric_width = 3 px`
  - `boundary_metric_impl = skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`
  - `connected_components_impl = scipy.ndimage.label`
  - `connected_components_connectivity = 8`
  - `deep_supervision = false` 已写入配置
  - `has_postprocess = false` 且 `has_tta = false` 作为 `v1` 默认公平口径
- 运行产物：
  - 正式 `UNetPP` run 目录
  - external_reproduction_note.md 中的 `UNetPP` 适配条目

### 6.5 `UNet++` 结果汇总与来源边界入口

- 代码文件：crc_gland_segmentation_project/scripts/compare_runs.py、crc_gland_segmentation_project/scripts/summarize_stage.py
- 入口类/函数：`build_external_main_table()`、`summarize_unetpp_external_run()`
- 输入：
  - run_meta.yaml
  - val_metrics.csv
  - testA_metrics.csv
  - testB_metrics.csv
  - 来源标记字段
  - 排名与补跑判定字段
- 输出：
  - external_main_table_draft.csv
  - quoted_vs_reproduced_rule_note.md
  - unetpp_reproduction_note.md 或等价方法级适配说明
- `dtype`：
  - 指标字段为 `float`
  - 标记字段为 `string / bool`
  - 排名字段为 `int`
- 前置断言：
  - `run_name` 符合 `H1_UNetPP_GlaS_v1_seed*`
  - `TestA / TestB` 已分开导出
  - `reproduced / † / *` 标记已明确
  - `direct_comparison_eligible` 已按统一规则计算
- 运行产物：
  - `UNetPP` 在外部主表中的正式条目
  - 必要时的三 seed 聚合结果

### 6.6 结构化记录字段底线

每个正式 `UNet++` run 至少必须具备以下字段：

- `run_name`
- `stage_code`
- `model_code`
- `model_name`
- `model_version`
- `implementation_source`
- `adaptation_note`
- `paper_setting_gap`
- `fairness_adjustment`
- `skip_topology`
- `dense_skip_depth`
- `deep_supervision`
- `accurate_mode`
- `fast_mode`
- `pruning_mode`
- `input_adapter_changed`
- `output_head_changed`
- `decoder_config_changed`
- `encoder_name`
- `encoder_pretrained`
- `data_proto_version`
- `train_proto_version`
- `eval_proto_version`
- `train_seed`
- `best_selector`
- `eval_cast_policy`
- `threshold_value`
- `threshold_source`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `has_postprocess`
- `has_tta`
- `result_source_type`
- `quoted_from_paper`
- `has_special_test_setting`
- `direct_comparison_eligible`
- `need_three_seed_followup`
- `aggregation`

---

## 7. 结果验收与回退

### 7.1 最低验收产物

本文件过线前，至少必须能提供：

1. `H1_UNetPP_GlaS_v1_seed3407/`
2. 对应完整的 config.yaml
3. 对应完整的 run_meta.yaml
4. 对应完整的 train_log.csv
5. 对应完整的 val_metrics.csv
6. 对应完整的 testA_metrics.csv
7. 对应完整的 testB_metrics.csv
8. external_reproduction_note.md 中对应的 `UNetPP` 条目
9. 能进入 external_main_table_draft.csv 的正式条目

### 7.2 通过线

只有同时满足下面条件，本文件才视为闭环：

- nested skip 结构本体已保留。
- `deep supervision`、`accurate mode`、`fast mode` 和 `pruning` 边界已明确裁决。
- plain `UNet++` 与 encoder 替换变体的边界已写清。
- 统一数据、训练、评估协议未被破坏。
- 实现来源和最小适配差异可追溯。
- `seed3407` 结果已形成，且必要时可按统一规则补三次重复。
- `reproduced / † / *` 与 `direct_comparison_eligible` 边界已明确定义。
- 结果已具备进入外部主表准备层和下游 `09/10/11` 的资格。

### 7.3 回退条件

下面任意一条成立，都必须先回退修订当前文件，而不是继续推进同层或下游文件：

- `UNet++` 实际实现已经退化成普通 `U-Net`、其它 encoder-decoder 变体，或与 nested skip 身份不符。
- `deep_supervision`、`accurate mode`、`fast mode`、`pruning` 或多分支 averaging 的状态没有结构化记录清楚。
- 为了适配第三方实现而偷偷更改训练协议、评估协议、阈值来源或 `best_selector`。
- `UNet++` 结果未按 `TestA / TestB` 分开导出。
- `implementation_source / adaptation_note / paper_setting_gap / fairness_adjustment` 缺失。
- 下游文件仍然需要自己重新解释 `UNet++` 的结构身份、来源边界或主表资格。

### 7.4 固定回退顺序

1. 先检查 `UNet++` 是否仍然保留 nested skip 结构身份。
2. 再检查 `deep supervision`、`accurate mode`、`fast mode`、`pruning` 和输出头是否被正确裁决与记录。
3. 再检查 encoder、预训练状态和适配差异字段是否完整。
4. 再检查统一数据、训练、评估协议是否真的没有漂移。
5. 最后检查结果来源边界、直比资格和下游 handoff 是否一致。

### 7.5 回退后的重新放行条件

- 问题来源已经按固定回退顺序定位并修复。
- 修复动作、影响范围和复验结果已写回 external_reproduction_note.md 或阶段总结。
- run_meta.yaml、external_main_table_draft.csv 和文字结论已经重新对齐。
- 当前文件重新满足第 `4-7` 节的执行链、接口、产物和资格要求。

---

## 8. 冲突裁决记录

- 冲突对象：旧版 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/02_UNetPP适配方案.md` 虽然已有结构边界和结果要求，但整体仍偏“公平子协议复刻版”，不是方法级执行协议。
- 冲突来源：旧版正文主轴仍不够像执行链，缺少“上位继承 -> 方法身份 -> 正式接入链 -> 结果资格 -> 回退链”的清晰节奏。
- 裁决结论：本轮按方法执行协议重写，主结构固定为 `任务定位 -> 前置文件 -> 上位继承与唯一变量 -> 正式接入链 -> 规则卡片 -> 代码落地接口 -> 验收与回退 -> 冲突裁决 -> 自检 -> Diagnostics 闭环`。
- 裁决理由：`UNet++` 是首批外部方法中最接近主线结构参照的一类；如果其结构边界和适配边界不先压实，后续 `03/04`、`09`、`10`、`11` 都会退回“方法名对方法名”的软比较。
- 对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/01_统一公平协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/04_AttUNet适配方案.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/05_增强对比进入条件.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/06_引用值与复现值标记规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/07_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/10_结果汇总/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/11_总验收与止损/00_阶段总协议.md`
- 是否需要回流修订：需要；后续处理 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/04_AttUNet适配方案.md` 时，必须同步把“结构本体 / 额外收益 / 接入链 / 结果资格 / 回退边界”压到同等强度。

---

## 9. 文件质量自检

- [x] 已在重写前完成 `00_总览与规范` 全套重读，而不是只读导航文件。
- [x] 已补读 `02_路线与投稿` 中与 `UNet++` 外部对比强相关的三份路线文件。
- [x] 已补读 `03_文献证据` 中与 `UNet++`、同层通用外部方法、增强外部候选和 task-specific 对照相关的正式深提取稿。
- [x] 已补读 `01_实验执行` 中与当前文件直接相关的上游、同层和下游文件，而不是复用上一份文件的邻近模板。
- [x] 已把 `本轮重写直接依赖的前置文件` 显式写成独立落点，而不是只在正文零散引用。
- [x] 已显式区分上游、同层、下游，并写清这些文件为什么与当前文件相关。
- [x] 已把 `current_mainline`、`external_run_fair`、`allowed_gap`、`unetpp_external_run`、`unetpp_v1`、`need_three_seed`、`direct_comparison_eligible` 写成正式定义。
- [x] 已把 nested skip 的结构本体、semantic gap 解释和核心公式写清到可直接支撑实现与论文写作的程度。
- [x] 已把 `deep supervision`、`accurate mode`、`fast mode`、`pruning` 的边界写成正式裁决，而不是口头提醒。
- [x] 已把 plain `UNet++` 与 encoder 替换变体、预训练变体的边界写清。
- [x] 已把 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 明确落入 `UNetPP` 的公平协议字段、前置断言和 run_meta.yaml 字段链，而不是只沿用抽象版本号。
- [x] 已把正文主轴改成 `任务定位 -> 上位继承 -> 接入链 -> 规则卡片 -> 代码接口 -> 结果资格 -> 回退链`，不再沿用旧版松散结构。
- [x] 已写清代码落点、入口函数、I/O、依赖配置、前置断言和运行产物。
- [x] 已把 `reproduced / † / *`、`single_seed / mean +- std`、`direct_comparison_eligible` 的写作边界前置写入当前文件。
- [x] 已写清 `Gate_H1` 与本文件的关系，而不是把阶段门控留给下游猜测。
- [x] 已保留独立 `回退条件`，没有把回退要求藏进通过线或总结句里。
- [x] 已补齐 `回退顺序` 与 `回退后重新放行条件`，避免“知道要回退但不知道如何放行”的缺口。
- [x] 已补写标准化 `冲突裁决记录`，明确旧版为什么不达标以及本轮如何重构。
- [x] 已对照同层强模板 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md` 检查 `文件质量自检` 条目数量、颗粒度和覆盖维度，没有缩水。
- [x] 已保留独立标题 `Diagnostics 闭环`，没有退回成弱标题或弱说明。
- [x] 已确保正文、自检、回退条件和 diagnostics 之间使用一致的术语、字段名和阶段码。
- [x] 当前文件没有把增强外部、task-specific 直比或下游验收职责错误卷入本文件角色。
- [x] 当前文件已经达到“可直接指导代码实现、结果汇总、下游 handoff 和论文写作”的最低强度。

---

## 10. Diagnostics 闭环

- 本轮执行要求：整篇重写落盘后，必须先回读磁盘最终版本，再执行 IDE `Markdown Diagnostics` 复核。
- 复核范围：标题层级、列表结构、代码块闭合、公式书写、字段命名一致性、`上游 / 同层 / 下游` 显式落点、`回退条件` 是否独立，以及 `文件质量自检` 与 `Diagnostics 闭环` 是否保持独立标题。
- 对照要求：`Diagnostics 闭环` 的标题与内容强度不得弱于同层强模板 `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/03_DeepLabV3P适配方案.md`。
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复，再重新复核。
- 闭环结果要求：最终汇报必须同步说明“已回读文件、已执行 diagnostics、是否存在问题、是否已修复”，不能只写“已检查”。

---

## 11. 一句话版本

> `UNet++` 在当前项目中已经被正式固定为首批核心外部方法中的“更强 U 型密集跳连结构”代表；`v1` 适配只保留 nested skip 这一结构本体，并在统一数据、统一训练、统一评估协议下以单输出版本进入公平比较，而不把 `deep supervision`、`accurate mode`、`fast mode`、`pruning`、encoder 替换或特殊测试流程带来的额外收益混进正式主表。
