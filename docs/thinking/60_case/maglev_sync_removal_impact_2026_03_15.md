# `.maglev/maglev_sync.py` Removal Impact Assessment - 2026-03-15

## 结论

在“当前没有任何存量项目实际使用旧初始化/同步链路”的前提下：

- `.maglev/maglev_sync.py` **可以删除**
- 但建议与 Spec 合并/归档动作一起执行
- 删除前应同步处理文档引用，并确认是否接受少量行为差异

## 删除判断依据

### 1. 当前正式入口已不依赖 `maglev_sync.py`

当前正式分发链路为：

- `dist/install.sh`
- `dist/maglev_installer.py`
- `packages/maglev-cli/bin/index.js`
- `scripts/maglev_release.py`

未发现现行 workflow、CLI 入口或发布脚本仍以 `.maglev/maglev_sync.py` 作为必需依赖。

### 2. 当前仓库中对 `maglev_sync.py` 的引用主要是文档性声明

现有引用主要落在以下几类：

- 旧 Spec 将其定义为主入口
- 新 Spec 将其声明为 deprecated / blacklist
- issue / skill 文档说明其已废弃

这说明它当前承担的更多是“历史语义”而不是“运行时依赖”。

## 当前引用清单

### A. 删除时必须调整的引用

这些位置如果保留不改，会继续让人误以为 `maglev_sync.py` 是有效入口：

- `specs/20_evolution/active/version_sync_tool/01_requirements.md`
- `specs/20_evolution/active/version_sync_tool/02_design_backend.md`

### B. 删除时建议同步调整的引用

这些位置虽然不是运行依赖，但会留下“文件存在但已废弃”的描述痕迹：

- `issues/active/task_maglev_distribution.md`
- `issues/closed/draft_issue_maglev_distribution.md`
- `specs/20_evolution/active/maglev_distribution/01_requirements.md`
- `specs/20_evolution/active/maglev_distribution/02_design_backend.md`
- `.agents/skills/maglev-changelog-generator/SKILL.md`

### C. 可保留为历史决议引用

以下文档可以保留对该文件的历史性描述：

- `docs/thinking/spec_consolidation_2026_03_15.md`

## 能力承接对照

### 已被 `dist/maglev_installer.py` 承接的能力

这些能力已经存在于统一 Installer 中：

- 零依赖 Python 单文件执行
- 读取 `manifest.json`
- 基于 `sync_state.json` 的幂等更新
- 四态同步：`NEW / SKIP / OVERWRITE / CONFLICT`
- 冲突备份：`.local_backup_<timestamp>`
- `--dry-run`
- `--force`
- 本地离线安装 `--local-dist`

### 尚未完全等价承接或需要重新确认的能力

这些能力在旧脚本中更明确，但在当前 Installer 中未见明确等价实现，或行为表达不完全一致：

1. **更新后打印远端 CHANGELOG 摘要**
   - 旧脚本：会在同步结束后拉取并打印 `CHANGELOG.md`
   - 新 Installer：当前 `do_update()` 中未见等价调用

2. **3 秒超时承诺**
   - 旧 Spec：要求 3 秒内优雅超时
   - 新 Installer：`urlopen(..., timeout=10)`

3. **版本烙印 `_maglev_engine_version`**
   - 旧 Spec 中明确提出
   - 新 Installer 未实现

4. **配置增量合并**
   - 旧 Spec 中提出 `.maglev/` 配置尽量做 KV merge
   - 新 Installer 当前仍以文件级同步为主

## 删除 `maglev_sync.py` 后的语义变化

### 可接受变化

在无历史用户的前提下，以下变化通常可以接受：

- 不再保留“独立同步器”入口
- 用户统一通过 Installer / Shell / Npx 入口执行更新
- 仓库不再维护双实现

### 需要显式接受的变化

如果直接删除旧脚本而不补行为，需要明确接受以下事实：

1. 当前主实现未必完全覆盖旧 Spec 的所有细节承诺
2. `version_sync_tool` 应被视为被吸收而非“完整逐条兑现”
3. 未来测试与验收应只针对主分发链路，不再对旧同步器做独立验收

## 删除建议顺序

### Step 1：先合并 Spec 语义

- 确认 `maglev_distribution` 为唯一主线
- 将 `version_sync_tool` 转为历史演进或归档

### Step 2：再删除代码文件

- 删除 `.maglev/maglev_sync.py`

### Step 3：同步改文档

最少需要同步修改：

- 将 `version_sync_tool` 中对 `maglev_sync.py` 的入口定义改为“已被统一 Installer 吸收”
- 将 `maglev_distribution` 中关于 `maglev_sync.py` 的描述从“Deprecated 文件”调整为“历史实现，已移除”

### Step 4：决定是否补行为缺口

建议单独判断以下是否要补到 `dist/maglev_installer.py`：

- 更新后打印远端 CHANGELOG 摘要
- 其他仍被主 Spec 承诺但未完全落地的行为

## 建议结论

建议采用以下执行口径：

1. `.maglev/maglev_sync.py` 不再保留。
2. 删除动作与 Spec 合并/归档在同一批次完成。
3. 删除前不必考虑向后兼容或降级策略。
4. 删除后只保留统一 Distribution Engine 作为更新同步的正式实现。
