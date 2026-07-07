# tools 目录分层说明

- `stage01_data_protocol/`: `01_数据协议` 的 A 类正式工具入口
- `c_pending_review/`: 当前已登记但尚未裁决为 A/B 的 C 类脚本

固定规则:

- 后续编号阶段新增 A 类正式工具时,进入新的 `tools/stageXX_[阶段名]/`
- B 类 gate / runtime / check / enforce 真实实现不进入本目录,统一放在 `b_class_auxiliary/tools/`
- C 类脚本在交付前清理前统一暂放 `tools/c_pending_review/`
