---
reality_id: spec-knowledge-layering.verification.known-gaps
title: 规格分层已知缺口
owner_domain: spec-knowledge-layering
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的分层事实
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 规格分层已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 语义归属检查 | `../spec-knowledge-layering/verification/test-matrix.md`、capability 页组 | 分层边界遵守不可机检 | open |
| 扫描产物 digest 时效 | `../spec-knowledge-layering/verification/test-matrix.md`、`../spec-knowledge-layering/implementation/data.md` 及本页组 frontmatter | evidence_digest 复核结论 | open |
| 愿景层新鲜度 | `../spec-knowledge-layering/capability/overview.md`、`../spec-knowledge-layering/implementation/architecture.md` | 愿景漂移检测 | open |
| status 时间戳漂移 | `../spec-knowledge-layering/implementation/data.md` | "最后更新"可信度 | open |
| 事实源口径差 | `../spec-knowledge-layering/capability/overview.md`、`../spec-knowledge-layering/capability/business-rules.md` | 层数/规模表述 | open |
| 草稿模板执行质量 | `../spec-knowledge-layering/capability/workflows.md` | draft 三态策略与 zone 模板的填充质量 | open |
| 归档双口径优先级 | `../spec-knowledge-layering/capability/business-rules.md`、`../spec-knowledge-layering/capability/workflows.md` | 废弃操作是否必须先判断可提取结论 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 分层语义归属无机器检查 | `.agents/skills/_internal/reality-admission/core.py` 角色边界声明（只查 frontmatter 身份、证据存在/digest、profile 声明，不规定章节/措辞/内容） | admission 自我定位为辅助验证器，语义归属被显式排除 | "演进内容误入现状层""现状写过程叙事"只能靠人工/对抗审查发现 | governance-quality 审查面 |
| 本页组两处 evidence digest 已过期 | frontmatter 声明 `specs/INDEX.md`（d267dc…）与 `specs/20_evolution/INDEX.md`（5ac6f8…）的 digest 与当前文件（722dc6…/93a7de…）不一致；两者为 track_scan 产物 | INDEX 的 knowledge_records 随结构变化累积刷新，文件级 digest 必然随后续 scan 过期 | strict 重跑 admission 会报 evidence_digest FAIL；正文引用的结构数值（stats.total 61、child_count 60/535）已与当前文件核对一致 | 结晶收口时以候选 commit 重绑 evidence_refs |
| 00_vision.md 无独立槽位页 | 目录盘点：单文件层，仅根 entity-index 文件记录承载 fingerprint/freshness | 根 INDEX 只证明"文件未变"，不证明"愿景仍准确"；修订触发是维护规则自觉 | 愿景漂移只能靠人工复核 | vision 修订流程提案 |
| status.md"最后更新"人工维护 | 多主题 status.md 的时间戳为手写引用块，无机器写回与校验 | 无检查比较时间戳与内容/git 活动 | 滞后时间窗不可量化 | 逆向 R 类发现累积 |
| `specs/README.md` 地图文本滞后 | README 写 20_evolution"尚无内容"，实际 active/ 有 9 个主题目录 | README 为手工 Map，未随目录演进刷新 | 新读者可能低估演进层规模 | specs 根 README 维护提案（不在本页组修改范围） |
| `internal Reality/positioning.md`"3 层 specs/"与四层口径差 | positioning.md 核心能力域表 vs `specs/README.md` 四层标准 | 两源并存，无法静态判定哪一方是笔误 | 引用层数时须注明来源口径 | 定位文档维护提案 |
| draft 模板执行质量无验证记录 | `.agents/skills/_internal/spec-pipeline/draft/unified-draft-template.md` 与 step-02 为参考文本，全仓无对应验证记录 | 模板存在性可证明，填充质量不可静态证明 | 草稿质量只能靠人工审阅 | 观测类主题 |
| abandon 与 crystallization 归档双口径未决 | `.agents/skills/_internal/spec-pipeline/crystallize/step-99-abandon.md` 直接移动归档；crystallization SKILL 要求先提取结论再归档 | 两机制触发条件不同（明确废弃 vs 完成收口），但"废弃前是否强制判断可提取结论"无契约 | 废弃操作可能绕过"先写回"要求 | `../spec-knowledge-layering/capability/business-rules.md` 决策表 B |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 语义归属无检查 | "分层边界 100% 遵守" | 无检查不得断言全覆盖 | ✗"admission 通过 = 内容归层正确" |
| digest 过期 | "页面证据永远与被引文件一致" | 文件级 digest 随扫描刷新失效 | ✗"手工改写 digest 数字使其匹配"（须重走候选 commit 登记） |
| status 时间戳 | "最后更新 = 实际最后修改时间" | 无机器写回与校验 | ✗"时间戳新鲜 = 主题活跃" |
| 愿景层 | "愿景与现状自动一致" | 无槽位页与专属门禁 | ✗"根 INDEX 有 fingerprint = 愿景被验证" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 语义归属 | admission 或新增检查器明示承担语义归属判定，并给出检查记录 | 希望性描述 | `../spec-knowledge-layering/verification/test-matrix.md` |
| digest 时效 | 结晶收口候选 commit 重新登记 evidence_refs（新 digest）且 admission 重跑 accepted | 手工改数字、只改正文不改 frontmatter | `../spec-knowledge-layering/verification/test-matrix.md`、`../spec-knowledge-layering/implementation/data.md` |
| 愿景层 | 00_vision.md 获得槽位页或专属检查（有静态锚点的新机制） | 一次性人工阅读结论 | `../spec-knowledge-layering/capability/overview.md` |
| status 时间戳 | 引入时间戳机器校验或写回（有锚点） | 抽查若干文件无异常 | `../spec-knowledge-layering/implementation/data.md` |
| README 滞后 | `specs/README.md` 更新 20_evolution 描述 | 只改目录不改地图 | `../spec-knowledge-layering/implementation/architecture.md` |
| 层数口径 | positioning.md 或 specs/README.md 明确"3 层/4 层"口径关系 | 第三方转述 | `../spec-knowledge-layering/capability/overview.md` |
| 草稿模板质量 | 带时间戳的草稿产出样本 + 与模板要求的比对结论 | 单次无对照的使用感受 | `../spec-knowledge-layering/capability/workflows.md` |
| 归档双口径 | crystallize 契约或治理规则明示两条路径的适用边界与优先级 | 推测性统一说法 | `../spec-knowledge-layering/capability/workflows.md` |

缺口登记原则：只登记"查过且无法证明"的项；未查过的对象不进入本页。
