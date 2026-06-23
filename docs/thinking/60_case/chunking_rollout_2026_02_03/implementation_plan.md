# Smart Chunking Implementation Plan (智能分片实施计划)

## 1. 现状分析 (Analysis)
*   **Infrastructure**: `maglev-spec-crystallize` 已经支持动态文件拆分 (Regex: `<!-- FILE: (.*?) -->`)。
*   **Gap**: `maglev-spec-draft` 目前倾向于生成单体 `01_requirements.md`，导致大需求场景下 Token 溢出或信息丢失。

## 2. 核心策略 (Strategy)
在 `maglev-spec-draft` 的 Prompt 中引入 **"Module Partitioning Strategy" (模块分片策略)**。

### 规则定义
当满足以下任一条件时，强制触发分片：
1.  **Volume**: 预估内容超过 500 行。
2.  **Complexity**: 涉及 >2 个独立的业务领域 (Domain)。

### 输出范式
不再输出单一文件，而是输出文件簇：
*   `<!-- FILE: 01_requirements_core.md -->`
*   `<!-- FILE: 01_requirements_admin.md -->`
*   `<!-- FILE: 02_design_api.md -->`
*   `<!-- FILE: 02_design_worker.md -->`

### 索引更新
`00_index.md` 必须具备 **"Dynamic Discovery"** 能力，不能只硬编码链接 `01_requirements.md`，而是要遍历列出所有 modules。

## 3. 实施步骤
1.  **Update Prompt**: 修改 `maglev-spec-draft/references/step-02-polymorphic-design.md`。
    *   新增 `### 🌟 Smart Chunking` 章节。
    *   提供命名规范: `01_requirements_{module}.md`。
2.  **Verify**: 确保 `00_index.md` 的模板能引导 AI 索引这些新文件。

## 4. 示例
```markdown
<!-- FILE: 00_index.md -->
# Spec Index
*   [Core Requirements](01_requirements_core.md)
*   [Admin Requirements](01_requirements_admin.md)
```
