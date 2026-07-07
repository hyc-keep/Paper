# experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md

## 先讲定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已经写了运行索引，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`？”

因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 更像机器和审计脚本友好的索引卡。
而当前这份文件更像给人直接看的最小结果摘要页。

先讲定位:

当前文件就是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md` 这份正式运行资产的对象级说明文。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md` 的运行资产说明文。
- 流程: 它位于训练主循环结束之后, 由 trainer 根据 `stop_reason`、`best_epoch`、`best_metric_value` 等字段生成。
- 结构: 当前文件按 `stop_reason`、`best_epoch`、`best_metric_name`、`best_metric_value`、`smoke_check`、`amp_active` 这几组摘要字段组织。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 向下服务人工审阅、总结页和阶段交接。
- 解释: 它回答“这次规范 smoke run 最后发生了什么, 当前最好是谁, 这个 run 是不是 smoke-check”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和当前 run 目录。
- 误区: 不能把它误读成完整阶段验收报告或完整实验总结。
- 自检: 读完后应能说清它为什么比 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 更适合给人快速看结论。
- 局限: 它只证明最小 smoke run 摘要页已经落盘, 不能替代完整结果包、可视化和测试结果。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里把最核心运行结论写成人可直接阅读 Markdown 的正式摘要资产。
- 它负责把索引字段重新组织成最短路径结论页, 让读者不用先展开 YAML/CSV 才知道这次 run 发生了什么。
- 作用: 把当前规范 smoke run 的关键信息压缩成一页人可直接阅读的正式摘要。
- 位置: 它位于 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/` 目录, 处在训练结束写盘之后、人工审阅和阶段交接之前。
- 职责: 对 `stop_reason=smoke_check_complete`、`best_epoch=1` 和 `best_metric_value=0.262806` 这组最小摘要结论负责。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `baseline run summary and audit handoff`
- 章节: `minimal human-readable summary for one run`
- 公式/定义: `stop_reason + best_epoch + best_metric_value + runtime flags -> one summary page`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 对应字段: `stop_reason`, `best_epoch`, `best_metric_name`, `best_metric_value`, `smoke_check`, `amp_active`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md` 之所以用最短字段列表写摘要, 不是为了省事。
它服务的是“结构化索引先存在, 再额外给一张人可直接读的最小摘要页”这条正式交接链。

## 当前这个文件说明了什么

它位于当前运行资产链的收口层:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 先给出索引字段
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 提供 best 数值来源
3. `../../../../src/engine/trainer.py` 把最关键结论压缩生成 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`

所以它是“让人先一眼看懂 run 结论”的正式摘要资产。

## 这张表/这个文件长什么样

当前文件是一个很短的 Markdown 摘要页。
说白了, 它至少由 6 组摘要字段组成: `stop_reason`、`best_epoch`、`best_metric_name`、`best_metric_value`、`smoke_check`、`amp_active`。

## 这些列/字段分别是什么意思

1. `stop_reason` 解释“这次 run 为什么停下”
2. `best_epoch`、`best_metric_name`、`best_metric_value` 解释“当前最好轮次是谁、按什么指标选、值是多少”
3. `smoke_check` 解释“这次 run 是不是最小 smoke 模式”
4. `amp_active` 解释“最终运行态下 AMP 是否真的启用”

## 当前实现状态

- 状态: `已存在`
- 可读性: `可直接人工审阅`
- 当前真实结论: `当前规范 smoke run 摘要页已经落盘, 且最优轮次为第 1 轮`

## 当前真实结果

当前最关键的真实路径至少有 4 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已作为它的上游索引资产存在
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已提供当前 best 指标数值来源
4. `../../../../src/engine/trainer.py` 已把摘要页写盘逻辑固定到真实目录 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/`

当前最关键的真实字段至少有 6 组:

1. `stop_reason=smoke_check_complete`
2. `best_epoch=1`
3. `best_metric_name=val_objdice`
4. `best_metric_value=0.262806`
5. `smoke_check=true`
6. `amp_active=false`

## 这份摘要页里到底写了什么

当前文件最核心的正文就是:

1. 这次 run 因为 `smoke_check_complete` 停下
2. 当前最好轮次是 `1`
3. 当前 best 指标名是 `val_objdice`
4. 当前 best 指标值是 `0.262806`
5. 当前 run 属于 `smoke_check=true`
6. 当前最终运行态 `amp_active=false`

## 对应代码里的真实协议痕迹

1. `../../../../src/engine/trainer.py` 在主循环结束后先拿到 `stop_reason`、`best_epoch`、`best_metric_value`
2. `../../../../src/engine/trainer.py` 固定把摘要文本写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 共同提供摘要页的上游事实来源

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
4. 回看 `../../../../src/engine/trainer.py` 的摘要页生成逻辑

通过标准:

- `stop_reason`、`best_epoch`、`best_metric_name`、`best_metric_value`、`smoke_check`、`amp_active` 六组字段都存在
- `best_metric_value=0.262806` 能和上游数值来源对上到合理精度
- 当前文件真实存在

## 这个文件没说明什么

当前文件能证明的是:

1. 当前 run 摘要页已经真实落盘
2. 最小 smoke run 的关键结论可以被直接人工阅读
3. 上游索引字段已经被正确压缩成简明摘要

当前文件还不能单独证明的是:

1. 完整长程实验总结已经写完
2. TestA/TestB 的正式测试结果已经交齐
3. 只凭这一页就可以替代 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`、checkpoint 和完整总结报告

## 常见问题

- 误解 1: 以为这份摘要页只是把 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 原样重排
  - 实际上它是给人快速看的摘要视图, 负责把索引字段整理成人可直接阅读的结论页
- 误解 2: 以为有了这份摘要页就等于完整实验总结完成
  - 实际上它只是一张最小摘要页, 还不替代完整总结和测试结果
- 误解 3: 以为 `best_metric_value=0.262806` 是独立产生的新数值
  - 实际上它来自同一条验证与选优主链, 只是被格式化成更适合阅读的摘要

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_last.ckpt.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md` 为什么是正式摘要资产
2. 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 的分工差异是什么
3. 为什么当前文件能证明摘要页资产链成立, 但还不能替代完整实验总结
