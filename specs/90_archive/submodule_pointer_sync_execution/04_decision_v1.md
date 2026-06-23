# Pointer Sync Decision v1

> 状态：首版决策已形成
> 结论档位：`Explicit Only`

## 1. 第一层结论

当前不建议：

- `Default in Update`

当前更合理的结论是：

- `Explicit Only`

也就是说，如果 Maglev 后续允许 submodule pointer sync，这个能力也必须通过显式触发进入，而不是混入常规 `update`。

## 2. 为什么不是 `Reject`

完全拒绝 pointer sync 也不合理，因为 submodule 模式一旦存在，就迟早会遇到一种真实需求：

- 本地工作区与 wrapper 当前记录的 revision 不一致，团队需要一个正式恢复动作

如果 Maglev 永远不承接这件事，用户最终仍会回到手工 Git 操作，无法保持统一解释和阻断规则。

## 3. 为什么不是 `Default in Update`

把 pointer sync 混进默认 `update` 的问题在于：

1. 常规 `update` 当前语义是更新 Maglev 资产，不是推进业务代码版本
2. 用户执行 `update` 时，不一定意识到会触及 submodule revision
3. 一旦同步发生，wrapper 项目会出现新的 pointer 变化，提交语义显著升级

因此默认自动执行仍然不可接受。

## 4. 第二层结论：首轮只考虑哪种同步

在 `Explicit Only` 前提下，当前首轮只建议考虑：

- `sync-to-recorded`

当前不建议首轮进入：

- `sync-to-latest`

## 5. 为什么首轮只允许 `sync-to-recorded`

因为它的语义更稳：

1. 它是在恢复 wrapper 已经记录的现实
2. 它不是主动推进业务仓库版本
3. 风险相对可解释，也更容易加入阻断条件

反过来，`sync-to-latest` 的本质是：

1. 推进业务代码版本
2. 改变团队当前工作的代码现实
3. 需要更强的审批、提交和分支约束

这已经超出当前主题的首轮安全边界。

## 6. 当前建议的执行形态

如果后续进入实现，当前更合理的执行形态是：

1. 显式 flag
   - 例如 `update --sync-submodules`
2. 执行语义先固定为 `sync-to-recorded`
3. 执行前必须给出风险确认
4. 执行后必须提示 wrapper 项目可能出现 pointer 变化

## 7. 当前建议的阻断规则

至少在下面这些情况阻断执行：

1. submodule 本地有未提交改动
2. `.gitmodules` 缺失或损坏
3. `.maglev/config.json` 中没有登记 `management_mode = submodule`
4. 用户没有显式确认这是高风险动作

## 8. 当前封板结论

到这一步，当前主题已经从“问题提出”进入“有明确决策”状态：

1. `Explicit Only`
2. 首轮仅考虑 `sync-to-recorded`
3. `sync-to-latest` 暂不进入首轮实现
