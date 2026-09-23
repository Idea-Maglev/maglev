---
reality_id: machine-index-engine.verification.known-gaps
title: 索引引擎已知缺口
owner_domain: machine-index-engine
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 当前无法证明的引擎行为与证据漂移
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 索引引擎已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 证据漂移（R1） | dogfooding.yaml；`../machine-index-engine/capability/business-rules.md`（导航门禁/升级链意图来源） | 自举样例与升级链设计意图的静态锚点 | open |
| verify 失败的运行时处置 | `../machine-index-engine/capability/use-cases.md` 场景 1；reality-sync 消费面 | preflight 失败后阻断/降级/忽略结论 | open |
| scan 写回失败分支 | `../machine-index-engine/operations/errors.md`；`../machine-index-engine/operations/state-model.md` | 写回中断后产物一致性结论 | open |
| code-tree 启用决策 | `../machine-index-engine/implementation/architecture.md`；`../machine-index-engine/operations/configuration.md` | 代码索引能力的可用性结论 | open |
| verify/scan 入口行为的测试保护 | `../machine-index-engine/verification/test-matrix.md`；`../machine-index-engine/verification/static-coverage.md` | exit 门禁语义的回归保护结论 | open |
| 收据 `confidence` 语义误用检测 | `../machine-index-engine/interfaces/cli.md`；`../machine-index-engine/verification/test-matrix.md` 未覆盖表 | `navigation_confidence` 是否被误消费为业务置信度 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| R1 证据漂移：dogfooding.yaml 的 expected_paths/expected_any_paths 指向 2026-07-21 导航门禁设计与复盘文档（`navigation-gate-scope-design.md`、`navigation-insufficient-escalation-design.md`、`navigation-governance-chain-closure-note.md`、`navigation-governance-dogfooding-sample.md`），工作树未发现 | dogfooding.yaml `tasks:` 段；docs/thinking/20_architecture/ 与 70_retrospective/ 目录清单（创建于 c9ba9d1，消失点疑似在未被逐文件追溯的合并/归档提交中） | 引用路径的文件不存在，样例无法作为可复跑的自举证据；升级链设计意图失去设计文档锚点，只能以 SKILL.md 现行文本与测试断言为界 | 自举验证样例部分失效（涉及 4 个任务的 expected 路径；其余任务锚点仍在） | 逆向轮 findings R1；建议修 dogfooding.yaml 或恢复文档 |
| verify 失败在启动流程中的真实处置（阻断/降级/忽略） | reality-sync SKILL.md 仅 intent 层引用（"启动期漂移哨兵"段定义 surface 行为）；无运行频率与真实处置记录 | 消费方行为属运行时，本轮 static_read 无法证明实际执行 | preflight 失败的实际影响只能按契约理解 | reality-sync 域页（批次3） |
| scan 写回失败的分支行为（重试/回滚/部分状态） | 脚本三 handler 正常路径均返回 0；材料未记录失败分支 | 无实现分支或测试可查 | 写回中断后的一致性无法评估 | index-librarian 演进主题 |
| code-tree 启用决策 | registry.example.code-tree.yaml 存在模板但本仓未登记 | 成本收益决策无记录 | "本仓代码索引不可用"是登记事实，不是评估结论 | index-librarian 演进主题 |
| verify/scan 入口 handler 无专项测试 | 两个测试文件的方法清单均未覆盖 verify/scan 入口 | 测试直接覆盖 `common/` 构件与收据逻辑 | exit 门禁语义无回归保护 | `../machine-index-engine/verification/test-matrix.md` 未覆盖表 |
| 收据 `confidence` 的消费边界无检测 | SKILL.md 将其限定为 `navigation_confidence`（不作业务证据/范围许可/语义置信度）；测试清单无消费方侧断言 | 语义限定只有契约文本，无误用检测设施 | 误用无法被机器发现，只能靠人工审查 | `../machine-index-engine/verification/test-matrix.md` 未覆盖表 |

缺口登记原则：只登记"查过且无法证明"的项；未查过的对象不进入本页（避免以未知冒充缺口）。

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| dogfooding 样例漂移 | "导航门禁升级链已按设计文档落地并通过自举验证" | 引用文档不存在时，设计意图与自举验证均不可引用 | ✗"dogfooding.yaml 里有 expected_paths 所以升级链已验证" |
| 无运行记录机制 | verify 触发频率、preflight 失败率、输出采纳率类任何统计 | 无数据源不得产出统计 | ✗"preflight 每次会话都跑且可靠" |
| scan 写回失败分支未知 | "scan 失败会自动回滚/可安全重试" | 未定位失败分支不得声称恢复语义 | ✗"scan 是幂等的所以中断无害" |
| code-tree 未启用且无决策记录 | "代码索引能力不可用/已废弃" | 未启用是登记事实；启用与否的评估结论缺决策记录 | ✗"code-tree 已被放弃" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| R1 证据漂移 | dogfooding.yaml 指向的 4 份文档恢复入库，或 dogfooding.yaml 更新为现存路径并复跑自举样例通过 | 仅删除失效条目而不提供替代锚点 | `../machine-index-engine/operations/configuration.md`；`../machine-index-engine/capability/business-rules.md` |
| verify 失败的运行时处置 | reality-sync 域页记录 preflight 失败分支的可定位处置行为（带静态锚点），或带时间戳的运行样本记录 | 单次无对照的使用感受 | `../machine-index-engine/capability/use-cases.md` |
| scan 写回失败分支 | 脚本失败分支实现 + 测试，或明确"无恢复语义"的设计记录 | 推测性描述 | `../machine-index-engine/operations/errors.md` |
| code-tree 启用决策 | 启用/不启用的决策记录（含成本收益依据），或本仓启用该 track 的登记变更 | 仅有模板文件 | `../machine-index-engine/operations/configuration.md` |
| verify/scan 入口测试 | 覆盖 exit 分支的 handler 测试入库并映射进 test-matrix | 仅手工运行一次的输出 | `../machine-index-engine/verification/test-matrix.md` |
| 收据 `confidence` 误用检测 | 消费方测试断言"confidence 不被当作业务证据消费"，或质量层登记该检测规则 | 契约文本重申 | `../machine-index-engine/interfaces/cli.md` |
