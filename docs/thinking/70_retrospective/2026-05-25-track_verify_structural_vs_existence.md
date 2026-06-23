# track_verify 的能力盲区：结构检查 ≠ 产物存在性检查

> **Context**: 用户要求做索引自查时，`track_verify` 对所有 track 均报 "ok"，但实际上 `specs/_meta/index.yaml` 并不存在。
> **Date**: 2026-05-25
> **Origin**: v0.4.2 开发会话中索引巡检环节

## 发现过程

1. 用户执行 "做一下索引的自查与修复"
2. AI 对所有 track 运行 `track_verify` → 全部返回 "ok"
3. 用户质疑："为什么 verify 通过了，但 `specs/_meta/index.yaml` 不存在？"
4. 根因：`track_verify` 仅做**结构性检查**（track 配置是否合法、字段是否完整），不检查**产物是否实际生成**

## 教训

| 维度 | 旧理解 | 正确理解 |
|------|--------|----------|
| verify 语义 | "索引产物存在且正确" | "track 配置结构合法" |
| 产物检查 | verify 应该覆盖 | 需要 scan 才能生成产物 |
| 正确巡检流程 | 单步 verify | scan → verify → map（三步完整） |

## 修复

在 dir-tree 重构中，`_verify_dir_tree()` 新增了：

- 检查 output 文件是否存在
- 检查各目录的 INDEX.md 是否存在
- 检查 INDEX.md frontmatter 有效性

这使 verify 从纯结构校验升级为**产物存在性 + 结构正确性**双重检查。

## 反模式提示

> 如果一个 verify 函数只能验证"输入格式对不对"而无法发现"输出缺不缺"，它给人的绿灯是假的。
> 巡检三步曲 scan → verify → map 应该作为整体执行，不要单独依赖 verify。
