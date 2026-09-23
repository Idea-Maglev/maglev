---
name: maglev-wiki
description: 基于项目事实推导 Wiki 结构，经独立充分性挑战与人类审核后完成内容生产、审查和增量更新。
metadata:
  formal_action_name: Wiki 内容生产
  top_level_capability: 运营文档体系
  system_layer: Specialized Support Layer
  lifecycle_chain: specialized_support
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
  author: feiyu.gao
  last_updated: 2026-09-09
  version: "2.2.0"
---

# Maglev Wiki 内容生产

本 Skill 从项目事实和真实读者任务推导 Wiki。结构计划只是生产者提案，不能同时充当内容全集和验收全集；正文写作前必须完成独立 Blind Challenge、差异处置和人类审核。

- Source Universe 独立登记可访问来源全集、摘要、排除项、变更信号和可选 Evidence Provider；Challenge Receipt 记录挑战者实际可见输入，Plan 不能反向定义两者。
- 生产 Agent 基于 Source Universe 推导维度、方面、页面和内容深度。
- 独立挑战 Agent 在不可见 Plan 和现有 Wiki 的隔离上下文中，只重建读者问题、风险、遗漏候选和深度信号，不生成第二套页面树。
- Plan 与 Challenge 必须形成差异账本。人类审核结构、遗漏、替代方案和剩余风险后，正文阶段才可开始。
- 模板只提供约束、建议和示例；不规定页面数量、文件划分、章节、篇幅或内容量。
- 最终审查同时消费 Plan 任务、Challenge 任务、风险与 unknown、变更影响和独立业务问答，并记录实际反证过程。
- 脚本只校验路径、摘要、隔离收据、差异处置、链接、漂移和计划对应关系；脚本不生成信息架构，不裁判自然语言质量。

## 工作流

用户提出“生成 Wiki”或“更新 Wiki”后，按 [Wiki 内容生产工作流](references/wiki-authoring.workflow.md) 执行：

1. 加载人类可读基准与项目配置；
2. 构建 Source Universe；
3. 在独立上下文中并行形成 Producer Plan 和 Blind Challenge；
4. 由第三个独立上下文生成 Divergence Ledger，登记剩余风险并输出单一 Markdown 结构审阅面；
5. 人类批准后单独生成审批收据，再按批准页面构建证据并写作；
6. 执行结构检查和开放世界读者任务审查，自动修订可安全修复的问题；
7. 生成人类成品验收简报，明确接受后记录增量基线。

## 结构与挑战资产

```text
.maglev/wiki.yaml                    # 项目输入：标题、语言、来源边界和受众提示
.maglev/wiki/                        # Wiki 生成与审查资产的专属状态目录
  wiki-source-universe.yaml          # 当前执行的实际证据范围，不定义页面
  wiki-challenge-receipt.yaml        # 隔离挑战的规范输入和执行收据
  wiki-challenge.yaml                # 独立问题、风险、深度信号和来源依据
  wiki-plan.yaml                     # 生产者提出的页面结构，始终保持 pending
  wiki-divergence.yaml               # 第三方差异处置、集成凭据和剩余风险
  wiki-plan.md                       # 人类唯一结构审阅面
  wiki-plan-approval.yaml            # 人类批准后单独生成的摘要绑定收据
  wiki-reviews/<review-id>/          # 成品验收和页面级审查资产
```

Challenge concern 只能表达读者问题、重要性、风险、深度信号和来源；任意层级都不能包含维度、页面或页面绑定。每项 concern 必须得到 `covered`、`merged`、`deferred`、`not_applicable` 或 `blocked` 处置；`deferred` 与 `blocked` 必须进入剩余风险账本。
审批收据同时绑定 Source Universe、Challenge、Divergence、Plan 和固定路径 `.maglev/wiki/wiki-plan.md` 的摘要；任一摘要变化都会使批准失效。执行与审批收据提供可审计声明，但仓库内脚本不能认证会话历史或人类身份，拥有同等写权限的恶意执行者仍可伪造收据。因此整体充分性保持 `provisional`，审批真实性依赖 Agent 遵守“仅在用户明确批准后签发”的治理纪律；需要抵抗恶意写入时必须接入仓库外可信验证器。

## 模板与 Evidence Provider

通用写作指导位于 `templates/wiki-packs/general/v1/methodology-catalog.md`；软件研发项目的观察建议位于 `templates/wiki-packs/software-development/v1/README.md`。

- **约束**：必须满足的安全、证据和审批边界；
- **建议**：按项目受众和事实采用；
- **示例**：只说明判断方式，不代表合适的页面数、章节数、篇幅或内容深度。

原始代码扫描、attention map 或知识抽取结果可以作为 Evidence Provider 加入 Source Universe。Provider 只增加候选问题和证据，不直接增加页面，也不能授予通过结论。

## 成品验收

最终审查任务集合包括：

```text
Plan 页面任务
∪ Blind Challenge 问题
∪ 风险与 unknown 任务
∪ 本次变更影响任务
∪ 独立业务问答
```

审查必须记录尝试推翻的结论、反例来源、最可能错误的页面和被排除的遗漏候选。没有真实用户问题或独立业务问答时，可以验证合规性和来源充分性，但整体充分性只能为 `provisional`。

## 命令

```bash
WIKI=.agents/skills/maglev-wiki/scripts

./scripts/maglev-python "$WIKI/wiki_config.py" validate --root .
./scripts/maglev-python "$WIKI/wiki_content.py" build-universe --root .
# Producer 与独立 Challenger 分别生成 plan、challenge-receipt 和 challenge；
# 第三个独立 Integrator 生成 divergence，并登记 integration 与 residual_risks。
./scripts/maglev-python "$WIKI/wiki_content.py" validate-open-world --root .
./scripts/maglev-python "$WIKI/wiki_content.py" render-plan --root .
# 人类明确批准后，另写 .maglev/wiki/wiki-plan-approval.yaml；不得回写 Producer Plan 冒充批准。
./scripts/maglev-python "$WIKI/wiki_content.py" validate-plan --root . --require-approved
./scripts/maglev-python "$WIKI/wiki_content.py" build-evidence --root . \
  --output .maglev/wiki/wiki-reviews/<review-id>/evidence.yaml
./scripts/maglev-python "$WIKI/wiki_generate.py" --root . --dry-run --json
./scripts/maglev-python "$WIKI/wiki_generate.py" --root .
./scripts/maglev-python "$WIKI/wiki_frontmatter.py" --root . <pages...>
./scripts/maglev-python "$WIKI/check_wiki_structure.py" --root . --json
./scripts/maglev-python "$WIKI/check_wiki_drift.py" --root . --json
./scripts/maglev-python "$WIKI/wiki_content.py" check-readable --root .
```
