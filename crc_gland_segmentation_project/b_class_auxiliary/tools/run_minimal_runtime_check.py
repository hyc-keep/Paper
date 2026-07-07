"""Generate a truthful runtime-check report backed by explicit evidence files."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None


PLACEHOLDER_SIGNALS = (
    "Skeleton placeholder.",
    "TODO: implement this module according to the frozen protocol.",
    "TODO: implement this entrypoint according to the frozen protocol.",
    "TODO: implement this tool entrypoint",
    'raise NotImplementedError("Implement this module according to the frozen protocol.")',
)
RUNTIME_KEYS = (
    "smoke_run_pass",
    "dataloader_batch_check_pass",
    "tensor_shape_dtype_pass",
    "loss_finite_pass",
    "grad_step_pass",
)
STATUS_ORDER = {"fail": 3, "partial": 2, "pass": 1, "not_applicable": 0}


@dataclass
class FileCheck:
    label: str
    relative_path: str
    ready: bool
    reason: str


@dataclass
class RuntimeStatus:
    key: str
    status: str
    reason: str


def infer_runtime_profile(experiment_config: dict[str, Any]) -> str:
    stage_code = normalize_relpath(str(experiment_config.get("stage_code", ""))).lower()
    model_code = normalize_relpath(str(experiment_config.get("model_code", ""))).lower()
    if stage_code == "01_data_protocol_preflight" or model_code == "train_entrypoint_preflight_only":
        return "data_protocol_preflight"
    return "full_training_runtime"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a truthful runtime-check report for a formal experiment config."
    )
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[2]),
        help="Absolute path to the project root.",
    )
    parser.add_argument(
        "--experiment-config",
        required=True,
        help="Relative path to the experiment YAML file.",
    )
    parser.add_argument(
        "--split",
        default="train",
        choices=("train", "val", "testA", "testB", "test"),
        help="Which split to inspect for physical sample evidence.",
    )
    parser.add_argument(
        "--sample-index",
        type=int,
        default=0,
        help="Zero-based sample index inside the selected split.",
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help="Device hint passed to the formal runtime-check command.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=1,
        help="How many steps the formal train entrypoint should run in runtime-check mode.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=120,
        help="Timeout for the formal runtime-check subprocess.",
    )
    parser.add_argument(
        "--output",
        default="b_class_auxiliary/runtime_checks/runtime_check_report.md",
        help="Relative path of the generated markdown report.",
    )
    parser.add_argument(
        "--evidence-output",
        default="b_class_auxiliary/runtime_checks/runtime_evidence.json",
        help="Relative path of the generated merged runtime evidence JSON.",
    )
    parser.add_argument(
        "--log-output",
        default="b_class_auxiliary/runtime_checks/runtime_check.log",
        help="Relative path of the generated runtime log file.",
    )
    parser.add_argument(
        "--train-runtime-output",
        default="b_class_auxiliary/runtime_checks/train_runtime_payload.json",
        help="Relative path that the formal runtime command should write into.",
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/").strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def simple_yaml_load(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        stripped = raw_line.strip()
        if ":" not in stripped:
            raise ValueError(f"Unsupported YAML line: {raw_line}")
        key, raw_value = stripped.split(":", 1)
        value = raw_value.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if not value:
            nested: dict[str, Any] = {}
            current[key] = nested
            stack.append((indent, nested))
        else:
            current[key] = parse_scalar(value)
    return root


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    text = read_text(path)
    data = yaml.safe_load(text) if yaml is not None else simple_yaml_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping YAML: {path}")
    return data


def load_json_mapping(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping JSON: {path}")
    return data


def is_placeholder_text(text: str) -> bool:
    return any(signal in text for signal in PLACEHOLDER_SIGNALS)


def status_rank(value: str) -> int:
    return STATUS_ORDER.get(value, 0)


def combine_status(*values: str) -> str:
    ranked = sorted(values, key=status_rank, reverse=True)
    return ranked[0] if ranked else "fail"


def safe_relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def check_file_ready(project_root: Path, relative_path: str, label: str) -> FileCheck:
    file_path = project_root / normalize_relpath(relative_path)
    if not file_path.exists():
        return FileCheck(label, normalize_relpath(relative_path), False, "file_missing")
    text = read_text(file_path)
    if is_placeholder_text(text):
        return FileCheck(
            label,
            normalize_relpath(relative_path),
            False,
            "placeholder_stub_detected",
        )
    return FileCheck(label, normalize_relpath(relative_path), True, "implemented")


def build_file_checks(project_root: Path, runtime_profile: str) -> list[FileCheck]:
    checks = [
        check_file_ready(project_root, "scripts/train.py", "train_entrypoint"),
        check_file_ready(project_root, "src/data/datasets.py", "dataset_module"),
    ]
    if runtime_profile == "full_training_runtime":
        checks.extend(
            [
                check_file_ready(project_root, "src/engine/trainer.py", "trainer"),
                check_file_ready(project_root, "src/models/__init__.py", "model_registry"),
                check_file_ready(project_root, "src/models/unet.py", "model_module"),
                check_file_ready(project_root, "src/losses/seg_losses.py", "loss_module"),
            ]
        )
    return checks


def inspect_image(path: Path) -> dict[str, Any]:
    if Image is None:
        return {
            "status": "partial",
            "reason": "pillow_not_available",
            "size": None,
            "mode": None,
            "extrema": None,
            "unique_values": None,
        }
    try:
        with Image.open(path) as image:
            image.load()
            colors = image.getcolors(maxcolors=2048)
            if colors is None:
                unique_values: list[str] | None = [">2048_unique_values"]
            else:
                unique_values = [str(color) for _, color in colors[:16]]
            return {
                "status": "pass",
                "reason": "image_readable",
                "size": [image.size[1], image.size[0]],
                "mode": image.mode,
                "extrema": image.getextrema(),
                "unique_values": unique_values,
            }
    except Exception as exc:  # pragma: no cover - depends on local files
        return {
            "status": "fail",
            "reason": f"image_read_error:{exc}",
            "size": None,
            "mode": None,
            "extrema": None,
            "unique_values": None,
        }


def discover_raw_sample(
    project_root: Path,
    dataset_code: str,
    split_name: str,
    sample_index: int,
) -> dict[str, Any]:
    dataset_code = normalize_relpath(dataset_code).lower()
    if dataset_code != "glas":
        return {
            "status": "fail",
            "reason": f"raw_sample_discovery_not_supported:{dataset_code or 'unknown'}",
            "source": "raw_asset_discovery",
        }

    split_to_prefix = {
        "train": "train_",
        "val": "train_",
        "testA": "testA_",
        "testB": "testB_",
        "test": "testA_",
    }
    dataset_root = project_root / "datasets" / "01_GlaS_official_raw"
    prefix = split_to_prefix.get(split_name, "train_")
    if not dataset_root.exists():
        return {
            "status": "fail",
            "reason": f"dataset_root_missing:{safe_relpath(dataset_root, project_root)}",
            "source": "raw_asset_discovery",
        }

    image_paths = sorted(
        path
        for path in dataset_root.glob(f"{prefix}*.bmp")
        if not path.name.endswith("_anno.bmp")
    )
    if not image_paths:
        return {
            "status": "fail",
            "reason": f"no_images_for_prefix:{prefix}",
            "source": "raw_asset_discovery",
        }
    if sample_index < 0 or sample_index >= len(image_paths):
        return {
            "status": "fail",
            "reason": f"sample_index_out_of_range:{sample_index}/{len(image_paths)}",
            "source": "raw_asset_discovery",
        }

    image_path = image_paths[sample_index]
    mask_path = image_path.with_name(f"{image_path.stem}_anno{image_path.suffix}")
    image_info = inspect_image(image_path)
    mask_info = inspect_image(mask_path) if mask_path.exists() else {"status": "fail", "reason": "mask_missing"}
    status = "pass"
    if image_info.get("status") != "pass" or mask_info.get("status") != "pass":
        status = "partial"
    return {
        "status": status,
        "reason": "raw_assets_readable" if status == "pass" else "raw_assets_partial",
        "source": "raw_asset_discovery",
        "split_name": split_name,
        "split_csv": None,
        "sample_id": image_path.stem,
        "image_path": safe_relpath(image_path, project_root),
        "mask_path": safe_relpath(mask_path, project_root),
        "image_exists": image_path.exists(),
        "mask_exists": mask_path.exists(),
        "image_shape_hw": image_info.get("size"),
        "image_dtype": "uint8" if image_info.get("size") else None,
        "image_mode": image_info.get("mode"),
        "mask_shape_hw": mask_info.get("size"),
        "mask_dtype": "uint8" if mask_info.get("size") else None,
        "mask_mode": mask_info.get("mode"),
        "mask_unique_values": mask_info.get("unique_values"),
        "image_extrema": image_info.get("extrema"),
        "mask_extrema": mask_info.get("extrema"),
    }


def load_sample_evidence(
    project_root: Path,
    experiment_config: dict[str, Any],
    data_config: dict[str, Any] | None,
    split_name: str,
    sample_index: int,
) -> dict[str, Any]:
    if data_config:
        split_dir = project_root / normalize_relpath(str(data_config.get("split_dir", "")))
        csv_files = data_config.get("csv_files", {})
        if isinstance(csv_files, dict):
            csv_name = csv_files.get(split_name)
            if csv_name:
                csv_path = split_dir / normalize_relpath(str(csv_name))
                if csv_path.exists():
                    with csv_path.open("r", encoding="utf-8", newline="") as handle:
                        rows = list(csv.DictReader(handle))
                    if 0 <= sample_index < len(rows):
                        row = rows[sample_index]
                        image_path = project_root / normalize_relpath(row.get("image_relpath", ""))
                        mask_path = project_root / normalize_relpath(row.get("mask_relpath", ""))
                        image_info = inspect_image(image_path) if image_path.exists() else {"status": "fail", "reason": "image_missing"}
                        mask_info = inspect_image(mask_path) if mask_path.exists() else {"status": "fail", "reason": "mask_missing"}
                        status = "pass"
                        if image_info.get("status") != "pass" or mask_info.get("status") != "pass":
                            status = "partial"
                        return {
                            "status": status,
                            "reason": "split_csv_sample_readable" if status == "pass" else "split_csv_sample_partial",
                            "source": "split_csv",
                            "split_name": split_name,
                            "split_csv": safe_relpath(csv_path, project_root),
                            "sample_id": row.get("sample_id", ""),
                            "image_path": safe_relpath(image_path, project_root),
                            "mask_path": safe_relpath(mask_path, project_root),
                            "image_exists": image_path.exists(),
                            "mask_exists": mask_path.exists(),
                            "image_shape_hw": image_info.get("size"),
                            "image_dtype": "uint8" if image_info.get("size") else None,
                            "image_mode": image_info.get("mode"),
                            "mask_shape_hw": mask_info.get("size"),
                            "mask_dtype": "uint8" if mask_info.get("size") else None,
                            "mask_mode": mask_info.get("mode"),
                            "mask_unique_values": mask_info.get("unique_values"),
                            "image_extrema": image_info.get("extrema"),
                            "mask_extrema": mask_info.get("extrema"),
                        }
    dataset_code = str(experiment_config.get("dataset_code", ""))
    return discover_raw_sample(project_root, dataset_code, split_name, sample_index)


def collect_config_resolution(
    project_root: Path,
    experiment_config: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    config_refs = experiment_config.get("config_refs", {})
    if not isinstance(config_refs, dict):
        return {"config_refs": {}, "resolved": {}, "missing": ["config_refs_mapping_missing"]}, ["config_refs_mapping_missing"]

    resolved: dict[str, Any] = {}
    missing: list[str] = []
    for key, raw_path in config_refs.items():
        rel_path = normalize_relpath(str(raw_path))
        config_path = (project_root / rel_path).resolve()
        exists = config_path.exists()
        resolved[key] = {
            "relative_path": rel_path,
            "exists": exists,
        }
        if not exists:
            missing.append(f"{key}:{rel_path}")
    return {"config_refs": config_refs, "resolved": resolved, "missing": missing}, missing


def build_runtime_command(
    project_root: Path,
    experiment_config_rel: str,
    run_name: str,
    train_runtime_output_path: Path,
    args: argparse.Namespace,
) -> list[str]:
    return [
        sys.executable,
        str(project_root / "scripts" / "train.py"),
        "--config",
        experiment_config_rel,
        "--run-name",
        run_name,
        "--runtime-check",
        "--runtime-check-output",
        safe_relpath(train_runtime_output_path, project_root),
        "--device",
        args.device,
        "--max-steps",
        str(args.max_steps),
    ]


def run_formal_runtime_check(
    project_root: Path,
    experiment_config_rel: str,
    experiment_config: dict[str, Any],
    train_runtime_output_path: Path,
    log_output_path: Path,
    args: argparse.Namespace,
    file_checks: list[FileCheck],
    missing_configs: list[str],
) -> dict[str, Any]:
    blocking_reasons: list[str] = []
    if missing_configs:
        blocking_reasons.extend([f"missing_config:{item}" for item in missing_configs])
    for file_check in file_checks:
        if not file_check.ready:
            blocking_reasons.append(f"{file_check.label}:{file_check.reason}")

    command = build_runtime_command(
        project_root,
        experiment_config_rel,
        str(experiment_config.get("run_name", "runtime_check")),
        train_runtime_output_path,
        args,
    )
    record: dict[str, Any] = {
        "attempted": False,
        "mode": "train_runtime_check_cli",
        "command": command,
        "cwd": project_root.as_posix(),
        "exit_code": None,
        "timed_out": False,
        "stdout_log": safe_relpath(log_output_path, project_root),
        "train_runtime_output": safe_relpath(train_runtime_output_path, project_root),
        "blocking_reasons": blocking_reasons,
        "payload": {},
        "status": "fail" if blocking_reasons else "partial",
        "reason": "blocked_before_subprocess" if blocking_reasons else "subprocess_not_run",
    }

    if train_runtime_output_path.exists():
        train_runtime_output_path.unlink()

    if blocking_reasons:
        log_output_path.write_text(
            "[runtime_check] blocked before subprocess\n"
            + "\n".join(f"- {item}" for item in blocking_reasons)
            + "\n",
            encoding="utf-8",
        )
        return record

    try:
        completed = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=args.timeout_seconds,
            check=False,
        )
        record["attempted"] = True
        record["exit_code"] = completed.returncode
        log_output_path.write_text(
            "[runtime_check] stdout\n"
            + completed.stdout
            + "\n[runtime_check] stderr\n"
            + completed.stderr,
            encoding="utf-8",
        )
    except subprocess.TimeoutExpired as exc:
        record["attempted"] = True
        record["timed_out"] = True
        record["status"] = "fail"
        record["reason"] = f"timeout_after_{args.timeout_seconds}s"
        log_output_path.write_text(
            "[runtime_check] timeout\n"
            + (exc.stdout or "")
            + "\n[runtime_check] stderr\n"
            + (exc.stderr or ""),
            encoding="utf-8",
        )
        return record

    if record["exit_code"] != 0:
        record["status"] = "fail"
        record["reason"] = f"subprocess_exit_{record['exit_code']}"
        return record

    if not train_runtime_output_path.exists():
        record["status"] = "fail"
        record["reason"] = "runtime_payload_missing"
        return record

    try:
        payload = load_json_mapping(train_runtime_output_path)
    except Exception as exc:  # pragma: no cover - depends on local payload
        record["status"] = "fail"
        record["reason"] = f"runtime_payload_invalid:{exc}"
        return record

    record["payload"] = payload
    record["status"] = "pass"
    record["reason"] = "runtime_payload_loaded"
    return record


def stringify_list(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, list):
        return str(value)
    return str(value)


def is_finite_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, str):
        try:
            return math.isfinite(float(value))
        except ValueError:
            return False
    return False


def extract_runtime_fields(sample_evidence: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    runtime_fields = {
        "sample_path": payload.get("sample_path") or sample_evidence.get("image_path"),
        "sample_id": payload.get("sample_id") or sample_evidence.get("sample_id"),
        "input_shape": payload.get("input_shape"),
        "input_dtype": payload.get("input_dtype"),
        "target_shape": payload.get("target_shape"),
        "target_dtype": payload.get("target_dtype"),
        "target_unique_values": payload.get("target_unique_values") or sample_evidence.get("mask_unique_values"),
        "output_shape": payload.get("output_shape"),
        "output_dtype": payload.get("output_dtype"),
        "loss_value": payload.get("loss_value"),
        "loss_is_finite": payload.get("loss_is_finite"),
        "backward_executed": payload.get("backward_executed"),
        "optimizer_step_executed": payload.get("optimizer_step_executed"),
    }
    return runtime_fields


def make_runtime_statuses(
    sample_evidence: dict[str, Any],
    execution: dict[str, Any],
    runtime_fields: dict[str, Any],
    runtime_profile: str,
) -> list[RuntimeStatus]:
    payload = execution.get("payload", {})
    attempted = bool(execution.get("attempted"))
    successful_runtime = execution.get("status") == "pass"
    sample_available = sample_evidence.get("status") in {"pass", "partial"}
    dataloader_ready = (
        successful_runtime
        and runtime_fields.get("sample_path")
        and runtime_fields.get("sample_id")
        and runtime_fields.get("input_shape")
        and runtime_fields.get("input_dtype")
        and runtime_fields.get("target_shape")
        and runtime_fields.get("target_dtype")
    )
    tensor_ready = dataloader_ready and runtime_fields.get("output_shape") and runtime_fields.get("output_dtype")
    loss_ready = (
        tensor_ready
        and is_finite_number(runtime_fields.get("loss_value"))
        and bool(runtime_fields.get("loss_is_finite")) is True
    )
    grad_ready = (
        loss_ready
        and bool(runtime_fields.get("backward_executed"))
        and bool(runtime_fields.get("optimizer_step_executed"))
    )

    if successful_runtime and payload.get("entrypoint_check_pass") is True:
        smoke_status = "pass"
        smoke_reason = "formal runtime-check subprocess completed and confirmed formal asset entrypoint checks"
    elif attempted:
        smoke_status = "fail"
        smoke_reason = f"formal runtime-check subprocess failed: {execution.get('reason', 'unknown')}"
    else:
        smoke_status = "fail"
        smoke_reason = f"formal runtime-check subprocess was blocked: {', '.join(execution.get('blocking_reasons', [])) or execution.get('reason', 'unknown')}"

    if dataloader_ready:
        batch_status = "pass"
        batch_reason = "formal runtime payload contains sample path/id and input/target tensor metadata"
    elif sample_available:
        batch_status = "partial"
        batch_reason = (
            "raw sample assets are readable, but no truthful formal dataloader batch evidence was produced"
        )
    else:
        batch_status = "fail"
        batch_reason = f"sample evidence unavailable: {sample_evidence.get('reason', 'unknown')}"

    if runtime_profile == "data_protocol_preflight":
        if dataloader_ready:
            tensor_status = "pass"
            tensor_reason = "preflight payload contains input/target tensor shape and dtype for the formal asset chain"
        elif sample_available:
            tensor_status = "partial"
            tensor_reason = "raw sample assets exist, but preflight tensor metadata is still missing"
        else:
            tensor_status = "fail"
            tensor_reason = f"preflight tensor evidence blocked at sample stage: {sample_evidence.get('reason', 'unknown')}"

        loss_status = "not_applicable"
        loss_reason = "data protocol preflight stops before model/loss execution"
        grad_status = "not_applicable"
        grad_reason = "data protocol preflight stops before backward and optimizer.step"
    else:
        if tensor_ready:
            tensor_status = "pass"
            tensor_reason = "formal runtime payload contains input/target/output tensor shape and dtype"
        elif sample_available:
            tensor_status = "partial"
            tensor_reason = "raw sample assets exist, but formal tensor evidence is still missing"
        else:
            tensor_status = "fail"
            tensor_reason = f"tensor evidence blocked at sample stage: {sample_evidence.get('reason', 'unknown')}"

        loss_status = "pass" if loss_ready else "fail"
        loss_reason = (
            f"loss_value={runtime_fields.get('loss_value')} and loss_is_finite=True"
            if loss_ready
            else f"loss finite evidence missing or non-finite: {payload.get('loss_value', runtime_fields.get('loss_value'))}"
        )

        grad_status = "pass" if grad_ready else "fail"
        grad_reason = (
            "formal runtime payload confirms backward and optimizer.step"
            if grad_ready
            else "formal runtime payload does not confirm both backward and optimizer.step"
        )

    return [
        RuntimeStatus("smoke_run_pass", smoke_status, smoke_reason),
        RuntimeStatus("dataloader_batch_check_pass", batch_status, batch_reason),
        RuntimeStatus("tensor_shape_dtype_pass", tensor_status, tensor_reason),
        RuntimeStatus("loss_finite_pass", loss_status, loss_reason),
        RuntimeStatus("grad_step_pass", grad_status, grad_reason),
    ]


def summarize_statuses(statuses: list[RuntimeStatus]) -> str:
    current = "pass"
    for item in statuses:
        current = combine_status(current, item.status)
    return current


def build_runtime_evidence(
    project_root: Path,
    experiment_config_rel: str,
    experiment_config: dict[str, Any],
    config_resolution: dict[str, Any],
    file_checks: list[FileCheck],
    sample_evidence: dict[str, Any],
    execution: dict[str, Any],
    runtime_fields: dict[str, Any],
    runtime_statuses: list[RuntimeStatus],
    evidence_output_path: Path,
    log_output_path: Path,
) -> dict[str, Any]:
    checks = {item.key: item.status for item in runtime_statuses}
    evidence = {
        "project_root": project_root.as_posix(),
        "experiment_config": experiment_config_rel,
        "run_name": experiment_config.get("run_name"),
        "stage_code": experiment_config.get("stage_code"),
        "dataset_code": experiment_config.get("dataset_code"),
        "model_code": experiment_config.get("model_code"),
        "runtime_profile": infer_runtime_profile(experiment_config),
        "config_resolution": config_resolution,
        "formal_chain_readiness": [asdict(item) for item in file_checks],
        "raw_sample_evidence": sample_evidence,
        "runtime_execution": execution,
        "runtime_fields": runtime_fields,
        "checks": checks,
        "overall_status": summarize_statuses(runtime_statuses),
        "runtime_evidence_json": safe_relpath(evidence_output_path, project_root),
        "runtime_log": safe_relpath(log_output_path, project_root),
    }
    return evidence


def build_report(
    project_root: Path,
    experiment_config_rel: str,
    experiment_config: dict[str, Any],
    config_resolution: dict[str, Any],
    file_checks: list[FileCheck],
    sample_evidence: dict[str, Any],
    execution: dict[str, Any],
    runtime_fields: dict[str, Any],
    runtime_statuses: list[RuntimeStatus],
    evidence_output_path: Path,
    log_output_path: Path,
) -> str:
    overall_status = summarize_statuses(runtime_statuses)
    lines = [
        "# Runtime Check Report",
        "",
        "## 1. Inputs",
        f"- project_root: `{project_root.as_posix()}`",
        f"- experiment_config: `{experiment_config_rel}`",
        f"- run_name: `{experiment_config.get('run_name', 'unknown')}`",
        f"- stage_code: `{experiment_config.get('stage_code', 'unknown')}`",
        f"- dataset_code: `{experiment_config.get('dataset_code', 'unknown')}`",
        f"- model_code: `{experiment_config.get('model_code', 'unknown')}`",
        f"- runtime_profile: `{infer_runtime_profile(experiment_config)}`",
        "",
        "## 2. Config Resolution",
    ]
    resolved = config_resolution.get("resolved", {})
    for key in ("data", "model", "train", "eval"):
        entry = resolved.get(key)
        if not entry:
            continue
        status = "pass" if entry.get("exists") else "fail"
        lines.append(f"- {key}_config_exists: `{status}` -> `{entry.get('relative_path')}`")
    missing_configs = config_resolution.get("missing", [])
    lines.append(
        f"- missing_configs: `{', '.join(missing_configs) if missing_configs else 'none'}`"
    )
    lines.extend(
        [
            "",
            "## 3. Formal Chain Readiness",
        ]
    )
    for check in file_checks:
        status = "pass" if check.ready else "fail"
        lines.append(
            f"- {check.label}: `{status}` -> `{check.relative_path}` ({check.reason})"
        )
    lines.extend(
        [
            "",
            "## 4. Raw Sample Evidence",
            f"- sample_source: `{sample_evidence.get('source')}`",
            f"- sample_status: `{sample_evidence.get('status')}`",
            f"- sample_reason: `{sample_evidence.get('reason')}`",
            f"- split_name: `{sample_evidence.get('split_name')}`",
            f"- split_csv: `{sample_evidence.get('split_csv')}`",
            f"- sample_id: `{sample_evidence.get('sample_id')}`",
            f"- image_path: `{sample_evidence.get('image_path')}`",
            f"- mask_path: `{sample_evidence.get('mask_path')}`",
            f"- image_shape_hw: `{stringify_list(sample_evidence.get('image_shape_hw'))}`",
            f"- image_dtype: `{sample_evidence.get('image_dtype')}`",
            f"- mask_shape_hw: `{stringify_list(sample_evidence.get('mask_shape_hw'))}`",
            f"- mask_dtype: `{sample_evidence.get('mask_dtype')}`",
            f"- mask_unique_values: `{stringify_list(sample_evidence.get('mask_unique_values'))}`",
            "",
            "## 5. Formal Runtime Execution",
            f"- runtime_execution_attempted: `{execution.get('attempted')}`",
            f"- runtime_execution_status: `{execution.get('status')}`",
            f"- runtime_execution_reason: `{execution.get('reason')}`",
            f"- runtime_execution_exit_code: `{execution.get('exit_code')}`",
            f"- runtime_blocking_reasons: `{stringify_list(execution.get('blocking_reasons'))}`",
            f"- runtime_command: `{ ' '.join(execution.get('command', [])) }`",
            f"- runtime_log: `{safe_relpath(log_output_path, project_root)}`",
            f"- runtime_evidence_json: `{safe_relpath(evidence_output_path, project_root)}`",
            "",
            "## 6. Runtime Fields",
            f"- sample_path: `{runtime_fields.get('sample_path')}`",
            f"- sample_id: `{runtime_fields.get('sample_id')}`",
            f"- input_shape: `{stringify_list(runtime_fields.get('input_shape'))}`",
            f"- input_dtype: `{runtime_fields.get('input_dtype')}`",
            f"- target_shape: `{stringify_list(runtime_fields.get('target_shape'))}`",
            f"- target_dtype: `{runtime_fields.get('target_dtype')}`",
            f"- target_unique_values: `{stringify_list(runtime_fields.get('target_unique_values'))}`",
            f"- output_shape: `{stringify_list(runtime_fields.get('output_shape'))}`",
            f"- output_dtype: `{runtime_fields.get('output_dtype')}`",
            f"- loss_value: `{runtime_fields.get('loss_value')}`",
            f"- loss_is_finite: `{runtime_fields.get('loss_is_finite')}`",
            f"- backward_executed: `{runtime_fields.get('backward_executed')}`",
            f"- optimizer_step_executed: `{runtime_fields.get('optimizer_step_executed')}`",
            "",
            "## 7. Runtime Check Status",
        ]
    )
    for item in runtime_statuses:
        lines.append(f"- {item.key}: {item.status} ({item.reason})")
    lines.extend(
        [
            "",
            "## 8. Conclusion",
            f"- runtime_check_status: `{overall_status}`",
            "- truthful_interpretation: only evidence produced by the formal runtime subprocess may upgrade this report to `pass`; supporting raw-asset inspection alone cannot do that.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    experiment_config_rel = normalize_relpath(args.experiment_config)
    experiment_config_path = (project_root / experiment_config_rel).resolve()
    if not experiment_config_path.exists():
        raise SystemExit(f"Experiment config does not exist: {experiment_config_path}")

    output_path = (project_root / normalize_relpath(args.output)).resolve()
    evidence_output_path = (project_root / normalize_relpath(args.evidence_output)).resolve()
    log_output_path = (project_root / normalize_relpath(args.log_output)).resolve()
    train_runtime_output_path = (
        project_root / normalize_relpath(args.train_runtime_output)
    ).resolve()
    for path in (output_path, evidence_output_path, log_output_path, train_runtime_output_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    experiment_config = load_yaml_mapping(experiment_config_path)
    runtime_profile = infer_runtime_profile(experiment_config)
    config_resolution, missing_configs = collect_config_resolution(project_root, experiment_config)
    data_entry = config_resolution.get("resolved", {}).get("data", {})
    data_config: dict[str, Any] | None = None
    if data_entry.get("exists"):
        data_config = load_yaml_mapping((project_root / data_entry["relative_path"]).resolve())

    file_checks = build_file_checks(project_root, runtime_profile)
    sample_evidence = load_sample_evidence(
        project_root,
        experiment_config,
        data_config,
        args.split,
        args.sample_index,
    )
    execution = run_formal_runtime_check(
        project_root,
        experiment_config_rel,
        experiment_config,
        train_runtime_output_path,
        log_output_path,
        args,
        file_checks,
        missing_configs,
    )
    runtime_fields = extract_runtime_fields(sample_evidence, execution.get("payload", {}))
    runtime_statuses = make_runtime_statuses(sample_evidence, execution, runtime_fields, runtime_profile)
    runtime_evidence = build_runtime_evidence(
        project_root,
        experiment_config_rel,
        experiment_config,
        config_resolution,
        file_checks,
        sample_evidence,
        execution,
        runtime_fields,
        runtime_statuses,
        evidence_output_path,
        log_output_path,
    )
    evidence_output_path.write_text(
        json.dumps(runtime_evidence, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    output_path.write_text(
        build_report(
            project_root,
            experiment_config_rel,
            experiment_config,
            config_resolution,
            file_checks,
            sample_evidence,
            execution,
            runtime_fields,
            runtime_statuses,
            evidence_output_path,
            log_output_path,
        ),
        encoding="utf-8",
    )

    overall_status = summarize_statuses(runtime_statuses)
    print(f"runtime_check_status={overall_status}")
    print(f"report_path={output_path.as_posix()}")
    print(f"runtime_evidence_json={evidence_output_path.as_posix()}")
    print(f"runtime_log={log_output_path.as_posix()}")
    for item in runtime_statuses:
        print(f"{item.key}={item.status}")
    return 0 if overall_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
