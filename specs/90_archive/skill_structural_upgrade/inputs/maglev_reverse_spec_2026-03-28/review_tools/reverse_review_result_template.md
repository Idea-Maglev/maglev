# 逆向产物评审结果模板

## 适用场景
用于在完成一份 reverse 产物评分后，输出一份统一格式的评审结论。

适用于：
- 评审 `Lean / Standard / Deep` 任一档逆向结果
- 给团队同步逆向质量现状
- 为后续补充动作提供明确清单

---

## 模板

```markdown
# Reverse Review Result

## 1. Review Summary
- Review Target: {模块名 / 目录}
- Expected Profile: {Lean / Standard / Deep}
- Actual Profile: {Lean / Standard / Deep / 不合格}
- Reviewer: {人或 AI}
- Review Date: YYYY-MM-DD

## 2. Score Summary
- 骨架完整度: {x}/12
- 内容可信度: {x}/10
- 工程可用性: {x}/12
- 深度能力: {x}/10

## 3. Final Verdict
- 结论: {通过 / 有条件通过 / 不通过}
- 判断:
  - 当前结果达到 {Lean / Standard / Deep} 合格线
  - 当前结果未达到 {Lean / Standard / Deep} 合格线

## 4. Strengths
- {优点 1}
- {优点 2}
- {优点 3}

## 5. Gaps
- {缺口 1}
- {缺口 2}
- {缺口 3}

## 6. Redlines
- {是否触发红线问题}
- {如触发，列出具体项}

## 7. Recommended Actions
- P0: {必须补的内容}
- P1: {建议补的内容}
- P2: {可选优化项}

## 8. Suggested Next Step
- {建议直接补 Standard}
- {建议升级到 Deep}
- {建议先核实契约后再继续}
```

---

## 精简版模板

适合日常快速评语：

```markdown
结论: 当前 reverse 结果达到 {Lean / Standard / Deep} 合格线。
优点:
- ...
- ...

短板:
- ...
- ...

建议:
- 先补 ...
- 再补 ...
```

---

## 建议写法

### 1. 如果结果刚好合格
```markdown
结论: 当前结果达到 Standard 合格线，已可用于交接和改动前分析。
短板:
- Runtime / Security / RMM 仍未覆盖
- 测试映射仅能确认缺失，无法确认真实覆盖

建议:
- 如涉及高风险重构，继续补到 Deep
```

### 2. 如果结果接近但未达标
```markdown
结论: 当前结果接近 Standard，但尚未达到合格线。
主要问题:
- 缺少状态机
- 缺少数据字典
- 缺少明确 trace

建议:
- 先补足骨架层，再重新评审
```

### 3. 如果结果明显不合格
```markdown
结论: 当前结果不合格，尚不能视为可交接 reverse 产物。
红线问题:
- 没有架构图
- 没有主流程图
- 没有数据结构

建议:
- 按最低合格标准重做
```

---

## 与评分表配合方式

推荐顺序：
1. 先用 `reverse_review_scorecard.md` 打分
2. 再用本模板输出结论
3. 最后把 `P0 / P1 / P2` 补充动作回写到任务列表或 review comment 中
