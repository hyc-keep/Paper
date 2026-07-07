# experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md

## 这份文件的定位

这份文档解释的是主 run 的训练日志 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`。

当前它记录的是一次 full run 的完整训练轨迹，是覆盖 `68` 个 epoch 的正式训练表。

## 一眼先抓住什么

- 当前训练日志完整覆盖到 `epoch 68`。
- 当前 `epoch_count=68`，与 `run_meta.yaml` 一致。
- 当前 run 以 `early_stopping` 正常结束，没有跑满 `120`，但这是按协议允许的正常收尾。
- 日志中旧的半截 `45` 已经清掉，当前 `45` 与 `val 45` 对得上。
- 当前这张表已经足够支撑正式训练侧验收，而不是仅证明“训练链接通”。

## 这个文件是干什么的

它负责记录 full run 每一轮训练侧的正式数值，包括:

1. `epoch`
2. `epoch_train_loss`
3. `epoch_loss_bce`
4. `epoch_loss_dice`
5. `lr`
6. `batch_size`
7. `amp`
8. `epoch_time_sec`

如果没有它，就无法审计主 run 从第 1 轮到第 68 轮的训练轨迹，也无法核对 `last.ckpt`、学习率衰减和早停位置。

## 当前真实结果

当前应当按 full run 现实理解这份文件:

- 当前总 epoch 数: `68`
- 当前最后一轮: `epoch=68`
- 当前表内连续记录 `epoch 1..68`
- 当前 `lr` 随 scheduler 衰减到末轮 `3.90625e-06`
- 当前训练轨迹覆盖 early stopping 之前的完整长程过程

当前表中最关键的阶段性事实包括:

- `epoch 48` 对应最佳验证期附近
- `epoch 68` 对应实际停训位置
- 旧的半截 `45` 已删除，只保留与 `val_metrics.csv` 对得上的正式 `45`

## 它和上下游怎么衔接

上游依赖:

1. `../../../../src/engine/trainer.py`

下游消费:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/curves/train_curve.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
4. 阶段验收里的 `pass_train`

## 对应代码里的真实协议痕迹

关键逻辑如下:

1. `../../../../src/engine/trainer.py` 每个 epoch 结束后构造 `train_row`
2. 通过 `_append_csv_row(...)` 追加到 `train_log.csv`
3. 训练结束后再把 `train_rows` 重写为 `train_curve.csv`

因此现在讨论这份文件时，应直接把它理解成 full run 的原始训练主表。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`

通过标准:

- 行数对应 `epoch 1..68`
- 最后一轮是 `68`
- 没有重复的旧 `45`
- `epoch_count=68`
- `stop_reason=early_stopping`

## 这个文件没说明什么

当前文件能证明的是:

1. full run 训练主表已经完整落盘。
2. 当前主 run 的训练侧资产链已经完整落盘。
3. 训练侧正式验收所需的逐轮记录已经具备。

当前文件不单独替代的是:

1. `val_metrics.csv` 的验证结果
2. `best.ckpt` / `last.ckpt` 的模型状态
3. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
4. `run_summary.md` / `stage_summary.md` 的收口结论

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `train_log.csv` 是 full run 的长程训练主表。
2. 为什么 `epoch_count=68` 依然可以是正式完成，因为它对应 `early_stopping`。
3. 为什么清掉旧的重复 `45` 对正式审计一致性是必要的。
