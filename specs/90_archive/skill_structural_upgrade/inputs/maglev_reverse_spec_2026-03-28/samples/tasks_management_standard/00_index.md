# Index: Tasks 任务管理 (Standard Reverse Sample)

## 元数据
- Feature: Tasks 任务管理
- Status: Structural
- Entry Type: API-First + UI-First + Event-First
- Confidence: Medium
- Scope:
  - `pcp-mpx/pcp_mpx/api/router/task_plan_record_api.py`
  - `pcp-mpx/pcp_mpx/service/task_plan_record_service.py`
  - `pcp-mpx/pcp_mpx/domain/req/task_plan_record_req.py`
  - `pcp-mpx/pcp_mpx/domain/resp/task_plan_record_resp.py`
  - `pcp-mpx/pcp_mpx/db/pgsql/models/task_plan_record.py`
  - `mpx-web/src/api/task.ts`
  - `mpx-web/src/composables/useTaskState.ts`
  - `mpx-web/src/composables/useTaskSocket.ts`
  - `mpx-web/src/types/task.ts`
  - `mpx-web/src/views/TasksView.vue`

## 输出档位
- Profile: `Standard`
- Included Layers:
  - Core Layer
  - Recommended Layer
- Excluded Layers:
  - Runtime 深化分析
  - Security Surface
  - Configuration Matrix
  - RMM Scorecard
  - Expert Review Queue

## 关联文档
- [Requirements](./01_requirements.md)
- [Design](./02_design.md)
