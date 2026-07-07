"""Threshold helpers for stage02 evaluation.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: binary segmentation post-processing after logit prediction
- 章节: sigmoid followed by fixed threshold to obtain binary mask
- 公式/定义: logits(float32) -> sigmoid(probabilities) -> threshold -> uint8 mask
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: src/eval/run_eval.py, configs/eval/eval_proto_v1.yaml
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前阈值来源被正式冻结为 `threshold_source=val17`，阈值值固定为 `0.5`，不在这里引入自适应阈值策略。
- 阈值前显式转成 float32，和当前评估协议中的 `float32_before_threshold` 保持一致。
"""

from __future__ import annotations

import torch


def apply_threshold(logits: torch.Tensor, threshold_value: float) -> torch.Tensor:
    """Convert stage02 logits into binary masks with the frozen threshold rule.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: probability thresholding in binary segmentation evaluation
    - 章节: sigmoid conversion and fixed cutoff decision
    - 公式/定义: sigmoid(logits.float()) >= threshold_value
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/threshold.py, src/eval/run_eval.py, configs/eval/eval_proto_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前输出显式压成 `torch.uint8` 二值 mask，方便后续 metric 链统一按离散预测处理。
    - 函数只负责阈值化，不混入 connected-components 或别的后处理步骤，保持职责单一。
    """
    probabilities = torch.sigmoid(logits.float())
    return (probabilities >= threshold_value).to(dtype=torch.uint8)
