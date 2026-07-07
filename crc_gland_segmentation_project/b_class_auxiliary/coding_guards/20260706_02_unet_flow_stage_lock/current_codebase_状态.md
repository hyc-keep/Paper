# Current Codebase 状态

## 0. 本轮最小扫描范围

| 目录 | 为什么必须扫描 | 最低检查动作 |
|------|---------------|-------------|
| `datasets/` | 当前阶段必须确认数据阶段交接资产是否真的在工程区内存在，而不是只剩口头描述 | 检查 `datasets/01_GlaS_official_raw/Grade.csv`、`datasets/DATASET_SOURCE_NOTES.md`；确认当前扫描到 `759` 个文件，且 `GlaS` 原始资产与来源说明都已在工程区 |
| `splits/` | 当前阶段必须确认正式 split CSV 是否已经冻结给 stage02 继承 | 检查 `splits/glas/glas_train68.csv`、`splits/glas/glas_val17.csv`、`splits/crag/crag_train153.csv`；确认当前扫描到 `10` 个文件、`2` 个子目录 |
| `configs/` | 当前阶段必须确认正式配置体系是否至少已经具备 data 层 | 检查 `configs/data/glas.yaml`、`configs/data/crag.yaml`；确认当前扫描到 `3` 个文件、`1` 个子目录 |
| `src/` | 当前阶段必须确认正式源码主链已经有哪些能力、哪些子模块还停在 stage02 之前 | 检查 `src/data/datasets.py`、`src/data/csv_loader.py`、`src/data/mask_ops.py`；确认当前扫描到 `15` 个文件、`3` 个子目录 |
| `scripts/` | 当前阶段必须确认现有脚本入口是 stage01 preflight 还是 stage02 训练链 | 检查 `scripts/train.py`、`scripts/README.md`；确认当前扫描到 `2` 个文件 |
| `tools/` | 当前阶段必须确认 A 类正式工具链是否已经按阶段目录落位，以及是否还残留待裁决工具 | 检查 `tools/stage01_data_protocol/prepare_glas_split.py`、`tools/stage01_data_protocol/validate_data_assets.py`、`tools/c_pending_review/build_manual_audit_notebook.py`；确认当前扫描到 `11` 个文件、`2` 个子目录 |
| `b_class_auxiliary/` | 当前阶段必须确认 B 类门禁脚本、运行留痕和 coding guards 是否已经从正式主区隔离 | 检查 `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`、`b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/00_阶段实现卡.md`；确认当前扫描到 `53` 个文件、`21` 个子目录 |
| `experiments/` | 当前阶段必须确认是否已经存在 stage02 正式 run 资产，避免把未来资产写成当前已存在 | 检查 `experiments/README.md`；确认当前扫描到 `1` 个文件 |
| `external/` | 当前阶段必须确认第三方实现适配层现在处于什么状态，避免误写成已经接入 baseline | 检查 `external/README.md`；确认当前扫描到 `1` 个文件 |
| `reports/` | 当前阶段必须确认 A 类正式报告链已经有哪些数据阶段资产，并和 B 类流程留痕保持分离 | 检查 `reports/stage_reports/asset_manifest.json`、`reports/data_checks/data_check_report.md`、`reports/stage_reports/data_stage_acceptance.md`；确认当前扫描到 `171` 个文件、`36` 个子目录 |

## 1. 当前阶段相关目录扫描

| 目录 | 已有文件/资产 | 状态 | 本次是否受影响 |
|------|--------------|------|---------------|
| `datasets/` | `datasets/DATASETS_README.md`、`datasets/DATASET_SOURCE_NOTES.md`、`datasets/01_GlaS_official_raw/Grade.csv`、`datasets/01_GlaS_official_raw/testA_1.bmp` | 已存在 `759` 个文件、`14` 个子目录；数据阶段原始资产和来源说明都已在工程区，当前可被 stage02 直接继承 | `否`；本轮只核对数据身份，不改数据资产 |
| `splits/` | `splits/glas/glas_train68.csv`、`splits/glas/glas_val17.csv`、`splits/glas/glas_testA60.csv`、`splits/crag/crag_train153.csv` | 已存在 `10` 个文件、`2` 个子目录；`GlaS` 与 `CRAG` 正式 split 已冻结给后续阶段继承 | `否`；本轮只确认 split 可被 stage02 复用 |
| `configs/` | `configs/data/glas.yaml`、`configs/data/crag.yaml`、`configs/data/README.md` | 已存在 3 个文件、1 个子目录；当前配置体系只落地了 data 层，stage02 需要的 model、train、eval、experiment 配置还未落地 | 是；后续编码阶段将从这里向上扩出 stage02 配置链 |
| `src/` | `src/data/datasets.py`、`src/data/csv_loader.py`、`src/data/boundary_targets.py`、`src/data/distance_targets.py`、`src/data/mask_ops.py` | 已存在 15 个文件、3 个子目录；当前源码主链以 data 层为主，尚未落地 stage02 需要的 models、losses、engine、eval 子模块 | 是；这里是后续 stage02 正式代码的核心新增区 |
| `scripts/` | `scripts/train.py`、`scripts/README.md` | 已存在 2 个文件；当前脚本层只有 stage01 formal preflight 入口与说明文，stage02 的 test、export_visuals、summarize_stage 脚本尚未落地 | 是；后续编码阶段会在脚本层补齐 stage02 主链入口 |
| `tools/` | `tools/stage01_data_protocol/build_boundary_targets.py`、`tools/stage01_data_protocol/build_distance_targets.py`、`tools/stage01_data_protocol/prepare_glas_split.py`、`tools/c_pending_review/build_manual_audit_notebook.py` | 已存在 `11` 个文件、`2` 个子目录；A 类正式工具已按 `stage01_data_protocol` 分区，另有 `c_pending_review` 待裁决工具 | `否`；本轮不改 A 类正式工具链 |
| `b_class_auxiliary/` | `b_class_auxiliary/tools/check_precheck_docs.py`、`b_class_auxiliary/tools/check_stage_definition_gate.py`、`b_class_auxiliary/runtime_checks/research_alignment_gate_report.md`、`b_class_auxiliary/coding_guards/20260705_02_unet_flow_research/研究定标记录.md` | 已存在 53 个文件、21 个子目录；B 类门禁脚本、运行留痕和研究/阶段锁定 guard 已集中隔离 | 是；本轮继续在这里补齐 stage02 的 Pre-check 文档链 |
| `experiments/` | `experiments/README.md` | 已存在 `1` 个文件；当前只有正式 run 目录说明文，stage02 还没有任何真实 run 资产 | `否`；本轮不产生运行资产 |
| `external/` | `external/README.md` | 已存在 `1` 个文件；当前只有第三方实现适配层说明文，baseline 与外部对比仍未进入正式接入阶段 | `否`；本轮不接外部实现 |
| `reports/` | `reports/stage_reports/asset_manifest.json`、`reports/stage_reports/data_stage_acceptance.md`、`reports/data_checks/data_check_report.md`、`reports/data_checks/binary_mask_summary.csv`、`reports/stage_reports/implementation_tracking/01_数据协议/scripts_train.py.md` | 已存在 `171` 个文件、`36` 个子目录；data stage 的正式报告、preview、stage report 与 implementation_tracking 已齐全，且与 B 类留痕目录分离 | `否`；本轮只把它作为 stage02 继承上游证据，不新增正式报告 |

## 2. 已实现能力
- 已有正式数据入口: `datasets/01_GlaS_official_raw/*`、`datasets/DATASET_SOURCE_NOTES.md`
- 已有正式 split 资产: `splits/glas/*.csv` 与 `splits/crag/*.csv`
- 已有正式 data 配置: `configs/data/glas.yaml`、`configs/data/crag.yaml`
- 已有 data 层源码: `src/data/datasets.py`、`src/data/csv_loader.py`、`src/data/mask_ops.py`、`src/data/boundary_targets.py`、`src/data/distance_targets.py`
- 已有 stage01 formal preflight 入口: `scripts/train.py`
- 已有 A 类正式工具: `tools/stage01_data_protocol/*.py`
- 已有 B 类研究、阶段锁定与各类 gate 脚本: `b_class_auxiliary/tools/*`、`b_class_auxiliary/runtime_checks/*`、`b_class_auxiliary/coding_guards/*`
- 已有 data stage 正式报告链: `reports/data_checks/*`、`reports/data_preview/*`、`reports/stage_reports/data_stage_acceptance.md`、`reports/stage_reports/asset_manifest.json`

## 3. 缺口与风险
- 缺口1: stage02 协议点名的 models、losses、metrics、engine、eval 子模块还未落地到 `src/`
- 缺口2: stage02 需要的 configs/model、configs/train、configs/eval、configs/experiment 仍未建立
- 缺口3: stage02 需要的 scripts/test.py、scripts/export_visuals.py、scripts/summarize_stage.py 仍未落地
- 缺口4: `experiments/` 当前只有 README，尚未形成 `A1_UNet_GlaS_v1_seed3407` 的正式运行资产链
- 风险1: 如果把 `scripts/train.py` 直接口头扩写成 stage02 完整训练入口，会把 stage01 的 `data_protocol_preflight` 职责和 stage02 的训练闭环职责混在一起
- 风险2: 如果不在编码前先把 object metrics、threshold、best selector 和 TestA/TestB 分开导出入口写死，后续运行证据很容易再次漂移

## 4. 本次预计新增/修改

| 文件 | 动作 | 原因 | 是否已有相近实现 |
|------|------|------|----------------|
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md` | `update` | 需要把 Pre-check 的上游约束、路线约束和未来工程落点收紧到真实阶段边界 | `是`；当前目录已有初稿 |
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_gate_check.md` | `create` | 需要把“当前为何允许进入 Pre-check”写成正式门控检查文件 | `否`；当前任务目录此前没有这份文件 |
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md` | `create` | 需要把 stage02 当前工程现实、已有能力、缺口和风险写成可审计结果 | `否`；当前任务目录此前没有这份文件 |
| `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md` | `create` | 需要把 Pre-check 汇总件正式落盘，并为 precheck gate 提供输入 | `否`；当前任务目录此前没有这份文件 |
| stage02 正式代码与配置对象 | `not_applicable` | 本轮只做 Pre-check，不进入正式编码；这里只预登记后续将涉及的对象范围 | `是`；`scripts/train.py` 与 `src/data/*` 可作为后续扩展参照，但不等于 stage02 主链已成立 |

## 5. 预期工程落点汇总

| 对象层 | 目录/文件 | 本轮为什么会受影响 |
|------|----------|------------------|
| 代码层 | src/models/unet.py、src/losses/seg_losses.py、src/metrics/object_metrics.py、src/engine/trainer.py、src/eval/run_eval.py、scripts/train.py、scripts/test.py、scripts/export_visuals.py、scripts/summarize_stage.py | 本轮不创建这些对象，但必须先把它们登记为后续 stage02 允许进入的唯一正式代码层 |
| 配置层 | configs/model/unet_v1.yaml、configs/train/unet_flow_v1.yaml、configs/eval/eval_proto_v1.yaml、configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml | 本轮不创建这些配置，但必须先确认 stage02 的正式配置链应该落在这里 |
| 运行资产层 | experiments/A1_UNet_GlaS_v1_seed3407/ | 本轮不产生 run 资产，但必须明确未来正式资产落点 |
| 报告层 | reports/stage_reports/unet_flow_stage_summary.md、reports/tables/unet_flow_stage_manifest.csv、reports/stage_reports/implementation_tracking/02_UNet流程验证/* | 本轮不新增 A 类正式报告，但必须提前登记 stage02 的结果和说明文落点 |
| guard 层 | `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/pre_check_extraction.md`、`b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/stage_gate_check.md`、`b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md`、`b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/20260706_02_unet_flow_pre_check_guard.md` | 本轮所有实际新增都只允许落在 stage02 的 Pre-check guard 目录 |
