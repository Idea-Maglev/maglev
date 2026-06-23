# 经验沉淀：组件级需求拆解 vs Maglev 特性级原子

> **发现日期**: 2026-04-21
> **触发场景**: v2.15 Cover Page 特性归档审查
> **关联路径**: `specs/20_evolution/active/v2.15-feat-cover-page/01-fields/workflow-zx/`

---

## 一、现象描述

在 v2.15-feat-cover-page 的实施过程中，执行者（赵轩 @zoey.zhao3）在 `01-fields/` 子特性目录下创建了深层嵌套的个人工作区：

```
01-fields/workflow-zx/
├── backup/           ← 历史方案备份（6 文件, ~2,155 行）
├── context/          ← 字段规则 CSV + 可见性映射
└── component-cards/  ← 组件设计卡片
    ├── README.md          ← 索引 + 推荐阅读顺序
    ├── cover-page/        ← CoverPageGenerator 设计 + 实现方案
    ├── sub-tables/        ← 5 个子表组件卡片 + overview + 执行顺序
    └── assets/            ← UI 截图
```

**量化指标**：

| 维度 | 数值 |
|------|------|
| `workflow-zx/` 专属文件 | 30 个 |
| 组件设计卡片 | 6 张 |
| 目录最大嵌套层级 | 8 层 |
| 整个 feat 目录总文件 | 106 个 |
| 总 Markdown 行数（不含 ref/） | 30,067 行 |

---

## 二、行为动机分析

### 1. 降低认知负荷

Cover Page 是 v2.15 最复杂的前端特性——两张 1:N 子表（收益明细 / 费用分摊）、复合级联选择器、跨表数据复制、PDF 生成。将每个组件拆为独立卡片，是执行者在 **管理自身复杂度** 的自然策略。

### 2. AI 协作的上下文投喂

`context/`（字段可见性规则 CSV + 字段表）和 `backup/`（历史方案迭代）本质上是 **给 AI 准备的喂料区**。执行者在用目录结构替代记忆，确保每次对话都能快速定位上下文。

### 3. 个人进度看板替代

`00_implementation_order.md` 含可勾选步骤清单（Phase 0-6），组件卡片标注状态（Draft / In Progress）——这是在缺少项目管理工具时，用文件系统自建的 **个人看板**。

---

## 三、双视角对比

### Maglev 框架治理视角

| 维度 | Maglev 标准 | 实际做法 | 评价 |
|------|-------------|---------|------|
| **Spec 粒度** | `active/feat_xxx/` 是原子单元，内含 `00_prd → 04_api_spec` 扁平文件 | 7 个子目录 × 多层嵌套，每层都有完整 Spec 套件 | ⚠️ 过度细分。Maglev 的 feat 是业务特性级，不是组件级 |
| **个人命名空间** | 无此概念。Spec 属于项目，不属于个人 | `workflow-zx/` 是个人空间 | ❌ 违反协议。仓库不应有个人命名空间 |
| **backup 目录** | 不存在。历史通过 Git 管理 | 6 个 backup 文件共 ~2,155 行 | ❌ 反模式。Git 就是版本管理工具 |
| **组件设计卡片** | 无此机制。技术细节走 `02_design` 或 `03_tech_spec` | 6 张独立卡片 + overview + impl order | ⚠️ 自创机制。有价值但偏离标准 |
| **进度跟踪** | `board.md` (project-board) + Dashboard | 自建 implementation_order + 卡片状态字段 | ⚠️ 重复造轮 |
| **上下文数据** | `10_reality/` 存放已交付事实 | `workflow-zx/context/` 存半持久上下文 | ⚠️ 位置错误 |

### 执行者日常开发视角

| 维度 | 实际得到的 | Maglev 能提供但未使用的 | 差距原因 |
|------|-----------|----------------------|---------|
| **上下文持久化** | component-cards 让 AI 快速理解组件边界 | `10_reality/` + `repository_map.md` | 不确定 10_reality 在交付前能否写入 |
| **进度跟踪** | implementation_order checkbox | `project-board` skill + `status.md` | skill 在 v0.3.2 才引入，当时不可用 |
| **方案迭代** | backup/ 保留所有历史方案 | Git history + `90_archive/` | 操作习惯——本地文件比 `git log` 更直觉 |
| **AI 喂料** | context/ 存放字段规则 CSV | Maglev 无显式的「AI 上下文喂料区」 | **框架缺口**——合理需求但未覆盖 |
| **复杂组件分解** | 每组件一张卡片，接口/数据流/截图齐全 | `03_tech_spec` 可承载 | 当 tech_spec 超 700 行时拆分是合理的 |

---

## 四、核心矛盾

> **Maglev 以 feature 为原子，执行者以 component 为原子。**

当一个 feature 涉及 6+ 个复杂 UI 组件时，单文件 `03_tech_spec_frontend.md` 会膨胀到不可维护（本例 737 行还不含组件细节）。执行者自然会创造 sub-document 机制，但因为没有标准约束，就产生了个人命名空间 + 深层嵌套。

---

## 五、对 Maglev 框架的改进建议

### 建议 1：引入「Tech Spec 子文档」约定

当 `03_tech_spec` 超过 500 行或涉及 3+ 个独立组件时，允许拆分为子文档：

```
active/feat_xxx/
├── 03_tech_spec_frontend.md           ← 主文档（概览 + 数据流）
└── 03_tech_spec_frontend/
    ├── component_revenue_details.md   ← 子文档
    ├── component_cost_allocation.md
    └── component_cascader_cell.md
```

**约束**：子文档目录名必须与主文档同名，路径可被 AI 自动发现。

### 建议 2：明确「AI 上下文数据区」 ✅ 已完成

> 对应 spec: `specs/90_archive/ai_context_data_area/`

在 `active/feat_xxx/` 下标准化一个 `context/` 子目录：

```
active/feat_xxx/
├── context/         ← 半结构化上下文（CSV, 字段映射, 截图）
│   └── 随 feat 归档时一同进入 90_archive
└── ...
```

**区别**：
- `ref/` = 外部参考资料（PRD 原稿、设计图）
- `context/` = 项目内在上下文（字段规则、代码映射、状态表）

### 建议 3：禁止个人命名空间 + backup ⏳ 部分落地

> "禁止 backup/"规则已写入 `collaboration.md` §3。
> "禁止个人命名空间"尚未写入 `specs_lifecycle.md`，待后续治理迭代。

在 `specs_lifecycle.md` 中显式声明：

> `20_evolution/active/` 下不允许以人名（如 `workflow-zx/`、`notes-john/`）命名的目录。
> 不允许 `backup/` 目录——版本管理由 Git 负责。

---

## 六、对执行者的建议

1. **组件卡片的价值应被提炼**——数据流图、接口定义质量很高，应重构为 `03_tech_spec_frontend/` 子文档或 `10_reality` 前端设计文档，而非留在私人角落。

2. **backup 文件应清理**——2,155 行备份让目录臃肿且困惑。确认 Git 历史完整后删除。

3. **context/ 的有效内容上提**——字段可见性规则和字段表是项目级知识，应属于 `10_reality/01_vehicle_programs/frontend/` 或 spec 顶层 `context/`。

4. **善用 project-board**——v0.3.2 引入的 `board.md` + `status.md` 已可替代自建的 implementation_order。

---

## 七、一句话总结

> 执行者用目录结构弥补了 Maglev 在「组件级拆解」和「AI 上下文管理」上的机制缺口，产出质量高但路径偏离标准。核心矛盾是框架以 feature 为原子而执行者以 component 为原子——这是 Maglev 应该正视的粒度适配问题。
