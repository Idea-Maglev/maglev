# Maglev Workflow Exposure Plan (技能显性化计划)

## 核心理由 (Rationale)
您的提议非常合理。当前 Maglev 拥有 27 个技能，但仅暴露了 3 个 Workflow (`generate-commit-message`, `maglev-init`, `maglev-librarian`)。
**痛点**: 用户必须记得技能名称才能在对话中调用，或者翻阅文档。
**解决**: 利用 IDE 的 `/` 指令补全特性，将常用技能封装为 Workflow，实现 "触手可及"。

## 筛选标准 (Filter Criteria)
并非所有 Skill 都需要 Workflow。我们将排除 **原子能力 (Atomic Skills)**，只暴露 **面向用户的前台技能 (User-Facing Skills)**。

### ✅ 纳入清单 (To Be Generated)

| Category | Skill Name | Workflow Name | Description |
| :--- | :--- | :--- | :--- |
| **Creation** | `maglev-create-prd` | `/create-prd` | 启动 PRD 生成向导 |
| | `maglev-quick-spec` | `/create-spec` | 启动技术方案生成 (Deep Mode) |
| | `maglev-quick-dev` | `/quick-dev` | 快速开发功能 |
| | `maglev-create-test-cases` | `/create-tests` | 生成测试用例 |
| **Discovery** | `maglev-design-ux` | `/design-ux` | 启动 UX 设计师访谈 |
| | `maglev-research` | `/research` | 启动深度调研 |
| **Governance** | `maglev-audit-prd` | `/audit-prd` | 审计当前 PRD |
| | `maglev-audit-spec` | `/audit-spec` | 审计当前 Spec |
| | `maglev-cross-validate` | `/validate-all` | 全域交叉验证 |
| **Utility** | `maglev-map-maker` | `/map` | 生成/更新 Atlas 地图 |
| | `maglev-standup` | `/standup` | 每日站会 |
| | `maglev-tutor` | `/tutor` | 启动教程模式 |
| | `maglev-skill-forge` | `/new-skill` | 创建新技能 |

### ❌ 排除清单 (Excluded / Internal)
*   `atomizer` (由其它技能调用)
*   `maglev_spec_ingest/draft/crystallize/context` (Spec 流水线内部环节)
*   `mermaid_expert` (工具型，通常作为子步骤)
*   `maglev-plan-unit-tests-*` (通常包含在 `quick-dev` 或 `create-tests` 中，除非用户强烈要求独立)

## 实施方案 (Implementation)
1.  **Batch Create**: 为上述 "纳入清单" 中的每个技能创建一个对应的 `.agents/workflows/{name}.md`。
2.  **Template**:
    ```markdown
    ---
    description: [Description]
    ---
    # [Workflow Name]
    
    1. 呼叫技能:
       > "请启动 `{Skill-Name}` 技能。"
    ```
3.  **Update Manifest**: 更新 `solutions/starter-kit/README.md` 的交互指南。

## 待确认项
是否同意上述筛选标准？特别是 `maglev-plan-unit-tests-*` 是否需要独立暴露？
