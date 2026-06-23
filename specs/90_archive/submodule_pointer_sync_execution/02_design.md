# Design

## 1. 当前倾向

当前最合理的初始倾向是：

- `Explicit Only`

也就是说，如果 Maglev 将来允许 pointer sync，也应作为显式动作执行，而不是混入常规 `update`。

## 2. 为什么默认不考虑 `Default in Update`

因为常规 `update` 当前语义仍是：

1. 更新 Maglev 资产
2. 解释风险
3. 不主动推进业务代码现实

如果把 pointer sync 塞进默认 `update`，就会直接改变这条边界。

## 3. 需要比较的两个执行语义

### A. `sync-to-recorded`

作用：

1. 让本地 submodule 工作区回到 wrapper 当前记录的 revision

更像：

- 修复本地工作区不一致

### B. `sync-to-latest`

作用：

1. 主动推进 submodule pointer 到新的 revision

更像：

- 推进业务仓库版本

这两类动作不应共用同一个默认入口。

## 4. 当前更安全的起点

如果后续进入真实实现，当前更安全的起点是：

1. 先只考虑 `sync-to-recorded`
2. 暂不考虑 `sync-to-latest`

因为前者是在恢复一致性，后者是在推进版本。

## 5. 当前预期的执行形态

当前更合理的形态优先级是：

1. 独立 flag
   - 例如 `update --sync-submodules`
2. 独立 workflow
3. 最后才考虑并入默认 `update`

## 6. 必要阻断条件

至少应阻断下面这些情况：

1. submodule 本地存在未提交改动
2. `.gitmodules` 缺失或损坏
3. `.maglev/config.json` 中未登记 submodule 管理方式
4. 用户未显式确认高风险动作
