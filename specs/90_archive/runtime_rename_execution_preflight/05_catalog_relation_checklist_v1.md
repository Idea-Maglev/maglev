# catalog relation checklist v1

> 状态：已完成
> 作用：为主流程核心四对象未来若执行 `skill-only` rename 时，提供 `.agents/private-catalog.yaml` 的 relation-level 同步清单。

## 1. 对象定义层

未来若执行 `skill-only` rename，四个对象自身必须同步检查：

1. `name`
2. `path`
3. `runtime_name_status`

其中：

- `runtime_name_status` 最后再切

## 2. relation-level 必改清单

### A. `entry-router`

必须同步检查：

1. `entry-router -> maglev-standup`
2. `entry-router -> maglev-create-spec`
3. `entry-router -> maglev-quick-dev`
4. `entry-router -> maglev-cross-validate`

### B. `requirement-convergence`

必须同步检查：

1. `requirement-convergence -> maglev-create-spec`

### C. 质量层三面

必须同步检查：

1. `spec-audit-surface -> maglev-cross-validate`
2. `review-validation-surface -> maglev-cross-validate`
3. `test-design-surface -> maglev-cross-validate`

## 3. 推荐执行顺序

未来真正执行时，推荐顺序：

1. 先改四个对象定义的 `name`
2. 再改相关 `relations.target`
3. 再验证 relation graph 是否已无旧 target 残留
4. 最后再改 `path`
5. 全部完成后才切 `runtime_name_status`

## 4. 最小验证清单

执行后至少应验证：

1. `.agents/private-catalog.yaml` 中，四对象的旧 `name` 是否已被替换
2. relation-level 是否仍残留旧 `target`
3. 受影响对象是否仍能被正确分组、巡逻和路由

## 5. 当前结论

`catalog relation checklist` 现在已经足够作为后续 execution 主题的直接输入。

当前不需要在 preflight 里继续细化到更小粒度。
