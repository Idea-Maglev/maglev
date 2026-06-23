---
title: 'maglev-cli version --json'
slug: 'version-json-flag'
type: spec
complexity_tier: '1-Atomic'
delivery_type: 'code'
maglev_status: 'accepted'
created: '2026-05-31'
status: 'in-progress'
stepsCompleted: []
tech_stack: [node, javascript]
files_to_modify:
  - packages/maglev-cli/bin/index.js
---

# version --json 子命令

## 需求

为 `maglev-cli version` 添加 `--json` 标志，输出结构化 JSON 代替人类可读文本。

## 验收标准

- AC-1: `maglev-cli version --json` 输出合法 JSON
- AC-2: JSON 包含字段 `cli_version`, `bundled_version`, `node_version`, `platform`
- AC-3: 不带 `--json` 时行为不变（向后兼容）
- AC-4: manifest.json 缺失时 JSON 输出含 `error` 字段

## 设计

在 `bin/index.js` 的 `printVersion()` 函数中检测 `--json` flag：
- 若存在，输出 `JSON.stringify(...)` 并 exit 0
- 错误情况输出含 error 字段的 JSON 并 exit 2

## 测试策略

使用 Node.js 内置 test runner (`node --test`) 或 Jest。
测试文件: `packages/maglev-cli/tests/version-json.test.js`
