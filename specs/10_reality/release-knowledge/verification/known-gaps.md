---
reality_id: release-knowledge.verification.known-gaps
title: 发行知识已知缺口
owner_domain: release-knowledge
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的发行知识事实
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 发行知识已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 发布渠道一致性 | 本页组全部 capability 页 | 0.7.4"已发布"类表述 | resolved（用户裁决：撤回发版准备，迭代未完；见上方撤回条目） |
| 证据链强度 | workflows / test-matrix | 归档→镜像同步的一手证明力 | open |
| 语义化质量 | business-rules / test-matrix | "面向用户"承诺的落地质量 | open |
| 索引双清单一致性 | static-coverage / use-cases | 历史版本入口完整性 | open |
| 历史覆盖 | static-coverage | "版本知识全覆盖"表述 | accepted（历史断层） |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 0.7.4 发版准备已撤回（裁决落地），trunk 归档与渠道重新一致 | 用户裁决：0.7.4 迭代未完；master revert 77e7626 一手可核（已推送）；f2a9ef1 保留于 origin/release | 归档是知识面事实，发布是渠道事实；撤回后 trunk 两边均为 0.7.3，不能互相推断的分歧已随撤回解除 | 本分支工作树因分叉时序仍含 0.7.4 准备产物，合并后以 trunk 为准；真发版时重走归档→渠道全链 | 用户在迭代完成后重新裁决 |
| 归档→镜像同步只有弱证据链 | r1 发版会话实录（未落档工件）；可对照事实：`.maglev_build/CHANGELOG.md` 与 0.7.4 归档当前内容一致；同步行为有测试覆盖 | 会话实录不可回放核验；当前一致性不证明当时同步过程 | "实录证实"只能保持弱证据链表述 | 下次发版观察复现 |
| 语义化质量无机器门禁 | SKILL.md DoD 为文本约束；tests/ 无对应断言 | 无校验实现，承诺不可机器验证 | "面向用户无过程叙事"依赖人工审阅 | 发版轮 review |
| 双产物内容一致性无门禁 | `_validate_changelog_artifacts` 只查存在性与登记，不比对内容 | 构建态与归档内容漂移不可被机器发现 | DoD 2"两份内容一致"不可机器判定 | 发版轮人工对照 |
| index 手工清单缺 0.4.3/0.4.4 | 一手盘点：文件存在、knowledge_records 有记录、手工链接清单无 | 双清单口径不一致 | 历史版本入口不唯一 | 补链或裁决以机器索引为准 |
| Draft 对比逻辑未实现 | step4 生成空骨架（脚本注释自认"此处由对比逻辑填入"） | Draft 覆盖度无法机器验证 | DoD 1"必须覆盖核心变化"不可机器判定 | delivery-runtime 域 |
| 早期版本（<0.1.4）无归档 | `docs/releases/` 序列起点 0.1.4（2026-03-21） | 无材料可查 | 历史断层 | 接受为历史事实 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| npm 未发布 | "0.7.4 已发布 / npm 可安装"（迭代完成前）；"trunk 归档存在"（撤回后） | 渠道状态无本域直接证据；trunk 归档已撤回 | ✗"归档存在所以已发布" |
| 弱证据链同步实录 | "同步机制已被实录证实"的强表述 | 未落档会话不升格为一手证据 | ✗"每次发版都会自动同步"（单实例 + 测试推演，非多版实录） |
| 无质量门禁 | "语义化合格率 X%"类任何统计 | 无校验不得产出统计 | ✗"DoD 存在所以质量达标" |
| 双产物一致性无门禁 | "构建态与归档必然一致" | 一致性靠人工 DoD，非机器保证 | ✗"校验通过所以两份内容相同" |
| 手工清单缺口 | "30 个版本入口齐全" | 分母与映射须区分双清单 | ✗"index 覆盖全部归档" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| npm 未发布 | npm registry 对 0.7.4 的可核验查询结果（发布后） | 归档存在、会话叙述 | `../release-knowledge/verification/test-matrix.md` |
| 弱证据链同步实录 | 下次发版落档的会话工件或再次复现的脚本输出 | 当前文件一致性的单次对照 | `../release-knowledge/capability/workflows.md` |
| 语义化质量 | 带对照的质量门禁实现或审阅记录 | 单人无对照的使用感受 | `../release-knowledge/capability/business-rules.md` |
| 双产物内容一致性 | 内容比对实现（校验或测试） | 单版本的人工对照 | `../release-knowledge/capability/business-rules.md` |
| 手工清单缺口 | index.md 补登记链接，或明确裁决以 knowledge_records 为准 | 保持现状不表态 | `../release-knowledge/verification/static-coverage.md` |
