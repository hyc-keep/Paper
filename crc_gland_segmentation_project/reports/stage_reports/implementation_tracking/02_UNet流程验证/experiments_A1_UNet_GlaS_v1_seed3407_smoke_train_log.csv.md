# experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_log.csv.md

## 这份文件的定位

你现在可能会问:

“既然 runtime-check 已经证明 loss 跑出来了，为什么还要单独解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`？”

因为 runtime-check 更像一次物理打点。
而当前这份文件回答的是“规范 smoke run 的训练侧有没有把结果写成正式表，而不是只留终端输出”。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 的运行资产说明文。
- 流程: 它位于 trainer 完成 epoch 训练之后、结果目录需要留下结构化训练记录的环节。
- 结构: 当前文件按 epoch 身份、loss 分量、学习率与 batch、AMP 与时间这几组字段组织。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py`, 向下衔接 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、阶段验收和训练日志核对。
- 解释: 它回答“规范 smoke run 训练侧到底有没有把每轮关键数值写成正式表”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 和当前 run 目录。
- 误区: 不能把单行 smoke-check 日志误读成长程正式训练趋势。
- 自检: 读完后应能说清表头字段是谁写的、这一行数值说明了什么、哪些结论还不能提前说。
- 局限: 它只证明训练日志资产链已经接通, 不能替代验证表、总结页和完整 epoch 序列。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里记录训练侧 epoch 结果的正式日志资产。
- 它负责回答“训练这边到底有没有留下结构化数值记录”, 而不是只靠终端输出或记忆回忆。

当前这份 CSV 很小, 只有一行。
但它小不代表不正式, 它恰好说明: 规范 smoke run 已经把训练日志链打通了。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `baseline training trace persistence`
- 章节: `epoch-level optimization records should be auditable`
- 公式/定义: `one epoch result -> one structured smoke training log row`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 当前训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 对应字段: `epoch`, `epoch_train_loss`, `epoch_loss_bce`, `epoch_loss_dice`, `lr`, `batch_size`, `amp`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件补充: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 用 CSV 记录 epoch、loss、学习率和时间，是为了把 smoke 训练侧结果写成可回查的结构化记录。

路线锁定文件先要求 stage02 把最小训练闭环跑通。
正式规则文件又要求训练侧结果不要只停在终端打印, 而要落成可以回查的正式结果表。

所以这份资产的组织方式本质上是在服务“每完成一轮 smoke 训练, 就留下一个可审计的 epoch 级数值记录”这条正式规则链。

## 当前这个文件说明了什么

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 说明的是:

1. 上游的 `../../../../src/engine/trainer.py` 已把 epoch 训练结果写成正式 CSV
2. 当前 smoke run 目录已经不只剩终端输出, 而是有一张可审计的训练日志表
3. 下游的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、阶段验收核对和总结页都可以继续消费这里的训练字段

## 这张表/这个文件长什么样

当前文件虽然只有 1 行数据, 但结构很清楚:

1. epoch 身份列
2. train 总 loss 列
3. BCE / Dice 分量列
4. 学习率与 batch 列
5. AMP 和 epoch 时间列

## 这些列/字段分别是什么意思

这里的字段至少分成 5 组:

1. `epoch` 先解释这一行属于第几轮训练
2. `epoch_train_loss` 解释这一轮训练总 loss 到底是多少
3. `epoch_loss_bce` 和 `epoch_loss_dice` 解释 BCE 与 Dice 两个分量各占多少
4. `lr` 与 `batch_size` 解释当轮优化步使用的学习率和 batch 规模
5. `amp` 与 `epoch_time_sec` 解释配置层 AMP 允许值和这一轮训练耗时

它不负责告诉你全阶段最后赢没赢。
它先负责保证“这一轮到底跑了什么数”能被正式回查。

## 当前实现状态

- 状态: `已存在`
- 当前行数: `1`
- 当前真实结论: `当前只记录到规范 smoke-check 的 1 个 epoch, 但训练日志链已经打通`

这里也要诚实写清:
当前文件能证明“训练日志 CSV 已真实写出”, 但不能单独证明长程训练趋势已经稳定。

## 当前真实结果

当前最关键的真实路径至少有 5 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`
2. `../../../../src/engine/trainer.py` 已把训练日志路径固定到当前结果目录
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已和当前训练日志处在同一 run 目录
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已作为验证侧配套结果表存在
5. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 已冻结当前 smoke 目录身份

当前最关键的真实字段至少有 8 组:

1. `epoch=1`
2. `epoch_train_loss=1.210294485092163`
3. `epoch_loss_bce=0.6425005197525024`
4. `epoch_loss_dice=0.5677939653396606`
5. `lr=0.001`
6. `batch_size=2`
7. `amp=true`
8. `epoch_time_sec=13.2616`

这说明当前文件虽然小, 但已经是带有真实数值的训练记录。

## 这份训练日志里到底写了什么

当前表头是:

`epoch,epoch_train_loss,epoch_loss_bce,epoch_loss_dice,lr,batch_size,amp,epoch_time_sec`

当前唯一一行真实数值是:

- `epoch=1`
- `epoch_train_loss=1.210294485092163`
- `epoch_loss_bce=0.6425005197525024`
- `epoch_loss_dice=0.5677939653396606`
- `lr=0.001`
- `batch_size=2`
- `amp=true`
- `epoch_time_sec=13.2616`

## 对应代码里的真实协议痕迹

当前最关键的代码痕迹有三处:

1. `../../../../src/engine/trainer.py` 把训练日志路径固定到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`
2. `../../../../src/engine/trainer.py` 通过 `_append_csv_row(...)` 统一写表头和一行 epoch 结果
3. `../../../../scripts/train.py` 负责在 `smoke_check=true` 时先建立 `A1_UNet_GlaS_v1_seed3407_smoke` 结果目录

因此当前 CSV 是 trainer 的正式输出资产。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`
2. 回看 `../../../../src/engine/trainer.py`
3. 再对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`

通过标准:

- 表头字段完整存在
- 当前至少有 `epoch=1` 这一行
- `lr=0.001`、`batch_size=2` 和 train config 冻结值对得上
- `amp=true` 说明记录的是配置层允许值, 最终运行态还要结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 里的 `amp_active`

## 这个文件没说明什么

当前文件能证明的是:

1. 训练日志资产链已经从 trainer 真的落到结果目录
2. 当前规范 smoke run 至少留下了 1 行正式训练记录
3. loss、学习率和 batch 等关键字段已经有结构化表头

当前文件还不能单独证明的是:

1. 长程训练趋势已经稳定
2. 完整正式训练已经跑满并交齐所有 epoch 记录
3. 只看训练日志就足够代替验证表、run meta 和总结页

## 常见问题

- 误解 1: 以为一行 CSV 没什么价值
  - 实际上它已经证明训练日志资产链从 trainer 到结果目录是通的
- 误解 2: 以为 `amp=true` 就代表本次 CPU 运行真的启用了 AMP
  - 实际上这里更接近“配置允许值”, 最终运行态还要结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 里的 `amp_active`
- 误解 3: 以为有了 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 就能证明完整正式训练结束
  - 实际上当前只有 smoke-check 级别的一轮记录

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `src_engine_trainer.py.md`
- `configs_train_unet_flow_v1.yaml.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. 当前 smoke 训练日志 CSV 由谁写出, 字段为何是现在这几个
2. 为什么只有一行也足以证明日志资产链已经接通
3. 为什么它仍然不能被夸大成完整长程训练趋势证据
