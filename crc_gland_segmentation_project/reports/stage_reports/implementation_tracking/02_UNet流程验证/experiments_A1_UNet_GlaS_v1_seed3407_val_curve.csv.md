# experiments_A1_UNet_GlaS_v1_seed3407_val_curve.csv.md

## 这份文件的定位

这份文档解释的是主 run 的验证曲线表 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/val_curve.csv`。

当前它是 full run `epoch 1..68` 的验证趋势表。它由 `val_metrics.csv` 提炼而来，专门服务验证走势回看、best 轮解释和阶段总结。

## 一眼先抓住什么

- 当前文件对应主 run full run 的验证曲线表。
- 当前表内共有 `68` 个 epoch 点，从 `1` 连续到 `68`。
- 当前保留的列是 `epoch`、`val_loss`、`val_objdice`、`val_dice`、`val_iou`。
- 当前最佳轮是 `epoch=48`，对应 `val_objdice=0.7626771700880477`。
- 当前最后一轮是 `epoch=68`，对应 `val_objdice=0.7340940301447756`。
- 当前它服务的是验证走势与选优解释，不替代完整验证指标表。

## 这个文件是干什么的

这份 `val_curve.csv` 是从 `val_metrics.csv` 提炼出的轻量验证趋势表。

它把最适合看验证曲线和 best 轮走势的字段单独整理出来，方便回答:

1. `val_loss` 怎样随 epoch 变化
2. `val_objdice` 在哪一轮达到最高
3. `val_dice` 与 `val_iou` 怎样随训练推进而变化

## 当前真实结果

当前最关键的真实字段包括:

- `epoch_count=68`
- `epoch 1`: `val_loss=1.4928572045432196`, `val_objdice=0.2853621859779372`
- `epoch 45`: `val_loss=0.500511646270752`, `val_objdice=0.735281817229058`
- `epoch 48`: `val_loss=0.5105387204223208`, `val_objdice=0.7626771700880477`, `val_dice=0.8383296307209251`, `val_iou=0.7398965439200875`
- `epoch 68`: `val_loss=0.5386648211214278`, `val_objdice=0.7340940301447756`, `val_dice=0.8242471180887933`, `val_iou=0.7300416118417983`

这说明当前文件记录的是完整长程验证趋势。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
2. `../../../../src/engine/trainer.py`

下游消费:

1. 验证曲线绘制
2. best 轮解释
3. `run_summary.md` 和阶段总结中的验证趋势说明

因此它是完整验证表的曲线视图，不是新的评估入口。

## 对应代码里的真实协议痕迹

关键逻辑有三层:

1. `../../../../src/engine/trainer.py` 在主循环中累计 `val_rows`。
2. 训练结束后，`trainer.py` 把 `val_rows` 导出为 `curves/val_curve.csv`。
3. `run_meta.yaml` 与 `best.ckpt` 的 best 选择解释，最终都能回查到这份曲线表和 `val_metrics.csv`。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/val_curve.csv`
2. 确认 epoch 从 `1` 连续到 `68`
3. 查 `epoch 48` 的 `val_objdice`
4. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`

通过标准:

- 曲线点覆盖 `epoch 1..68`
- 行号覆盖 `1..68`
- `epoch 48` 是最佳验证轮
- `epoch 68` 与完整验证表末轮对得上

## 这个文件没说明什么

当前文件能证明的是:

1. 主 run 的验证趋势表已经完整落盘。
2. `val_objdice` 的 best 轮可以被直接回查。
3. 验证曲线资产链已经和 full run 现实对齐。

当前文件不单独替代的是:

1. `val_metrics.csv` 的完整指标列
2. `run_meta.yaml` 的阶段汇总字段
3. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_train_curve.csv.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `val_curve.csv` 是 full run 的验证趋势表。
2. 为什么 `epoch 48` 是最佳轮而 `epoch 68` 仍是最后一轮。
3. 为什么它适合看走势，但不替代完整验证指标表。
