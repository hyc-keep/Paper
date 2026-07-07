# src_utils___init__.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/utils/__init__.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `stable reproducibility helpers exposed behind one utility facade`
- 章节: `package-level access to global seed and dataloader worker seeding`
- 公式/定义: `src.utils` package -> `set_global_seed()` + `seed_worker()` as the formal reproducibility API

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/utils/__init__.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 对应字段: `train_seed`
- 上游训练配置: `../../../../configs/train/unet_flow_v1.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/utils/__init__.py`
- 符号: `set_global_seed()` / `seed_worker()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 的随机性公开入口到底是谁。

答案就是 `../../../../src/utils/__init__.py`。

你可以把它理解成 reproducibility 层的“正式接口面板”。

用人话说，真正去设 Python / NumPy / Torch seed 的逻辑在 `../../../../src/utils/seed.py`，但训练入口不应该直接和具体实现文件死绑。

它应该面对一个已经冻结好的 utility 包门面。

如果没有这份文件，训练入口只是碰巧调用了某个 seed helper；有了它，才算正式声明“随机性入口就在这里”。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
        ↓
scripts/train.py
        ↓
src/utils/__init__.py
        ↓
src/utils/seed.py
        ↓
single-seed training runtime identity
```

这里最关键的事实有四条:

1. `../../../../scripts/train.py` 当前真实写了 `from src.utils import set_global_seed`
2. `../../../../src/utils/__init__.py` 公开了 `set_global_seed()` 和 `seed_worker()`
3. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 冻结了 `train_seed=3407`
4. 当前 stage02 的单 seed run 身份就是靠这条入口链建立的

当前最硬的物理证据至少有 5 组:

1. 文件路径已经固定在 `../../../../src/utils/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.utils import set_global_seed`
3. `../../../../scripts/train.py` 已写明 `set_global_seed(int(experiment_config["train_seed"]))`
4. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 的正式 run 名已经把 `seed3407` 写进实验身份
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明当前正式 run 已实际完成 `backward_executed=true` 和 `optimizer_step_executed=true`

说白了，这里不是“utils 目录里的一个语法壳”，而是当前正式随机性入口的公开接口层。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/utils/seed.py`
- `../../../../src/engine/trainer.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前训练随机性口径必须冻结到正式入口
2. 当前 `train_seed=3407` 不能只停留在 experiment config 文本里
3. 当前说明文可以把“utility 门面”和“seed 具体实现”拆开解释

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式随机性包门面
- 当前冻结字段:
  - `train_seed=3407`
- 当前最硬证据:
  - `../../../../scripts/train.py` 通过 `src.utils` 取正式随机性入口
  - `../../../../src/utils/__init__.py` 用 `__all__` 明确公开 `set_global_seed` 和 `seed_worker`
  - `../../../../scripts/train.py` 已写明 `set_global_seed(int(experiment_config["train_seed"]))`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明当前正式 run 已完成一次真实训练步

这里必须诚实说明:

当前证据更强地证明了“正式训练入口已经通过 `src.utils` 门面消费随机性入口”，还没有单独证明 dataloader worker 的多进程随机性在当前 CPU runtime-check 场景里被专门拆出来审计。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 从 `../../../../src/utils/seed.py` 导出 `set_global_seed()`
2. 从 `../../../../src/utils/seed.py` 导出 `seed_worker()`
3. 用 `__all__` 把正式公开随机性 API 清单固定下来

### 关键点 1: 为什么这里只公开 seed 相关接口

因为当前 utility 层最正式、最冻结的职责就是 reproducibility。

这里如果混入很多杂项 helper，正式边界会开始发虚。

### 关键点 2: 为什么包门面值得单独进 A 类

因为当前训练入口真实 import 面就在这里。

只要 `scripts/train.py` 正式通过它取随机性入口，它就已经进入工程公开边界。

### 关键点 3: 为什么门面对象不能被 `src_utils_seed.py.md` 替代

因为二者回答的问题不一样:

1. `src_utils_seed.py.md` 解释随机种子怎么具体落地
2. 这份门面说明文解释正式入口为什么锁定在 `src.utils`

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

“为什么不让 `../../../../scripts/train.py` 直接从 `src.utils.seed` 导入，不要多一层门面？”

用人话说，短期可以。

但那样 utility 公开接口层就不存在了。

单独保留 `src.utils` 门面以后，训练入口、说明文和后续裁决都能先盯住正式随机性入口，再往下追具体实现。

### 设计取舍 1: 为什么这里公开 `seed_worker()`

因为正式随机性边界不只包含主进程 seed，也包含 dataloader worker seed。

### 设计取舍 2: 为什么 utility 层当前不继续扩别的 helper

因为当前最稳定、最能形成正式公开边界的只有随机性入口。

### 设计取舍 3: 为什么 run 名里的 `seed3407` 也算证据

因为它把 experiment 身份、配置冻结和入口消费统一绑在了一起。

它不能替代代码调用证据，但能补强“当前单 seed run 身份没有漂移”。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. 打开 `../../../../scripts/train.py`
3. 打开 `../../../../src/utils/__init__.py`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- 训练入口是否直接从 `src.utils` 导入 `set_global_seed`
- `train_seed=3407` 是否和 experiment 身份一致
- `__all__` 是否已经把正式随机性 API 列清楚
- 当前 runtime 是否已经真实执行过一次训练步

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/utils/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.utils import set_global_seed`
3. `../../../../scripts/train.py` 已写明 `set_global_seed(int(experiment_config["train_seed"]))`
4. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 已把 `seed3407` 写进正式实验身份
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `optimizer_step_executed=true`

## 常见误区

- 误区 1: 以为 `src.utils.__init__` 只是工具导出壳
  - 实际上它已经是正式随机性入口层
- 误区 2: 以为 seed 入口只要有配置值就够了
  - 实际上还得有训练入口真实消费它
- 误区 3: 以为 utility 门面不值得单独解释
  - 实际上公开接口层和底层实现层在审计上不是一回事

## 建议联读

- `src_utils_seed.py.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `scripts_train.py.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`，确认单 seed run 身份冻结来源
2. 再去看 `src_utils_seed.py.md`，理解随机种子具体怎样落地
3. 最后回到 `scripts_train.py.md`，确认训练入口为什么只面对 `src.utils` 门面

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 为什么 `src.utils` 包门面本身应该算正式对象
2. 它和 `../../../../src/utils/seed.py` 的边界分别是什么
3. 为什么当前训练入口必须通过这个门面取随机性入口
4. 为什么单 seed 实验身份可以反过来补强这个门面的正式性

## 5 分钟自检任务

1. 回到 `../../../../scripts/train.py`，找到 `from src.utils import set_global_seed`
2. 回到 `../../../../src/utils/__init__.py`，说出它公开了哪两个正式符号
3. 再回看 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`，解释为什么 `seed3407` 不能只停留在文件名上，还要被入口真实消费

如果这三步你都能顺下来，说明你已经把这份 utility package 门面说明文真正看懂了。
