# experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_curve.csv.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 已经记录了训练日志，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`？”

因为前者更像完整训练日志原表。
而当前这份文件更像给曲线分析和后续汇总准备的轻量训练曲线表。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv` 的运行资产说明文。
- 流程: 它位于 epoch 级训练日志已经累计完成之后, 由 trainer 对 `train_rows` 再整理导出为曲线专用表。
- 结构: 当前文件按 `epoch`、`epoch_train_loss`、`epoch_loss_bce`、`epoch_loss_dice`、`lr` 五列组织。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`, 向下服务曲线绘制、趋势回看和阶段总结。
- 解释: 它回答“训练曲线需要的核心列有没有被单独整理出来”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 和当前 run 目录。
- 误区: 不能把它误读成新的训练来源表或完整日志替身。
- 自检: 读完后应能说清它为什么比 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 更适合画曲线, 但又为什么不能替代原始训练日志。
- 局限: 它只证明训练曲线表已经落盘, 不能替代完整日志、验证表和最终结论。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里专门服务训练曲线阅读的正式资产。
- 它把训练日志里最适合做趋势图的列重新整理成一张更短、更稳定的曲线表。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `epoch-level optimization trace persistence`
- 章节: `training curve export for reproducible trend inspection`
- 公式/定义: `train_rows -> compact train curve table`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 当前训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 对应字段: `epoch`, `epoch_train_loss`, `epoch_loss_bce`, `epoch_loss_dice`, `lr`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv` 只保留训练曲线最核心的 5 列，是为了让趋势阅读和曲线绘制更稳定直接。
它服务的是“完整日志先保留, 曲线表再精简导出”这条正式结果链。

## 当前这个文件说明了什么

它位于当前训练资产链的整理层:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 先保留完整 epoch 日志
2. `../../../../src/engine/trainer.py` 把 `train_rows` 汇总为曲线表
3. 当前文件再把训练趋势最核心的 5 列写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`

所以它是从正式日志中抽取出来的曲线视图资产。

## 这张表/这个文件长什么样

当前文件只有 1 行真实数据, 但结构非常明确:

1. `epoch`
2. `epoch_train_loss`
3. `epoch_loss_bce`
4. `epoch_loss_dice`
5. `lr`

## 这些列/字段分别是什么意思

1. `epoch` 解释当前曲线点对应第几轮
2. `epoch_train_loss` 解释这一轮训练总 loss
3. `epoch_loss_bce` 与 `epoch_loss_dice` 解释 BCE/Dice 两个损失分量
4. `lr` 解释当轮训练采用的学习率

## 当前实现状态

- 状态: `已存在`
- 当前行数: `1`
- 当前真实结论: `训练曲线表已经落盘, 但当前仍是规范 smoke run 的 1 个曲线点`

## 当前真实结果

当前最关键的真实路径至少有 4 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 已作为它的上游日志存在
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv` 已作为同目录对照曲线存在
4. `../../../../src/engine/trainer.py` 已把曲线表写盘逻辑固定到真实目录 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/`

当前最关键的真实字段至少有 5 组:

1. `epoch=1`
2. `epoch_train_loss=1.210294485092163`
3. `epoch_loss_bce=0.6425005197525024`
4. `epoch_loss_dice=0.5677939653396606`
5. `lr=0.001`

## 这份曲线表里到底写了什么

当前表头是:

`epoch,epoch_train_loss,epoch_loss_bce,epoch_loss_dice,lr`

当前唯一一行真实数值是:

- `epoch=1`
- `epoch_train_loss=1.210294485092163`
- `epoch_loss_bce=0.6425005197525024`
- `epoch_loss_dice=0.5677939653396606`
- `lr=0.001`

## 对应代码里的真实协议痕迹

1. `../../../../src/engine/trainer.py` 先在主循环里累计 `train_rows`
2. `../../../../src/engine/trainer.py` 结束后把 `train_rows` 写成 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 提供更完整的上游日志来源

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`
3. 回看 `../../../../src/engine/trainer.py` 里写当前曲线表的分支

通过标准:

- 当前文件真实存在
- 表头包含 `epoch`、`epoch_train_loss`、`epoch_loss_bce`、`epoch_loss_dice`、`lr`
- 当前唯一一行数值能和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 的同轮记录对上

## 这个文件没说明什么

当前文件能证明的是:

1. 训练曲线表已经真实落盘
2. 完整训练日志已经进一步整理成曲线友好格式
3. 当前训练趋势点可以被后续总结或可视化消费

当前文件还不能单独证明的是:

1. 长程训练趋势已经稳定
2. 只看训练曲线就能推断验证表现
3. 只凭这一张表就足以替代 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv` 和总结页

## 常见问题

- 误解 1: 以为这份表和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 完全重复
  - 实际上前者是曲线精简表, 后者是更完整的训练日志
- 误解 2: 以为只有 1 行就不算正式曲线资产
  - 实际上当前只是最小 smoke run, 但曲线资产链已经成立
- 误解 3: 以为看训练曲线就等于看完整个阶段表现
  - 实际上还要结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_curve.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv` 为什么不是冗余副本
2. 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 的分工差异是什么
3. 为什么当前文件能证明训练曲线资产链成立, 但还不能夸大成完整训练趋势结论
