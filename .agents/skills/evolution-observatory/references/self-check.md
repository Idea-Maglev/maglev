# Self-Check Checklist

## 用途

每轮研究 Phase 6 执行。所有 `blocking: true` 项必须通过才能标记本轮完成。

## Checklist

| ID | 检查项 | Blocking | 说明 |
|----|--------|----------|------|
| CHK-1 | Registry 已更新 | ✅ Yes | 至少更新了 `last_researched` / `version_tracked`，或新增了 insights/products |
| CHK-2 | Open insights 已 review | ✅ Yes | Phase 2 已执行，结论已记录（即使全部保持 valid） |
| CHK-3 | 报告符合 output-template | ✅ Yes | M-1 ~ M-6 全覆盖（垂域可 N/A），Actionable Insights 章节存在 |
| CHK-4 | 新竞品探索已执行 | ✅ Yes | Phase 4 已执行，结果已记录（即使"未发现新竞品"） |
| CHK-5 | 报告已 commit | ✅ Yes | Message 以 `research(observatory):` 为前缀 |
| CHK-6 | 本轮摘要已输出 | ❌ No | 输出覆盖对象 + 新增 insights + Registry 变化 |

## 执行规则

1. 逐项检查，输出 ✅/❌ 状态
2. 任一 blocking 项为 ❌：
   - **不可标记本轮完成**
   - 明确指出缺失项
   - 提示 Creator 是否继续补齐或中止
3. 全部 blocking 项为 ✅：
   - 输出本轮摘要
   - 标记本轮完成

## 摘要输出格式

```
## 本轮研究摘要

- **覆盖对象**: {product name} ({version})
- **新增 Insights**: {N} 条（{列出 ID 和标题}）
- **Registry 变化**:
  - 产品更新: {list}
  - 新增产品: {list or "无"}
  - Insight 状态变更: {list or "无"}
- **新竞品发现**: {list or "本轮未发现"}
- **Dimension Upgrades**: {pending 变化 or "无变化"}
```
