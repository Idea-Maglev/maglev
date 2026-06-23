# Visual Cross-Verification Strategy (视觉交叉验证策略)

> **Context**: 2026-01-31 讨论归档。关于如何解决 Maglev 体系下 "带页面的项目" 如何做自动化交叉验证的问题。
> **Core Problem**: 前端验证涉及 "Pixel Perfect" (易脆) 和 "Interaction" (复杂) 双重挑战。

## 1. 验证分层模型 (verification Layering)

我们将前端验证拆解为三层，每层采用不同的技术手段：

| 层级 | 验证对象 | 推荐技术 (Tech Stack) | 稳定性 | 成本 |
| :--- | :--- | :--- | :--- | :--- |
| **L1: 骨相 (Tokens)** | Design System (Color, Spacing, Font) | **Storybook + CI Lint** | ⭐⭐⭐⭐⭐ | Low |
| **L2: 皮相 (Visual)** | Layout, Styling (Look & Feel) | **AI Visual Regression** (Applitools/Percy) | ⭐⭐⭐⭐ | Medium |
| **L3: 灵魂 (Interaction)** | Flows, Logic, State Changes | **Spec-Driven E2E** (Playwright + AI) | ⭐⭐⭐ | High (Old Way)<br>Low (Maglev Way) |

## 2. Maglev 解决方案 (The Maglev Way)

利用 Maglev 的 **Standard Spec Structure** 作为自动化验证的 "真理源头" (Source of Truth)：

1.  **对于 L2 (Visual)**:
    *   **Spec**: `specs/.../assets/` 目录存放 "Golden Snapshots" (由 Librarian 自动从 Figma 同步)。
    *   **Action**: AI 验证 Agent 读取 `assets/` 中的截图，与从 dev server 抓取的截图进行 "语义级比对" (Semantic Diff)，忽略微小的渲染差异。

2.  **对于 L3 (Interaction)**:
    *   **Spec**: `specs/.../02_design.md` 中的 **Interaction Table** 定义了 `Component -> Event -> Action`。
    *   **Action**: AI 验证 Agent 解析 Interaction Table，自动生成 Playwright 测试脚本。

## 3. 结论 (Conclusion)
*   **可行性**: 现代 AI 工具已解决了 "UI 测试维护成本高" 的痛点。
*   **关键路径**: 必须先落实 **Spec 结构化标准** (特别是 `assets/` 和 `Interaction Table`)，后续的自动化验证才有可能。
