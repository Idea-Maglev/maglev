---
title: "系统架构与责任边界"
dimension: evaluator
audience: evaluator
page_type: reference
last_updated: "2026-10-08"
generator: wiki_authoring
---

# 系统架构与责任边界

Maglev 的静态架构由多个能力域、主流程入口、运行时和事实层组成。这里的关系图只表达来源中能够定位的静态责任和依赖；它不等于部署拓扑，也不证明每条运行链已经端到端验证。

> 面向正在评估 Maglev 的技术负责人与架构师：读完本页，你会了解能力域与主链路、相关方责任和跨系统依赖，并区分静态关系与未证实的运行结果。

## 三层结构：方法论、当前规则、技能

Maglev 不是单个工具，而是一套帮助团队在 AI Coding 时代稳定协作、持续交付并沉淀资产的方法论、协议和可执行能力集合。它关注的问题聚焦在一处：意图、设计、代码和验证之间的漂移——AI 放大了执行速度，也放大了这种漂移。在仓库内，这套能力以三层结构组织：

| 层 | 位置 | 回答的问题 |
|----|------|-----------|
| 方法论 | `docs/thinking/` | 为什么这样做 |
| 当前规则 | `.agents/skills/`、`.agents/workflows/`、`specs/10_reality/` | 当前执行边界、兼容入口和事实 |
| 技能 | `.agents/skills/` | 能做什么 |

三层分工让"为什么""现在是什么""能做什么"各自独立演化。`specs/10_reality/` 是当前事实层，登记能力域映射、模块间有静态锚点的关系，以及系统边界与未知项；评估架构时，这里是第一手核对对象。

## 证据可追溯：事实层怎么核对

"第一手核对对象"之所以成立，是因为事实层的每条声明都带可机械核对的凭据（机制见 [10_reality README](../../../specs/10_reality/README.md)）：

```mermaid
flowchart LR
    P["事实页<br/>reality_id + claim_refs"] --> R["claim 登记册<br/>脚本从 frontmatter 机械枚举"]
    R --> D["digest 绑定<br/>sha256 指纹"]
    D --> E["证据文件<br/>逐字节可复核"]
```

- **reality_id + digest 绑定**：每个能力域页面登记 `reality_id`，页面 claim 由脚本从 frontmatter 机械枚举入登记册，并以 sha256 digest 绑定证据文件——核对走逐字节复核，不走"读起来可信"。
- **knowledge_status 四态**：`established / unknown / not_established / not_applicable` 表达每条事实的证据充分度；状态不来自叙述流畅度，也不表示运行时验证通过。
- **边界诚实声明**：digest 一致不等于内容真实，"结构通过"不能包装成"内容真实"——这条限制写进机制本身，而不是留给评估者自己发现。

对评估的直接含义：架构声明可以逐条核对到证据文件，未证实的能力以 `unknown` 显式登记在已知缺口账本里，而不是从架构图上消失。

## 能力域与主链路

Maglev 的产品范围组织为 14 个能力域：协作生命周期、治理与质量、技能运行时、交付运行时、接入与集成、能力进化、机器索引引擎、项目地图、会话现状同步、知识沉淀、Agent 上下文面、规格知识分层、运营文档体系、发行知识。每个能力域有明确的 owning 模块与边界依据。

评估架构时，最值得关注的是贯穿这些能力域的主干技能链：

```mermaid
flowchart LR
    ER["entry-router · 入口分诊"] --> RS["reality-sync · 会话现状同步"]
    RS --> RQ["requirement-convergence · 需求收敛"]
    RQ --> SD["spec-designer · 方案设计"]
    SD --> EX["执行分支：context-implementer / code-execution-slot"]
    EX --> IV["integrated-validator · 综合验证"]
    IV --> CRY["crystallization · 结晶回写"]
    CRY -->|"回写长期结论"| REAL["specs/10_reality 当前事实层"]
```

主链之外，有几类支撑模块与它咬合：`code-execution-slot` 从项目 `.maglev/extensions.lock` 读取 enabled 候选，决定"用什么执行代码"；`extension-manager` 通过 install / enable / disable / update 命令维护这份 lock；`maglev-cli` 安装器在初始化时向 `AGENTS.md` 与 `llms.txt` 注入双入口骨架和受管区块，已存在的文件一律跳过、不覆盖用户内容；`index-librarian` 生成 `specs/` 与 `docs/` 各级 `INDEX.md` 索引网络；`maglev-map-maker` 从治理事实确定性生成唯一的人读项目入口 `docs/ATLAS.md`。

## 相关方与责任边界

相关方按任务和静态交互理解，不能仅凭角色名称推断人员安排或权限（[项目相关方与角色关系](../../../specs/10_reality/stakeholders.md)）。

| 参与方 | 静态交互 | 不能据此推断 |
|---|---|---|
| 维护者与贡献者 | 维护事实、规则、索引或发行资产 | 具体人员指派、排期或绩效 |
| 开发者与 AI Agent | 按协作主流程工作，Agent 消费受管上下文 | Agent 实际响应质量或绕过治理门禁 |
| 技术评估者 | 核对定位、架构、能力与证据 | 未有证据支持的收益或运行保证 |
| 外部仓库与 Provider（外部能力提供方） | 在扩展分发与发布链中交互 | 网络可达、授权有效、远端写入成功或 Provider 业务能力 |

## 跨系统依赖与运行未知

同进程模块关系与跨系统依赖分开查看；下表只登记静态交互锚点（[系统依赖与集成边界](../../../specs/10_reality/system-dependencies.md)）。

| 依赖 | 已登记用途 | 当前边界 |
|---|---|---|
| Git 发布源 | 安装器读取发行清单与文件；环境变量 `MAGLEV_UPSTREAM_URL` 可覆盖默认上游 | 可达性、缓存和自动重试未知 |
| `uv`（Python 环境管理工具）与系统 Python | 为协议脚本提供运行环境；系统 Python 是回退路径，默认目标版本为 3.11 | 所有发行版兼容性与两种运行时均缺失时的行为未知 |
| Node.js（JavaScript 运行环境） | 扩展 CLI 声明需要 `>=20.0.0` | 版本不匹配时是否实际拒绝尚未验证 |
| Git 扩展源仓库 | 搜索、克隆和探测扩展源 | 网络、鉴权与 Provider 运行结果未知 |
| npm（Node.js 包管理器）包仓库 | CLI 发布与版本验证 | 仓库可用性和实际发布完成度未知 |

这些条目不证明网络可达、授权有效、远端副作用成功或端到端运行关系成立；详细限制以对应事实页为准。

## 与编码工具的上下游关系

Maglev 不是编码工具的替代品，而是编码工具的**上游输入层**和**下游验证层**。上游供什么、下游查什么，可以分开看：

```mermaid
flowchart LR
    Spec["高质量 Spec"] --> Generation["更准确的代码生成"]
    Boundary["明确的执行边界"] --> Scope["更少的越界实现"]
    Evidence["验证依据和完成标准"] --> Validation["代码可被验证"]
    Assets["可沉淀的资产"] --> Maintenance["后续可维护"]
```

上游侧，Maglev 把模糊输入整理成高质量 Spec、明确执行边界、给出验证依据，编码工具据此生成更准确、越界更少的代码。下游侧，Maglev 对生成结果做对齐检查：验证依据与完成标准让代码可被验证，沉淀的资产让后续可维护。

代码执行走 `code-execution-slot`：Slot 从 `.maglev/extensions.lock` 读取 enabled 候选，Agent 根据任务上下文和选择说明加载对应 `entry_skill`；没有合适候选时回退到 agent-native 执行。这里有两道硬约束：扩展不会自动进入所有上下文，也不能绕过需求和方案阶段。编码工具侧不限定具体 provider——Maglev 更偏好能直接消费 Spec、遵循边界并返回测试与 review 证据的工具。

## 刻意边界：不做什么

| 不做的事 | 原因 |
|---------|------|
| 替代代码生成层 | 已有成熟的外部编码工具 |
| 追求编码层的"更强" | 那是编码工具的战场，不是 Maglev 的 |
| 运维 / 部署 / 监控 | 不是 Maglev 的定位，交给 CI/CD 等工具 |
| 做平台 / IDE | Maglev 是协议层，不锁定任何平台 |

这些边界对评估的直接含义：编码工具选型仍是独立决策，Maglev 不在这一层参与竞争；它改变的是这些工具收到的输入质量和产出被检查的方式。

## 下一步

- 看五个阶段如何衔接、各阶段产出什么：[核心工作流](lifecycle-and-governance.md)
- 看 Maglev 与相邻概念各自的战场：[与相邻概念的边界](../business/comparisons.md)
- 看扩展机制与集成边界：[扩展机制与集成](runtime-and-extensibility.md)
- 准备接入时，从安装开始：[安装 maglev-cli](../developer/first-success.md)
