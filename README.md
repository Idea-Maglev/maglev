# Maglev

> Maglev 不是另一个让 AI 多写一点代码的工具，而是一套帮助团队在 AI Coding 时代稳定协作、持续交付并沉淀资产的方法论、协议和可执行能力集合。

## 它解决什么问题

很多团队已经感受到 AI 带来的速度提升，但也越来越容易遇到这些问题：

- 代码写得更快了，返工却没有明显减少
- 每个人都在用 AI，但协作边界并不一致
- 需求、设计、代码和验证还是很容易脱节
- 老项目、复杂项目、跨角色协作项目依然难接

Maglev 关心的不是单点生成速度，而是：

- 怎么让团队和 AI 围绕同一份执行依据协作
- 怎么把一次需求变成可验证、可复用、可继续维护的资产
- 怎么把 AI 使用从个人习惯升级成团队能力

如果你想先看更完整的用户表达，建议先读：

- [欢迎来到 Maglev](docs/marketing/welcome.md)
- [Maglev 解决什么问题？](docs/marketing/assets/problem_statement/published.md)

## 30 秒开始

如果你只是想先把 Maglev 装进一个项目，在项目根目录执行：

```bash
npx @idea-maglev/maglev-cli init
```

如果项目已经初始化过，想先预览一次更新：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

更多用户文档见：

- [Maglev 快速开始](docs/guides/20_operations/maglev_distribution_quickstart.md)
- [Maglev 初始化使用手册](docs/guides/20_operations/maglev_init_manual.md)
- [Maglev 更新与同步手册](docs/guides/20_operations/maglev_update_manual.md)
- [Maglev 多入口使用说明](docs/guides/20_operations/maglev_entrypoints.md)

## Maglev 现在由什么构成

当前 Maglev 可以理解成三层：

- 方法论：定义为什么这样做，主要在 [docs/thinking/](docs/thinking/)
- 协议：定义做事的规矩，主要在 [.maglev/protocols/](.maglev/protocols/)
- 能力：定义具体能做什么，主要在 [.agents/skills/](.agents/skills/)

同时，它已经具备一条可运行的分发链路：

- CLI 入口：[`@idea-maglev/maglev-cli`](packages/maglev-cli/package.json)
- 初始化与更新执行核心：发行物中的 `maglev_installer.py`（当前由 npm 包内镜像携带）
- 用户操作文档：[`docs/guides/20_operations/`](docs/guides/20_operations/)

当前能力现状的统一说明见：

- [Maglev OS 现状需求](specs/10_reality/01_requirements.md)
- [Distribution Runtime Reality](specs/10_reality/distribution_runtime.md)
- [Active Evolution Index](specs/20_evolution/active/README.md)

## 它能实际做什么

Maglev 不是只讲原则，当前已经围绕几类核心动作提供能力：

- 入口路由与会话分流：`entry-router`
- 现状同步：`reality-sync`（兼容入口：`/standup`）
- 需求收敛：`requirement-convergence`
- 方案设计：`spec-designer`（兼容入口：`/create-spec`）
- 代码逆向成 Spec：`maglev-reverse-spec`
- 存量项目接入：`maglev-legacy-adopter`
- 上下文实施：`context-implementer`（兼容入口：`/quick-dev`）
- 审计、评审与综合验证：`spec-audit-surface`、`review-validation-surface`、`test-design-surface`、`integrated-validator`（兼容入口：`/validate-all`）
- 现实结晶：`crystallization`
- 知识沉淀检查：`knowledge-check`
- 项目地图与知识索引：`maglev-map-maker`、`index-librarian`
- 技能发现与能力进化：`skill-scout`、`skill-squadron`

如果你想看一页用户视角的能力说明，而不是直接读技能目录，建议看：

- [Maglev 现在具体有哪些能力](docs/marketing/assets/capability_snapshot/published.md)
- [一个最小工作流示例](docs/marketing/assets/minimal_workflow_showcase/published.md)
- [一个老项目接入案例](docs/marketing/assets/legacy_system_showcase/published.md)

## 安装后怎么用

安装完成后，Maglev 的常见使用方式通常分成两层：

- 安装前入口：`npm` / `npx`
- 安装后交互层：AI Workflow / Skill

也就是说，一个全新项目不应该默认假设 `/standup`、`/create-spec` 这些历史入口已经存在，而是应先执行 `init` 完成初始化。

当前需要特别注意：

- 这四个 slash command 仍然存在，但它们现在是兼容 workflow 入口
- 当前主流程的 skill runtime name 已切到新名
- 统一项目级索引见 [Active Evolution Index](specs/20_evolution/active/README.md)

项目接入后，典型工作流会像这样：

1. 用 `npx @idea-maglev/maglev-cli init` 完成初始化
2. 在 AI 会话入口先做路由和分流，当前更建议由 `entry-router` 承接
3. 如项目现状不清，先做 `现状同步（reality-sync）`；如需求边界不稳，先走 `requirement-convergence`
4. 根据任务进入 `方案设计（spec-designer）`、逆向、`上下文实施（context-implementer）` 等能力
5. 在交付前用审计、评审、综合验证类能力做收口
6. 在结果成立后，用 `crystallization` 做后段闭环；如需检查知识沉淀，用 `knowledge-check`

如果你更关心这里的边界关系，继续看：

- [Maglev 不直接写代码，那代码部分怎么解决？](docs/marketing/assets/how_maglev_handles_coding_execution/published.md)
- [为什么 AI Coding 越强，越需要治理](docs/marketing/assets/why_ai_coding_needs_governance/published.md)

## 推荐阅读路径

如果你不想自己找，按下面几条路径看会比较顺。

首次了解 Maglev：

1. [欢迎来到 Maglev](docs/marketing/welcome.md)
2. [Maglev 解决什么问题？](docs/marketing/assets/problem_statement/published.md)
3. [一个最小工作流示例](docs/marketing/assets/minimal_workflow_showcase/published.md)
4. [Maglev 现在具体有哪些能力](docs/marketing/assets/capability_snapshot/published.md)

想先把项目跑起来：

1. [Maglev 快速开始](docs/guides/20_operations/maglev_distribution_quickstart.md)
2. [Maglev 初始化使用手册](docs/guides/20_operations/maglev_init_manual.md)
3. [Maglev 更新与同步手册](docs/guides/20_operations/maglev_update_manual.md)

更关心老项目和存量系统：

1. [为什么老项目和存量系统会成为 Maglev 的关键场景](docs/marketing/assets/why_legacy_systems_matter/published.md)
2. [一个老项目接入案例](docs/marketing/assets/legacy_system_showcase/published.md)

## 仓库导航

| 路径 | 作用 |
| :--- | :--- |
| [docs/marketing/](docs/marketing/) | 用户表达、案例、角色化内容与对外阅读入口 |
| [docs/guides/](docs/guides/) | 面向使用者和维护者的操作手册 |
| [docs/thinking/](docs/thinking/) | 方法论、决策与架构思考 |
| [.maglev/protocols/](.maglev/protocols/) | Maglev 的协议层与规则边界 |
| [.agents/skills/](.agents/skills/) | 本地技能目录与执行能力 |
| [specs/](specs/) | 项目规格与现状描述 |
| [references/](references/) | 外部资料、论文与对照阅读 |
| [archive/starter-kit_legacy/](archive/starter-kit_legacy/) | 旧版 Starter Kit 归档，仅供历史参考 |
| [archive/](archive/) | 历史归档内容 |

## 贡献与协作

如果你准备参与这个仓库，建议先看：

- [协作协议](.maglev/protocols/collaboration.md)
- [指南总入口](docs/guides/README.md)
- [Maglev 开发与发布流程](docs/guides/20_operations/maglev_development_release_workflow.md)
- [思考与决策日志](docs/thinking/README.md)
- [贡献记录](contributors/contribution_log.md)

问题反馈目前使用仓库内路径：

- [issues/](issues/)
