# experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 已经把配置快照写出来了，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`？”

因为前者更像开跑前的协议留底。
而当前这份文件更像规范 smoke run 跑完以后留下的结果总索引卡。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 的运行资产说明文。
- 流程: 它位于配置快照和 epoch 结果表已经落盘之后, 用来汇总当前 smoke run 身份与结果结论。
- 结构: 当前文件按 run 身份、协议版本链、训练与评估冻结字段、结果结论四组信息组织。
- 衔接: 它向上回接 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 向下服务 best 结果回查和阶段验收。
- 解释: 它回答“这次规范 smoke run 是谁、按什么协议跑、为什么停、当前最好是谁”。
- 验证: 需要同时对照 `../../../../scripts/train.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和当前 run 目录。
- 误区: 不能把它误读成完整测试包、总结页或可视化资产。
- 自检: 读完后应能说清 `best_selector`、`threshold_source`、`best_epoch` 和 `stop_reason` 各自回答什么问题。
- 局限: 它只证明规范 smoke run 的元信息与 best 结果已经落盘, 不能替代长程训练和完整验收。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` 运行目录里最直接回答“这次 run 最后怎样结束、最好轮次是谁、协议版本链是什么”的正式记录资产。
- 它把配置身份、运行结论和选优结果压进同一份 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`, 方便后续阶段、总结页和人工核对一起回查。

如果没有这份文件, 读者只能看到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 有数字, 但很难快速知道:

- 当前 run 到底是不是规范 smoke-check
- 最优轮次是谁
- 最优指标按什么选
- 这次 run 消费的是哪四份配置

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `baseline run tracking and best-checkpoint provenance`
- 章节: `one run should keep protocol identity and selection result together`
- 公式/定义: `run identity + protocol versions + best result -> one auditable smoke run meta`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../scripts/train.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 对应字段: `run_name`, `train_proto_version`, `eval_proto_version`, `best_selector`, `threshold_source`, `best_epoch`, `best_metric_value`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义是:

1. 当前文件为什么必须存在, 是阶段验收和命名记录规范共同要求
2. 当前文件为什么要显式记录 `best_selector`、`threshold_source` 和版本链, 是评估口径规则明确要求
3. 当前文件为什么属于 `02_UNet流程验证` 的规范 smoke run 正式运行资产, 不是临时备注

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 之所以把 run 身份、协议版本链、选优字段和结果结论压在一处, 不是因为这样看起来方便。

路线锁定文件 `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md` 先限定了 stage02 要先建立最小闭环 run 资产链。

正式规则文件 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md` 和 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md` 又要求版本链、best 选择器和阈值来源必须可审计地回查。

所以这份资产的组织方式本质上是在服务“结果目录里必须有一张能把 smoke run 身份、评估口径和当前 best 结果连起来的正式索引卡”。

## 当前这个文件说明了什么

你可以把它理解成“当前规范 smoke run 的结果总索引卡”。

它位于当前运行资产链的中间层:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 先写配置快照
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 记录训练侧每轮结果
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 记录验证侧每轮结果
4. 当前文件把 run 身份、协议版本和“谁是当前最优”压成单一记录

所以它比单看日志更像“结果回查入口”。

## 这张表/这个文件长什么样

说白了, 当前文件主要分成 4 组信息:

1. run 身份
2. 协议版本链
3. 训练与评估冻结字段
4. 当前 run 的结果结论

## 这些列/字段分别是什么意思

你可以把 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 想成 smoke 结果目录首页贴着的一张索引卡。

这里的字段不是一团混写, 而是 4 组不同职责:

1. run 身份字段解释“这次 run 是谁、属于哪个 stage、模型版本是什么”
2. 协议版本链字段解释“data/train/eval/loss/postprocess 分别沿用哪一版正式协议”
3. 训练与评估冻结字段解释“best 按什么选、threshold 从哪来、scheduler 盯哪一列”
4. 结果结论字段解释“这次 run 为什么停、最好轮次是谁、best 指标值是多少、当前设备与 epoch 数是多少”

只看 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 你当然也能一点点猜。
但当前文件更适合先快速回答“这次 smoke run 是谁、按什么协议跑、为什么停、当前最好是谁”。

## 当前实现状态

- 状态: `已存在`
- 可读性: `可直接人工审阅`
- 当前真实 run 名: `A1_UNet_GlaS_v1_seed3407_smoke`
- 当前 stop_reason: `smoke_check_complete`
- 当前真实结论: `这是当前已落盘的规范 smoke run meta, 用来集中记录 smoke 目录的结果索引信息`

这里同样必须诚实说明:

当前文件已经能证明“run 身份、版本链和 best 结果记录机制已落盘”, 但不能单独证明 TestA 和 TestB 的完整测试包、可视化和最终阶段交接包都已完成。

## 当前真实结果

当前最关键的真实路径至少有 5 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml` 已和它处在同一 run 目录
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 已给出训练侧 epoch 记录
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已给出验证侧指标记录
5. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 已写明 `smoke_check_run_name=A1_UNet_GlaS_v1_seed3407_smoke`

当前最关键的真实字段至少有 10 组:

1. `run_name=A1_UNet_GlaS_v1_seed3407_smoke`
2. `train_proto_version=train_proto_v1`
3. `eval_proto_version=eval_proto_v1`
4. `best_selector=val_objdice_max`
5. `threshold_source=val17`
6. `stop_reason=smoke_check_complete`
7. `best_epoch=1`
8. `best_metric_value=0.26280593599215546`
9. `amp_active=false`
10. `device=cpu`

这说明当前文件已经和真实 smoke 结果目录及真实数值对得上的 run 索引卡。

## 这份 run meta 里到底锁了什么

### 1. 运行身份

当前真实字段包括:

- `run_name: A1_UNet_GlaS_v1_seed3407_smoke`
- `stage_code: A1`
- `dataset_code: glas`
- `model_name: unet`
- `model_version: unet_v1`
- `config_version: v1`

这保证后面回看时不会把 smoke 目录身份和主 run 身份混开。

### 2. 协议版本链

当前真实字段包括:

- `data_proto_version: 01_data_protocol_v1`
- `train_proto_version: train_proto_v1`
- `eval_proto_version: eval_proto_v1`
- `loss_version: seg_loss_v1`
- `postprocess_version: none_in_v1`

这正对应命名与结果记录规范里要求的“版本链必须显式记录”。

### 3. 训练与评估关键冻结字段

当前真实字段包括:

- `optimizer: AdamW`
- `scheduler: ReduceLROnPlateau`
- `scheduler_monitor: val_objdice`
- `epoch_max: 120`
- `early_stop_patience: 20`
- `best_selector: val_objdice_max`
- `threshold_value: 0.5`
- `threshold_source: val17`
- `smoke_check: true`

也就是说, 它不只告诉你这次 run 跑了, 还告诉你它按什么标准选 best。

### 4. 当前 run 的结果结论

当前真实字段包括:

- `stop_reason: smoke_check_complete`
- `best_epoch: 1`
- `best_metric_value: 0.26280593599215546`
- `amp_active: false`
- `epoch_count: 1`
- `device: cpu`

这说明当前规范 smoke run 的确已经形成“跑了多少、为什么停、当前最好是谁”的结果卡片。

## 对应代码里的真实协议痕迹

当前最关键的代码痕迹有四处:

1. `../../../../scripts/train.py` 里 `build_run_meta(...)` 先生成版本链和冻结字段
2. `../../../../scripts/train.py` 在 `smoke_check=true` 时先写一次 run meta 资产到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`
3. 训练结束后 `../../../../scripts/train.py` 再把 `stop_reason`、`best_epoch`、`best_metric_value`、`epoch_count` 更新回同一路径
4. `../../../../src/eval/checkpoint_selector.py` 和 `../../../../src/engine/trainer.py` 共同决定 best 结果如何产生

所以这份 run meta 是训练入口和验证链一起落出来的规范 smoke 正式资产, 不是手工补注释。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/config.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
4. 再回看 `../../../../scripts/train.py`

通过标准:

- `best_selector` 仍是 `val_objdice_max`
- `threshold_source` 仍是 `val17`
- `best_epoch=1` 与当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 的单行记录不冲突
- `smoke_check=true`、`stop_reason=smoke_check_complete` 和当前规范 smoke run 现实一致

## 这个文件没说明什么

当前文件能证明的是:

1. 当前 smoke run 的身份、版本链和 best 结果已被结构化写进结果目录
2. 规范 smoke run 没有只留下终端输出, 而是留下了正式元信息资产
3. 后续阶段或总结页可以先从这里快速回查关键字段

当前文件还不能单独证明的是:

1. TestA 和 TestB 的正式测试结果都已交齐
2. 完整长程正式训练已经结束
3. 只凭这一份 run meta 就足以替代总结页、可视化和错误回退记录

## 常见问题

- 误解 1: 以为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 只是目录级说明
  - 实际上它是把 run 身份、协议版本、best 选择和停训结果压成一张正式索引卡
- 误解 2: 以为它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 完全等价
  - 实际上一个对应主 run 目录, 一个对应规范 smoke run 目录, best 指标值也不同
- 误解 3: 以为它已经能替代总结页
  - 实际上它更像索引卡, 人读摘要还要结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_config.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
- `scripts_train.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. 规范 smoke run 的结果索引卡由谁写出
2. 为什么 `best_metric_value=0.26280593599215546` 要和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 对账
3. 为什么这份文件能证明 smoke meta 资产链成立, 但还不能替代完整交接包
