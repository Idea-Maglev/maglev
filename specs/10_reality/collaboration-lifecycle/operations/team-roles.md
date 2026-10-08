---
reality_id: collaboration-lifecycle.operations.team-roles
title: 协作角色映射与项目团队配置
owner_domain: collaboration-lifecycle
owner_slot: operations
fact_type: operational_surface
knowledge_status: established
scope:
  includes:
    - 项目看板 VO/TP/XG 铁三角的阶段-角色状态映射机制与项目级/spec 级团队配置规则
  excludes:
    - 排期、工时、人员绩效与外部系统集成（project-board 明确不负责）
    - Multica 小队 Agent 角色拓扑（属 capability/multica-squad-kit.md）
---

# 协作角色映射与项目团队配置

## 1. 责任范围（主体-资源-动作）

| 主体/角色 | 资源 | 动作 | 业务依据 | 执行依据 |
| --- | --- | --- | --- | --- |
| VO（Value Owner） | 活跃需求 | 主导需求收敛阶段；在方案设计及以后阶段标记已完成 | `.agents/skills/project-board/references/step-03-map-roles.md` 阶段映射表 | `project-board` Step 3 读取配置后渲染 |
| TP（Tech Pilot） | 活跃需求 | 主导方案设计与编码实施阶段 | 同上 | 同上 |
| XG（Experience Guardian） | 活跃需求 | 主导综合验证阶段 | 同上 | 同上 |
| `project-board` | `specs/20_evolution/board.md` 与 `status.md` | 映射并渲染角色状态；只观测，不驱动流程 | `.agents/skills/project-board/SKILL.md` 负责与不负责段 | 4 步工作流（扫描 → 阶段判断 → 角色映射 → 渲染持久化） |

## 2. 阶段-角色状态决策矩阵

| 阶段 | VO | TP | XG | 策略锚点 |
| --- | --- | --- | --- | --- |
| 需求收敛 | 主导中 | 待介入 | 未参与 | `step-03-map-roles.md` 阶段映射表 |
| 方案设计 | 已完成 | 主导中 | 待介入 | 同上 |
| 编码实施 | 已完成 | 主导中 | 待介入 | 同上 |
| 综合验证 | 已完成 | 已完成 | 主导中 | 同上 |
| 结晶归档 | 已完成 | 已完成 | 已完成 | 同上 |

阶段判断不确定时，看板标记"待确认"，不默认归类（`.agents/skills/project-board/SKILL.md` 判定纪律；`references/stage-evidence-rules.md` 要求文件存在之外交叉验证内容与下游证据）。

## 3. 配置实现与覆盖规则

| 配置层 | 位置 | 行为 | 状态 |
| --- | --- | --- | --- |
| 项目级 | `.maglev/team.yaml` 的 `team.vo/tp/xg` | 提供 `name` 与 `title`；`name` 为空字符串视同未配置，看板展示角色代号或 `(未配置)` | established |
| Spec 级 | `{spec_dir}/team.yaml` 或 `{spec_dir}/00_intent.md` 的 `## 角色` 章节 | 存在时覆盖项目级配置 | established（`step-03-map-roles.md` 覆盖规则） |
| 本仓当前值 | `.maglev/team.yaml`：VO `title: "Value Owner (产品经理)"`、TP `title: "Tech Pilot (技术领航者)"`、XG `title: "Experience Guardian (测试工程师)"`；三个 `name` 均为空字符串 | 看板按未配置处理，展示角色代号 | established（登记事实） |

## 4. 不适用或未知边界

| 判断 | 范围与依据 | 不能说明什么 | 深挖 |
| --- | --- | --- | --- |
| 边界 | 角色映射仅服务看板展示 | 不构成排期、绩效或人员管理数据 | `../capability/overview.md` |
| 边界 | 本仓当前无任何 spec 级 `team.yaml` 覆盖被本页登记 | 不证明未来 spec 不引入覆盖 | 各 spec 自身目录 |
| unknown | 三个角色当前均未配置具体人员，无法核对人名与职责的实际对应 | 本页不声明任何真实人员承担 VO/TP/XG | 填写 `.maglev/team.yaml` 后由看板渲染验证 |

## 5. 证据与状态绑定

| 结论 | 知识状态 | 证据充分度 | 缺失或冲突 | owner 页面/深挖 |
| --- | --- | --- | --- | --- |
| VO/TP/XG 三角映射机制与阶段矩阵 | established | 契约级（SKILL + step 参考文件） | 无 | `../capability/overview.md` |
| 本仓团队配置为空名登记 | established | 配置文件直读 | 无 | `.maglev/team.yaml` |
| 角色状态在真实看板渲染中的呈现 | established（契约级） | 渲染规则可定位 | 未收集渲染样本运行记录 | `specs/20_evolution/board.md` |
