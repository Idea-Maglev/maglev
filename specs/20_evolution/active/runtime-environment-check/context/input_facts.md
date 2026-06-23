# Input Facts — Runtime Environment Check

## 来源依据

| 来源 | 类型 | 用途 |
|---|---|---|
| `../../../../../../maglev-project/maglev-3de/docs/thinking/2026-06-18-maglev-runtime-bootstrap-feedback.md` | 实践反馈 | 固定 Python 运行时缺失导致冷启动失败的事实、根因和建议 |
| 用户请求 | 对话摘要 | 固定本轮目标：创建新需求并补充机制，让运行环境准备更丝滑 |
| `.agents/skills/reality-sync/SKILL.md` | 现有流程 | 确认冷启动漂移哨兵当前直接调用 `track_verify.py` |
| `.agents/skills/index-librarian/SKILL.md` | 现有流程 | 确认协议脚本调用方式、状态报告契约与 exit code 约定 |
| `scripts/maglev_release.py` | 发行脚本 | 确认 runtime_internal 资产通过 catalog 纳入分发包 |
| `packages/maglev-cli/runtime-src/maglev_installer.py` | installer 源码 | 确认目标项目 `.gitignore` 管理块和文件下载行为 |

## 事实摘要

- `index-librarian` 协议脚本已使用 Python 3.10+ 类型语法，系统 Python 3.9 会在导入阶段失败。
- 目标项目可能已经安装 `uv`，但非交互 shell 的 PATH 不一定包含 `~/.local/bin`。
- 当前 `reality-sync` 冷启动直接执行 `python3 track_verify.py`，没有先做运行时 preflight。
- 当前 `track failed` 对用户暴露的是索引失败，但真实根因可能是 Python 版本、依赖或运行时入口不可用。
- Maglev 发行链路可通过 `.agents/private-catalog.yaml` 的 `runtime_internal` path 下发脚本资产。

## 收敛边界

- 本轮优先覆盖 Maglev 自身协议脚本运行时，不重写私域飞书脚本和外部工具链。
- 本轮优先覆盖 `reality-sync → index-librarian track_verify` 冷启动路径。
- 受控环境应是项目本地状态，不进入 Git 版本管理。
