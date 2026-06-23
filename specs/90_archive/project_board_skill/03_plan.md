# 实施计划: project_board_skill

> 👤 **Executive Brief**
>
> 分 4 步实施：Skill 骨架 → 核心逻辑（扫描+判断+渲染）→ 集成改造 → 验证。
> 每步有独立的验证点，可以逐步交付。

---

## 1. 任务清单

### Phase 1: Skill 骨架

| 任务 | 说明 | 产出 | 状态 |
|------|------|------|------|
| T-1.1 | 创建 `.agents/skills/project-board/SKILL.md` | Skill 入口文件 | ✅ |
| T-1.2 | 创建 `references/board.workflow.md` | 工作流编排 | ✅ |
| T-1.3 | 创建 `references/stage-evidence-rules.md` | 证据规则参考 | ✅ |
| T-1.4 | 创建 `specs/10_reality/team.md` 模板 | 团队配置模板 | ✅ |

**验证**: Skill 可被 AI Agent 识别和加载

### Phase 2: 核心逻辑

| 任务 | 说明 | 产出 | 状态 |
|------|------|------|------|
| T-2.1 | 创建 `references/step-01-scan.md` | 扫描步骤定义 | ✅ |
| T-2.2 | 创建 `references/step-02-judge-stage.md` | 阶段判断步骤 | ✅ |
| T-2.3 | 创建 `references/step-03-map-roles.md` | 角色映射步骤 | ✅ |
| T-2.4 | 创建 `references/step-04-render-board.md` | 渲染与持久化步骤 | ✅ |

**验证**: 在当前 Maglev 仓库上执行一次完整扫描，输出 board.md

### Phase 3: 集成改造

| 任务 | 说明 | 产出 | 状态 |
|------|------|------|------|
| T-3.1 | 修改 reality-sync step-01-sync.md | 追加 board 读取步骤 | ✅ |
| T-3.2 | 修改 crystallization 相关步骤 | 追加归档后 board 更新 | ✅ |
| T-3.3 | 注册 skill 到 AGENTS.md | 可发现性 | ✅ |

**验证**: reality-sync 启动时展示看板摘要；crystallization 归档后看板自动更新

### Phase 4: 验证

| 任务 | 说明 | 产出 | 状态 |
|------|------|------|------|
| T-4.1 | 在当前仓库全量测试 | 完整 board.md + 各 spec 的 status.md | ✅ |
| T-4.2 | 边界测试（空仓库、单需求、10+ 需求） | 验证输出格式稳定性 | ⚠️ 已补 contract fixture，未跑真实更新链路 |
| T-4.3 | 缓存测试（首次 vs 二次更新） | 验证增量更新正确性 | ⚠️ 已补缓存契约校验，未覆盖真实首二次更新 |

---

## 2. 验证计划

| 验收标准 | 测试方法 |
|----------|---------|
| AC-F1-1: 扫描识别活跃 spec | 在 Maglev 仓库执行，验证 active/ 下所有 spec 被列出 |
| AC-F2-1: 交叉证据判断阶段 | 对比人工判断结果与 Skill 输出 |
| AC-F2-3: 不确定时标记待确认 | 构造缺失证据场景，验证 confidence=uncertain |
| AC-F3-2: 人员名称展示 | 创建 team.md 后验证 |
| AC-F4-1: 矩阵视图 | 验证 Markdown 表格在终端和 IDE 中可读 |
| AC-F5-2: 时间戳 | 验证 board.md 包含更新时间 |
| AC-F6-1: 事件驱动 | 在 crystallization 后验证 board 自动更新 |
| AC-F7-1: 子看板 | 验证每个 spec 目录下生成 status.md |
