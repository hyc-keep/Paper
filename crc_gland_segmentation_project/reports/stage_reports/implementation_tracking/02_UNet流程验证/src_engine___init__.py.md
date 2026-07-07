# src_engine___init__.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/engine/__init__.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `stable training loop services exposed through one engine facade`
- 章节: `package-level access to scheduler, early stop, and trainer loop`
- 公式/定义: `src.engine` package -> `EarlyStopper` + `build_scheduler()` + `train_model()` as the formal engine-facing API

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/__init__.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/train/unet_flow_v1.yaml`
- 对应字段: `scheduler`, `scheduler_monitor`, `early_stop_patience`, `epoch_max`
- 上游评估配置: `../../../../configs/eval/eval_proto_v1.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/engine/__init__.py`
- 符号: `EarlyStopper` / `build_scheduler()` / `train_model()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 的训练引擎公开入口到底是谁。

答案就是 `../../../../src/engine/__init__.py`。

你可以把它理解成训练闭环的“中控台门面”。

用人话说，真正执行 trainer、scheduler、early stop 细节的是 `../../../../src/engine/trainer.py`、`../../../../src/engine/lr_scheduler.py` 和 `../../../../src/engine/early_stop.py` 这三个下游文件，但正式训练入口并不应该自己去各处拼这些深层路径。

它应该对着一个已经锁定好的 engine 包门面工作。

如果没有这份文件，训练入口会同时承担“找引擎对象”和“调用引擎对象”两层职责，说明文和审计边界就会更乱。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/train/unet_flow_v1.yaml + configs/eval/eval_proto_v1.yaml
        ↓
scripts/train.py
        ↓
src/engine/__init__.py
        ↓
src/engine/lr_scheduler.py + src/engine/early_stop.py + src/engine/trainer.py
        ↓
val_objdice / optimizer.step / best checkpoint / stop reason
```

这里最关键的事实有五条:

1. `../../../../scripts/train.py` 当前真实写了 `from src.engine import EarlyStopper, build_scheduler, train_model`
2. `../../../../src/engine/__init__.py` 把 scheduler、early stop 和 trainer 三个正式入口集中暴露
3. `../../../../scripts/train.py` 会先构造 `scheduler` 和 `early_stopper`，再调用 `train_model()`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 已经写明 `optimizer_step_executed=True`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 已经写明 `backward_executed=true` 与 `optimizer_step_executed=true`

当前最硬的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/engine/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.engine import EarlyStopper, build_scheduler, train_model`
3. `../../../../scripts/train.py` 已写明 `scheduler = build_scheduler(optimizer, train_config)`
4. `../../../../scripts/train.py` 已写明 `early_stopper = EarlyStopper(..., mode="max")`
5. `../../../../scripts/train.py` 已写明 `summary = train_model(...)`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `optimizer_step_executed=True`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true` 与 `optimizer_step_executed=true`

说白了，这里不是“engine 目录里的 `__init__` 文件”，而是正式训练闭环的统一公开入口。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/train/unet_flow_v1.yaml`
- `../../../../configs/eval/eval_proto_v1.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/engine/trainer.py`
- `../../../../src/engine/lr_scheduler.py`
- `../../../../src/engine/early_stop.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义是:

1. 当前训练闭环不能只靠一个大脚本硬写
2. 当前 scheduler、early stop 和 trainer 必须形成正式公开入口层
3. 当前说明文可以把“engine 门面”和“三个底层引擎对象”拆开解释

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式训练引擎包门面
- 当前冻结字段:
  - `scheduler=ReduceLROnPlateau`
  - `scheduler_monitor=val_objdice`
  - `early_stop_patience=20`
  - `best_selector=val_objdice_max`
- 当前最硬证据:
  - `../../../../scripts/train.py` 通过 `src.engine` 取 trainer/scheduler/early-stop 入口
  - `../../../../src/engine/__init__.py` 用 `__all__` 把 3 个正式引擎对象列清楚
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `optimizer_step_executed=True`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`

这里必须诚实说明:

当前证据更强地证明了“stage02 正式训练入口已经通过 `src.engine` 门面接通训练闭环”，还没有单独证明完整多 epoch 提前停止逻辑已经在当前 runtime-check 场景里被真正触发。

## 脚本核心逻辑

### 主要流程

你可以把它想成 4 步:

1. 从 `../../../../src/engine/early_stop.py` 导出 `EarlyStopper`
2. 从 `../../../../src/engine/lr_scheduler.py` 导出 `build_scheduler()`
3. 从 `../../../../src/engine/trainer.py` 导出 `train_model()`
4. 用 `__all__` 把正式训练引擎公开 API 钉死

### 关键点 1: 为什么这三个对象应该一起挂在门面上

因为它们一起构成当前最小训练闭环。

如果少了其中任何一个，训练入口都还得自己下沉到深层模块去拼流程。

### 关键点 2: 为什么包门面值得单独进 A 类

因为当前 `scripts/train.py` 的真实 import 面就在这里。

而且当前训练入口就是通过这层门面把“调度、停训、主循环”三件事一起接进来。

### 关键点 3: 为什么这里不继续暴露别的 engine helper

因为当前冻结的是最小正式闭环，不是所有潜在 engine 工具集合。

门面越窄，审计边界越清楚。

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

“为什么不让 `../../../../scripts/train.py` 直接分别从 `../../../../src/engine/trainer.py`、`../../../../src/engine/lr_scheduler.py`、`../../../../src/engine/early_stop.py` 导入？”

用人话说，当然也能跑。

但那样正式入口层就不存在了。

单独保留 `src.engine` 门面以后，训练入口和说明文都可以先围绕统一引擎 API，再往下追具体实现对象。

### 设计取舍 1: 为什么这里同时公开 trainer、scheduler、early stop

因为当前正式训练闭环恰好就是这三层组合。

### 设计取舍 2: 为什么包门面和 `../../../../src/engine/trainer.py` 不能混成一篇

因为二者回答的问题不同:

1. `../../../../src/engine/trainer.py` 解释主循环怎么跑
2. 这份门面说明文解释正式引擎入口在哪里

### 设计取舍 3: 为什么 runtime-check 仍然能证明这层门面有价值

因为哪怕 runtime-check 只跑最小 batch，它也已经真实走过了 loss、backward 和 optimizer.step。

只要入口就是通过 `src.engine` 取引擎对象，这层门面就已经进入正式证据链。

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../scripts/train.py`
2. 打开 `../../../../src/engine/__init__.py`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- 训练入口是否直接从 `src.engine` 导入三个正式引擎对象
- `scheduler` 和 `early_stopper` 是否都在入口里被实例化
- `backward_executed` 和 `optimizer_step_executed` 是否都为真
- `__all__` 是否已经把正式 engine API 列清楚

### 当前真实结果

当前最关键的物理证据至少有 8 组:

1. 文件路径已经固定在 `../../../../src/engine/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.engine import EarlyStopper, build_scheduler, train_model`
3. `../../../../scripts/train.py` 已写明 `scheduler = build_scheduler(optimizer, train_config)`
4. `../../../../scripts/train.py` 已写明 `early_stopper = EarlyStopper(..., mode="max")`
5. `../../../../scripts/train.py` 已写明 `summary = train_model(...)`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `optimizer_step_executed=True`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`
8. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `optimizer_step_executed=true`

## 常见误区

- 误区 1: 以为 `src.engine.__init__` 只是导出汇总
  - 实际上它已经是训练入口的真实引擎公开接口
- 误区 2: 以为解释了 `../../../../src/engine/trainer.py` 就够了
  - 实际上门面层和底层实现层不是一回事
- 误区 3: 以为 runtime-check 没跑到 early stop 就不能解释 engine 门面
  - 实际上门面对象解释的是正式入口层，不是声称每个分支都已被逐项触发

## 建议联读

- `src_engine_trainer.py.md`
- `src_engine_lr_scheduler.py.md`
- `src_engine_early_stop.py.md`
- `configs_train_unet_flow_v1.yaml.md`
- `scripts_train.py.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `src_engine_trainer.py.md`，理解主循环闭环
2. 再去看 `src_engine_lr_scheduler.py.md` 和 `src_engine_early_stop.py.md`，理解调度与停训规则
3. 最后回到 `scripts_train.py.md`，确认入口为什么只面对 `src.engine` 门面

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 为什么 `src.engine` 包门面本身应该算正式对象
2. 它和 `../../../../src/engine/trainer.py`、`../../../../src/engine/lr_scheduler.py`、`../../../../src/engine/early_stop.py` 的边界分别是什么
3. 为什么当前训练入口必须通过这个门面拼接闭环
4. 为什么 runtime-check 足以证明这层入口已经真的进入主链

## 5 分钟自检任务

1. 回到 `../../../../scripts/train.py`，找到 `from src.engine import ...`
2. 回到 `../../../../src/engine/__init__.py`，说出它公开了哪 3 个正式符号
3. 再回看 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`，解释为什么 `optimizer_step_executed=true` 能说明这条引擎入口链已经真的跑过

如果这三步你都能顺下来，说明你已经把这份 engine package 门面说明文真正看懂了。
