# src_data_csv_loader.py.md

## 这个脚本的作用

- 这个文件不是训练器,它只负责 formal split CSV 的读入、字段校验和路径解析
- 你可以把它理解成 `splits/*.csv` 进入项目代码前的第一道协议闸门

如果这里把字段名、相对路径或 `sample_id` 放松了,后面的 `datasets.py` 和 `scripts/train.py` 就会在错误输入上继续跑。

## 结构化溯源卡片

- 正式对象: `src/data/csv_loader.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `benchmark split protocol and ground-truth organization`
- 公式/定义: `每个样本必须对应稳定的图像-标签配对与固定 split 身份`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `src/data/csv_loader.py`
- commit: `workspace_local_20260704`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `split_csv_schema_version`, `sample_id_rule_version`, `image_relpath`, `mask_relpath`

### 当前实现落点
- 文件: `src/data/csv_loader.py`
- 符号: `COMMON_FIELDS`, `required_fields_for()`, `validate_csv_schema()`, `validate_unique_sample_ids()`, `resolve_row_paths()`

## 这个文件在整个阶段中的位置

这份代码处在很靠前的位置:

1. 上游是 `splits/glas/*.csv` 和 `splits/crag/*.csv`
2. 当前文件先把 CSV 读成 row dict,再校验列名、空字段和 `sample_id`
3. `src/data/datasets.py` 再把这些 row 变成后续入口真正消费的 sample 列表

换句话说,`csv_loader.py` 解决的不是“怎么训练”,而是“训练前到底认哪一行 CSV 才算合法样本”。

## 当前实现状态

- 状态: `已实现`
- 可运行性: `可直接被 src/data/datasets.py 调用`
- 测试覆盖: `已被当前数据阶段 preflight 链真实消费`

它现在的职责很聚焦,没有做多余抽象。
这反而是对的,因为当前阶段只要求把数据协议压实。

## 主要流程

### 1. 定义每类数据集必须有的字段

- 公共字段是 `sample_id,image_relpath,mask_relpath,dataset,split`
- GlaS 额外要求 `grade,source_partition`
- CRAG 额外要求 `source_subset`

这里直接把 GlaS 和 CRAG 的 schema 拆开,能避免“一个宽松 CSV 到处兼容”的歧义。

### 2. 读取 CSV 行

`load_csv_rows()` 用 `csv.DictReader` 直接读成 `list[dict[str, str]]`。

用人话说,它不做业务判断,只是先把磁盘上的表格读出来。

### 3. 校验 schema

`validate_csv_schema()` 主要做三件事:

1. CSV 不能是空表
2. 必需字段不能缺
3. `image_relpath` 和 `mask_relpath` 不能写绝对路径

第三条很关键。
因为一旦允许绝对路径,这份 split 就不再是可交付资产,它会偷偷绑定某一台机器的目录结构。

### 4. 校验 sample_id 唯一性

`validate_unique_sample_ids()` 会把所有 `sample_id` 放进集合里检查重复。

这一步看起来普通,但非常必要。
后续 runtime 报告、验收报告、人工审阅记录都要回链 `sample_id`。
如果这里不唯一,下游证据就会混掉。

### 5. 把相对路径解析成工程内绝对路径

`resolve_row_paths()` 用 `project_root / relpath` 的方式生成 `image_path` 和 `mask_path`。

这说明一个明确设计取舍:

- split CSV 里只保存相对路径
- 工程运行时再用项目根目录拼出真实文件

这个设计让 CSV 可以随项目一起交付,而不是随某台电脑一起交付。

## 关键函数说明

### `required_fields_for(dataset_code)`

- 作用: 根据 `glas` 或 `crag` 返回该数据集必须出现的字段
- 输入: `dataset_code`
- 输出: 对应字段元组
- 核心逻辑: 公共字段 + 数据集特有字段

它的意义不是写得花,而是把“字段要求”从后续流程里抽出来统一维护。

### `validate_csv_schema(rows, dataset_code)`

- 作用: 判断 CSV 是否满足当前数据集的正式 schema
- 输入: CSV 行列表和数据集代码
- 输出: issue 列表
- 核心逻辑: 缺列、空值、绝对路径都记成问题

这里返回 issue 列表而不是直接退出,是为了让 `datasets.py` 在报错时把问题成组抛出来。

### `validate_unique_sample_ids(rows)`

- 作用: 保证 `sample_id` 唯一
- 输入: CSV 行列表
- 输出: issue 列表

新手最容易误会的地方是: 只要文件路径不同,`sample_id` 重复也没关系。
这在当前项目里不成立,因为 `sample_id` 已经是正式证据链里的主键。

### `resolve_row_paths(project_root, row)`

- 作用: 把 CSV 里的相对路径还原成工程内文件路径
- 输入: `project_root`, `row`
- 输出: `image_path`, `mask_path`

这一步没有顺手检查文件是否存在,因为存在性检查由后续阶段做。
它这里只负责“如何解析路径”,职责边界比较干净。

## 代码里的真实协议痕迹

当前代码里最能说明阶段边界的地方有三处:

1. `COMMON_FIELDS` / `GLAS_EXTRA_FIELDS` / `CRAG_EXTRA_FIELDS`
2. `absolute_path_forbidden`
3. `duplicate_sample_id`

说白了,这三个点分别对应:

- 你这张表要长什么样
- 你不能把机器私有路径塞进正式资产
- 你不能让一个样本身份在同一份正式资产里重复

## 如何验证这份代码没读偏

### 验证 1: 看真实 CSV 是否满足字段要求

1. 打开 `splits/glas/glas_train68.csv`
2. 观察表头里是否包含 `sample_id,image_relpath,mask_relpath,dataset,split,grade,source_partition`
3. 再打开 `splits/crag/crag_train153.csv`
4. 观察是否把 GlaS 的 `grade` 换成了 `source_subset`

通过标准:

- GlaS 和 CRAG 各自命中自己的字段组合

### 验证 2: 看路径是不是相对路径

1. 继续看上面两份 CSV
2. 检查 `image_relpath` 和 `mask_relpath`

通过标准:

- 路径都像 `datasets/01_GlaS_official_raw/train_1.bmp`
- 不能以盘符开头,也不能是绝对路径

### 验证 3: 看下游是不是直接消费它

1. 打开 `src/data/datasets.py`
2. 看 `build_dataset_from_csv()` 是否直接调用了 `load_csv_rows()`、`validate_csv_schema()`、`validate_unique_sample_ids()`、`resolve_row_paths()`

通过标准:

- 四个关键函数都在下游总装配入口里被真实使用

## 最容易误解的地方

### 误区 1

“这不就是普通 CSV 读写工具吗,为什么也要单独写说明文?”

不对。
它不是通用工具,而是 `01_数据协议` 的正式 schema 守门员。
如果这里放松,整个 formal split 资产就会变得不可信。

### 误区 2

“路径最终都会变绝对路径,那 CSV 里直接写绝对路径不是更省事吗?”

也不对。
这样会破坏可交付性,因为别人拿到项目包后根本没有你的本地盘符结构。

## 读完后下一步看什么

读完这份文件后,最应该接着看:

1. `src_data_datasets.py.md`
2. `configs_data_glas.yaml.md`
3. `configs_data_crag.yaml.md`

因为 `csv_loader.py` 只解决了“CSV 合不合法”,真正把它拼成样本列表的是 `datasets.py`。
