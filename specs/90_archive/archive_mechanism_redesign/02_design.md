# Design: 归档机制重设计

## 变更总览

| # | 文件 | 变更类型 | 说明 |
|---|------|---------|------|
| A | `references/step-05-archive-with-log.md` | 新建 | 归档执行步骤 + 日志模板 + 门禁 |
| B | `references/step-04-backfill-discovery.md` | 修改 | `next_step: null` → 指向 Step 5 |
| C | `references/crystallization.workflow.md` | 修改 | 流程增加 Step 5 |
| D | `SKILL.md` | 修改 | 归档从"可选"升级为"close 时必选" |
| E | `specs/20_evolution/active/README.md` | 修改 | 新增本 spec 索引条目 |
| F | `specs/90_archive/README.md` | 修改 | 升级为结构化归档索引模板 |

## 变更 A: step-05-archive-with-log.md（新建）

```markdown
---
name: archive-with-log
description: 当 active 判定 close 时，执行结构化归档
next_step: null
---

# Step 5: Archive with Log

## 目标

在 active close 后，将已完成的 spec 归入 90_archive，并附带结构化归档日志。

## 触发条件

仅当 Step 3 判定 `active_decision: close` 时执行此步骤。若为 `continue` 或 `split`，输出 `skipped: not a close decision` 后结束。

## 前置条件（门禁）

在执行文件搬迁前，逐项确认：

1. ✅ Step 2 的 Reality 回写已执行（10_reality 有对应更新）
2. ✅ spec README 已更新状态为 Archived
3. ✅ 归档日志已填写到 spec README 中
4. ✅ 90_archive/README.md 索引条目已准备

**任意一项未通过 → 报告缺失项，不执行搬迁。**

## 动作

1. 在 spec README 中填写归档日志（按模板）
2. 更新 spec README 状态为 Archived
3. 准备 90_archive/README.md 索引条目
4. 执行 4 项门禁检查
5. 全部通过后执行 mv
6. 更新 20_evolution/active/README.md（移除条目）

## 归档日志模板

在 spec README 的状态段落后新增：

## 归档日志

- **结晶状态**：✅ 已完成 → [10_reality/01_requirements.md §X.X]
- **关键结论**：[1-3 句概括写入 reality 的核心内容]
- **执行经验**：[这个需求实际执行中的经验/教训]
- **时间线**：YYYY-MM-DD 启动 → YYYY-MM-DD 归档

## 输出格式

- `archive_gate_passed: yes | no`
- `gate_failures`（如有）
- `archive_log_summary`

## 输出

- 一份门禁检查结果
- 一份已填写的归档日志
- 一组执行的文件操作
```

## 变更 B: step-04-backfill-discovery.md（修改）

将 Step 4 正式链接到 Step 5：

```diff
- next_step: null
+ next_step: references/step-05-archive-with-log.md
```

Step 5 自身负责判断是否执行（非 close 时跳过），Step 4 无需关心路由逻辑。

## 变更 C: crystallization.workflow.md（修改）

流程增加 Step 5：

```diff
 ## 流程 (Process)

 1. 结晶条件确认
 2. 现实回写判定
 3. active 状态收口
 4. 可发现性回填
+5. 结构化归档（仅当 Step 3 判定 close 时）
```

## 变更 D: SKILL.md（修改）

在"归档反模式"章节，将"归档过程记录（可选）"改为：

```diff
 正确的归档操作：

 1. **提取结论** → 写入 `10_reality`（当前事实）
 2. **收口 active** → 标记状态（结束/继续/拆分）
-3. **归档过程记录**（可选）→ 移入 `90_archive`
+3. **结构化归档**（close 时必选）→ 填写归档日志 + 通过门禁 + 移入 `90_archive`
+
+详见 `references/step-05-archive-with-log.md`。
```

## 变更 E: active/README.md（修改）

新增本 spec 索引条目。

## 变更 F: 90_archive/README.md（升级为结构化模板）

当前 90_archive/README.md 只有链接列表，缺少摘要和结晶状态。升级为：

```markdown
# specs archive index

> 项目编年史：记录已完成需求的结晶状态、关键结论和执行经验。
> 日常运作中偏忽略，仅在分析、溯源和复盘时读取。

## 归档口径

归档条目满足以下条件：
1. 已完成结晶 — 结论已写入 `10_reality`
2. 已填写归档日志 — 包含结晶状态、关键结论、执行经验、时间线
3. 不再作为当前活跃工作面

## 归档条目

| # | 主题 | 结晶状态 | 关键结论 | 归档时间 |
|---|------|---------|---------|---------|
| 1 | [skill_structural_upgrade](./skill_structural_upgrade/) | ⚠️ 历史条目 | — | pre-v2 |
| ... | | | | |
| N | [新归档条目](./xxx/) | ✅ → 10_reality §X.X | 一句话结论 | YYYY-MM-DD |

## 当前进行中主题

→ [20_evolution/active/README.md](../20_evolution/active/README.md)
```

**此变更为 Step 5 的强卡点**：每次归档时必须同步更新 90_archive/README.md 的索引表，填写结晶状态和关键结论。不更新此表 = 门禁不通过。

对应 Step 5 门禁修改为 5 项：

1. ✅ 10_reality 有对应更新（结晶已完成）
2. ✅ spec README 已标记 Archived + 已填写归档日志
3. ✅ **90_archive/README.md 索引表已更新**（含结晶状态和关键结论）
4. ✅ 20_evolution/active/README.md 已移除条目

## 验证计划

### V1: 端到端验证（用 lifecycle_closure_disambiguation 实操）

实施完成后，以 `lifecycle_closure_disambiguation` 为首个实操对象，走完完整结晶+归档流程：

1. 调用 crystallization skill
2. Step 1: 确认就绪 → 应判定 ready（已实施完毕）
3. Step 2: 判断回写 → 应识别 10_reality §2.9 已有更新（之前已写入）
4. Step 3: 收口 active → 应判定 close
5. Step 4: 回填发现性 → 判断是否需要
6. **Step 5: 结构化归档 → 验证门禁 4 项全部通过后执行**

验收：
- spec README 包含完整归档日志（4 个字段均非空）
- 90_archive/README.md 索引表有新行（含结晶状态和关键结论）
- active/README.md 已移除该条目
- 文件已在 90_archive/ 目录下

### V2: 门禁拦截验证

模拟以下场景，确认门禁能阻止不完整归档：

| 场景 | 预期结果 |
|------|---------|
| 未写入 10_reality 就归档 | Step 5 报告"结晶未完成" |
| 未填写归档日志就归档 | Step 5 报告"归档日志缺失" |
| 未更新 90_archive/README.md 就搬迁 | Step 5 报告"索引表未更新" |

### V3: 模板结构验证

检查实施后的文件结构：

- `step-05-archive-with-log.md` 存在且包含门禁清单和日志模板
- `crystallization.workflow.md` 包含 Step 5
- `SKILL.md` 的归档操作标记为"close 时必选"
- `90_archive/README.md` 使用结构化索引表模板
