# Input Facts — Spec Provenance Governance

## 用户输入

- 用户在其他项目做 specs 时发现：所有 specs 必须有相关来源证据和来源信息，来源可能是文档、会议、聊天，或与 AI 的沟通。
- 用户指出：specs 中途可能变更，所有 specs 相关文件如果通过 AI 变更，应该有相关变更记录。
- 用户要求参考 `../../../../../../../maglev-project/maglev-foresight` 的实践，分析改进项目。
- 用户强调：新增文件和结构化管理未必带来额外工作，因为这些内容本来就是执行者参与过的内容；真正的目标是让执行者看到证据、对生成结果有信心，并让 AI 根据输入充分思考，而不是填字数。
- 用户进一步指出：AC 的“摘要”仍然需要，因为过往出现过 AI 只通过片段文字判定 AC，而不是基于完整上下文，导致产出片面化和窄化。

## 已观察到的项目实践

- `../../../../../../../maglev-project/maglev-foresight/docs/guides/requirements-self-check.md` 已要求 AC 到证据的正向检查，以及源文件到 AC 的反向覆盖率检查。
- `../../../../../../../maglev-project/maglev-foresight/specs/20_evolution/active/foresight-perception-market-pv/01_requirements.md` 已在 AC 表中使用“原文摘要 / 证据来源 / 会议证据 / PRD 证据”等做法。
- `../../../../../../../maglev-project/maglev-foresight/specs/20_evolution/active/foresight-perception-market-pv/01_requirements.md` 已有“变更记录”章节，记录日期、变更项、旧值、新值和来源。
- `../../../../../../../maglev-project/maglev-foresight/specs/20_evolution/active/foresight-perception/context/` 中存在 PRD、会议纪要、transcript、设计稿、影响分析等上下文材料。
- 当前 Maglev 的 `spec-designer` 流程已有 `context/input_facts.md` 存档要求，但还没有把“条目级来源摘要、上下文判定、AI 语义变更记录”作为标准输出要求。

## 已收敛判断

- 结构化来源和变更记录不是额外仪式，而是执行者应保留的工作痕迹。
- 需求正文应只保留读者能直接消费的规则，避免把会话中被放弃的方案或内部取舍写成需求内容。
- “证据”不应只是行号或片段引用，必须包含来源摘要和上下文判定。
- AI 语义变更记录只记录影响范围、需求、验收、约束、设计决策的变更；普通格式整理不记录。


## 后续补充决策

- 语义变更记录不需要额外独立 log 文件，随对应 spec 文件维护即可。若变更过多，应视为项目健康风险。
- 来源审计必须双向：检查 AC / Decision 是否都有来源，也检查来源中产生的有效信息是否被 AC / Decision 覆盖。
- AI 对话原始记录通常不需要保存；在需求中说明来自 AI 并写出摘要即可。若这类思考很有价值，应沉淀到 `docs/thinking/`，而不是塞进需求正文。
