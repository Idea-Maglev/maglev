# 协作协议 (Collaboration Protocol)

> **Source**: 从 `standards/collaboration_conventions.md` 中提取的独有规则。
> **Updated**: 2026-02-13

## 1. 贡献者记录 (Contributor Logging)
采用 **双维度评价体系**：
- **意图主导 (Intent Driver)**: 谁定义了"做什么"？（通常由 Human 主导）
- **执行载体 (Execution Carrier)**: 谁完成了"怎么做"？（通常由 AI 主导）

在 `contributors/contribution_log.md` 中必须记录这两个维度。
- **[必填] Human Prompt Summary**: 必须记录人类给出的关键 Prompt。

## 2. 参考资料归档 (Reference Archiving)
`references/` 目录按类型分类：
- `references/papers/`: 学术论文 (命名: `YYYY-Title.pdf`)
- `references/articles/`: 博客文章 (Markdown 记录链接、摘要和推荐理由)
- `references/tools/`: 工具介绍
- `references/prompts/`: 高效 Prompt 案例

对于长篇资料，必须创建同名 Markdown 文件，包含来源链接、推荐理由和核心摘要。

## 3. 上下文数据区 vs 外部引用 (context/ vs ref/)

Spec 目录下可包含两类辅助子目录，职责严格区分：

| 维度 | `context/` | `ref/` |
|------|-----------|--------|
| 性质 | 项目内在上下文 | 外部引用 |
| 可变性 | 随 spec 演化 | 不可变输入 |
| 典型内容 | 字段规则 CSV、代码结构分析、接口映射、配置快照 | PRD 原稿、设计图、论文、外部 API 文档 |
| 生产者 | 执行者 + AI 协作 | 外部角色（产品、设计、第三方） |
| 归档 | 全量跟随 spec | 全量跟随 spec |

**规则**：
- `context/input_facts.md` 为必需文件，其余为可选
- 文件名须有语义（如 `field_visibility_rules.csv`），格式不限（md/csv/json/yaml）
- 禁止在 `context/` 下创建个人命名空间或 backup 目录——版本管理由 Git 负责

## 4. AI 技能维护 (Skill Maintenance)
- **沉淀即技能**: 被验证有效的流程应封装为 `.agents/skills/` 下的 Skill。
- **同步更新**: 核心文档变更时，必须检查引用该文档的 Skill 是否需要更新。
