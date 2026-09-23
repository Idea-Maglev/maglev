---
reality_id: knowledge-sedimentation.verification.known-gaps
title: 知识沉淀已知缺口
owner_domain: knowledge-sedimentation
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的沉淀能力事实
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 知识沉淀已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 运行时执行 | 本页组全部 capability 页 | 检查/归类执行率结论 | open |
| canonical 实例化 | capability 页 + static-coverage | 实例与 canonical 一致性结论 | open |
| 内容新鲜度 | `docs/thinking/` 各段目录 | thinking 层是否落后实践 | open |
| 跨域语义 | `../spec-knowledge-layering/capability/workflows.md`（M6）/ 文档治理 | 反哺完成度；docs/thinking 双域角色 | open |
| 依赖完整性 | SKILL.md 依赖声明 | 依赖图可信度 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 9 段归类实际执行率（会话是否真的触发检查） | SKILL 契约 + 全仓无会话级遥测 | 契约证明"应何时检查"，不证明"是否真的检查"；触发按需、无强制门禁 | 沉淀体系可能形同虚设 | 观测类主题 |
| segments_source 实例标注缺失 | SKILL.md 要求实例文件头标注；实测 `docs/thinking/INDEX.md` 头部无该字段 | 意图条款与落盘现状并列存在，无履行证据 | 无法机器核验实例与 canonical 的漂移 | 项目侧补标注（`segments-canonical.md`：实例同步由项目负责） |
| 各段内容新鲜度 | 段目录 INDEX freshness: current 是索引器收录状态 | 索引状态不构成内容质量证据 | thinking 层结论可能落后实践 | knowledge-check 轮次 |
| thinking→specs 反哺完成度 | `../spec-knowledge-layering/capability/workflows.md` 流转图证明交接点存在 | 反哺是跨能力工作流，本页组无其执行记录 | 哪些"为什么"还没变成"是什么"不可统计 | spec-pipeline 主题 |
| 贡献记录与思考资产的对账缺失 | `references/step-02-audit-records.md` 只核对 `contributors/contribution_log.md` 是否更新；该日志记录 Intent/Workload，不校验思考文档本身 | "贡献记录已更新"不等于"对应思考已落 docs/thinking 对应段" | 贡献记录存在可能掩盖沉淀缺口 | knowledge-check 轮次 |
| 检查产物无持久化格式 | SKILL.md"交付结果"段只定义会话内交付（资产清单/完整性/边界/缺口），references 无输出落盘模板 | 交付物定义存在，但无落盘格式与位置约定 | 检查结果只活在会话里，无法事后审计执行率 | 观测类主题 |
| contribute_methodology 依赖失效 | SKILL.md"依赖与集成"列出该对象；`.agents/skills/` 与 `public capability catalog` 均无此对象；`specs/90_archive/skill_structural_upgrade/design/03at_non_core_skill_retention_decision_v1.md` 记录其已删除 | 依赖声明指向已删除对象，SKILL.md 未随清理同步 | 按 SKILL.md 排查依赖的会话会扑空；依赖图失真 | skill 治理主题 |
| `docs/thinking/` 双域角色无调和说明 | 文档治理登记 id=historical-thinking（class=historical / disposition=reference-only / successor=internal Reality/README.md）vs AGENTS.md 知识沉淀注记（持续写入 `docs/thinking/`） | 两域对同一路径的角色描述无互相引用或调和条款 | 新会话可能误读 `docs/thinking/` 为只读历史语料 | 治理裁决类主题 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 无运行记录 | "归类执行率 X%"类任何统计 | 无数据源不得产出统计 | ✗"9 段目录齐全所以沉淀在发生" |
| 无 segments_source 标注 | "实例与 canonical 一致"表述 | 无校验锚点不得宣称一致 | ✗"canonical 存在所以实例未漂移" |
| freshness: current | "段内容未过时"结论 | 索引状态不是内容质量 | ✗"索引 current 所以思考都还有效" |
| 双域角色未调和 | "docs/thinking 已废弃/只读"或"治理登记不适用"任一单边结论 | 两域证据并列，裁决前不得取一边 | ✗"治理标 historical 所以沉淀已停" |
| 贡献记录对账缺失 | "贡献记录在更新所以沉淀在发生"结论 | 记录更新与思考落盘是两类事实 | ✗"contribution_log 有新行说明知识都沉淀了" |
| 无产物落盘格式 | "检查产物已归档"表述 | 无落盘格式定义不得宣称产物持久化 | ✗"检查过了所以有留痕" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 执行率 | 带时间戳的会话检查样本记录 + 与 `docs/thinking/` 新增文档的人工比对结论 | 单次"我记得检查过"的使用感受 | `../knowledge-sedimentation/verification/static-coverage.md`、`../knowledge-sedimentation/verification/test-matrix.md` |
| 实例标注 | INDEX.md 文件头出现 segments_source 标注，或项目级 sync 校验脚本及其输出 | 计划性语言（"将补上"） | `../knowledge-sedimentation/verification/static-coverage.md` |
| 内容新鲜度 | 段文档与当前 specs/实现的人工比对结论 | freshness 字段本身 | `../knowledge-sedimentation/capability/workflows.md` |
| contribute_methodology 依赖 | SKILL.md 依赖声明更新（移除或恢复该对象）+ 目录/catalog 佐证 | 仅归档记录（现状仍失真） | —（跨域，属 skill 治理） |
| 贡献记录对账 | 检查契约增补"贡献记录更新与对应思考落盘"的对账动作 | 只看 contribution_log 是否有新行 | `../knowledge-sedimentation/capability/workflows.md` 步骤 2 |
| 产物持久化 | SKILL/references 增补检查产物的落盘格式与位置约定 | "建议落盘"类计划性语言 | `../knowledge-sedimentation/verification/test-matrix.md` 未覆盖表 |
| 双域角色 | 治理域或本域任一方增补调和条款并互相引用 | 临时口头解释 | `../spec-knowledge-layering/capability/workflows.md`、`specs/_meta/documentation-governance.json` |
