# Input Facts: Incremental

## 1. Base Spec
- **Intent**: `specs/20_evolution/active/project_board_skill/00_intent.md`
- **Requirements**: `specs/20_evolution/active/project_board_skill/01_requirements.md`
- **Status**: 需求定义完成，handoff approved，进入方案设计

## 2. 需求边界摘要

### In Scope
- 新建标准 Skill `project-board`，部署到所有 Maglev 化项目
- 扫描 `specs/20_evolution/active/` 识别活跃需求
- 交叉证据判断流程阶段（文件存在性 + 内容质量 + 代码变更 + 测试覆盖）
- 映射 VO/TP/XG 角色状态
- 两级看板：总看板 `board.md` + 子看板 `status.md`
- 生命周期事件驱动 + 手动触发
- 缓存模型 + 时间戳标注

### Out of Scope
- 外部系统集成、工时统计、绩效评估、历史趋势
- Git commit 级细粒度追踪
- PM 层进度管理

## 3. 设计前提（苏格拉底访谈确认）

| 前提 | 决策 | 来源 |
|------|------|------|
| 人员-角色映射 | 项目级配置为主（如 `specs/10_reality/team.md`），spec 级可覆盖 | 访谈 R1 |
| Skill 集成模式 | 独立 Skill 负责更新生成，reality-sync 启动时读取展示摘要 | 访谈 R2 |
| 阶段判断深度 | 文件存在是必要不充分条件，需内容质量/下游证据交叉确认 | 访谈 R3 |
| 查询策略 | 允许缓存 + 时间戳，不强求每次实时查询 | 访谈 R3 |
| 归档联动 | crystallization 归档时调用 board 更新，去掉已归档项 | 访谈 R4 |

## 4. 功能需求 (7 FR / 18 AC)

| FR | 名称 | AC 数 |
|----|------|-------|
| F-1 | 活跃需求扫描 | 2 |
| F-2 | 流程阶段判断 | 3 |
| F-3 | 角色状态映射 | 3 |
| F-4 | 看板视图输出 | 3 |
| F-5 | 持久化看板文件 | 3 |
| F-6 | 生命周期事件驱动更新 | 3 |
| F-7 | 需求级子看板 | 3 |

## 5. 现有参考

- `docs/guides/10_concepts/role_personas.md` — VO/TP/XG 角色定义
- `specs/10_reality/glossary.md` — 术语基线
- `docs/DASHBOARD.md` — 现有静态快照（不直接改写，但可参考格式）
- `.agents/skills/reality-sync/SKILL.md` — 集成目标（读取展示）
- `.agents/skills/crystallization/SKILL.md` — 集成目标（归档联动）
