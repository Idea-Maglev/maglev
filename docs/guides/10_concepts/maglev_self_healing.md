# Maglev Self-Healing: The Check-and-Balance System (自愈机制)

> **Context**: User Insight. "Maglev 具有自愈性...多源交叉验证...生产环境校准。"
> **Core Concept**: Maglev 不是一个脆弱的静态文档堆，而是一个动态的 **"Homeostatic System" (稳态系统)**。

## 1. The Triangulation of Truth (真理三角测距)

传统项目脆弱是因为只有 **Code** 是活的，文档是死的。
Maglev 通过三个顶点进行实时校准：

*   **A. Spec (Intent)**: 我们想做什么？
*   **B. Code (Physics)**: 我们实际做了什么？
*   **C. Runtime (Reality)**: 生产环境跑得怎么样？

### 自愈场景 (Self-Healing Scenarios)

#### Scenario 1: Spec Rot (文档腐烂)
*   **Symptom**: 程序员改了 Code 没改 Spec。
*   **Healing**: `Gatekeeper` (Commit Hook) 发现 Drift。
*   **Action**: AI 自动提议：*"检测到 Code 变更。正在反向更新 Spec 以匹配 Code..."* -> **Spec Healed**.

#### Scenario 2: Buggy Code (代码缺陷)
*   **Symptom**: Code 跑通了测试，但 Runtime 报错。
*   **Healing**: `Observatory` (Log Analysis) 发现异常。
*   **Action**: AI 读取 Runtime Log，对比 Spec 定义。*"Spec 说这里应该返回 JSON，但 Log 报错 500。代码实现有误。正在生成 Fix..."* -> **Code Healed**.

#### Scenario 3: Legacy Chaos (遗留混乱)
*   **Symptom**: 接手一个只有代码没有文档的项目。
*   **Healing**: `Reverse Spec` 能力。
*   **Action**: Maglev 扫描 Code，自动生成初始 Spec。虽然不完美，但建立起了基准。 -> **Context Healed**.

## 2. Antifragility (反脆弱性)

Maglev 的系统**永远有机会**自愈。
只要三角中还有一个点是"真"的（比如代码还在跑），AI 就能利用这一点推导出另外两点。
*   有 Code 无 Spec -> Reverse Engineering.
*   有 Spec 无 Code -> Atomizer Generation.
*   有 Log 无 Spec/Code -> Behavior Analysis.

> **Conclusion**: Maglev 的核心不是"无懈可击的文档"，而是**"永不停歇的校准循环"**。这赋予了项目生物般的生命力。
