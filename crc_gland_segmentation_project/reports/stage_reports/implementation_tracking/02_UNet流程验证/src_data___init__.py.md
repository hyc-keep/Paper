# src_data___init__.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/data/__init__.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `dataset protocol and preprocessing utilities exposed behind one stable package facade`
- 章节: `package-level public API for data config, dataset assembly, mask protocol, and transform helpers`
- 公式/定义: `src.data` package -> one formal import surface consumed by the stage02 train entrypoint

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/__init__.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/data/glas.yaml`
- 对应字段: `dataset_code`, `input_size`, `mask_positive_rule`, `normalize_mean`, `normalize_std`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/data/__init__.py`
- 符号: `DataConfig` / `build_dataset_from_csv()` / `build_segmentation_dataset()` / `load_data_config()` / `simple_yaml_load()` / `build_augment_config()` / `build_train_transform()` / `build_eval_transform()`

## 这个脚本的作用

这份对象说明文回答的是一个很容易被忽略的问题:

为什么 `scripts/train.py` 明明要同时碰 data config、dataset、mask 协议和 transform，却只写了一组 `from src.data import ...`。

答案就是 `../../../../src/data/__init__.py`。

你可以把它理解成 stage02 数据主链的“总配电箱”。

用人话说，底层当然还是 `../../../../src/data/datasets.py`、`../../../../src/data/mask_ops.py`、`../../../../src/data/transforms.py` 这些具体对象在干活，但正式训练入口并不应该自己到处拼深层导入路径。

它应该面对一层已经锁定好的包级门面。

如果没有这份文件，入口脚本就会直接依赖很多散开的子模块路径，后面一旦数据链继续细分，训练入口、说明文和 gate 回链都会变得很散。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
scripts/train.py
        ↓
src/data/__init__.py
        ↓
datasets.py + mask_ops.py + transforms.py + yaml/config helpers
        ↓
runtime-check / train loader / val loader
```

这里最关键的事实有四条:

1. `../../../../scripts/train.py` 当前真实写了 `from src.data import build_augment_config, build_dataset_from_csv, build_eval_transform, build_segmentation_dataset, build_train_transform, load_data_config, simple_yaml_load`
2. `../../../../src/data/__init__.py` 把 dataset、mask、transform 和 config helper 集中暴露成一个正式公开入口
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已经证明当前正式样本来自 `split_csv`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经证明这一条数据链最后真的走到了 `output_shape=[2, 1, 512, 512]`

当前最硬的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/data/__init__.py`
2. `../../../../scripts/train.py` 已经通过 `from src.data import ...` 正式消费这个包门面
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_source=split_csv`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明字段 `split_csv` 对应真实文件 `../../../../splits/glas/glas_train68.csv`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明字段 `sample_path` 对应真实路径 `../../../../datasets/01_GlaS_official_raw/train_42.bmp`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`

说白了，这里不是“包里顺手放一个 `__init__` 文件”，而是正式训练入口和底层数据对象之间的稳定接口层。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../scripts/train.py`
- `../../../../configs/data/glas.yaml`

### 下游消费者

- `../../../../src/data/datasets.py`
- `../../../../src/data/mask_ops.py`
- `../../../../src/data/transforms.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义很直接:

1. 当前数据链不允许训练入口随手拼局部导入路径
2. 当前 data package 必须作为正式公开入口存在
3. 当前说明文可以把“包级门面”和“具体实现对象”拆开解释

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式数据包门面
- 当前冻结字段:
  - `dataset_code=glas`
  - `input_size=[512, 512]`
  - `mask_positive_rule=mask_gt_0`
  - `normalize_mean=[0.485, 0.456, 0.406]`
  - `normalize_std=[0.229, 0.224, 0.225]`
- 当前最硬证据:
  - `../../../../scripts/train.py` 直接从 `src.data` 导入数据链正式入口
  - `../../../../src/data/__init__.py` 用 `__all__` 把公开 API 明确列出来
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_source=split_csv`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`

这里必须诚实说明:

当前证据更强地证明了“正式训练入口确实通过 `src.data` 这个包门面进入数据链”，还没有单独证明 `../../../../src/data/boundary_targets.py` 或 `../../../../src/data/distance_targets.py` 已经作为当前 stage02 正式 runtime 路径被触发。

## 脚本核心逻辑

### 主要流程

你可以把它想成 4 步:

1. 从 `../../../../src/data/datasets.py` 导出 data config、dataset 构建和 yaml 读取入口
2. 从 `../../../../src/data/mask_ops.py` 导出 mask 读取、二值化和 resize helper
3. 从 `../../../../src/data/transforms.py` 导出 augment config 和 train/eval transform builder
4. 用 `__all__` 把当前正式公开 API 清单钉死

### 关键点 1: 为什么要有包级门面

因为 stage02 当前已经不是只靠一两个 data helper 就能跑通的状态了。

数据链至少同时包含:

1. 配置读取
2. split CSV 解析
3. mask 协议
4. transform 装配

如果入口脚本直接分别导入，接口边界会越来越乱。

### 关键点 2: 为什么 `__all__` 很重要

因为它让“正式暴露什么、不正式暴露什么”变成显式清单，而不是读者自己猜。

当前说明文之所以能把 `src.data` 作为 A 类对象单独解释，也正是因为这里已经形成了正式公开入口，而不是随手导入集合。

### 关键点 3: 为什么这里要诚实保留 boundary/distance 导出

因为当前包门面里确实导出了 `build_boundary_band`、`euclidean_distance_transform()` 和 `normalize_distance_map()`。

但“被导出”不等于“已经进入本轮 learning-doc A 类映射”。

这也是当前门面对象最值得单独解释的一点: 它既是正式入口层，又要保持和下游细分对象裁决解耦。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是由 `../../../../scripts/train.py` 间接消费。

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

“为什么不让 `../../../../scripts/train.py` 直接从 `src.data.datasets`、`src.data.transforms` 这些深层路径分别导入？”

用人话说，当然也能跑。

但那样训练入口会同时承担“找对象”和“用对象”两层职责。

单独保留一个包门面以后，入口脚本只面对稳定 API，细分对象怎么拆层可以留给 data 包内部自己收敛。

### 设计取舍 1: 为什么这里公开 `simple_yaml_load()`

因为当前正式入口在解析 experiment config 之后，还要继续解引用 data/model/train/eval 配置。

把 yaml helper 放进 `src.data` 门面，能保证入口脚本仍然通过统一数据包接口工作。

### 设计取舍 2: 为什么门面对象值得单独进 A 类

因为当前 `scripts/train.py` 的真实 import 面就在这里。

只要它是正式训练入口真正依赖的包级公开接口，它就不再只是“语法必须有的 `__init__` 文件”，而是正式工程边界的一部分。

### 设计取舍 3: 为什么这里不把所有导出对象都自动升 A

因为 A/B/C 裁决看的是当前轮次正式落点，不是简单看某个名字有没有出现在 `__all__`。

这份门面对象的职责是“正式公开入口”，不是代替每个细分对象自动完成裁决。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../scripts/train.py`
2. 打开 `../../../../src/data/__init__.py`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- `scripts/train.py` 是否直接从 `src.data` 导入正式数据链 API
- `__all__` 是否已经把公开接口清单显式写出
- `sample_source` 和 `split_csv` 是否确实进入 runtime 报告
- `output_shape` 是否证明这条数据链已经继续走到模型输出

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/data/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.data import ...`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `sample_source=split_csv`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明字段 `split_csv` 对应真实文件 `../../../../splits/glas/glas_train68.csv`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明字段 `sample_path` 对应真实路径 `../../../../datasets/01_GlaS_official_raw/train_42.bmp`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明字段 `mask_path` 对应真实路径 `../../../../datasets/01_GlaS_official_raw/train_42_anno.bmp`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`

## 常见误区

- 误区 1: 以为 `src.data.__init__` 只是 Python 语法壳
  - 实际上这里已经是 `scripts/train.py` 当前真实 import 面
- 误区 2: 以为 data 包门面等于所有下游对象都已经纳入 A 类
  - 实际上门面对象和细分对象的裁决要分开看
- 误区 3: 以为把导入写得更深就更“真实”
  - 实际上正式工程里更重要的是公开接口稳定

## 建议联读

- `src_data_datasets.py.md`
- `src_data_csv_loader.py.md`
- `src_data_mask_ops.py.md`
- `src_data_transforms.py.md`
- `scripts_train.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_data_datasets.py.md`，理解 dataset 主装配层
2. 再去看 `src_data_mask_ops.py.md` 和 `src_data_transforms.py.md`，把标签协议和变换层分开看清
3. 最后回到 `scripts_train.py.md`，确认训练入口为什么只面对 `src.data` 这个门面

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 为什么 `src.data` 包门面本身应该算正式对象
2. 它和 `../../../../src/data/datasets.py`、`../../../../src/data/mask_ops.py`、`../../../../src/data/transforms.py` 的边界分别是什么
3. 为什么 `scripts/train.py` 不该继续散写深层 data 导入
4. 为什么“被导出”不等于“自动升级成 A 类说明文对象”

## 5 分钟自检任务

1. 回到 `../../../../scripts/train.py`，找到 `from src.data import ...`
2. 回到 `../../../../src/data/__init__.py`，说出它公开了哪几类对象
3. 再回看 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`，解释 `sample_source=split_csv` 为什么能证明这个门面已经真的进入主链

如果这三步你都能顺下来，说明你已经把这份 data package 门面说明文真正看懂了。
