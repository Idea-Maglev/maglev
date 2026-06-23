# Atomic Spec Generation Architecture (原子化 Spec 生成架构)

> **Context**: User 提议将 Spec 生成过程拆解为原子能力，由主技能协调。
> **Goal**: 详细定义 `Ingest` -> `Draft` -> `Crystallize` 三个原子技能的职责边界与输入输出。

## 1. 架构总览 (Architecture Overview)

```mermaid
graph TD
    User[用户输入] --> Coord[Coordinator: maglev-quick-spec]
    
    subgraph "Phase 1: 感知"
    Coord --> S1[Skill: spec-ingest]
    S1 --> Context[Raw Context (JSON)]
    end
    
    subgraph "Phase 2: 思考"
    Coord --> S2[Skill: spec-draft]
    Context --> S2
    S2 --> Draft[Unified Draft (Markdown)]
    end
    
    subgraph "Phase 3: 行动"
    Coord --> S3[Skill: spec-crystallize]
    Draft --> S3
    S3 --> Artifacts[Spec Cluster (Files)]
    end
```

## 2. 原子技能定义 (Atomic Skill Definitions)

### Skill 1: `spec-ingest` (摄入者)
> **Motto**: "我不生产信息，我只是信息的搬运工和清洗工。"

*   **核心职责**:
    1.  **识别源头**: 判断用户给的是 Idea、Doc 文件还是 Legacy 代码目录。
    2.  **标准化**: 将异构输入转化为统一的 JSON 格式。
    3.  **取证 (Fact Extraction)**: 将分析结果固化为 Markdown，作为 Spec 的 "输入事实" (Input Facts)。

*   **输入 (Input)**:
    *   `source_type`: "idea" | "doc" | "legacy"
    *   `content`: 文本串 或 文件路径

*   **Deep Dive: Legacy Noise Reduction (降噪逻辑)**
    针对 "存量项目" (Type 3)，为了避免污染下文，Ingest Skill 执行三层过滤：
    1.  **Map (制图)**: 仅使用 `list_dir` 获取文件列表，过滤掉 `test/`, `mock/`, `node_modules/` 等噪音目录。
    2.  **Skeleton (画骨)**: 对于业务代码，不读取全文。而是使用 `view_file_outline` 提取 Class/Function 签名 (Signature)。*Code (1000 lines) -> Signature (50 lines)*。
    3.  **Schema (取数)**: 仅针对 Data Model 文件读取全文，或使用 `grep` 提取 SQL DDL/ORM 定义。
    *结果*: 下游技能只看到 "系统长什么样 (Interface)" 和 "数据存什么 (Schema)"，看不到具体的 "IF/ELSE 逻辑"。

*   **输出 (Output)**: 
    1.  `ingest_context.json` (Transient for Draft)
    2.  **`context/input_facts.md`** (Persistent Artifact): 
        *   **本质**: "事实的摘要与名录" (Catalog & Summary of Reality)。
        *   **内容**: 涉及到的文件列表、关键接口定义、相关 PRD 的摘要。
        *   *用途*: 这是 Spec 的 "前提" (Premise)。如果 Premise 变了 (如代码变了)，Spec 就需要重算。

### Skill 2: `spec-draft` (起草者)
> **Motto**: "我是多态的建筑师。给我意图，还你蓝图。"

*   **核心职责**:
    1.  **结构化**: 根据 `standard_spec_structure.md` 填充内容。
    2.  **多态适配 (Polymorphism)**:
        *   若 `project_type=frontend` -> 生成 UI Interaction Table。
        *   若 `project_type=backend` -> 生成 API Swagger & ERD。
    3.  **逻辑补全**: 基于 `ingest_context` 中的 Legacy 引用，自动推导代码变更点。

*   **输入 (Input)**:
    *   `ingest_context.json`
    *   `project_type`: "frontend" | "backend" | "agent"

*   **输出 (Output)**: `draft_unified.md` (包含 00, 01, 02, 03 四部分的单一草稿文件)

### Skill 3: `spec-crystallize` (固化者)
> **Motto**: "我不做设计，我只负责刻碑。"

*   **核心职责**:
    1.  **物理拆分**: 将 `draft_unified.md` 拆解为 `00_index`, `01_req`...
    2.  **事实固化**: 将 `context/input_facts.md` 存入 `specs/.../{slug}/context/` 目录。
    3.  **资产链接**: 对 `assets/` 目录下的图片/文件进行哈希重命名和链接修正。
    4.  **副作用管理**:
        *   调用 Librarian 更新 `README.md`。
        *   更新 `task.md` (如果 Spec 里有 Plan)。
        *   Git Commit (可选)。

*   **输入 (Input)**:
    *   `draft_unified.md`
    *   `input_facts.md` (from Ingest)
    *   `target_directory`

*   **输出 (Output)**: 
    *   File System Changes (Spec Cluster + Context Snapshot)
    *   Report: "Spec Created at {path}"

## 3. 优势分析 (Why This Works)

1.  **复杂性隔离**: `spec-ingest` 专门处理“脏活”（读乱七八糟的老代码），保证传给 `spec-draft` 的数据是干净的 JSON。
2.  **可测试性**: 我们可以单独测试 `spec-draft` 的生成质量，而不需要每次都去扫描代码。
3.  **人类介入点 (HIL)**: 用户可以在 Phase 2 (Draft) 结束时介入，直接修改 Markdown 草稿，然后再让 `spec-crystallize` 去拆分。这比修改 JSON 方便得多。
