# GitHub 本地与服务器同步详细流程

## 1. 这份文档解决什么问题

这份文档专门解决下面这几个问题：

1. 现在本地工程已经存在，怎样先安全上传到 GitHub。
2. 后面租到 GPU 服务器后，怎样把服务器接进同一个仓库。
3. 本地和服务器后续怎样同步、合并、避免覆盖。
4. 切到服务器打开新窗口后，没有历史记录时，怎样继续当前任务。

这份文档的目标不是解释 Git 原理，而是让你可以按顺序照着做。

---

## 2. 当前推荐架构

当前最推荐的工作流只有一条主线：

```text
本地 Paper 工程
    ↓ push
GitHub 私有仓库
    ↓ clone / pull
GPU 服务器工程
```

后续同步原则如下：

```text
本地改动 -> commit -> push -> 服务器 pull
服务器改动 -> commit -> push -> 本地 pull
```

不要采用下面这种方式：

- 本地改一份
- 服务器改一份
- 最后手动复制文件覆盖

这会非常容易把：

- 代码版本
- 阶段文档
- 运行结果
- 状态页

全部搞乱。

---

## 3. 你当前的真实情况

当前你已经具备：

- 本地工程目录：`d:\12_Medical_Image_Segmentation\Paper`
- 已创建 GitHub 仓库：`https://github.com/hyc-keep/Paper.git`
- 根目录下已有多份项目说明文档，可以作为后续切换窗口时的接力入口
- GitHub 首次基线已经 push 成功
- 当前 `main` 已与 `origin/main` 建立 tracking

当前最推荐的动作顺序是：

1. 服务器基于当前 GitHub 基线 clone
2. 服务器读取接力文档并准备 GPU 环境
3. GPU 执行阶段以服务器为主线
4. 文本类关键资产继续通过 GitHub 同步
5. 大结果和大缓存不要重新纳入 Git

### 3.1 当前上传的内容够不够

结论直接说：

**够作为服务器接力的正式基线，但不等于项目所有大资产都已经上传。**

当前已经足够上传并且已经适合上传的是：

- 代码
- 配置
- 阶段文档
- 接力文档
- 关键实验元数据
- 关键状态页

当前故意不上传，而且后面也不应该指望 GitHub 自动同步的是：

- 数据集
- checkpoint
- 大量预测结果
- 大量可视化图片
- 大型中间缓存
- 生成型报告大资产

也就是说：

**GitHub 现在承载的是“可接力的正式文本与代码基线”，不是“整个服务器磁盘镜像”。**

---

## 4. 第一次上传前必须先知道的事

### 4.1 第一次上传的本质

第一次上传不是“随便传一份代码上去”，而是：

**把你现在这份本地工程固化成后续服务器工作的正式起点。**

所以第一次上传前，一定要先做好 `.gitignore`，否则很可能把下面这些不该进仓库的内容一起传上去：

- 数据集
- checkpoint
- 大量结果图片
- 本地环境目录
- 临时日志

### 4.2 当前应该进 Git 的内容

建议进 Git 的内容：

- `crc_gland_segmentation_project/src/`
- `crc_gland_segmentation_project/scripts/`
- `crc_gland_segmentation_project/configs/`
- `crc_gland_segmentation_project/reports/stage_reports/`
- `crc_gland_segmentation_project/b_class_auxiliary/`
- `Paper/*.md`
- 关键小型结果文件，例如：
  - `run_meta.yaml`
  - `summaries/run_summary.md`
  - `testA_metrics.csv`
  - `testB_metrics.csv`
  - `metric_crosscheck_note.md`
  - `error_cases.md`

### 4.3 当前不建议进 Git 的内容

不建议进 Git 的内容：

- `datasets/`
- `*.ckpt`
- `visuals/`
- `predictions/`
- 大量 `png / bmp` 结果图
- 本地环境目录
- 临时日志

---

## 5. 第一次本地上传 GitHub 的完整步骤

以下步骤默认你在：

`d:\12_Medical_Image_Segmentation\Paper`

目录下执行。

### 第 1 步：确认 GitHub 仓库是 Private

优先建议你把仓库设为私有仓库。

原因：

1. 当前项目还处于实验阶段
2. 仓库里会包含很多阶段文档与过程资产
3. 后续可能还会出现不适合公开的大量实验细节

### 第 2 步：先写 `.gitignore`

先不要着急执行 `git add .`。

先把 `.gitignore` 放好，确保不该进入仓库的内容已经被排除。

当前项目建议直接使用根目录下的：

- `Paper/.gitignore`

### 第 3 步：初始化本地 Git 仓库

如果当前 `Paper` 根目录还没有初始化 Git，就执行：

```bash
git init
git branch -M main
```

### 第 4 步：先看状态，不要直接提交

执行：

```bash
git status
```

这一步的目标是确认：

1. 没有把数据集加进去
2. 没有把 checkpoint 加进去
3. 没有把大量结果图片加进去
4. 保留下来的都是你真正要版本管理的文件

### 第 5 步：加入文件

确认没问题后执行：

```bash
git add .
git status
```

这里再次看一遍 `git status`。

如果你发现：

- 有 `datasets/`
- 有 `*.ckpt`
- 有大量 `visuals/` 图片

说明 `.gitignore` 需要先修正，再继续。

### 第 6 步：第一次提交

确认无误后执行：

```bash
git commit -m "init: import local baseline before server execution"
```

### 第 7 步：绑定 GitHub 远端

你当前已经创建的仓库地址是：

```text
https://github.com/hyc-keep/Paper.git
```

所以执行：

```bash
git remote add origin https://github.com/hyc-keep/Paper.git
```

### 第 8 步：第一次 push

执行：

```bash
git push -u origin main
```

### 第 9 步：如果 push 失败，先判断是哪一种情况

最常见有两种情况。

#### 情况 A：远端是空仓库

如果远端是空仓库，通常上一步就会成功。

#### 情况 B：远端不是空仓库

如果你在 GitHub 建仓库时顺手勾选了：

- `README`
- `.gitignore`
- `License`

那么远端不是空仓库，这时第一次 push 可能失败。

处理方式：

```bash
git pull origin main --allow-unrelated-histories
```

如果有冲突，处理完后再执行：

```bash
git push -u origin main
```

---

## 6. GitHub 认证怎么处理

### 6.1 现在最简单的方式

你当前仓库地址是 HTTPS，所以最简单的入门方式是：

- 先用 HTTPS
- 之后如果你想长期稳定使用，再切到 SSH

### 6.2 如果用 HTTPS，会要求什么

GitHub 现在通常不会直接支持普通密码 push。

常见做法是：

1. 浏览器已登录 GitHub
2. Git Credential Manager 帮你记住登录
3. 或者使用 Personal Access Token

### 6.3 如果后面你觉得 HTTPS 麻烦

后面可以再切换到 SSH。

但当前为了先把基线上传成功，用 HTTPS 是完全可以的。

---

## 7. 服务器接入 GitHub 的完整步骤

等你租到 GPU 服务器后，再做这部分。

### 第 1 步：进入服务器

进入服务器后，先准备好：

- Python 环境
- CUDA 环境
- Git

### 第 2 步：在服务器上 clone 仓库

执行：

```bash
git clone https://github.com/hyc-keep/Paper.git
```

这一步会把你当前本地已经上传的基线工程拉到服务器。

### 第 3 步：进入服务器上的项目目录

执行：

```bash
cd Paper
```

### 第 4 步：在服务器窗口中先读接力文档

因为切到服务器后通常会打开一个新窗口，没有之前的聊天历史，所以第一件事不是立刻跑命令，而是：

先打开并更新：

- `Paper/服务器切换接力说明.md`

在新窗口里，建议你直接对助手说：

```md
请先读取 `Paper/服务器切换接力说明.md`，再继续当前任务。
```

这样就能快速恢复当前上下文。

---

## 8. 后续本地与服务器怎样同步

这是整个流程里最重要的一部分。

### 8.1 总原则

后续一旦进入 GPU 执行阶段，建议：

**服务器为主线，本地为同步副本。**

也就是说：

- 正式代码修改
- 正式文档回填
- 正式 GPU run
- 正式结果更新

优先在服务器那份工程里完成。

本地主要负责：

- pull 同步
- 备份
- 查看
- 小规模补充

### 8.1.1 以后同步要分两条线看

后面不要再把“同步”理解成只有一种。

实际上会有两条同步线：

#### 第 1 条：Git 同步

负责这些内容：

- 代码
- 配置
- 文档
- 状态页
- 关键元数据

#### 第 2 条：非 Git 同步

负责这些内容：

- 数据集
- checkpoint
- visuals
- predictions
- 大量日志
- 其他大结果

这类内容更适合：

- 留在服务器
- 通过 `PyCharm Deployment`
- 或通过 SFTP / 手动打包下载

不要试图让 Git 同时承担这两条线。

### 8.1.2 Trae、PyCharm、Git 的推荐分工

后面最稳的分工是：

- `Trae`：负责服务器执行、改代码、改文档、跑训练、跑评估
- `PyCharm`：负责远程浏览、看日志、按需下载、少量辅助编辑
- `Git`：负责关键文本资产的正式留痕和双端同步

如果你想同时让 `Trae` 和 `PyCharm` 连同一台服务器，是可以的。

但一定记住下面这条：

**它们可以同时连接，但不要同时改同一个文件。**

### 8.2 当服务器有新改动时

在服务器上执行：

```bash
git status
git add .
git commit -m "docs: update stage02 progress on server"
git push
```

然后回到本地执行：

```bash
git pull
```

如果服务器上产生的是大结果，而不是代码或文档，则不要硬 commit 进去。

这时更推荐：

1. 先把关键结论回填到文档和元数据
2. 把这些轻量文本资产 `commit + push`
3. 需要本地查看的大结果再通过 `PyCharm` 或 SFTP 单独下载

### 8.3 当本地有新改动时

在本地执行：

```bash
git status
git add .
git commit -m "docs: refine local handoff and notes"
git push
```

然后服务器执行：

```bash
git pull
```

如果本地只是为了查看服务器结果，不建议通过本地再反向覆盖服务器。

GPU 阶段更稳的原则始终是：

**服务器为主线，本地为同步副本。**

---

## 9. 本地和服务器都改了同一个文件怎么办

这就是 Git 合并冲突场景。

### 9.1 先不要慌

冲突不是坏事。

它只是说明：

- 本地改了同一个文件
- 服务器也改了同一个文件

Git 不敢替你瞎决定，所以让你手动确认。

### 9.2 标准处理方式

假设你在本地执行：

```bash
git pull
```

然后出现冲突。

这时按下面顺序处理：

1. 打开冲突文件
2. 看 Git 标记出来的冲突块
3. 决定保留哪部分，或者把两边内容正确合并
4. 保存文件
5. 执行：

```bash
git add 冲突文件
git commit -m "merge: resolve local and server changes"
git push
```

### 9.3 最常见的冲突来源

最容易冲突的通常是：

- `README.md`
- `implementation_status.md`
- `当前阶段为什么能pass以及下一步怎么看.md`
- 同一个脚本文件

所以后续建议你尽量减少“本地和服务器同时修改同一份核心文件”的情况。

---

## 10. 怎样尽量减少冲突

最有效的方法不是学更多 Git 命令，而是提前分工。

### 推荐分工

#### 当服务器已经成为主线时

本地尽量少做这些事：

- 不要并行大改核心代码
- 不要并行大改阶段状态页
- 不要并行大改同一份对象说明文

#### 本地更适合做的事

- 查看
- pull 同步
- 备份
- 轻量补充
- 根目录通用说明文更新

#### 服务器更适合做的事

- 正式 GPU 训练
- 正式评估
- 正式状态页回填
- 正式代码修改

### 10.1 如果你同时开 Trae 和 PyCharm

这是允许的，但建议遵守下面的操作纪律：

1. `Trae` 正在改某个脚本或文档时，不要让 `PyCharm` 自动上传覆盖这个文件。
2. `PyCharm` 更适合远程看文件、搜代码、看日志、下载结果，不要把它当全项目镜像同步工具。
3. 本地想拿到最新代码和文档，优先 `git pull`，不是手动复制覆盖。
4. 本地想拿到大结果，优先按需下载，不要把整个 `checkpoints/`、`visuals/` 全量塞进 Git。

---

## 11. 服务器新窗口没有历史记录时怎么办

这是你最关心的问题之一。

答案是：

**靠接力文档，不靠聊天记录本身。**

### 推荐固定做法

每次切换前，先更新：

- `Paper/服务器切换接力说明.md`

至少写清楚这 5 件事：

1. 当前阶段
2. 当前最重要结论
3. 当前最核心阻断项
4. 当前下一步
5. 当前必须优先读取的文件

### 到服务器新窗口后

第一句话直接发：

```md
请先读取 `Paper/服务器切换接力说明.md`，再继续当前任务。
```

如果你想更稳一点，再补一句：

```md
当前不要从头审查，请接着做接力文档里列出的下一步。
```

这样新窗口就不会从零开始了。

---

## 12. VPN 到底什么时候需要

如果你使用 GitHub，在国内网络环境下通常有下面几种可能：

1. 网页能打开，但 `git push/pull` 偶尔慢
2. 有时能 push，有时超时
3. 大多数时候都还行，但稳定性一般

所以现实建议是：

- 先直接试
- 如果 `git push/pull` 明显不稳定，再开 VPN

也就是说：

**VPN 不是绝对必须，但如果 GitHub 网络不稳，开 VPN 会更省事。**

---

## 13. 你现在最推荐的实际执行顺序

请按下面顺序推进，不要跳步。

### 当前阶段

1. 先把 `Paper/.gitignore` 放好
2. 本地初始化 Git
3. 本地第一次提交
4. 本地 push 到 GitHub
5. 确认 GitHub 上的基线工程已经完整可见

### 后续切服务器

6. 在服务器上 clone GitHub 仓库
7. 更新并使用 `Paper/服务器切换接力说明.md`
8. 服务器执行正式 GPU 相关任务
9. 服务器 commit + push
10. 本地 pull 同步

---

## 14. 最后一句话

真正稳定的工作流只有一句话：

**先把本地工程上传成 GitHub 基线，再让服务器基于这份基线继续工作，后续所有同步都走 Git，不走手动覆盖。**

如果你严格按这条做，后面即使切窗口、切机器、切环境，也不会轻易把项目状态搞乱。
