# spec pipeline 物理内部化重构 阶段总结

> 状态：已完成

## 1. 本轮完成项

1. 建立了新的 private / internal 目录结构
2. 将 `ingest` / `validate-context` 并入 `spec-designer/references/pipeline/`
3. 将 `draft` / `crystallize` 并入 `.agents/skills/_internal/spec-pipeline/`
4. 切换了 `spec-designer` / `maglev-reverse-spec` 的活引用
5. 删除了旧的四个独立 skill 目录

## 2. 当前结论

spec pipeline 已从“口径内部化”推进到“物理内部化”。

当前仓库不再需要：

- `.agents/skills/maglev-spec-ingest/`
- `.agents/skills/maglev-spec-draft/`
- `.agents/skills/maglev-spec-crystallize/`
- `.agents/skills/maglev-validate-spec-context/`

## 3. 后续仅需维护

1. 文档零星回填
2. 新 internal 路径的长期稳定性维护
3. 如有必要，再进入下一轮更细的 pipeline 优化
