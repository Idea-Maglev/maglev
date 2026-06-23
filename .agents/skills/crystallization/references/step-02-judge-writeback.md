---
name: judge-writeback
description: 判断哪些变化应写回现实以及写回粒度
next_step: references/step-03-close-active.md
---

# Step 2: Judge Writeback

## 目标

判断哪些变化应写进 `10_reality`，以及该写到哪里、写多细。

## 动作

1. 列出当前主题已成立的变化。
2. 判断哪些变化构成新事实。
3. 判断写回位置：
   - 哪个 reality 文档
   - 哪个模块或章节
4. 判断写回粒度：
   - 事实层
   - 结构层
   - 可发现性层
5. 明确哪些内容不应写回 Reality，而应保留在 active 或归档中。

## 判定规则

- 只有会改变项目当前现状判断的内容，才进入 `10_reality`。
- 过程说明、探索记录、替代方案与临时判断，不进入 `10_reality`。
- 写回粒度优先“最小可维护更新”，避免把 active 文档整体搬进 Reality。
- 不得通过“引用 `90_archive` 中的主题 / 决策文档”来解释当前事实；Reality 应直接表达结晶后的现状。
- `90_archive` 只保留历史依据价值，`20_evolution` 只保留进行中主题；两者都不是 Reality 的主体承载面。

### 回写质量卡点（防堆砌）

写入前必须逐项确认：

1. **能力级而非实现级**？描述的是"能做什么"，不是"内部怎么实现的"
2. **合并而非追加**？应更新已有章节，而非新增章节
3. **当前状态而非变更记录**？表述为"X 是 Y"，而非"X 从 A 改为 Y"或"X 已退役"
4. **删除检验**？如果删掉这条，reality 的描述会不会出错？如果不会，不写入

## 输出格式

- `writeback_required: yes | no`
- `writeback_targets`
- `writeback_granularity`
- `non_writeback_items`

## 输出

- 一份 Reality 回写判断
- 一组不应回写的过程信息
