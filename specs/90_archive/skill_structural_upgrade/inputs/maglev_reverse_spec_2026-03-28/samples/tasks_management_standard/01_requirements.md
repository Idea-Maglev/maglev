# Requirements - Tasks 任务管理

## 1. Feature Summary
- 该模块用于承载任务规划记录的查询、展示、删除和状态同步。
- 后端围绕 `task_plan_record` 提供 CRUD 与查询接口，前端以列表页和任务卡片形式展示任务执行过程。
- 前端不仅依赖 REST API，也通过 WebSocket 订阅实时更新计划状态与子任务状态。

## 2. Evidence Summary
- [FACT] 后端提供 `create/update/delete/get/query` 五类任务规划记录接口。
- [FACT] 查询列表时服务层强制使用 `created_user = 当前用户` 作为过滤条件。
- [FACT] 前端 `useTaskState` 会把后端 `TaskPlanRecord` 转成 UI `Task`，并基于 `plan_status` 推导进度和状态。
- [FACT] 前端 `useTaskSocket` 订阅 `task_plan_{domainAccount}` 频道，实时更新任务状态和步骤状态。
- [INFERENCE] 任务页主要承担“执行过程可视化”和“失败后查看现场”的职责，而不是任务编辑器。
- [UNKNOWN] 删除接口是否真正限制为只删除 `created/executing` 状态，当前 service 代码中未见显式校验。

## 3. User Stories
- 作为用户，我希望查看所有任务记录，并能按进行中/已完成筛选。
- 作为用户，我希望看到每个任务步骤的实时执行状态和结果。
- 作为用户，我希望删除不再需要的任务记录。
- 作为维护者，我希望任务记录按用户隔离，避免跨用户看到彼此任务。

## 4. Acceptance Criteria
- AC-01: 任务查询必须只返回当前用户创建的任务。
- AC-02: 列表页能根据 `plan_status` 将任务映射为 `pending/running/done/cancelled/failed`。
- AC-03: WebSocket 推送到达后，前端任务列表中的步骤状态应同步刷新。
- AC-04: 删除成功后，对应任务应从前端全局状态移除。

## 5. Domain Model
- `TaskPlanRecord`: 任务规划记录主对象，承载计划蓝图、运行态、元数据和扩展信息。
- `TaskExecuteStatusItem`: 子任务运行态对象，记录步骤级执行状态、时间、错误与答案。
- `Task`: 前端展示对象，由 `TaskPlanRecord` 映射而来，补齐进度和 UI 状态。

## 6. Unknowns / Quests
- [Q-01] 删除时是否真的校验 `plan_status in {created, executing}`？
- [Q-02] `tasks` 在后端创建模型中允许 `dict | list`，但前端默认按数组处理，线上是否始终为数组？
- [Q-03] WebSocket 事件中的 `task_execute_status` 与 REST 查询返回的结构是否完全一致？
- [Q-04] `goal` 已在后端注释中标记“废弃”，但前端仍使用 `goal || global_schedule.goal`，是否存在迁移未收口？

## 7. Implementation Trace
- Router: `pcp-mpx/pcp_mpx/api/router/task_plan_record_api.py`
- Service: `pcp-mpx/pcp_mpx/service/task_plan_record_service.py`
- Model: `pcp-mpx/pcp_mpx/db/pgsql/models/task_plan_record.py`
- Request Models: `pcp-mpx/pcp_mpx/domain/req/task_plan_record_req.py`
- Response Models: `pcp-mpx/pcp_mpx/domain/resp/task_plan_record_resp.py`
- Frontend API: `mpx-web/src/api/task.ts`
- Frontend State: `mpx-web/src/composables/useTaskState.ts`
- Frontend Socket: `mpx-web/src/composables/useTaskSocket.ts`
- Frontend Types: `mpx-web/src/types/task.ts`
- View: `mpx-web/src/views/TasksView.vue`
