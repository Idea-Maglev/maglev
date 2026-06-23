# 技术栈指北 (Tech Stack Compass)

本文档介绍了 Maglev 能够运转的底层技术基础设施。

## 1. 核心协议 (The Protocol)

### **Model Context Protocol (MCP)**
- **官网**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **定义**: 2024/2025 年的 AI 交互标准协议。
- **Role in Maglev**:
  - 它是连接 **Context (知识)** 和 **Action (能力)** 的桥梁。
  - 我们的 `.agents/skills/` 本质上就是 MCP Servers 的一种轻量化实现（或客户端适配）。
  - Maglev 未来的 `feature_roadmap` 强烈依赖 MCP 来打通 Jira, GitHub, Slack 等外部系统。

## 2. 知识库工具 (Knowledge Base)

### **Obsidian**
- **定义**: 本地优先的 Markdown 知识库。
- **Role in Maglev**:
  - **"Spec Editor"**: Maglev 的 Spec 都是 Markdown，Obsidian 是目前编辑体验最好的工具。
  - **"Graph View"**: 帮助人类通过可视化连接理解 `solutions/` 和 `thinking/` 之间的关联。
  - **Local First**: 契合 Maglev "Repo as Truth" 的安全理念。

## 3. 编排工具 (Orchestration)

### **VibeKanban**
- **定义**: 下一代的可视化看板，支持 AI Agent 编排。
- **Role in Maglev**:
  - 它是 Maglev 的 **"North Star Interface"**。
  - 虽然初期可以使用 GitHub Issues/Projects，但 VibeKanban 提供的 **"Thinking Integration"** (将 Issue 和 Context 绑定) 是其他工具不具备的。
  - 我们的 `maglev_bridge` 脚本就是为了让 Maglev Repo 能“原生”对接 VibeKanban。
