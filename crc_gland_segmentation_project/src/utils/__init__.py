"""Formal utility package entrypoint for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: stable reproducibility helpers exposed behind one utility facade
- 章节: package-level access to global seed and dataloader worker seeding
- 公式/定义: `src.utils` package -> `set_global_seed()` + `seed_worker()` as the formal reproducibility API
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/utils/__init__.py, src/utils/seed.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前包门面只公开随机种子相关接口，不在 utility 层继续混入与 stage02 主链无关的杂项 helper。
- 正式训练入口统一从 `src.utils` 取 reproducibility 入口，方便说明文把“包级门面”和“seed 具体实现”拆开讲。
"""

from .seed import seed_worker, set_global_seed

__all__ = ["seed_worker", "set_global_seed"]
