# scripts_test.py.md

## 结构化溯源卡片

- 正式对象: `../../../../scripts/test.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: `validation split freezes protocol, test splits report final metrics`
- 公式/定义: 由 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt` 配合 `../../../../configs/eval/eval_proto_v1.yaml`，导出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../scripts/test.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `best_selector=val_objdice_max`, `threshold_value=0.5`, `threshold_source=val17`, `boundary_metric_width=3`
- 上游实验配置: `../../../../configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`

### 当前实现落点

- 文件: `../../../../scripts/test.py`
- 符号: `parse_args()` / `_resolve_run_dir()` / `_load_checkpoint()` / `_write_metrics_csv()` / `_write_metric_crosscheck_note()` / `_update_run_meta()` / `main()`

## 这个脚本的作用

这份说明文回答的是:

当前 stage02 里，到底是谁把已经训练好的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt` 变成正式的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 这一组评估资产。

答案就是 `../../../../scripts/test.py`。

你可以把它理解成“评估侧总调度入口”。

`../../../../src/eval/run_eval.py` 负责算 split，`../../../../src/eval/export_visuals.py` 负责导图和错例总结，但真正把 checkpoint、dataloader、metrics csv、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 串成一条正式资产链的人，是这里。

用人话说，这不是“顺手写个 test 命令”。
它是在回答一个更硬的问题:
训练结束以后，项目到底按哪一个入口、哪一个阈值、哪一个顺序，把结果正式落盘。

如果没有这份脚本，当前目录里就算零散存在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/`，你也很难证明这些资产是不是走的同一条正式协议。

## 这个脚本在整个阶段中的位置

先记住一句话:

`../../../../scripts/test.py` 不负责重新训练模型，它只负责消费已经冻结好的训练资产，然后把测试资产稳定导出来。

它在链路里的位置可以先画成这样:

```text
experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt
        + configs/eval/eval_proto_v1.yaml
        + ../../../../src/eval/run_eval.py
        + src/eval/export_visuals.py
                    ↓
            ../../../../scripts/test.py
                    ↓
testA_metrics.csv / testB_metrics.csv
experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md
predictions/testA/* / predictions/testB/*
visuals/testA/* / visuals/testB/*
summaries/error_cases.md
summaries/run_summary.md
experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml
```

上游依赖最关键的有 6 个:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/checkpoints/best.ckpt`
2. `../../../../configs/eval/eval_proto_v1.yaml`
3. `../../../../configs/data/glas.yaml`
4. `../../../../src/eval/run_eval.py`
5. `../../../../src/eval/export_visuals.py`
6. `../../../../src/models/unet.py`

下游消费者也很明确:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`
6. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`

这里最容易误解的一点是:
它虽然叫 `../../../../scripts/test.py`，但不是“随便测一测”。
当前它其实在实现 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md` 里规定的正式测试顺序。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段默认配置: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/01_任务与默认配置.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验证测试文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链最重要的意义有 3 条:

1. 当前测试集不能反向参与挑 checkpoint
2. 当前阈值只能来自 `val17`
3. 当前 `TestA` 和 `TestB` 必须分开导出，不能混成一个总分

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式测试入口与结果资产调度器
- 当前真实边界: `已完成本地 CPU 级最小联通检查，不把当前结果扩写成 GPU 全量正式实验`
- 当前最硬证据:
  - `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 已落盘 `sample + aggregate` 双层结果
  - `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 已落盘 `sample + aggregate` 双层结果
  - `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 写明 `metric_crosscheck_result=pass`
  - `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 写明 `testA_objdice=0.08680183161763688`
  - `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 写明 `testB_objdice=0.25959866009914456`

你现在可能会问:

“既然 `../../../../src/eval/run_eval.py` 已经能算 split 指标，为什么还需要单独的 `../../../../scripts/test.py`？”

因为两者职责不一样。

`../../../../src/eval/run_eval.py` 更像能力层，负责给一个 split 算结果。
`../../../../scripts/test.py` 更像正式工作流层，负责把多个 split 的执行顺序、结果目录、交叉核对和总结回填统一起来。

## 脚本核心逻辑

### 主要流程

这个脚本的主链可以拆成 8 步:

1. 读取 `--config` 指向的 experiment config
2. 解析 run 目录和 checkpoint 路径
3. 构建 data config、eval transform、dataset、dataloader
4. 加载 `best.ckpt` 到正式 UNet
5. 通过 `evaluate_split()` 先跑 `testA` 再跑 `testB`
6. 把 sample rows 和 aggregate metrics 写成两份 CSV
7. 重新聚合生成 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md`
8. 回填 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`，并按需要导出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`

### 关键函数 1：`_resolve_run_dir()` 与 `_resolve_checkpoint_path()`

这两个函数解决的是同一个问题:
当前到底评估哪个 run，读哪个 checkpoint。

为什么这一步重要？

因为 stage02 明确禁止“看完测试集再换 checkpoint”。
如果这里没有把 run 目录和 checkpoint 路径固定好，后面的 split 结果就可能不是同一条协议产物。

换句话说，它在保护“唯一 best.ckpt 来源”。

### 关键函数 2：`_write_metrics_csv()`

这个函数不只是把数字写出去。
它还在固定正式表结构。

当前固定列至少包括:

1. `row_type`
2. `sample_id`
3. `split_role`
4. `image_path`
5. `mask_path`
6. `pred_path`
7. `objdice`
8. `dice`
9. `iou`
10. `f1`
11. `boundary_f1`
12. `hd95`
13. `object_hausdorff`

说白了，这样做是为了同时保住两层能力:

1. 人能看单样本结果
2. 脚本能读 aggregate 行做下游核对

为什么不用只留 aggregate 一行？

因为那样后面的 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 就会失去样本级回指能力。

### 关键函数 3：`_write_metric_crosscheck_note()`

这个函数特别关键。

它在做的不是“再复制一遍指标”，而是在检查 sample 行均值和 aggregate 行是否真的一致。

当前真实结果里:

- `testA` 的 `objdice` sample_mean 和 aggregate 都是 `0.08680183161763688`
- `testB` 的 `objdice` sample_mean 和 aggregate 都是 `0.25959866009914456`

这一步为什么重要？

因为首轮阶段最怕的不是分数低，而是 CSV 聚合逻辑写错了却没人发现。

### 关键函数 4：`_update_run_meta()`

这个函数负责把测试阶段结论回填到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`。

当前回填的关键字段包括:

- `metric_list`
- `metric_crosscheck_result`
- `metric_crosscheck_note_path`
- `visual_version`
- `testA_sample_count`
- `testB_sample_count`
- `testA_objdice`
- `testB_objdice`
- `num_visual_samples_testA`
- `num_visual_samples_testB`

你可以先把它想成“把分散结果压回索引卡”的动作。

如果不用这一步，结果目录里虽然会多出文件，但 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 看不出这轮测试到底导出了什么。

## 如何运行这个脚本

当前最常见的运行方式是:

```bash
python scripts/test.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --device cpu
```

本地 CPU 联通检查可以额外限制样本数:

```bash
python scripts/test.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --device cpu --max-samples-per-split 2 --max-visual-samples 2
```

如果只想跳过可视化导出，可以显式加:

```bash
python scripts/test.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --device cpu --skip-visuals
```

这里有两个协议边界要记住:

1. `--max-samples-per-split` 只服务本地联通检查
2. 正式测试不应该靠这个参数裁剪 split

## 如何验证脚本运行结果

最短验证路径可以按 5 步走:

1. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 是否同时存在
2. 检查两份 CSV 是否同时包含 `sample` 行和 `aggregate` 行
3. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 是否写明 `metric_crosscheck_result=pass`
4. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 是否回填 `testA_objdice`、`testB_objdice`
5. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 是否回填 `major_failure_modes`

通过标准也很明确:

- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 中 aggregate `objdice` 为 `0.08680183161763688`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 中 aggregate `objdice` 为 `0.25959866009914456`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 返回 `pass`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 与 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 的 split 级字段互相一致

## 容易误解的地方

- 不要把 `scripts/test.py` 误读成模型开发入口，它不改结构也不训练权重
- 不要把 `--max-samples-per-split` 当成正式实验参数，它只是本地 CPU 联通检查开关
- 不要因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 已更新，就误以为可以跳过 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`

## 为什么不用别的设计

当前没有把可视化导出和错误总结完全塞进 `../../../../src/eval/run_eval.py`，也没有把 crosscheck 留给手工做。

原因很直接:

1. `../../../../src/eval/run_eval.py` 更适合保持“给一个 split 算结果”的纯能力层
2. crosscheck 如果靠人工，很难稳定回填到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`
3. 可视化导出需要支持重跑，所以单独保留 `scripts/export_visuals.py` 更稳

## 5 分钟自检任务

如果你真的看懂了这个脚本，5 分钟内应该能回答下面 4 个问题:

1. 为什么 `threshold_source` 必须还是 `val17`
2. 为什么 `TestA` 和 `TestB` 不能只导一个总表
3. 为什么 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/metric_crosscheck_note.md` 不能省
4. 为什么 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md` 也要被回填

## 建议联读

- `src_eval_run_eval.py.md`
- `src_eval_export_visuals.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_testA_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_metric_crosscheck_note.md`
