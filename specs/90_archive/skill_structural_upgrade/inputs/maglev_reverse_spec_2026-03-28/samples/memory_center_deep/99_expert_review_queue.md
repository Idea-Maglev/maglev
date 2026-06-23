# Expert Review Queue - Memory 记忆中心

## Architectural Intent
- [Q-01] 长期记忆是否有独立的关系型元数据存储，还是完全依赖向量库文档？
- [Q-02] 前端当前是否只是管理界面，而创建/更新主要由后台 Agent 或 Job 触发？

## Data Semantics
- [Q-03] `memory_type` 是否只有 `daily/weekly/monthly_summary` 三类，还是开放字符串？
- [Q-04] `date_key_number` 是否由向量服务自动派生？
- [Q-05] 搜索结果中的 `score` 是否在所有环境都可用？

## Security & Isolation
- [Q-06] `update/delete/get_by_id` 是否有隐藏的用户隔离保护？
- [Q-07] 如果用户拿到其他文档 ID，当前删除/更新是否会被拒绝？

## Runtime & Risk
- [Q-08] 更新链路删除成功、写入失败时，是否存在补偿机制？
- [Q-09] 是否有重试、告警、审计日志或人工修复入口？
- [Q-10] 前后端契约漂移是历史遗留，还是当前代码仅为离线/未启用实现？
