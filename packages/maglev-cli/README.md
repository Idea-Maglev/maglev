# Maglev

Maglev 是一套帮助团队在 AI Coding 时代稳定协作、持续交付并沉淀资产的方法论、协议和可执行能力集合。

`@idea-maglev/maglev-cli` 是 Maglev 的 npm / npx 分发入口，用于把 Maglev 初始化到项目中，并在后续同步更新 Maglev 的协议、技能和运行时资产。

## 什么时候使用这个包

使用这个包可以完成两类操作：

- 初始化新项目：把 Maglev 的基础目录、协议和 AI 工作流安装到当前项目。
- 更新已有项目：把项目中的 Maglev 资产同步到当前发布版本。

如果你只是第一次接触 Maglev，可以先把它理解为：

> 用 `npx @idea-maglev/maglev-cli init` 把 Maglev 装进项目，再让 AI 基于 Maglev 的流程做需求收敛、方案设计、实施和验证。

## 快速开始

在目标项目根目录执行：

```bash
npx @idea-maglev/maglev-cli init
```

如果你更习惯全局安装，也可以：

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli init
```

项目已经安装过 Maglev 时，可以先预览更新：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

确认无误后再执行：

```bash
npx @idea-maglev/maglev-cli update
```

## 安装前需要什么

开始前请确认本机具备：

- Node.js / npm
- Python 3，可通过 `python3` 或 `python` 启动 Maglev 安装器
- 建议安装 `uv`，或准备 Python 3.11+，用于 Maglev 协议脚本的受控运行时

初始化完成后，可以在项目根目录验证 Maglev 运行时：

```bash
./scripts/maglev-python --doctor
```

如果 doctor 报 `env_failed`，优先处理 Python / `uv` 环境；这通常不是项目索引内容损坏。

## 常用命令

```bash
# 初始化当前项目
npx @idea-maglev/maglev-cli init

# 预览更新
npx @idea-maglev/maglev-cli update --dry-run

# 执行更新
npx @idea-maglev/maglev-cli update

# 查看 CLI 与包内发行物版本
npx @idea-maglev/maglev-cli version
npx @idea-maglev/maglev-cli version --json
```

## 安装后会看到什么

初始化成功后，项目中通常会出现：

- `.agents/`：Maglev 的 AI 技能与工作流入口
- `.maglev/`：Maglev 本地配置、同步状态与协议
- `specs/`：规格、当前事实和演进主题
- `issues/`：任务、反馈和草稿入口
- `scripts/maglev-python`：Maglev 协议脚本的受控 Python 运行时入口

其中 `.maglev/sync_state.json` 是后续执行 `update` 的关键状态文件。

## 公司私域环境

如果你在 private enterprise 内部环境中使用 Maglev，通常需要先确认私域 npm 源、网络和权限。不要在当前业务项目里寻找私域安装文档；这些说明维护在 Maglev 源仓库中。

你可以让智能体打开 Maglev 源仓库，查找 private enterprise 私域安装引导，重点确认：

- 如何配置 `@idea-maglev` scope registry
- 什么时候不需要登录私域 npm
- 如何让智能体代为执行安装检查
- 安装完成后如何恢复 npm 源配置

## 更多文档

CLI 初始化后的业务项目不默认携带完整 Maglev 文档。需要进一步了解安装、更新、入口关系、私域配置或方法论时，请让智能体去 Maglev 源仓库查阅对应文档，而不是在当前业务项目里查找 `docs/guides/` 或 `docs/private/`。

可以直接对智能体说：

```text
请到 Maglev 源仓库查看最新文档，帮我确认当前问题对应的安装、更新、入口或私域环境说明。不要假设当前业务项目里已经同步了 Maglev 的完整 docs 目录。
```

## 维护者说明

这个 README 面向 npm 包使用者。维护者如果需要修改安装器、构建发行物或发布新版本，请回到 Maglev 源仓库阅读发布手册。

不要直接编辑 `packages/maglev-cli/dist/` 下的构建产物；安装器源文件位于 `packages/maglev-cli/runtime-src/`，发行物由 `scripts/maglev_release.py` 生成。
