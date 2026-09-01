---
name: step-02-role-topology
description: 将通用角色拓扑映射到 Maglev Squad Kit
next_step: references/step-03-collaboration-contract.md
---

# Step 2: Maglev Adapter Mapping

## 目标

把通用角色拓扑映射到 Maglev Squad Kit 的 `manifest.yaml`、`squad.json` 和 `agents/*.json`，同时保留通用协同契约。

## 动作

1. 先完成通用责任到 Maglev 角色的映射：
   - 通用 `routing_responsibility` → Maglev `coordinator`，由 `leader_role` 和 `agents/coordinator.json` 同时声明。
   - 该映射只表示 Maglev Adapter 的具体实现；其他小队可以将同一职责映射到不同的协调角色名称。
2. 将通用角色字段映射到 Maglev 文件：
   - `role` → `manifest.yaml` role id。
   - `display_name` → Agent `name_template`。
   - `responsibility` → Agent `description` 与 `instructions`。
   - `read_write_boundary` → Agent 禁止事项与写入门禁。
   - `default_return` → 标准 Handoff 的下一步交回规则。
3. 检查 Maglev Adapter 特有字段：
   - `member_role_description`
   - `concurrency_limit`
   - `entry_conditions`
   - `outputs`
   - `next_owner`
4. 检查权限与运行约束：
   - 谁需要写入治理资产。
   - 谁必须只读。
   - 谁需要 Workspace 可调用权限。
   - 哪些角色可在 Coordinator 授权下并行。
5. 设计名称：
   - 模板标题可以包含 `Maglev {project_slug}`。
   - 展示名会做 UI 友好归一化。
   - 受管身份不得依赖展示名称，必须依赖 managed marker 和 lock。

## 输出

| role | Maglev 文件 | 职责 | 读写边界 | entry_conditions | outputs | next_owner |
|---|---|---|---|---|---|
| coordinator | manifest + agents/coordinator.json | 选择下一责任角色 | 只读 | 已获得准入证据 | 委派评论、评估记录 | selected role |
