# experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_curve.csv.md

## 这份文件的定位

你现在可能会问:

“既然 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已经记录了验证结果，为什么还要再解释 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`？”

因为前者更像完整验证指标表。
而当前这份文件更像给验证曲线和总结页准备的轻量趋势表。

## 一眼先抓住什么

- 定位: 当前文件是 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv` 的运行资产说明文。
- 流程: 它位于完整验证结果表已经累计完成之后, 由 trainer 对 `val_rows` 再整理导出为曲线专用表。
- 结构: 当前文件按 `epoch`、`val_loss`、`val_objdice`、`val_dice`、`val_iou` 五列组织。
- 衔接: 它向上回接 `../../../../src/engine/trainer.py` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`, 向下服务验证曲线、选优趋势解释和阶段总结。
- 解释: 它回答“验证走势需要的核心列有没有被单独整理出来”。
- 验证: 需要同时对照 `../../../../src/engine/trainer.py`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 和当前 run 目录。
- 误区: 不能把它误读成新的验证来源表或完整指标表替身。
- 自检: 读完后应能说清它为什么比 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 更适合画曲线, 但又为什么不能替代完整验证表。
- 局限: 它只证明验证曲线表已经落盘, 不能替代完整指标、best 选择记录和测试结果。

## 这个文件是干什么的

- 它是当前 `A1_UNet_GlaS_v1_seed3407_smoke` run 目录里专门服务验证曲线阅读的正式资产。
- 它把完整验证表里最适合看走势和选优的字段单独整理出来, 方便后续曲线或总结页消费。

## 结构化溯源卡片

- 正式对象: `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`
- 对应阶段: `02_UNet流程验证`

### 论文依据

- 论文: `segmentation validation trend persistence`
- 章节: `compact validation curve export for model selection inspection`
- 公式/定义: `val_rows -> compact val curve table`

### 代码依据

- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../src/engine/trainer.py`
- commit: `workspace_local_20260706`
- 许可证: `project_internal`

### 冻结回链

- 阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 命名与记录规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 评估口径规则: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`
- 对应字段: `val_loss`, `val_objdice`, `val_dice`, `val_iou`

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/00_阶段总协议.md`
- 当前阶段验证测试与可视化协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/03_验证测试与可视化.md`
- 当前阶段验收: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/05_阶段验收.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 正式规则文件 1: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/03_命名与结果记录规范.md`
- 正式规则文件 2: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/04_评估口径与官方脚本对齐.md`

## 为什么这份资产要这样组织

当前 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv` 没有把 boundary 和 object 距离所有列都塞进来，是为了让验证走势和选优阅读更聚焦。
它服务的是“完整指标保留在原表, 验证走势另给一张更适合画曲线的轻量表”。

## 当前这个文件说明了什么

它位于当前验证资产链的整理层:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 先保留完整验证指标表
2. `../../../../src/engine/trainer.py` 把 `val_rows` 汇总成曲线表
3. 当前文件再把验证走势最核心的 5 列写到 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`

所以它是从正式验证表中抽取出来的曲线视图资产。

## 这张表/这个文件长什么样

当前文件只有 1 行真实数据, 但结构非常明确:

1. `epoch`
2. `val_loss`
3. `val_objdice`
4. `val_dice`
5. `val_iou`

## 这些列/字段分别是什么意思

1. `epoch` 解释当前曲线点对应第几轮
2. `val_loss` 解释这一轮验证总损失
3. `val_objdice` 解释当前主选优指标
4. `val_dice` 与 `val_iou` 解释验证侧最核心的重叠表现

## 当前实现状态

- 状态: `已存在`
- 当前行数: `1`
- 当前真实结论: `验证曲线表已经落盘, 但当前仍是规范 smoke run 的 1 个曲线点`

## 当前真实结果

当前最关键的真实路径至少有 4 组:

1. 当前资产路径已经固定在 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`
2. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 已作为它的上游完整验证表存在
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/train_curve.csv` 已作为同目录对照曲线存在
4. `../../../../src/engine/trainer.py` 已把曲线表写盘逻辑固定到真实目录 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/`

当前最关键的真实字段至少有 5 组:

1. `epoch=1`
2. `val_loss=1.2901947498321533`
3. `val_objdice=0.26280593599215546`
4. `val_dice=0.49554966074459383`
5. `val_iou=0.3651432910243176`

## 这份曲线表里到底写了什么

当前表头是:

`epoch,val_loss,val_objdice,val_dice,val_iou`

当前唯一一行真实数值是:

- `epoch=1`
- `val_loss=1.2901947498321533`
- `val_objdice=0.26280593599215546`
- `val_dice=0.49554966074459383`
- `val_iou=0.3651432910243176`

## 对应代码里的真实协议痕迹

1. `../../../../src/engine/trainer.py` 先在主循环里累计 `val_rows`
2. `../../../../src/engine/trainer.py` 结束后把 `val_rows` 写成 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`
3. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 提供更完整的上游验证来源表

## 如何手工验证这个文件的正确性

检查方法:

1. 打开 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv`
2. 对照 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`
3. 回看 `../../../../src/engine/trainer.py` 里写当前曲线表的分支

通过标准:

- 当前文件真实存在
- 表头包含 `epoch`、`val_loss`、`val_objdice`、`val_dice`、`val_iou`
- 当前唯一一行数值能和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 的同轮记录对上

## 这个文件没说明什么

当前文件能证明的是:

1. 验证曲线表已经真实落盘
2. 完整验证表已经进一步整理成曲线友好格式
3. 当前验证走势和主选优指标可以被后续总结或可视化消费

当前文件还不能单独证明的是:

1. 完整测试包已经交齐
2. 只看 `val_objdice`、`val_dice`、`val_iou` 就能替代完整指标表
3. 只凭这一张表就足以替代 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 和总结页

## 常见问题

- 误解 1: 以为这份表和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 完全重复
  - 实际上前者是曲线精简表, 后者是完整验证指标表
- 误解 2: 以为当前只有 1 行就不算正式曲线资产
  - 实际上当前只是最小 smoke run, 但验证曲线资产链已经成立
- 误解 3: 以为看验证曲线就等于看完完整评估
  - 实际上还要结合 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv`、`../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/run_meta.yaml` 和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/summaries/run_summary.md`

## 建议联读

- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_val_metrics.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_train_curve.csv.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_summary.md`
- `experiments_A1_UNet_GlaS_v1_seed3407_smoke_run_meta.yaml.md`
- `src_engine_trainer.py.md`

## 学完后你应该具备什么能力

学完这份文档后, 你至少应该能回答:

1. `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/curves/val_curve.csv` 为什么不是重复表
2. 它和 `../../../../experiments/A1_UNet_GlaS_v1_seed3407_smoke/val_metrics.csv` 的分工差异是什么
3. 为什么当前文件能证明验证曲线资产链成立, 但还不能替代完整评估结果
