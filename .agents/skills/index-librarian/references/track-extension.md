# 加新 Track —— 用户最小操作清单

> 引用：`SKILL.md` "必需的参考资料"；`02_design.md` §3.6.4 "用户加 track 的体验"。
> 适用：你的项目已经接入 `index-librarian` skill，并且 `index-librarian/protocol/registry.yaml` 已存在。

## 1. 你能加的 Track 类型

| `type` | 用途 | 输出 |
|:---|:---|:---|
| `spec-tree` | `specs/` 多体系仓库 | 各级 `INDEX.md` |
| `docs-tree` | `docs/` 文档树 | 各级 `INDEX.md` |
| `repo-entry` | 仓库根目录 | `repo-entry.yaml` + `repo-map.md` |
| `code-tree` | `packages/` / `src/` 等代码子树 | `code-tree.yaml`（含 radar 摘要） |

## 2. 三步加 Track

### Step 1 — 复制对应的 example 模板

模板位置：`.agents/skills/index-librarian/protocol/registry.example.<type>.yaml`

把模板里的 `tracks:` 段（或单条 track 条目）复制到你的 `registry.yaml` 的 `tracks:` 段末尾。

### Step 2 — 改 4 个最小字段

每条 track 至少改这 4 个字段：

```yaml
- id: <my-unique-id>          # 全仓库唯一，建议 kebab-case
  type: <spec-tree|docs-tree|repo-entry|code-tree>
  root: <path/to/dir/>        # 相对仓库根
  output: <path/to/output>    # 默认产物路径，可保留模板默认
```

其余字段（`enabled` / `depth_limit` / `radar_summary` 等）可保留模板默认。

### Step 3 — 跑一次 scan + verify 验证

```bash
PROTOCOL=".agents/skills/index-librarian/protocol"
./scripts/maglev-python $PROTOCOL/scripts/_track_resolver.py --list           # 确认新 track 已识别
./scripts/maglev-python $PROTOCOL/scripts/track_scan.py   --track-id <my-id>  # 生成产物
./scripts/maglev-python $PROTOCOL/scripts/track_verify.py --track-id <my-id>  # 校验
```

或者直接让 `index-librarian` skill 跑全套：跟它说 "扫描 track `<my-id>`" 即可。

## 3. 常见错误与提示

| 现象 | 原因 | 修复 |
|:---|:---|:---|
| `track not found` | `id` 拼错 / `enabled: false` | 校对 id；改 `enabled: true` |
| `unknown track type` | `type` 不在四枚举内 | 改成上表中的 `type` |
| `root does not exist` | 路径写错或相对位置不对 | `root` 必须相对仓库根 |
| `code-tree` `radar_summary: skipped` | 你环境没装 `radar` binary | 这是预期降级；产物 yaml 仍可用，需要完整依赖图请装 radar |
| `repo-entry` 输出仍是 `.yaml` | 你 `output` 写了 `.yaml` 后缀 | 脚本会自动切到 `.md`（map），这是正常行为 |

## 4. 不要做的事

- ❌ 不要手编 `INDEX.md` / `repo-map.md` / `code-tree.yaml` —— 产物由脚本独占写权。
- ❌ 不要用 `code-tree` 的 `radar_summary` 当 radar 替代品 —— 真要分析依赖请直接调 `radar` skill。
- ❌ 不要把同一 `root` 挂多个相同 `type` 的 track —— 后写的会覆盖前者的产物。

## 5. 进阶：自定义字段

`spec-tree` / `docs-tree` 支持继承 `index-schema.md` 第 §1-§6 全部 frontmatter / stats 规则；`repo-entry` / `code-tree` 由对应脚本契约约束（不走 entity-index frontmatter）。详见 `index-schema.md` §0。

需要更深定制（如自定义 `entity_type` / 多语种 anchor 文件名）时：

- 改 `index-librarian/protocol/scripts/_code_tree_helpers.py` 的 `DEFAULT_ANCHOR_FILES` / `DEFAULT_IGNORE_DIRS` 是仓库级影响，慎用。
- 单 track 级覆盖建议放进该 track 的 registry 条目（如 `anchor_files: [...]` / `ignore_dirs: [...]`）。
