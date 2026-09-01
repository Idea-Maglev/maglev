---
name: synthesize-review
description: 汇总 review findings，并给出唯一下一步建议
next_step: null
---

# Step 4: Synthesize Review

## 目标

把结果层 findings 汇总成统一 review 结论。

## 动作

1. 合并 compliance 和 quality/risk findings。
2. 区分 blocker、major、minor。
3. 如果是 Reality 结果，分别汇总 `structure`、`content`、`confidence` 三层状态，并保留
   candidate commit、baseline、Template Pack、Module Map、Gate A/B 和 Reality digest；
4. 给出唯一下一步建议：
   - 继续推进
   - 先修正实现
   - 转交综合验证

## 输出格式

- `consolidated_review_findings`
- `severity_split`
- `next_action`
