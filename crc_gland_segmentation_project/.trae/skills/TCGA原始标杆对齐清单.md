# TCGA原始标杆对齐清单

> **正式角色**: `implementation_tracking` 学习型说明文的原始标杆对照规程
> **调用顺序**: 先看 `00_技能体系导航.md`、`实验执行文档编写规范.md`，再读本清单，最后再看 `示例_学习型说明文_融合版.md`
> **工程落点**: 对标结论必须回填到 `b_class_auxiliary/coding_guards/[任务目录]/YYYYMMDD_[任务]_post_qc_guard.md` 的 `## 4.3 学习型说明文人工审稿回填`

---

## 正式角色

- 当前清单文件: `TCGA原始标杆对齐清单.md`
- 这份清单负责锁定真正的 TCGA 原始对标对象
- 这份清单负责回答“你当前说明文到底对齐了谁”
- 这份清单只服务学习型说明文,不服务正式协议正文

## 当前边界

- 不替代 `crc_gland_segmentation_project/.trae/skills/实验执行文档编写规范.md`
- 不替代 `crc_gland_segmentation_project/.trae/skills/示例_学习型说明文_融合版.md`
- 不替代 `crc_gland_segmentation_project/.trae/skills/学习型说明文人工审稿清单.md`
- 不替代 `b_class_auxiliary/tools/check_learning_docs.py`

## 状态口径边界

- `Stage Gate`: `allow / blocked`
- `Diagnostics / Post-QC`: `pass / partial / fail / not_applicable`
- `implementation_tracking` 阅读入口: `not_started / blocked / partial / pass`

本清单自己的判断结论，统一回填到 `Diagnostics / Post-QC` 这一层，而不是直接改写阶段总体状态。

---

## 1. 当前唯一有效的原始标杆

后续凡是声称“已经对齐 TCGA 风格”的学习型说明文,默认都要回到下面这些真实文档:

- 标杆工程根目录: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project`
- 数据链样例: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/01_dataset_pipeline/01_copy_raw_dataset_学习说明.md`
- 训练链样例: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/02_training_workflow/01_train_unet_学习说明.md`
- 核心模块样例: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/src/tcga_unet/layer_01_core/data_学习说明.md`
- 损失函数样例: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/src/tcga_unet/layer_01_core/losses_学习说明.md`
- 工作流入口样例: `D:/12_Medical_Image_Segmentation/dl_projects_learning/02_medical_image_segmentation/01_tcga_brain_mri_segmentation/learning/01_tcga_unet_project/02_training_workflow/README.md`

## 2. 这份原始标杆真正强在哪里

后续说明文至少同时命中下面三层:

| 层次 | TCGA 原始标杆的典型信号 | 我们后续必须继承什么 |
|------|------------------------|----------------------|
| 概念层 | “这个文件到底在整个项目里干什么” | 先把定位讲明白，不让新手一上来就迷路 |
| 实现层 | “源码顺序、函数职责、张量链路” | 让读者能顺着文档回到代码 |
| 工程层 | “为什么这样设计，而不是另一种写法” | 让读者知道取舍，不只是背结果 |

TCGA 原始标杆最稳定的阅读顺序是:

- 先讲“这个文件在做什么”
- 再讲“为什么要这样设计”
- 再讲“源码主流程怎么走”
- 再讲“最容易误解的地方”
- 最后讲“学完后你应该具备什么能力”或“下一步建议联读谁”

Markdown 里的“视觉可读性”至少要靠下面这些动作体现:

- 每段先给一句结论，再补解释，避免整页长段落
- 多用短段落、表格、编号流程和对照句，减少大段抽象堆砌
- 一级问题尽量单独成节，让读者滚动时能一眼看到“我现在在读哪一块”
- 关键警告、误区、边界要单独成行，不要藏在长段正文中

---

## 3. 后续写作时最低要对照什么

人工终审时,至少逐项对照下面 6 个维度:

| 维度 | 最低通过信号 | 常见假对齐 |
|------|-------------|-----------|
| 定位速度 | 新手 30 秒内能说出文件职责 | 开头只有空泛背景 |
| 口语解释 | 真正出现“你可以把它理解成/换句话说/你可能会问”并且后面有展开 | 只在开头口语化一句 |
| 流程链路 | 有源码顺序、输入输出、执行链说明 | 只列函数名，没有顺序 |
| 设计取舍 | 明确讲为什么这么写、为什么不用别的方案 | 只报最终结论 |
| 误区预防 | 明确挡住新手最容易犯的错 | 不写“为什么不能这样做” |
| 收口引导 | 有联读建议、自检任务或学完能力说明 | 文档末尾突然结束 |

---

## 4. 写前最低动作

只要本轮准备正式写 `implementation_tracking` 学习型说明文,最低动作固定为:

1. 先读 `实验执行文档编写规范.md`
2. 再读本清单，锁定原始 TCGA 对标对象
3. 至少抽读本清单 §1 中列出的 2 份真实 TCGA 学习说明文
4. 再读 `示例_学习型说明文_融合版.md`
5. 再读 `学习型说明文人工审稿清单.md`，确认本轮最终会被按什么问题清单终审
6. 动笔前先明确: 本轮要优先对齐的是“解释力度”“阅读顺序”“误区预防”还是“视觉层次”

## 5. 人工审稿时必须留下的物理证据

后续在 `Post-QC Guard` 里回填时,不能只写“已经对齐 TCGA 风格”。

最低要留下下面三类物理证据:

- 你本轮实际对照了哪两份 TCGA 原始文档
- 你当前文档里哪几个章节或句子，体现了这种对齐
- 还差哪一类信号没有补齐，例如“有流程，没有取舍”“有口语化，没有联读收口”

回填时至少要写:

- 对照的 TCGA 原始文档路径
- 当前说明文中最能说明“已经讲透”的章节标题
- 至少 1 处具体表述或 1 组真实路径/字段/数值证据
- 并在 `crc_gland_segmentation_project/.trae/skills/学习型说明文人工审稿清单.md` 的问题框架下说明：本轮到底在哪几项达标、哪几项仍有缺口

---

## 6. 红线

- 不要把“对照了融合示范稿”误判成“已经对照了 TCGA 原始标杆”
- 不要把“篇幅更长”误判成“更像 TCGA”
- 不要把“加了很多审计字段”误判成“新手更容易懂”
- 如果人工审稿没有显式写出本轮对照了哪些 TCGA 原始文档，就不能声称这轮已经完成 TCGA 原始标杆对齐

---

## 7. 验收与回退

### 7.1 通过标准

- 至少能明确回指 2 份真实 TCGA 原始学习说明文
- 至少能说清本轮文档在哪 6 个维度上达标、哪些维度仍然欠缺
- `Post-QC Guard` 已写入本清单路径、对照对象和关键证据

### 7.2 回退条件

- 如果人工审稿里没有写明 TCGA 原始对照对象，直接回退
- 如果只写“接近示范稿”，但没有真实原始标杆对照证据，直接回退
- 如果文档仍然是长段抽象叙述，缺少结论先行、对比表或误区拦截，不能判 `pass`

---

## 8. 一句话版本

> 这份清单负责把“像 TCGA 一样详细”从一句模糊要求变成可回查、可审稿、可回填的正式规程: 后续必须先锁定真实 TCGA 原始文档，再判断当前说明文是否同时达到小白友好、论文严谨和可视化引导这三条线。
