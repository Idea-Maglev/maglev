---
name: 'step-02-context-gathering'
description: '直接模式的快速上下文收集 - 识别文件、模式、依赖项'

workflow_path: '{project-root}/_bmad/bmm/workflows/bmad-quick-flow/quick-dev'
thisStepFile: './step-02-context-gathering.md'
nextStepFile: './step-03-execute.md'
---

# 步骤 2: 上下文收集 (直接模式)

**目标：** 快速收集直接指令的上下文 - 文件、模式、依赖项。

**注意：** 此步骤仅在模式 B (直接指令) 下运行。如果 `{execution_mode}` 是 "tech-spec"，此步骤被跳过。

---

## 可用状态

来自 step-01:

- `{baseline_commit}` - 工作流开始时的 Git HEAD
- `{execution_mode}` - 应该是 "direct"
- `{project_context}` - 如果存在则加载

---

## 执行序列

### 0. 依赖图解析（当 tech-spec 模式且 03_plan.md 含依赖图时）

如果 `{execution_mode}` 是 "tech-spec" 且 03_plan.md 包含「任务依赖」区段（Mermaid flowchart）：

1. 解析 Mermaid flowchart，提取任务节点（T1, T2...）和依赖边（T1 → T2）
2. 按拓扑排序确定执行顺序
3. 标记可并行任务组（入度相同、无互相依赖的任务集合）
4. 将排序后的执行序列作为 `{task_execution_order}` 传递给 step-03

如果 03_plan.md 不包含依赖图：
- 保持当前行为——按列表顺序构建执行序列

### 1. 识别要修改的文件

根据用户的直接指令：

- 使用 glob/grep 搜索相关文件
- 识别需要更改的具体文件
- 注意文件位置和用途

### 2. 查找相关模式

检查识别的文件及其周围环境：

- 使用的代码风格和惯例
- 类似功能的现有模式
- 导入/导出模式
- 错误处理方法
- 测试模式（如果附近存在测试）

### 3. 注意依赖项

识别：

- 使用的外部库
- 内部模块依赖项
- 可能需要更新的配置文件
- 可能受影响的相关文件

### 4. 创建心理计划

将收集的上下文合成为：

- 要完成的任务列表
- 验收标准（从用户请求推断）
- 操作顺序
- 要触摸的文件

---

## 呈现计划

向用户显示：

```
**上下文已收集：**

**要修改的文件：**
- {list files}

**识别的模式：**
- {key patterns}

**计划：**
1. {task 1}
2. {task 2}
...

**推断的 AC：**
- {acceptance criteria}

准备好执行了吗？(y/n/adjust)
```

- **y:** 继续执行
- **n:** 收集更多上下文或澄清
- **adjust:** 根据反馈修改计划

---

## 下一步指令

**关键：** 当用户确认准备就绪时，明确说明：

- **y:** "**下一步:** 完整阅读并遵循：`step-03-execute.md`"
- **n/adjust:** 继续收集上下文，然后重新呈现计划

---

## 成功指标

- 识别出要修改的文件
- 记录相关模式
- 注意依赖项
- 创建带有任务和 AC 的心理计划
- 用户确认准备继续

## 失败模式

- 当模式 A (tech-spec) 时执行此步骤
- 在未识别要修改的文件的情况下继续
- 未呈现计划供用户确认
- 错过现有代码中的明显模式
