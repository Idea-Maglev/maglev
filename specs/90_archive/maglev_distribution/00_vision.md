---
title: "Maglev Distribution & Installation - Vision"
status: "Archived"
---

# 00 Vision: Maglev 智能体宇宙的发放与连接

> 本组 Spec 已完成其历史使命，现状已结晶到 `specs/10_reality/`，本文件仅作为历史设计归档保留。

## Spec Lineage (演进关系)
- 本 Spec 曾是分发主线的核心设计文档。
- 早期的 `version_sync_tool` 定义了零依赖同步、四态更新、`sync_state.json` 与冲突备份等基础能力。
- 随着问题空间从“同步工具”扩展到“初始化 + 更新 + 发版 + 多入口包装”，上述能力已被统一吸收进当前的 Distribution Engine。

## Core Philosophy (核心理念)
- **Frictionless Entry (无感接入)**：让天下所有的存量/增量业务代码，只需一行口令即可“接入大脑 (Brain-Plugged)”。剥离手工下载 Zip 的作坊式体验。
- **Immutable Sandbox (引擎沙盒的绝对纯洁)**：Maglev 框架下发的规则与技能（`.agents`, `.maglev`），对使用者而言必须是不可被污染的公域抽象（SSOT），它应当像一个运行在你工程侧边的守护进程，而不是混入你代码中的泥石流。
- **Meta-Circular Evolution (造物主的优雅闭环)**：我们在开发 Maglev 本身时，绝不用“Ctrl+C / Ctrl+V”去组装教程与代码。框架本身的沉淀（specs）与分发（release）必须完全通过自动化的编译流水线实现解耦。

## User Journey (用户旅程图景)
1. **The Click**: 用户在控制台输入 `curl ... | bash` 或 `npx maglev-cli`。
2. **The Question**: 终端黑屏绿字问用户：“你的前端在哪里？你的后端长啥样？”
3. **The Light**: 系统自动生成 `.agents`, `.maglev` 与 `specs/` 骨架及元数据映射。
4. **The Whisper**: 控制台高亮提示：“Maglev 环境就绪。现在，你可以敲入 `/tutor` 与我对话。”
