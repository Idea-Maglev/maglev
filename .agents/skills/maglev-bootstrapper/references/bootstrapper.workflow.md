---
name: bootstrapper
description: 执行 Maglev 初始化
output_folder: .
step_analyze: references/step-01-analyze.md
step_inject: references/step-02-inject.md
step_config: references/step-03-config.md
step_ai_context_check: references/step-04-ai-context-check.md
---

# Bootstrapper Workflow

**Goal**: 环境准备就绪 (Ready to Spec)。

## 流程 (Process)

### 1. Analyze (Step 01)
- 扫描根目录。
- 决策: `mode = GREENFIELD` (Empty) or `mode = ADOPTION` (Existing Files).

### 2. Inject (Step 02)
- 根据 `mode` 复制文件结构。
- **Source**: 当前仓库根目录下受治理的 `.agents/`、`.maglev/`、`docs/`、`specs/` 等资产，或正式 release 产物；不要再假设存在现役 `starter-kit/` 模板目录。
- 面向消费者项目时，只复制能力和规则；实例数据、Maglev 源仓库 Reality、仓库地图和当前事实必须保持空白。

### 3. Config (Step 03)
- 生成 `core_rules.md` (Context Injection).
- 只有用户确认登记仓库后，才设置受管仓库清单 `crosscutting/repository-map/repositories.md`。

### 4. AI Context Check (Step 04)
- 检查 `AGENTS.md` 与 `llms.txt` 是否达到最小可用标准。
- 若不足，输出结构化补齐建议。

## 初始化
1. 阅读 `references/step-01-analyze.md`。
