# Maglev Kickoff: The "Evolution, Not Revolution" Deck
> **Target Audience**: Traditional Development Team (Change-averse, sturdy, skeptical of AI).
> **Goal**: 降低抵触情绪，建立心理安全感，达成"试一试"的共识。
> **Tone**: 务实 (Pragmatic)、尊重 (Respectful)、演进 (Evolutionary).

## Slide 1: The Reality Check (我们面临的真实痛点)
*   **The Hook**: "大家最近加班多吗？"
*   **The Facts**:
    *   **需求不讲理**: "PRD 只有一句话，做出来说不对。"
    *   **维护噩梦**: "改一个 Bug，崩了三个旧功能。"
    *   **机械劳动**: "每天都在写 CRUD，写转换层，写 Getter/Setter，这是我们作为工程师的价值吗？"
*   **Message**: 我们不是为了"赶时髦"引入 AI，我们是为了**"这种日子我不想再过了"**。

## Slide 2: What is Maglev? (它不是什么，是什么)
*   **它不是**:
    *   ❌ 替代你的 AI 裁员机器。
    *   ❌ 一个需要你从头学习的全新语言。
    *   ❌ 一个只会写 Hello World 的玩具。
*   **它是**:
    *   ✅ **一个永远不喊累的"初级程序员"**：你把逻辑讲清楚 (Spec)，它负责敲代码。
    *   ✅ **一个极度严格的"QA 检察官"**：它会并在 CI 阶段拦住所有文档和代码不一致的提交。
    *   ✅ **你的"外骨骼"**：你依然是核心，穿上它，你一个人就是一支队伍。

## Slide 3: The New Deal (新的工作契约)
我们现有的工作方式 vs Maglev 方式：

| 维度 | 以前 (Traditional) | 以后 (Maglev) | 你的收益 |
| :--- | :--- | :--- | :--- |
| **代码 (Coding)** | 手写每一行 Loop, If-Else | AI 生成 90% | **告别腱鞘炎**，聚焦核心逻辑。 |
| **文档 (Docs)** | 没人写 / 写了也没人看 / 它是死的 | **Doc is Code**. 没文档就不准提交代码 | **再也不用猜**前任留下的坑了。 |
| **调试 (Debug)** | 漫无目的的 Log 排查 | AI 对照 Spec 进行三角验证 | **秒级定位**，喝茶时间多一点。 |

## Slide 4: Respect Legacy (我们如何对待现在的代码)
*   **Concern**: "我们的老代码很复杂，AI 懂个屁。"
*   **Answer**: "Exactly. 所以我们不动它。"
*   **Strategy**:
    1.  **不推倒重来**: 所有的 Old Code 都是资产。
    2.  **逆向学习**: 我们会让 AI 先去"读"你们的代码，生成文档（Reverse Engineering）。
    3.  **增量开发**: 只有**新功能**才用新模式。旧代码维持原状，或者被"冻结"为 API 供新代码调用。

## Slide 5: The "Gatekeeper" (为什么这很安全)
*   **Safety Net**: 最终的 `git push` 权限依然在**你们**手里。
*   **Review Shift**:
    *   以前：你要 Review 实习生写的烂代码。
    *   现在：你要 Review AI 写的代码。
*   **Rule**: 只要你觉得 AI 写得不对，**拒绝它，或者修改它**。你永远拥有"一票否决权"。

## Slide 6: Pilot Plan (先试两周，不行就撤)
*   **Scope**: 选取一个**非核心、边缘**的小模块（比如"后台报表"或"工具类"）。
*   **Team**: 只要 1 个产品经理 + 1 个技术骨干（志愿者）。
*   **Commitment**: 给我们两周时间。
    *   如果效率没提升 -> 我们回滚，当作无事发生。
    *   如果爽到了 -> 我们再讨论下一步。

## Slide 7: Q&A (开诚布公)
*   "学会这套东西要多久？" (Answer: 半天。主要是学怎么写好 Prompt/Spec。)
*   "我的 IDE 支持吗？" (Answer: 支持 Cursor/vscode，不强制换 IDE。)
*   "AI 泄露代码怎么办？" (Answer: 我们使用企业级 API / 这是内网部署... *根据实际情况作答*)

---
**核心话术 (Key Takeaway)**:
"Maglev 不会取代工程师。**会使用 Maglev 的工程师，将取代只懂手写代码的工程师。** 让我们一起做前者。"
