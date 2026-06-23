# runtime rename execution preflight

> 作用：承接 `runtime_rename_migration` 的 readiness 结论，在真正进入物理 rename execution 之前，补齐最后两项执行前规格。

## 主入口

- `02_design.md`
- `04_migration_shape_decision_v1.md`
- `05_catalog_relation_checklist_v1.md`

## 当前说明

这轮主题不直接执行物理 rename。

本主题只处理两件事：

1. 决定 `skill-only` 还是 `skill + workflow` 的迁移方案
2. 形成 relation-level 的 catalog migration checklist

当前样板性入口文档已收敛，保留 preflight 设计与两份执行前关键结论。

后续 execution 主题已落到：

- [../runtime_rename_execution/README.md](../runtime_rename_execution/README.md)
