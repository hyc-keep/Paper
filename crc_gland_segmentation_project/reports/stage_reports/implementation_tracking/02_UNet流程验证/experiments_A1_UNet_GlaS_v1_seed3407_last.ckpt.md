# experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md

## 这份文件的定位

这份文档解释的是主 run 的最后状态 checkpoint `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`。

当前它记录的是 full run 实际停表时的最终训练状态。

## 一眼先抓住什么

- 当前 `last.ckpt` 对应主 run full run 的最后一轮状态。
- 当前最后轮次是 `epoch=68`。
- 当前最后轮的 `metric_value=0.7340940301447756`。
- 它与 `run_meta.yaml` 的 `epoch_count=68`、`stop_reason=early_stopping` 一致。
- 它和 `best.ckpt` 不同: `last.ckpt` 记录最后停在哪，`best.ckpt` 记录最佳是谁。

## 这个文件是干什么的

它回答的是:

1. 主 run full run 最后停在什么状态
2. 如果要继续恢复最后训练态，应该从哪份 checkpoint 接
3. 最后一轮和最佳轮是否相同

当前答案是:

- 最后一轮是 `68`
- 最佳轮是 `48`
- 两者不同，因此 `last.ckpt` 和 `best.ckpt` 必须并存

## 当前真实结果

当前关键事实如下:

- 路径: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
- `epoch=68`
- `metric_value=0.7340940301447756`
- `model_state_dict` 存在
- `optimizer_state_dict` 存在
- `run_meta.yaml` 对应 `epoch_count=68`
- `run_meta.yaml` 对应 `stop_reason=early_stopping`
- `train_log.csv` / `val_metrics.csv` 都已经到 `68`

所以它现在代表的是 full run 的正式停训状态。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
3. `../../../../src/engine/trainer.py`

下游用途:

1. 训练恢复
2. 训练停表核对
3. 与 `best.ckpt` 做 “最后一轮 vs 最佳一轮” 对账

## 对应代码里的真实协议痕迹

关键逻辑如下:

1. `../../../../src/engine/trainer.py` 每轮验证后都会无条件写 `last.ckpt`。
2. `../../../../src/engine/trainer.py` 保存 `epoch`、`model_state_dict`、`optimizer_state_dict`、`metric_value`。
3. 因此 `last.ckpt` 的语义是 latest training state，不是 best model。

当前 full run 已经跑到 `68` 并以 `early_stopping` 收尾，所以这份文件必须按 `epoch=68` 的现实解读。

## 如何手工验证这个文件的正确性

检查方法:

1. 读取 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/last.ckpt`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`

通过标准:

- `epoch=68`
- `metric_value=0.7340940301447756`
- `epoch_count=68`
- `stop_reason=early_stopping`
- `best_epoch=48`，且与 `last.ckpt` 不同轮

## 这个文件没说明什么

当前文件能证明的是:

1. full run 最后一轮状态已经真实落盘。
2. 当前主 run 可以从最后训练态继续恢复。
3. 当前停表位置与日志和 `run_meta.yaml` 一致。

当前文件不替代的是:

1. `best.ckpt` 的最佳模型语义
2. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
3. `run_summary.md` / `stage_summary.md` 的阶段收口解释

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `last.ckpt` 必须解释成 full run 第 68 轮状态。
2. 为什么它不能和 `best.ckpt` 混为一谈。
3. `epoch=68`、`metric_value=0.7340940301447756` 如何与日志和 `run_meta.yaml` 对账。
