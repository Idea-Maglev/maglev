# 项目术语表

> 面向新贡献者与 AI Agent 的项目级术语账本：每个术语给出项目内定义、定义来源锚点、真实使用位置与当前状态。
> 新会话启动时由 reality-sync 加载，requirement-convergence 可直接引用。

## 1. 术语使用范围

| 范围 | 纳入术语 | 排除内容 | 命名来源 |
| --- | --- | --- | --- |
| 项目级跨域术语（生命周期 / 主流程 / 质量机制 / 文档体系 / 入口与治理） | 本页账本全部条目 | 单个能力域内部术语：由各域 capability / implementation 页面承载，不入项目级账本（事实按业务域组织，见 `specs/10_reality/00_profile.yaml:12-27` 的 `domains` 划分） | `.agents/skills/*/SKILL.md`、`AGENTS.md`、`specs/README.md` |
| 需求与文档编号体系 | `AC-F{N}-{M}`、`AC-I{N}-{M}`、EARS 中文关键词 | 运行时时点状态值（hooks trace、squad-kit lock、admission 阶段值等）：归 evidence / state 页面 | `.agents/skills/requirement-convergence/references/step-02-define-requirements.md`、`.agents/skills/spec-designer/references/interaction-requirement-template.md` |
| 演进中的候选术语 | 来自未结晶 active 主题的条目，以 `not_established` 入账 | 已否决或仅存于 90_archive 历史叙事的用词：不作为现行定义来源 | `specs/20_evolution/active/` 各主题 `status.md` |

> 排除依据：10_reality 不是需求文档镜像（无 F-x / AC-x 编号、无验收标准表）、不是过程归档（`AGENTS.md:52-55`）。

## 2. 术语账本

| 术语/缩写 | 项目内定义 | 来源锚点 | 使用页面/模块 | 状态 |
| --- | --- | --- | --- | --- |
| 10_reality | 项目当前已成立的事实基线，是理解现状的唯一信源 | `specs/README.md:8` | `specs/10_reality/`；`specs/10_reality/crosscutting/repository-map/overview.md:24` | established |
| 20_evolution | 仍在推进中的演进主题与待验证的设计 | `specs/README.md:15` | `specs/20_evolution/active/`；`specs/10_reality/crosscutting/repository-map/overview.md:24` | established |
| 90_archive | 历史依据与已结束主题的归档区，不作为当前现状入口 | `specs/README.md:19` | `specs/10_reality/crosscutting/repository-map/overview.md:24`；`AGENTS.md:55` | established |
| 结晶 (Crystallization) | 在综合验证后判断变化是否成立、把已成立变化写回 10_reality、收口 active 并回填可发现性的后段闭环动作 | `.agents/skills/crystallization/SKILL.md:3` | `AGENTS.md:73-82` 主链路；`specs/10_reality/spec-knowledge-layering/capability/overview.md:64` | established |
| 写回 (Writeback) | 将已成立的项目变化正式记录到 10_reality 的动作 | `.agents/skills/crystallization/SKILL.md:26` | `specs/10_reality/spec-knowledge-layering/capability/workflows.md:73` | established |
| 收口 (Close) | 对 active 演进主题的状态确定：结束 / 继续 / 拆分 | `.agents/skills/crystallization/SKILL.md:27` | `specs/10_reality/spec-knowledge-layering/verification/static-coverage.md:53` | established |
| 归档反模式 | 错误做法：直接搬运 active→archive 而未将结论写入 reality | `.agents/skills/crystallization/SKILL.md:114` | `specs/10_reality/spec-knowledge-layering/capability/business-rules.md:37`；`AGENTS.md:115` | established |
| Main Flow（主流程） | 核心工作链：entry-router → reality-sync → requirement-convergence → spec-designer → 执行分支（context-implementer \| code-execution-slot）→ integrated-validator → crystallization，横切 knowledge-check | `AGENTS.md:73-82` | `.agents/skills/entry-router/SKILL.md:49` | established |
| Skill（技能） | Maglev 的可执行能力对象，每个 Skill 负责特定工作阶段或任务；列表与生命周期状态以 private-catalog 为单一权威 | `AGENTS.md:69`；`public capability catalog:1` | `public capability catalog`；`AGENTS.md:64` | established |
| Reality Sync（现状同步） | 会话启动器：通过 Reality / Risk / Action / Mode 四类同步对齐仓库真实状态，输出 Session Brief | `.agents/skills/reality-sync/SKILL.md:19`；`.agents/skills/reality-sync/SKILL.md:35` | `AGENTS.md:76`；`specs/10_reality/session-reality-sync/capability/overview.md` | established |
| Requirement Convergence（需求收敛） | 入口分流→需求定义→Ready Gate→交接，确保需求边界明确 | `.agents/skills/requirement-convergence/SKILL.md:3` | `AGENTS.md:77` | established |
| Spec Designer（方案设计） | 需求边界稳定后通过受控对话与结构化流程形成可执行技术方案 | `.agents/skills/spec-designer/SKILL.md:3` | `AGENTS.md:78` | established |
| Context Implementer（上下文实施） | 方案依据清楚后完成受控的**非代码**实施、自检与对抗性审查；含代码交付物的方案由 code-execution-slot 路由，混合改动先 Slot 后 CI | `.agents/skills/context-implementer/SKILL.md:3`；`.agents/skills/context-implementer/SKILL.md:29` | `AGENTS.md:79` 执行分支；`.agents/skills/context-implementer/SKILL.md:55` | established |
| Integrated Validator（综合验证） | 需求↔规格↔代码↔测试的多维度交叉验证 | `.agents/skills/integrated-validator/SKILL.md:3` | `AGENTS.md:80` | established |
| AC（验收标准） | Acceptance Criteria，验证需求是否满足的具体判定点 | `.agents/skills/requirement-convergence/references/step-02-define-requirements.md:57` | 同文件 `:77`；`specs/90_archive/main_flow_quality_gates/context/requirement_template_preview.md:9` | established |
| AC-F{N}-{M} | 功能需求 AC 编号：F=功能序号，M=AC 序号；Maglev 自行设计 | `.agents/skills/requirement-convergence/references/step-02-define-requirements.md:77` | `.agents/skills/requirement-convergence/references/prd-output-contract.md:54`；`specs/90_archive/main_flow_quality_gates/context/requirement_template_preview.md:68` | established |
| AC-I{N}-{M} | 交互需求 AC 编号：I=交互需求序号，M=AC 序号；与 F 系并行、全局唯一 | `.agents/skills/spec-designer/references/interaction-requirement-template.md:78` | 同文件 `:14`、`:50`；`specs/90_archive/spec_document_architecture/context/design_interaction_template_preview.md:36` | established |
| EARS 格式 | 结构化需求表达，中文关键词：当…时 / 若…则 / 在…期间 / 应 | `specs/90_archive/main_flow_quality_gates/context/requirement_template_preview.md:69` | `.agents/skills/spec-designer/references/interaction-requirement-template.md:79` | established |
| Ready Gate | 需求收敛阶段的 AI 自检关卡，6 个条件全部满足才可进入方案设计；第 6 条要求把影响范围或设计方向的外部事实区分用户意图、直接观察、推断、历史和阻断状态 | `.agents/skills/requirement-convergence/references/step-03-ready-gate.md:29-37` | `.agents/skills/requirement-convergence/SKILL.md:26`；同文件 `:63` | established |
| 质量门禁 (Quality Gate) | 工作流检查点：AI 自检层 + 用户审批层，强制阻塞不合格产物 | `specs/90_archive/main_flow_quality_gates/01_requirements.md:1` | `specs/10_reality/spec-knowledge-layering/capability/overview.md:64`（floor/ceiling 卡点、admission 收据） | established |
| 对抗性审查 | 上下文实施中从相反角度检查实现一致性的机制 | `.agents/skills/context-implementer/SKILL.md:3` | 同文件 `:31`、`:61` | established |
| 需求覆盖表 | 设计文档中 AC→设计位置的映射表，确保每个 AC 至少被一个组件引用；Maglev 自行设计 | `specs/90_archive/main_flow_quality_gates/context/design_template_preview.md:103` | `.agents/skills/spec-designer/references/tech-spec-template.md:108` | established |
| 文档关系声明 | spec 文件中的上游/下游/平行引用，用于互联验证 | `specs/90_archive/spec_document_architecture/00_intent.md:20` | `specs/90_archive/reality-governance-convergence/00_index.md:21`（下游声明） | established |
| 交互需求文档 | 01_requirements_interaction.md，定义 UI 状态/操作响应/视觉约束/可访问性 | `.agents/skills/spec-designer/references/interaction-requirement-template.md:3` | 同文件 `:14`、`:50` | established |
| 交互设计文档 | 02_design_interaction.md，含 stateDiagram、组件 API、响应式策略 | `.agents/skills/spec-designer/references/interaction-design-template.md:3` | `specs/90_archive/spec_document_architecture/context/design_interaction_template_preview.md:1` | established |
| 输出合约 (Output Contract) | Skill 间的结构化交接协议，明确上游必须提供什么、下游期望什么；现行实例为 PRD Output Contract | `.agents/skills/requirement-convergence/references/prd-output-contract.md:6` | `.agents/skills/requirement-convergence/SKILL.md`（交接节） | established |
| Entry-Router | 会话入口路由器：识别请求类型、判断下游路径并交接 | `.agents/skills/entry-router/SKILL.md:3` | `AGENTS.md:75` 主链路首环 | established |
| Knowledge-Check | 知识沉淀检查：在会话切换或收尾时确认思考/方案是否已落盘，并做 9 段位段归类 | `.agents/skills/knowledge-check/SKILL.md:3` | `AGENTS.md:82` 横切能力 | established |
| 可发现性 (Discoverability) | 新写回的 reality 能否被后续会话有效发现；结晶触发地图与索引的可发现性回填 | `.agents/skills/crystallization/SKILL.md:28` | 同文件 `:43`、`:98` | established |
| _internal | `.agents/skills/` 下被多个 skill 共享、不作为独立分发入口的内部模块目录（distribution_scope: runtime_internal） | `public capability catalog:44` | `specs/10_reality/00_profile.yaml:874`（作为 evidence_refs 引用）；`specs/10_reality/agent-context-surface/operations/errors.md` | established |
| Extension Pack | 包含 `extension.yaml` 的可分发能力包，声明 skill、reference、script、template、validator 等资产 | `.agents/skills/extension-manager/references/extension-authoring.md:3` | `.agents/skills/extension-evolver/SKILL.md:3`；`specs/10_reality/delivery-runtime/implementation/extension-distribution.md` | established |
| Extension Registry | 由 `registry.yaml` 描述的扩展索引源；消费者项目通过 `.maglev/extensions.sources.yaml` 配置 | `.agents/skills/extension-manager/SKILL.md:102` | 同文件 `:69`；`specs/10_reality/delivery-runtime/implementation/extension-distribution.md:39` | established |
| asset_pack | CLI 安装并在 lock 中登记项目资产归属的扩展管理模式 | `.agents/skills/extension-manager/SKILL.md:109` | `specs/10_reality/delivery-runtime/implementation/extension-distribution.md:33` | established |
| external_integration | CLI 只检测和登记外部 provider 状态、不复制或修改 provider 资产的管理模式 | `specs/10_reality/delivery-runtime/implementation/extension-distribution.md:33` | `.agents/skills/code-execution-slot/protocol/scripts/resolve_slot.py:35` | established |
| Hooks 事实观测 | 从 hooks、文件系统和 parser 导出的独立可复算运行事实；不将模型文本或缺失退出码解释为结果 | `specs/90_archive/hooks-objective-observability/01_requirements.md:10` | `specs/10_reality/governance-quality/evidence/hooks-observability.md:35` | established |
| unverified | 当前证据不足以判断业务完成、skill 成功或命令结果时的显式状态；不等于失败、放弃或默认成功 | `specs/90_archive/hooks-objective-observability/01_requirements.md:71` | `specs/10_reality/governance-quality/evidence/hooks-observability.md:43` | established |
| 页面契约 (Page Contract) | 由 Pack 管理的单个逻辑页面生产与审阅义务：读者问题、专属结构、来源角色、图表条件、未知项、深挖入口和反模式 | `specs/90_archive/reality-agent-portability-baseline/01_requirements.md:78` | `templates/reality-packs/software-development/v2/root-pages/`（该主题 v2 Pack 页面契约资产） | not_established |
| 正向示例 (Positive Example) | 与模板和方法论双向关联的完整示例，用于展示页面如何用真实结构表达事实；不等同于可复制进业务 Reality 的正文 | `templates/reality-packs/software-development/v2/pack.yaml:153`（`positive_example_anchor` 声明） | `templates/reality-packs/software-development/v2/root-pages/*.md` 的「完整正向示例」节 | not_established |
| 人工审阅结论 (Human Review Decision) | 针对页面目的、方法论适配、事实—来源关系和示例可用性的独立审核结论；任何 Gate 未通过只能输出 `blocked`、`rework_required` 或 `not_proven`，不能由自动检查提升 | `specs/90_archive/reality-agent-portability-baseline/01_requirements.md:166`；同文件 `:197`（R-TPL-13 三层审核独立表达） | 同文件 `:83`（Reverse Review Result 交接对象） | not_established |

> 状态为 `not_established` 的三条来自 active 主题 `reality-agent-portability-baseline`（status: validation_blocked，未结晶），其定义随该主题演进，结晶后再转 established。

## 3. 别名、冲突与禁止推断

| 词语 | 别名/冲突 | 影响 | 当前处理 | 深挖 |
| --- | --- | --- | --- | --- |
| 上下文实施 | 与代码执行插槽 (code-execution-slot) 同属"实施"环节，易混用 | 代码交付物误走上下文实施会绕过扩展选择纪律 | 按 AGENTS.md 路由：spec 含代码交付物 → code-execution-slot；纯非代码 → context-implementer；混合先 Slot 后 CI | `AGENTS.md:79`；`.agents/skills/context-implementer/SKILL.md:55` |
| 收口 | 与"归档"曾被混用（AI 跳过结晶直接搬迁的归档反模式） | 结论不进 10_reality，事实层失真 | 结晶负责收口；归档受门禁：禁止将 20_evolution 直接搬到 90_archive | `.agents/skills/crystallization/SKILL.md:114`；`specs/90_archive/lifecycle_closure_disambiguation/README.md:20` |
| unverified | 易被读成"失败"或被当成"默认成功" | 误报业务失败，或掩盖缺失的证据 | unverified 是观测边界：不等于失败、放弃或默认成功 | `specs/10_reality/governance-quality/evidence/hooks-observability.md:43` |
| 现状同步 | 别名：Reality Sync / Session Bootstrapper（同一技能的中英文名） | 无语义冲突，仅表述差异 | 文档中以"Reality Sync（现状同步）"并列出现 | `.agents/skills/reality-sync/SKILL.md:3` |
| 综合验证 | 别名：Integrated Validator（formal_action_name: 综合验证） | 无语义冲突，仅表述差异 | 中英名并存，正式动作为"综合验证" | `.agents/skills/integrated-validator/SKILL.md:5` |
| 同名异义 | 项目级账本内未发现已登记的同名异义术语（检索口径：`specs/` 与 `.agents/skills/` 中"同名异义"仅命中 maglev-reverse-spec 的检查规则） | 新术语入账时可能引入同名异义 | maglev-reverse-spec 在数据结构分析中把"同名异义"显式标注为 MISMATCH；发现新冲突时经结晶回写本页登记 | `.agents/skills/maglev-reverse-spec/references/step-03-data-structure-analysis.md:71` |
| 正向示例 | 模板示例与项目事实的冲突风险：示例只说明表达形状 | 把模板示例复制为项目事实会伪造现状 | 页面契约规定正向示例不能复制为项目事实 | `templates/reality-packs/software-development/v2/root-pages/README.md`（落地约束节） |

## 4. 状态词解释

| 状态词 | 在 Reality 中的含义 | 不表示什么 | 依据 |
| --- | --- | --- | --- |
| established | 有直接证据（digest 绑定）支撑的当前事实；证据充分度 direct：证据文件逐字节可复核 | 不表示生产环境验证过，也不表示运行时成立 | `specs/10_reality/spec-knowledge-layering/evidence/claim-register.md:26` |
| unknown | 查过、无法成立的点；证据充分度 missing：写明缺什么 | 不是"没查过"，也不等于失败 | `specs/10_reality/spec-knowledge-layering/evidence/claim-register.md:27` |
| not_established | 有线索但证据不足；证据充分度 partial：部分证据，不得当 established 用 | 不是已成立事实，也不是被否决的结论 | `specs/10_reality/spec-knowledge-layering/evidence/claim-register.md:28` |
| not_applicable | 页面/契约对该模块不适用；须记录判断依据 | 不是"没有证据"的委婉说法 | `specs/10_reality/spec-knowledge-layering/evidence/claim-register.md:29` |

> 四个状态词的词表登记于 `specs/10_reality/00_profile.yaml:184-189`；状态来自来源角色与证据，不来自叙述流畅度（`specs/10_reality/spec-knowledge-layering/evidence/claim-register.md:31`）。
