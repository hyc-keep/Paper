# Label Protocol Report

- mask_rule_version: `mask_rule_v1`
- mask_positive_rule: `mask_gt_0`
- mask_disk_value_rule: `0_255`
- input_size: `512x512`
- image_interp: `bilinear`
- mask_interp: `nearest`
- binary_mask_summary_csv: `reports/data_checks/binary_mask_summary.csv`
- total_samples_checked: `378`
- invalid_binary_masks: `0`
- pass_binary_mask: `True`
- pass_dtype: `True`
- invalid_dtype_masks: `0`
- pass_resize_rule: `True`
- resize_rule_failure_count: `0`

## Resize Rule Config Checks

- glas: config=`configs/data/glas.yaml` input_size=`[512, 512]` image_interp=`bilinear` mask_interp=`nearest` status=`pass`
- crag: config=`configs/data/crag.yaml` input_size=`[512, 512]` image_interp=`bilinear` mask_interp=`nearest` status=`pass`

## Conclusion
- note: `formal binary-mask protocol has been checked against all split CSV samples, and resize rule status now requires both frozen config alignment and binary-safe nearest-mask resizing.`
