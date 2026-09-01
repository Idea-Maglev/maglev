# Step 2: Bootstrap (基础设施注入)

## 目标
补全 Maglev 运行所需的最小环境。

## 逻辑
1.  **If .maglev missing**:
    - 提示用户: "检测到缺少 Maglev 核心配置。建议运行 `maglev-bootstrapper` 或手动复制 Starter Kit。"
    - *Auto-Fix*: 如果用户同意，且你具备 `maglev-bootstrapper` 能力，尝试调用它。否则，提供复制指令。
2.  **If specs/ missing**:
    - 创建 `specs/00_planning`, `specs/10_reality`, `specs/20_evolution`, `specs/90_archive`。
3.  **If issues/ missing**:
    - 创建 `issues/active`, `issues/closed`。

4. **Reality bootstrap boundary**:
    - 不复制 Maglev 自身的 Profile、Reality 页面或现状文档到消费者项目。
    - 如果目标项目没有 `specs/10_reality/00_profile.yaml`，在第一次 Reality Projection
      的同一个 candidate commit 中建立项目自己的最小 Profile 与首批页面。
    - 首次 Profile 先登记技术 `source_units`，再依据业务对象、用户任务、流程、权限和数据责任
      建立 `domain_registry`；不得从 submodule 清单直接生成 domains。
    - `domain_policy: business_evidence` Profile 必须按共享 Contract 创建每个 domain 的
      `README.md`、`capability/`、`implementation/`、`interfaces/`、`operations/`、
      `verification/` 和 `evidence/` 入口；Bootstrap 只能创建空骨架，不能把业务事实写成
      `domains/<id>.md` 或 `modules/<id>.md`。
    - 事实正文只能在 `{domain}/{owner_slot}/{fact_slug}.md`，并由 Profile `documents`
      登记；缺少适用事实的 slot 保留 `INDEX.md`，状态写为 `unknown` 或有证据的
      `not_applicable`。
    - 不创建 ignored Candidate 目录或项目内临时 Validation Request/Result 文件。
