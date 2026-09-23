---
reality_id: delivery-runtime.capability.overview
title: 交付运行时能力
owner_domain: delivery-runtime
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - npm/npx 用户安装与更新主路径、CLI 入口契约、安装更新执行核心、发行构建、扩展分发与 Python 协议运行时的当前事实
  excludes:
    - 版本说明知识的生产与归档（属 release-knowledge 域）
    - 扩展的运行时选择语义细节（rk.dr.ext.install-vs-enable 概述，执行插槽细节属 skill-runtime 域）
---
# 交付运行时能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 使用 Maglev 的下游项目 | 安装、更新运行时并保持受管文件一致 | manifest 驱动的差异化更新与退役保护 | `packages/maglev-cli/runtime-src/maglev_installer.py`（`RETIREMENT_MANIFEST_SCHEMA_VERSION = 2`） |
| Maglev 维护者 | 发布新版本并治理退役资产 | 发行构建、npm 发布与 Git tag 的单入口流程 | `scripts/maglev_release.py`（retired_files 注册表校验） |
| 扩展使用者 | 搜索、安装与生命周期管理扩展 | `maglev-extension` 命令面与 lock 状态管理 | `packages/maglev-extension-cli/package.json` |
| 协议脚本调用方 | 在项目本地环境运行 Python 协议脚本 | uv 优先、系统回退的运行时入口 | `scripts/maglev-python`（`MAGLEV_UV`、`--doctor`） |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| `npx @idea-maglev/maglev-cli init/update` | CLI 可用 | 受管文件落盘；bundled 入口经 `--local-dist` 与离线入口共享退役校验 | CLI 入口 | established | supported |
| 版本不匹配或产物缺失 | bundled/dist 状态异常 | 显式报错，不静默使用不一致发行物 | CLI 入口 | established | supported |
| 发版执行 | catalog distribution scope 就绪 | 发行目录 + manifest（含 retired_files）+ npm publish + tag | 发行构建 | established | supported |
| `maglev-extension` 生命周期命令 | extensions.sources.yaml 存在（init 写默认官方源） | 安装/启用状态写入下游 `.maglev/extensions.lock` | 扩展分发 | established | supported（lock 为下游产物，见[已知缺口](../verification/known-gaps.md)） |
| submodule 项目 init/同步 | `.maglev/config.json` 登记了 submodule | HEAD 漂移检测并回到记录版本 | 安装核心 | established | supported |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外 | 版本说明知识的生产与归档 | 属 release-knowledge 域，本域只承载交付机制 | `../../release-knowledge/capability/overview.md` |
| 范围外 | 扩展的运行时执行插槽选择 | 属 skill-runtime 域（code-execution-slot） | `../../skill-runtime/capability/overview.md` |
| 未证实 | `--force` 与退役保护的逐分支交互 | 源码分支未穷尽审计 | [已知缺口](../verification/known-gaps.md) |
| 不持有 | 下游项目 `.maglev/extensions.lock` 当前状态 | 本仓不持有下游运行态文件 | [已知缺口](../verification/known-gaps.md) |

## 4. 事实与深挖

- CLI 入口、安装核心、发行构建、扩展分发
- 下游布局、Python 运行时
- 分发路径、[已知缺口](../verification/known-gaps.md)、Claim 登记册
