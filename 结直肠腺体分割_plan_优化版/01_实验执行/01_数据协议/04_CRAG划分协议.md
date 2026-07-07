# CRAG划分协议

本文件不是“说明 `CRAG` 怎么分 train / val / test”的备忘，而是 `01_数据协议` 中负责冻结 `CRAG` 正式 split、正式放行顺序、正式交接资产与下游消费边界的执行协议。

它要先写死四件事：

- 当前项目只承认哪一版 `CRAG` 数据身份与目录边界
- 为什么执行层只承认 `train153 / val20 / test40`
- `train153` 如何由 `train_sup_16 + train_unsup_137` 在 `CSV` 层合并生成
- `CRAG` split 何时才允许写入 `crc_gland_segmentation_project/configs/data/crag.yaml` 并交给后续训练阶段消费

如果这一层不先压成正式协议，后面最危险的问题不是“某次结果略有波动”，而是某个模型私自改 split、训练池与验证测试边界漂移、`source_subset` 丢失，最终让 `CRAG` 失去第二 benchmark 的正式证据地位。

---

## 1. 文件角色与执行边界

当前文件负责冻结 `CRAG` 的正式执行身份、`train153 / val20 / test40`、`source_subset` 与正式放行链。

当前文件不负责展开六步检查、标签生成和模型训练细节；它只负责把 `CRAG` split 协议本身写成不可漂移的正式边界。

## 2. 本轮直接依赖的前置文件

本轮直接依赖 `00_总览与规范`、路线层锁定文件、04_MILD-Net.md、07_TA-Net.md、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md` 和 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`。

## 3. 本阶段唯一允许处理的变量

当前文件只允许处理 `CRAG` 正式执行版目录身份、`train153` 的合并规则、`CSV` schema、`source_subset` 字段和 split 放行顺序。

不允许在这里重开主 benchmark 角色、标签规则、训练结构或测试口径。

## 4. 阶段门控表达式

当前文件固定门控为：`pass_split_crag = pass_layout and pass_schema and pass_source_subset and pass_check_gate`。

只有当 `CRAG` split 已经完成 schema/source_subset 校验并通过六步检查闭环时，才允许写入正式配置并交给下游阶段消费。

---

## 1. 文件定位

### 1.1 当前文件负责什么

当前文件负责冻结以下内容：

- `CRAG` 的正式执行身份与目录边界
- `train153 / val20 / test40` 的唯一有效定义
- `train153` 的训练池合并规则
- `source_subset`、`sample_id`、路径字段与 `CSV` schema
- split 写入前的检查门控、放行字段与重划禁令
- `CRAG` 结果作为第二 benchmark 的下游消费边界

### 1.2 当前文件不负责什么

当前文件不负责重开以下内容：

- image / mask 的六步检查细节
- 二值标签、resize、可视化与派生标签规则
- `CRAG` 阶段的训练超参数、结构与评估实现

这些内容分别由下列文件展开：

- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\05_标签转换与可视化规则.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 后续 `09_CRAG验证/*`

### 1.3 当前文件的真实目标

当前文件真正要解决的问题不是“把 `CRAG` 勉强拆成三个子集”，而是把 `CRAG` 固定成后续整个项目都共同继承的同一套正式资产：

- 同一版本地整理副本
- 同一套 `train153 / val20 / test40`
- 同一套 `CSV` schema 与样本追溯字段
- 同一条“先生成 split -> 再校验 schema/source_subset -> 再通过检查门控 -> 最后写入正式配置”的放行链

只有这样，`CRAG` 才能稳定承担第二 benchmark 的补充验证职责。

---

## 2. 本轮直接依赖的前置文件与相关文件角色

### 2.1 当前文件必须继承的冻结前提

本文件必须继承下列上游固定边界：

- `CRAG` 当前执行资产固定为 `crc_gland_segmentation_project/datasets/02_CRAG_reorganized_local_copy`
- `CRAG` 在本项目中是第二 benchmark，不是主结论数据集
- 正式数据消费链固定为 `configs/data/*.yaml -> splits/*/*.csv -> dataset_root + relpath -> 正式标签`
- `best_selector = val_objdice_max`
- `threshold_source` 只能来自验证集，不能来自测试集
- 下游训练入口只允许消费已经通过数据阶段放行的正式资产

### 2.2 本轮重写直接依赖的前置文件

本轮已按协议重读并提取下列文件：

- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`
- `结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`
- `结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- `结直肠腺体分割_plan_优化版/02_路线与投稿/03_结直肠腺体分割_投稿层级自查与止损判断.md`
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/04_MILD-Net.md`
- `结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/07_TA-Net.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/01_数据源与目录约定.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/03_GlaS划分协议.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/05_标签转换与可视化规则.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`

### 2.3 上游 / 同层 / 下游文件的真实角色

#### 上游文件

- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`：给当前文件提供 `pass_split / pass_check / pass_handoff` 的阶段门控位置，本文件必须把 `CRAG` 的 split 放行条件写成可执行协议
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`：给当前文件提供 `CRAG` 本地整理版执行副本的正式身份，本文件必须保护这一目录边界
- `02_路线与投稿/*`：要求 `GlaS` 做主结论、`CRAG` 做第二 benchmark，因此本文件必须把 `CRAG` 写成补充验证数据而不是主调参场
- 04_MILD-Net.md 与 07_TA-Net.md：共同强化 `CRAG` 在腺体任务中的 benchmark 地位，因此本文件必须把 split、来源与使用边界写成硬协议

#### 同层文件

- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`：给本文件提供 split 写入前必须通过的六步检查门控
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\03_GlaS划分协议.md`：作为同层对照稿，要求本文件也必须把 split 写成正式冻结协议，而不是目录说明
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\05_标签转换与可视化规则.md`：要求本文件的路径与标签消费边界和 `mask > 0` 口径保持一致
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`：要求本文件把 `CRAG` split 视作正式交付资产的一部分，而不是临时中间文件
- `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`：要求本文件的放行结论能直接进入数据阶段验收

#### 下游文件

- `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`：只允许消费已经写入正式配置的数据资产，因此本文件必须写清 `crc_gland_segmentation_project/configs/data/crag.yaml` 的放行前提
- 后续 `09_CRAG验证/*`：会直接消费这里冻结的 `train153 / val20 / test40`、`source_subset`、阈值来源边界和结果解释口径

### 2.4 当前文件允许锁定和禁止重开的内容

当前文件只允许锁定：

- `CRAG` split 定义
- 训练池合并规则
- `CSV` schema 与路径规则
- `source_subset` 与 `sample_id` 追溯规则
- split 放行与重划禁令

当前文件禁止借机重开：

- `CRAG` 训练协议主变量
- 对象级指标定义
- 测试集阈值来源
- `CRAG` 阶段的方法搜索空间

---

## 3. 正式提取与冻结边界

### 3.1 路线层提取

从 `02_路线与投稿` 层提取到的当前结论是：

- `GlaS` 是主 benchmark，`CRAG` 只承担第二 benchmark 的补充验证职责
- `CRAG` 阶段要验证的是主线趋势能否跨数据集保留，而不是在 `CRAG` 上重新发明新 protocol
- 因为 `CRAG` 不是主调参场，所以 split 必须先冻结，再允许后续训练和评估继承

### 3.2 文献层提取

从 `MILD-Net`、`TA-Net` 提取到的当前结论是：

- `CRAG` 是腺体分割中被反复使用的正式 benchmark，不是可任意裁切的辅助集
- 文献使用 `CRAG` 的价值在于补充跨数据集可信度，因此本项目也必须保护其验证 / 测试边界
- 如果当前项目的 `CRAG` split、来源说明和追溯字段不稳定，后续与文献 direct comparison 的解释基础会被破坏

### 3.2.1 文献支持与当前工程冻结的边界

这里必须显式区分两层含义：

- 文献层已经充分支持 `CRAG` 作为腺体任务正式 benchmark 的角色。
- 但文献层并没有在当前项目里自动提供“全社区唯一官方 `train153 / val20 / test40`”这一结论。
- 因此，当前文件冻结的是 `基于本地整理版结构的项目正式工程 split`，而不是把它误写成“`CRAG` 官方唯一 split”。

本文件后续统一使用下面这组字段表达该边界：

```text
split_provenance_type = project_frozen_from_local_layout
benchmark_role_supported = true
official_universal_split_claim = false
```

这条边界必须写死的原因是：

- 后续 `09_CRAG验证/*` 需要一个稳定、唯一、可交接的训练 / 验证 / 测试三分结构。
- 但后续 direct comparison 仍然必须继续检查 `same_split`、`same_metric_protocol` 和 `no_major_test_gap`，不能因为当前项目已经冻结了 `train153 / val20 / test40`，就自动把所有文献 `CRAG` 数字都写成完全公平直比。

### 3.3 代码映射边界

本轮必须明确区分两层含义：

- `[project_root]/` 下的路径是未来正式工程必须实现的接口契约
- 当前 `plan/` 工作区中的文档并不等于这些脚本已经存在

本轮复查结果表明，当前主工作区未检索到 prepare_crag_split.py、csv_loader.py、check_dataset_pairs.py、validate_data_assets.py 的现成实现。  
因此，本文件后续写到的这些路径只能解释为正式工程落点，不能误写成“当前工作区已存在代码”。

---

## 4. 正式 split 冻结规则

### 4.1 `CRAG` split 主规则

- 当前结论：`CRAG` 固定采用本地整理版结构 `train_sup_16 / train_unsup_137 / val20 / test40`，执行层只承认 `train153 / val20 / test40`
- 规则类型：`路线层锁定 + 工程冻结规则`
- 适用阶段：`01_数据协议`，并持续生效到后续 `CRAG` 验证阶段
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`，`结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 核心公式或定义参考：`train153 = train_sup_16 union train_unsup_137`，其中 union 只允许发生在正式 `CSV` 层
- 采用原因：后续训练、验证、测试都需要稳定三分结构，而 `CRAG` 的定位是补充验证，不是重新设计 protocol
- 不采用的相邻方案：不采用为不同模型维护多套 `CRAG` split；不采用在模型阶段重新挪动 `val20 / test40`
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`[project_root]/splits/crag/*.csv`，`crc_gland_segmentation_project/configs/data/crag.yaml`
- 运行记录字段：`crag_layout_version`，`crag_split_version`，`dataset_role`，`split_provenance_type`，`official_universal_split_claim`
- 验收方式：执行层只允许出现 `train153 / val20 / test40`；`val20 / test40` 不得回流训练；`train153` 样本数必须稳定为 `153`

### 4.2 训练、验证、测试的正式职责

#### `train153` 职责规则

- 当前结论：`train153` 只承担 `CRAG` 补充验证阶段的训练职责，不参与正式测试结论
- 规则类型：`工程冻结规则`
- 适用阶段：`09_CRAG验证/*`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，`结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`
- 采用原因：训练池必须与验证 / 测试职责分离，避免第二 benchmark 也被污染成调参集
- 不采用的相邻方案：不采用只用 `train_sup_16` 跑正式结果却继续沿用 `train153` 名称；不采用训练时混入 `val20 / test40`
- 代码落点：`crc_gland_segmentation_project/splits/crag/crag_train153.csv`
- 运行记录字段：`train_split_name`，`num_train_total`，`source_subset`
- 验收方式：训练配置只允许引用 crag_train153.csv；所有训练样本都能回指来源子集

#### `val20` 职责规则

- 当前结论：`val20` 只承担验证监控、checkpoint 选择与阈值冻结职责，不得混入正式测试结论
- 规则类型：`工程冻结规则`
- 适用阶段：`09_CRAG验证/*`
- 直接依据：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- 核心公式或定义参考：`best_epoch = argmax_t ObjDice(val20, epoch=t)`
- 采用原因：`CRAG` 上的阈值与 checkpoint 仍必须只由验证集驱动，不能由测试集回调
- 不采用的相邻方案：不采用把 `val20` 写进主结果表；不采用看完 `val20` 再重划 split
- 代码落点：`crc_gland_segmentation_project/splits/crag/crag_val20.csv`，`crc_gland_segmentation_project/configs/data/crag.yaml`
- 运行记录字段：`val_split_name`，`best_selector`，`threshold_source`
- 验收方式：`threshold_source` 只能指向 `val20`；正式 `CRAG` 测试结果不得混入 `val20`

#### `test40` 职责规则

- 当前结论：`test40` 只用于最终 `CRAG` 结果汇报、文献对比与案例展示，不得参与调参或阈值搜索
- 规则类型：`工程冻结规则`
- 适用阶段：`09_CRAG验证/*`
- 直接依据：04_MILD-Net.md，07_TA-Net.md，`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 核心公式或定义参考：正式报告链固定为 `Report(test40, metric_k; threshold frozen from validation)`
- 采用原因：`CRAG` 的价值是给主线补充可信度，而不是再次用测试集回调模型
- 不采用的相邻方案：不采用在 `test40` 上调阈值；不采用看完 `test40` 后改结构或改 split
- 代码落点：`crc_gland_segmentation_project/splits/crag/crag_test40.csv`，[project_root]/test_metrics.csv
- 运行记录字段：`test_split_name`，`eval_proto_version`，`threshold_value`
- 验收方式：`test40` 只用于最终评估与展示；任何测试集回调都必须判为违规

---

## 5. 正式 `CSV` schema 与路径规则

### 5.1 `CRAG` `CSV` schema 规则

- 当前结论：每个 `CRAG` 正式 `CSV` 必须至少包含 `sample_id`, `image_relpath`, `mask_relpath`, `dataset`, `split`, `source_subset`
- 规则类型：`工程冻结规则`
- 适用阶段：`01_数据协议` 生成 split 时生效，后续训练与评估阶段继承
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`
- 核心公式或定义参考：`sample_id = dataset + "_" + source_subset + "_" + stem(image_filename)`
- 采用原因：训练池合并后必须仍能回指样本来源，否则无法解释异常来源与子集贡献
- 不采用的相邻方案：不采用省略 `source_subset`；不采用不同 split 使用不同 schema；不采用仅靠文件名隐式猜来源
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`crc_gland_segmentation_project/src/data/csv_loader.py`，`[project_root]/splits/crag/*.csv`
- 运行记录字段：`split_csv_schema_version`，`sample_id_rule_version`，`source_subset`
- 验收方式：三个 `CSV` schema 必须一致；训练记录必须保留来源子集；路径列只允许写工程根相对路径

### 5.2 路径与字段固定写法

正式 `CSV` 字段固定要求如下：

- `dataset` 固定写 `CRAG`
- `split` 固定写 `train153 / val20 / test40`
- `source_subset` 对训练样本固定保留 `train_sup_16` 或 `train_unsup_137`
- `image_relpath / mask_relpath` 只允许写工程根相对路径

相对路径示例：

- `[crag_example]/train_sup_16/image/xxx.png`
- `[crag_example]/train_sup_16/mask/xxx.png`

明确不允许：

- 本机绝对路径
- 临时复制目录
- 把 `val20 / test40` 错写成训练来源字段

### 5.3 必须导出的最小正式文件集

后面必须生成并冻结：

- `crc_gland_segmentation_project/splits/crag/crag_train153.csv`
- `crc_gland_segmentation_project/splits/crag/crag_val20.csv`
- `crc_gland_segmentation_project/splits/crag/crag_test40.csv`

这三个文件不是临时中间产物，而是后续 `crc_gland_segmentation_project/configs/data/crag.yaml` 与 `09_CRAG验证/*` 唯一允许读取的正式入口。

---

## 6. 训练池合并与 `source_subset` 追溯

### 6.1 训练池合并规则

- 当前结论：正式训练集 `train153` 由 `train_sup_16` 与 `train_unsup_137` 在 `CSV` 层顺序合并生成，不允许手工复制磁盘目录
- 规则类型：`工程冻结规则`
- 适用阶段：`01_数据协议`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\00_阶段总协议.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md`
- 核心公式或定义参考：`train153 = train_sup_16 union train_unsup_137`
- 采用原因：把训练池合并写成显式工程协议，才能避免手工复制导致路径、来源和版本关系丢失
- 不采用的相邻方案：不采用磁盘层新建“合并目录”；不采用训练时临时扫描多个根目录再拼接；不采用只保留最终训练数不保留来源身份
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`crc_gland_segmentation_project/splits/crag/crag_train153.csv`
- 运行记录字段：`train_pool_rule`，`num_train_sup`，`num_train_unsup`，`num_train_total`
- 验收方式：`train153` 样本数必须为 `153`；每条训练记录都必须保留原始 `source_subset`

### 6.2 为什么必须保留 `source_subset`

`source_subset` 不是装饰字段，而是正式追溯字段。  
它至少承担三类职责：

- 回指样本来自 `train_sup_16` 还是 `train_unsup_137`
- 在数据检查与错误分析时追溯异常是否集中于某一来源子集
- 为后续文档、报告和可能的扩展实验保留统一来源口径

只要 `source_subset` 丢失，`train153` 就会退化成“不可解释的大训练池”，这不允许进入正式配置。

---

## 7. split 写入前的门控链

### 7.1 `CRAG` split 放行规则

- 当前结论：`CRAG` split 必须先生成正式 `CSV`，再完成 schema 与 `source_subset` 校验，再通过 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md` 的六步检查闭环，最后才允许写入 `crc_gland_segmentation_project/configs/data/crag.yaml`
- 规则类型：`工程冻结规则`
- 适用阶段：`01_数据协议`
- 直接依据：`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`，`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md`
- 核心公式或定义参考：`pass_split_release = pass_csv_build and pass_schema and pass_source_subset and pass_data_check and pass_handoff`
- 采用原因：把 `CRAG` split 从“生成文件”提升为“正式放行资产”，防止坏 split 提前流入训练
- 不采用的相邻方案：不采用先写 `crc_gland_segmentation_project/configs/data/crag.yaml` 后补检查；不采用只有目录检查没有 schema 校验；不采用口头确认放行
- 代码落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/check_dataset_pairs.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/validate_data_assets.py`，`crc_gland_segmentation_project/configs/data/crag.yaml`
- 运行记录字段：`pass_split`，`pass_data_check`，`handoff_ready`，`next_action`
- 验收方式：只有在全部门控为真时，`crc_gland_segmentation_project/configs/data/crag.yaml` 才允许引用正式 split；任一子门失败都必须阻断

### 7.2 与数据阶段总门的关系

本文件给出的不是孤立 `pass_split`，而是必须接入总门控链：

```text
data_stage_pass
= pass_source
and pass_split
and pass_pair
and pass_label
and pass_check
and pass_preview
and pass_handoff

其中：
pass_split   <- CRAG split schema / uniqueness / source_subset / config freeze all pass
pass_check   <- 六步数据检查闭环通过
pass_handoff <- split assets + reports + manifest 已可追溯
```

因此：

- 只要 `pass_data_check = False`，本文件的 `pass_split` 就不能被视为最终通过
- 只要 `asset_manifest`、检查报告或预览证据缺失，`handoff_ready` 就不得成立
- `data_stage_pass = False` 时，下游 `preflight_pass` 必须同步为 `False`

### 7.3 生成、校验、放行的固定顺序

本文件只承认以下固定顺序：

1. 读取 `train_sup_16 / train_unsup_137 / val20 / test40`
2. 生成 `train153 / val20 / test40` 的正式 `CSV`
3. 校验 `sample_id`、schema、`source_subset`、跨 split 唯一性与相对路径
4. 继承六步检查闭环与人工抽查证据
5. 导出 `crag_split_report` 与 `asset_manifest`
6. 写入 `crc_gland_segmentation_project/configs/data/crag.yaml`
7. 允许后续 `CRAG` 训练、验证、测试阶段消费

任何跳过中间门控、直接写配置或直接开训的行为，都必须判定为违规。

---

## 8. 与检查、交付、验收和下游训练的闭环

### 8.1 与 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md` 的闭环

本文件必须显式继承六步检查闭环：

- 数量检查
- 配对检查
- 路径可读性检查
- 前景有效性检查
- 统计汇总
- 人工抽查

只有这些环节全部通过，`CRAG` split 才能从“已生成”升级为“已放行”。

### 8.2 与 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md` 的闭环

本文件生成的不只是三个 `CSV`，还必须把下列内容纳入正式数据资产包：

- `splits/crag/*.csv`
- `crc_gland_segmentation_project/reports/data_checks/crag_split_report.md`
- `crc_gland_segmentation_project/reports/data_checks/duplicate_check_report.md`
- `crc_gland_segmentation_project/configs/data/crag.yaml`
- `asset_manifest`

缺少任何一类资产，都不允许把 `CRAG` split 判为可交接。

### 8.3 与 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md` 的闭环

本文件的结论必须能直接回答数据阶段验收最关心的几个问题：

- `CRAG` split 是否已经固定
- 三个正式 `CSV` 是否已经存在
- `source_subset` 是否可追溯
- 是否存在跨 split 泄漏或测试集回流训练
- 是否已经形成正式报告与交接资产

只要有任一项答不上来，数据阶段就不得判通过。

### 8.4 与 `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md` 的闭环

虽然 `UNet` 主线主要消费 `GlaS`，但下游阶段已经把“训练入口只能读取正式数据资产”的规则写死。  
因此本文件也必须遵守相同门控逻辑：

- 只能通过正式配置读 split
- 不能重新扫描原始目录替代正式 `CSV`
- 不能在训练代码里临时重建 `CRAG` split

这个约束会继续传递到后续 `09_CRAG验证/*`。

### 8.5 与文献 direct comparison 的比较边界

当前文件虽然冻结了项目正式 `CRAG` split，但它不自动保证所有文献结果都可与当前项目直接并排。

后续 `CRAG` 结果表必须继续额外检查：

```text
crag_direct_comparison_eligible
= same_benchmark
and same_split
and same_metric_protocol
and no_major_test_gap
```

这意味着：

- 若某篇文献的 `CRAG` 划分并不等同于当前项目固定的 `train153 / val20 / test40`，则它最多只能作为 `reference_only` 或显式降级说明。
- 若某篇文献依赖额外后处理、特殊测试流程或对象级实现口径不同，也不能因为同属 `CRAG` benchmark 就自动写成完全公平 direct comparison。
- 后续 `结直肠腺体分割_plan_优化版/01_实验执行/09_CRAG验证/03_结果解释规则.md` 必须直接继承这里的 split 边界，而不是在结果解释阶段重新口头发明“差不多可比”。

---

## 9. 不通过线、红线与重划回退规则

### 9.1 一般不通过线

下面任一情况成立，都不允许把 `CRAG` split 写入正式配置：

- `train153 / val20 / test40` 任何一个 `CSV` 缺失
- schema 不一致
- `source_subset` 丢失或错误继承
- `sample_id` 不能稳定回指
- `image_relpath / mask_relpath` 不是工程根相对路径
- 六步检查未完成
- 正式检查报告或交接资产缺失

### 9.2 数据红线

下面任一情况成立，都必须立即回退，不允许继续进入后续 `CRAG` 验证：

- 同一 `sample_id` 出现在多个 split
- `val20` 或 `test40` 回流训练
- 为某个模型私自生成单独一版 `CRAG` split
- `source_subset` 被删除、改写或无法追溯
- 当前本地整理版来源说明不清，无法确认目录身份

### 9.3 如果后面确实必须改 `CRAG` 划分

只有在当前本地整理版被证明不再可用时，才允许重开 `CRAG` 划分，并且必须固定按以下顺序：

1. 明确记录当前 `CRAG` 资产为什么失效
2. 回改 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\01_数据源与目录约定.md` 与本文件
3. 删除旧 split 资产与旧 manifest
4. 重新生成全部 `CRAG` split 与检查报告
5. 重新完成数据阶段放行
6. 从头重新启动后续 `CRAG` 验证

任何“改一点点 split 但不回改协议”的做法都不允许。

---

## 10. 正式输出资产与运行记录字段

### 10.1 最小正式输出资产

本文件要求至少输出：

- `crc_gland_segmentation_project/splits/crag/crag_train153.csv`
- `crc_gland_segmentation_project/splits/crag/crag_val20.csv`
- `crc_gland_segmentation_project/splits/crag/crag_test40.csv`
- `crc_gland_segmentation_project/reports/data_checks/crag_split_report.md`
- `crc_gland_segmentation_project/reports/data_checks/duplicate_check_report.md`
- `crc_gland_segmentation_project/configs/data/crag.yaml`
- `asset_manifest`

### 10.2 必须回写的正式字段

本文件不是只导出 `CSV`，还必须回写至少下列字段：

- `crag_layout_version`
- `crag_split_version`
- `split_csv_schema_version`
- `sample_id_rule_version`
- `source_subset`
- `data_check_version`
- `manual_audit_version`
- `asset_manifest`
- `pass_split`
- `pass_data_check`
- `handoff_ready`
- `data_stage_pass`
- `next_action`

这些字段共同决定 `CRAG` split 是否已经成为正式可交接资产。

---

## 11. 回退条件

### 11.1 数据阶段内回退触发条件

只要出现下面任意一条，本文件对应的 `CRAG` split 协议就不得放行，必须先回退到当前文件与其上游数据阶段文件修正，而不是继续把问题带进后续 `CRAG` 验证或其它下游阶段：

- `train153 / val20 / test40` 任一正式 `CSV` 缺失、版本漂移或 schema 失配
- `source_subset` 丢失、误写、无法回指训练样本原始来源，或被错误继承到 `val20 / test40`
- `sample_id`、`image_relpath`、`mask_relpath` 不能稳定回指当前本地整理版 `CRAG` 目录
- `crc_gland_segmentation_project/configs/data/crag.yaml` 在六步检查闭环未通过时就提前引用正式 split
- `asset_manifest`、`handoff_ready`、`pass_split`、`pass_data_check` 与实际 split 资产状态不一致
- 下游脚本绕开正式 `CSV`，重新扫描目录、临时重建另一版 `CRAG` split，或把 `test40` 重新带回训练 / 调参链

### 11.2 下游异常时的强制回退顺序

如果 `09_CRAG验证/*` 或其它下游阶段出现明显异常，例如指标与肉眼长期严重矛盾、`val20` 与 `test40` 分裂异常、案例回查对不上样本身份等，必须按下面顺序强制回退：

1. 检查 `crag_train153 / val20 / test40` 的 `CSV` 版本、样本数与 schema
2. 检查 `source_subset`、`sample_id`、`image_relpath / mask_relpath` 是否还能回指正式数据根
3. 检查 `train153 = train_sup_16 union train_unsup_137` 是否仍只在 `CSV` 层合并，而不是被磁盘目录或训练入口偷偷改写
4. 检查六步数据检查闭环、人工抽查与 split 放行链是否真的先于 `crc_gland_segmentation_project/configs/data/crag.yaml` 生效
5. 检查 `asset_manifest`、`handoff_ready`、`data_stage_pass` 与正式报告资产是否仍然一致
6. 检查下游训练与评估入口是否真的只通过正式配置和正式 `CSV` 消费 `CRAG`

### 11.3 回退后的重新放行条件

发生回退后，只有同时满足下面条件，才允许重新把当前 `CRAG` split 标记为正式可交接资产：

- `splits/crag/*.csv` 已按当前正式版本重新导出并完成 schema 校验
- crag_split_report.md、重复样本报告和相关检查资产已同步更新
- `crc_gland_segmentation_project/configs/data/crag.yaml` 已回指新一轮正式 split 版本
- `asset_manifest`、`handoff_ready`、`data_stage_pass` 与 `next_action` 已重新登记
- 下游训练前预飞检查重新通过，且不再存在绕开正式 split 的兜底逻辑

---

## 12. 代码落地接口

### 11.0 接口状态说明

本节必须和旧稿显式区分：

- 下列路径是按 `00_总览与规范` 冻结的 `[project_root]/` 正式工程落点
- 它们是后续必须实现的接口契约
- 它们不是当前 `plan/` 工作区里已经存在的现成脚本
- 当前主工作区复查未检索到这些真实脚本，因此本节不能把它们写成“已实现代码”

### 11.1 `CRAG` split 生成入口

- 工程正式落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`
- 当前主工作区状态：`plan/` 目录中尚未确认到现成实现；这里冻结的是正式工程接口契约
- 入口类 / 函数：`build_crag_split()`，`load_crag_subset_manifest()`，`merge_crag_train_pool()`
- 输入：`dataset_root`，`subset_dir_map`，`crag_layout_version`，`crag_split_version`，`sample_id_rule_version`
- 输出：`train153 / val20 / test40` 的正式索引表、split 元信息、正式 `CSV`
- `dtype`：路径字段为 `PathLike/string`；样本数与索引为 `int`
- 依赖配置：`crag_layout_version`，`crag_split_version`，`split_csv_schema_version`，`sample_id_rule_version`，`dataset_source_note`
- 前置断言：`dataset_root` 必须指向 `crc_gland_segmentation_project/datasets/02_CRAG_reorganized_local_copy`；四个来源子集目录必须同时存在；`train153` 只能在 `CSV` 层合并生成；同一 `sample_id` 不得跨 split 重复
- 运行产物：`[project_root]/splits/crag/*.csv`，`crc_gland_segmentation_project/reports/data_checks/crag_split_report.md`

### 11.2 `CSV` schema 与 `source_subset` 校验入口

- 工程正式落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`crc_gland_segmentation_project/src/data/csv_loader.py`
- 当前主工作区状态：当前 `plan/` 目录中尚未确认到现成实现；本节定义的是后续必须实现的校验接口
- 入口类 / 函数：`build_crag_sample_id()`，`validate_crag_csv_schema()`，`validate_crag_source_subset()`，`validate_crag_split_uniqueness()`
- 输入：样本文件名、`source_subset`、相对路径字段、正式 split `CSV`
- 输出：统一 `sample_id`、schema 校验结果、来源字段一致性结论、重复样本清单
- `dtype`：`sample_id`、路径字段和 `source_subset` 为 `string`；校验状态为 `bool`
- 依赖配置：`split_csv_schema_version`，`sample_id_rule_version`，`crag_layout_version`，`dataset_root`
- 前置断言：三个 `CSV` 必须共享同一套 schema；路径列只允许写工程根相对路径；训练集记录必须保留 `train_sup_16 / train_unsup_137` 的 `source_subset`；`val20 / test40` 不得误继承训练来源字段
- 运行产物：schema 校验通过记录、跨 split 唯一性结论、重复样本报告

### 11.3 split 放行与配置冻结入口

- 工程正式落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/check_dataset_pairs.py`，`crc_gland_segmentation_project/tools/stage01_data_protocol/validate_data_assets.py`，`crc_gland_segmentation_project/configs/data/crag.yaml`
- 当前主工作区状态：当前 `plan/` 目录中尚未确认到现成实现；这里冻结的是 split 放行和正式配置写入的接口颗粒度
- 入口类 / 函数：`validate_crag_check_gate()`，`export_crag_split_config()`，`freeze_crag_split_manifest()`
- 输入：六步检查汇总、正式 split `CSV`、来源说明文件路径、当前 split 版本
- 输出：是否允许放行到 `crc_gland_segmentation_project/configs/data/crag.yaml` 的门控结论、split manifest、与检查结果绑定的数据配置
- `dtype`：放行状态为 `bool`；版本、subset 名和配置字段为 `string`
- 依赖配置：`data_check_version`，`crag_split_version`，`crag_layout_version`，`dataset_source_note`，`asset_manifest_version`
- 前置断言：只有在六步检查闭环通过后，才允许把 `splits/crag/*.csv` 写入正式数据配置；一旦发现 `test40` 回流训练、`sample_id` 跨 split、`source_subset` 丢失或来源说明缺失，`next_action` 必须固定为 `rollback`
- 运行产物：`crc_gland_segmentation_project/configs/data/crag.yaml`，`crc_gland_segmentation_project/reports/data_checks/crag_split_report.md`，`asset_manifest`

### 11.4 下游训练前预飞检查入口

- 工程正式落点：`crc_gland_segmentation_project/tools/stage01_data_protocol/validate_data_assets.py`，`crc_gland_segmentation_project/scripts/train.py`
- 当前主工作区状态：当前 `plan/` 目录中尚未确认到现成实现；这里定义的是下游训练前必须遵守的阻断接口
- 入口类 / 函数：`validate_data_stage_acceptance()`，`run_crag_preflight()`
- 输入：正式 `CSV`、`asset_manifest`、`data_stage_pass`、`handoff_ready`、数据配置路径
- 输出：`preflight_pass`、阻断原因、可供训练入口读取的前置校验结果
- `dtype`：门控状态为 `bool`；失败原因为 `string`
- 依赖配置：`data_stage_pass`，`handoff_ready`，`asset_manifest`，`data_proto_version`
- 前置断言：下游训练只能读取已经通过放行的正式 split；若 `pass_split = False`、`pass_data_check = False` 或报告资产缺失，`preflight_pass` 必须为 `False`
- 运行产物：训练前置检查记录、run_meta.yaml 中的数据放行字段

---

## 13. 冲突裁决记录

- 冲突对象：本文件是继续停留在“`CRAG` split 说明文”，还是提升为“正式 split 冻结 + 放行协议”
- 冲突来源：旧稿虽然已经写出 `train153 / val20 / test40`、训练池合并和 `source_subset`，但仍有四个关键缺口：路线层与文献层锚点不够硬；和 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\02_数据检查与配对规则.md` 的门控链没有写透；和 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\07_数据阶段验收.md` 的交付闭环不够强；代码接口没有明确区分“未来正式工程落点”和“当前 `plan/` 工作区未落地状态”
- 裁决结论：本轮按整文件重写方式，把本文件提升为“先生成 split -> 再校验 schema/source_subset -> 再继承六步检查闭环 -> 最后冻结到 `crc_gland_segmentation_project/configs/data/crag.yaml`”的正式协议，并显式补入双层代码映射与下游预飞阻断接口
- 裁决理由：如果当前文件继续只说明“`CRAG` 怎么分三份”，后续 `09_CRAG验证/*` 仍会把 split 理解成可随时重建的中间文件，而不是训练代码唯一允许读取的正式资产
- 受影响文件：`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/04_CRAG划分协议.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/02_数据检查与配对规则.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`，`结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`，`结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`，后续 `09_CRAG验证/*`
- 是否需要回流修订：需要；后续进入 `09_CRAG验证/*` 时，必须继续显式继承本文件固定的 `split + source_subset + threshold_source + manifest` 口径，不允许重新口头解释
- 代码实现影响：影响 `crc_gland_segmentation_project/tools/stage01_data_protocol/prepare_crag_split.py`、`crc_gland_segmentation_project/src/data/csv_loader.py`、`crc_gland_segmentation_project/tools/stage01_data_protocol/check_dataset_pairs.py`、`crc_gland_segmentation_project/tools/stage01_data_protocol/validate_data_assets.py`、`crc_gland_segmentation_project/configs/data/crag.yaml` 的接口组织、字段命名和放行时机

---

## 14. 文件质量自检

- [x] 已在修改前重新遍历 `00_总览与规范`
- [x] 已完成最低前置阅读：`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md`、`结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/07_实验执行全局修订与质检规范.md`
- [x] 已遍历 `02_路线与投稿` 的相关文件
- [x] 已遍历 `03_文献证据` 的相关正式深提取稿
- [x] 已检查 `01_实验执行` 全局相关文件，包括前面和后面的内容
- [x] 对后续文件中的相关内容做了甄别，而不是机械继承
- [x] 发现冲突时，已经补写标准化 `冲突裁决记录`
- [x] 已区分 `官方协议固定项 / 路线层已锁定 / 论文直接支持 / 论文支持的候选范围 / 工程冻结规则 / 待确认项`
- [x] 已写清当前文件最核心规则的来源
- [x] 已写清为什么这样设计，而不是只给结论
- [x] 已写清公式、定义或原理解释（如果该文件涉及这些内容）
- [x] 公式、定义或原理已经达到“可直接翻译代码 + 可直接写入论文”的最低深度
- [x] 关键符号、术语、版本名和代码字段与前后文件保持一致
- [x] 已写清参数、结构、训练、评估或数据规则的作用
- [x] 已写清为什么不采用相邻方案（如果该文件涉及方案选择）
- [x] 已写清代码落点和运行记录字段
- [x] 代码落地对象已经细化到入口函数/类、I/O、配置字段和运行产物
- [x] 已写清验收方式与独立 `回退条件`
- [x] 当前修改影响到的其它文件，已经列出并同步回改或显式标记待回改
- [x] 所有 `待确认项` 都已写清关闭截止阶段、阻塞动作和回流修订要求
- [x] `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/06_实验执行证据化写作模板.md` `§7` 的检查项与一票否决项已同步核对
- [x] 已完成与同层最近合格文件的 `文件质量自检 / Diagnostics 闭环` 强度对照；当前文件继续以 `结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\05_标签转换与可视化规则.md`、`结直肠腺体分割_plan_优化版\01_实验执行\01_数据协议\06_数据产物清单.md` 为收尾强度参照，补齐独立 `回退条件`
- [x] 当前文件已完成 diagnostics，且无新增诊断问题
- [x] 当前文件已经达到“可直接指导代码与论文写作”的最小强度

---

## 15. Diagnostics 闭环

- 本轮执行：已对当前文件执行 IDE diagnostics 复核
- 本轮结果：当前文件无新增未解决 diagnostics 问题
- 闭环结论：本文件满足“先修复、后声明完成”的 diagnostics 要求

---

## 16. 一句话版本

> `CRAG` 的正式执行协议已经固定为：以当前本地整理版为唯一合法数据资产，把 `train_sup_16 + train_unsup_137` 在 `CSV` 层合并登记为 `train153`，并与固定的 `val20 / test40` 共同构成后续唯一有效的 `CRAG` 训练、验证、测试三分结构；只有在 schema、`source_subset`、六步检查闭环和交接资产都通过后，它才允许写入 `crc_gland_segmentation_project/configs/data/crag.yaml` 并被后续阶段正式消费。

