"""Standalone visual-export entrypoint for stage02 test assets.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: segmentation evaluation needs reproducible visual evidence bundles
- 章节: split-wise raw / gt / pred / overlay export after metrics are available
- 公式/定义: run_dir + testA/testB metrics csv + prediction pngs -> visuals + error_cases
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: scripts/test.py, src/eval/export_visuals.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前脚本只负责根据已落盘的测试结果重建 `visuals/*` 与 `summaries/error_cases.md`，避免为重导可视化再次重复跑整条测试链。
- 正式评估仍以 `scripts/test.py` 为主入口；本脚本是面向可视化重导的窄工具。
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.eval import export_run_visual_assets


def parse_args() -> argparse.Namespace:
    """Parse the narrow visual re-export CLI contract.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: segmentation evaluation needs reproducible visual evidence bundles
    - 章节: split-wise visual assets are rebuilt from existing metric rows and prediction masks
    - 公式/定义: run_dir + max_samples_per_split -> one deterministic visual re-export scope
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/export_visuals.py, src/eval/export_visuals.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前 CLI 只开放 run 目录和样本上限，避免它越权长成第二个正式评估入口。
    - 当前默认值 `5` 对应每个 split 导出最差 5 个样本的可视化观察面。
    """
    parser = argparse.ArgumentParser(description="Re-export stage02 visuals from existing test assets.")
    parser.add_argument("--run-dir", required=True, help="Run directory relative to the project root.")
    parser.add_argument(
        "--max-samples-per-split",
        type=int,
        default=5,
        help="How many worst-case samples to export per split.",
    )
    return parser.parse_args()


def main() -> int:
    """Rebuild stage02 visual assets from existing run artifacts.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: segmentation evaluation needs reproducible visual evidence bundles
    - 章节: existing test metrics and prediction masks can be reused to regenerate visual summaries
    - 公式/定义: run_dir + exported predictions -> visuals/testA + visuals/testB + summaries/error_cases.md
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/export_visuals.py, src/eval/export_visuals.py, scripts/test.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前主函数只负责解析目录、调用 `export_run_visual_assets()` 并打印关键落盘结果，不重新触发模型推理。
    - 当前结果链固定回写 `error_cases` 和 split 级 visual 计数，便于 Post-QC 与 learning-doc 对账。
    """
    args = parse_args()
    run_dir = Path(args.run_dir)
    if not run_dir.is_absolute():
        run_dir = (PROJECT_ROOT / run_dir).resolve()
    result = export_run_visual_assets(run_dir=run_dir, max_samples_per_split=args.max_samples_per_split)
    print(f"run_dir={run_dir.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"error_cases={result['error_cases_path']}")
    print(f"testA_visual_count={result['visual_counts']['testA']}")
    print(f"testB_visual_count={result['visual_counts']['testB']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
