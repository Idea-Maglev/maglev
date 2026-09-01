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


## Maglev 现在由什么构成

当前 Maglev 可以理解成三层：

- 能力：定义具体能做什么，主要在 [.agents/skills/](.agents/skills/)

同时，它已经具备一条可运行的分发链路：

- CLI 入口：[`@idea-maglev/maglev-cli`](packages/maglev-cli/package.json)
- 初始化与更新执行核心：发行物中的 `maglev_installer.py`（当前由 npm 包内镜像携带）



## 它能实际做什么

Maglev 不是只讲原则，当前已经围绕几类核心动作提供能力：

<!-- maglev:managed:mainline -->
当前主链路（由治理注册表生成）：

- `entry-router`
- `reality-sync`
- `requirement-convergence`
- `spec-designer`
- 执行分支：`context-implementer` | `code-execution-slot`
- `integrated-validator`
- `crystallization`
- 横切能力：`knowledge-check`
<!-- /maglev:managed:mainline -->

<!-- maglev:managed:compatibility -->
兼容 workflow 入口（由治理注册表生成）：

- `/standup` → `reality-sync`
- `/create-spec` → `spec-designer`
- `/quick-dev` → `context-implementer`
- `/validate-all` → `integrated-validator`
<!-- /maglev:managed:compatibility -->

- 代码逆向成 Spec：`maglev-reverse-spec`
- 存量项目接入：`maglev-legacy-adopter`
- 项目地图与知识索引：`maglev-map-maker`、`index-librarian`
- 技能发现与能力进化：`skill-scout`、`skill-squadron`

如果你想看一页用户视角的能力说明，而不是直接读技能目录，建议看：


## 安装后怎么用

安装完成后，Maglev 的常见使用方式通常分成两层：

- 安装前入口：`npm` / `npx`
- 安装后交互层：AI Workflow / Skill

也就是说，一个全新项目不应该默认假设 `/standup`、`/create-spec` 这些历史入口已经存在，而是应先执行 `init` 完成初始化。

当前需要特别注意：

- 这四个 slash command 仍然存在，但它们现在是兼容 workflow 入口
- 当前主流程的 skill runtime name 已切到新名

项目接入后，典型工作流会像这样：

1. 用 `npx @idea-maglev/maglev-cli init` 完成初始化
2. 在 AI 会话入口先做路由和分流，当前更建议由 `entry-router` 承接
3. 如项目现状不清，先做 `现状同步（reality-sync）`；如需求边界不稳，先走 `requirement-convergence`
4. 根据任务进入 `方案设计（spec-designer）`、逆向、`上下文实施（context-implementer）` 等能力
5. 在交付前用审计、评审、综合验证类能力做收口
6. 在结果成立后，用 `crystallization` 做后段闭环；如需检查知识沉淀，用 `knowledge-check`

如果你更关心这里的边界关系，继续看：


## 仓库导航

| 路径 | 作用 |
| :--- | :--- |
| [.agents/skills/](.agents/skills/) 与 [.agents/workflows/](.agents/workflows/) | 当前主流程能力与兼容入口 |
| [.agents/skills/](.agents/skills/) | 本地技能目录与执行能力 |
| [references/](references/) | 外部资料、论文与对照阅读 |

## 贡献与协作

如果你准备参与这个仓库，建议先看：

- [主流程入口](.agents/skills/entry-router/SKILL.md)

问题反馈目前使用仓库内路径：

- [issues/](https://github.com/Idea-Maglev/maglev/issues)
