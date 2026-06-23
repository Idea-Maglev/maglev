# Maglev 功能规划 — 基于 Observatory 竞品洞察推导

> **日期**: 2026-05-25
> **类型**: 功能规划 / 产品路线
> **数据源**: `specs/10_reality/competitive_registry.yaml` — 10 产品 22 条 insights
> **定位约束**: `specs/10_reality/positioning.md` — Maglev 是方法论+协议+能力集合，非编码工具

---

## 数据基础

| 产品 | Insight 数 | HIGH | MEDIUM | LOW |
|------|-----------|------|--------|-----|
| Superpowers | 3 | 0 | 1 | 2 |
| BMAD Method | 5 | 1 | 2 | 2 |
| OpenSpec (OPSX) | 3 | 1 | 1 | 1 |
| GitHub Spec Kit | 3 | 0 | 2 | 1 |
| 快手 CodeFlicker | 2 | 1 | 1 | 0 |
| Hermes Agent | 1 | 0 | 1 | 0 |
| Windows MCP | 1 | 0 | 0 | 1 |
| gstack | 3 | 1 | 1 | 1 |
| 跨产品元洞察 | 1 | 1 | 0 | 0 |
| **合计** | **22** | **5** | **9** | **8** |

**Response strategy 分布**: absorb(7), differentiate(4), watch(11)

**核心发现**: 22 条 insights 按 target 聚类后形成 **7 个功能方向**（见下文），其中 absorb 类 insight 直接驱动功能设计。

---

## 优先级体系

| 标签 | 含义 | 判定依据 |
|------|------|---------|
| P0 | 核心差异化 | HIGH 优先级 + demand_signal=high + maglev_applicability=high |
| P1 | 重要增强 | MEDIUM 优先级 + absorb 策略 |
| P2 | 有价值但不急 | MEDIUM + watch/differentiate |
| P3 | 远期储备 | LOW 优先级 or demand_signal=low |

---

## 功能列表

### F-1: 超轻量变更路径

| 维度 | 内容 |
|------|------|
| **描述** | 为 80% 的日常小变更（修 bug、调配置、加字段）提供一步 propose+apply 路径——一句自然语言 → tracked spec，不强制走完整的 requirement-convergence → spec-designer 流程。结合声明式意图路由，自动判断何时走轻量/何时走完整 |
| **优先级** | **P0** |
| **适用阶段** | 日常开发全程；entry-router 入口决策；hotfix/minor change 场景 |
| **为什么需要** | 当前 Maglev 的最短路径也需 5-10 分钟。80% 的日常变更不值得这个成本。用户要么跳过流程（知识丢失），要么觉得"太重"而放弃使用。这是 Maglev 留存率的 #1 瓶颈 |
| **证据** | ① **OPSX-002** (HIGH, differentiate): "80% 日常变更是小改动，不值得走完整流程" ② **GST-001** (HIGH, absorb): gstack PROACTIVE 声明式路由——自动发现最合适的 skill ③ **BMAD-005** (LOW, watch): "不同复杂度匹配不同深度流程" |
| **可借鉴产品** | |
| 1. **OpenSpec OPSX 流动工作流** | 一步 propose+apply，change 即 spec，不强制前置设计。**理由**: 直接竞品的直接解法——Maglev 需做到同等轻量但保留追溯 |
| 2. **gstack PROACTIVE 路由表** | `.gstack.md` 声明式映射 intent → skill，zero-config routing。**理由**: entry-router 可吸收此模式，用声明式配置替代硬编码路由 |
| 3. **Linear** | 一句话创建 Issue + 自动归类到 Cycle/Project。**理由**: 输入极轻但追溯完整——正是 Maglev 要的平衡 |
| **实现成本** | 🟢 低（1-2 周）。entry-router 增加 "quick-capture" 路径 + mini-spec 模板。声明式路由表需 2-3 周额外设计 |
| **对现有用户影响** | ✅ 高正向。所有用户立即受益——小事不再需要走全套。不影响大任务的完整路径 |

---

### F-2: 结构化决策记录（Decision Log）

| 维度 | 内容 |
|------|------|
| **描述** | 每个 Spec 附带决策追踪：[选项 A vs B → 选了 A → 因为 X]。轻量格式（不是 ADR 级别的长文档），嵌入 spec 的 front matter 或附属 section。支持跨会话查询"当初为什么选了这个方案" |
| **优先级** | **P0** |
| **适用阶段** | spec-designer 输出时自动记录；AI 新会话启动时读取；代码 review 时追溯 |
| **为什么需要** | AI 新会话不知道之前为什么选了某个方案 → 重复提问或做出矛盾决策。这是 AI 协作中"跨会话上下文丢失"的核心表现。人类开发者也有同样痛点——3 个月后回头看代码不知道为什么这样设计 |
| **证据** | ① **BMAD-001** (HIGH, absorb): "Per-Spec Decision Log 模式" — demand_signal=high, maglev_applicability=high ② KS-002 间接支持：个人效率≠组织效率的根源之一就是决策不可见 ③ ADR 社区实践：ThoughtWorks Tech Radar 推荐级别 |
| **可借鉴产品** | |
| 1. **BMAD Method** | 每个 Spec 自带 decision trail，在方案设计阶段自动记录"考虑了什么、选了什么、为什么"。**理由**: 同赛道直接竞品的成熟实践，已验证在 AI 工作流中有效 |
| 2. **ADR (adr-tools)** | Status/Context/Decision/Consequences 四字段格式。被 Netflix/Spotify/gov.uk 等采用。**理由**: 格式设计可参考，但需简化为 Maglev 风格（嵌入 spec 而非独立文件） |
| 3. **Notion AI Decision Matrix** | AI 辅助对比选项 + 自动记录决策理由。**理由**: "AI 原生决策记录"的用户体验参考 |
| **实现成本** | 🟢 低（1-2 周）。spec-designer 输出时新增 `decisions:` section；reality-sync 读取时加载决策上下文。格式：`- question: / options: / chosen: / rationale: / date:` |
| **对现有用户影响** | ✅ 高正向。所有用户受益——"为什么当时这样决定"是普遍痛点。作为 spec 可选 section，不增加强制负担 |

---

### F-3: Spec 质量门禁（可审计规则 + TDD 铁律）

| 维度 | 内容 |
|------|------|
| **描述** | 为 spec-audit-surface 增加可配置的质量规则集（类似 linter）：spec 完整性检查、一致性验证、测试覆盖要求。规则可开关、可自定义阈值。违反时阻断进入实施阶段 |
| **优先级** | **P1** |
| **适用阶段** | spec-designer 输出后、context-implementer 开始前（Gate 位置）；PR review 时辅助检查 |
| **为什么需要** | Spec 质量参差不齐——有的 spec 写了 intent 但没写 validation criteria，有的写了 scope 但没覆盖 edge case。AI 生成代码后不写测试或覆盖不足。缺少客观可审计的"合格线" |
| **证据** | ① **BMAD-002** (MEDIUM, absorb): "Spec Law 8 条可审计规则"——demand_signal=medium, maglev_applicability=high ② **SP-003** (MEDIUM, absorb): "TDD 铁律——强制测试纪律约束"——demand_signal=high, maglev_applicability=high ③ BMAD-003 (MEDIUM, absorb): "Activation 防跳步 Guardrails" |
| **可借鉴产品** | |
| 1. **BMAD Method Spec Law** | 8 条硬编码规则（每条都是 boolean pass/fail），跑通才允许进入下一步。**理由**: 直接可参考的规则集设计，且已证明"硬卡点"比"建议"更有效 |
| 2. **Superpowers TDD 铁律** | "没有测试先不写代码"——在 AI 编码中强制 test-first。**理由**: TDD 在 AI 时代更重要（AI 生成代码量大，没测试=技术债爆炸） |
| 3. **ESLint / SonarQube** | 可配置规则 + severity 级别 + 可关闭单条。**理由**: "可配置 linter"的用户体验已被全行业验证——Maglev 的 spec linter 应采用同样模式 |
| **实现成本** | 🟡 中（3-4 周）。需要：① 定义规则 schema（id/check/severity/message）② 实现 8-12 条核心规则 ③ 配置文件支持（哪些规则开/关/warn/error）④ 与 spec-audit-surface + test-design-surface 集成 |
| **对现有用户影响** | ⚠️ 需要平衡。规则太严会增加使用摩擦（与 F-1 冲突）。建议：默认 warn 不 block，用户可升级为 error。quick-capture 路径（F-1）走更松的规则集 |

---

### F-4: 接口标准化 + Combo Stack 兼容

| 维度 | 内容 |
|------|------|
| **描述** | 确保 Maglev 的核心输出（spec、decision log、validation result）有标准化格式，可被第三方工具消费。包括：① spec 输出格式规范 ② maglev-cli 支持多 IDE/Agent 平台集成 ③ 定义 Maglev 在 combo stack 中的"接口契约" |
| **优先级** | **P0** |
| **适用阶段** | 所有输出节点；与编码工具集成时；用户组合多工具时 |
| **为什么需要** | 市场趋势：用户习惯组合多工具（"combo stack"），不接受 monolith 锁定。如果 Maglev 的 spec 只能被自己的 context-implementer 消费，而不能被 gstack/Cursor/Windsurf 消费，用户会选择更开放的方案 |
| **证据** | ① **META-001** (HIGH, differentiate): "combo stack 趋势——Maglev 应确保关键接口标准化"——demand_signal=high ② **GSK-001** (MEDIUM, absorb): "Integration Registry 多平台适配"——GitHub Spec Kit 已支持 90+ extensions ③ positioning.md §4："Maglev 是编码工具的上游输入层和下游验证层" |
| **可借鉴产品** | |
| 1. **GitHub Spec Kit Integration Registry** | 支持 18+ presets × 90+ extensions × 多 AI 平台。用 JSON schema 定义输入输出格式。**理由**: 规模最大的同赛道产品，其 integration 设计是行业标杆 |
| 2. **MCP (Model Context Protocol)** | Anthropic 定义的 AI agent 工具接口标准。**理由**: 如果 Maglev 的 spec 能作为 MCP resource 暴露，任何支持 MCP 的 agent 都能消费 |
| 3. **OpenAPI Specification** | REST API 的标准化描述格式——证明"定义好输出格式"能催生整个生态。**理由**: spec-as-interface 的哲学验证 |
| **实现成本** | 🟡 中-高（4-6 周）。需要：① 定义 spec 输出的 JSON schema ② maglev-cli 增加 export 命令（`spec export --format <json|markdown|sdd>`）③ 编写 2-3 个 integration 示例（Cursor rules / gstack skill / Claude AGENTS.md 格式） |
| **对现有用户影响** | ✅ 高正向。现有用户最大痛点之一——"我用 Maglev 设计但用 Cursor 编码，中间手动复制粘贴"。标准化后自动流转 |

---

### F-5: 场景化 Bootstrapper（Preset 配置）

| 维度 | 内容 |
|------|------|
| **描述** | maglev-bootstrapper 支持场景化预设：`maglev init --preset solo|team|fde|enterprise`。每个 preset 预配置不同的 skill 组合、流程深度、规则严格度。新用户 30 秒内完成适合自己的初始化 |
| **优先级** | **P1** |
| **适用阶段** | 新用户初次安装；团队规模/场景变化时重新配置；FDE 为不同客户快速搭建 |
| **为什么需要** | 不同场景需要不同初始配置——solo 开发者不需要 crystallization，FDE 需要便携模式，企业团队需要审计规则。一刀切的 `maglev init` 要么太重（吓跑个人用户）要么太轻（企业用户觉得不够） |
| **证据** | ① **GSK-002** (MEDIUM, absorb): "Preset/场景配置模板"——GitHub Spec Kit 有 18+ presets 覆盖不同场景 ② KS-001 (MEDIUM, differentiate): "L1→L2→L3 演进"——preset 可对应不同成熟度阶段 |
| **可借鉴产品** | |
| 1. **GitHub Spec Kit Presets** | 18+ presets（minimal, standard, enterprise, mobile, data-pipeline 等）。**理由**: 同赛道直接参考，证明 preset 模式用户接受度高 |
| 2. **Create React App → Vite templates** | `npm create vite -- --template react-ts`——模板选择是前端工具的标准实践。**理由**: "init 时选模板"的 DX 已被验证 |
| 3. **Terraform Modules Registry** | 预制模块 + 组合使用。**理由**: "模块化预设 + 用户可覆盖"的架构模式 |
| **实现成本** | 🟡 中（2-4 周）。需要：① 定义 3-5 个 preset 的 YAML 配置（哪些 skill 开启/关闭、规则严格度、目录结构）② maglev-bootstrapper 增加 `--preset` 参数 ③ 允许 preset 继承和 override |
| **对现有用户影响** | ✅ 正向。现有用户可用 `maglev config apply-preset team` 快速调整配置。新用户上手体验显著改善 |

---

### F-6: 防跳步 Guardrails 强化

| 维度 | 内容 |
|------|------|
| **描述** | 增强 maglev-discipline 的"防跳步"机制：① 定义明确的 phase gate（哪些中间产物必须存在才能进入下一步）② 当 AI 试图跳步时强制拦截并解释为什么 ③ 可配置"哪些步骤可跳"（轻量路径允许跳，完整路径不允许） |
| **优先级** | **P1** |
| **适用阶段** | 主流程全程（requirement → spec → implement → validate）；AI agent 执行期间 |
| **为什么需要** | AI 天然倾向"直接给出结果"而非按步骤执行——跳过需求分析直接写代码、跳过测试直接提交。maglev-discipline 已有 L0-L4 压力框架，但缺少"在 AI 运行时的自动拦截"机制 |
| **证据** | ① **BMAD-003** (MEDIUM, absorb): "Activation 防跳步 Guardrails"——demand_signal=high, maglev_applicability=high ② GST-003: "Boil the Lake 完整性原则"——AI 时代完整实现的边际成本接近零 ③ WMCP-001: 4 层安全模型的"Capability"层=能力边界检查 |
| **可借鉴产品** | |
| 1. **BMAD Method Activation** | Phase 开始前检查前置条件是否满足，条件不满足=不允许激活下一步。**理由**: 同赛道最成熟的"防跳步"实现 |
| 2. **GitHub Actions required status checks** | PR 合并前必须通过指定 checks——证明"强制 gate"在开发工作流中被广泛接受。**理由**: "gate"模式的工程实践验证 |
| 3. **Kubernetes Admission Controllers** | 资源创建前拦截检查——不符合 policy 直接拒绝。**理由**: "拦截 → 解释 → 拒绝"的设计模式 |
| **实现成本** | 🟡 中（2-3 周）。需要：① 定义每个 phase 的 entry condition（前置产物清单）② 在 skill 之间的切换点增加检查逻辑 ③ 与 F-1（轻量路径）协调——轻量路径的 gate 更松 |
| **对现有用户影响** | ⚠️ 双面。对"想要纪律"的用户是核心价值；对"觉得已经很重"的用户可能是负担。关键：必须与 F-1 配合——确保轻量路径的 gate 足够松 |

---

### F-7: Skill 模板化体系

| 维度 | 内容 |
|------|------|
| **描述** | Skill 定义支持 schema + template 分离：共享逻辑（纪律规则、工具列表、安全约束）抽取为可继承的 base template，具体 skill 只需定义差异部分。支持模板生成（从 `.tmpl` 文件批量生成 SKILL.md） |
| **优先级** | **P2** |
| **适用阶段** | 新增 skill 时；skill 体系批量更新时（如纪律规则变更需同步 30 个 skill）；第三方贡献者创建 skill 时 |
| **为什么需要** | 当前 30 个 skill 有大量重复内容（纪律引用、tool 列表、安全规则）。修改一条纪律需要逐个更新。且第三方用户想定制 workflow 但不想/不能重写整个 SKILL.md |
| **证据** | ① **OPSX-001** (MEDIUM, watch): "schema+template 分离——用户想定制 workflow 但不想重写整个指令" ② **GST-002** (MEDIUM, watch): "Skill 模板生成（.tmpl → SKILL.md）——多 skill 有大量共享内容" ③ GSK-003 (LOW): Extension API 远期需要标准化 skill 接口 |
| **可借鉴产品** | |
| 1. **gstack .tmpl 模板机制** | 用 Go template 语法从基础模板生成 70+ skill 文件，共享 personality/tools/conventions。**理由**: 已验证在 70+ skill 规模下模板生成有效 |
| 2. **OpenSpec schema+template** | 用户定义 schema（字段）+ 覆盖 template（展现方式），不触碰核心逻辑。**理由**: "可定制但不可破坏"的设计哲学 |
| 3. **Yeoman / Cookiecutter** | 项目模板脚手架——问答式生成 + 变量替换。**理由**: 成熟的"从模板生成"DX 设计 |
| **实现成本** | 🟡 中（3-5 周）。需要：① 抽取 30 个 skill 的公共部分为 `_base.md` ② 定义继承/覆盖语法 ③ 构建 `skill generate` 命令 ④ 迁移现有 skill 到新格式（渐进式，不需一次全改） |
| **对现有用户影响** | ⚠️ 中性偏正。对日常使用无感（生成结果与现在一样）。对 skill 维护者/贡献者显著提效。风险：过度抽象可能增加理解复杂度 |

---

### F-8: 跨会话知识持久化

| 维度 | 内容 |
|------|------|
| **描述** | AI agent 在多次会话中学到的知识、偏好、上下文能持久化保存并在后续会话中自动加载。当前 knowledge-check 做"是否该记录"的判断，但存储仅为文件——需要结构化的知识图谱 + 按需加载 |
| **优先级** | **P2** |
| **适用阶段** | 每次会话启动时（reality-sync 加载）；跨会话的知识积累；团队知识共享 |
| **为什么需要** | AI agent 每次新会话从零开始——不记得上次讨论的偏好、项目的 quirks、失败过的方案。Maglev 的 crystallization 做知识沉淀，但沉淀的知识没有"自动回到 agent 上下文"的机制 |
| **证据** | ① **HERM-001** (MEDIUM, differentiate): "Skills 模块+跨会话记忆可参考 knowledge-check 持久化设计"——AI agent 跨会话丢失学习到的知识和偏好 ② positioning.md: Maglev 的核心价值是"沉淀资产"——但沉淀了不能用等于没沉淀 |
| **可借鉴产品** | |
| 1. **Hermes Agent 跨会话记忆** | 持久记忆模块，自动记住用户偏好和项目上下文，下次会话自动加载。**理由**: 同赛道产品的直接实现 |
| 2. **Cursor .cursorrules + memory** | 项目级持久配置 + AI 自动学习的记忆文件。**理由**: 轻量实现——单文件即可做到"下次还记得" |
| 3. **Mem0** | AI 应用的记忆层——分层存储（短期/长期/episodic），按需召回。**理由**: 最前沿的"AI记忆"技术方案，架构可参考 |
| **实现成本** | 🟡 中-高（4-6 周）。需要：① 定义知识条目格式 ② 实现"存入"机制（knowledge-check 已有判断，需增加结构化存储）③ 实现"召回"机制（reality-sync 启动时按相关性加载）④ 考虑知识过期/冲突处理 |
| **对现有用户影响** | ✅ 高正向。这直接解决"每次新会话都要重复解释项目背景"的痛。是 Maglev 与纯 AI coding tool 的关键差异化点 |

---

### F-9: 价值叙事体系（定位证据链）

| 维度 | 内容 |
|------|------|
| **描述** | 将"个人 AI 效率 ≠ 组织效率"作为 Maglev 价值叙事的核心证据，建立从问题定义→解法→证据→案例的完整叙事链。体现在 README、docs、onboarding 中 |
| **优先级** | **P0**（但属于文档/定位工作，非代码功能） |
| **适用阶段** | 用户首次了解 Maglev 时（README）；评估是否采用时（价值主张页）；向团队推广时（ROI 证据） |
| **为什么需要** | Maglev 当前缺少"为什么用你而不是直接用 AI coding tool"的有力回答。快手万人规模验证的"个人 AI 效率 ≠ 组织效率"是最有力的外部证据——用了 AI 代码量↑30% 但需求交付速度没变 |
| **证据** | ① **KS-002** (HIGH, differentiate): "'个人AI效率≠组织效率'作为 Maglev 价值定位证据"——demand_signal=high ② KS-001 (MEDIUM): "L1→L2→L3 组织级 AI 演进"——Maglev 帮用户从 L1 到 L2/L3 ③ positioning.md: Maglev 解决的是"漂移"，漂移在团队规模化后指数级放大 |
| **可借鉴产品** | |
| 1. **快手 CodeFlicker 公开演讲** | 万人规模数据证明"个人效率提升 ≠ 组织效率提升"。**理由**: 直接可引用的权威第三方证据 |
| 2. **Stripe 的 "increase the GDP of the internet"** | 用宏大叙事包装技术产品。**理由**: Maglev 可用"让 AI 时代的组织效率真正提升"做类似定位 |
| 3. **Basecamp "Shape Up"** | 通过出书和方法论传播来推广自家工具。**理由**: 方法论产品用内容营销而非功能营销 |
| **实现成本** | 🟢 低（1 周文档工作）。① README 增加"为什么不只是 AI coding tool"section ② 引用快手数据作为外部证据 ③ 设计 L1→L2→L3 演进叙事 |
| **对现有用户影响** | ✅ 纯正向。帮助现有用户在团队内推广 Maglev 时有"说辞"和证据 |

---

## 汇总视图

| # | 功能 | 优先级 | 成本 | 来源 Insights | 策略 | 实施阶段 |
|---|------|--------|------|--------------|------|---------|
| F-1 | 超轻量变更路径 | P0 | 🟢 低 | OPSX-002, GST-001, BMAD-005 | absorb+differentiate | Phase 1 |
| F-2 | 结构化决策记录 | P0 | 🟢 低 | BMAD-001 | absorb | Phase 1 |
| F-4 | 接口标准化 + Combo Stack | P0 | 🟡 中-高 | META-001, GSK-001 | differentiate+absorb | Phase 2 |
| F-9 | 价值叙事体系 | P0 | 🟢 低 | KS-002, KS-001 | differentiate | Phase 1 |
| F-3 | Spec 质量门禁 | P1 | 🟡 中 | BMAD-002, SP-003, BMAD-003 | absorb | Phase 2 |
| F-5 | 场景化 Bootstrapper | P1 | 🟡 中 | GSK-002, KS-001 | absorb | Phase 2 |
| F-6 | 防跳步 Guardrails 强化 | P1 | 🟡 中 | BMAD-003, GST-003, WMCP-001 | absorb | Phase 2 |
| F-7 | Skill 模板化体系 | P2 | 🟡 中 | OPSX-001, GST-002, GSK-003 | watch→长期 | Phase 3 |
| F-8 | 跨会话知识持久化 | P2 | 🟡 中-高 | HERM-001 | differentiate | Phase 3 |

---

## 实施路线建议

### Phase 1 — 核心差异化（3-5 周）

**目标**：让 Maglev 的核心价值可被感知且入门摩擦降到最低

| 功能 | 工作量 | 核心产出 |
|------|--------|---------|
| F-1 (超轻量路径) | 1-2 周 | entry-router 新增 quick-capture + 声明式路由 |
| F-2 (Decision Log) | 1-2 周 | spec 新增 decisions section + spec-designer 自动填充 |
| F-9 (价值叙事) | 1 周 | README 重写 + L1→L2→L3 框架 + 外部证据引用 |

**Phase 1 验证标准**：新用户从 init → 第一个 tracked spec < 60 秒；回到旧 spec 时能看到当初的决策理由

### Phase 2 — 生态就绪（6-10 周）

**目标**：让 Maglev 能嵌入用户已有工具链，且质量可保障

| 功能 | 工作量 | 核心产出 |
|------|--------|---------|
| F-4 (接口标准化) | 4-6 周 | spec JSON schema + export 命令 + 2-3 个 integration |
| F-3 (质量门禁) | 3-4 周 | 8-12 条 spec 规则 + 可配置 severity |
| F-5 (Preset) | 2-4 周 | 3-5 个 preset + init --preset 命令 |
| F-6 (防跳步强化) | 2-3 周 | phase gate 定义 + 运行时拦截 |

**Phase 2 验证标准**：Maglev spec 可被至少 2 个外部工具（Cursor + gstack）直接消费；spec 质量有客观衡量指标

### Phase 3 — 深度护城河（远期）

| 功能 | 触发条件 |
|------|---------|
| F-7 (Skill 模板化) | skill 数量 > 40 或第三方贡献者出现 |
| F-8 (跨会话知识) | 用户反馈"每次新会话重复说"排进 top 3 痛点 |

---

## 与 watch 类 Insights 的关系

以下 11 条 watch 策略的 insights 暂不驱动功能，但保持监控：

| ID | 标题 | 为什么 watch |
|----|------|-------------|
| SP-001 | Subagent 模式 | context-implementer 刻意轻量，不是 Maglev 核心 |
| SP-002 | Visual Companion | Maglev 不做 UI/前端层 |
| BMAD-004 | Forensic Investigation | 需求信号弱，applicability 低 |
| BMAD-005 | 复杂度自适应路由 | 已被 F-1 部分覆盖（声明式路由） |
| OPSX-001 | schema+template 分离 | 归入 F-7 远期 |
| OPSX-003 | 多仓库协调 | 需求信号弱，当前单仓库够用 |
| GSK-003 | Extension API | 需要 F-4 先就绪 |
| GST-002 | Skill 模板生成 | 归入 F-7 远期 |
| GST-003 | Boil the Lake | 哲学参考，已融入 F-6 |
| WMCP-001 | 4 层安全模型 | Maglev 非 OS 级，参考有限 |
| KS-001 | L1→L2→L3 演进 | 叙事参考，已融入 F-9 |

---

## 关键决策点

1. **F-1 与 F-3 的张力**：轻量路径越轻 → 质量门禁越难执行。解法：两套规则集（quick-capture 用 loose rules，full-spec 用 strict rules）
2. **F-4 的格式选择**：JSON Schema vs Markdown front matter vs 自定义 DSL。建议先 JSON Schema（工具链最成熟），Markdown 作为人类友好层
3. **F-8 的隐私边界**：跨会话记忆存什么、不存什么。建议默认 opt-in，且只存"项目级知识"不存"个人偏好"
4. **Kiro（AWS）空白**：Observatory 中 Kiro 尚无 insights——需要尽快深度调研，可能影响 F-4 方向

---

*综合推导自 10 产品 22 条 insights × positioning.md 锚定规则 × response_strategy 分类*
