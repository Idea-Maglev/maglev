# Design

## 1. 变更清单

共 7 处变更，涉及 5 个文件：

| # | 文件 | 变更内容 | 对应需求 |
|---|------|----------|----------|
| A | entry-router `step-03-select-route.md` | 新增后段闭环路由路径 | §1 |
| B | knowledge-check `SKILL.md` | 新增「与 crystallization 的边界」段落 | §2 |
| C | crystallization `SKILL.md` | 新增「与 knowledge-check 的边界」段落 + 归档反模式警告 | §2, §3 |
| D | `private-catalog.yaml` | 补齐主流程关系链 4 条 + knowledge-check 时序 | §4 |
| E | entry-router `SKILL.md` | 集成列表中新增 knowledge-check 和 crystallization | §1 |

## 2. 变更 A：entry-router 路由表扩展

### 文件：`.agents/skills/entry-router/references/step-03-select-route.md`

在现有路由优先级列表末尾（`maglev-tutor` 之后）新增两条：

```
- 任务收尾、知识资产检查 -> `knowledge-check`
- 成果已验证、需写回现实并收口 -> `crystallization`
```

选择规则新增：

```
- `knowledge-check` 优先于 `crystallization`，除非用户明确要求写回 reality 或收口 active。
- `crystallization` 只在有已验证成果需要固化时进入。
- 若用户说"归档"且上下文不明确，先路由到 `knowledge-check`（安全默认）。
```

### 判断依据

| 用户意图信号 | 路由到 |
|------------|--------|
| "检查一下有没有遗漏" / "会话要切了" / "帮我看看记录" | knowledge-check |
| "功能做完了" / "写回 reality" / "收口 active" | crystallization |
| "归档"（无更多上下文） | knowledge-check（安全默认，检查完后可转交 crystallization） |
| "归档"（上下文含已验证的功能成果） | crystallization |

## 3. 变更 B：knowledge-check 边界声明

### 文件：`.agents/skills/knowledge-check/SKILL.md`

在「何时使用」之后新增段落：

```markdown
## 与 crystallization 的边界

这两个技能在"收尾"场景中容易混淆。区分标准：

| 维度 | knowledge-check | crystallization |
|------|----------------|-----------------|
| 核心动作 | 检查知识是否已记录 | 把已成立的结果写回 reality |
| 比喻 | "你保存了吗？" | "发布到生产环境" |
| 触发场景 | 会话切换、探索结束、任务收尾 | 功能验证通过、需要固化为项目事实 |
| 输出 | 缺口清单 + 补齐建议 | reality 回写 + active 收口 + 可发现性回填 |

### 典型触发意图

用这个技能：
- "帮我看看有没有什么还没记录的"
- "这轮讨论先到这里"
- "会话要切了，检查一下"

不用这个技能（用 crystallization）：
- "功能做完了，归档吧"
- "把结论写回 reality"
- "active 里的东西该收口了"

### 两者都需要时

先 knowledge-check（确认知识已保存）→ 再 crystallization（写回 reality + 收口 active）。
knowledge-check 完成后，若发现有需要固化的成果，应主动建议转交 crystallization。
```

## 4. 变更 C：crystallization 边界声明 + 反模式警告

### 文件：`.agents/skills/crystallization/SKILL.md`

#### 4a. 在「何时使用」之后新增边界段落：

```markdown
## 与 knowledge-check 的边界

| 维度 | crystallization | knowledge-check |
|------|----------------|-----------------|
| 核心动作 | 把已成立的结果写回 reality | 检查知识是否已记录 |
| 比喻 | "发布到生产环境" | "你保存了吗？" |
| 触发场景 | 功能验证通过、需要固化为项目事实 | 会话切换、探索结束、任务收尾 |
| 输出 | reality 回写 + active 收口 + 可发现性回填 | 缺口清单 + 补齐建议 |

### 典型触发意图

用这个技能：
- "功能做完了，帮我判断哪些该写回现实"
- "active 里的东西该收口了"
- "验证通过了，固化结果"

不用这个技能（用 knowledge-check）：
- "帮我看看有没有遗漏的知识资产"
- "会话要切了"
- "这轮讨论先到这里"

### 两者都需要时

先 knowledge-check → 再 crystallization。如果用户直接触发 crystallization 且未做过知识检查，应在开始前询问是否需要先运行 knowledge-check。
```

#### 4b. 在「判定纪律」段落新增归档反模式：

```markdown
### ⚠️ 归档反模式（禁止）

以下操作是被禁止的：

- ❌ 将 `20_evolution/active/` 下的内容直接搬运到 `90_archive/`
- ❌ 在未将结论写入 `10_reality` 的情况下执行归档
- ❌ 让 `90_archive` 成为理解当前项目状态的必读入口

正确的归档操作（三步）：

1. **提取结论** → 写入 `10_reality`（以"当前事实"的形式，不是"去看历史"）
2. **收口 active** → 在 `20_evolution/active/` 中标记状态（结束/继续/拆分）
3. **归档过程记录**（可选）→ 将历史推演、过程文档移入 `90_archive`

核心不变量：**只看 `10_reality` 就能了解项目当前状态。**
```

## 5. 变更 D：private-catalog 关系链补齐

### 文件：`.agents/private-catalog.yaml`

新增以下关系（补齐主流程链）：

```yaml
# spec-designer 新增：
relations:
  - target: 'requirement-convergence'
    type: 'called_by'
    direction: 'inbound'
    description: '需求边界稳定后，由需求收敛转入方案设计'
  - target: 'context-implementer'
    type: 'calls'
    direction: 'outbound'
    description: '方案设计完成后，转入上下文实施'

# context-implementer 新增：
relations:
  - target: 'spec-designer'
    type: 'called_by'
    direction: 'inbound'
    description: '方案设计完成后，由方案设计转入上下文实施'
  - target: 'integrated-validator'
    type: 'calls'
    direction: 'outbound'
    description: '实施完成后，转入综合验证'

# integrated-validator 新增：
relations:
  - target: 'context-implementer'
    type: 'called_by'
    direction: 'inbound'
    description: '实施完成后，由上下文实施转入综合验证'
  - target: 'crystallization'
    type: 'calls'
    direction: 'outbound'
    description: '验证通过后，转入现实结晶'

# knowledge-check 修改：
relations:
  - target: 'crystallization'
    type: 'precedes'
    direction: 'outbound'
    description: '知识沉淀检查完成后，若需写回 reality 和收口 active，转交 crystallization'
```

## 6. 变更 E：entry-router 集成列表

### 文件：`.agents/skills/entry-router/SKILL.md`

在「依赖与集成」列表中新增：
```
- `知识沉淀检查（knowledge-check）`
- `现实结晶（crystallization）`
```

## 7. 不做的事

- 不修改 crystallization 的 active END/CONTINUE/SPLIT 判定逻辑
- 不修改 knowledge-check 的扫描算法
- 不在此主题中处理 MEDIUM/LOW 级别的技能边界问题
- 不修改 `10_reality`、`20_evolution`、`90_archive` 的目录结构
