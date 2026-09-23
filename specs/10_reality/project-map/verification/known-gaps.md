---
reality_id: project-map.verification.known-gaps
title: 项目地图已知缺口
owner_domain: project-map
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的地图行为
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# 项目地图已知缺口

## 1. 缺口范围

缺口分两类：现役实例与运行采样类（需要显式生成/运行才能关闭），测试与机制盲区类（需要补测试或补机制才能关闭）。

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 现役地图实例 | docs/ATLAS.md 及本页组所有引用现役实例之处 | 地图内容是否反映当前结构 | open |
| `--check` 运行时判定 | `../project-map/operations/configuration.md` 处置指引 | 过期判定的实测形态 | open |
| 测试盲区 | test-matrix / static-coverage | CLI 层与 Low 置信度结论 | open |
| 时序耦合 | operations 刷新时机 | 结晶→看板→地图链路的执行频率 | open |
| 渲染断言盲区 | test-matrix / static-coverage | Reality 拓扑节与证据来源节的渲染正确性 | open |
| 写盘机制 | implementation/project-map.md、operations | 并发与中途失败下的产物一致性 | open |

## 2. 缺口账本

每行给出已查依据与不可成立的理由；"为什么不能成立"是本页核心列——缺口不是"未知"，而是"已知为何无法下结论"。

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 现役 docs/ATLAS.md 生成于 source_commit `15dd0db` 且 source_dirty=true（2026-08-17T11:08:17Z），早于本轮逆向变更 | docs/ATLAS.md frontmatter | 地图是派生视图，内容只反映生成时点；此后 0.7.3/0.7.4 与逆向轮的结构变更未反映 | 消费方不得把现役 ATLAS 当作当前结构事实 | 需显式重生成（本逆向轮不自动写地图） |
| `--check` 在本轮变更后的实际判定结果 | 本轮未运行生成/检查（避免与逆向候选混淆） | 未运行即无实测证据 | 无法确认现役地图按指纹规则是否判过期 | 候选提交后运行验证 |
| "结晶→看板→地图"时序耦合无执行记录 | 静态盘点无运行记录机制 | 契约只定义"何时应该刷新"，不产生执行日志 | 刷新纪律的遵守程度不可统计 | collaboration-lifecycle 域 |
| Low 置信度组合无测试断言 | `tests/test_maglev_map_maker.py` 全文仅 High/Medium 断言（L88、L162、L189） | 规则存在（`_confidence` L251）≠ 行为被验证 | "三级置信度"仅两级有测试证明 | 补 Low 组合测试 |
| CLI `main`/argparse 与 `--output`/`--snapshot`/`--generated-at` 无测试 | tests 仅直调 `generate()`/`check()` | 参数解析与路径覆盖行为未被断言 | CLI 使用口径只有静态可读性 | 补 CLI 层测试 |
| `_render_reality` 与证据来源表渲染无直接断言 | tests 断言 snapshot 字段（L148-L162），未断言 ATLAS 中 domain 标题与来源表行 | snapshot 字段正确 ≠ 渲染输出正确 | ATLAS 第 3、5 节的正确性无测试证明 | 补渲染输出断言 |
| 生成后 stdout 提示无稳定性契约 | `generate` 打印一行（L437-L440），无测试断言其格式 | 打印文本可随实现改动而变化 | 依赖 stdout 文本的自动化脚本会脆弱 | 观测类主题 |
| 写盘无锁且非原子（并发/中途失败行为未定义） | 脚本无 lock/rename 机制（静态检索无匹配）；`generate` 顺序写 snapshot 与 ATLAS（L430-L436），中途失败会留下新旧不一致的两份产物 | 无并发控制即无并发安全结论 | 并发生成或写盘中断后的产物状态未知 | 补原子写或并发说明 |
| 地图唯一性无工具强制 | `--output` 可把 ATLAS 写到任意路径（L466、L473-L475），无防重复机制 | SKILL.md"唯一的人读地图"是纪律约定，不是工具强制 | 多份地图出现时无告警 | 纪律层 |
| 旧独立 Markdown 地图文件是否已清离未盘点 | 本轮未盘点 docs/ 及全仓的地图类 Markdown 文件 | SKILL.md 判定纪律只约束生成行为，不证明存量已清理 | 遗留旧地图可能被误当 ATLAS | 盘点类主题 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 现役实例过期 | "当前仓库结构是 X"类以 ATLAS 为据的结论 | 派生视图不得新于其 source_commit | ✗"ATLAS 显示当前结构是……" |
| `--check` 未运行 | "check 通过/不通过"陈述 | 未运行不得报告运行结果 | ✗"check 应该会通过" |
| 无执行记录 | 刷新频率类任何统计 | 无数据源不得产出统计 | ✗"地图总是及时刷新" |
| Low 无断言 | "三级置信度已全覆盖"表述 | 无断言的组合不得计入测试分母 | ✗"置信度逻辑测试充分" |
| 渲染断言盲区 | "ATLAS 渲染被测试保证"表述 | 无断言的渲染节不得计入已验证范围 | ✗"渲染逻辑已被 8 个测试覆盖" |
| snapshot 属运行时产物 | 任何以 `.maglev/temp/atlas-snapshot.json` 为据的证据绑定 | gitignored 运行时产物不得作 digest 绑定证据 | ✗"snapshot 证明……" |
| 旧地图未盘点 | "仓库中只有一份人读地图"的存量陈述 | 未盘点不得断言存量唯一 | ✗"全仓只有 ATLAS 一份地图" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 现役实例过期 | 新一次显式生成后的 ATLAS frontmatter（source_commit 新于逆向候选，source_digest 与当时指纹一致） | 手工编辑 ATLAS 文本 | `../project-map/operations/configuration.md` |
| `--check` 判定 | 带输出文本与时间戳的 `--check` 运行记录 | 推测"应当通过" | `../project-map/verification/test-matrix.md` |
| Low 组合无断言 | tests 中新增 Low 组合断言并运行通过 | 口头确认 Low"显然正确" | `../project-map/verification/static-coverage.md` |
| CLI 无测试 | 直调 `main()` 或以自定义 `--output` 运行的测试断言 | 仅阅读 argparse 源码 | `../project-map/verification/static-coverage.md` |
| 渲染断言盲区 | tests 中新增"ATLAS 含 domain 标题/证据来源行"断言并运行通过 | snapshot 字段断言 | `../project-map/verification/test-matrix.md` |
| stdout 无契约 | stdout 格式被纳入测试断言或被明确声明为非契约 | 以当次运行输出为准的口头描述 | `../project-map/operations/configuration.md` |
| 写盘机制 | 原子写（临时文件+rename）或并发说明落地，并带中途失败场景的验证记录 | "并发很少发生"的使用经验 | `../project-map/implementation/architecture.md` |
| 地图唯一性 | 工具层防重复机制，或 SKILL.md 纪律条款补充 `--output` 使用约束 | "没人会传 --output"的假设 | `../project-map/operations/configuration.md` |
| 旧地图未盘点 | docs/ 与全仓 Markdown 的地图类文件盘点记录 | 未检索的口头确认 | `../project-map/implementation/architecture.md` |
