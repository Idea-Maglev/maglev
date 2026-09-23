---
title: "第一次接入并确认成功"
dimension: developer
audience: developer
page_type: tutorial
last_updated: "2026-09-15"
generator: wiki_authoring
---

# 第一次接入并确认成功

这条路径适用于还没有 Maglev 状态的目标项目。你可以自己在终端执行安装，也可以让 AI Agent 代为执行；成功依据是 Agent 实际执行的命令、生成的受管文件和明确的阻塞信息，不是一段没有执行证据的回复。

> 本页完成任务：**自行执行安装，或通过 Prompt 让 AI Agent 完成安装并回报实际结果。**

## 选择安装方式

方式 A 由你通过官方 npm 入口完成安装；方式 B 让 AI Agent 代为执行该安装并提交验证证据。若 Agent 已提供 Maglev Prompt 入口，还可由该入口启动其自身的接入流程。

### 共用前置条件

- Node.js / npm 环境（npx 可用）
- 终端可访问 npm 源
- 本机有 `python3` 或 `python`，建议安装 `uv`——`init` / `update` 入口最终都靠 Python 启动安装器（出处：[分发快速上手](../../../source operation guides/20_operations/maglev_distribution_quickstart.md)）

### 方式 A：在终端执行

在项目根目录按顺序执行：

```bash
npx @idea-maglev/maglev-cli init
```

如需全局安装后长期使用：

```bash
npm install -g @idea-maglev/maglev-cli
```

预期结果：命令行输出安装成功信息，`maglev` 命令可用。公司私域环境需先配置内部 npm 源与网络权限，见[分发快速上手](../../../source operation guides/20_operations/maglev_distribution_quickstart.md)。

### 方式 B：通过 Prompt 让 AI Agent 安装

如果你不想自行操作终端，把下面整段发送给平时使用的编码 Agent：

```text
请在当前项目安装并初始化 Maglev。请使用官方 npm 入口执行 `npx @idea-maglev/maglev-cli init`。如初始化需要确认代码仓库或项目设置，先向我提问。结束时请报告生成的受管文件，以及任何未解决的阻塞项。
```

Agent 需要终端执行和 npm 网络访问权限；缺少权限或环境时，应说明具体阻塞项，而不是宣称安装成功。上方完整 Prompt 适用于任何具备这些权限的编码 Agent。若 Agent 的界面明确提供 Maglev Prompt 入口，也可以输入 `Initialize Maglev` 或 `/maglev-init`；这是一条平台已集成的快捷路由，不应假定普通 Agent 天然识别它。该入口会扫描当前目录、执行接入流程、收集仓库信息并完成 AI 上下文自检（事实依据：[接入与集成能力](../../../internal Reality/adoption-integration/capability/overview.md)）。

## 可选：检查协议运行时

只有需要立即运行项目内的 Maglev 协议脚本，或需要排查安装后的运行环境时，再执行：

```bash
./scripts/maglev-python --doctor
```

自检输出应包含 `repo_root`、`python` 环境路径与版本信息。`--doctor` 检查的是 `scripts/maglev-python` 这条受控运行时入口（uv 优先、系统回退），不决定 `maglev-cli init` 是否已经完成安装（出处：[交付运行时能力](../../../internal Reality/delivery-runtime/capability/overview.md)）。如果由 Agent 执行这项可选检查，让它附上实际输出。

无论选择哪种安装方式，都应确认 `.agents/`、`.maglev/`、`specs/`、`docs/`、`issues/` 等受管骨架已经生成。

## 常见问题

- **npx 拉包超时**：检查 npm 源配置或改用全局安装方式；私域环境的 npm 源与网络要求见[分发快速上手](../../../source operation guides/20_operations/maglev_distribution_quickstart.md)
- **init 后环境检查失败**：按提示安装 `uv` 或确认 Python >= 3.11（`scripts/maglev-python` 的最低版本要求即 3.11），更多现象见[分发排障手册](../../../source operation guides/20_operations/maglev_distribution_troubleshooting.md)

## 下一步

- [教程：从安装到第一次完整交付](first-success.md)：装好后从零走完第一次完整交付
- [日常推进手册](session-workflow.md)：接入后每个工作循环怎么操作
- [从请求到结晶的日常协作](session-workflow.md)：开始与 Agent 协作前了解主链、交接点与验证边界。
- [故障排查与常见问题](update-and-recovery.md)：安装或自检报错先查这里
- 操作事实原文：[Maglev 分发与快速上手](../../../source operation guides/20_operations/maglev_distribution_quickstart.md)

---

读完本教程，你可以在一个尚未接入 Maglev 的新项目里完成初始化，并按 **需求收敛 → 方案 → 实施 → 验证** 的顺序走完一次小模块交付。上手约半天，主要学的不是新工具，而是怎么把需求讲清楚（Spec）：你把逻辑讲清楚，AI 负责敲代码，你负责裁决。

主流程如下：

```mermaid
flowchart LR
    A[初始化项目] --> B[验证运行时就绪]
    B --> C[需求收敛：写 Spec]
    C --> D[方案与实施：AI 生成 + 人裁决]
    D --> E[验证：对照 Spec 收口]
    E -->|发现问题| D
```

## 前置条件

- 在目标项目的 Git 仓库根目录操作（不是 Git 仓库只会警告，不会阻断初始化）
- 系统中有可用的 `python3` 或 `python`；建议安装 `uv`，用于后续受控 Python 协议运行时
- Node / npm 环境，`npx` 可用
- IDE 用 Cursor 或 VS Code 即可，不强制更换 IDE
- 按受控范围选一个真实、可验证的小任务作为首次练习；先定义成功信号和停止条件，不预先承诺效率收益。

## 第 1 步：初始化项目

在 Git 仓库根目录执行：

```bash
npx @idea-maglev/maglev-cli init
```

也可以先全局安装再执行：

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli init
```

执行后会有一轮交互式问答：

1. **项目名称**：默认取当前目录名
2. **项目简述**：写入 `.maglev/config.json`
3. **是否交互式注册子仓库**：接入模式默认 `clone`；还没想清楚就跳过，不会卡住初始化，后续再补 `internal Reality/repository_map.md`

初始化完成后，项目里会出现 `specs/`、`docs/`、`issues/`、`tests/`、`.agents/`、`.maglev/` 等目录骨架，以及三个本地配置文件：`.maglev/config.json`、`.maglev/extensions.sources.yaml`、`.maglev/sync_state.json`（`.maglev/` 承载配置与同步状态的布局事实出处：[下游项目运行布局](../../../internal Reality/delivery-runtime/operations/downstream-layout.md)）。

## 第 2 步：验证运行时就绪

依次执行：

```bash
./scripts/maglev-python --doctor
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
npx @idea-maglev/maglev-extension-cli sources list --json
```

四条都通过，说明 `/standup` 等安装后入口依赖的协议运行时与扩展源已就绪（受控 Python 运行时与 CLI 入口的能力事实出处：[交付运行时能力](../../../internal Reality/delivery-runtime/capability/overview.md)）。再确认根目录没有出现 `install.sh` 和 `maglev_installer.py`——按当前分发规则，这两个文件不应作为目标项目资产下发。

## 第 3 步：需求收敛——把意图写成 Spec

Maglev 的新工作契约是 **Doc is Code**：没文档就不准提交代码（出处：[传统团队起步指南](../../../source operation guides/00_start/maglev_traditional_team_kickoff.md)）。把前置条件中选定的试点模块需求写成一个 Markdown 文件，讲清楚三件事：用户用它完成什么（核心价值）、怎样算做完（可逐条勾选核对的验收标准）、参考设计（设计稿链接或草图截图）。写完即提交进仓库，让需求不再躺在聊天记录里。需求文件放哪、长什么样，见[日常推进手册](session-workflow.md)。

## 第 4 步：方案与实施——AI 生成，人裁决

对待项目里已有代码的策略是**增量开发**：

1. 不推倒重来，旧代码是资产，维持原状
2. 需要复用时，把旧代码"冻结"为 API 供新代码调用
3. 只有**新功能**才走 Spec → AI 生成的新模式

实施时，在 IDE 中把 Spec 和相关上下文一起交给 AI 生成代码，然后逐行 Review：

- 发现遗漏（比如 AI 漏了倒计时之类的边界逻辑）就手动补全，或追问 AI
- 只要你觉得 AI 写得不对，**拒绝它，或者修改它**——你永远拥有一票否决权
- 最终 `git push` 权限始终在你手里

## 第 5 步：验证——对照 Spec 收口

- 运行项目，对照第 3 步写下的验收标准逐条核对
- 排查问题时让 AI **对照 Spec 做三角验证**，而不是漫无目的地翻日志
- 提交阶段，CI 会拦住所有文档和代码不一致的内容（出处：[传统团队起步指南](../../../source operation guides/00_start/maglev_traditional_team_kickoff.md)）

全部验收标准通过，第一次交付完成。

## 常见问题

- **明明执行 `init`，却提示切换为 Update 模式**：当前目录残留 `.maglev/sync_state.json`，安装器把它识别为已接入项目。首装测试请换一个全新目录。
- **提示未找到 Python**：npm / npx 入口最终也依赖 Python 启动安装器。安装 Python 3 并确保 `python3` 或 `python` 在 PATH 中。
- **想先看看 init 会做什么再执行**：用 `--dry-run` 只预览动作、不真正写文件：`npx @idea-maglev/maglev-cli init --dry-run`（自动化场景再加 `--skip-prompt`，参数说明见[Maglev 初始化手册](../../../source operation guides/20_operations/maglev_init_manual.md)）。
- **跳过了子仓库登记**：初始化仍会成功；后续把代码仓库按 `clone` 或 `submodule` 方式接入，并更新 `internal Reality/repository_map.md`。

## 下一步

- [日常推进手册](session-workflow.md)：接入后每个工作循环怎么操作
- [安装 maglev-cli](first-success.md)：只关注安装与运行时自检
- [存量项目接入](brownfield-adoption.md)：目标不是新项目而是老项目时看这里
- [故障排查与常见问题](update-and-recovery.md)：安装、更新或环境报错先查这里
