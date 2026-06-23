# Evolution Observatory Workflow

## 概述

Phase 0 + 6 Phase 持续情报净化循环。本文件定义领域无关的通用执行步骤。

## Phase 0: Self-Knowledge Anchor（自我认知锚定）

**目标**: 在开始任何外部对比前，确保对 Maglev 定位、边界和关系的理解是正确的。

**步骤**:
1. 读取 `specs/10_reality/positioning.md`
2. 内化核心锚定规则（第 6 节）：
   - 先判断"是不是我们的战场"
   - 编码层创新 = 环境约束变化，不是追赶目标
   - 需求预测，不是功能模仿
3. 如果 positioning.md 不存在，向 Creator 报告并建议补建

**产出**: 锚定完成，进入 Phase 1

---

## Phase 1: Scope & Plan（范围与计划）

**目标**: 确定本轮研究对象和范围。

**步骤**:
1. 读取 `specs/10_reality/competitive_registry.yaml`
2. 解析 Creator 的自然语言指令，确定研究对象
3. 若未指定具体对象：按"距上次研究时间最长" + "活跃度最高"推荐 Top 3 候选
4. 确定本轮覆盖维度（mandatory 全覆盖 + 根据目标特性选择 exploratory）
5. 向 Creator 展示研究计划：对象、维度、预期产出
6. 等待 Creator 确认后进入 Phase 2

**产出**: 本轮研究计划（对象 + 维度 + 范围边界）

---

## Phase 2: Insight Review（洞察回顾）

**目标**: 重新评估已有 open insights 的有效性。

**步骤**:
1. 从 Registry 中提取所有 `status: open` 的 insights
2. 逐条评估：
   - 该 insight 依赖的框架版本是否有重大更新？
   - Maglev 是否已从其他路径解决了同一问题？
   - 是否有更优替代方案？
3. 对仍然有效的：标记为"confirmed valid"
4. 对可能过时的：向 Creator 建议标记为 `superseded`（附带理由和 superseded_by）
5. **⚠️ 等待 Creator 确认后才执行状态变更**

**产出**: Insight Review 结论（哪些仍有效、哪些建议 supersede）

---

## Phase 3: Deep Research（深度研究）

**目标**: 按维度体系深入研究目标对象。

**步骤**:
1. 读取 `references/dimensions.md`，获取 mandatory 维度列表
2. 收集信息（多来源交叉）：
   - 官方文档 / GitHub Repo（代码结构、SKILL.md、README）
   - Web 搜索（最新动态、社区反馈、更新日志）
   - 实际试用（如可行）
3. 按每个 mandatory 维度（M-1 ~ M-N）填充对比分析
4. 识别 exploratory 维度（目标框架的独特特性不在 mandatory 列表中的）
5. 记录 exploratory 维度使用情况到 `dimension_upgrades.pending`
6. 深度撰写 M-6（对 Maglev 的启示），不少于 500 字

**产出**: 研究分析内容（待格式化为最终报告）

---

## Phase 4: Discovery（新竞品发现）

**目标**: 探索是否有新的活跃框架/产品值得纳入 Registry。

**步骤**:
1. Web 搜索：AI coding framework / agent framework / collaboration tool 最新动态
2. GitHub Trending：相关领域的新星项目
3. 社区信号：Reddit / HN / Twitter 讨论热度
4. 过滤标准：
   - 活跃度 ≥ medium（近 3 个月有实质更新）
   - 与 Maglev 有可对比性（横向或垂域）
   - 不在当前 Registry 中
5. 对每个候选：输出（名称 + 理由 + 初步分类 + 纳入建议）
6. 由 Creator 决定是否纳入

**产出**: 新竞品推荐列表（即使为空也必须记录"本轮未发现新竞品"）

---

## Phase 5: Output & Archive（产出与归档）

**目标**: 按模板生成报告，提炼 insights，更新 Registry。

**步骤**:
1. 读取 `references/output-template.md`
2. 将 Phase 3 的分析内容格式化为标准报告
3. 从 M-6（启示）中提炼 Actionable Insights：
   - 每条 insight 带：ID（{PRODUCT}-NNN）、标题、建议目标 skill/process、优先级
4. 将报告写入 `docs/thinking/10_critique/YYYY-MM-DD-{slug}.md`
5. 更新 Registry：
   - 更新产品的 `last_researched` 和 `version_tracked`
   - 添加新 insights（status: open）
   - 纳入 Phase 4 确认的新竞品
6. Git commit（message: `research(observatory): {description}`）

**产出**: 研究报告（已归档）+ Registry 已更新 + Git committed

---

## Phase 6: Self-Check（自检）

**目标**: 确认本轮执行完整性。

**步骤**:
1. 读取 `references/self-check.md`
2. 逐项检查 checklist
3. 所有 blocking 项必须通过
4. 输出本轮研究摘要：
   - 覆盖对象
   - 新增 insights 数量
   - Registry 变化摘要
   - 新竞品发现情况

**阻断规则**: 任一 blocking 项未通过 → 不可标记本轮完成，明确指出缺失项。

**产出**: 自检结果 + 本轮摘要
