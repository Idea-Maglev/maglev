# Design

## 1. 当前判断

“把代码仓库改用 submodule 管理”不是一个小实现点，而是一项新的接入模型决策。

它至少改变三件事：

1. Maglev wrapper 项目如何绑定下游代码仓库
2. `init` 如何创建代码仓库工作区
3. `update` 是否需要承接 submodule pointer 的同步语义

## 2. 当前默认不直接实施

在没有完成决策前，不应直接把：

- `git clone`

替换成：

- `git submodule add`

原因是这样做会在未完成结构收口时，直接改写：

1. 初始化行为
2. 配置模型
3. 团队协作模型

## 3. 当前需要比较的三个方案

### A. Reject

维持现状：

1. 继续使用普通 `git clone`
2. repository_map 只记录路径和描述
3. 不把代码仓库 revision 绑定进 wrapper

### B. Optional / Recommended

引入双模式：

1. 默认仍可 `git clone`
2. 对需要强环境一致性的项目，允许或推荐使用 submodule
3. `bootstrapper` 需要显式询问接入模式

### C. Default

把 submodule 升为新默认：

1. `init` 的外部仓库登记默认走 `git submodule add`
2. `.maglev/config.json` 需要记录 submodule 管理状态
3. `update` 需要定义 submodule 是否同步、如何同步

## 4. 当前最关键的比较标准

本轮不是比较“哪个更优雅”，而是比较：

1. 哪种方式最能保证多仓库环境可复现
2. 哪种方式最不容易制造新的协作灾难
3. 哪种方式最容易被 `init / update` 正式承接

## 5. 影响面预告

如果后续进入实现，预计至少会改：

1. `packages/maglev-cli/dist/maglev_installer.py`
2. `maglev-bootstrapper`
3. `maglev-updater`
4. `docs/guides/20_operations/maglev_init_manual.md`
5. `specs/10_reality/repository_map.md`
6. `.maglev/config.json` 的相关字段说明
