# residual legacy name inventory v1

> 状态：已完成
> 作用：记录主流程四对象 rename 后仍保留的旧运行名残留，并对其进行分层判断。

## 1. 当前观察

基于首轮扫描，旧名残留主要集中在以下几类：

补充扫描结论：

1. 当前未再发现指向四个旧 skill 目录的现役失效路径引用
2. 当前可见的主流旧名说明，大多已经转成：
   - `历史入口：...`
   - `兼容入口：/...`
3. 因此本主题后续不应再以“大规模洗旧名”为目标，而应只处理会误导当前结构事实的残留

### A. execution / migration 过程文档

包括：

- `runtime_rename_execution/*`
- `runtime_rename_migration/*`
- `runtime_name_strategy/*`

判断：

- `保留`

原因：

- 这些文档本身就在记录从旧名到新名的迁移过程
- 旧名在这里是过程事实，不是运行面误导

### B. 既有 active 主题中的旧路径说明

包括：

- `spec_pipeline_internalization/*`
- `skill_structural_upgrade/design/archive/scout/*`

判断：

- `部分保留，部分后续回填`

原因：

- 一部分是当时的过程记录，应保留
- 另一部分若直接写旧 skill 路径，可能会误导读者理解当前仓库结构

### C. docs/thinking 说明材料

包括：

- 架构蓝图
- 旧重构计划
- 方案比对与论文思考

判断：

- `默认保留历史命名`

附加条件：

- 若其中链接到已不存在的当前路径，应修正为现路径或显式标注为历史路径

### D. 现役说明面

当前结论：

- `.agents/` 现役层已基本清空四个旧运行名
- Reality / guides / marketing 主表述也已切到新名
- 兼容入口说明已形成统一模式：
  - `reality-sync` / `/standup`
  - `spec-designer` / `/create-spec`
  - `context-implementer` / `/quick-dev`
  - `integrated-validator` / `/validate-all`

判断：

- `本轮已完成`

## 2. 当前最小清理建议

下一步真正需要做的不是大规模洗旧名，而是只处理两类对象：

1. `docs/thinking/` 中链接到已不存在 skill 目录的失效旧路径
2. active 主题中会让人误以为旧 skill 目录仍是当前结构事实的路径说明

## 2.1 本轮已收口对象

当前已补齐：

1. `spec_pipeline_internalization/*`
   - 已将当前结构事实从 `maglev-create-spec` 回填为 `spec-designer`
2. `docs/thinking/skill_lifecycle_management.md`
   - 已将“当前示例 skill / 当前路径事实”回填为 `spec-designer`

因此当前 remaining cleanup 已进一步缩小：

1. execution / migration 过程文档中的旧路径说明
   - `保留`
2. `docs/thinking/` 中以旧对象名做概念讨论、但不指向失效当前路径的历史草案
   - `默认保留`

## 3. 暂不处理范围

以下范围当前不建议继续清：

1. execution / migration / strategy 主题中的旧名差异记录
2. archive 中的历史命名
3. 仅用于解释“历史入口”或“兼容入口”的旧名说明

## 4. 当前结论

`runtime_rename_post_cleanup` 已完成本轮目标：

1. 现役层失效旧路径未再发现
2. 会误导当前结构事实的 active / thinking 文档已完成最小回填
3. 旧名残留的保留边界已经明确

后续不应继续在本主题下扩写“是否继续洗旧名”，而应转入下一主题：

- `workflow_name_strategy`
