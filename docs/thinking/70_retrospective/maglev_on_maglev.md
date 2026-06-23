# Maglev 自举计划 (Maglev on Maglev)

> **Status**: Draft
> **Code Name**: Ouroboros (衔尾蛇)
> **Date**: 2026-02-13

## 1. 核心洞察
用户指出：“**应该将 Maglev 本身 Maglev 化**”。
这是一个战略级的转折点。这意味着 Maglev 不再仅仅是一个“工具包”，而是一个需要被严格工程化管理的“产品”。

**Why Now?**
1.  **复杂度临界点**: Skill 数量已突破 20+，手动维护已不可行。
2.  **一致性危机**: 不同的 Skill 风格各异，更新不同步。
3.  **质量自证**: 如果 Maglev 不能用 Maglev 的方法治理好自己，如何说服用户？

## 2. 什么是 "Maglev 化"?
将 Maglev 的核心法则应用于 Maglev 项目自身的开发维护。

| 核心法则 | 现状 (Current) | 目标 (Target) |
| :--- | :--- | :--- |
| **Spec First** | Skill 的开发依赖 `SKILL.md` (说明书)，缺乏严谨的技术 Spec。 | **Specs for Skills**. 每个 Skill 都有 `specs/` (Reqs/Design)，定义输入输出 schema、依赖关系。 |
| **Context is King** | AI 也是“看文档写代码”，但文档和代码有时脱节。 | **Context-Driven Dev**. 我们修改 Skill 时，必须先加载该 Skill 的 Spec。 |
| **Iron Triangle** | 缺乏质量验证与测试。 | **Skill Test Suite**. 我们可以编写测试用例来验证 Skill 生成的产物是否符合标准。 |

## 3. 实施路径 (Roadmap)

### Phase 1: Establish Truth (确立真理)
为 Maglev 核心组件建立 Spec。
- 创建 `specs/maglev_system/`
    - `01_requirements.md`: 定义 Skill Manager, Bootstrapping, Testing 等核心需求。
    - `02_architecture.md`: 定义 Skill 的标准结构、配置分离规范 (RFC-001)。

### Phase 2: Refactor via Spec (通过 Spec 重构)
以 "Skill 更新机制" 为试点，**先写 Spec，再开发**。
- 不再随意写个 Python 脚本，而是先走 `maglev-create-spec` 流程，定义 `maglev-manager` 的接口。
- 利用 Maglev 的能力来生成 `maglev-manager` 的代码。

### Phase 3: Automated Quality (自动化质量)
建立 "Meta-Testing" 机制。
- **Skill CI**: 当我们修改了 `maglev-create-spec` 后，自动运行一个测试：让新版 Skill 生成一个 Spec，然后用 `maglev-audit-spec` 去审计它生成的 Spec 及其质量。
- **Self-Healing**: 如果审计失败，Skill 也就是“构建失败”。

## 4. 对 "Skill 更新机制" 的影响
之前的 "Skill 更新机制" (RFC 文档) 现在不仅仅是一个独立的 Feature，而是 **Maglev 系统的一个核心模块**。
它需要被正式地写入 `specs/maglev_system/02_architecture.md`。

---
**结论**:
这不仅是技术升级，更是**治理模式升级**。
我们将从 "Manual Craftsmanship" (手工作坊) 转向 "Industrial Engineering" (工业化生产)。
所有的 Skill，都是这个工厂生产出的“精密部件”，必须经过 Spec 定义和 Quality 检验。
