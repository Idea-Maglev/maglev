# Maglev 根目录重构计划 (源码归位)

> **目标**: 将 `solutions/starter-kit/` 核心内容合并到 `<private-repo-path-redacted>/my/maglev` 根目录，建立纯净的 Monorepo 结构。
> **原则**: Root is Source. Starter Kit is Build Target (Gitignored).

## 1. 迁移映射 (The Move)

| 源路径 (`solutions/starter-kit/`) | 目标路径 (`./`) | 策略 | 备注 |
| :--- | :--- | :--- | :--- |
| `.agents/skills/` | `.agents/skills/` | **Merge (合并)** | 优先保留根目录较新的 Skill；如果不冲突则直接合并。 |
| `.agents/workflows/` | `.agents/workflows/` | **Merge (合并)** | 用户自定义的工作流优先级最高。 |
| `.maglev/` | `.maglev/` | **Merge (合并)** | 规则与配置。需注意根目录如已有相应配置，需人工核对。 |
| `docs/` | `docs/guides/` | **Move (移动)** | 将 Starter Kit 的原始文档归入 `docs/guides/`。 |
| `specs/` | `specs/templates/` | **Move (移动)** | Starter Kit 的 Specs 为模板。移动至 `specs/templates/`。 |
| `README.md` | `docs/PRODUCT_MANUAL.md` | **Rename (重命名)** | 根目录 `README.md` 描述 OS 项目本身。 |
| `contributors/` | `contributors/` | **Merge (合并)** | 合并贡献者列表。 |
| `references/` | `references/` | **Merge (合并)** | 合并参考资料 (如果存在)。 |
| `issues/` | `issues/` | **Merge (合并)** | 如有。 |

## 2. 迁移后目录结构 (Monorepo)

```text
.
├── .agents/                 # [Runtime + Source]
│   ├── skills/             #   -> Skill 源码 (Maglev OS 的第一公民)
│   └── workflows/          #   -> 工作流定义
├── .maglev/                # [Config] 项目规则配置
├── docs/                   # [Documentation]
│   ├── thinking/           #   -> 架构决策记录 (ADR)
│   ├── guides/             #   -> 用户手册 (原 starter-kit/docs)
│   └── PRODUCT_MANUAL.md   #   -> 产品说明 (原 starter-kit/README.md)
├── specs/                  # [Specifications]
│   ├── 10_reality/         #   -> Maglev OS 的现状
│   ├── 20_evolution/       #   -> 重构与演进计划
│   ├── 30_solution/        #   -> Starter Kit 构建配置
│   └── templates/          #   -> 模板 specs (原 starter-kit/specs)
├── contributors/           # [Community]
├── references/             # [Knowledge]
├── solutions/              # [Output]
│   ├── examples/           #   -> 示例项目 (Consumers)
│   └── starter-kit/        #   -> [Build Target] (已清空，仅作为构建输出目录存在)
└── README.md               # [Project] Maglev OS 项目介绍
```

## 3. 执行计划 (Execution)
1.  **Backup (备份)**: 备份根目录 `.agents`, `.maglev`, `docs`。
2.  **Move & Merge (迁移)**:
    *   执行 `rsync -av solutions/starter-kit/ ./` (排除 `solutions` 自身)。
    *   处理 `README.md` 重命名冲突。
    *   处理 `specs` 和 `docs` 的移动逻辑。
3.  **Cleanup (清理)**: 清空 `solutions/starter-kit` (或保留 `.gitkeep`)。
4.  **Verification (验证)**: 验证 `maglev-bootstrapper` 能否直接从根目录运行。

---
*Planned by Maglev Architect*
