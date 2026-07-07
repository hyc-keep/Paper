# experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md

## 这份文件的定位

这份文档解释的是主 run 的正式摘要页 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`。

它是当前 full run 的人工阅读入口。读者应通过它快速看到这次正式 A1 run 是否已经完成训练、测试、可视化和阶段收口。

## 一眼先抓住什么

- 当前 run 是 `smoke_check=false` 的正式 full run。
- 当前训练以 `early_stopping` 正常结束。
- 当前最优验证结果来自 `best_epoch=48`，`best_metric_value=0.7626771700880477`。
- 当前测试已经覆盖 `TestA60/TestB20`。
- 当前门禁结果已经是 `stage_pass=true`、`protocol_error=false`、`next_action=enter_03_unet_stability`。
- 当前 `truthful_interpretation` 应当和正式现实一致，明确表达 formal closure 已经成立。

## 这个文件是干什么的

这份 `run_summary.md` 是主 run 的最短人工结论页。

它把以下内容压缩给人工审阅者:

1. 训练如何结束
2. 最优轮次是谁
3. 当前 split-wise 测试是否已经补齐
4. crosscheck 是否通过
5. 视觉错误模式有哪些
6. 当前阶段是否已经可以从 `02` 转入 `03`

如果没有这份文件，读者只能在 `run_meta.yaml`、`testA_metrics.csv`、`testB_metrics.csv`、`metric_crosscheck_note.md` 和阶段汇总里来回拼接结论。

## 当前真实结果

当前主 run 摘要页应该表达的真实结论是:

- `stop_reason=early_stopping`
- `best_epoch=48`
- `best_metric_name=val_objdice`
- `best_metric_value=0.7626771700880477`
- `smoke_check=false`
- `amp_active=false`
- `pass_train=true`
- `pass_val=true`
- `pass_test=true`
- `pass_eval=true`
- `pass_visual=true`
- `pass_record=true`
- `stage_pass=true`
- `protocol_error=false`
- `freeze_status=true`
- `handoff_ready_for_a2=true`
- `next_action=enter_03_unet_stability`
- `testA_expected_count=60`
- `testA_actual_count=60`
- `testA_objdice=0.6941893856375373`
- `testB_expected_count=20`
- `testB_actual_count=20`
- `testB_objdice=0.7619798771629787`
- `metric_crosscheck_result=pass`

因此，这份摘要页现在已经是正式验收结论页。

## 它和上下游怎么衔接

上游依赖:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/val_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
6. `../../../../reports/stage_reports/unet_flow_stage_summary.md`

下游用途:

1. 人工复审快速阅读
2. 阶段交接快速结论页
3. 与 `run_meta.yaml` / `stage_summary` 做一致性核对

## 对应代码里的真实协议痕迹

当前摘要页的真实生成逻辑已经从单纯 trainer 输出升级成两段式:

1. `../../../../src/engine/trainer.py` 先写训练结论字段。
2. `../../../../scripts/summarize_stage.py` 再把阶段门禁、split 计数、formal closure 解释写回这份摘要页。

因此，当前摘要页的最终语义应以“正式 full run + 正式阶段汇总回填”理解。

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 对照 `../../../../reports/stage_reports/unet_flow_stage_summary.md`

通过标准:

- `stage_pass=true`
- `protocol_error=false`
- `next_action=enter_03_unet_stability`
- `testA_actual_count=60`
- `testB_actual_count=20`
- `truthful_interpretation` 明确写出 formal A1 acceptance 已经成立

## 这个文件没说明什么

当前文件能证明的是:

1. 当前主 run full run 已经达到正式摘要级收口。
2. 训练、测试、crosscheck 和阶段门禁可以被一页快速概括。
3. 当前主目录的训练、测试和阶段结论已经可以被一页稳定概括。

当前文件不替代的是:

1. `train_log.csv` / `val_metrics.csv` 的逐轮详情
2. `testA_metrics.csv` / `testB_metrics.csv` 的逐样本详情
3. `best.ckpt` / `last.ckpt` 的 checkpoint 实体
4. `visuals/*` 和 `error_cases.md` 的观察面

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`

## 学完后你应该具备什么能力

学完后，至少应能回答:

1. 为什么当前 `run_summary.md` 必须和 `run_meta.yaml`、`stage_pass=true` 保持完全同步。
2. 为什么它现在是正式 full run 摘要页。
3. 为什么 `truthful_interpretation` 必须直接表达当前正式验收已经成立。
