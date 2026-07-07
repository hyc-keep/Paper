# experiments_A1_UNet_GlaS_v1_seed3407_smoke_config.yaml.md

## 这份文件的定位

你现在可能会问:

“当前 stage02 已经有 5 份配置说明文了，为什么还要单独解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`？”

因为前面的 5 份配置说明文回答的是“单份配置各自冻结了什么”。
而当前这份运行资产回答的是“规范 smoke run 实际把哪 5 段配置一起打包落进了结果目录”。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 的运行资产说明文。
- 流程: 它位于 experiment config 解引用之后、smoke run 目录结果资产落盘之前的配置快照环节。
- 结构: 当前文件按 experiment、data、model、train、eval 五段组织。
- 衔接: 它向上回接 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 和 `../../../../scripts/train.py`, 向下衔接 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`。
- 解释: 它回答“规范 smoke run 实际采用了哪套冻结配置”。
- 验证: 需要同时对照 `../../../../scripts/train.py`、5 份源配置和当前 smoke run 目录。
- 误区: 不能把它误读成主 run `../../../../experiments/A1_UNet_GlaS_v1_seed3407/config.yaml` 的重复副本。
- 自检: 读完后应能说清为什么配置里冻结的是 `smoke_check_run_name=A1_UNet_GlaS_v1_seed3407_smoke`。
- 局限: 它只证明规范 smoke run 配置快照已落盘, 不能替代长程训练、测试和可视化资产。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` 运行目录里把 experiment、data、model、train、eval 五段配置合并落盘的正式资产。
- 它回答的是“规范 smoke run 到底按哪一套冻结配置真的启动了”。

如果没有这份文件, 读者很容易只能看到 `../../../../scripts/train.py` 会写结果, 但不知道当次 smoke run 究竟消费了哪些正式配置字段。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `U-Net baseline execution package`
- 章节: `frozen train and eval protocol must remain auditable`
- 公式/定义: `experiment + data + model + train + eval -> one smoke-run-local config snapshot`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../scripts/train.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 参数冻结总表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `run_name`, `smoke_check_run_name`, `config_refs`, `data_proto_version`, `train_proto_version`, `eval_proto_version`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 3: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义是:

1. 当前文件是 `02_UNet流程验证` 的规范 smoke run 正式运行资产
2. 它为什么要写成结果目录里的单独文件, 不是主观决定, 而是阶段验收和命名记录规范共同要求
3. 它为什么特别要保留 `smoke_check_run_name`, 是为了把规范 smoke 目录身份写死在配置快照里

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 之所以按 experiment、data、model、train、eval 五段组织, 不是随意排版。

路线锁定文件 `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md` 已经把 stage02 锁定成“先把单头 `UNet` 最小闭环跑通”的路线。

正式规则文件 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`、`../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md` 和 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` 又要求把冻结配置与结果目录资产明确落盘。

所以这份资产的组织方式本质上是在服务“主 run 和规范 smoke run 都要各自留下可回查配置快照”这条正式协议链。

## 它在流程里怎么工作

你可以把它理解成“规范 smoke run 实际开跑时的总配置快照”。

它位于当前 stage02 运行资产链的前半段:

1. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 先声明主 run 名和 `smoke_check_run_name`
2. `../../../../scripts/train.py` 在 `smoke_check=true` 时选择 `A1_UNet_GlaS_v1_seed3407_smoke`
3. 当前文件把五段配置合并写入 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
4. 后面的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 再继续记录运行结果

所以它是 smoke 结果目录里最关键的“开跑协议留底”。

## 这张表/这个文件长什么样

说白了, 当前文件就是 5 段拼起来的:

1. `experiment`
2. `data`
3. `model`
4. `train`
5. `eval`

你可以把它想成“把 5 张分散协议卡装订成一本 smoke run 现场留底”。

## 这些列/字段分别是什么意思

前面的 5 份配置说明文更像 5 张单科讲义, 而当前这份 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 更像 smoke 现场真正发到考场里的总试卷。

这里的字段分工可以直接拆成 5 组:

1. `experiment` 字段先解释主 run 身份、smoke 别名、seed 和源配置入口
2. `data` 字段解释数据根目录、split 目录、输入尺寸、mask 判正和 boundary/distance 规则
3. `model` 字段解释当前 `UNet` 结构版本和关键宽度参数
4. `train` 字段解释损失、优化器、scheduler、epoch 上限、batch、AMP 和 smoke 限制
5. `eval` 字段解释 best 选择器、threshold 来源、cast policy 和 boundary metric 宽度

所以这份文件是在把“这次规范 smoke run 真正采用了什么配置”按字段组重新讲清。

## 当前实现状态

- 状态: `已存在`
- 可读性: `可直接人工审阅`
- 当前 run 名: `A1_UNet_GlaS_v1_seed3407_smoke`
- 当前真实结论: `这是当前已落盘的规范 smoke run 配置快照, 用来固定 smoke 目录的配置现场`

这里必须诚实说明:

当前这份资产已经能证明“规范 smoke run 目录确实把冻结配置快照写出来了”, 但不能单独证明“stage02 的完整正式训练、测试和可视化包都已交齐”。

## 当前这个文件说明了什么

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 说明的是:

1. 这次规范 smoke run 真正采用的 5 段冻结配置已经在结果目录里合并落盘
2. 上游的 experiment/data/model/train/eval 配置链已经被当前文件汇成单点回查入口
3. 下游的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 都建立在这份配置快照之上
4. 当前配置里显式保留了 `smoke_check_run_name=A1_UNet_GlaS_v1_seed3407_smoke`
5. 直接依赖的正式规则文件包括 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`、`../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md` 和 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 当前真实结果

当前最关键的真实路径至少有 6 组:

1. 运行资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
2. `../../../../scripts/train.py` 在 `smoke_check=true` 时已把配置快照写进当前结果目录 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已和当前配置快照处在同一 run 目录
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 已证明训练日志资产也写进了同一目录
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已证明验证结果资产也写进了同一目录
6. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 已写明 `smoke_check_run_name: A1_UNet_GlaS_v1_seed3407_smoke`

当前最关键的真实字段至少有 9 组:

1. 字段 `dataset_root` 对应真实路径 `../../../../datasets/01_GlaS_official_raw`
2. 字段 `split_dir` 对应真实路径 `../../../../splits/glas`
3. `input_size=[512, 512]`
4. `mask_positive_rule=mask_gt_0`
5. `model_version=unet_v1`
6. `optimizer=AdamW`
7. `best_selector=val_objdice_max`
8. `threshold_source=val17`
9. `smoke_epochs=1`

这说明当前文件已经不只是抽象模板, 而是和真实 smoke run 目录、真实数据路径、真实训练规则对得上的配置快照。

## 这份配置快照里到底锁了什么

### 1. experiment 身份

当前文件最上面写明:

- `run_name: A1_UNet_GlaS_v1_seed3407`
- `smoke_check_run_name: A1_UNet_GlaS_v1_seed3407_smoke`
- `stage_code: A1`
- `dataset_code: glas`
- `train_seed: 3407`
- `result_tag: reproduced`

这说明规范 smoke 目录身份不是靠目录名猜, 而是被正式字段写死在结果目录里。

### 2. data 协议

当前真实字段包括:

- 字段 `dataset_root` 对应真实路径 `../../../../datasets/01_GlaS_official_raw`
- 字段 `split_dir` 对应真实路径 `../../../../splits/glas`
- `input_size: [512, 512]`
- `mask_positive_rule: mask_gt_0`
- `boundary_width: 3`
- `distance_type: euclidean`

也就是说, 当前数据协议、mask 规则和 boundary/distance 协议都被一起快照下来, 没有留给操作者临场口头解释。

### 3. model 和 train 冻结

当前真实字段包括:

- `model_version: unet_v1`
- `base_channels: 32`
- `loss_name: bce_dice`
- `optimizer: AdamW`
- `scheduler: ReduceLROnPlateau`
- `epoch_max: 120`
- `batch_size: 2`
- `amp: true`
- `smoke_epochs: 1`
- `smoke_train_batches: 2`

这说明模型结构和训练超参数没有只停留在源码默认值里, 而是被拷进了 smoke run 目录。

### 4. eval 口径

当前真实字段包括:

- `best_selector: val_objdice_max`
- `best_metric_name: val_objdice`
- `threshold_value: 0.5`
- `threshold_source: val17`
- `eval_cast_policy: float32_before_threshold`
- `boundary_metric_width: 3`

这正是后面 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和 checkpoint 选择逻辑要继续消费的协议底板。

## 对应代码里的真实协议痕迹

当前最关键的代码痕迹有三处:

1. `../../../../scripts/train.py` 在进入正式训练支路后先拼出 `config_snapshot`
2. `../../../../scripts/train.py` 在 `smoke_check=true` 时把快照写进 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
3. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 决定主 run 名和 smoke run 名的双目录身份

所以当前文件是训练入口真实写出来的规范 smoke 运行资产。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
2. 对照 `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
3. 再对照 `../../../../configs/data/glas.yaml`、`../../../../configs/model/unet_v1.yaml`、`../../../../configs/train/unet_flow_v1.yaml`、`../../../../configs/eval/eval_proto_v1.yaml`
4. 最后回看 `../../../../scripts/train.py`

通过标准:

- 当前文件确实分成 experiment、data、model、train、eval 这五段
- `smoke_check_run_name` 字段真实存在
- `best_selector`、`threshold_source`、`smoke_epochs` 都能和上游配置对上
- 路径 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 真实存在

## 这个文件没说明什么

当前文件能证明的是:

1. 规范 smoke run 目录里的配置快照已经真实落盘
2. 这次 smoke run 消费的 5 段配置可以从一个地方回查
3. 结果目录没有只剩零散日志和口头说明

当前文件还不能单独证明的是:

1. `TestA` 和 `TestB` 的完整正式测试包已经落盘
2. 完整长程训练已经把所有 checkpoint、可视化和总结资产都交齐
3. 只凭这一份文件就可以宣布整个 `02_UNet流程验证` 全量验收完成

## 常见问题

- 误解 1: 以为它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/config.yaml` 完全重复
  - 实际上它对应的是规范 smoke run 目录, 重点是把 `smoke_check_run_name` 与 smoke 限制一起落盘
- 误解 2: 以为有了这份快照就等于完整 run 结果都齐了
  - 实际上它只证明配置快照已落盘, 结果资产还要继续看同目录里的 meta、日志、checkpoint 和 summary
- 误解 3: 以为 smoke run 配置就不是正式资产
  - 实际上它正是配置冻结名对应的规范 smoke 目录资产

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `scripts_train.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. 规范 smoke run 的配置快照为什么也是正式运行资产
2. `smoke_check_run_name` 为什么必须和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 对上
3. 为什么这份文件能证明 smoke 配置资产链成立, 但还不能替代完整结果目录解释
