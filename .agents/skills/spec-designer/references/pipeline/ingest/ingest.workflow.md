---
name: spec-ingest
description: create-spec 内部模块：摄入异构输入并生成标准化上下文。
output_folder: '{project-root}/.maglev/temp/ingest'
---

# Spec Ingest Workflow

**目标**: 将 Idea, Docs, 或 Legacy Code 转化为标准化的 `ingest_context.json` 和 `input_facts.md`。

## 步骤序列

### 1. Identify Source (识别源头)
读取 `./step-01-identify-source.md`。
*   确定输入类型 (Type 1/2/3)。
*   获取原始路径或文本。

### 2. Map & Skeleton (全景制图)
读取 `./step-02-map-skeleton.md`。
*   **Type 3 Only**: 执行快速扫描 (Level 1)。
*   生成目录树和关键签名概览。
*   **Interaction**: 询问用户是否有需要 "Deep Dive" 的具体模块。

### 3. Zoom & Extract (聚焦提取)
读取 `./step-03-zoom-extract.md`。
*   **Type 3 Only**: 对用户选定的模块执行深度扫描 (Level 2)。
*   **Type 1/2**: 执行常规提取。
*   合并所有信息生成最终的 `ingest_context.json` 和 `input_facts.md`。
