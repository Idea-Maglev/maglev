# spec pipeline 物理内部化重构 Design

## 1. 设计目标

这轮设计不再解决“它们是不是独立 skill”，而是解决：

> 既然它们已经不是独立 skill，文件结构应该怎样改，才能让宿主关系真实成立。

## 2. 当前对象重判

### 2.1 ingest

`ingest` 只被 `spec-designer` 使用。

因此它更适合被并入：

- `.agents/skills/spec-designer/references/pipeline/ingest/`

### 2.2 validate-context

`validate-context` 当前也只被 `spec-designer` 直接调用。

因此它更适合被并入：

- `.agents/skills/spec-designer/references/pipeline/validate-context/`

### 2.3 draft

`draft` 同时被 `spec-designer` 与 `maglev-reverse-spec` 使用。

它不适合直接塞回任一宿主私有目录，否则另一方会再次产生“不自然跨宿主引用”。

当前更稳的方向是：

- 在 `.agents/skills/` 下新增一个非现役、仅内部使用的共享目录
- 例如：`.agents/skills/_internal/spec-pipeline/draft/`

### 2.4 crystallize

`crystallize` 的使用面与 draft 类似：

- `create-spec` 直接依赖
- `reverse-spec` 在逻辑上也依赖其后续落盘能力

因此也更适合并入共享 internal pack：

- `.agents/skills/_internal/spec-pipeline/crystallize/`

## 3. 推荐目录结构

```text
.agents/skills/
  _internal/
    spec-pipeline/
      draft/
        draft.workflow.md
        step-01-load-context.md
        step-02-polymorphic-design.md
        unified-draft-template.md
      crystallize/
        crystallize.workflow.md
        step-01-split-files.md
        step-02-finalize.md
        step-99-abandon.md
  spec-designer/
    references/
      pipeline/
        ingest/
          ingest.workflow.md
          step-01-identify-source.md
          step-02-extract-facts.md
          step-02-map-skeleton.md
          step-03-zoom-extract.md
        validate-context/
          validate.workflow.md
          step-01-validate-schema.md
```

## 4. 迁移原则

1. 先迁引用，再删旧目录
2. 先让宿主文件引用新路径稳定工作
3. 共享模块不再以独立现役 skill 出现
4. internal 目录不进入用户推荐入口，不进入现役显性心智

## 5. 迁移顺序

### Phase 1

创建新目录结构并复制文件。

### Phase 2

修改：

- `spec-designer` 全部 wrapper / integrity / verify 引用
- `maglev-reverse-spec` handoff / integrity 引用

### Phase 3

全量搜索仓库内残留路径与说明。

### Phase 4

删除旧目录：

- `.agents/skills/maglev-spec-ingest/`
- `.agents/skills/maglev-spec-draft/`
- `.agents/skills/maglev-spec-crystallize/`
- `.agents/skills/maglev-validate-spec-context/`

## 6. 当前结论

本轮最推荐的物理内部化方案不是“全部塞回 `create-spec`”，而是：

- `ingest` / `validate-context` 并入 `spec-designer` 私有 pipeline
- `draft` / `crystallize` 并入 `_internal/spec-pipeline/` 共享模块包

这样既能去掉“独立 skill 假象”，又不会让 `reverse-spec` 被迫依赖 `spec-designer` 的私有实现目录。
