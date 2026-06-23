# Input Facts: Evolution Observatory

## 来源

- 需求收敛会话（2026-05-25）
- 已有对比文档分析（7+ 篇，docs/thinking/10_critique/）
- 行业研究实践经验（本会话 Superpowers + Windows MCP 研究）

## 核心事实

1. Maglev 已有 7+ 篇行业对比文档，但产出方式是 ad-hoc 的，无标准化流程
2. 现有对标对象：Superpowers v5.1.0、BMAD、OpenSpec、GitHub Spec Kit、快手 KDev、Hermes Agent、OpenAI Frontier
3. 每次研究由人主动触发，AI 执行深度分析
4. 产出需要长期可积累、跨会话可消费
5. Insight 有生命周期：open → proposed → absorbed / superseded
6. 机制本身作为 Maglev skill 存在，通过 SKILL.md + workflow + template 保证执行稳定性

## 已确认设计决策

| # | 决策 | 理由 |
|---|------|------|
| D-1 | 存储在当前仓库内分层 | 消费者是 Maglev 自身，同仓最小获取成本 |
| D-2 | Registry 用 YAML 格式 | AI 可解析 + 人可读 + Git diff 友好 |
| D-3 | 研究报告归档到 docs/thinking/10_critique/ | 延续已有实践 |
| D-4 | Insight 标记 superseded 需人确认 | 避免误废 |
| D-5 | 机制作为 skill 存在于 .agents/skills/ | 可被 entry-router 路由、每次执行强制读取 SKILL.md |

## 约束

- 不构建自动化定时触发
- 不直接产出代码变更（insight → spec-designer → code 路径）
- 维度体系需覆盖已有文档的主要对比轴
- Registry 需容纳已有和未来的对标对象
