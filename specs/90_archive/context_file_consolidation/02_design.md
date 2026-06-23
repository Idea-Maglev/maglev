# Design: AI 上下文文件整合

## 变更总览

| # | 文件 | 变更类型 | 说明 |
|---|------|---------|------|
| A | `AGENTS.md` | 修改 | 新增工作原则章节（从 core_rules 提炼） |
| B | `llms.txt` | 修改 | 删除重复段、去除 core_rules 引用 |
| C | `.maglev/rules/core_rules.md` | 删除 | 标记 deprecated 后删除 |

## 变更 A: AGENTS.md（修改）

在 Git 工作流纪律章节后新增：

```markdown
## 工作原则

以下原则从项目实践中提炼，补充 skill 层未覆盖的全局行为期望：

- **可追溯性**：构建思维链时必须将"为什么"（docs/thinking/）与"是什么"（specs/）连接。严禁在不理解上下文的情况下只搬 Spec。
- **主动维护**：发现索引缺失、Issue 与 spec 不同步、或断链时，主动提议修复而非等待指令。
- **灵感留存**：在对话中识别有价值但不属于当前任务的观点时，主动提议记录到 `docs/thinking/`。
```

说明：
- 从 TRACEABILITY 提炼"可追溯性"，去除已由 skill 覆盖的审计细节
- 从 CUSTODIAN 提炼"主动维护"，去除不存在的 Dashboard 引用
- 从 CAPTURE 提炼"灵感留存"，去除不存在的 `{user}/` 路径

不搬运的内容及原因：
- EVIDENCE → reverse-spec/integrated-validator 已有更精确的证据要求
- LOGGING → docs/dev_log.md 不存在，contribution_log.md 由 knowledge-check 管理
- INDEXING → maglev-librarian 已覆盖
- USER_FOCUS → .maglev/user.yaml 不存在，无实现基础
- COLLAB → docs/thinking/ 无 [AGREED] 机制，规则无法执行

## 变更 B: llms.txt（修改）

### 删除段落

1. **§2 核心法则**（L53-61）→ 删除整段。Spec First 已在 00_vision.md，其余在 AGENTS.md
2. **§5 AI 上下文资产**（L84-97）→ 删除。AGENTS.md 已是 AI 上下文的权威来源
3. **§1.2 当前主流程运行名**（L22-36）→ 删除。与 AGENTS.md L85-90 重复
4. **L5 文档写作约束**（身份定义中）→ 删除。与 AGENTS.md L3-5 重复

### 保留段落

- §1.1 核心指令表（slash commands）→ llms.txt 独有，保留
- §1.3 分发入口 → 保留
- §1.4 导航系统 → 保留
- §3 文件体系 → 精简为一句话 + 指向 AGENTS.md
- §4 接入指南 → 保留

## 变更 C: core_rules.md（删除）

直接删除 `.maglev/rules/core_rules.md`。

理由：
1. 12 条规则已按 R2 处理完毕（重复/已覆盖/过时/提炼后归入 AGENTS.md）
2. 无其他文件 import 此文件（仅 llms.txt §2 引用，变更 B 已删除该引用）
3. 不需要 deprecated 过渡期——文件本身已长期不被 AI 读取

## 验证计划

### V1: 无断链验证

```bash
grep -r "core_rules" . --include="*.md" | grep -v "90_archive\|node_modules\|\.git"
```

预期：0 条结果（所有引用已清理）

### V2: AGENTS.md 完整性

- 工作原则章节存在且包含 3 条原则
- 不含已由 skill 覆盖的细节指令
- 不引用不存在的文件路径

### V3: llms.txt 精简验证

- 不含 core_rules.md 引用
- 不含与 AGENTS.md 重复的 runtime names 段
- 保留 slash commands 表、分发入口、接入指南
