---
name: audit-requirements
description: 审查 requirements 的清晰度、边界和可验证性
next_step: references/step-03-audit-spec-cluster.md
---

# Step 2: Audit Requirements

## 目标

审查 requirements 是否已经具备进入后续工作的最低质量。

## 动作

1. 检查范围、非目标、成功信号是否清楚。
2. 检查需求是否可执行、可验证。
3. 检查是否存在明显冲突、缺失或模糊表达。
4. 检查 requirements 是否存在“来源依据”章节。
5. 检查关键 AC 是否包含：验收标准、来源摘要、上下文判定、证据。
6. 执行正向来源检查：每条正式 AC 是否都有可理解的来源摘要、上下文判定和证据。
7. 执行反向覆盖检查：来源依据中列出的主要来源，其有效需求信息是否已被 AC 覆盖，或被明确标为不采纳、待确认、out of scope。
8. 检查 AI 对话来源是否只以摘要形式进入 requirements；高价值思考是否被建议沉淀到 `docs/thinking/`，而不是塞进需求正文。

## Provenance finding 分级

- `blocker`: 正式 AC 无来源摘要、上下文判定或证据；AI 语义变更缺少变更记录。
- `major`: 来源中有效需求信息未被 AC 覆盖，且可能影响需求、验收或范围。
- `minor`: 证据可回查性不足，但不影响当前设计方向。

## 输出格式

- `requirements_audit_result`
- `requirements_findings`
