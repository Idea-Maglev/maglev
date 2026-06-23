---
description: 安装后的 Maglev 更新入口，统一承接 dry-run 预览与正式 update
metadata:
  formal_action_name: 安装后更新
  top_level_capability: 整体接入
  object_kind: workflow
  lifecycle_chain: system_enablement
  author: Maglev contributors
  last_updated: 2026-03-30
---
# Update Workflow

在项目已经接入 Maglev 后，使用 `maglev-updater` 统一处理更新预览、正式更新和结果解释。

目标：
- 先判断当前项目是否具备更新条件
- 在有风险或信息不足时，默认建议 `--dry-run` 预览
- 统一解释新增、覆盖、冲突备份和同步状态变化
- 让 AI 入口与 CLI update 共用同一套更新语义
- 在 `dry-run` 或正式更新后，补做 `AGENTS.md` / `llms.txt` 的 AI 上下文漂移检查

执行方式：
1. 启动 `maglev-updater` 技能。
2. 先读取 `.maglev/sync_state.json` 与 `.maglev/config.json`，判断当前版本和上游地址。
3. 如果当前仓库可能存在本地修改、团队协作风险，或用户只想先看影响范围，则建议执行 `npx @idea-maglev/maglev-cli update --dry-run`，或等价的本地命令。
4. 如果用户明确要直接更新，或上下文已经足够确认风险可接受，可以直接调用正式 `update`。
5. 如果 CLI 提示“包内镜像未同步”或“.maglev_build/ 与 CLI 版本不一致”，不要继续假装可以更新；应先提示维护者执行 `python3 scripts/maglev_release.py --dry-run --skip-audit` 同步包内镜像。
6. 在解释阶段补充 AI 上下文漂移检查：确认 `AGENTS.md` / `llms.txt` 是否缺失、是否仍停留在旧 runtime name、是否混淆兼容 workflow 入口与当前 skill runtime name。
7. 用中文总结本次更新涉及的新增、覆盖、冲突备份、AI context 风险与下一步检查项。

补充说明：
- 即使用户只执行 `update --dry-run`，也应看到 AI 上下文漂移检查结果。
- 如果存在缺口，结果里应直接给出最小补齐建议和最小示例块。
