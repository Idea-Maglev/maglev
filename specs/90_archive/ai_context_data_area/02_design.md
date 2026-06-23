# 技术设计：AI 上下文数据区

## 1. 现状分析

### 已有机制
- spec-pipeline crystallize 阶段（`step-01-split-files.md`）已自动创建 `context/` 并放入 `input_facts.md`
- crystallization 归档时 `mv` 整个 spec 目录，context/ 自动跟随
- project-board 扫描时不检查 context/ 内容（仅检查 00-03 标准文件）

### 缺口
- `context/` 仅被定义为存放 `input_facts.md`，未扩展为通用 AI 上下文数据区
- 无文档区分 `context/` 与 `ref/` 的边界
- 执行者不知道此目录可以存放更多数据

## 2. 设计决策

| # | 决策点 | 选择 | 理由 |
|---|--------|------|------|
| D-1 | context/ 路径 | `active/feat_xxx/context/`（spec 内部） | 已有机制，零路径改动 |
| D-2 | 与 ref/ 的区分 | ref/ = 外部不可变引用；context/ = 项目内在可演化上下文 | 来自反模式文档分析 |
| D-3 | 归档策略 | 全量随 spec 归档，不脱敏不精简 | 上下文是 spec 可复现性的一部分 |
| D-4 | 文件格式约束 | 不限格式（md/csv/json/yaml），文件名需有语义 | 上下文数据天然多样 |
| D-5 | 向后兼容 | `input_facts.md` 保留为必需；其余可选 | 不影响已有 spec |

## 3. 标准目录结构（更新后）

```
active/feat_xxx/
├── 00_index.md                 # 索引与元数据
├── 00_intent.md                # 意图与问题陈述
├── 01_requirements.md          # 功能需求
├── 02_design.md                # 技术设计
├── 03_plan.md                  # 实施计划
├── context/                    # AI 上下文数据区
│   ├── input_facts.md          # [必需] 方案设计输入事实基准
│   ├── {semantic_name}.csv     # [可选] 字段规则、数据映射
│   ├── {semantic_name}.md      # [可选] 代码结构分析、接口映射
│   └── {semantic_name}.json    # [可选] 配置快照、状态表
├── ref/                        # 外部引用（可选）
│   └── ...                     # PRD 原稿、设计图等不可变输入
└── status.md                   # 看板状态（由 project-board 生成）
```

## 4. context/ vs ref/ 区分规则

| 维度 | context/ | ref/ |
|------|----------|------|
| 性质 | 项目内在上下文 | 外部引用 |
| 可变性 | 随 spec 演化 | 不可变输入 |
| 典型内容 | 字段规则 CSV、可见性映射、代码结构分析、接口映射、状态表 | PRD 原稿、设计图、论文、外部 API 文档 |
| 生产者 | 执行者 + AI 协作 | 外部角色（产品、设计、第三方） |
| 消费者 | AI 助手 + 执行者 | 方案设计阶段参考 |
| 归档 | 全量跟随 spec | 全量跟随 spec |

## 5. 变更清单

| # | 文件 | 变更类型 | 内容 |
|---|------|----------|------|
| C-1 | `.agents/skills/_internal/spec-pipeline/crystallize/step-01-split-files.md` | 修改 | §1 准备目录段补充 context/ 用途说明 |
| C-2 | `.maglev/protocols/collaboration.md` | 修改 | 新增 § context/ vs ref/ 区分规则 |
| C-3 | `specs/20_evolution/active/README.md` | 修改 | 目录结构说明中增加 context/ |
| C-4 | `docs/thinking/component_level_spec_decomposition_antipattern.md` | 新建 | 沉淀 modelconfig 反模式分析 |

## 6. 不影响项

- **project-board**: 扫描逻辑不变（只检查 00-03 标准文件 + git 提交）
- **crystallization 归档**: 已有的 `mv` 操作自动搬迁整个 spec 目录，无需额外处理
- **已有 spec**: input_facts.md 保留为必需，向后兼容
- **spec-designer**: crystallize 管道已创建 context/，只需更新说明文字
