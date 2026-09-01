---
name: step-02-inject
description: 骨架注入
next_step: references/step-03-config.md
---

# Step 2: Structure Injection (骨架注入)

## 目标
物理创建消费者项目的空白治理目录结构，不复制 Maglev 源仓库的 Reality、地图或事实页。

## 动作
1.  **Inject Core**:
    *   Copy 能力资产 `.agents/` -> Root.
    *   Copy 运行规则 `.maglev/` -> Root，但不复制 Maglev 源仓库的实例数据。
    *   Create empty `specs/`, `docs/`, `issues/`, `tests/`.
2.  **Handle Mode**:
    *   **Greenfield**: Create `code_storages/` directory.
    *   **Adoption**:
        *   Ask user: "Should I move existing `src` to `code_storages/` (Recommended) or keep it in Root (Legacy Mode)?"
        *   If Legacy Mode, note this for config step.

## 关键指令
- 使用 `mkdir -p` 创建目录。
- 确保不要覆盖用户已有的重要文件 (如 `.gitignore`)。

## AI 引导摘要生成

注册新仓库后，自动生成 AI 引导摘要：

1. **扫描项目文件生成摘要**：
   - 产品上下文: README.md 前 3 段 + package.json description
   - 技术约定: package.json dependencies + tsconfig + .eslintrc + Makefile
   - 代码结构: src/ 或 lib/ 目录（2 层深度）

2. **展示给用户确认**（不直接写入）

3. **仅在用户确认登记至少一个仓库后**追加到 `crosscutting/repository-map/repositories.md` 的 AI 引导摘要区

摘要写入 `specs/10_reality/crosscutting/repository-map/repositories.md`。没有登记仓库时不得创建该文件。

## 交互示例
AI: "Injecting Maglev core structures..."
AI: "Done. `specs/`, `.agents/` created."
