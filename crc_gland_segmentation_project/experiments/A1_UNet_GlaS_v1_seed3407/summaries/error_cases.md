# Error Cases

- failure_taxonomy_version: `failure_taxonomy_v1`
- source_assets: `testA_metrics.csv`, `testB_metrics.csv`, `predictions/testA/*`, `predictions/testB/*`
- analyzed_sample_count: `80`

## Split Summary

### testA

- sample_count: `60`
- adhesion_merge: `48`
- fragmented_complex_region: `11`
- boundary_over_smooth: `1`

### testB

- sample_count: `20`
- adhesion_merge: `10`
- fragmented_complex_region: `6`
- small_gland_miss: `3`
- boundary_over_smooth: `1`

## Worst Cases

- `testA` / `GlaS_official_testA_testA_21` / `failure_type=adhesion_merge` / `objdice=0.341479` / `dice=0.741725` / `boundary_f1=0.446804` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_21_overlay.png`
- `testA` / `GlaS_official_testA_testA_45` / `failure_type=adhesion_merge` / `objdice=0.361464` / `dice=0.757293` / `boundary_f1=0.303729` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_45_overlay.png`
- `testA` / `GlaS_official_testA_testA_54` / `failure_type=adhesion_merge` / `objdice=0.374931` / `dice=0.894477` / `boundary_f1=0.608513` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_54_overlay.png`
- `testB` / `GlaS_official_testB_testB_16` / `failure_type=adhesion_merge` / `objdice=0.377239` / `dice=0.822674` / `boundary_f1=0.406740` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testB/GlaS_official_testB_testB_16_overlay.png`
- `testA` / `GlaS_official_testA_testA_43` / `failure_type=adhesion_merge` / `objdice=0.390681` / `dice=0.924841` / `boundary_f1=0.662095` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_43_overlay.png`
- `testA` / `GlaS_official_testA_testA_10` / `failure_type=adhesion_merge` / `objdice=0.406440` / `dice=0.837828` / `boundary_f1=0.529012` / `overlay=experiments/A1_UNet_GlaS_v1_seed3407/visuals/testA/GlaS_official_testA_testA_10_overlay.png`
