"""Formal train entrypoint for stage01 preflight and stage02 UNet smoke runs.

对应阶段: 02_UNet流程验证
理论依据:
- 论文: Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest
- 章节: benchmark split definition and gland-mask supervision protocol
- 公式/定义: train/val/test role separation and binary gland-mask supervision
代码参考:
- 仓库: project_local_crc_gland_segmentation_project
- 文件: src/data/datasets.py, src/engine/trainer.py, src/eval/run_eval.py
- commit: workspace_local_20260706
- 许可证: project_internal
本项目调整:
- 继续兼容 stage01 的 formal preflight 入口, 但把 stage02 的正式训练与 runtime-check 放回同一个项目本地入口。
- runtime-check 不再停留在“样本可读”,而是实际执行一次 dataloader -> model -> loss -> backward -> optimizer.step。
- 配置解析保持 experiment/data/model/train/eval 五段式, 方便和 implementation_tracking 说明文逐项回链。
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
from typing import Any

import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data import (
    build_augment_config,
    build_dataset_from_csv,
    build_eval_transform,
    build_segmentation_dataset,
    build_train_transform,
    load_data_config,
    simple_yaml_load,
)
from src.engine import EarlyStopper, build_scheduler, train_model
from src.eval.checkpoint_selector import BestCheckpointState, update_best_checkpoint
from src.losses import build_seg_loss
from src.models import build_unet_model
from src.utils import set_global_seed


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the formal project entrypoint.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: benchmark split role separation
    - 公式/定义: training entrypoint must receive explicit config and run role
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/train.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 保留 stage01 `--runtime-check` 兼容参数, 同时复用到 stage02 formal runtime。
    - 把 `--smoke-check`、`--device` 和 `--config` 显式暴露, 避免训练协议靠隐式默认值漂移。
    """
    parser = argparse.ArgumentParser(description="Formal project-local training entrypoint.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional logical run name override.")
    parser.add_argument("--device", default="cpu", help="Requested device hint.")
    parser.add_argument("--smoke-check", action="store_true", help="Run only the minimal local smoke training loop.")
    parser.add_argument(
        "--resume-from-last",
        action="store_true",
        help="Resume the interrupted formal training run from `checkpoints/last.ckpt`.",
    )
    parser.add_argument("--max-steps", type=int, default=1, help="Reserved for stage01 preflight compatibility.")
    parser.add_argument(
        "--runtime-check",
        action="store_true",
        help="Emit a lightweight payload after formal asset checks for stage01 preflight compatibility.",
    )
    parser.add_argument(
        "--runtime-check-output",
        default="b_class_auxiliary/runtime_checks/train_runtime_payload.json",
        help="Relative path for the runtime-check payload JSON.",
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().replace("\\", "/").strip()


def load_experiment_config(project_root: Path, relative_path: str) -> tuple[Path, dict[str, Any]]:
    """Load the formal experiment config declared by the caller.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: split-specific benchmark execution
    - 公式/定义: experiment role must be tied to an explicit protocol package
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 实验入口必须先解析 experiment config, 再去解引用 data/model/train/eval, 不允许脚本直接猜目录。
    - 这里要求配置一定是 mapping, 为后续 run_meta 与说明文冻结回链提供稳定字段来源。
    """
    config_path = (project_root / normalize_relpath(relative_path)).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"experiment config not found: {config_path}")
    data = simple_yaml_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"experiment config must be a mapping: {config_path}")
    return config_path, data


def load_json_mapping(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"json payload must be a mapping: {path}")
    return data


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def filter_rows_through_epoch(rows: list[dict[str, str]], max_epoch: int) -> list[dict[str, str]]:
    filtered: list[dict[str, str]] = []
    for row in rows:
        try:
            epoch_value = int(row["epoch"])
        except (KeyError, TypeError, ValueError):
            continue
        if epoch_value <= max_epoch:
            filtered.append(row)
    return filtered


def dump_simple_yaml(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(dump_simple_yaml(item, indent + 2))
            elif isinstance(item, list):
                rendered = ", ".join(str(element) for element in item)
                lines.append(f"{prefix}{key}: [{rendered}]")
            elif isinstance(item, bool):
                lines.append(f"{prefix}{key}: {'true' if item else 'false'}")
            else:
                lines.append(f"{prefix}{key}: {item}")
        return "\n".join(lines)
    raise TypeError(f"Unsupported yaml dump value: {type(value)!r}")


def resolve_device(device_hint: str) -> torch.device:
    if device_hint.startswith("cuda") and torch.cuda.is_available():
        return torch.device(device_hint)
    return torch.device("cpu")


def resolve_config_ref(project_root: Path, experiment_config: dict[str, Any], key: str) -> Path:
    """Resolve one config reference from the experiment bundle.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: benchmark protocol must keep train/val/test roles explicit
    - 公式/定义: protocol package references should stay auditable
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/experiment/A1_UNet_GlaS_v1_seed3407.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 统一用 `config_refs` 串联 data/model/train/eval 四类协议文件。
    - 缺字段时直接报错, 不允许静默回退到猜测路径。
    """
    config_refs = experiment_config.get("config_refs", {})
    if not isinstance(config_refs, dict):
        raise ValueError("experiment config must provide config_refs mapping")
    ref = config_refs.get(key)
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError(f"missing config_refs.{key}")
    return (project_root / normalize_relpath(ref)).resolve()


def resolve_data_config_path(project_root: Path, experiment_config: dict[str, Any]) -> Path:
    """Resolve the data config used by the current experiment.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: dataset identity and split role must stay stable
    - 公式/定义: train/val/test data source cannot be inferred by ad-hoc scanning
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: configs/data/glas.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 优先消费 `config_refs.data`, 只在历史兼容路径上允许通过 `dataset_code` 兜底。
    - 这样能把 `configs/data -> splits/*.csv -> dataset_root` 这条正式消费链保持成唯一入口。
    """
    config_refs = experiment_config.get("config_refs", {})
    if isinstance(config_refs, dict):
        data_ref = config_refs.get("data")
        if isinstance(data_ref, str) and data_ref.strip():
            return (project_root / normalize_relpath(data_ref)).resolve()

    dataset_code = str(experiment_config.get("dataset_code", "")).strip().lower()
    if dataset_code in {"glas", "crag"}:
        return (project_root / "configs" / "data" / f"{dataset_code}.yaml").resolve()
    raise ValueError("experiment config must provide config_refs.data or dataset_code in {glas, crag}")


def resolve_asset_manifest_path(project_root: Path, experiment_config: dict[str, Any]) -> Path:
    config_refs = experiment_config.get("config_refs", {})
    if isinstance(config_refs, dict):
        manifest_ref = config_refs.get("asset_manifest")
        if isinstance(manifest_ref, str) and manifest_ref.strip():
            return (project_root / normalize_relpath(manifest_ref)).resolve()
    return (project_root / "reports" / "stage_reports" / "asset_manifest.json").resolve()


def resolve_split_name(experiment_config: dict[str, Any]) -> str:
    split_name = str(experiment_config.get("runtime_split", experiment_config.get("train_split", "train"))).strip()
    return split_name or "train"


def validate_formal_handoff(
    project_root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    data_config_path: Path,
    data_proto_version: str,
    dataset_code: str,
    split_name: str,
) -> dict[str, Any]:
    """Check whether the formal data-stage handoff is ready for stage02.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: benchmark split identity and raw-mask availability
    - 公式/定义: formal execution must consume the frozen split and registered assets
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: reports/stage_reports/asset_manifest.json
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 把 stage01 的 handoff 结果显式升级成 stage02 的准入检查, 包括 `data_stage_pass`、`handoff_ready`、`preflight_pass`。
    - 额外校验 split 资产和 data config 是否已在 manifest 注册, 避免训练入口绕开正式数据链。
    """
    blockers: list[str] = []
    if manifest.get("data_stage_pass") is not True:
        blockers.append("data_stage_pass_false")
    if manifest.get("handoff_ready") is not True:
        blockers.append("handoff_ready_false")
    if manifest.get("preflight_pass") is not True:
        blockers.append("preflight_pass_false")

    manifest_proto_version = str(manifest.get("data_protocol_package_version", "")).strip()
    if manifest_proto_version != data_proto_version:
        blockers.append(f"data_protocol_version_mismatch:{manifest_proto_version or 'missing'}!={data_proto_version}")

    split_assets = manifest.get("split_assets", [])
    split_asset_exists = False
    if isinstance(split_assets, list):
        for item in split_assets:
            if not isinstance(item, dict):
                continue
            if (
                str(item.get("dataset", "")).strip().lower() == dataset_code.lower()
                and str(item.get("split_name", "")).strip() == split_name
                and item.get("exists") is True
            ):
                split_asset_exists = True
                break
    if not split_asset_exists:
        blockers.append(f"split_asset_missing:{dataset_code}:{split_name}")

    data_config_relpath = data_config_path.relative_to(project_root).as_posix()
    config_assets = manifest.get("config_source_assets", [])
    data_config_registered = False
    if isinstance(config_assets, list):
        for item in config_assets:
            if not isinstance(item, dict):
                continue
            if (
                str(item.get("type", "")).strip() == "config"
                and str(item.get("relative_path", "")).strip() == data_config_relpath
                and item.get("exists") is True
            ):
                data_config_registered = True
                break
    if not data_config_registered:
        blockers.append(f"data_config_not_registered:{data_config_relpath}")

    return {
        "asset_manifest": manifest_path.relative_to(project_root).as_posix(),
        "asset_manifest_version": str(manifest.get("asset_manifest_version", "")),
        "data_protocol_package_version": manifest_proto_version,
        "data_stage_pass": manifest.get("data_stage_pass") is True,
        "handoff_ready": manifest.get("handoff_ready") is True,
        "preflight_pass": manifest.get("preflight_pass") is True,
        "split_asset_exists": split_asset_exists,
        "data_config_registered": data_config_registered,
        "blockers": blockers,
    }


def inspect_sample_paths(image_path: Path, mask_path: Path) -> dict[str, Any]:
    """Inspect one raw image/mask pair and expose physical evidence fields.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: raw image and gland-mask supervision
    - 公式/定义: image/mask shape and dtype are the first physical evidence before training
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: b_class_auxiliary/runtime_checks/runtime_evidence.json
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 在 stage01 preflight 中先把 image/mask 的 shape、dtype、unique 值写成结构化字段。
    - 这些字段后续继续被 stage02 learning doc 和 runtime gate 复用, 不再只存在于临时 print。
    """
    if Image is None:
        return {
            "input_shape": None,
            "input_dtype": None,
            "target_shape": None,
            "target_dtype": None,
            "target_unique_values": None,
        }

    with Image.open(image_path) as image:
        image.load()
        input_shape = [image.size[1], image.size[0], len(image.getbands())]
        input_dtype = "uint8"

    with Image.open(mask_path) as mask:
        mask.load()
        colors = mask.getcolors(maxcolors=2048)
        if colors is None:
            target_unique_values: list[str] | None = [">2048_unique_values"]
        else:
            target_unique_values = [str(color) for _, color in colors[:32]]
        target_shape = [mask.size[1], mask.size[0]]
        target_dtype = "uint8"

    return {
        "input_shape": input_shape,
        "input_dtype": input_dtype,
        "target_shape": target_shape,
        "target_dtype": target_dtype,
        "target_unique_values": target_unique_values,
    }


def build_runtime_payload(
    project_root: Path,
    config_path: Path,
    data_config_path: Path,
    handoff_check: dict[str, Any],
    sample: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    image_path = Path(sample["image_path"]).resolve()
    mask_path = Path(sample["mask_path"]).resolve()
    sample_inspection = inspect_sample_paths(image_path, mask_path)
    return {
        "run_name": args.run_name,
        "mode": "runtime_check" if args.runtime_check else "normal",
        "device": args.device,
        "max_steps": args.max_steps,
        "experiment_config": config_path.relative_to(project_root).as_posix(),
        "data_config": data_config_path.relative_to(project_root).as_posix(),
        "asset_manifest": handoff_check["asset_manifest"],
        "asset_manifest_version": handoff_check["asset_manifest_version"],
        "data_protocol_package_version": handoff_check["data_protocol_package_version"],
        "data_stage_pass": handoff_check["data_stage_pass"],
        "handoff_ready": handoff_check["handoff_ready"],
        "preflight_pass": handoff_check["preflight_pass"],
        "split_asset_exists": handoff_check["split_asset_exists"],
        "data_config_registered": handoff_check["data_config_registered"],
        "sample_id": sample["sample_id"],
        "sample_path": image_path.relative_to(project_root).as_posix(),
        "mask_path": mask_path.relative_to(project_root).as_posix(),
        "input_shape": sample_inspection["input_shape"],
        "input_dtype": sample_inspection["input_dtype"],
        "target_shape": sample_inspection["target_shape"],
        "target_dtype": sample_inspection["target_dtype"],
        "target_unique_values": sample_inspection["target_unique_values"],
        "output_shape": None,
        "output_dtype": None,
        "loss_value": None,
        "loss_is_finite": None,
        "backward_executed": None,
        "optimizer_step_executed": None,
        "runtime_profile": "data_protocol_preflight",
        "entrypoint_check_pass": True,
        "entrypoint_check_reason": "formal_split_assets_and_handoff_gates_resolved",
    }


def run_stage01_preflight(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    experiment_config: dict[str, Any],
) -> int:
    """Execute the formal stage01-style preflight branch.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge
    - 章节: split-specific data consumption before model training
    - 公式/定义: formal execution must first prove that the frozen data assets can be resolved
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: reports/stage_reports/data_stage_acceptance.md
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 这个分支被保留下来, 用来承接 stage01 的 formal preflight 资产证明。
    - 即使项目已经进入 stage02, 仍然需要它作为“输入层没有跑偏”的上游证据来源。
    """
    data_config_path = resolve_data_config_path(project_root, experiment_config)
    data_config = load_data_config(project_root, data_config_path)
    asset_manifest_path = resolve_asset_manifest_path(project_root, experiment_config)
    asset_manifest = load_json_mapping(asset_manifest_path)
    split_name = resolve_split_name(experiment_config)
    handoff_check = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config.data_proto_version,
        dataset_code=data_config.dataset_code,
        split_name=split_name,
    )
    if handoff_check["blockers"]:
        raise RuntimeError("formal handoff gate blocked: " + ", ".join(handoff_check["blockers"]))

    samples = build_dataset_from_csv(project_root, data_config, split_name)
    if not samples:
        raise RuntimeError(f"formal split is empty: {split_name}")
    sample = samples[0]
    if not Path(sample["image_path"]).exists() or not Path(sample["mask_path"]).exists():
        raise FileNotFoundError("formal split resolved a missing image or mask asset")

    payload = build_runtime_payload(project_root, config_path, data_config_path, handoff_check, sample, args)
    if args.runtime_check:
        output_path = (project_root / normalize_relpath(args.runtime_check_output)).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"run_name={args.run_name}")
    print(f"experiment_config={config_path.relative_to(project_root).as_posix()}")
    print(f"data_config={data_config_path.relative_to(project_root).as_posix()}")
    print(f"asset_manifest={handoff_check['asset_manifest']}")
    print(f"dataset_code={data_config.dataset_code}")
    print(f"split_name={split_name}")
    print(f"sample_id={sample['sample_id']}")
    print(f"image_path={Path(sample['image_path']).resolve().relative_to(project_root).as_posix()}")
    print(f"mask_path={Path(sample['mask_path']).resolve().relative_to(project_root).as_posix()}")
    if args.runtime_check:
        print(f"runtime_check_output={normalize_relpath(args.runtime_check_output)}")
    return 0


def should_run_stage01_preflight(experiment_config: dict[str, Any]) -> bool:
    stage_code = str(experiment_config.get("stage_code", "")).strip()
    model_code = str(experiment_config.get("model_code", "")).strip()
    return stage_code == "01_data_protocol_preflight" or model_code == "train_entrypoint_preflight_only"


def load_training_configs(project_root: Path, experiment_config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    data_config_path = resolve_config_ref(project_root, experiment_config, "data")
    model_config_path = resolve_config_ref(project_root, experiment_config, "model")
    train_config_path = resolve_config_ref(project_root, experiment_config, "train")
    eval_config_path = resolve_config_ref(project_root, experiment_config, "eval")
    return {
        "data": simple_yaml_load(data_config_path.read_text(encoding="utf-8")),
        "model": simple_yaml_load(model_config_path.read_text(encoding="utf-8")),
        "train": simple_yaml_load(train_config_path.read_text(encoding="utf-8")),
        "eval": simple_yaml_load(eval_config_path.read_text(encoding="utf-8")),
        "paths": {
            "data": data_config_path.relative_to(project_root).as_posix(),
            "model": model_config_path.relative_to(project_root).as_posix(),
            "train": train_config_path.relative_to(project_root).as_posix(),
            "eval": eval_config_path.relative_to(project_root).as_posix(),
        },
    }


def build_output_dir(project_root: Path, run_name: str) -> Path:
    return (project_root / "experiments" / run_name).resolve()


def build_run_meta(
    experiment_config: dict[str, Any],
    config_bundle: dict[str, Any],
    data_config_obj: Any,
    train_run_name: str,
    smoke_check: bool,
) -> dict[str, Any]:
    train_config = config_bundle["train"]
    eval_config = config_bundle["eval"]
    model_config = config_bundle["model"]
    return {
        "run_name": train_run_name,
        "stage_code": str(experiment_config["stage_code"]),
        "dataset_code": str(experiment_config["dataset_code"]),
        "model_name": str(model_config["model_name"]),
        "model_version": str(model_config["model_version"]),
        "config_version": str(experiment_config["config_version"]),
        "data_proto_version": str(data_config_obj.data_proto_version),
        "train_proto_version": str(train_config["train_proto_version"]),
        "aug_version": str(train_config["aug_version"]),
        "aug_profile_name": str(train_config["aug_profile_name"]),
        "eval_aug_enable": bool(train_config["eval_aug_enable"]),
        "eval_proto_version": str(eval_config["eval_proto_version"]),
        "loss_name": str(train_config["loss_name"]),
        "loss_version": str(train_config["loss_version"]),
        "postprocess_version": str(eval_config["postprocess_version"]),
        "optimizer": str(train_config["optimizer"]),
        "lr": float(train_config["lr"]),
        "weight_decay": float(train_config["weight_decay"]),
        "scheduler": str(train_config["scheduler"]),
        "scheduler_monitor": str(train_config["scheduler_monitor"]),
        "epoch_max": int(train_config["epoch_max"]),
        "early_stop_patience": int(train_config["early_stop_patience"]),
        "batch_size": int(train_config["batch_size"]),
        "amp": bool(train_config["amp"]),
        "train_seed": int(experiment_config["train_seed"]),
        "best_selector": str(eval_config["best_selector"]),
        "threshold_value": float(eval_config["threshold_value"]),
        "threshold_source": str(eval_config["threshold_source"]),
        "result_tag": str(experiment_config["result_tag"]),
        "aggregation": str(experiment_config["aggregation"]),
        "smoke_check": smoke_check,
        "config_refs": config_bundle["paths"],
    }


def _relative_path_or_posix(path_value: str | Path, project_root: Path) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        return path.as_posix()
    return path.resolve().relative_to(project_root).as_posix()


def _tensor_dtype_name(tensor: torch.Tensor) -> str:
    return str(tensor.dtype).replace("torch.", "")


def _normalize_unique_value(value: float) -> int | float:
    rounded = round(value)
    if abs(value - rounded) < 1.0e-6:
        return int(rounded)
    return float(value)


def _extract_first_string(value: Any) -> str:
    if isinstance(value, (list, tuple)) and value:
        return str(value[0])
    return str(value)


def run_stage02_runtime_check(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    config_bundle: dict[str, Any],
    train_loader: DataLoader[dict[str, Any]],
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> int:
    """Run the minimal formal stage02 training step and emit runtime evidence.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net
    - 章节: encoder-decoder forward with supervised pixel-wise optimization
    - 公式/定义: logits -> loss -> backward -> optimizer.step must be physically executed
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/models/unet.py, src/losses/seg_losses.py, src/engine/trainer.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - runtime-check 在这里真实跑一个 batch, 输出 `input_shape/target_shape/output_shape/loss_value/backward_executed/optimizer_step_executed`。
    - 这样 learning doc 和 runtime gate 都能回链到同一份 formal payload, 不再靠口头声称训练链成立。
    """
    model.to(device)
    model.train()
    max_steps = max(1, int(args.max_steps))
    payload: dict[str, Any] | None = None

    for batch_index, batch in enumerate(train_loader, start=1):
        images = batch["image"].to(device=device, dtype=torch.float32)
        targets = batch["mask"].to(device=device, dtype=torch.float32)

        optimizer.zero_grad(set_to_none=True)
        logits = model(images)
        loss_dict = loss_fn(logits, targets)
        loss_total = loss_dict["loss_total"]
        loss_total.backward()
        optimizer.step()

        target_unique_values = [
            _normalize_unique_value(float(item))
            for item in torch.unique(targets.detach().cpu()).tolist()
        ]

        payload = {
            "run_name": args.run_name,
            "mode": "runtime_check",
            "device": device.type,
            "max_steps": max_steps,
            "steps_executed": batch_index,
            "experiment_config": config_path.relative_to(project_root).as_posix(),
            "data_config": config_bundle["paths"]["data"],
            "model_config": config_bundle["paths"]["model"],
            "train_config": config_bundle["paths"]["train"],
            "eval_config": config_bundle["paths"]["eval"],
            "sample_id": _extract_first_string(batch["sample_id"]),
            "sample_path": _relative_path_or_posix(_extract_first_string(batch["image_path"]), project_root),
            "mask_path": _relative_path_or_posix(_extract_first_string(batch["mask_path"]), project_root),
            "input_shape": list(images.shape),
            "input_dtype": _tensor_dtype_name(images),
            "target_shape": list(targets.shape),
            "target_dtype": _tensor_dtype_name(targets),
            "target_unique_values": target_unique_values,
            "output_shape": list(logits.shape),
            "output_dtype": _tensor_dtype_name(logits),
            "loss_value": float(loss_total.detach().item()),
            "loss_is_finite": bool(torch.isfinite(loss_total.detach()).item()),
            "backward_executed": True,
            "optimizer_step_executed": True,
            "runtime_profile": "full_training_runtime",
            "entrypoint_check_pass": True,
            "entrypoint_check_reason": "formal_train_step_completed",
        }
        if batch_index >= max_steps:
            break

    if payload is None:
        raise RuntimeError("runtime-check dataloader produced zero batches")

    output_path = (project_root / normalize_relpath(args.runtime_check_output)).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"run_name={args.run_name}")
    print(f"device={device.type}")
    print(f"runtime_check_output={normalize_relpath(args.runtime_check_output)}")
    print(f"steps_executed={payload['steps_executed']}")
    print(f"sample_id={payload['sample_id']}")
    print(f"loss_value={payload['loss_value']:.6f}")
    return 0


def run_stage02_training(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    experiment_config: dict[str, Any],
) -> int:
    """Execute the formal stage02 UNet smoke/full training branch.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: U-Net
    - 章节: supervised segmentation training loop
    - 公式/定义: train -> val -> scheduler -> checkpoint is the minimal closed loop
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: src/engine/trainer.py, src/eval/run_eval.py, configs/train/unet_flow_v1.yaml
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 先复核 train/val handoff, 再构造 dataset/model/loss/optimizer/scheduler, 防止训练支路绕开正式资产。
    - `--runtime-check` 直接复用这一支的真实构图, 避免出现第二套临时训练入口。
    """
    config_bundle = load_training_configs(project_root, experiment_config)
    data_config_path = (project_root / config_bundle["paths"]["data"]).resolve()
    data_config_obj = load_data_config(project_root, data_config_path)

    asset_manifest_path = resolve_asset_manifest_path(project_root, experiment_config)
    asset_manifest = load_json_mapping(asset_manifest_path)
    train_handoff = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config_obj.data_proto_version,
        dataset_code=data_config_obj.dataset_code,
        split_name="train",
    )
    val_handoff = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config_obj.data_proto_version,
        dataset_code=data_config_obj.dataset_code,
        split_name="val",
    )
    blockers = train_handoff["blockers"] + val_handoff["blockers"]
    if blockers:
        raise RuntimeError("stage02 handoff gate blocked: " + ", ".join(blockers))

    device = resolve_device(args.device)
    smoke_check = bool(args.smoke_check)
    train_run_name = args.run_name or (
        str(experiment_config["smoke_check_run_name"]) if smoke_check else str(experiment_config["run_name"])
    )
    output_dir = build_output_dir(project_root, train_run_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    set_global_seed(int(experiment_config["train_seed"]))

    train_config = config_bundle["train"]
    model_config = config_bundle["model"]
    eval_config = config_bundle["eval"]

    augment_config = build_augment_config(train_config)
    train_transform = build_train_transform(data_config_obj, augment_config)
    eval_transform = build_eval_transform(data_config_obj)

    train_dataset = build_segmentation_dataset(project_root, data_config_obj, "train", transform=train_transform)
    val_dataset = build_segmentation_dataset(project_root, data_config_obj, "val", transform=eval_transform)

    train_loader = DataLoader(
        train_dataset,
        batch_size=int(train_config["batch_size"]),
        shuffle=True,
        num_workers=int(train_config["num_workers"]),
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=int(train_config["batch_size"]),
        shuffle=False,
        num_workers=int(train_config["num_workers"]),
    )

    model = build_unet_model(model_config)
    loss_fn = build_seg_loss(train_config)
    optimizer = AdamW(model.parameters(), lr=float(train_config["lr"]), weight_decay=float(train_config["weight_decay"]))

    if args.runtime_check:
        return run_stage02_runtime_check(
            args=args,
            project_root=project_root,
            config_path=config_path,
            config_bundle=config_bundle,
            train_loader=train_loader,
            model=model,
            loss_fn=loss_fn,
            optimizer=optimizer,
            device=device,
        )

    scheduler = build_scheduler(optimizer, train_config)
    early_stopper = EarlyStopper(patience=int(train_config["early_stop_patience"]), mode="max")

    resume_state: dict[str, Any] | None = None
    if args.resume_from_last:
        last_checkpoint_path = output_dir / "checkpoints" / "last.ckpt"
        if not last_checkpoint_path.exists():
            raise FileNotFoundError(f"resume checkpoint not found: {last_checkpoint_path}")
        checkpoint = torch.load(last_checkpoint_path, map_location="cpu")
        if not isinstance(checkpoint, dict):
            raise ValueError(f"resume checkpoint format is invalid: {last_checkpoint_path}")
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])

        train_rows = load_csv_rows(output_dir / "train_log.csv")
        val_rows = load_csv_rows(output_dir / "val_metrics.csv")
        if not val_rows:
            raise RuntimeError("cannot resume without existing val_metrics.csv rows")

        resume_epoch = int(checkpoint.get("epoch", 0))
        train_rows = filter_rows_through_epoch(train_rows, max_epoch=resume_epoch)
        val_rows = filter_rows_through_epoch(val_rows, max_epoch=resume_epoch)
        if not val_rows:
            raise RuntimeError(
                "cannot resume because no validated epochs remain after aligning CSV history to last.ckpt"
            )

        best_state: BestCheckpointState | None = None
        for row in val_rows:
            metric_value = float(row["val_objdice"])
            epoch_value = int(row["epoch"])
            scheduler.step(metric_value)
            early_stopper.update(metric_value)
            best_state, _ = update_best_checkpoint(best_state, epoch=epoch_value, metric_value=metric_value)

        resume_state = {
            "next_epoch": resume_epoch + 1,
            "train_rows": train_rows,
            "val_rows": val_rows,
            "best_state": best_state,
        }

    run_meta = build_run_meta(experiment_config, config_bundle, data_config_obj, train_run_name, smoke_check)
    if resume_state is not None:
        run_meta["resume_from_last"] = True
        run_meta["resume_start_epoch"] = int(resume_state["next_epoch"])
    config_snapshot = {
        "experiment": experiment_config,
        "data": config_bundle["data"],
        "model": model_config,
        "train": train_config,
        "eval": eval_config,
    }
    (output_dir / "config.yaml").write_text(dump_simple_yaml(config_snapshot) + "\n", encoding="utf-8")
    (output_dir / "run_meta.yaml").write_text(dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    summary = train_model(
        model=model,
        loss_fn=loss_fn,
        optimizer=optimizer,
        scheduler=scheduler,
        early_stopper=early_stopper,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        output_dir=output_dir,
        train_config=train_config,
        eval_config=eval_config,
        smoke_check=smoke_check,
        resume_state=resume_state,
    )

    run_meta.update(
        {
            "stop_reason": summary["stop_reason"],
            "best_epoch": summary["best_epoch"],
            "best_metric_value": summary["best_metric_value"],
            "amp_active": summary["amp_active"],
            "epoch_count": summary["epoch_count"],
            "device": device.type,
        }
    )
    (output_dir / "run_meta.yaml").write_text(dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    print(f"run_name={train_run_name}")
    print(f"output_dir={output_dir.relative_to(project_root).as_posix()}")
    print(f"device={device.type}")
    print(f"smoke_check={str(smoke_check).lower()}")
    print(f"best_epoch={summary['best_epoch']}")
    print(f"best_metric_name=val_objdice")
    print(f"best_metric_value={summary['best_metric_value']:.6f}")
    print(f"stop_reason={summary['stop_reason']}")
    return 0


def main() -> int:
    """Route the formal entrypoint to stage01 preflight or stage02 training.

    对应阶段: 02_UNet流程验证
    理论依据:
    - 论文: GlaS Challenge and U-Net baseline protocol
    - 章节: data handoff before baseline training
    - 公式/定义: a single auditable entrypoint should dispatch by experiment role, not by ad-hoc scripts
    代码参考:
    - 仓库: project_local_crc_gland_segmentation_project
    - 文件: scripts/train.py
    - commit: workspace_local_20260706
    - 许可证: project_internal
    本项目调整:
    - 当前只保留一个正式项目本地入口, 通过 experiment config 决定走 preflight 还是 stage02 训练。
    - 这样 implementation_tracking、runtime gate 和 code-quality gate 可以一直回链到同一个入口文件。
    """
    args = parse_args()
    project_root = PROJECT_ROOT
    config_path, experiment_config = load_experiment_config(project_root, args.config)

    if should_run_stage01_preflight(experiment_config):
        if args.run_name is None:
            args.run_name = str(experiment_config.get("run_name", "manual_run"))
        return run_stage01_preflight(args, project_root, config_path, experiment_config)
    return run_stage02_training(args, project_root, config_path, experiment_config)


if __name__ == "__main__":
    raise SystemExit(main())
