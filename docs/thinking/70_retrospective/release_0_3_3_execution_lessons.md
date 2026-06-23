# Release 0.3.3 执行经验沉淀

> **Created**: 2026-04-25
> **Status**: active
> **Segment**: 70_retrospective
> **Context**: 0.3.3 完整发布走完 8 步流程，遇到三个非显式记录的卡点，留作 0.3.4+ 复用

---

## 1. 卡点一：release 脚本的 stdin 阻塞

### 现象

`scripts/maglev_release.py` 在 8 步流程中需要 stdin 确认两次（审计、changelog 各一次），但 bash sync 模式下 stdin 不被脚本读取，导致脚本悬挂。

### 修复

```bash
echo -e "Y\nY" | python3 -u scripts/maglev_release.py
```

要点：
- 必须 `-u`（unbuffered）确保 Python 即时刷新输出
- 必须 `\n` 分隔，**两次确认一起喂**
- 不要尝试用交互模式 — async + write_bash 也容易因 prompt 时机错位而吞输入

### 预防

未来 0.3.4 应考虑把 release 脚本改成接受 `--yes` flag，避免 piping 把关系搞复杂。

## 2. 卡点二：release 分支命名 ref 冲突

### 现象

按习惯创建 `release/0.3.3` 分支时，git push 失败 — 远程已存在裸 ref `release`，导致 `release/X` 路径冲突（git ref 不允许某 ref 同时是另一个 ref 的前缀）。

### 修复

改用 `chore/release-0.3.3` 命名空间。从此本仓库 release 分支统一走 `chore/release-X.Y.Z`。

### 预防

应在 contributors 文档或 release 脚本前置检查中固化此命名规范。

## 3. 卡点三：release 第 7 步的 NPM publish 是脚本外动作

### 现象

`maglev_release.py` step 7 是 "verify npm"，**不会自己 publish**。脚本会去 npm registry 查目标版本，发现不存在直接失败。

### 修复

```bash
cd packages/maglev-cli && npm publish --registry=private npm mirror
```

publish 完成后回到仓库根目录重新跑 release，step 7 就过。

### 预防

容易被脚本流程"自动化"假象误导。建议在 release 文档前置标注："step 6 完成后，必须手动执行 npm publish"。

## 4. 隐含纪律

- `release.version.json set X.Y.Z` 同步 8 个受管文件，但其中 4 个 CHANGELOG 和 dist/ 是 gitignored，所以 `git diff` 看不到全部改动 → **不要靠 git diff 验证 set 命令是否成功，要看脚本输出**
- master FF 合入前必须本地拉最新 origin/master，避免与 release 期间他人提交冲突

## 5. release 检查清单（0.3.4+ 复用）

```
□ 0. 切到 chore/release-X.Y.Z 分支（不要用 release/）
□ 1. python3 scripts/maglev_version.py set X.Y.Z
□ 2. echo -e "Y\nY" | python3 -u scripts/maglev_release.py --dry-run
□ 3. cd packages/maglev-cli && npm publish --registry=...（在 step 6 之后再做）
□ 4. echo -e "Y\nY" | python3 -u scripts/maglev_release.py
□ 5. master FF + push + tag push
□ 6. docs/releases/X.Y.Z.md + index.md
```

## 6. 关联

- `docs/releases/0.3.3.md` — 用户面向发布说明
- `scripts/maglev_release.py` — 流程脚本（候选改进：加 `--yes` flag）
- `release.version.json` — 版本与同步清单源
