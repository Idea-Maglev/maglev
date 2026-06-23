---
name: backfill-discovery
description: 必要时触发地图与索引回填，保证新现实可被发现
next_step: references/step-05-archive-with-log.md
---

# Step 4: Backfill Discovery

## 目标

确保新现实不只被写回，还能被后续会话发现。

## 动作

1. 判断当前主题变化是否影响：
   - 项目地图
   - 索引 / 导航
2. 若影响地图，调用或转交 `maglev-map-maker`。
3. 若影响索引，调用或转交 `index-librarian`。
4. 输出当前主题是否已完成可发现性回填。

## 触发规则

- 影响 `10_reality` 结构时，优先考虑 `maglev-map-maker`
- 影响入口、目录、索引或可检索路径时，优先考虑 `index-librarian`
- 若当前主题变化不影响后续发现路径，可以显式输出"无需回填"

## 输出格式

- `discovery_backfill_required: yes | no`
- `map_backfill`
- `index_backfill`
- `downstream_actions`

## 输出

- 一份可发现性回填判断
- 一组必要的下游回填动作
