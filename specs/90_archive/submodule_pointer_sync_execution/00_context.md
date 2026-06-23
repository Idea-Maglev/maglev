# Context

## 1. 上游前提

`submodule_adoption_model` 已经形成下面这些稳定前提：

1. `clone` 仍是默认模式
2. `submodule` 是正式可选模式
3. `update` 当前只观察和解释 submodule 状态
4. pointer sync 当前明确不是默认自动行为

## 1.5 自首版以来的现实漂移（2026-05-18 reality-recheck）

自 2026-04-22 首版决策定稿后，仓库发生两项可能影响实施的演进：

- **distribution_runtime 升级（archived #19 `runtime_distribute_project_index_protocol`）**：引入 `distribution_scope` 校验、dist catalog 拆分、`check_runtime_distribution.py` CI。实施 pointer sync 时需评估：sync-to-recorded 完成后是否触发或绕过此校验链路。当前判断不会，因为 pointer sync 只动 git submodule 工作区，不动 `.maglev/` dist 物料；但应在实施 PR 中显式验证。
- **CLI 入口实测**：`packages/maglev-cli/dist/maglev_installer.py` 当前 argparse 是 positional 风格 `command ∈ {init, update}` + 顶层 flags，**没有 subparser**。`maglev update --sync-submodules` 这种 update 子命令 flag 形态需要先决定加 subparser 还是直接做顶层 flag。详见 `05_execution_spec_v1.md §3`。

## 2. 为什么要单独开主题

pointer sync 和普通 Maglev 资产更新不同，它会直接改变：

1. 下游代码仓库所指向的 commit
2. wrapper 项目中的 submodule pointer 记录
3. 团队当前实际工作的代码现实

因此它不能作为一个“顺手的 update 细节”混入现有主题。

## 3. 当前风险

在没有单独规则前，pointer sync 至少有这些风险：

1. 本地 submodule 未提交改动被覆盖
2. 团队以为只是更新 Maglev，其实推进了业务代码版本
3. wrapper 项目出现 pointer 变化，但用户没意识到需要提交
4. 同步目标不明确：是当前记录的 revision，还是远端最新分支
