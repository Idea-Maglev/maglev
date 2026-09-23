---
reality_id: collaboration-lifecycle.verification.known-gaps
title: 协作生命周期已知缺口
owner_domain: collaboration-lifecycle
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 本域已查证但当前无法成立的协作能力声明及其阻断规则与关闭条件
  excludes:
    - 已证明的测试事实（属 verification/multica-squad-kit.md）
    - 未查证对象的猜测（不进入本页）
---

# 协作生命周期已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 真实第三方 Runtime 接力 | `../capability/multica-squad-kit.md`（L3 等级行）；`../verification/multica-squad-kit.md`（Runtime 记录行） | `runtime_verified` 不成立，模板质量上限为 L2/`template_verified` | open |
| 本地受管安装漂移 | `../implementation/multica-squad-kit.md`（未知项第 1 行） | 本地 Squad 对象与当前模板版本的对应关系 | open |
| 远端受管对象状态的本地可复核性 | `../verification/multica-squad-kit.md`（未覆盖表第 3 行） | 历史"无 drift"结论的实时有效性 | open |
| 页面验证数字的时点漂移 | `../verification/multica-squad-kit.md`（全量测试行） | 测试计数类数字的引用方式 | open |
| `maglev-platform-operations` 作者面 | `../implementation/multica-squad-kit.md`（未知项第 2 行） | 该模板的作者源约定与可验证程度 | open |

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | 关闭条件 |
| --- | --- | --- | --- | --- |
| 真实第三方 Runtime 端到端接力（L3/`runtime_verified`）未证明 | `.maglev/runtime/validation-ledgers/vr_20260818T125419Z_f074035f4f50/claims.json`：最新 claim 状态 `not_proven`，理由 `no external handoff receipt observed for requirement`；`specs/90_archive/multica-todolist-runtime-validation/status.md` 记录综合验证进行中、置信度 `uncertain` | 逐轮账本中只有"未观察到外部 Handoff 回执"的记录，不存在可绑定的真实接力证据；本地测试与 fake Runtime E2E 只覆盖本地编排 | 小队质量声明上限被机器卡点限制在 L2；任何"已在真实 Multica 中稳定运行"的说法都不可引用 | 存在带字段级 Workspace Task 证据的 Runtime Proof（`kit.test.js` 已编码该接受条件）并登记进验证账本 |
| 本地受管安装落后于当前模板 | `.maglev/multica/squad-kit.lock.json` 记录 `maglev-complete@0.1.0`（2026-08-07 applied，8 个 Agent、无 scheduler），`catalog.yaml` 当前模板为 `0.4.0`（9 角色） | lock 与模板是两个时点的状态；本仓不存在 0.4.0 应用到本地受管对象的 plan/apply 记录 | 本仓 Squad Kit 的受管对象不是当前模板能力的安装证据 | 对本地对象执行升级并产生新的 self-check receipt 与 drift 回查记录 |
| 远端受管对象状态无法从本地文件实时复核 | 旧页面与 `specs/90_archive/multica-lite-squad-templates/00_index.md` 引用的 Squad/Bridge ID 不在本地 lock 中；本地只有 2026-08-07 的 lock 与 2026-08-12~18 的账本 | "无 drift"是历史时点回执，不是当前状态；本仓无实时远端查询结果文件 | 不得引用旧页对象 ID 声明当前远端一致性 | 新的受管回执（plan/apply 或 drift 回查输出）入库并绑定时间戳 |
| 页面验证数字漂移 | 旧 verification 页写"272/272、280/280、Lite 7/7"；r2 轮实测 `299/299`、Lite `9/9`、`package e2e: pass` | 测试计数随提交变化，任何写死数字在下一轮即失真 | 数字只能作为"引用时点快照"，不能作为稳定事实复用 | 每次引用时重跑并标注运行时点，或改以测试文件锚点（文件 + 用例名 + digest）表达 |
| `maglev-platform-operations` 作者面与 Runtime 面未收敛 | 其 `manifest.yaml` 声明 `squad: squad.json`（JSON 资产），与 `maglev-complete` manifest 的"YAML 唯一作者源"不是同一约定；版本 0.1.0、非默认 | 该模板没有与母模板同等的作者源收敛声明，也无对应 Runtime 验证意图 | 只能声明静态候选模板，不得声明与 `maglev-complete` 同级的质量 | 模板作者面收敛（对齐 YAML 作者源或声明等价校验）并获得主题级验证结论 |

缺口登记原则：只登记"查过且无法证明"的项；未查过的对象不进入本页。

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| Runtime Proof 未证明 | `runtime_verified`、小队"已稳定运行"、跨项目 Accepted 实践 | 无真实第三方回执不得声明 L3（`multica-squad-design-method/SKILL.md` 质量分级与判定纪律） | ✗"package E2E 通过所以 Runtime 已验证"（E2E 用的是隔离 fake Runtime） |
| 本地安装漂移 | "本仓已安装当前 Squad Kit 能力" | lock 记录的是 0.1.0 时点对象，不是 0.4.0 模板能力的安装证据 | ✗"模板 0.4.0 已在本仓生效" |
| 远端状态不可实时复核 | "受管对象当前无 drift" | 历史回执不构成当前状态证明 | ✗"上次回查无 drift，所以现在也无 drift" |
| 数字漂移 | 任何写死的测试通过数 | 计数必须绑定运行时点，过期即失效 | ✗"测试永远是 299/299" |

## 4. 相关页面

| 缺口 | 相关页面 |
| --- | --- |
| Runtime Proof / 本地安装漂移 / 远端状态 / 数字漂移 / platform-operations | `../verification/multica-squad-kit.md`；`../implementation/multica-squad-kit.md`；`../capability/multica-squad-kit.md` |

> 证据口径说明：`.maglev/` 下为本机运行态（本仓不入库）；本页对 lock 与 validation ledger 当前内容的观察属于作者工作区时点记录，机制证据绑定已入库的模板资产与 ledger 源码。
