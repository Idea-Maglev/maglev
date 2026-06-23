# Maglev 初始化使用手册

> 目标：说明第一次把 Maglev 接入一个项目时，应该怎么执行 `init`，以及它会在本地做什么。

## 1. 什么叫“初始化”

在 Maglev 当前实现里，`init` 的含义是：

- 获取发行清单 `manifest.json`
- 将 Maglev 运行资产落到当前项目
- 创建基础目录骨架
- 采集项目最小配置
- 写入本地配置和同步状态

初始化完成后，这个项目就从“普通仓库”变成了“已接入 Maglev 的仓库”。

当前统一执行核心见：

- [maglev_installer.py](../../../packages/maglev-cli/runtime-src/maglev_installer.py)（源文件；`dist/` 下的是构建产物）

## 2. 初始化前要确认什么

建议在项目根目录执行初始化，并先确认：

- 当前目录是目标项目根目录
- 最好已经是 Git 仓库
- 系统中有可用的 `python3` 或 `python`，能运行 Maglev 安装器
- 建议安装 `uv`，用于后续受控 Python 协议运行时
- 如果走本地离线方式，发行物目录完整
- 如果走 npm / Npx 方式，目标包已经发布，且包内 `dist/` 完整

注意：

- 当前实现即使发现目录不是 Git 仓库，也只是警告，不会阻断初始化
- 但从使用习惯上，仍建议你在 Git 仓库根目录执行

## 3. 哪些方式可以执行 `init`

### 方式 A：直接调用统一执行核心

这是最直接、最便于验证的一种方式，更适合仓库维护者或本地测试：

```bash
python3 .maglev_build/maglev_installer.py init --local-dist /path/to/.maglev_build --skip-prompt
```

适合：

- 本地验证
- 离线初始化
- 精确观察初始化行为

### 方式 B：通过 npm / npx 包入口

```bash
npx @idea-maglev/maglev-cli init
```

适合：

- 使用 Node / npm 环境
- 想通过正式发布的 npm 包完成首装

如果你更习惯先安装再执行，也可以：

```bash
npm install -g @idea-maglev/maglev-cli
maglev-cli init
```

说明：

- 这里说的是“用户通过已发布的 npm 包使用”
- 不是在 Maglev 源仓库里直接执行 `node packages/maglev-cli/bin/index.js`

实现见：

- [index.js](../../../packages/maglev-cli/bin/index.js)

### 方式 C：关于 Shell / `curl`

当前不建议把 Shell / `curl` 方式作为正式用户初始化入口。

原因：

- 现有脚本后续依赖 GitLab 上游内容
- 对用户机器而言存在登录与权限门槛
- 在公开发行制品与 OSS / CDN 分发打通之前，这条链路更适合作为内部实现或测试能力，而不是面向用户的正式路径

如果你只是想真正把 Maglev 装到项目里，请优先使用 npm / npx 包入口。

## 4. 初始化时到底会发生什么

从用户视角看，`init` 大致会经历这几步：

1. 环境探测
2. 获取 `manifest.json`
3. 下载或拷贝发行资产
4. 创建骨架目录
5. 进行交互式项目配置
6. 写入同步状态
7. 安装后可通过 `scripts/maglev-python --doctor` 验证 Maglev 协议运行时

如果你使用的是 `--dry-run`，其中会涉及写文件的动作只会输出预览，不真正执行。

## 5. 初始化后项目里会生成什么

### 目录骨架

当前会确保这些目录存在：

```text
specs/00_vision/
specs/10_reality/
specs/20_evolution/active/
specs/90_archive/
docs/thinking/
docs/guides/
issues/active/
issues/closed/
tests/
.maglev/
```

说明：

- 即使某些目录原本不存在，初始化也会自动补齐
- 这些目录用于承载 Maglev 的规范、文档、任务和本地状态

### 运行资产

初始化还会把发行物中的资产同步到本地，例如：

- `.agents/`
- `.maglev/` 下的规则和配置
- `scripts/maglev-python` 受控 Python 运行时入口
- 其他在 `manifest.json` 中声明的下发文件

### 本地配置文件

初始化完成后，至少应看到：

- `.maglev/config.json`
- `.maglev/sync_state.json`

其中：

- `config.json`
  - 记录项目名称、描述、上游地址、仓库配置等
- `sync_state.json`
  - 记录当前版本、同步时间和文件基线哈希

### `.gitignore`

如果当前项目里还没有 `.gitignore`，初始化会自动创建一个最小版本。

当前至少会写入 Maglev 管理块，用于忽略本地备份、Python 缓存和运行时状态。你需要重点确认 `.maglev/runtime/` 不会进入 Git：

```gitignore
# Maglev local-only state
.maglev/temp/
.maglev/runtime/
```

## 6. 初始化时会问你什么

如果你没有使用 `--skip-prompt`，当前实现会进行一次交互式问答。

### 问题 1：项目名称

默认值：

- 当前目录名

用途：

- 写入 `.maglev/config.json`
- 可能出现在生成的 `repository_map.md` 中

### 问题 2：项目简述

用途：

- 写入 `.maglev/config.json`

### 问题 3：是否交互式注册子仓库

你可以选择：

- 交互式关联/注册子仓库
- 跳过

这一步的真实目的不是“强制你现在就做 Git 操作”，而是：

- 告诉 Maglev：当前项目实际会和哪些代码仓库一起协作
- 顺手生成一版初始 `repository_map.md`
- 记录这些仓库的来源、路径和管理方式

如果你现在跳过：

- 初始化仍然会成功完成
- 只是本次不会自动导入或登记任何 Git 仓库
- 后续需要你手动补仓库信息，或重新生成 `repository_map.md`

所以可以这样理解：

- 如果你已经知道当前工作台要接哪些仓库，现在登记最省事
- 如果你还没想清楚，先跳过也没问题，不会卡住初始化

如果你选择注册子仓库，当前实现还会继续问：

- 仓库接入模式
- 仓库 Git 地址
- 本地路径
- 仓库简述

### 当前支持的子仓库接入模式

初始化时，当前支持两种模式：

- `clone`
  - 适合最小接入
  - 直接把代码仓库拉到本地目录
- `submodule`
  - 适合多仓库可复现工作台
  - 由当前 Maglev 项目托管子仓库 revision

当前默认值是：

- `clone`

也就是说，如果你只是想快速把项目接起来，不需要额外理解 submodule 也可以继续使用默认模式。

### 如何判断现在要不要登记 Git 仓库

建议现在就登记：

- 你准备把某个代码仓库拉到当前项目目录下协作
- 你希望 Maglev 从一开始就知道这些仓库的路径和来源
- 你需要一份初始 `repository_map.md`

建议先跳过：

- 你现在只是先把 Maglev 骨架接进项目
- 你还没决定要接入哪些代码仓库
- 你当前目录本身已经就是唯一主仓，不需要再导入额外仓库

如果后面再补，你主要还需要做两件事：

- 把代码仓库按 `clone` 或 `submodule` 方式接进来
- 更新 `specs/10_reality/repository_map.md`

## 7. 初始化时可能附带做的事

### 生成 `repository_map.md`

如果 `specs/10_reality/` 目录存在，当前实现会尝试生成：

- `specs/10_reality/repository_map.md`

内容会包含：

- Project 名称
- 交互式登记过的仓库列表
- 每个仓库当前的管理方式（`clone` 或 `submodule`）

这意味着：

- 它不一定完全反映整个仓库现实
- 更像初始化时生成的一份基础资产地图

当前仓库主地图可参考：

- [repository_map.md](../../../specs/10_reality/repository_map.md)

### 接入外部仓库

如果你在问答中填写了仓库 Git 地址，初始化会按你选择的模式执行：

- `clone`：执行普通 clone
- `submodule`：执行 submodule add

当前实现对这些情况会给出提示：

- 目录已存在
- 权限拒绝
- 仓库未找到
- clone / submodule add 失败

但它不会因为单个仓库登记失败就整体中断初始化。

### 初始化后的 AI 上下文检查

初始化结束后，当前还会补做一轮 AI 上下文检查。

它会检查：

- `AGENTS.md` 是否存在
- `llms.txt` 是否存在
- 是否仍在使用旧 runtime name
- 是否足以帮助 AI 理解当前项目和 Maglev 入口

如果发现缺口，终端里会直接给出：

- 最小补齐建议
- `AGENTS.md` / `llms.txt` 的最小示例块


### 初始化后的运行时检查

初始化完成后，建议立即执行：

```bash
./scripts/maglev-python --doctor
```

这个命令会检查并准备 Maglev 协议脚本使用的项目本地 Python 运行时。它会优先使用 `uv`，也会在可用时使用系统 Python 3.11+ 兜底。

如果 doctor 通过，再执行：

```bash
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills
./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id specs
```

这两条命令通过后，说明 `/standup` / `reality-sync` 冷启动依赖的索引检查路径已经可用。

说明：`reality-sync` 启动时会自动先做 runtime preflight；手动执行 doctor 主要用于初始化后的验收、CI 或排障。

## 8. `--skip-prompt`、`--dry-run`、`--local-dist` 怎么用

### `--skip-prompt`

作用：

- 跳过所有交互式问题，使用默认配置

当前默认行为：

- `project_name` 使用当前目录名
- `project_description` 为空
- 不进入仓库注册流程

适合：

- 自动化验证
- 本地测试
- 你只想先把最小骨架装起来

### `--dry-run`

作用：

- 只预览初始化动作，不真正写文件

适合：

- 想先确认会下载哪些资产
- 想看会创建哪些目录
- 想看如果登记子仓库，会走 `clone` 还是 `submodule`
- 想验证参数链路是否正确

### `--local-dist`

作用：

- 从本地发行物目录读取 `manifest.json` 和资产，跳过网络

适合：

- 本地开发验证
- 离线初始化
- 验证新发行物是否可用

## 9. 什么时候 `init` 会变成 `update`

这是当前实现里一个非常重要的行为。

如果你执行的是：

```bash
... init
```

但当前目录里已经存在：

- `.maglev/sync_state.json`

那么安装器会自动输出提示，并把当前动作切换成 `update`。

这意味着：

- `init` 不是无条件强制初始化
- 它会根据本地状态识别项目是否已经接入过 Maglev

如果你本来想测首装，却发现行为像更新，先检查：

- 当前目录是否残留 `.maglev/sync_state.json`

## 10. 如何确认初始化成功

建议至少检查这几项：

1. 是否存在 `.maglev/config.json`
2. 是否存在 `.maglev/sync_state.json`
3. 是否生成了 `.agents/`
4. 是否生成了 `specs/`、`docs/`、`issues/`、`tests/`
5. 是否存在并可执行 `scripts/maglev-python`
6. `./scripts/maglev-python --doctor` 是否成功
7. `track_verify --track-id skills` 和 `track_verify --track-id specs` 是否返回 `ok`
8. 根目录是否没有出现：
   - `install.sh`
   - `maglev_installer.py`

第 8 点尤其重要，因为当前分发规则已经收口，这两个文件不应再作为目标项目根目录资产下发。

## 11. 常见初始化场景

### 场景 A：快速离线验证

建议：

```bash
python3 .maglev_build/maglev_installer.py init --local-dist /path/to/.maglev_build --skip-prompt
```

### 场景 B：先看一眼会做什么

建议：

```bash
python3 .maglev_build/maglev_installer.py init --local-dist /path/to/.maglev_build --dry-run --skip-prompt
```

### 场景 C：第一次正式接入一个项目

建议：

1. 在 Git 仓库根目录执行
2. 优先使用 npm / Npx 包完成安装
3. 初始化成功后检查 `.maglev/config.json`、`.maglev/sync_state.json` 和 `scripts/maglev-python`
4. 执行 `./scripts/maglev-python --doctor` 与两个 `track_verify` 验证命令
5. 然后再开始用 `/standup` 等安装后交互入口

## 12. 当前已知限制

这份手册优先描述“当前真实实现”，你还需要知道：

- AI workflow / skill 不应被理解为首装入口
- 当前 `repository_map.md` 的生成逻辑比较轻量
- 初始化时的仓库 clone 只是辅助能力，不是分发主链路本身
- `init` / `update` 的安装器启动仍依赖本机 Python；Maglev 协议脚本运行时由 `scripts/maglev-python` 托管

## 13. 继续阅读

建议继续看：

1. [Maglev 快速开始](./maglev_distribution_quickstart.md)
2. [Maglev 更新与同步手册](./maglev_update_manual.md)
3. [Maglev 多入口使用说明](./maglev_entrypoints.md)
4. [分发技术设计](../../../specs/20_evolution/active/maglev_distribution/02_design_backend.md)
