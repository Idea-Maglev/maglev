# Input Facts: AI 上下文数据区

## 1. 触发来源
- modelconfig 项目 v2.15 Cover Page 归档审查
- 反模式文档: `docs/thinking/component_level_spec_decomposition_antipattern.md`（归档自 modelconfig 仓库）

## 2. 需求边界

### In Scope
- 标准化 context/ 子目录约定
- 定义 context/ 与 ref/ 边界
- 确保归档时搬迁
- 模板/文档体现

### Out of Scope
- Tech Spec 子文档拆分机制
- 个人命名空间禁令
- 已有项目改造
- 格式强制校验

## 3. 关键事实
- spec-pipeline crystallize 已创建 context/ 并放入 input_facts.md
- crystallization 归档使用 mv 整目录搬迁
- project-board 不检查 context/ 内容
- 现有 context/ 仅在 step-01-split-files.md 中被引用
