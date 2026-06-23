# Combo Stack 趋势分析：Superpowers + OpenSpec + gstack

> **日期**: 2026-05-25
> **触发**: Observatory 校准阶段发现行业 combo stack 趋势
> **性质**: 战略级竞争分析 + Maglev 定位思考

## 现象

行业中出现了将多个 AI 编码框架组合使用的趋势：

- **OpenSpec**: 规格定义层 — "写什么"
- **gstack** (Garry Tan / YC): 组织/角色治理层 — "怎么组织"
- **Superpowers** (Jesse Vincent): 执行纪律层 — "怎么写"

三个工具各覆盖一个维度，组合后形成完整的 AI 编码流水线。

## gstack 概要

- **作者**: Garry Tan (Y Combinator President)
- **发布**: 2026-03
- **定位**: Role-based governance + strict phase gates for AI coding
- **核心特征**:
  - 角色分解 (CEO, Eng Manager, QA Lead, Release Manager)
  - 严格阶段门控 (/plan-ceo-review, /review, /ship, /qa)
  - 持久化 headless Chromium (QA 自动化)
  - Markdown skill files, MIT license
  - 跨平台 (Claude Code, Codex, Gemini CLI, Cursor)
- **哲学**: "Discipline > Model size" — 纪律和流程比模型能力更重要

## 为什么用户选择组合而非单一框架

| 单一工具不够 | 覆盖的维度 | 缺失的维度 |
|-------------|-----------|-----------|
| OpenSpec | spec 创建 ✅ | 执行纪律 ❌, 角色治理 ❌ |
| gstack | 角色/门控 ✅ | spec 方法论 ❌, 编码铁律 ⚠️ |
| Superpowers | 编码纪律 ✅ | spec 管理 ❌, 角色分离 ❌ |

**本质**：三个独立维度的需求同时存在且都足够强，但没有单一工具同时做好。

## Maglev 功能对标

| combo stack 角色 | Maglev 对应 | 覆盖程度 |
|-----------------|-------------|----------|
| OpenSpec (spec 创建) | requirement-convergence + spec-designer | ✅ 完整 |
| gstack (组织/角色) | entry-router + maglev-discipline + skill 体系 | ✅ 完整 |
| Superpowers (执行纪律) | context-implementer + integrated-validator | ✅ 完整 |

→ Maglev 在功能覆盖上等价于 3 工具组合，且有**集成深度优势**（跨层追踪）。

## combo stack 的优劣势对比

| 维度 | 3-tool combo | Maglev 一体化 |
|------|-------------|---------------|
| 灵活性 | ✅ 可换任一层 | ❌ 全或无 |
| 集成深度 | ❌ 手动对接，无共享状态 | ✅ spec→code→test 全链路追踪 |
| 入门门槛 | ⚠️ 学 3 个工具 | ⚠️ 学 1 个但更深 |
| 一致性 | ❌ 三套术语/范式冲突 | ✅ 统一术语和范式 |
| 社区规模 | ✅ 三个社区叠加 | ❌ 单一社区 |
| 维护负担 | ❌ 三个工具同步升级 | ✅ 一次升级 |
| 部分采纳 | ✅ 可以只用一个 | ❌ 难以只用 Maglev 的一个 skill |

## 战略选择分析

### 方向 A: "集成替代品"

> "为什么用 3 个工具？Maglev 一个就够，而且集成更深。"

- **优势**: 一致性、追踪能力、单一学习曲线
- **风险**: 用户感觉"太重"、锁定感、没有社区生态
- **适合**: 已经决定全面采纳的用户

### 方向 B: "可组合模块"

> "Maglev 的每一层可以独立使用，也可以和其他工具搭配。"

- **优势**: 灵活、可逐步采纳、降低切换成本
- **风险**: 集成深度下降、维护更复杂、定位模糊
- **适合**: 已有其他工具习惯的用户

### 方向 C: "集成优先，接口开放"（推荐）

> "默认一体化使用效果最好，但关键接口标准化，允许外部工具对接。"

- **例如**: spec-designer 输出标准格式 → 用户可以用 OpenSpec 替代 spec 层
- **例如**: context-implementer 接受标准 tasks input → 用户可以自己生成任务
- **优势**: 保留集成深度的同时降低采纳摩擦
- **关键**: 定义 2-3 个"接口契约"而不是全部标准化

### 建议方向 C 的具体接口标准化候选

| 接口 | 上游 | 下游 | 标准化收益 |
|------|------|------|-----------|
| `spec output format` | spec-designer 或外部 | context-implementer | 允许用其他工具写 spec |
| `tasks input format` | spec-designer 或外部 | context-implementer | 允许自定义任务拆解 |
| `validation result format` | integrated-validator | 外部 CI/report | 允许接入已有 CI |

## 新增 Insight

```yaml
- id: "META-001"
  title: "combo stack 趋势 → Maglev 应确保关键接口标准化"
  demand_driver: "用户习惯组合多工具，不接受 monolith 锁定；combo stack 是获客入口"
  demand_signal: high
  maglev_applicability: high
  response_strategy: differentiate
  target: "架构层 / installer / spec-designer output"
```

## 后续行动建议

1. 将 gstack 纳入 competitive_registry（high activity, 与 Maglev 高度重叠）
2. 在 spec-designer 的输出中定义标准化 schema（使其可被外部工具消费）
3. 考虑"渐进式采纳路径"：用户可以只安装 Maglev 的 discipline 层（对标 gstack），再逐步加 spec 层
