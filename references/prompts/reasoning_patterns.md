# 结构化思维模式 (Reasoning Patterns)

在 Maglev 中，Prompt 不仅仅是命令，更是 **"思维的程序化"**。以下是我们在 Skill 中广泛使用的几种模式。

## 1. Chain of Thought (CoT Step-by-Step)

### **Pattern**
```markdown
Let's think step by step:
1. Analyze the user's request.
2. Identify the affected components.
3. Propose a plan.
4. Execute the plan.
```

### **Maglev Application**
- 显式体现在 **`thinking/`** 目录的强制性上。我们不让 AI 直接生成 `solutions/`，而是强制先生成 `thinking/`（即外显的 Chain of Thought）。

## 2. Role-Based Prompting (Persona)

### **Pattern**
```markdown
You are a [Role Name], an expert in [Field].
Your goal is to [Goal].
You must adhere to [Constraints].
```

### **Maglev Application**
- 我们的 `role_personas.md` 就是一个巨大的 Prompt 库。
- 当你需要 AI 扮演 Tech Pilot 时，不仅是给它个名字，而是给它注入**特定的关注点** (Feasibility, Code Quality, Security)。

## 3. ReAct (Reason + Act)

### **Pattern**
```markdown
Thought: I need to find the user's current directory.
Action: list_dir(cwd)
Observation: The directory contains ['src', 'README.md']
Thought: I see 'src', so this is a project root.
```

### **Maglev Application**
- 这是我们所有 `.agents/skills/` 的底层逻辑。
- Agent 不应该“猜测”，而应该“思考-行动-观察-再思考”。

## 4. Few-Shot Prompting (In-Context Learning)

### **Pattern**
```markdown
Example 1:
Input: Fix bug #123
Output: [Analysis] -> [Patch]

Example 2:
...

Now, handle this input:
```

### **Maglev Application**
- 在 `efficiency_matrix` 的 `spec_to_code` 环节，我们强烈建议用户提供 **"Reference Implementation"** 作为 One-Shot 或 Few-Shot 样本，以大幅提高生成代码的准确率。
