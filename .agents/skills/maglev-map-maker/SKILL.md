---
name: maglev-map-maker
description: 项目地图生成器。组合 Reality、项目看板与 Git tracked tree，确定性生成并校验唯一的人读项目地图 docs/ATLAS.md。
metadata:
  formal_action_name: 项目地图生成
  top_level_capability: 现状表达
  system_layer: Observation Layer
  lifecycle_chain: reality_expression
  runtime_name_status: active_legacy_name
  distribution_scope: runtime_internal
  version: "3.0.0"
---

# Maglev Map Maker（项目地图生成器）

## 核心职责

本技能负责生成唯一的人读项目地图 `docs/ATLAS.md`。它不再依赖 AI 手工扫描和自由推断，
而是调用确定性脚本组合以下权威输入：

- `specs/10_reality/crosscutting/repository-map/repositories.md`：受管仓库清单（若存在）
- `specs/10_reality/00_profile.yaml`：Reality 能力域
- `specs/20_evolution/board.md`：活跃需求和阶段状态（若存在）
- Git tracked tree：仓库结构

`docs/ATLAS.md` 是派生观察视图，不替代 Reality、项目看板、索引或业务代码事实。

## 何时使用

- 用户说“生成项目地图”“生成仓库地图”“更新 Atlas”时。
- 存量项目完成接入后，需要首次建立人读地图时。
- 结晶导致 Reality、目录结构或活跃状态变化，且项目看板已刷新后。
- 需要判断现有 Atlas 是否过期时。

初始化与日常 `reality-sync` 不自动写地图；用户也不需要手动调用
`index-librarian` 的内部脚本。

## 执行契约

```bash
SCRIPT=".agents/skills/maglev-map-maker/scripts/generate_atlas.py"

# 生成或更新
./scripts/maglev-python "$SCRIPT" --root .

# 只检查新鲜度，不写文件
./scripts/maglev-python "$SCRIPT" --root . --check
```

生成动作同时写入：

- `docs/ATLAS.md`：唯一人读地图
- `.maglev/temp/atlas-snapshot.json`：本次生成的结构化证据（不提交）

## 置信度

| 等级 | 条件 |
|:---|:---|
| High | 仓库清单、Reality Profile、项目看板均可用 |
| Medium | 当前 Git 仓库可用，且至少存在 Reality Profile 或项目看板 |
| Low | 只能从 Git tracked tree 生成 |

## 判定纪律

- 项目阶段以 `project-board` 为 owner；本技能不重复猜测生命周期状态。
- 仓库身份以 Reality 仓库清单为 owner；缺失时仅回退到当前 Git 根并降低置信度。
- `.agents/`、`.maglev/`、`dist/`、vendor 等管理或生成目录不进入业务结构图。
- `--check` 以 tracked path 和权威输入内容指纹判断新鲜度。
- 旧的独立 Markdown 索引地图不是输入，也不得重新生成。

## 必需的参考资料

- `references/map.workflow.md`
- `references/step-01-world.md`
- `references/step-01b-terrain.md`
- `references/step-02-city.md`
- `references/step-03-street.md`
