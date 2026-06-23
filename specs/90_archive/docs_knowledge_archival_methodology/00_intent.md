# Intent

## 1. 当前目标

为 Maglev 的 `docs/` 建立**长期可持续的知识归档与索引机制**，把现状的"知识堆砌"治理为"有机分层"。归纳方法论先行，索引脚本随后。

## 2. 这个主题只回答什么

1. 知识沉淀的**生命周期**应包含哪些状态（灵感 → 草稿 → 沉淀 → 归档）以及状态之间的**触发条件**。
2. `docs/thinking/` 的**位段语义编号规则**应如何定义（00/10/20/30/...），以及命名应统一为编号轨还是时间轨。
3. **主题聚类规则**——同类如何相吸、跨类如何析出、什么时候允许新建主题。
4. 索引化是否要复制 `my-smart-workbench` 的 `index-protocol`，复制范围是什么、如何特化到 Maglev `docs/` 的颗粒度差异。
5. 现有 `maglev-librarian` skill 是否要升级承担文档索引职责，还是新建独立 skill。
6. 归档（`90_archive/`）的触发条件、保留策略、与 `specs/90_archive/` 是否合一。

## 3. 这个主题不回答什么

1. `specs/` 的 reality / evolution / archive 三态规则——已由 Maglev 范式固定。
2. `contributors/contribution_log.md` 的写法——已固定为倒序表格。
3. 单个 thinking 文档的**写作风格**或**正文结构**——只管分类、不管内容。
4. 是否引入跨会话语义记忆（SQLite + FTS5 类似 Hermes）——这是另一条主题。
5. `packages/` / `scripts/` / `tests/` 等非 `docs/` 内容的索引——本主题只管 `docs/`。
6. `dist/` 与 `.maglev_build/` 等构建产物——已 gitignore，不入索引。

## 4. 上游证据

- 用户痛感（2026-04-24 会话）：
  > "当前对于知识归档我发现了堆砌的问题，maglev 中 docs 里面的内容越来越多，越来越混乱。"
- 现状量化：
  - `docs/` 总计 178 个 md
  - `docs/thinking/` 30 个裸 md + 18 个主题子目录
  - 编号轨 `30_/35_/40_/50_/52_` 跳跃且无位段语义说明
  - 时间轨 `xxx_2026_02_03/` 多份并存（2 月集中爆发）
  - 已有 `00_meta/ 10_critique/ 20_architecture/ 90_archive/` 但**未强制使用**
  - 无 INDEX.md、无 schema、无机器校验
- 参考实现：`/Users/Maglev contributors/workspace/<private-repo-path-redacted>/my/my-smart-workbench/.agents/skills/_internal/index-protocol/`
  - Registry + Schema + Scripts 三件套已运行 ~2 个月稳定
  - `index-librarian` skill 编排 `scan → verify → calibrate`
- 已有 Maglev 资产：
  - `maglev-librarian` skill（仅扫描，无 schema 强约束）
  - `private-catalog.yaml`（registry 模式已验证可行）
  - `crystallization` skill（spec 归档已有方法论，可类比）

## 5. 成功标准

- 方法论文档落地后，任何贡献者都能基于规则**判断一份新 thinking 应放在哪、用什么编号、何时该归档**。
- `docs/thinking/` 的现有 30 + 18 个对象按规则**重组到位**，编号位段连续可解释。
- 索引脚本能机器化**校验** schema 一致性（exit code 0 = 健康）。
- 归档触发不依赖个人记忆——**有明确条件**（时间窗 / 上位重写 / 引用断链）。
- 半年后回看：docs/ 仍可遍历、可定位、不堆砌。
