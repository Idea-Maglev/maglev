---
status: active
opened_at: 2026-04-27
last_revised_at: 2026-04-28
revision: v5.2 (consistency fix)
---

# Intent

> ⚠️ **本文件 v4 在 v3 PR-A 基础上再做一次抽象升级**。v3 写死三 Track（specs/docs/repo），v4 修正为"索引能力是公共能力，registry.yaml 声明式 tracks，generic 脚本对任意目录对象可跑"，同时立两条护栏：默认窄范围（不浪费）+ 不侵入代码仓库（必要时委派 radar）。修订理由见 §4.4。

## 1. 当前目标

让 `index-librarian` 体系演进为**通用项目级索引能力**——通过 `registry.yaml` 声明式 `tracks:`，generic 脚本对任意声明的目录对象（specs/、docs/、研究产物、决策记录、报告……）按统一协议跑索引/统计/认知图/归档触发。完整覆盖 `maglev-librarian` 现有职责后通过行为对等性验证废弃旧对象，并把这套通用能力随 `pip install maglev` 分发到用户项目作为**静默基建**。

## 2. 设计护栏

1. **默认窄范围**：开箱即用的 default track set 仅包含 `specs/`、`docs/`、仓库根入口（depth=1）三项，不主动扫整个仓库；用户需要更多就在自己的 `registry.yaml` 显式声明，避免无差别扫描浪费。
2. **不侵入代码仓库的元数据层**：repo-entry track 只看元数据文件（README、AGENTS.md、llms.txt、CHANGELOG、package.json 等），不下钻代码二级目录。
3. **code-tree 由 protocol 主导 + radar 作辅助执行器（v5）**：当用户为代码目录显式声明 type=code-tree 的 track 时，generic 脚本主导执行 4 个动作；scan 输出 `anchors:` 段（锚点导航，复刻 smart_map.py 模式）；可选启用 `radar_summary:` 段（subprocess 调用 radar 拉取 hotspot/unused/cycles 摘要）。**核心约束是防上下文爆炸**：继承 smart_map.py 防爆参数（IGNORE_DIRS / MAX_DEPTH=5 / MAX_LINES=200），radar 摘要按 `max_output_lines` 截断；radar 不可用时降级为仅锚点导航，不阻断流程。

## 3. 这个主题回答什么

1. **通用 track 抽象**：`registry.yaml` 中 `tracks:` 字段的 schema 设计（type / root / patterns / output / thresholds / depth_limit / delegate_to 等），让任意目录对象都能在统一协议下被索引。
2. **默认 track set**：maglev 自己仓库的 default 列表是什么（specs / docs / repo-entry），用户加 track 是否需要显式继承默认。
3. **代码仓库边界（v5 修订）**：当用户声明 type=code-tree 的 track 时，protocol 主导执行 4 动作，scan 输出 `anchors:` 段（必出）+ `radar_summary:` 段（可选，subprocess 调用 radar 拉摘要）；防上下文爆炸通过继承 smart_map.py 防爆参数 + radar 摘要截断实现。
4. **能力对齐**：当前 `index-librarian` 仅覆盖 docs/，如何让 generic 脚本统一覆盖 specs/、docs/、仓库入口（即 maglev-librarian 现有三 Track 职责）以及未来用户加的 track。
5. **maglev-librarian 处置时序**：先撤回 deprecated 标签（防真空期）→ generic 脚本完成对等性验证 → 再物理废弃。
6. **行为对等性如何度量**：generic 脚本相对 maglev-librarian 在 default track set 上的输入/输出/触发/失败兜底是否对等，缺什么补什么。
7. **分发清单**：generic 协议 + 脚本 + index-librarian skill 哪些随 runtime 分发到用户，哪些只在 Maglev 仓库根可见。
8. **声明—事实一致性**：catalog 中所有 `distribution_scope: 'runtime_internal'` 对象与实际 runtime 产物的一致性。
9. **用户接入体验**：用户安装后默认就能跑 default track set；扩展时只需在自己 `registry.yaml` 加 `tracks:` 项。
10. **与上游 spec 的修订关系**：`docs_knowledge_archival_methodology` 已对 maglev-librarian 打 deprecated，本主题如何修订该决策。

## 4. 这个主题不回答什么

1. `docs-index-protocol` 内部已稳定的 schema/lifecycle 方法论（已由 `docs_knowledge_archival_methodology` 主题完成）。
2. 其他 `_internal/` skill（`spec-pipeline`、`ai-context-check`）是否同步 runtime 化——按需开新主题。
3. AGENTS.md / catalog 自身的结构治理。
4. installer 的整体重构——只在最小必要范围内对 release.py 做改动；installer 保持零改动。
5. `spec-pipeline` 与 specs track 的职责切分——`spec-pipeline` 管"流程编排"，本主题 specs track 管"索引/统计"，二者并存。
6. **代码仓库的完整 AST / 调用图 / 死代码深度分析**——这部分由 `radar` skill 承担，本主题 code-tree 仅以摘要形式（hotspot Top N / cycles 计数 / unused 计数）调用 radar 子能力，不重新实现 AST。
7. 用户 track 配置错误时的自动修复——用户自负责声明合法 root 路径与 patterns。
8. 跨 track 关系图（specs ↔ docs ↔ repo 之间的边）——本主题先做 per-track 索引，跨 track 留给后续主题。

## 5. 上游证据

### 5.1 用户原始诉求（2026-04-27 会话）
> 对于这套机制不是 maglev 私有，而是 maglev 用户也是共用的对吧。

### 5.2 PR-A 修订诉求（2026-04-28 上午）
> 新做的索引处理工具覆盖面只有 docs 是不对的……实际我需要的是前面索引机制来覆盖当前 maglev 的项目场景。

> 让新索引机制完整覆盖 maglev-librarian 能力（Track A+B+C），然后才真正废弃它，并把这套完整能力随 install 分发到用户。

### 5.3 v4 通用化诉求（2026-04-28 下午）
> 当前索引 track 的范围还需要 issue ……如果给用户扩展索引范围的机制是否会带来很大的复杂度和改动开销，因为在工作台这边是有相关的考虑的。

> 索引机制是一个公共能力，不是为某个目录服务的能力。

> 可以对任何目录对象都跑，但是还是需要在实际项目中限制范围 避免浪费，这里对代码的索引要注意 不要对代码仓库有侵入性，如果不确定如何处理代码仓库的索引情况 就借助 radar 技能只对可操作的代码仓库根目录追加索引，不要深入到代码仓库的二级目录中，避免冗余和不好管理。

### 5.5 修订事实链

| 时间 | 决策 | 范围错配 |
|---|---|---|
| 上游 spec K2 | index-librarian 替代 maglev-librarian | 替代品仅覆盖 Track B（docs/） |
| 本主题 v1/v2 | "分发 docs 索引能力" | 把上游错配照搬 |
| 本主题 v3（PR-A） | "三 Track 完整替代 + 分发" | 把"三 Track"作为终态，未识别索引能力的公共属性 |
| 本主题 v4（通用化） | "公共索引能力 + registry.yaml 声明式 tracks + 默认窄范围 + 不侵入代码 + 委派 radar" | 把索引升级为 generic 能力，用户可声明扩展，代码索引由 radar 负责 |
| 本主题 v5（code-tree 主导化） | "索引主体仍由 protocol 承担 + radar 作辅助执行器 + 防上下文爆炸" | 识别 maglev-librarian 在代码层从未有过 AST 能力（Track C 只到根目录锚点）→ code-tree 是绿地新增能力，应由 protocol 主导执行 + 调用 radar 子命令获取摘要，而非"退出 + 推到 radar" |
| 本主题 v5.1（runtime AI 护栏） | "runtime AI 报告契约 + example 模板"——SKILL.md 固定 radar 摘要不展开 + 多 track 状态 4 态模板，每 type 提供 example yaml | 防止 AI 助手在 runtime 解读 radar_summary 时上下文爆炸，以及现场写 track config schema 出错 |

### 5.4 当前事实快照（2026-04-28 扫描）

- `.agents/private-catalog.yaml` 中 15 个 `distribution_scope: 'runtime_internal'` 条目（其中 `maglev-librarian` 标 deprecated，14 个 active）。
- `scripts/maglev_release.py:170-194` 的 `_is_public` **不读 catalog 的 `distribution_scope` 字段** → 当前所有 15 个 runtime_internal 都被错误曝光给 user catalog。
- `packages/maglev-cli/runtime-src/` 下没有 `.agents/` → installer 当前并未分发任何 skill，声明—事实双重错位。
- `index-librarian/SKILL.md` 仅基于 `docs-index-protocol`（六脚本：cognitive_map / archive_triggers / index_scan / index_verify / index_update / index_init），全部聚焦 docs/，不覆盖 specs/ 和仓库入口。
- `maglev-librarian/SKILL.md` 声明 3 Track（L34-37）+ 自带独有脚本 `scripts/smart_map.py`（仓库入口图）。
- 上游 spec `docs_knowledge_archival_methodology/02_design.md` 的 K2 决策只覆盖 Track B，但已对 maglev-librarian 打 `deprecated` 标签。

## 6. 上下文锚点

- 前序主题: `specs/20_evolution/active/docs_knowledge_archival_methodology/`（方法论 + dogfooding 实施；本主题修订其 K2 决策的范围）
- 关键资产 A（待保留）: `.agents/skills/maglev-librarian/`（含 3 Track 能力声明 + `scripts/smart_map.py`）
- 关键资产 B（待扩展）: `.agents/skills/index-librarian/`（仅 Track B；本主题需扩为三 Track 编排）
- 关键资产 C（待扩展）: `.agents/skills/_internal/docs-index-protocol/`（仅 docs/）；可能重命名为 `project-index-protocol`
- 分发载体: `packages/maglev-cli/runtime-src/`（当前为空）
- release 改动落点: `scripts/maglev_release.py`

## 7. 成功判据（粗粒度，按 Step 1-6 锚点）

| Step | 成功信号 |
|---|---|
| **Step 1 撤回 deprecated** | `maglev-librarian` 在 catalog 与 SKILL.md 中恢复为 active；其与 `index-librarian` 的关系标注更新为"等对等性验证后废弃" |
| **Step 2 通用 track 抽象 + 默认 track set** | `registry.yaml` 引入 `tracks:` 字段；generic 脚本（track_scan / track_verify / track_archive_triggers / track_map）实现并能按 track-id 参数化执行；maglev 自己仓库声明 default track set（specs / docs / repo-entry depth=1） |
| **Step 3 index-librarian 重写** | SKILL.md 显式承担"按 registry.yaml tracks 声明执行"；formal_action_name 与 maglev-librarian 一致；显式列出 default track 实例 + 委派 radar 边界 |
| **Step 4 行为对等性验证通过** | 在 default track set 三实例上，新机制相对 maglev-librarian 的输入/输出/触发/失败兜底全覆盖；矩阵 12 行（3 实例 × 4 维度）全 pass |
| **Step 5 物理废弃** | `maglev-librarian/` 删；live 引用清理；历史 trace 保留 |
| **Step 6 用户可用** | 用户 `maglev install` 后能看到 generic 协议 + index-librarian skill + 默认 track 配置；用户可在自己 `registry.yaml` 加 `tracks:` 项扩展；脚本对缺失 root 给清晰退出而非 traceback |

## 8. 设计原则（静默基建）

索引能力是后台基建，不刷存在感：**安装即可用、用错给提示、正常不打扰、主动查可见**。详见 `01_requirements.md` §6。

## 9. 与上游主题的关系

- 本主题**修订**而非 supersede 上游 `docs_knowledge_archival_methodology` 的 K2 决策（"maglev-librarian deprecated"）：上游决策范围只覆盖 Track B，本主题在补齐 + 抽象升级后才真正完成废弃。
- 上游 spec 自身保持 active，但其 `02_design.md` K2 决策段需加修订标注，指向本主题。
- 本主题完成后，`maglev-librarian` 才进入物理废弃状态。

## 10. 与 radar 的关系

- **角色定位**：radar 是 code-tree track 的**辅助执行器**，而非"代码索引能力的替代者"——maglev-librarian 历史上也没有 AST 能力（Track C `smart_map.py` 仅到根目录锚点级别），因此 code-tree 是 v5 的绿地新增能力。
- **协作模式**：generic 脚本主导 code-tree 4 动作；scan 阶段先输出 `anchors:` 段（继承 smart_map.py 的 IGNORE_DIRS/ANCHOR_FILES/MAX_DEPTH/MAX_LINES 防爆模式）；如 track config 启用 `radar_summary.enabled: true`，再 subprocess 调用 radar 子命令（hotspot/unused/cycles）拉取摘要并截断后写入第二段。
- **容错降级**：radar binary 不存在 / 调用超时 / 版本不兼容时，generic 脚本降级为仅输出 anchors 段 + yaml 中记录 `radar_summary: { skipped: true, reason: "..." }` + warn；不阻断后续 track。
- **范围隔离**：仓库根 track（repo-entry）`depth_limit: 1`，不下钻代码目录；code-tree 必须由用户显式声明，maglev 自身 default track set 不预置。
