# GlaS划分协议

本文件不是对 `GlaS` 做“数据拆分说明”，而是把 `GlaS` 在当前项目里的正式 split 协议写成后续代码、实验、写作和验收都必须继承的唯一版本。

它要锁死的是：

- `GlaS` 在本项目里只承认哪四个正式 split
- 官方 `85 / 60 / 20` 边界如何被工程化冻结为 `train68 / val17 / testA60 / testB20`
- `train68 / val17` 如何一次性分层生成、记录版本并长期冻结
- 正式 `CSV` 应如何写 `sample_id`、相对路径、`grade` 与 `source_partition`
- 哪些检查通过后 split 才允许放行到 `crc_gland_segmentation_project/configs/data/glas.yaml`
- 什么行为属于违规重划，触发后必须如何回退

如果这一层不先压成正式协议，后面最危险的不是文件名写错，而是：

- 跑完一个模型后重新拆 `train / val`
- 把 `TestA / TestB` 合并成一个总值掩盖难度差异
- 不同阶段其实在不同 split 上比较，却误写成同一协议
- 训练入口绕过正式 `CSV`，回退到扫描原始目录

---

## 1. 文件角色与执行边界

当前文件负责冻结 `GlaS` 的唯一正式 split 协议、四个 split 的职责边界、`CSV` schema 和放行条件。

当前文件不负责展开六步检查细节、标签生成细节和下游训练实现；它只负责把 `GlaS` split 本身锁死。

## 2. 本轮直接依赖的前置文件

本轮直接依赖 `00_总览与规范`、路线层锁定文件、01_GlaS-Challenge.md、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md` 与 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`。

## 3. 本阶段唯一允许处理的变量

当前文件只允许处理 `official_train85 -> train68 + val17` 的工程冻结方式、`TestA / TestB` 的保留方式、`CSV` 字段与版本记录方式。

不允许在这里重开 benchmark 角色、标签规则、训练超参数和评估实现。

## 4. 阶段门控表达式

当前文件固定门控为：`pass_split_glas = pass_partition and pass_schema and pass_uniqueness and pass_check_gate`。

只有当 `GlaS` split 已通过六步检查并绑定正式配置时，才允许进入后续训练与验收消费链。

---

## 1. 文件定位

### 1.1 当前文件负责什么

当前文件负责冻结：

- `GlaS` 的正式 split 身份
- 四个 split 的职责边界
- `train68 / val17` 的生成、分层与随机性控制
- 正式 `CSV` schema、主键规则、路径规则与版本字段
- split 放行到正式配置前的最小门控条件

### 1.2 当前文件不负责什么

当前文件不负责：

- image / mask 配对细节与六步检查展开
- 二值标签、resize、边界图和距离图定义
- 训练超参数、模型结构与评估实现细节

这些内容分别由下列文件负责：

- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\05_标签转换与可视化规则.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- `02_UNet流程验证/*`

### 1.3 当前文件的真实目标

当前文件真正要解决的是：

> 让后面所有正式训练、验证、测试、结果汇总和论文写作都围绕唯一一套 `GlaS train68 / val17 / testA60 / testB20` 协议展开，而不是让 split 随模型、脚本或实验轮次漂移。

---

## 2. 本轮直接依赖的前置文件与执行边界

### 2.1 当前必须继承的固定前提

本文件必须继承下列已冻结前提：

- `GlaS` 是主 benchmark
- 官方测试边界必须保留 `TestA / TestB` 分开报告
- 官方 train `85` 允许在工程层拆出固定验证集
- 主结果表仍围绕 `F1 / Object Dice / Object Hausdorff`
- 下游数据访问只能通过 `configs/data/*.yaml -> splits/glas/*.csv -> dataset_root + relpath`

### 2.2 `00_总览与规范` 依赖

本轮重写直接继承以下总览规范：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`：要求当前文件按正式协议整篇重写，并显式写出前置文件、上下游、回退条件和 diagnostics 闭环
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`：要求 `splits/glas/*.csv`、`crc_gland_segmentation_project/configs/data/glas.yaml`、`reports/data_checks/*.md` 的工程身份和目录职责保持一致
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：固定 `GlaS train68 / val17 / testA60 / testB20`、`split_seed = 3407`、`best_selector = val_objdice_max` 和验证集阈值来源边界
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`：约束 `glas_split_version`、`sample_id_rule_version`、`split_csv_schema_version`、`threshold_source` 等运行记录字段命名
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：要求 `TestA / TestB` 保持独立测试身份，验证集负责 selector 与 threshold，测试集不得回调协议
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：要求把 split 生成、schema 校验、放行冻结和下游消费边界落到明确代码接口
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`：要求保留依据、验收、回退、代码落地接口、冲突裁决记录和文件质量自检
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`：要求当前文件在写盘后继续完成回读、diagnostics 和同批模板强度对照

### 2.3 `02_路线与投稿` 与 `03_文献证据` 依赖

本轮重写直接使用以下路线与文献依据：

- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`

这些文件共同决定：`GlaS` 是主 benchmark，官方 `TestA / TestB` 必须保留，工程内部需要固定 `val17` 作为验证集，但这种内部验证集生成必须被明确记录为项目工程冻结，而不是被误写成官方 split 本身。

### 2.4 当前文件允许锁什么，禁止重开什么

当前文件只允许锁：

- `GlaS` split 定义
- split 职责边界
- `CSV` schema、主键与路径规则
- split 生成、放行和重划禁令

当前文件不允许借机重开：

- 标签规则
- 输入尺寸
- normalize
- 训练 seed
- optimizer / scheduler
- checkpoint selector
- threshold 搜索空间

### 2.5 本轮相关文件遍历与角色说明

本文件属于 `B 类：数据协议类`，因此不能只列参考文件名，还必须说明上游、同层和下游文件为什么直接相关。

#### 上游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`：决定 `GlaS` 正式 split 已冻结为 `train68 / val17 / testA60 / testB20`，当前文件只能把它压成实现协议，不能重新找候选。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`：决定 `TestA / TestB` 必须分开，阈值只能来自验证集，因此当前文件必须把 `val17` 与 `testA / testB` 的职责边界写死。
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`：决定 split 必须通过 `crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`、`splits/glas/*.csv` 和 `crc_gland_segmentation_project/configs/data/glas.yaml` 落地，当前文件必须把接口粒度写够。
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`：决定数据阶段必须先完成 split 固定，且 `GlaS` 的工程验证需要保留独立验证集。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`：提供官方 `85 / 60 / 20` 边界、`TestA / TestB` 身份和对象级协议传统，是本文件最核心的 benchmark 来源。
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`：证明后续腺体任务论文会延续 `GlaS A / B` 分开汇报，也说明工程内部保留验证集是合理做法，但不能把其训练 recipe 误写成官方 split。

#### 同层文件

- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`：提供数据阶段总门控与下游唯一消费链，本文件必须与它保持完全一致。
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`：决定 `dataset_root` 的唯一身份，本文件必须据此限定 `crc_gland_segmentation_project/datasets/01_GlaS_official_raw` 为唯一正式数据源。
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`：负责六步检查闭环，本文件必须把 split 放行与该门控绑定，而不是只写“生成 CSV 即完成”。
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\04_CRAG划分协议.md`：与本文件共同构成数据阶段两套 split 协议，本文件需要和它对齐 `CSV schema / 放行 / manifest` 的口径。
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md` 与 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`：决定本文件生成的 split 资产何时才算正式交付、何时允许进入 `UNet`。

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`：它是当前文件最直接的消费者，必须显式继承本文件冻结后的 `train68 / val17 / testA60 / testB20`，并且只允许从正式配置和正式 `CSV` 读取。
- `02_UNet流程验证/*` 细则文件：后续训练、验证、测试和可视化都要依赖这里的 split 边界，因此本文件必须提前阻断“训练入口自己扫目录”的旧习惯。
- 后续 `03_UNet稳定性/*`、`04_Baseline/*`、`05_LKMA/*`、`06_Boundary/*`、`07_Distance/*`：它们默认共享同一数据入口，本文件必须保证 split 永不随模型阶段漂移。

这里的实际含义是：

- 上游文件负责给本文件提供 benchmark 边界、评估约束和工程落点
- 同层文件负责把本文件的 split 协议接成检查、产物和验收闭环
- 下游文件负责消费本文件冻结的正式 split，因此本文件必须优先回答“它们只能怎么读、什么时候允许读、读之前必须满足什么”

---

## 3. 当前唯一有效的 `GlaS` 划分

### 3.1 正式 split 主规则

#### `GlaS` split 主规则

- 当前结论：`GlaS` 固定采用 `official_train85 -> train68 + val17`，并保留 `TestA60` 与 `TestB20` 作为不可破坏的官方测试边界
- 当前值或最终版本：`glas_split_v1`
- 候选范围：`train68 / val17 / testA60 / testB20`
- 规则类型：`官方协议固定项 + 工程冻结规则`
- 直接依据：01_GlaS-Challenge.md，04_MILD-Net.md，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`
- 核心公式或定义参考：`official_train = 85`；工程内部一次性生成 `StratifiedSplit(official_train85, label=grade, ratio=68/17, seed=3407)`；测试边界固定保持 `TestA = 60`, `TestB = 20`
- 采用原因：既保留官方 benchmark 的测试边界，又给后续 `best checkpoint` 选择和阈值冻结提供固定验证集
- 不采用的相邻方案：不采用 `train70 / val15`；不采用 `5-fold`；不采用把 `TestA + TestB` 合并成单一正式测试值
- 适用阶段：`01_数据协议` 起生效，后续全部模型阶段继承
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`splits/glas/*.csv`，`crc_gland_segmentation_project/configs/data/glas.yaml`
- 运行记录字段：`split_seed`, `grade_csv_version`, `glas_split_version`, `source_partition_rule_version`
- 验收方式：检查四个正式 `CSV` 样本数为 `68 / 17 / 60 / 20`；检查 `sample_id` 不跨 split 重复；检查 `TestA / TestB` 未回流训练或验证

### 3.2 后面正式实验只承认这四个 split

从现在开始，后面正式实验中 `GlaS` 只承认：

- `train68`
- `val17`
- `testA60`
- `testB20`

当前明确不允许再出现：

- `train70 / val15`
- `5-fold`
- `official_train85` 直接兼作训练和验证却不留固定 `val`
- 合并 `TestA + TestB` 直接报一个总值替代正式结果

### 3.3 这样划分的依据

当前协议不是为了“凑四个好看的文件名”，而是同时满足三件事：

1. 对齐 `GlaS Challenge` 的官方测试边界
2. 对齐路线层要求的数据阶段固定验证集
3. 对齐后续 `UNet -> baseline -> 模块阶段` 统一的 checkpoint 与阈值来源

因此，这里的 `train68 / val17 / testA60 / testB20` 不是任意工程习惯，而是：

- 保留 benchmark 官方测试边界
- 把工程验证职责从测试集剥离出去
- 为后续跨模型公平比较建立同一数据输入层

---

## 4. 四个 split 的职责边界

### 4.1 `train68` 职责规则

- 当前结论：`train68` 只承担训练与训练增强职责，不参与正式测试结论
- 当前值或最终版本：`glas_train_role_v1`
- 候选范围：`training only`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，02_结直肠腺体分割_分阶段实验路线与执行标准.md
- 核心公式或定义参考：`train68` 只进入 `fit(model, train_loader)`，不进入正式测试汇总链
- 采用原因：把训练样本和正式结论样本严格分开，避免后续把收敛观察误写成测试证据
- 不采用的相邻方案：不采用从 `train68` 里临时挑一部分充当“额外测试”；不采用训练阶段直接查看 `TestA / TestB`
- 适用阶段：`01_数据协议` 起生效
- 代码落点：`crc_gland_segmentation_project/splits/glas/glas_train68.csv`，`crc_gland_segmentation_project/configs/data/glas.yaml`
- 运行记录字段：`train_split_name`, `train_num_samples`
- 验收方式：检查正式 `config` 把 `train68` 只用于训练 dataloader；检查主结果表不出现 `train68`

### 4.2 `val17` 职责规则

- 当前结论：`val17` 只承担验证、早停、学习率调度观察、模型选择与阈值冻结职责，不得充当正式测试集
- 当前值或最终版本：`glas_val_role_v1`
- 候选范围：`validation only`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- 核心公式或定义参考：后续验证链固定围绕 `best_epoch = argmax_t ObjDice(val17, epoch=t)`；`threshold_source = val17`
- 采用原因：后续 `best checkpoint` 与正式阈值必须建立在固定验证集上，而不是依赖测试集回调
- 不采用的相邻方案：不采用把 `val17` 写进正式主结果表；不采用看完 `val17` 后再重划 split
- 适用阶段：`01_数据协议` 起生效，全部模型阶段继承
- 代码落点：`crc_gland_segmentation_project/splits/glas/glas_val17.csv`，`crc_gland_segmentation_project/configs/data/glas.yaml`，[project_root]/src/eval/checkpoint_selector.py
- 运行记录字段：`val_split_name`, `best_selector`, `threshold_source`
- 验收方式：检查 `val17` 只出现在验证链；检查主表与测试资产不混入 `val17`

### 4.3 `testA60` 职责规则

- 当前结论：`testA60` 是正式测试子集之一，必须独立产出指标、预测和可视化
- 当前值或最终版本：`glas_testA_role_v1`
- 候选范围：`official test subset`
- 规则类型：`官方协议固定项 + 工程冻结规则`
- 直接依据：01_GlaS-Challenge.md，04_MILD-Net.md
- 核心公式或定义参考：正式结果链必须包含 `Report(TestA60, metric_k)`
- 采用原因：`TestA` 是官方 benchmark 的组成部分，必须保留可回溯的 split 级证据，而不是被合并吞掉
- 不采用的相邻方案：不采用只在最终表里保留一个“overall GlaS”单值；不采用把 `testA60` 回用于阈值或 checkpoint 调整
- 适用阶段：`01_数据协议` 起生效
- 代码落点：`crc_gland_segmentation_project/splits/glas/glas_testA60.csv`，testA_metrics.csv
- 运行记录字段：`test_split_name`, `metrics_version`
- 验收方式：检查 testA_metrics.csv 和 `visuals/testA/` 独立存在；检查 `testA60` 不回流训练或验证

### 4.4 `testB20` 职责规则

- 当前结论：`testB20` 是正式困难测试子集，必须与 `testA60` 分开报告，不能被平均值掩盖
- 当前值或最终版本：`glas_testB_role_v1`
- 候选范围：`hard subset report`
- 规则类型：`官方协议固定项 + 工程冻结规则`
- 直接依据：01_GlaS-Challenge.md，04_MILD-Net.md
- 核心公式或定义参考：正式结果链必须同时包含 `Report(TestA60, metric_k)` 与 `Report(TestB20, metric_k)`
- 采用原因：`TestB` 更容易暴露恶性样本、边界模糊和对象黏连问题，是后续错误分析的重要证据来源
- 不采用的相邻方案：不采用 `TestA + TestB` 合成单值替代正式记录；不采用只汇报 `TestA`
- 适用阶段：`01_数据协议` 起生效
- 代码落点：`crc_gland_segmentation_project/splits/glas/glas_testB20.csv`，testB_metrics.csv
- 运行记录字段：`test_split_name`, `metrics_version`, `difficulty_note`
- 验收方式：检查 `TestA / TestB` 分别出现在结果文件、汇总表和可视化目录中；检查 `TestB` 未被拿回训练或验证

---

## 5. `train68 / val17` 的正式生成规则

### 5.1 生成总原则

`train68 / val17` 必须从官方 train `85` 中一次性固定生成。

生成后必须同时完成：

- 写入正式 `CSV`
- 记录 split seed、Grade.csv 版本和脚本版本
- 生成 split 摘要报告
- 后续整个项目默认不再改

### 5.2 分层抽样规则

#### 分层抽样规则

- 当前结论：`train68 / val17` 必须按 Grade.csv 中的 `benign / malignant` 做分层抽样
- 当前值或最终版本：`glas_stratified_split_v1`
- 候选范围：`grade-stratified split`
- 规则类型：`工程冻结规则`
- 直接依据：01_GlaS-Challenge.md，04_MILD-Net.md，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`
- 核心公式或定义参考：`StratifiedSplit(official_train85, label=grade, ratio=68/17, seed=3407)`
- 采用原因：`GlaS` 良恶性比例本身不完全均衡；不分层会让 `val17` 偏向某一类，导致后续波动难解释
- 不采用的相邻方案：不采用纯随机拆分却不记录标签分布；不采用人工手调 split；不采用按文件名顺序截断
- 适用阶段：`01_数据协议`
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`crc_gland_segmentation_project/reports/data_checks/glas_split_report.md`
- 运行记录字段：`split_seed`, `grade_distribution_train68`, `grade_distribution_val17`
- 验收方式：检查 `train68 / val17` 都包含良恶性样本；检查比例无明显漂移；检查报告中包含分层摘要

### 5.3 类别比例与接受范围

按官方 train `85` 的传统口径，内部拆分时优先维持近似比例：

- `train68`：约 `30` 个 benign、`38` 个 malignant
- `val17`：约 `7` 个 benign、`10` 个 malignant

如果 Grade.csv 的实际统计与上述口径有轻微出入，以正式读取结果为准，但必须满足：

- `train68` 与 `val17` 都保留良恶性样本
- 类别比例不发生明显漂移
- 差异可在 split 报告中解释

### 5.4 随机性控制与版本记录

#### split seed 与版本记录规则

- 当前结论：第一次生成 `train68 / val17` 时必须同时记录 `split_seed = 3407`、`grade_csv_version`、脚本版本和生成日期
- 当前值或最终版本：`glas_split_seed_v1`
- 候选范围：`single deterministic split seed`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`
- 核心公式或定义参考：`split_seed` 是数据划分 seed；训练重复 seed 另行记录为 `3407 / 1234 / 2025`
- 采用原因：必须把数据划分随机性和训练随机性明确拆开，否则后续结果无法判断波动来源
- 不采用的相邻方案：不采用每次导出 `CSV` 都重新随机；不采用只记训练 seed 不记 split seed
- 适用阶段：`01_数据协议`
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`splits/glas/*.csv`，`crc_gland_segmentation_project/reports/data_checks/glas_split_report.md`
- 运行记录字段：`split_seed`, `grade_csv_version`, `split_script_version`, `split_export_date`
- 验收方式：检查正式 split 报告和数据配置显式记录上述字段；检查后续训练 run 能回指到固定 split 版本

---

## 6. 正式 `CSV`、主键与路径规则

### 6.1 当前最小正式文件集

后面必须生成下面四个文件：

- `crc_gland_segmentation_project/splits/glas/glas_train68.csv`
- `crc_gland_segmentation_project/splits/glas/glas_val17.csv`
- `crc_gland_segmentation_project/splits/glas/glas_testA60.csv`
- `crc_gland_segmentation_project/splits/glas/glas_testB20.csv`

### 6.2 `CSV` schema 规则

#### `GlaS` `CSV` schema 规则

- 当前结论：每个 `GlaS` 正式 `CSV` 必须至少包含 `sample_id`, `image_relpath`, `mask_relpath`, `dataset`, `split`, `grade`, `source_partition`
- 当前值或最终版本：`glas_csv_schema_v1`
- 候选范围：`official split csv schema`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md` 第 `4.4` 条，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`
- 核心公式或定义参考：正式读取链固定为 `config -> split_csv -> image_relpath/mask_relpath -> dataset_root`
- 采用原因：后面训练、评估、可视化、错误分析和写作都需要同一套可追溯样本字段
- 不采用的相邻方案：不采用只写 image 路径不写 `sample_id`；不采用不同 split 用不同字段集合；不采用路径列混入绝对路径
- 适用阶段：`01_数据协议` 起生效
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`splits/glas/*.csv`，`crc_gland_segmentation_project/src/data/csv_loader.py`
- 运行记录字段：`split_csv_schema_version`, `sample_id_rule_version`
- 验收方式：检查四个 `CSV` schema 完全一致；检查 `sample_id` 全局唯一；检查路径列只写工程根相对路径

### 6.3 正式主键规则

#### `sample_id` 规则

- 当前结论：正式样本主键固定为 `sample_id = dataset + "_" + source_partition + "_" + stem(image_filename)`
- 当前值或最终版本：`glas_sample_id_rule_v1`
- 候选范围：`deterministic file-name based sample id`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`
- 核心公式或定义参考：`sample_id` 必须由可回放的确定性命名映射构造，不能依赖运行时随机序号
- 采用原因：同一套主键要服务于 split 校验、训练记录、错误分析和最终论文图表索引
- 不采用的相邻方案：不采用按导出顺序编号；不采用人工单独维护一份编号表
- 适用阶段：`01_数据协议`
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`crc_gland_segmentation_project/src/data/csv_loader.py`
- 运行记录字段：`sample_id_rule_version`
- 验收方式：检查 `sample_id` 可从文件名和 `source_partition` 直接回放；检查跨 split 无重复

### 6.4 `source_partition` 与路径规则

当前固定写法如下：

- `dataset` 固定写 `GlaS`
- `split` 固定写 `train68 / val17 / testA60 / testB20`
- `source_partition` 固定写 `official_train / official_testA / official_testB`
- `image_relpath` 与 `mask_relpath` 只写工程根相对路径

允许的相对路径示例：

- `[dataset_example]/train_001.bmp`
- `[dataset_example]/train_001_anno.bmp`

明确不允许：

- 本机绝对路径
- 临时缓存路径
- 不带 `crc_gland_segmentation_project/datasets/` 根前缀的模糊相对路径

### 6.5 命名与自动配对规则

生成 `CSV` 前必须基于稳定文件名映射规则自动配对：

- 官方 train 图像：`train_*.bmp`
- 官方 train 标注：`train_*_anno.bmp`
- 官方 `TestA` 图像：`testA_*.bmp`
- 官方 `TestA` 标注：`testA_*_anno.bmp`
- 官方 `TestB` 图像：`testB_*.bmp`
- 官方 `TestB` 标注：`testB_*_anno.bmp`

当前明确不允许：

- 手工补几个例外样本却不记录
- 同时存在多套命名规则却不版本化
- 在 `CSV` 导出阶段临时硬编码单个样本特判

---

## 7. split 放行、冻结与重划禁令

### 7.1 split 放行规则

#### split 放行规则

- 当前结论：`GlaS` split 只有在 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md` 的六步检查闭环全部通过后，才允许写入 `crc_gland_segmentation_project/configs/data/glas.yaml`
- 当前值或最终版本：`glas_split_gate_v1`
- 候选范围：`check-gated split release`
- 规则类型：`工程冻结规则`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- 核心公式或定义参考：`pass_glas_split = pass_count and pass_pair and pass_readable and pass_foreground and pass_stats and pass_manual_audit`
- 采用原因：正式 split 不是“能生成就算完成”的中间产物，而是后续训练代码唯一允许消费的正式资产
- 不采用的相邻方案：不采用先把 `CSV` 接进训练、再慢慢补检查；不采用只凭终端输出判断通过
- 适用阶段：`01_数据协议`
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/check_dataset_pairs.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`crc_gland_segmentation_project/configs/data/glas.yaml`
- 运行记录字段：`data_check_version`, `glas_split_version`, `asset_manifest`, `handoff_ready`
- 验收方式：检查 split 报告中包含放行结论；检查 `crc_gland_segmentation_project/configs/data/glas.yaml` 只在六步检查通过后生成

### 7.2 当前不允许的重划行为

下面任何一种都视为违规：

- 跑完 `UNet` 后觉得结果不理想，再重划 `train / val`
- 看到 `TestB` 太差，把一部分 `TestB` 拿回训练
- 为某个外部模型单独再造一版 split
- 没记录 seed、Grade.csv 版本和脚本版本却重新导出 `CSV`
- 在下游训练代码里绕过正式 `CSV` 临时扫描目录

### 7.3 如果后面确实必须改 split

如果后面确实必须改 split，只能按下面顺序处理：

1. 先说明为什么现有 `glas_split_v1` 不再可用
2. 更新本文件和相关来源说明
3. 删除旧 `splits/glas/*.csv`
4. 重新生成 split 与检查资产
5. 重建 `crc_gland_segmentation_project/configs/data/glas.yaml`
6. 从新版本重新启动后续实验

这意味着：

- 改 split 不是局部修补
- 改 split 等价于数据协议版本升级
- 旧实验结果不得与新 split 结果混写

---

## 8. 下游消费与评估约束

### 8.1 下游唯一允许的数据消费链

后续 `UNet` 及其后续所有阶段，只允许按下面这条固定链读取 `GlaS`：

```text
configs/data/glas.yaml
-> splits/glas/*.csv
-> dataset_root + image_relpath/mask_relpath
-> 正式二值标签与派生标签
```

这里明确禁止：

- 在 `crc_gland_segmentation_project/scripts/train.py` 或任何下游脚本里重新扫描原始目录
- 因为缺某个中间资产就临时改读另一份本地副本
- 训练入口未检查数据阶段放行状态就直接开跑

### 8.2 `val17` 与 `testA60 / testB20` 的使用规则

`val17` 只允许用于：

- 验证指标观察
- early stopping
- learning rate 调度观察
- `best checkpoint` 选择
- 阈值冻结

`testA60 / testB20` 只允许用于：

- 正式测试
- 最终结果汇报
- 成功/失败案例导出
- 困难子集分析

明确不允许：

- 用 `TestA / TestB` 调阈值
- 用 `TestA / TestB` 选 `best checkpoint`
- 把 `TestA + TestB` 的平均值替代 split 级正式记录

### 8.3 与 `02_UNet流程验证` 的交接边界

本文件交给 `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md` 的不是“一个大概的 GlaS 数据说明”，而是：

- `4` 个正式 split `CSV`
- 固定的 `split_seed / glas_split_version / split_csv_schema_version`
- `val17` 只能做验证、`testA / testB` 只能做正式测试的职责边界
- split 已通过六步检查门控并允许进入正式配置的放行结论

如果下游还能绕开这里的资产链，本文件就不是真正的 gate。

---

## 9. 当前阶段最低检查清单

在 `GlaS` 划分阶段，至少要确认：

- `85` 个官方 train 样本全部可读
- Grade.csv 正常可读并覆盖官方 train `85`
- `train68 / val17` 分层成功且记录 seed
- `TestA60 / TestB20` 没有混进训练或验证
- 四个 `CSV` 的样本数分别正确
- 同一 `sample_id` 不会出现在多个 split
- `image_relpath / mask_relpath` 都能解析回正式数据根目录
- split 报告可回指当前 `glas_split_version`

---

## 10. 与后续代码工程的对应关系

这份协议后面会直接映射到：

- `crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`
- `splits/glas/*.csv`
- `crc_gland_segmentation_project/configs/data/glas.yaml`
- `crc_gland_segmentation_project/reports/data_checks/glas_split_report.md`
- `crc_gland_segmentation_project/reports/data_checks/duplicate_check_report.md`

代码层必须保证：

- 同一个脚本可重复生成相同 split
- 不依赖人工拖文件或人工改 `CSV`
- 同时输出样本数、类别分布和放行结论摘要
- schema 校验、唯一性校验和检查门控共用同一套版本字段

---

## 11. 回退条件

### 11.1 数据阶段内回退触发条件

只要出现下面任意一条，本文件对应的 `GlaS` split 协议就不得放行，必须先回退到当前文件和其上游数据阶段文件修正，而不是继续把问题带进 `UNet`：

- `train68 / val17 / testA60 / testB20` 任一正式 split 边界被改写
- `TestA / TestB` 被合并汇报、回流训练或回流验证
- Grade.csv 缺失、不可读，或其版本与当前 split 报告不一致
- `sample_id`、`image_relpath`、`mask_relpath`、`grade`、`source_partition` 与正式 `CSV` schema 脱节
- `crc_gland_segmentation_project/configs/data/glas.yaml` 在六步检查通过前就提前引用正式 split
- 下游训练入口绕开正式 `CSV`，重新扫描原始目录或临时重建另一版 `GlaS` split

### 11.2 下游异常时的强制回退顺序

如果 `02_UNet流程验证` 或更后阶段出现全背景预测、`val17` 与 `TestA / TestB` 异常分裂、测试结果与肉眼长期严重矛盾等问题，必须按下面顺序强制回退：

1. 检查 `glas_train68 / val17 / testA60 / testB20` 的 `CSV` 版本与样本数
2. 检查 `sample_id / image_relpath / mask_relpath / source_partition / grade` 是否还能回指原始样本
3. 检查 Grade.csv 的分层读取与 `split_seed = 3407` 是否被改写
4. 检查六步数据检查闭环是否真的在 split 放行前通过
5. 检查 `crc_gland_segmentation_project/configs/data/glas.yaml` 与 `asset_manifest` 是否仍只引用当前正式 split
6. 检查训练入口是否真的只通过正式 `CSV` 与正式配置消费 `GlaS`

### 11.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新把当前 `GlaS` split 标记为正式可交接资产：

- `splits/glas/*.csv` 已按当前正式版本重新导出
- glas_split_report.md、duplicate_check_report.md 与相关检查资产已同步更新
- `crc_gland_segmentation_project/configs/data/glas.yaml` 已回指新一轮正式 split 版本
- `asset_manifest`、`handoff_ready`、`data_stage_pass` 与 `next_action` 已完成重新登记
- 下游训练前预飞检查重新通过，且不再存在绕开正式 split 的兜底逻辑

---

## 12. 代码落地接口

### 11.1 `GlaS` split 生成入口

- 代码文件：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`
- 入口类/函数：`build_glas_split()`，`load_glas_grade_table()`，`stratified_train_val_split()`
- 输入：`dataset_root`，`grade_csv_path`，`split_seed = 3407`，官方 train/test 文件清单
- 输出：`train68 / val17 / testA60 / testB20` 的样本索引、split 元信息、正式 `CSV`
- `dtype`：文件路径和 split 字段为 `string/PathLike`；样本数与索引为 `int`；标签分布统计为 `int`
- 依赖配置：`glas_split_version`，`split_seed`，`grade_csv_version`，`split_csv_schema_version`，`sample_id_rule_version`
- 前置断言：`dataset_root` 必须指向 `crc_gland_segmentation_project/datasets/01_GlaS_official_raw`；Grade.csv 可读且覆盖官方 train `85`；`TestA / TestB` 不参与分层抽样；同一 `sample_id` 不得跨 split 重复
- 运行产物：`crc_gland_segmentation_project/splits/glas/glas_train68.csv`，`crc_gland_segmentation_project/splits/glas/glas_val17.csv`，`crc_gland_segmentation_project/splits/glas/glas_testA60.csv`，`crc_gland_segmentation_project/splits/glas/glas_testB20.csv`，`crc_gland_segmentation_project/reports/data_checks/glas_split_report.md`

### 11.2 `CSV` schema 与主键校验入口

- 代码文件：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`crc_gland_segmentation_project/src/data/csv_loader.py`
- 入口类/函数：`build_glas_sample_id()`，`validate_glas_csv_schema()`，`validate_glas_split_uniqueness()`
- 输入：样本文件名、`source_partition`、相对路径字段、正式 split `CSV`
- 输出：统一的 `sample_id`、schema 校验结果、重复样本与坏路径清单
- `dtype`：`sample_id` 与路径字段为 `string`；schema 校验状态为 `bool`
- 依赖配置：`split_csv_schema_version`，`sample_id_rule_version`，`dataset_root`
- 前置断言：四个 `CSV` 必须共享同一套 schema；`image_relpath` 与 `mask_relpath` 只允许写工程根相对路径；`sample_id` 在 `GlaS` 全数据范围内全局唯一
- 运行产物：`splits/glas/*.csv` 的 schema 校验通过记录，`crc_gland_segmentation_project/reports/data_checks/duplicate_check_report.md`

### 11.3 split 放行与冻结入口

- 代码文件：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/check_dataset_pairs.py`，`crc_gland_segmentation_project/configs/data/glas.yaml`
- 入口类/函数：`validate_glas_check_gate()`，`export_glas_split_config()`，`freeze_glas_split_manifest()`
- 输入：六步数据检查汇总、正式 split `CSV`、来源说明文件路径、当前 split 版本
- 输出：是否允许放行到 `crc_gland_segmentation_project/configs/data/glas.yaml` 的门控结论、可交接的 split manifest、与检查结果绑定的数据配置
- `dtype`：放行状态为 `bool`；版本、路径和配置字段为 `string`
- 依赖配置：`data_check_version`，`glas_split_version`，`dataset_source_note`，`dataset_role`
- 前置断言：只有在 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md` 的六步闭环全部通过后，才允许把 `splits/glas/*.csv` 写入正式数据配置；一旦发现测试集回流训练、`sample_id` 跨 split、Grade.csv 缺失或路径不可读，`next_action` 必须为 `rollback`
- 运行产物：`crc_gland_segmentation_project/configs/data/glas.yaml`，`crc_gland_segmentation_project/reports/data_checks/glas_split_report.md` 中的放行结论，`asset_manifest`

---

## 13. 冲突裁决记录

- 冲突对象：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\03_GlaS划分协议.md` 中 split 规则、放行逻辑与下游消费边界的组织方式
- 冲突来源：旧写法虽然已经具备 `train68 / val17 / testA60 / testB20`、分层抽样、`CSV` schema 和代码接口，但仍偏向“怎么拆分”的说明文，对“如何与六步检查门控绑定、如何进入正式配置、下游只能怎么消费”写得不够硬
- 裁决结论：本文件本轮统一改写为“正式 split 定义 -> 职责边界 -> 分层生成 -> `CSV` schema -> 放行冻结 -> 下游消费 -> 回退禁令”的完整协议；继续保留三类代码接口，但把 split 放行与 `crc_gland_segmentation_project/configs/data/glas.yaml`、`asset_manifest` 和 `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md` 的消费链显式绑死
- 裁决理由：如果 `GlaS` 划分文件继续只说明“怎么拆”，而不写清“什么时候才算正式 split、如何阻断下游扫目录、如何回退”，后面的 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md` 和 `02_UNet流程验证/*` 仍可能把 split 理解成可临时替换的中间产物
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`，`结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 是否需要回流修订：需要；后续进入 `02_UNet流程验证/*` 时，必须继续显式继承本文件新增的 split 放行、数据消费链与回退口径，不允许再次出现“CSV 缺失就扫描原始目录”的兜底逻辑
- 代码实现影响：影响 `crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_glas_split.py` 的接口拆分、`crc_gland_segmentation_project/src/data/csv_loader.py` 的 schema 校验逻辑、`crc_gland_segmentation_project/configs/data/glas.yaml` 的生成时机，以及 `crc_gland_segmentation_project/reports/data_checks/glas_split_report.md` 是否承担正式放行记录

---

## 14. 文件质量自检

- [x] 已在修改前重新遍历 `00_总览与规范`
- [x] 已完成最低前置阅读：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`
- [x] 已继续补读 `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
- [x] 已遍历 `02_路线与投稿` 的相关文件
- [x] 已遍历 `03_文献证据` 的相关正式深提取稿
- [x] 已检查 `01_实验执行` 全局相关文件，包括前面、同层和后面的内容
- [x] 已显式区分并记录上游 / 同层 / 下游文件的真实角色，而不是只列文件名
- [x] 对后续文件中的相关内容做了甄别，而不是机械继承
- [x] 当前版本按“整文件重写”而不是“局部补句”执行
- [x] 已区分 `官方协议固定项 / 路线层已锁定 / 论文支持的候选范围 / 工程冻结规则`
- [x] 已写清当前文件最核心规则的来源
- [x] 已写清为什么这样设计，而不是只给结论
- [x] 已写清公式、定义或原理解释（如果该文件涉及这些内容）
- [x] 公式、定义或原理已经达到“可直接翻译代码 + 可直接写入论文”的最低深度
- [x] 关键符号、术语、版本名和代码字段与前后文件保持一致
- [x] 已写清参数、结构、训练、评估或数据规则的作用
- [x] 已写清为什么不采用相邻方案
- [x] 已写清代码落点和运行记录字段
- [x] 代码落地对象已经细化到入口函数/类、I/O、配置字段和运行产物
- [x] 已把 split 放行、正式配置和下游唯一消费链写清
- [x] 已写清验收方式与独立 `回退条件`
- [x] 当前修改影响到的其它文件，已经列出并显式标记待继续回流修订
- [x] 所有 `待确认项` 都已写清关闭截止阶段、阻塞动作和回流修订要求；当前文件本轮无新增待确认项
- [x] `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md` `§7` 的检查项与一票否决项已同步核对
- [x] 已完成与同层最近合格文件的 `文件质量自检 / Diagnostics 闭环` 强度对照；当前文件以 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\04_CRAG划分协议.md` 为主强度参照，已补齐独立 `回退条件` 与独立 `Diagnostics 闭环`
- [x] 当前文件已完成 diagnostics，且无新增诊断问题
- [x] 当前文件已经达到“可直接指导代码与论文写作”的最小强度

---

## 15. Diagnostics 闭环

- 本轮执行：整篇回修后，已重新回读磁盘最终版，重点复核 `本轮重写直接依赖的前置文件`、`上游 / 同层 / 下游`、独立 `回退条件`、`代码落地接口`、`冲突裁决记录` 和 `文件质量自检` 是否全部落盘
- 本轮结果：当前文件的结构留痕与数据阶段门控链已经补齐，未再保留“把回退条件并入放行描述”的弱写法
- 闭环要求：只有在 IDE diagnostics 无新增未解决问题时，当前文件才允许继续作为 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md` 和 `02_UNet流程验证/*` 的正式前置文件

---

## 16. 一句话版本

> `GlaS` 的正式执行协议已经固定为：官方 train `85` 一次性按 Grade.csv 分层拆成 `train68 / val17`，并保留 `TestA60 / TestB20` 作为不可破坏的官方测试边界；后面任何训练、验证、测试、结果汇总和论文写作都必须围绕这四个正式 split、同一套 `CSV` schema、同一条正式数据消费链和同一条 split 放行门控展开，不允许中途随模型重划。

