---
name: superpowers-bridge
description: Superpowers 桥接器。在实施阶段将代码类任务委托给 Superpowers 执行，收集结果回流 Maglev 验证体系。
metadata:
  formal_action_name: SP 桥接
  top_level_capability: 上下文实施
  system_layer: Core Flow Layer
  lifecycle_chain: main_flow
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: Maglev contributors
  last_updated: 2026-05-31
---

# Superpowers Bridge

## 概览 (Overview)

这是 Maglev 主流程中的**代码执行委托**技能。

当前说明：

- 结构动作名：`SP 桥接`
- 运行面名称：`superpowers-bridge`

它负责：

- 判断 spec 的交付物是否包含代码，决定执行路由
- 检测 Superpowers 是否已安装
- 构造启动指令，将 Maglev spec 上下文传递给 SP
- SP 执行完成后收集结果，交付给 integrated-validator

它不负责：

- 代替 spec-designer 做方案设计
- 代替 context-implementer 做非代码实施
- 管理 SP 的内部执行逻辑（TDD 纪律、subagent 分派由 SP 自治）
- 直接编写代码

它的交付结果至少应包含：

- 路由决策记录（代码 → SP / 非代码 → CI）
- SP 启动指令（已填充的模板）
- SP 执行结果摘要（变更文件、测试状态、review 结果）
- 可传递给 integrated-validator 的验证包

## 核心原则

**没有复杂度阈值。** 任何含代码交付物的 spec 都走 SP。SP 内部自行决定规模适配：
- 1 行代码修复 → 直接 TDD 循环
- 多文件功能 → subagent-driven-development

**"委托"= 注意力切换。** 不是 RPC 调用。当 bridge 激活后，agent 从阅读 Maglev skill 切换到阅读 SP skill（writing-plans → subagent-driven-development → TDD → finishing-a-development-branch）。

**SP brainstorming 完全跳过。** Maglev 已完成 requirement-convergence + spec-designer，SP 的 brainstorming 阶段是冗余的。

## 何时使用 (When to use)

- spec-designer 完成方案设计后，交付物包含代码时
- 用户明确说"用 SP 执行"时
- entry-router 判定为"直接实施"且涉及代码变更时

## 何时不使用

- spec 的交付物仅为文档、配置、分析、或 Maglev 自身 skill 维护 → 走 context-implementer
- Superpowers 未安装且用户选择跳过 → 回退到 context-implementer
- 需求或方案尚未明确时

## Skill 优先级协议

Maglev entry-router 始终是最高层入口。SP skill 仅在本 bridge 显式激活后才生效。

**绝对禁止**:
- SP 的 `using-superpowers` skill 自动触发
- SP 的 `brainstorming` skill 自动触发
- 任何 SP skill 绕过 Maglev 上游（requirement-convergence / spec-designer）直接启动

**执行链**:
```
entry-router → spec-designer → superpowers-bridge → [SP skills] → integrated-validator
```

## 交互模式 (Interaction)

### Phase 1: 路由判断

判断当前 spec 是否需要 SP 执行：

**"代码交付物"判据** (满足任一即可):
1. spec frontmatter 的 `delivery_type: code | mixed`
2. `files_to_modify` 中涉及源码文件 (`.py`, `.ts`, `.js`, `.go`, `.rs`, `.java` 等)
3. `02_design.md` / `03_plan.md` 含"实现"、"编写函数"、"创建模块"等关键词

**"非代码交付物"判据** (全部满足):
1. `delivery_type: docs | ops`
2. 仅涉及 `.md`, `.yaml`, `.json`（配置类）
3. 或属于 Maglev 自身 skill/协议维护（即使含代码片段，如 SKILL.md 中示例代码）

**手动覆盖**: 用户随时可以说"这个不用 SP"或"这个用 SP"，覆盖自动判断。

### Phase 2: SP 安装检测

检测 Superpowers 是否可用。按如下优先级检测：

1. 当前工作目录下是否有 SP skill 文件（如 `skills/writing-plans/SKILL.md`）
2. Agent 平台级插件是否安装（Claude Code plugin / Codex CLI plugin 等）
3. 用户 home 目录是否有 SP 全局安装

**检测失败时**: 向用户说明 SP 未安装，提供安装引导链接 (https://github.com/obra/superpowers)，并询问是否回退到 context-implementer。

### Phase 3: 构造启动指令

使用**启动指令模板**向 SP 传递上下文。SP 的 writing-plans 能消费自然语言 spec，无需格式转换。

**启动指令模板**:

```
== Superpowers 执行启动 ==

目标: {spec_title}
来源: Maglev spec cluster @ {spec_cluster_path}

== 设计输入 ==
- 设计文档: {spec_cluster_path}/02_design.md
- 需求文档: {spec_cluster_path}/01_requirements.md
- 项目技术栈: {tech_stack}
- 测试框架: {test_framework} (如 pytest/jest/go test)
- 已有测试: {existing_test_count} 个
- 代码入口: {entry_files}

== 跳过 ==
- 跳过 brainstorming（Maglev 已完成）
- 从 writing-plans 开始

== 约束 ==
- 遵循 TDD (superpowers:test-driven-development)
- 完成后使用 superpowers:finishing-a-development-branch
- 遇到 BLOCKED 时上报用户，不自行降级

== 补充上下文 ==
{additional_context}
```

**两种启动模式**:
- **Design-first** (默认): Maglev `02_design.md` → SP writing-plans → 执行
- **Plan-ready** (加速): 若 Maglev `03_plan.md` 已含细粒度任务+代码块 → 直接作为 SP plan → 跳过 writing-plans

### Phase 4: 结果回收

SP 的 `finishing-a-development-branch` 完成后：

1. **收集变更信息**:
   - `git diff --stat` (变更文件列表和规模)
   - 测试通过状态 (pass/fail + 覆盖率)
   - SP review 结果摘要

2. **构造验证包** 传递给 `integrated-validator`:
   - 原始 spec cluster 路径
   - 代码变更 diff
   - 测试执行结果
   - SP review 摘要

3. **状态记录**:
   - 在 spec frontmatter 回填 `sp_plan_path`
   - 记录执行状态 (completed / blocked / partial)

## 判定纪律 (Decision Discipline)

- 路由判断必须有明确依据，不凭直觉
- SP 检测失败必须向用户说明，不静默回退
- 启动指令必须填充完整上下文，不传空模板
- 结果回收必须等 SP 完成，不中途截断
- **背景纪律**：本 skill 执行期间持续遵循 `maglev-discipline` 红线（闭环验证 / 事实驱动 / 穷尽方法），每个 step 起始前先做 `[MAGLEV-DIAGNOSIS]` 自检

## 混合交付物处理

当 spec 同时含代码和非代码交付物时，采用**串行模式**：

1. 先由 `superpowers-bridge` 执行代码部分 (SP)
2. SP 完成后，`context-implementer` 执行非代码部分
3. 最后由 `integrated-validator` 统一验证

## SP Review vs Maglev Validator

两者互补，不冗余：

| 维度 | SP Review | Maglev integrated-validator |
|------|-----------|----------------------------|
| 粒度 | 任务级（每个 subagent 交付物） | 项目级（整体 spec 合规） |
| 关注点 | 代码质量、TDD 合规、bug | 四层交叉验证（需求↔spec↔代码↔测试） |
| 类比 | 保证每块砖合格 | 保证整栋楼合图纸 |

## 示例

用户："按这个 spec 实现功能。"
你："检测到 spec 含代码交付物（delivery_type: code），启动 SP 桥接流程。"

用户："这个只改文档和配置。"
你："交付物为纯非代码，路由到 context-implementer。"

用户："直接用 SP 执行。"
你："收到手动覆盖，无论 delivery_type 如何，启动 SP 桥接。"

## 常见错误

- 在 SP 未安装时静默回退（应显式告知用户）
- 传递空的或不完整的启动指令
- 试图管理 SP 的内部执行步骤（SP 自治，bridge 只做输入/输出桥接）
- 跳过结果回收直接进入下一阶段
- 在 spec 尚未完成时提前启动 SP
