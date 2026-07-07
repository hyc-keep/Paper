# experiments_A1_UNet_GlaS_v1_seed3407_config.yaml.md

## 这份文件的定位

这份文档解释的是主 run 的配置快照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/config.yaml`。

当前它对应的是主 run full run 的现场配置留底。它回答的是“这次正式 A1 run 实际把哪 5 段冻结配置一起写进结果目录”，让读者可以直接从结果目录回查正式运行所使用的整套协议。

## 一眼先抓住什么

- 当前文件对应主 run `A1_UNet_GlaS_v1_seed3407` 的正式配置快照。
- 当前快照按 `experiment/data/model/train/eval` 五段组织。
- 当前它服务的是 full run 主目录，和 `run_meta.yaml`、`train_log.csv`、`val_metrics.csv` 属于同一条正式资产链。
- 当前文件里会保留 `smoke_check_run_name`、`smoke_epochs` 等协议字段，用来完整记录实验体系中的 smoke 对照位点。
- 当前文件可以证明“冻结配置已真实落盘”，但不能单独代替训练、测试和阶段收口结论。

## 这个文件是干什么的

这份 `config.yaml` 是主 run 的总配置快照。

它把以下信息压在一个结果目录文件里:

1. run 身份字段
2. 数据协议字段
3. 模型结构字段
4. 训练超参数字段
5. 评估口径字段

如果没有它，读者需要在 5 份源配置之间来回对照，才能确认这次正式 run 到底消费了哪套冻结字段。

## 当前真实结果

当前最关键的真实字段包括:

- `run_name=A1_UNet_GlaS_v1_seed3407`
- `train_seed=3407`
- `smoke_check_run_name=A1_UNet_GlaS_v1_seed3407_smoke`
- `dataset_root=datasets/01_GlaS_official_raw`
- `split_dir=splits/glas`
- `input_size=[512, 512]`
- `mask_positive_rule=mask_gt_0`
- `model_version=unet_v1`
- `optimizer=AdamW`
- `scheduler=ReduceLROnPlateau`
- `epoch_max=120`
- `early_stop_patience=20`
- `batch_size=2`
- `best_selector=val_objdice_max`
- `threshold_value=0.5`
- `threshold_source=val17`
- `connected_components_connectivity=8`

这说明主 run 的配置现实已经完整落盘，而且可以直接回查到训练、验证、测试和阶段汇总所依赖的冻结协议。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. `../../../../configs/data/glas.yaml`
3. `../../../../configs/model/unet_v1.yaml`
4. `../../../../configs/train/unet_flow_v1.yaml`
5. `../../../../configs/eval/eval_proto_v1.yaml`
6. `../../../../scripts/train.py`

下游消费:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/train_log.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

因此它是主 run 结果目录的配置入口，而不是独立的说明性附件。

## 对应代码里的真实协议痕迹

关键逻辑有三层:

1. `../../../../scripts/train.py` 解引用 experiment/data/model/train/eval 五段配置。
2. `../../../../scripts/train.py` 组装 `config_snapshot` 并写入结果目录。
3. 后续训练、验证、测试和阶段汇总资产都默认继承这份快照中的冻结字段。

所以当前文件不是手工复制品，而是训练入口真实写出的正式运行资产。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/config.yaml`
2. 确认它分成 `experiment/data/model/train/eval` 五段
3. 对照 5 份源配置
4. 再对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`

通过标准:

- `run_name` 对得上
- `train_seed` 对得上
- `model_version` 对得上
- `best_selector` 与 `threshold_source` 对得上
- 主 run 目录中的其它正式资产都能回接到这份快照

## 这个文件没说明什么

当前文件能证明的是:

1. 主 run 的冻结配置已经真实落盘。
2. 这次正式 run 消费的配置字段可以从单一文件回查。
3. 主 run full run 的结果目录不是只剩零散日志。

当前文件不单独替代的是:

1. `train_log.csv` / `val_metrics.csv` 的逐轮记录
2. `best.ckpt` / `last.ckpt` 的模型状态
3. `testA_metrics.csv` / `testB_metrics.csv` 的正式测试结果
4. `run_summary.md` / `stage_summary.md` 的阶段收口结论

## 建议联读

- `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
- `configs_train_unet_flow_v1.yaml.md`
- `configs_eval_eval_proto_v1.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 主 run 的 `config.yaml` 到底冻结了哪五段配置。
2. 为什么它属于 full run 主目录的正式配置留底。
3. 为什么它能证明协议冻结已落盘，但不能单独替代阶段验收结论。
