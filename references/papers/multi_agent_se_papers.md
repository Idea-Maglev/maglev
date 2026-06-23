# 核心论文索引 (Key Papers Index)

本文档收录了对 "Maglev" 项目方法论产生深远影响的学术论文，特别是关于 **多 Agent 协作 (Multi-Agent Collaboration)** 和 **软件工程自动化 (SE Automation)** 的领域。

## 1. Multi-Agent Systems in SE

### **[2307.07924] Communicative Agents for Software Development (ChatDev)**
- **来源**: Tsinghua University / ModelBest
- **核心理念**: **"Chat Chain"**。将软件开发分解为 Design, Coding, Testing, Documentation 等原子环节，每个环节由两个 Agent（如 CTO & Programmer）进行对话式交互。
- **Maglev 借鉴点**: 
  - 我们的 **"Ring Iteration" (环形迭代)** 受其 "Chat Chain" 启发。
  - **"Role-Playing"**: 论文证明了赋予 LLM 特定角色（如 CEO, CTO）能显著提升产出质量。Maglev 的 `consult_maglev_guide` 和 `role_personas.md` 深度应用了此理论。
- **推荐指数**: ⭐⭐⭐⭐⭐

### **[2308.00352] MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework**
- **来源**: DeepWisdom
- **核心理念**: **"Code = SOP (Standard Operating Procedure)"**。不仅仅是让 Agent 聊天，而是将人类公司的 SOP（如 PRD 定义、API 接口定义）硬编码为 Agent 的行动准则。
- **Maglev 借鉴点**:
  - **结构化输出**: MetaGPT 强制要求输出结构化文档（Data Structures, API Design）。这直接验证了我们 **"Spec-Driven"** 和 **"All-in-One Repo"** 策略的正确性。
  - **Role Definition**: 其对 Product Manager, Architect, Engineer 的精细定义是我们 "铁三角" 模型的理论先驱。
- **推荐指数**: ⭐⭐⭐⭐⭐

## 2. Evaluation & Benchmarking

### **[2310.06770] SWE-bench: Can Language Models Resolve Real-World GitHub Issues?**
- **来源**: Princeton University
- **核心理念**: 不要只测代码片段，要测 **"Repo-Level"** 的真实 Issue 解决能力。
- **Maglev 借鉴点**:
  - 我们的 **"Efficiency Matrix"** (尤其是 `eff.bug_pilot`) 的最终目标就是通过类似 SWE-bench 的测试。
  - 提示我们：真实的 B2B 开发难点不在于生成一个函数，而在于 **Context Retrieval** 和 **Cross-File Dependency**。
- **推荐指数**: ⭐⭐⭐⭐

## 3. Reasoning & Planning

### **[2305.10601] Tree of Thoughts: Deliberate Problem Solving with Large Language Models**
- **来源**: Princeton / Google DeepMind
- **核心理念**: 在做决定前，先进行多路径的推演 (Lookahead) 和回溯 (Backtracking)。
- **Maglev 借鉴点**:
  - 这是我们 **`thinking/` 目录存在的理论基石**。
  - Maglev 要求在写代码前先写 `thinking/` 文档，就是在强迫人类和 AI 共同执行 "Tree of Thoughts" 过程，避免线性思维的盲目性。
- **推荐指数**: ⭐⭐⭐⭐
