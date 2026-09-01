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
2. 若影响地图，登记 `maglev-map-maker` 为归档后的下游动作；若同时影响活跃状态，必须等待
   `project-board` 更新后再执行。
3. 若影响索引，调用或转交 `index-librarian`。
4. 输出当前主题是否已完成可发现性回填。

## 触发规则

- 影响 `10_reality` 结构时，登记 `maglev-map-maker`
- 影响入口、目录、索引或可检索路径时，优先考虑 `index-librarian`
- 影响 active/归档状态时，顺序固定为 `project-board → maglev-map-maker`
- 若当前主题变化不影响后续发现路径，可以显式输出"无需回填"

### Profile 发现性检查

回填只依据目标项目自己的 Profile、注册页面和索引生成规则：

1. 确认新增或修改页面已经登记到 Profile；
2. 确认模板包声明的项目级入口页按 `target_path` 位于目标 Reality 根目录，未出现未声明的输出容器；
3. 确认索引由 `index-librarian` 从当前事实确定性生成；
4. 不为未登记的跨模块标记、手写 README 约定或旧导航字段增加额外门禁。

## 输出格式

- `discovery_backfill_required: yes | no`
- `map_backfill`
- `index_backfill`
- `downstream_actions`

## 输出

- 一份可发现性回填判断
- 一组必要的下游回填动作
