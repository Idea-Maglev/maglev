---
status: active
opened_at: 2026-04-27
last_revised_at: 2026-04-28
revision: v5.2 (consistency fix)
mode: prd_document
---

# Requirements

> ⚠️ **v4 在 v3 PR-A 基础上再升一级抽象**：v3 写死三 Track 名（specs/docs/repo），v4 改为"generic 索引能力 + registry.yaml 声明式 tracks + 默认窄范围 + 不侵入代码 + 委派 radar"。修订理由见 `00_intent.md` §4.4。

## 1. 核心对象 (core_object)

让 `index-librarian` + 协议脚本演进为**通用项目级索引能力**：通过 `registry.yaml` 声明式 `tracks:`，generic 脚本对任意目录对象按统一协议跑索引/统计/认知图/归档触发；maglev 自己仓库声明 default track set（specs / docs / repo-entry），用户可在自己 `registry.yaml` 加 `tracks:` 项扩展，但默认窄范围、不侵入代码、必要时委派 radar。在三 default track 实例上完成行为对等性验证后物理废弃 `maglev-librarian`，并把这套通用能力随 `maglev install` 分发到用户项目作为静默基建。

## 2. 目标用户 (target_user)

- **主消费方**：装了 maglev 的项目维护者（pip install maglev 之后想在自己的 specs/、docs/、仓库入口上跑索引/统计/认知图）。
- **次消费方**：Maglev 维护者自己（修齐声明—事实错位、修复"早打 deprecated"造成的真空期风险）。
- **不是**：终端最终用户（这是基建能力，不是面向最终用户的功能）。

## 3. 协作上下文 (collaboration_context)

- 上一会话末尾用户质询"这套是不是 maglev 用户共用的对吧"。
- 本会话两轮对抗性审计揭示双重错位：
  - 错位 1：catalog 声明 runtime_internal 的 15 个对象当前**全部错误曝光**（release.py 不读 distribution_scope 字段）。
  - 错位 2：`maglev-librarian` 已被上游打 deprecated 标签，但替代品 `index-librarian` 仅覆盖 Track B，缺 Track A/C → 标签是早打的。
- 用户拍板 PR-A：直接扩本主题边界覆盖 Step 1-6 全包。
- 本主题需稳定文档基线，避免 spec-designer 阶段反复回头追问"覆盖什么/谁先废弃"。

## 4. In Scope（本轮要做）

1. **Step 1**：撤回 `maglev-librarian` 的 deprecated 标签，改回 active；标注"等对等性验证后再废弃"。
2. **Step 2**：在 `_internal/docs-index-protocol/registry.yaml` 引入 `tracks:` 声明式 schema；实现 generic 脚本（`track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py`）按 `--track-id` 参数化执行；声明默认 track set（specs / docs / repo-entry）。
3. **Step 3**：重写 `index-librarian/SKILL.md`，描述层"按 registry.yaml tracks 声明执行"；显式列出 default track 实例 + 委派 radar 边界。
4. **Step 4**：建立行为对等性验证矩阵——在 default track set 三实例上，generic 脚本相对 maglev-librarian 全覆盖。
5. **Step 5**：仅在 Step 4 通过后物理废弃 `maglev-librarian`。
6. **Step 6**：通过 release.py 调整把 generic 协议 + index-librarian + 默认 track 配置随 runtime 分发到用户。
7. **建立持续防漂移机制**：声明—事实一致性校验脚本。
8. **静默基建合规**：用户接入零交互、零 banner、零教程。
9. **修订上游 spec K2 决策**：加修订标注，指向本主题。
10. **代码索引边界（v5 修订）**：track schema 支持 type=code-tree；scan 输出 anchors + （可选）radar_summary 两段；防爆参数继承 smart_map.py；radar 不可用时降级。repo-entry track depth_limit=1 不变。

## 5. Out of Scope（本轮不做）

1. `docs-index-protocol` 已稳定的 schema/lifecycle 方法论修改。
2. 其他 `_internal/` skill（`spec-pipeline`、`ai-context-check`）的 runtime 化。
3. AGENTS.md / `private-catalog.yaml` 的结构治理。
4. installer 的整体重构。
5. archive_triggers / cognitive_map 阈值的复杂参数化（仅要求集中声明 + per-track 覆盖）。
6. 用户项目颗粒度差异的自动适配（用户可手工调阈值/track）。
7. **代码仓库的完整 AST / 调用图 / 死代码深度分析**——由 `radar` skill 承担；本主题 code-tree 仅以摘要形式（hotspot Top N / cycles 计数 / unused 计数）调用 radar 子能力，不重新实现 AST。
8. 跨 track 关系图（specs ↔ docs ↔ repo 之间的边）——本主题先做 per-track 索引。
9. 用户 track 配置错误时的自动修复——用户自负责。
10. 在用户项目里造任何 demo `docs/` 或 `specs/` 目录。

## 6. 设计原则（贯穿全文，spec-designer 应保留）

**索引能力是公共能力 + 静默基建**：

- 通用化 → 索引脚本不绑定具体目录名；通过 `registry.yaml tracks:` 声明对象
- 默认窄范围 → maglev 自己预置 specs/docs/repo-entry；用户加 track 是显式动作
- 不侵入代码 → 默认 track 不下钻代码目录；code-tree 由用户显式声明；防上下文爆炸通过继承 smart_map.py 防爆参数 + radar 摘要截断（v5）
- 安装即可用 → 不需要 `maglev enable`
- 用错给提示 → 不需要预设教程
- 正常不打扰 → install 不打 banner
- 主动查可见 → catalog / `.agents/` 树客观存在

**先补齐再废弃**：

- 任何在替代品未覆盖之前的 deprecated 标签，都应被识别为"早打标签"并撤回。
- deprecated 状态应是替代完成后的最终状态。

## 7. Success Signal（最低成功信号）

1. **Step 1 完成**：`maglev-librarian` catalog 与 SKILL.md 不再标 deprecated；标注"等对等性验证后废弃"。
2. **Step 2-3 完成**：新机制能在三 Track（specs / docs / repo-entry）上输出与 maglev-librarian 同等价值的产物。
3. **Step 4 通过**：行为对等性验证矩阵每行勾选；缺项不允许进入 Step 5。
4. **Step 5 完成**：`maglev-librarian` 物理移除；`90_archive/`、thinking、contribution_log 等历史档案保留。
5. **Step 6 完成**：用户在干净项目 `maglev install` 后能看到新机制资产；脚本对缺失目录给出清晰退出；声明—事实校验脚本本地与 CI 都可运行；install 流程不为本能力 banner。
6. **上游修订标注**：`docs_knowledge_archival_methodology/02_design.md` K2 段已加 PR-A 修订引用。

## 8. Key Unknowns（仍开放，留给 spec-designer 决策）

| ID | 未知 | 影响 |
|---|---|---|
| **U-PR1** | `_internal/docs-index-protocol/` 是否重命名为 `project-index-protocol` | 命名 / 引用半径 |
| **U-PR4** | `index-librarian.formal_action_name` 是改回"项目索引维护"还是保持"索引管理" | 路由匹配 |
| **U-PR5** | 行为对等性"通过"的定义——是输入/输出严格一致，还是覆盖等价能力 | Step 4 通过门槛 |
| **U-V4-1** | track schema 必填字段集——type / root / patterns / output / thresholds / depth_limit / delegate_to 中哪些必填 | schema 复杂度 vs 表达力 |
| **U-V4-2** | 用户能否禁用 default track（如不要 specs/）——是允许 disable 字段还是不允许 | 默认契约的强度 |
| **U-V4-3** | （v5 已关闭）`delegate_to: radar` 的具体调用契约——v5 决定 radar 作辅助执行器（subprocess invoke），见 02_design D7/D24/D26 | 实现复杂度 |
| **U-V5-1** | radar binary 在 maglev 安装链路中的可用性保障——是否在 installer 检测 / 是否文档建议用户单独安装 | 容错降级触发频率 |
| **U-V5-2** | `radar_summary.max_output_lines` 默认值 200 是否需要因不同语言/项目规模调整 | 上下文爆炸阈值 |

## 9. 漂移风险 (drift_risk)

如果不做这轮文档落盘：

1. **早打 deprecated 真空期会扩散**：开发者依赖 maglev-librarian 的能力会在没有等价替代时被告知"已废弃"，造成误解。
2. **三 Track 覆盖如果不在 Step 2/3 显式落实，会被"docs 已就绪"误导**：v1/v2 已经犯过一次该错。
3. **行为对等性如果不立矩阵，"覆盖了"会变成主观判断**：Step 4 没有客观门槛就会被绕过。
4. **声明—事实错位会再次出现**：不固化校验脚本，下次新增 runtime_internal 对象仍会重蹈覆辙。
5. **上游 K2 决策不修订**：跨主题决策错配会沉淀为系统性技术债。

## 10. 期望产物 (expected_prd_outcome)

- 本主题最终固定住的：①Step 1-6 各 Step 的可验证完成信号；②三 Track 能力清单；③静默基建原则；④脚本兜底策略；⑤声明—事实一致性校验机制；⑥上游 K2 修订标注。
- 这份 `01_requirements.md` 在多会话切换时仍是稳定基线。

## 11. 下游消费方 (downstream_consumers)

- `spec-designer`（**主消费方**）：进入设计阶段消费功能需求 + 静默原则 + 五项关键未知。
- `context-implementer`：编码时按 AC 实施，按 Step 1-6 顺序执行。
- `integrated-validator`：验证时按 AC + 行为对等性矩阵检验。
- `crystallization`：本主题完成后回写到 reality；同时回写上游主题的 K2 修订关系。

---

## 12. 功能需求 (Functional Requirements)

### F1 — Step 1：撤回 maglev-librarian 早打的 deprecated 标签

> 作为索引能力的潜在使用者，我不希望在替代品尚不完整时，被告知现有能力已废弃；维护者也不应分发一个"已废弃但仍是唯一完整能力"的对象。

| AC ID | 验收标准 |
|---|---|
| **AC-F1-1** | `.agents/private-catalog.yaml` 中 `maglev-librarian` 条目应改回 `status: active` 或 `status: deprecation_pending`（任一显式表达"等替代品就绪"的状态）；`runtime_name_status: deprecated` 同步撤回。 |
| **AC-F1-2** | `.agents/skills/maglev-librarian/SKILL.md` 顶部 metadata 与说明文案应去除"deprecated"语义，改为"replacement in progress（被 index-librarian 替代中，等三 Track 对等性验证完成后退役）"。 |
| **AC-F1-3** | catalog 中 `index-librarian` 的 relations 字段保留 `replaces: maglev-librarian` 边，但语义从"已替代"调整为"替代中"。 |
| **AC-F1-4** | Step 1 完成后无任何 live 路由会因"找不到 maglev-librarian"而失败——`workflows/maglev-librarian.md` 保持原状。 |

### F2 — Step 2：通用 track 抽象 + 默认 track set

> 作为新机制的设计者，我需要确保索引能力是 generic 的——脚本对任意 registry.yaml 中声明的 track 都能跑，并预置默认 track set 满足 maglev 自身需求。

| AC ID | 验收标准 |
|---|---|
| **AC-F2-1** | `_internal/docs-index-protocol/registry.yaml` 应引入 `tracks:` 顶级字段，每个 track 至少包含：`id`（标识符）、`type`（如 `docs-tree` / `spec-tree` / `repo-entry` / `code-tree`）、`root`（目录路径）、`output`（索引产物路径），可选字段：`patterns`、`thresholds`、`depth_limit`、`delegate_to`。 |
| **AC-F2-2** | 应实现 generic 脚本 `track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py`，全部接受 `--track-id <id>` 参数，从 registry.yaml 读对应 track 配置执行。 |
| **AC-F2-3** | `_internal/docs-index-protocol/registry.yaml`（maglev 自身）应声明默认 track set：① `id: specs` type=spec-tree root=`specs/`；② `id: docs` type=docs-tree root=`docs/`；③ `id: repo-entry` type=repo-entry root=`.` depth_limit=1。 |
| **AC-F2-4** | 现有 6 个 docs 脚本（cognitive_map / archive_triggers / index_scan / index_verify / index_update / index_init）应保留作 docs-tree type 的 backing 实现，或被 generic 脚本完全替代——v4 02_design 决策。 |
| **AC-F2-5** | repo-entry track 的 `depth_limit: 1` 应被 generic 脚本严格遵守——不下钻到子目录；只扫元数据文件（README/AGENTS.md/llms.txt/CHANGELOG/package.json 等可配置 patterns）。 |
| **AC-F2-6** | track schema 应支持 type=code-tree；generic 脚本对该 type 主导执行 4 动作（详见 F12），不再 exit 0；schema 仍可向后兼容 `delegate_to: radar` 字段（视为旧式标记，行为按 type 决定）。 |
| **AC-F2-7** | 用户可在自己项目的 `.agents/skills/_internal/docs-index-protocol/registry.yaml`（或 install 后等价路径）追加 `tracks:` 项；index-librarian 应能识别用户新增 track 并调度执行。 |
| **AC-F2-8（v5.1 runtime AI 护栏）** | 每 type（spec-tree / docs-tree / repo-entry / code-tree）应有对应 example 模板文件，路径 `_internal/docs-index-protocol/registry.example.<type>.yaml`；用户或 AI 助手帮用户新增 track 时应**复制 example 后再修改**，而非凭记忆现场写 schema。AC 校验：4 个 example 文件存在 + 每个文件含完整必填+常用可选字段 + SKILL.md 引用 example 路径。 |

### F3 — Step 3：index-librarian 重写为 generic 编排

> 作为索引能力的统一入口，`index-librarian` 应按 `registry.yaml tracks:` 声明动态调度，不写死具体 Track 名。

| AC ID | 验收标准 |
|---|---|
| **AC-F3-1** | `.agents/skills/index-librarian/SKILL.md` 描述层应明示"按 `_internal/docs-index-protocol/registry.yaml` 中 `tracks:` 声明执行"，列出 default track 实例（specs/docs/repo-entry）作示例。 |
| **AC-F3-2** | `formal_action_name` 决策（U-PR4）落实——若改回"项目索引维护"则与 maglev-librarian 完全对齐。 |
| **AC-F3-3** | catalog 中 `index-librarian.metadata` 字段应与 maglev-librarian 现状一致或显式说明差异。 |
| **AC-F3-4** | `index-librarian` 应能依次调度多 track 执行，单 track 失败不阻断其他 track（清晰错误 + 继续）。 |
| **AC-F3-5** | SKILL.md 应显式声明委派 radar 的边界："代码仓库依赖/调用图分析请使用 radar skill；本能力仅做目录索引/统计/归档触发。" |

### F4 — Step 4：行为对等性验证（在 default track set 实例上）

> 作为本主题质量门槛，必须证明 generic 脚本在 default track set 三实例上不弱于 maglev-librarian。

| AC ID | 验收标准 |
|---|---|
| **AC-F4-1** | 02_design 中应包含**行为对等性验证矩阵**，覆盖 default track set 3 实例 × 4 维度（输入/输出/触发/失败兜底）共 12 行；每行注明 maglev-librarian 现状、新机制（generic 脚本 + 该 track 配置）现状、对等性结论（pass/partial/miss）。 |
| **AC-F4-2** | 验证矩阵任一行为 `partial` 或 `miss` 时，**禁止**进入 Step 5；必须先补齐到 pass。 |
| **AC-F4-3** | 矩阵执行结果应作为本主题强制 gate——记录在 status.md 的 "Step 4 验证记录" 段。 |
| **AC-F4-4** | 对等性"通过"定义（U-PR5）：本轮采用"覆盖等价能力 + 输出可被相同消费方读取"标准，不要求 byte-identical。 |
| **AC-F4-5** | 用户新增 track 不在对等性验证范围内（用户自负责），但 generic 脚本对其失败处理应同样遵循 F7 兜底协议。 |

### F5 — Step 5：物理废弃 maglev-librarian

> 仅在 Step 4 通过后，对旧对象执行物理清理；保留历史 trace。

| AC ID | 验收标准 |
|---|---|
| **AC-F5-1** | `.agents/skills/maglev-librarian/` 目录及其 references/、scripts/ 全部删除。 |
| **AC-F5-2** | `.agents/workflows/maglev-librarian.md` 删除。 |
| **AC-F5-3** | `.agents/private-catalog.yaml` 中 `name: 'maglev-librarian'` 整段删除；`index-librarian.relations` 中 `replaces: maglev-librarian` 边的语义改为"已替代"。 |
| **AC-F5-4** | live 区域引用改写：`issues/draft/draft_issue_capability_matrix_skills.md` 中 3 处 `maglev-librarian` 改为 `index-librarian`。 |
| **AC-F5-5** | 历史 trace 保留：`90_archive/`、`docs/thinking/`、`contributors/contribution_log.md`、`archive/starter-kit_legacy/`、上游 spec `docs_knowledge_archival_methodology/` 自身、`specs/10_reality/01_requirements.md:31` 等保持原文。 |
| **AC-F5-6** | `index-librarian` 自身 SKILL.md 与 `crystallization/references/step-04-backfill-discovery.md` 中"取代废弃的 maglev-librarian"等迁移说明保留作历史参照。 |
| **AC-F5-7** | Step 5 执行前最后一次 `grep -rn maglev-librarian .` 影响半径扫描，对照白名单（C 类历史 trace）确认无非预期残留。 |

### F6 — Step 6：用户分发与 release 修齐

> 作为安装 maglev 的开发者，我希望 maglev 安装后我项目的 `.agents/` 下出现新的项目级索引能力，而不需要主动开关或配置。

| AC ID | 验收标准 |
|---|---|
| **AC-F6-1** | 用户在干净项目执行 `maglev install` 后，`.agents/skills/_internal/<project-index-protocol or 现命名>/` 与 `.agents/skills/index-librarian/` 应出现在用户项目。 |
| **AC-F6-2** | 用户侧 `private-catalog.yaml` 不曝光全部 14 个 active runtime_internal 条目（曝光指 `distribution_scope: 'runtime_internal'` 字段在 user catalog 中应被剔除）。 |
| **AC-F6-3** | release.py 应在装配产物前完成"runtime_internal 对象 → BUILD_DIR copytree"动作；缺路径时 fail-fast。 |
| **AC-F6-4** | installer 保持零改动；新增/修改文件随 manifest 自动覆盖到用户侧。 |
| **AC-F6-5** | 用户已有 `private-catalog.yaml` 与新版冲突时，复用 installer 现有 `.local_backup_<ts>` 备份机制。 |

### F7 — 脚本对目录假设的解耦 + 默认窄范围

> 作为初次使用这套机制的用户，缺失目录不该崩溃；同时默认行为不能把整个仓库当作扫描对象。

| AC ID | 验收标准 |
|---|---|
| **AC-F7-1** | generic 脚本在 track root 路径不存在时，应输出明确"未找到 track <id> 的 root 路径 <path>"提示并以 exit 0 退出。 |
| **AC-F7-2** | `track_map.py --inject` 在缺失元数据子目录（如 `_meta/`）时按需创建（懒创建）。 |
| **AC-F7-3** | `track_archive_triggers.py` 在缺失归档段（如 `90_archive/`）时输出"该 track 尚无归档段"+ exit 0。 |
| **AC-F7-4** | 错误输出统一格式：`Error: <reason>\nTip: <可复制初始化指令>`；Python traceback 仅在 `--debug` 时保留。 |
| **AC-F7-5** | repo-entry track 严格遵守 depth_limit=1，不下钻到任何子目录（包括代码目录与文档目录）。 |
| **AC-F7-6** | 当未声明任何 track（用户清空 tracks:）时，`index-librarian` 应输出"未声明 track，跳过"+ exit 0；不擅自创建默认。 |
| **AC-F7-7** | generic 脚本不应主动遍历未声明 track 的目录（如不应自动扫描 src/ 即使存在）。

### F8 — 阈值与配置集中化

> 作为多样化项目的接入方，我希望阈值在我项目颗粒度小时不会刷屏，且能调。

| AC ID | 验收标准 |
|---|---|
| **AC-F8-1** | archive 触发器、cognitive map、verify health 等阈值集中在 `_internal/<project-index-protocol>/registry.yaml` 一处声明。 |
| **AC-F8-2** | 至少一个 documented 的覆盖路径（`registry.yaml` 字段被 spec-designer 拍板）。 |

### F9 — 声明—事实一致性校验

> 作为 Maglev 维护者，我希望 catalog 中所有 runtime_internal 对象都真的在 runtime 产物里，避免再次出现错位。

| AC ID | 验收标准 |
|---|---|
| **AC-F9-1** | 应有独立可执行脚本（`scripts/check_runtime_distribution.py`）能比对 `private-catalog.yaml` 的 runtime_internal 列表与文件系统/BUILD_DIR 产物，差异时报错。 |
| **AC-F9-2** | release.py 应在 step1b 引用同款逻辑作为 pre-flight。 |
| **AC-F9-3** | 当 catalog 添加新 runtime_internal 对象但未加入 manifest 路径时，AC-F9-1 校验应失败。 |
| **AC-F9-4** | 校验脚本应可在 CI 单独运行，不依赖完整 release 流水线。 |

### F10 — 静默基建合规

> 作为安装 maglev 的开发者，我不希望被告知"这里有个新能力请关注"。

| AC ID | 验收标准 |
|---|---|
| **AC-F10-1** | `maglev install` 完成时，安装日志中**不应**为本主题能力单独打 banner、教程或试运行命令。 |
| **AC-F10-2** | `legacy-adopter` / `bootstrapper` 接入时**不应**就本能力提问"是否启用"。 |
| **AC-F10-3** | 能力的存在通过 `.agents/` 树的客观出现来体现；用户主动 `cat catalog` 或运行 `maglev list-skills`（若存在）能看到。 |

### F11 — 上游 spec K2 修订标注

> 作为跨主题决策溯源者，应能从上游 spec 找到本主题的修订关系。

| AC ID | 验收标准 |
|---|---|
| **AC-F11-1** | `specs/20_evolution/active/docs_knowledge_archival_methodology/02_design.md` 的 K2 决策段落应加修订标注，指向本主题（`runtime_distribute_project_index_protocol`）。 |
| **AC-F11-2** | 上游 spec 的 status.md 顶部加一条决策修订记录条目。 |
| **AC-F11-3** | 不修改上游 spec 的核心决策内容——只加"本决策范围已被本主题修订"的元标注。 |

---

### F12 — code-tree track 与 radar 的协作边界（v5 重写）

> 索引创建主体责任在本主题；radar 作为代码场景的**辅助执行器**承担依赖/死代码分析的子能力调用。整体设计点是"防上下文爆炸"。

| AC ID | 验收标准 |
|---|---|
| **AC-F12-1** | type=code-tree 的 track 由 generic 脚本主导执行 4 个动作；scan 输出至少包含 `anchors:` 段（锚点文件 + 目录树，复刻 smart_map.py 锚点逻辑）；不再"退出 + 提示用 radar"。 |
| **AC-F12-2** | track config 中 `radar_summary.enabled: true` 时，generic 脚本应 subprocess invoke radar 子命令拉取摘要（默认 hotspot Top N + cycles 计数 + unused 计数），并截断到 `max_output_lines` 后写入 yaml `radar_summary:` 段；摘要段未启用时该段省略。 |
| **AC-F12-3** | radar binary 不存在 / 调用超时 / 版本不兼容时，generic 脚本应降级为仅输出 `anchors:` 段 + 在 yaml 中记录 `radar_summary: { skipped: true, reason: "..." }` + 控制台 warn；不阻断后续 track 执行。 |
| **AC-F12-4** | code-tree 的防爆参数应继承 `scripts/smart_map.py` 现有常量为 generic 默认值（IGNORE_DIRS / ANCHOR_FILES / MAX_DEPTH=5 / MAX_LINES=200）；track config 可在 `radar_summary.*` 字段细化。 |
| **AC-F12-5** | maglev 自身 `registry.yaml` 不预置 type=code-tree 的 default track；用户如需扫代码自行声明 track 实例（这是显式动作，符合"默认窄范围"原则）。 |
| **AC-F12-6** | `index-librarian/SKILL.md` 应说明：code-tree 的依赖分析能力由 radar 提供；本协议负责调度与摘要落盘；用户若需要原始依赖图请直接使用 radar skill 的对应子命令。 |
| **AC-F12-7** | repo-entry track 的 `depth_limit: 1` 不可被任何 default 配置覆盖；code-tree 的 depth_limit 默认 5（同 smart_map），用户可在 track config 调整。 |
| **AC-F12-8（v5.1 runtime AI 护栏）** | `index-librarian/SKILL.md` 必须固定 `radar_summary` 段的 user-facing 报告契约——**仅统计行 + Top 3 hotspot 名称**，禁止逐个展开 hotspot/unused/cycles 列表；超过 Top 3 的部分以 "(+N more)" 提示并指引用户用 `radar` skill 直接查询。AC 校验：SKILL.md 含明文 "禁止展开 radar 详细列表" 段；index-librarian 单 track 报告示例 ≤ 5 行。 |
| **AC-F12-9（v5.1 runtime AI 护栏）** | `index-librarian/SKILL.md` 必须固定**多 track 状态报告模板**：每 track 一行 `{track-id}: {status} ({summary})`，status 枚举值仅 `ok` / `partial` / `skipped` / `failed` 四态；SKILL.md 含状态语义对照表 + 报告示例。AC 校验：SKILL.md 含报告模板段；index-librarian 在多 track 部分失败场景输出符合模板。 |

## 13. 术语表

- **track**：本主题核心概念——一个声明式的"可索引对象"描述符，包含 id / type / root / patterns / output / thresholds / depth_limit / delegate_to 等字段，由 `_internal/docs-index-protocol/registry.yaml` 中 `tracks:` 列表声明。
- **default track set**：maglev 自身 registry.yaml 预置的 track 实例集合（specs / docs / repo-entry 三个），保证 maglev 仓库自身的索引能力开箱可用。
- **generic 脚本**：`track_scan.py / track_verify.py / track_archive_triggers.py / track_map.py`，对任意 track-id 参数化执行，不绑定具体目录名。
- **runtime 分发**：通过 `pip install maglev`，maglev installer 在用户项目目录写入的文件集合。
- **dogfooding 资产**：Maglev 仓库根 `.agents/` 下、目前只供 Maglev 自己开发使用的 skill 与协议产物。
- **行为对等性矩阵**：default track set 3 实例 × 4 维度的 12 行检查表，作为 Step 5 物理废弃的强制 gate。
- **早打 deprecated**：替代品尚未完整覆盖原对象能力前打的 deprecated 标签。
- **声明—事实错位**：catalog 中 `distribution_scope` 已声明 `runtime_internal` 但 runtime 产物中实际不包含该对象。
- **静默基建**：能力存在但不刷存在感，安装即可用、用错给提示、正常不打扰、主动查可见。
- **默认窄范围**：开箱默认仅扫已声明 default track；不主动遍历整个仓库；用户加 track 是显式动作。
- **不侵入代码**：repo-entry depth_limit=1，仅看根级元数据文件；code-tree 通过防爆参数（IGNORE_DIRS/MAX_DEPTH/MAX_LINES）控制扫描范围，依赖分析子能力委托 radar。
- **PR-A**：v3 主题方向修订记号——Project Repair 路径 A，扩边界一次性完成"完整替代 + 分发"全链路。
- **v4 通用化**：v3 的进一步抽象升级——从写死三 Track 到 generic + 声明式 tracks。
- **v5 code-tree 主导化**：v4 把 code-tree 委派给 radar 退出，v5 改为 protocol 主导执行 + radar 作辅助拉取摘要的两段式输出（anchors + radar_summary）；核心约束从"不侵入代码"细化为"防上下文爆炸"。
- **radar 辅助执行器**：v5 中 radar 在 code-tree 场景的角色——subprocess 被调用提供依赖/死代码摘要，原始大结果由 protocol 截断后落盘，radar 不直接对外输出索引清单。
