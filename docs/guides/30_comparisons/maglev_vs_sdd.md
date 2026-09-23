# Maglev vs Spec-Driven Development (SDD): 整体与局部

**Spec-Driven Development (SDD)** 是 AI 编程时代兴起的一种技术范式，强调 "Spec First, Code Later"。
**Maglev** 体系完全采纳了 SDD 的核心技术主张，但我们认为单纯的 SDD 并不足以支撑企业级的 B2B 开发转型。

本文档将从组织、流程、治理三个维度，阐述 Maglev 如何将 SDD 这一“引擎”装入“整车”中。

## 1. 核心定义 (The Core Definition)

### SDD (The Engine)
- **公式**: `Result = AI(Spec)`
- **核心假设**: 只要 Spec 写得足够清晰，AI 就能生成完美的代码。
- **关注点**: **Prompt Engineering**, **Context Management**, **Code Generation**。
- **典型工具**: Spec-Kit, Cursor, Copilot Workspace。

### Maglev (The Vehicle)
- **公式**: `Value = People(Roles) + Engine(SDD) + Governance(Rules)`
- **核心假设**: Spec 不会自动产生且极难维护；代码正确不代表体验极佳；没有组织变革，工具有效也无法落地。
- **关注点**: **Organizational Efficiency**, **Role Collaboration**, **Quality Assurance**, **ROI**.

---

## 2. 缺失环节点评 (The Missing Links)

SDD 范式在落地时通常会撞上三堵墙，而 Maglev 正是为打破这三堵墙而设计的。

### 2.1 谁来写 Spec? (The "Writer" Problem)
- **SDD 的死角**: 假设每个人都是优秀的 Spec Writer。现实是 PM 只会写 Word，Dev 只想写 Code。让 Dev 去写详细的 Markdown Spec 往往比直接写代码还可以更痛苦。
- **Maglev 的解法**: 定义了 **Value Owner (VO)** 角色。
    - 我们不要求 Dev 写 Spec，而是要求 VO（产品/业务专家）学会用结构化 Markdown 表达意图。
    - **收益**: 将模糊的业务需求在源头结构化，而不是不仅浪费了 Dev 的时间，还将垃圾意图输入给 AI。

### 2.2 谁来验收体验? (The "Quality" Problem)
- **SDD 的死角**: "Unit Test passed" = "Job Done"。AI 生成的代码往往逻辑正确但体验稀烂（UI 丑陋、交互生硬、边界情况处理反人类）。
- **Maglev 的解法**: 引入 **Experience Guardian (XG)** 角色。
    - **Tech Pilot** 负责让测试通过（功能正确）。
    - **Experience Guardian** 负责验收“非功能性体验”（好用、好看、健壮）。
    - **收益**: 确保交付的不仅仅是代码，更是**产品价值**。

### 2.3 怎么确保一致性? (The "Governance" Problem)
- **SDD 的死角**: 每个人写的 Spec 风格迥异，生成的代码千奇百怪。工具没有约束力。
- **Maglev 的解法**: **Governance as Code**。
    - 通过 `.maglev/config/rules/core_rules.md` 统一全员（包括 AI）的行为准则。
    - 利用 **Skill Adapter** 强制 AI 遵守团队规范。
    - **收益**: 将“依赖个人素质”转变为“依赖系统约束”。

---

## 3. 融合关系 (The Integration)

Maglev 并不是要替代 SDD，而是要**保护** SDD。

| 层级 | Maglev 的组件 | SDD 在其中的位置 |
| :--- | :--- | :--- |
| **战略层** | **Thinking/Paradigms** | 承认 SDD 是 AI 时代的必然选择，否定“手写代码”的旧习。 |
| **组织层** | **Iron Triangle (Roles)** | 只有 VO 写好了 Spec，SDD 引擎才能启动；只有 TP 懂 Prompt，SDD 才能运转。 |
| **执行层** | **Ring Iteration (Process)** | **Step 2 (Build)** 完全就是标准的 SDD 过程：`Spec -> Code`。 |
| **资产层** | **Unified Assets** | `/specs` 目录就是为 SDD 准备的燃料库。 |

## 4. 结论

- 如果你是一个独立开发者，**SDD** 足矣。写好文档，让 AI 帮你写代码。
- 如果你是一个 B2B 研发团队，你需要 **Maglev**。因为你需要解决分工、协作、考核、质量控制等一系列“人”的问题，才能让 SDD 引擎在一个复杂的组织中平稳、高效地运转。

**Maglev = SDD + Organizational Refactoring**
