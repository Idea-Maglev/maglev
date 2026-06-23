# 索引技能是通用基础能力，不应被 Maglev 体系所影响

> **Context**: 在统一 spec-tree/docs-tree 为 dir-tree 的设计过程中，用户明确提出索引器应该是目录无关的（directory-agnostic），不应绑定任何 Maglev 特有语义。
> **Date**: 2026-05-25
> **Origin**: unified_doc_tree_indexer 设计会话

## 核心主张

index-librarian 是一个**纯基础设施层能力**。它的职责是：

1. 递归发现目录结构
2. 为每个目录生成/更新 INDEX.md
3. 聚合子目录统计

它**不应该**：

- 知道 `specs/` 和 `docs/` 有什么语义区别
- 为不同目录树应用不同的生成逻辑
- 包含任何 Maglev 生命周期概念（active/archive/crystallize）

## 设计推论

| 推论 | 实践体现 |
|------|----------|
| 单一类型即可覆盖所有目录树 | `dir-tree` 取代了 `spec-tree` + `docs-tree` |
| 配置差异通过 registry 参数化 | `ignore`、`max_depth`、`entity_type` 等字段 |
| 语义解读留给消费方 | track_map 按 track 做认知地图，索引器本身不参与 |
| 自定义字段保留策略 | 已有 INDEX.md 的自定义 frontmatter 字段永不覆写 |

## 为什么重要

如果索引器绑定了 Maglev 语义，会导致：

- 每新增一种目录结构就需要新增 track type（spec-tree → docs-tree → thinking-tree → ...）
- 索引逻辑中散布领域判断，无法被非 Maglev 项目复用
- 类型爆炸后维护成本线性增长

用户原话的核心判断：**"索引技能是通用基础能力，不应被 Maglev 体系所影响"**。

## 相关产物

- 设计文档: `specs/20_evolution/active/unified_doc_tree_indexer/02_design.md`
- 实现: `.agents/skills/index-librarian/protocol/scripts/common/index_gen.py`
- 注册表: `.agents/skills/index-librarian/protocol/registry.yaml` (protocol v3.0)
