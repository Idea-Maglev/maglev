# Maglev 更新与同步手册

> 目标：给已经接入 Maglev 的用户一份真正可执行的更新说明，帮助你安全预览更新、执行更新，并知道更新后该检查什么。

## 1. 先看最常用的命令

如果你只是想先看看这次更新会改什么，推荐先执行：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

如果确认没有问题，再执行正式更新：

```bash
npx @idea-maglev/maglev-cli update
```

如果你是全局安装方式，也可以使用：

```bash
maglev-cli update --dry-run
maglev-cli update
```

---

## 2. 这篇文档适合谁

这篇文档适合：

- 已经把 Maglev 接入到项目里的人
- 想升级已有 Maglev 资产的人
- 想先预览更新影响，再决定是否执行的人

如果你还没有安装过 Maglev，请先看：

- [Maglev 快速开始](./maglev_distribution_quickstart.md)

---

## 3. 什么情况下可以更新

一个项目可以更新，通常意味着它已经完成过一次初始化，并且项目里已经有：

- `.agents/`
- `.maglev/`
- `.maglev/sync_state.json`

其中最关键的是：

- `.maglev/sync_state.json`

如果这个文件不存在，当前项目通常还不能正常进入更新流程。

---

## 4. 推荐怎么更新

### 第一步：先预览

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

这一步只会告诉你：

- 哪些文件准备新增
- 哪些文件准备更新
- 哪些文件可能和本地修改冲突
- `AGENTS.md` / `llms.txt` 是否已经和当前 Maglev 结构漂移
- 已登记的 submodule 仓库当前是否处于可见、可解释状态
- 是否会下发或更新 `scripts/maglev-python` 运行时入口

它不会真正改动你的项目文件。

### 第二步：确认后正式执行

```bash
npx @idea-maglev/maglev-cli update
```

这一步才会真正把更新写入项目。


### 第三步：验证 Maglev 协议运行时

更新完成后，建议执行：

```bash
./scripts/maglev-python --doctor
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
```

如果 doctor 返回 `env_failed`，先安装 `uv` 或 Python 3.11+ 后重试。doctor 通过后再处理 track 的 `partial` / `failed`。

---

## 5. 更新时你最需要关心什么

从使用者视角看，更新时最需要关心的是这些事：

### 1. 这次会不会改到我本地手动改过的文件

如果你改过 Maglev 自带文件，更新时可能会遇到冲突处理。

因此最稳妥的做法永远是先跑一次：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

### 2. 更新后有没有生成备份文件

如果本地修改和新版本发生冲突，Maglev 会保留你的本地版本备份。

你更新后可以搜索：

- `*.local_backup_<timestamp>`

如果看到了这类文件，说明更新过程中为你保留了本地修改副本。

### 3. 更新后同步状态有没有刷新

更新完成后，建议确认：

- `.maglev/sync_state.json` 仍然存在
- 同步时间和版本信息已经刷新

### 4. 更新后的运行时是否可用

如果这次更新包含 `scripts/maglev-python` 或 index-librarian 相关文件，建议执行 doctor 与 track verify。这样可以确认后续 `/standup` / `reality-sync` 不会因为 Python 版本或依赖缺失失败。

### 5. 如果你使用了 submodule，当前状态是否正常

如果你的项目在初始化时把某些代码仓库登记成了 `submodule` 模式，当前 update 会额外告诉你：

- 是否检测到已登记的 submodule 仓库
- 是否缺少 `.gitmodules`
- submodule 工作区目录是否存在
- 子仓库目录里是否检测到 `.git` 标记

当前这一步只做观察和解释，不会自动帮你同步 pointer。

---

## 6. 常见更新场景

### 场景 A：我只是想看看这次更新会改什么

执行：

```bash
npx @idea-maglev/maglev-cli update --dry-run
```

适合：

- 真实项目第一次升级前
- 你不确定本地是否改过 Maglev 文件
- 想先评估风险
- 想顺便确认 AI 上下文和 submodule 状态有没有漂移

### 场景 B：项目已经接入过，我想正常升级

执行：

```bash
npx @idea-maglev/maglev-cli update
```

适合：

- 已经确认项目可正常更新
- 刚做完一次 `--dry-run`
- 想把项目同步到当前版本

### 场景 C：我改过部分 Maglev 文件，但还是想升级

推荐顺序：

1. 先执行 `npx @idea-maglev/maglev-cli update --dry-run`
2. 观察是否有冲突提示
3. 再决定是否执行正式更新

### 场景 D：我习惯全局命令

执行：

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli update --dry-run
maglev-cli update
```

---

## 7. 更新后怎么确认成功

建议你至少检查下面 5 件事：

### 1. 命令执行没有报错退出

如果终端没有报错，并且命令正常结束，说明更新流程已经跑完。

### 2. 目标目录仍然存在

确认这些目录还在：

- `.agents/`
- `.maglev/`

### 3. 同步状态文件仍然存在并已刷新

确认下面这个文件还在：

- `.maglev/sync_state.json`

如果你愿意进一步检查，也可以打开这个文件，确认同步时间或版本信息已经变化。

### 4. 如果你本地改过文件，确认是否出现备份

如有冲突，检查是否出现：

- `*.local_backup_<timestamp>`

### 5. 如果你的项目用了 submodule，确认状态输出是否正常

如果当前项目登记了 `submodule` 模式仓库，更新输出里应能看到：

- `子仓库管理检查`

如果它提示：

- 缺少 `.gitmodules`
- 工作区缺失
- submodule 目录未初始化

说明当前还需要你手动处理仓库状态。

---

## 8. 什么时候不要急着正式更新

下面这些情况，建议先停在 `--dry-run`：

- 你不确定团队里有没有人改过 `.agents/` 或 `.maglev/` 下的文件
- 这个项目是正式业务仓库，不能接受误覆盖
- 你想先看看这次升级范围是否符合预期

对多数使用者来说，`--dry-run` 应该成为默认习惯。

---

## 9. 常见问题

### Q1：为什么我执行 `update` 提示缺少 `.maglev/sync_state.json`？

通常说明这个项目还没有完成过一次正常初始化，或者该文件被删除了。请先确认项目是否真的已经接入过 Maglev。

### Q2：`update --dry-run` 会不会改文件？

不会。它只做预览，不真正写入文件。

但它会额外做两类检查：

- AI 上下文漂移检查
- 已登记 submodule 的状态观察

### Q3：如果我本地改过 Maglev 文件，会不会被直接覆盖？

正常情况下，Maglev 会尽量保留冲突备份，而不是静默吃掉你的修改。稳妥做法仍然是先执行 `--dry-run`。

### Q4：如果我的项目用了 submodule，`update` 会不会自动帮我同步？

当前不会。

现阶段 `update` 对 submodule 的职责是：

- 识别
- 解释
- 给建议

而不是自动执行 pointer 同步。

如果它提示 submodule 工作区需要初始化，你应手动执行：

```bash
git submodule update --init --recursive
```

### Q5：为什么我应该优先用 CLI，而不是直接研究底层实现？

因为对使用者来说，最重要的是“能不能安全完成更新”，而不是先理解内部同步算法。

---

## 10. 下一步看什么

如果你已经掌握基本更新方式，推荐继续看：

1. [Maglev 快速开始](./maglev_distribution_quickstart.md)
2. [Maglev 多入口使用说明](./maglev_entrypoints.md)

如果把这篇文档压缩成一句话，那就是：

> 已接入的项目先用 `update --dry-run` 预览，再执行 `update`，并在更新后检查 `.maglev/sync_state.json`、AI 上下文结果和子仓库管理状态。
