---
title: "Maglev Distribution & Installation - Requirements"
status: "Archived"
---

# 01 Requirements: 分发生命周期规约 (Ready-to-Code)

> 本组 Spec 已完成其历史使命，现状已结晶到 `specs/10_reality/`，本文件仅作为历史需求归档保留。

---

## 0. 历史主线声明 (Primary Spec Declaration)

- 本 Spec 曾是当前分发主线的核心需求规范。
- 早期 `version_sync_tool` 中关于安全同步的能力要求，已被当前 Distribution Engine 吸收。
- 当前唯一正式的下游执行核心为 `maglev_installer.py`；Shell 与 Npx 入口都只作为其包装层。

## 1. 用户故事 (User Stories)

### US-1: 初次安装 (First-Time Init)
> 作为一个**新接触 Maglev 的开发者**，我希望在我的存量 Git 仓库中执行一行命令，就能自动获得 Maglev 的完整能力（Skills, Workflows, Rules），并且不破坏我现有的工程结构。

**前置条件**: 用户已自行创建并 clone 了一个 Git 仓库到本地，该仓库中没有 `.maglev/` 或 `.agents/` 目录。

**完整交互流程**:
```
$ curl -sSL https://maglev.dev/install.sh | bash
   (或 npx maglev-cli@latest)

[1/5] 🔍 检测当前目录...
      当前目录: <local-path-redacted>
      Git 仓库: ✅ 已检测到 (.git)
      Maglev 状态: ❌ 未安装

[2/5] 📡 连接远端仓库...
      最新版本: v2.3.0 (2026-03-10)
      资产清单: 29 个 Skills, 16 个 Workflows, 3 个 Protocols

[3/5] 📥 下载并注入核心资产...
      → .agents/skills/          (29 items)
      → .agents/workflows/       (16 items)
      → .maglev/rules/          (3 items)
      → .maglev/protocols/      (2 items)
      → specs/ (空骨架)
      → docs/ (空骨架)
      → issues/ (空骨架)

[4/5] 📋 项目注册 (交互式问答)
      ? 请输入项目名称: my-awesome-app
      ? 请输入项目简述: 基于 Vue3 + Spring Boot 的协作平台
      ? 您希望如何配置代码仓库？
        [1] 交互式注册 (逐个添加仓库)
        [2] 读取已有配置文件 (从指定的 config.json 导入)
        [3] 跳过此步骤 (后续再配置)
        > 1

      --- 仓库 #1 ---
      ? 仓库 Git 地址 (SSH 或 HTTPS):
        > git@github.com:example/frontend.git
      ? 仓库描述 (这个仓库是做什么的):
        > 协作平台的前端项目，基于 Vue 3 SPA
      📥 正在 clone 仓库到 ./frontend ...
      ✅ clone 成功

      ? 是否继续添加仓库？ (Y/n): Y

      --- 仓库 #2 ---
      ? 仓库 Git 地址 (SSH 或 HTTPS):
        > https://github.com/example/backend.git
      ? 仓库描述:
        > 协作平台的后端项目，基于 Spring Boot RESTful API
      📥 正在 clone 仓库到 ./backend ...
      ✅ clone 成功

      ? 是否继续添加仓库？ (Y/n): n

      ✅ 已注册 2 个代码仓库
      ✅ 已生成 specs/10_reality/repository_map.md
      ✅ 已生成 .maglev/config.json

[5/5] ✅ Maglev 环境就绪！(v2.3.0)
      ─────────────────────────────────────
      🚀 快速开始:
        1. 在 IDE 中打开此项目
        2. 输入 /tutor   → 启动交互式教程
        3. 输入 /standup  → 每日项目状态同步
        4. 输入 /map     → 生成项目全景地图
      ─────────────────────────────────────
```

**验收标准**:
- [AC-1.1] 执行命令后，当前目录下新增 `.agents/`, `.maglev/`, `specs/`, `docs/`, `issues/` 目录结构，且原有文件无任何被删除或修改。
- [AC-1.2] `.maglev/config.json` 包含用户输入的项目名称、描述和仓库映射（含 Git URL 和描述）。
- [AC-1.3] `specs/10_reality/repository_map.md` 包含用户注册的仓库信息表格。
- [AC-1.4] `.maglev/sync_state.json` 记录了本次下发的所有文件的 SHA-256 Hash 与版本号。
- [AC-1.5] 用户注册的仓库已被成功 clone 到当前目录下对应的子目录中。
- [AC-1.6] 若 clone 失败，工具不中断安装流程，而是跳过该仓库并输出可操作的诊断建议和帮助文档链接。

---

### US-2: 增量更新 (Incremental Update)
> 作为一个**已安装 Maglev 的开发者**，我希望能通过同一个命令检查是否有新版本，并安全地将新文件同步到本地，同时不覆盖我可能做过的本地自定义修改。

**前置条件**: 用户的仓库中已存在 `.maglev/sync_state.json`（表示此前执行 init 成功）。

**完整交互流程**:
```
$ curl -sSL https://maglev.dev/install.sh | bash

[1/4] 🔍 检测当前目录...
      Maglev 状态: ✅ 已安装 (v2.3.0, 同步于 2026-03-10)

[2/4] 📡 检查上游更新...
      本地版本: v2.3.0
      最新版本: v2.4.0 (2026-03-15)
      → 发现 3 个新增文件, 5 个更新文件

[3/4] 📥 执行增量同步...
      [+] 新增: .agents/skills/maglev-research/SKILL.md
      [+] 新增: .agents/skills/maglev-research/references/research.workflow.md
      [+] 新增: .agents/workflows/research.md
      [~] 覆盖: .agents/skills/maglev-tutor/references/step-01-intro.md
      [~] 覆盖: .agents/skills/maglev-tutor/references/step-02-concepts.md
      [~] 覆盖: .maglev/rules/core_rules.md
      [~] 覆盖: .maglev/protocols/collaboration.md
      [!] 冲突: .agents/workflows/standup.md (本地已修改)
          → 本地修改已备份为: standup.md.local_backup_20260315143022
          → 官方新版本已放入原位
      [-] 跳过: .agents/skills/atomizer/SKILL.md (无变化)
      ... (其余 24 个文件无变化，已跳过)

[4/4] ✅ 同步完成！(v2.3.0 → v2.4.0)
      新增: 3 | 更新: 5 | 跳过: 24 | 冲突备份: 1

      ═══════════════════════════════════════
      📜 更新日志 (v2.4.0)
      ═══════════════════════════════════════
      - [新增] maglev-research: 深度调研技能
      - [优化] maglev-tutor: 教程内容更新
      - [修复] core_rules: 修正协作规范中的歧义
      ... (详见远端完整 CHANGELOG.md)
```

**验收标准**:
- [AC-2.1] 如果本地版本与远端版本相同，工具提示"已是最新版本"并退出，不执行任何文件操作。
- [AC-2.2] 远端有新增文件时，直接下载写入本地，不影响已有文件。
- [AC-2.3] 远端有更新文件、且本地**未被用户修改**时，执行覆盖。
- [AC-2.4] 远端有更新文件、但本地**已被用户修改**时，将本地文件重命名为 `{filename}.local_backup_{timestamp}`，然后再用远端新版覆盖原位置。终端输出冲突提示。
- [AC-2.5] `sync_state.json` 更新为新版本号与新的完整文件 Hash 列表。
- [AC-2.6] 终端自动打印远端 CHANGELOG.md 的前 20 行摘要。

---

### US-3: Dry-Run 模式 (试运行预览)
> 作为一个**谨慎的开发者**，我希望在正式执行同步前，先预览哪些文件会被新增、覆盖或触发冲突，而不实际修改任何文件。

**前置条件**: 通过参数 `--dry-run` 触发。

**完整交互流程**:
```
$ curl -sSL https://maglev.dev/install.sh | bash -s -- --dry-run

[DRY-RUN MODE] 以下为模拟结果，未对任何文件进行实际修改:
[+] 将新增: .agents/skills/maglev-research/SKILL.md
[~] 将覆盖: .maglev/rules/core_rules.md
[!] 将冲突: .agents/workflows/standup.md (本地已修改)
[-] 将跳过: .agents/skills/atomizer/SKILL.md (无变化)

模拟结束。如需执行，请去掉 --dry-run 参数重新运行。
```

**验收标准**:
- [AC-3.1] 不创建、修改、删除任何文件。
- [AC-3.2] 不更新 `sync_state.json`。
- [AC-3.3] 终端完整输出所有将要发生的文件操作的预览。

---

### US-4: 发布新版本 (Creator Release — 仅 Creator 使用)
> 作为 **Maglev 框架的维护者 (Creator)**，我希望在完成一轮框架迭代后，通过一个命令自动编译出干净的发行包，并推送到远端托管平台。

**前置条件**: 仅在 Maglev 源仓库中执行。

**完整交互流程**:
```
$ python scripts/maglev_release.py --version 2.4.0

[1/6] 🔍 Pre-Release Audit...
      执行 maglev-audit-spec... ✅ 通过
      执行 validate-all... ✅ 通过

[2/6] 🔖 解析公私域标签...
      扫描 .agents/skills/ : 32 个 Skills
        → public: 29 | private: 3
      扫描 .agents/workflows/ : 18 个 Workflows
        → public: 16 | private: 2
      扫描 .maglev/ :
        → public: rules/, protocols/, knowledge_base/
        → private: temp/, legacy sync artifacts

[3/6] 📦 构建发行目录 (dist/)...
      提取 specs/ 精华 → dist/.agents/skills/maglev-tutor/references/
      复制公域 Skills → dist/.agents/skills/ (29 items)
      复制公域 Workflows → dist/.agents/workflows/ (16 items)
      复制公域 .maglev → dist/.maglev/ (精简版)

[4/6] 📝 生成 Changelog...
      对比上一版本 manifest 与当前 dist/...
      → 新增: 3 个文件 | 修改: 5 个文件 | 删除: 0 个文件
      ✅ 已生成变更事实清单: dist/CHANGELOG_DRAFT.md

      ⏸  脚本已暂停。请在 IDE 中执行 /generate-changelog 
         让 AI 助手基于变更清单生成语义化 CHANGELOG。
         审阅确认后，按回车继续...

      [用户按回车]
      ✅ 已确认 dist/CHANGELOG.md

[5/6] 🔒 计算 Hash 并生成清单...
      SHA-256 计算: 147 个文件
      生成 dist/manifest.json
        → version: "2.4.0"
        → publish_date: "2026-03-15"
        → files: [...]

[6/6] 🚀 发布到远端...
      推送至: https://github.com/.../maglev/latest/
      ✅ v2.4.0 发布成功！
```

**验收标准**:
- [AC-4.1] Private 标签的 Skills/Workflows 不出现在 `dist/` 及 `manifest.json` 中。
- [AC-4.2] `manifest.json` 中每个文件条目包含 `path` 和 `sha256` 字段。
- [AC-4.3] 如果 Audit 未通过，流水线中止并输出失败原因，不生成 manifest。
- [AC-4.4] `dist/.maglev/` 是一个精简的只读 Runtime 版本（不含 `temp/`、历史同步实现等私有文件）。
- [AC-4.5] Release Compiler 自动生成 `CHANGELOG_DRAFT.md`（文件级变更事实清单），并暂停等待 Creator 通过 AI Skill 生成语义化描述后确认。
- [AC-4.6] 最终发布的 `dist/CHANGELOG.md` 包含经 Creator 确认的语义化变更描述。

---

## 2. 核心功能规约 (Functional Specifications)

### 2.1 双入口形态 (Dual Entry Points)

| 属性 | Shell 模式 | Npx 模式 |
| :--- | :--- | :--- |
| **调用方式** | `curl -sSL https://maglev.dev/install.sh \| bash` | `npx maglev-cli@latest` |
| **参数传递** | `bash -s -- --dry-run` | `npx maglev-cli@latest --dry-run` |
| **环境依赖** | bash, curl (标准 Unix 工具) | Node.js >= 16 |
| **内部引擎** | 下载并执行 Python 脚本 (`maglev_installer.py`) | Node CLI 包装并执行内置 `maglev_installer.py` |
| **适用场景** | 无 Node 环境的后端/运维团队 | 前端/全栈项目 |

`packages/maglev-cli/` 属于正式分发入口包装层，负责在 Npx 模式下携带包内镜像并调用统一的 Python 执行器。

### 2.2 CLI 参数定义 (Command-Line Interface)

```
maglev-cli [command] [options]

Commands:
  init          初始化当前目录为 Maglev 项目 (默认行为)
  update        检查并执行增量更新

Options:
  --dry-run     试运行模式，仅预览变更，不修改文件
  --force       强制覆盖所有本地修改，跳过冲突备份
  --skip-prompt 跳过交互式问答 (适用于 CI/CD 环境)
  --upstream    指定自定义的上游仓库地址
  --version     显示当前工具版本
  --help        显示帮助信息
```

### 2.3 终端交互式问答流程 (Interactive Questionnaire)

仅在 **Init 态**（本地无 `.maglev/config.json`）触发。

#### 2.3.1 基本信息问答

| 序号 | 问题 | 类型 | 默认值 | 验证规则 |
| :--- | :--- | :--- | :--- | :--- |
| Q1 | 请输入项目名称 | 文本 | 当前目录名 | 非空，无特殊字符 |
| Q2 | 请输入项目简述 | 文本 | (空) | 可选 |

#### 2.3.2 仓库配置模式选择

在基本信息填写后，用户选择仓库配置方式：

| 选项 | 说明 |
| :--- | :--- |
| **[1] 交互式注册** | 通过问答逐个添加仓库（Git URL + 描述），工具自动执行 clone |
| **[2] 读取已有配置** | 指定一个已有的 `config.json` 文件路径，直接导入其中的仓库配置 |
| **[3] 跳过此步骤** | 不配置任何仓库，后续用户可手动编辑 `config.json` 或重新执行 init |

#### 2.3.3 交互式注册 (选择选项 1) 的单仓库问答循环

对每个仓库重复以下问答，直到用户选择“不再添加”：

| 序号 | 问题 | 类型 | 验证规则 |
| :--- | :--- | :--- | :--- |
| R1 | 仓库 Git 地址 (SSH 或 HTTPS) | 文本 | 必填，必须以 `git@` 或 `https://` 开头，以 `.git` 结尾 |
| R2 | 仓库描述 (这个仓库是做什么的) | 文本 | 必填，如“XX系统的前端项目”或“XX系统的全栈项目” |
| R3 | 是否继续添加仓库？ (Y/n) | 确认 | 默认 Y |

填写完每个仓库后，工具立即执行 `git clone`，目标目录名自动从 Git URL 中提取（如 `git@github.com:example/frontend.git` → `./frontend`）。

#### 2.3.4 Clone 失败处理策略

clone 操作可能因以下原因失败，工具必须**不中断安装流程**，而是跳过该仓库并给出可操作的建议：

| 错误场景 | 终端输出示例 |
| :--- | :--- |
| SSH 密钥未配置 / 权限不足 | `❌ clone 失败: Permission denied (publickey).`<br>`  建议: 请检查您的 SSH 密钥是否已添加到 Git 服务器。`<br>`  帮助文档: {HELP_DOC_URL}`<br>`  此仓库已跳过，您可在安装完成后手动 clone。` |
| 仓库地址不存在 / URL 错误 | `❌ clone 失败: Repository not found.`<br>`  建议: 请确认仓库地址是否正确，以及您是否有访问权限。`<br>`  帮助文档: {HELP_DOC_URL}`<br>`  此仓库已跳过。` |
| 网络不可达 | `❌ clone 失败: Could not resolve host.`<br>`  建议: 请检查网络连接。`<br>`  此仓库已跳过。` |
| 目标目录已存在 | `⚠️ 目录 ./frontend 已存在，跳过 clone。`<br>`  已将该目录直接记录为关联仓库。` |

**注**: `{HELP_DOC_URL}` 为可配置的帮助文档地址，由 Creator 在发行时配置。

在所有仓库处理完毕后，工具输出汇总：
```
✅ 成功 clone: 2 个仓库
⚠️ 已跳过: 1 个仓库 (请手动处理)
```

如果用户传入了 `--skip-prompt`，则跳过所有仓库注册步骤，仅生成最小化的 `config.json`。

### 2.4 知识内聚转移 (Starter Kit Deprecation)

原 `starter-kit/` 中的知识资产归档规则：

| 原文件 | 目标位置 | 归档方式 |
| :--- | :--- | :--- |
| `starter-kit/README.md` → 能力清单、指令表 | `.agents/skills/maglev-tutor/references/capabilities_inventory.md` | 提纯后嵌入，由 Release Compiler 自动执行 |
| `starter-kit/maglev_init_guide.md` → 铁三角概念、目标状态 | `.agents/skills/maglev-tutor/references/maglev_concepts.md` | 提纯后嵌入，由 Release Compiler 自动执行 |
| `starter-kit/maglev_init_guide.md` → Getting Started 步骤 | 硬编码到 CLI 的终端输出逻辑中 | 不存储为文件，直接在安装后打印 |
| `starter-kit/specs/`, `starter-kit/docs/` 等骨架目录 | 由 `init` 命令动态创建 | 不再以文件分发 |

### 2.5 公私域隔离标记规范 (Public/Private Tagging)

在每个 Skill 的 `SKILL.md` YAML 头部新增 `distribution` 字段：

```yaml
---
name: maglev-tutor
description: 交互式 Maglev 导师
distribution: public    # public | private
---
```

- `public`: 会被打入发行包分发给用户。
- `private`: 仅存在于源仓库中，发行时物理剔除。
- **默认值**: 如未声明，视为 `public`（向后兼容）。

以下技能/资产预标记为 **private**（初步清单，Creator 需最终确认）：

| 资产 | 理由 |
| :--- | :--- |
| `maglev-release-compiler` (待开发) | 框架发布工具链,用户无需使用 |
| `maglev-changelog-generator` (待开发) | 框架发布时的 Changelog 生成工具，用户无需使用 |
| `maglev-archival-check` | 框架内部归档审查，用户项目无此需求 |
| `contribute_methodology` | 框架方法论生成辅助, 仅框架贡献者使用 |
| `.maglev/temp/` | 临时文件目录 |
| `.maglev/maglev_sync.py` | 历史同步实现，已移除 |

---

## 3. 非功能性需求 (Non-Functional Requirements)

### 3.1 性能
- 首次 Init（含下载）应在 60 秒内完成（标准网络环境）。
- 增量 Update（无变化时）应在 5 秒内完成。

### 3.2 容错
- 网络中断时，工具应输出明确的错误提示并以非零退出码终止，不留下半成品文件。
- 下载中断后重新执行命令，应能从头开始完整执行（幂等性）。

### 3.3 兼容性
- Shell 模式: macOS, Linux (bash 4+)
- Npx 模式: Node.js >= 16
- 不依赖任何第三方 Python 库（仅标准库）

### 3.4 安全
- 远端 `manifest.json` 通过 HTTPS 获取。
- 每个文件下载后必须与 manifest 中声明的 SHA-256 Hash 进行校验，不匹配则丢弃并报错。
