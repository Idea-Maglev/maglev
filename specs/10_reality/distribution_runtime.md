# Distribution Runtime Reality

> **Updated**: 2026-06-01
> **Scope**: 描述 Maglev 当前分发、安装、更新链路的真实现状。

## 1. 当前主路径

- 用户安装主路径：`npm / npx`
- 用户更新主路径：`npm / npx` 调用统一执行核心
- 当前不再作为正式对外主路径：`curl | bash`

对应用户文档：

- [Maglev 快速开始](../../docs/guides/20_operations/maglev_distribution_quickstart.md)
- [Maglev 更新与同步手册](../../docs/guides/20_operations/maglev_update_manual.md)
- [Maglev 多入口使用说明](../../docs/guides/20_operations/maglev_entrypoints.md)

## 2. 当前执行分层

### 2.1 执行核心

- `maglev_installer.py`
  - 当前唯一的安装 / 更新 / 同步执行核心
  - 它存在于发行物目录与 npm 包内镜像中
  - 它不再作为下游项目根目录文件存在
  - 提供 submodule pointer 同步能力：当下游仓库存在 git submodule 且 HEAD 偏离父仓库 recorded SHA 时，能在 init / `--sync-submodules` 路径下将其拉回 recorded 版本，避免下游使用错误的 submodule 内容

### 2.2 用户入口包装层

- [packages/maglev-cli/package.json](../../packages/maglev-cli/package.json)
- [packages/maglev-cli/bin/index.js](../../packages/maglev-cli/bin/index.js)
  - 当前正式对外的 npm / npx 用户入口
  - 支持 `version --json` 子命令，输出结构化 JSON（含 `cli_version`, `bundled_version`, `node_version`, `platform`）

### 2.3 上游构建层

- [scripts/maglev_release.py](../../scripts/maglev_release.py)
  - 当前发行物构建器，负责生成 manifest 并同步包内镜像
  - 校验 `private-catalog.yaml` 的 `distribution_scope` 合法性，生成仅含 `user_visible` 条目的 dist 版 catalog
- [scripts/check_runtime_distribution.py](../../scripts/check_runtime_distribution.py)
  - 独立 CI 校验脚本，确保 `runtime_internal` 资产在源仓库与 dist 中边界正确

## 3. 当前运行时结构

### 3.1 正式运行目录

当前 Skills / Workflows 的正式运行时目录是：

- `.agents/`

这已经取代旧的：

- `.agent/`

### 3.2 状态与配置目录

- `.maglev/`
  - 关键状态文件：`.maglev/config.json`、`.maglev/sync_state.json`

### 3.3 发行镜像层

当前有两层相关产物：

1. `.maglev_build/`
   - release dry-run / build 沙箱
2. `packages/maglev-cli/dist/`
   - npm 包内镜像

当前两者都已对齐到：

- `.agents/`
- `.maglev/`
- `manifest.json`

但需要注意：

- 长期版本真相不应只落在这些构建目录中
- 版本归档应进入受 Git 管控的位置，例如：
  - `release.version.json`
  - `docs/releases/`

## 4. 当前下游项目边界

- 下游项目正式接收：`.agents/`、`.maglev/`、`specs/`、`docs/`、`issues/`
- 下游项目根目录不再接收：`install.sh`、`maglev_installer.py`
- 初始化会在缺失时自动落盘最小 `AGENTS.md` 与 `llms.txt`（含"写作与产物纯净"5 条硬规则）
- 初始化会写入或扩展 `.gitignore` 中的 `Maglev managed` 块，覆盖 `.maglev_build/`、`__pycache__/`、`*.pyc`
- 初始化会检测下游仓库的 git submodule pointer 漂移，并在 fresh / 已有 `.git` 两种路径下都尝试将其同步回父仓库 recorded SHA
- 发版打包通过 `shutil.ignore_patterns` 过滤 `__pycache__` 与 `*.pyc`，dist 不再夹带 Python 缓存

对应用户文档：

- [Maglev 快速开始](../../docs/guides/20_operations/maglev_distribution_quickstart.md)
- [Maglev 初始化手册](../../docs/guides/20_operations/maglev_init_manual.md)

## 5. 交互层

- `现状同步（reality-sync）`
  - skill 定义见 [.agents/skills/reality-sync/SKILL.md](../../.agents/skills/reality-sync/SKILL.md)
  - 对外操作说明见 [Maglev 多入口使用说明](../../docs/guides/20_operations/maglev_entrypoints.md)
  - 兼容 workflow 入口：`/standup`

- 主流程四对象统一使用 skill runtime name：
  - `reality-sync`
  - `spec-designer`
  - `context-implementer`
  - `integrated-validator`
  - 当前在研主题索引见 [../20_evolution/active/README.md](../20_evolution/active/README.md)

- 正式的 AI 更新 workflow / skill

当前多入口关系的真实状态是：

- CLI 会调用发行物 / 包内镜像中的 installer 作为执行核心
- npm / npx 是用户主入口
- AI workflow / skill 目前只在安装后交互场景成熟，不含正式 update 入口

## 6. 当前已知缺口

- 公开 OSS / CDN 分发尚未打通
- `curl | bash` 仍不能作为正式对外主路径
- 构建目录不能作为长期真相源，长期版本记录需继续依赖受 Git 管控的位置
- AI 更新入口尚未产品化
- `task_public_distribution_channel` 仍未闭环
- `task_ai_tooling_compatibility_followup` 仍未闭环

---
*This document captures runtime truth, not implementation history.*
