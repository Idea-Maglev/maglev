---
reality_id: capability-evolution.verification.known-gaps
title: 能力进化已知缺口
owner_domain: capability-evolution
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 能力进化机制契约在静态材料中无法证明为已执行的缺口账本与关闭条件
  excludes:
    - 机制契约本身（属 implementation/evolution-cycle）
    - skill-runtime 域对象页面的缺口（归该域账本）
---
# 能力进化已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 生命周期执行 | evidence/competitive-registry.yaml | 观测养分回流不可宣称 | open |
| 侦察与迭代产物 | skill-scout / extension-evolver 契约 | 执行覆盖不可清点 | open |
| catalog 完备性 | private-catalog.yaml | 登记数 ≠ 技能总数 | open |
| 归属口径 | catalog ↔ r1 gate-a-record | 域归属分歧显式保留，无机械校验 | open |
| test-matrix | 本域 verification | 不产 test-matrix（裁决） | blocked-by-decision |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| insight 生命周期后半段（proposed → absorbed）无执行实例 | competitive-registry.yaml 全部 25 条 insight `status: open`，0 条 proposed/absorbed/superseded（本轮 status 字段统计）；机制要求 proposed 需 spec-designer 引用、absorbed 需改进合入 master | 静态盘点无任一实例，"观测养分已回流"不能成立 | 回流宣称被阻断 | `../evidence/competitive-registry.yaml` |
| 3 条 insight 缺研究报告锚点 | registry 中 KS-001、KS-002、HERM-001 的 `source_report: null`，其余 22 条均有指向路径 | 研究报告未归档 | 溯源链不完整 | `../evidence/competitive-registry.yaml` |
| 观测新鲜度无保证 | registry `last_researched` 最大值 2026-06-01（wanman），kiro 为 null；observatory SKILL.md 明文"由人主动触发，AI 不自动启动"，无调度/提醒设施 | 静态盘点无新鲜度机制 | 竞品状态可能陈旧 | `../evidence/competitive-registry.yaml` |
| skill-scout 执行记录不可静态清点 | SKILL.md 只说中间产物"以 Markdown/YAML 文件持久化"，references 无落盘路径约定（本轮检索无结果）；全仓未发现 SkillProfile / AdaptationSpec / PatrolReport 产物文件（本轮 find 无结果） | 无产物可清点 | 覆盖宣称被阻断 | `.agents/skills/skill-scout/SKILL.md` |
| extension-evolver 无本仓运行实例 | 全仓无任何 `maintenance/` 目录（本轮 find 无结果）；`.maglev/` 下无 extensions.lock | 无实例记录 | 迭代闭环未启动 | `.agents/skills/extension-evolver/SKILL.md` |
| catalog 完备性无机械校验 | catalog 自述"不是 `.agents/skills/` 的机械镜像"；本轮目录对比：9 个 private document integration 对象未登记，也无逐对象免登记裁决记录 | 无法区分"裁决免登记"与"漏登记" | 登记数不能当总数 | `public capability catalog` |
| 对象清单与页面归属两处口径需人工同步 | catalog 把四对象登记为 `top_level_capability: '能力进化'`，r1 gate-a-record.md 把其知识资产页归 skill-runtime 域；r2 Gate B 裁决"沿用既有槽位归属，本轮不重切边界"，分歧显式保留且无机械校验 | 双口径无一致性校验 | 归属查询需人工裁决 | `specs/90_archive/reality-knowledge-reverse-r1/gate-a-record.md` |
| 本域不产 test-matrix | r2 Gate B 裁决"test-matrix 仅在存在真实测试锚点时产出，不为均匀而虚构"；本轮 tests/ 盘点无 evolution-observatory / skill-scout / extension-evolver 测试锚点 | 裁决性缺席 | 覆盖矩阵留白 | `../verification/test-matrix.md`（未产出） |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 生命周期无实例 | "observatory 已为 Maglev 输送 N 个改进" | 无 absorbed 实例不得宣称回流已发生 | ✗"insight 优先级高说明已消化" |
| last_researched 陈旧 | 把 registry 的 version_tracked 当作竞品当前版本 | version_tracked 是登记时快照 | ✗"Superpowers 当前为 v5.1.0" |
| catalog 非机械镜像 | "Maglev 共有 N 个技能"类全量统计 | catalog 只登记进入治理的对象 | ✗"catalog 数 = 技能总数" |
| scout 无执行痕迹 | "所有已登记对象均已巡逻" | 无 PatrolReport 产物不得宣称覆盖 | ✗"契约存在所以执行过" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 生命周期后半段 | registry 出现第一条非 open insight（proposed 需填 proposed_spec 路径，absorbed 需填 absorbed_at 日期） | 继续新增 open 条目 | `../evidence/competitive-registry.yaml` |
| 研究锚点缺失 | 研究报告归档后回填 source_report 路径（创建侧补记录） | 会话内引用 | `../evidence/competitive-registry.yaml` |
| 观测新鲜度 | 新一轮 `research(observatory)` 提交更新 last_researched，或触发节奏条款落地 | 手工改日期 | `../evidence/competitive-registry.yaml` |
| scout 产物 | references 增加落盘路径约定，或出现首批持久化产物可清点 | SKILL 文本更新 | `.agents/skills/skill-scout/SKILL.md` |
| evolver 实例 | 首个真实 Extension Pack 按 `maintenance/records/YYYY-MM-DD-<topic>.md` 留记录并附 check/test-install 运行证据 | manifest 更新 | `.agents/skills/extension-evolver/SKILL.md` |
| catalog 完备性 | 每个未登记对象一条显式裁决，或机械对比校验 | 一次性人工核对 | `public capability catalog` |
| 归属口径 | Gate 裁决更新覆盖 multica 归属，或建立机械一致性校验 | 会话内口头对齐 | `specs/90_archive/reality-knowledge-reverse-r1/gate-a-record.md` |
| test-matrix | 上述技能出现真实测试锚点后按裁决产出 | 为均匀性虚构矩阵 | `../verification/known-gaps.md` |
