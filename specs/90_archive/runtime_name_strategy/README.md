# runtime name 策略专项收口

> 作用：承接 `skill结构性升级` 封板后的下一轮主题，专门处理结构动作名、运行面名称与迁移顺序之间的收口策略。

## 主入口

- `02_design.md`
- `04_core_flow_rename_execution_strategy_v1.md`
- `05_core_flow_rename_readiness_assessment_v1.md`

## 当前说明

这轮主题不再重判对象边界，也不再处理 spec pipeline 内部化。

本主题只回答三件事：

1. 哪些对象仍处于 `active_legacy_name`
2. 哪些对象应继续保持兼容，不急于物理改名
3. 哪些对象已具备进入运行面 rename 回合的条件

当前已新增主流程核心四对象的执行策略落点：

- `04_core_flow_rename_execution_strategy_v1.md`

当前已完成 readiness 判断：

- `05_core_flow_rename_readiness_assessment_v1.md`

当前样板性入口文档已收敛，保留阅读价值最高的设计、执行策略与 readiness 结论。

后续 migration 主题已独立为：

- [../runtime_rename_migration/README.md](../runtime_rename_migration/README.md)
