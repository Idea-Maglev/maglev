# 功能需求：AI 上下文数据区

## FR-1: context/ 目录约定扩展

**用户故事**: 作为 Maglev 化项目的执行者，我需要在 spec 目录中有一个标准化的位置来存放 AI 协作时的半结构化上下文数据，以避免自建非标准目录结构。

- **AC-F1-1**: 当执行者需要存放字段规则、代码映射、状态表等半结构化数据时，应使用 `active/feat_xxx/context/` 目录，而不是创建个人命名空间或非标准子目录
- **AC-F1-2**: `context/` 中 `input_facts.md` 保持为必需文件（向后兼容），其余文件为可选
- **AC-F1-3**: context/ 中除 `input_facts.md` 外的文件名需有语义（不允许 `temp.md`、`data.csv` 等无意义命名）

## FR-2: context/ 与 ref/ 边界定义

**用户故事**: 作为 Maglev 化项目的执行者，我需要清楚知道 context/ 和 ref/ 的区别，以正确存放不同类型的参考资料。

- **AC-F2-1**: 框架文档中明确定义 context/ 存放「项目内在上下文」——随 spec 演化、AI 需要消费的数据
- **AC-F2-2**: 框架文档中明确定义 ref/ 存放「外部引用」——PRD 原稿、设计图等不可变输入
- **AC-F2-3**: 至少在 `collaboration.md` 或同级协议文档中包含 context/ vs ref/ 的区分说明

## FR-3: 归档生命周期

**用户故事**: 作为 Maglev 框架使用者，我需要 context/ 在 spec 归档时被正确搬迁，确保归档 spec 的可复现性。

- **AC-F3-1**: crystallization 归档时，context/ 全量随 spec 目录搬迁到 `90_archive/`，不做脱敏或精简
- **AC-F3-2**: 归档后的 context/ 内容作为 spec 的一部分，支持后续回溯

## FR-4: 文档与模板更新

**用户故事**: 作为 Maglev 化项目的新执行者，我需要在模板和文档中看到 context/ 的使用说明，以快速理解该目录的用途。

- **AC-F4-1**: `_internal/spec-pipeline/crystallize/step-01-split-files.md` 的目录准备段落中包含 context/ 的用途说明
- **AC-F4-2**: `specs/20_evolution/active/README.md` 的目录结构说明中包含 context/

## 术语表

- **context/**: Spec 级别的 AI 上下文数据区，存放随需求演化的半结构化内部数据
- **ref/**: 外部引用资料目录，存放不可变的输入材料（PRD 原稿、设计图等）
- **input_facts.md**: context/ 中的必需文件，记录方案设计时的输入事实基准
- **半结构化数据**: 不完全遵循固定 schema 但有组织的数据，如 CSV 字段表、Markdown 映射表、JSON 配置快照
