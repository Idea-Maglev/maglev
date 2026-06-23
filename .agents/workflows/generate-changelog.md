---
description: 基于变更草案(DRAFT)自动生成语义化的 CHANGELOG.md (仅 Creator 可用)
metadata:
  formal_action_name: 版本说明生成
  top_level_capability: 非核心主流程能力
  object_kind: workflow
  lifecycle_chain: specialized_support
  distribution_scope: private_only
  author: Maglev contributors
  last_updated: 2026-03-30
  distribution: private
---

# Generate Changelog Workflow

本工作流用于在 Maglev 版本发布过程 (Step 4) 中，基于构建脚本生成的 `CHANGELOG_DRAFT.md`，智能提取变更文件的业务含义，并生成友好的发行说明。

## 适用场景

当执行 `python scripts/maglev_release.py` 并在 Step 4 暂停等待时，触发此工作流。

## 工作流步骤

1. **读取发行草案**
   - 使用 `view_file` 工具读取 `.maglev_build/CHANGELOG_DRAFT.md`。
   - 提取其中的 `[NEW]`, `[MODIFIED]`, `[DELETED]` 文件列表。
   
2. **上下文推断 (Context Gathering)**
   - 对于列表中涉及到的核心修改文件（例如 `.agents/skills/*/SKILL.md`, `.agents/workflows/*.md`）：
     - 使用 `view_file` 查阅其内容（特别是开头几百行），理解该模块的功能作用。
     - 分析文件在本次大版本中到底新增或优化了什么能力。
     
3. **调用生成技能**
   - 使用收集到的见解，调用 `maglev-changelog-generator` Skill。
   - 要求按照该 Skill 中定义的格式，生成面向用户的 `.maglev_build/CHANGELOG.md`。
   - 同时将同一份内容归档到 `docs/releases/<version>.md`。
   - 并更新 `docs/releases/index.md`，登记这个版本的入口链接。

4. **审核与输出**
   - 生成完毕后，向 Creator 展示 Changelog 内容。
   - 确认 `docs/releases/` 中已经有对应版本的归档文件。
   - 确认 `docs/releases/index.md` 已包含对应版本链接。
   - 提示 Creator：可以在审阅无误后，返回之前暂停的运行着 `maglev_release.py` 的终端并按回车继续推送流程。
