# src_models___init__.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/models/__init__.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `stable segmentation model construction exposed behind one package-level builder`
- 章节: `package facade for the frozen UNet public entry`
- 公式/定义: `src.models` package -> `UNet` + `build_unet_model()` as the formal model-facing API

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/models/__init__.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/model/unet_v1.yaml`
- 对应字段: `model_name`, `model_version`, `in_channels`, `out_channels`, `base_channels`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../src/models/__init__.py`
- 符号: `UNet` / `build_unet_model()`

## 这个脚本的作用

这份对象说明文回答的是:

当前 stage02 到底是谁把“正式模型入口”从具体实现细节里单独拎出来。

答案就是 `../../../../src/models/__init__.py`。

你可以把它理解成模型层的“正式挂号窗口”。

用人话说，真正实现 UNet 细节的是 `../../../../src/models/unet.py`，但训练入口并不应该总是直接盯着那个具体文件。

它应该面对已经冻结好的模型公开入口。

如果没有这份文件，训练入口、runtime checker 和后续说明文都只能回链到具体实现文件，没法把“包级正式入口”和“底层结构实现”分层讲清楚。

## 这个脚本在整个阶段中的位置

这份对象在链路里的位置可以先记成下面这样:

```text
configs/model/unet_v1.yaml
        ↓
scripts/train.py
        ↓
src/models/__init__.py
        ↓
src/models/unet.py
        ↓
runtime-check output_shape=[2, 1, 512, 512]
```

这里最关键的事实有四条:

1. `../../../../scripts/train.py` 当前真实写了 `from src.models import build_unet_model`
2. `../../../../src/models/__init__.py` 只公开 `UNet` 和 `build_unet_model`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明字段 `model_registry` 已回链到真实文件 `../../../../src/models/__init__.py`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`

当前最硬的物理证据至少有 6 组:

1. 文件路径已经固定在 `../../../../src/models/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.models import build_unet_model`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `model_registry=pass`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 明确回链到 `src/models/__init__.py`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`

说白了，这里不是“模型目录里必须有个 `__init__`”，而是训练入口到底通过哪个包级接口拿到正式模型。

## 与项目其他部分的关联

### 上游依赖

- `../../../../configs/model/unet_v1.yaml`
- `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- `../../../../scripts/train.py`

### 下游消费者

- `../../../../src/models/unet.py`
- `../../../../src/engine/trainer.py`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

这一组回链最重要的意义是:

1. 当前正式模型只允许标准单头 UNet
2. 当前正式模型入口必须可审计
3. 当前包门面和底层实现要分层说明

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式模型包门面
- 当前冻结字段:
  - `model_name=unet`
  - `model_version=unet_v1`
  - `in_channels=3`
  - `out_channels=1`
- 当前最硬证据:
  - `../../../../scripts/train.py` 通过 `src.models` 取模型 builder
  - `../../../../src/models/__init__.py` 用 `__all__` 明确公开 `UNet` 与 `build_unet_model`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明 `model_registry=pass`
  - `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`

这里必须诚实说明:

当前证据更强地证明了“当前 stage02 正式模型公开入口已经锁定到 `src.models` 包门面”，还没有单独证明后续若引入别的模型家族时，这个门面已经对多模型共存场景完成扩展。

## 脚本核心逻辑

### 主要流程

你可以把它想成 3 步:

1. 从 `../../../../src/models/unet.py` 导出 `UNet`
2. 从 `../../../../src/models/unet.py` 导出 `build_unet_model()`
3. 用 `__all__` 把正式公开模型 API 清单固定下来

### 关键点 1: 为什么要同时公开类和 builder

因为两层角色不一样。

`UNet` 是正式模型主体；
`build_unet_model()` 是配置到实例的正式装配入口。

把它们都挂在门面上，训练入口和说明文都更容易对齐。

### 关键点 2: 为什么包门面值得单独进 A 类

因为当前 runtime checker 已经把 `src/models/__init__.py` 当成真实 `model_registry` 锚点。

只要它进入了正式运行和审计链，就不是普通语法壳。

### 关键点 3: 为什么这里不直接暴露更多实验接口

因为当前 stage02 冻结的是单头 UNet 基线，不是模型实验超市。

门面越窄，正式边界越清楚。

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

“为什么不让 `../../../../scripts/train.py` 直接从 `src.models.unet` 导入 builder，就别多一层门面了？”

用人话说，短期当然也能跑。

但那样模型入口层就不存在了，训练入口会和具体实现路径死绑。

单独保留包门面以后，正式入口、runtime checker 和说明文都能先盯住“模型公开接口”，再往下追具体结构。

### 设计取舍 1: 为什么当前只公开 UNet

因为首轮冻结范围就是单头 UNet。

这里如果提前暴露多模型分支，只会让边界变虚。

### 设计取舍 2: 为什么 `model_registry` 要回链到包门面

因为 checker 更关心“正式训练入口认谁为模型注册层”，而不是只关心某个底层文件是否存在。

### 设计取舍 3: 为什么这个对象不能被 `src_models_unet.py.md` 替代

因为二者回答的问题不同:

1. `src_models_unet.py.md` 解释结构实现
2. 这份门面说明文解释正式公开入口

## 如何验证脚本运行结果

### 检查方法

1. 打开 `../../../../scripts/train.py`
2. 打开 `../../../../src/models/__init__.py`
3. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`
4. 打开 `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json`

### 当前最关键的核对点

- 训练入口是否直接从 `src.models` 导入 builder
- `model_registry` 是否已经回链到 `../../../../src/models/__init__.py`
- 输出 shape 是否和单通道分割头一致
- loss 是否已经真的跑出来

### 当前真实结果

当前最关键的物理证据至少有 7 组:

1. 文件路径已经固定在 `../../../../src/models/__init__.py`
2. `../../../../scripts/train.py` 已写明 `from src.models import build_unet_model`
3. `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md` 写明字段 `model_registry` 已回链到真实文件 `../../../../src/models/__init__.py`
4. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `output_shape=[2, 1, 512, 512]`
5. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `loss_value=1.2771382331848145`
6. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `backward_executed=true`
7. `../../../../b_class_auxiliary/runtime_checks/runtime_evidence.json` 写明 `optimizer_step_executed=true`

## 常见误区

- 误区 1: 以为 `src.models.__init__` 只是语法壳
  - 实际上它已经是 runtime checker 真实回链的 `model_registry`
- 误区 2: 以为解释了 `../../../../src/models/unet.py` 就等于解释了模型入口层
  - 实际上包门面和底层实现回答的问题不同
- 误区 3: 以为包门面越宽越灵活
  - 实际上当前阶段更需要冻结边界，而不是提前铺很多实验接口

## 建议联读

- `src_models_unet.py.md`
- `configs_model_unet_v1.yaml.md`
- `scripts_train.py.md`
- `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`

## 与下游对象怎么衔接

如果你看完这里还想继续往下追，最短路径是:

1. 先去看 `configs_model_unet_v1.yaml.md`，确认模型参数冻结来源
2. 再去看 `src_models_unet.py.md`，理解具体 UNet 结构
3. 最后回到 `scripts_train.py.md`，看训练入口怎样通过 `src.models` 门面把模型接进主链

## 学完后你应该具备什么能力

学完这份文档后，你至少应该能回答下面 4 个问题:

1. 为什么 `src.models` 包门面本身应该算正式对象
2. 它和 `src/models/unet.py` 的分工边界是什么
3. 为什么 `model_registry` 更适合回链到包门面
4. 为什么当前门面只公开 UNet 而不继续扩更多模型

## 5 分钟自检任务

1. 回到 `../../../../scripts/train.py`，找到 `from src.models import build_unet_model`
2. 回到 `../../../../src/models/__init__.py`，说出它公开了哪两个正式符号
3. 再回看 `../../../../b_class_auxiliary/runtime_checks/runtime_check_report.md`，解释 `model_registry=pass` 为什么能证明这个门面已经进入正式运行链

如果这三步你都能顺下来，说明你已经把这份 model package 门面说明文真正看懂了。
