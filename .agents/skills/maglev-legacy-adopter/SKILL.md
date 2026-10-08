---
name: maglev-legacy-adopter
description: 存量项目接入器。负责环境诊断、基础设施注入，并编排逆向工程与索引构建。
metadata:
  formal_action_name: 存量接入
  top_level_capability: 整体接入
  system_layer: Infrastructure Layer
  lifecycle_chain: system_enablement
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
---

# 存量接入器 (Legacy Adopter)

> 结构动作名：`存量接入`
> 运行面名称：`maglev-legacy-adopter`
> 这不等于已经完成正式物理改名。

## 核心规则

1. 接入过程不得破坏现有代码逻辑。
2. 不要求项目先有完整文档，而是允许根据代码和已有产物重建结构理解。
3. 存量接入不是终点，接入后应继续完成逆向、审计和索引回填，确保产物可持续维护。

## 何时使用

- 需要把一个已有仓库纳入 Maglev 结构时。
- 项目已存在代码与运行现实，但缺少可直接进入 Maglev 主流程的基础承接时。
- 需要为后续逆向、索引和治理建立最小接入环境时。

## 处理流程

### Phase 1: 环境诊断

**目标**：评估项目现状，确定接入策略。

- 扫描项目根目录。
- 检查关键特征：`pom.xml` / `package.json`、`README.md`、`specs/` 等。
- 将 `.agents/`、`.maglev/` 以及由 Maglev 生成的索引/治理文件单独标记为
  `maglev_managed_context`；它们只能证明接入工具和治理资产状态，不能直接作为业务
  Feature Map、业务流程或业务 Reality 的事实来源。
- 如果发现已有 `docs/ATLAS.md`、`repo-entry.yaml` 或类似导航产物，先执行或核对其
  新鲜度检查；未能证明它来自当前目标仓库的最新证据时，只能作为导航线索，不能作为
  逆向输入事实。
- 若发现关键目录结构缺失，应明确提示当前接入风险和最小补齐建议。
- 仓库根目录、submodule 和 package 只能登记为 `source_units`；不得把 source unit
  清单直接转换成 domain 或 Reality 一级目录。

### Phase 2: 基础设施注入

**目标**：建立 Maglev 运作所需的最小环境。

- 确认 `.maglev` 配置（Rules/Protocols）是否存在。
- 确认 `.agents` 技能库是否完整。
- 若缺失，引导进入 `maglev-bootstrapper` 或补齐最小基础设施。

### Phase 3: 逆向工程准备

**目标**：建立第一个可持续依赖的现实锚点。

- 询问本项目中最核心、或近期准备修改的功能范围。
- 若项目已有 `specs/10_reality/00_profile.yaml`，先读取并核对其来源；
  只有目标明确属于 Maglev 源仓库时才能使用 `maglev-core-v1`。消费者项目没有
  自己的已确认 Profile 时保持无 Profile 状态，不得复制 Maglev 的 domains、Reality 页或当前事实。
- 调用 `maglev-reverse-spec` 建立第一个 Reality Projection，并将结果映射到目标项目自己的 Profile
  主域和槽位。
- 首次建立 Profile 时，先建立技术 `source_units`，再根据业务对象、用户任务、流程、权限
  和数据责任形成 `domain_registry`；没有业务边界证据时不得注册 domain。
- `domain_policy: business_evidence` Profile 必须按共享 Contract 建立每个 domain 的完整
  slot skeleton；事实正文只能落在 `{domain}/{owner_slot}/`，不得继续生成
  `domains/<id>.md`、`modules/<module_slug>.md` 或 domain 根目录单文件。
- 无法映射的事实保持 unknown，不按主题新建目录。

### Phase 4: Projection Validation & Admission

**目标**：确保逆向结果达到可继续协作的质量门槛。

- 从 candidate commit 创建独立 Validator worktree。
- 验证完整 Reality tree、既有 Reality 与本次 diff。
- 生成绑定 candidate commit、完整 Reality digest、change digest、Profile/Contract
  version 的 Validation Result。
- 调用共享 Reality Admission；只有 `accepted` 或 `no_change` 才能进入后续索引和地图动作。
- `integrated-validator` 的报告只能作为 source evidence，除非已绑定同一 Projection。

### Phase 5: 索引登记

**目标**：将新接入结果纳入可发现性体系。

- 调用 `index-librarian`
- 仅在 Admission Receipt 成功后更新对应索引，使后续会话可以发现已准入结果。

### Phase 6: 首次项目地图

**目标**：在仓库身份、Reality 与索引边界稳定后生成唯一的人读地图。

- 若项目已具备 Git 根目录，调用 `maglev-map-maker` 生成 `docs/ATLAS.md`
- 立即运行 Map Maker 的 `--check`
- 地图生成失败不伪装接入完成；保留错误和下一责任对象

## 必需的参考资料

- 工作流入口: `references/legacy-adopter.workflow.md`
- 诊断步骤: `references/step-01-mri-scan.md`
- 引导步骤: `references/step-02-bootstrap.md`
