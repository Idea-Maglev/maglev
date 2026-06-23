# Maglev 快速开始

> 目标：给第一次使用 Maglev 的用户一条最短可行路径，帮助你完成安装、确认结果，并知道下一步看什么。

## 1. 先看最短路径

如果你只想尽快开始，在项目根目录执行：

```bash
npx @idea-maglev/maglev-cli init
```

如果你更习惯先全局安装，再执行命令，也可以：

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli init
```

执行完成后，继续看本文的“安装后你会看到什么”。

---

## 2. 这篇文档适合谁

这篇文档适合：

- 第一次把 Maglev 接入一个项目的人
- 想先试一下 Maglev 能不能跑起来的人
- 不关心内部实现，只想知道怎么开始的人

如果你当前更关心的是“更新已有项目”，请直接看：

- [Maglev 更新与同步手册](./maglev_update_manual.md)

如果你想理解不同入口之间的关系，再继续看：

- [Maglev 多入口使用说明](./maglev_entrypoints.md)

如果你在公司私域环境中安装，需要先配置内部 npm 源、网络和权限，请看：

- [安装排障说明](./maglev_distribution_troubleshooting.md)

---

## 3. 开始之前需要什么

开始前请确认：

- 你在一个项目根目录里执行命令
- 本机已经安装 `Node.js` / `npm`
- 本机已经安装 `python3` 或 `python`，可运行 Maglev 安装器
- 建议安装 `uv`，让 Maglev 后续的 Python 协议脚本使用受控运行时

如果你不确定安装器能否启动，可以先执行：

```bash
python3 --version
```

如果你的终端提示找不到 Python，请先安装 Python，再回来执行 Maglev。

安装完成后，Maglev 项目内的 Python 协议脚本不再直接依赖裸系统 `python3`。你可以用下面的命令确认受控运行时是否可用：

```bash
./scripts/maglev-python --doctor
```

---

## 4. 第一次安装怎么做

### 方式 A：推荐方式

```bash
npx @idea-maglev/maglev-cli init
```

适合：

- 想直接体验
- 不想提前全局安装
- 想用当前推荐的正式入口

### 方式 B：全局安装后再执行

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli init
```

适合：

- 你会反复在多个项目里使用 Maglev
- 你更习惯全局命令

---

## 5. 安装过程中会发生什么

正常情况下，Maglev 会在当前项目里完成初始化，并落下它需要的基础目录和配置。

你不用先手动创建这些目录。

如果命令执行顺利，安装结束后，项目里通常会出现这些内容：

- `.agents/`
- `.maglev/`
- `specs/`
- `docs/`
- `issues/`
- `tests/`

其中最值得你关心的是：

- `.agents/`
  - 后续 AI 工作流和技能入口
- `.maglev/config.json`
  - 当前项目的本地配置
- `.maglev/sync_state.json`
  - 后续更新会使用的本地同步状态
- `scripts/maglev-python`
  - Maglev 协议脚本的受控 Python 运行时入口

---

## 6. 安装后你会看到什么

安装成功后，你可以重点检查这几件事：

### 1. 目录是否已经生成

至少确认下面两个目录已经出现：

- `.agents/`
- `.maglev/`

### 2. 同步状态文件是否存在

确认下面这个文件已经生成：

- `.maglev/sync_state.json`

如果这个文件存在，说明后续已经可以进入 `update` 流程。

### 3. Maglev 运行时是否可靠

确认受控 Python 运行时入口存在并能完成 doctor 检查：

```bash
test -x scripts/maglev-python
./scripts/maglev-python --doctor
```

如果 doctor 成功，继续验证冷启动会用到的索引检查：

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
```

期望结果是 `skills` 和 `specs` 都返回 `ok`。如果 doctor 报 `env_failed`，先安装 `uv` 或 Python 3.11+，再重新执行 doctor。

---

## 7. 安装成功后下一步做什么

通常建议按这个顺序继续：

1. 先确认 `.agents/`、`.maglev/` 和 `scripts/maglev-python` 已经落地
2. 执行 `./scripts/maglev-python --doctor` 确认 Maglev 运行时可用
3. 再通过 AI 工作流了解当前项目状态，例如 `/standup`
4. 需要更新时，再使用 `update`

如果你只是想先理解“装完以后能做什么”，建议继续看：

- [一个最小工作流示例](../../marketing/assets/minimal_workflow_showcase/published.md)
- [一个老项目接入案例](../../marketing/assets/legacy_system_showcase/published.md)

---

## 8. 已经安装过了怎么办

如果当前项目已经有：

- `.agents/`
- `.maglev/`
- `.maglev/sync_state.json`

那通常说明这个项目已经初始化过了。

这时不要再把它当成第一次安装处理，而应该看更新文档：

- [Maglev 更新与同步手册](./maglev_update_manual.md)

最常见的预览更新命令是：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

---

## 9. 常见问题

### Q1：我应该在什么目录执行 `init`？

在你想接入 Maglev 的项目根目录执行。

### Q2：为什么提示找不到 Python？

`init` / `update` 入口仍需要本机能运行安装器，因此请先安装 `python3` 或 `python`。

如果初始化已经完成，但后续 `/standup` 或索引检查提示 `env_failed`，请在项目根目录执行：

```bash
./scripts/maglev-python --doctor
```

doctor 会准备 Maglev 协议脚本使用的项目本地运行时。若仍失败，优先安装 `uv` 或 Python 3.11+ 后重试。

### Q3：执行 `init` 后没有看到 `.maglev/sync_state.json`

这通常说明初始化没有完整完成。请回看终端输出，排查失败步骤后重新执行。

### Q4：我已经初始化过，还能再执行 `init` 吗？

不建议把它当成重复首装来理解。已有项目更适合走 `update` 路径。

---

## 10. 下一步看什么

如果你已经完成安装，推荐继续看：

1. [Maglev 更新与同步手册](./maglev_update_manual.md)
2. [Maglev 多入口使用说明](./maglev_entrypoints.md)
3. [一个最小工作流示例](../../marketing/assets/minimal_workflow_showcase/published.md)

如果把这篇文档压缩成一句话，那就是：

> 先用 `npx @idea-maglev/maglev-cli init` 把 Maglev 装进项目里，确认 `.agents/` 和 `.maglev/` 已经生成，再继续往下用。
