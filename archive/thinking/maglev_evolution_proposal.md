# Maglev Methodology Evolution Proposal (v2.0 Candidate)

> **Source Project**: MindBase (Brownfield Transformation)
> **Practitioner**: Feiyu Gao & AI Architect
> **Objective**: 将 MindBase 实战中涌现的"最佳实践"提炼为通用方法论，反哺 Maglev Core。

## 1. 核心范式转移 (Paradigm Shifts)

| 维度 | Maglev v1.0 (Theory) | Maglev v2.0 (Practice) | 动因 |
| :--- | :--- | :--- | :--- |
| **规则形态** | 静态文档 (`docs/rules/*.md`) | **动态上下文 (`core_rules.md`)** | 静态文档没人看，必须注入到 IDE/AI 的上下文中才能生效。 |
| **同步方向** | 严格正向 (Spec -> Code) | **双向闭环 (Bi-Directional)** | 承认"探索性编程"的合法性，利用 AI 能力低成本完成逆向同步。 |
| **治理手段** | 人工流程 (Checklist) | **工具链强制 (Workflow/Script)** | 人性不可靠，"Run Script" 比 "Follow Doc" 更容易执行。 |
| **异常处理** | 未定义 (Default to Failure) | **降级与治愈 (Debit & Heal)** | 缺乏降级通道会导致规则被彻底抛弃；需建立合法的"举债"机制。 |

## 2. 具体新增模块 (Proposed Modules)

建议将以下 MindBase 产物标准化并纳入 `maglev` 仓库：

### 2.1 Maglev Acceleration Pack (加速包)
> **定位**: "开箱即用"的 AI 配置文件，让新项目 5 分钟内具备 Maglev 能力。

*   **Artifact**: `.maglev/rules/core_rules.md`
    *   *Standard*: 定义了 Map-First, Truth-First, Evidence-Based 三大铁律。
    *   *Innovation*: 强制中文环境，强制日志更新。
*   **Artifact**: `.agents/workflows/maglev-init.md`
    *   *Innovation*: 标准化的上下文加载仪式。

### 2.2 The "Debt Protocol" (债务协议)
> **定位**: 处理"理想与现实差距"的标准操作程序 (SOP)。

*   **Artifact**: `.maglev/protocols/commit_standard.md`
    *   *Standard*: 定义了 "Sync Status" (Synced / Debt)。
    *   *Innovation*: **Fallback Mode**。允许 `[Debt]` 提交，但要求后续通过 `maglev_audit` 治愈。
*   **Tool**: `.maglev/scripts/generate_commit_msg.py`
    *   *Innovation*: 智能推断测试文件，降低填写阻力；自动识别 UI 变更要求截图。

### 2.3 AI-Native Toolchain (原生工具链)
> **定位**: 只有 AI 能执行的高级技能。

*   **Skill**: `maglev_audit`
    *   *Capability*: 自动阅读 Spec，自动 Grep 代码，自动生成 Gap Report。
*   **Skill**: `maglev_reverse_eng`
    *   *Capability*: "Spec 回填"的核心引擎。

## 3. 移除/废弃建议 (Deprecations)

*   **废弃**: 纯人工维护的 `ChangeLog.md`。
    *   *替代*: 基于 `dev_log.md` (里程碑) 和 `git log` (原子提交) 的组合。
*   **降级**: 过于复杂的 UML 图。
    *   *替代*: Mermaid (Code-friendly) + 自然语言描述。AI 读 Mermaid 比读图片准得多。

## 4. 实施路线图 (Rollout Plan)

1.  **Extract**: 从 MindBase 仓库中提取上述通用脚本和文档。
2.  **Template**: 将其去敏化，制作成 `maglev-starter-kit`。
3.  **Upgrade**: 更新 `maglev` 主仓库的 README，从"文档库"转型为"工具库"。
