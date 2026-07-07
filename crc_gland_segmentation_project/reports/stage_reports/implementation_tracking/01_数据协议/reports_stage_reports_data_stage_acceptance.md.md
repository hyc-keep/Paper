# reports_stage_reports_data_stage_acceptance.md.md

## 结构化溯源卡片

- 正式对象: `../../data_stage_acceptance.md`
- 对应阶段: `01_数据协议`

### 论文依据
- 论文: `Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest`
- 章节: benchmark readiness, data integrity and evaluation preconditions
- 公式/定义: 阶段验收不能只看单个脚本成功，而要看整条正式数据链是否闭环

### 代码依据
- 仓库: `project_local_crc_gland_segmentation_project`
- 文件: `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- commit: `workspace_local_20260705`
- 许可证: `project_internal`

### 冻结回链
- 冻结文件: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md`
- 对应字段: `data_stage_pass`, `handoff_ready`, `preflight_pass`, `next_action`

### 当前实现落点
- 文件: `../../data_stage_acceptance.md`
- 生成来源文件: `../../../../tools/stage01_data_protocol/validate_data_assets.py`
- 生成来源符号: `build_acceptance_report()`

## 这个文件的作用

这份文件不是普通阅读笔记，也不是流程留痕。
它是 `01_数据协议` 这一步“正式能不能交给下一阶段”的最终验收结果。

你可以把它理解成“数据阶段的正式判定单”。

前面的很多对象都很重要:

- split CSV
- data check 报告
- label protocol 报告
- preview 图
- `scripts/train.py` 的 preflight 证据

但这些对象单看都只是局部真相。
`../../data_stage_acceptance.md` 的作用，就是把这些局部真相收束成统一结论。

## 这个文件在整个阶段中的位置

如果把 `01_数据协议` 看成一条生产线，这个文件就在最末端:

```text
源数据 / split / 配置 / label 目标 / preview / preflight
        ↓
../../../../tools/stage01_data_protocol/validate_data_assets.py
        ↓
../../data_stage_acceptance.md
        ↓
handoff_ready = True / data_stage_pass = True / preflight_pass = True
        ↓
next_action = enter_02_unet
```

换句话说，这份文件不负责重新生成资产，而是负责回答:

1. 当前阶段有没有真的闭环
2. 哪些门状态是 `True`
3. 下一步该前进还是回退

## 当前这个文件说明了什么

用人话说，这份文件不是解释某一个脚本怎么写，而是在给整个 `01_数据协议` 做最终定位。

它回答的是三件事:

1. 当前阶段有没有真的达到正式交接线
2. 这个 `pass` 到底只覆盖到哪里
3. 下一阶段是不是可以沿着当前输入层继续走

## 阶段协议回链卡片

- 当前阶段总协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/00_阶段总协议.md`
- 数据阶段验收协议: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/07_数据阶段验收.md`
- 数据产物清单: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/01_数据协议/06_数据产物清单.md`
- 执行导航: `../../../../../结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/00_执行导航.md`
- 当前对象清单: `00_交付范围内正式对象清单.md`
- 路线锁定文件: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/02_结直肠腺体分割_分阶段实验路线与执行标准.md`
- 路线锁定文件补充: `../../../../../结直肠腺体分割_plan_优化版/02_路线与投稿/01_结直肠腺体分割_高性价比路线总锁定.md`

这里的回链要说明的是:
这份验收结果不是“我看着差不多所以给 pass”，而是有明确协议要求必须存在的正式结果。

## 当前真实结果

当前文件里最关键的字段有:

- `asset_manifest`: `reports/stage_reports/asset_manifest.json`
- `split_assets_ready`: `True`
- `check_assets_ready`: `True`
- `label_assets_ready`: `True`
- `preview_assets_ready`: `True`
- `config_assets_ready`: `True`
- `source_assets_ready`: `True`
- `pass_source`: `True`
- `pass_split`: `True`
- `pass_pair`: `True`
- `pass_label`: `True`
- `pass_check`: `True`
- `pass_preview`: `True`
- `pass_handoff`: `True`
- `assets_traceable`: `True`
- `protocol_explainable`: `True`
- `data_stage_pass`: `True`
- `handoff_ready`: `True`
- `preflight_pass`: `True`
- `next_action`: `enter_02_unet`

你可以把这组字段看成当前阶段的总成绩单。

## 当前阶段通过的判定标准

这里最容易读偏的一点是:
这份文件里的每个 `True`，回答的是“这一条门状态有没有满足”，不是“后续所有阶段都完成了”。

正式推荐的理解方式是:

- `pass_source` 和 `pass_split`: 输入层是否完整
- `pass_pair`、`pass_label`、`pass_check`、`pass_preview`: 质检链是否完整
- `pass_handoff` 和 `handoff_ready`: 是否具备交接条件
- `data_stage_pass`: 当前数据阶段总体是否放行
- `preflight_pass`: 训练入口是否能接到这条正式链
- `next_action`: 现在该继续前进还是回退

## 这些列/字段分别是什么意思

- `pass_source` / `pass_split`: 输入层和正式 split 资产是否完整。
- `pass_pair` / `pass_label` / `pass_check` / `pass_preview`: 数据检查、标签协议、预览链是否都闭环。
- `pass_handoff` / `handoff_ready`: 当前阶段是否具备正式交接条件。
- `data_stage_pass`: `01_数据协议` 这一阶段是否整体放行。
- `preflight_pass`: 训练入口是否已经接住当前冻结输入层。
- `next_action`: 当前正式建议动作，当前真实值是 `enter_02_unet`。

### 必须满足的硬性条件

1. **正式输入层必须完整**
   - **验证方法**: 看 `pass_source`、`pass_split`、`config_assets_ready`、`source_assets_ready`
   - **判定结果**: `满足`。当前配置文件、数据源说明和全部 split CSV 都已落盘

2. **数据检查和标签协议必须闭环**
   - **验证方法**: 看 `pass_pair`、`pass_label`、`pass_check`
   - **判定结果**: `满足`。当前这些字段全部为 `True`

3. **预览和人工抽查必须达到阶段要求**
   - **验证方法**: 看 `pass_preview` 和上游 `manual_audit_status`
   - **判定结果**: `满足`。当前预览目录和人工抽查结果都已被上游总校验脚本接受

4. **交接状态和 preflight 必须成立**
   - **验证方法**: 看 `handoff_ready`、`preflight_pass`
   - **判定结果**: `满足`。当前既可交接，也能进入下一阶段前的训练入口预飞

### 可选但建议满足的条件

- `assets_traceable = True`
- `protocol_explainable = True`

这两项不是“有文件就行”，而是在说:
当前交付包既能追溯来源，也能对外解释清楚。

## 当前阶段的物理验收证据

### 证据 1: 结构化资产清单

- 文件路径: `../../asset_manifest.json`
- 关键字段:
  - GlaS split 行数: 68 / 17 / 60 / 20
  - CRAG split 行数: 153 / 20 / 40
  - preview 目录计数: 全部 `pass`
- 通过标准: split 资产真实存在，preview 目录数量满足阈值

### 证据 2: 数据阶段总校验报告

- 文件路径: `../../../data_checks/data_asset_validation_report.md`
- 关键字段:
  - `data_stage_pass = True`
  - `preflight_pass = True`
  - `next_action = enter_02_unet`
- 通过标准: validation report 与 acceptance report 结论一致

### 证据 3: 训练入口 preflight 证据

- 文件路径: `../../../runtime_checks/runtime_check_report.md`
- 关键字段:
  - `runtime_profile = data_protocol_preflight`
  - `sample_id = GlaS_official_train_train_1`
  - `input_shape = [522, 775, 3]`
  - `target_shape = [522, 775]`
- 通过标准: 正式训练入口已经真实读取到冻结后的样本链

### 证据 4: 当前验收结果本体

- 文件路径: `../../data_stage_acceptance.md`
- 关键字段:
  - `handoff_ready = True`
  - `data_stage_pass = True`
  - `preflight_pass = True`
  - `next_action = enter_02_unet`
- 通过标准: 这些字段同时成立，且没有 blocking reason

## 这份结果到底该怎么理解

这里最容易误判的地方是把“阶段验收通过”和“项目后续全部完成”混成一件事。

正确理解应该是:

1. 当前通过的是 `01_数据协议`
2. 当前通过依赖的是冻结输入层、split 资产、检查资产、preview 资产和 preflight 入口同时成立
3. 这还不等于模型前向、loss、backward、optimizer.step 已经全部跑通

说白了，这份结果是在告诉你“数据阶段可以交接了”，不是在告诉你“训练阶段已经完成了”。

## 当前阶段交付的正式资产清单

| 资产类别 | 资产路径 | 作用 | 下游消费者 |
|---|---|---|---|
| Split CSV | `splits/glas/*.csv` | GlaS 正式样本划分 | `src/data/datasets.py`, `scripts/train.py` |
| Split CSV | `splits/crag/*.csv` | CRAG 正式样本划分 | `src/data/datasets.py`, `scripts/train.py` |
| 数据配置 | `configs/data/glas.yaml`, `configs/data/crag.yaml` | 冻结数据根和 CSV 映射 | `src/data/datasets.py`, `tools/stage01_data_protocol/validate_data_assets.py` |
| 检查资产 | `reports/data_checks/*` | 证明 pair / label / foreground / manual audit 成立 | `tools/stage01_data_protocol/validate_data_assets.py` |
| 预览资产 | `reports/data_preview/*` | 证明预览链和人工审阅入口存在 | `tools/stage01_data_protocol/validate_data_assets.py` |
| 结构化快照 | `reports/stage_reports/asset_manifest.json` | 保存交接包当前快照 | `../../data_stage_acceptance.md`, 下游人工复核 |
| 正式验收结果 | `../../data_stage_acceptance.md` | 写出本阶段最终裁决 | `02_UNet流程验证` 进入前复核 |

## 当前阶段未完成但不影响放行的事项

这里一定要诚实。
当前阶段可以放行，不等于所有相关工作都全部做完。

当前明确还没做完、但不阻塞 `01_数据协议` 放行的项有:

- 后续模型实现文件还没进入正式实现
- 后续 loss 实现文件还没进入正式实现
- 后续 trainer 实现文件还没进入正式实现
- 完整训练链的 `loss_finite_pass`
- 完整训练链的 `grad_step_pass`
- 剩余 5 份 A 类对象说明文还没补完

这些项不阻塞当前阶段的原因是:
它们属于下游训练阶段，或者属于说明文覆盖度继续补齐，不属于“数据链是否成立”的最低通过线。

## 下游阶段的放行条件

进入 `02_UNet流程验证` 前，至少还要确认下面这些事:

1. **模型、loss、trainer 三件套必须落地**
   - 如何确认: 检查后续模型、loss、trainer 正式实现文件是否存在且不是占位壳

2. **完整 runtime 证据必须出现**
   - 如何确认: 新的 runtime 报告里必须出现 `output_shape`、`loss_value`、`backward_executed=True`、`optimizer_step_executed=True`

3. **当前输入层不能被绕开**
   - 如何确认: 新阶段依然沿用 `configs/data/*.yaml -> splits/*.csv -> src/data/datasets.py -> scripts/train.py`

## 回退触发条件

如果出现下面任一情况，就必须回退到 `01_数据协议` 重新执行:

1. **split 资产与配置不一致**
   - 检测方法: `../../../data_checks/data_asset_validation_report.md` 中 `pass_split != True`
   - 回退操作: 重新检查 `../../../../tools/stage01_data_protocol/prepare_glas_split.py`、`../../../../tools/stage01_data_protocol/prepare_crag_split.py` 和 `../../../../configs/data/*.yaml`

2. **检查或标签协议链破损**
   - 检测方法: `pass_pair`、`pass_label`、`pass_check` 任一不是 `True`
   - 回退操作: 重跑检查脚本和标签派生脚本，修复上游资产

3. **训练入口不再认正式数据链**
   - 检测方法: `preflight_pass != True` 或 runtime 报告里 `split_csv` 不再指向正式 CSV
   - 回退操作: 回退到数据阶段重查入口接线

4. **下一阶段偷偷改写了输入层契约**
   - 检测方法: 新训练代码绕开 `configs/data/*.yaml` 或直接扫描原始目录
   - 回退操作: 回退到当前阶段，重新锁定数据输入协议

## 如何手工验证这个文件的正确性

### 验证步骤 1: 核对正式验收字段

1. 打开 `../../data_stage_acceptance.md`
2. 查看 `data_stage_pass`、`handoff_ready`、`preflight_pass`
3. 记录 `next_action`

期望结果:

- 三个通过字段都为 `True`
- `next_action = enter_02_unet`

### 验证步骤 2: 核对结构化资产快照

1. 打开 `../../asset_manifest.json`
2. 查看 `split_assets`
3. 查看 `preview_assets`

期望结果:

- split 行数是 68 / 17 / 60 / 20 / 153 / 20 / 40
- preview 目录计数全部为 `pass`

### 验证步骤 3: 核对 preflight 入口证据

1. 打开 `../../../runtime_checks/runtime_check_report.md`
2. 看 `runtime_profile`
3. 看 `sample_id`、`input_shape`、`target_shape`

期望结果:

- `runtime_profile = data_protocol_preflight`
- `sample_id = GlaS_official_train_train_1`
- `input_shape = [522, 775, 3]`
- `target_shape = [522, 775]`

## 下一步工作清单

- [ ] 补完剩余 5 份 A 类对象说明文
- [ ] 在 `02_UNet流程验证` 中补模型、loss、trainer 正式对象
- [ ] 用新的 runtime 证据证明完整训练链成立

## 这个文件没说明什么

它没有说明:

- 模型训练效果已经成立
- loss 和 backward 已经跑通
- 后续所有说明文都已经补齐

所以不要把这份验收结果误读成“整个项目已经完成”。

## 常见问题

### 误区 1: `data_stage_pass = True` 就等于完整训练已经通过

不是。
它只说明数据阶段已经形成正式交接闭环。

### 误区 2: 只要 `asset_manifest.json` 存在就一定通过

也不是。
manifest 只是结构化快照，真正的阶段裁决还是看 `../../data_stage_acceptance.md` 里的门状态。

### 误区 3: 这份文件只是把上游报告抄了一遍

不对。
它是正式验收结果本体，负责把上游局部证据收束成最终可交接结论。

## 5 分钟自检任务

如果你只给自己 5 分钟，建议做这三件事:

1. 打开 `../../data_stage_acceptance.md`，确认 `data_stage_pass = True`
2. 打开 `../../asset_manifest.json`，确认 split 行数是 68 / 17 / 60 / 20 / 153 / 20 / 40
3. 打开 `../../../runtime_checks/runtime_check_report.md`，确认 `runtime_profile = data_protocol_preflight`

## 读完后怎么自检

如果你已经读完这份说明文，至少要能独立回答下面两个问题:

1. 为什么当前 `01_数据协议` 已经能写 `pass`
2. 为什么这个 `pass` 又不等于完整训练阶段已经完成

学完后你应该具备什么能力？

你应该能清楚区分:

- 数据阶段为什么已经能放行
- 这个 `pass` 的边界到底在哪
- 为什么它和“完整训练还没完成”并不冲突
