# Intent: AI 上下文文件整合

## 动机

当前有三份文件承载 AI 行为规则，存在约 40% 内容重复。core_rules.md 有 8 条独有规则（EVIDENCE, LOGGING, TRACEABILITY, COLLAB, CAPTURE, USER_FOCUS, CUSTODIAN, INDEXING），但因位置隐蔽经常不被 AI 读取。

同时，Maglev 缺少 SpecKit `/speckit.constitution` 的对应能力——项目治理原则散落在错误位置且不被下游引用。

## 目标

1. 消除三文件重叠，每条规则只在一个文件中定义
2. core_rules.md 的 AI 行为规则和工作纪律合并进 AGENTS.md
3. 确定"项目治理原则"的正式位置与格式
4. core_rules.md 退役

## 边界

**做**：
- 三文件内容审计与去重
- core_rules.md 独有内容归并
- 项目治理原则位置确定
- core_rules.md 退役

**不做**：
- 扩展点架构设计（见 extension_point_architecture）
- AGENTS.md 大幅重构（只做必要的内容吸收）
- 新增 AI 行为规则
