# Maglev Specs Lifecycle Protocol (Spec 全生命周期协议)

> **Type**: Core Solution (定义层)
> **Status**: Experimental (Agency Inversion Model + Uncertainty Principle)
> **Theory**: Johnny.Decimal & Lifecycle Governance

## 1. 核心定义 (The Definition)

我们将 `specs/` 定义为**"产品生命周期引擎"**。
AI 不仅是引擎的操作者，更是引擎的**看守者 (Custodian)**。

## 2. 目录标准 (Directory Standard)

| 编号 | 状态 (State) | 隐喻 | 必须包含 (Mandatory) | AI 职责 (Custodian Duty) |
| :--- | :--- | :--- | :--- | :--- |
| **00** | **Vision** (展望) | ☁️ | `roadmap.md` | 北极星。仅供读取参考。 |
| **10** | **Reality** (现状) | 🏛️ | `repository_map.md` | **SSOT**。唯有"已交付"的真理方可入库。 |
| **20** | **Evolution** (演进) | 🏗️ | `intake/`, `active/` | **施工现场**。 |
|      | `intake/`    | 📦 | `01_prds/`<br>`02_meetings/`<br>`03_designs/` | **原料仓 (Warehouse)**。不做区分，只要是 Input 全扔这里。 |
|      | `active/`    | 🧱 | `feat_xxx/`<br>`feat_xxx/context/` | **流水线**。存放原子化的 Spec 和 DraftAssets。`context/` 为 AI 上下文数据区（详见 `collaboration.md` §3）。 |
| **90** | **Archive** (历史) | 🏺 | `feat_xxx/` | 任务结束后，Visual Assets 默认归档于此。 |
| **99** | **Debt** (债务) |  | `debt_register.md` | 发现临时代码 (Hacks) 时，**主动**记录。 |

## 3. 工作流：三拍子节奏 (Workflow: The Three-Beat Rhythm)

> **Universal Rule**: 所有关键动作必须遵循 **Propose -> Reflect -> Execute** 的三拍子。
> **Trigger**: 一切始于 **Issue** (Feature or Bug)。Spec 是 Issue 的意图投影。

### 3.0 任务启动 (The Trigger)
*   **Feature Flow (Green)**: 用户创建 Feature Issue -> 触发 Atomizer -> 生成 Spec。
*   **Bug Flow (Red)**: 用户创建 Bug Issue -> 触发 Reverse Correction -> 修正 Spec。

### 3.0 意图雾化 (The Atomizer)
*   **Context**: 当输入为 Massive PRD 时。
*   **Step 1: Proposal (拟定方案)**
    *   **🤖 AI Drive**: "请分析 `intake/PRD.md`，拟定任务拆解计划。"
    *   AI 输出: "建议拆分为 A, B, C 三个任务..."
*   **Step 2: Reflection (反思与对齐) [CRITICAL]**
    *   **Reflect**: AI 自查或人类追问。"反思: 这样拆解是否遗漏了鉴权模块？B 任务的依赖是否清晰？"
    *   **Align**: 修正方案，直到达成共识。
*   **Step 3: Atomization (雾化生成)**
    *   **🤖 AI Drive**: "按此方案执行拆解。"
    *   **Action**: Batch Create Issues in `issues/active/` + Traceability Links.
    *   **🖐 Manual Drive**: 人工创建 Issue 文件并手动粘贴 PRD 链接。

### 3.1 意图雾化 (The Atomizer & Synthesizer)
*   **Context**: 当输入为多模态原料 (PRD, Meeting, Design) 时。
*   **Step 1: Proposal (Synthesis)**
    *   **🤖 AI Drive**: "阅读 `intake/` 下的所有材料，识别冲突，生成 Spec Context。"
    *   **AI Output**: "检测到设计稿按钮颜色与会议记录冲突。建议以设计稿为准。是否确认？"
*   **Step 2: Reflection (反思与对齐) [CRITICAL]**
*   **Step 3: Atomization (雾化生成)**

### 3.2 启动原子意图 (Start Intent)
*   **Context**: 当输入为原子想法 (Atomic Idea) 时。
*   **Step 1: Proposal**: 用户: "我想做 X"。
*   **Step 2: Reflection**: AI: "理解。但做 X 是否涉及到 Y 的修改？" -> 用户确认。
*   **Step 3: Execution**:
    *   **Action**: 创建 Issue + 初始化 `specs/20_evolution/active/` 目录 + 更新 Dashboard。
    *   **[Side-Effect]**: 检查 `INDEX.md` 和 `specs/repository_map.md`，确保新模块被索引。
    *   **🖐 Manual Drive**: 人工在 `issues/active` 创建 Markdown，手动更新 `issues/README.md`。

### 3.3 演进与执行 (Evolve & Execute) - "Sandbox Mode"
*   **Constraint**: **严禁触碰 `10_reality`**。即便代码写完了，Spec 也暂时停留在 `20_evolution`。
*   **Step 1: Proposal (Drafting)**
    *   **🤖 AI Drive**: "基于 PRD 章节生成 Spec Draft。"
    *   **🖐 Manual Drive**: 人工参考 PRD，在 `20_evolution/active/` 下手写 Spec。
*   **Step 2: Reflection (Review)**
    *   Human: "这个接口设计有各种边界情况没考虑。" -> AI 修正 Draft。
*   **Step 3: Execution (Coding)**
    *   **🤖 AI Drive**: "Spec 已确认，开始写代码。"
    *   **🖐 Manual Drive**: 人工对照 Spec 写代码。
    *   **Action**: 更新 Dashboard 状态为 "🏗️ Coding"。

### 3.4 技术方案生成 (The Tech Synthesizer) [NEW]
*   **Context**: Spec 已确认，技术实现偏复杂 (Complex Feature/Arch Change)。
*   **Constraint**: 必须遵循 **[13-Point Robustness Checklist]** (Build/Evolve/Run)。
*   **Step 1: Context Load**
    *   **Action**: AI 读取 `10_reality/repository_map.md`。
*   **Step 2: Proposal (Tech Draft)**
    *   **Action**: 生成 `technical_design.md` 或写入 Spec 的 Implementation 章节。
*   **Step 3: Reflection (Robustness Check)**
    *   **Check**: 检查 Migration, Rollback, Observability 等 13 点。
    *   **Human Fallback**: 抛出无法闭环的外部依赖 (Blocker)。

### 3.5 视觉验证 (Visual Verification) [可选]
*   **Context**: Spec 已定，代码未写。**仅当涉及 UI 变更时触发。**
*   **Step 1: Proposal**
    *   **🤖 AI Drive**: (Optional) "基于 Spec 生成一个 HTML 原型用于验证。"
    *   **Action**: 生成 `specs/20_evolution/active/feat-x/assets/prototype.html`。
*   **Step 2: Reflection (User Check)**
    *   **🖐 Manual Drive**: 打开 HTML 点一点。"流程通了，但缺少加载状态。"
*   **Step 3: Execution**: 修正 Spec。

### 3.6 结算与处置 (Delivery & Disposal Strategy)
*   **Context**: 迭代交付。
*   **Strategy**: **"Separation of Fate" (命运分离)**。
    *   **Visuals (Designs/Prototypes)** -> **Archive** (Ephemeral).
    *   **Logics (Specs/Mermaid)** -> **Reality** (Truth).
*   **Step 3: Execution (Batch Merge)**
    *   **Action**: `mv assets/*.html` to `90_archive`; `merge spec.md` to `10_reality`.
    *   **[Side-Effect]**: 更新 `INDEX.md` 中的 "关键资产直达" 区块。

## 4. 缺陷处理 (Correction Stream)
*   **Context**: 生产环境报错或测试失败 (Red Flow)。
*   **Trigger**: **Bug Issue**。
*   **Flow**: 
    1.  **Trace**: AI 根据报错定位到 Code。
    2.  **Reverse**: AI 发现 Code 与 Spec 不一致，或 Spec 本身逻辑有误。
    3.  **Fix**: 先修 Spec (或补全 Spec)，再修 Code。
*   **Exceptions**: 允许 Hotfix跳过 `20_evolution`，但在 Commit 前必须补全 Spec (Post-Calibration)。

## 5. 治理 (Governance)
- **AI 也是用户**: AI 应像用户一样，主动维护 User Profile (如果被允许)。
- **Dashboard 是圣经**: AI 在每次对话结束后，都应自我反思："我更新 Dashboard 了吗？"
- **Gatekeeper (守门人)**: 
    -   **Context**: Commit 阶段的强制安检。
    -   **Rule**: `git push` 时，Gatekeeper 会检查：
        1.  **Traceability**: 本次修改的代码是否有对应的 Spec 依据？
        2.  **Consistency**: Spec 是否已更新以匹配 Code？
    -   **Verdict**: 只有校验通过，Code 才能入库。这是维持 SSOT 的最后一道防线。
