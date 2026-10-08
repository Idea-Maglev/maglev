---
reality_id: delivery-runtime.interfaces.cli
title: 交付运行时命令入口
owner_domain: delivery-runtime
owner_slot: interfaces
fact_type: cli_contract
knowledge_status: established
scope:
  includes:
    - 三个命令入口（@idea-maglev/maglev-cli、maglev-extension、scripts/maglev-python）的命令目录、参数、静态可知输出与退出分支、调用场景与实现锚点
  excludes:
    - bin/index.js 分发位置判定的深挖（属 implementation/cli.md，本页链接不复制）
    - 命令背后的安装更新流程（属 capability/workflows.md）
---

# 交付运行时命令入口

## 1. Synopsis 与命令范围

| 入口 | 类型 | 调用方/场景 | 意图来源 | 注册锚点 |
| --- | --- | --- | --- | --- |
| `@idea-maglev/maglev-cli`（`packages/maglev-cli/bin/index.js`） | CLI 命令 | 下游项目用户执行安装、更新与版本查询 | CLI 入口 | `packages/maglev-cli/package.json` bin 注册（分发路径） |
| `maglev-extension`（`packages/maglev-extension-cli/bin/maglev-extension.js`） | CLI 命令 | 扩展使用者与扩展作者（authoring/registry 子命令） | [扩展分发](../implementation/extension-distribution.md) | `packages/maglev-extension-cli/package.json` 7 行 `bin.maglev-extension` |
| `scripts/maglev-python` | 仓库脚本 | 协议脚本调用方在项目本地环境运行 Python 脚本 | Python 运行时 | 脚本 usage 文本（10-21 行） |

## 2. 命令与选项

| 命令/Job | 参数或选项 | 必填/默认事实 | 处理器 | 状态 |
| --- | --- | --- | --- | --- |
| `maglev-cli version`（含 `--version`/`-v`） | `--json` | 可选；缺省输出人读两行 | `printVersion`（64-105 行） | established |
| `maglev-cli init` / `maglev-cli update` | 透传安装器参数（含 `--force`、`--dry-run`、`--local-dist` 由入口注入） | 命令名必填 | 入口转交安装器（157-165 行）；参数面由安装器 argparse 定义（2304 行起） | established |
| `maglev-extension search/inspect/install/update/check/test-install` | `<id>` 位置参数、`--workspace-root` | inspect/install/update/check 要求 id | `run` 分发（56-84 行） | established |
| `maglev-extension enable/disable/remove` | `<id>`、`--workspace-root` | id 必填；external integration 走 `integration.*` 分支 | 79-84 行 | established |
| `maglev-extension init/registry init/registry add/sources list/sources add/slot resolve` | authoring 与 registry 管理选项（`--profile`、`--id`、`--source-path` 等） | 各子命令要求目标参数 | 22-55 行、117-128 行 | established |
| `maglev-extension --version/--help` | 无 | — | 11-17 行 | established |
| `scripts/maglev-python --doctor` | 无 | — | ensure_runtime 后输出诊断并 `exit 0`（195-202 行） | established |
| `scripts/maglev-python --check` | 无 | — | 输出诊断；环境就绪 `exit 0`，否则 `env_failed` `exit 2`（187-194 行） | established |
| `scripts/maglev-python [--] <script.py> [args...]` | `--` 分隔后透传 | 脚本路径必填，缺失时 usage 到 stderr 并 `exit 2` | `exec venv_python`（204-209 行） | established |

## 3. 输入、静态可知输出与退出分支

| 入口 | 输入约束 | 静态可知输出/副作用 | exit/失败分支 | 证据 |
| --- | --- | --- | --- | --- |
| `maglev-cli version` | 无 | `maglev-cli: <cli 版本>` 与 `bundled-dist: <manifest 版本>` 两行；`--json` 时输出 `{cli_version, bundled_version, node_version, platform}` | manifest 缺失 `exit 2`；版本不一致 `exit 2`；成功 `exit 0` | 73-103、108-111 行；`version-json.test.js` 六个命名用例 |
| `maglev-cli init/update` | Python 可执行文件存在 | 打印 "Maglev Distribution Engine (Npx Entry)"，转交安装器执行 | Python 缺失 `exit 1`（128 行）；安装器缺失 `exit 1`（146 行）；build-dist 版本不一致 `exit 2`（141 行）；包内版本不一致 `exit 2`（150 行）；安装器失败透传其状态码或 1（165 行）；成功 `exit 0` | 113-165 行 |
| `maglev-extension <command>` | id/目标参数按命令要求 | JSON envelope 输出（`commandResult` 构造，含 status 与 issues） | `emit`：status 为 fail 时 `exitCode 1`，否则 0；不支持的 issue level 直接拒绝 | `maglev-extension.js` 136-139 行；`cli.test.js` envelope 与失败 envelope 用例 |
| `scripts/maglev-python --check/--doctor` | 项目内运行 | 输出 repo_root、uv、venv、python、requirements 诊断行 | `--check` 未就绪 `exit 2`；`--doctor` 完成 `exit 0` | 145-202 行 |
| `scripts/maglev-python <script>` | 脚本路径必填 | 在受管 venv 内 `exec` 脚本并透传参数 | 无脚本参数 `exit 2`；运行时未就绪由 ensure_runtime 失败路径决定（返回 2） | 204-209 行、140-142 行 |

## 4. 调用场景与实现锚点

| 入口 | 调用场景 | 实现链 | 测试/验证 | 边界 |
| --- | --- | --- | --- | --- |
| `maglev-cli version --json` | 用户与脚本核对 CLI 与发行物版本 | `printVersion` → `resolveDistDir` → JSON 输出 | `packages/maglev-cli/tests/version-json.test.js`（JSON 有效性、必填字段、cli_version 与 package.json 一致、纯文本向后兼容、node_version、platform） | 只证明输出契约，不证明安装行为 |
| `maglev-cli init/update` | 下游项目安装与更新 | `bin/index.js` → `--local-dist` → `maglev_installer.py` | 测试矩阵 更新流行 | 不证明上游网络行为 |
| `maglev-extension search/install/...` | 扩展发现与生命周期管理 | `run` → `registry.js`/`asset-manager.js`/`consumer-lifecycle.js` | `cli.test.js`（单源失败继续带 warning、全失败聚合报错、lock 校验等命名用例） | 不证明真实 Git 远端状态 |
| `scripts/maglev-python` | 协议脚本运行 | `find_uv`/`find_system_python` → `ensure_runtime` → `exec` | Python 运行时 | 不证明协议脚本业务语义 |

## 5. 未知项与深挖

| 项目 | 未知原因 | 已查材料 | 深挖 |
| --- | --- | --- | --- |
| `maglev-cli` 无参数/未知命令的输出 | 入口对未知首参直接走安装器转交路径，未定位专用 usage 文本 | `bin/index.js` 108-165 行 | CLI 入口 |
| `maglev-extension` 各子命令的完整选项清单 | 本页只登记静态可枚举的命令面与通用选项，选项级契约未逐个展开 | `run` 分发段与 `commandName`（117-128 行） | [扩展分发](../implementation/extension-distribution.md) |
| 安装器 argparse 全量参数面 | 参数定义在安装器尾部（2304 行起），本页只列 CLI 转交涉及的核心项 | `maglev_installer.py` argparse 段 | 安装核心 |
