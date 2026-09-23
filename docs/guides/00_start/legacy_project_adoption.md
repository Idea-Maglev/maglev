# 遗留项目接入指南：渐进式对齐 (Legacy Project Adoption: Progressive Alignment)

> "不要为了追求方法的纯洁性，而牺牲了业务的连续性。"

Maglev 的 "Spec-First" 原则在全新项目 (Greenfield) 中是神圣的，但在遗留项目 (Brownfield) 中，我们必须承认：**代码是唯一的真理**。

本文档定义了如何在**文档缺失、甚至过时**的遗留项目中，平滑地引入 Maglev 体系。

## 1. 核心策略：反向对齐 (The Reverse Alignment)

对于老项目，我们不要求“先补全文档再干活”，而是采用 **"Code First Entry, Spec First Evolution" (代码切入，规格演进)** 的策略。

### 传统的 Maglev 流
`Idea -> Spec (Doc) -> Code`

### 遗留项目的适配流
1.  **Current State**: `Code (Source of Truth)`
2.  **Reverse Engineering**: `Code -> AI Analysis -> Snapshot Spec`
3.  **Future State**: `Snapshot Spec + New Requirement -> Updated Spec -> New Code`

---

## 2. 实施阶段 (Three Phases)

### Phase 1: 零文档接入 (Zero-Spec Entry)
*目标：先让 AI 帮上忙，建立信任，不增加负担。*

- **场景**: 修复 Bug，微小优化。
- **Action**:
    - 甚至不需要 `specs/` 目录。
    - 直接把相关代码文件喂给 AI (Context窗)。
    - Prompt: "你是一个高级工程师，阅读这段代码，修复 NPE bug，保持原有代码风格。"
- **Maglev 含量**: 10% (仅使用了 AI Coding 工具，未引入流程)。

### Phase 2: 局部逆向 (Partial Reverse Engineering)
*目标：在修改热点区域建立“根据地”。*

**推荐工具**: 使用 **`maglev-legacy-adopter`** 技能 (Skill)。

- **场景**: 针对某个核心模块 (e.g., `PaymentService`) 进行功能迭代。
- **Action**:
    - **Step 1 (Adoption)**: 运行 `/maglev-legacy-adopter`。
    - **Step 2 (MRI)**: 技能会自动诊断项目结构并初始化 `.maglev` 环境。
    - **Step 3 (Reverse)**: 技能会调用 `maglev-reverse-spec` 逆向您指定的模块。
    - **Step 4 (Admission)**: 逆向结果经共享 Reality Admission 准入，只有 `accepted` / `no_change` 才继续。
    - **Step 5 (Index)**: 技能会自动调用 `index-librarian` 登记资产。
- **Maglev 含量**: 60% (引入了 Spec asset，建立了局部闭环)。

### Phase 3: 增量覆盖 (Incremental Coverage)
*目标：随着迭代，逐步将 "Code Truth" 搬运回 "Spec Truth"。*

- **原则**: **不动不补**。只有当你要修改某个模块时，才去补全它的 Spec。
- **Action**:
    - 随着 Sprint 进行，你的 `specs/` 目录会自然生长，覆盖掉那些最活跃的业务域。
    - 那些躺在角落里的一万年不改的死代码 (Legacy Code)，就让它们安静地躺着，**不需要 Spec**。
- **Maglev 含量**: 100% (对于活跃代码部分)。

---

## 3. 工具技法 (Techniques)

### 3.1 AI 逆向 Prompt 模板
(如果您无法使用 Skill，可手动参考此模板)

```markdown
# Role
你是一位软件考古学家 (Software Archaeologist)。

# Task
分析提供的代码文件。
逆向还原业务逻辑，并根据标准设计模式进行校验。
输出一份 Markdown 格式的技术规格书 (Technical Specification)。

# Requirements
1. **Structure**: 必须包含严格的 YAML frontmatter、场景列表 (Scenario List) 和逻辑流程 (Logic Flow)。
2. **Precision**: 明确区分“显式逻辑”(代码实现的)和“隐含意图”(注释或命名暗示的)。
3. **Format**: 严格遵循当前仓库的 Maglev Spec 结构与模板约定，例如 `specs/templates/technical_design_template.md`。
```

### 3.2 "Spec-Less" Commit 豁免
在 VibeKanban 或 Husky 中，允许对 Legacy Path 配置豁免规则：
- 如果修改的是 `/legacy/*` 目录，不强制检查 Spec 关联。
- 如果修改的是 `/active/*` 目录，必须有 Spec。

---

## 4. 结论
Maglev 不是洁癖患者的圣经。
在遗留项目中，**代码优先 (Code First)** 是实事求是的态度。
通过 **`maglev-legacy-adopter`** 技能，我们可以极低成本地将“代码现状”还原为“规格文档”，从而实现从“野蛮生长”到“规格驱动”的无痛切换。
