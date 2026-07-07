# Project Source Root

This directory stores the restarted formal source modules.

## Current Scope

- `src/data/`
  - rebuilt in this round for data-config parsing, CSV schema validation, and
    dataset path resolution

## Deferred Scope

- model, engine, loss, and evaluation modules are intentionally not recreated
  in this round because `01_数据协议` is only allowed to restore the formal
  input layer
