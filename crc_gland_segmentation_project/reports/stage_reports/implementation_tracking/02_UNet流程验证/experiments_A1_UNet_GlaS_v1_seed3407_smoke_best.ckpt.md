# experiments_A1_UNet_GlaS_v1_seed3407_smoke_best.ckpt.md

## 先讲定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已经写了 `best_epoch` 和 `best_metric_value`，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt`？”

因为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 更像结果索引卡。
而当前这份文件更像“规范 smoke run 当前最优模型现场快照”。

先讲定位:

当前文件就是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 这份正式运行资产的对象级说明文。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 的运行资产说明文。
- 流程: 它位于每轮验证结果已经产出之后, 由 trainer 按 `val_objdice` 选优规则决定是否覆盖写盘。
- 结构: 当前文件是二进制 checkpoint, 逻辑上由 `epoch`、`model_state_dict`、`optimizer_state_dict`、`metric_value` 四组内容组成。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py`、`../../../../src/eval/checkpoint_selector.py` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 向下服务恢复、评估和最优模型回查。
- 解释: 它回答“当前规范 smoke run 的最优模型快照到底落没落盘, 是按什么标准选出来的”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和当前 run 目录。
- 误区: 不能把它误读成完整训练包、最终总结页或所有实验结论的唯一来源。
- 自检: 读完后应能说清为什么当前它和 `best_epoch=1`、`best_metric_value=0.26280593599215546` 对得上。
- 局限: 它只证明当前最优 checkpoint 已落盘, 不能替代完整测试结果、可视化资产和长程训练结论。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里按正式选优规则留下的最优 checkpoint 资产。
- 它负责回答“如果后面要恢复当前最优模型, 到底该从哪一个真实文件拿权重和优化器状态”。
- 作用: 把当前规范 smoke run 的最优模型快照稳定落盘, 供恢复和回查直接使用。
- 位置: 它位于 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/` 目录, 处在验证选优之后、下游恢复之前。
- 职责: 对 `best_epoch=1` 与 `best_metric_value=0.26280593599215546` 对应的最优 checkpoint 实体负责。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `supervised model selection workflow`
- 章节: `checkpoint persistence for best model recovery`
- 公式/定义: `epoch + model_state + optimizer_state + metric_value -> best checkpoint artifact`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`, `../../../../src/eval/checkpoint_selector.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 对应字段: `best_selector`, `best_epoch`, `best_metric_value`, `metric_value`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 之所以只保存最小恢复所需字段, 不是因为 trainer 功能不完整。

路线锁定文件先把 stage02 锁定成“先建立最小可审计闭环”的路线。
正式规则文件又要求最优模型快照必须能回查, 但不要求现在就引入更复杂训练态。

所以这份资产的组织方式本质上是在服务“先把最优恢复链稳定落盘, 再谈后续完整扩展”。

## 当前这个文件说明了什么

它位于当前运行资产链的后半段:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 先给出每轮 `val_objdice`
2. `../../../../src/eval/checkpoint_selector.py` 决定当前轮是否刷新 best
3. `../../../../src/engine/trainer.py` 把最优快照写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 再把 `best_epoch` 和 `best_metric_value` 写成索引字段

所以它是当前 best 模型真正可恢复的实体文件。

## 这张表/这个文件长什么样

当前文件不是 CSV 或 YAML, 而是 PyTorch checkpoint 二进制文件。

说白了, 它逻辑上至少包含 4 组内容:

1. `epoch`
2. `model_state_dict`
3. `optimizer_state_dict`
4. `metric_value`

## 这些列/字段分别是什么意思

1. `epoch` 解释“这份最优快照来自第几轮”
2. `model_state_dict` 解释“当前最优模型权重到底是哪一组参数”
3. `optimizer_state_dict` 解释“如果需要继续恢复训练, 优化器状态应该从哪里接上”
4. `metric_value` 解释“这份 checkpoint 为什么被认定成 best”

## 当前实现状态

- 状态: `已存在`
- 可读性: `二进制文件, 需要按 checkpoint 语义理解`
- 当前真实结论: `当前最优 checkpoint 已落盘, 且当前最优轮次来自规范 smoke run 的第 1 轮`

## 当前真实结果

当前最关键的真实路径至少有 5 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 已作为同目录对照资产存在
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已给出当前 best 选择所依赖的验证数值
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已写明 `best_epoch=1`
5. `../../../../src/engine/trainer.py` 已把 best checkpoint 写盘逻辑固定到当前路径

当前最关键的真实字段至少有 5 组:

1. `best_selector=val_objdice_max`
2. `best_epoch=1`
3. `best_metric_value=0.26280593599215546`
4. `val_objdice=0.26280593599215546`
5. `metric_value` 会被和当前 best 指标一起打包写进 checkpoint

## 如何手工验证这个文件的正确性

检查方法:

1. 先确认路径 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 真实存在
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 看 `best_epoch` 和 `best_metric_value`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 看当前唯一一行 `val_objdice`
4. 回看 `../../../../src/engine/trainer.py` 里的 `_save_checkpoint(...)` 和 `is_best` 分支

通过标准:

- `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 真实存在
- `best_epoch=1` 与当前最小 run 的单行验证记录不冲突
- `best_metric_value=0.26280593599215546` 能和 `val_objdice=0.26280593599215546` 对上

## 这个文件没说明什么

当前文件能证明的是:

1. 当前最优 checkpoint 已经真实落盘
2. best 选择规则已经从验证表一路落实到实体文件
3. 当前最优模型的恢复入口已经存在

当前文件还不能单独证明的是:

1. TestA 和 TestB 的正式测试结果都已交齐
2. 当前 best 一定代表完整长程训练的最终最优结论
3. 只凭这一份 checkpoint 就足以替代总结页、验证表和可视化输出

## 常见问题

- 误解 1: 以为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 只是目录里随手留的模型副本
  - 实际上它是按 `val_objdice` 正式选优规则写出的最优恢复快照
- 误解 2: 以为有了这份文件就等于完整阶段验收完成
  - 实际上它只证明最优模型快照已落盘, 不替代测试、总结和可视化资产
- 误解 3: 以为当前 best 结果天然代表长程训练结论
  - 实际上当前 run 仍带有 `smoke_check=true` 痕迹, 不能夸大解释

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_last.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
- `src_eval_checkpoint_selector.py.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. 当前规范 smoke run 的最优 checkpoint 为什么不是普通模型副本
2. 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`、`../../../../src/eval/checkpoint_selector.py` 分别怎么配合
3. 为什么当前文件能证明 best 资产链成立, 但还不能替代完整阶段验收
