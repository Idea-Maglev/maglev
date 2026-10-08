---
reality_id: delivery-runtime.operations.downstream-layout
title: 下游项目运行布局
owner_domain: delivery-runtime
owner_slot: operations
fact_type: system_topology
knowledge_status: established
scope:
  includes:
    - 安装器在下游项目维护的受管文件布局；构建沙箱与发行镜像的定位；受管仓库清单的落点
  excludes:
    - 各受管文件的内容语义（属相应域）
---

# 下游项目运行布局

安装器在下游项目中维护 `.agents/`、`.maglev/`、`AGENTS.md` 与 `llms.txt`。`.agents/` 承载运行时能力，`.maglev/` 保存配置与同步状态；`AGENTS.md` 和 `llms.txt` 提供 Agent 的协作纪律与导航入口。初始化不会重新生成已退役的协议目录；旧项目升级时由 manifest 退役元数据执行保守迁移。

Python 协议脚本通过 `scripts/maglev-python` 使用项目本地运行环境执行。发行构建使用 `.maglev_build/` 作为临时沙箱，`packages/maglev-cli/dist/` 是 npm 包的发行镜像；两者不是长期事实源。

下游仓库的受管代码仓库清单写入 `crosscutting/repository-map/repositories.md`，并在存在 Reality Profile 时登记为受控横切事实页。

深挖：[已知缺口](../verification/known-gaps.md)。
