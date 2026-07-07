# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `4`

## Split Summary

### testA

- sample_count: `2`
- adhesion_merge: `2`

### testB

- sample_count: `2`
- boundary_over_smooth: `1`
- adhesion_merge: `1`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_1` / `failure_type=adhesion_merge` / `objdice=0.044334` / `dice=0.145651` / `boundary_f1=0.572777` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_1_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.129269` / `dice=0.508682` / `boundary_f1=0.446563` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
- `testB` / `GlaS_official_testB_testB_1` / `failure_type=boundary_over_smooth` / `objdice=0.204663` / `dice=0.522288` / `boundary_f1=0.219285` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_1_overlay.png`
- `testB` / `GlaS_official_testB_testB_10` / `failure_type=adhesion_merge` / `objdice=0.314534` / `dice=0.642589` / `boundary_f1=0.322279` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_10_overlay.png`
