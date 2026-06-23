# Requirements — Runtime Environment Check

## 来源依据

| 来源 | 类型 | 用途 |
|---|---|---|
| [context/input_facts.md](./context/input_facts.md) | 输入事实 | 固定实际故障、现有流程和本轮范围 |
| `../../../../../../maglev-project/maglev-3de/docs/thinking/2026-06-18-maglev-runtime-bootstrap-feedback.md` | 实践反馈 | 固定 Python 3.9、PyYAML、uv PATH、preflight 与错误分类需求 |
| [00_intent.md](./00_intent.md) | intent | 固定目标、成功信号和非目标 |

## 范围

### In Scope

- 新增统一 Python runtime wrapper，用于执行 Maglev 协议脚本。
- 为 `index-librarian` 协议声明最小 Python 依赖。
- 为 `reality-sync` 冷启动路径增加 runtime preflight 规则。
- 将运行时失败从 track 内容失败中分离为 `env_failed`。
- 将 runtime wrapper 纳入 Maglev 分发资产，并忽略本地 runtime 状态。

### Out of Scope

- 不批量迁移所有 `python3` 文档引用。
- 不替换 installer 自身的 Python 3.6+ 启动前提。
- 不引入全局 `~/.maglev/` 运行时状态。
- 不要求用户手动维护虚拟环境。

## 功能需求 F-1: 受控 Python 运行时入口

**用户故事**: 作为 Maglev 使用者，我希望协议脚本通过统一入口运行，以便不同开发机上的系统 Python 差异不会破坏冷启动流程。

| AC | 验收标准 | 来源摘要 | 上下文判定 | 证据 |
|---|---|---|---|---|
| AC-F1-1 | 当执行 `./scripts/maglev-python <script.py> ...` 时，入口应使用项目本地受控 Python 环境运行脚本。 | 反馈报告指出直接依赖系统 `python3` 导致 Python 3.9 执行 3.10+ 语法失败。 | 统一入口是阻断运行时漂移的最小机制，应先覆盖协议脚本而不是要求每个 skill 自己处理 Python。 | [context/input_facts.md](./context/input_facts.md) |
| AC-F1-2 | 当 `uv` 可用或位于常见用户安装路径时，入口应优先用 `uv` 准备 Python 运行时。 | 反馈报告指出用户已安装 `uv`，但非交互 shell PATH 不包含 `~/.local/bin`。 | wrapper 不能只依赖 `command -v uv`；需要检查常见路径以适配 Codex/CLI 非交互环境。 | 实践反馈 |
| AC-F1-3 | 当 `uv` 不可用但系统存在 Python>=3.11 时，入口应能用系统 Python 创建本地虚拟环境并安装依赖。 | 反馈报告目标是稳定运行环境，不是强制唯一安装器。 | `uv` 是优先路径，但不是唯一生路；兜底能降低首次运行阻力。 | 实践反馈 |

## 功能需求 F-2: 协议依赖契约

**用户故事**: 作为协议维护者，我希望每组 Python 协议显式声明依赖，以便 wrapper 和 preflight 能按同一份契约准备环境。

| AC | 验收标准 | 来源摘要 | 上下文判定 | 证据 |
|---|---|---|---|---|
| AC-F2-1 | `index-librarian/protocol/` 应声明 Python 依赖清单，至少包含 `PyYAML`。 | 反馈报告指出 index-librarian 依赖 Python 3.10+ 与 PyYAML，但此前没有显式最小依赖清单。 | 依赖清单应靠近协议目录，便于 wrapper、reality-sync 和后续 bootstrapper 复用。 | 实践反馈 |
| AC-F2-2 | wrapper 应默认消费 `index-librarian` 的依赖清单，并允许通过环境变量覆盖。 | 初始落点是 index-librarian 冷启动路径，但未来可能有其他协议。 | 默认值保证当前路径即开即用，覆盖能力避免把 wrapper 锁死在单协议。 | 现有 `index-librarian` 协议路径 |

## 功能需求 F-3: 主流程 preflight 与错误分类

**用户故事**: 作为会话启动者，我希望冷启动先检查运行环境，并在环境不可用时看到明确修复动作，而不是看到误导性的 track 失败。

| AC | 验收标准 | 来源摘要 | 上下文判定 | 证据 |
|---|---|---|---|---|
| AC-F3-1 | `reality-sync` 启动期漂移哨兵应先执行 runtime doctor/preflight，再执行 track verify。 | 反馈报告指出冷启动直接触发 Python 脚本，没有前置检查。 | preflight 应在用户看到 Python 栈错误前拦截环境问题。 | `.agents/skills/reality-sync/SKILL.md` |
| AC-F3-2 | 当 wrapper 或运行时准备失败时，报告状态应使用 `env_failed`，并提示安装 `uv` 或 Python>=3.11。 | 反馈报告指出 `track failed` 同时覆盖脚本错误、registry 错误与环境错误。 | 环境失败不是索引内容失败，必须单独表达，否则用户会修错方向。 | 实践反馈 |
| AC-F3-3 | 当 runtime preflight 通过但 `track_verify` 失败时，仍按既有 `partial` / `failed` track 规则处理。 | 本轮不改变索引校验业务语义。 | 错误分类只新增环境前置状态，不扰动原 track 语义。 | `.agents/skills/index-librarian/SKILL.md` |

## 功能需求 F-4: 分发与本地状态治理

**用户故事**: 作为 Maglev 接入项目维护者，我希望运行时入口随 Maglev 下发，本地虚拟环境不污染 Git。

| AC | 验收标准 | 来源摘要 | 上下文判定 | 证据 |
|---|---|---|---|---|
| AC-F4-1 | `scripts/maglev-python` 应作为 `runtime_internal` 资产纳入 catalog，以便 release manifest 下发。 | 发行脚本从 catalog 收集 runtime_internal path。 | 不注册 catalog 会导致源仓库可用但目标项目缺失 wrapper。 | `scripts/maglev_release.py` |
| AC-F4-2 | installer 下载 `scripts/maglev-python` 后应确保它有可执行权限。 | installer 远端下载按二进制写文件，不保留源文件 mode。 | 运行命令使用 `./scripts/maglev-python`，缺少可执行位会让首次使用失败。 | `packages/maglev-cli/runtime-src/maglev_installer.py` |
| AC-F4-3 | `.maglev/runtime/` 应进入 `.gitignore` 与 installer managed ignore block。 | wrapper 默认创建项目本地运行时。 | 本地虚拟环境属于机器状态，不应进入仓库，也不应污染分发。 | `.gitignore`；installer managed block |

## 非功能需求

### NFR-1: 用户看到修复动作，而不是栈错误

环境失败输出应直接说明缺少什么和如何修复，不要求用户阅读 Python traceback。

### NFR-2: 项目本地、可删除、可重建

受控运行时应保存在项目本地忽略目录中，可删除后由 wrapper 重新创建。

### NFR-3: 最小侵入

本轮只迁移高风险冷启动路径，保留其他脚本现状，避免一次性重写过大。

## Ready Gate

- gate_result: ready
- next_object_candidate: `spec-designer`
- reason: 运行时入口、依赖契约、preflight、错误分类和分发边界已明确。
- consumption_rationale: 后续设计需要确定 wrapper 行为、分发纳入方式和冷启动状态契约。
- prd_mode_required: false
- missing_items: 无阻塞项。
