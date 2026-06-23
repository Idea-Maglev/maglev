---
type: thinking-note
segment: 70_retrospective
status: active
linked_to:
  - docs/thinking/70_retrospective/2026-04-27-multi_round_reflection_session.md
---

# 治理类清洗会话反思（2026-04-29）

## 会话内容速描

一次围绕 `artifact-purity-keeper` 工具能力进行 dogfooding 的会话，最终落地两条清洗主题：

1. **协议产物归位**：`_internal/docs-index-protocol/` → `index-librarian/protocol/`，并更名为 `index-protocol`（去掉 `docs-` 前缀，因为它已经服务 4 类 track，不只是 docs）
2. **SKILL.md narrative-shift 三件套清理**：16 个 SKILL.md 的 "已确认/已切换为/仍保留" 命名演进叙事统一替换为干净陈述

两条工作分别落在：
- `refactor/merge-index-protocol-into-librarian`（2 commits）
- `fix/skill-narrative-shift-cleanup`（1 commit）

## 三个值得留下的教训

### 1. 报告类任务的"案例锚定窄化"是认知偏差

会话中我先扫了 crystallization skill 的"本轮"用例修复，再扫全 28 skill 出报告。报告 v1 把 relative-time 真火重点压在"本轮"上，并笼统说 process-code "多数合法"。

**真相**：
- `relative-time` 61 处中"本轮"57 处几乎全是协议泛指，真污染密度极低
- `process-code` 中 Step N 71 处也几乎全是 SKILL.md 描述自家步骤，是合法协议描述
- **真重灾户是 `_internal/docs-index-protocol/`**：~10 处 D/AC 内部决策编号 + Phase 演进阶段叙事，被报告 v1 完全略过

**根因**：拿手头一个新案例当所有同规则 finding 的代表。这是**典型的认知锚定**。

**防范策略**（已写入扫描器报告 v2 末尾）：
- 给每个规则**单独审视子模式分布**
- 按文件具体审样本，不直接基于规则名归纳
- 对扫描类任务，输出报告时按规则正则的所有子模式分别抽样

### 2. "先报告再行动" 在扫描类任务中尤其重要

扫 crystallization 时我连续提了两个未授权的扫描器优化 commit（dcbea90、3e763bb），用户明确指出"加重了管理成本"。

**纪律**：
- 扫描类任务 = 报告类任务，不应在没有用户决策的情况下直接扩散到周边修复
- 即便发现"顺手能修的小问题"，也应先列出请用户确认，再批量执行
- 区分"完成本任务"和"开启新任务"：扩展扫描规则属于新任务

### 3. 治理类操作不该硬塞进 maglev 主流程

本会话的两条主题都没在 `specs/20_evolution/active/` 下建立载体，工作量也不值得反向构造 spec 文档。最初尝试走 crystallization 流程归档，被自身的反模式挡住：

> ❌ 将 `20_evolution/active/` 内容直接搬运到 `90_archive/`
> ❌ 在未将结论写入 `10_reality` 的情况下执行归档

**正确去向梯度**（治理类操作）：
| 工作量 | 去向 |
|---|---|
| 仅代码改动，无方法论沉淀 | git history + commit message 即可 |
| 有可推广的方法论或反思 | `docs/thinking/70_retrospective/` |
| 改变了项目能力级当前事实 | 回写 `specs/10_reality/` |
| 真正具备 active 主题量级（多周期、多人协作、有验证关卡） | 走完整 maglev 主流程再归档 |

本次清洗用 git history + retrospective 两件就足够。

## 工程级副产物

| 产物 | 收益 |
|---|---|
| `index-librarian/protocol/` 自包含 | 协议与编排者闭环，无需跨目录引用，与 `artifact-purity-keeper/scripts/` 同构 |
| `index-protocol` 改名 | 名实相符（已服务 4-track，不再是 docs-only） |
| 16 个 SKILL.md 统一陈述风格 | 首读者不再被"已切换为/仍保留"的演进叙事干扰 |
| `_internal/docs-index-protocol/` 内部产物 0 findings | 协议正文回归"当前事实"，决策编号与 Phase 叙事剥离 |

## 一句话总结

**报告类任务最容易栽在"被一个生动案例带偏"，治理类任务最容易栽在"硬套主流程范式"。两者的解药都是回到第一性问题：当前要解决的真实分布是什么？这个工作的最小有效记录方式是什么？**
