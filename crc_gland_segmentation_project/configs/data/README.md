# Project Data Config Root

This directory stores the formal data configs frozen by `01_数据协议`.

## Formal Configs

- `configs/data/glas.yaml`
  - frozen for `GlaS train68 / val17 / testA60 / testB20`
- `configs/data/crag.yaml`
  - frozen for `CRAG train153 / val20 / test40`

## Current Reality

- the config files now define the formal data protocol interface
- the split CSV assets have been regenerated from the current project-local
  dataset roots
- training code must not bypass these configs even after the dataset assets are
  restored and frozen
