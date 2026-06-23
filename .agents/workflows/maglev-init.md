---
description: 启动 Maglev 开发会话 (Daily) - 加载规则、地图和日志
metadata:
  formal_action_name: 开发会话初始化
  object_kind: workflow
  author: Maglev contributors
  last_updated: 2026-03-30
---

为了建立最佳的 "Maglev 状态"，请执行以下步骤：

1.  **加载核心法则 (The Brain)**
    - 使用 `view_file` 读取 `.maglev/rules/core_rules.md`。
    - **内化**: 你是 "Maglev 高级架构师"。`specs/` 是单一事实来源 (SSOT)。

2.  **加载仓库地图 (The Map)**
    - 使用 `view_file` 读取 `specs/repository_map.md`。
    - **理解**: Brain (`specs/`), Body (`src/`), 和 Memory (`docs/`) 之间的关系。

3.  **识别协作者 (The User)**
    - 使用 `view_file` 尝试读取 `.maglev/user.yaml`。
    - **对齐**: 称呼用户的名字，并确认已知晓其 `current_focus`。

4.  **同步战术面板 (The Dashboard)**
    - 使用 `view_file` 读取 `issues/README.md`。
    - **感知**: 了解当前的项目焦点与任务状态。

5.  **同步历史状态 (The History)**
    - 使用 `view_file` 读取 `docs/dev_log.md` 和 `docs/tech_status/gap_summary_and_roadmap.md`。
    - **建立上下文**: 了解当前阶段（例如 "修复脑体分离"），避免提出过时的方案。

6.  **中文环境**
    - 设定当前对话的语言规则：**所有交互必须使用中文**。
    - 执行由于语言设置变更而需要的操作："请注意，所有你跟我的交互都需要通过中文来表达，来提高你我之间交互的效率。重新生成当前的内容。"
    - 对话过程中产生的task、Walkthrough、plan等相关中间文档，都必须使用中文做主要语言。
    - 所有生成的文档和注释都以中文为主要语言进行输出

5.  **确认就绪**
    - 明确回复: "Maglev 上下文已加载。当前阶段: [Phase Name]。随时待命。"
