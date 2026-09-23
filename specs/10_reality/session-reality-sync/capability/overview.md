---
reality_id: session-reality-sync.capability.overview
title: 会话现状同步能力
owner_domain: session-reality-sync
owner_slot: capability
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力对象：会话起点对齐（Reality/Risk/Action/Mode 四类同步）
  excludes:
    - 索引 preflight 的引擎实现（属 M1 页组）
    - 会话上下文文件面（属 M5 agent-context）
---

# 会话现状同步能力

## 1. 能力定位与受益者

| 受益者/调用方 | 要完成的任务 | 模块提供的结果 | 产品依据 |
| --- | --- | --- | --- |
| 人类开发者 | 在新会话快速知道"现在仓库是什么状态、有什么风险、下一步做什么" | 四类同步组成的结构化输出 | `.agents/skills/reality-sync/SKILL.md` 四类同步定义 |
| AI Agent | 在不读全仓的前提下对齐工作起点，避免凭记忆行动 | 同上，作为会话起点的事实底座 | 同上 |

## 2. 触发条件与可见结果

| 触发/入口 | 前置条件 | 可见结果 | 实现/验证深挖 | 知识状态 | 证据充分度 |
| --- | --- | --- | --- | --- | --- |
| 用户说 "Standup."（`/standup` 兼容入口） | 仓库就绪、skills 索引可验证 | `[Space]/[Mind]/[Risk]/[Action]` 输出节 | `../session-reality-sync/capability/workflows.md` | established（契约文本） | 契约级 |
| 长任务切换上下文 | 同上 | 同上，按新起点重算 | 同上 | established（契约文本） | 契约级 |
| 主线不明的模糊请求 | entry-router 分诊 | 交接至本能力 | crosscutting entry-router | established（Gate A 裁决） | 裁决级 |

## 3. 作用边界与不承诺事项

| 边界类型 | 不覆盖或未证实的内容 | 依据/已查范围 | 下一步静态入口 |
| --- | --- | --- | --- |
| 不发起任务级检索 | 同步只检查入口索引可验证与新鲜，不代用户做任务导航 | SKILL.md"索引健康"段 | `../machine-index-engine/capability/overview.md` |
| 不保证输出的事实质量 | 四类内容的贴合度依赖当次索引状态，无运行质量记录 | 本轮无运行记录机制 | `../session-reality-sync/verification/known-gaps.md` |
| 不修改仓库 | 同步为只读能力 | SKILL.md 全文无写操作 | — |

## 4. 事实与深挖

四类同步的机制事实、preflight 门禁与工作流分解见
`../session-reality-sync/capability/business-rules.md`（约束）与
`../session-reality-sync/capability/workflows.md`（流程）；本页不复制其内容。
