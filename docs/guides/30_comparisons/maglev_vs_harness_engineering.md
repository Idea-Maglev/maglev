# Maglev vs Harness Engineering: 边界澄清版

> **TL;DR**:
> 如果把 `Harness engineering` 按广义理解，它覆盖的范围会部分进入“智能体应用开发基础设施”领域，而这并不是 Maglev 的直接问题域。
> 因此，Maglev 与 Harness engineering 的公平比较，应当限制在 **组织内 AI Coding / AI 驱动的软件研发执行** 这一交集内。

## 1. 为什么要专门做这篇澄清？

`Harness engineering` 是一个新兴概念，外延还在扩张。
当它被广义使用时，可能同时包含两类东西：

1. **AI Coding 执行体系**
   - coding agent 的上下文组织
   - lint / test / CI / policy feedback loops
   - 文档与代码一致性维护
   - cleanup / drift detection

2. **智能体应用开发基础设施**
   - agent runtime orchestration
   - browser-native autonomous workflows
   - tool-calling fabric
   - agent observability platform
   - 多 agent 长链路自治控制

而 Maglev 的核心问题域并不是“怎么开发一个智能体产品”，而是：

> **如何在软件研发交付过程中，让人、AI、Spec、Code、治理长期保持对齐。**

所以如果不先澄清边界，比较很容易失真。

---

## 2. 一句话结论

### 广义结论

如果把 `Harness engineering` 按广义理解，它的外延**大于** Maglev 的直接覆盖范围。

### 公平比较下的结论

如果把范围限制在 **组织内 AI Coding / AI 驱动的软件研发执行**，
那么更准确的关系是：

- `Harness engineering` 更偏 **执行环境、反馈回路、机械约束**
- `Maglev` 更偏 **Spec、治理、协作协议、Brownfield 纳管**

在这个交集内，可以把 `Harness engineering` 视为 **Maglev 执行层的重要能力簇**。

---

## 3. 哪些部分可以直接比较？

下面这些内容适合直接拿来和 Maglev 比较：

| 可比区域 | Harness engineering 关注点 | Maglev 关注点 |
| :--- | :--- | :--- |
| **上下文组织** | 让 coding agent 读到正确 repo context | 通过 Specs / Thinking / Map 显式组织真理源 |
| **执行约束** | lint、test、CI、policy feedback loops | Gatekeeper、Spec First、cross-validate |
| **一致性维护** | drift detection、cleanup jobs | Reverse Spec、三角自愈 |
| **组织落地** | 把 AI Coding 变成稳定工程系统 | 把 AI Coding 放进完整协作协议中 |

这部分是双方真正重叠的战场。

---

## 4. 哪些部分不应该直接比较？

下面这些内容更偏“智能体应用开发基础设施”，不适合直接拿来要求 Maglev 对标：

- 通用 agent runtime
- browser-native autonomous control
- tool-calling orchestration fabric
- agent product observability platform
- 长时自治智能体系统

这些问题更像是在讨论：

> “如何构建一个 agent product / agent platform？”

而不是：

> “如何治理组织内 AI Coding 与软件研发执行？”

Maglev 不是为前者直接设计的。

---

## 5. 在公平比较口径下，二者各自的强项

### Harness engineering 的强项

- 更贴近 coding agent 的一线执行问题
- 更容易沉淀成平台能力、工具能力、CI 能力
- 对 build / test / log 反馈回路更直接
- 对“如何减少 agent 跑偏”更有操作性

### Maglev 的强项

- 更重视意图建模，而不是只重执行纠偏
- 更强调 Spec 作为上游真理源
- 更适合把代码、文档、规则、协作放进统一框架
- 对 Brownfield 治理与逆向固化更友好

---

## 6. 最推荐的组合关系

如果团队目标是组织内 AI Coding 的长期建设，最合理的组合不是二选一，而是：

1. 用 **Maglev** 管：
   - Intent
   - Spec
   - Governance
   - Brownfield adoption
   - cross-role alignment

2. 用 **Harness engineering** 管：
   - coding execution environment
   - build / test / log feedback loops
   - mechanical constraints
   - cleanup / drift reduction

这时可以把二者理解为：

> **Maglev 负责“别把方向搞错”，Harness engineering 负责“别把执行跑飞”。**

---

## 7. 最终表述建议

以后如果在项目中再提这组结论，建议使用下面这句更精确的话：

> **在组织内 AI Coding / AI 驱动的软件研发执行这一交集内，Harness engineering 是 Maglev 执行层的重要补强；但如果把 Harness engineering 扩展到智能体应用开发基础设施，二者就不再处于同一比较平面。**

---

## 8. 关联阅读

- `docs/thinking/10_critique/2026-03-16-maglev_vs_harness_engineering.md`
- `docs/thinking/20_architecture/2026-03-16-harness_maglev_integration_blueprint.md`
