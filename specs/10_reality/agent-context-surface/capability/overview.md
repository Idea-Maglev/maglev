---
reality_id: agent-context-surface.capability.overview
title: Agent 上下文面能力
owner_domain: agent-context-surface
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - AGENTS.md 与 llms.txt 双入口、managed 区块注入链、ai-context-check 统一检查契约与状态模型的当前事实
  excludes:
    - installer 安装更新全流程（属 delivery-runtime 域）
    - 文档治理注册表机制（属 governance-quality 域）
---
# Agent 上下文面能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 跨平台 agent | 获得会话入口：红线、目录速查、定位锚点、managed 区块、Skill 优先级协议 | `AGENTS.md` 会话入口 | `AGENTS.md`（managed 标记 72-92 行） |
| AI 代理 | 获得上下文地图：身份、快速开始、导航 | `llms.txt` 上下文地图 | `llms.txt`（managed 标记 22-42 行） |
| 安装用户 | 初始化时获得入口骨架 | installer 注入最小骨架与纪律区块；已存在文件用户内容不动 | `packages/maglev-cli/runtime-src/maglev_installer.py`（`ensure_ai_context_files`） |
| 治理流程 | 主链路/兼容入口由注册表统一渲染 | `generate_documentation_surfaces.py` 渲染/校验 managed 区块（标记对必须恰好一对） | `scripts/generate_documentation_surfaces.py`（`TARGETS`） |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 会话启动 | agent 读取仓库入口 | AGENTS.md/llms.txt 双入口生效 | 上下文入口 | established | supported |
| init 缺失入口文件 | installer 运行 | 写最小骨架 + 纪律注入 | 上下文入口 | established | supported |
| ai-context-check 执行 | 契约已登记 | 四判定 + 补齐建议；只判断不重写 | 状态模型 | established | supported |
| 治理注册表变更 | 注册表先行更新 | managed 区块重渲染；标记对不符报结构错误 | 文档源治理 | established | supported |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 范围外 | installer 安装更新全流程 | 属 delivery-runtime 域 | `../delivery-runtime/capability/overview.md` |
| 范围外 | 索引与地图产物 | 属 machine-index-engine / project-map 域 | `../project-map/capability/overview.md` |
| 不承诺 | 双入口内容总是与源同步 | CLAUDE.md 适配层已观察到陈旧条目（生成器无删除分支） | `../adoption-integration/verification/known-gaps.md` |

## 4. 事实与深挖

- 上下文入口、配置、错误语义、状态模型
- [已知缺口](../verification/known-gaps.md)、Claim 登记册
