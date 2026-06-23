# Documentation Strategy Analysis (文档策略分析)

## 1. 验证：交互式导读 (Interactive Guide)
*   **状态**: ✅ **已支持** (Native).
*   **证据**: 
    *   Maglev 本身就是基于 Chat 的。用户天然可以随时问："帮我总结这个 Spec"。
    *   `maglev-tutor` 技能提供了更结构化的引导。
    *   **结论**: 不需要专门的"新机制"，只需要培养用户的习惯 (Prompt Habit)。

## 2. 策略对比：分层 vs 锚点 (Layering vs Anchors)

### Strategy 1: Explicit Layering (显性分层)
*   **机制**: 物理隔离。Zone 1 (Brief) 在头部，Zone 2 (Details) 在中部，Zone 3 (Context) 在底部/折叠。
*   **优点**: 
    *   **Cognitive Relief**: 打开文档看到的不再是满屏细节，而是清晰的摘要。
    *   **Audience Friendly**: 业务方只看 Zone 1，技术方看 Zone 2。
*   **缺点**: 
    *   **Redundancy**: 摘要和正文可能存在部分重复。
    *   **Maintenance**: 改了正文容易忘改摘要 (Sync Risk)。

### Strategy 2: Visual Anchors (视觉锚点)
*   **机制**: 混排。在段落前加 Emoji (👤/🤖/⚠️)。
*   **优点**: 
    *   **Compact**: 文档紧凑，无冗余。
    *   **Contextual**: 决策和上下文紧挨着，方便追溯。
*   **缺点**: 
    *   **Noise**: 如果 AI 生成内容占比 80%，整篇文档即使有 Emoji 看起来还是很累。
    *   **Search Cost**: 用户仍需"扫视"全文来寻找 Emoji。

## 3. 推荐结论 (Recommendation)
**首选 Strategy 1 (显性分层)**。

**理由**:
1.  **痛点匹配**: 用户反馈的是 "看不懂" (Too Much Information)。Only Layering can explicitly **hide** the noise.
2.  **行业标准**: 这符合经典的 "Pyramid Principle" (金字塔原理) —— 结论先行。
3.  **可实施性**: 我们可以调整 Spec 模板，增加一个 `# Executive Summary` 章节，强制 AI 填充。

## 下一步建议
修改 `maglev-spec-draft` 或 `maglev-create-prd` 的 Prompt 模板，增加 "Executive Summary" 章节要求。
