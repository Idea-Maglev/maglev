# Spec Merge Execution Plan - 2026-03-15

## 目标

将当前“版本同步工具”与“分发与安装机制”两条语义主线收敛为一条明确主线，避免：

- 双 `Active` Spec 并存
- 双实现语义并存
- 测试与验收对象不清

本次执行目标：

1. 保留 `maglev_distribution` 为唯一主 `Active` Spec
2. 将 `version_sync_tool` 转为被吸收/归档对象
3. 删除 `.maglev/maglev_sync.py`
4. 统一当前分支的正式实现口径

## 执行原则

- 先收口语义，再删代码
- 先改 Spec，再改 issue/task，再删旧文件
- 不在本轮同时做大规模目录重构
- 不处理历史兼容或降级策略

## 建议执行顺序

### Phase 1: 收口主 Spec

#### 1. 修改 `maglev_distribution` 的主文档

目标文件：

- `specs/20_evolution/active/maglev_distribution/00_vision.md`
- `specs/20_evolution/active/maglev_distribution/01_requirements.md`
- `specs/20_evolution/active/maglev_distribution/02_design_backend.md`

建议修改：

1. 增加一段 lineage / evolution 说明
   - 明确 `version_sync_tool` 是该体系的前置母体
   - 明确四态同步、安全更新、`sync_state.json` 等能力已被吸收

2. 将所有“`maglev_sync.py` 已废弃”措辞升级为：
   - “历史实现，已移除”
   - 避免继续暗示仓库中仍应保留该文件

3. 在 requirements/design 中补一段统一口径：
   - 当前唯一正式下游执行实现为 `maglev_installer.py`
   - Shell 与 Npx 入口均以其为唯一核心执行源

#### 2. 确认 `packages/maglev-cli` 被纳入主 Spec

目标文件：

- `specs/20_evolution/active/maglev_distribution/01_requirements.md`
- `specs/20_evolution/active/maglev_distribution/02_design_backend.md`

建议修改：

- 补充一句明确表述：`packages/maglev-cli/` 为正式分发入口包装层
- 说明其依赖包内镜像资产执行离线安装

### Phase 2: 归档旧 Spec

#### 3. 处理 `version_sync_tool` 目录

当前目录：

- `specs/20_evolution/active/version_sync_tool/`

建议动作二选一：

方案 A，推荐：
- 整体迁移到归档目录
- 例如：`specs/90_archive/version_sync_tool/`

方案 B，过渡态：
- 暂留原路径
- 但将文档头部状态从 `Active` 改为 `Superseded`
- 首段增加“已被 `maglev_distribution` 吸收”的说明

本轮更推荐方案 B，如果你希望最小扰动；如果你希望一次收干净，则用方案 A。

#### 4. 修改旧 Spec 的文档头和首段

目标文件：

- `specs/20_evolution/active/version_sync_tool/00_vision.md`
- `specs/20_evolution/active/version_sync_tool/01_requirements.md`
- `specs/20_evolution/active/version_sync_tool/02_design_backend.md`

建议修改：

1. `status: "Active"` 改为 `status: "Superseded"`
2. 增加说明：
   - 本组 Spec 已被 `maglev_distribution` 吸收
   - 仅保留为演进记录
3. 将“入口是 `python .maglev/maglev_sync.py`”改为历史表述，而不是现行要求

### Phase 3: 清理旧实现

#### 5. 删除 `.maglev/maglev_sync.py`

目标文件：

- `.maglev/maglev_sync.py`

动作：

- 直接删除

前置确认：

- 当前无存量项目依赖
- 当前正式入口不引用该文件

#### 6. 清理与旧实现绑定的描述

目标文件：

- `issues/active/task_maglev_distribution.md`
- `issues/closed/draft_issue_maglev_distribution.md`
- `.agents/skills/maglev-changelog-generator/SKILL.md`

建议修改：

- 将“Deprecated 文件”改成“历史实现已移除”
- 删除任何会暗示该文件仍然存在的措辞

### Phase 4: 建立正式实现口径

#### 7. 建立统一实现映射

建议在主 Spec 或附属决议文档中显式写出：

- 核心执行器：`dist/maglev_installer.py`
- Shell 入口：`dist/install.sh`
- Npx 入口：`packages/maglev-cli/bin/index.js`
- 发版编译器：`scripts/maglev_release.py`
- 包内镜像：`packages/maglev-cli/dist/`

#### 8. 标记当前未闭环差异

不要求本轮立即实现，但应写入后续 gap：

- `maglev_installer.py` 尚未显式打印远端 CHANGELOG 摘要
- `dist/` 同时扮演源码与发行物角色，后续需要进一步整理

## 文件级修改清单

### 必改

- `specs/20_evolution/active/maglev_distribution/00_vision.md`
- `specs/20_evolution/active/maglev_distribution/01_requirements.md`
- `specs/20_evolution/active/maglev_distribution/02_design_backend.md`
- `specs/20_evolution/active/version_sync_tool/00_vision.md`
- `specs/20_evolution/active/version_sync_tool/01_requirements.md`
- `specs/20_evolution/active/version_sync_tool/02_design_backend.md`
- `issues/active/task_maglev_distribution.md`
- `issues/closed/draft_issue_maglev_distribution.md`
- `.agents/skills/maglev-changelog-generator/SKILL.md`

### 必删

- `.maglev/maglev_sync.py`

### 本轮可不动

- `dist/maglev_installer.py`
- `dist/install.sh`
- `scripts/maglev_release.py`
- `packages/maglev-cli/`

说明：

这些实现文件本轮重点是“确认其主实现身份”，而不是立刻重构目录。

## 审核检查点

执行完成后，需要确认以下结果：

1. 仓库中不再存在双 `Active` 主线
2. 仓库中不再存在 `.maglev/maglev_sync.py`
3. 所有主 Spec 不再把 `maglev_sync.py` 当作现行入口
4. `packages/maglev-cli` 被明确纳入正式范围
5. 当前正式实现链路表述一致

## 建议的本轮收尾状态

如果以上动作完成，可将当前分支状态定义为：

- 已完成 Spec 主线收口
- 已移除过渡实现
- 已建立统一验收口径
- 目录重构与行为补齐留作下一阶段任务
