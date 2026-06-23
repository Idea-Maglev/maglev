# 06 — 实施计划 v1（编码实施切片 + 实测证据）

> 创建于: 2026-05-18  
> 上游依据: `04_decision_v2.md`（CLI 形态 A + 行为矩阵）+ `05_execution_spec_v1.md`（执行规格）  
> 配套 PR: !6 (feat/submodule-pointer-sync-impl)

## 1. 实施范围

把 `05_execution_spec_v1.md` §1–§12 规格落地到 `packages/maglev-cli/runtime-src/maglev_installer.py`，覆盖 sync-to-recorded 全链路，不做 sync-to-latest。

## 2. 切片清单（T1–T10）

| ID | 切片 | 状态 | 实施位置 |
|----|------|------|---------|
| T1 | argparse 顶层加 `--sync-submodules` flag（A 形态）| ✅ | `main()` ~第 1235 行 |
| T2 | `init` 命令收到 `--sync-submodules` 报 exit 2 | ✅ | `main()` ~第 1260 行 |
| T3 | `_run_git` 安全封装（不抛、识别 git 不存在）| ✅ | ~第 417 行 |
| T4 | `_read_gitmodules_paths` 用 `git config -f .gitmodules` 解析 | ✅ | ~第 444 行 |
| T5 | `_read_recorded_revision` 用 `git ls-tree HEAD --` | ✅ | ~第 467 行 |
| T6 | `_read_submodule_head` + `_submodule_has_uncommitted_changes` | ✅ | ~第 434, 485 行 |
| T7 | `plan_sync_to_recorded` 五态状态机（wrapper_not_git / no_submodules / blocked / all_aligned / ready）| ✅ | ~第 495 行 |
| T8 | `print_sync_plan` + `print_sync_results` | ✅ | ~第 603, 700 行 |
| T9 | `confirm_sync_proceed` 行为矩阵（dry_run / skip+force / skip 无 force / 交互）| ✅ | ~第 637 行 |
| T10 | `run_sync_to_recorded_flow` orchestrator + do_update 两处接入点 | ✅ | ~第 720, 882, 938 行 |

## 3. 与 spec 对照矩阵

| spec 条款 | 实施落点 | 验证手段 |
|----------|---------|---------|
| §3 CLI 形态 A（顶层 flag）| T1 | `--help` 显示 flag |
| §3 init 禁用 sync flag | T2 | `maglev init --sync-submodules` → exit 2 |
| §7 sync 流程契约 | T3–T10 | fixture 端到端 |
| §7 阻断条件 6 项 | T7 plan_sync_to_recorded | fixture blocked 场景 ✅ |
| §7 wrapper 不是 git 仓库早返回 | T7 `os.path.exists(.git)` | adversarial fix（兼容 worktree）|
| §12 复用 `check_submodule_repos` | T7 调用基础报告 | code review |
| §04_decision_v2 §3 行为矩阵 | T9 confirm_sync_proceed | 矩阵直测 ✅ |

## 4. 实测证据链

### 4.1 静态校验

```bash
$ python3 -m py_compile packages/maglev-cli/runtime-src/maglev_installer.py  # OK
$ python3 packages/maglev-cli/dist/maglev_installer.py --help | grep sync
  --sync-submodules     在 update 流程末尾追加 submodule pointer sync (...)
```

### 4.2 init 阻断

```bash
$ python3 dist/maglev_installer.py init --sync-submodules
[ERROR] `init` 不支持 --sync-submodules; 该 flag 仅在 `update` 命令上生效.
# exit 2
```

### 4.3 plan_sync_to_recorded 五态全量 fixture 测试

构造 `/tmp/maglev_sync_fixture/`（wrapper + libs/foo submodule 两 commit v1/v2）：

| 场景 | 配置 | 期望 status | 实测 |
|------|------|-----------|------|
| no .maglev | 无 `.maglev/config.json` | `no_submodules` | ✅ |
| all_aligned | submodule HEAD == recorded | `all_aligned` | ✅ |
| ready | submodule HEAD 退回 v1, recorded=v2 | `ready` (1 to_sync) | ✅ |
| blocked-uncommitted | submodule 有 untracked 文件 | `blocked` (reason 含"未提交改动") | ✅ |
| blocked-config-mismatch | `.maglev/config.json` 含 bar, `.gitmodules` 无 | `blocked` (含 2 条 mismatch) | ✅ |

### 4.4 confirm_sync_proceed 行为矩阵直测

```
skip_prompt + force        → True   ✅
skip_prompt no force       → False (打印 error)  ✅
dry_run                    → False (早返回)  ✅
```

### 4.5 端到端真实执行

ready 场景：submodule HEAD `3784741` → 执行后 `975d14e` (= recorded)，符合预期 ✅

```
[SYNC] 🧭 Pointer Sync 计划
  状态: ready
  待 sync (恢复到 wrapper 记录): 1
    - libs/foo  378474146f06 → 975d14ea87b0
⚠️  (--skip-prompt + --force) 已显式授权, 跳过交互确认.

[SYNC] ✅ Pointer Sync 执行结果
  成功 sync: 1
    ✓ libs/foo: Submodule path 'libs/foo': checked out '975d14ea87b0...'
```

## 5. 对抗审查（Step 5）发现与处置

| ID | Finding | 处置 |
|----|---------|------|
| R1 | `git submodule update --init -- <path>` 对已初始化 submodule 是否能拉回 recorded？ | 实测已验证：detached at v1 + recorded=v2 → 成功切回 v2。✅ 接受 |
| R2 | subprocess 含空格 path | 用 list args 非 shell=True，安全。✅ 接受 |
| R3 | `os.path.isdir('.git')` 不兼容 git worktree（worktree 下 .git 是 file）| **已修复**：改为 `os.path.exists(...)` |
| R4 | config 中 local_path 为 `../etc`（路径穿越）| `check_submodule_repos` 已过滤 + `ls-tree` 不会匹配。✅ 边界可接受 |
| R5 | sync 失败的 exit code 不影响 do_update 退出码 | spec 决策：sync 是 post-update 增强动作，不反推 update 状态。但已 print_error 提示。✅ 接受 |
| R6 | 含空格的 submodule path | `git config --get-regexp` 直出，空格 path 用 `split(None, 1)` 取末段。已 cover |

## 6. 不在本切片范围

- sync-to-latest（推进远端） — 未来 PR
- 自动 `git add` wrapper 的 pointer 变化 — 始终交还用户判断
- submodule 全自动更新场景下的 conflict 解决 — 高风险，不做

## 7. 后续 follow-up（不阻塞本 PR 合并）

- 在真实多 submodule 项目下（>3 个）做一次回归
- 综合验证 + 结晶（下一会话发起）
