# Spec Consolidation Decision - 2026-03-15

## 背景

当前分支同时存在两组处于 `Active` 状态的相关 Spec：

- `specs/20_evolution/active/version_sync_tool/`
- `specs/20_evolution/active/maglev_distribution/`

二者都覆盖了 Maglev 的“版本维持 / 更新同步”问题，但边界并不平行：

- `version_sync_tool` 聚焦单一同步器
- `maglev_distribution` 已升维为完整分发体系，包含下游安装/更新与上游发版

这导致当前分支在“Spec 主线”“实现归属”“验收对象”三方面都存在歧义。

## 决议

### 1. 是否合并

结论：**需要合并**。

合并方式不是并列拼接，而是：

- 以 `maglev_distribution` 作为唯一主 `Active` Spec
- 将 `version_sync_tool` 视为其前置母体 / 演进来源
- 将 `version_sync_tool` 中仍然有效的同步约束吸收进 `maglev_distribution`

### 2. 合并后的主线

合并后建议采用以下口径：

- `maglev_distribution`：唯一有效主线 Spec
- `version_sync_tool`：历史演进 Spec，后续转归档或 `Superseded`

### 3. 演进关系说明

建议在 `maglev_distribution` 中补充一段显式 lineage 说明：

1. `version_sync_tool` 首先定义了零依赖同步器、四态同步、`sync_state.json`、冲突备份与变更播报。
2. 随着需求从“更新工具”扩展到“安装 + 更新 + 发版 + 多入口包装”，该能力被升维吸收到 `maglev_distribution`。
3. 原始 `maglev_sync.py` 属于过渡实现，最终目标由统一的 Distribution Engine 承载。

## 当前实现范围识别

### A. 主交付实现

这些产物应作为当前主验收对象保留：

- `dist/maglev_installer.py`
- `dist/install.sh`
- `scripts/maglev_release.py`
- `packages/maglev-cli/package.json`
- `packages/maglev-cli/bin/index.js`
- `issues/active/task_maglev_distribution.md`

### B. 过渡实现

这些产物不应再被视为最终主实现，但具有演进参考价值：

- `.maglev/maglev_sync.py`
- `specs/20_evolution/active/version_sync_tool/`

### C. 发行镜像 / 包内镜像

这些内容是交付物的一部分，但不应与“源码真身”混淆：

- `dist/manifest.json`
- `dist/CHANGELOG.md`
- `dist/CHANGELOG_DRAFT.md`
- `packages/maglev-cli/dist/`

## 合并后对现有开发内容的处置建议

### 1. 保留为正式交付

保留并持续维护：

- `dist/maglev_installer.py`
- `dist/install.sh`
- `scripts/maglev_release.py`
- `packages/maglev-cli/`
- `dist/` 下的正式发行资产

### 2. 吸收进入主 Spec 的能力点

应从 `version_sync_tool` 吸收进入 `maglev_distribution` 的内容：

- 零依赖执行
- 四态同步：`NEW / SKIP / OVERWRITE / CONFLICT`
- 本地状态基线：`sync_state.json`
- 冲突备份策略
- 幂等性
- 断网保护
- CHANGELOG 播报

### 3. 标记为 Legacy / Deprecated

应显式降级但暂不删除：

- `.maglev/maglev_sync.py`

建议处理：

- 文件头明确标记 `Deprecated`
- 在主 Spec 中写清“仅作过渡实现参考，不作为最终验收对象”

### 4. 归档旧 Spec

`version_sync_tool` 不建议直接删除，建议后续执行：

1. 从 `specs/20_evolution/active/version_sync_tool/` 迁出
2. 调整文档头部状态为 `Superseded` 或 `Archived`
3. 增加“已被 `maglev_distribution` 吸收”的说明

## 结构性风险判断

当前分支的真实风险不只是“功能是否完成”，而是“职责边界是否清晰”。

### 风险 1：同一能力存在双实现语义

同步相关能力同时存在于：

- `.maglev/maglev_sync.py`
- `dist/maglev_installer.py`

风险：

- 后续测试目标不清
- 维护时易发生行为漂移
- 容易把过渡实现误判为正式交付

### 风险 2：`dist/` 同时承担源码与发行物角色

当前 `dist/` 目录中存在：

- 实际运行入口：`maglev_installer.py`, `install.sh`
- 发行结果：`manifest.json`, `CHANGELOG.md`, `.agents/`, `.maglev/`

风险：

- 源文件与构建产物边界模糊
- review 时难以区分“手写源码”与“生成快照”
- 后续若重建发行流程，容易出现源产物倒置

### 风险 3：NPM 包依赖包内镜像

`packages/maglev-cli/bin/index.js` 直接依赖包内 `dist/` 中的离线资产。

风险：

- CLI 可用性依赖于包内镜像与主发行资产保持一致
- 若缺少统一校验，容易出现“npm 包内容”与“release 内容”不一致

## 当前建议的操作顺序

### Phase 1：先做决议收口

- 确认 `maglev_distribution` 为唯一主线
- 确认 `version_sync_tool` 转入历史演进位

### Phase 2：再做 Spec 和实现映射

- 建立“主 Spec -> 主代码 -> 发行物 -> 包装层”的一一映射
- 明确哪些是最终验收对象，哪些只是中间产物

### Phase 3：最后决定是否做目录重构

目录整理是后置动作，不建议与本轮 Spec 合并决议同时推进。

优先建议先把语义和归属收口，再决定是否把：

- `dist/maglev_installer.py`
- `dist/install.sh`

迁移到更清晰的源码目录。

## 供审核的结论摘要

以下结论建议作为本轮审核口径：

1. `version_sync_tool` 与 `maglev_distribution` 需要合并。
2. 合并后仅保留 `maglev_distribution` 为主 `Active` Spec。
3. `.maglev/maglev_sync.py` 应视为过渡实现，不再作为最终主验收对象。
4. `packages/maglev-cli` 是当前分支正式范围的一部分，不能遗漏。
5. 当前最大的风险是职责边界松散，而不是单点功能缺失。
