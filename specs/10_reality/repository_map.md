# Maglev OS Repository Map

> **Updated**: 2026-04-23
> **Principle**: 指向而非复述 (Point, Don't Repeat)。

## 1. 核心目录

| Path | Role | Description |
| :--- | :--- | :--- |
| `.agents/skills/` | **Capabilities** | 当前运行时能力对象目录，已完成主流程 skill rename、非核心对象清理与 internal 模块收口；私域 skill 的命名、状态与替代关系统一通过 `.agents/private-catalog.yaml` 治理 |
| `.agents/workflows/` | **Workflows** | IDE Slash Commands 定义 |
| `.maglev/` | **Config** | 核心规则与配置 |
| `docs/thinking/` | **Decision Log** | 哲学、批判、架构、案例与复盘等思考资产；已按 9 位段（00_meta / 10_critique / 20_architecture / 30_philosophy / 40_paper / 50_alignment / 60_case / 70_retrospective / 90_archive）组织，每段含 collection `INDEX.md`；由 `index-librarian` skill 维护索引一致性 |
| `docs/guides/` | **User Manuals** | 面向用户与维护者的操作手册 |
| `.maglev/protocols/` | **Protocols** | 协作规范、提交标准、Spec 生命周期 |
| `specs/` | **Specifications** | 项目自身的规格说明 |
| `specs/20_evolution/active/` | **Active Evolution Index** | 当前仍在推进、尚未封板的演进主题索引 |
| `specs/90_archive/` | **Archive** | 历史 Spec 与已结束演进主题的归档区，不作为当前现状入口 |
| `.maglev_build/` | **Build Sandbox** | release dry-run / build 生成的发行构建沙箱 |
| `scripts/` | **Release Tooling** | 上游发布与编译脚本 |
| `packages/maglev-cli/` | **CLI Package** | npm / npx 用户入口与包内发行镜像 |
| `archive/starter-kit_legacy/` | **Legacy Archive** | 旧版 Starter Kit 归档，仅作历史对照 |
| `references/` | **Knowledge** | 学术论文、技术文章 |
| `contributors/` | **Community** | 贡献者记录 |
| `solutions/` | **Output** | 示例项目与方案 |

## 2. 核心资产概览

### 方法论层 (Methodology)
*   → `docs/thinking/` : 思考与决策日志，按 9 位段（00_meta / 10_critique / 20_architecture / 30_philosophy / 40_paper / 50_alignment / 60_case / 70_retrospective / 90_archive）组织，每段含 collection `INDEX.md`；root `INDEX.md` 含位段表与认知地图占位
*   → `docs/thinking/30_philosophy_maglev_equation.md` : Maglev 宣言
*   → `.maglev/protocols/collaboration.md` : 协作规范

### 工具层 (Capabilities)
*   → `.agents/skills/` : skill 运行目录；主流程四对象 `reality-sync` / `spec-designer` / `context-implementer` / `integrated-validator`
*   → `.agents/skills/_internal/` : internal 模块目录，不是隐藏 skill 列表；承接不应独立暴露但被多个现役 skill 共享的内部模块与契约（含 spec pipeline 共享模块与 AI context check 契约）
*   → `.agents/workflows/` : Slash Command 定义；四个主流程 workflow 文件名作为兼容入口

### 产品层 (Product)
*   → `.maglev_build/` : release dry-run / build 的发行构建沙箱
*   → `packages/maglev-cli/` : 当前对外推荐的 npm / npx 安装入口，内部携带包内镜像
*   → `docs/guides/20_operations/` : 快速开始、初始化、更新、排障、发布手册
*   → `archive/starter-kit_legacy/` : 历史 Starter Kit 归档
*   → `llms.txt` : LLM 可读项目描述

## 3. 专题现状入口

当前分发、安装、更新链路的专题现状，统一见：

*   [distribution_runtime.md](./distribution_runtime.md)

当前仍在推进的演进主题，统一见：

*   [../20_evolution/active/README.md](../20_evolution/active/README.md)

## 4. 当前结构真相补充

### 4.1 主流程 skill runtime name

当前四个主流程运行名已是：

1. `reality-sync`
2. `spec-designer`
3. `context-implementer`
4. `integrated-validator`

### 4.2 主流程 workflow 入口

当前四个 workflow 文件名继续保留为兼容入口：

1. `standup.md`
2. `create-spec.md`
3. `quick-dev.md`
4. `validate-all.md`

### 4.3 当前未闭环的项目级问题

当前仍应持续关注的 active issue：

1. `issues/active/task_public_distribution_channel.md`

### 4.4 活跃主题观测入口

当前活跃 evolution 主题的可观测现状由 `project-board` Skill 持续维护：

*   总看板：`specs/20_evolution/board.md`
*   子看板：每个活跃 spec 目录下的 `status.md`
*   更新机制：手动触发 `/board`，或在 crystallization Step 5 归档后自动刷新

### 4.5 `_internal` 目录的结构定位

`.agents/skills/_internal/` 的存在是为了表达“内部模块真实存在，但不应继续伪装成独立 skill”。

当前判断口径如下：

1. 放在 `_internal` 里的对象，不作为独立入口分发
2. 它们通常被多个现役 skill 复用，或者属于某个主 skill 的内部流水线
3. `_internal` 不是新的用户入口层，也不是一组隐藏可调用 skill
4. 如果某个对象具备独立入口、独立分发和独立治理价值，就不应留在 `_internal`

## 5. AI 引导摘要

> 当仓库包含多个子项目或需要 AI 快速理解项目上下文时，以下摘要提供结构化入口。
> 由 maglev-bootstrapper 自动扫描 + 用户确认后写入。摘要过期时由 maglev-map-maker 提醒。

### 摘要模板

每个仓库/子项目按以下格式维护 AI 引导摘要（控制在 20 行以内）：

```markdown
## {仓库名} — AI 引导摘要

> 生成日期: {YYYY-MM-DD} | 生成方式: maglev-bootstrapper 自动扫描 + 用户确认

### 产品上下文
- 目标用户: {谁在用}
- 核心功能: {做什么}
- 业务规则: {关键约束}

### 技术约定
- 技术栈: {框架 + 语言 + 工具链}
- 构建: `{build command}` | 测试: `{test command}` | 开发: `{dev command}`
- 规范: {lint + format 规则}

### 代码结构
- `{dir1}/` — {职责}
- `{dir2}/` — {职责}
- `{dir3}/` — {职责}
```

---
*Mapped by Maglev Reality Checker - 2026-02-13*
