---
page_id: verification.static-coverage
slot: verification
template_kind: page_contract
status: pending_human_quality_review
---

# 静态覆盖账本模板

## 读者问题

在明确的静态分母内，哪些对象已映射、未映射、阻塞或不支持；统计为什么可信或为什么不能计算？

## 静态来源角色

Inventory/扫描声明、范围、Provider provenance 和映射记录建立覆盖事实；成功退出或空集合不等于完整
分母。

## 落地结构

### 1. 分母与范围

| Inventory kind | 范围 | Provider/方法 | 分母状态 | 不计算原因 |
| --- | --- | --- | --- | --- |

### 2. 逐项映射账本

| Inventory 项 | 类型/锚点 | 映射页面/claim | 映射状态 | provenance |
| --- | --- | --- | --- | --- |

### 3. 缺口、阻塞与统计限制

| 项目/范围 | 状态 | 原因 | 不能得出的统计结论 | 下一步 |
| --- | --- | --- | --- | --- |

### 4. 复核入口

说明审阅者如何回到 Provider、范围声明和 source-map；不把比例当内容质量。

## 完整正向示例

### 分母与范围

| Inventory kind | 范围 | Provider/方法 | 分母状态 | 不计算原因 |
| --- | --- | --- | --- | --- |
| 测试函数 | `tests/` | 测试文件清单 | complete | 不适用 |
| 服务类 | `src/` | 语法解析 Provider | blocked | Provider 不支持当前语言时不得报 0 |

### 逐项映射账本

| Inventory 项 | 类型/锚点 | 映射页面/claim | 映射状态 | provenance |
| --- | --- | --- | --- | --- |
| `tests/title.test.ts#rejects-empty-title` | 测试 | `verification/test-matrix.md` | mapped | 完整测试范围 |

### 缺口、阻塞与统计限制

| 项目/范围 | 状态 | 原因 | 不能得出的统计结论 | 下一步 |
| --- | --- | --- | --- | --- |
| 服务类 | blocked | Provider 语言不支持 | 不得计算服务类覆盖率 | 选择可声明能力的 Provider |

## 模板审阅项

- 分母、范围、Provider 和统计限制是否同时出现？
- blocked 是否不被伪装成零对象或低覆盖率？
- 映射账本是否可回到 source-map 和具体页面？
