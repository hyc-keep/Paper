# scripts_export_visuals.py.md

## 结构化溯源卡片

- 正式对象: `../../../../scripts/export_visuals.py`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `Metrics Reloaded: recommendations for image analysis validation`
- 章节: `numeric metrics should be complemented by case-level visual evidence`
- 公式/定义: `run_dir + metrics csv + prediction masks -> visuals bundles + error summary`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../scripts/export_visuals.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 冻结文件: `../../../../configs/eval/eval_proto_v1.yaml`
- 对应字段: `visual_version=visual_proto_v1`, `boundary_metric_width=3`
- 冻结表: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 上游资产: `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv`, `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`
- 总冻结规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`

### 当前实现落点

- 文件: `../../../../scripts/export_visuals.py`
- 符号: `parse_args()` / `main()`

## 这个脚本的作用

这份说明文回答的是:

当前 stage02 里，如果数字结果已经落盘，但想重导 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 这一类 visual 目录和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`，应该走哪一个正式入口。

答案就是 `../../../../scripts/export_visuals.py`。

你可以把它理解成“可视化重导开关”。

`../../../../scripts/test.py` 是完整测试入口，而这个脚本是窄入口。
它不重新跑模型，不重新算 CSV，而是直接消费已有结果资产。

用人话说，它是在解决一个很实际的问题:
如果你只是想重做四件套导图和错例总结，不应该为了这件事重新走整条测试链。

## 这个脚本在整个阶段中的位置

先把它记成这样:

```text
testA_metrics.csv / testB_metrics.csv
predictions/testA/* / predictions/testB/*
            ↓
scripts/export_visuals.py
            ↓
visuals/testA/* / visuals/testB/*
experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md
```

它的上游依赖有 4 层:

1. 已存在的 run 目录
2. split 级 metrics csv
3. 已导出的 prediction png
4. metrics csv 里仍然能回指到真实可读的 `image_path` 和 `mask_path`

它的下游消费者也很明确:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/*`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/*`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`

这里最关键的设计边界只有一句话:
它服务的是“重导”，不是“重评估”。

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段验证测试文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 当前阶段错误排查: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/04_错误排查.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 上一阶段放行文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

这一组回链在强调 3 件事:

1. 可视化证据包不是可有可无
2. 错例总结必须能回指到真实样本
3. 这里的重导不能篡改 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv` 的正式数值口径

## 当前实现状态

- 当前状态: `已实现`
- 当前定位: `stage02` 的正式可视化重导入口
- 当前真实边界: `只重建 visual assets，不重新计算 metrics csv`
- 当前最硬证据:
  - `main()` 只接收 `run_dir` 和 `max_samples_per_split`
  - 输出真实回写 `experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`
  - 输出真实打印 `testA_visual_count=2`
  - 输出真实打印 `testB_visual_count=2`

你现在可能会问:

“既然 `scripts/test.py` 已经能导图了，为什么还要单独保留这个入口？”

因为重导场景是真实存在的。

比如你改了 overlay 配色、错例筛选规则或者只想重建可视化目录，这时候重新走模型推理只会更慢、更容易引入额外变量。

## 脚本核心逻辑

### 主要流程

这个脚本的主链只有 5 步:

1. 解析 `--run-dir`
2. 把相对路径转成项目根路径下的绝对目录
3. 把 `max_samples_per_split` 传给 `export_run_visual_assets()`
4. 接收返回的 `error_cases_path` 和 split 级 visual 计数
5. 把关键结果打印到控制台

### 关键函数 1：`parse_args()`

这个函数看起来很薄，但它在固定协议边界。

当前只允许两个输入:

1. `--run-dir`
2. `--max-samples-per-split`

为什么不用把 checkpoint、config、device 也开放进来？

因为那样这个脚本就会开始越权，慢慢长成第二个 `scripts/test.py`。

### 关键函数 2：`main()`

`main()` 做的事情其实就是把“薄 CLI”落实到底。

它没有自己解析 metrics csv，也没有自己导图。
真正的实现都交给 `../../../../src/eval/export_visuals.py`。

换句话说，这里主动保持薄，是设计，不是偷懒。

### 当前最重要的取舍

为什么不用“一个入口同时支持重评估和重导图”？

因为那样最容易把两类动作混在一起:

1. 重算结果
2. 重建表现层资产

当前把它们拆开之后，问题定位会更清楚。
如果重导出来的 overlay 不对，你先查 `src/eval/export_visuals.py` 就行，不用怀疑 checkpoint 有没有重新跑偏。

## 如何运行这个脚本

最常见的用法是:

```bash
python scripts/export_visuals.py --run-dir experiments/A1_UNet_GlaS_v1_seed3407 --max-samples-per-split 2
```

如果要按默认值导出每个 split 最差的 5 个样本，可以写成:

```bash
python scripts/export_visuals.py --run-dir experiments/A1_UNet_GlaS_v1_seed3407
```

这里有两个使用边界要记住:

1. `run_dir` 必须已经包含 metrics csv 和 predictions
2. metrics csv 里回指的原图与 GT 路径必须仍然可读
3. 这个脚本不会帮你补测试结果，只会消费已有结果

## 如何验证脚本运行结果

最短检查路径可以按 4 步走:

1. 检查控制台是否打印 `experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md`
2. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/` 下是否出现 raw、gt、pred、overlay 四件套
3. 检查 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 是否回填 overlay 路径
4. 检查 visual count 是否与真实导图数量一致

通过标准很明确:

- `testA_visual_count` 和 `testB_visual_count` 为正整数
- `../../../../experiments/A1_UNet_GlaS_v1_seed3407/summaries/error_cases.md` 中最差样本能回指到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/` 或 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/`
- 没有重新改写 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testA_metrics.csv` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407/testB_metrics.csv`

## 容易误解的地方

- 不要把这个脚本当成正式测试入口，它不是
- 不要期待它自动补 prediction png，如果 prediction 本身不存在，它也无能为力
- 不要因为它很薄，就误会它不重要；可重导能力本身就是正式资产链的一部分

## 为什么不用别的设计

当前没有把重导逻辑塞回 `scripts/test.py`，也没有把它做成 IDE 手动脚本。

原因很简单:

1. 单独入口更容易复现
2. 命令行参数更容易纳入结果链说明
3. 手动临时脚本最难审计，也最容易在下次找不到

## 5 分钟自检任务

如果你已经看懂这个脚本，应该能回答:

1. 为什么它不接受 checkpoint 参数
2. 为什么它不重新算 metrics
3. 为什么它只接 run 目录和样本数上限
4. 为什么重导能力本身也是 stage02 正式对象

## 建议联读

- `scripts_test.py.md`
- `src_eval_export_visuals.py.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_error_cases.md`
