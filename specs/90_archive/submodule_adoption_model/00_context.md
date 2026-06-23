# Context

## 1. 当前实现现状

当前 `maglev-bootstrapper` 与 installer 的仓库接入逻辑，仍建立在普通 `git clone` 模型上：

1. `packages/maglev-cli/dist/maglev_installer.py`
   - 交互式收集 `git_url` / `local_path`
   - 尝试执行 `git clone`
   - 将 `clone_status` 写入 `.maglev/config.json`
2. `docs/guides/20_operations/maglev_init_manual.md`
   - 也明确把“Clone 外部仓库”写成当前初始化行为

## 2. 这不是第一次讨论

仓库里已经存在一份历史架构推演：

- `docs/thinking/20_architecture/adoption_model_evolution.md`

其中 `Round 1` 明确反对过“Wrapper Repo + Submodule”的旧方案，核心担忧是：

1. IDE 上下文割裂
2. Git Submodule 工程摩擦高
3. Code / Spec 割裂

## 3. 为什么现在需要重开这个问题

现在与当时不同的地方在于：

1. Maglev 已经形成 npm / npx 的正式分发入口
2. `init` / `update` 执行链路已经存在，可以承接更强的工程约束
3. 当前项目更关注“可复现的多仓库现实”而不只是“先把目录拉下来”

因此，这次不是重新讨论纯 Wrapper 架构，而是讨论：

“在当前分发与接入体系下，代码仓库是否应改为由 submodule 托管”

## 4. 当前边界

本主题当前不直接做：

1. 立刻改 installer
2. 立刻改 init manual
3. 立刻改 `.maglev/config.json` schema

当前先做决策与影响面收口。
