# Skill Safety & Usability Analysis (Red Team)

## 1. `reverse_engineer_guide` (Software Archaeologist)

### 🔴 Risk A: Context Explosion (爆内存)
- **Problem**: 现在的 Skill 试图通过 "Deep Scan" 读取遗留代码。如果用户指向一个包含 50 个文件的 `src/legacy/` 目录，AI 会尝试将它们全部读入 Context，导致 Token 溢出或“忘头顾尾”。
- **Real World Failure**: 用户说 "逆向这个库"，AI 读了前 10 个文件，然后开始胡编乱造后面 40 个文件的逻辑。
- **Mitigation**:
    - **强制原子化**: Skill 必须拒绝处理目录。只能接受 **单一文件** 或 **< 5 个文件** 的列表。
    - **指令修正**: *"I can only process one key file at a time. Please point me to the Entry Point."*

### 🔴 Risk B: State Loss (存档丢失)
- **Problem**: "Resume Mode" 依赖于 AI 主动去读旧的 Markdown Frontmatter。如果 AI 在长对话中忘记了这个步骤，它就会覆盖掉之前的进度。
- **Real World Failure**: 分析了 3 天的文档，因为一次不小心的 `Overwrite`，导致之前的 `coverage` 记录被清空。
- **Mitigation**:
    - **Append-Only Strategy**: 除非用户明确要求，否则永远只追加不覆盖。

## 2. `contribute_methodology` (Methodology Architect)

### 🔴 Risk C: Over-Engineering (过度设计)
- **Problem**: 强制执行 "Thinking -> Solution" 流程。但用户有时只是想补一句 "Commit Message 规范"。
- **Real World Failure**: 用户想改个错别字，Skill 非要他先写一篇 `thinking/typo_analysis.md`。这会把用户逼疯。
- **Mitigation**:
    - **Fast Track**: 引入 "Hotfix" 模式。如果变更 < 50 字或只是修 Bug，跳过 Thinking 步骤。

### 🔴 Risk D: Path Hell (路径地狱)
- **Problem**: "Target Directory" 的概念对 AI 来说很模糊。用户说 "这里"，AI 认为是 Root，实际是 `/src/feature`。
- **Real World Failure**: 文档被建得到处都是，`thinking/` 文件夹遍地开花，难以管理。
- **Mitigation**:
    - **Confirmation Dialog**: 在写文件前，**必须**输出绝对路径供用户确认。
    - **Centralized Fallback**: 如果不知道放哪，统一扔到 `.archive/` 待整理。

## 3. General Issues

### 🔴 Risk E: Skill Collision (技能冲突)
- **Problem**: `structure_thinking` (Thinking Partner) 和 `contribute_methodology` (Methodology Architect) 极其相似。
- **Real World Failure**: 用户说 "帮我设计个方案"，两个 Agent 打架，或者 AI 随机选一个。
- **Mitigation**:
    - **Merge**: 应该将二者合并。一个是“通用思考”，一个是“特定产出”，本质是一样的。建议合并为 `structured_creator`。

---

## 4. Action Plan
1.  **Merge**: 合并 `structure_thinking` 和 `contribute_methodology`，减少认知负担。
2.  **Example Fix**: 在 Skill 定义中明确 "One file at a time" 的输入限制。
3.  **Fast Path**: 在工作流中增加 "Is this a complex change?" 的判断分支。
