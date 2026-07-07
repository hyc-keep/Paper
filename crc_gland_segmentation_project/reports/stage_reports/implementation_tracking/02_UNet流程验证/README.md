# 02_UNet流程验证 阅读入口

## 先看结论

- 当前 `02_UNet流程验证` 的主 run 已经是 full run，不再是旧的最小 smoke 目录。
- 当前主 run 对应 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/`，其真实状态是 `smoke_check=false`、`stop_reason=early_stopping`、`best_epoch=48`、`epoch_count=68`、`TestA60/TestB20` 已补齐、`stage_pass=true`。
- 当前规范 smoke run 仍然保留在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/`，它是单独的参照目录，不应再拿来解释主目录。
- 当前阅读入口状态是 `pass（当前锁定范围）`，表示主链说明文已经和正式 full run 现实对齐；这不等于 stage02 全量所有对象都已扩写完。
- 当前锁定范围共 `50` 个 A 类对象，已覆盖训练主链、5 份核心配置、主 run full run 资产、规范 smoke run 资产，以及测试/可视化正式资产链。

## 如果你只先读 3 份

请先读:

1. `00_交付范围内正式对象清单.md`
2. `implementation_status.md`
3. `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`

如果你要快速确认“主目录为什么不是 smoke 目录”，再接着读:

4. `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
5. `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
6. `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`

## 最推荐阅读顺序

建议按下面顺序读:

1. `00_交付范围内正式对象清单.md`
2. `implementation_status.md`
3. `scripts_train.py.md`
4. `configs_experiment_A1_UNet_GlaS_v1_seed3407.yaml.md`
5. `configs_data_glas.yaml.md`
6. `configs_model_unet_v1.yaml.md`
7. `configs_train_unet_flow_v1.yaml.md`
8. `configs_eval_eval_proto_v1.yaml.md`
9. `src_data___init__.py.md`
10. `src_models___init__.py.md`
11. `src_losses___init__.py.md`
12. `src_engine___init__.py.md`
13. `src_utils___init__.py.md`
14. `src_data_datasets.py.md`
15. `src_data_csv_loader.py.md`
16. `src_data_mask_ops.py.md`
17. `src_data_transforms.py.md`
18. `src_models_unet.py.md`
19. `src_losses_seg_losses.py.md`
20. `src_engine_lr_scheduler.py.md`
21. `src_engine_early_stop.py.md`
22. `src_engine_trainer.py.md`
23. `src_metrics_seg_metrics.py.md`
24. `src_eval_threshold.py.md`
25. `src_eval_run_eval.py.md`
26. `src_eval_checkpoint_selector.py.md`
27. `src_utils_seed.py.md`
28. `experiments_A1_UNet_GlaS_v1_seed3407_config.yaml.md`
29. `experiments_A1_UNet_GlaS_v1_seed3407_run_meta.yaml.md`
30. `experiments_A1_UNet_GlaS_v1_seed3407_train_log.csv.md`
31. `experiments_A1_UNet_GlaS_v1_seed3407_val_metrics.csv.md`
32. `experiments_A1_UNet_GlaS_v1_seed3407_best.ckpt.md`
33. `experiments_A1_UNet_GlaS_v1_seed3407_last.ckpt.md`
34. `experiments_A1_UNet_GlaS_v1_seed3407_train_curve.csv.md`
35. `experiments_A1_UNet_GlaS_v1_seed3407_val_curve.csv.md`
36. `experiments_A1_UNet_GlaS_v1_seed3407_run_summary.md`
37. `scripts_test.py.md`
38. `scripts_export_visuals.py.md`
39. `src_eval_export_visuals.py.md`
40. `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
41. `experiments_A1_UNet_GlaS_v1_seed3407_testB_metrics.csv.md`
42. `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
43. `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
44. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_config.yaml.md`
45. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
46. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_log.csv.md`
47. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
48. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_best.ckpt.md`
49. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_last.ckpt.md`
50. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_curve.csv.md`
51. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_curve.csv.md`
52. `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
53. `当前阶段为什么能pass以及下一步怎么看.md`

## 这一版和旧版最重要的区别

这次最关键的更新不是“又补了一批说明文”，而是把主 run 和 smoke run 的世界观重新对齐了。

当前必须明确区分:

1. 主 run `../../../../experiments/A1_UNet_GlaS_v1_seed3407/` 是 full run 正式资产。
2. smoke run `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/` 是单独保留的规范 smoke 目录。
3. 入口页、对象说明文、`run_meta.yaml`、`run_summary.md`、`unet_flow_stage_summary.md` 都必须跟这个区分一致。

## 当前这组文档覆盖什么

当前这组文档直接覆盖:

1. `3` 份脚本入口与结果脚本: `scripts/train.py`、`scripts/test.py`、`scripts/export_visuals.py`
2. `20` 份源码对象: data/model/loss/engine/utils 门面与训练、验证、指标、可视化主链源码
3. `5` 份核心配置: experiment/data/model/train/eval
4. `13` 份主 run full run 资产: config、run_meta、train_log、val_metrics、best、last、两份 curve、run_summary、testA、testB、metric_crosscheck、error_cases
5. `9` 份规范 smoke run 资产: config、run_meta、train_log、val_metrics、best、last、两份 curve、run_summary

合计 `50` 个 A 类对象。

## 当前最关键的真实结果

如果你只想抓住主 run 的物理事实，先记住下面这些字段:

- `smoke_check=false`
- `stop_reason=early_stopping`
- `best_epoch=48`
- `epoch_count=68`
- `testA_sample_count=60`
- `testB_sample_count=20`
- `metric_crosscheck_result=pass`
- `stage_pass=true`
- `protocol_error=false`
- `next_action=enter_03_unet_stability`

这些字段共同说明: 当前主目录已经是正式收口后的 full run，而不是最初那版 smoke 运行目录。

## 不要读偏

最容易读偏的地方有四个:

1. 不要把主目录再解释成“最小 smoke run”。
2. 不要把 smoke 目录当成主目录的当前现实。
3. 不要因为当前锁定范围说明文已 `pass`，就自动脑补 stage02 全量所有对象都已说明完。
4. 不要只看旧 guard 口径，忽略现在 `run_meta.yaml`、`run_summary.md` 和 `stage_summary` 已经写明的正式通过状态。

## 这一页的职责边界

这份 README 负责三件事:

1. 告诉读者先看什么
2. 告诉读者主 run 与 smoke run 应怎样区分
3. 告诉读者当前锁定范围已经覆盖到哪里

它不替代:

1. `实现依据记录.md`
2. 对象级说明文本体
3. `runtime_check_report.md`、`runtime_evidence.json`、`workflow_gate_report.md`

## 下一步怎么接

如果后续继续扩说明文范围，最短路径仍然是:

1. 先在 `00_交付范围内正式对象清单.md` 里重新裁定新增对象是否纳入 A 类。
2. 再在 `implementation_status.md` 里同步更新覆盖范围和诚实边界。
3. 最后补对象级说明文，保证入口页、对象页、正式产物三者继续一致。
