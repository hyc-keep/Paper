# 02_UNet流程验证 执行检查清单

## 1. 文档用途

这份文档是 `02_UNet流程验证_严格修补方案.md` 的执行版 checklist。

如果前一份文档回答的是“为什么当前还不能算严格通过、原则上应该怎么修”，那么这份文档回答的是：

**从现在开始，具体要先做什么、再做什么、每一步检查什么、哪些文件要改、改到什么程度才能进入下一步。**

这份文档的目标不是做理论解释，而是把后续工作拆成一项一项可执行动作，便于按顺序推进，也便于后续审计时逐项回查。

---

## 2. 总体执行原则

开始执行前，先统一下面 6 条原则。

### 2.1 原则一：不删旧证据

当前 CPU run、旧阶段文档、旧入口页都不能因为“不够严格”就直接删除。

严格审计更看重：

1. 保留历史证据
2. 正确标注身份
3. 明确说明哪些是旧口径、哪些是当前正式口径

而不是把不舒服的证据清掉。

### 2.2 原则二：先修身份，再跑 GPU

不要一边保持“当前 CPU 主 run 已正式通过”的旧叙事，一边又直接启动 GPU 正式 run。

先修身份的原因很简单：

- 否则后续会出现同一个正式 run 名同时代表 CPU 与 GPU 两种现实
- 后面的 `run_meta.yaml`、`run_summary.md`、README、状态页都会混乱

### 2.3 原则三：GPU run 不是新实验

后续要补的 GPU run，不是“开一个新方案试试看”，也不是“为了拿更高分顺便重跑”。

它的唯一职责是：

**把规划原文已经冻结、但当前尚未严格成立的正式 A1 真正补齐。**

### 2.4 原则四：不改冻结协议

GPU 正式 run 期间，不允许顺手修改实验定义。以下内容应保持冻结：

- `seed = 3407`
- `model = unet_v1`
- `optimizer = AdamW`
- `lr = 1e-3`
- `weight_decay = 1e-4`
- `scheduler = ReduceLROnPlateau`
- `epoch_max = 120`
- `early_stopping = 20`
- `best_selector = val_objdice_max`
- `threshold_source = val17`
- `eval_proto_version = eval_proto_v1`
- `AMP on`

### 2.5 原则五：先 smoke，再正式 run

GPU 正式 run 前，必须先做不入表的 GPU smoke check。

如果 smoke 都没跑，或者 smoke 没确认 AMP / backward / optimizer.step / 显存稳定性，就直接进入正式 run，这在严格审计里是不合格的。

### 2.6 原则六：所有入口文档必须说同一个世界

最终必须确保：

- 实验目录 README
- 阶段入口 README
- `implementation_status.md`
- `当前阶段为什么能pass以及下一步怎么看.md`
- 对象级说明文
- `run_meta.yaml`
- `run_summary.md`

都在描述同一个现实，不能一部分还停留在“CPU 已正式通过”，另一部分已经切到“GPU 正式 A1 已成立”。

---

## 3. 阶段 0：开始前的裁决

在真正改文件和运行之前，先做一次明确裁决。

### 3.1 本轮裁决结论

当前应当先接受下面这条结论：

**当前 CPU 结果保留，但不再承担严格规划意义下的正式 A1 身份。**

这句话如果不先统一，后面整个修补过程都会变形。

### 3.2 本轮禁止事项

在这条结论统一之前，先不要做下面这些事：

1. 不要继续写“当前 A1 已严格通过 02”。
2. 不要把现有 CPU 目录继续当最终正式 run 主证据。
3. 不要先开 GPU 正式 run 再回头解释当前 CPU 目录是什么。
4. 不要先重写大批 learning docs 而不先定 run 身份。

### 3.3 本轮通过标准

只有当团队内语义统一成下面这样，才可以进入下一阶段：

- 当前 CPU 结果是历史 CPU 联通/前检证据
- 规划要求的正式 A1 还需要单 GPU + AMP 补齐

---

## 4. 阶段 1：先修文档口径与 run 身份

这一阶段的目标，不是立刻让 `02` 通过，而是先把“当前谁是什么身份”说清楚。

### 4.1 必须优先处理的文件

优先处理下面这些文件：

1. `crc_gland_segmentation_project/experiments/README.md`
2. `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md`
3. `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/implementation_status.md`
4. `crc_gland_segmentation_project/reports/stage_reports/implementation_tracking/02_UNet流程验证/当前阶段为什么能pass以及下一步怎么看.md`

### 4.2 `experiments/README.md` 应该改成什么

这份文件至少需要明确写出：

1. `experiments/` 当前已有的目录分类
2. 哪些目录属于 `smoke`
3. 哪些目录属于 `debug / backup / history`
4. 当前 CPU 目录属于“历史 CPU 联通/前检证据”
5. 当前尚未补齐严格规划意义下的正式 GPU A1 时，不能把 CPU 目录写成最终正式主证据

### 4.3 阶段入口 README 应该改成什么

阶段入口 README 至少需要补清楚：

1. 当前代码闭环为什么已经成立
2. 当前严格规划为何仍未完全成立
3. 当前 CPU 结果与后续 GPU 正式 A1 的关系
4. 进入下一步之前必须补哪一轮 run

### 4.4 `implementation_status.md` 应该改成什么

建议把状态拆成三层，而不是继续只给一个看似完整的 `pass`：

1. `工程闭环状态`
2. `严格规划状态`
3. `下一步准入条件`

推荐的写法是：

- 工程闭环：`pass`
- 严格规划放行：`not_yet_pass` 或 `conditional`
- 下一步：`补单GPU+AMP正式A1`

### 4.5 `当前阶段为什么能pass以及下一步怎么看.md` 应该改成什么

这份文件应改成“双层结论”：

1. 为什么当前在工程与证据链意义上已经非常接近通过
2. 为什么在严格规划意义上仍差一轮正式 GPU A1

### 4.6 这一阶段的通过标准

只有当上面这些入口文件都能诚实写出“CPU 结果只是前检/联通证据，正式 GPU A1 尚待补齐”时，才允许进入 GPU 准备阶段。

---

## 5. 阶段 2：GPU 正式 run 前的技术准备

这一阶段不追求产出最终指标，只追求“跑正式 GPU A1 前没有明显技术雷”。

### 5.1 环境检查

逐项确认：

1. GPU 可见
2. CUDA 可用
3. PyTorch 能正确识别 GPU
4. 训练入口可接收并使用 `cuda`
5. AMP 可正常启用

### 5.2 配置检查

确认这些配置仍是当前冻结版本：

1. `configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml`
2. `configs/model/unet_v1.yaml`
3. `configs/train/unet_flow_v1.yaml`
4. `configs/eval/eval_proto_v1.yaml`
5. `configs/data/glas.yaml`

### 5.3 数据与 split 检查

确认以下对象不发生漂移：

1. `splits/glas/glas_train68.csv`
2. `splits/glas/glas_val17.csv`
3. `splits/glas/glas_testA60.csv`
4. `splits/glas/glas_testB20.csv`

### 5.4 正式 run 名义检查

在严格规划下，正式 run 名义应继续使用冻结的正式名称：

- `A1_UNet_GlaS_v1_seed3407`

开始 GPU 正式 run 前，必须先明确：

- 当前 CPU 目录如何保留
- 之后哪个目录承担正式 GPU A1 的最终身份

### 5.5 本阶段通过标准

只有当环境、配置、split 和 run 身份安排都已经明确，才可以进入 GPU smoke check。

---

## 6. 阶段 3：执行不入表 GPU smoke check

这一步必须做，而且不能把它和正式 run 混写。

### 6.1 smoke check 的目标

GPU smoke check 的目标不是拿指标，而是确认下面这些硬条件：

1. dataloader 正常
2. model forward 正常
3. loss 正常
4. backward 正常
5. optimizer.step 正常
6. GPU 显存不立刻 OOM
7. AMP 路径正常
8. 训练入口和评估入口都能在 GPU 语义下工作

### 6.2 smoke check 禁止事项

1. 不把 smoke 结果写成正式 A1 结果
2. 不把 smoke 目录当成正式主目录
3. 不在 smoke 阶段修改正式实验定义
4. 不在 smoke 阶段使用 `TestA/TestB` 做模型选择

### 6.3 smoke check 通过标准

只要以下条件全部满足，就算通过：

1. 无 OOM
2. forward / backward / optimizer.step 正常
3. AMP 确认可用
4. 日志与输出路径正常
5. 当前选择的正式 batch size 可稳定支撑进入正式 run

### 6.4 smoke check 失败时怎么办

如果 smoke 失败，不要直接进入正式 run。

应该按下面顺序处理：

1. 先看是不是环境问题
2. 再看是不是设备选择问题
3. 再看是不是 batch size 过大
4. 再看是不是 AMP 路径问题
5. 修完后重新做 smoke check

只有 smoke 通过后，才能进入正式 GPU A1。

---

## 7. 阶段 4：执行正式 GPU A1

这是整个清单里最关键的一步。

### 7.1 正式 run 必须满足的条件

正式 A1 运行时必须同时满足：

1. 单 GPU
2. `AMP on`
3. 冻结 seed
4. 冻结训练协议
5. 冻结模型结构
6. 冻结评估协议
7. 冻结 best selector
8. 冻结 threshold 来源

### 7.2 正式 run 中禁止做的事

1. 不改 `seed`
2. 不改模型结构
3. 不改 loss
4. 不改 eval 协议
5. 不改 split
6. 不把 `TestA/TestB` 当调参工具
7. 不在正式 run 中边试多个 batch size 边把结果记入正式资产
8. 不把中途 debug 结果混进正式目录

### 7.3 正式 run 期间要盯的关键信号

建议盯以下信号：

1. 训练是否稳定推进
2. 验证是否按 epoch 正常执行
3. scheduler 是否正常响应
4. checkpoint 是否正常保存
5. 日志是否连续且语义一致
6. 是否出现协议级异常

### 7.4 正式 run 完成的最小判据

正式 run 完成后，至少要看到：

1. `train_log.csv`
2. `val_metrics.csv`
3. `best.ckpt`
4. `last.ckpt`
5. `config.yaml`
6. `run_meta.yaml`
7. `summaries/run_summary.md`

如果这些对象都没有在同一轮正式 GPU 语义下稳定落盘，就还不能进入下一阶段。

---

## 8. 阶段 5：导出正式测试、评估与可视化资产

GPU 正式训练结束后，必须马上完成评测资产链补齐。

### 8.1 必导出的正式对象

必须导出：

1. `testA_metrics.csv`
2. `testB_metrics.csv`
3. `metric_crosscheck_note.md`
4. `visuals/testA/*`
5. `visuals/testB/*`
6. `summaries/error_cases.md`
7. `summaries/run_summary.md`

### 8.2 这一阶段的核对重点

核对重点不是“数值是否漂亮”，而是：

1. `TestA` 的样本数是否为 60
2. `TestB` 的样本数是否为 20
3. metrics CSV 是否包含 sample 行与 aggregate 行
4. crosscheck 是否通过
5. visuals 是否真的来自正式 best checkpoint
6. `error_cases.md` 是否能回指到真实 overlay

### 8.3 这一阶段常见错误

1. 只导出 aggregate，不保留 sample 行
2. 指标表与 `run_meta.yaml` 数值对不上
3. visuals 是旧 run 的，不是当前正式 GPU run 的
4. `error_cases.md` 路径回指不到真实文件

### 8.4 本阶段通过标准

只有当测试、评估、可视化与 summary 全部指向同一轮正式 GPU A1 时，本阶段才通过。

---

## 9. 阶段 6：回填正式元数据与状态页

这一步的目标是：让所有入口页都切换到最新正式现实。

### 9.1 必须回填的核心文件

1. `experiments/.../run_meta.yaml`
2. `experiments/.../summaries/run_summary.md`
3. `crc_gland_segmentation_project/experiments/README.md`
4. `reports/stage_reports/implementation_tracking/02_UNet流程验证/README.md`
5. `reports/stage_reports/implementation_tracking/02_UNet流程验证/implementation_status.md`
6. `reports/stage_reports/implementation_tracking/02_UNet流程验证/当前阶段为什么能pass以及下一步怎么看.md`

### 9.2 `run_meta.yaml` 需要重点确认什么

建议逐项核对：

1. `device` 已是 `cuda:*`
2. `smoke_check = false`
3. `amp` 与正式协议一致
4. `stage_pass = true`
5. `protocol_error = false`
6. `testA_sample_count = 60`
7. `testB_sample_count = 20`
8. `metric_crosscheck_result = pass`
9. `next_action = enter_03_unet_stability`

### 9.3 `run_summary.md` 需要重点确认什么

这份文件应明确写出：

1. 当前 run 是正式 GPU A1
2. 当前 run 不是 smoke
3. 当前 run 不是 CPU 联通 run
4. 当前 run 的测试与可视化资产链已补齐
5. 当前 run 的 handoff 已经具备进入 `03` 的资格

### 9.4 阶段入口页需要重点确认什么

阶段入口页必须能用最直接的语言说清：

1. 历史 CPU run 是什么
2. 当前正式 GPU A1 是什么
3. 为什么现在才是严格意义下的通过

### 9.5 本阶段通过标准

只要还有任意一个入口文件继续用旧世界观写法，这一阶段就不算通过。

---

## 10. 阶段 7：learning docs 与对象说明文同步

当前 learning docs 锁定范围已经基本成立，但 GPU 正式 A1 补完后，需要再做一次同步核对。

### 10.1 优先核对哪些说明文

优先核对：

1. 正式 run 对应的对象级说明文
2. `run_meta.yaml.md`
3. `run_summary.md` 对应说明文
4. `train_log.csv.md`
5. `val_metrics.csv.md`
6. `testA_metrics.csv.md`
7. `testB_metrics.csv.md`
8. `metric_crosscheck_note.md`
9. `error_cases.md`

### 10.2 核对什么

重点核对：

1. 当前说明文是否仍把 CPU run 写成正式 A1
2. 当前说明文是否已切换到 GPU 正式 run 语义
3. 当前说明文中的关键字段、关键数值、关键路径是否回指真实对象
4. 说明文是否还能诚实区分 smoke、CPU 前检和正式 GPU A1

### 10.3 本阶段通过标准

对象说明文必须和正式资产保持同一个现实，不能出现“资产已经换了，说明文还在解释旧 CPU 世界”的情况。

---

## 11. 阶段 8：最终复审

这一阶段不再新增资产，只做最终裁决。

### 11.1 复审时必须同时满足的四类条件

#### 1. 运行条件

- 正式 A1 为单 GPU
- AMP 已按规划启用
- smoke 与正式 run 已分离

#### 2. 资产条件

- train / val / test / eval / visual / record 六链完整
- 所有正式资产在同一轮 GPU 语义下成立

#### 3. 文档条件

- README 正确
- 状态页正确
- 说明文正确
- 无旧世界观残留

#### 4. 结论条件

- 可以诚实写出“已严格符合 02 规划”
- 可以诚实写出“允许进入 03_UNet稳定性”

### 11.2 复审失败时怎么处理

如果最终复审失败，不要急着重跑。

先判断失败是哪一类：

1. 运行失败
2. 资产不一致
3. 文档不一致
4. 阶段结论口径不一致

然后只修这一类问题，不要把全部工作重新推翻。

### 11.3 复审通过时允许写出的最终结论

只有当上面所有条件都成立时，才允许写出下面这句最终结论：

**`02_UNet流程验证` 已按规划完成正式单 GPU + AMP 的 A1 基线运行，正式训练、验证、测试、评估、可视化与记录资产链完整一致，文档口径与真实资产一致，因此允许进入 `03_UNet稳定性`。**

---

## 12. 最终建议的执行顺序

如果你只想看最短的执行路径，就按下面顺序推进：

1. 先修入口文档，明确当前 CPU run 只是历史联通/前检证据。
2. 确认 GPU 环境、配置、split 和正式 run 身份安排。
3. 先做不入表 GPU smoke check。
4. 通过后执行正式单 GPU + AMP A1。
5. 导出完整 TestA60、TestB20、crosscheck、visuals、error_cases。
6. 回填正式 `run_meta.yaml`、`run_summary.md` 和阶段入口页。
7. 同步核对 learning docs 与对象说明文。
8. 做最终复审。
9. 复审通过后再正式宣布 `02` 通过并进入 `03`。

---

## 13. 一句话收口

这份执行清单真正要你做的事情只有一句话：

**先把当前 CPU 结果的身份说清，再补一轮符合规划的正式 GPU A1，然后把所有资产、状态页和说明文统一到这轮正式 A1 上。**
