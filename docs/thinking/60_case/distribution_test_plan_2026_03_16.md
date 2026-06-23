# Distribution Test Plan - 2026-03-16

## 1. 测试目标

本轮测试用于对当前分支上的 `maglev_distribution` 主线进行收尾验收。

测试目标分为四类：

1. 验证下游分发链路可用
2. 验证上游发行链路可用
3. 验证 Npx 包装层与包内镜像一致
4. 验证主 Spec、实现对象与任务记录一致

本轮测试**不再**以 `version_sync_tool` 或 `.maglev/maglev_sync.py` 为主验收对象。

## 2. 测试范围

### 纳入范围

- `specs/20_evolution/active/maglev_distribution/`
- `dist/maglev_installer.py`
- `dist/install.sh`
- `scripts/maglev_release.py`
- `packages/maglev-cli/bin/index.js`
- `packages/maglev-cli/package.json`
- `dist/manifest.json`
- `dist/CHANGELOG.md`
- `dist/CHANGELOG_DRAFT.md`
- `dist/.agents/`
- `dist/.maglev/`
- `packages/maglev-cli/dist/`

### 排除范围

- `specs/20_evolution/active/version_sync_tool/` 仅作为历史参考
- 已删除的 `.maglev/maglev_sync.py`
- 不属于 Maglev 核心框架下发范围的业务代码仓库

## 3. 测试策略

### 3.1 分层策略

测试按四层执行：

1. **下游链路测试**
   - 目标：验证 init/update/dry-run/force/local-dist

2. **上游链路测试**
   - 目标：验证 release/build/manifest/changelog/npm 镜像同步

3. **包装层测试**
   - 目标：验证 `packages/maglev-cli` 的可执行性和镜像依赖

4. **文档一致性测试**
   - 目标：验证 Spec、任务记录和正式交付对象一致

### 3.2 测试结论等级

- `PASS`
  - 主链路与主要验收标准均通过

- `PASS WITH GAP`
  - 主链路通过，但存在已知差距或未闭环点

- `FAIL`
  - 主链路不可用、行为错误、或存在高风险断链

## 4. 测试环境建议

建议准备以下测试目录：

- `sandbox/init-case`
- `sandbox/update-case`
- `sandbox/error-case`
- `sandbox/release-case`

建议优先使用本地离线源测试，降低网络噪声：

- 主离线源：当前仓库 `dist/`
- 模拟更新源：复制一份 `dist/` 为 `dist_v2_mock/`

## 5. 核心测试矩阵

### A. 下游链路测试

#### DT-001 Init 离线初始化

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 在空 Git 目录执行：
   `python dist/maglev_installer.py init --local-dist /abs/path/dist --skip-prompt`

预期：

- 生成 `.agents/`, `.maglev/`, `specs/`, `docs/`, `issues/`, `tests/`
- 生成 `.maglev/config.json`
- 生成 `.maglev/sync_state.json`
- `sync_state.json.last_synced_version == dist/manifest.json.version`

#### DT-002 Init 状态完整性

目标对象：

- `dist/maglev_installer.py`
- `dist/manifest.json`

步骤：

1. 在完成 DT-001 后，随机抽查若干 manifest 文件

预期：

- 本地文件存在
- 本地 SHA-256 与 manifest 一致
- `file_baselines` 包含对应文件

#### DT-003 Init Dry-Run

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 在空目录执行：
   `python dist/maglev_installer.py init --local-dist /abs/path/dist --dry-run --skip-prompt`

预期：

- 不创建任何文件
- 不生成 `.maglev/sync_state.json`
- 输出预览信息

#### DT-004 Update 幂等性

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 在已初始化目录执行：
   `python dist/maglev_installer.py update --local-dist /abs/path/dist`

预期：

- 输出“当前已是最新版本，无需更新”
- 不生成备份文件
- 不发生多余文件写入

#### DT-005 Update NEW

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 准备 `dist_v2_mock`
2. 为 manifest 添加一个新文件并保证源文件存在
3. 运行 update 指向 `dist_v2_mock`

预期：

- 输出 `NEW`
- 新文件下载成功
- `sync_state.json` 含新文件 baseline

#### DT-006 Update OVERWRITE

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 在 `dist_v2_mock` 中修改某已纳管文件
2. 本地不修改该文件
3. 运行 update

预期：

- 输出 `OVERWRITE`
- 本地文件被替换
- 不生成备份

#### DT-007 Update CONFLICT

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 本地修改一个已纳管文件
2. 在 `dist_v2_mock` 中也修改该文件
3. 运行 update

预期：

- 输出 `CONFLICT`
- 生成 `.local_backup_<timestamp>`
- 原位置落入官方新版

#### DT-008 Update Local Missing

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 删除一个已纳管文件
2. 执行 update

预期：

- 文件被恢复
- baseline 正常更新

#### DT-009 Update Force

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 本地修改一个已纳管文件
2. 上游也修改该文件
3. 执行 `update --force`

预期：

- 不生成备份
- 直接覆盖本地文件

#### DT-010 Update Dry-Run

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 构造 NEW / OVERWRITE / CONFLICT 混合场景
2. 执行 `update --dry-run`

预期：

- 仅输出预览
- 不更新状态文件
- 不生成备份

#### DT-011 Shell 入口链路

目标对象：

- `dist/install.sh`

步骤：

1. 在受控测试环境执行 shell 入口
2. 验证参数透传至 Python 安装器

预期：

- 能成功下载/调用 installer
- 参数如 `--dry-run`、`init`、`update` 正常透传

#### DT-012 Npx 离线入口链路

目标对象：

- `packages/maglev-cli/bin/index.js`
- `packages/maglev-cli/dist/`

步骤：

1. 从包目录执行 CLI 入口
2. 验证其调用包内 `dist/maglev_installer.py`

预期：

- 正常识别 Python
- 正常传入 `--local-dist`
- 可在无网络条件下完成离线安装

### B. 上游发行链路测试

#### RT-001 Release Dry-Run

目标对象：

- `scripts/maglev_release.py`

步骤：

1. 执行：
   `python scripts/maglev_release.py --version X.Y.Z --dry-run --skip-audit`

预期：

- 生成构建沙箱
- 流程可推进至 manifest 阶段
- dry-run 模式下不执行推送

#### RT-002 Parse Visibility

目标对象：

- `scripts/maglev_release.py`

步骤：

1. 执行 release dry-run
2. 检查输出统计

预期：

- private 资产被识别
- public 资产被纳入构建

#### RT-003 Manifest 生成正确性

目标对象：

- `scripts/maglev_release.py`
- `dist/manifest.json`

步骤：

1. 读取生成后的 manifest
2. 随机抽查若干文件 hash

预期：

- 包含 `version`, `publish_date`, `changelog_url`, `files`
- 每条文件记录含 `path` 和 `sha256`

#### RT-004 NPM 包内镜像同步

目标对象：

- `scripts/maglev_release.py`
- `packages/maglev-cli/dist/`

步骤：

1. 执行 release dry-run
2. 检查 `packages/maglev-cli/dist/`

预期：

- 包内镜像被更新
- 至少包含 `maglev_installer.py`, `install.sh`, `manifest.json`, `CHANGELOG.md`

#### RT-005 CHANGELOG 草案链路

目标对象：

- `scripts/maglev_release.py`
- `dist/CHANGELOG_DRAFT.md`
- `dist/CHANGELOG.md`

步骤：

1. 执行 release 流程到草案生成阶段
2. 检查 draft 和 final changelog

预期：

- 生成 `CHANGELOG_DRAFT.md`
- 流程会等待 Creator 确认 `CHANGELOG.md`

### C. 文档一致性测试

#### CT-001 主 Spec 唯一性

目标对象：

- `specs/20_evolution/active/maglev_distribution/`
- `specs/20_evolution/active/version_sync_tool/`

预期：

- `maglev_distribution` 保持 `Active`
- `version_sync_tool` 为 `Superseded`

#### CT-002 旧入口清理

目标对象：

- 主 Spec
- 任务文档
- skill 文档

预期：

- 不再把 `.maglev/maglev_sync.py` 作为现行主入口
- 如有提及，只能作为历史实现说明

#### CT-003 Npx 入口纳管

目标对象：

- 主 Spec
- `packages/maglev-cli/`

预期：

- Spec 已明确 `packages/maglev-cli` 为正式入口包装层
- 实现文件存在且可运行

### D. 异常场景测试

#### ET-001 坏 Manifest

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 构造非法 JSON manifest
2. 执行 init 或 update

预期：

- 优雅退出
- 不产生破损态

#### ET-002 Hash 校验失败

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 篡改 manifest 中某个 sha256
2. 执行 init 或 update

预期：

- 输出 hash 校验失败
- 该文件不应被视为成功同步

#### ET-003 上游不可达

目标对象：

- `dist/maglev_installer.py`
- `dist/install.sh`

步骤：

1. 指定错误 upstream
2. 执行 init 或 update

预期：

- 优雅失败
- 不污染工作区

#### ET-004 Clone 失败

目标对象：

- `dist/maglev_installer.py`

步骤：

1. 在 init 交互中输入不可 clone 的仓库地址

预期：

- 不中断整个 init
- 输出诊断建议
- config 中记录 `clone_status`

## 6. 已知 Gap 专项检查

这些检查项不直接判主链路失败，但必须在收尾报告中单列：

### GAP-001 CHANGELOG 摘要播报

现状：

- 主 Spec 承诺 update 后输出 CHANGELOG 摘要
- 当前 `dist/maglev_installer.py` 未见显式实现

结论等级建议：

- 若主链路通过但未播报，记为 `PASS WITH GAP`

### GAP-002 `dist/` 双重角色

现状：

- `dist/` 同时承载实现真身与发行物

结论等级建议：

- 记为结构性风险，不阻断当前功能收尾

### GAP-003 包内镜像一致性依赖流程

现状：

- `packages/maglev-cli/dist/` 的一致性依赖 release 同步

结论等级建议：

- 记为流程性风险，不单独判失败

## 7. 执行顺序建议

建议按以下顺序执行：

1. `CT-001 ~ CT-003`
2. `DT-001 ~ DT-004`
3. `DT-005 ~ DT-010`
4. `DT-011 ~ DT-012`
5. `RT-001 ~ RT-005`
6. `ET-001 ~ ET-004`
7. `GAP-001 ~ GAP-003`

## 8. 测试报告模板

建议最终报告包含：

- 测试日期
- 测试环境
- 主验收 Spec
- 通过用例数 / 总用例数
- 主链路结论：`PASS / PASS WITH GAP / FAIL`
- 已确认通过项
- 已知 Gap
- 是否允许任务收尾

## 9. 推荐收尾口径

如果出现以下结果：

- 主链路全部通过
- 文档一致性通过
- Gap 仅剩 CHANGELOG 摘要播报或结构性整理

则建议结论为：

- `PASS WITH GAP`
- 允许以“功能交付完成、结构整理待后续专项”方式收尾当前任务
