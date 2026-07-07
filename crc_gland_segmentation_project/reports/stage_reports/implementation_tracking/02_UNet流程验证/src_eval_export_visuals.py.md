# src_eval_export_visuals.py.md

## 结构化溯源卡片

- 正式对象: `../../../../src/eval/export_visuals.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `MILD-Net: gland instance segmentation with explicit error modes`
- 章节: `qualitative inspection should accompany object-level metrics`
- 公式/定义: `raw + gt + pred -> overlay` and `sample rows -> failure taxonomy summary`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/eval/export_visuals.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `visual_version=visual_proto_v1`, `boundary_metric_width=3`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`

### 当前实现落点

- 文件: `../../../../src/eval/export_visuals.py`
- 符号: `build_overlay_panel()` / `classify_failure_type()` / `export_prediction_visuals()` / `write_error_cases_summary()` / `export_run_visual_assets()`

## 这个脚本的作用

这份说明文回答的是:

当前 stage02 里，到底是谁把 split 级 CSV 和 prediction png 变成 raw、gt、pred、overlay 四件套，以及 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 里的失败类型总结。

答案就是 `../../../../src/eval/export_visuals.py`。

你可以把它理解成“结果表现层引擎”。

`../../../../scripts/export_visuals.py` 只是入口壳。
真正决定 overlay 怎么画、worst cases 怎么选、失败类型怎么归类的人，是这里。

用人话说，这个模块负责的是“让人看懂结果”，不是“让人得到一个数字”。

如果没有这份模块，当前 run 虽然还能导出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`，但很难稳定落下人类可读的视觉证据包。

## 这个脚本在整个阶段中的位置

它在链路里的位置可以先记成下面这样:

```text
experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv / experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv
        + predictions/testA/* / predictions/testB/*
        + raw image / gt mask
                    ↓
          src/eval/export_visuals.py
                    ↓
visuals/testA/* / visuals/testB/*
experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md
```

最关键的上游依赖有 6 个:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/testA/*`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/predictions/testB/*`
5. sample rows 里 `image_path` 回指的原图文件
6. sample rows 里 `mask_path` 回指的 GT mask 文件

下游消费者同样明确:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/*`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/*`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

这里要记住一个边界:
它负责视觉和错例归纳，不负责反向修改 metrics csv 的数值。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段验证测试文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 当前阶段错误排查: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/04_错误排查.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链在证明:

1. 视觉证据包属于正式结果资产，不是装饰图
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 不是随手点评，而是阶段排查输入
3. 当前失败类型是工程观察面，不包装成最终论文 taxonomy

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式可视化导出与错误归类模块
- 当前真实边界: `错误类型采用启发式规则，只服务首轮流程排雷`
- 当前最硬证据:
  - `build_overlay_panel()` 真实生成 GT 绿色、Pred 红色、重叠黄色的 overlay
  - `classify_failure_type()` 真实返回 `all_background`、`adhesion_merge`、`boundary_over_smooth`、`small_gland_miss`、`fragmented_complex_region`
  - `write_error_cases_summary()` 真实写出 `failure_taxonomy_version=failure_taxonomy_v1`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 已真实记录 `adhesion_merge` 和 `boundary_over_smooth`

你现在可能会问:

“失败类型不是应该靠更复杂的方法学吗，为什么这里先用启发式？”

因为当前阶段是 `A1` 首轮流程验证。
它的任务是先把结果观察面建立起来，而不是提前把 taxonomy 包装成最终研究结论。

## 脚本核心逻辑

### 主要流程

这个模块的主链可以拆成 6 步:

1. 从 split 级 metrics csv 读出 sample rows
2. 根据 `image_path`、`mask_path`、`pred_path` 取回原图、GT 和预测
3. 必要时把原图和 GT resize 到 prediction 的形状
4. 生成人能复查的 raw、gt、pred、overlay 四件套
5. 根据样本指标和连通域关系归类失败类型
6. 写回 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 和 split 级 visual 目录

### 关键函数 1：`build_overlay_panel()`

这个函数解决的是“让肉眼一眼看出哪里对、哪里错”。

当前配色规则是:

1. GT 绿色
2. Pred 红色
3. 重叠区域黄色

为什么不用更复杂的 plotting 系统？

因为当前最重要的是稳定和可重导，而不是论文排版。

换句话说，这里优先的是“永远能导出来”，不是“看起来最花哨”。

### 关键函数 2：`classify_failure_type()`

这个函数是当前模块里最值得盯的一段。

它并不是瞎猜错误类型，而是基于几类可解释信号:

1. `pred_area == 0 && target_area > 0` 时判成 `all_background`
2. 一个预测连通域覆盖多个目标连通域时判成 `adhesion_merge`
3. 小目标完全没被覆盖时判成 `small_gland_miss`
4. `boundary_f1` 很低但 `dice` 没低到完全崩时判成 `boundary_over_smooth`
5. 其余复杂情况回到 `fragmented_complex_region`

说白了，这是一套“可解释但保守”的工程规则。

### 关键函数 3：`export_prediction_visuals()`

这个函数负责从 sample rows 里选最差样本并导出四件套。

当前排序依据是 `objdice` 从低到高。

为什么不用随机抽样？

因为当前阶段最需要看的不是平均样本，而是最差案例。

### 关键函数 4：`write_error_cases_summary()`

这个函数把 split 级计数和 worst cases 两层信息压成 Markdown。

当前真实 summary 至少保留:

1. `failure_taxonomy_version`
2. 每个 split 的 failure 计数
3. worst cases 的 `sample_id`
4. worst cases 的 `objdice`、`dice`、`boundary_f1`
5. overlay 回指路径

这样做的意义很直接:
后面 `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/04_错误排查.md` 和人工审阅，不需要再回去手工翻原图。

## 如何运行这个脚本

这个模块通常不直接单独运行，而是被下面两个入口调用:

1. `../../../../scripts/test.py`
2. `../../../../scripts/export_visuals.py`

如果你想理解真实调用方式，最短命令链是:

```bash
python scripts/test.py --config configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml --device cpu --max-samples-per-split 2 --max-visual-samples 2
```

或:

```bash
python scripts/export_visuals.py --run-dir experiments/A1_UNet_GlaS_v1_seed3407 --max-samples-per-split 2
```

这里的协议边界要记住:

1. visual 导出依赖已有 prediction png
2. sample rows 里回指的原图和 GT 路径必须仍然可读
3. 这个模块不重新跑模型
4. 这个模块不负责生成 metrics csv

## 如何验证脚本运行结果

最短验证路径可以按 5 步走:

1. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/` 是否同时存在 raw、gt、pred、overlay 文件
2. 检查 overlay 文件名是否能回指 `sample_id`
3. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 是否列出 `failure_taxonomy_version=failure_taxonomy_v1`
4. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 的 worst-case 行是否包含 overlay 路径
5. 检查最差样本是否真的来自较低 `objdice` 的 sample rows

通过标准可以先看当前真实结果:

- `testA` 当前最差两个样本都是 `adhesion_merge`
- `testB` 当前已出现 `boundary_over_smooth`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 已真实回指 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 已真实回指 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_1_overlay.png`

## 容易误解的地方

- 不要把 `boundary_over_smooth` 误读成模型最终结论，它只是首轮观察标签
- 不要把 overlay 颜色方案当成研究结论，它只是稳定的工程展示层
- 不要因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 很短，就误会它没价值；错例回指本身就是正式交接输入

## 为什么不用别的设计

当前没有直接依赖大型可视化框架，也没有把 failure taxonomy 设计成难复现的复杂规则。

原因有 3 个:

1. 首轮阶段优先要可重导
2. 规则必须能从源码读懂，而不是黑箱判断
3. 视觉层和数值层必须能共用同一份 sample rows

## 5 分钟自检任务

如果你已经吃透这个模块，应该能回答:

1. 为什么 overlay 层不应该去改 metrics
2. 为什么 worst-case 排序先看 `objdice`
3. 为什么 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 必须保留 overlay 回指
4. 为什么当前 failure taxonomy 只能诚实叫工程观察面

## 建议联读

- `scripts_export_visuals.py.md`
- `scripts_test.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
