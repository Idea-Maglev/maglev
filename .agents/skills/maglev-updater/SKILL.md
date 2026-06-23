---
name: maglev-updater
description: 安装后更新入口。负责预览更新、执行 update、解释结果，并统一版本与同步状态口径。
metadata:
  formal_action_name: 安装后更新
  top_level_capability: 整体接入
  system_layer: Infrastructure Layer
  lifecycle_chain: system_enablement
  runtime_name_status: active_legacy_name
  distribution_scope: private_only
  author: Maglev Core
  last_updated: 2026-03-30
  version: "1.0.0"
---

# Maglev Updater

> 结构动作名：`安装后更新`
> 运行面名称：`maglev-updater`
> 这不等于已经完成正式物理改名。

## 概览
`maglev-updater` 是安装后的正式 AI 更新入口。
它不直接发明新的更新逻辑，而是复用现有 CLI / installer 链路，把更新动作组织成统一、可解释的用户流程。

它不负责：

- 代替初始化接入
- 脱离现有 CLI / installer 另起一套更新机制
- 在未确认项目已接入 Maglev 时假装可以更新

## 核心职责
1. 识别当前项目是否已经接入 Maglev。
2. 读取本地同步状态，说明当前版本与上次同步时间。
3. 在有风险或信息不足时，优先建议 `dry-run` 预览；但不要把它误写成唯一入口。
4. 在用户确认后执行正式更新。
5. 用统一结构解释：
   - 新增文件
   - 覆盖更新
   - 冲突备份
   - 更新后的检查建议
6. 在 `dry-run` 或正式更新后，检查 `AGENTS.md` / `llms.txt` 是否已与当前 Maglev 结构漂移。

## 执行步骤

### Step 1. 检查更新前提
先确认项目中是否存在：

- `.maglev/`
- `.maglev/sync_state.json`

如果缺失：
- 不要假装可以更新。
- 明确提示用户该项目还没完成初始化，应该先执行 `init`。

### Step 2. 读取本地状态
读取：

- `.maglev/sync_state.json`
- `.maglev/config.json`（如果存在）

至少提取：

- `last_synced_version`
- `last_synced_time`
- `upstream_url`（如果有）

### Step 3. 按风险决定是否先预览
当出现下面这些情况时，默认建议先预览：

- 当前仓库可能有本地改动
- 用户只想先看更新影响
- 这是正式业务仓库
- AI 还无法确认覆盖风险是否可接受

推荐命令：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

如果当前环境明确已全局安装，也可以使用：

```bash
maglev-cli update --dry-run
```

如果用户明确要求“直接更新”，且上下文已经足够确认风险可接受，则可以直接执行正式更新，不要机械地卡在 `dry-run`。

### Step 4. 解释 dry-run / update 输出
当命令输出出现以下状态时，要统一翻译成用户能理解的语言：

- `NEW`：本次会新增的 Maglev 资产
- `OVERWRITE`：会被新版本覆盖的现有文件
- `CONFLICT`：本地有改动，更新时会先生成备份再覆盖
- `SKIP`：本地与远端一致，不需要处理

如果 CLI 提示下面这类错误，也要按真实状态解释，而不是继续假装能更新：

- 包内镜像缺失 installer
- `.maglev_build/` 与 CLI 版本不一致

这通常意味着：

- 当前正在源仓库开发态验证
- 但包内镜像还没通过 release dry-run 同步

此时应明确建议：

```bash
python3 scripts/maglev_release.py --dry-run --skip-audit
```

### Step 4.5 AI Context Drift Check
在 `dry-run` 或正式更新后的解释阶段，额外检查：

- `AGENTS.md` 是否存在
- `llms.txt` 是否存在
- 是否仍使用旧主流程 runtime name
- 是否混淆 skill runtime name 与 workflow 兼容入口
- 是否遗漏 init / update / 主流程入口说明

说明：

- 这项检查不是只在正式 update 后才出现
- 用户执行 `update --dry-run` 时，也应能看到同样的漂移检查结果
- 如果存在缺口，输出里应直接附最小补齐建议与示例块

参考：

- `references/ai-context-drift-check.md`
- `../_internal/ai-context-check/contract.md`

### Step 5. 正式更新后的收尾
正式更新完成后，提醒用户至少检查：

1. `.maglev/sync_state.json` 是否刷新到新版本
2. 是否出现 `*.local_backup_*`
3. 当前团队是否需要同步本次变更

> **关于 Tag 与 NPM 发布**：release 脚本（`maglev_release.py`）在 step 7-8 会自动验证私域 NPM registry 是否已发布当前版本，并在确认后创建 Git tag。updater 不需要关注 tag 创建，但可以利用 tag 信息辅助判断用户侧版本状态。

## 输出要求
输出时优先使用下面这个结构：

1. `当前状态`
2. `建议命令`
3. `预期影响`
4. `更新后检查`
5. `AI 上下文漂移检查`

要求：
- 中文表达
- 先讲结论，再讲命令
- 不要把 CLI 和 AI update 说成两套不同机制
