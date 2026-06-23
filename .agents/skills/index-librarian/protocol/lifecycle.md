# 文档生命周期方法论（F1，3 态）

> **位置**：`.agents/skills/index-librarian/protocol/lifecycle.md`
> **来源**：`specs/20_evolution/active/docs_knowledge_archival_methodology/01_requirements.md` F1

## 0. 适用范围（Track 维度）

本生命周期方法论（active / crystallized / archived 3 态）**仅适用于产生 `INDEX.md` 网络的 track**：

- ✅ `spec-tree`、`docs-tree`：完整适用，含 §1-§6 全部规则
- ❌ `repo-entry`：仓库根目录锚点产物，无 frontmatter status 概念，不走本生命周期
- ❌ `code-tree`：代码层 anchors + radar 摘要产物，由源码 git 历史 + radar `unused` 等机制管理，不走本 status 字段流转

启用何种 track 由仓库 `registry.yaml` 的 `tracks` 段驱动；同一仓库可同时挂载多种 track，但只有 `spec-tree` / `docs-tree` 的叶子受本文规则约束。

## 1. 三态模型与 MemoryOS 映射

| 生命态 | frontmatter `status` | 物理位置 | MemoryOS 映射 | 含义 |
|:---|:---|:---|:---|:---|
| 成熟 | `active`（或缺省） | `docs/<module>/<segment>/` | **MTM** (Mid-Term Memory) | 已归位段、被 INDEX 索引、可被其他文档引用 |
| 沉淀 | `crystallized` | 同 MTM 位置 | **LPM** (Long-Term Memory) 凝结态 | 被 ≥ 1 处引用 + age ≥ N 月稳定；受保护 |
| 归档 | `archived` | `docs/<module>/90_archive/<segment>/` | 自然遗忘（可恢复） | 已归档但内容保留（git history） |

**默认状态**：缺失 `status` 视为 `active`。这反映真实使用模式——文档落盘时即为成品，无中间草稿态。

## 2. 态间转移

```
   (write to segment)              (cite + age)              (F6 trigger + manual)
   ∅ ----------------> XX_segment/  ----------------> XX_segment/  ----------------> 90_archive/XX/
                       status:active                  status:crystallized            status:archived
                                                       ↑
                                                LPM Protected
                                                (no auto archive)
```

### 显式触发条件

| 转移 | 条件 | 实施 |
|:---|:---|:---|
| (∅ → active) | 作者写下并直接归位段 | `touch docs/<module>/XX_segment/<name>.md` + frontmatter `status: active` 或缺省 |
| active → crystallized | inbound ≥ 1 AND age ≥ N 月（默认 N=3） | 自动检测候选（`crystallization_triggers.py`，未来工作）；人工确认 + 改 frontmatter `status: crystallized` |
| 任意 → archived | F6 三条触发器之一（time_window / supersede / orphan） | `archive_triggers.py --apply` 或 `git mv` 到 `90_archive/<seg>/` |

## 3. LPM 保护规则

**凝结态（`status: crystallized`）不允许自动归档**：

- `archive_triggers.py` 内部检查：候选叶子若 `status == 'crystallized'`，标注 `protected_lpm: true`，不进 `--apply` 路径
- 人工显式归档（包括 LPM）必须 `git mv` + 同步改 `status: archived`
- 这是有意的"沉没成本"：LPM 文档代表已在仓库中形成稳定引用网络，自动迁移会造成大量断链

## 4. 与 F6 归档触发器的关系

| F6 触发器 | 适用 status | LPM 保护 |
|:---|:---|:---|
| time_window (>= M 月无 commit) | active | ✅ crystallized 不进 apply |
| supersede (`superseded_by` 字段) | 任意 | ⚠️ crystallized 也允许（前提：人工已写 superseded_by） |
| orphan (inbound=0 + age >= N 月) | active | ✅ crystallized 不进 apply |

## 5. 实施现状

- ✅ schema §6.2 已声明 status 枚举（`active / crystallized / archived`，3 态）
- ✅ schema §6.6 保留区仅列 `_meta/`
- ✅ archive_triggers.py LPM 保护（`status == 'crystallized'` 自动跳过 --apply）
- ⚠️ `crystallization_triggers.py`（active → crystallized 自动候选检测）暂未实现，留作 F1 后续
- ⚠️ verify status 字段为软约束（缺失视为 active）；老叶子大量缺 status 不再视为缺陷

## 6. 工程化要点（与脚本契约）

1. **scripts 排除规则**：所有脚本（`index_update.py` / `index_verify.py` / `archive_triggers.py` / `cognitive_map.py`）在收集叶子时跳过：
   - `_meta/` 子树（机读元数据，如 `knowledge_graph.json`）
   - `90_archive/` 子树（archive_triggers 排除评估，但 update/verify 仍需扫到以维护索引一致性）
   - 任何以 `.` 开头的目录

2. **status 字段读取**：从叶子 frontmatter 读 `status`，缺失视为 `active`（贴合真实使用模式的默认值）

3. **态机一致性**：物理位置 + frontmatter status 之间存在不变量
   - `XX_segment/*` 顶层 → status ∈ {active, crystallized}
   - `90_archive/*` → status 必须为 `archived`
   - 违反不变量时 verify 应警告（L08 级）

## 7. 撤回 `draft` 态的元洞察（关键）

**真实使用模式**：docs/ 文档基本是 AI+用户在会话末尾"快照式总结"产出，不是撰稿/出版业那种"先写草稿→修改→发布"的过程。每篇文档落盘时**即为成品**——后续修正靠"再写一篇 follow-up"或"红队反思补充"，**不是修改原稿**。

因此：
- `draft` 状态从未被消费（`_drafts/` 直至撤回前 0 篇真实草稿）
- 强行保留 `draft` 是**抽象错位**——MemoryOS / 长篇撰稿的 4 态生命周期借来硬套
- 撤回是承认"骨架先于数据"也有反面：**装好骨架但抽象错位，会比不装更糟**

完整反思见 `docs/thinking/00_meta/2026-04-27-lifecycle_abstraction_overdesign.md`。
