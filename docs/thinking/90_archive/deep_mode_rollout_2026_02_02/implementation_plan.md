# Deep Mode 技能深化推广计划

## 目标描述 (Goal)
将 Maglev 的核心生成类技能从 **Task Executor (任务执行者)** 升级为 **Thinking Partner (思考伙伴)**。
引入 **"Deep Mode" (深度模式)**，即通过 **Facilitator (引导者)** 角色和 **Socratic Questioning (苏格拉底式发问)** 机制，在产出结果前先与用户达成深度共识。

---

## 技能审计结果 (Skill Audit)

### 需要 Deep Mode 的技能 (Candidates)
> [!IMPORTANT]
> 这些是 **"生成类"** 技能，输出高度依赖于对意图的深度理解。

| Skill | 当前角色 | 现有深度机制 | 升级优先级 | 升级原因 |
|-------|---------|-------------|-----------|---------|
| `quick-spec` | Coordinator | ❌ 无 | **P0** | 核心生成技能，最常用 |
| `design-ux` | UX Designer | ⚠️ 浅 (Empathy 步骤) | **P1** | 需要更深的用户画像访谈 |
| `research` | Researcher | ❌ 无 | **P1** | 需要假设挑战机制 |

### 已有深度机制的技能 (Already Deep)
> [!NOTE]
> 这些技能已经内置了引导或挑战机制，无需改造。

| Skill | 已有机制 | 说明 |
|-------|---------|------|
| `create-prd` | ✅ `advanced-elicitation.workflow.xml` | 已有 12 步引导流程 |
| `create-test-cases` | ✅ `QA Strategist` + `Guided Mode` | 已有 Persona CoT |
| `reverse-spec` | ✅ `Guided Mode` + `CHECKPOINT` | 已有 5 步暂停确认 |

### 不需要 Deep Mode 的技能 (Not Applicable)
> [!TIP]
> 这些是 **"审计类"** 或 **"自动化类"** 技能，输入明确，无需意图澄清。

| Skill | 类型 | 为什么不需要 |
|-------|------|-------------|
| `audit-prd` | 审计 | 输入是既定 PRD，任务是检查，不生成 |
| `audit-spec` | 审计 | 同上 |
| `cross-validate` | 验证 | 自动对比，无生成 |
| `code-review-*` | 审计 | 对比 Spec vs Code |
| `librarian` | 索引 | 纯自动化任务 |
| `map-maker` | 索引 | 纯自动化任务 |
| `skill-forge` | 脚手架 | 已有 Architect 角色引导 |
| `spec-ingest/draft/crystallize` | 原子 | 被 `quick-spec` 编排，不直接面向用户 |
| `validate-spec-context` | 验证 | 纯检查 |
| `legacy-adopter` | 编排 | 不生成内容，只调度其他技能 |
| `bootstrapper` | 初始化 | 无需意图理解 |
| `quick-dev` | 执行 | 小改动快速通道，无需深度 |

---

## 分阶段推广策略 (Phased Rollout)

### Phase 0: 模式定义 (Deep Mode Template)
> [!IMPORTANT]
> 在升级任何 Skill 之前，先定义 "Deep Mode" 的通用模板 (Reusable Pattern)。

**产出**: `references/deep-mode-interview.template.md` (放在 `maglev-skill-forge` 模板库中)

**模板核心内容**:
1. **Role Shift**: 从 Executor → Facilitator
2. **Phase 0: Clarification Interview**: 强制性的意图澄清阶段
3. **Proactive Challenge**: 主动挑战假设的标准问题库

---

### Phase 1: 先锋技能 - `maglev-quick-spec` (P0)
> [!NOTE]
> 选择此技能作为先锋，因为它是最常用的生成技能，且已有 `advanced-elicitation.workflow.xml`。

**变更范围**:
| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | MODIFY | Role: Coordinator → **Product Architect** |
| `coordinator.workflow.md` | MODIFY | 在 Phase 1 前插入 Phase 0 |
| `references/step-00-socratic-interview.md` | NEW | 苏格拉底式访谈脚本 |

**访谈核心问题**:
1. "Why this feature?" (价值根因)
2. "What if it fails?" (边界条件)
3. "How do we know it's done?" (成功标准)

---

### Phase 2: 体验层 - `maglev-design-ux` (P1)

**变更范围**:
| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | MODIFY | Role: UX Designer → **Empathetic Design Partner** |
| `step-01-empathy.md` | MODIFY | 增加深度用户画像访谈 |

**访谈核心问题**:
1. "Who is the user, really?" (反对默认用户假设)
2. "What are they feeling before/during/after?" (情绪曲线)

---

### Phase 3: 洞察层 - `maglev-research` (P1)

**变更范围**:
| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | MODIFY | Role: Researcher → **Research Lead** |
| `step-01-scope.md` | MODIFY | 增加假设挑战环节 |

**访谈核心问题**:
1. "Is this the right question?" (问题重构)
2. "What if the opposite is true?" (反事实推理)

---

## 验证计划 (Verification Plan)

### Dry Run Tests
| Skill | 测试输入 | 预期行为 |
|-------|---------|---------|
| `quick-spec` | "做个类似 Tinder 的 App" | AI 应追问目标用户、核心差异化 |
| `design-ux` | "设计一个登录页" | AI 应追问用户是谁、情绪目标 |
| `research` | "AI 的未来" | AI 应追问具体研究问题、假设列表 |

---

## 时间估算 (Effort)

| Phase | 预计工作量 | 依赖 |
|-------|-----------|------|
| Phase 0 (Template) | 30 min | None |
| Phase 1 (quick-spec) | 1 hour | Phase 0 |
| Phase 2 (design-ux) | 45 min | Phase 0 |
| Phase 3 (research) | 45 min | Phase 0 |

