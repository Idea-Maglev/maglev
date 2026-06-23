# agent context assets sync

> 作用：解决 `AGENTS.md` 与 `llms.txt` 在 Maglev 化项目中缺乏自检与漂移识别的问题，避免 AI 运行时上下文与真实能力结构继续脱节。

## 主入口

- `00_intent.md`
- `00_context.md`
- `01_requirements.md`
- `02_design.md`
- `03_plan.md`
- `04_context_check_integration_spec_v1.md`

## 当前说明

本主题不处理 skill runtime rename 本身。

本主题只处理两类 AI 上下文资产的检查能力：

1. `AGENTS.md`
2. `llms.txt`

## 当前进展

首轮最小实现已经落到现役执行面：

1. `maglev-bootstrapper` 已补 `init` 后的 readiness check 口径
2. `maglev-updater` / `update` workflow 已补升级时的 drift check 口径
3. `packages/maglev-cli/dist/maglev_installer.py` 已内置最小 AI context 检查逻辑

当前已进入封板状态，closeout 见：

- `05_closeout.md`
