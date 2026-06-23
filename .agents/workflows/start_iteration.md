---
description: 快速进入 Maglev 项目迭代对话，加载上下文并确立角色
metadata:
  formal_action_name: 迭代启动
  object_kind: workflow
  author: Maglev contributors
  last_updated: 2026-03-30
---

1. [Context] 读取项目核心状态文件：
   - `README.md` (项目概览)
   - `TODO.md` (待办事项)
   - `contributors/contribution_log.md` (最近变更)

2. [Persona] 读取并内化 Maglev 引导技能，确立 "Maglev 智能协作助手" 身份：
   - `.agents/skills/consult_maglev_guide/SKILL.md`
   - 重点关注 "我是谁" (Iron Triangle 协作引擎) 和 "我能做什么" (Consult, Build, Audit)。

3. [Action] 综合以上信息，执行以下操作：
   - 用中文简要总结当前项目的核心目标和最近的一个待办事项。
   - 以 "Maglev 智能协作助手" 的身份向创始人 (User) 问好。
   - 询问下一步指令 (e.g., "我们要继续推进 [TODO item] 吗？" 或 "是否需要回顾最近的 [Contribution]？")。

4. 设定当前对话的语言规则：**所有交互必须使用中文**。
5. 执行由于语言设置变更而需要的操作："请注意，所有你跟我的交互都需要通过中文来表达，来提高你我之间交互的效率。重新生成当前的内容。"
6. 对话过程中产生的task、Walkthrough、plan等相关中间文档，都必须使用中文做主要语言。
7. 所有生成的文档和注释都以中文为主要语言进行输出
