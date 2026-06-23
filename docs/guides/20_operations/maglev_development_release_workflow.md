# Maglev 开发与发布流程

> 目标：给 Maglev 维护者一份从日常开发、版本变更、回归校验到正式发布的统一操作路径，避免把版本管理、发行构建和人工判断拆成多套零散动作。

## 1. 这篇文档适合谁

这篇文档面向：

- 维护 Maglev 源仓库的人
- 需要修改 skill、workflow、分发链路或发布资产的人
- 需要把一次开发变更安全推进到 release 的人

如果你只是想使用已经发布的 Maglev，请优先看：

- [Maglev 快速开始](./maglev_distribution_quickstart.md)
- [Maglev 初始化使用手册](./maglev_init_manual.md)
- [Maglev 更新与同步手册](./maglev_update_manual.md)

如果你想从零重建发行物并手动演练一次用户更新，可以继续看：

- [Maglev 重建与更新联调手册](./maglev_rebuild_and_update_e2e_manual.md)

## 2. 当前有哪些文档，分别解决什么问题

在这篇文档之前，仓库里已经有几份相关手册：

- [Maglev 发布说明与维护手册](./maglev_release_manual.md)
  - 重点解释 release 构建本身怎么执行。
- [Maglev 更新与同步手册](./maglev_update_manual.md)
  - 面向已经接入 Maglev 的使用者，解释怎么 update。
- [Maglev 初始化使用手册](./maglev_init_manual.md)
  - 面向使用者，解释怎么 init。
- [协作协议](./collaboration_playbook.md)
  - 解释团队协作和 Review 的基本约定。

它们各自有价值，但还缺一条维护者视角的主路径：

1. 我改完代码后先做什么
2. 我怎么统一改版本
3. 我怎么验证版本事实没有漂移
4. 我怎么做 dry-run release
5. 我什么时候可以正式发布

这篇文档就是用来补这条主路径的。

## 3. 维护者最常用的 4 个入口

当前维护 Maglev 时，最常用的是下面 4 个入口：

1. 开发与修改源码
   - 直接在仓库里修改 `scripts/`、`.agents/`、`packages/maglev-cli/` 等资产
2. 统一版本管理
   - `python3 scripts/maglev_version.py ...`
3. 发行构建
   - `python3 scripts/maglev_release.py ...`
4. 本地回归验证
   - `python3 -m unittest tests.test_maglev_version`

如果你想减少手工拼命令的成本，也可以直接使用：

- `python3 scripts/maglev_smoke_test.py`
- `python3 scripts/maglev_e2e_check.py`

## 4. 一次完整开发的推荐顺序

推荐始终按下面顺序做：

1. 先改源码或文档
2. 跑最小回归，确认本地改动没有破坏关键链路
3. 如果本次需要变更版本，用统一版本脚本执行
4. 再跑一次版本一致性检查
5. 做 release dry-run
6. 检查构建产物
7. 确认 changelog
8. 最后再做正式发布

这条顺序的核心目标是：

- 先验证功能
- 再固化版本
- 最后生成发行物

而不是一上来手工改版本或直接推发布。

## 5. 日常开发阶段怎么做

### 5.1 修改代码或资产

当前维护动作通常发生在这些目录：

- `.agents/skills/`
- `.agents/workflows/`
- `scripts/`
- `packages/maglev-cli/`
- `docs/guides/20_operations/`

常见修改类型包括：

- 新增或调整 skill / workflow
- 修改分发与更新逻辑
- 调整版本治理脚本
- 修正维护者手册或排障说明

### 5.2 先做本地最小验证

如果你的改动涉及版本治理，至少先执行：

```bash
python3 -m unittest tests.test_maglev_version
python3 scripts/maglev_version.py check
```

如果你改的是 CLI 包装层，也建议执行：

```bash
node packages/maglev-cli/bin/index.js version
```

这一步的目标不是证明“所有东西都没问题”，而是尽早发现：

- 版本脚本坏了
- 版本事实已经漂移
- CLI 展示的版本和发行物版本不一致

## 6. 如何统一修改版本

当前不要手工分别修改：

- `release.version.json`
- `packages/maglev-cli/package.json`
- `packages/maglev-cli/dist/manifest.json`
- `.maglev_build/manifest.json`
- `CHANGELOG` 标题

这些版本事实统一由下面这个脚本管理：

- [`scripts/maglev_version.py`](../../../scripts/maglev_version.py)

### 6.1 查看当前版本状态

```bash
python3 scripts/maglev_version.py show
```

### 6.2 检查当前版本是否一致

```bash
python3 scripts/maglev_version.py check
```

### 6.3 将版本同步到目标版本

```bash
python3 scripts/maglev_version.py set 0.1.4
```

当前脚本会统一处理：

- 统一版本源
- 包内 manifest
- 构建目录 manifest
- 当前 changelog 标题中的版本号

### 6.4 当前版本管理的边界

这个脚本当前解决的是“开发态与构建态版本事实一致性”，不是完整替代 release 构建。

更准确地说：

- 它负责统一管理版本号
- 它不负责重新计算 manifest 哈希
- 它不负责重新生成完整发行物

所以正确顺序仍然是：

1. `set`
2. `check`
3. `release --dry-run`

## 7. 发布前必须做的检查

在执行 release 之前，至少做这几件事：

### 7.1 版本一致性检查

```bash
python3 scripts/maglev_version.py check
```

当前 `maglev_release.py` 在启动时也会自动调用这个检查。

这意味着如果版本事实漂移，release 会直接失败，而不是带着错误版本继续构建。

### 7.2 最小自动化回归

```bash
python3 -m unittest tests.test_maglev_version
```

### 7.3 Git 工作区检查

正式发布前，确认：

```bash
git status --short
```

当前 release 脚本在非 `--dry-run` 模式下会检查工作区是否干净。

## 8. 如何做 release dry-run

推荐命令：

```bash
python3 scripts/maglev_release.py --dry-run --skip-audit
```

如果你只是本地验证，不一定需要显式传 `--version`，因为脚本会默认读取：

- `release.version.json`

如果你传了 `--version`，它必须和统一版本源一致，否则会直接失败。

### 8.1 dry-run 后重点看什么

重点检查：

- `.maglev_build/manifest.json`
- `.maglev_build/CHANGELOG_DRAFT.md`
- `.maglev_build/CHANGELOG.md`
- `packages/maglev-cli/dist/`
- `docs/releases/<version>.md`

同时确认：

- 包内镜像和构建产物版本一致
- 真正发给用户项目的运行资产没有越界
- 当前版本说明已经归档到 `docs/releases/`

## 9. 如何正式发布

当下面这些条件都满足后，再执行正式发布：

- 功能改动已验证
- `maglev_version.py check` 通过
- 最小回归通过
- dry-run 产物检查通过
- changelog 已确认

正式命令：

```bash
python3 scripts/maglev_release.py
```

如果你确实需要显式校验版本，也可以使用：

```bash
python3 scripts/maglev_release.py --version 0.1.4
```

### 9.1 正式发布完成后：打版本 Git Tag

`maglev_release.py` 执行完成后，还有一个重要的最后一步：**为当前 commit 打上正式的 Git tag**。

这个 tag 是版本治理的硬约束，用于：

- 标记正式发布时刻的源代码状态
- 建立版本号与 commit 的对应关系
- 方便追溯历史版本

#### Tag 格式约定

- **格式**：`v<major>.<minor>.<patch>`
  - 示例：`v0.2.0`、`v1.0.0`
- **必须带 `v` 前缀**，不要打 `0.2.0` 这样的无前缀 tag
- 标签指向发布时的 commit（即执行 `maglev_release.py` 后的 HEAD）

#### 打 Tag 的标准命令

在正式 release 完成后，立即执行：

```bash
git tag v0.2.0
```

如果需要推送到远端：

```bash
git push origin v0.2.0
```

#### 验证 Tag

打完 tag 后验证一下：

```bash
git tag -l | grep v0.2
git show-ref refs/tags/v0.2.0
```

#### 注意事项

- 不要手工改 tag 后再 push；如果标签错了，应删除后重新打：
  ```bash
  git tag -d v0.2.0
  git tag v0.2.0
  ```
- tag 应该和 `release.version.json` 中的版本号保持一致
- 打 tag 应在确认 release 构建完全成功后再进行

## 10. 推荐的最小维护命令清单

如果你只想记住最小命令集，记下面这些就够了：

```bash
# 1. 看当前版本状态
python3 scripts/maglev_version.py show

# 2. 统一改版本
python3 scripts/maglev_version.py set 0.1.4

# 3. 校验版本一致性
python3 scripts/maglev_version.py check

# 4. 跑最小回归
python3 -m unittest tests.test_maglev_version

# 5. 验证 CLI 看到的版本
node packages/maglev-cli/bin/index.js version

# 6. 做本地发行 dry-run
python3 scripts/maglev_release.py --dry-run --skip-audit

# 7. 执行正式发布
python3 scripts/maglev_release.py

# 8. 发布完成后打版本 tag
git tag v0.1.4
```

## 11. 当前这条流程解决了什么问题

和之前相比，当前流程至少解决了这几个问题：

- 不再依赖人工记忆去找所有版本文件
- 新会话不需要重新猜“版本到底改哪几处”
- release 前能自动识别版本漂移
- 版本管理已经有最小自动化回归保护 
- 明确定义了 Git tag 格式与打标时机，避免版本号和源码 commit 的关联丢失
## 12. 仍然要注意的限制

当前流程仍有这些边界：

- `maglev_version.py` 不是完整 release 编译器
- 它不会替你重新生成完整发行物哈希
- 版本变更、校验、发布这些动作应串行执行，不要并行跑

## 13. 多版本 changelog 当前如何维护

当前采用按版本归档文件的方式维护发行说明：

- 构建态文件：`.maglev_build/CHANGELOG.md`
- 长期归档目录：`docs/releases/`

也就是说：

- `.maglev_build/CHANGELOG.md` 只服务于本次 release 流程
- `docs/releases/<version>.md` 才是受 Git 管控的长期历史记录

当前索引见：

- [发布记录索引](../../releases/index.md)

如果后续要继续增强，优先方向通常是：

1. 给版本脚本补更多回归测试
2. 把这条链路接进正式 CI
3. 进一步收口 release 产物与 npm 包镜像的自动同步验证
