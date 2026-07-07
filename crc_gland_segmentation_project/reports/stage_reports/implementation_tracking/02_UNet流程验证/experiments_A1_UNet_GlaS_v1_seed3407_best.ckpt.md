# experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md

## 这份文件的定位

这份文档解释的是主 run 的正式最优 checkpoint `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`。

当前它记录的是 full run 中按 `val_objdice_max` 选出来的正式最优快照。

## 一眼先抓住什么

- 当前 `best.ckpt` 对应的是主 run full run 的正式最优权重。
- 当前最优轮次是 `epoch=48`。
- 当前最优指标值是 `metric_value=0.7626771700880477`。
- 这个结果与 `run_meta.yaml` 的 `best_epoch=48`、`best_metric_value=0.7626771700880477` 一致。
- 后续 `scripts/test.py` 正式测试默认消费的就是这份 checkpoint。

## 这个文件是干什么的

它回答的是:

1. 当前 full run 里哪一轮被认定为最佳
2. 最佳模型的参数快照保存在哪里
3. 后续正式测试应该默认加载哪个 checkpoint

如果没有这份文件，虽然 `run_meta.yaml` 会告诉你 `best_epoch=48`，但无法直接执行正式 `TestA/TestB` 推理和结果导出。

## 当前真实结果

当前最关键的真实信息是:

- 路径: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
- `epoch=48`
- `metric_value=0.7626771700880477`
- `model_state_dict` 存在
- `optimizer_state_dict` 存在
- 当前正式测试使用这份 checkpoint 导出了 `TestA60/TestB20`

这说明它已经是主 run 正式测试默认消费的最佳模型入口。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
2. `../../../../src/eval/checkpoint_selector.py`
3. `../../../../src/engine/trainer.py`

下游消费:

1. `../../../../scripts/test.py`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/*`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/*`

## 对应代码里的真实协议痕迹

关键逻辑很清楚:

1. `../../../../src/eval/checkpoint_selector.py` 按 `val_objdice` 决定当前轮是否刷新 best。
2. `../../../../src/engine/trainer.py` 在 `is_best` 为真时写入 `best.ckpt`。
3. `../../../../scripts/test.py` 默认解析 `run_dir/checkpoints/best.ckpt` 作为正式测试入口。

所以现在讨论 `best.ckpt` 时，应直接把它理解成 full run 的正式最佳 checkpoint。

## 如何手工验证这个文件的正确性

检查方法:

1. 读取 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`

通过标准:

- `epoch=48`
- `metric_value=0.7626771700880477`
- `run_meta.yaml` 中 `best_epoch=48`
- `run_meta.yaml` 中 `best_checkpoint_epoch=48`
- `scripts/test.py` 默认使用这份 checkpoint 成功导出 `TestA60/TestB20`

## 这个文件没说明什么

当前文件能证明的是:

1. full run 最优模型快照已经真实落盘。
2. 正式测试默认消费的最佳模型入口已经成立。
3. 当前主 run 的最佳模型入口已经稳定落盘并可直接回查。

当前文件不单独替代的是:

1. `val_metrics.csv` 的逐轮对比表
2. `last.ckpt` 的最后停轮状态
3. `testA_metrics.csv` / `testB_metrics.csv` 的测试结果
4. `run_summary.md` / `run_meta.yaml` 的收口结论页

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `best.ckpt` 是 full run 的最佳模型入口。
2. 为什么正式测试默认应该加载它，而不是 `last.ckpt`。
3. `epoch=48` 和 `metric_value=0.7626771700880477` 如何与 `run_meta.yaml`、`val_metrics.csv` 对账。
