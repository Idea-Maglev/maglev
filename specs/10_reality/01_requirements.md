# Maglev OS 现状需求 (Reality Requirements)

> **Updated**: 2026-06-01
> **Principle**: 此文件描述 Maglev 当前已满足的能力与已知缺口。以能力域组织，不按完成时间排列。每个 skill 名从 `.agents/skills/` 实际目录取。

## 1. 核心定位

Maglev 是一个 **Agent-Driven 方法论体系**，由三层构成：
*   **方法论** (`docs/thinking/`): "为什么这样做"
*   **协议** (`.maglev/protocols/`): "做事的规矩"（协作、提交、spec 生命周期）
*   **技能** (`.agents/skills/`): "能做什么"（25 个 skill，含主流程 7 个 + 质量面 3 个 + 支撑 15 个）

## 2. 已满足的能力

### 2.1 会话与路由
*   会话入口路由 → `entry-router`（识别请求类型、选定下游 skill）
*   现状同步 → `reality-sync`（建立 Reality / Risk / Action / Mode 四类认知）

### 2.2 需求与方案
*   需求收敛 → `requirement-convergence`（入口分流、需求定义、Ready Gate）
*   方案设计 → `spec-designer`（受控对话 → 可执行技术方案）
*   Spec 输入审计 → `spec-audit-surface`（实施前的需求与 spec 一致性审查）

### 2.3 实施与验证
*   代码执行委托 → `superpowers-bridge`（判断 spec 交付物类型，代码类委托给 Superpowers 执行，回收结果到验证体系）
*   非代码实施 → `context-implementer`（文档、配置、分析、Maglev 自维护的受控实施与自检）
*   综合验证 → `integrated-validator`（编排质量面，完成 requirements ↔ spec ↔ code ↔ tests 一致性校验）
*   Review 与验证面 → `review-validation-surface`（统一 review，汇总偏差与风险）
*   测试设计面 → `test-design-surface`（测试设计、覆盖策略、验证支撑）

### 2.4 知识与上下文
*   知识库索引 → `index-librarian`（编排 `index-protocol` v2.0 multi-track；统一 `dir-tree` 类型对任意目录递归生成 INDEX.md 网络；另有 `repo-entry` / `code-tree` 类型；完成 scan → verify → calibrate → navigate）
*   项目地图 → `maglev-map-maker`（基于仓库产物生成全景地图）
*   项目看板 → `project-board`（扫描 active specs/issues，证据驱动的阶段判断 + 角色映射，输出 `specs/20_evolution/board.md` 总看板与每个活跃 spec 的 `status.md` 子看板）
*   知识沉淀检查 → `knowledge-check`（检查思考、方案、参考资料是否已落盘）
*   结晶与归档 → `crystallization`（5 步流程：确认就绪 → 回写 reality → 收口 active → 回填发现 → 结构化归档）
*   写作前同步 → `maglev-content-sync`（重载定义与边界，降低新会话写作跑偏）
*   AI 上下文由 `AGENTS.md` 和 `llms.txt` 两个自动加载文件承载

### 2.5 项目初始化
*   Greenfield / Brownfield 初始化 → `maglev-bootstrapper`
*   存量项目接入 → `maglev-legacy-adopter`（环境诊断 → 基础设施注入 → 逆向工程编排）
*   逆向工程 → `maglev-reverse-spec`（从代码重建功能、流程、数据结构、协议边界）

### 2.6 分发与安装
*   npm / npx 首装入口 → `@idea-maglev/maglev-cli`
*   安装 / 更新执行器 → 发行物中的 `maglev_installer.py`
*   安装后更新 → `maglev-updater`（预览 → 执行 → 解释结果）
*   发行构建 → `scripts/maglev_release.py`
*   CHANGELOG 生成 → `maglev-changelog-generator`（读取变更草案 → 语义化 CHANGELOG）
*   运行时结构与分发详情 → [distribution_runtime.md](./distribution_runtime.md)

### 2.7 辅助工具
*   教学 → `maglev-tutor`（对话式课程）
*   UX 设计 → `maglev-design-ux`（Persona、User Journey、UI 状态图）

### 2.8 技能治理与行为纪律
*   技能发现与优化 → `skill-scout`（发现、私域化改造、持续优化能力对象）
*   编队巡逻 → `skill-squadron`（关联 skill 组的批量分析与协同优化）
*   行为纪律治理 → `maglev-discipline`（反 AI 惰性纪律；定义 3 条红线、8 类惰性模式识别、L0-L4 压力升级，通过 AGENTS.md 顶部区块 + 主流程 skill 引用实现三层防御）
*   持续进化观测 → `evolution-observatory`（系统化竞品观测与自我进化驱动；6 Phase 工作流 + 竞品 Registry + Insight 生命周期）

## 3. 已知缺口 (Known Gaps)
*   **公开安装链路未打通**: 详见 [distribution_runtime.md](./distribution_runtime.md)
*   **无 Kernel**: 没有集中式的 Skill 生命周期管理
*   **无自动化测试**: Skills 本身没有单元测试

---
*Defined by Maglev Reality Audit*
