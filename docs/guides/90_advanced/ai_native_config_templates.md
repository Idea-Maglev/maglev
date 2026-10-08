# AI Native 配置模板 (Configuration Templates)

本文档提供了 Maglev 体系所需的“治理即代码”核心配置模板。
这些文件应存放于 `.maglev/config/` 目录下。

## 1. 角色定义 (roles.yaml)
定义了每个角色的“应然”状态（标准能力模型）。

```yaml
# .maglev/config/roles.yaml
roles:
  value_owner:
    description: "产品的价值定义者与验收者"
    required_skills:
      structural_expression: 4  # 结构化表达能力 (L1-L5)
      market_insight: 3
    responsibilities:
      - "Define intent via Markdown specs"
      - "Acceptance testing"
    forbidden:
      - "Directly modifying production code"

  tech_pilot:
    description: "AI 结对编程的领航员与架构守护者"
    required_skills:
      code_review: 5            # 必须具备极强的 Review 能力
      system_design: 4
      prompt_engineering: 4
    responsibilities:
      - "Prompting AI for implementation"
      - "Code integration & debugging"
      - "Architecture review"
```

## 2. 团队映射 (team.yaml)
定义了团队成员的“实然”状态（实际能力雷达），用于计算 Capability Gap。

```yaml
# .maglev/config/team.yaml
members:
  - handle: "@example-user"
    role: "tech_pilot"
    skills:
      code_review: 5
      system_design: 5
      prompt_engineering: 4
    # No Gap, standard implementation mode

  - handle: "@junior.dev"
    role: "tech_pilot"
    skills:
      code_review: 2    # Gap: Level 2 vs Required Level 5
    # Action: Trigger "Strict Review Mode" or "Auto-Review Agent"
```

## 3. 通用行为准则 (core_rules.md)
跨工具通用的自然语言准则。

```markdown
# Core Behavior Rules

## 1. Collaboration Protocol
- **Always** iterate in the "Ring Iteration" loop: Intent -> Build -> Check.
- **Never** commit code without a corresponding Issue or Spec update.

## 2. Coding Standards
- Prefer **Functional Programming** style where applicable.
- All public functions must have Python type hints.
- Use **TDD**: Write tests before implementation.

## 3. AI Interaction
- If the user provides a vague intent, **ask for clarification** instead of guessing.
- When `user.skill_level < role.required_level`, explain the code logic in detail.
```

## 4. 工具适配器配置 (Tool Adapters)

### 4.1 Cursor (.cursorrules)
简单版：直接引用 Core Rules。

```markdown
# .cursorrules

You are an AI assistant following the Maglev methodology.

<CORE_RULES>
{Include content from .maglev/config/rules/core_rules.md}
</CORE_RULES>

<ROLE_CONTEXT>
Current User: @junior.dev
Role: Tech Pilot
Skill Gap Detected: Code Review (L2 < L5).
STRATEGY: You must act as a Senior Architect. Explain every critical change you make. Verification is mandatory.
</ROLE_CONTEXT>
```

### 4.2 Antigravity (System Prompt)
在 System Prompt 中动态注入：

```text
[System]
You are operating within the Maglev framework.
Refer to `.maglev/config/rules/core_rules.md` for operational guidelines.
Check `.maglev/config/team.yaml` to adapt your communication style to the current user's skill level.
```
