---
title: "Version Sync Tool - Vision"
status: "Superseded"
---

# 00 Vision: 版本维持与同步工具

> 本组 Spec 已被 `specs/20_evolution/active/maglev_distribution/` 吸收，现仅保留为历史演进记录。

## Core Philosophy (核心理念)
- **Empowerment over Replacement**: 提供能力而不是取代控制。用户的本地修改 (`Local Modification`) 必须受到一等公民的保护。
- **Invisible Magic**: 同步过程应当像呼吸一样自然，不需要用户安装庞大、反人类的依赖栈，开箱即用。
- **Defensive Engineering**: 在覆盖任何官方物料前，首先默认本地是危险的/被修改过的，严格执行对比与冲突剥离。

## User Persona (用户画像)
1. **End User (终端开发者)**: 期望能够运行一行极简的挂载代码/命令，就把陈旧的 Maglev 引擎全部更新，但“不要动我在 `.agents` 里加的自定义技能”。
2. **Maglev Creator (维护者)**: 期望有一个稳固的机制来分发自己的大版本引擎与技能集，能够确保接收方体验平滑。
