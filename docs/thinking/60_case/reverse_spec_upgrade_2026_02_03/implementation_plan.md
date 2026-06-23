# Reverse Spec Upgrade: Interactive Deep Scan (逆向工程升级)

## 1. 核心问题 (Problem Statement)
*   **浅层索引 (Shallow Indexing)**: 当前仅扫描 `src/views` 或 `Controller`，容易遗漏深层目录或动态路由。
*   **Token 爆炸风险**: 缺乏"嗅探"机制，一旦全量扫描大项目必炸 Token。
*   **重复造轮子**: 自行生成 Spec 模板，未能复用 `maglev-create-spec` 的高质量生成逻辑。

## 2. 升级策略 (Upgrade Strategy)

### A. Phase 1: Interactive Scanner (交互式扫描器)
*   **Step**: `step-01-project-map.md`
*   **Changes**:
    1.  **Survey Mode (测绘模式)**: 先只读目录树 (Depth=2)，不读文件内容。
    2.  **Repo Stats**: 报告 "Found 200 files in `src/pages`".
    3.  **User Choice (关键交互)**:
        > "⚠️ `src/pages` 包含 200 个文件，可能导致 Token 溢出。
        >
        > 请选择策略:
        > - **[S]mart Sample**: 仅分析 `router/index.js` 来推断页面结构。(推荐)
        > - **[D]eep Scan**: 强制扫描该目录下的所有文件。(高消耗)
        > - **[M]anual**: 我来指定核心入口文件。"

### B. Phase 2: Spec Pipeline Reuse (管线复用)
*   **Step**: `step-04-spec-synthesis.md`
*   **Changes**:
    *   **Abandon**: 废弃手动凭借字符串生成 Markdown 的逻辑。
    *   **Admit**: 将逆向得到的信息整理为标准 `input_facts.md` 和 `ingest_context.json`。
        *   `intent`: "Reverse Engineer Feature X"
        *   `project_type`: "Legacy Conversion"
    *   **Delegate**: 调用 `maglev-spec-draft` 技能来生成最终文档。
        *   这样能自动享受到 **Smart Chunking**, **Three-Zone Architecture**, **Backend Bias Fix** 等所有最新特性。

### C. Deep Router Analysis (深度路由分析)
*   **Step**: 新增 `step-01b-router-analysis.md` (Optional)
*   **Logic**:
    *   如果是前端项目，专门读取 `router/index.js` 或 `routes.ts`。
    *   解析 Import 语句，建立 `Path -> File` 映射，比单纯扫文件及目录更准确。

## 3. 实施计划 (Execution Plan)

- [ ] **Step 1 Upgrade**: 实现 "Survey -> Ask -> Scan" 交互逻辑。
- [ ] **Router Analysis**: 增加对 Router 文件的专门解析能力。
- [ ] **Pipeline Rewiring**: 改造 Step 4，使其输出中间态 Context，并 Link 到 `maglev-spec-draft`。
