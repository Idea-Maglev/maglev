# Kiro for Claude Code 深度分析 — Maglev 可借鉴模式

> 日期：2026-04-13
> 来源：https://github.com/notdp/kiro-for-cc
> 目的：识别 Maglev spec 流程和 agent 管理中可借鉴的模式

---

## 1. Kiro 核心架构

Kiro 是 Claude Code 的 spec-driven 开发扩展，核心流程：

```
Requirements (EARS 格式) → [用户明确批准] → Design (Mermaid 架构图) → [用户明确批准] → Tasks (依赖图+清单) → [用户明确批准] → Implementation
```

6 个 Agent：spec-requirements / spec-design / spec-tasks / spec-judge / spec-impl / spec-test  
3 个 Steering 文档：product.md / tech.md / structure.md

---

## 2. 逐模式深度对比

### 模式 A：强制审批门禁

#### Kiro 实现细节

Kiro 的 `spec-workflow-starter.md` 用状态机严格定义门禁：

```
Requirements --> ReviewReq : Complete Requirements
ReviewReq --> Requirements : Feedback/Changes Requested
ReviewReq --> Design : Explicit Approval   ← 必须 explicit
```

核心原则明确写在 workflow 定义里：
> "A core principal is that we rely on the user establishing ground-truths as we progress through. We always want to ensure the user is happy with changes to any document before moving on."

Agent 端也有硬约束（spec-requirements.md）：
> "The model MUST ask for explicit approval after iterations"
> "The model MUST continue revision cycle until approval"

#### Maglev 当前实现

| 检查点 | Maglev 怎么做 | 实际效果 |
|--------|--------------|---------|
| 需求→设计 | `step-03-ready-gate.md` 检查 5 个条件（核心对象明确、InScope/OutScope 可区分…） | **AI 自判**，输出 `gate_result: ready/not_ready`，不等用户批准 |
| 设计→实施 | `wrapper-02-draft.md` 有 Human-in-the-Loop 询问（"直接因化/手动修改/重新生成"） | **有询问但选项是操作选择**，不是"设计是否正确" |
| 实施后 | `step-04-verify-output.md` 检查文件完整性（00_index.md 到 03_plan.md） | **结构检查**，不是内容批准 |

#### 差异判断

**Maglev 的 Ready Gate 是"AI 自检是否 ready"，Kiro 是"用户确认内容是否 correct"。这是本质区别。**

Ready Gate 的 5 个条件（核心对象明确、InScope 可区分、成功信号清楚等）都是 AI 可以自说自话的——AI 完全可能判断"核心对象明确"但实际上理解有偏差。Kiro 不给 AI 这个权限：不管 AI 认为多完美，都必须等用户说"approved"。

`wrapper-02-draft.md` 确实有 Human-in-the-Loop，但询问的是"你想直接拆分还是手动修改还是重新生成"——这是**操作方式选择**，不是**内容批准**。用户可能选了"直接因化"但其实没仔细看。

#### 改进路径

在 `requirement-convergence` 的 step-04-handoff 和 `spec-designer` 的 wrapper-02-draft 增加一个硬约束：

```
在交接前，必须向用户展示核心产物摘要，并获得 explicit approval。
gate_result 只决定"是否结构上可以交接"，
用户确认决定"是否内容上允许交接"。
```

预期效果：
- 减少"AI 自信地跳过有问题的需求"（对应 P0 需求遗漏 24%）
- 减少"PRD 变更点被 AI 静默跳过"（对应 P0 PRD→Spec 断裂）

但注意：**不能每个子步骤都加门禁**。Maglev 是方法论框架，不是 IDE 插件，过度审批会让流程退化为"AI 的事事请示模式"。建议**只在阶段交接点**加：需求→设计、设计→实施。

---

### 模式 B：EARS 结构化需求格式

#### Kiro 实现细节

spec-requirements agent 的核心规则：

```markdown
### Requirement N
**User Story:** As a [role], I want [feature], so that [benefit]

#### Acceptance Criteria
1. WHEN [触发条件] THEN [系统] SHALL [响应]
2. IF [前置条件] THEN [系统] SHALL [响应]
3. WHILE [持续状态] THEN [系统] SHALL [响应]
```

关键约束：
- **先生成初版，不问问题**（"MUST generate initial version WITHOUT asking sequential questions first"）
- EARS 关键词保留英文，其余内容跟随用户语言偏好
- 每条需求必须有 User Story + EARS 格式验收标准

#### Maglev 当前实现

`requirement-convergence` 的 step-02-define-requirements 输出格式：

```yaml
core_object: string
in_scope: [string]
out_of_scope: [string]
success_signal: [string]
key_unknowns: [string]
```

`prd-output-contract.md` 的扩展字段也是自由文本：

```yaml
prd_output_package:
  core_object: string
  target_user: string
  in_scope: [string]  # 自由文本列表
  success_signal: [string]  # 自由文本列表
```

#### 差异判断

**Maglev 的需求产物是"边界描述"（什么做、什么不做），Kiro 的需求产物是"行为规格"（什么条件下系统必须怎么做）。**

两者解决的问题不同：
- Maglev 的 requirement-convergence 解决的是"范围漂移"——先固定边界再设计
- Kiro 的 spec-requirements 解决的是"需求模糊"——把模糊想法变成可测试的规格

这意味着：Maglev 收敛了边界但**没有收敛行为**。边界清楚了（做 A 不做 B），但 A 的具体行为还是模糊的（"支持 X 功能"但没说在什么条件下如何响应）。

#### 改进路径

不替换当前的 requirement-convergence 输出格式（边界收敛仍然有价值），而是在 **prd-output-contract.md** 或者 **spec-designer 的输入端**增加"行为级需求"模板：

```markdown
### 功能需求 F-{N}: {名称}

**用户故事**: 作为 [角色]，我希望 [功能]，以便 [价值]

**验收标准**:
1. 当 [触发条件] 时，系统应 [响应行为]
2. 若 [前置条件]，则系统应 [响应行为]
3. 在 [持续状态] 期间，系统应 [响应行为]

**边界情况**: [如果有]
```

不照搬 EARS（WHEN/SHALL 偏嵌入式工程），但借鉴其核心思想：**每条需求必须有触发条件和预期行为，而不仅仅是功能描述**。

预期效果：
- 直接可生成测试用例（对应 P0 需求遗漏 24%——遗漏的根因是需求没有达到可测试精度）
- 设计阶段不再需要"推测"需求具体行为

#### Maglev 能做得更好的地方

Kiro 的 EARS 是**纯格式约束**，不关心需求的上下游一致性。Maglev 可以把行为级需求和 `integrated-validator` 的交叉验证打通：

- 每条验收标准自带 ID（AC-F1-1、AC-F1-2）
- `spec-audit-surface` 检查 AC 是否都有对应设计
- `test-design-surface` 检查 AC 是否都有对应测试用例
- `review-validation-surface` 检查实现是否覆盖所有 AC

这是 Kiro 做不到的（它没有独立质量层）。**结构化需求 + 质量层交叉验证 = 从源头到测试的全链路可追溯**。

---

### 模式 C：并行 Agent + Judge 评审

#### Kiro 实现细节

树形评审算法：
```
N 个 Agent 并行生成 → ceil(N/4) 个 Judge 评审 → 逐层淘汰 → 最终 1 份
```

评分维度：完整性(25) + 清晰度(25) + 可行性(25) + 创新性(25)

Judge 可以"选最佳"或"综合 N 个版本优点创建新版本"。

#### Maglev 当前实现

所有 skill 单线程执行。方案设计只产出一个版本。
`spec-audit-surface` 是事后审计，不是生成阶段的质量竞争。

#### 差异判断

**并行生成在 Maglev 的场景里价值有限。**

原因：
1. Maglev 的 spec-designer 需要大量项目上下文和对话输入（Socratic Interview），不是一句 feature description 就能产出方案
2. 并行 N 个 Agent 意味着每个 Agent 都要独立收集上下文、独立提问——用户体验极差（要回答 N 遍同样的问题）
3. Kiro 能并行是因为输入高度结构化（feature_name + feature_description + spec_base_path），Maglev 的输入是非结构化的人机对话

#### 实际可借鉴的点

不借鉴"并行生成"，但借鉴 **Judge 评分维度**：

当前 `spec-audit-surface` 做一致性审计但不评分。可以在审计报告中增加量化评分：
- 完整性：需求是否全覆盖
- 清晰度：设计是否可直接消费
- 可行性：技术选型是否匹配当前栈
- 一致性（替代"创新性"）：需求↔设计↔测试是否对齐

这不需要并行 Agent，只需要给 `spec-audit-surface` 加评分输出。

---

### 模式 D：任务依赖图 + 自动编排

#### Kiro 实现细节

spec-tasks agent 必须生成：
1. checkbox 任务清单（最多 2 层层级）
2. Mermaid 依赖图（哪些任务可以并行）

每个任务必须：
- 引用具体需求编号（如 "Requirements: 1.2, 3.3"）
- 只包含编码任务（排除部署、测试环境搭建等）
- 子任务用 decimal notation（1.1, 1.2, 2.1）

```markdown
- [ ] 1. 设置项目结构
  - 创建目录结构
  - 定义接口
  - _Requirements: 1.1_
```

#### Maglev 当前实现

`spec-designer` 的产物是 `03_plan.md`（计划文档），格式没有强制约束。
`context-implementer` 读取 plan 但不解析依赖关系。
step-03-execute.md 明确说"按顺序执行所有任务"。

#### 差异判断

**缺少依赖图导致两个问题：**

1. 实施顺序完全靠 AI 推测——可能先实现了依赖后置的组件
2. 无法判断哪些任务可以并行或独立执行——所有任务只能串行

**但 Maglev 的 03_plan.md 比 Kiro 的 tasks.md 承载了更多信息。**

Maglev 的计划文档不仅是任务清单，还包含设计决策、约束说明、技术选型理由等。Kiro 的 tasks.md 是纯执行清单，设计信息在 design.md 里。

#### 改进路径

不改变 03_plan.md 的丰富性，但要求它在任务列表部分增加：
1. 每个任务引用对应的需求/设计条目
2. 用 Mermaid 图表达任务依赖关系
3. 标记可并行执行的任务组

在 `context-implementer` 的 step-03-execute.md 中增加：
- 读取依赖图决定执行顺序（如果存在）
- 对于无依赖的任务，考虑批量执行

#### Maglev 能做得更好的地方

Kiro 的任务只有 task→requirement 的单向引用。Maglev 可以实现 **requirements ↔ task ↔ test 三向追溯**：
- 每个任务引用需求 AC 编号
- 每个任务完成后自动关联到哪些测试用例覆盖了它
- `integrated-validator` 可以检查"是否每个 AC 都有对应任务且该任务有测试覆盖"

---

### 模式 E：Steering 三文档

#### Kiro 实现细节

初始化时分析代码库，自动生成：
- `product.md` — 产品规则、功能边界、业务逻辑
- `tech.md` — 技术栈、构建命令、约定
- `structure.md` — 目录结构、命名模式、架构

每次 AI 对话自动注入这些文档。

#### Maglev 当前实现

- `AGENTS.md` — Maglev 框架操作指引（非项目专属）
- `llms.txt` — 同上
- `maglev-bootstrapper` 生成 `repository_map.md`（仓库列表 + 路径）
- 没有项目级的产品规则、技术标准、代码结构文档

#### 差异判断

**Maglev 的 AI 上下文是"框架级"的（如何操作 Maglev），Kiro 的是"项目级"的（项目本身是什么）。**

这直接关联 P0 问题"知识可发现性不足"——赵轩反馈"AI 不知道我已梳理的知识"。原因就是 Maglev bootstrapper 只注册了仓库路径，没有让 AI 理解项目的产品逻辑、技术约定和代码结构。

#### 改进路径

在 `maglev-bootstrapper` 或 `maglev-legacy-adopter` 的 Phase 3（配置）之后增加 Phase 3.5：

1. 扫描代码目录，自动生成 `.maglev/steering/` 下的三个文档
2. 或者更轻量：在 `AGENTS.md` 的项目专属部分增加结构化模板

不建议完全照搬 product/tech/structure 三文档分离——Maglev 已经有 `10_reality` 体系承载项目现状。更好的方式是在 `repository_map.md` 的基础上，为每个注册仓库增加技术摘要、产品摘要和结构摘要。

#### 注意：这可能是 Maglev 的负担点

如果 steering 文档需要手动维护，就变成了用户的额外负担。Kiro 的优势是它作为 IDE 扩展可以在后台自动分析代码库并更新 steering 文档。Maglev 作为方法论框架没有"后台运行"的能力——steering 文档一旦创建，就需要人维护。

解法：
- 把 steering 信息生成和更新作为 `reality-sync` 的可选步骤
- 或者把它作为 `maglev-map-maker` 的增强输出

---

## 3. Maglev 反而是负担的风险

### 风险 1：门禁过多导致流程阻塞

如果在 5 个模式全部落地：结构化需求 + 审批门禁 + 评分 + 依赖图 + steering 文档——一个中等功能的 spec 流程将从当前的 ~3 步变成 ~8 步。每多一个步骤，用户"嫌麻烦直接跳过 Maglev"的概率就增大。

**缓解：明确区分"必须做"和"可以做"。只有审批门禁和结构化需求是硬性改进，其余作为可选增强。**

### 风险 2：结构化需求增加前段耗时

EARS 格式要求每条需求都有触发条件+预期行为+验收标准。对于快速原型或探索性任务，这是过度工程化。

**缓解：设置"轻量模式"开关。context-implementer 的 mode detection 已经有类似机制（简单任务跳过 tech-spec）。同理，requirement-convergence 也应该区分"需要 EARS 级别"和"边界收敛就够"。**

### 风险 3：Steering 文档变成又一个需要维护的东西

Maglev 已经有 10_reality、AGENTS.md、llms.txt、repository_map.md。再加 3 个 steering 文档就有 7 个"描述项目是什么"的文件。

**缓解：不新增文件，而是增强现有文件。在 repository_map.md 里为每个仓库增加 tech/product/structure 三段摘要。**

---

## 4. 结论：什么值得做，什么是过度

| 模式 | 值得做？ | 理由 | Maglev 结合后能做更好？ |
|------|---------|------|----------------------|
| A: 审批门禁 | ✅ 必须做 | AI 自判不可靠，P0 的直接解 | 是。Maglev 的 Ready Gate + 用户确认 = AI自检 + 人工兜底的双层保障 |
| B: 结构化需求 | ✅ 必须做 | 需求遗漏根因，可测试是关键 | 是。结构化需求 + 质量层交叉验证 = 全链路追溯（Kiro 做不到） |
| C: Judge 评分 | ⚠️ 有限借鉴 | 并行生成不适合，评分维度可借鉴 | 增强 spec-audit-surface 的输出格式即可 |
| D: 任务依赖图 | ✅ 值得做 | 降低实施阶段顺序出错风险 | 是。依赖图 + 三向追溯（req↔task↔test） |
| E: Steering 文档 | ⚠️ 慎做 | 有价值但有维护负担风险 | 增强 repository_map.md 而非新增文件 |

---

## 5. 推荐行动路径

### 第一批（低成本高回报）
1. **结构化需求模板** — 改 `prd-output-contract.md`，增加行为级需求格式
2. **审批门禁** — 在 `step-04-handoff.md` 和 `wrapper-02-draft.md` 增加 explicit approval 硬约束

### 第二批（中等投入）
3. **任务依赖图** — 在 `spec-designer` 的 plan 模板中增加 Mermaid 依赖图要求
4. **审计评分** — 在 `spec-audit-surface` 增加量化评分输出

### 第三批（需要验证）
5. **Steering 增强** — 在 `repository_map.md` 增加项目级 AI 引导摘要

---

## 6. 来源归属纪律

在实施过程中确立的来源归属规则，避免错误标注知识产权：

| 元素 | 归属 | 说明 |
|------|------|------|
| kiro-for-cc 仓库 | 近似来源（approximate source） | 非 Kiro 官方实现，是社区适配 |
| EARS 格式 | 行业通用 | Alistair Mavin 提出的需求工程方法 |
| EARS 中文关键词（当/若/应） | 用户决策 | 中文化选词由用户确定 |
| AC-F{N}-{M} 编号体系 | Maglev 发明 | Kiro 无此编号机制 |
| I 系 AC（AC-I{N}-{M}） | Maglev 设计 | 与 F 系并行，Kiro 无交互需求概念 |
| 需求覆盖表 | Maglev 发明 | Kiro 设计文档无此结构 |
| 设计决策表 | Maglev 发明 | Kiro 无显式设计决策记录 |
| 4 维度交互 AC | 综合行业通用 UI 需求维度 | Kiro 无交互/前端相关内容 |
| 文档关系声明 | Maglev 设计 | Kiro 文件间无显式关系声明 |

