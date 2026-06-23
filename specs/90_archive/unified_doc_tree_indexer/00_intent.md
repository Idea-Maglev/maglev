# Intent: unified_doc_tree_indexer

## 一句话

将 index-librarian 的 `spec-tree` 和 `docs-tree` 统一为 `dir-tree`，让任何目录都能用同样方式生成 INDEX.md 网络。

## 真实问题陈述

1. **spec-tree 是空壳**：schema 承诺产出 INDEX.md 网络，实际只写 summary YAML（实现欠债）
2. **docs-tree 只索引一个子目录**：只覆盖 `docs/thinking/`，`docs/guides/` 等 4 个子目录无索引
3. **两种 type 本质相同**：都是"对文档目录生成 INDEX.md"，不应有两条代码路径
4. **verify 不检查产物存在性**：所有 track type 的 verify 都不验证索引产物是否真正生成
5. **索引技能被 Maglev 结构绑架**：代码里硬编码了 Maglev 特有的目录语义，不具备通用性

## 核心设计原则

> 索引技能是通用基础能力，不应被 Maglev 体系所影响。Maglev 体系应适应索引技能。

## 预期结果

- `specs/` 和 `docs/` 用同一种索引逻辑
- 任意目录通过 registry 配置即可接入索引
- verify 能检测产物缺失
- 已有 INDEX.md（如 docs/thinking/）向后兼容
