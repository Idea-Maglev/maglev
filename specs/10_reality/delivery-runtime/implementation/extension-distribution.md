---
reality_id: delivery-runtime.implementation.extension-distribution
title: 扩展分发与执行选择
owner_domain: delivery-runtime
owner_slot: implementation
fact_type: product_logic
knowledge_status: established
scope:
  includes:
    - maglev-extension 命令面；asset_pack/external_integration 两类安装；安装不等于可执行的选择语义；官方与第三方 Registry 的当前事实
  excludes:
    - 扩展的运行时执行插槽选择细节（属 skill-runtime 域）
    - 扩展包内部 Provider 的业务能力（属各 Provider 文档）
---

# 扩展分发与执行选择

`@idea-maglev/maglev-extension-cli` 提供 `maglev-extension` 命令，用于搜索、安装、更新、启用、禁用、移除和检查扩展。项目的 Registry source 位于 `.maglev/extensions.sources.yaml`，安装与启用状态记录在 `.maglev/extensions.lock`（两者是下游项目产物，由安装/扩展命令生成；本仓库自身不持有）。

`asset_pack` 安装 manifest 声明的受管资产；`external_integration` 只记录外部 provider 的检测和启用状态，不复制或修改 provider 文件。安装不等于可用于代码执行：`code-execution-slot` 只从 lock 中选择已启用、且外部集成已检测成功的候选。

`maglev init` 在缺失 `.maglev/extensions.sources.yaml` 时会写入默认 `maglev-official` Git Registry source，并对官方 SSH / HTTP(S) URL 做 best-effort 选通。若探测失败，初始化仍继续完成，并写入 canonical 官方源 `https://github.com/Idea-Maglev/maglev.git`（`ref: master`）。

`search`、`inspect` 和 `install` 按 enabled source 顺序消费 Registry。单个 source 失败但后续 source 健康时，命令继续成功并返回 warning；只有全部 enabled source 都失败时才阻断。

外部 Platform Operations Extension 由第三方团队独立维护，Maglev 只消费其 Registry source 和 Extension source，不复制 Provider 实现。当前已确认的 Extension 包包含 7 个 Provider：`aamp`、`private-document-provider`、`private-user-operations-provider`、`private-issue-provider`、`private-project-intake-provider`、`private-handover-provider`、`private-file-provider`。

该 Extension 不声明 `code-execution` slot，安装默认不启用 Provider。安装后的 Provider Skill 位于消费者项目 `.agents/skills/<provider>/`，契约与处置说明位于 `docs/extensions/`，来源、版本、commit 和安装资产记录在 `.maglev/extensions.lock`。

该 Extension 只作为未来平台操作小队的 Provider 来源，不等同于已构建或已同步的平台操作 Squad；当前未向生产 Multica Workspace 写入 Squad。

## 第三方 Registry 与机制保留边界

private third-party Registry `private third-party Git Registry` 以 `master` 提供 `private-project-workbench` 能力包。当前正式发布 commit 为 `<private-commit-redacted>`，能力包版本为 `0.3.0`。验证记录见 private validation report。

该 Registry 的 manifest 是安装资产唯一权威。其审计账本覆盖源项目冻结基线中的 84 个非 Maglev 技能，当前候选分为 `ready`、`adaptation_required`、`blocked` 和 `excluded`；未通过安全与自洽审查的技能不进入安装资产。

对需要private document service、enterprise system、database、Figma、private platform 或其他外部服务的技能，Registry 可以保留调用机制和配置入口，但不携带凭证、个人认证状态或敏感日志。没有消费方凭证时，运行状态记录为 `runtime_verification: not_run`；外部服务可达性、授权、远端写入和业务副作用由消费方负责验证。Maglev 只验证扩展发现、资产安装、生命周期状态、provenance 和调用准备度。

正式生命周期证据由 Maglev Testbed private branch 保存，使用 Maglev `release-0.7.1` CLI 验证官方与第三方来源共存、搜索、检查、安装、启用、更新、移除和资产清理。

深挖：[已知缺口](../verification/known-gaps.md)。
