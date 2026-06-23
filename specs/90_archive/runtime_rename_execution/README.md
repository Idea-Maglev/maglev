# runtime rename execution

> 作用：承接 `runtime_rename_execution_preflight` 的最后前置结论，为主流程核心四对象的 `skill-only` rename execution 提供正式执行规格。

上层归档总览可见：

- [specs archive index](../README.md)

## 主入口

- `00_intent.md`
- `00_context.md`
- `01_requirements.md`
- `02_design.md`
- `03_plan.md`
- `04_execution_spec_v1.md`
- `05_target_runtime_names_v1.md`
- `06_standup_rollout_spec_v1.md`
- `07_create_spec_rollout_spec_v1.md`
- `08_quick_dev_rollout_spec_v1.md`
- `09_cross_validate_rollout_spec_v1.md`
- `10_execution_closeout_v1.md`

## 当前说明

本主题已经进入真实 execution，并已完成第一轮试点对象：

1. `maglev-standup` -> `reality-sync`
2. `maglev-create-spec` -> `spec-designer`
3. `maglev-quick-dev` -> `context-implementer`
4. `maglev-cross-validate` -> `integrated-validator`

当前主题已经完成主流程四对象的 `skill-only` rename execution，并进入封板状态。
