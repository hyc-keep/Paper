# 01_数据协议 阅读入口

## 先看结论

- 当前 `01_数据协议` 这个阶段的状态: `pass`
- 这里的 `pass` 指的是: GlaS 和 CRAG 的正式数据资产、split、检查、预览、交接和 preflight 入口已经形成可交接闭环
- 这里的 `pass` 不指: `完整 UNet 训练链已经存在`
- 不要误会: `scripts/train.py` 现在只是 `01_数据协议` 需要的最小 formal preflight 入口,不是 `02_UNet流程验证` 的完整训练实现
- 当前说明文覆盖状态: `pass`
- 当前计数口径: A 类正式对象共 `24` 个,其中已完成逐文件说明文 `24` 份,当前没有 `pending`; 阶段级文档共 `3` 份且已齐备
- 当前已经补到的逐文件说明对象:
  - `scripts/train.py`
  - `src/data/csv_loader.py`
  - `src/data/datasets.py`
  - `src/data/mask_ops.py`
  - `src/data/boundary_targets.py`
  - `src/data/distance_targets.py`
  - `configs/data/glas.yaml`
  - `configs/data/crag.yaml`
  - `splits/glas/glas_train68.csv`
  - `splits/crag/crag_train153.csv`
  - `splits/glas/glas_val17.csv`
  - `splits/glas/glas_testA60.csv`
  - `splits/glas/glas_testB20.csv`
  - `splits/crag/crag_val20.csv`
  - `splits/crag/crag_test40.csv`
  - `tools/stage01_data_protocol/prepare_glas_split.py`
  - `tools/stage01_data_protocol/prepare_crag_split.py`
  - `tools/stage01_data_protocol/convert_masks.py`
  - `tools/stage01_data_protocol/build_boundary_targets.py`
  - `tools/stage01_data_protocol/build_distance_targets.py`
  - `tools/stage01_data_protocol/check_dataset_pairs.py`
  - `tools/stage01_data_protocol/preview_dataset_samples.py`
  - `tools/stage01_data_protocol/validate_data_assets.py`
  - `reports/stage_reports/data_stage_acceptance.md`

## 最推荐阅读顺序

请直接按下面顺序读:

1. `reports/stage_reports/implementation_tracking/01_数据协议/00_交付范围内正式对象清单.md`
2. `reports/stage_reports/implementation_tracking/01_数据协议/implementation_status.md`
3. `reports/stage_reports/implementation_tracking/01_数据协议/src_data_csv_loader.py.md`
4. `reports/stage_reports/implementation_tracking/01_数据协议/src_data_datasets.py.md`
5. `reports/stage_reports/implementation_tracking/01_数据协议/splits_glas_glas_train68.csv.md`
6. `reports/stage_reports/implementation_tracking/01_数据协议/splits_crag_crag_train153.csv.md`
7. `reports/stage_reports/implementation_tracking/01_数据协议/splits_glas_glas_val17.csv.md`
8. `reports/stage_reports/implementation_tracking/01_数据协议/splits_glas_glas_testA60.csv.md`
9. `reports/stage_reports/implementation_tracking/01_数据协议/splits_glas_glas_testB20.csv.md`
10. `reports/stage_reports/implementation_tracking/01_数据协议/splits_crag_crag_val20.csv.md`
11. `reports/stage_reports/implementation_tracking/01_数据协议/splits_crag_crag_test40.csv.md`
12. `reports/stage_reports/implementation_tracking/01_数据协议/src_data_mask_ops.py.md`
13. `reports/stage_reports/implementation_tracking/01_数据协议/src_data_boundary_targets.py.md`
14. `reports/stage_reports/implementation_tracking/01_数据协议/src_data_distance_targets.py.md`
15. `reports/stage_reports/implementation_tracking/01_数据协议/configs_data_glas.yaml.md`
16. `reports/stage_reports/implementation_tracking/01_数据协议/configs_data_crag.yaml.md`
17. `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_glas_split.py.md`
18. `reports/stage_reports/implementation_tracking/01_数据协议/tools_prepare_crag_split.py.md`
19. `reports/stage_reports/implementation_tracking/01_数据协议/tools_validate_data_assets.py.md`
20. `reports/stage_reports/implementation_tracking/01_数据协议/reports_stage_reports_data_stage_acceptance.md.md`
21. `reports/stage_reports/implementation_tracking/01_数据协议/tools_convert_masks.py.md`
22. `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_boundary_targets.py.md`
23. `reports/stage_reports/implementation_tracking/01_数据协议/tools_build_distance_targets.py.md`
24. `reports/stage_reports/implementation_tracking/01_数据协议/tools_check_dataset_pairs.py.md`
25. `reports/stage_reports/implementation_tracking/01_数据协议/tools_preview_dataset_samples.py.md`
26. `reports/stage_reports/implementation_tracking/01_数据协议/scripts_train.py.md`
27. `scripts/README.md`
28. `reports/stage_reports/data_stage_acceptance.md`
29. `b_class_auxiliary/runtime_checks/runtime_check_report.md`
30. `reports/stage_reports/implementation_tracking/01_数据协议/当前阶段为什么能pass以及下一步怎么看.md`

如果你只想最快理解这一阶段，请直接从 `01` 往下读。

## 这一版和旧版最重要的区别

这一版最重要的区别，不再是只围着 `scripts/train.py` 打转，而是开始把它上游真正依赖的正式对象补出来。

以前最容易混淆的地方是：目录里一旦出现 `scripts/train.py`，人就会下意识以为训练链已经恢复。
现在这组文档把边界继续往前推了一步: 你必须先看清 `configs/data/*.yaml`、`splits/*/*.csv`、`src/data/*.py` 和正式 split 资产怎么接,再去理解 preflight 入口。

换句话说，这一版真正补上的不是“训练能力”，而是“正式数据消费链的可解释性”。

## 这一组文档在整个阶段中的位置

这组文档的作用，不是替代 `b_class_auxiliary/runtime_checks/实现依据记录.md`，也不是替代 `b_class_auxiliary/coding_guards/**`。

它的职责更具体:

1. 把 `01_数据协议` 当前已经形成的正式交付对象讲清楚
2. 把“配置 -> split -> sample -> mask/target 派生 -> preflight”这一条唯一消费链讲清楚
3. 把当前已经解释到哪里、还没解释到哪里讲清楚

这里直接回链三份最关键的上游依据:

- `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/05_代码工程映射与实现策略.md`

### 理论依据 / 代码参考来源 / 冻结回链

- 理论依据: `../../../../../结直肠腺体分割_plan_优化版/03_文献证据/05_腺体任务经典论文/01_GlaS-Challenge.md`
- 代码参考来源: 当前阶段入口最终通过 `src/data/datasets.py` 消费 `configs/data/*.yaml` 与 `splits/*/*.csv`
- 冻结回链: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

## 你现在最该先搞明白的四件事

1. `01_数据协议` 当前到底有哪些对象已经纳入正式说明映射:
   先看 `00_交付范围内正式对象清单.md`，再看 `reports/stage_reports/data_stage_acceptance.md`，里面会直接写清 done / pending，以及 `data_stage_pass=True`、`handoff_ready=True`、`preflight_pass=True` 这些正式字段。
2. 正式 split CSV 到样本列表这一步是谁在负责:
   看 `src_data_csv_loader.py.md`、`src_data_datasets.py.md`、`splits_glas_glas_train68.csv.md`、`splits_crag_crag_train153.csv.md`、`src_data_mask_ops.py.md`、`src_data_boundary_targets.py.md` 和 `src_data_distance_targets.py.md`。
3. 当前阶段到底依赖哪些正式输入配置:
   重点看 `configs_data_glas.yaml.md` 和 `configs_data_crag.yaml.md`。
4. 后面进入 `02_UNet流程验证` 前还差什么:
   看 `当前阶段为什么能pass以及下一步怎么看.md`。

## 当前这一组文档覆盖什么

这组文档只覆盖最终会随项目一起交付、并且当前已经进入正式链的对象。

所以它现在优先解释:

- `00_交付范围内正式对象清单.md`
- `src/data/csv_loader.py`
- `src/data/datasets.py`
- `splits/glas/glas_train68.csv`
- `splits/crag/crag_train153.csv`
- `splits/glas/glas_val17.csv`
- `splits/glas/glas_testA60.csv`
- `splits/glas/glas_testB20.csv`
- `splits/crag/crag_val20.csv`
- `splits/crag/crag_test40.csv`
- `src/data/mask_ops.py`
- `src/data/boundary_targets.py`
- `src/data/distance_targets.py`
- `configs/data/glas.yaml`
- `configs/data/crag.yaml`
- `tools/stage01_data_protocol/prepare_glas_split.py`
- `tools/stage01_data_protocol/prepare_crag_split.py`
- `tools/stage01_data_protocol/convert_masks.py`
- `tools/stage01_data_protocol/build_boundary_targets.py`
- `tools/stage01_data_protocol/build_distance_targets.py`
- `tools/stage01_data_protocol/check_dataset_pairs.py`
- `tools/stage01_data_protocol/preview_dataset_samples.py`
- `tools/stage01_data_protocol/validate_data_assets.py`
- `scripts/train.py`
- `scripts/README.md`
- `reports/stage_reports/data_stage_acceptance.md`

它不会把下面这些内部流程留痕冒充成对外交付说明文:

- `b_class_auxiliary/coding_guards/**`
- `b_class_auxiliary/runtime_checks/post_qc_guard.md`
- `b_class_auxiliary/runtime_checks/diagnostics_result.txt`
- 只服务 runtime gate / code-quality gate 的内部脚本说明

还没有补完的对象会在对象清单里继续保持 `pending`,而不是假装已经覆盖。

## 当前最真实的边界

用人话说，这一阶段现在已经能回答三件事:

- 这套项目到底认哪一版数据资产、哪几份 split、哪几份检查和交接文件
- 正式配置和 split CSV 是怎么被装成 sample 的
- 后续训练入口有没有老老实实消费这套正式资产

但它还不能回答另外两件事:

- UNet 前向输出长什么样
- loss、backward、optimizer.step 有没有真实跑通

这两件事还没有，不是所有“看起来像训练”的文件都已经完成；这一点和当前阶段 `pass` 不冲突。
同时，当前说明文覆盖已经推进到 `pass`。
按当前统一口径看，A 类正式对象 24 个都已经有逐文件说明文；这和阶段级入口文档已经齐备是一致的。

## 下一步怎么接

后面进入 `02_UNet流程验证` 时，不是重新解释数据阶段，而是继承这里已经冻结的输入层。

下一步最短路径是:

1. 继续保留 `configs/data -> splits/*.csv -> dataset_root + relpath` 这一条唯一消费链
2. 在 `02_UNet流程验证` 中补模型、loss 和 trainer 相关实现
3. 用新的 runtime 证据证明完整训练链成立

建议联读:

- `src_data_datasets.py.md`
- `splits_glas_glas_train68.csv.md`
- `splits_crag_crag_train153.csv.md`
- `splits_glas_glas_val17.csv.md`
- `splits_glas_glas_testA60.csv.md`
- `splits_glas_glas_testB20.csv.md`
- `splits_crag_crag_val20.csv.md`
- `splits_crag_crag_test40.csv.md`
- `src_data_mask_ops.py.md`
- `src_data_boundary_targets.py.md`
- `src_data_distance_targets.py.md`
- `configs_data_glas.yaml.md`
- `scripts_train.py.md`

## 如何快速验证你没有读偏

检查方法:

1. 先看 `00_交付范围内正式对象清单.md`
2. 再看 `reports/stage_reports/data_stage_acceptance.md` 里的 `data_stage_pass` 和 `preflight_pass`
3. 最后看 `b_class_auxiliary/runtime_checks/runtime_check_report.md` 里的 `runtime_profile`

通过标准:

- 你能明确说出当前通过的是 `01_数据协议` 的 preflight
- 你不会把当前入口误读成完整训练器
- 你也能明确说出当前说明文覆盖已经全部完成
