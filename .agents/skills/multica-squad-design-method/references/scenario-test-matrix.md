# Scenario Test Matrix

每支小队至少要覆盖以下场景。L1 可以是设计审查，L2 需要静态测试或模板断言，L3 需要真实 Runtime Proof。

| 场景 | L1 设计证据 | L2 模板证据 | L3 运行证据 |
|---|---|---|---|
| 协调/路由责任角色选择下一责任人 | 角色拓扑说明 | 路由指令或测试断言 | 真实委派评论 |
| 共享产物准入 | 不可变版本和接收方准入说明 | 版本/准入断言 | 接收方同步回执 |
| 精确 mention 触发 | 协同契约说明 | 模板包含 mention 规则 | Task 被目标 Agent 接收 |
| 禁止裸 `@name` | 禁止事项 | 测试断言 | 无裸 mention 触发路径 |
| 成员 completed Handoff | Handoff 格式 | Agent 指令包含终态 Handoff | 成员发布 completed Handoff |
| 成员 blocked Handoff | 阻塞规则 | Agent 指令包含 blocked 规则 | 成员发布 blocked Handoff |
| 禁止横向委派 | 协同边界 | Agent 指令包含禁止项 | 成员没有自行派发下游任务 |
| 一次性只读并行审查 | 例外条件 | 路由责任角色授权规则 | 授权场景可追踪 |
| 一次性人工动作 | 停止条件 | `human_action`/`ready_to_close` 断言 | 人类动作完成回执 |
| 人类角色路由 | 角色、成员描述和顺序 | 多角色、第一顺位和 `human_targets` 断言 | 责任承载回执 |
| 独立复审 | 反馈和复审条件 | Review Packet 与独立复审断言 | 修复后独立角色复审 |
| 写入门禁 | Adapter Contract | 模板或测试断言门禁 | 写入前批准与快照可追踪 |
