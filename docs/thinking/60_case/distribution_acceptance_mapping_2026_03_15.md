# Distribution Acceptance Mapping - 2026-03-15

## 目的

本文件用于建立当前分支的统一验收口径，明确：

- 哪个 Spec 是主验收依据
- 哪些文件是正式实现
- 哪些文件属于发行物
- 哪些文件属于入口包装层
- 哪些内容应被排除在主验收对象之外

这份映射用于后续测试计划、验收结论和收尾报告。

## 一、主线结论

当前分支唯一主验收 Spec：

- `specs/20_evolution/active/maglev_distribution/`

历史演进 Spec，不再作为主验收对象：

- `specs/20_evolution/active/version_sync_tool/`

已移除的过渡实现：

- `.maglev/maglev_sync.py`

## 二、验收分层

### 1. 主 Spec 层

这些文件定义“应该交付什么”：

- `specs/20_evolution/active/maglev_distribution/00_vision.md`
- `specs/20_evolution/active/maglev_distribution/01_requirements.md`
- `specs/20_evolution/active/maglev_distribution/02_design_backend.md`

验收职责：

- 确认分发目标、安装/更新流程、发版链路、Npx 包装层是否成立
- 确认当前交付范围覆盖主 Spec 中承诺的核心能力

### 2. 主实现层

这些文件定义“系统真正怎么跑”：

- `dist/maglev_installer.py`
- `dist/install.sh`
- `scripts/maglev_release.py`
- `packages/maglev-cli/bin/index.js`
- `packages/maglev-cli/package.json`

验收职责：

- `dist/maglev_installer.py`
  - 下游 Init / Update / Dry-Run / Force / Local Dist
  - 四态同步
  - `sync_state.json`

- `dist/install.sh`
  - Shell 入口
  - 远端下载安装器
  - 参数透传

- `scripts/maglev_release.py`
  - 上游构建与发布编译流程
  - 生成构建沙箱、manifest、CHANGELOG 草案
  - 同步 npm 包内镜像

- `packages/maglev-cli/bin/index.js`
  - Npx 入口
  - Python 环境探测
  - 调用包内 `dist/maglev_installer.py`
  - 传入 `--local-dist`

- `packages/maglev-cli/package.json`
  - npm 包标识与 bin 入口声明

### 3. 发行物层

这些文件定义“实际对下游发布了什么”：

- `dist/manifest.json`
- `dist/CHANGELOG.md`
- `dist/CHANGELOG_DRAFT.md`
- `dist/.agents/...`
- `dist/.maglev/...`

验收职责：

- `manifest.json` 是否包含正确版本号和文件哈希
- 发行包中是否只包含 public/runtime 资产
- CHANGELOG 草案和正式 CHANGELOG 是否符合发布流程预期

### 4. 包内镜像层

这些文件定义“npm 包内实际内嵌了什么”：

- `packages/maglev-cli/dist/`

验收职责：

- npm 包内镜像是否与当前 release 构建结果一致
- `maglev-cli` 是否能离线调用这些镜像资产

### 5. 支撑文档层

这些文件不直接执行功能，但会影响验收口径：

- `issues/active/task_maglev_distribution.md`
- `issues/closed/draft_issue_maglev_distribution.md`
- `.agents/skills/maglev-changelog-generator/SKILL.md`

验收职责：

- 确保任务记录与当前主语义一致
- 不再误导 review/test 目标

## 三、对象到职责映射表

| 层级 | 文件/目录 | 角色 | 是否主验收对象 |
| :--- | :--- | :--- | :--- |
| Spec | `specs/20_evolution/active/maglev_distribution/` | 主规范 | 是 |
| Spec | `specs/20_evolution/active/version_sync_tool/` | 历史演进记录 | 否 |
| Runtime | `dist/maglev_installer.py` | 下游统一执行核心 | 是 |
| Entry | `dist/install.sh` | Shell 入口 | 是 |
| Entry | `packages/maglev-cli/bin/index.js` | Npx 入口包装层 | 是 |
| Package | `packages/maglev-cli/package.json` | npm 包元数据 | 是 |
| Release | `scripts/maglev_release.py` | 上游发行编译器 | 是 |
| Artifact | `dist/manifest.json` | 发行清单 | 是 |
| Artifact | `dist/CHANGELOG.md` | 面向用户的发行说明 | 是 |
| Artifact | `dist/CHANGELOG_DRAFT.md` | 语义化日志草案输入 | 条件性 |
| Artifact | `dist/.agents/` | 下发 Skills / Workflows | 是 |
| Artifact | `dist/.maglev/` | 下发 Runtime 协议与规则 | 是 |
| Package Artifact | `packages/maglev-cli/dist/` | npm 包内镜像 | 是 |
| Legacy | `.maglev/maglev_sync.py` | 过渡实现，已移除 | 否 |

## 四、后续测试应该如何引用这张表

### 下游链路测试

对应对象：

- `dist/maglev_installer.py`
- `dist/install.sh`
- `packages/maglev-cli/bin/index.js`
- `packages/maglev-cli/dist/`

覆盖内容：

- Init
- Update
- 四态同步
- Dry-Run
- Force
- 离线安装
- Npx 包装入口

### 上游链路测试

对应对象：

- `scripts/maglev_release.py`
- `dist/manifest.json`
- `dist/CHANGELOG_DRAFT.md`
- `dist/CHANGELOG.md`

覆盖内容：

- Parse Visibility
- Assemble dist
- Manifest 生成
- npm 包内镜像同步
- CHANGELOG 草案/确认链路

### 文档一致性测试

对应对象：

- `specs/20_evolution/active/maglev_distribution/`
- `issues/active/task_maglev_distribution.md`
- `packages/maglev-cli/`

覆盖内容：

- 主 Spec 与实现对象一致
- 主 Spec 不再引用旧入口为现行实现
- Npx 入口被纳入正式范围

## 五、当前已知 Gap

以下内容当前应视为“已知差距”，测试时需要单独标注，而不是混入主链路失败：

1. `dist/maglev_installer.py` 当前未见显式的远端 CHANGELOG 摘要打印逻辑。
2. `dist/` 仍同时扮演“源码承载区”和“发行物区”。
3. `packages/maglev-cli/dist/` 的一致性依赖 release 流程同步，而不是更强的结构约束。

## 六、使用结论

从这一刻开始，后续任何测试计划、验收报告、收尾结论，都建议按以下口径执行：

1. 只以 `maglev_distribution` 为主 Spec。
2. 只以 `dist/maglev_installer.py` 为下游统一执行核心。
3. 只以 `scripts/maglev_release.py` 为上游发布链路核心。
4. 将 `packages/maglev-cli/` 视为正式交付的一部分，而不是附属脚本。
5. 不再将 `version_sync_tool` 或 `maglev_sync.py` 作为主验收对象。
