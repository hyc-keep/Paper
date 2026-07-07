# scripts_train.py.md

## 结构化溯源卡片

- 正式对象: `../../../../scripts/train.py`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `benchmark split and ground-truth protocol`
- 公式/定义: `官方测试边界不能在训练入口重新解释,标签以正式 mask 为准`

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/data/datasets.py`
- commit: `workspace_local_20260704`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `GlaS 正式 split`, `input_size=512x512`, normalize_mean_and_normalize_std, `mask_positive_rule`

### 当前实现落点
- 文件: `../../../../scripts/train.py`
- 符号: `parse_args()` / `load_experiment_config()` / `resolve_data_config_path()` / `build_runtime_payload()` / `main()`

## 这个脚本的作用

这个脚本负责一件事: 在真正训练开始之前，先证明训练入口会不会老老实实消费已经冻结好的正式数据资产。

你可以把它理解成“训练前总闸门”。
它现在还不是完整训练器，但它已经是正式入口。

为什么要先有这个入口？
因为如果入口自己都还能绕开 `configs/data/glas.yaml`、`splits/glas/glas_train68.csv`、`datasets/01_GlaS_official_raw`，那前面整个 `01_数据协议` 就只是写在纸上的规则，不是能被工程执行的规则。

用人话说，这个脚本现在最重要的价值不是“算出 loss”，而是“先别吃错数据”。

这里建议联读:

- `../../../../scripts/README.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../reports/stage_reports/data_stage_acceptance.md`

## 这个脚本在整个阶段中的位置

如果你现在还不熟整个项目，可以先记住一句话:

`scripts/train.py` 在当前阶段是 formal asset preflight 入口，不是完整训练工作流。

它在链路里的位置可以画成这样:

```text
b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml
        ↓
configs/data/glas.yaml
        ↓
splits/glas/glas_train68.csv
        ↓
datasets/01_GlaS_official_raw/train_1.bmp
        ↓
scripts/train.py
        ↓
b_class_auxiliary/runtime_checks/train_runtime_payload.json
        ↓
b_class_auxiliary/runtime_checks/runtime_evidence.json
```

上游依赖有四个:

1. `b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml`
2. `configs/data/glas.yaml`
3. `splits/glas/glas_train68.csv`
4. `src/data/datasets.py`

下游消费者也很明确:

1. `b_class_auxiliary/tools/run_minimal_runtime_check.py` 会调用它
2. `b_class_auxiliary/runtime_checks/runtime_check_report.md` 会解释它产出的证据
3. `b_class_auxiliary/runtime_checks/code_quality_gate_report.md` 会根据这些证据裁决当前 coding 链

你现在可能会问:

“既然它后面被 runtime gate 和 code-quality gate 消费，为什么说明文还把它当正式对象？”

因为 gate 是内部流程留痕，但 `scripts/train.py` 本身会跟项目一起交付，而且别人真正要接手入口时，第一眼看的就是它。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 当前阶段验收协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`
- 正式规则文件 0: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/01_工程目录框架.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`

这一组回链的意义不是堆路径，而是证明当前说明文解释的真的是 `01_数据协议` 的正式入口，而不是我临时拍脑袋给 `scripts/train.py` 安了一个角色。

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `01_数据协议` 的最小正式训练入口
- 当前真实边界: `只做到 data_protocol_preflight`
- 当前已经形成的物理证据:
  - `sample_id=GlaS_official_train_train_1`
  - `input_shape=[522, 775, 3]`
  - `target_shape=[522, 775]`
  - `entrypoint_check_pass=true`
- 当前没有形成的物理证据:
  - `output_shape`
  - `loss_value`
  - `backward_executed`
  - `optimizer_step_executed`

这一步必须显式写出来。
否则文件虽然叫 `scripts/train.py`，但别人会自动以为它已经能跑完整训练。

## 脚本核心逻辑

### 主要流程

这个脚本现在的核心流程可以拆成 5 步:

1. 读取 `--config` 指向的 experiment config
2. 从 experiment config 解析 `config_refs.data` 或 `dataset_code`
3. 通过 `src/data/datasets.py` 加载正式数据配置和 split CSV
4. 选一个真实 sample，检查 image/mask 路径是否存在
5. 在 `--runtime-check` 模式下把证据写到 `b_class_auxiliary/runtime_checks/train_runtime_payload.json`

### 关键函数 1：`load_experiment_config()`

它解决的是“入口先认哪份实验配置”的问题。

当前脚本不会自己猜配置，也不会扫描目录。
它要求调用方明确传入 `b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml` 这样的配置文件。

这一步的价值，是把“入口到底认谁”为显式输入，而不是隐式约定。

### 关键函数 2：`resolve_data_config_path()`

这个函数负责把 experiment config 里的 `config_refs.data` 解析成真实文件。

当前最常见的路径就是 `configs/data/glas.yaml`。
如果 experiment config 没写 `config_refs.data`，它才会退回到 `dataset_code in {glas, crag}` 的兜底逻辑。

为什么这样设计？
因为当前阶段最需要保护的是“正式配置文件”这个边界。

为什么不用别的设计？

| 候选方案 | 看起来的好处 | 实际问题 | 最终决策 |
|---|---|---|---|
| 直接在 `scripts/train.py` 里写死数据目录 | 代码短 | 以后换数据配置会漂移,也无法审计 | 否决 |
| 运行时扫描 `datasets/` 自动猜 split | 看起来省事 | 直接破坏 `configs/data -> splits/*.csv -> dataset_root + relpath` | 否决 |
| 先认 experiment config,再解析 data config | 输入边界清楚 | 多一层配置跳转 | 采用 |

### 关键函数 3：`resolve_split_name()`

这个函数把 `runtime_split` 或 `train_split` 解释成最终 split 名。

当前 preflight experiment config 写的是 `runtime_split: train`。
这意味着入口真正读取的是 `splits/glas/glas_train68.csv` 对应的 train split。

这一步看起来很小，但它把“当前到底测哪一个 split”写成了显式字段。

### 关键函数 4：`inspect_sample_paths()`

这个函数不做模型前向，只做样本物理检查。

它会:

1. 用 `PIL.Image` 打开 image
2. 记录 `input_shape` 和 `input_dtype`
3. 用同样方式打开 mask
4. 记录 `target_shape`、`target_dtype` 和前若干个 `target_unique_values`

这里最关键的不是图像打开成功，而是把证据写成结构化字段。

当前真实结果已经落在 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 里:

- `input_shape=[522, 775, 3]`
- `target_shape=[522, 775]`
- `target_unique_values=['0', '1', '2', '3', '4', '5', '6', '7']`

### 关键函数 5：`build_runtime_payload()`

这个函数把当前 preflight 结论压成统一 payload。

payload 里最值得盯住的字段有:

- `runtime_profile=data_protocol_preflight`
- `entrypoint_check_pass=true`
- `entrypoint_check_reason=formal_split_assets_resolved`
- `sample_path` 对应 `datasets/01_GlaS_official_raw/train_1.bmp`
- `mask_path` 对应 `datasets/01_GlaS_official_raw/train_1_anno.bmp`

这几个字段合在一起，真正回答的是:

“这个入口到底有没有按照正式 split 和正式数据根解析出真实样本？”

### 为什么现在故意不做模型前向

很多人第一次看这个文件，会本能地问:

“既然都叫 `scripts/train.py` 了，为什么不顺手把模型、loss、optimizer 也接上？”

答案是：当前阶段不允许。

当前 `01_数据协议` 的任务，是冻结输入层和训练前预飞检查。
如果这里顺手把模型和优化链补上，表面上像省事，实际上会把数据阶段和训练阶段混在一起。

说白了，这不是“少写了一点代码”，而是故意不越阶段。

## 如何运行这个脚本

### 运行方式 1：直接走 runtime-check

```bash
cd crc_gland_segmentation_project
python scripts/train.py --config b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml --run-name preflight_train_entrypoint_runtime_check --runtime-check --runtime-check-output b_class_auxiliary/runtime_checks/train_runtime_payload.json --device cpu --max-steps 1
```

这条命令的目标不是训练，而是产出最小 runtime payload。

### 运行方式 2：让上游工具调用它

```bash
cd crc_gland_segmentation_project
python b_class_auxiliary/tools/run_minimal_runtime_check.py --experiment-config b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml
```

这时真正执行入口的还是 `scripts/train.py`，只是外面多了一层汇总器。

### 参数说明

| 参数 | 当前取值 | 作用 | 当前阶段为什么需要它 |
|---|---|---|---|
| `--config` | `b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml` | 指定 experiment config | 防止入口自己猜配置 |
| `--run-name` | `preflight_train_entrypoint_runtime_check` | 记录本次逻辑运行名 | 方便回链 runtime 证据 |
| `--runtime-check` | `True` | 打开轻量证据输出模式 | 当前阶段只需要 preflight payload |
| `--runtime-check-output` | `b_class_auxiliary/runtime_checks/train_runtime_payload.json` | 指定 payload 输出路径 | 供 runtime gate 汇总 |
| `--device` | `cpu` | 当前设备提示 | 当前只做最小 smoke 检查 |
| `--max-steps` | `1` | 当前最大步数 | 当前不进入完整训练循环 |

## 如何验证脚本运行结果

### 验证点 1：正式配置有没有被正确解析

检查方法:

1. 打开 `b_class_auxiliary/runtime_checks/preflight_train_entrypoint_experiment.yaml`
2. 确认 `config_refs.data` 当前指向 `configs/data/glas.yaml`
3. 运行上面的 runtime-check 命令
4. 查看终端或 `b_class_auxiliary/runtime_checks/runtime_check.log`

通过标准:

- 日志里能看到 `data_config` 且对应 `configs/data/glas.yaml`
- 没有 `experiment config not found` 或 `data config not found`

### 验证点 2：正式 split 有没有被真实读取

检查方法:

1. 打开 `splits/glas/glas_train68.csv`
2. 运行上面那条 `scripts/train.py` runtime-check 命令
3. 查看 `b_class_auxiliary/runtime_checks/runtime_check_report.md`

通过标准:

- 报告里出现 `split_name=train`
- 报告里出现 `split_csv` 且对应 `splits/glas/glas_train68.csv`
- 报告里出现 `sample_id=GlaS_official_train_train_1`

### 验证点 3：样本物理证据有没有落盘

检查方法:

1. 打开 `b_class_auxiliary/runtime_checks/runtime_evidence.json`
2. 看 `runtime_fields`
3. 对照 `datasets/01_GlaS_official_raw/train_1.bmp` 与 `datasets/01_GlaS_official_raw/train_1_anno.bmp`

通过标准:

- `sample_path` 和 `mask_path` 都是真实存在的文件
- `input_shape=[522, 775, 3]`
- `target_shape=[522, 775]`
- `entrypoint_check_pass=true`

### 验证点 4：不要误判成完整训练

检查方法:

1. 继续看 `b_class_auxiliary/runtime_checks/runtime_check_report.md`
2. 找 `loss_finite_pass`
3. 找 `grad_step_pass`

通过标准:

- 两项都应是 `not_applicable`
- 不能被写成 `pass`

这一步很重要。
因为它直接决定当前文档是不是在诚实描述阶段边界。

## 与项目其他部分的关联

这个脚本和下面这些对象关系最紧:

- `../../../../configs/data/glas.yaml`：定义正式数据根、split 目录和字段版本
- `../../../../splits/glas/glas_train68.csv`：定义当前 train split 的真实样本列表
- `../../../../src/data/datasets.py`：负责把 YAML 和 CSV 解析成 sample 列表
- `../../../../reports/stage_reports/data_stage_acceptance.md`：负责把 preflight_pass 写成阶段交接状态

换句话说，`scripts/train.py` 现在不是孤立入口，而是数据阶段交接链的最后一个执行锚点。

## 容易误解的地方

### 误解 1：有了 `scripts/train.py` 就等于有了完整训练

不是。
当前 `scripts/train.py` 只做到 asset resolution 和 payload 生成。

### 误解 2：看到 `runtime_check_status=pass` 就等于 loss 链也通过

也不是。
当前 `pass` 的前提是 `runtime_profile=data_protocol_preflight`。

### 误解 3：这个脚本以后一定不能扩展

也不是。
后面可以扩展，但扩展必须发生在 `02_UNet流程验证`，而且不能破坏这里已经冻结的输入链。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事:

1. 打开 `../../../../scripts/train.py`，确认 `build_runtime_payload()` 里真的写了 `runtime_profile=data_protocol_preflight`
2. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`，确认 `input_shape=[522, 775, 3]`
3. 打开 `../../../../reports/stage_reports/data_stage_acceptance.md`，确认 `preflight_pass=True`

学完后你应该具备什么能力？

你应该能一眼分清:

- 当前 `scripts/train.py` 已经成立的部分是什么
- 它故意还没做的部分是什么
- 为什么这两件事同时成立，并不矛盾
