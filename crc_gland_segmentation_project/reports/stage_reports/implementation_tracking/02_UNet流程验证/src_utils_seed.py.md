# src_utils_seed.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/utils/seed.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `reproducible deep-learning experiment setup`
- 章节: `align Python, NumPy and Torch random states before training`
- 公式/定义: one frozen train_seed -> synchronized RNG states

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/utils/seed.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 对应字段: `train_seed=3407`, `aggregation=single_seed`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/utils/seed.py`
- 符号: `set_global_seed()` / `seed_worker()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 里，到底是谁把 `train_seed=3407` 这条正式实验设定真正落实成运行时随机状态。

答案就是 `../../../../src/utils/seed.py`。

你可以把它理解成 stage02 训练链里的“随机性总闸”。

用人话说，配置文件里写了一个种子值，还不等于程序真的按这个种子跑。真正负责把 Python、NumPy、Torch 这些随机源一起钉住的，是这里。

如果没有这份文件，`../../../../scripts/train.py` 虽然知道 `train_seed=3407`，也没法保证 transform 随机增强、参数初始化和训练行为都对齐到同一套 run 语义。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
src/utils/seed.py
        ↓
scripts/train.py
        ↓
transforms / model init / optimizer / training run
```

这里最关键的事实有三条:

1. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 已冻结 `train_seed=3407`
2. `../../../../scripts/train.py` 会在构造 transform、dataset、model 和 optimizer 之前调用 `set_global_seed(int(experiment_config["train_seed"]))`
3. 当前 experiment config 已写明 `aggregation=single_seed`，说明正式 run 不是多 seed 聚合实验

当前最硬的物理证据至少有 5 组:

1. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 写明 `train_seed=3407`
2. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 写明 `aggregation=single_seed`
3. `../../../../scripts/train.py` 写明 `set_global_seed(int(experiment_config["train_seed"]))`
4. `../../../../scripts/train.py` 在 seed 之后才构造 transform、dataset、model 和 optimizer
5. 当前 run 名 `A1_UNet_GlaS_v1_seed3407` 也把 seed 编码进正式实验身份

说白了，这里不是锦上添花的小工具，而是把“这次 run 到底按哪个随机种子算”变成正式工程行为的地方。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../scripts/train.py`
- `../../../../src/data/transforms.py`
- `../../../../src/models/unet.py`
- `../../../../reports/stage_reports/implementation_tracking/02_UNet流程验证/scripts_train.py.md`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义很直接:

1. 当前 seed 不是实验时临时填的注释值，而是正式 experiment 身份的一部分
2. 当前 run 是单 seed 语义，不是多次重复后再聚合
3. 当前随机性冻结必须发生在训练构图之前，不然配置和真实行为会断链

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式随机种子对齐层
- 当前冻结字段:
  - `train_seed=3407`
  - `aggregation=single_seed`
- 当前最硬证据:
  - `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 写明 `train_seed=3407`
  - `../../../../scripts/train.py` 写明 `set_global_seed(int(experiment_config["train_seed"]))`
  - 当前正式 run 名已经固定为 `A1_UNet_GlaS_v1_seed3407`

这里必须诚实说明:

当前证据能证明的是“全局随机种子已经被正式入口消费”，还没有单独证明“worker 级 seeding 在多 worker DataLoader 场景里已经作为正式 run 路径被触发”，因为当前 `num_workers=0`。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 用 `set_global_seed()` 同步 Python、NumPy、Torch 的全局随机源
2. 如果 CUDA 可用，再同步 CUDA 路径
3. 用 `seed_worker()` 为后续多 worker DataLoader 预留统一 worker seeding 口径

### 关键点 1: 为什么要同时 seed 三套随机源

因为当前训练链不是只靠一个库在制造随机性。

transform、numpy、torch 各自都可能带来不同的随机行为，必须一起钉住。

### 关键点 2: 为什么在构图之前就调用

因为当前想冻结的是整个 run，不只是训练 for 循环里的后半段。

如果参数初始化或增强配置在 seed 之前就发生，后面再 seed 也补不回来。

### 关键点 3: 为什么当前还保留 `seed_worker()`

因为虽然正式 DataLoader 现在还是 `num_workers=0`，但后面一旦扩 worker，总不能再临时补另一套随机规则。

现在把口径先放在同一文件里，边界更稳。

## 如何运行这个脚本

这份对象本身不是独立 CLI。

它的正式运行方式，是通过 `../../../../scripts/train.py` 的训练支路间接进入。

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

“为什么不直接在训练入口里手写几行 `random.seed()` 就完了？”

用人话说，当然能写，但那样 seed 规则就会和正式对象边界绑不住。

单独拆成工具对象以后，配置、入口、实现和说明文都更容易对账。

### 设计取舍 1: 为什么 run 名也显式编码 seed

因为当前是单 seed 运行语义。

把 seed 写进 run 名，有助于把实验身份和随机性设置绑在一起。

### 设计取舍 2: 为什么当前不额外写 deterministic backend 开关

因为当前 stage02 最小正式闭环先保证主链可解释。

是否进一步冻结 cudnn 级别细节，不在这一轮说明文里提前夸大。

### 设计取舍 3: 为什么 `seed_worker()` 还保留

因为它回答的是“将来扩 worker 时用什么口径”，不是“当前一定已经在正式 run 中被触发”。

把这条边界讲清楚，比假装它已经完整进入主链更重要。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. 打开 `../../../../scripts/train.py`
3. 对照 `../../../../src/utils/seed.py`
4. 回看 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

### 当前最关键的核对点

- `train_seed=3407` 是否和 `set_global_seed(int(experiment_config["train_seed"]))` 对上
- seed 调用是否发生在 transform、dataset、model、optimizer 构造之前
- `aggregation=single_seed` 是否和当前 run 身份对上

### 当前真实结果

当前最关键的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/utils/seed.py`
2. 具体路径已经固定在 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
3. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 写明 `train_seed=3407`
4. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 写明 `aggregation=single_seed`
5. `../../../../scripts/train.py` 写明 `set_global_seed(int(experiment_config["train_seed"]))`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `run_name=A1_UNet_GlaS_v1_seed3407`

## 常见误区

- 误区 1: 以为 seed 只是为了好看
  - 实际上它在正式定义这次 run 的随机性身份
- 误区 2: 以为只有 torch 需要 seed
  - 实际上 Python 和 NumPy 也会影响当前训练链
- 误区 3: 以为 `seed_worker()` 已经在当前正式 run 里被充分验证
  - 实际上当前 DataLoader 仍是 `num_workers=0`

## 建议联读

- `scripts_train.py.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `src_data_transforms.py.md`
- `src_models_unet.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`，搞清楚 seed 是怎样进入正式 experiment 身份的
2. 再去看 `scripts_train.py.md`，搞清楚 seed 调用发生在训练构图的哪一步
3. 最后去看 `src_data_transforms.py.md` 和 `src_models_unet.py.md`，理解随机增强与参数初始化为什么都受这条规则影响

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 当前这个 seed 对象在 stage02 里到底负责哪一段正式职责
2. 为什么当前要把 `train_seed=3407` 写成正式 experiment 身份的一部分
3. 为什么 seed 必须先于训练构图调用
4. 为什么当前不能把 worker seeding 解释成已经完整进入正式多 worker 主链

## 5 分钟自检任务

1. 回到 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`，找到 `train_seed`
2. 回到 `../../../../scripts/train.py`，找到 `set_global_seed(int(experiment_config["train_seed"]))`
3. 再回看 `../../../../src/utils/seed.py`，说出 `set_global_seed()` 和 `seed_worker()` 各自负责哪一层随机性

如果这三步你都能顺下来，说明你已经把这份 seed 说明文真正看懂了。
