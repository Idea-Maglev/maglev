# Maglev vs OpenSpec: 深度对比分析报告

> **TL;DR**: Maglev 是一个**全栈的 AI 研发操作系统 (Operating System)**，涵盖组织、流程和工程；而 OpenSpec 是一个**专注于 AI 代码生成的交互协议 (Protocol)**。Maglev 可以不仅包含 OpenSpec 的理念，甚至可以直接集成 OpenSpec 作为其底层的 "执行驱动器"。

## 1. 核心定义与定位 (Definition & Positioning)

| 维度 | Maglev (磁悬浮) | OpenSpec |
| :--- | :--- | :--- |
| **定义** | **AI Native B2B 研发方法论** (Methodology) | **AI 辅助编程规范标准** (Standard / Tool) |
| **核心隐喻** | **操作系统**：调度人(PM/Dev)与AI(Agent)的协作资源 | **合同/契约**：人与AI之间的明确指令集 |
| **解决问题** | 解决 B2B 软件开发的**系统性复杂性** (组织僵化、沟通损耗、资产混乱) | 解决 AI 编程的**局部随机性** ("Vibe Coding"、幻觉、非确定性输出) |
| **适用范围** | 整个项目全生命周期 (从立项、需求到交付、维护) | 代码生成环节 (Coding Phase) |

## 2. Spec 体系对比 (The "Spec" Aspect)

两者的核心交集在于都推崇 **"Spec-Driven Development" (SDD)**，但在具体实现上差异巨大。

### OpenSpec 的 Spec
*   **形态**: 专注于 **Prompt Engineering 的结构化封装**。通常是 Markdown 文件，包含 Context, Instructions, Constraints。
*   **工作流**: 严格的 **Proposal -> Apply -> Archive** 三步曲。
*   **侧重点**: **确定性 (Determinism)**。防止 AI 瞎写，确保每次运行结果一致，便于审计。
*   **文件结构**: `openspec/specs/` (Source of Truth) vs `openspec/changes/` (Change Requests)。类似于 Git 的 Staging Area 概念。

### Maglev 的 Spec ("意图结晶")
*   **形态**: **全维度的资产库**。不仅是给 AI 看的代码指令，还包含给 Value Owner 看的业务逻辑、给 Experience Guardian 看的交互原则。
*   **体系**: **Johnny Decimal (00-99) 系统**。
    *   Maglev 的 Spec 往往是分层的：`sys.01.product_spec` (产品意图) -> `sys.02.tech_design` (技术设计) -> Code。
*   **侧重点**: **资产复用与演进 (Evolution)**。Maglev 强调 Spec 是活的 (Living Documentation)，通过 "环形迭代" 不断从 Code 中逆向还原更新 Spec，保持 "Spec <-> Code" 的绝对同步。
*   **双态分离**: Maglev 也强调 Intent 与 Implementation 的分离，但在组织层面更强调 "铁三角" 中不同角色对不同层级 Spec 的所有权。

## 3. 详细维度对比表

| 对比项 | Maglev | OpenSpec | 评价 |
| :--- | :--- | :--- | :--- |
| **用户角色** | **铁三角** (VO/TP/XG) 多角色协作 | 主要是 **Developer** (开发者) 单人使用 | Maglev 解决的是团队问题，OpenSpec 解决的是个人效率/质量问题。 |
| **上下文管理** | **全局上下文** (通过 `.maglev/rules`, `repo_map` 等) | **任务级上下文** (每个 Spec 文件自包含) | Maglev 更适合大型复杂项目，OpenSpec 更适合原子化任务。 |
| **可观测性** | 强调 **Process Audit** (谁在什么时候改了什么意图) | 强调 **Code Audit** (这次变更生成了什么代码) | Maglev 关注因果，OpenSpec 关注结果。 |
| **生态兼容** | 开放架构，可集成各种工具 (Git, Obsidian, CI/CD) | 专注标准，可被各种 IDE/Agent 集成 (Cursor, Copilot) | |

## 4. 关系与融合 (Relationship)

**Maglev 是 "道"，OpenSpec 是 "术"。**

你完全可以在 Maglev 项目中使用 OpenSpec。事实上，OpenSpec 是 Maglev 体系中 "Tech Pilot" (技术领航员) 角色用来指挥 AI 进行具体编码工作的**绝佳工具**。

### 如何在 Maglev 中使用 OpenSpec？

1.  **上游 (Intent)**: 使用 Maglev 的 JD 体系 (`docs/thinking/`) 定义高层业务意图和架构决策。这部分是给 "人" (Context Provider) 和高级 Agent 看的。
2.  **中游 (Protocol)**: 当需要实现某个具体模块时，Tech Pilot 将 Maglev 的高层意图转化为 **OpenSpec** 格式的文件。
    *   *例如：将 `sys.10.auth_logic.md` (Maglev Spec) 转化为 `openspec/specs/auth_module.md` (OpenSpec).*
3.  **下游 (Execution)**: 调用支持 OpenSpec 的工具 (或直接用 Cursor) 执行生成，利用 OpenSpec 的机制确保代码质量。
4.  **回流 (Sync)**: 生成的代码经过测试后，Maglev 的 "逆向工程" 机制会确保上游的 JD 文档被更新，维持闭环。

## 5. 结论

*   如果你只是在写一个小工具，或者独自开发，**OpenSpec** 是防止 AI "写飞" 的好帮手，轻量、直接。
*   如果你在管理一个 B2B 团队，面临需求频繁变更、人员流动、代码腐化等系统性问题，你需要 **Maglev** 来构建整套防线。
*   **最佳实践**：用 Maglev 治理项目，用 OpenSpec 治理具体的 AI 编码任务。
