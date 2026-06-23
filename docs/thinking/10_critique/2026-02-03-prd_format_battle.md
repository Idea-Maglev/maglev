# Critique: PRD 格式之争 (User Story vs OpenSpec)

> **背景**: 我们最近将 PRD 标准从敏捷通用的 "User Stories" 升级为 "OpenSpec" (Gherkin/BDD)。这真的是更好的选择吗？

## 1. 选手介绍 (The Contenders)

### 选手 A: 敏捷经典 (User Story)
*   **格式**: `作为 <用户>, 我想要 <行为>, 以便 <价值>` + `AC: 1. 登录成功...`
*   **哲学**: **同理心驱动 (Empathy-driven)**。关注 "Who" (谁) 和 "Why" (为什么)。
*   **优势**:
    *   ✅ **易读性**: PM 和业务方喜欢，通俗易懂。
    *   ✅ **价值导向**: 时刻提醒我们关注业务价值，而非实现细节。
*   **劣势**:
    *   ❌ **歧义性**: "登录成功" 这四个字背后可能隐藏着 100 种不同的技术实现。
    *   ❌ **AI 摩擦**: LLM 经常因为逻辑不严密而产生幻觉，补充错误的细节。

### 选手 B: 工程师之选 (OpenSpec / Gherkin)
*   **格式**: `需求: 支持登录` -> `场景: 验证通过` -> `GIVEN 有效凭证 WHEN 提交 THEN 返回 Token`。
*   **哲学**: **逻辑驱动 (Logic-driven)**。关注 "State" (状态) 和 "Behavior" (行为)。
*   **优势**:
    *   ✅ **零歧义**: `GIVEN/WHEN/THEN` 强制确立因果逻辑。
    *   ✅ **可测试**: 直接映射到自动化测试用例 (Vitest/Jest)。
    *   ✅ **AI 原生**: LLM 在严格的逻辑指令下表现极其稳定。
*   **劣势**:
    *   ❌ **认知负荷**: 对非技术人员来说，阅读起来很枯燥，像在读代码。
    *   ❌ **啰嗦**: 结构化文本带来的"样板代码" (Boilerplate) 显著增加。

## 2. 裁决 (The Verdict)

这并不是非黑即白的选择，而是 **同理心 (Empathy) 与 精确度 (Precision) 之间的权衡**。

*   **对于 "探索" (Why)**: User Story 更好。它捕获了 *意图*。
*   **对于 "交付" (How)**: OpenSpec 更好。它断言了 *正确性*。

### Maglev 之道: 混合分层 (Hybrid Layering)

我们不需要为了一个杀掉另一个，**Three-Zone Architecture (三区架构)** 让我们鱼与熊掌兼得：

1.  **Zone 1 (决策摘要)** & **Zone 3 (溯源)**: 使用 **User Story** 的语言。讲清楚 "Why" 和 "Value"，给人类看。
2.  **Zone 2 (需求规格)**: 使用 **OpenSpec/Gherkin**。定义严格的执行逻辑，给 AI (生成代码) 和 QA (生成测试) 看。

**核心逻辑**:
Executive Brief 告诉 *人类* 我们为什么要做这个。
Zone 2 Spec 告诉 *AI/开发* 具体怎么构建和测试它。

### 建议 (Recommendation)
在 Zone 2 (核心规格) 坚持使用 **OpenSpec** (这更适合 Agentic Coding)，但在 Zone 1 (摘要) 务必保持高层级、充满同理心的即视感。
