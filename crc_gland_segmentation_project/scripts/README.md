# Project Scripts

- status: `minimal_train_entrypoint_restored`
- purpose: hold formal project-local entry scripts required by the frozen execution plan.
- current_reality: `scripts/train.py` now exists as the minimal formal train entrypoint used by the data-stage preflight gate.
- current_boundary: the entrypoint only resolves frozen split assets and emits runtime-check bookkeeping; it does not claim that the `02_UNet流程验证` training chain is already implemented.
- next_stage_requirement: later stage coding should extend this root with experiment configs and truthful runtime evidence without bypassing the frozen data assets.
