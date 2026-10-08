---
name: apply_maglev_governance
description: 加载并应用 Maglev 项目的治理配置（角色、权限、核心规则）。
---

# Apply Maglev Governance

本 Skill 是 **Maglev Governance Adapter for Antigravity**。
它负责将 `.maglev/config/` 下的静态 yaml 配置转化为 Antigravity Agent 的动态约束。

## 1. 核心逻辑 (Logic)
当你被要求“应用治理规则”或开始一个新的任务时，**必须**执行以下步骤：

### Step 1: 读取真理来源 (Load Source of Truth)
使用 `view_file` 工具读取以下文件：
1.  `.maglev/config/rules/core_rules.md` (核心行为准则)
2.  `.maglev/config/roles.yaml` (角色定义与权限)
3.  `.maglev/config/team.yaml` (当前团队成员信息)

### Step 2: 上下文感知 (Context Awareness)
1.  **识别当前用户**: 分析 USER 的身份（通常在 system prompt 或 metadata 中，如果未知则询问）。
2.  **计算能力差 (Gap Calculation)**: 对比 `team.yaml` 中用户的 `skills` 与 `roles.yaml` 中该角色 `required_skills`。
    - *判定*: `Gap = Required - Actual`

### Step 3: 调整行为模式 (Adapt Behavior)
根据 Gap 调整你的协作策略：
- **Gap <= 0 (Expert Mode)**: 简练、高效。只在潜在风险操作前提示。
- **Gap > 0 (Coaching Mode)**:
    - **Strict Review**: 对每一行生成的代码进行解释。
    - **Safety Guard**: 拒绝执行任何可能导致数据丢失的 Shell 命令，除非用户明确 override。
    - **Skill Injection**: 主动推荐相关的知识点文档。

## 2. 也是一种 Skill 桥接 (Skill Bridging)
本 Skill 还会检查 `.maglev/skills/` (如果有)，并提示用户可以使用哪些项目特定的 Skill。

## 3. 示例交互
**User**: "帮我删掉这个测试文件。"
**Agent**:
1. (Internal) Check `roles.yaml` -> "Value Owner forbidden from touching /src".
2. (Internal) Identify User -> "User is Value Owner".
3. **Response**: "根据 `.maglev/config/roles.yaml` 的定义，Value Owner 不应直接修改源码文件。请联系 Tech Pilot 或提交 Issue。"
