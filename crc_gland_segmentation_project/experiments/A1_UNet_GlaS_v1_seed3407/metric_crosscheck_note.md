# Metric Crosscheck Note

- crosscheck_scope: `python_reaggregation_from_split_csv`
- official_reference_type: `project_internal_reaggregation_sanity_check`
- threshold_source: `val17`
- threshold_value: `0.5`
- metric_crosscheck_result: `pass`
- boundary_metric_width: `3`
- boundary_metric_impl: `binary_erosion_xor_plus_binary_dilation`
- connected_components_connectivity: `8`

## Split Checks

### testA

- sample_count: `60`
- sampled_ids: `GlaS_official_testA_testA_1, GlaS_official_testA_testA_10, GlaS_official_testA_testA_11, GlaS_official_testA_testA_12, GlaS_official_testA_testA_13`
- `objdice`: sample_mean=`0.6941893856375374` / aggregate=`0.6941893856375373` / status=`pass`
- `dice`: sample_mean=`0.8654398833523302` / aggregate=`0.8654398833523301` / status=`pass`
- `iou`: sample_mean=`0.7734292115380336` / aggregate=`0.7734292115380336` / status=`pass`
- `f1`: sample_mean=`0.8654398833523302` / aggregate=`0.8654398833523301` / status=`pass`
- `boundary_f1`: sample_mean=`0.6110884138696463` / aggregate=`0.6110884138696463` / status=`pass`
- `hd95`: sample_mean=`57.3055351893107` / aggregate=`57.305535189310696` / status=`pass`
- `object_hausdorff`: sample_mean=`140.98546768742966` / aggregate=`140.98546768742966` / status=`pass`

### testB

- sample_count: `20`
- sampled_ids: `GlaS_official_testB_testB_1, GlaS_official_testB_testB_10, GlaS_official_testB_testB_11, GlaS_official_testB_testB_12, GlaS_official_testB_testB_13`
- `objdice`: sample_mean=`0.7619798771629788` / aggregate=`0.7619798771629787` / status=`pass`
- `dice`: sample_mean=`0.8730129078649844` / aggregate=`0.8730129078649842` / status=`pass`
- `iou`: sample_mean=`0.7848204239589237` / aggregate=`0.7848204239589236` / status=`pass`
- `f1`: sample_mean=`0.8730129078649844` / aggregate=`0.8730129078649842` / status=`pass`
- `boundary_f1`: sample_mean=`0.6059969204962079` / aggregate=`0.6059969204962081` / status=`pass`
- `hd95`: sample_mean=`39.11294776678085` / aggregate=`39.11294776678085` / status=`pass`
- `object_hausdorff`: sample_mean=`132.50118776506844` / aggregate=`132.5011877650684` / status=`pass`

