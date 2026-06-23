# skill结构性升级 元数据落点方案 v1

> 状态：进行中
> 作用：明确当前元数据字段未来应落在哪些真实载体里，避免把所有字段都塞进单一文件或继续停留在分析文档层。

## 1. 目标

当前已经有：

- 元数据字段草案
- 两轮 metadata pilot

下一步不该直接全量回填，而应先回答：

1. 哪些字段适合跟对象本体走
2. 哪些字段适合放在 catalog / index 层
3. 哪些字段只适合保留在治理快照里

## 2. 当前可用载体

基于当前仓库现实，后续最相关的载体有四类：

1. `SKILL.md` 头部 frontmatter
2. `.agents/private-catalog.yaml`
3. `.agents/workflows/*.md` 的 frontmatter 或正文元信息
4. 治理快照类文档

## 3. 分层落点原则

后续元数据落点优先遵循：

1. **离对象最近的字段，放对象本体**
2. **用于检索、分发、批量分析的字段，放 catalog / index**
3. **会频繁变化、带判断色彩的字段，不直接写死在对象本体**
4. **workflow 对象不强行复用 skill 的全部字段**

## 4. 建议落点

### A. `SKILL.md` frontmatter

适合放：

1. `name`
2. `description`
3. `metadata`（仅放非触发型、稳定的结构字段）

原因：

- 这是当前可确认的 Codex skill 最小标准格式
- `name` 和 `description` 是明确会被读取并用于 skill 触发判断的字段
- `metadata` 是编辑器支持的标准扩展位，适合承接不参与触发判断但有治理价值的稳定字段

当前不建议直接放在 frontmatter 顶层：

1. `formal_action_name`
2. `top_level_capability`
3. `system_layer`
4. `lifecycle_chain`
5. `current_direction`
6. `naming_readiness`
7. `removal_status`

原因：

- 这些要么属于治理元数据，要么不属于当前可确认的标准 frontmatter 字段
- 即使运行时通常会忽略它们，也容易触发编辑器 schema 报错

当前建议放进 `metadata` 的字段：

1. `formal_action_name`
2. `top_level_capability`
3. `system_layer`
4. `lifecycle_chain`
5. `runtime_name_status`
6. `distribution_scope`
7. `author`
8. `last_updated`
9. `version`
10. `distribution`

### B. `.agents/private-catalog.yaml`

适合放：

1. `canonical_skill_name`
2. `formal_action_name`
3. `runtime_name_status`
4. `distribution_scope`
5. `top_level_capability`
6. `object_kind`
7. `status`
8. `relations`

原因：

- 它已经是项目级治理对象清单
- 适合承接跨对象查询与巡逻输入
- 能被 `skill-scout` / `skill-squadron` 直接消费

补充约束：

- catalog 不应只收 `skill`
- 对 `Workflow-first` 对象，应通过 `workflows:` 独立列表纳入
- `skill-squadron` 的关系图应同时消费 `skills:` 与 `workflows:`
- catalog 不是文件系统镜像，而是治理对象面
- `relations.target` 只能指向已登记的治理对象，不能指向数据文件或普通文档

建议后续补的字段：

1. `formal_action_name`
2. `runtime_name_status`
3. `distribution_scope`
4. `top_level_capability`
5. `object_kind`

### C. `.agents/workflows/*.md`

适合放：

1. `description`
2. `metadata.formal_action_name`
3. `metadata.top_level_capability`
4. `metadata.object_kind: workflow`
5. `metadata.lifecycle_chain`
6. `metadata.author`
7. `metadata.last_updated`

原因：

- `Workflow-first` 对象当前真实承接点就在 workflow
- 不应强行把这些对象先写进 skill 本体
- workflow 同样适合保持标准顶层字段克制，自定义治理字段放入 `metadata`
- skill 与 workflow 应共享同一条规则：有治理价值但不参与触发判断的稳定字段，统一收进 `metadata`

典型对象：

1. `需求收敛`
2. `现实结晶`
3. `skill-scout`
4. `skill-squadron`

### D. 治理快照类文档

适合放：

1. `current_direction`
2. `naming_readiness`
3. `removal_status`
4. `coverage_status`
5. `risk_type`

原因：

- 这些字段本质上是治理判断
- 需要被持续复判
- 不适合直接写死在对象本体

当前典型承载位置：

1. `design/02e_skill_batch_analysis_base_table.md`
2. `design/02g_skill_governance_queue.md`
3. 后续若产品化，可迁移到专门的 metadata index

## 5. 第一阶段建议落点

当前更适合的第一阶段，不是全量改造，而是只落最小一层：

### 第一阶段

- 在 `SKILL.md` 中保持标准顶层字段：
  - `name`
  - `description`
- 将稳定但非触发型字段收进 `metadata`

### 第二阶段

- 在 `.agents/private-catalog.yaml` 补：
  - `canonical_skill_name`
  - `formal_action_name`
  - `runtime_name_status`
  - `object_kind`

### 第三阶段

- 为 `Workflow-first` 对象补 workflow 元信息

### 第四阶段

- 再考虑是否引入单独 metadata index

## 6. 当前结论

当前最稳的落点方案是：

- **对象本体** 承载最小标准 frontmatter + `metadata`
- **catalog / workflow** 承载分发和编排层字段
- **治理快照** 承载会变化的判断字段

这样既不会让 `SKILL.md` 偏离 Codex skill schema，也不会让元数据继续只停留在设计文档里。
