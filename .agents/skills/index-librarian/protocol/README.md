# Index Protocol (内部协议)

> **位置**：`.agents/skills/index-librarian/protocol/`
> **可见性**：runtime_internal（不向用户暴露，由 `index-librarian` 编排）
> **作用域**：通用 track 索引治理协议，服务 `docs/` / `specs/` / `code/` / `repo-entry` 等多类 track（由 `registry.yaml` 声明）
> **来源**：搬运自 `my-smart-workbench/.agents/skills/_internal/index-protocol/`，2026-04 抽象为 Maglev 通用 track 协议

## 这是什么

为 Maglev 仓库提供**机器可校验的索引治理协议**：

- 凡是确定性逻辑能做的，不让 AI 做
- 任何 INDEX.md 不允许 AI 直接编辑，必须通过 `index_update.py`
- AI 仅读取脚本 JSON 输出做呈现与决策

## 核心组件

| 文件 | 作用 |
|------|------|
| `registry.yaml` | 声明哪些 track 纳入治理（4 类 track：spec-tree / docs-tree / code-tree / repo-entry） |
| `index-schema.md` | INDEX.md frontmatter 规则与位段语义 |
| `index-verify.md` | 校验规则定义 |
| `index-update.md` | 更新规则定义 |
| `scripts/index_init.py` | 初始化模块 INDEX.md |
| `scripts/index_scan.py` | 扫描模块健康度 |
| `scripts/index_verify.py` | 校验 schema 一致性 |
| `scripts/index_update.py` | 更新 INDEX.md（聚合 stats、生成 body table、注入认知地图） |
| `scripts/archive_triggers.py` | F6 归档触发器：扫描时间窗 / 上位重写 / 引用断链候选 |
| `scripts/cognitive_map.py` | F8 认知地图：聚合跨段引用 → Mermaid + knowledge_graph.json |
| `scripts/common/` | 共用工具（frontmatter / logger / stats DSL） |
| `scripts/module_checks/` | 模块特定校验插件 |
| `scripts/templates/` | INDEX.md 模板（root / partition / collection） |

## 调用约定

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"

./scripts/maglev-python ${PROTOCOL}/scripts/index_scan.py        # 扫描
./scripts/maglev-python ${PROTOCOL}/scripts/index_verify.py      # 校验
./scripts/maglev-python ${PROTOCOL}/scripts/index_update.py      # 更新
./scripts/maglev-python ${PROTOCOL}/scripts/index_init.py        # 初始化
```

| Exit Code | 含义 |
|-----------|------|
| 0 | 健康 / 全部通过 |
| 1 | 有 error 级问题 / 部分失败 |
| 2 | 脚本自身错误 |

## 不要做的事

- ❌ 不要 AI 直接编辑 INDEX.md
- ❌ 不要 AI 自己计算文件数 / stats
- ❌ 不要绕过 registry 给孤立目录写 INDEX.md
- ❌ 不要在协议层硬编码 Maglev 业务逻辑（应放 `module_checks/<module>.py`）

## 与上游 workbench 协议的关系

- **同源**：搬运自 my-smart-workbench `_internal/index-protocol/`（2026-04-24 同步点）
- **独立演进**：Maglev 后续可基于自身需求扩展 schema（如位段隐喻名、认知地图字段），但保持核心契约一致
- **不引入跨仓依赖**：完整独立拷贝，无 git submodule

## 编排入口

由 `.agents/skills/index-librarian/` 编排。
