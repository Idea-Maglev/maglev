# Maglev 接入模式演进推演 (Adoption Model Evolution Log)

> **Document Status**: Archived
> **Decision**: 最终确立 **"Workstation Mode" (工作站模式)** 为标准接入方案 (Track B)。
> **Context**: 本文档记录了针对 "如何将 Maglev 引入存量项目" 这一命题的三轮红队 (Red Team) 对抗与架构推演过程。

---

## Round 1: 物理隔离的诱惑 (The Wrapper Trap)

**Proposal**: 为了不侵入业务仓库，提出建立一个 `Consumer Wrapper Repo`，将业务仓库作为 Submodule 引入。
**Red Team Attack**:
1.  **IDE 上下文割裂**: 开发者习惯直接打开业务仓库根目录，导致位于父目录的 Maglev Spec 不可见。
2.  **Git Submodule 灾难**: 同步成本极高，容易导致 HEAD 游离。
3.  **Code/Spec 割裂**: 无法原子化提交，Spec 回滚困难。

**Result**: 驳回纯 Wrapper 模式，但用户坚持 "多仓库聚合" 和 "零侵入" 的需求。

---

## Round 2: 协作分裂 (The Schism)

**Proposal**: 坚持 Wrapper 结构（父子目录），但不使用 Submodule，仅做目录嵌套。
**Red Team Attack**: 
1.  **影子规格 (Shadow Spec)**: 如果 Spec 只存在于父仓库，那些只 clone 了子仓库开发的同事（或 CI）将完全看不到 Spec。
2.  **环境熵增**: 每个开发者都需要手动 `mkdir wrapper; cd wrapper; git clone repo_a;`，环境一致性极差。
3.  **阶级对立**: 只有架构师看得到 Spec (Wrapper)，一线开发只能盲写 (Inner)。

**Result**: 确认必须解决 Spec 的 "可见性" 和 "环境统一性" 问题。

---

## Round 3: 工程摩擦 (Engineering Friction)

**Proposal**: **Workstation Mode**。定义 `maglev-workspace` 为统一工作台，强制所有开发在此目录下工作。
**Red Team Attack**:
1.  **双脑不同步 (Split-Brain)**: 开发者在 Inner Repo 切了分支，但忘了切 Outer Repo 的分支，导致 Spec 版本错位。
2.  **CI 盲区 (Gatekeeper Blindness)**: CI Runner 依然只拉取 Inner Repo，因此无法进行 "Spec-First" 检查。
3.  **脏提交 (Dirty Commit)**: `source/` 目录可能被意外提交进 Outer Repo。

**Final Defense (The Glue)**:
风险已从 "逻辑死局" 降维为 "工程成本"。通过以下机制化解：
-   **Workspace Hooks**: 自动同步内外层分支状态。
-   **CI Injection**: 修改 CI 脚本，主动拉取 Maglev 上下文。
-   **Pre-commit Guard**: 物理阻断脏文件提交。

---

## 最终结论 (Verdict)

**Workstation Mode** 是平衡 "组织管理" (统一视角) 与 "工程隔离" (业务零侵入) 的最优解。虽然它需要一定的 "胶水脚本" 维护成本，但它成功实现了：
1.  **非侵入性**: 业务仓库无需任何改动（除了被挂载）。
2.  **全景视角**: `specs/` 与 `source/` 同屏展示。
3.  **可回滚性**: 随时可以删除外壳，退回到纯业务开发模式。
