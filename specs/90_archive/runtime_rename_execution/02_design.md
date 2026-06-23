# runtime rename execution Design

## 1. 设计目标

把 `skill-only` rename execution 从“知道要做什么”，推进到“知道按什么顺序做、每步如何确认没做坏”。

## 2. 执行对象

本主题只覆盖：

1. `maglev-standup`
2. `maglev-create-spec`
3. `maglev-quick-dev`
4. `maglev-cross-validate`

## 3. 设计重点

### A. 执行顺序必须降低路由断裂风险

由于：

- `entry-router`
- `requirement-convergence`
- 质量层三面

都依赖旧 target 名称，所以 execution 顺序不应随意。

### B. 验证必须分层

每次执行后至少要验证：

1. 目录与对象定义层
2. catalog relation 层
3. 协作对象引用层

### C. 回滚不靠猜

如果任一步后出现：

1. target 残留不一致
2. catalog 对象定义与 path 脱节
3. 协作对象无法继续正确引用

就应暂停，而不是继续推进后续对象。

## 4. 当前结论方向

本主题的目标不是立即 rename，而是导出：

1. 一份正式 execution spec
2. 一份可在真实执行时直接照着走的顺序与验证框架
