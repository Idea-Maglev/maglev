---
name: index-librarian-workflow
description: 索引管家工作流 — 按 track 扫描并验证机器索引
---

# Index Librarian Workflow

## 步骤链

```mermaid
flowchart LR
    A[选择已启用 track] --> B[scan]
    B --> C[verify]
    C -->|通过| F[报告]
    C -->|不通过| G[修正内容或生成器后重新 scan]
    G --> C
```

## 路由规则

| 用户意图 | 命令 | 后续动作 |
|:---|:---|:---|
| 检查全部索引 / 索引状态 | `track_scan.py --all` | `track_verify.py --all` |
| 扫描一个 track | `track_scan.py --track-id <id>` | 按需运行同一 track 的 verify |
| 验证一个 track | `track_verify.py --track-id <id>` | 不通过时先重新 scan，再定位根因 |
所有命令的路径基准如下：

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"
```

`--all` 只处理 registry 中 `enabled` 未设置或为 `true` 的有效 track。`enabled: false` 的 track 不参与批量运行，也不能作为单 track 目标解析。

## 报告

每个 track 以一行状态报告：

```text
{track-id}: {status} ({summary})
```

状态必须使用 `ok`、`partial`、`skipped`、`env_failed` 或 `failed`。不要以目录列表替代 scan / verify 输出。
