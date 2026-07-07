# 02_UNet流程验证 严格修补方案

## 1. 这份文档解决什么问题

这份文档只回答一个问题：

在严格遵守 `结直肠腺体分割_plan_优化版/01_实验执行/02_UNet流程验证/` 规划原文的前提下，当前 `crc_gland_segmentation_project` 到底还缺什么，应该怎么修补，修补到什么程度才可以诚实地宣布 `02_UNet流程验证` 真正通过并进入 `03_UNet稳定性`。

这份文档不是新的计划，也不是新的研究定标记录，而是对当前真实状态的严格收口说明。它的目标不是“帮当前状态找理由”，而是把真正还差的那一步说清楚，把后续动作变成可执行清单。

---

## 2. 先给结论

### 2.1 当前最重要的结论

当前 `02_UNet流程验证` 已经完成了以下几件重要事情：

1. 正式代码主链已经存在，包括 `UNet`、训练入口、评估入口、像素级/对象级/边界级指标、测试导出与可视化导出。
2. 正式参考资料已经具备，不缺会阻塞当前阶段的论文、评测口径和工程代码参考。
3. 本地 CPU 级联通检查已经成立，说明正式工程入口、数据读取、前向、loss、backward、optimizer.step 和最小评估资产链都能真实跑通。
4. 当前锁定范围内的 learning docs、runtime、code quality、Post-QC 等文档链已经基本形成闭环。

但是，在“严格按规划原文执行”的口径下，当前仍然不能无条件宣布 `02_UNet流程验证` 已经完全合规通过。

### 2.2 当前真正的阻断点

当前真正的阻断点不是文献，不是模型代码，不是指标实现，而是：

**当前主 run 的硬件执行口径与 02 阶段规划正文不完全一致。**

规划正文把正式训练写成了：

- `AMP on`
- 正式 `batch_size` 取“单卡稳定不溢出的最大值”
- 正式 run 前必须先做一次不入表的 `smoke check`

这套表述本质上是按“单 GPU 正式 run”写的，不是按“CPU 正式 run”写的。

而当前主实验目录 `experiments/A1_UNet_GlaS_v1_seed3407/` 中记录的是：

- `device: cpu`
- `amp_active: false`
- `smoke_check: false`

这说明当前这轮 run 可以证明“CPU 联通验证与最小正式资产链成立”，但不能在最严格的规划口径下直接等价为“正式 GPU A1 已成立”。

### 2.3 一句话裁决

当前最诚实的状态应当写成：

**02 阶段已经完成 CPU 级流程验证、最小正式资产闭环与说明文锁定范围收口，但如果要严格符合规划原文，仍需补一轮单 GPU + AMP 的正式 A1 run，并围绕这轮正式 run 重新完成身份收口和文档统一。**

---

## 3. 为什么当前不能直接算“严格通过”

### 3.1 规划原文的硬件语义

`02_UNet流程验证` 的规划原文里，正式训练协议不是中性描述，而是带有很强的 GPU 语义：

1. 训练协议固定为 `AMP on`。
2. 正式 `batch_size` 定义为“单卡稳定不溢出的最大值”。
3. `smoke check` 被单独定义为正式 run 前的最小排雷动作，而不是正式结果本身。

这意味着：

- CPU 可以用于前检、联通、最小 smoke、局部验证。
- 但真正承载“正式 A1 基线”身份的 run，应当是按单卡 GPU 路线执行的正式 run。

### 3.2 当前项目内文档自己也承认了边界

当前项目中的 `post_qc_guard.md` 已经非常诚实地写明：

- 当前结论只代表“本地 CPU 级联通检查与最小评估资产链成立”
- 当前结论“不扩写为 GPU 正式大规模训练结论”

这意味着项目内部最关键的门禁文档自己也没有把当前 CPU 结果定义为“正式 GPU A1 已成立”。既然门禁文档都没有这样写，那么严格审计时也不能越权把它解释成“已经完全通过”。

### 3.3 现在最危险的误判是什么

当前最危险的误判不是“代码没写好”，而是下面这几种叙事混淆：

1. 把 CPU 联通结果继续说成正式 A1。
2. 把“锁定范围内 learning docs 已 pass”误读成“02 全量正式对象已无条件 pass”。
3. 把“当前能进入下一步稳定性工作”误读成“当前已经严格满足规划原文”。
4. 把已有的正式资产链闭环，误读成“硬件执行口径也已经自动满足”。

这些误判一旦不改，后续即使补了 GPU run，也会留下严重的身份混乱：同一个 run 名字到底代表 CPU 前检结果，还是 GPU 正式结果，会变得说不清。

---

## 4. 当前哪些部分已经足够，不需要推倒重来

### 4.1 文献与参考资料部分已经足够

当前正式参考资料里已经具备：

- `UNet` 论文依据
- `GlaS` 任务与评测口径
- 代码映射清单
- 版本来源记录
- 参考资料终审结论

因此当前不需要回头重做研究定标，不需要重新补一整套参考资料主链。这个部分不是当前的主阻断项。

### 4.2 代码主链已经具备正式闭环能力

当前工程里已经有：

- `src/models/unet.py`
- `scripts/train.py`
- `src/engine/*`
- `src/eval/run_eval.py`
- `scripts/test.py`
- `scripts/export_visuals.py`
- `src/metrics/*`

这说明正式主链不是空壳，不存在“根本没实现”的问题。当前也不需要因为硬件口径问题去推翻模型、指标或测试代码。

### 4.3 当前 CPU 结果有价值，不能删除

当前 CPU 结果虽然不能直接充当严格口径下的正式 A1，但它依然有重要价值：

1. 它证明正式训练入口能真实跑通。
2. 它证明数据、模型、loss、optimizer 和评估链没有结构性断裂。
3. 它证明测试与可视化资产链已经可以落盘。
4. 它是后续 GPU run 前的重要前检证据。

因此当前 CPU 结果应该保留，不能删除，不能硬抹平，只能**重新定义身份**。

---

## 5. 严格符合规划时，真正必须修补的内容

### 5.1 第一类修补：身份修补

这是最重要的一类修补。

当前 `experiments/A1_UNet_GlaS_v1_seed3407/` 目录中的 run，不能继续承担“正式 A1”这个最终身份。因为这个目录里已经明确写死了：

- `device: cpu`
- `amp_active: false`

如果继续让它占用正式 A1 的身份，那么后续所有结论都会带着一个根本冲突：

- 规划要求正式 A1 走单 GPU + AMP
- 但目录里真实记录的却是 CPU + no active AMP

因此首先必须做的是：

**把当前 CPU run 从“正式 A1 身份”中剥离出来，降级为“CPU 联通/前检/最小验证证据”。**

这一步的重点不是删文件，而是修正“这个目录到底代表什么”。

### 5.2 第二类修补：执行修补

在身份修补之后，必须补做一轮真正符合规划的正式 A1。

这轮 run 必须满足以下条件：

1. 单 GPU 执行。
2. `AMP on`。
3. 正式 run 前先完成一次不入表的 GPU smoke check。
4. 不改变当前阶段已经冻结的实验定义。

也就是说，这不是“顺便重做一次实验”，而是“补齐规划原文里本来就要求存在、但当前还未严格成立的那一轮正式 run”。

### 5.3 第三类修补：资产修补

GPU 正式 run 补做之后，不能只产出一个新的 `best.ckpt` 就结束。必须重新形成完整正式资产链，至少包括：

- `config.yaml`
- `run_meta.yaml`
- `train_log.csv`
- `val_metrics.csv`
- `best.ckpt`
- `last.ckpt`
- `testA_metrics.csv`
- `testB_metrics.csv`
- `metric_crosscheck_note.md`
- `visuals/testA/*`
- `visuals/testB/*`
- `summaries/error_cases.md`
- `summaries/run_summary.md`

严格口径下，只有这些对象在同一轮正式 GPU 语义下互相一致，才可以认为“正式 A1 已成立”。

### 5.4 第四类修补：文档修补

当前还残留一些旧文档口径，这些必须修掉，否则后续仍会审计失败。

最典型的旧口径包括：

1. `crc_gland_segmentation_project/experiments/README.md` 仍在说当前没有正式实验目录。
2. `b_class_auxiliary/coding_guards/20260706_02_unet_flow_stage_lock/current_codebase_状态.md` 仍保留旧的 Pre-check 扫描现实，容易被误读成“当前事实”。
3. `implementation_status.md`、阶段入口 README 和“当前阶段为什么能pass以及下一步怎么看”这类入口文档，需要重新明确 CPU 证据与 GPU 正式 run 的职责边界。

---

## 6. 最稳妥的总体策略

### 6.1 不删除旧证据，只做身份降级

当前最正确的策略不是清理掉当前 CPU 证据，而是保留它、标注它、降级它。

这样做的好处是：

1. 审计链完整。
2. 可以证明项目并不是“没有任何真实运行”，而是“先完成了 CPU 级流程验证”。
3. 后续 GPU 正式 run 与当前 CPU run 的关系可以被清楚解释。

### 6.2 不让同一个正式身份同时代表两件事

最需要避免的是下面这种状态：

- 同一个 `A1_UNet_GlaS_v1_seed3407`
- 既代表 CPU 联通结果
- 又代表 GPU 正式结果

这会让：

- `run_meta.yaml`
- `run_summary.md`
- learning docs
- 阶段状态页
- 审计结论

全部失去单一语义。

因此必须坚持一个原则：

**一个正式 run 名，只能对应一种清晰、唯一、可审计的现实。**

### 6.3 推荐的最终身份布局

推荐把运行资产分成三类身份：

1. `smoke run`
   - 只负责最小排雷
   - 不承担正式结果身份

2. `CPU 联通/前检 run`
   - 只负责证明工程主链能跑
   - 不承担正式 A1 身份

3. `正式 GPU A1 run`
   - 承担 02 阶段最终准出主证据
   - 负责为进入 `03_UNet稳定性` 提供正式基线

---

## 7. 严格修补的执行顺序

下面这部分是整个文档最重要的可执行清单。

### 第 1 步：冻结当前叙事

在任何进一步动作之前，先停止继续使用下面这种叙事：

- “当前 CPU 主 run 已经正式通过 02”
- “当前已经严格满足规划，只差一点文案”

这两种说法都不够诚实，必须先停止。

### 第 2 步：给当前 CPU 结果明确身份

需要把当前 CPU 结果明确改写为：

- 历史 CPU 联通证据
- 历史前检/最小正式链验证证据
- 非严格口径下的流程验证结果

这一层要落实到以下入口文档中：

- `crc_gland_segmentation_project/experiments/README.md`
- `reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md`
- `reports/stage_reports/implementation_tracking/02_UNet流程验证/implementation_status.md`
- `reports/stage_reports/implementation_tracking/02_UNet流程验证/当前阶段为什么能pass以及下一步怎么看.md`

### 第 3 步：确认 GPU 环境并做不入表 smoke check

在正式 GPU run 之前，必须先完成一次不入表的 GPU smoke check。

这个 smoke check 的目标不是产出最终指标，而是确认：

1. 单 GPU 环境可用。
2. `cuda` 能被训练入口识别。
3. AMP 能正常启用。
4. dataloader 正常。
5. 前向正常。
6. loss 正常。
7. backward 正常。
8. optimizer.step 正常。
9. 显存不会在当前正式 `batch_size` 下立刻 OOM。

只有 smoke check 通过，才允许进入正式 GPU run。

### 第 4 步：执行单 GPU + AMP 的正式 A1

这一步是当前整个阶段最关键的一步。

必须严格保持冻结协议，不允许借机偷偷修改实验定义。

正式 run 时必须保持：

- `seed = 3407`
- `run_name = A1_UNet_GlaS_v1_seed3407`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `optimizer = AdamW`
- `lr = 1e-3`
- `weight_decay = 1e-4`
- `scheduler = ReduceLROnPlateau`
- `epoch_max = 120`
- `early_stopping = 20`
- `AMP on`
- `batch_size = 单卡稳定不 OOM 的最大正式值`

这一步不允许做下面这些事情：

- 改 seed
- 改模型结构
- 改损失定义
- 改 split
- 改 best selector
- 改 threshold 来源
- 在正式 run 过程中一边试多个 batch size 一边记入正式结果
- 使用 `TestA/TestB` 调阈值或选模型

### 第 5 步：完整导出正式评测与可视化资产

正式 GPU A1 结束后，必须立即完成完整导出，包括：

- `TestA60`
- `TestB20`
- 对应的 metrics CSV
- `metric_crosscheck_note.md`
- `visuals/testA/*`
- `visuals/testB/*`
- `summaries/error_cases.md`
- `summaries/run_summary.md`

这一步的重点不是“分数好不好看”，而是：

**正式训练、正式 checkpoint、正式测试、正式评估、正式可视化、正式总结，必须全部落在同一轮正式 GPU 语义下。**

### 第 6 步：重新回填 run 元数据与阶段入口

GPU 正式 run 完成后，需要重新回填：

- `run_meta.yaml`
- `run_summary.md`
- 阶段入口 README
- `implementation_status.md`
- “当前阶段为什么能pass以及下一步怎么看”
- 相关对象级说明文

这一轮回填的目标，是让所有入口页都能诚实回答下面三个问题：

1. 当前 CPU 结果是什么身份。
2. 当前正式 GPU A1 是哪一个目录。
3. 为什么现在才可以严格宣称 02 通过。

### 第 7 步：重新跑门禁与审计

GPU 正式 run 和文档收口完成后，需要重新进行：

- runtime 证据核对
- code quality 门禁
- learning docs 门禁
- Post-QC 结论核对
- 阶段最终审计

只有这一轮完整重审通过后，才可以把结论真正写成：

`02_UNet流程验证 已严格符合规划，可进入 03_UNet稳定性`

---

## 8. 文件级修补建议

这一部分把关键文件按“应该怎么处理”写清楚。

### 8.1 `crc_gland_segmentation_project/experiments/README.md`

这是当前最需要优先修补的文件之一。

当前它的问题是：它还停留在“没有正式实验目录”的旧现实里。

严格修补后，这个文件至少要说明：

1. `experiments/` 下当前有哪些 run 目录。
2. 哪些目录属于 `smoke`。
3. 哪些目录属于 `debug`、`backup`、`historical CPU precheck`。
4. 哪个目录才是当前正式 A1。
5. 在正式 GPU A1 建立前，不允许把 CPU 目录写成“正式主证据”。

### 8.2 `b_class_auxiliary/coding_guards/.../current_codebase_状态.md`

这份文件本质上是阶段锁定时刻的历史扫描结果。

正确做法不是粗暴抹掉它的历史内容，而是：

1. 保留它作为当时 Pre-check 现实的留痕。
2. 在显眼位置注明它只代表当时扫描时刻的现实。
3. 明确当前正式现实应以最新的阶段入口文档和实验目录为准。

这样既不会破坏审计历史，也不会让人误读它是当前事实。

### 8.3 `implementation_status.md`

这份文件是最核心的阶段状态页之一。

严格修补后，它应该明确拆开三层状态：

1. CPU 联通状态是否成立。
2. 当前正式 GPU A1 是否成立。
3. 当前是否满足严格放行条件。

在 GPU 正式 run 完成之前，这份文件不应继续给出容易被误解成“严格通过”的绝对性口径。

### 8.4 `当前阶段为什么能pass以及下一步怎么看.md`

这份文件不能再只写“为什么当前能 pass”，而必须同时解释：

1. 当前为什么在工程闭环意义上已经成立。
2. 当前为什么在严格规划意义上仍有一步没补。
3. 下一步必须补的是哪一轮 run、哪类资产、哪类说明文。

### 8.5 `experiments/A1_UNet_GlaS_v1_seed3407/run_meta.yaml`

这份文件目前最大的问题不是内容少，而是它的身份太敏感。

因为它明确记录了：

- `device: cpu`
- `amp_active: false`

因此在正式 GPU A1 建立前，这份文件不能继续被解释成“严格规划意义下的正式 run 元数据”。

更稳妥的处理方式是：

1. 保留它作为当前 CPU 结果的元数据。
2. 在入口文档中明确说明它的身份边界。
3. 等真正的 GPU 正式 A1 建立后，再让新的正式 `run_meta.yaml` 承担最终放行主证据身份。

### 8.6 `experiments/A1_UNet_GlaS_v1_seed3407/summaries/run_summary.md`

这份文件与 `run_meta.yaml` 的问题类似。

它应当被解释为：

- 当前 CPU 级联通和最小正式资产链的总结

而不是：

- 严格规划意义下最终正式 A1 总结

等 GPU 正式 run 完成后，正式 A1 的 `run_summary.md` 应承担最终准出说明责任。

---

## 9. GPU 正式 run 前的最小准备清单

在真正开跑前，建议先逐项确认以下内容。

### 9.1 环境准备

- GPU 可见
- CUDA 环境正常
- PyTorch 可以正确识别 GPU
- 训练入口支持 `--device cuda`
- AMP 路径可启用

### 9.2 配置准备

- `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml` 不变
- `configs/model/unet_v1.yaml` 不变
- `configs/train/unet_flow_v1.yaml` 不变
- `configs/eval/eval_proto_v1.yaml` 不变
- `configs/data/glas.yaml` 不变

### 9.3 语义准备

开跑前必须先统一一件事：

这轮 GPU run 不是“新方案”，不是“补试一个更好的分数”，而是“把 02 阶段原本规划要求存在的正式 A1 真正补齐”。

只有把这层语义讲清楚，后面的说明文和阶段状态页才不会再漂移。

---

## 10. GPU 正式 run 完成后必须核对什么

### 10.1 元数据核对

新的正式 `run_meta.yaml` 至少应满足：

- `device` 为 `cuda:*`
- `smoke_check = false`
- `amp` 对应正式开启语义
- `stage_pass = true`
- `protocol_error = false`
- `testA_sample_count = 60`
- `testB_sample_count = 20`
- `metric_crosscheck_result = pass`
- `next_action = enter_03_unet_stability`

### 10.2 训练资产核对

必须同时存在并能互相回链：

- `train_log.csv`
- `val_metrics.csv`
- `best.ckpt`
- `last.ckpt`
- `config.yaml`
- `run_meta.yaml`

### 10.3 测试与评估资产核对

必须同时存在并能互相解释：

- `testA_metrics.csv`
- `testB_metrics.csv`
- `metric_crosscheck_note.md`
- `visuals/testA/*`
- `visuals/testB/*`
- `summaries/error_cases.md`
- `summaries/run_summary.md`

### 10.4 说明文核对

需要确认：

1. 入口页和对象页说的是同一个世界。
2. 说明文没有再把 CPU 结果写成正式 A1。
3. 说明文能够准确区分 smoke、CPU 联通证据和正式 GPU A1。

---

## 11. 最终放行标准

下面这些条件必须同时成立，才可以在“严格符合规划”的口径下宣布 `02_UNet流程验证` 通过。

### 11.1 运行口径成立

- 正式 A1 为单 GPU 执行
- 正式训练协议与 `AMP on` 一致
- 正式 run 前完成 GPU smoke check
- 正式 run 不再被 CPU 目录替代

### 11.2 资产链成立

- `train`
- `val`
- `test`
- `eval`
- `visual`
- `record`

六类资产都在同一轮正式 GPU 语义下互相一致。

### 11.3 文档链成立

- 实验目录 README 口径正确
- 阶段入口 README 口径正确
- `implementation_status.md` 口径正确
- `当前阶段为什么能pass以及下一步怎么看.md` 口径正确
- 对象级说明文与正式资产没有世界观冲突

### 11.4 阶段结论成立

最终必须能够诚实写出下面这句话，且不自相矛盾：

**`02_UNet流程验证` 的正式 A1 基线已按规划完成单 GPU + AMP 正式运行，正式训练、验证、测试、评估、可视化与记录资产链完整一致，因此允许进入 `03_UNet稳定性`。**

---

## 12. 当前最推荐的执行方案

如果只给一个最推荐方案，那么就是下面这套：

1. 保留当前 CPU 结果，不删除。
2. 明确把当前 CPU 结果降级为“历史 CPU 联通/前检证据”。
3. 修正实验目录入口文档与阶段入口文档，不再让当前 CPU 结果冒充正式 A1。
4. 在 GPU 上做一次不入表 smoke check。
5. 按冻结协议执行正式 `A1_UNet_GlaS_v1_seed3407` 单 GPU + AMP run。
6. 完整导出 TestA60、TestB20、crosscheck、visuals 和 error cases。
7. 回填正式 `run_meta.yaml`、`run_summary.md`、阶段状态页与对象说明文。
8. 重新跑门禁并重新做阶段审计。
9. 只有当新一轮正式 GPU A1 与文档世界观完全一致时，才正式放行进入 `03_UNet稳定性`。

---

## 13. 最后一句话

当前 02 阶段真正缺的，不是更多解释，不是更多文案，也不是重写模型和指标，而是：

**一轮符合规划原文的单 GPU + AMP 正式 A1，以及围绕这轮正式 A1 完成的身份收口、资产收口和文档收口。**

只要这一步补齐，`02_UNet流程验证` 就能从“工程上基本成立”升级为“严格规划意义下正式通过”。
