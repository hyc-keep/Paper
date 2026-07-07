# mean_std汇总规则

本文件不是 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md` 的摘要版，也不是对旧稿“再补一张表格示意”的轻量修订。

它在当前项目中的唯一定位是：

> 作为 `A2` 阶段的统计与汇总细则，把三次正式 `UNet` 重复实验怎样落 raw per-seed 表、怎样生成 `mean +- std` 聚合表、怎样写结果身份字段、怎样解释波动与异常、以及怎样向同层验收和下游 baseline 交付结果，一次写死。

从现在开始，只要讨论 `A2` 阶段三次正式 run 的统计对象、结果 schema、聚合约束、文字解释和交接边界，就以本文件为准。

---

## 1. 文件角色与执行边界

### 1.1 当前文件负责什么

当前文件只负责冻结下面六件事：

1. `A2` 阶段唯一合法的统计对象和协议一致性边界。
2. raw per-seed 结果表的最小字段、行粒度和文件落点。
3. `mean +- std` 聚合表的最小字段、聚合粒度和文件落点。
4. `result_tag / aggregation / n_runs / seeds` 等统计身份字段的固定写法。
5. 波动解释、异常 run 标记和统计文字总结的最小表达规则。
6. 本文件向 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\03_阶段验收.md` 与 `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` 的交接条件。

### 1.2 当前文件不负责什么

当前文件不重新定义以下内容：

- `UNet` 结构、输入规格、损失函数、优化器和训练过程本身。
- 三次正式 seed 的执行顺序、逐 run 资产清单和异常 run 排查流程。
- `A2` 阶段最终是否放行到下游阶段的总门控结论。
- 后续 baseline 和模块阶段的方法设计。

这些职责分别以下列文件为准：

- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`

### 1.3 为什么当前文件必须独立存在

因为 `A2` 阶段最容易发生的偷换，不是 seed 没跑，而是：

- 三次 run 已经跑了，却没有统一保留 raw 结果。
- 只报一个最好值，不报波动范围。
- 不同 split、不同协议、不同阈值被混在一起做“均值”。
- 异常 run 被直接覆盖，导致 `mean +- std` 失真。

如果没有一份独立的统计与汇总细则，同层验收文件和下游 baseline 文件就会被迫反向补 schema、补身份字段、补异常解释，最终导致 `A2` 失去“第一份正式统计协议”的作用。

---

## 2. 本轮直接依赖的前置文件

### 2.1 `00_总览与规范` 依赖

本轮重写直接应用以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件按正式实验细则整篇重写，不能在旧稿后面加几条汇总说明就算完成。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求把 `crc_gland_segmentation_project/experiments/`、`crc_gland_segmentation_project/reports/`、`crc_gland_segmentation_project/scripts/` 的结果交付边界写清，不能只留自然语言表格示意。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：提供 `A2` 必须继承的固定 seeds、输入规范、优化协议、阈值来源和评估版本边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：约束 `run_name`、`result_tag`、`aggregation`、`n_runs`、`seeds` 和结果表字段命名。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：约束 `TestA / TestB` 分开统计、对象级指标与像素级指标并存、测试阶段不得重搜阈值。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把统计规则落到入口函数、输入输出、依赖配置和产物路径。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求保留规则卡片、代码落地接口、冲突裁决、验收与回退说明。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求显式写明前置文件、上游 / 同层 / 下游、独立 `回退条件`、强版 `文件质量自检` 和独立 `Diagnostics 闭环`。

### 2.2 `02_路线与投稿` 依赖

本轮重写直接继承以下路线约束：

- 01_结直肠腺体分割_高性价比路线总锁定.md：锁定主线必须先建立稳定 `UNet` 基线，再讨论后续 backbone 和模块。
- 02_结直肠腺体分割_分阶段实验路线与执行标准.md：明确 `A2` 是第一正式统计入口，结果不再允许停留在单次 best。
- 03_结直肠腺体分割_投稿层级自查与止损判断.md：要求 `A2` 的表述停留在“最小稳定基线成立”，不能把波动统计包装成方法优势。

### 2.3 `03_文献证据` 依赖

本轮重写直接继承以下文献依据：

- `结直肠腺体分割_plan_优化版/03_文献证据/01_经典基线与对比方法/02_U-Net.md`：提供 `UNet` 作为最小分割基线的结构身份。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供 `GlaS train68 / val17 / testA60 / testB20` 和对象级评估口径的 benchmark 依据。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：提供腺体任务中 `small_gland_miss`、`adhesion_split_fail`、`boundary_blur`、`testB_harder` 等错误模式的解释背景。

### 2.4 上游 / 同层 / 下游

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`：提供 `A1` 已冻结的训练协议、评估协议、`best_selector = val_objdice_max` 和 `threshold_source = val17`，是本文件所有统计对象的母协议。
- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`：提供 `A1` 放行到 `A2` 的前置边界，保证本文件只汇总已通过流程验证的正式协议。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`：给出 `A2` 阶段的总目标、三次固定 seed 的稳定性定位和向下游交接的总边界。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`：直接提供三次正式 run 的身份、资产清单、异常 run 裁决和允许进入统计层的前置条件。

#### 同层文件

- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`：负责 `A2` 总角色和全局交接边界；本文件是它的统计与汇总细则。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`：负责 seed 执行细则；本文件消费其输出的逐 run 正式资产。
- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`：消费本文件生成的 raw 表、聚合表和统计解释，负责阶段放行与阻断。

#### 同层模板强度对照

- 主对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 辅助对照模板：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`

本轮对照的固定结论是：

- 当前文件虽然是统计细则，但 `文件质量自检` 和 `Diagnostics 闭环` 的标题独立性、条目颗粒度和闭环写法，不得弱于同层最近完成的 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\01_三次重复设计.md`。
- 当前文件虽然不负责阶段最终放行，但仍需保留独立 `回退条件`，因为它直接决定哪些 run 允许进入聚合与验收。
- 当前文件虽然是结果层规则，但仍需写清与 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\03_阶段验收.md`、`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md` 的交接方式，不能让下游反向猜测统计 schema。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`：直接消费 raw per-seed 表、`mean +- std` 聚合表、异常说明和统计文字结论。
- `结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`：直接消费 `A2` 的稳定基线结果，要求本文件先把统计 schema、结果身份和 split 级结果写死。
- 后续 `05_LKMA`、`06_Boundary`、`07_Distance` 阶段：都将复用本文件定义的 raw 表和聚合表 schema，用于横向比较。

---

## 3. 本阶段唯一允许处理的变量

### 3.1 当前统计协议的核心定义

对固定指标 `m`、固定 split `s` 和三个正式 seed 结果 `x_1, x_2, x_3`，本阶段统一定义：

- `mean(m, s) = (1/3) * sum_k x_k`
- `std(m, s) = sqrt((1/3) * sum_k (x_k - mean)^2)`

其中：

- `x_k` 只能来自三次正式 run：`A2_UNet_GlaS_v1_seed3407`、`A2_UNet_GlaS_v1_seed1234`、`A2_UNet_GlaS_v1_seed2025`
- `m` 只能是固定指标名
- `s` 只能是固定 split：`TestA` 或 `TestB`

### 3.2 当前文件直接继承的冻结字段

本文件继承并禁止改动的正式协议字段包括：

- `GlaS train68 / val17 / testA60 / testB20`
- `mask > 0`
- `RGB`
- `512 x 512`
- `ImageNet mean/std`
- `light_aug_v1`
- `L_seg = L_BCE + L_Dice`
- `AdamW`
- `lr = 1e-3`
- `weight_decay = 1e-4`
- `ReduceLROnPlateau`
- `epoch_max = 120`
- `early_stopping = 20`
- `AMP on`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `threshold_value`
- `eval_cast_policy = logits/probabilities must be kept or cast to float32 before thresholding`
- `boundary_metric_width = 3 px`
- `boundary_metric_impl = skimage.segmentation.find_boundaries(mode=inner) + binary_dilation`
- `connected_components_impl = scipy.ndimage.label`
- `connected_components_connectivity = 8`
- `eval_proto_version = eval_proto_v1`
- `postprocess_version = none_in_v1`

### 3.3 当前阶段真正统计的是什么

当前阶段统计的是：

- 固定协议下的随机波动范围。
- `TestA / TestB` 分别在对象级和像素级指标上的均值与标准差。
- 异常波动是否仍可由逐 run 错误模式解释。

它不统计：

- 临时改阈值后的“更优结果”。
- 改增强、改后处理、改 backbone 后的混合结果。
- 单次异常修复重跑与正式三次重复的混算值。

### 3.4 为什么从 `A2` 开始必须采用 `mean +- std`

原因固定为：

- `A2` 是第一正式统计入口，后续所有 baseline 和模块比较都需要一个稳定的最小基线。
- 单次 best 不能刻画随机波动，也无法解释后续方法增益是否超出自然波动范围。
- `A2` 阶段必须先把工程表格、论文表格和阶段验收字段统一到同一 schema。

---

## 4. 阶段门控表达式

### 4.1 唯一合法统计对象

- 当前结论：`A2` 的 `mean +- std` 只能对“同一协议、同一 split、同一指标、三个正式 seed”的结果做聚合。
- 规则类型：`上游继承规则 + 工程冻结规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 核心公式或定义参考：`mean(m, s)` 与 `std(m, s)` 只对 `x_1, x_2, x_3` 聚合，且三次结果满足 `proto(r_i) = proto(r_j)`
- 采用原因：只有把差异压缩到随机性本身，稳定性统计才有解释力。
- 不采用的相邻方案：不采用把 `TestA / TestB` 混算；不采用混入协议漂移 run；不采用把异常补跑混进正式三次结果。
- 代码落点：scripts/summarize_stage.py，scripts/compare_runs.py
- 运行记录字段：`run_name`，`split_role`，`metric_name`，`config_version`，`train_proto_version`，`eval_proto_version`，`eval_cast_policy`，`boundary_metric_width`，`boundary_metric_impl`，`connected_components_impl`，`connected_components_connectivity`
- 验收方式：聚合前逐项校验 split、metric、seed 集合和协议字段；若 `threshold` 前 `dtype`、`Boundary F1` 宽度/实现或连通域实现字段任一不一致，即阻断汇总。

### 4.2 raw per-seed 表必须先于聚合表存在

- 当前结论：任何 `mean +- std` 聚合之前，必须先存在三次正式 run 的 raw per-seed 结果表。
- 规则类型：`工程冻结规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 核心公式或定义参考：`aggregation = single_seed` 用于逐 run 原始结果层，`aggregation = mean+-std` 只用于聚合层
- 采用原因：没有 raw 表，就无法回查异常 run 来源，也无法验证均值和标准差是否由正式三次结果真实生成。
- 不采用的相邻方案：不采用只在 markdown 中写几行示例；不采用只保留最终均值；不采用从截图或人工抄录反推 raw 值。
- 代码落点：reports/tables/unet_seed_results.csv，`collect_unet_seed_results()`
- 运行记录字段：`run_name`，`seed`，`metric_name`，`metric_value`，`result_tag`，`aggregation`
- 验收方式：检查 reports/tables/unet_seed_results.csv 是否覆盖三个正式 seed、两个 split 和最小指标集。

### 4.3 聚合表必须显式携带结果身份字段

- 当前结论：`mean +- std` 聚合表必须显式记录 `result_tag = reproduced`、`aggregation = mean+-std`、`n_runs = 3`、`seeds = 3407,1234,2025`。
- 规则类型：`工程冻结规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`，`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`
- 核心公式或定义参考：聚合身份固定为 `reproduced + mean+-std + 3 runs`
- 采用原因：结果身份不显式落字段，下游就无法区分单次值、正式重复值和后续阶段对比值。
- 不采用的相邻方案：不采用只写 `mean/std` 不写身份；不采用只在表标题写“三次平均”而不落列；不采用把 seeds 藏进注释。
- 代码落点：reports/tables/unet_mean_std_summary.csv，`build_mean_std_summary()`，`aggregate_seed_metrics()`
- 运行记录字段：`mean`，`std`，`n_runs`，`seeds`，`result_tag`，`aggregation`
- 验收方式：聚合表逐行检查身份字段是否齐全且取值固定。

### 4.4 split 与指标必须分开报告

- 当前结论：`TestA`、`TestB` 必须分开统计；`F1`、`Object Dice`、`Object Hausdorff`、`Dice`、`IoU` 必须逐指标独立统计。
- 规则类型：`评估口径继承规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`，`结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`
- 核心公式或定义参考：统计粒度固定为 `(split_role, metric_name)` 二元组
- 采用原因：`TestA / TestB` 难度不同，指标方向也不同，混合后会掩盖真实波动结构。
- 不采用的相邻方案：不采用 `GlaS overall mean`；不采用不同指标加权合成“总分”；不采用把 `Object Hausdorff` 按越大越好解释。
- 代码落点：testA_metrics.csv，testB_metrics.csv，`aggregate_seed_metrics()`
- 运行记录字段：`split_role`，`metric_name`，`metric_value`
- 验收方式：结果表按 split 和 metric 展开后，每个二元组都能追溯到三个 raw 值。

### 4.5 波动解释必须绑定错误模式与异常 run

- 当前结论：统计文字不能只报 `mean +- std`，必须同时交代主要错误模式、异常 run 是否存在、以及波动是否可解释。
- 规则类型：`实验解释规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`，`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md`
- 核心公式或定义参考：`std` 只描述离散程度，不自动等价于“模型更好”或“模型更差”
- 采用原因：稳定性阶段的目标是建立可解释的波动范围，而不是把标准差当作装饰数字。
- 不采用的相邻方案：不采用“标准差不大，所以模型很好”这种空洞表述；不采用只写均值不写错误模式；不采用发现异常 run 后仍按正常波动总结。
- 代码落点：reports/stage_reports/unet_stability_note.md，`write_unet_stability_note()`
- 运行记录字段：`metric_name`，`mean`，`std`，`note`，`failure_type`
- 验收方式：阶段文字总结必须同时引用聚合值、错误模式摘要和异常 run 裁决状态。

### 4.6 统计结果必须可交接到验收与下游 baseline

- 当前结论：只有 raw 表完整、聚合表完整、异常 run 已裁决、统计解释已落盘时，才允许把结果交给 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\03_阶段验收.md` 和下游 baseline 阶段。
- 规则类型：`同层交接规则 + 下游交付规则`
- 适用阶段：`03_UNet稳定性`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`，`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`
- 核心公式或定义参考：`handoff_stats_ready = raw_ready and aggregate_ready and proto_consistent and abnormal_runs_resolved`
- 采用原因：验收和 baseline 不应反向替本文件补 schema、补字段、补解释。
- 不采用的相邻方案：不采用只交一个 `mean +- std` 表；不采用只交 markdown 结论不给 csv；不采用边验收边回填统计字段。
- 代码落点：reports/tables/unet_seed_results.csv，reports/tables/unet_mean_std_summary.csv，reports/stage_reports/unet_stability_note.md
- 运行记录字段：`handoff_ready`，`result_tag`，`aggregation`，`n_runs`
- 验收方式：同层验收前检查三个正式交付物是否齐全，且字段与正文一致。

---

## 5. 统计对象与一致性校验

### 5.1 当前唯一合法的统计对象

当前 `mean +- std` 只允许作用于：

- 同一协议下的三个正式 seed。
- 同一个 split。
- 同一个指标。

例如：

- `TestA` 上的 `F1`
- `TestB` 上的 `Object Dice`
- `TestB` 上的 `Object Hausdorff`

都必须分别在三个正式 seed 的对应结果上单独统计。

### 5.2 当前不允许混算的内容

不允许把下面内容混在一起统计：

- `TestA` 和 `TestB`
- 不同 `threshold_value`
- 不同 `eval_proto_version`
- 不同 `eval_cast_policy`
- 不同 `boundary_metric_width`
- 不同 `boundary_metric_impl`
- 不同 `connected_components_impl`
- 不同 `connected_components_connectivity`
- 不同 `postprocess_version`
- 单次异常补跑与正式三次 run
- `A1` 排雷结果与 `A2` 正式重复结果

### 5.3 汇总前必须一致的字段

进入统计前至少必须核对下面字段完全一致：

- `config_version`
- `data_proto_version`
- `train_proto_version`
- `aug_version`
- `eval_proto_version`
- `model_version`
- `loss_version`
- `postprocess_version`
- `best_selector`
- `threshold_source`
- `threshold_value`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`

### 5.4 当前正式汇总的最小指标集

在 `UNet` 稳定性阶段，至少对下面指标做 `mean +- std` 汇总：

- `F1`
- `Object Dice`
- `Object Hausdorff`
- `Dice`
- `IoU`

如果 `HD95` 已稳定导出，也允许一并统计，但不得替代上述最小指标集。

---

## 6. raw per-seed 表规则

### 6.1 raw 表的正式职责

raw per-seed 表负责保存事实层原始结果，它必须先于聚合层存在，并承担下面三项职责：

1. 保留三次正式 run 的 split 级、指标级原始值。
2. 为后续 `mean +- std` 聚合提供唯一合法输入。
3. 为异常 run 回查和统计解释提供证据层入口。

### 6.2 raw 表的建议文件落点

当前阶段 raw 表统一落到：

- reports/tables/unet_seed_results.csv

同一项目内不再并行维护另一份口径不一致的“私人统计表”。

### 6.3 raw 表最小字段

raw per-seed 表至少要有：

- `run_name`
- `stage`
- `dataset`
- `model_name`
- `config_version`
- `data_proto_version`
- `train_proto_version`
- `eval_proto_version`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `seed`
- `split_role`
- `metric_name`
- `metric_value`
- `best_selector`
- `threshold_source`
- `threshold_value`
- `checkpoint_path`
- `result_tag`
- `aggregation`
- `note`

### 6.4 raw 表示意

| run_name | model_name | dataset | split_role | seed | metric_name | metric_value | config_version | eval_proto_version | eval_cast_policy | boundary_metric_width | boundary_metric_impl | connected_components_impl | connected_components_connectivity | threshold_value | result_tag | aggregation |
|----------|------------|---------|------------|------|-------------|--------------|----------------|--------------------|------------------|-----------------------|----------------------|---------------------------|-----------------------------------|-----------------|------------|-------------|
| `A2_UNet_GlaS_v1_seed3407` | `UNet` | `GlaS` | `TestA` | `3407` | `F1` | `...` | `v1` | `eval_proto_v1` | `float32_before_threshold` | `3px` | `find_boundaries+binary_dilation` | `scipy.ndimage.label` | `8` | `...` | `reproduced` | `single_seed` |
| `A2_UNet_GlaS_v1_seed1234` | `UNet` | `GlaS` | `TestA` | `1234` | `F1` | `...` | `v1` | `eval_proto_v1` | `float32_before_threshold` | `3px` | `find_boundaries+binary_dilation` | `scipy.ndimage.label` | `8` | `...` | `reproduced` | `single_seed` |
| `A2_UNet_GlaS_v1_seed2025` | `UNet` | `GlaS` | `TestA` | `2025` | `F1` | `...` | `v1` | `eval_proto_v1` | `float32_before_threshold` | `3px` | `find_boundaries+binary_dilation` | `scipy.ndimage.label` | `8` | `...` | `reproduced` | `single_seed` |

`TestB` 与其它指标同理分别保留，不允许只保留“代表性几行”。

### 6.5 raw 表固定写法

在 `A2` 阶段：

- `result_tag` 固定写 `reproduced`
- `aggregation` 固定写 `single_seed`
- `run_name` 只能来自三次正式 run 名

---

## 7. 聚合表规则

### 7.1 聚合表的正式职责

聚合表负责把 raw 层的三次正式结果按固定粒度转换为：

- 可直接进入阶段验收的 `mean +- std` 结果
- 可直接进入论文主表和后续 baseline 对照表的结构化记录

### 7.2 聚合表的建议文件落点

当前阶段聚合表统一落到：

- reports/tables/unet_mean_std_summary.csv

### 7.3 聚合表最小字段

聚合表至少要有：

- `model_name`
- `dataset`
- `split_role`
- `metric_name`
- `mean`
- `std`
- `n_runs`
- `seeds`
- `config_version`
- `train_proto_version`
- `eval_proto_version`
- `eval_cast_policy`
- `boundary_metric_width`
- `boundary_metric_impl`
- `connected_components_impl`
- `connected_components_connectivity`
- `result_tag`
- `aggregation`

### 7.4 聚合表示意

| model_name | dataset | split_role | metric_name | mean | std | n_runs | seeds | config_version | eval_proto_version | eval_cast_policy | boundary_metric_width | boundary_metric_impl | connected_components_impl | connected_components_connectivity | result_tag | aggregation |
|------------|---------|------------|-------------|------|-----|--------|-------|----------------|--------------------|------------------|-----------------------|----------------------|---------------------------|-----------------------------------|------------|-------------|
| `UNet` | `GlaS` | `TestA` | `F1` | `...` | `...` | `3` | `3407,1234,2025` | `v1` | `eval_proto_v1` | `float32_before_threshold` | `3px` | `find_boundaries+binary_dilation` | `scipy.ndimage.label` | `8` | `reproduced` | `mean+-std` |
| `UNet` | `GlaS` | `TestB` | `Object Dice` | `...` | `...` | `3` | `3407,1234,2025` | `v1` | `eval_proto_v1` | `float32_before_threshold` | `3px` | `find_boundaries+binary_dilation` | `scipy.ndimage.label` | `8` | `reproduced` | `mean+-std` |

### 7.5 聚合表固定写法

在 `A2` 阶段：

- `result_tag` 固定写 `reproduced`
- `aggregation` 固定写 `mean+-std`
- `n_runs` 固定写 `3`
- `seeds` 固定写 `3407,1234,2025`

---

## 8. 结果表达与文字解释规则

### 8.1 当前统一数值写法

当前建议统一写成：

- `mean +- std`

例如：

- `0.842 +- 0.006`
- `84.2 +- 0.6`

### 8.2 当前允许的格式边界

只要同一张表里的数字口径统一，就可以：

- 全部用 `0.xxx`
- 或全部用百分数

但不能混写。

### 8.3 当前不允许的写法

不允许：

- 均值一列用百分数，标准差一列用小数
- 同表里一部分写 `mean +- std`，另一部分只写 best
- 聚合表没有 `n_runs`
- 聚合表没有 `seeds`
- 聚合表不写 `result_tag / aggregation`

### 8.4 当前如何解释波动

统计文字至少要同时回答下面三件事：

1. 均值水平处在什么范围。
2. 标准差是否处于可解释波动内。
3. 最主要错误模式是否跨 seed 保持一致。

### 8.5 当前更值得关注的异常

如果出现下面情况，要提高警惕：

- 某一个 seed 明显远离另外两个。
- `TestB` 波动远大于 `TestA`。
- 某个主指标和其它指标方向冲突严重。
- 某次 run 的可视化与数值判断不一致。

### 8.6 当前错误的解释方式

不允许只写：

- “标准差不大，所以模型很好。”

更好的写法是：

- 说明均值水平。
- 说明波动是否可接受。
- 说明 `small_gland_miss`、`adhesion_split_fail`、`boundary_blur`、`testB_harder` 是否跨 seed 一致出现。
- 若存在异常 run，说明它是否已被裁决为 bug、协议漂移或真实波动。

---

## 9. 回退条件

### 9.1 独立回退触发条件

只要出现下面任意一条，本文件负责的统计与汇总流程就必须先回退处理，不能直接流入 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\03_阶段验收.md` 或下游 baseline：

- raw 表缺失某个正式 seed、某个 split 或某个最小指标。
- 聚合前发现三次 run 的协议字段不一致。
- 聚合值无法回查到 raw 表，或 raw 表无法回查到正式 run 资产。
- 某个异常 run 还未完成裁决，却已经被写入正式 `mean +- std` 结果。
- 统计文字只给均值，不解释波动、错误模式或异常 run。
- `result_tag / aggregation / n_runs / seeds` 等身份字段缺失或取值漂移。
- `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 未落入 raw 表、聚合表或聚合前一致性校验字段。

### 9.2 固定回退顺序

发生回退时，统一按下面顺序检查：

1. 检查三次正式 run 身份是否仍对应 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\01_三次重复设计.md` 的正式清单。
2. 检查协议字段是否与 `A1` 和 `A2` 阶段冻结规则一致。
3. 检查 raw 表是否完整且与正式 run 资产一致。
4. 检查聚合逻辑是否只按“同一协议、同一 split、同一指标、三个正式 seed”执行。
5. 检查统计文字是否正确引用异常 run 裁决和错误模式总结。

### 9.3 回退后的重新放行条件

回退后，只有同时满足下面条件，才允许恢复“可进入验收 / 可交给下游”的状态：

- raw 表与聚合表已按固定 schema 补齐。
- 协议一致性校验重新通过。
- 异常 run 已完成裁决并留痕。
- 统计文字已经绑定错误模式与波动解释。
- 当前结果重新满足第 `4.6` 节的交接条件。

---

## 10. 代码落地接口

### 10.1 raw per-seed 汇总入口

- 代码文件：scripts/summarize_stage.py，reports/tables/unet_seed_results.csv
- 入口类/函数：`collect_unet_seed_results()`
- 输入：三个正式 run 的 run_meta.yaml、testA_metrics.csv、testB_metrics.csv、summaries/error_cases.md
- 输出：逐 seed 原始结果表
- `dtype`：`seed` 与 `n_runs` 为 `int`；指标为 `float32`；协议字段与标签为字符串
- 依赖配置：`config_version`，`data_proto_version`，`train_proto_version`，`eval_proto_version`，`threshold_value`，`eval_cast_policy`，`boundary_metric_width`，`boundary_metric_impl`，`connected_components_impl`，`connected_components_connectivity`，`result_tag`，`aggregation`
- 前置断言：参与汇总的 run 必须协议一致、状态正常、split 结果齐全且已完成异常 run 裁决；若 run_meta.yaml 缺少评估实现硬字段，则 raw 表不得生成正式记录
- 运行产物：reports/tables/unet_seed_results.csv

### 10.2 `mean+-std` 聚合入口

- 代码文件：scripts/compare_runs.py，scripts/summarize_stage.py，reports/tables/unet_mean_std_summary.csv
- 入口类/函数：`build_mean_std_summary()`，`aggregate_seed_metrics()`
- 输入：raw per-seed 结果表
- 输出：聚合后的 `mean +- std` 结果表
- `dtype`：`mean/std` 为 `float32`；`n_runs` 为 `int`；`seeds` 与协议字段为字符串
- 依赖配置：`metric_name`，`split_role`，`config_version`，`train_proto_version`，`eval_proto_version`，`eval_cast_policy`，`boundary_metric_width`，`boundary_metric_impl`，`connected_components_impl`，`connected_components_connectivity`，`aggregation`
- 前置断言：只能按“同一协议、同一 split、同一指标、三个固定 seed”聚合；若 `eval_cast_policy`、`Boundary F1` 宽度/实现或连通域实现字段不一致，必须拒绝输出正式聚合表
- 运行产物：reports/tables/unet_mean_std_summary.csv

### 10.3 稳定性文字总结入口

- 代码文件：scripts/summarize_stage.py，reports/stage_reports/unet_stability_note.md
- 入口类/函数：`write_unet_stability_note()`
- 输入：聚合表、错误模式总结、异常 run 说明
- 输出：稳定性阶段文字解释
- `dtype`：文字说明为 `markdown`；统计值为 `float32`
- 依赖配置：`result_tag`，`aggregation`，`split_role`，`metric_name`，`failure_type`
- 前置断言：必须同时引用聚合结果、错误模式和异常 run 裁决；不能只根据单个最好 seed 写结论
- 运行产物：reports/stage_reports/unet_stability_note.md

### 10.4 统计交接校验入口

- 代码文件：scripts/summarize_stage.py，reports/stage_reports/unet_stability_stage_summary.md
- 入口类/函数：`validate_unet_stability_stage()`，`finalize_stage_a2_handoff()`
- 输入：raw 表、聚合表、稳定性文字总结、三次正式 run 元数据
- 输出：统计层交接状态、缺失项列表、是否允许进入阶段验收与下游 baseline
- `dtype`：状态字段为 `bool`；缺失项为字符串列表；计数字段为 `int`
- 依赖配置：`handoff_ready`，`n_runs`，`aggregation`，`result_tag`，`eval_cast_policy`，`boundary_metric_width`，`boundary_metric_impl`，`connected_components_impl`，`connected_components_connectivity`
- 前置断言：三个正式交付物必须同时存在，且字段与正文 schema 一致；若 handoff 前缺少任一评估实现硬字段，则不得标记 `handoff_ready = true`
- 运行产物：reports/stage_reports/unet_stability_stage_summary.md

---

## 11. 冲突裁决记录

- 冲突对象：旧稿中的统计口径停留在自然语言层，缺少显式 `result_tag / aggregation / n_runs / seeds / config_version / train_proto_version / eval_proto_version` 字段，也没有把 raw 表和聚合表正式收口到固定文件路径；同时未把 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 落入统计消费者字段链。
- 冲突来源：旧稿已经有“保留 raw per-seed results”和“生成 `mean +- std`”的基本想法，但没有把它提升到正式 schema、正式入口函数和正式交付物层级，也没有阻断“评估实现不同却被并表”的风险。
- 裁决结论：从现在开始，`A2` 阶段 raw 表统一落到 reports/tables/unet_seed_results.csv，聚合表统一落到 reports/tables/unet_mean_std_summary.csv，并显式记录 `config_version / train_proto_version / eval_proto_version / eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity / result_tag / aggregation / n_runs / seeds`。
- 裁决理由：如果统计细则继续只停留在“表格示意”，或不把评估实现硬字段写进 schema 与聚合前校验，后续 `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\03_阶段验收.md`、`04_Baseline` 及更后阶段就无法复用同一 schema，也无法严格区分单次值、正式重复值、协议版本和评估实现版本。
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/02_mean_std汇总规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/03_阶段验收.md`，`结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 是否需要回流修订：需要；若后续同层或下游文件仍使用“只写平均值”或缺字段的弱口径，必须按本文件 schema 同步回改。
- 代码实现影响：影响 scripts/summarize_stage.py、scripts/compare_runs.py、`reports/tables/*.csv` 和阶段交接校验逻辑。

---

## 12. 文件质量自检

- [x] 已在重写前重新遍历 `00_总览与规范` 全套，并把与当前文件相关的命名规范、评估口径、代码映射和质检要求真实落到正文。
- [x] 已补读 `02_路线与投稿`、`03_文献证据`、`02_UNet流程验证` 和同层 `00/01/03` 文件，而不是停在总览层。
- [x] 已显式写出 `本轮重写直接依赖的前置文件`，没有只在正文里零散借用上游结论。
- [x] 已按当前文件角色区分上游 / 同层 / 下游，并解释这些文件为什么与“统计与汇总细则”直接相关。
- [x] 已完成与同层已重写文件 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 的模板强度对照，确认当前文件的 `文件质量自检` 和 `Diagnostics 闭环` 没有缩水。
- [x] 当前版本按整篇重写执行，不是对旧稿补几段说明或补几张表格示意。
- [x] 已写清当前文件负责什么、不负责什么，以及为什么必须独立锁定 `A2` 的统计与汇总协议。
- [x] 已写清统计公式、统计对象、协议一致性边界和从 `A2` 开始必须使用 `mean +- std` 的原因。
- [x] 已把 `eval_cast_policy / boundary_metric_width / boundary_metric_impl / connected_components_impl / connected_components_connectivity` 显式落到聚合前一致性校验、raw 表 schema、聚合表 schema、回退条件和接口依赖字段。
- [x] 已把统计对象、raw 表、聚合表、split/metric 粒度、波动解释和交接条件写成正式规则卡片。
- [x] 每条核心规则都保留了 `当前结论 / 规则类型 / 适用阶段 / 直接依据 / 采用原因 / 不采用的相邻方案 / 代码落点 / 运行记录字段 / 验收方式`。
- [x] 关键术语、字段名、run 名、结果身份和版本名已与 `00_总览与规范`、`02_UNet流程验证`、`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/00_阶段总协议.md`、`结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 保持一致。
- [x] 已写清 `result_tag / aggregation / n_runs / seeds` 的固定写法，避免下游再猜结果身份。
- [x] 已写清 split 与指标必须分开统计，且聚合前必须先保留 raw per-seed 表。
- [x] 已写清波动解释必须绑定错误模式与异常 run，不能把 `std` 当作装饰数字。
- [x] 已写清独立 `回退条件`，没有把回退要求藏进验收或一句总结里顺带提到。
- [x] 已写清代码落地接口，接口对象细化到入口函数、I/O、依赖配置、前置断言和运行产物。
- [x] 已补写 `冲突裁决记录`，说明旧口径与新口径如何统一、影响哪些文件以及后续如何回流修订。
- [x] `文件质量自检` 与 `Diagnostics 闭环` 保持独立标题和完整结论写法，没有退化为一句“已检查”。
- [x] 当前文件在落盘后仍需执行回读和 diagnostics 复核，闭环动作不会被正文写作替代。
- [x] 当前文件已经达到“可直接指导结果汇总、阶段验收、下游 baseline 复用和论文结果表书写”的最低强度。

---

## 13. Diagnostics 闭环

- 本轮执行：整篇重写落盘后，必须先回读当前文件，再执行 IDE diagnostics 复核，不能写完即算完成。
- 复核范围：至少覆盖标题层级、表格结构、字段命名一致性、规则卡片完整性、同层交接术语以及是否存在可见 markdown 诊断问题。
- 通过条件：当前文件无新增未解决 diagnostics 问题时，方可声明本轮重写完成；若 diagnostics 报出问题，必须先回写修复再复核。
- 对照要求：本节保持与同层 `结直肠腺体分割_plan_优化版/01_实验执行/03_UNet稳定性/01_三次重复设计.md` 同等级的独立标题与闭环表达，不允许退化为“diagnostics 正常”一句话。

---

## 14. 一句话版本

> `结直肠腺体分割_plan_优化版\01_实验执行\03_UNet稳定性\02_mean_std汇总规则.md` 的正式职责已经固定为：在 `A1` 和 `A2` 已冻结的 `UNet` 协议之上，只允许对 `A2_UNet_GlaS_v1_seed3407 / seed1234 / seed2025` 三次正式 run 的 raw per-seed 结果按 `TestA / TestB` 与各指标分别生成 `mean +- std` 聚合表，并显式记录 `result_tag / aggregation / n_runs / seeds / 版本字段`，同时把异常 run 裁决和错误模式解释一起交付给阶段验收与下游 baseline。
