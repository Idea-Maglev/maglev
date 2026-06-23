# Requirements - Memory 记忆中心

## 1. Feature Summary
- 该模块用于存储、检索和维护用户的长期记忆文本，为后续对话提供历史上下文。
- 核心能力分为两类：显式条件查询和基于向量的语义检索。
- 模块当前更接近“面向总结类文本的记忆仓”，不是通用知识图谱或结构化记忆引擎。

## 2. Evidence Summary
- [FACT] 后端路由层提供创建、更新、删除、单条查询、条件列表查询和语义检索六类接口。
- [FACT] 服务层直接面向 `tencent_vector_db_service` 操作文档，不存在独立的关系型元数据持久层代码迹象。
- [FACT] 创建时服务层组装的主文档字段为 `id/text/user_id/memory_type/time_scope/date_key/created_at`。
- [FACT] 条件查询和语义检索都会强制拼入 `user_id` 作为过滤条件。
- [FACT] 更新逻辑通过“按 ID 查旧文档 -> 删除旧文档 -> 写入新文档”实现。
- [INFERENCE] 当前系统把向量库文档本身同时当作“主存储 + 检索索引”，而不是只把向量库存成副本。
- [UNKNOWN] 向量服务是否在内部自动补齐 `date_key_number`、`score` 等派生字段。

## 3. User Stories
- 作为用户，我希望系统记住我的日/周/月总结，以便新的会话可以复用历史背景。
- 作为用户，我希望通过自然语言搜索找到相关记忆，而不需要记住精确标题。
- 作为用户，我希望删除无用记忆后，前端界面能立即反映删除结果。
- 作为维护者，我希望查询和检索始终带租户边界，避免用户之间的记忆串扰。

## 4. Acceptance Criteria
- AC-01: 所有查询与检索请求都必须以当前用户 `user_id` 为强制过滤条件。
- AC-02: 列表查询支持 `memory_type` 和日期范围过滤，并按 `date_key_number desc` 排序。
- AC-03: 语义搜索应返回可用于排序或阈值过滤的相似度信息。
- AC-04: 更新后，新文档内容应替代旧文档，并对后续查询/检索立即可见。
- AC-05: 当前前端态在删除成功后必须同步移除被删项。

## 5. Domain Model
- `LongTermMemory`: 面向用户的长期文本记忆对象。
- `MemoryType`: 记忆的业务分类，目前呈现为摘要型枚举。
- `Vector Document`: 存入向量服务的实际承载结构，兼具文本、元数据和检索入口。
- `Semantic Search Result`: 向量服务返回的匹配项，理论上应附带相似度。

## 6. Security Expectations
- 任何列表查询和语义检索都不应允许调用方自行指定 `user_id` 覆盖当前上下文。
- 删除和更新至少应保证只能操作属于当前用户的文档。
- 前端不应通过传参方式持有租户边界，而应依赖后端上下文注入。

## 7. Unknowns / Quests
- [Q-01] `update/delete/get_by_id` 当前没有显式传入 `user_id`，实际是否由向量服务层做了额外隔离？
- [Q-02] 前端 `queryMemories`/`searchMemories` 的类型定义与后端请求模型不一致，线上兼容层在哪里？
- [Q-03] 语义检索返回结构究竟是二维数组、平铺数组还是 `items` 包装对象？
- [Q-04] 向量服务的删除和写入是否具备事务性或幂等性保护？
- [Q-05] 如果向量写入失败，当前是否存在补偿、重试或死信处理？

## 8. Implementation Trace
- Router: `pcp-mpx/pcp_mpx/api/router/long_term_memory_api.py`
- Service: `pcp-mpx/pcp_mpx/service/long_term_memory_service.py`
- Request Models: `pcp-mpx/pcp_mpx/domain/req/long_term_memory_req.py`
- Response Models: `pcp-mpx/pcp_mpx/domain/resp/long_term_memory_resp.py`
- Frontend API: `mpx-web/src/api/memory.ts`
- Frontend State: `mpx-web/src/composables/useMemories.ts`
- Frontend Types: `mpx-web/src/types/memory.ts`
