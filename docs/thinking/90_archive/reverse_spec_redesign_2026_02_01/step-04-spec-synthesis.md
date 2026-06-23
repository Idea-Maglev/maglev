---
description: maglev-reverse-spec Step 4 - Spec Synthesis (v2.1 with Chunking)
---

# Step 4: Spec Synthesis (规格合成) v2.1

## 目标
将 Step 1-3 收集的上下文信息，合成为符合 Maglev 标准的 Spec 文件簇。
支持**智能分片 (Smart Chunking)**：当内容超过阈值时，自动拆分为子文件。

## 输出结构

### 基础结构 (Always Generated)
```
specs/10_reality/reverse_{feature_slug}/
├── 00_index.md          <- 元数据 + 关联 + 限制声明
├── 01_requirements.md   <- 业务需求
└── 02_design.md         <- 技术设计
```

### 扩展结构 (Threshold-Triggered)
```
specs/10_reality/reverse_{feature_slug}/
├── 00_index.md
├── 01_requirements.md            <- 需求摘要
├── 01_req_core.md                <- [可选] 核心 User Stories
├── 01_req_edge.md                <- [可选] 边缘场景
├── 02_design.md                  <- 设计摘要
├── 02_api.md                     <- [可选] API 契约详情
├── 02_schema.md                  <- [可选] 数据模型详情
├── 02_frontend.md                <- [可选] 前端设计详情
└── 02_flow.md                    <- [可选] 业务流程/状态机
```

---

## 分片规则 (Chunking Rules)

| 内容类型 | 阈值 | 动作 |
|----------|------|------|
| User Stories | > 5 | 拆分 `01_req_core.md`, `01_req_edge.md` |
| API Endpoints | > 3 | 拆分 `02_api.md` |
| Entities/Tables | > 3 | 拆分 `02_schema.md` |
| 前端组件 | > 3 | 拆分 `02_frontend.md` |
| 状态机/复杂流程 | 存在 | 拆分 `02_flow.md` |

**原则**: 默认只生成基础 3 文件。只有触发阈值时才拆分。

---

## 00_index.md 模板

```yaml
---
title: "{Feature Name} (逆向)"
slug: reverse_{feature_slug}
status: draft
reverse_spec_version: 1
source: reverse-engineering
created_at: {timestamp}
source_commit: {git_hash}  # 可选
---

# {Feature Name}

> 本文档由 `maglev-reverse-spec` v2.1 自动生成。

## 源文件 (Analyzed Sources)
### Frontend
- `{frontend_file_1}`
- `{frontend_file_2}`

### Backend
- `{controller_file}`
- `{service_file}`

### Entities
- `{entity_file_1}`
- `{entity_file_2}`

## Known Limitations
> **重要**: 以下内容未被本次逆向捕获，可能需要人工补充。

- [ ] 未捕获: {limitation_1}
- [ ] 未捕获: {limitation_2}
- [ ] 不确定: {uncertainty_1}

## Spec Cluster
- [01_requirements.md](./01_requirements.md)
- [02_design.md](./02_design.md)
```

---

## 01_requirements.md 模板

```markdown
---
title: "{Feature Name} - 需求规格"
status: draft
---

# 业务需求 (Reverse Engineered)

## 概述
{Feature 的一句话描述}

## User Stories

### US-R001: {Story Title}
**As a** {角色}
**I want to** {行为}
**So that** {价值}

**Acceptance Criteria**:
- [ ] {AC_1}
- [ ] {AC_2}
```

---

## 02_design.md 模板

```markdown
---
title: "{Feature Name} - 技术设计"
status: draft
---

# 技术设计 (Reverse Engineered)

## 架构概述
{一句话描述技术架构}

## 子文档 (如有拆分)
- [API 契约](./02_api.md)
- [数据模型](./02_schema.md)
- [前端设计](./02_frontend.md)

## API 摘要
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/{resource} | 列表 |
| POST | /api/{resource} | 创建 |

## 数据模型摘要
| Entity | Fields (Key) |
|--------|--------------|
| {Entity1} | id, name, ... |
```

---

## 02_frontend.md 模板 (可选)

```markdown
---
title: "{Feature Name} - 前端设计"
status: draft
---

# 前端设计

## 技术栈
- Framework: {Vue/React/Angular}
- State: {Vuex/Pinia/Redux}

## 组件树
```
{PageComponent}
├── {ChildComponent1}
├── {ChildComponent2}
└── {ChildComponent3}
```

## API 调用 (引用)
> 详细契约见 [02_api.md](./02_api.md)

| Action | API Reference |
|--------|---------------|
| 加载列表 | `GET /api/{resource}` |
| 删除项目 | `DELETE /api/{resource}/{id}` |
```

---

## Checkpoint 输出模板

```
[CHECKPOINT - Step 4 Complete]

Spec 草稿已生成。

📊 内容统计:
- User Stories: {N} 个
- API Endpoints: {N} 个
- Entities: {N} 个
- Components: {N} 个

📁 文件计划:
- 00_index.md ✓
- 01_requirements.md ✓
- 02_design.md ✓
{如有拆分:}
- 02_api.md ✓ (触发: API > 3)
- 02_schema.md ✓ (触发: Entity > 3)

⚠️ Known Limitations:
- {limitation_1}
- {limitation_2}

请审阅上述内容。输入 'confirm' 写入文件，或 'edit' 进行修改。
```
