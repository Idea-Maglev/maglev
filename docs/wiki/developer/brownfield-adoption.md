---
title: "存量项目渐进式接入"
dimension: developer
audience: developer
page_type: how-to
last_updated: "2026-09-15"
generator: wiki_authoring
---

# 存量项目渐进式接入

存量接入的原则是**代码切入，规格演进**：先从正在发生的真实变更建立局部理解，再把快照规格和新需求带入后续实现。不要把一次局部逆向结果当成整个系统的完整真相。

老项目文档缺失甚至过时时，**代码是唯一的真理**。接入策略是反向对齐（Code First Entry, Spec First Evolution）：不要求先补全文档再干活，而是让 AI 先"读"代码重建现状，再让 Spec 随迭代自然生长（策略出处：[存量项目引入 Maglev](../../../source operation guides/00_start/legacy_project_adoption.md)）。底线是业务连续性：不要为了追求方法的纯洁性，而牺牲了业务的连续性。

```mermaid
flowchart LR
    A[代码现状<br>Source of Truth] -->|逆向重建| B[Snapshot Spec]
    B --> C[Snapshot Spec + 新需求]
    C --> D[Updated Spec]
    D --> E[新代码]
    E -->|下一个迭代| B
```

## 三条接入路径怎么选

接入 Maglev 有三条路径，按项目当前状态选，不要混着跑（出处：[接入与集成能力](../../../internal Reality/adoption-integration/capability/overview.md)）：

| 你的处境 | 走哪条路径 | 它做什么 |
| :--- | :--- | :--- |
| 空目录或新环境，还没有业务代码 | `maglev-bootstrapper`（`/maglev-init` 或 "Initialize Maglev"） | Greenfield/Adoption 判定，注入骨架目录（`.agents/`、`.maglev/`、空 `specs/`、`docs/`、`issues/`），完成仓库登记与初始化自检 |
| 已有代码仓库，要整体纳入 Maglev 且不破坏现有逻辑 | `maglev-legacy-adopter` | 六阶段接入：环境诊断 → 基础设施注入 → 逆向准备 → Projection 验证准入 → 索引登记 → 首次项目地图 |
| 只想为项目重建可独立核对的当前事实 | `maglev-reverse-spec` | 经 Gate A / Gate B 人工裁决的逆向重建：阶段 A 语义审阅、阶段 B 事实核对与准入；不修业务代码、不补测试、不做设计决策 |

选错的典型信号：项目里已有业务代码却跑 `/maglev-init`（应走 legacy-adopter）；只需要摸清某个模块现状，却启动整套接入流程（直接走 reverse-spec 代价更小）。本页下文展开的正是后两条路径——存量项目最常见。

### 消费者隔离：接入的是空白实例

无论走哪条路径，消费者项目默认只得到**空白 Maglev 实例**：不携带 Maglev 源仓库的 Reality、项目地图或事实页——那些是 Maglev 自己仓库的当前事实，不是你项目的。bootstrapper 仅在你确认登记至少一个仓库后，才会生成/更新 `internal Reality/crosscutting/repository-map/repositories.md`；未登记仓库不得创建该文件。你项目的 Reality 只能从自己的逆向重建与需求迭代里长出来。

## 分阶段接入存量项目

### 按三阶段推进，不搞一刀切

三个阶段的完整展开见[存量项目引入 Maglev](../../../source operation guides/00_start/legacy_project_adoption.md)：

**Phase 1：零文档接入**（修 Bug、微小优化时）。甚至不需要 `specs/` 目录：直接把相关代码文件放进 AI 上下文，让它"阅读这段代码，修复 NPE bug，保持原有代码风格"。此阶段只用 AI 编码能力，不引入流程。

**Phase 2：局部逆向**（要迭代某个核心模块，如 `PaymentService` 时）。运行 `/maglev-legacy-adopter`，技能会依次完成：

1. 自动诊断项目结构并初始化 `.maglev` 环境
2. 调用 `maglev-reverse-spec` 逆向你指定的模块
3. 逆向结果经共享 Reality Admission 准入，只有 `accepted` / `no_change` 才继续
4. 调用 `index-librarian` 登记资产，并在项目具备 Git 根目录时用 `maglev-map-maker` 生成 `docs/ATLAS.md`

**Phase 3：增量覆盖**（日常迭代）。**不动不补**：只有要修改的模块才补全它的 Spec；随着 Sprint 进行，`specs/` 自然覆盖最活跃的业务域；万年不改的死代码让它安静躺着，不需要 Spec。

### 给存量路径配置豁免

在 VibeKanban 或 Husky 中配置 Spec 检查豁免规则：修改 `/legacy/*` 目录不强制检查 Spec 关联；修改 `/active/*` 目录必须有 Spec。

### 需要完整重建当前事实时：走逆向现状重建流程

1. **准备**：锁定目标项目根目录、当前基线提交、当前用途（交接、重构前分析、接口核对或验证）、允许读取的来源及其角色（`intent` 目标与约束 / `implementation` 代码与配置 / `verification` 测试与断言），以及相互隔离的人读产物目录和机器证据目录
2. **建立读取契约**：一份可回查的最小契约，例如：

```yaml
reverse:
  project_id: <项目标识>
  project_root: <项目相对路径>
  baseline: <基线提交>
  source_units:
    - unit_id: application
      relative_path: src
      roles: [implementation]
      exclusions: []
  output:
    human_review_root: <项目外或隔离的人读目录>
    machine_evidence_root: <项目外或隔离的机器证据目录>
```

3. **阶段 A——语义审阅**：按项目形态选阅读入口（有页面的应用找页面路由、接口服务找接口资源、异步系统找任务与事件、命令行工具找命令、数据系统找实体与数据生命周期），直接阅读原文生成语义审阅包；结论必须标 `[FACT]` / `[INFERENCE]` / `[UNKNOWN]` / `[BLOCKED]`，没有直接证据不能写成事实；然后人工审阅四件事——模块边界、拆分合并、跨模块公共内容、无法归属项，裁决用 `accept` / `split` / `merge` / `defer` / `keep_unclassified` / `request_scope_change`（阶段 A 的完整流程出处：[逆向现状重建手册](../../../source operation guides/20_operations/reverse_reality_manual.md)）
4. **阶段 B——事实核对与准入**：先做只读结构校验；再按当前用途核对事实，每个维度登记 `covered` / `not_applicable` / `unknown` / `blocked`；把已核对事实写入**目标项目自己的**现实资料位置（逆向只改现实资料，不改业务代码、测试、数据）；最后由独立验证方检出同一候选提交核对后准入，记录 `base_commit` 与 `candidate_commit`（阶段 B 的准入与证据要求出处：[逆向现状重建手册](../../../source operation guides/20_operations/reverse_reality_manual.md)）


## 验证

接入成功的标志：

- 修改热点模块前有 Snapshot Spec 可依，新需求走"Updated Spec → 新代码"而不是直接改代码
- `specs/` 覆盖了活跃业务域，且没有为死代码空造 Spec
- 逆向产出的现实资料写入目标项目自己的位置，业务代码零改动

## 下一步

- [安装 maglev-cli](first-success.md)：老项目首次安装 Maglev 环境本身的命令
- [日常推进手册](session-workflow.md)：接入完成后，每个工作循环怎么操作
- [故障排查与常见问题](update-and-recovery.md)：安装或初始化报错先查这里
