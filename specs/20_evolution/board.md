# 项目看板

> 最后更新: 2026-06-19T00:00:00+08:00 | 活跃需求: 1 | 未启动: 2

## 图例

| 符号 | 含义 |
|------|------|
| ✅ | 阶段已完成 |
| ⏳ | 阶段进行中 |
| ⬜ | 阶段未开始 |

**流程阶段**: 需求收敛 → 方案设计 → 编码实施 → 综合验证 → 结晶归档

## 看板视图

```mermaid
graph LR
    classDef active fill:#4CAF50,color:#fff,stroke:#333
    classDef waiting fill:#f5f5f5,color:#999,stroke:#ddd

    subgraph S1[需求收敛]
        empty1[" "]:::waiting
    end
    subgraph S2[方案设计]
        empty2[" "]:::waiting
    end
    subgraph S3[编码实施]
        runtime_env["runtime-environment-check"]:::active
    end
    subgraph S4[综合验证]
        empty4[" "]:::waiting
    end
    subgraph S5[结晶归档]
        empty5[" "]:::waiting
    end

    S1 --> S2 --> S3 --> S4 --> S5
```

## 活跃需求

| 需求 | 意图 | 进度 | 导航 |
|------|------|------|------|
| runtime-environment-check | 补齐 Maglev 受控 Python 运行时、preflight 与环境错误分类 | ✅→✅→⏳→⬜→⬜ | [详情](./active/runtime-environment-check/INDEX.md) |

## 未启动需求

| 需求 | 意图 | 进度 | 导航 |
|------|------|------|------|
| task_public_distribution_channel | 打通公开发行制品与 OSS 分发通道 | ⏳→⬜→⬜→⬜→⬜ | [详情](../../issues/active/task_public_distribution_channel.md) |
| task_requirement_convergence_execution_stability | requirement-convergence 执行层稳定性 | ⏳→⬜→⬜→⬜→⬜ | [详情](../../issues/active/task_requirement_convergence_execution_stability.md) |

## 本次变更摘要

- **runtime-environment-check**: 新增 → **编码实施** → 正在补齐受控 Python 运行时与环境检查机制
  - 需求来源：`maglev-3de` 冷启动实践反馈暴露系统 Python 3.9、PyYAML、uv PATH 与 `track failed` 误导问题
  - 实施落地：`scripts/maglev-python` + `index-librarian/protocol/requirements.txt` + `reality-sync` preflight 规则
  - 验证：runtime doctor、skills/specs track verify、catalog check、installer py_compile 与裸 python 回归检查均通过


- **superpowers_integration**: 方案设计 → **结晶归档** → 已移入 `specs/90_archive/superpowers_integration/` (#24)
  - Reality 回写：`01_requirements.md` §2.3（代码执行委托 superpowers-bridge + context-implementer 退出代码执行）
  - 实施落地：superpowers-bridge skill + 优先级协议 + positioning 更新
  - 验证：v0.5.0 发版承载

- **version_json_flag**: 编码实施 → **结晶归档** → 已移入 `specs/90_archive/version_json_flag/` (#25)
  - Reality 回写：`distribution_runtime.md` §2.2（CLI version --json 子命令）
  - 实施落地：bin/index.js + tests/version-json.test.js
  - 验证：v0.5.0 发版承载

- **evolution_observatory**: 编码实施 → **结晶归档** → 已移入 `specs/90_archive/evolution_observatory/` (#26)
  - Reality 回写：`01_requirements.md` §2.8（持续进化观测 skill）
  - 实施落地：skill 骨架 + references + competitive_registry.yaml + catalog 注册
  - 验证：v0.5.0 发版承载

- **unified_doc_tree_indexer**: 方案设计 → **结晶归档** → 已移入 `specs/90_archive/unified_doc_tree_indexer/` (#27)
  - Reality 回写：`01_requirements.md` §2.4（index-librarian 统一 dir-tree 描述）
  - 实施落地：track_scan/track_verify 统一 dir-tree + common/index_gen.py + registry 清洗
  - 验证：`track_verify --track-id specs` ok + `track_verify --track-id docs` ok
