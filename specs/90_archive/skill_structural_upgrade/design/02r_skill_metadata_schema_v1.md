# skill结构性升级 Skill 元数据草案 v1

> 状态：进行中
> 作用：保留后续治理、分发和入口解释所需的最小元数据字段。
> 完整展开归档：
> - `archive/02r_skill_metadata_schema_v1_full.md`

## 1. 目标

当前元数据草案只解决 4 个问题：

1. 这个对象承接什么能力
2. 它位于哪一层
3. 它当前是什么形态
4. 它应如何被解释、分发和治理

补充约束：

- `SKILL.md` frontmatter 应保持标准格式
- 非触发型但有治理价值的稳定字段，优先放进 `metadata`
- catalog 与治理文档继续承接跨对象和会变化的判断

## 2. 最小字段集合

当前建议的最小字段集合如下：

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| `id` | 稳定对象标识 | `maglev-create-spec` |
| `canonical_skill_name` | 未来正式 skill 名 | `spec-designer` |
| `formal_action_name` | 当前正式动作名 | `方案设计` |
| `runtime_name_status` | 当前运行面命名状态 | `active_legacy_name` |
| `distribution_scope` | 当前分发范围 | `user_visible` |
| `top_level_capability` | 所属顶层能力 | `方案设计` |
| `exposure_level` | 用户显性 / 体系显性 / 体系内部 | `用户显性` |
| `system_layer` | 所属系统承接层 | `Core Flow Layer` |
| `object_kind` | 对象形态 | `skill` / `workflow` / `module` / `surface` / `cluster` / `context_object` |
| `lifecycle_chain` | 所属生命周期链 | `main_flow` |
| `author` | 当前对象作者 | `Maglev contributors` |
| `last_updated` | 最后更新时间 | `2026-03-30` |
| `current_direction` | 当前治理方向 | `Keep` |
| `naming_readiness` | 当前定名准备度 | `formal_ready` |
| `removal_status` | 是否已从运行面移除 | `active` |

## 3. 关键字段解释

### A. `formal_action_name`

用于统一 README、Reality、设计文档和入口口径，描述“这个对象在做什么”。

### B. `canonical_skill_name`

用于记录未来正式 skill 名。若对象当前不是 skill，或名称尚未定稿，可为空。

### C. `runtime_name_status`

用于区分：

1. `active_legacy_name`
2. `canonical_name_active`

避免把结构动作名误读成已完成物理改名。

### D. `object_kind`

用于强制先判“这是什么对象”，再讨论要不要把它当 skill。

当前建议枚举：

1. `skill`
2. `workflow`
3. `module`
4. `surface`
5. `cluster`
6. `context_object`

### E. `distribution_scope`

用于区分治理清单、运行面和用户分发面。

当前建议枚举：

1. `user_visible`
2. `runtime_internal`
3. `private_only`

### F. `author` / `last_updated`

用于提供最小可追溯信息。

规则：

- `author` 优先取当前 git 账号
- 若当前作用域取不到 git 账号，则不要伪造
- `last_updated` 使用当前日期，格式统一为 `YYYY-MM-DD`

## 4. 放置规则

### A. `SKILL.md`

保留标准顶层字段：

1. `name`
2. `description`

自定义治理字段统一放进：

- `metadata`

### B. `.agents/workflows/*.md`

同样保持顶层字段克制，自定义治理字段统一放进：

- `metadata`

最低建议字段：

1. `formal_action_name`
2. `object_kind`
3. `author`
4. `last_updated`

### C. `.agents/private-catalog.yaml`

用于承接跨对象检索、分组、巡逻和分发范围判断。

### D. 治理快照文档

用于承接会变化的判断字段，例如：

1. `current_direction`
2. `naming_readiness`
3. `removal_status`
4. `risk_type`

## 5. 示例

### `maglev-standup`

```yaml
id: maglev-standup
canonical_skill_name: null
formal_action_name: 现状同步
runtime_name_status: active_legacy_name
distribution_scope: user_visible
top_level_capability: 现状同步
exposure_level: 用户显性
system_layer: Core Flow Layer
object_kind: skill
lifecycle_chain: main_flow
author: Maglev contributors
last_updated: 2026-03-30
current_direction: Keep
naming_readiness: formal_ready
removal_status: active
```

### `requirement-convergence`

```yaml
id: requirement-convergence
canonical_skill_name: null
formal_action_name: 需求收敛
runtime_name_status: canonical_name_active
distribution_scope: user_visible
top_level_capability: 需求收敛
exposure_level: 用户显性
system_layer: Core Flow Layer
object_kind: workflow
lifecycle_chain: main_flow
author: Maglev contributors
last_updated: 2026-03-30
current_direction: Workflow-first
naming_readiness: semantic_only
removal_status: active
```

## 6. 当前结论

当前最稳的做法是：

- 对象本体承载最小标准 frontmatter + `metadata`
- catalog / workflow 承载分发与编排层字段
- 治理快照承载会变化的判断字段

后续新增或改造对象时，优先复用这套最小元数据集合，而不是继续扩一张更大的表。
