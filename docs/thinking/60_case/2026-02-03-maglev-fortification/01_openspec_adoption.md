# OpenSpec Adoption Plan (PRD Standard Upgrade)

## 1. 核心目标 (Goal)
将 PRD 生成标准从通用的 "User Story" 升级为更严谨的 **"OpenSpec Standard"** (based on `spec.md`)，同时保持 **Three-Zone Architecture** 分层结构。

## 2. 标准定义 (OpenSpec Standard)

### Structure
*   **Requirement**: 声明系统必须满足的能力 (SHALL statements).
*   **Scenario**: 具体的使用场景描述.
*   **Steps (Gherkin)**:
    *   **GIVEN**: 前置条件
    *   **WHEN**: 触发动作
    *   **THEN**: 预期结果
    *   **AND**:补充条件/结果

### Integration with Zone Architecture
*   **Zone 1**: Decision Brief (不变).
*   **Zone 2 (Logic Core)**: *Replace standard User Stories with OpenSpec format.*
*   **Zone 3**: Context Trace (不变).

## 3. 实施步骤 (Execution)

### A. Create Template
创建 `solutions/starter-kit/.agents/skills/maglev-create-prd/references/templates/zone-template-prd-openspec.md`。

```markdown
# {Product Name} PRD

> 👤 **Executive Brief (决策摘要)**
> ...

## Requirements (Zone 2)

### Requirement: {Title}
The system SHALL {behavior}.

#### Scenario: {Scenario Title}
- **GIVEN** {Context}
- **WHEN** {Action}
- **THEN** {Result}
- **AND** {Additional Result}
```

### B. Update Skill Step
修改 `step-c-04-journeys.md`:
1.  引用新模板。
2.  更新 Prompt 指令，强制要求使用 OpenSpec 格式生成需求。

## 4. 预期收益
*   更高精度的需求描述。
*   天然支持 BDD 测试用例生成。
*   消除自然语言 User Story 的歧义。
