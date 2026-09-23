---
reality_id: agent-context-surface.verification.known-gaps
title: Agent 上下文入口已知缺口
owner_domain: agent-context-surface
owner_slot: verification
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - 静态无法证明的上下文面行为
  excludes:
    - 已证明事实（属 test-matrix / static-coverage）
---

# Agent 上下文入口已知缺口

## 1. 缺口范围

| 缺口域 | 涉及页面/模块 | 影响的结论 | 状态 |
| --- | --- | --- | --- |
| 判定分支测试覆盖 | error-semantics、test-matrix | 四判定的部分分支无自动化护栏 | open |
| 注入函数行为 | state-model、delivery-runtime | 骨架写入与 discipline 注入无直接测试 | open |
| 模板内容质量 | configuration | minimal 基线存在静态缺陷 | open |
| 治理对账 | configuration、error-semantics | 契约口径与实现的同步无机读保障 | open |
| 运行时行为 | 本页组全部页面 | 双入口的实际消费效果 | open |

缺口来源限定：本页只记录"已查静态材料后仍不能成立"的事实，每条附已查依据与不能
成立的原因；运行日志、预想故障场景与待办性质的"待完善"不作为缺口登记。

claim 标识符说明：frontmatter 中 `rk.ac.kg.no-dedicated-tests` 沿用旧轮次账本命名，
其指称对象已按第 2 节第 1 行收窄为"分支级覆盖不完整"（专项测试文件存在是本轮新
证据）；`rk.ac.kg.legacy-block` 的指称对象按第 2 节第 8 行改述为设计事实。标识符
保留不改，以便 `evidence/claim-register.md` 跨页追溯。

## 2. 缺口账本

| 缺口 | 已查依据 | 为什么不能成立 | 影响 | owner/深挖 |
| --- | --- | --- | --- | --- |
| 判定分支测试覆盖不完整（旧账"tests/ 无 ai-context 专项测试"已证伪并收窄） | `tests/test_maglev_ai_context_check.py` 存在，含 4 用例（missing/legacy-drift/sufficient/precedence-drift） | 专项测试文件存在，但 `contaminated` 分支、discipline 缺失分支、`SURFACE_MARKER`/`SURFACE_MISSING` 结构错误分支无用例 | 污染检测与结构错误场景无回归保护；对四判定的覆盖表述必须按用例清单逐支说明 | `../agent-context-surface/verification/test-matrix.md` 第 3 节 |
| `ensure_discipline_pointer` 三态无直接测试 | 全仓 tests/ 仅在 `test_maglev_init_repo_modes.py`（92、99、355 行）将其 mock | 被测编排把该函数替换为存根，三态语义（injected/updated/skipped）只有静态阅读依据 | 纪律区块注入回归只能靠人工复核 | delivery-runtime 安装测试 |
| `AGENTS.minimal.md` 模板重复区块 | 模板 61-65 行与 67-71 行出现两段相同的「Skill 优先级协议」 | 两个静态锚点直接可读，属模板文本缺陷而非检查误报 | minimal 基线的参照可信度受损；以模板为底稿的补齐会复制重复段 | 模板维护轮次 |
| 契约口径与实现的映射无正式维护 | `contract.md#3-对齐漂移` 列 5 项检查（散文），installer 实现的 drift reasons 为 5 类 token 条件，两者对应但非逐字映射（如"是否混淆 workflow 入口名与 runtime name" ↔ 实现"只描述了兼容 workflow 入口，未说明当前 skill runtime name"） | 契约为散文、实现为 token 检查，无机读对账 | 契约修订或实现调整可能单侧漂移而不被发现 | `../agent-context-surface/operations/errors.md` |
| Agent 实际遵循率 | llms.txt/AGENTS.md 本体 + 全仓无会话级遥测 | 静态材料只能证明"入口说什么"，不能证明"agent 是否照做" | 双入口的实效结论只能来自使用观测 | 观测类主题 |
| `llms.txt` 末尾 `Updated: 2026-04-11` 的维护机制 | 全文 + scripts/ 清单无生成锚点 | 未定位任何写入该时间戳的脚本或技能 | 该行可能是过期手写痕迹，其准确性无护栏 | 治理类主题 |
| 消费项目运行时面 | 本轮 static_read 范围声明 | 未运行 installer，注入效果无实例证据 | 消费侧结论全部保留给 adoption-integration | adoption-integration 轮次 |
| 双轨最小形态无一致性校验 | `templates/AGENTS.minimal.md`（含 managed 区块标记）与 installer `_minimal_agents_example()`（纯文本列表）结构不同 | 两个载体都是"最小可用参照"，但无比对机制保证同步演进 | init 骨架与契约模板引导的底稿结构不一致，补齐结果因入口而异 | `../agent-context-surface/operations/configuration.md` |
| update 路径不兜底 `missing` | `ensure_ai_context_files` 仅挂 init 编排 | update 对缺失双入口只报告不落盘 | 缺失文件在只跑 update 的项目上持续存在 | delivery-runtime 页组 |
| `README.md` managed 区块的维护归属 | `generate_documentation_surfaces.py#TARGETS` 含 README.md，区块存在于 69-89 行 | 该文件的日常内容维护归谁（人工或治理流程）未在本轮核对 | 无法把 README 的治理对账计入本模块结论 | 治理类主题 |
| legacy 词表的 markdown 渲染分支不可达 | `generate_documentation_surfaces.py#render_legacy` 支持 markdown 风格，但 TARGETS 中 legacy 仅挂载于 installer.py（python 风格） | 当前分母下该分支无调用路径 | 非缺陷，但说明 legacy 区块的 md 载体能力未被任何目标使用；`rk.ac.kg.legacy-block` 旧表述（"AGENTS.md 缺 legacy 标记"）应理解为 TARGETS 设计事实而非漂移 | 治理类主题 |

## 3. 阻断 provenance

| 缺口 | 被阻断的事实/统计 | 阻断规则 | 不允许的替代说法 |
| --- | --- | --- | --- |
| 判定分支覆盖 partial | "四判定已全覆盖"类结论 | 覆盖表述必须逐分支对照用例清单 | ✗"存在专项测试所以四判定都有护栏"；✗"tests/ 无 ai-context 专项测试"（已证伪） |
| 无运行遥测 | "agent 遵循率 X%"类任何统计 | 无数据源不得产出统计 | ✗"双入口齐备所以 agent 必然遵循" |
| 消费项目 not_computed | 消费侧注入/检查效果结论 | 未运行不得断言运行时行为 | ✗"init 源码存在所以消费项目骨架已生成" |
| legacy 区块设计事实 | "AGENTS.md 漂移缺失 legacy 区块" | TARGETS 未挂载 ≠ 漂移 | ✗"legacy 区块丢失" |
| README.md 归属未核对 | "README 治理已对账"类结论 | unmapped 对象不得计入已映射统计 | ✗"全部治理目标均已对账" |
| 双轨最小形态 | "init 骨架 = 契约模板"类等同表述 | 两载体结构不同且无比对锚点 | ✗"消费项目拿到的骨架与模板一致" |

## 4. 关闭条件与相关页面

| 缺口 | 可接受的关闭证据 | 不足以关闭的材料 | 相关页面 |
| --- | --- | --- | --- |
| 判定分支覆盖 | `tests/test_maglev_ai_context_check.py` 新增 contaminated/结构错误分支用例并通过 | 对实现的文字复述 | `../agent-context-surface/verification/test-matrix.md` |
| `ensure_discipline_pointer` 三态 | 针对该函数的直接单测（临时目录写入三场景） | 仅在编排测试中继续 mock | delivery-runtime 安装测试 |
| 模板重复区块 | 模板文件中重复段被移除且 generator `--check` 通过 | 口头确认 | `../agent-context-surface/operations/configuration.md` |
| 契约-实现映射 | 契约维度与实现 reasons 的机读对照（或契约改为结构化清单并被测试引用） | 一次人工比对记录 | `../agent-context-surface/operations/errors.md` |
| Agent 遵循率 | 带时间戳的会话样本记录 + 与双入口口径的人工比对结论 | 单次无对照的使用感受 | `../agent-context-surface/verification/static-coverage.md` |
| llms.txt 时间戳 | 定位到生成/更新锚点（脚本或技能）或移除该行 | 推测维护者 | 治理类主题 |
| 双轨最小形态 | 为两载体建立机读比对（或内嵌骨架改为引用模板） | 一次性人工对齐 | `../agent-context-surface/operations/configuration.md` |
| update 不兜底 missing | update 编排加入兜底调用并有测试锁定 | 仅修改文档表述 | delivery-runtime 页组 |
| README.md 归属 | 定位 README 内容维护流程的锚点（脚本/技能/纪律条款）并登记 | 推断维护者 | 治理类主题 |
