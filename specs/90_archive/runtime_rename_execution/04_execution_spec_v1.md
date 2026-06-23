# runtime rename execution spec v1

> 状态：已完成
> 作用：为主流程核心四对象未来的 `skill-only` rename execution 提供正式执行规格。

## 1. 执行对象

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 2. 推荐执行顺序

当前推荐顺序：

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

### 顺序理由

- `maglev-standup` 位于最前段，但 relation 影响面最容易理解，适合作为第一轮试点对象
- `maglev-create-spec` 是唯一同时被 `entry-router` 与 `requirement-convergence` 直接指向的主设计对象，应在前段试点成功后再推进
- `maglev-quick-dev` 主要承接实施阶段，依赖面相对比 `create-spec` 更简单
- `maglev-cross-validate` 同时被质量层三面 complement 指向，关系最密，适合最后处理

## 3. 单对象执行框架

未来真正执行每个对象时，统一按以下顺序：

1. 修改 skill 目录名
2. 修改该对象在 `.agents/private-catalog.yaml` 中的 `name`
3. 修改该对象在 `.agents/private-catalog.yaml` 中的 `path`
4. 修改所有受影响的 `relations.target`
5. 运行一致性搜索，确认旧名不再作为 active relation target 存在
6. 最后再将该对象的 `runtime_name_status` 切到 `canonical_name_active`

## 4. 每步后的最小验证

每处理完一个对象，至少验证：

### A. 目录与对象定义层

1. skill 新目录存在
2. 旧目录已退出运行面
3. catalog 中该对象的 `name` 与 `path` 已对应

### B. relation 层

1. catalog 中该对象相关的 `relations.target` 已全部同步
2. 不再残留旧 target 与新 target 混写

### C. 协作层

1. `entry-router` / `requirement-convergence` / 质量层三面在 catalog 里的 target 关系仍可解析
2. 不存在因为单对象 rename 导致的关系断链

## 5. 暂停条件

出现以下任一情况，应暂停 execution：

1. catalog 中出现对象 `name` 已改，但 relation target 仍大量残留旧名
2. `path` 已改，但目录结构与 catalog 不一致
3. 无法确认某一对象的 relation 影响面已经收干净
4. 单对象执行后，路由或分组对象的 target 关系出现断链

## 6. 回滚边界

当前推荐：

1. 一次 execution 最多只处理一个对象
2. 若单对象执行后验证未通过，直接回滚该对象本轮改动
3. 不允许在前一个对象尚未验证通过时继续推进下一个对象

## 7. 当前结论

这份 execution spec 已足够作为后续真正物理 rename 的直接执行底稿。

也就是说，下一步如果继续，已经不需要再开“判断型主题”，而是可以开始对第一个对象做真实 execution。
