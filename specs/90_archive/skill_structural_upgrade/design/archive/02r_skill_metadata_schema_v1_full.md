# skill结构性升级 Skill 元数据草案 v1

> 状态：进行中
> 作用：为后续 skill 治理、分发、入口解释与结构升级提供一组最小可执行元数据字段。

## 1. 目标

这份元数据草案不追求一次覆盖所有信息，而是先保证后续系统能稳定回答：

1. 这个对象承接什么能力
2. 它位于哪一层
3. 它当前是什么形态
4. 它应如何被解释、分发和治理

补充约束：

- `SKILL.md` frontmatter 当前应保持 Codex skill 的最小标准格式
- 本文中的字段是治理元数据字段，不等于都应写入 `SKILL.md` frontmatter 顶层
- 对于确实需要随 skill 本体同行、但不参与触发判断的稳定字段，应优先放进 `metadata`

## 2. 设计原则

当前元数据设计优先满足：

1. 先服务结构治理，再考虑展示美观
2. 先支持批量分析，再支持细节扩展
3. 先区分能力、形态、生命周期，再区分具体实现
4. 字段数量保持克制，避免又造一个难维护的大表

## 3. 最小字段集合

当前建议的最小字段集合如下：

| 字段 | 含义 | 示例 |
| :--- | :--- | :--- |
| `id` | 稳定对象标识，通常等于当前对象名 | `maglev-create-spec` |
| `canonical_skill_name` | 未来正式 skill 名；若当前尚未定稿或当前不是 skill，可为空 | `spec-designer` |
| `formal_action_name` | 当前正式动作名或正式结构名 | `方案设计` |
| `runtime_name_status` | 当前运行面命名状态 | `active_legacy_name` |
| `distribution_scope` | 当前分发范围 | `user_visible` |
| `top_level_capability` | 所属顶层能力 | `方案设计` |
| `exposure_level` | 用户显性 / 体系显性 / 体系内部 | `用户显性` |
| `system_layer` | 所属系统承接层 | `Core Flow Layer` |
| `object_kind` | 对象形态 | `skill` / `workflow` / `module` / `surface` / `cluster` / `context_object` |
| `lifecycle_chain` | 所属生命周期链 | `main_flow` / `thinking_archive` / `crystallization` / `integration` / `evolution` |
| `author` | 当前 skill 作者 | `Maglev contributors` |
| `last_updated` | 最后更新时间 | `2026-03-30` |
| `current_direction` | 当前治理方向 | `Keep` / `Rename` / `Demote` / `Merge` / `Workflow-first` / `Observe` |
| `naming_readiness` | 当前定名准备度 | `formal_ready` / `semantic_only` / `removed` |
| `removal_status` | 是否已从运行面移除 | `active` / `removed` |

## 4. 字段解释

### A. `formal_action_name`

作用：

- 统一 README、Reality、设计文档和后续入口口径
- 描述“这个对象在做什么”
- 不要求等于未来正式 skill 名

当前典型值：

- `现状同步`
- `方案设计`
- `上下文实施`
- `综合验证`

### B. `canonical_skill_name`

作用：

- 记录未来正式 skill 名
- 只在对象确实应以 skill 形态存在时填写

补充说明：

- 它可以不同于 `formal_action_name`
- 它也不需要继续拟合历史对象名
- 若当前对象仍是 `workflow` / `cluster` / `surface`，该字段可暂为空

### C. `runtime_name_status`

作用：

- 区分“结构动作名已稳定”和“运行面名字是否已经切换”
- 避免后续把结构动作名误读成已完成物理改名

当前建议枚举：

1. `active_legacy_name`
2. `canonical_name_active`

### D. `object_kind`

作用：

- 强制先判“这是什么对象”，再讨论要不要把它当 skill

当前建议枚举：

1. `skill`
2. `workflow`
3. `module`
4. `surface`
5. `cluster`
6. `context_object`

### E. `distribution_scope`

作用：

- 区分“进入治理清单”与“对用户分发可见”不是同一件事
- 防止把运行面内部对象误判成用户公开对象

当前建议枚举：

1. `user_visible`
2. `runtime_internal`
3. `private_only`

### F. `lifecycle_chain`

作用：

- 避免不同生命周期对象继续共用同一个语义入口

当前建议枚举：

1. `main_flow`
2. `thinking_archive`
3. `crystallization`
4. `integration`
5. `evolution`

### G. `author`

作用：

- 标记当前 skill 的作者信息
- 为后续维护和追责提供最小可追溯信息

规则：

- 默认优先读取当前仓库作用域下的 git 账号
- 若当前作用域取不到 git 账号，则不要伪造作者名称
- 允许留空或由用户手动补充

### H. `last_updated`

作用：

- 标记当前 skill 最近一次被确认更新的日期
- 为维护者判断信息新鲜度提供最小依据

规则：

- 使用当前日期
- 格式统一为 `YYYY-MM-DD`

### G. `naming_readiness`

作用：

- 区分“结构已成立”和“名称已定稿”

当前建议枚举：

1. `formal_ready`
2. `semantic_only`
3. `removed`

## 5. 示例映射

### A. `maglev-standup`

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

### B. `需求收敛`

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

### C. `knowledge-check`

```yaml
id: knowledge-check
canonical_skill_name: knowledge-check
formal_action_name: 知识沉淀检查
runtime_name_status: canonical_name_active
distribution_scope: runtime_internal
top_level_capability: 思考沉淀
exposure_level: 体系内部
system_layer: Quality / Guardrail Layer
object_kind: skill
lifecycle_chain: thinking_archive
author: Maglev contributors
last_updated: 2026-03-30
current_direction: Keep
naming_readiness: formal_ready
removal_status: active
```

### D. `maglev-create-spec`

```yaml
id: maglev-create-spec
canonical_skill_name: null
formal_action_name: 方案设计
runtime_name_status: active_legacy_name
distribution_scope: user_visible
top_level_capability: 方案设计
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

说明：

- 这里故意保持 `canonical_skill_name: null`
- 因为当前我们已经有正式动作名，但还没有要求未来正式 skill 名必须立即定稿

## 6. 当前第一批建议落字段的对象

当前最适合先落这组元数据的，不是全量 skill，而是三类高价值对象：

### A. 已接近正式定名的主流程对象

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

### B. 当前 `Workflow-first` 对象

1. `需求收敛`
2. `现实结晶`

### C. 当前已完成替换的高风险旧对象

1. `atomizer` -> `entry-router`
2. `maglev_archival_check` -> `knowledge-check`

## 7. 当前结论

这版元数据草案 v1 的作用，是把前面已经稳定的结构判断转成后续系统可消费的字段面。

它当前最重要的价值有三个：

1. 让 `skill-squadron` 的批量分析字段可以向真正的元数据层过渡
2. 让正式动作名、对象形态和治理方向进入同一套结构
3. 为后续 skill 文件、索引和分发口径统一提供落点

补充结论：

- 从现在开始，后续命名讨论应明确区分：
  - `formal_action_name`
  - `canonical_skill_name`
  - `runtime_name_status`
  - `distribution_scope`
  - `removal_status`
