# Requirements: Evolution Observatory

## 文档关系

- **上游**: PRD（需求收敛产物，2026-05-25 会话）
- **下游**: 02_design.md, 03_plan.md
- **平行**: 无

## 1.1 核心意图

构建一套可持续执行的"行业框架观察→分析→学习→反省→改进建议"闭环机制，作为 Maglev skill 长期运行。

## 1.2 功能需求

### F-1: 竞品注册表管理

**用户故事**: 作为 Creator，我希望维护一个结构化的竞品/框架注册表，以便清楚知道 Maglev 在观察谁、为什么观察、当前状态如何。

**验收标准**:
- AC-F1-1: 当新增一个观察对象时，Registry 应包含：名称、分类(横向/垂域)、版本、首次纳入日期、关注理由、活跃度评估
- AC-F1-2: 当对象分类为横向时，系统应将其标记为与 Maglev 同层竞品；分类为垂域时，标记为子能力参考
- AC-F1-3: 当 Registry 被读取时，应能按分类、活跃度、最近研究日期排序/筛选

**边界情况**:
- 一个产品可能同时有横向和垂域两面（如 Superpowers 整体是横向，但其 TDD 模块是垂域参考）→ 支持多分类标签

### F-2: 研究触发与范围选定

**用户故事**: 作为 Creator，我希望通过自然语言触发一轮研究并指定范围，以便 AI 知道本轮要深入哪些对象。

**验收标准**:
- AC-F2-1: 当 Creator 触发研究时，AI 应读取 Registry 获取可研究对象列表，结合自然语言指令确定本轮范围
- AC-F2-2: 若 Creator 未指定具体对象，AI 应基于"距上次研究时间最长"+"活跃度最高"推荐候选
- AC-F2-3: 当范围确定后，AI 应在开始深入研究前向 Creator 展示本轮研究计划（对象+维度+预期产出）

### F-3: 对标维度体系

**用户故事**: 作为研究执行者(AI)，我希望有一组预定义的对比维度，以便每轮研究产出的结构可比、可积累。

**验收标准**:
- AC-F3-1: 当执行研究时，mandatory 维度必须全部覆盖，不可省略
- AC-F3-2: 当 AI 发现目标框架有不在 mandatory 列表中的显著特性时，应作为 exploratory 维度补充对比
- AC-F3-3: 当某个 exploratory 维度在连续 3 次研究中都被使用时，系统应建议将其升级为 mandatory

**边界情况**:
- 垂域工具可能在某些 mandatory 维度上无法直接对比（如"生命周期管理"对纯 TDD 工具不适用）→ 标记为 N/A 而非强制对比

### F-4: 标准化研究产出

**用户故事**: 作为 Creator，我希望每轮研究产出格式一致，以便长期积累可对比、可检索。

**验收标准**:
- AC-F4-1: 当研究完成时，产出必须符合 output-template.md 定义的结构
- AC-F4-2: 当报告产出后，应以 `research(observatory):` 为 commit message 前缀归档到 `docs/thinking/10_critique/`
- AC-F4-3: 当报告产出后，应包含"Actionable Insights"章节，每条 insight 带 ID、标题、建议目标、优先级

### F-5: Insight 生命周期管理

**用户故事**: 作为 Creator，我希望研究洞察被持续追踪，以便知道哪些被消化了、哪些还在等待、哪些已过时。

**验收标准**:
- AC-F5-1: 当研究产出新 insight 时，系统应在 Registry 中创建记录，状态为 open
- AC-F5-2: 当 insight 被 spec-designer 引用并产出 spec 时，状态应更新为 proposed，并记录 spec 路径
- AC-F5-3: 当 insight 对应的改进已合并时，状态应更新为 absorbed，记录日期
- AC-F5-4: 当 AI 在 Insight Review 中发现某条 open insight 已被更优方案替代时，应建议标记为 superseded，附带 superseded_by 和 reason
- AC-F5-5: 若 superseded 建议被 Creator 确认，系统应更新状态并保留原始 insight 完整内容（不删除）

### F-6: 新竞品发现

**用户故事**: 作为 Creator，我希望每轮研究自动探索是否有新的活跃框架/产品值得纳入，以便 Registry 不会固化。

**验收标准**:
- AC-F6-1: 当执行研究时，AI 应在研究主对象之外额外进行行业扫描（web search + GitHub trending）
- AC-F6-2: 当发现潜在新竞品时，应输出推荐列表（名称+理由+初步分类），由 Creator 决定是否纳入
- AC-F6-3: 若 Creator 确认纳入，系统应在 Registry 中创建新条目

### F-7: 执行自检

**用户故事**: 作为研究执行者(AI)，我希望每轮结束前有自检 checklist，以便确保没有遗漏关键步骤。

**验收标准**:
- AC-F7-1: 当研究结束时，AI 应逐项检查：Registry 已更新、open insights 已 review、产出符合模板、新竞品探索已执行、commit 已完成
- AC-F7-2: 若任一检查项未通过，AI 应阻止标记本轮完成，并明确指出缺失项
- AC-F7-3: 当所有检查项通过时，AI 应输出本轮研究的摘要（覆盖对象+新增 insights+Registry 变化）

## 1.3 非功能需求

- **跨会话可消费**: 任意新会话读取 skill 文件即可完整执行，不依赖历史对话
- **向后兼容**: 已有 7+ 篇对比文档不受影响，新机制只约束未来产出
- **可升级**: skill 定义可通过正常 spec-designer 流程迭代改进
- **Git 友好**: 所有状态（Registry、报告、模板）均为文本文件，diff 可读

## 1.4 术语表

- **Registry（竞品注册表）**: YAML 文件，记录所有 Maglev 观察的框架/产品、分类、版本及 insights 状态
- **Mandatory 维度**: 每轮研究必须覆盖的对比轴，确保产出可积累
- **Exploratory 维度**: AI 根据目标框架特性自主扩展的额外对比轴
- **Insight**: 研究报告中对 Maglev 有可操作价值的洞察/建议
- **Insight Review**: 每轮研究开始时对已有 open insights 的有效性重新评估
- **Superseded**: insight 因被更优方案替代而不再推荐执行的状态
- **横向竞品**: 与 Maglev 同层的 AI 团队协作框架
- **垂域参考**: 特定 AI 工具/实践，作为 Maglev 子能力的改进参考

## 1.5 粗略边界

- **上界**: 不做自动化触发、不直接产出代码变更
- **下界**: 至少产出 skill 定义 + Registry + 模板 + 维度定义
- **左界**: 从 Creator 自然语言触发开始
- **右界**: 到研究报告归档 + Registry 更新 + 自检通过结束
