# Requirements - Memory 记忆中心

## 1. Feature Summary
- 该模块用于管理用户的长期记忆，支持创建、更新、删除、按条件查询和语义检索。
- 用户侧目标是让系统跨会话保留历史知识，并在需要时通过筛选或语义搜索找回相关内容。
- 当前前端实现聚焦“列表查看、前端关键字过滤、语义搜索、删除”，未看到创建/更新 UI 入口。

## 2. Evidence Summary
- [FACT] 后端暴露了 `POST/PUT/DELETE/GET/query/search` 六类长期记忆接口。
- [FACT] 记忆文档至少包含 `id/text/user_id/memory_type/time_scope/date_key/created_at` 七个核心字段。
- [FACT] 语义检索在服务层强制注入 `user_id` 过滤。
- [FACT] 前端 `useMemories` 通过 `queryMemories / searchMemories / deleteMemory` 三个 API 封装操作记忆列表。
- [INFERENCE] 该模块主要被设计为用户长期偏好、总结类信息的持久化容器，而不是通用知识库。
- [UNKNOWN] 语义检索返回值的真实响应结构与前端类型定义是否完全一致。

## 3. User Stories
- 作为用户，我希望系统保存我的阶段性总结和偏好，以便后续对话复用。
- 作为用户，我希望通过时间筛选或语义描述快速找回相关记忆。
- 作为用户，我希望删除某条不再需要的记忆，并立即从当前列表中消失。

## 4. Acceptance Criteria
- AC-01: 用户可以按 `memory_type` 和日期范围查询自己的记忆列表。
- AC-02: 语义检索必须带 `user_id` 过滤，避免跨用户命中。
- AC-03: 删除操作成功后，前端列表应移除对应项。
- AC-04: 更新操作保留未修改字段，并以“删除旧文档 + 写入新文档”的方式同步向量存储。

## 5. Domain Model
- `LongTermMemory`: 长期记忆主对象，承载文本内容与时间/类型元数据。
- `MemoryType`: 当前前端定义的摘要型分类，包含 `daily_summary / weekly_summary / monthly_summary`。
- `Semantic Search Result`: 在主对象基础上附带相似度分数 `score` 的检索结果。

## 6. Unknowns / Quests
- [Q-01] 前端 `QueryMemoriesParams` 使用 `limit`，而后端请求模型使用 `page_number/page_size`，当前线上是否有兼容层？
- [Q-02] 前端 `SearchMemoriesParams` 和 `QueryMemoriesParams` 都声明 `user_id`，但实际调用未传，是否只是过时类型？
- [Q-03] 前端将语义检索结果当作二维数组读取 `response.data[0]`，而后端路由当前返回 `LongTermMemoryListResp(items=items)`，两端哪个才是线上真实契约？
- [Q-04] 服务层没有显式 `score_threshold` 过滤逻辑，现有产品预期是否已变化？

## 7. Implementation Trace
- Router: `pcp-mpx/pcp_mpx/api/router/long_term_memory_api.py`
- Service: `pcp-mpx/pcp_mpx/service/long_term_memory_service.py`
- Request Models: `pcp-mpx/pcp_mpx/domain/req/long_term_memory_req.py`
- Response Models: `pcp-mpx/pcp_mpx/domain/resp/long_term_memory_resp.py`
- Frontend API: `mpx-web/src/api/memory.ts`
- Frontend State: `mpx-web/src/composables/useMemories.ts`
- Frontend Types: `mpx-web/src/types/memory.ts`
