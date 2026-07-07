"""Best-checkpoint selection helpers for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: supervised model selection workflow
- 章节: best-checkpoint tracking by monitored validation metric
- 公式/定义: current best state + current metric -> updated best state plus selection flag
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: src/engine/trainer.py, configs/eval/eval_proto_v1.yaml
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 best selector 被正式冻结为 `val_objdice_max`，所以这里明确只实现“越大越好”的最小比较逻辑。
- 选择器只维护最小必要状态 `best_epoch` 和 `best_metric_value`，避免 stage02 首轮闭环过早引入复杂 checkpoint 策略。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BestCheckpointState:
    """Immutable snapshot of the current best-checkpoint selection state.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: experiment tracking for best epoch selection
    - 章节: persistent best-epoch and best-metric summary
    - 公式/定义: best_epoch plus best_metric_value
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/checkpoint_selector.py, src/engine/trainer.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前状态对象只保留后续保存 `best.ckpt` 所必需的两个字段，说明文与运行资产都更容易对账。
    - 采用 frozen dataclass，避免 trainer 在循环中原地改写状态造成语义不清。
    """
    best_epoch: int
    best_metric_value: float


def update_best_checkpoint(
    current_state: BestCheckpointState | None,
    epoch: int,
    metric_value: float,
) -> tuple[BestCheckpointState, bool]:
    """Update the best-checkpoint state using the frozen stage02 metric rule.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: model selection by validation metric maximization
    - 章节: keep checkpoint when current metric improves over best metric
    - 公式/定义: metric_value > current_best -> new state and save flag
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/eval/checkpoint_selector.py, src/engine/trainer.py, configs/eval/eval_proto_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前比较逻辑不接受 mode 参数，也不在函数内推断 min/max，避免和冻结的 `best_selector=val_objdice_max` 发生歧义。
    - 返回值同时给出新状态和是否写 `best.ckpt` 的布尔标记，方便 trainer 保持最小耦合。
    """
    if current_state is None or metric_value > current_state.best_metric_value:
        return BestCheckpointState(best_epoch=epoch, best_metric_value=metric_value), True
    return current_state, False
