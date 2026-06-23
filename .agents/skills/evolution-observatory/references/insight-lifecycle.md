# Insight Lifecycle

## 状态定义

| 状态 | 含义 | 进入条件 |
|------|------|----------|
| `open` | 已发现，等待消费 | 研究报告产出时自动创建 |
| `proposed` | 已进入方案设计 | spec-designer 引用此 insight 时 |
| `absorbed` | 已合并实施 | 对应改进已合入 master |
| `superseded` | 被更优方案替代 | Creator 确认后标记 |

## 状态转换规则

```
[创建] → open
         ├── → proposed (spec 引用)
         │       └── → absorbed (改进合并)
         ├── → superseded (被替代, 需人确认)
         └── (长期 open → 触发再评估, 不自动变更)
```

## Insight Record Schema

```yaml
- id: "{PRODUCT}-{NNN}"           # 全局唯一, 产品前缀 + 3位序号
  title: string                    # 一句话描述
  source_report: string            # 产出此 insight 的研究报告路径
  status: open | proposed | absorbed | superseded
  priority: high | medium | low
  target: string                   # 建议改进的目标 skill 或 process
  proposed_spec: string | null     # proposed 状态时填 spec 路径
  absorbed_at: string | null       # absorbed 日期 (ISO 8601)
  superseded_by: string | null     # 替代者的 insight ID
  superseded_reason: string | null # 替代理由
  created_at: string               # 创建日期 (ISO 8601)
```

## Insight Review 规则

每轮研究 Phase 2 自动执行，评估所有 `status: open` 的 insights：

### 评估维度

1. **框架演进**: 该 insight 依赖的框架是否有重大版本更新，原结论是否仍成立？
2. **Maglev 自身演进**: Maglev 是否已通过其他路径解决了同一问题？
3. **更优替代**: 当轮或历史研究是否发现了覆盖同一问题域的更好方案？
4. **时效性**: 超过 N 轮（建议 4 轮）仍为 open → 触发再评估（不是自动废弃）

### 操作规则

- AI 输出 review 建议（保留 / 建议 supersede / 建议优先级调整）
- **Superseded 标记必须由 Creator 确认**，AI 不可自动执行
- 确认后：更新 status + 填写 superseded_by + superseded_reason
- 被 supersede 的 insight **保留完整内容**（不删除），仅标记状态

## 不可变性原则

- 研究报告一经 commit 不可回溯修改（point-in-time 快照）
- Insight 的 source_report、title、created_at 字段创建后不可变
- 只有 status 和关联字段（proposed_spec、absorbed_at、superseded_*）可更新
