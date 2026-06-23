# `git rebase --onto` 跳过 merge commit 导致功能代码丢失

- 日期：2026-04-29
- 类别：Retrospective / Git 操作反模式
- 触发场景：0.4.0 重新发布过程中 push master 被拒后的同步操作

## 1. 现象

本地 master 有 3 个新 commit（hotfix changelog + minimal example 升级 + 其文档）+ 1 个 merge commit（`82504c9`，把 fix 分支带入 integration→master）。

远端 master 在我推送前被 GitLab UI 用等价 merge（`4904be7`）抢先合入，导致本地 push 被拒。

为同步远端，执行：

```bash
git rebase --onto origin/master 82504c9 master
```

意图：把 `82504c9..master` 的差异（即"我比远端多的 3 个 commit"）重放到 origin/master 之上。

**实际后果**：
- `82504c9` 是 merge commit，其第二亲（`da9299c → ff400fc` fix 链）的内容**没有作为独立 commit 重放**。
- 三个文档 commit 重放成功，但 `ff400fc`（installer fix 主体）被静默丢弃。
- `git diff origin/master master` 显示 fix 相关代码（`ensure_ai_context_files` / Maglev managed gitignore 块 / dist pycache 排除）全部消失。

## 2. 根因

`git rebase --onto <newbase> <upstream> <branch>` 重放的是 `upstream..branch` 中的**线性 commit**。当 `<upstream>` 本身是 merge commit，且 merge 引入的"功能 commit"位于其第二亲分支上时，那些功能 commit 不在 first-parent 链路上，rebase 默认不会重放它们。

换句话说：**rebase 只重放主干 commit，不会重放 merge 引入的合并分支上的独立 commit**。

## 3. 修复

cherry-pick 把丢失的功能 commit 单独捡回：

```bash
git cherry-pick ff400fc
```

cherry-pick 后必须重新验证：
- 源码 grep 关键标志位（本次：`ensure_ai_context_files` / `Maglev managed` / `ignore_patterns`）
- 重建产物（本次：`packages/maglev-cli/dist/`）
- 重新打 tag（本次 v0.4.0 tag 此前指向已被 rebase 替换的 orphan commit `e5b3ac1`）

## 4. 教训与红线

**红线 1**：`git rebase --onto` 的 `<upstream>` 是 merge commit 时，必须先识别 merge 第二亲分支上的所有功能 commit 列表，rebase 后用 cherry-pick 单独找回。

**红线 2**：rebase / 强制操作之后，必须做"内容 diff 验证"而不是只看 commit log。本次事故的早期信号是 `git log` 看起来"3 个文档 commit 都在"，但功能代码已经没了。

**红线 3**：tag 在 rebase 之前推送的，rebase 后 tag 指向的 commit 可能已经不在主分支历史中（变成 orphan）。push master 之前必须重新对齐 tag。

## 5. 推荐替代路径

遇到本地 master 与远端发散（远端被 UI 合并、本地有线性新增），更安全的做法：

- **优先 merge 而非 rebase**：`git merge origin/master` 直接产生合并 commit，所有功能 commit 都保留在 history。代价是 history 多一个 merge node，但功能完整性优于线性美观。
- 若必须 rebase 保持线性，先用 `git log --oneline --all --graph` 把 merge 节点的两个亲都看清楚，明确哪些 commit 在第二亲上需要单独保留。

## 6. 关联

- 0.4.0 重新发布过程：`docs/releases/0.4.0.md` Hotfix 段
- 行业扫描沉淀：`docs/thinking/20_architecture/2026-04-28-agents_md_rules_industry_scan.md`
- 涉及 commits：`ff400fc`（fix 原始）→ rebase 丢失 → cherry-pick 找回为 `4123923`
