---
name: step-03-collaboration-contract
description: 补齐 Maglev 专属双路径入口、Bridge 边界和写入门禁
next_step: references/step-04-template-authoring.md
---

# Step 3: Maglev Collaboration Boundaries

## 目标

在通用协同契约之上，补齐 Maglev 专属的 `entry-router` 双路径、Bridge 自包含模式、Work Graph / lease 写入门禁和验证要求。

## 必须继承的通用协议点

1. Coordinator 是唯一默认路由者。
2. Coordinator 每轮只委派一个主责任角色。
3. 委派必须使用 Squad Roster 的精确 mention markdown：`[@名称](mention://agent/<uuid>)`。
4. 必须发布新评论触发；不得编辑旧评论补 mention。
5. 不得使用裸 `@name`。
6. 成员只响应属于自己的新委派 Task。
7. 成员完成、阻塞或失败时必须发布标准终态 Handoff。
8. 成员默认交回 Coordinator 评估。
9. 成员不得横向互相委派。
10. 只有 Coordinator 委派评论明确授权“一次性只读并行审查”时，成员才可以 mention 指定协作者。
11. 自动接力失败时按顺序检查：
    - 目标 Agent 是否对 Workspace 可调用。
    - Runtime 是否在线。
    - mention markdown 是否为 `mention://agent/<uuid>` 或 `mention://squad/<uuid>` 精确格式。
    - 评论是否为新建评论而不是编辑旧评论。
12. 写入任务必须具备 Work Graph、lease、基线提交、允许文件范围和项目负责人批准。

## 通用契约的 Maglev 实现映射

- 共享产物必须关联不可变 commit、声明的 ref 和 `receiver_sync`；接收方未确认时不得派发依赖该产物的执行任务。
- Coordinator 消费 Handoff 时必须保留 `decision_fingerprint` 和调度预算；没有新增证据时转为有限的 `blocked`、`awaiting_external` 或 `human_action`，完成时使用 `ready_to_close`。
- 人类动作先消费 `shared_contract.human_role_routing`，再按角色、成员描述和顺序生成目标；没有人类动作时保留空 `human_targets`。
- 审查输入必须包含生产者 skill 的只读来源、Review Packet 和共享阶段最低门槛；反馈只路由一个主修复角色，修复后由独立角色复审。

## Maglev 标准 Handoff

```markdown
## Maglev 小队 Handoff

- 状态：completed / blocked / failed
- 当前角色：
- 当前阶段：
- 输入证据：
- 输出产物：
- 事实结论：
- 推断结论：
- 未知项：
- 是否修改文件：
- 修改范围：
- Git 基线：
- 验证命令：
- 阻塞原因：
- 下一建议责任人：
- 是否需要项目负责人确认：
```

## Maglev 专属双路径

- 若 `.agents/skills/entry-router/` 可加载，才允许声称进入仓库 Maglev 能力链路。
- 若仓库尚未初始化或 `entry-router` 不可加载，只能进入 Bridge 自包含准备模式。
- 准备模式不得调用不存在的仓库 skill，不得修改业务代码，不得声称主流程已可运行。
- 初始化或治理资产写入完成后，必须重新验证 `entry-router`。

## Maglev 写入门禁

写入 `.agents/`、`specs/`、`docs/` 或其他治理资产前，必须具备：

- Work Graph。
- lease。
- 基线提交。
- 允许文件范围。
- 项目负责人批准。
- 写入前后 Git 快照。

没有这些证据时，只能给出建议或 blocked Handoff。

## 输出

- Maglev Bridge 协议段落。
- Maglev Handoff 格式。
- Work Graph / lease 写入门禁。
- 自动接力失败排查顺序。
- `entry-router` 双路径说明。
