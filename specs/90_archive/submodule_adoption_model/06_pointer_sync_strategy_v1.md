# Submodule Pointer Sync Strategy v1

> 状态：首版策略已形成
> 当前结论：`不默认自动同步`

## 1. 核心结论

当前不建议把 submodule pointer 同步做成 `update` 的默认自动行为。

当前更合理的策略是：

1. `update` 默认只做观察、解释和建议
2. pointer 同步应作为后续显式动作引入
3. 在没有单独确认前，不应在常规 `update` 中自动执行 `git submodule update --remote`

## 2. 为什么不能默认自动同步

submodule pointer 同步和普通 Maglev 资产更新不同，它会直接改变下游代码仓库所指向的 revision。

这会带来三类风险：

1. 代码版本跳变
   - 当前项目的代码现实会一起变化，不再只是 Maglev 资产更新
2. 团队预期错位
   - 某些团队可能只想更新 Maglev 自身，不想顺带推进业务仓库版本
3. 提交语义变复杂
   - wrapper 项目会出现“Maglev 资产更新 + submodule pointer 变化”混合提交

## 3. 当前建议的三档策略

### A. `observe`

只检查并报告：

1. 是否登记了 submodule
2. 工作区是否完整
3. 是否需要用户手动初始化

这是当前已落地的状态。

### B. `recommend`

在检测到 submodule 工作区缺失或未初始化时，给出建议命令：

```bash
git submodule update --init --recursive
```

这也是当前已落地范围的一部分。

### C. `explicit-sync`

未来如果真的要支持 pointer 同步，建议只走显式动作，例如：

1. 单独命令
2. 单独 flag
3. 明确确认步骤

而不是把它混进常规 `update`

## 4. 当前推荐的后续形态

如果后续进入实现，推荐的形态是：

1. 保持 `update` 默认只观察
2. 新增一个显式选项，例如：
   - `update --sync-submodules`
   - 或独立 workflow / skill
3. 在真正执行 pointer 同步前，再次提示风险并要求确认

## 5. 执行前必须回答的问题

如果未来要做显式 pointer 同步，至少要先回答：

1. 是同步到 `.gitmodules` / 当前 pointer 所要求的 revision
   - 还是同步到远端最新分支
2. 如果本地 submodule 有未提交改动，如何处理
3. pointer 变化是否应回写到 wrapper 项目并提示提交
4. 团队是否允许 `update` 触及业务代码现实

## 6. 当前对 `maglev-updater` 的约束

在这份策略生效前，`maglev-updater` 应保持：

1. 识别 submodule 状态
2. 解释当前风险
3. 给出建议命令

但不应：

1. 自动同步 pointer
2. 自动切换 submodule 分支
3. 自动提交 wrapper 项目中的 pointer 变化

## 7. 当前建议

当前这条主题到这里已经足够进入封板准备。

如果后续继续推进，应该单独开一个更窄的新主题，例如：

- `submodule_pointer_sync_execution`

而不是继续把高风险自动同步逻辑塞回当前 implementation 主题。
