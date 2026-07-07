# experiments_A1_UNet_GlaS_v1_seed3407_smoke_last.ckpt.md

## 这份文件的定位

你现在可能会问:

“既然已经有 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 了，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt`？”

因为前者回答的是“当前最优是谁”。
而当前这份文件回答的是“训练实际停在什么状态”。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 的运行资产说明文。
- 流程: 它位于每轮训练和验证结束之后, 由 trainer 无条件更新写盘, 用来记录当前最新训练状态。
- 结构: 当前文件是二进制 checkpoint, 逻辑上由 `epoch`、`model_state_dict`、`optimizer_state_dict`、`metric_value` 四组内容组成。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 向下服务续跑、排障和“训练到底停在哪”回查。
- 解释: 它回答“当前规范 smoke run 最后一轮的模型和优化器状态到底保存在哪”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 和当前 run 目录。
- 误区: 不能把它误读成“当前最优模型”或“最终阶段结论”。
- 自检: 读完后应能说清 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 为什么要并存。
- 局限: 它只证明最后一轮训练状态已落盘, 不能替代 best 选择解释、测试结果和完整总结。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里回答“训练最后停在哪一轮、最后一轮状态如何恢复”的正式 checkpoint 资产。
- 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 的角色不同: 一个强调“最后停在哪”, 一个强调“最佳是谁”。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `supervised training state persistence`
- 章节: `last-step checkpoint for recovery and audit`
- 公式/定义: `latest epoch + model_state + optimizer_state + metric_value -> last checkpoint artifact`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 对应字段: `epoch_count`, `stop_reason`, `metric_value`, `epoch`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段训练步骤: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/02_训练步骤.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 之所以和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 共用同一保存结构, 不是因为 trainer 偷懒。

路线锁定文件先把 stage02 锁成“先保证训练最小闭环可恢复”。
正式规则文件又要求最后状态和最佳状态都必须可追溯。

所以这份资产的组织方式本质上是在服务“用统一 checkpoint 结构同时支持 latest 恢复和 best 对照”。

## 当前这个文件说明了什么

它位于当前运行资产链的最末段:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 先记录训练侧最后一轮
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 记录验证侧最后一轮
3. `../../../../src/engine/trainer.py` 无条件把当前轮快照写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt`
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 再把 `stop_reason`、`epoch_count` 等索引字段写出来

所以它代表“最后停表时的完整状态快照”。

## 这张表/这个文件长什么样

当前文件不是可直接展开阅读的文本文件, 而是 PyTorch checkpoint 二进制文件。
说白了, 它逻辑上至少包含 4 组内容: `epoch`、`model_state_dict`、`optimizer_state_dict`、`metric_value`。

## 这些列/字段分别是什么意思

1. `epoch` 解释“训练最后停在第几轮”
2. `model_state_dict` 解释“最后一轮对应的模型参数是什么”
3. `optimizer_state_dict` 解释“如果要从最后状态续跑, 优化器应该接哪一个状态”
4. `metric_value` 解释“最后一轮对应的验证指标值是多少”

## 当前实现状态

- 状态: `已存在`
- 可读性: `二进制文件, 需要按 checkpoint 语义理解`
- 当前真实结论: `当前最后一轮 checkpoint 已落盘, 且当前规范 smoke run 在第 1 轮结束`

## 当前真实结果

当前最关键的真实路径至少有 5 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 已作为同目录对照资产存在
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 已给出当前最后一轮训练记录
4. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已给出当前最后一轮验证记录
5. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 已写明 `epoch_count=1` 与 `stop_reason=smoke_check_complete`

当前最关键的真实字段至少有 5 组:

1. `epoch_count=1`
2. `stop_reason=smoke_check_complete`
3. `best_epoch=1`
4. `epoch=1`
5. `metric_value` 会随最后一轮状态一起写进 checkpoint

## 如何手工验证这个文件的正确性

检查方法:

1. 先确认路径 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 真实存在
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv` 看最后一轮是否为 `epoch=1`
3. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 看最后一轮验证记录
4. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 看 `epoch_count=1` 与 `stop_reason=smoke_check_complete`
5. 回看 `../../../../src/engine/trainer.py` 里写 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 的无条件分支

通过标准:

- 当前最后一轮与 `epoch_count=1` 对得上
- 当前停止原因与 `smoke_check_complete` 一致
- 你能明确说出 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 的职责差异

## 这个文件没说明什么

当前文件能证明的是:

1. 当前最后一轮状态 checkpoint 已经真实落盘
2. 如果需要续跑或排障, 当前有一个明确的最后状态恢复入口
3. 训练日志、验证日志和 checkpoint 状态已经能互相回查

当前文件还不能单独证明的是:

1. 当前最后一轮一定等于全程最优
2. 完整长程训练已经交齐全部 epoch 结果
3. 只凭这一份 checkpoint 就能替代验证表、总结页和后续测试结果

## 常见问题

- 误解 1: 以为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 是重复文件
  - 实际上一个回答“最后停在哪”, 一个回答“最好是谁”
- 误解 2: 以为 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 就是当前最优模型
  - 实际上只有当最后一轮碰巧也是 best 时它们才会一致
- 误解 3: 以为当前有这份文件就说明完整训练跑满
  - 实际上当前仍是 `smoke_check_complete` 的最小 run

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_best.ckpt.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_log.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/last.ckpt` 为什么和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/checkpoints/best.ckpt` 必须区分
2. 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/train_log.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 分别怎么对账
3. 为什么当前文件能证明最后状态恢复链成立, 但还不能被夸大成完整阶段结论
