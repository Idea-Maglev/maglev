---
name: reality-admission
description: 共享 Reality Contract、完整投影验证与准入确认内核。
metadata:
  formal_action_name: Reality 准入
  top_level_capability: Reality 治理
  system_layer: Reality / Context Layer
  lifecycle_chain: reality_admission
  runtime_name_status: canonical_name_active
  distribution_scope: runtime_internal
  author: feiyu.gao
  last_updated: 2026-08-19
---

# Reality Admission

Reality Admission 以 **Git 中已提交的完整 Reality 投影**为验证对象。Producer 先在
受控分支或 worktree 中把新事实与既有 `specs/10_reality` 合并，并提交为候选
revision；独立 Validation Provider checkout 同一 commit，验证完整 Reality、变更
diff 与仓库证据。Admission 只确认该已验证 revision，绝不依赖被忽略的候选目录，
也不会在验证后再写另一份 Reality。

## 核心入口

```python
from pathlib import Path
import importlib.util

core_path = Path(".agents/skills/_internal/reality-admission/core.py")
spec = importlib.util.spec_from_file_location("reality_admission_core", core_path)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

projection = core.RealityProjection.from_repository(
    "specs/10_reality",
    base_ref="<修改前 commit>",
    candidate_ref="HEAD",
    intended_use=["onboarding"],
)
validation = core.ValidationResult.from_mapping(validation_result)
admission = core.Admission("specs/10_reality")
plan = admission.dry_run(projection, validation)
receipt = admission.accept(plan)
```

`RealityProjection` 绑定：

- 修改前 `base_commit`；
- 已提交且在当前 worktree checkout 的 `candidate_commit`；
- 完整 Reality tree digest；
- `base_commit → candidate_commit` 的 Reality diff digest；
- Profile / Contract version 与 intended use。

创建投影时要求工作树干净，因此独立 worktree 读取的是同一份代码和 Reality，不会
漏掉被忽略文件或未提交改动。

## 命令行入口

以下命令使用分发的 `scripts/maglev-python`，它负责提供 PyYAML 等协议脚本依赖。
手工复制这些技能到旧项目时，必须同时复制该运行时及其 requirements。

输出当前投影描述：

```bash
./scripts/maglev-python .agents/skills/_internal/reality-admission/scripts/reality_admission.py \
  --reality-root specs/10_reality \
  --base-ref <修改前-commit> \
  --candidate-ref HEAD \
  --intended-use onboarding \
  --json
```

Validation Result 可通过 Agent 原生返回值传递；只有 Adapter 必须序列化时才使用文件。
CLI 也支持从标准输入读取 JSON，不要求创建项目内临时目录：

```bash
cat validation-result.json | \
./scripts/maglev-python .agents/skills/_internal/reality-admission/scripts/reality_admission.py \
  --reality-root specs/10_reality \
  --base-ref <修改前-commit> \
  --candidate-ref HEAD \
  --intended-use onboarding \
  --validation-result - \
  --accept \
  --json
```

成功状态为 `accepted`；若 `base_commit → candidate_commit` 没有 Reality 变化，则为
`no_change`。Admission 不写 Reality，因此不需要 staging、journal 或 recovery。

## 脚本角色边界（关键原则）

Admission 脚本是**辅助验证器，不是结构权威**：

- 脚本只校验客观可追溯性事实：frontmatter 身份字段、reality_id 唯一性、证据文件
  存在性与 digest 一致性、Profile 声明一致性、投影摘要与提交一致性。
- 脚本**不规定**页面章节、标题、措辞模式或篇幅；Reality 页面的结构与写法由本轮
  选定的模板包（`templates/reality-packs/registry.yaml` 登记）唯一决定。
- 脚本发现占位符等残留时只输出非阻断 `WARN` 提示，指引作者**回到模板包对照反思
  修复**；禁止为了让产物通过脚本而把内容改写成脚本期望的形状。
- 页面结构或内容质量结论一律由独立 Validation Provider 依据模板包给出（structure /
  content / confidence 三层），不由脚本代替。

## 共享契约

- [Reality Contract](protocol/reality_contract.yaml)
- [Reality Projection schema](protocol/reality_projection.schema.json)
- [Validation Result schema](protocol/validation_result.schema.json)
- [Generic Pack Consumer](pack_consumer.py)
- [Reverse Work Contract schema](../../maglev-reverse-spec/protocol/work_contract.schema.json)
- [Semantic Review Package schema](../../maglev-reverse-spec/protocol/semantic_review_package.schema.json)
- [Reverse Review Result schema](../../maglev-reverse-spec/protocol/reverse_review_result.schema.json)

逆向生成的交接契约由 Reverse 能力负责，不由 Admission 持有或生成。Admission 不用交接契约
决定模块或生成内容，只在最终 Projection 阶段消费已经绑定的 review 结果和 Git 摘要。
上述 Reverse Schema 是当前活动交接契约；历史实验 Schema 仅保留在
`specs/90_archive/abandoned/2026-08-26-reality-v2-experiment/contracts/`，不得作为当前输入。

Profile 与 Reality Docs 仍是唯一当前事实权威。Projection、Validation Result、
Admission Plan 和 Receipt 都只是绑定特定 Git revision 的验证协议，不构成第二事实源。

首次建立或扩展 Profile 时，若声明 `domain_policy: business_evidence`，每个 domain
必须在 `domain_registry` 中提供 `boundary_reason`、`boundary_basis` 和
`evidence_refs`。仓库、submodule、package 等技术来源应登记为 `source_units`；
`owner_submodules` 和 `owner_repositories` 不能作为 domain 归属字段。

同一 Profile 还必须声明并实际创建 Contract 的 domain slot skeleton：
`README.md`、`capability/`、`implementation/`、`interfaces/`、`operations/`、
`verification/`、`evidence/`。事实正文只能位于 `{domain}/{owner_slot}/` 并进入
`documents` 注册；Admission 会拒绝 `domains/<id>.md`、`modules/<module_slug>.md`
和 domain 根目录单文件等旧路径。
