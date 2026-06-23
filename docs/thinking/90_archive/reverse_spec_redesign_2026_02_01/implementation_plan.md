# maglev-reverse-spec 技能重构计划

## 🎯 目标 (Goal)
将 `maglev-reverse-spec` 从一个"纯后端考古工具"升级为**页面驱动的全栈逆向引擎**，并恢复 BMAD 风格的强制检查点，确保用户在每个关键节点都有控制权。

---

## 🔥 核心问题 (Problems to Solve)
| # | 问题 | 根因 | 修复方案 |
|---|------|------|----------|
| 1 | 问目录而非功能模块 | 缺少项目功能地图 | 新增 "Feature Map" 步骤 |
| 2 | 只逆向后端 | 未追踪前后端调用链 | "Page-First" 策略 |
| 3 | 产物与 00-03 标准不对齐 | 输出模板过时 | 强制输出 00-03 结构 |
| 4 | Token 失控/无安全感 | 无强制暂停点 | "Guided Mode" (Checkpoints) |

---

## 🏛️ 新架构设计 (New Architecture)

### 核心策略：Page-First Full-Stack Reverse
```
[User Request] --> [Step 1: Project Map] --> [Step 2: Page Analysis]
                          |                         |
                          v                         v
                   (识别技术栈/入口)          (选择页面/功能)
                                                    |
                                                    v
                                      [Step 3: Stack Trace]
                                                    |
                             (追踪 Page -> API -> Service -> DB)
                                                    |
                                                    v
                                      [Step 4: Spec Synthesis]
                                                    |
                              (输出 00_index + 01_req + 02_design)
                                                    |
                                                    v
                                     [Step 5: User Review] --> [WAIT]
```

### 执行模式 (Execution Mode)
*   **Guided Mode (Default)**: 每个 Step 结束后强制暂停，展示阶段性产物，等待用户确认。
*   **Turbo Mode (Opt-in)**: 用户可显式触发全自动模式，跳过中间确认。

---

## 🌐 多技术栈支持 (Multi-Tech-Stack Support)

### 问题
当前设计中的示例主要以 Java/Vue 为主。实际项目可能是：
*   **Backend**: Java, Python, Go, Node.js, Rust
*   **Frontend**: Vue, React, Angular, Svelte, 原生 HTML/JS

### 解决方案：Tech Stack Adapter Pattern
将 Stack Trace (Step 3) 的核心逻辑抽象为**适配器接口**，每个技术栈实现自己的"追踪器"。

```
                    [Core Reverse Engine]
                           |
          +----------------+----------------+
          |                |                |
    [Java Adapter]   [Python Adapter]  [Node Adapter]
          |                |                |
    - 识别 Controller  - 识别 Flask/FastAPI - 识别 Express Route
    - 追踪 @Service    - 追踪 def handler  - 追踪 async function
    - 解析 JPA Entity  - 解析 SQLAlchemy   - 解析 Prisma/Mongoose
```

### 适配器识别逻辑 (Auto-Detection)
在 Step 1 (Project Map) 中，根据以下特征自动选择适配器：
| 检测文件 | 技术栈 | Adapter |
|----------|--------|---------|
| `pom.xml` / `build.gradle` | Java (Spring) | `java-spring` |
| `requirements.txt` / `pyproject.toml` | Python | `python-fastapi` / `python-flask` |
| `package.json` (with express/nestjs) | Node.js | `node-express` / `node-nest` |
| `go.mod` | Go | `go-gin` / `go-echo` |
| `Cargo.toml` | Rust | `rust-actix` |

### 扩展策略
1.  **Phase 1 (Now)**: 内置 Java + Vue/React + Node 适配器。
2.  **Phase 2 (Later)**: 开放 Adapter 接口，允许用户自定义 `references/adapters/{stack}.md`。

## 📋 详细步骤设计 (Step Definitions)

### Step 1: Project Map (项目地图)
**目标**: 宏观理解项目结构，识别用户可感知的功能入口。
**动作**:
1.  扫描 `package.json`/`pom.xml`/`go.mod` 识别技术栈。
2.  扫描前端入口 (`src/pages/`, `src/views/`, `routes/`) 列出所有页面。
3.  扫描后端入口 (`src/main/`, `app/`) 列出核心服务/Controller。
4.  生成 **Feature Map** (JSON/Markdown)，列出可逆向的"功能单元"。

**Checkpoint**:
> "项目扫描完成。识别到以下功能入口：
> [ ] 用户登录 (LoginPage.vue + AuthController.java)
> [ ] 订单列表 (OrderList.vue + OrderService.java)
> ...
> 请选择一个开始逆向，或输入 'all' 逐个处理。"

---

### Step 2: Page Analysis (页面分析)
**目标**: 深入分析选定页面的 UI 结构和交互逻辑。
**动作**:
1.  读取页面文件 (`.vue`, `.tsx`, `.html`)。
2.  提取组件结构、Props/State。
3.  识别 API 调用 (`axios.get('/api/orders')`)。

**Checkpoint**:
> "页面分析完成: `OrderList.vue`。
> - 组件: OrderTable, Pagination, FilterBar
> - API 调用: `GET /api/orders`, `DELETE /api/orders/{id}`
> 是否继续追踪后端？[Y/n]"

---

### Step 3: Stack Trace (全栈追踪)
**目标**: 从 API 入口追踪到 Service、Repository 和 Database。
**动作**:
1.  根据 Step 2 识别的 API，定位后端 Controller/Handler。
2.  追踪 Service 层调用链。
3.  记录数据库表/实体映射。

**Checkpoint**:
> "后端追踪完成。
> - Controller: `OrderController.java`
> - Service: `OrderServiceImpl.java`
> - Repository: `OrderRepository.java`
> - Entities: `Order`, `OrderItem`
> 是否继续生成 Spec？[Y/n]"

---

### Step 4: Spec Synthesis (规格合成)
**目标**: 将前后端分析结果合成为标准 Spec 文件簇。
**输出结构** (对齐 00-03 标准):
```
specs/10_reality/reverse_{feature_slug}/
├── 00_index.md          <- title, status, slug, source_files
├── 01_requirements.md   <- 还原的业务需求 (User Story 形式)
├── 02_design.md         <- 技术设计 (API Contracts, Data Model)
└── 03_plan.md           <- [空或TBD] 逆向不涉及任务规划
```

**Checkpoint**:
> "Spec 草稿已生成。请审阅：
> - `00_index.md`: [View Link]
> - `01_requirements.md`: [View Link]
> - `02_design.md`: [View Link]
> 确认无误后，输入 'confirm' 写入文件系统。"

---

### Step 5: User Review & Commit (用户审阅与提交)
**目标**: 等待用户确认后，持久化文件并触发 Librarian 索引。
**动作**:
1.  将 Spec 文件写入 `specs/10_reality/...`。
2.  调用 `maglev-librarian` 更新 `specs/README.md`。
3.  (可选) 调用 `maglev-audit-spec` 进行质量检查。

---

## 🛠️ 执行计划 (Execution Plan)
| 阶段 | 任务 | 产出 |
|------|------|------|
| **1** | 重写 `SKILL.md` | 新入口定义 |
| **2** | 创建 Steps 1-5 参考文件 | `references/step-*.md` |
| **3** | 更新输出模板 | `templates/reverse_output/` |
| **4** | 更新上游调用者 | `maglev-legacy-adopter` |
| **5** | 更新文档 | `legacy_project_adoption.md` |

---

> **[!IMPORTANT]**
> 此次重构的核心原则是 **"用户在每一步都有发言权"**。我们不追求一键自动化，而追求**可控的渐进式逆向**。
