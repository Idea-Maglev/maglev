# private catalog migration strategy v1

> 状态：已完成
> 作用：为主流程核心四对象未来可能发生的物理 rename 提供 `.agents/private-catalog.yaml` 迁移策略，避免只改 skill 目录名而打断分发、关系图与治理字段。

## 1. 适用对象

本策略只覆盖：

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 2. 当前 catalog 现状

这四个对象当前都表现为：

1. `name` 使用历史运行名
2. `path` 指向历史 skill 目录
3. `formal_action_name` 已稳定
4. `runtime_name_status = active_legacy_name`

同时，至少以下位置仍直接依赖它们的 `name`：

1. `entry-router.relations.target`
2. `requirement-convergence.relations.target`
3. `spec-audit-surface` / `review-validation-surface` / `test-design-surface` 对 `maglev-cross-validate` 的 complement target
4. 其他由 `calls` / `called_by` / `complements` 关系直接引用旧名的节点

因此，catalog 迁移不能只改对象定义本身，必须把 relation graph 一起迁。

## 3. catalog 迁移原则

### A. 一次迁移一组字段

若未来真的执行物理 rename，以下字段必须同轮迁移：

1. `name`
2. `path`
3. 所有 `relations.target`

禁止只改其中一部分。

### B. `formal_action_name` 不是迁移目标

`formal_action_name` 当前已经稳定，不应在 rename migration 中再次修改。

它在迁移中的作用是：

- 作为结构语义真相
- 为运行面 rename 提供映射依据

### C. `runtime_name_status` 必须最后再切

只有在以下条件都满足后，才允许把状态从 `active_legacy_name` 改成 `canonical_name_active`：

1. skill 目录已完成物理 rename
2. workflow 兼容策略已明确
3. catalog 中所有关系 target 已同步
4. 入口与协作对象已不再依赖旧运行名作为唯一标识

## 4. 推荐迁移方式

### Strategy 1: 两阶段 catalog 迁移

当前推荐：

1. 第一阶段只稳定文档、Reality、协作对象中的双写口径
2. 第二阶段才进入 catalog 物理迁移

原因：

- 当前 catalog 既是分发视图，也是关系图输入
- 过早改动会直接放大对路由与巡逻逻辑的影响

### Strategy 2: relation-first checklist

catalog 真正迁移前，必须先逐项复核以下 relation 引用：

1. `entry-router -> maglev-standup`
2. `entry-router -> maglev-create-spec`
3. `entry-router -> maglev-quick-dev`
4. `entry-router -> maglev-cross-validate`
5. `requirement-convergence -> maglev-create-spec`
6. `spec-audit-surface -> maglev-cross-validate`
7. `review-validation-surface -> maglev-cross-validate`
8. `test-design-surface -> maglev-cross-validate`

若这些 target 尚未有统一迁移方案，则不应改 catalog。

## 5. 当前结论

当前最稳的结论不是“可以开始改 catalog”，而是：

1. catalog 已经具备 rename migration 所需治理字段
2. 但当前仍不应直接修改 `name`、`path`、`relations.target`
3. catalog 迁移必须作为真正 rename execution 主题中的集中动作处理

也就是说：

> `runtime_rename_migration` 这轮可以把 catalog 策略定清，但不应在当前主题里直接执行 catalog rename。
