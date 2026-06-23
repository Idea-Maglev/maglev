# target runtime names v1

> 状态：已完成
> 作用：为主流程核心四对象提供一版推荐的目标 runtime names，作为后续真正物理 rename 的执行目标。

## 1. 命名原则

当前采用以下原则：

1. 使用 kebab-case
2. 不直接照搬中文正式动作名
3. 不继续拟合历史前缀 `maglev-`
4. 优先体现对象职责，而不是保留历史实现语义
5. 与已有 `canonical_name_active` 对象风格保持相近

## 2. 推荐目标名

### A. `maglev-standup`

当前正式动作名：

- `现状同步`

推荐目标 runtime name：

- `reality-sync`

理由：

- 比 `standup` 更贴近当前结构职责
- 比 `session-bootstrap` 更短，也更接近当前真实用途
- 与 Reality / current state 语义一致

### B. `maglev-create-spec`

当前正式动作名：

- `方案设计`

推荐目标 runtime name：

- `spec-designer`

理由：

- 已在元数据草案中出现过示例
- 比 `create-spec` 更强调“设计对象”而不是“生成动作”
- 能保留它与 Spec 产物的强关联

### C. `maglev-quick-dev`

当前正式动作名：

- `上下文实施`

推荐目标 runtime name：

- `context-implementer`

理由：

- 去掉了 `quick` 的误导语义
- 明确它承接的是基于上下文的实施动作
- 与对象当前职责更一致

### D. `maglev-cross-validate`

当前正式动作名：

- `综合验证`

推荐目标 runtime name：

- `integrated-validator`

理由：

- 比 `cross-validate` 更贴近“主流程汇聚验证”角色
- 可避免继续把它理解成单纯字面交叉比对
- 与质量层三面的边界更清楚

## 3. 当前结论

当前推荐的未来目标 runtime names 是：

1. `maglev-standup` -> `reality-sync`
2. `maglev-create-spec` -> `spec-designer`
3. `maglev-quick-dev` -> `context-implementer`
4. `maglev-cross-validate` -> `integrated-validator`

## 4. 给人的理解方式

为了避免这些英文 runtime names 只对结构清楚、对人不直观，当前推荐始终配合角色化解释：

- `reality-sync`
  更适合对人解释成：先把当前项目现状、风险和下一步对齐的入口。
- `spec-designer`
  更适合对人解释成：把需求收成可执行方案的对象。
- `context-implementer`
  更适合对人解释成：在方案明确后推进实现和自检的对象。
- `integrated-validator`
  更适合对人解释成：把需求、方案、代码、测试重新拉回同一条线上检查的对象。

也就是说，runtime name 用于对象分发和治理；
面向人的解释，仍应优先保留：

1. `现状同步`
2. `方案设计`
3. `上下文实施`
4. `综合验证`

## 5. 说明

这份文档当前只是 execution 目标名建议，不等于已经执行 rename。

后续若进入真正 execution：

1. 应先按这份目标名作为执行目标
2. 若其中某个名称被证明仍有明显歧义，再在 execution 主题内单点调整
