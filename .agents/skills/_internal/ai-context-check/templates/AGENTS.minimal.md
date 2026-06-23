<!-- maglev:managed:discipline -->
# 🔴 会话纪律（maglev-discipline）

> 本区块为 Maglev 框架的会话级强制层，所有 agent 在本项目工作时必须遵循。

## 三条不可灰度红线

1. **闭环验证**：交付前必须用证据（命令输出、文件 diff、可观察事实）说话，禁止用"已完成/已修复"代替证据
2. **事实驱动**：声明任何状态前必须有工具验证依据，禁止凭记忆/印象下结论
3. **穷尽方法**：宣告无法解决前必须走完 maglev-discipline 通用 5 步方法论

## 强制读取

进入任何主流程（`reality-sync` / `spec-designer` / `context-implementer` / `integrated-validator`）或本项目治理任务前，必须读取 `.agents/skills/maglev-discipline/SKILL.md`，并将其红线协议作为本会话默认背景纪律。

---
<!-- /maglev:managed:discipline -->

# AGENTS.md 最小草稿

- 默认使用简体中文回答。
- 项目中引用链接优先使用相对路径。
- 修改代码前，先阅读与当前任务直接相关的规格、说明或实现文件。

## 项目理解

- 本项目目标：`<一句话说明项目做什么>`
- 关键目录：
  - `<目录 1>`: `<用途>`
  - `<目录 2>`: `<用途>`
  - `.agents/`: Maglev 技能与 workflow
  - `.maglev/`: 规则与同步状态
- 当前主要入口：
  - `<任务入口或常用命令>`

## Maglev 使用方式

- 本项目已接入 Maglev。
- 当前主流程 skill runtime name：
  - `reality-sync`
  - `spec-designer`
  - `context-implementer`
  - `integrated-validator`
- 兼容 workflow 入口：
  - `/standup`
  - `/create-spec`
  - `/quick-dev`
  - `/validate-all`

## 协作约束

- 在信息不足时，先说明缺口，再继续执行。
- 写面向用户的文档时，优先回答“这是什么、为什么和我有关、我现在该怎么做”。
- 不要把只属于上游 Maglev 源仓库的现实直接当作当前项目事实。
