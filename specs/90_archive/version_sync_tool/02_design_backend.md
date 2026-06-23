---
title: "Version Sync Tool - Technical Design"
status: "Superseded"
---

# 02 Design: 版本同步核心引擎 (Ready-to-Code)

> 本组 Spec 已被 `specs/20_evolution/active/maglev_distribution/` 吸收，现仅保留为历史设计记录。

## 1. 物理架构与部署模型

历史方案中，工具核心被封装为一个零第三方依赖的 Python 脚本，以支撑最大程度的用户侧兼容性。

### 1.1 目录拓扑结构 (Directory Topology)
被同步的用户工程 (Local Workspace) 结构要求如下：
```text
[Local Project Root]
  ├── .maglev/
  │    ├── sync_state.json   (本地持久化的同步历史状态机，核心基准)
  │    ├── maglev_sync.py    (历史方案中的工具位置，当前已移除)
  ├── .agents/
  │    ├── skills/           (主要被管理的资产)
  │    ├── workflows/        (主要被管理的资产)
  ├── ...
```

### 1.2 远端宿主约定 (Upstream Contract)
历史方案中的 `maglev_sync.py` 执行工作的第一步是去寻找一个**绝对可靠**的只读源（Upstream）。官方在发布 Release 时必须提供如下可被直接 GET 获取的静态资源：
- `https://[upstream-url]/latest/manifest.json` : 记录清单与校验和
- `https://[upstream-url]/latest/CHANGELOG.md` : 用于展示
- `https://[upstream-url]/latest/assets/...` : 原生的技能与规则文件夹结构（包含被管控的文件原文）

## 2. 数据模型字典 (Data Models)

### 2.1 上游清单元数据 (`manifest.json`)
由官方发版流水线自动生成的准入基线。
```json
{
  "version": "v2.2.0",
  "publish_date": "2026-03-01T12:00:00Z",
  "files": [
    {
      "path": ".agents/skills/maglev-create-spec/SKILL.md",
      "sha256": "4b971x6...a7d9"
    },
    {
      "path": ".maglev/protocols/collaboration.md",
      "sha256": "8a32d...1x89"
    }
  ]
}
```

### 2.2 本地状态机记录 (`.maglev/sync_state.json`)
由历史方案中的 `maglev_sync.py` 执行完毕后覆写生成的基准档案。
```json
{
  "last_synced_version": "v2.1.2",
  "last_synced_time": "2026-02-15T08:00:00Z",
  "file_baselines": {
    ".agents/skills/maglev-create-spec/SKILL.md": "old_hash_from_v2.1.2",
    ".maglev/protocols/collaboration.md": "old_hash_from_v2.1.2"
  }
}
```

## 3. 核心算法流程 (Core Algorithm: The Synchronization State Machine)

同步器运转时的核心计算过程在 `def sync_engine()` 中被严密保护。

### Phase 1: Context Loading & Verification
1. **获取参数**: 若用户传入 `--dry-run` 则不执行任何物理写入操作。
2. **下载远端 Manifest**: 尝试 HTTP 获取，如果 HTTP 状态码不是 200 或连接超时，直接终止并报错 `[Errno 1] Upstream Unreachable`。判断此 Manifest 的 `version` 是否等于本地 `sync_state.json` 中的 `last_synced_version`。如果是，且用户未加 `--force` 标志，判定任务具有**幂等性**，直接 `exit(0)`。
3. **加载本地基线**: 读取内存字典 `local_state_map = list_hashes_from_state_file()`。

### Phase 2: Diff Engine Computations
针对 `manifest.json` 发放的每一个文件节点 `{ file_path, remote_hash }`:
```python
def process_file_node(file_path, remote_hash):
    # 状态A：本文件是上游全新的
    if file_path not in local_state_map:
        download_to(file_path)
        return "ADDED"

    remote_baseline_hash = local_state_map[file_path]
    
    # 状态B：上游文件根本没变过 (远端的 Hash == 这次要推的 Hash)
    # 跳过，不消耗带宽
    if remote_hash == remote_baseline_hash:
        return "SKIPPED"

    # 如果走到了这里说明: 上游文件有更新。需要检查本地是否已被魔改。
    current_local_hash = compute_sha256(file_path)
    
    # 状态C: 官方有更新，但本地安然无恙
    if current_local_hash == remote_baseline_hash:
        download_to(file_path, overwrite=True)
        return "UPDATED_SILENTLY"
    
    # 状态D: 官方有更新，且本地Hash被破坏！这是真正的“魔改者”
    if current_local_hash != remote_baseline_hash:
        backup_path = file_path + f".local_backup_{timestamp}.md"
        rename(file_path, backup_path)
        download_to(file_path)
        return ("CONFLICT_BACKUP", backup_path)
```

### Phase 3: Committing State
- 当所有下载动作与备份动作处理完后，在**内存中**组装完成一份全新的 `sync_state.json`，包含了这一次全部文件的准确 `sha256`。
- 将这个新对象写入磁盘，完成持久态跃迁。

### Phase 4: Output Rendering
- 在控制台高亮色彩打印刚刚所有的 `ADDED`, `UPDATED_SILENTLY`, `CONFLICT_BACKUP`。
- 拉取 `https://[upstream-url]/latest/CHANGELOG.md`，截取最近一个版本段落输出。
- 如发现了至少 1 个 `CONFLICT_BACKUP` 记录，控制台用红/黄警告输出：“⚠️ 检测到您的本地资产被覆盖，被魔改的版本我们已留存，请自行排查解决不兼容的内容。”

## 4. API & Module Boundaries

由于基于 Python 单文件执行，我们将功能紧密闭环，只提供以下几个内聚的方法契约：
1. `class RemoteClient`: 负责纯粹的 `urllib.request` 与重试包围。
2. `class FileHasher`: 负责传入文件路径流读取其 SHA256，防御大文件内存溢出。
3. `class UpstreamManifestParser`: 解析并且验证从远端拿回的 json 是否合法（缺字段报错）。
4. `class SyncCoordinator`: 编排核心算法的主节点，串换所有的步骤。
