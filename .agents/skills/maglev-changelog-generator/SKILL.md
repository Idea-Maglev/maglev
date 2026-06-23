---
name: maglev-changelog-generator
description: 读取 Changelog Draft，结合源码分析，生成面向用户的语义化 CHANGELOG.md (仅 Creator)
metadata:
  formal_action_name: 版本说明生成
  top_level_capability: 非核心主流程能力
  system_layer: Specialized Support Layer
  lifecycle_chain: specialized_support
  runtime_name_status: active_legacy_name
  distribution_scope: private_only
  author: Maglev Core
  version: "1.0.0"
  last_updated: 2026-04-23
  distribution: private
---

# Maglev Changelog Generator (Private Skill)

> 结构动作名：`版本说明生成`
> 运行面名称：`maglev-changelog-generator`
> 这不等于已经完成正式物理改名。

## 🎯 核心目标
将由发布脚本 (`maglev_release.py`) 自动生成的机械的 `.maglev_build/CHANGELOG_DRAFT.md` (仅列出了新增、修改、删除的文件路径)，转化为结构清晰、面向用户痛点的**语义化 Changelog**，以此作为发行版本的主要说明。

## ⚠️ 触发条件
仅在 Creator 执行全流程发版工作流 (`/generate-changelog`) 时被调用。

## 🛠️ 执行步骤 (AI 行为指导)

### Step 1: 研读 Draft 与提取 Context
1. 分析 `.maglev_build/CHANGELOG_DRAFT.md` 提供的变更文件列表。
2. 对具有实质影响的文件（如 `*.py`, `*.md`, `*.json` 等核心资产）：
   - 使用 `view_file` 或相关工具，查阅修改前后的 Diff 或其当前内容。
   - 分析：这个文件变更**解决了什么功能痛点**？或带来了哪些**新特性**？

### Step 2: 归类与提炼 (Semantics Extraction)
将机械的文件列表转换为面向用户的业务分类：
- **✨ 新特性 (Features)**: 新增的 Workflow、Skill 或完整的业务能力集。
- **🚀 性能优化与打磨 (Enhancements)**: 现有的 Workflow、Prompt 优化，体验提升。
- **🐛 缺陷修复 (Bug Fixes)**: 对特定崩溃、执行异常或逻辑漏洞的修补。
- **💥 破坏性变更 (Breaking Changes)**: 参数改变、工作流删除、需要用户主动适应的架构调整。

> **规则**: 不要把 "修改了 `core_rules.md`" 算作功能特性。要写明 "将项目全局 SSOT 规范统一，修正了代码审查中的冗余描述"。

### Step 3: 输出本次发行说明并归档
根据提取出的信息：

1. 在 `.maglev_build/` 目录下生成 `CHANGELOG.md`
2. 在 `docs/releases/` 下生成对应版本文件，例如 `docs/releases/0.1.4.md`
3. 更新 `docs/releases/index.md`，为当前版本追加入口链接

两份内容应保持一致，前者用于本次 release 构建，后者用于长期版本归档。必须严守以下格式要求。

---
## 📝 CHANGELOG.md 标准输出模板

```markdown
# [1.2.0] - YYYY-MM-DD (按实际当前日期)

## ✨ 新特性 (Features)
- **核心组件化升级**: 新增了 `maglev-changelog-generator`，支持全自动提取语义化日志。([#Issue号或保留为空])
- **Npx cli**: 新增了 NPM 入口代理程序，支持 `npx maglev-cli` 执行初始化。

## 🚀 性能优化与打磨 (Enhancements)
- **更新算法重构**: `maglev_installer.py` 中重构为了四态状态机同步策略，更新效率与准确度大幅提升。

## 🐛 缺陷修复 (Bug Fixes)
- 修复了在只读目录下执行 `init` 找不到 `.git` 引发的崩溃问题。

## 💥 破坏性变更 (Breaking Changes)
- 历史同步入口已移除，请使用统一的 Python Installer 脚本代替。

---
*注: 此更新日志由 Maglev Changerlog Generator 自动提炼。*
```

---
## ✅ 终态检查 (Definition of Done)
1. 生成的 `.maglev_build/CHANGELOG.md` 必须准确包含本次发布 Draft 中所有的核心功能变化。
2. `docs/releases/<version>.md` 必须存在，并与本次 release 的正式说明一致。
3. `docs/releases/index.md` 必须已登记当前版本链接。
4. 不可包含无关紧要的、枯燥的文件 Hash 修改描述。
5. 必须在执行完毕后用中文友善输出：
   > "✨ Changelog 已生成并写入至 `.maglev_build/CHANGELOG.md`，并已归档到 `docs/releases/<version>.md`，同时更新了 `docs/releases/index.md`。请在此终端核对内容，无误后请在之前暂停的 release compiler 脚本所在终端内按【回车键】继续 Publish。"
