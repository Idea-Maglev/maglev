---
maglev_status: accepted
accepted_date: 2026-04-14
---

# Intent

## 归档日志

- **结晶状态**：✅ 已完成 → 15 个 skill 文件已直接写回运行时能力
- **关键结论**：主流程增加审批门禁（RC handoff + SD output）、结构化 AC 生成（EARS + AC-F{N}-{M}）、AC 追溯链（需求覆盖表贯穿设计和计划）、标准化设计模板、任务依赖图（topological sort）、审计评分（4 维度 25 分制）、验证层前端能力补齐（4 个 validation skill）
- **执行经验**：T8 实现路径与设计文档偏差（wrapper-03-plan.md 不存在，实际在 tech-spec-template §3），提前做 3 层一致性审计可早发现此类偏差
- **时间线**：2026-04-13 启动 → 2026-04-14 归档

## 1. 当前目标

在 Maglev 主流程（需求收敛 → 方案设计 → 上下文实施）及其审计/验证层中增加 7 项质量保障机制：

1. **F-1 阶段交接强制审批**：在 3 个关键交接点增加人类 explicit approval
2. **F-2 结构化行为级需求**：AC 格式 + 自动生成
3. **F-3 AC 追溯链**：设计标准化 + 覆盖表 + 一致性检查
4. **F-4 任务依赖图**：结构化任务 + Mermaid 依赖 + 拓扑序执行
5. **F-5 审计评分**：4 维度 × 25 分量化评分
6. **F-6 AI 引导增强**：repository_map 摘要 + 半自动更新
7. **F-7 验证层前端能力**：4 个验证技能的前端实质性检查

## 2. 这个主题只回答什么

1. 哪些交接点增加审批门禁，以什么方式
2. 结构化需求的格式定义（AC 编号规范、字段约束）
3. 审批记录如何写入 spec 上下文
4. 结构化 AC 如何被后续设计/任务/测试引用
5. 任务依赖图的格式和执行编排
6. 审计评分维度和计算方式
7. AI 引导摘要的结构和更新机制
8. 验证层前端检查的具体维度
9. 15 个受影响文件的改动方案
10. 16 个实施任务的依赖图和执行顺序

## 3. 这个主题不回答什么

1. 文档拆分（功能/交互分文件）→ `spec_document_architecture`
2. 交互需求/设计模板 → `spec_document_architecture`
3. 术语表机制 → `spec_document_architecture`
4. 文档互联互验 → `spec_document_architecture`
5. maglev-design-ux 定位细节 → `spec_document_architecture`
