"""Formal split-CSV parsing and validation helpers for stage02.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: benchmark manifest validation before supervised segmentation training
- 章节: split schema checking, relative-path normalization, and sample-ID uniqueness
- 公式/定义: split CSV rows -> schema validation + unique-ID validation + resolved image/mask paths
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: splits/glas/*.csv, src/data/csv_loader.py, src/data/datasets.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 当前只接受正式 split CSV 里的相对路径，不允许把绝对路径混进资产层，避免环境切换时路径语义漂移。
- 在 dataset 构造前先完成 schema 和 sample_id 唯一性检查，尽量把坏 split 资产挡在训练主链外面。
"""

from __future__ import annotations

import csv
from pathlib import Path


COMMON_FIELDS = ("sample_id", "image_relpath", "mask_relpath", "dataset", "split")
GLAS_EXTRA_FIELDS = ("grade", "source_partition")
CRAG_EXTRA_FIELDS = ("source_subset",)


def normalize_relpath(value: str) -> str:
    """Normalize one relative path field from the formal split CSV.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: dataset manifest path normalization before file resolution
    - 章节: canonical slash style for portable sample manifests
    - 公式/定义: raw csv path string -> trimmed portable relative path
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: splits/glas/*.csv, src/data/csv_loader.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一把反斜杠压成正斜杠，保证 Windows 本地资产和说明文里的相对路径锚点口径一致。
    - 这里只做最小清洗，不在这里偷偷改写目录层级或重定向路径根。
    """
    return value.strip().replace("\\", "/").strip()


def load_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """Load raw rows from one frozen split CSV file.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: manifest rows as the formal sample list before dataset instantiation
    - 章节: csv row loading prior to schema validation
    - 公式/定义: csv file -> list of row dictionaries
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: splits/glas/*.csv, src/data/csv_loader.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前保持最小读取语义，只返回原始 DictReader 结果，把 schema 和唯一性检查留给后续函数。
    - 统一使用 utf-8 和 newline 控制，避免 csv 资产在不同本地环境下出现空行偏差。
    """
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def required_fields_for(dataset_code: str) -> tuple[str, ...]:
    """Return the frozen required CSV fields for one dataset code.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: dataset-specific manifest schema under one segmentation protocol
    - 章节: shared common fields plus dataset-specific metadata columns
    - 公式/定义: dataset_code -> required csv field tuple
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml, src/data/csv_loader.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前只显式支持 `glas` 和 `crag` 两类正式 dataset code，不允许 runtime 现场发明新的别名。
    - dataset-specific 扩展列和共用列分开维护，方便说明文回链“哪些列是协议主干、哪些列是数据集特有元信息”。
    """
    dataset = dataset_code.strip().lower()
    if dataset == "glas":
        return COMMON_FIELDS + GLAS_EXTRA_FIELDS
    if dataset == "crag":
        return COMMON_FIELDS + CRAG_EXTRA_FIELDS
    raise ValueError(f"Unsupported dataset_code: {dataset_code}")


def validate_csv_schema(rows: list[dict[str, str]], dataset_code: str) -> list[str]:
    """Validate required fields, empties, and path style for split rows.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: schema validation before sample loading
    - 章节: required-column completeness and portable path constraints
    - 公式/定义: csv rows + dataset_code -> schema issue list
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/data/csv_loader.py, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前不仅检查缺列和空字段，还禁止 `image_relpath`、`mask_relpath` 使用绝对路径，避免 split 资产和项目根脱钩。
    - 返回 issue 列表而不是直接退出，方便上游 dataset 构造把多项问题一次性写清楚。
    """
    issues: list[str] = []
    required = required_fields_for(dataset_code)
    if not rows:
        return ["csv_has_no_rows"]

    row_keys = tuple(rows[0].keys())
    for field in required:
        if field not in row_keys:
            issues.append(f"missing_field:{field}")

    for index, row in enumerate(rows):
        for field in required:
            if not row.get(field, "").strip():
                issues.append(f"empty_field:{index}:{field}")
        for field in ("image_relpath", "mask_relpath"):
            value = row.get(field, "")
            if value and Path(value).is_absolute():
                issues.append(f"absolute_path_forbidden:{index}:{field}")
    return issues


def validate_unique_sample_ids(rows: list[dict[str, str]]) -> list[str]:
    """Validate that one split CSV does not repeat formal sample IDs.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: unique sample identity in benchmark split manifests
    - 章节: one row corresponds to one formal sample anchor
    - 公式/定义: csv rows -> duplicate or missing sample_id issue list
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: splits/glas/*.csv, src/data/csv_loader.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前把 `sample_id` 当成 runtime_evidence 和说明文回链的硬锚点，因此在 split 资产层就必须唯一。
    - 对缺失和重复分开编码，方便上游 dataset 构造在报错时保留精确问题类型。
    """
    issues: list[str] = []
    seen: set[str] = set()
    for index, row in enumerate(rows):
        sample_id = row.get("sample_id", "").strip()
        if not sample_id:
            issues.append(f"missing_sample_id:{index}")
            continue
        if sample_id in seen:
            issues.append(f"duplicate_sample_id:{sample_id}")
            continue
        seen.add(sample_id)
    return issues


def resolve_row_paths(project_root: Path, row: dict[str, str]) -> tuple[Path, Path]:
    """Resolve one CSV row into concrete image and mask file paths.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: relative sample references resolved against project asset root
    - 章节: manifest row -> concrete filesystem assets
    - 公式/定义: project_root + csv row relpaths -> resolved image_path and mask_path
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: splits/glas/*.csv, src/data/csv_loader.py, src/data/datasets.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前统一从项目根解析 image/mask 相对路径，保证 split 资产、runtime report 和说明文里的真实路径锚点保持同一基线。
    - 这里只负责路径展开，不在这里偷偷检查图像可读性，把职责留给 dataset 读取阶段。
    """
    image_path = (project_root / normalize_relpath(row["image_relpath"])).resolve()
    mask_path = (project_root / normalize_relpath(row["mask_relpath"])).resolve()
    return image_path, mask_path
