# 距离图与 `lambda` 范围

本文件不是 `07_Distance` 阶段里“距离损失大概怎么调”的说明文，也不是把 `euclidean / SDM / skeleton / topology` 等相邻路线混在一起的参数备忘录。

它在当前项目中的唯一职责是：

> 作为 `07_Distance` 的正式 `distance target protocol + lambda boundary protocol`，把距离图唯一从哪里来、唯一按什么定义生成、唯一如何归一化、`lambda_dist` 的正式候选集合与主版本怎样冻结、训练/验证/测试/可视化/阶段汇总怎样保证完全同口径，以及这些规则如何落到代码、运行记录、阶段裁决、回退和下游交接，一次写死。

从现在开始，只要讨论 `Distance-aware Loss v1` 的距离图来源、值域、主版本、备选边界、字段链和实现一致性，都必须以本文件为准；若与同层文件冲突，以 `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md` 管阶段身份与门控，以 `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md` 管“为什么当前只能这样设计”，而本文件负责把“距离图究竟怎样唯一生成、`lambda_dist` 究竟怎样收口”压成可直接落代码、可直接验收、可直接交接的正式协议。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面九件事：

1. `Distance` 阶段距离监督目标唯一来自哪里，以及为什么必须固定为冻结二值 gland mask。
2. 距离图唯一合法定义是什么，以及为什么首版只能固定为 `Euclidean distance map`。
3. 距离图值域、归一化规则和生成顺序怎样收口成唯一协议。
4. 训练、验证、测试、可视化、错误案例分析和阶段汇总怎样复用同一正式实现，避免多条链各写一套。
5. `lambda_dist` 的正式候选集合、首轮主版本和备选触发边界怎样冻结。
6. 哪些更重的相邻路线必须被显式排除，避免把当前阶段扩成 shape/topology 家族搜索。
7. 哪些代码入口、配置字段和运行记录字段必须显式存在，不能藏在默认值里。
8. 距离图协议漂移时，什么情况必须先回退修正，而不能继续推进 `结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\03_实验步骤.md`、`结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\04_保留或降级标准.md` 或下游阶段。
9. 本文件怎样作为 07_Distance/03-04 与 `08/09` 的上游 target 母规范。

### 1.2 当前文件不负责什么

当前文件不重新定义下面这些内容：

- `Distance` 阶段为什么存在，以及为什么当前只能做最小可解释的 `Distance-aware Loss v1`。
- `screening_main -> three_seed_main -> optional_one_backup -> stage_decision` 的执行顺序本体。
- `keep / downgrade / drop` 的最终证据排序和阶段裁决细则。
- baseline、`LKMA`、`Boundary` 的结构身份、训练协议、评估协议和正式结论。
- `Gate_E1` 的阶段门控表达与 `distance_kept_base / distance_input_base` 的最终 handoff 资产定义。
- `08_外部对比` 与 `09_CRAG验证` 的执行规则、统计表结构和最终实验结论。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

因为 `Distance` 阶段最容易出现的伪完成状态不是“完全没写距离图”，而是：

- 训练说自己在用距离图，分析脚本和可视化却各自重建了另一版 target。
- 主版本名都写成 `Distance-aware Loss`，实际却混用了 `euclidean`、`signed distance` 或不同归一化。
- `lambda_dist` 口头上是“辅助项”，实际却被放大成多距离图定义乘多权重的联合搜索。
- `keep` 明明只能基于主版本三 seed 证据形成，却被备选值、单 seed 或 screening 偶然结果提前替代。
- 下游 `08/09` 想继承 `Distance` 结论时，说不清它们读取的是哪一版 target protocol 与哪一版正式主线。

如果没有一份独立 target 协议文件，`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md` 会被迫同时承担“为什么这样设计”和“target 到底怎样生成”的双重职责，`结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\03_实验步骤.md` 与 `结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\04_保留或降级标准.md` 也会被迫各自补一套距离图定义，最终使 target 口径再次分叉。

---

## 2. 前置文件依赖

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求修改 `01_实验执行` 下任意 md 前先重读总览层，并按正式协议整篇重写而不是保留旧说明文骨架。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把 `crc_gland_segmentation_project/src/`、`crc_gland_segmentation_project/configs/`、`crc_gland_segmentation_project/scripts/`、`crc_gland_segmentation_project/reports/` 中与距离图有关的正式落点写清。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：冻结首轮距离图为 `Euclidean distance map`，`lambda_dist` 边界为 `0.05 / 0.1 / 0.2`，默认主版本为 `0.1`。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：约束 `run_name`、`distance_target_version`、`distance_type`、`distance_norm`、`lambda_dist` 等字段的命名与回查方式。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：冻结 `best_selector = val_objdice_max`、`threshold_source = val17` 与对象级主指标优先口径。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求规则必须落到正式函数入口、I/O、依赖配置、前置断言和运行产物。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求保留规则卡片、公式定义、代码落地接口、冲突裁决、回退和收尾闭环。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求显式补齐 `本轮重写直接依赖的前置文件`、`上游 / 同层 / 下游`、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 2.2 路线依据

本轮重写直接继承以下路线约束：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`：锁定主线顺序为 `UNet -> ResNet34-U-Net -> LKMA -> Boundary Head -> Distance-aware Loss`。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：明确 `Distance` 是 `Boundary` 之后的第三模块阶段，距离图首轮固定为 `Euclidean distance map`，值域统一 `[0, 1]`，`lambda_dist` 默认 `0.1`，备选边界为 `0.05 / 0.1 / 0.2`。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`：约束当前阶段只回答“距离监督是否值得进入主线”，不能越级写成新方法主线突破。

### 2.3 文献依据

本轮重写直接继承以下文献层证据：

- `结直肠腺体分割_plan_优化版/03_文献证据/02_边界_形状_损失支撑/02_Distance-Map-Loss.md`：提供距离图辅助监督值得验证的直接依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/02_边界_形状_损失支撑/04_Shape-Aware-SDM.md`：说明 `signed distance map` 是相邻但更重的 shape-aware 路线，不属于当前首版最小协议。
- `结直肠腺体分割_plan_优化版/03_文献证据/02_边界_形状_损失支撑/05_clDice.md`：说明 skeleton / connectivity 约束属于更偏 topology 的路线。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/07_TA-Net.md`：说明 `MA distance map`、marker、`watershed` 恢复链属于更复杂的腺体实例路线。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/14_SkeletonAwareDT.md`：说明 skeleton-aware distance transform 是更重的表示层路线，而不是当前普通欧氏距离监督的等价替代。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`：冻结 `train_proto_v1 / eval_proto_v1`、优化协议、`best_selector` 和阈值来源，决定距离图只能作为附加监督目标接入现有主链。
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`：提供独立回退、阶段放行和收尾闭环的强模板写法，是当前文件收尾强度的重要对照来源。
- `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`：冻结 `Boundary` 阶段输出身份，是 `current_base` 来源的直接制度上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`：冻结 `Distance` 阶段身份、`Gate_E1`、handoff 语义和下游消费边界，是本文件的母协议上游。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`：冻结“为什么当前只能采用最小距离监督抽象”的设计层理由，是当前文件的直接设计上游。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`：直接消费本文件冻结的 `distance_target_version`、`distance_type`、`distance_norm` 和 `lambda_dist` 边界，用来决定 screening、三 seed 主版本和备选版本怎样启动。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`：直接消费本文件冻结的 target 版本、主版本锚点和备选触发边界，用来决定 `keep / downgrade / drop`。

#### 同批模板强度对照

- 主结构模板：`结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/02_边界标签生成规则.md`
- 设计上游模板：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- 收尾强度模板：`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- 门控与交接模板：`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`

本轮对照的固定结论是：

- 当前文件虽然是 target 协议，不是设计依据，但前部必须显式具备 `文件角色与执行边界`、`本轮重写直接依赖的前置文件` 和 `上游 / 同层 / 下游`，不能弱于 `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/02_边界标签生成规则.md`。
- 当前文件虽然不直接定义 `Gate_E1`，但必须足够强到能让 `结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\03_实验步骤.md`、`结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\04_保留或降级标准.md` 与 `08/09` 无歧义读取同一 target 版本和同一 `lambda_dist` 主版本。
- 当前文件的独立 `回退条件`、`文件质量自检` 和独立 `Diagnostics 闭环` 的标题强度、条目颗粒度和闭环表达不得弱于 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`：下游直接消费 `Distance` 阶段正式结论来决定 `current_mainline` 是否切换为 `distance_kept_base`。
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`：继续消费由 `Distance` 唯一决定的主线，不允许在跨数据集验证时重新定义 target 协议或主版本身份。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前文件真正要证明什么

本文件真正要证明的不是“距离图可以这样做”，而是下面七件事已经被正式写成唯一协议：

1. 当前 `Distance` 阶段的距离图只能从冻结二值 gland mask 派生，而不能从预测结果、后处理结果或分析脚本反推。
2. 当前正式 target 定义已经唯一固定为 `Euclidean distance map`，而不是 `SDM`、`MA distance map`、骨架距离或方向场。
3. 当前归一化规则已经唯一固定为 `norm01`，值域统一为 `[0, 1]`。
4. 当前训练、验证、测试、可视化、分析和汇总必须共用同一 target 构建实现，不允许多入口漂移。
5. 当前 `lambda_dist` 已收口为 `{0.05, 0.1, 0.2}`，且主版本只能是 `0.1`。
6. 当前备选版本最多只允许补一个，角色是判断主版本“过弱还是过强”，而不是扩大搜索空间。
7. 当前文件已经足以为 `结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\03_实验步骤.md`、`结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\04_保留或降级标准.md` 和下游主线提供唯一合法的 target 口径。

### 3.2 为什么 target protocol 必须先于正式 run 写死

因为 `Distance` 阶段当前真正要验证的是：

> 在 `current_base` 已冻结、训练与评估协议已冻结、`Distance-aware Loss v1` 已被压成最小可解释抽象的前提下，连续距离监督本身是否值得保留。

如果 target protocol 还在漂移，后续就无法判断收益来自：

- 连续距离信息本身。
- 还是来自距离定义、归一化或权重范围被偷偷换掉。
- 还是来自 target 生成实现被拆成多套脚本后产生的口径差异。

因此，target 协议必须先于 `screening_main` 和三 seed 主版本冻结，否则整个阶段都会从单变量验证退化成 target 漂移实验。

### 3.3 当前文件与 `01/03/04` 的分工

四份同层文件的固定分工是：

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`：回答“为什么当前只能这样做”。
- 本文件：回答“距离图与 `lambda_dist` 究竟怎样唯一定义”。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`：回答“正式 run 怎样按顺序执行”。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`：回答“证据怎样排序并形成结论”。

如果把这四类职责混写，就会同时丢失两种清晰性：

- 设计层说不清哪些是“为什么”，哪些是“协议本体”。
- 执行层说不清哪些字段是 target 字段，哪些字段是阶段门控字段。

---

## 4. 上游继承、当前基座与唯一变量

### 4.1 当前文件直接继承哪些冻结项

本文件直接继承并不得擅自改动的上位规则如下：

- 主任务：`2D gland segmentation`
- 主数据集：`GlaS`
- 正式 split：`train68 / val17 / testA60 / testB20`
- 标签总口径：`mask > 0`
- 输入尺寸：`512 x 512`
- `current_base`：由 `Boundary` 阶段正式结论唯一决定
- `train_proto_version = train_proto_v1`
- `eval_proto_version = eval_proto_v1`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `postprocess_version = none_in_v1`
- `eval_cast_policy = float32 before thresholding`
- `boundary_metric_width = 3 px`
- `boundary_metric_impl = skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`
- `connected_components_impl = scipy.ndimage.label`
- `connected_components_connectivity = 8-connectivity`
- 固定三 seed：`3407 / 1234 / 2025`
- `run_name` 模板：`E1_[model_code]_GlaS_v1_seed*`

### 4.2 当前阶段唯一合法起点

当前阶段的比较基座不是重新选择，而是由 `Boundary` 阶段正式结论唯一决定：

```text
current_base = (boundary_decision_level == keep) ? boundary_kept_base : boundary_input_base
```

这意味着：

- 只有 `06_Boundary` 已形成正式结论并完成 handoff，`Distance` 才允许启动。
- 任何正式 `Distance` run 都必须能追溯到 `Boundary` 的 decision note、stage manifest 和 `current_base` 说明。
- 本文件不能借机重开 `current_base` 的来源，只能在该基座上冻结距离 target 协议与 `lambda_dist` 边界。
- `Boundary` handoff 中的 `current_base_next` 必须与这里使用的 `current_base` 完全等价；本文件只承认上游唯一交接语义，不接受手工改写起点。

### 4.3 当前文件唯一允许冻结的变量

当前文件唯一允许定义和冻结的变量固定为：

- `distance_target_version`
- `distance_target_source`
- `distance_build_mode`
- `distance_type`
- `distance_norm`
- `distance_value_range`
- `lambda_dist`
- `lambda_dist_policy_version`
- `backup_variant`

### 4.4 当前文件明确不允许重开的内容

当前文件不允许借机重新打开：

- baseline backbone、`LKMA` 配置和 `Boundary` 标签协议
- 数据协议、输入尺寸、增强包、主损失、optimizer、scheduler
- checkpoint selector、阈值来源和后处理定义
- `signed distance map`
- `clDice`
- `TA-Net`
- `SkeletonAwareDT`
- `direction field`
- `marker branch`
- `watershed` 恢复链
- 多距离图定义乘多 `lambda` 的联合网格搜索

换句话说，这里只负责“距离图怎样唯一生成、`lambda_dist` 怎样唯一收口”，不负责把 `Distance` 写成新的表示路线或搜索阶段。

---

## 5. 如何判断设计有效(验收标准)

下面所有核心规则都写成正式协议格式；后续实现、实验和阶段汇总时，只允许把这些规则忠实落地，不允许再擅自补新的隐含 target 变量。

### 5.1 距离图唯一来源规则

- 当前结论：距离图唯一来源固定为数据阶段冻结的二值 gland mask，且二值前景定义固定为 `M(x) = 1[mask(x) > 0]`。
- 规则类型：`工程冻结规则 + 标签定义规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 核心公式或定义参考：`M(x) = 1[mask(x) > 0]`
- 采用原因：只有先把监督源唯一化，训练、可视化、汇总和下游 handoff 才能共享同一 target 身份。
- 不采用的相邻方案：不从预测 mask、后处理结果或分析脚本反推当前正式距离图。
- 代码落点：`crc_gland_segmentation_project/src/data/mask_ops.py`、`crc_gland_segmentation_project/src/data/distance_targets.py`
- 运行记录字段：`distance_target_source`、`distance_target_version`、`foreground_rule`
- 验收方式：检查正式 `Distance` run 的 run_meta.yaml 都明确记录距离图来源为冻结二值 mask。

### 5.2 正式距离图定义规则

- 当前结论：首轮正式距离图定义固定为 `Euclidean distance map`。
- 规则类型：`论文支持的候选范围 + 工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：02_Distance-Map-Loss.md、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- 核心公式或定义参考：`D = EDT(M)`
- 采用原因：`Euclidean distance map` 是当前最小、最稳、最容易复查的距离表示，足以验证连续距离约束本身是否有补充价值。
- 不采用的相邻方案：不采用 `signed distance map`、`MA distance map`、`skeleton-aware distance transform`、`direction field`。
- 代码落点：`crc_gland_segmentation_project/src/data/distance_targets.py`
- 运行记录字段：`distance_type`
- 验收方式：检查正式配置、训练日志和阶段报告统一写成 `distance_type = euclidean`。

### 5.3 距离图归一化和值域规则

- 当前结论：正式距离图统一归一化到 `[0, 1]`，配置字段固定为 `distance_norm = norm01`、`distance_value_range = [0, 1]`。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- 核心公式或定义参考：`D_norm = Normalize01(D)`
- 采用原因：统一值域能减少距离损失尺度漂移，使 `lambda_dist` 的解释保持稳定。
- 不采用的相邻方案：不采用 `[-1, 1]` 的 `SDM` 值域；不采用未归一化原始距离；不采用按 batch 临时缩放。
- 代码落点：`crc_gland_segmentation_project/src/data/distance_targets.py`、[project_root]/configs/model/distance_loss_v1.yaml
- 运行记录字段：`distance_norm`、`distance_value_range`、`distance_norm_scope`、`distance_zero_denominator_action`
- 验收方式：检查 run_meta.yaml 明确记录 `norm01` 与 `[0, 1]`，且训练/分析口径一致；检查没有出现 batch 级或全局级临时归一化

### 5.4 距离图正式生成流程规则

- 当前结论：正式生成流程固定为 `冻结二值 mask -> EDT -> norm01 -> 训练/验证/测试/可视化/分析共用`。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：02_Distance-Map-Loss.md、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- 核心公式或定义参考：`target_pipeline = build_binary_mask -> build_euclidean_distance_map -> normalize_distance_map`
- 采用原因：流程必须足够直接，避免在不同环节出现额外裁剪、截断或私有 target 变体。
- 不采用的相邻方案：不采用训练前离线生成一版、分析时再动态构建另一版；不采用可视化阶段单独二次平滑却不记录版本。
- 代码落点：`crc_gland_segmentation_project/src/data/distance_targets.py`、`crc_gland_segmentation_project/scripts/train.py`、[project_root]/scripts/test.py
- 运行记录字段：`distance_target_version`、`distance_build_mode`
- 验收方式：检查训练、测试与汇总都调用同一 target 入口函数，且日志记录同一 target 版本。

### 5.5 与主分割损失关系规则

- 当前结论：距离项只能作为附加损失，不得替代或弱化 `L_seg`。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- 核心公式或定义参考：`L_total = L_seg + lambda_dist * L_dist`
- 采用原因：本阶段研究问题是“距离项有没有额外价值”，不是“用距离项重写主监督”。
- 不采用的相邻方案：不采用 distance-only 训练主版本；不把距离项写成新的主任务回归头。
- 代码落点：[project_root]/src/losses/distance_losses.py、[project_root]/src/losses/seg_losses.py
- 运行记录字段：`loss_version`、`dist_loss_type`、`lambda_dist`
- 验收方式：检查训练日志仍保留主分割损失与距离损失的分项记录。

### 5.6 `lambda_dist` 候选集合规则

- 当前结论：`lambda_dist` 正式候选集合固定为 `{0.05, 0.1, 0.2}`。
- 规则类型：`参数冻结执行化 + 工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`、`结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 核心公式或定义参考：`Lambda_dist = {0.05, 0.1, 0.2}`
- 采用原因：当前距离项是附加监督，权重必须保持小而可解释，不能压过主分割目标。
- 不采用的相邻方案：不做 `0.01~1.0` 大范围搜索；不做连续网格或 Bayesian search。
- 代码落点：[project_root]/configs/experiment/distance_e1_v1.yaml、[project_root]/src/losses/distance_losses.py
- 运行记录字段：`lambda_dist`、`lambda_dist_policy_version`
- 验收方式：检查任何正式 `Distance` run 的 `lambda_dist` 都只能落在这三值集合内。

### 5.7 主版本规则

- 当前结论：首轮主版本固定为 `distance_type = euclidean`、`distance_norm = norm01`、`lambda_dist = 0.1`。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`
- 核心公式或定义参考：`main_distance_variant = DistanceAwareLoss(euclidean, norm01, lambda=0.1)`
- 采用原因：`0.1` 足以让距离项产生可见影响，同时仍维持“主分割主导、距离项辅助”的角色关系。
- 不采用的相邻方案：不把 `0.05` 或 `0.2` 直接写成首轮主版本；不按不同 seed 更换主测值。
- 代码落点：[project_root]/configs/experiment/distance_e1_v1.yaml
- 运行记录字段：`distance_type`、`distance_norm`、`lambda_dist`、`variant_rank`
- 验收方式：检查首个 `screening_main` 与后续 `three_seed_main` 都以 `0.1` 为主版本。

### 5.8 备选版本边界规则

- 当前结论：只有当主版本 `0.1` 接近可用但证据不清时，才允许最多补一个备选值 `0.05` 或 `0.2`。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`
- 核心公式或定义参考：`optional_backup_lambda in {0.05, 0.2}`
- 采用原因：备选值的角色是判断距离项“过弱还是过强”，不是扩大搜索空间。
- 不采用的相邻方案：不在主版本不过线后同时补两个备选值；不边跑边改 `lambda_dist`；不为不同 seed 使用不同备选值。
- 代码落点：[project_root]/configs/experiment/distance_e1_v1.yaml、[project_root]/scripts/summarize_stage.py
- 运行记录字段：`backup_variant`、`backup_reason`、`lambda_dist`
- 验收方式：检查备选版本最多只有一个，且有显式触发理由和独立记录字段。

### 5.9 禁止路线清单规则

- 当前结论：`Distance v1` 正式禁止 `signed distance map`、`clDice`、`direction field`、`MA distance map`、`skeleton-aware distance transform`、`marker branch`、`watershed` 恢复链和复杂 topology-preserving loss。
- 规则类型：`裁决后冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：04_Shape-Aware-SDM.md、05_clDice.md、07_TA-Net.md、14_SkeletonAwareDT.md
- 核心公式或定义参考：这些路线都要求新增输出头、表示空间、拓扑约束或后处理依赖，已经超出 `Distance-aware Loss v1` 的单附加损失边界。
- 采用原因：当前阶段只验证最小距离监督本身，不能把 `Distance` 写成 shape/topology 家族试验场。
- 不采用的相邻方案：不把这些路线伪装成“只是另一种 distance target”。
- 代码落点：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`
- 运行记录字段：`rejected_route`、`rejected_reason`
- 验收方式：检查正式配置、代码和阶段总结中不存在上述路线对应模块与字段。

### 5.10 三链一致性与字段链规则

- 当前结论：训练、验证/测试、可视化/分析和阶段汇总必须共享同一 target 实现与同一字段链；正式结果还必须继续绑定 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 五个评估实现硬字段。
- 规则类型：`工程冻结规则`
- 适用阶段：`07_Distance`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
- 核心公式或定义参考：`single_source_of_truth(distance_target_version, distance_type, distance_norm, lambda_dist)`
- 采用原因：如果三条链被拆散，最后无法判断模型收益来自真实算法还是来自口径差异。
- 不采用的相邻方案：不保留多个正式实现入口；不让离线缓存和动态生成各写一套定义。
- 代码落点：`crc_gland_segmentation_project/src/data/distance_targets.py`、`crc_gland_segmentation_project/scripts/train.py`、[project_root]/scripts/test.py、[project_root]/scripts/summarize_stage.py
- 运行记录字段：`run_name`、`distance_target_version`、`distance_type`、`distance_norm`、`lambda_dist`、`eval_cast_policy`、`boundary_metric_width`、`boundary_metric_impl`、`connected_components_impl`、`connected_components_connectivity`
- 验收方式：检查所有正式结果文件中的字段链一致，且可回溯到同一实现文件；检查五个评估实现硬字段同时进入 config.yaml、run_meta.yaml、per-seed raw、`mean+-std`、compare 表、distance_stage_manifest.csv 与 handoff 资产。

### 5.11 下游读取约束规则

- 当前结论：下游只允许继承由主版本正式结论绑定的 `distance_kept_base` 或 `distance_input_base`，不得私自读取备选版本或未定版 target；同时 handoff 必须保留 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity`，避免下游只知道 target 版本而不知道评估实现版本。
- 规则类型：`阶段交接规则 + 下游消费规则`
- 适用阶段：`07_Distance` 结束后立即生效
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- 核心公式或定义参考：`current_mainline = (decision_level == keep) ? distance_kept_base : distance_input_base`
- 采用原因：下游阶段只允许从唯一合法主线启动，不能继续消费未定版、备选搜索结果或口头偏好。
- 不采用的相邻方案：不把 `downgrade` 或备选版本默认当主线；不在没有正式 decision note 的情况下直接启动 `08/09`。
- 代码落点：[project_root]/scripts/summarize_stage.py、[project_root]/reports/tables/distance_stage_manifest.csv
- 运行记录字段：`decision_level`、`distance_kept_base`、`distance_input_base`、`current_mainline`
- 验收方式：检查 stage summary 和 manifest 已显式写明下一阶段合法主线与资产路径。

---

## 6. 距离图与 `lambda` 的公式级定义

### 6.1 前景定义

冻结二值 gland mask 记为：

```text
M(x) = 1[mask(x) > 0]
```

其中：

- `M(x) = 1` 表示像素 `x` 属于 gland 前景。
- `M(x) = 0` 表示像素 `x` 属于背景。

### 6.2 距离图定义

首版正式距离图固定为：

```text
D = EDT(M)
```

这里的 `EDT` 表示对冻结前景 mask 计算 `Euclidean Distance Transform`。

当前协议只要求：

- 训练、分析和可视化都使用同一 `EDT` 定义。
- `D(x)` 在当前阶段被解释为 gland 前景内部到最近边界的欧氏距离，因此靠近轮廓的前景像素取值更小，位于腺体更深内部的像素取值更大。
- 不在本阶段引入 signed distance 的内外符号约定。
- 不引入骨架、marker 或方向场等额外表示。

### 6.3 归一化定义

首版距离图统一做 `norm01` 归一化：

```text
D_norm = Normalize01(D)
```

形式上记为：

```text
D_norm(x) in [0, 1]
```

### 6.3.1 `norm01` 的颗粒度与零分母处理

当前 `norm01` 必须继续写死两条实现边界，避免训练脚本、分析脚本和可视化脚本各自理解：

```text
distance_norm_scope = per_sample
D_norm = D / max(D), if max(D) > 0
```

固定解释如下：

- `norm01` 只允许按单样本距离图归一化，不允许按 batch、整数据集或离线统计值做全局缩放。
- 同一张图上的训练、验证、测试、可视化和阶段汇总都必须共用同一个 `per_sample` 归一化实现。
- 若某张样本的距离图出现 `max(D) = 0`，这不允许被静默吞掉或自动改成私有兜底值；必须按 `distance_zero_denominator_action = fail_fast` 回退到 target 构建检查。

这样写死的原因是：

- `lambda_dist` 只有在距离图尺度稳定时才具备可解释性。
- 若归一化颗粒度在不同脚本间漂移，后面的任何 `keep / downgrade / drop` 都无法判断是在比较同一版距离协议。

### 6.4 总损失定义

当前距离监督与主分割目标的组合形式固定为：

```text
L_total = L_seg + lambda_dist * L_dist
```

其中：

- `L_seg` 为已冻结主分割损失。
- `L_dist` 为距离监督附加项。
- `lambda_dist` 为本文件冻结的距离损失权重。

### 6.4.1 `L_dist` 的唯一函数形式

当前阶段不引入额外 distance regression head，`L_dist` 的唯一实现起点固定为“距离图加权的逐像素 `BCEWithLogits`”：

```text
Input:
    logits_seg in R^(B x 1 x H x W)
    M in {0, 1}^(B x 1 x H x W)
    D_norm in [0, 1]^(B x 1 x H x W)

Internal:
    bce_map = BCEWithLogits(logits_seg, M; reduction = none)
             # bce_map in R^(B x 1 x H x W)
    weight = 1 + (1 - D_norm) * M
             # weight in [1, 2]^(B x 1 x H x W)
    L_dist = Mean(weight * bce_map)

Output:
    L_dist in R
```

这里的固定实现语义是：

- `L_dist` 直接作用在主分割 logits 上，不单独新增 distance prediction branch，也不把当前阶段扩成距离回归任务。
- `BCEWithLogits` 使用 `reduction = none` 先保留逐像素损失图，再与显式定义的 boundary-proximal weight 逐点相乘，最后对 `B x H x W` 全部像素取 `mean` 得到标量。
- `weight = 1 + (1 - D_norm) * M` 是当前阶段唯一允许的距离权重形式，因此背景区域保持单位权重，前景内部越靠近轮廓权重越高，像素权重整体范围固定在 `[1, 2]`；不允许再额外乘未记录的 class weight、focal factor 或手工 boundary mask。
- `L_dist` 仍然对整张图求均值，但被显式放大的只是在 gland 前景内部更靠近边界的像素；若后续想改成前景内回归、signed distance regression、显式外侧距离加权或 topology-aware loss，必须视为新路线而不是本协议内实现细化。
- 在 AMP 打开时，`logits_seg` 可以来自混合精度前向，但 `bce_map`、`weight` 与最终 `L_dist` 在实现上必须保持或转回 `float32` 聚合，避免因为精度缩放让 `lambda_dist` 解释失真。

### 6.5 主版本记法

主版本写法固定为：

```text
distance_type = euclidean
distance_norm = norm01
distance_value_range = [0, 1]
lambda_dist = 0.1
```

---

## 7. 实验搜索边界与阶段关系

### 7.1 当前唯一合法主版本

当前唯一合法主版本固定为：

```text
Distance main version = current_base + DistanceLoss(euclidean_norm01, lambda=0.1)
```

### 7.2 当前允许的备选版本

若必须补试，当前只允许二选一：

- `current_base + DistanceLoss(euclidean_norm01, lambda=0.05)`
- `current_base + DistanceLoss(euclidean_norm01, lambda=0.2)`

### 7.3 当前明确禁止的搜索方式

当前正式禁止：

- `distance_type x lambda_dist` 二维网格搜索。
- 主版本未完成闭环前并行补多个备选值。
- 因单 seed 偶然结果即时回调 `lambda_dist`。
- 看完 `TestA / TestB` 后再回调 `lambda_dist`。
- 为不同 seed 使用不同 `lambda_dist`。
- 主版本不过线后同时扩展距离图定义与 `lambda` 搜索边界。

### 7.4 主版本与阶段裁决关系

当前阶段必须坚持下面这条强约束：

```text
keep <= main_version(lambda=0.1, three_seed_formal_evidence)
```

也就是说：

- 只有 `lambda_dist = 0.1` 的主版本完成三 seed 正式 run、`mean+-std` 聚合、案例图和成本记录后，才允许形成 `keep`。
- 备选版本如果存在，只能作为“过弱或过强”的辅助解释，不能替代主版本成为正式保留依据。
- `Gate_E1` 和下游交接仍由 `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md` 负责，但本文件必须保证其读取的 target 协议是唯一且稳定的。

---

## 8. 代码实现约束

### 8.1 本阶段必须新增或正式存在的对象

- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/02_距离图与lambda范围.md`
- `crc_gland_segmentation_project/src/data/mask_ops.py`
- `crc_gland_segmentation_project/src/data/distance_targets.py`
- [project_root]/src/losses/distance_losses.py
- [project_root]/configs/model/distance_loss_v1.yaml
- [project_root]/configs/experiment/distance_e1_v1.yaml
- `crc_gland_segmentation_project/scripts/train.py`
- [project_root]/scripts/test.py
- [project_root]/scripts/summarize_stage.py
- [project_root]/reports/stage_reports/distance_decision_note.md

### 8.2 本阶段必须复用或对齐的对象

- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`

### 8.3 本阶段禁止修改的对象

- `splits/glas/*.csv`
- `crc_gland_segmentation_project/configs/data/glas.yaml` 中已冻结的数据路径与标签口径
- 主指标定义与对象级匹配规则
- baseline、`LKMA`、`Boundary` 已冻结的结构、配置和正式结论
- `08_外部对比` 与 `09_CRAG验证` 的主线定义

### 8.4 本阶段必须新增或明确的记录字段

后续任何正式 `Distance` run、阶段汇总或下游 handoff，至少要记录：

- `run_name`
- `stage_code`
- `base_variant`
- `base_decision_source`
- `distance_target_version`
- `distance_target_source`
- `distance_build_mode`
- `distance_type`
- `distance_norm`
- `distance_value_range`
- `dist_version`
- `dist_loss_type`
- `lambda_dist`
- `lambda_dist_policy_version`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `variant_rank`
- `backup_variant`
- `backup_reason`
- `train_proto_version`
- `eval_proto_version`
- `best_selector`
- `threshold_source`
- `decision_level`
- `distance_kept_base`
- `distance_input_base`
- `current_mainline`

### 8.5 本阶段代码落地底线

本阶段任何脚本都必须满足：

- 距离图生成是显式可配置、可追溯的，而不是散落在多个脚本里的隐式默认值。
- 同一个正式 `run_name` 只能对应一个明确的 `distance_type / distance_norm / lambda_dist` 组合。
- `best_selector`、`threshold_source` 和距离图来源不能藏在代码默认值里而不写入 run_meta.yaml。
- 聚合脚本必须同时保留 per-seed raw、`mean+-std`、边界/对象级指标、案例图和成本记录，不能只留摘要表。
- 下游 handoff 资产必须能回溯到当前正式 target 协议，而不是只写“使用了 distance loss”。

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件负责的 target 协议就必须先回退修正，而不是继续推进 07_Distance/03-04、`08_外部对比` 或 `09_CRAG验证`：

- 距离图来源没有被固定为冻结二值 mask，导致 target 来源仍可口头自由切换。
- 正式距离图没有被固定为 `Euclidean distance map + norm01`，导致 `SDM`、骨架距离或私有变体可混入正式 run。
- `lambda_dist` 边界没有被收口为 `{0.05, 0.1, 0.2}`，或主版本 `0.1` 没有被独立写死。
- target 生成流程没有被固定为 `冻结二值 mask -> EDT -> norm01 -> 全链共用`，导致训练、测试、分析之间实现分叉。
- `Boundary` handoff 的 `current_base_next` 与本文件实际使用的 `current_base` 不一致，或 target 协议无法回指到上游正式起点。
- `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 没有同时写入 config.yaml、run_meta.yaml、per-seed raw、`mean+-std`、compare 表、distance_stage_manifest.csv 与 handoff 资产。
- 自检声称“已写清回退条件 / Diagnostics 闭环”，但正文没有独立标题和独立闭环要求。
- 下游文件无法无歧义读取 `distance_target_version`、`distance_type`、`distance_norm`、`lambda_dist` 和主版本身份，导致 handoff 资产语义不清。

### 9.2 固定回退顺序

回退时统一按下面顺序排查：

1. 先检查距离图来源是否仍唯一绑定到冻结二值 mask。
2. 再检查距离图定义是否仍固定为 `Euclidean distance map`。
3. 再检查 `distance_norm`、`distance_value_range` 与 `lambda_dist` 主版本是否仍完全一致。
4. 再检查训练、测试、可视化和分析是否确实调用同一正式实现，而不是各自维护私有版本。
5. 最后检查备选触发条件、下游交接字段、独立自检和 diagnostics 闭环是否仍与正式协议一致。

### 9.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新声明本文件通过：

- 距离图来源、定义、归一化和值域重新完全收口为唯一协议。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md` 不再需要替本文件补写 target 定义或 `lambda` 边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md` 可以无歧义区分主版本与备选版本，并坚持 `keep` 只由主版本三 seed 证据形成。
- `结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md` 可以无歧义读取当前 target 协议与下游主线身份。
- 本文件重新满足第 `5` 节规则卡片、第 `10` 节代码落地接口以及第 `11-12` 节收尾闭环要求。

---

## 10. 代码落地接口

### 10.1 距离图构建接口

- 代码文件：`crc_gland_segmentation_project/src/data/distance_targets.py`、`crc_gland_segmentation_project/src/data/mask_ops.py`
- 入口类/函数：`build_distance_target()`、`build_euclidean_distance_map()`、`normalize_distance_map()`
- 输入：冻结二值 mask `B x 1 x H x W`
- 输出：归一化距离图 `B x 1 x H x W`
- dtype：输入 mask 为 `uint8` 或 `float32`；输出距离图为 `float32`
- 依赖配置：`distance_target_version`、`distance_target_source`、`distance_type`、`distance_norm`、`distance_norm_scope`、`distance_zero_denominator_action`
- 前置断言：输入必须来自冻结二值 mask；输出空间尺寸必须与输入 mask 一致；训练与分析必须复用同一套构建逻辑；`norm01` 只能按 `per_sample` 生效；若 `max(D) = 0` 必须 `fail_fast`；并且 target 协议必须可回指到 `current_base_next -> current_base` 的唯一上游语义。
- 运行产物：训练目标张量、heatmap 可视化、run_meta.yaml 中的距离图字段，以及与五个评估实现硬字段对齐的正式记录链。

### 10.2 距离损失接口

- 代码文件：[project_root]/src/losses/distance_losses.py
- 入口类/函数：`compute_distance_loss()`、`attach_distance_loss()`
- 输入：主分割 logits、距离图张量、`lambda_dist`
- 输出：`L_dist` 与 `L_total`
- dtype：logits 为 `float32` 或 AMP 下的 `float16/bfloat16`；距离图为 `float32`
- 依赖配置：`dist_version`、`dist_loss_type`、`lambda_dist`、`distance_type`、`distance_norm`
- 前置断言：`lambda_dist` 只能取 `{0.05, 0.1, 0.2}`；主版本固定使用 `0.1`；训练协议继续完整继承当前基座；`eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 必须与当前 target 协议一并记录。
- 运行产物：训练日志中的 `loss_dist`、`loss_total`，以及 `config.yaml / run_meta.yaml` 中的权重字段和五个评估实现硬字段。

### 10.3 阶段汇总与裁决接口

- 代码文件：[project_root]/scripts/summarize_stage.py
- 入口类/函数：`validate_distance_stage()`、`compare_current_base_vs_distance()`、`write_distance_decision_note()`
- 输入：per-seed 指标表、`mean+-std` 聚合表、target 字段链、可视化案例与成本记录
- 输出：阶段门控结论与 `keep / downgrade / drop` 说明
- dtype：指标字段为 `float`；结论字段为 `string`
- 依赖配置：`distance_type`、`distance_norm`、`lambda_dist`、`decision_level`、`decision_reason`
- 前置断言：只能对正式主版本和最多一个备选版本做裁决；不得混入私有距离图定义；`keep` 只能基于主版本三 seed 正式证据形成。
- 运行产物：[project_root]/reports/tables/current_base_vs_distance_mean_std.csv、[project_root]/reports/stage_reports/distance_decision_note.md

### 10.4 下游交接接口

- 代码文件：[project_root]/scripts/summarize_stage.py、[project_root]/reports/tables/distance_stage_manifest.csv
- 入口类/函数：`finalize_distance_stage_decision_inputs()`、`build_stage_handoff_manifest()`
- 输入：主版本结论、target 协议字段、`distance_kept_base`、`distance_input_base`
- 输出：handoff manifest 与下一阶段主线说明
- dtype：指标字段为 `float`；版本和结论字段为 `string`
- 依赖配置：`decision_level`、`distance_target_version`、`lambda_dist`、`current_mainline`
- 前置断言：handoff 资产必须显式记录本阶段采用的 target 协议、主版本身份，以及 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity`，不得只写“用了 distance supervision”。
- 运行产物：阶段 handoff manifest、下游主线说明、decision note 引用链，以及 formal handoff 中的五个评估实现硬字段。

---

## 11. 冲突裁决记录

- 冲突对象：旧版文件中“距离图和 `lambda` 的说明文”写法，与当前批次要求的“可直接指导代码、实验、验收和下游交接的正式 target protocol”之间的不一致。
- 冲突来源：旧版虽然已经写到 `Euclidean distance map`、`norm01`、`lambda_dist = 0.1` 和 `0.05 / 0.1 / 0.2`，但仍缺少与同批强模板一致的 `文件角色与执行边界`、`本轮重写直接依赖的前置文件`、显式 `上游 / 同层 / 下游`、独立 `回退条件`、下游读取约束、同批模板强度对照，以及独立 `Diagnostics 闭环`。
- 裁决结论：本轮将当前文件正式升级为同批强模板版本；明确距离图只能来自冻结二值 mask，正式定义只能是 `Euclidean distance map`，值域统一为 `norm01` 的 `[0, 1]`，主版本固定为 `lambda_dist = 0.1`，备选值最多只允许在 `0.05 / 0.2` 中补一个，`SDM / clDice / TA-Net / SkeletonAwareDT` 和 topology 恢复链全部不进入当前正式协议。
- 裁决理由：如果继续保留旧结构，虽然正文信息不少，但仍不足以保证 `结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\03_实验步骤.md`、`结直肠腺体分割_plan_优化版\01_实验执行\07_Distance\04_保留或降级标准.md`、`08_外部对比` 和 `09_CRAG验证` 使用的是同一 target 协议和同一主版本口径。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/02_距离图与lambda范围.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`
- 是否需要回流修订：需要；后续进入 `03`、`04` 和 `08/09` 时，必须直接继承本文件已经冻结的 target 协议、主版本锚点和备选边界。
- 代码实现影响：影响 `distance target` 构建函数、正式配置字段、日志记录 schema、阶段汇总比较表字段，以及下游 handoff 资产的 target 身份说明。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的硬规则真实落到正文。
- [x] 已继续补读 `02_路线与投稿`、`03_文献证据`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/03_实验步骤.md`、`结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/04_保留或降级标准.md`、`结直肠腺体分割_plan_优化版/01_实验执行/08_外部对比/00_阶段总协议.md` 和 `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/00_阶段总协议.md`，而不是停在总览层。
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论。
- [x] 已按当前文件真实角色区分上游 / 同层 / 下游，并说明这些文件为什么与“距离图与 `lambda` 协议”直接相关。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/02_边界标签生成规则.md` 的主结构模板对照，确认前部结构、目标职责与同层分工没有弱化。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/01_设计依据.md` 的上游分工对照，确认当前文件不越界重写设计裁决。
- [x] 已完成与 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md` 的收尾强度对照，确认独立 `回退条件`、`文件质量自检` 和独立 `Diagnostics 闭环` 没有缩水。
- [x] 当前版本按整篇重写执行，不是对旧稿追加零散补丁说明。
- [x] 已写清当前文件负责什么、不负责什么，以及为什么它必须独立承担 `Distance` target protocol 职责。
- [x] 已写清距离图唯一来源、唯一定义、归一化规则、主版本锚点、备选边界和禁止路线清单。
- [x] 已把关键 target 规则写成正式规则卡片，并保留 `当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式`。
- [x] 涉及 `M(x) = 1[mask(x) > 0]`、`D = EDT(M)`、`D_norm = Normalize01(D)`、`L_total = L_seg + lambda_dist * L_dist` 和 `current_mainline = (decision_level == keep) ? distance_kept_base : distance_input_base` 的地方，已补充公式、定义或实现级解释，并达到“可直接翻译代码 + 可直接写入论文”的最低深度。
- [x] 关键术语、版本名、run 字段和代码字段已与 `04_Baseline`、`06_Boundary`、07_Distance/01/03/04 和 `08/09` 保持一致。
- [x] 已写清当前文件不能重开的相邻变量，避免把 `Distance` 阶段写成新的表示路线或联合搜索阶段。
- [x] 已写清独立 `回退条件`，没有把回退要求藏进总结句、验收句或 handoff 说明里顺带带过。
- [x] 已写清代码实现约束和代码落地接口，接口对象细化到入口函数、I/O、依赖配置、前置断言和运行产物。
- [x] 已补写 `冲突裁决记录`，说明旧口径与同批强模板如何统一、影响哪些文件以及后续如何回流修订。
- [x] `文件质量自检` 条目颗粒度未缩成摘要版，覆盖了前置阅读、模板对照、正文结构、规则卡片、回退、交接、接口和收尾闭环。
- [x] `Diagnostics 闭环` 保留独立标题与正式结论写法，没有退化为一句“diagnostics 正常”。
- [x] 当前文件在落盘后必须执行回读和 diagnostics 复核，闭环动作不会被正文写作替代。
- [x] 当前文件已经达到“可直接指导 target 实现、实验执行、阶段裁决、下游交接和论文写作”的最低强度。

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成。
- 复核范围：至少覆盖标题层级、列表结构、术语一致性、字段命名一致性、`上游 / 同层 / 下游` 显式落点、公式书写和是否存在可见 markdown 诊断问题。
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核。
- 失败处理：若 diagnostics 报错指向标题层级、列表断裂、反引号闭合、公式块或引用块异常，必须先修正文档结构，再重新回读和复核。
- 对照要求：本节保持与 `结直肠腺体分割_plan_优化版/01_实验执行/06_Boundary/02_边界标签生成规则.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/02_训练协议.md` 和 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md` 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话。

---

## 14. 一句话版本

> `结直肠腺体分割_plan_优化版/01_实验执行/07_Distance/02_距离图与lambda范围.md` 的正式职责已经固定为：只从冻结二值 gland mask 出发，唯一生成 `Euclidean distance map`，统一归一化到 `norm01` 的 `[0, 1]`，并把 `lambda_dist` 收口为主版本 `0.1` 与最多一个备选值 `0.05 / 0.2`；训练、验证、测试、可视化、汇总和下游交接必须共用同一 target 实现、同一字段链和同一主版本身份，`SDM / clDice / TA-Net / SkeletonAwareDT` 等更重路线全部不进入当前首版正式协议。
