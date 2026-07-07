"""Formal model package entrypoint for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: stable segmentation model construction exposed behind one package-level builder
- 章节: package facade for the frozen UNet public entry
- 公式/定义: `src.models` package -> `build_unet_model()` and `UNet` as the formal model-facing API
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/train.py, src/models/__init__.py, src/models/unet.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前只公开 `UNet` 与 `build_unet_model` 两个正式入口，避免 stage02 在包门面层继续暴露未冻结的模型实验接口。
- 训练入口统一从 `src.models` 导入，而不是直接依赖更深子模块路径，方便说明文把“正式入口层”和“具体实现层”拆开解释。
"""

from .unet import UNet, build_unet_model

__all__ = ["UNet", "build_unet_model"]
