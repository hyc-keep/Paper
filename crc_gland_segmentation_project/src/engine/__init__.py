"""Formal training-engine package entrypoint for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: stable training loop services exposed through one engine facade
- 章节: package-level access to scheduler, early stop, and trainer loop
- 公式/定义: `src.engine` package -> `EarlyStopper` + `build_scheduler()` + `train_model()` as the formal engine-facing API
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/engine/__init__.py, src/engine/trainer.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前把 early-stop、scheduler 和 trainer 主闭环统一暴露在 `src.engine` 门面后面，减少训练入口直接依赖多个深层子模块路径。
- 包门面只收当前已经冻结并进入正式训练闭环的 3 个对象，不在这里继续暴露未纳入当前基线的 engine 实验接口。
"""

from .early_stop import EarlyStopper
from .lr_scheduler import build_scheduler
from .trainer import train_model

__all__ = ["EarlyStopper", "build_scheduler", "train_model"]
