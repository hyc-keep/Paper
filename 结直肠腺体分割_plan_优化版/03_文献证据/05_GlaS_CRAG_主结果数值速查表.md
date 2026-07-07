# GlaS / CRAG 主结果数值速查表

这份文档只做一件事：

> 把后续做实验对比、写结果分析时最常查的 `GlaS / CRAG` 主结果数字汇总到一处，避免每次反复打开多篇正式深提取稿。

---

## 1. 文档定位

### 1.1 这份文档负责什么

- 汇总高频会比较的方法主结果数字
- 标明每个数字来自哪篇正式稿、哪张表、哪一页
- 区分“可以直接横比”和“只能参考、不能硬比”的结果

### 1.2 这份文档不负责什么

- 不替代单篇正式深提取稿中的完整上下文
- 不补写论文里没有明确给出的数值
- 不把不同指标口径硬凑成一张统一排行榜

### 1.3 使用规则

1. 如果你要做 `GlaS / CRAG` 主结果表，优先看 `第 2 节`
2. 如果你要找语义分割口径的 `Dice / Jaccard`，看 `第 3 节`
3. 如果你看到的是不同数据拆分、不同任务或不同指标，先不要直接横比，去看 `第 4 节` 的说明

### 1.4 统一记法

- 本表把 `0.xxx` 统一换写成百分数 `xx.x%`
- `ObjDice` 表示 `object-level Dice`
- `ObjHaus` 表示 `object-level Hausdorff`
- 若原文只给 `Dice / Hausdorff`，则保留原文口径，不强行改写成对象级指标

### 1.5 对我们项目最重要的指标优先级

按你当前路线，后续最值得优先盯住的不是所有数字，而是下面这组：

1. `GlaS`：`F1 / ObjDice / ObjHaus`
2. `CRAG`：`F1 / ObjDice / ObjHaus`
3. 语义口径补充：`Dice / IoU(Jaccard)`

原因：

- 你当前主线是腺体任务，不是纯语义分割 benchmark
- `GlaS` 传统比较最稳的是对象级三指标
- `CRAG` 后续做主表时也更适合优先对齐 `F1 / ObjDice / ObjHaus`
- `Dice / IoU` 仍然有用，但更适合作为补充结果或和通用分割方法对话

---

## 2. 严格优先表：对象级协议下可直接优先比较的结果

说明：

- 这一节优先收录 `GlaS challenge` 三指标或 `CRAG` 任务内常用对象级三指标
- 这些数字最适合后续做腺体任务主表、结果讨论和基线定位

| 方法 | 数据集/拆分 | F1 | ObjDice / Dice | ObjHaus / Haus | 是否可直接放进我们的主结果表 | 对我们项目最有参考价值的指标 | 备注 | 出处 |
|------|-------------|----|----------------|----------------|------------------------------|------------------------------|------|------|
| `DCAN` | `GlaS Part A` | `91.16%` | `89.74%` | `45.42` | `是` | `边界分支最早期强锚点；GlaS 对象级三指标` | `CUMedVision2` 对应 challenge 主结果 | `03_DCAN.md -> challenge tables, p.6-p.8` |
| `DCAN` | `GlaS Part B` | `71.58%` | `78.10%` | `160.35` | `是` | `malignant/困难子集的老锚点` | `CUMedVision2` 对应 challenge 主结果 | `03_DCAN.md -> challenge tables, p.6-p.8` |
| `Deep Multichannel` | `GlaS Test A` | `89.30%` | `90.80%` | `44.13` | `是` | `任务内经典多分支参考，尤其看 ObjDice / Haus` | 多通道融合路线 | `08_Deep-Multichannel.md -> Table III-IV, p.10-p.11` |
| `Deep Multichannel` | `GlaS Test B` | `84.30%` | `83.30%` | `116.82` | `是` | `困难子集下的多通道经典参考` | 多通道融合路线 | `08_Deep-Multichannel.md -> Table III-IV, p.10-p.11` |
| `MILD-Net-RTS` | `GlaS A` | `91.40%` | `91.30%` | `41.54` | `是` | `你当前主线最稳的任务内强基线之一` | `RTS` 后处理版本 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `MILD-Net-RTS` | `GlaS B` | `84.40%` | `83.60%` | `105.89` | `是` | `GlaS 困难子集的主线强基线` | `RTS` 后处理版本 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `MILD-Net-RTS` | `CRAG` | `82.50%` | `87.50%` | `160.14` | `是` | `CRAG 的主线起始对照` | 主线强基线之一 | `04_MILD-Net.md -> Table 1/2/3, p.11-p.12` |
| `TA-Net` | `GlaS` | `90.50%` | `90.20%` | `50.80` | `有条件` | `topology 路线支撑价值高，但 GlaS 为 A/B 平均口径` | 文中为 `Test A/B` 平均口径 | `07_TA-Net.md -> p.6` |
| `TA-Net` | `CRAG` | `84.20%` | `89.30%` | `105.20` | `是` | `CRAG 上 topology 结构先验强锚点，尤其是 ObjHaus` | topology-aware 强参考 | `07_TA-Net.md -> p.6` |
| `DEA-Net` | `GlaS` | `89.30%` | `89.60%` | `60.80` | `是` | `近期任务内边界增强路线的直接对照` | 三项都强，近期任务内方法 | `12_DEA-Net.md -> Table 2, p.3-p.4` |
| `DEA-Net` | `CRAG` | `86.00%` | `89.90%` | `129.40` | `是` | `CRAG 上近期强对照，优先看 F1 / ObjDice` | `F1 / Dice` 最好，但 `Haus` 不是最好 | `12_DEA-Net.md -> Table 2, p.3-p.4` |
| `Prompted SAM-H` | `GlaS Part A` | `92.90%` | `92.10%` | `41.19` | `有条件` | `foundation model 路线是否值得单列对照` | prompted foundation model 路线 | `13_SAM-Grade-Prompt.md -> Table 1-2, p.4` |
| `Prompted SAM-H` | `GlaS Part B` | `84.10%` | `88.10%` | `74.30` | `有条件` | `作为高阶扩展路线参考，不必强制首批复现` | prompted foundation model 路线 | `13_SAM-Grade-Prompt.md -> Table 1-2, p.4` |
| `SDT` | `GlaS Part A` | `93.10%` | `91.90%` | `32.29` | `是` | `如果你要强调 topology / skeleton 表示，这行极有价值；尤其是 Haus` | skeleton-aware distance transform | `14_SkeletonAwareDT.md -> Table 1, p.8` |
| `SDT` | `GlaS Part B` | `86.60%` | `85.10%` | `82.40` | `是` | `困难子集上的 skeleton 表示强参考` | skeleton-aware distance transform | `14_SkeletonAwareDT.md -> Table 1, p.8` |
| `Ours (to be filled)` | `GlaS / CRAG` | `待填` | `待填` | `待填` | `待填` | `后续直接和任务内锚点比较差距` | 结果冻结后再按 `GlaS / CRAG` 正式拆分回填 | `06_我们项目的GlaS_CRAG对照主结果表模板.md` |

### 2.1 当前最适合直接拿来做主表参考的几组

- `GlaS challenge` 经典锚点：`DCAN / MILD-Net-RTS / SDT / Prompted SAM-H`
- `CRAG` 主线强参考：`MILD-Net-RTS / TA-Net / DEA-Net`
- 如果你要强调近期腺体任务路线：优先看 `TA-Net / DEA-Net / SDT`

### 2.2 用这张表时要注意

- `TA-Net` 的 `GlaS` 值是 `Test A/B 平均`，不能直接当成 `Part A` 或 `Part B`
- `DEA-Net` 的 `GlaS / CRAG` 是对象级三指标，但数值写法本身就是百分数
- `Prompted SAM-H` 很强，但它更适合写“foundation model 路线可行”，不应替代全部任务内专用模型的比较
- `Ours` 这一行只是速查占位；正式结果仍优先以 `06` 的主结果表模板持续回填，等最终冻结后再回写这里

### 2.3 我建议你后续主结果表最小先放哪些

如果你下一步要做自己的对比表，最小集合建议是：

- `GlaS`：`DCAN / MILD-Net-RTS / DEA-Net / SDT`
- `CRAG`：`MILD-Net-RTS / TA-Net / DEA-Net`

如果后面你想再加一条“高阶扩展路线”：

- 加 `Prompted SAM-H`

如果你想强调“经典多分支任务内方法也考虑过”：

- 加 `Deep Multichannel`

---

## 3. 补充表：语义分割口径结果

说明：

- 这一节保留对后续实验也有用、但指标口径不是 challenge 对象级三指标的结果
- 更适合写模块有效性、语义分割性能趋势、attention 是否有增益

| 方法 | 数据集 | Dice | Jaccard / IoU | 其他 | 是否建议放进我们的补充结果表 | 对我们项目最有参考价值的指标 | 备注 | 出处 |
|------|--------|------|---------------|------|----------------------------------|------------------------------|------|------|
| `SCAU-Net (SA+CA)` | `GlaS` | `90.63%` | `Jaccard 83.32%` | `RVD 0.0197` | `是` | `Dice / Jaccard`，用于 attention 模块补充对照 | 语义分割口径，不是对象级三指标 | `10_SCAU-Net.md -> 主结果表, p.6-p.7` |
| `SCAU-Net (SA+CA)` | `CRAG` | `91.00%` | `Jaccard 83.81%` | `RVD -0.0074` | `是` | `Dice / Jaccard`，用于 attention 模块补充对照 | 语义分割口径，不是对象级三指标 | `10_SCAU-Net.md -> 主结果表, p.6-p.7` |
| `MAC-Net` | `GlaS` | `81.00%` | `IoU 70.10%` | `Accuracy 80.1%` | `否` | `只看 zero-shot 泛化趋势，不看绝对数值` | `EBHI-Seg` 训练后 zero-shot 到 `GlaS`，只作泛化参考 | `01_MAC-Net.md -> Table 2-3, p.8-p.10` |

### 3.1 这一节怎么用

- 如果后面你的实验主表也只报 `Dice / IoU`，这张表很方便
- 但如果你要对齐 `GlaS challenge` 传统腺体文献，仍应优先回到 `第 2 节`

### 3.2 语义口径里最值得你盯的

- `SCAU-Net`：最值得看 `GlaS / CRAG` 上的 `Dice / Jaccard`
- `MAC-Net`：最值得看的是“跨数据泛化趋势”，不是绝对精度

---

## 4. 不建议直接横比，但值得保留的参考结果

说明：

- 这些论文有价值，但与当前主线的拆分、任务定义或指标口径不完全一致
- 可以写 related work、历史脉络或任务难度差异，别直接塞进主结果总表做一行对一行比较

| 方法 | 数据集/设置 | 结果 | 为什么不建议直接横比 | 出处 |
|------|-------------|------|----------------------|------|
| `Semantic Segmentation + TVS` | `早期 GlaS 版本 Test A` | `F1 68.0%, ObjDice 75.0%, Haus 103.49` | 早期数据总量口径为 `161/16` 版本，不是后续常用主线口径 | `02_Semantic-Segmentation-TVS.md -> Table 1, p.9-p.10` |
| `Semantic Segmentation + TVS` | `早期 GlaS 版本 Test B` | `F1 55.0%, ObjDice 61.0%, Haus 213.58` | 同上 | `02_Semantic-Segmentation-TVS.md -> Table 1, p.9-p.10` |
| `Automatic Mucous Glands` | `Warwick-QU benign subset` | `Dice 92.0%, object Dice 88.0%` | 只用 benign 子集，不是完整 `GlaS` 或 `CRAG` | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |
| `Automatic Mucous Glands` | `PATH-DT-MSU without open glands` | `Dice 78.0%, object Dice 77.0%` | 自建数据集，难度与定义不同 | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |
| `Automatic Mucous Glands` | `PATH-DT-MSU with open glands` | `Dice 77.0%, object Dice 70.0%` | 自建数据集，且 open glands 设置不同 | `11_Automatic-Mucous-Glands.md -> p.7-p.8` |

---

## 5. 后续实验时最实用的用法

### 5.1 如果你要定主结果表

- `GlaS` 优先从 `第 2 节` 选 `DCAN / MILD-Net-RTS / SDT / Prompted SAM-H`
- `CRAG` 优先从 `第 2 节` 选 `MILD-Net-RTS / TA-Net / DEA-Net`

### 5.2 如果你要写“为什么我们的模块合理”

- attention 路线：看 `SCAU-Net`
- topology / structure 路线：看 `TA-Net / SDT`
- boundary-enhanced 路线：看 `DEA-Net`

### 5.3 如果你只想快速查一个锚点数字

- `DCAN, GlaS Part A`：`F1 91.16 / ObjDice 89.74 / ObjHaus 45.42`
- `MILD-Net-RTS, CRAG`：`F1 82.5 / ObjDice 87.5 / ObjHaus 160.14`
- `TA-Net, CRAG`：`F1 84.2 / ObjDice 89.3 / ObjHaus 105.2`
- `DEA-Net, CRAG`：`F1 86.0 / ObjDice 89.9 / ObjHaus 129.4`
- `SDT, GlaS Part A`：`F1 93.1 / Dice 91.9 / Haus 32.29`

### 5.4 我建议你自己的实验最小必报指标

如果你后面想让结果表既稳又不乱，我建议最低限度报：

- `GlaS`：`F1 / ObjDice / ObjHaus`
- `CRAG`：`F1 / ObjDice / ObjHaus`
- 补充表：`Dice / IoU`

如果篇幅不够：

- 主表只保留 `F1 / ObjDice / ObjHaus`
- 把 `Dice / IoU` 放到补充实验或附录

如果后面你要突出边界/结构优势：

- 优先看 `ObjHaus`

如果后面你要突出实例识别能力：

- 优先看 `F1`

如果后面你要突出整体分割重叠质量：

- 优先看 `ObjDice`

---

## 6. 一句话版本

> 以后只要你想知道“某个腺体方法在 `GlaS / CRAG` 上大概是多少”，先来这份速查表；真要核对上下文、训练细节和公平比较条件，再回对应正式深提取稿。
