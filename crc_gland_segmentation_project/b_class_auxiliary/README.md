# B 类辅助目录

这个目录专门存放 `B 类(AI 辅助与流程文件)` 的运行留痕与门禁产物，避免继续和 A 类正式项目报告混在 `reports/` 主树里。

当前固定子目录:

- `tools/`: B 类 gate / runtime / check / enforce 脚本真实实现
- `runtime_checks/`: runtime-check、code-quality、workflow 等运行证据与门禁报告
- `coding_guards/`: 研究、阶段锁定、Pre-check、Post-QC 等 guard 留痕
- `workflow_gates/`: 当未显式指定 guard 目录时的兜底 workflow gate 输出目录

不迁入这里但仍属于 B 类的对象:

- `.trae/skills/`: 规程与模板固定路径

这样划分的目的只有一个: 让 A 类正式交付物和 B 类流程留痕在物理目录上也分开。
