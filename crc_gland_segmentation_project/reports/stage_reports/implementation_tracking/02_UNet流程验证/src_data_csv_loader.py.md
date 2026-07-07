# src_data_csv_loader.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/data/csv_loader.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `benchmark manifest validation before supervised segmentation training`
- 章节: `split schema checking and sample identity validation`
- 公式/定义: split CSV rows -> schema validation + unique sample id check + resolved image and mask paths

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/csv_loader.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `dataset_code`, `split_dir`, `csv_files.train`, `csv_files.val`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/data/csv_loader.py`
- 符号: `normalize_relpath()` / `load_csv_rows()` / `required_fields_for()` / `validate_csv_schema()` / `validate_unique_sample_ids()` / `resolve_row_paths()`

## 这个脚本的作用

这份对象说明文回答的是一个很容易被忽略、但特别关键的问题:

当前 stage02 到底是谁保证 split CSV 资产本身是“能拿来喂训练主链”的。

答案就是 `../../../../src/data/csv_loader.py`。

你可以把它理解成 stage02 数据链里的“入库验单工位”。

用人话说，dataset 主对象负责把样本装成训练可读的记录，但在真正装箱之前，得先有人确认:

1. CSV 列是不是齐
2. `sample_id` 有没有重复
3. `image_relpath`、`mask_relpath` 是不是相对路径
4. 路径能不能统一展开到项目根下面

如果没有这份文件，dataset 对象就会直接拿着一份可能有坏行、坏字段、坏路径的 split 资产进入训练闭环。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
configs/data/glas.yaml
        ↓
splits/glas/glas_train68.csv
        ↓
src/data/csv_loader.py
        ↓
src/data/datasets.py
        ↓
scripts/train.py / runtime-check / trainer
```

这里最关键的事实有三条:

1. `../../../../configs/data/glas.yaml` 冻结了 `dataset_code=glas`，并且字段 `csv_files.train` 对应真实文件 `../../../../splits/glas/glas_train68.csv`
2. `../../../../src/data/datasets.py` 会在 `build_dataset_from_csv()` 里直接调用这份对象做 schema、唯一性和路径解析
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已经证明当前训练样本确实来自 `../../../../splits/glas/glas_train68.csv`

当前最硬的物理证据至少有 6 组:

1. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_source=split_csv`
2. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `split_csv` 对应 `../../../../splits/glas/glas_train68.csv`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_id=GlaS_official_train_train_1`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `image_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1.bmp`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `sample_id=GlaS_official_train_train_42`

说白了，这里不是“理论上应该读 CSV”，而是当前正式样本资产已经沿着这条链真的进入了 runtime 主链。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../configs/data/glas.yaml`
- `../../../../splits/glas/glas_train68.csv`
- `../../../../src/data/datasets.py`

### 下游消费者

- `../../../../src/data/datasets.py`
- `../../../../scripts/train.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义很直接:

1. 当前 split 资产不是训练时临时拼的
2. 当前 CSV 字段语义和数据协议冻结字段绑在一起
3. 当前样本身份锚点 `sample_id` 必须在进入 dataset 之前就稳定

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式 split CSV 校验与路径解析层
- 当前冻结字段:
  - `dataset_code=glas`
  - `split_dir` 对应真实目录 `../../../../splits/glas`
  - `csv_files.train` 对应 `../../../../splits/glas/glas_train68.csv`
  - `csv_files.val` 对应 `../../../../splits/glas/glas_val17.csv`
- 当前最硬证据:
  - `../../../../src/data/datasets.py` 写明 `rows = load_csv_rows(csv_path)`
  - `../../../../src/data/datasets.py` 写明 `schema_issues = validate_csv_schema(rows, config.dataset_code)`
  - `../../../../src/data/datasets.py` 写明 `unique_issues = validate_unique_sample_ids(rows)`
  - `../../../../src/data/datasets.py` 写明 `image_path, mask_path = resolve_row_paths(project_root, row)`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明当前 `split_csv` 对应 `../../../../splits/glas/glas_train68.csv`

这里必须诚实说明:

当前证据更强地证明了“正式 split CSV 校验和路径解析已经进入 dataset 主链”，还没有单独证明“CRAG 分支的 CSV 资产也已经作为当前 stage02 正式 run 路径被触发”。

## 脚本核心逻辑

### 主要流程

你可以把它想成 5 步:

1. 用 `load_csv_rows()` 把正式 split CSV 读成行字典
2. 用 `required_fields_for()` 决定当前数据集必须有哪些字段
3. 用 `validate_csv_schema()` 检查缺列、空字段和绝对路径违规
4. 用 `validate_unique_sample_ids()` 检查 `sample_id` 是否重复
5. 用 `resolve_row_paths()` 把 `image_relpath`、`mask_relpath` 展开成真实文件路径

### 关键点 1: 为什么这里先做 schema 校验

因为 schema 错了，本质上是资产问题，不是训练问题。

说白了，当前应该在 dataset 还没开始读图像之前，就把坏 CSV 拦下来。

### 关键点 2: 为什么 `sample_id` 必须唯一

因为 `sample_id` 不只是训练里的一列文本，它还是 runtime report、runtime evidence 和说明文回链的共同锚点。

如果这里不唯一，后面的证据链就会开始发虚。

### 关键点 3: 为什么禁止绝对路径

因为当前正式 split 资产要跟项目根一起移动。

如果 CSV 里藏了本机绝对路径，换一台机器，说明文里的真实路径和训练现场就会立刻分叉。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../src/data/datasets.py` 再由 `../../../../scripts/train.py` 间接进入主链。

### 运行方式 1: formal runtime-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --run-name A1_UNet_GlaS_v1_seed3407 --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1
```

### 运行方式 2: local smoke-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --smoke-check --device cpu
```

## 为什么这样设计

### 为什么不用别的设计

你现在可能会问:

“为什么不把这些 CSV 校验逻辑直接塞进 dataset 主对象里？”

用人话说，当然能塞，但那样 dataset 主对象会同时背配置解析、样本装箱、CSV 规则校验和路径展开四层职责。

单独拆出来以后，读者更容易看清“正式 split 资产到底是在哪里被判定为合格”的。

### 设计取舍 1: 为什么 issue 用列表返回

因为当前更需要的是一次性看清楚 CSV 到底坏了哪几处。

如果第一处问题就直接抛异常，人工修资产时反而要来回试很多轮。

### 设计取舍 2: 为什么 `required_fields_for()` 按数据集分支

因为 `glas` 和 `crag` 的共通列相同，但附加元信息列不完全一样。

当前把它们拆开写，说明文也更容易讲清“哪些是协议主干，哪些是数据集特有元信息”。

### 设计取舍 3: 为什么路径解析统一从项目根开始

因为当前 runtime 报告和说明文里的真实路径都默认相对项目根回链。

统一基线后，路径证据才不会一半按 CSV 所在目录解释，一半按项目根解释。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/data/glas.yaml`
2. 打开 `../../../../splits/glas/glas_train68.csv`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 对照 `../../../../src/data/csv_loader.py`

### 当前最关键的核对点

- `dataset_code=glas` 是否和需要字段组对上
- `split_csv` 是否真的指向 `../../../../splits/glas/glas_train68.csv`
- `sample_id`、`image_relpath`、`mask_relpath` 是否都能稳定展开成真实路径

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/data/csv_loader.py`
2. 具体路径已经固定在 `../../../../splits/glas/glas_train68.csv`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_id=GlaS_official_train_train_1`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `image_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1.bmp`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `mask_path` 对应 `../../../../datasets/01_GlaS_official_raw/train_1_anno.bmp`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `sample_id=GlaS_official_train_train_42`
7. 字段 `csv_files.train` 对应真实文件 `../../../../splits/glas/glas_train68.csv`

## 常见误区

- 误区 1: 以为 split CSV 只是 dataset 的一个小附件
  - 实际上它是正式样本身份和路径锚点的入口资产
- 误区 2: 以为 `sample_id` 重复无非就是日志看起来乱一点
  - 实际上 runtime 证据、说明文回链和人工核对都会一起被污染
- 误区 3: 以为这里只是做字符串清洗
  - 实际上这里决定的是“这份 split 资产能不能进入正式训练主链”

## 建议联读

- `src_data_datasets.py.md`
- `configs_data_glas.yaml.md`
- `scripts_train.py.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_data_datasets.py.md`，搞清楚这些校验结果是怎样被 dataset 主对象消费的
2. 再去看 `configs_data_glas.yaml.md`，回到 split 资产冻结来源
3. 最后去看 `scripts_train.py.md`，看正式入口怎样把数据链接进 runtime-check

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前 split CSV 是在哪里被判定为“足够正式、能进训练主链”的
2. 为什么 `sample_id` 唯一性在这里就是硬规则
3. 为什么相对路径规范要早于图像读取动作
4. 为什么这份对象应该单独从 dataset 主对象里拆出来讲

## 5 分钟自检任务

1. 回到 `../../../../splits/glas/glas_train68.csv`，找到一行 `sample_id`
2. 回到 `../../../../src/data/csv_loader.py`，说出哪几个函数会先后检查这行资产
3. 再回看 `../../../../src/data/datasets.py`，说明这些结果最后是怎么变成 `image_path` 和 `mask_path` 的

如果这三步你都能顺下来，说明你已经把这份 CSV loader 说明文真正看懂了。
