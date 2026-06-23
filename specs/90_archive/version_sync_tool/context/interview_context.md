---
title: "Version Sync Tool - 共享上下文"
created_by: "maglev-create-spec"
last_updated: "2026-03-01"
---

## 用户画像 (Persona)
- **Who**: 
  - **初级/业务线开发者 (End User)**: 在各业务线工程内使用 Maglev 的人。他们需要最新鲜的 workflows 和 skills 但不懂如何安全更新。
  - **核心骨干/维护者 (Creator)**: 负责演进 Maglev 本体并向外部分发的人。他们痛点在于没有标准化分发渠道，只能四处帮人复制粘贴或靠口耳相传。
- **Pain Point**: 
  - 缺乏开箱即用的分发和同步机制，导致各业务线 Maglev 版本严重碎片化。
  - 手动复制 `.agents` 等文件极易覆盖业务线基于自身特点做出的“本地魔改”，更新等同于破坏。

## 核心问题 (Problem Statement)
- **Why**: 保护业务线侧因高速迭代本地积淀下来的自定义资产（特别是 `.maglev/` 和自定义的 Skills），同时依然能享受到 Maglev 官方引擎升级带来的生产力跃升。
- **Non-Goals**: 
  - 绝对不要强制覆盖用户的本地魔改文件。
  - 不做大而全的分布式包管理器体系，聚焦于对 Maglev 强相关资产 (`.agents/`, `.maglev/`) 的智能同步与冲突备份。

## 成功标准 (Success Criteria)
- **MVP**:
  - 提供一个可通过命令行（CLI / npm / python script 待权衡）一键触发的更新工具。
  - 只有属于“官方发行”且“本地无魔改”的文件被平滑更新。
  - 若遇本地魔改，系统需通过重命名、备份 (backup) 机制保护遗留资产，并在更新结束后通过直观日志告知用户。
  - 用户自定义的 `.maglev/` 数据需特别甄别：原则上以本地为准，仅增量补齐官方新增配置。
- **North Star**: 最终演化为一键式的 `maglev upgrade`，像 `brew` 或 `apt` 一样可靠、静默、防呆。

## 假设日志 (Assumptions Log)
| 假设 | 状态 | 来源 |
|------|------|------|
| 用户环境存在 Python/Node 这类运行时，故可派发脚本工具 | Confirmed | 会话确认 |
| 分发形式的选型须同时兼顾前/后端工程师（Python 与 NPM） | Challenged | 待确认具体的安装包形态 |
