# Plan — Runtime Environment Check

## 来源依据

| 来源 | 类型 | 用途 |
|---|---|---|
| [02_design.md](./02_design.md) | design | 实施任务拆解依据 |
| [01_requirements.md](./01_requirements.md) | requirements | 验收标准依据 |

## 实施任务

| Task | 内容 | 覆盖设计 | 状态 |
|---|---|---|---|
| T-1 | 新增 `scripts/maglev-python` runtime wrapper，支持 doctor、uv 探测、venv 与依赖安装。 | wrapper 设计 | done |
| T-2 | 新增 `index-librarian/protocol/requirements.txt`，声明 `PyYAML>=6.0`。 | 协议依赖契约 | done |
| T-3 | 更新 `reality-sync` 和 `index-librarian` 文档主路径，迁移到 wrapper 并加入 `env_failed`。 | preflight 与状态契约 | done |
| T-4 | 注册 `maglev-python-runtime` 为 runtime_internal 资产。 | 分发纳入 | done |
| T-5 | 更新 `.gitignore` 与 installer managed block，忽略 `.maglev/runtime/` 并保证 wrapper 可执行。 | 本地状态治理 | done |
| T-6 | 运行 doctor、track verify、catalog check、installer py_compile 与引用检查。 | 验证设计 | done |
| T-7 | 更新初始化、更新、快速开始和排障手册，说明 doctor、自动触发点、`env_failed` 与验收命令。 | 用户面文档 | done |

## 验证计划

| 验证项 | 方法 | 期望 |
|---|---|---|
| runtime doctor | `./scripts/maglev-python --doctor` | exit 0 |
| skills track verify | `./scripts/maglev-python .agents/skills/index-librarian/protocol/scripts/track_verify.py --track-id skills` | exit 0 |
| catalog path | `python3 scripts/check_runtime_distribution.py` | exit 0 |
| installer syntax | `python3 -m py_compile packages/maglev-cli/runtime-src/maglev_installer.py` | exit 0 |
| 裸 Python 回归 | `rg "python3 .*track_verify|python3 \\${PROTOCOL}" .agents/skills/reality-sync .agents/skills/index-librarian` | 无命中 |

## 变更记录

| 日期 | 变更对象 | 变更内容 | 变更原因 | 来源依据 |
|---|---|---|---|---|
| 2026-06-19 | runtime-environment-check spec | 新增需求、设计和实施计划。 | 将真实运行时故障沉淀为 Maglev 框架能力改进。 | [01_requirements.md](./01_requirements.md) |
