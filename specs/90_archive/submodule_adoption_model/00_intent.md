# Intent

## 1. 当前目标

评估 Maglev 化项目下托管的代码仓库，是否应从当前的普通 `git clone` 管理方式切换为 `git submodule` 管理方式。

## 2. 要解决的问题

当前 `init` 对外部代码仓库的处理，本质上仍是：

1. 记录 `git_url`
2. 决定 `local_path`
3. 尝试执行 `git clone`

这种方式虽然简单，但有两个明显问题：

1. Maglev wrapper 项目无法稳定记录下游代码仓库所绑定的 revision
2. 不同开发者本地环境很容易出现“目录结构一致，但代码版本不一致”的漂移

## 3. 当前要回答的决策问题

1. `git submodule` 是否值得成为新的标准接入方式
2. 如果值得，是“默认强制”还是“推荐模式”
3. 它会如何影响 `init`、`update`、`repository_map.md`、`.maglev/config.json` 和协作说明
