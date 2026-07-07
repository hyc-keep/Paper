# Debug Session: a1-train-stop

- status: `[OPEN]`
- session_id: `a1-train-stop`
- stage: `02_UNet流程验证`
- target_run: `A1_UNet_GlaS_v1_seed3407`
- symptom: `full train only materialized epoch-1 artifacts, then stopped updating files`
- started_at: `2026-07-06`

## Observed Facts

- New formal run directory exists at `experiments/A1_UNet_GlaS_v1_seed3407/`.
- Current physical artifacts stop at `train_log.csv`, `val_metrics.csv`, `checkpoints/best.ckpt`, `checkpoints/last.ckpt`.
- `train_log.csv` currently has only epoch `1`.
- `val_metrics.csv` currently has only epoch `1`.
- Recent process scans did not find a matching `train.py` process for this run.

## Hypotheses

- H1: training process exited unexpectedly right after epoch 1 because of a runtime exception in epoch 2 setup or validation feedback.
- H2: the background command wrapper reported `Running`, but the actual Python training process already exited and left a stale wrapper state.
- H3: the training loop is blocked by file or checkpoint I/O after epoch 1, so assets stop updating without a clean terminal exit.
- H4: the process matching query missed the real worker process, and training is still alive but has not yet reached the next epoch write point.

## Next Actions

- collect stronger runtime evidence without changing business logic
- decide whether to instrument epoch-boundary heartbeat or reproduce in a debug run
- only apply minimal instrumentation first if static evidence is insufficient

## Evidence Update 1

- observation_time: `2026-07-06 19:55:41`
- train_log_last_epoch: `1`
- val_metrics_last_epoch: `1`
- best_ckpt_epoch: `1`
- last_ckpt_epoch: `1`
- matched_python_process_found: `false`

## Hypothesis Status

- H1: `strengthened`
- H2: `strengthened`
- H3: `not_confirmed`
- H4: `weakened`

## Planned Reproduction

- launch an isolated debug run with `--run-name A1_UNet_GlaS_v1_seed3407_debugprobe`
- redirect stdout/stderr to dedicated files
- record PID and file growth without touching business logic

## Evidence Update 2

- isolated_probe_run: `A1_UNet_GlaS_v1_seed3407_debugprobe`
- probe_pid: `7332`
- probe_stderr: `debug-a1-train-stop.stderr.log`
- probe_error: `forrtl: error (200): program aborting due to window-CLOSE event`
- interpretation: `the probe died because of a console/window close event instead of a business-logic exception`

## Hypothesis Status 2

- H1: `weakened`
- H2: `strongly_supported`
- H3: `not_supported`
- H4: `rejected_for_original_run`

## Planned Reproduction 2

- retry isolated launch with `D:/conda_envs/sd/pythonw.exe`
- keep the same training logic and config
- verify whether a window-free process can survive past epoch 1

## Evidence Update 3

- pythonw_probe_run: `A1_UNet_GlaS_v1_seed3407_debugprobe_pythonw`
- pythonw_probe_pid: `3580`
- pythonw_probe_status_time: `2026-07-06 20:03:54`
- pythonw_probe_process_alive: `true`
- pythonw_probe_stderr_empty: `true`
- pythonw_probe_train_log_epoch_1: `written`
- provisional_root_cause: `console-attached background launch triggers window-close termination, while pythonw survives and continues training`

## Decision

- keep business logic unchanged
- switch formal A1 launch method from console-attached background python to `pythonw.exe`
- preserve failed partial official run by archiving before relaunch
