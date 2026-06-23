# Pointer Sync Decision v2

> 状态：v2 增量决策，沿用 v1 全部决策不变
> 增量范围：CLI 落地形态 + flag 语义
> 日期：2026-05-18

## 1. 与 v1 的关系

本文件**不推翻** `04_decision_v1.md` 任何结论。v1 已稳定的：

- `Explicit Only` 触发模型
- 首轮只做 `sync-to-recorded`
- 阻断条件 4 项

v2 仅补充实施层需要先敲定的两项：

1. CLI flag 在 argparse 中的形态（顶层 vs subcommand）
2. flag 语义与 `--skip-prompt` / `--force` / `--dry-run` 的交叉行为

## 2. CLI 落地形态决策：A（顶层 flag）

### 2.1 选项对比

| 维度 | A. 顶层 flag | B. 引入 subparser |
|---|---|---|
| 改动面 | argparse 加 1 个 flag，~3 行 | 重构 init/update 为 subcommand，触及 main()、is_update 判定逻辑、所有调用方 |
| 兼容性 | 完全兼容现有 `maglev update` 调用 | 旧调用可能因 subcommand 解析路径变化报错 |
| 对 npx 包装层影响 | 0 | 需要同步 bin/index.js argparse 转发逻辑 |
| 对 dist catalog / runtime-src 影响 | 0 | 可能触发 check_runtime_distribution.py 校验差异 |
| 语义干净度 | 中（顶层 flag 仅在 update 时生效需要校验） | 高（subcommand 天然限制作用域） |

### 2.2 决策

**选 A：顶层 flag `--sync-submodules`**。理由：

1. 最小侵入原则——首轮实施不应连带重构 installer 主结构
2. 兼容性优先——避免触发 #19 distribution_runtime 升级后的连锁校验
3. 语义干净度可以靠运行时校验补齐（`command != "update"` 时报错）

### 2.3 二次审查触发条件

如果未来出现以下任一情形，应升级到方案 B：

- installer 同时有 ≥3 个 "command 专属" flag（顶层 flag 命名空间污染）
- 需要 init 也支持 sync 的某种变体
- npx 包装层主动重构 argparse 转发

## 3. Flag 行为矩阵

| 场景 | 命令 | 期望行为 |
|---|---|---|
| 默认 | `maglev update --sync-submodules` | 交互确认 → 执行 sync |
| 跳过交互 | `maglev update --sync-submodules --skip-prompt` | ❌ 报错：高风险动作必须显式确认，要么交互、要么 --force |
| CI/自动化 | `maglev update --sync-submodules --skip-prompt --force` | 自动确认 → 执行 sync |
| 预览 | `maglev update --sync-submodules --dry-run` | 显示 plan，不执行（无须确认） |
| 单独触发 | `maglev update --sync-submodules` 已是最新版本 | 跳过常规 update，但仍执行 sync 流程 |
| 错误命令 | `maglev init --sync-submodules` | ❌ 报错：`--sync-submodules` 仅在 update 命令下生效 |

## 4. Sync 流程契约（实施需 100% 满足）

按 `05_execution_spec_v1.md` §7 + §12 的整合实施：

```
1. plan_sync_to_recorded(project_root)
   - 复用 check_submodule_repos 的 ready/missing/incomplete 状态
   - 加 .gitmodules ↔ .maglev/config.json 一致性检查
   - 对每个 ready submodule 检查 git diff 未提交改动
   - 用 git ls-tree HEAD <path> 读取 wrapper recorded revision
   - 对比 submodule 当前 HEAD 与 recorded 决定 to_sync / aligned
   返回 plan dict
2. print_sync_plan(plan, dry_run)
3. 早返回条件:
   - status == "no_submodules" → 提示后退出
   - status == "all_aligned" → 提示后退出
   - len(plan.blocks) > 0 → 列出阻断后退出
4. confirm_sync_proceed(plan, args) → bool
   按 §3 flag 行为矩阵处理 4 种组合
5. dry_run 路径：3 已展示 plan，4 跳过，直接退出
6. execute_sync_to_recorded(plan, project_root)
   对每个 to_sync entry 执行 git submodule update --init <path>
   注意：仅 sync-to-recorded，不带 --remote
7. print_sync_results(results)
   - aligned / synced / failed / git status 提示
```

## 5. 不做范围（v2 保持 v1 全部 "明确不做" 项）

`05_execution_spec_v1.md` §10 列出的"明确不做"项 v2 全部继承，特别强调：

- ❌ 不接受 `sync-to-latest` 语义
- ❌ 不自动 commit wrapper 项目
- ❌ 不绕过未提交改动强制 sync
- ❌ 不带 `--remote` flag

## 6. 实施落点（confirmed）

| 文件 | 改动 |
|---|---|
| `packages/maglev-cli/runtime-src/maglev_installer.py` | 加 argparse flag + sync 流程函数族 |
| `packages/maglev-cli/dist/maglev_installer.py` | 同步 runtime-src 内容（手动 cp 保持本地一致；release.py step5 会自动同步） |
| `specs/20_evolution/active/submodule_pointer_sync_execution/06_implementation_plan_v1.md` | 新增实施切片记录 |
| `specs/20_evolution/active/submodule_pointer_sync_execution/status.md` | 编码实施阶段从 ⬜ 升级到 ⏳/✅ |

## 7. 测试与验证策略

**Manual smoke test**（本会话执行）：
- `python3 packages/maglev-cli/runtime-src/maglev_installer.py update --sync-submodules --help` 验证 help 文本
- `--sync-submodules` 在非 submodule 项目下应 plan == "no_submodules"
- `--sync-submodules --dry-run` 不动文件

**未来集成测试**（不阻塞本轮）：
- 在测试 wrapper 项目上构造场景：1 submodule aligned + 1 with diff + 1 missing，验证 plan 三分类
- `--skip-prompt` 无 `--force` 必须报错
