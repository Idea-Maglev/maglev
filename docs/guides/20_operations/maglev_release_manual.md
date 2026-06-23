# Maglev 发布说明与维护手册

> 目标：说明维护者如何从源仓库构建新的发行物、生成 changelog，并把结果发布给用户使用。

如果你想看从“日常开发 -> 统一改版本 -> 校验 -> dry-run -> 正式发布”的完整主路径，建议先读：

- [Maglev 开发与发布流程](./maglev_development_release_workflow.md)

如果你想验证“删掉构建产物后如何从零重建，并手动测试用户 update”，建议再读：

- [Maglev 重建与更新联调手册](./maglev_rebuild_and_update_e2e_manual.md)

## 1. 这篇文档是给谁看的

这篇手册面向：

- Maglev 的维护者
- 负责构建发行物的人
- 需要验证 release / changelog / npm 包镜像是否一致的人

它不是用户安装手册，而是维护者侧的发版操作说明。

## 2. 当前发布链路的核心对象

当前发布相关的核心文件有：

- 发布编译器：
  - [maglev_release.py](../../../scripts/maglev_release.py)
- CLI 执行核心真相源：
  - [maglev_installer.py](../../../packages/maglev-cli/runtime-src/maglev_installer.py)
  - [install.sh](../../../packages/maglev-cli/runtime-src/install.sh)
- changelog 工作流：
  - [generate-changelog.md](../../../.agents/workflows/generate-changelog.md)
- changelog 生成 skill：
  - [SKILL.md](../../../.agents/skills/maglev-changelog-generator/SKILL.md)

发布完成后会涉及这些产物：

- `.maglev_build/`
- `.maglev_build/CHANGELOG_DRAFT.md`
- `.maglev_build/CHANGELOG.md`
- `.maglev_build/manifest.json`
- `packages/maglev-cli/dist/`
- `docs/releases/<version>.md`

## 3. 当前发布链路到底做什么

当前 `maglev_release.py` 负责：

1. 预发布审计
2. 识别哪些 skill / workflow 可进入公开发行物
3. 在 `.maglev_build/` 里组装发行沙箱
4. 生成 `CHANGELOG_DRAFT.md`
5. 计算哈希并生成 `manifest.json`
6. 同步一份镜像到 `packages/maglev-cli/dist/`
7. 在非 dry-run 模式下推送到远端 `release` 分支

这意味着：

- `.maglev_build/` 是这次发布的真实构建输出目录
- 它不是长期源码目录，而是一次发版的打包沙箱
- `packages/maglev-cli/runtime-src/` 是 installer 与 shell 入口的受控真相源
- `packages/maglev-cli/dist/` 只是 npm 包内镜像，不应再被当作源码维护

## 4. `.maglev_build/` 是什么

当前实现不会直接在 `dist/` 里原地拼装发行物，而是先在：

- `.maglev_build/`

里构建一份干净的发行沙箱。

这样做的目的有两个：

1. 避免污染源码工作区
2. 让 manifest、changelog 和发布快照都围绕同一份构建结果生成

在 dry-run 模式下，这个目录就是你验证 release 是否正确的核心观察点。

## 5. 发布前建议先做什么

### 1. 先确认这次到底要发什么

在发版前先确认：

- 哪些改动是本次要进发行物的
- 哪些只是仓库级文档或 marketing 信息

特别注意：

- changelog 可以记录 marketing 相关变化
- 但这不代表 marketing 文件本身应该进入 runtime 产物

### 2. 先做质量校验

当前脚本默认要求你先完成一次审计。

脚本会提示你在 AI 助手里执行：

- `/validate-all`

然后再回到 release 编译器确认继续。

### 3. 先统一版本事实

当前不要手工分别修改 `release.version.json`、`package.json`、`manifest.json` 或 changelog 标题。

推荐先执行：

```bash
python3 scripts/maglev_version.py set 0.1.4
python3 scripts/maglev_version.py check
```

当前 `maglev_release.py` 在启动时也会自动执行一次：

```bash
python3 scripts/maglev_version.py check
```

如果版本事实漂移，release 会直接失败。

### 4. 注意 Git 工作区状态

当前脚本在非 `--dry-run` 模式下会检查：

- `git status --porcelain`

如果工作区不干净，会中断正式发布。

原因是：

- 避免未提交内容在发版流转里丢失

## 6. 最推荐的发布顺序

建议按这个顺序执行：

1. 先做本地 dry-run
2. 检查 `.maglev_build/`
3. 生成并确认 changelog
4. 检查 `manifest.json`
5. 检查 `packages/maglev-cli/dist/` 是否已同步
6. 最后再做正式发布

这是当前最稳的工作方式。

## 7. 如何执行 dry-run

推荐命令：

```bash
python3 scripts/maglev_release.py --dry-run --skip-audit
```

适合：

- 本地验证
- 先看这次发布产物会长什么样
- 在不推送远端的前提下验证更新链路

参数说明：

- `--version`
  - 可选显式版本号；如传入，必须与 `release.version.json` 一致
- `--dry-run`
  - 只构建，不推送
- `--skip-audit`
  - 跳过脚本中的发布前审计等待

注意：

- `--skip-audit` 更适合本地验证，不建议默认用于正式发布
- 如果你不传 `--version`，脚本会默认读取 `release.version.json`

## 8. dry-run 之后要检查什么

### 1. 检查 `.maglev_build/` 是否生成成功

重点看：

- `.maglev_build/.agents/`
- `.maglev_build/.maglev/`
- `.maglev_build/CHANGELOG_DRAFT.md`
- `.maglev_build/manifest.json`

### 2. 检查新的变更是否真的进了发行物

例如你刚刚改的是：

- `现状同步（reality-sync）`

那就应检查：

- `.maglev_build/.agents/skills/reality-sync/`
- `.maglev_build/.agents/workflows/standup.md`

### 3. 检查真正会发给用户的内容

当前收口后，下游项目根目录不应再收到：

- `install.sh`
- `maglev_installer.py`

因此你应确认：

- `.maglev_build/manifest.json` 中不应再把它们列为下游项目资产

但同时你也应确认：

- `packages/maglev-cli/dist/` 中仍保留这两个文件

因为 npm 包入口仍然依赖它们。

## 9. CHANGELOG 是怎么生成的

当前 changelog 流程分两步。

### 第一步：release 编译器生成草案

`maglev_release.py` 会先生成：

- `.maglev_build/CHANGELOG_DRAFT.md`

这是一份面向 AI 的中间草案，不是最终给用户看的版本。

### 第二步：AI 工作流生成最终 changelog

然后你在 AI 助手里执行：

- `/generate-changelog`

当前工作流见：

- [generate-changelog.md](../../../.agents/workflows/generate-changelog.md)

对应 skill 见：

- [SKILL.md](../../../.agents/skills/maglev-changelog-generator/SKILL.md)

当前目标产物是：

- `.maglev_build/CHANGELOG.md`
- `docs/releases/<version>.md`

其中：

- `.maglev_build/CHANGELOG.md` 是本次构建使用的发行说明
- `docs/releases/<version>.md` 是长期归档的版本说明

## 10. 关于 changelog 和 marketing 的边界

这里有一个已经明确的规则：

- changelog 可以带 marketing 信息
- 但 marketing 内容不要进入真正发给用户项目的运行资产中

更准确地说：

- changelog 可以记录仓库层面的重要变化、定位变化、对外叙事
- 但真正发给用户项目的内容，仍然只应包含运行所需资产

所以发版时要同时看两件事：

1. `CHANGELOG.md` 是否完整表达了本次变化
2. `manifest.json` 是否只列出了应下发的运行资产

## 11. 为什么还要同步 `packages/maglev-cli/dist/`

当前发布脚本会在生成 `.maglev_build/` 后，把这份构建结果同步到：

- `packages/maglev-cli/dist/`

原因是：

- `maglev-cli` 的 npm / npx 入口要依赖包内镜像
- 它需要随包携带一份离线可执行的发行资产

当前还有一个重要边界：

- 下游项目根目录不应收到 `install.sh` / `maglev_installer.py`
- 但 `packages/maglev-cli/dist/` 仍需要保留这两个文件

这是当前多入口结构中的一个刻意保留。

## 12. 什么时候执行正式发布

只有在下面这些检查都通过后，才建议执行正式发布：

- dry-run 输出符合预期
- `.maglev_build/` 内容完整
- `CHANGELOG.md` 已生成并确认
- `manifest.json` 正确
- `packages/maglev-cli/dist/` 已同步

正式命令：

```bash
python3 scripts/maglev_release.py
```

如果你确实需要显式做版本一致性校验，也可以使用：

```bash
python3 scripts/maglev_release.py --version 0.1.4
```

正式发布时，脚本会：

- 在 `.maglev_build/` 里初始化一个独立 Git 仓库
- 构建发布快照
- 强推到远端 `release` 分支

## 13. 当前实现里需要特别注意的现实

这部分很重要，这篇手册优先描述“当前真实实现”，所以需要把几个现实写清楚。

### 1. `.maglev_build/` 和 `packages/maglev-cli/dist/` 的职责仍然容易混淆

当前仓库里：

- `.maglev_build/` 是 release 编译时的真实构建沙箱
- `packages/maglev-cli/dist/` 是 npm 包发布时随包携带的镜像

在本地验证时，不要把两者混为一谈。

### 2. changelog 工作流中的路径描述还有历史痕迹

当前 workflow / skill 文案中如果还残留旧路径描述，应视为历史痕迹，而不是当前实现事实。

但当前 release 编译器实际等待的是：

- `.maglev_build/CHANGELOG.md`

如果两边不一致，以当前脚本真实行为为准。

### 3. marketing 信息可以进 changelog，但不应污染发行资产

这条边界已经明确，后续发布时要持续检查：

- changelog 的叙事内容
- manifest 的运行资产边界

## 14. 一次发布前的最小检查清单

至少确认这几项：

1. 本次版本号是否正确
2. `.maglev_build/CHANGELOG.md` 是否存在
3. `.maglev_build/manifest.json` 是否存在
4. 关键变更文件是否已进入 `.maglev_build/`
5. `packages/maglev-cli/dist/` 是否已同步
6. 下游根目录不应下发的文件是否未进入 manifest

## 15. 继续阅读

建议继续看：

1. [Maglev 快速开始](./maglev_distribution_quickstart.md)
2. [Maglev 更新与同步手册](./maglev_update_manual.md)
3. [Maglev 分发排障手册](./maglev_distribution_troubleshooting.md)
4. [分发技术设计](../../../specs/20_evolution/active/maglev_distribution/02_design_backend.md)
5. [文档补全任务清单](../../../issues/closed/task_distribution_docs_backfill.md)
