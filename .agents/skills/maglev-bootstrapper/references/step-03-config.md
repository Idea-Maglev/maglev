---
name: step-03-config
description: 协议配置
next_step: references/step-04-ai-context-check.md
---

# Step 3: Protocol Configuration (协议配置)

## 目标
实例化规则文件，完成最后的一公里配置。

## 动作
1.  **Generate Core Rules**:
    *   Read `.maglev/rules/core_rules.md`.
    *   Replace `{{PROJECT_NAME}}` with actual folder name.
    *   Write to `.maglev/config/core_rules.md`.
2.  **Setup User Config**:
    *   Check if `.maglev/user.yaml` exists. If not, copy `user.example.yaml`.
3.  **Setup Repository Map**:
    *   消费者项目初始化时不预置 Reality Profile、domains 或事实页。
    *   `references/templates/maglev-core-v1/` 只属于 Maglev 源仓库，不得复制给消费者。
    *   Create or update the Profile-governed repository-map entry only after the user confirms
        at least one repository; do not invent a new Reality directory.
    *   If Adoption Mode, register the legacy `src` path only after explicit confirmation.

## 完成 (Finalize)
告知用户：
"🚀 Maglev 初始化完成！
1. 核心法则已注入。
2. 技能库已就绪。
3. 已完成 AI 上下文最小可用检查。
请尝试输入: `创建第一个 Spec`。"
