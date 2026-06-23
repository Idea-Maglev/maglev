# runtime rename migration

> 作用：承接 `runtime_name_strategy` 的 readiness 结论，专门盘清主流程核心四对象的 rename 影响面、双写统一面与迁移 checklist。

## 主入口

- `02_design.md`
- `04_impact_surface_inventory_v1.md`
- `05_migration_checklist_v1.md`
- `06_private_catalog_migration_strategy_v1.md`
- `07_execution_readiness_decision_v1.md`

## 当前说明

这轮主题不再重判正式动作名，也不再重判是否需要 rename。

本主题只处理三件事：

1. 主流程核心四对象的 rename 影响面盘点
2. 双写统一的优先顺序
3. 真正进入物理 rename 之前必须满足的迁移 checklist

当前样板性入口文档与阶段总结已收敛，保留设计、inventory、checklist、catalog 策略与 readiness 决策。
