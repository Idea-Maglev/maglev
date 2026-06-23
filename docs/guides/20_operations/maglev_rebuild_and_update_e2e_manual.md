# Maglev 重建与更新联调手册

> 目标：当你手动删除 `.maglev_build/` 或 `packages/maglev-cli/dist/` 后，提供一条从零重建发行物、再模拟用户更新的最短可执行路径。

## 1. 这篇手册适合谁

这篇手册面向：

- 正在维护 Maglev 源仓库的人
- 想验证 release 构建是否完整的人
- 想手动演练一次“维护者构建 -> 用户更新”的人

如果你只是正常发布版本，建议先读：

- [Maglev 开发与发布流程](./maglev_development_release_workflow.md)
- [Maglev 发布说明与维护手册](./maglev_release_manual.md)

## 2. 先说结论

如果你删掉了：

- `.maglev_build/`
- `packages/maglev-cli/dist/`

不要手工恢复这些目录。

正确做法是：

1. 用 `maglev_version.py` 对齐版本事实
2. 用 `maglev_release.py --dry-run --skip-audit` 重建发行物
3. 用 CLI 入口验证 `version`
4. 在一个临时项目里手动跑 `update --dry-run` 和 `update`

如果你不想每次手工拼接这些命令，现在也可以直接使用：

- `python3 scripts/maglev_smoke_test.py`
- `python3 scripts/maglev_e2e_check.py`

## 3. 从零重建发行物

### 3.1 清理旧构建产物

如果你想刻意从零验证，可以先删除旧产物：

```bash
rm -rf .maglev_build packages/maglev-cli/dist
```

### 3.2 对齐版本事实

先看当前版本：

```bash
python3 scripts/maglev_version.py show
```

如果这次需要切版本，例如切到 `0.1.4`：

```bash
python3 scripts/maglev_version.py set 0.1.4
python3 scripts/maglev_version.py check
```

如果只是重建而不改版本，也至少执行：

```bash
python3 scripts/maglev_version.py check
```

### 3.3 重建发行物

执行：

```bash
python3 scripts/maglev_release.py --dry-run --skip-audit
```

这一步会重新生成并同步：

- `.maglev_build/`
- `packages/maglev-cli/dist/`

如果脚本在 changelog 阶段停下，先补齐：

- `.maglev_build/CHANGELOG.md`
- `docs/releases/<version>.md`
- `docs/releases/index.md`

然后重新运行 dry-run。

## 4. 维护者侧先做哪些验证

### 4.1 检查版本一致性

```bash
python3 scripts/maglev_version.py check
node packages/maglev-cli/bin/index.js version
```

你应该能看到：

- CLI 版本正常输出
- `bundled-dist` 版本与 CLI 一致

### 4.2 跑自动化测试

推荐至少执行：

```bash
python3 -m unittest tests.test_maglev_version tests.test_maglev_release tests.test_maglev_update_flow
```

如果你只想验证更新链路，也可以只跑：

```bash
python3 -m unittest tests.test_maglev_update_flow
```

## 5. 如何手动模拟用户更新

当前用户入口应该是 CLI，而不是直接手工调用 installer。

### 5.1 准备一个临时项目

例如：

```bash
mkdir -p /tmp/maglev-demo/.maglev
```

创建一个最小的 `.maglev/sync_state.json`：

```json
{
  "last_synced_version": "0.1.3",
  "last_synced_time": "2026-03-19T00:00:00Z",
  "file_baselines": {}
}
```

把它保存到：

- `/tmp/maglev-demo/.maglev/sync_state.json`

### 5.2 预览更新

进入临时项目目录后执行：

```bash
cd /tmp/maglev-demo
node /你的-maglev-仓库/packages/maglev-cli/bin/index.js update --dry-run
```

预期现象：

- 命令成功退出
- 输出中出现 `DRY-RUN`
- 输出中能看到即将更新到的新版本

### 5.3 正式执行更新

继续在临时项目目录执行：

```bash
node /你的-maglev-仓库/packages/maglev-cli/bin/index.js update
```

预期现象：

- 输出中出现 `Maglev 更新完毕`
- `.maglev/sync_state.json` 被刷新到新版本
- 项目根目录出现或刷新 `CHANGELOG.md`

## 6. 如果遇到这些报错，应该怎么理解

### 1. 包内镜像缺失 installer

这通常说明：

- 你删掉了 `packages/maglev-cli/dist/`
- 但还没重新跑 release dry-run

先执行：

```bash
python3 scripts/maglev_release.py --dry-run --skip-audit
```

### 2. `.maglev_build/` 与 CLI 版本不一致

这通常说明：

- 你改了 `package.json` 或统一版本源
- 但还没重新构建 `.maglev_build/`

先执行：

```bash
python3 scripts/maglev_version.py check
python3 scripts/maglev_release.py --dry-run --skip-audit
```

### 3. 项目里没有 `.maglev/`

这说明当前目录不是一个已经接入 Maglev 的项目。

你不能直接测 `update`，应先完成初始化。

## 7. 最短演练顺序

如果你只想快速跑通一次，照这个顺序做：

1. `rm -rf .maglev_build packages/maglev-cli/dist`
2. `python3 scripts/maglev_version.py check`
3. `python3 scripts/maglev_release.py --dry-run --skip-audit`
4. `node packages/maglev-cli/bin/index.js version`
5. `python3 -m unittest tests.test_maglev_update_flow`
6. 在临时项目目录手动执行：
   - `node /你的-maglev-仓库/packages/maglev-cli/bin/index.js update --dry-run`
   - `node /你的-maglev-仓库/packages/maglev-cli/bin/index.js update`

这样就完成了一次“从零重建发行物，再模拟用户更新”的完整手动验证。

## 8. 更快的维护者入口

如果你只想确认关键链路没坏，可以执行：

```bash
python3 scripts/maglev_smoke_test.py
```

它会：

- 执行统一版本检查
- 跑版本治理与 release 门禁相关单测
- 在包内镜像已同步时补做 CLI `version` 检查

如果你想一键跑完整联调，可以执行：

```bash
python3 scripts/maglev_e2e_check.py
```

它会自动完成：

1. `maglev_version.py check`
2. `maglev_release.py --dry-run --skip-audit`
3. CLI `version` 检查
4. `tests.test_maglev_update_flow`
5. 临时项目中的真实 `update --dry-run`
6. 临时项目中的真实 `update`
