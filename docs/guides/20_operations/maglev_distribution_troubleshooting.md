# Maglev 分发排障手册

> 目标：当初始化、更新、入口调用或发行物验证出现问题时，快速判断问题落在哪一层，并给出可执行的排查路径。

## 1. 先别急着看日志，先判断卡在哪一层

当前可以先粗略分成 4 层：

1. **入口层**
   - Shell：`packages/maglev-cli/dist/install.sh`
   - npm / npx 包：`packages/maglev-cli/bin/index.js`
2. **真正干活的安装器**
   - `.maglev_build/maglev_installer.py` 或 `packages/maglev-cli/dist/maglev_installer.py`（构建产物；源文件在 `packages/maglev-cli/runtime-src/`）
3. **发行物**
   - `manifest.json`
   - `CHANGELOG.md`
   - `.maglev_build/` 或 `packages/maglev-cli/dist/` 中的下发资产
4. **本地状态**
   - `.maglev/config.json`
   - `.maglev/sync_state.json`

排障时建议先问自己：

- 是入口根本没跑起来
- 还是安装器跑起来了，但判断成了错误模式
- 还是文件下发了，但内容不对
- 还是状态文件不对，导致后续行为异常

## 2. 最常见的问题

### 问题 1：执行 `update` 时提示“未找到本地同步状态”

常见现象：

- 输出类似：
  - `未找到本地同步状态，无法执行 Update。请先执行 Init。`

原因：

- 当前目录里没有 `.maglev/sync_state.json`
- 当前项目还没有真正完成过 Maglev 初始化

怎么检查：

```bash
ls .maglev
```

重点看：

- 是否存在 `.maglev/sync_state.json`

怎么处理：

- 如果这是一个新项目，先执行 `init`
- 如果你本来以为它已经初始化过，检查是不是在错误目录下执行
- 如果 `.maglev/` 被误删，需要重新初始化或恢复状态文件

## 3. 问题 2：执行 `init` 时却自动进入了 `update`

常见现象：

- 你输入的是 `init`
- 但输出提示：
  - `检测到已存在 .maglev/sync_state.json。将自动切换为 Update 模式。`

原因：

- 当前目录已经存在 `.maglev/sync_state.json`
- 安装器因此把它识别为一个已接入 Maglev 的项目

怎么检查：

```bash
ls .maglev
cat .maglev/sync_state.json
```

怎么处理：

- 如果你本来想验证首装，请在一个全新目录中测试
- 如果这是历史测试残留，先确认是否需要清理该目录再重试
- 不要忽略这个提示，否则你会误以为初始化链路有问题

## 4. 问题 3：提示未找到 Python 或 `env_failed`

### 入口安装器找不到 Python

常见现象：

- Shell 或 npm / npx 包入口报错：
  - `未找到 Python。请安装 Python 3.6+ 后重试。`

原因：

- 当前环境既没有 `python3`
- 也没有可用的 `python`

怎么检查：

```bash
python3 --version
python --version
```

怎么处理：

- 安装 Python 3
- 确保 `python3` 或 `python` 在当前 PATH 中可用

说明：

- Shell 和 npm / npx 包入口最终都依赖 Python 执行统一安装器
- 所以即使你走的是 Node 入口，也仍然需要 Python 启动安装器

### Maglev 协议运行时 `env_failed`

常见现象：

- `/standup`、`reality-sync` 或索引检查提示 `env_failed`
- `track failed` 之前先出现 Python 版本、依赖或 `uv` 相关错误

原因：

- 安装器已经能运行，但 Maglev 协议脚本需要的受控 Python 运行时还没有准备好
- 当前机器缺少 `uv`，且没有可用的 Python 3.11+
- 依赖安装失败，或非交互 shell 找不到用户目录里的 `uv`

怎么检查：

```bash
./scripts/maglev-python --doctor
```

怎么处理：

- 优先安装 `uv`，然后重新执行 doctor
- 或安装 Python 3.11+，让 wrapper 使用系统 Python 兜底
- doctor 通过后，再执行对应的 `track_verify`

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
```

说明：

- `env_failed` 表示环境不可用，不表示索引内容坏了
- doctor 通过后，`partial` / `failed` 才表示 track 自身需要修复

## 5. 问题 4：Shell 入口无法下载安装器

常见现象：

- 输出类似：
  - `无法从远端下载安装器。请检查网络或 MAGLEV_UPSTREAM_URL 环境变量。`

原因：

- 当前网络无法访问上游地址
- `MAGLEV_UPSTREAM_URL` 配置错误
- 远端发布目录不完整

怎么检查：

```bash
echo $MAGLEV_UPSTREAM_URL
```

以及确认远端目标是否包含：

- `maglev_installer.py`
- `manifest.json`

怎么处理：

- 优先改用 `--local-dist` 做本地离线验证
- 如果必须走远端，检查上游发布地址是否正确
- 确认当前 release 产物已经生成完整

当前入口实现见：

- [install.sh](../../../packages/maglev-cli/dist/install.sh)

## 6. 问题 5：npm / npx 包提示包内离线安装器缺失

常见现象：

- 输出类似：
  - `离线安装器在包体中缺失`

原因：

- `packages/maglev-cli/dist/` 不完整
- 包内镜像没有和最新发行物同步
- 你打包/测试的并不是最新本地镜像

怎么检查：

确认这些文件是否存在：

- `packages/maglev-cli/dist/maglev_installer.py`
- `packages/maglev-cli/dist/manifest.json`
- `packages/maglev-cli/dist/.agents/`

怎么处理：

- 重新构建发行物并同步包内镜像
- 在发布前先做一次本地打包验证

当前入口实现见：

- [index.js](../../../packages/maglev-cli/bin/index.js)

## 7. 问题 6：本地离线源缺文件或 manifest 解析失败

常见现象：

- 输出类似：
  - `本地清单解析失败`
  - `本地离线源文件缺失`

原因：

- `--local-dist` 指向的目录不是完整发行物
- `manifest.json` 非法或损坏
- 发行目录里声明了文件，但源文件并不存在

怎么检查：

至少确认目录中存在：

- `manifest.json`
- `.agents/`
- `.maglev/`
- 其他被 manifest 声明的资产

怎么处理：

- 不要直接把任意目录当作 `--local-dist`
- 优先使用由 release 构建生成的发行物目录
- 如果你是手工改过 `manifest.json`，重新校验文件列表和哈希

## 8. 问题 7：出现 Hash 校验失败

常见现象：

- 输出类似：
  - `Hash 校验失败: <path>`

原因：

- 实际文件内容和 `manifest.json` 中声明的 SHA-256 不一致
- 发行物被手工修改过，但 manifest 没更新
- 构建产物与镜像不同步

怎么检查：

- 确认问题文件是否是最新构建产物
- 确认 `manifest.json` 是否来自同一套发行物

怎么处理：

- 重新构建发行物
- 重新生成 manifest
- 不要手工修改发行目录中的已登记资产

说明：

- 当前实现遇到单文件哈希失败时，会警告并继续处理其他文件
- 所以你还需要额外确认最终下发结果是否完整

## 9. 问题 8：更新后根目录仍然出现 `install.sh` 或 `maglev_installer.py`

常见现象：

- 初始化或更新后，目标项目根目录里仍看到：
  - `install.sh`
  - `maglev_installer.py`

原因：

- 你使用的发行物还不是最新规则下构建的
- `manifest.json` 仍把这两个文件视为下游项目资产
- `packages/maglev-cli/dist/` 或本地 `.maglev_build/` 没有同步到最新状态

怎么检查：

重点看：

- `.maglev_build/manifest.json`
- `packages/maglev-cli/dist/manifest.json`

确认其中是否还包含：

- `install.sh`
- `maglev_installer.py`

怎么处理：

- 使用最新构建的发行物重新初始化或更新
- 确认 release 构建逻辑已经把这两个文件从下游项目资产中移除

## 10. 问题 9：更新后某个文件没有变化，怀疑更新没生效

常见原因有三种：

1. 远端文件其实没有变化，进入了 `SKIP`
2. 你看的不是受 manifest 管理的文件
3. 你用的发行物版本和本地版本其实相同

怎么检查：

先看：

```bash
cat .maglev/sync_state.json
```

重点检查：

- `last_synced_version`
- `last_synced_time`

再确认目标文件是否在：

- `manifest.json`

如果要验证更新行为，建议直接修改一个确定被纳管的文件，例如：

- `.agents/workflows/standup.md`
- `.agents/skills/reality-sync/SKILL.md`

## 11. 问题 10：更新后出现了 `.local_backup_*`

这通常不是错误，而是保护机制生效。

含义：

- 远端版本变了
- 你本地也改过这个文件
- 更新器为了不吃掉本地修改，先做了备份

怎么处理：

- 比较原文件和备份文件差异
- 决定是否需要把本地修改重新合并到新版中

如果你本来就想直接强制覆盖，可以在确认风险后改用：

```bash
... update --force
```

## 12. 一条最实用的排障顺序

当你不确定问题在哪时，建议按这个顺序排：

1. 先确认当前是在对的目录里
2. 确认有没有 `.maglev/sync_state.json`
3. 确认入口本身能不能跑起来
4. 执行 `./scripts/maglev-python --doctor`，确认协议运行时可用
5. 执行 `track_verify --track-id skills` 和 `track_verify --track-id specs`
6. 再直接调用安装器做一次 `--dry-run`
7. 最后再检查发行物和镜像是否一致

推荐的最小验证命令：

```bash
./scripts/maglev-python --doctor
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
python3 .maglev_build/maglev_installer.py update --local-dist /path/to/.maglev_build --dry-run
```

它们最适合拿来回答这几个问题：

- Maglev 协议运行时是否可用
- 冷启动索引检查是否可用
- 当前目录会被识别为 `init` 还是 `update`
- 发行物是否可读
- 这次更新会发生什么

## 13. 什么时候该怀疑是文档问题，不是你操作有误

如果你遇到的是下面这些情况，往往不是你“不会用”，而是当前体系还在补文档和交互层：

- 入口边界不够清楚
- AI workflow 看起来像能做首装，但实际没有上下文支撑
- 文档里描述了理想行为，但本地发行物没同步到对应实现

这类情况建议回看：

1. [Maglev 快速开始](./maglev_distribution_quickstart.md)
2. [Maglev 初始化使用手册](./maglev_init_manual.md)
3. [Maglev 更新与同步手册](./maglev_update_manual.md)
4. [Maglev 多入口使用说明](./maglev_entrypoints.md)

## 14. 继续阅读

如果你想进一步理解背后的实现和测试边界，建议继续看：

1. [分发技术设计](../../../specs/20_evolution/active/maglev_distribution/02_design_backend.md)
2. [分发测试计划](../../../docs/thinking/60_case/distribution_test_plan_2026_03_16.md)
3. [文档补全任务清单](../../../issues/closed/task_distribution_docs_backfill.md)
