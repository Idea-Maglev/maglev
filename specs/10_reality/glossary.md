# 项目术语表

> 跨功能的项目级术语定义。由各 spec 的术语表汇总而来。
> 新会话启动时被 reality-sync 加载，后续 requirement-convergence 可引用复用。

## 已确认术语

### 生命周期

| 术语 | 定义 | 来源 |
|------|------|------|
| 10_reality | 项目当前已成立的事实基线，是理解现状的唯一信源 | repository_map |
| 20_evolution | 仍在推进中的演进主题与待验证的设计 | repository_map |
| 90_archive | 历史依据与已结束主题的归档区，不作为当前现状入口 | crystallization |
| 结晶 (Crystallization) | 将已验证的变化写回 reality 并收口 active 的后段闭环动作 | crystallization |
| 写回 (Writeback) | 将已成立的项目变化正式记录到 10_reality 的动作 | crystallization |
| 收口 (Close) | 对 active 演进主题的状态确定：结束 / 继续 / 拆分 | crystallization |
| 归档反模式 | 错误做法：直接搬运 active→archive 而未将结论写入 reality | crystallization |

### 主流程

| 术语 | 定义 | 来源 |
|------|------|------|
| Main Flow（主流程） | 核心工作链：现状同步→需求收敛→方案设计→上下文实施→综合验证→现实结晶 | AGENTS.md |
| Skill（技能） | Maglev 的可执行能力对象，每个 Skill 负责特定工作阶段或任务 | .agents/skills/ |
| Reality Sync（现状同步） | 会话启动时建立项目真实状态认知，输出可操作的 Session Brief | reality-sync |
| Requirement Convergence（需求收敛） | 入口分流→需求定义→Ready Gate→交接，确保需求边界明确 | requirement-convergence |
| Spec Designer（方案设计） | 需求稳定后通过结构化流程形成可执行技术方案 | spec-designer |
| Context Implementer（上下文实施） | 方案清楚后完成受控编码、自检与对抗性审查 | context-implementer |
| Integrated Validator（综合验证） | 需求↔规格↔代码↔测试的多维度交叉验证 | integrated-validator |

### 质量机制

| 术语 | 定义 | 来源 |
|------|------|------|
| AC（验收标准） | Acceptance Criteria，验证需求是否满足的具体判定点 | main_flow_quality_gates |
| AC-F{N}-{M} | 功能需求 AC 编号：F=功能序号，M=AC 序号；Maglev 发明 | main_flow_quality_gates |
| AC-I{N}-{M} | 交互需求 AC 编号：I=交互需求序号，M=AC 序号；与 F 系并行 | spec_document_architecture |
| EARS 格式 | 结构化需求表达：当…时 / 若…则 / 在…期间 / 应 | main_flow_quality_gates |
| Ready Gate | 需求收敛阶段的 AI 自检关卡，5 个条件全部满足才可进入方案设计 | requirement-convergence |
| 质量门禁 (Quality Gate) | 工作流检查点：AI 自检层 + 用户审批层，强制阻塞不合格产物 | main_flow_quality_gates |
| 对抗性审查 | 上下文实施中从相反角度检查实现一致性的机制 | context-implementer |
| 需求覆盖表 | 设计文档中 AC→设计位置的映射表，确保无遗漏；Maglev 发明 | main_flow_quality_gates |

### 文档体系

| 术语 | 定义 | 来源 |
|------|------|------|
| 文档关系声明 | 每个 spec 文件头部的上游/下游/平行引用，用于互联验证 | spec_document_architecture |
| 交互需求文档 | 01_requirements_interaction.md，定义 UI 状态/操作响应/视觉约束/可访问性 | spec_document_architecture |
| 交互设计文档 | 02_design_interaction.md，含 stateDiagram、组件 API、响应式策略 | spec_document_architecture |
| 输出合约 (Output Contract) | Skill 间的交接协议，明确上游必须提供什么、下游期望什么 | requirement-convergence |

### 入口与治理

| 术语 | 定义 | 来源 |
|------|------|------|
| Entry-Router | 会话入口路由，负责请求识别和下游技能分流 | entry-router |
| Knowledge-Check | 知识沉淀检查，在会话切换或收尾时确认思考/方案是否已落盘 | knowledge-check |
| 可发现性 (Discoverability) | 新写回的 reality 能否被后续会话有效发现 | crystallization |
| _internal | 不独立暴露但被多个 skill 共享的内部模块目录 | repository_map |

## 待确认术语

> 以下术语由 AI 自动提取，等待用户确认后移入「已确认」区。

| 术语 | 定义 | 来源 |
|------|------|------|
