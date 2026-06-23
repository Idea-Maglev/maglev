# Submodule Adoption Implementation Spec v1

> 状态：首版 implementation spec 已形成
> 基于决策：`Optional / Recommended`

## 1. 实现目标

在不推翻当前 `git clone` 模型的前提下，为 Maglev 化项目增加一个正式的 `submodule` 接入模式。

本轮目标不是把所有项目强制迁到 submodule，而是做到：

1. `init` 可以显式选择仓库接入模式
2. `repository_map.md` 能表达仓库管理方式
3. `.maglev/config.json` 能记录仓库是 `clone` 还是 `submodule`
4. `update` 至少能识别并解释 submodule 状态

## 2. `init` 交互设计

### 2.1 新的交互层级

当前 `interactive_questionnaire()` 里只有：

1. 是否注册子仓库
2. 仓库 URL
3. 仓库简述

新增后建议变成：

1. 是否注册子仓库
2. 仓库接入模式
   - `clone`
   - `submodule`
3. 仓库 URL
4. 本地路径
5. 仓库简述

### 2.2 默认值

基于当前决策，默认值建议：

- `clone`

原因：

1. 当前结论是 `Optional / Recommended`
2. 不应让现有最小接入用户被动承担 submodule 成本

### 2.3 子仓库模式文案

建议在交互中明确写成：

1. `clone`
   - 本地直接拉取仓库目录，适合最小接入
2. `submodule`
   - 由当前 Maglev 项目托管仓库 revision，适合多仓库可复现工作台

## 3. installer 行为设计

### 3.1 `clone` 模式

保留当前行为：

- `git clone <url> <local_path>`

### 3.2 `submodule` 模式

新增行为建议：

- `git submodule add <url> <local_path>`

首轮边界：

1. 只承接 `submodule add`
2. 不在 `init` 阶段自动切换 submodule 分支
3. 不在 `init` 阶段自动执行复杂 pointer 策略

### 3.3 dry-run 表达

`--dry-run` 时应明确区分：

1. `Would clone <url> into <path>`
2. `Would add submodule <url> into <path>`

不能继续都叫 `clone`。

## 4. `.maglev/config.json` schema 扩展

当前仓库记录大致是：

```json
{
  "name": "repo-a",
  "git_url": "git@github.com:example/repo-a.git",
  "local_path": "./repo-a",
  "description": "示例仓库",
  "clone_status": "success"
}
```

建议扩展成：

```json
{
  "name": "repo-a",
  "git_url": "git@github.com:example/repo-a.git",
  "local_path": "./repo-a",
  "description": "示例仓库",
  "management_mode": "clone",
  "repo_status": "success"
}
```

或在 submodule 模式下：

```json
{
  "name": "repo-a",
  "git_url": "git@github.com:example/repo-a.git",
  "local_path": "./repo-a",
  "description": "示例仓库",
  "management_mode": "submodule",
  "repo_status": "success"
}
```

### 4.1 字段迁移建议

建议：

1. 新增 `management_mode`
2. 用更通用的 `repo_status` 替换 `clone_status`
3. 首轮不强制记录 revision hash

原因：

1. 先把管理方式表达清楚
2. revision 记录可以在后续子主题再补

## 5. `repository_map.md` 表达方式

当前 `repository_map.md` 只表达：

1. 名称
2. 路径
3. 类型
4. 状态
5. 描述

如果引入 submodule，建议新增一列：

- `管理方式`

例如：

| 仓库名称 | 路径 | 类型 | 管理方式 | 状态 | 描述 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| frontend | `./frontend` | Frontend | clone | Active | Vue 前端 |
| backend | `./backend` | Backend | submodule | Active | Go 后端 |

这样 AI 和用户都能直接理解该仓库是普通目录还是受 submodule 托管。

## 6. `update` 设计

当前建议首轮只做：

1. 识别项目中是否存在 submodule 模式仓库
2. 检查 submodule 工作区是否已初始化
3. 在 `update` 输出中解释 submodule 当前状态

当前不建议首轮直接做：

1. 自动更新 submodule pointer
2. 自动执行 `git submodule update --remote`
3. 自动切换 submodule 分支

### 6.1 推荐首轮行为

`maglev-updater` / installer 对 submodule 的首轮行为应是：

1. `observe`
2. `report`
3. `recommend`

而不是：

1. `auto-sync`

## 7. 用户手册更新要求

一旦进入实现，至少应同步更新：

1. `maglev_init_manual.md`
2. `maglev_update_manual.md`

并明确写出：

1. 哪些场景适合 `clone`
2. 哪些场景适合 `submodule`
3. submodule 模式需要团队额外理解哪些 Git 行为

## 8. 首轮验收标准

进入实现后，至少应满足：

1. `init` 能显式区分 `clone` 和 `submodule`
2. `.maglev/config.json` 能表达管理方式
3. `repository_map.md` 能表达管理方式
4. `update --dry-run` 能识别 submodule 项目并解释当前状态
5. 没有把 submodule 自动同步逻辑混进首轮实现

## 9. 当前实现状态

当前已完成：

1. installer 交互层已支持 `clone / submodule` 二选一
2. `--dry-run` 已能区分 `Would clone` 与 `Would add submodule`
3. `.maglev/config.json` 已开始写入 `management_mode` 与 `repo_status`
4. `repository_map.md` 已开始写入 `管理方式`
5. `update` 已开始识别已登记的 submodule 仓库，并输出状态观察结果

当前尚未完成：

1. `update` 的自动 pointer 同步策略

当前已补：

2. `maglev_init_manual.md` / `maglev_update_manual.md` 的用户手册同步
