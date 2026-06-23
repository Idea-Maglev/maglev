# 技能扩展实施计划

## 🎯 目标
1. **新建** `maglev-cross-validate` - 全域交叉验证
2. **升级** `maglev-create-test-cases` - 现代化测试用例生成

---

## 📋 Part 1: maglev-cross-validate (新建)

### 概述
编排式技能，调用现有审计工具并内置轻量扫描器，完成 PRD ↔ Spec ↔ Code ↔ Tests 的一致性验证。

### 架构
```
maglev-cross-validate
├── Step 1: Collect Context
│   ├── 调用 maglev-audit-prd → PRD Context
│   ├── 调用 maglev-audit-spec → Spec Context
│   ├── 内置 Code Scanner → 扫描 API 实现
│   └── 内置 Test Scanner → 扫描测试文件
├── Step 2: Cross-Reference
│   ├── Layer 1: PRD ↔ Spec (US → API 追溯)
│   ├── Layer 2: Spec ↔ Code (API 定义 → 实现)
│   └── Layer 3: Spec ↔ Tests (AC → Test Case)
└── Step 3: Generate Report
    └── Unified Validation Report (健康度 + 问题清单)
```

### 文件结构
```
maglev-cross-validate/
├── SKILL.md
└── references/
    ├── cross-validate.workflow.md
    ├── step-01-collect-context.md
    ├── step-02-cross-reference.md
    └── step-03-generate-report.md
```

### Checkpoint 设计
- Step 1 后暂停：展示收集到的上下文统计
- Step 3 后暂停：展示验证报告，等待用户确认

---

## 📋 Part 2: maglev-create-test-cases (升级)

### 现状问题
| 问题 | 严重性 |
|------|--------|
| 包含过时的 `party-mode.workflow.md` | 🔴 高 |
| 缺少 Guided Mode (无 Checkpoint) | 🟡 中 |
| 未区分单测/集成测试/E2E | 🟡 中 |
| 输出未对齐 Spec 结构 | 🟡 中 |

### 升级内容
1. **删除** `party-mode.workflow.md` (BMAD 遗留)
2. **增加** Guided Mode (每步 Checkpoint)
3. **细化** 测试层级 (Unit / Integration / E2E)
4. **对齐** 输出结构到 `specs/{feature}/03_test_plan.md`

### 新步骤设计
| Step | 名称 | 说明 |
|------|------|------|
| 1 | Scope Analysis | 确定测试范围 (读取 PRD/Spec) |
| 2 | Strategy Design | 选择测试策略 (Unit/Int/E2E 比例) |
| 3 | Generate Cases | 按层级生成测试用例 |
| 4 | Coverage Check | 检查 AC 覆盖率 |
| 5 | Review | 用户审阅 + 输出 |

### 新输出结构
```
specs/{feature}/
└── 03_test_plan.md          <- 新增
    ├── 测试策略
    ├── 单元测试清单
    ├── 集成测试清单
    └── E2E 测试清单
```

---

## 🔧 执行计划

| 阶段 | 任务 | 优先级 |
|------|------|--------|
| **1** | 新建 `maglev-cross-validate` SKILL.md | 🔴 |
| **2** | 创建 cross-validate 步骤文件 | 🔴 |
| **3** | 清理 `create-test-cases` 遗留文件 | 🟡 |
| **4** | 升级 `create-test-cases` SKILL.md | 🟡 |
| **5** | 更新 `create-test-cases` 步骤文件 | 🟡 |
| **6** | 归档 + 更新 contribution_log | 🟢 |

---

> **[!IMPORTANT]**
> 两个技能有协同关系：`create-test-cases` 生成 `03_test_plan.md`，`cross-validate` 会读取它进行 Spec ↔ Test 验证。
