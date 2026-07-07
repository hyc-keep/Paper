"""Early stopping helpers for stage02 training.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: early stopping by monitored validation metric
- 章节: stop training when no further validation improvement is observed
- 公式/定义: current metric stream + patience -> improved flag plus should_stop flag
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: configs/train/unet_flow_v1.yaml, src/engine/trainer.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前 early stop 只服务 `val_objdice` 最大化语义，不引入更复杂的 warmup、delta 或窗口平均策略。
- 训练闭环里把 early stop 判定收成独立对象，避免 trainer 同时维护日志、checkpoint 和停训状态时职责继续变重。
"""

from __future__ import annotations


class EarlyStopper:
    """Track plateaued validation progress for the frozen stage02 stop rule.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: early stopping with patience on validation metric
    - 章节: reset bad-epoch counter on improvement, stop when patience exhausted
    - 公式/定义: metric sequence + patience + comparison mode -> improved or should_stop
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/engine/early_stop.py, src/engine/trainer.py, configs/train/unet_flow_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前默认比较模式虽然保留 `max/min`，但 stage02 正式训练只走 `mode=max`，和 `val_objdice` 选优链保持一致。
    - 状态只保留 `best_value` 与 `num_bad_epochs`，保证最小闭环可解释。
    """
    def __init__(self, patience: int, mode: str = "max") -> None:
        if mode not in {"max", "min"}:
            raise ValueError(f"Unsupported early-stop mode: {mode}")
        self.patience = patience
        self.mode = mode
        self.best_value: float | None = None
        self.num_bad_epochs = 0

    def update(self, value: float) -> tuple[bool, bool]:
        """Update the early-stop state with one new validation metric value.

        对应阶段: 02_UNet流程验证
        理论依据:
        - 论文: patience-based stop criterion
        - 章节: improve -> reset counter, otherwise -> accumulate bad epochs
        - 公式/定义: value compared with best_value -> improved flag and should_stop flag
        代码参考:
        - 仓库: project_local_crc_gland_segmentation_project
        - 文件: src/engine/early_stop.py, src/engine/trainer.py
        - commit: workspace_local_20260706
        - 许可证: project_internal
        本项目调整:
        - 当前函数返回 `(improved, should_stop)` 二元组，直接给 trainer 消费，不再在外层重复维护计数状态。
        - stage02 正式链默认把“更好”定义为 `value > best_value`，与 best checkpoint 规则方向保持一致。
        """
        improved = False
        if self.best_value is None:
            improved = True
        elif self.mode == "max":
            improved = value > self.best_value
        else:
            improved = value < self.best_value

        if improved:
            self.best_value = value
            self.num_bad_epochs = 0
            return True, False

        self.num_bad_epochs += 1
        should_stop = self.num_bad_epochs >= self.patience
        return False, should_stop
