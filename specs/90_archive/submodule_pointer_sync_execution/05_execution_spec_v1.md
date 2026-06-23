# Pointer Sync Execution Spec v1

> 状态：首版 execution spec
> 作用范围：仅覆盖 `sync-to-recorded`

## 1. 首轮执行范围

当前首轮 execution spec 只覆盖：

- `sync-to-recorded`

当前明确不覆盖：

- `sync-to-latest`
- 自动推进远端最新 revision
- 常规 `update` 中的隐式 pointer 同步

## 2. 执行目标

本轮执行目标不是推进业务代码版本，而是恢复 wrapper 当前已经记录的 submodule 现实。

也就是说，动作语义应固定为：

1. 读取 wrapper 当前记录的 submodule revision
2. 将本地 submodule 工作区恢复到该 revision
3. 向用户解释恢复结果与残留风险

## 3. 建议触发形态

当前最合理的首轮触发形态是：

1. 在 `update` 体系下增加显式 flag
2. flag 语义固定为 `sync-to-recorded`

建议形态示例：

- `maglev update --sync-submodules`

**实施前需要决策的命令侧细节**（2026-05-18 reality-recheck 补注）：

当前 `packages/maglev-cli/dist/maglev_installer.py` 的 argparse 是 positional 风格 `command ∈ {init, update}` + 顶层 flags（`--upstream / --dry-run / --force / --skip-prompt / --local-dist`），**没有 subparser**。`maglev update --sync-submodules` 这种 update 子命令 flag 形态有两种落地路径，需在实施 PR 起步前二选一：

- **A. 顶层 flag**（最小侵入）：`--sync-submodules` 直接作为顶层 flag，仅在 `command == "update"` 时生效；若与 init 同时给则报错。改动最小。
- **B. 引入 subparser**：把 init/update 改成 subcommand，再在 update 下挂 `--sync-submodules`。语义更干净，但触及 installer 主结构，需评估对 npx 包装层 / dist catalog / runtime-src 同步的连锁影响。

首轮倾向 A，但需要在 design / decision 文档补一条 v2 决策记录后再进入实现。

当前不建议：

- 在默认 `update` 中隐式执行
- 在 `init` 中自动执行
- 通过普通 `dry-run` 自动替用户推进 pointer

## 4. 执行前输入与前提

进入执行前，至少需要满足下面这些前提：

1. 当前项目存在 `.maglev/config.json`
2. 至少有一个仓库被登记为 `management_mode = submodule`
3. `.gitmodules` 存在且可读取
4. 当前 wrapper 项目本身处于可解释状态

如果以上任一前提不满足，应直接阻断，不进入同步动作。

## 5. 首轮阻断条件

首轮至少应阻断下面这些情况：

1. submodule 本地存在未提交改动
2. submodule 目录缺失
3. submodule 未初始化
4. `.gitmodules` 缺失或损坏
5. `.maglev/config.json` 与 `.gitmodules` 对同一路径的登记不一致
6. 用户未显式确认这是恢复性高风险动作

## 6. 首轮不阻断但需提示的情况

下面这些情况首轮可以不阻断，但必须明确提示：

1. 当前没有任何需要恢复的 submodule
2. 某些 submodule 已经对齐 recorded revision
3. wrapper 仓库在同步后可能出现 git status 变化

## 7. 建议执行步骤

首轮执行步骤建议固定为：

1. 读取 `.maglev/config.json`
2. 识别所有 `management_mode = submodule` 的仓库
3. 校验 `.gitmodules` 与本地目录状态
4. 对每个 submodule 检查是否存在本地未提交改动
5. 向用户输出即将恢复的目标列表
6. 在用户显式确认后执行 `sync-to-recorded`
7. 输出每个 submodule 的恢复结果
8. 提示 wrapper 仓库是否出现 pointer 相关变化

## 8. 用户确认点

首轮建议至少保留一个显式确认点，确认内容应包括：

1. 这是恢复到 wrapper 已记录 revision，不是拉取远端最新代码
2. 该动作会改动本地 submodule 工作区状态
3. 如果 wrapper 记录与本地现实不一致，执行后可能出现新的 git status 提示

如果用户没有确认，应直接退出，不做任何同步。

## 9. 执行后输出要求

执行后至少应向用户输出：

1. 哪些 submodule 被处理
2. 哪些已经对齐，无需恢复
3. 哪些因阻断条件未处理
4. 是否建议下一步执行 `git status`
5. 如果 wrapper 项目出现 pointer 变化，应提示用户自行评估是否提交

## 10. 当前明确不做

当前 execution spec 明确不做：

1. 自动提交 wrapper 项目
2. 自动推送 submodule 远端分支
3. 自动将 submodule 推进到远端最新 commit
4. 绕过本地未提交改动直接强制同步

## 11. 下一步实现落点

如果后续进入真实实现，当前更合理的落点是：

1. 先扩展 `packages/maglev-cli/dist/maglev_installer.py`
2. 让 `maglev-updater` 承接结果解释
3. 先做 `--dry-run` 预览，再进入真实执行

当前不建议一上来增加独立的新安装器脚本。

## 12. 已有起点：check_submodule_repos（2026-05-18 reality-recheck 新增）

实施起步时不需要从零构建探测层。当前 `maglev_installer.py` 中 `check_submodule_repos(project_root)` 已返回结构化 report：

```python
{
  "status": "none" | "ready" | "attention" | "unknown",
  "registered": [{name, local_path, working_tree_state}, ...],
  "reasons": [...],
  "suggestions": [...],
}
```

`working_tree_state ∈ {ready, missing, incomplete, unknown}`，再加上 `.gitmodules` 存在性检查，已天然覆盖本规格 §5 阻断条件的多数情形。pointer sync 实施只需在此报告之上：

- 加 "本地未提交改动" 检查（§5 条 1，当前 check_submodule_repos 未做 `git diff`）
- 加 ".maglev/config.json 与 .gitmodules 一致性" 检查（§5 条 5）
- 加 "wrapper 记录的 revision 探测"（pointer sync 特有，当前完全缺失）
- 加用户显式确认前置（§5 条 6）

`maglev-updater` skill 引用 reasons/suggestions 透传给用户即可，不需要单独发明输出格式。
