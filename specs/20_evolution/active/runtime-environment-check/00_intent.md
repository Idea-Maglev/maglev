# Intent — Runtime Environment Check

## 背景

Maglev 的主流程越来越依赖 Python 协议脚本，尤其是 `reality-sync` 冷启动时会调用 `index-librarian` 的 track 校验脚本。实际接入项目中已经出现系统 Python 版本偏低、依赖缺失、`uv` 不在非交互 shell PATH 中的问题，最终表现为 `track failed`，但用户看到的并不是运行时根因。

## 核心意图

为 Maglev 增加受控 Python 运行时与环境检查能力，让主流程入口在执行协议脚本前先确认运行环境可用，并在不可用时给出明确、可执行的修复动作。

本需求的目标不是让用户理解 Python 依赖细节，而是让 Maglev 自己承担运行时准备：统一入口、依赖契约、preflight、错误分类与分发下发。

## 成功信号

- Maglev 仓库存在统一 Python 运行时入口，可运行协议脚本并提供 doctor/preflight 输出。
- `index-librarian` 协议声明最小依赖，冷启动路径不再依赖裸 `python3`。
- `reality-sync` 的启动期漂移哨兵能区分 `env_failed` 与 track 内容失败。
- 分发链路能把运行时入口下发到目标项目，并避免提交本地虚拟环境。

## 本轮不追求

- 不重写所有 Python 脚本为 Node 或 shell。
- 不一次性迁移私域飞书、Lark、artifact scanner 等所有脚本入口。
- 不改变 `track_verify.py` 的索引校验业务语义。
- 不把 `.maglev/runtime/` 中的本地运行时提交入库。
