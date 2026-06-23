# Requirements — 主流程质量门禁

## 来源

- `issues/active/kiro_inspired_flow_improvements/01_approval_gates.md`（P0，已讨论完成）
- `issues/active/kiro_inspired_flow_improvements/02_structured_requirements.md`（P0，已讨论完成）
- `issues/active/kiro_inspired_flow_improvements/03_task_dependency.md`（P1，已讨论完成）
- `issues/active/kiro_inspired_flow_improvements/04_audit_scoring.md`（P1，已讨论完成）
- `issues/active/kiro_inspired_flow_improvements/05_project_steering.md`（P2，已讨论完成）
- Kiro for Claude Code 深度分析：`docs/thinking/20_architecture/kiro_for_cc_analysis_2026_04_13.md`
- 2.14 复盘 P0：需求遗漏率 24%、PRD→Spec 断裂

## 范围说明

> 本 spec 聚焦**主流程质量机制**：审批门禁、需求结构化、AC 追溯链、任务依赖图、审计评分、AI 引导。
>
> **不在本 spec 范围**（已移入 `spec_document_architecture`）：
> - 文档拆分（功能/交互分文件）
> - 交互需求/设计模板
> - 术语表机制
> - 文档互联互验
> - maglev-design-ux 定位

---

## 功能需求 F-1: 阶段交接强制审批

**用户故事**: 作为 Maglev 主流程的使用者，我希望在关键阶段交接前被要求确认内容，以便及时发现 AI 理解偏差

**验收标准**:

- AC-F1-1: 当 requirement-convergence 的 Ready Gate 通过且将交接给 spec-designer 时，系统应先向用户展示核心产物摘要（核心对象、InScope/OutScope、关键 AC），然后等待用户明确确认
- AC-F1-2: 若用户在审批时提出修改，则系统应回到 step-02 补齐，而非强制继续交接
- AC-F1-3: 当 spec-designer 的 draft 完成时，系统应先展示关键设计决策摘要，询问"设计方向是否正确"，获得确认后再提供操作方式选择（直接因化/手动修改/重新生成）
- AC-F1-4: 当 spec-designer 的 verify-output 结构检查通过后，系统应展示 spec 产出概要，询问"是否可以进入实施"
- AC-F1-5: 在所有审批点，系统应记录审批结果（谁确认、确认时间、确认内容摘要）到 spec 上下文

**边界情况**:
- 用户不可通过任何方式跳过审批（暂不提供快速模式）
- AI 不可自行判断"用户的回复等同于确认"——必须是明确的肯定信号

---

## 功能需求 F-2: 结构化行为级需求格式

**用户故事**: 作为方案设计的消费者，我希望需求产物中每条功能需求都有可测试的验收标准，以便设计和测试有明确的行为基线

**验收标准**:

- AC-F2-1: 当 requirement-convergence 进入 prd_document 模式时，输出的结构化需求文档应包含功能需求列表，每个功能需求至少包含：用户故事 + 1 条以上 AC
- AC-F2-2: 每条 AC 应符合格式"当 [触发条件] 时，系统应 [响应行为]"或"若 [前置条件]，则系统应 [响应行为]"，不允许仅写"支持 X 功能"
- AC-F2-3: AC 编号应采用 `AC-F{N}-{M}` 格式（F=功能需求编号，M=AC 序号），全局唯一
- AC-F2-4: 当不需要行为级需求时（简单任务、修复类），结构化需求文档可为空，系统应保持当前边界收敛格式不变
- AC-F2-5: AI 应根据 in_scope 和用户描述先自动生成初版 AC，用户审核修改，不逐条追问

**边界情况**:
- 如果用户提供的功能描述过于模糊无法生成 AC，AI 应先追问"这个功能在什么条件下触发？预期什么响应？"
- 非功能需求（性能、安全等）暂不要求 AC 格式，保持自由文本

---

## 功能需求 F-3: AC 编号下游引用与设计文档规范化

**用户故事**: 作为 integrated-validator 的使用者，我希望 AC 编号贯穿需求→设计→任务→测试全链路，并且设计文档有标准化结构，以便做精确的一致性检查和质量审计

**验收标准**:

- AC-F3-1: 当 spec-designer 生成 02_design.md 时，文档应包含「需求覆盖表」，列出每个 AC 在设计中的落地位置
- AC-F3-2: 当 spec-designer 生成 02_design.md 时，文档应包含标准化的必须小节：Overview、需求覆盖表、架构图（Mermaid）、组件职责表（含「覆盖 AC」列）、设计决策表
- AC-F3-3: 当 spec-designer 生成 03_plan.md 的任务列表时，每个任务应标注其覆盖的 AC 编号（格式：`_需求: AC-F1-1, AC-F2-3_`）
- AC-F3-4: 当 AC 编号在下游文档中被引用但源需求中不存在该编号时，系统应在审计时标记为一致性问题
- AC-F3-5: 设计文档中的需求覆盖表应确保每个 AC 至少被一个设计节引用，否则审计时标记为「未覆盖 AC」

**边界情况**:
- 如果输入需求不包含结构化 AC（简单任务），设计和任务文档不要求引用 AC 编号
- 设计文档的可选小节（数据流图、接口定义等）按项目类型适配，不强制填写

---

## 功能需求 F-4: 任务依赖图与执行编排

**用户故事**: 作为使用 context-implementer 执行任务的开发者，我希望任务之间的依赖关系被显式表达，以便 AI 按正确顺序执行且能识别可并行任务

**验收标准**:

- AC-F4-1: 当 spec-designer 生成 03_plan.md 时，文档应包含「实施任务」区段，每个任务格式为 checkbox + 编号 + 描述 + AC 引用（如 `- [ ] T1: 描述 → AC-F1-1, AC-F2-3`），最多 2 层层级
- AC-F4-2: 当实施任务超过 3 个时，03_plan.md 应包含「任务依赖」区段，使用 Mermaid flowchart 表达任务间的依赖关系，标注可并行任务
- AC-F4-3: 当 context-implementer 执行任务且 plan 包含依赖图时，应按拓扑排序确定执行顺序，可并行任务根据复杂度决定是否批量执行
- AC-F4-4: 当 context-implementer 完成一个任务时，应将对应 checkbox 标记为 `[x]`，只改状态不改描述和依赖图

**边界情况**:
- 简单任务（≤3 步）可用扁平列表，不要求依赖图
- plan 不包含依赖图时，context-implementer 保持当前行为（按列表顺序串行）
- 只包含编码任务，排除部署、环境搭建等

---

## 功能需求 F-5: 审计评分量化

**用户故事**: 作为完成 spec 的使用者，我希望有一个快速的质量评分，以便一眼判断"这份东西靠谱吗"而无需逐条阅读审计清单

**验收标准**:

- AC-F5-1: 当 spec-audit-surface 或 integrated-validator 完成审计时，输出应包含「质量评分」区段，覆盖 4 个维度：完整性、清晰度、可行性、一致性，各 25 分
- AC-F5-2: 评分输出应使用固定表格格式：维度 | 得分 | 关键发现，底部显示综合分 + 最低维度高亮
- AC-F5-3: 综合分使用算术平均，同时高亮最低维度作为风险信号（如 `综合: 82/100 🟡 ⚠️ 最低维度: 可行性 75`）
- AC-F5-4: 评分结果应写入 spec 上下文（如 `context/audit_score.md`），按阶段覆盖最新结果

**边界情况**:
- 评分是参考信号（🟢≥85 / 🟡70-84 / 🔴<70），不是硬门禁——硬门禁是 F-1 的人工审批
- 未生成结构化 AC 的简单任务不计算一致性维度，该维度标为 N/A

---

## 功能需求 F-6: 项目级 AI 引导增强

**用户故事**: 作为在新会话中启动 AI 的开发者，我希望 AI 能快速了解项目的产品逻辑、技术约定和代码结构，以便减少"AI 不知道已有知识"的问题

**验收标准**:

- AC-F6-1: `repository_map.md` 的每个仓库条目下应包含 AI 引导摘要，覆盖：产品上下文（核心功能、业务规则）、技术约定（框架、构建命令、编码规范）、代码结构（关键目录和职责）
- AC-F6-2: 当 maglev-bootstrapper 初始化或注册新仓库时，应通过扫描项目文件（README、package.json、目录结构等）自动生成摘要，用户确认后写入
- AC-F6-3: 当 maglev-map-maker 执行更新时，应检测摘要是否明显过期（如核心依赖版本变化、目录结构大幅变动），过期时提醒用户重新生成

**边界情况**:
- 每个仓库摘要控制在 20 行以内，防止 repository_map.md 膨胀
- 自动生成的摘要必须经用户确认才写入，不静默覆盖
- 摘要头部标注生成日期，reality-sync 可选检查过期

---

## 功能需求 F-7: 验证层前端/交互能力补齐

**用户故事**: 作为使用 Maglev 开发含 UI 项目的团队，我希望验证层能实质性地检验前端/交互产物的质量，而非仅做文件存在性检查，以便前后端产物获得同等质量保障

**验收标准**:

- AC-F7-1: 当 integrated-validator 执行 Layer 3（Spec ↔ Code Frontend）时，应检查：组件清单与实际组件文件的一致性、spec 中定义的 UI 状态在代码中是否有对应实现（如 loading/error/empty 状态处理）、组件 Props/Events 契约与实际实现是否匹配
- AC-F7-2: 当 spec-audit-surface 审计含交互需求的 spec 时，应检查：每个交互组件是否定义了完整的状态集（空/加载/成功/错误/骨架屏中至少覆盖 3 种）、I 系 AC 引用的 F 系 AC 是否存在、有多端适配需求时是否包含响应式策略
- AC-F7-3: 当 review-validation-surface 检查含前端代码的实现时，应纳入前端质量维度：组件状态管理模式、可访问性实现（ARIA 属性、键盘导航）、响应式断点覆盖
- AC-F7-4: 当 test-design-surface 设计含前端组件的测试策略时，应区分前端特有测试层：组件交互测试（Props/Events/Slots）、UI 状态转换测试、可访问性测试

**边界情况**:
- 纯后端项目不触发前端验证维度
- 前端验证的具体检查项应随交互模板的演进而更新（非一次性定义）

---

## 非功能需求

### NFR-1: 最小侵入性
改动应只修改必要的步骤文件和模板（step-04-handoff.md、wrapper-02-draft.md、step-04-verify-output.md、prd-output-contract.md、tech-spec-template.md 及验证层步骤文件），不改变主流程的阶段划分和 skill 之间的路由逻辑。

### NFR-2: 向后兼容
现有不使用结构化 AC 的工作流（简单任务、修复类）不应受影响。不生成结构化需求文档时，所有下游行为与当前一致。

### NFR-3: 纯 Markdown 输出
需求文档和设计文档的正式输出均为纯 Markdown 格式（人类可读优先），不使用 YAML/JSON 包裹内容。边界收敛摘要（prd_output_package）保持现有 YAML 格式不变。

### NFR-4: 渐进式采用
F-1~F-3 为 P0 优先实施。F-4（任务依赖图）和 F-5（审计评分）为 P1。F-6（AI 引导）为 P2。各功能独立可用，不强制一次性全部落地。
