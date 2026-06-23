# Intent

## 1. 当前目标

解决"归档"操作在 AI 辅助开发中被误解的问题：AI 助手将 `20_evolution` 内容直接搬运到 `90_archive`，导致结论从未进入 `10_reality`，项目现状永远过时。

同时修复 `knowledge-check` 与 `crystallization` 两个后段技能的触发边界模糊问题。

## 2. 这个主题只回答什么

1. "归档"请求应该触发什么操作（路由层）
2. knowledge-check 和 crystallization 各自在什么场景触发（边界层）
3. 两者同时需要时的执行顺序（时序层）
4. 如何防止 `20_evolution → 90_archive` 的直接搬运反模式（防护层）
5. 主流程关系链中缺失的 handoff 如何补齐

## 3. 这个主题不回答什么

1. crystallization 的 active 收口判定标准（END/CONTINUE/SPLIT）— 留给 crystallization 自身迭代
2. knowledge-check 的知识资产扫描逻辑改进 — 留给 knowledge-check 自身迭代
3. 其他扫描中发现的 MEDIUM/LOW 级别技能边界问题 — 留给后续主题

## 4. 问题来源

- 2.14 复盘中多位同学反馈"归档行为不符合预期"
- 技能边界全量扫描发现 3 个 HIGH 级问题（主流程关系链缺失、crystallization 触发缺失、错误恢复缺失）
- 实际使用中 AI 助手不能区分 knowledge-check 和 crystallization 的使用场景
