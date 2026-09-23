# AI 代理权翻转 (Agency Inversion): 从工具到管家

> **Context**: 用户指出 Maglev 当前虽有 AI 参与，但本质仍是 "人治"。如何让 AI 真正获得 "驱动力"？

## 1. 核心冲突 (The Conflict)

| 维度 | 旧 Maglev (v2.0) | AI-Native Maglev (Target) |
| :--- | :--- | :--- |
| **隐喻** | AI 是 **"强大的打字机"** | AI 是 **"项目的大管家"** |
| **驱动力** | Human Push ("去更新一下文档") | AI Pull ("检测到代码变更，我已更新文档，请确认") |
| **状态维护** | 人必须记得更新 Dashboard | AI 视为"强迫症"，自动维护一致性 |
| **最高准则** | "听人类的话" | "维护系统的熵减 (Entropy Reduction)" |

## 2. 什么是 "AI 驱动的思考能力"？

要让 AI "会思考"，必须在 System Prompt 中植入**"元目标 (Meta-Goal)"**。
AI 不应仅仅以 "完成 Prompt" 为目标，而应以 **"Maglev 系统健康"** 为最高目标。

### 定义 "Custodianship" (看守权)
AI 拥有对 `.maglev/` 与 `specs/` 目录的**看守权**。
*   **Rights**: 此时此刻，AI 有权指出人类的操作违规（"你直接改了代码但没改 Spec，这不行"）。
*   **Duties**: 每次会话结束，AI 必须整理当前 Evolution、更新 Dashboard，并维护 Spec 与 Code 的一致性。

## 3. 改造方案 (Transformation Plan)

### A. 宪法升级 (Constitutional Amendment)
在 `core_rules.md` 中注入主体性：
> *"你不是单纯的执行者，你是 Maglev 系统的守护者。你的首要任务是确保 Truth (Spec) 与 Reality (Code) 的一致性。当人类行为破坏了一致性时，你有责任介入。"

### B. 自动化副作用 (Automated Side-Effects)
将"文档维护"定义为所有操作的 Hidden Side-Effect：
*   用户说 "修好了 Bug"。
*   AI 思考：
    1. 通过需求收敛确认变更意图和验收信号。
    2. 在对应 Evolution Fast Track 或 Standard Track 中修改代码。
    3. 更新 Spec 状态并执行验证。
    4. 更新 Dashboard，必要时进入结晶。

## 4. 结论
这一转变的核心在于：**把"管理成本"从人类转移给 AI**。
人类只负责 **Intent (发号施令)** 和 **Audit (最终签字)**，中间所有的状态流转、文档对齐、看板维护，都是 AI 的**分内之事**。
