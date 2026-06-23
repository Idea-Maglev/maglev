# Maglev 多入口使用说明

> 目标：明确 Maglev 当前有哪些正式入口，它们分别在什么阶段可用，以及彼此是什么关系。

## 1. 先说结论

Maglev 不是“所有入口在所有阶段都可用”。

更容易理解的说法是：

- **安装前入口**
  - npm / npx 包
- **安装后入口**
  - AI 工作流 / Skill
  - 安装器的后续命令

也就是说：

- 在一个还没有接入 Maglev 的项目里，AI 助手**不是正式安装入口**
- 在一个已经完成初始化的项目里，AI 助手才开始真正帮得上忙

## 2. 为什么要这样分

原因很简单：

- 安装前，目标项目里还没有这些东西：
  - `.agents/`
  - `.maglev/`
  - 本地 workflow / skill
  - `sync_state.json`
- 所以这时项目内部还没有足够基础来承载 Maglev 的 AI 工作流

所以在“首装”这个阶段，当前真正推荐给用户的入口是：

- npm / npx 包

而不是项目内的 `/init`、`/standup` 之类工作流。

## 3. 当前的正式入口分层

### A. 安装前入口

这是“把 Maglev 首次带进项目”的入口。

#### 1. npm / npx 包

你可以把它理解成：

- Node 生态里的安装入口

特点：

- 使用包内自带的离线资产
- 调用包内 `maglev_installer.py`
- 自动附带 `--local-dist`

适合：

- 当前运行环境更偏 Node / npm
- 想通过正式 npm 包完成安装

实现位置：

- [index.js](../../../packages/maglev-cli/bin/index.js)

#### 2. Shell / `curl`（当前不作为正式用户入口）

当前仓库仍然有：

- [install.sh](../../../packages/maglev-cli/dist/install.sh)

但在公开发行制品和 OSS / CDN 分发通道打通之前，它不适合作为正式用户入口。

原因：

- 后续依赖仍指向 GitLab 上游内容
- 会把登录和权限问题暴露给最终用户

所以当前文档中的正式用户路径，统一以 npm / npx 为主。

### B. 安装后入口

这是“项目已经接入 Maglev 之后”的操作入口。

#### 1. AI Workflow / Skill

你可以把它理解成：

- 更友好的使用界面
- 帮用户理解当前状态、下一步动作和风险

当前适合承接：

- 上下文同步
- 导航
- 解释
- 后续更新入口的产品化封装

当前示例：

- `/standup`

注意：

- 这类入口建立在项目已经有 `.agents/` 资产的前提上
- 因此它不应被视为首装入口

#### 2. 安装器的后续命令

作用：

- 在初始化完成后继续执行：
  - `update`
  - `dry-run`
  - `force`
  - 本地离线更新

当前对应实现：

- 包内镜像或发行物中的 `maglev_installer.py`

注意：

- 下游项目根目录不会直接出现 `maglev_installer.py`
- 对用户来说，推荐入口仍然是 `npx @idea-maglev/maglev-cli`

### C. 源仓库维护入口

这是“你正在维护 Maglev 自己，而不是在业务项目里使用 Maglev”的入口。

#### 1. 统一版本管理脚本

作用：

- 查看当前版本状态
- 统一修改版本
- 校验版本事实是否漂移

当前对应实现：

- [maglev_version.py](../../../scripts/maglev_version.py)

常见命令：

```bash
python3 scripts/maglev_version.py show
python3 scripts/maglev_version.py set 0.1.4
python3 scripts/maglev_version.py check
```

#### 2. 发行构建脚本

作用：

- 基于当前源仓库构建 release 产物
- 生成 manifest 与 changelog 草案
- 同步 npm 包镜像目录

当前对应实现：

- [maglev_release.py](../../../scripts/maglev_release.py)

如果你要维护和发布 Maglev 本身，建议继续看：

- [Maglev 开发与发布流程](./maglev_development_release_workflow.md)
- [Maglev 发布说明与维护手册](./maglev_release_manual.md)
- [Maglev 重建与更新联调手册](./maglev_rebuild_and_update_e2e_manual.md)

## 4. 这些入口之间是什么关系

更直白地说：

- **真正干活的核心**
  - 发行物 / 包内镜像中的 `maglev_installer.py`
- **对外入口**
  - `npx maglev-cli`
- **更友好的交互层**
  - AI workflow / skill
- **维护者治理入口**
  - `maglev_version.py` / `maglev_release.py`

也就是说：

- npm / npx 不是另一套独立逻辑
- AI workflow / skill 也不是另一套同步引擎
- 它们都应围绕同一个执行核心组织
- `.maglev_build/` 是 release 构建沙箱，`packages/maglev-cli/dist/` 是 npm 包内镜像；两者都不是长期真相源

## 5. 不同阶段该用哪个入口

### 场景 A：一个完全空白、还没接入 Maglev 的项目

建议：

- 直接用 npm / npx 包安装

不建议：

- 假设项目里已经存在 `/init` 或 `/standup`

### 场景 B：一个已经初始化过的 Maglev 项目

建议：

- 用 AI workflow 做上下文同步与导航
- 用统一执行核心或其 npm 包入口执行更新

### 场景 C：需要验证发行物更新是否生效

建议：

- 优先直接调用统一执行核心
- 或通过 npm / npx 包验证

原因：

- 这样最容易隔离问题
- 也最容易确认是发行物、镜像还是 AI 交互层出了问题

### 场景 D：你正在修改 Maglev 自己并准备发版

建议：

- 先用 `maglev_version.py` 统一修改和校验版本
- 再用 `maglev_release.py --dry-run --skip-audit` 做本地发行验证

不建议：

- 手工分别改多个版本文件
- 跳过版本一致性检查直接做 release

## 6. 当前还没完全补齐的地方

虽然模型已经比较清楚，但当前仓库还有几个未闭环点：

- 安装前与安装后入口的边界，还没有全面回填到所有入口文档
- 正式的 AI 更新入口还没有完全产品化
- 部分旧文档仍会让人误以为 `/init` 是任何场景下都天然可用

这些都属于当前分发体系的遗留补全项。

## 7. 推荐阅读顺序

如果你想完整理解当前分发体系，推荐按这个顺序继续：

1. [Maglev 快速开始](./maglev_distribution_quickstart.md)
2. [Maglev 更新与同步手册](./maglev_update_manual.md)
3. [角色与流程翻译](./maglev_role_flow_translation.md)
4. [Maglev 开发与发布流程](./maglev_development_release_workflow.md)
5. [Maglev 发布说明与维护手册](./maglev_release_manual.md)
6. [分发技术设计](../../../specs/20_evolution/active/maglev_distribution/02_design_backend.md)
7. [分发 runtime 治理任务归档](../../../issues/closed/task_distribution_runtime_governance.md)
