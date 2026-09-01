---
name: maglev-reverse-spec
description: 面向任意存量项目重建当前事实、功能边界、流程、数据和验证依据，并交付可独立核对的现实资料。
metadata:
  formal_action_name: 逆向现状重建
  top_level_capability: 整体接入
  system_layer: Infrastructure Layer
  lifecycle_chain: system_enablement
  runtime_name_status: canonical_name_active
  distribution_scope: user_visible
---

# 逆向现状重建

## 这项能力解决什么

把一个已有项目中分散在需求材料、页面、接口、任务、数据结构、代码和测试里的当前事实，
整理成可阅读、可回查、可继续验证的现实资料。

这项能力的核心不是“扫描出多少文件”，而是回答：

- 项目当前有哪些稳定的业务入口；
- 每个入口实际承担什么用户目标或业务责任；
- 入口经过哪些实现、数据和状态；
- 哪些内容有直接证据，哪些只是推断，哪些仍未知；
- 哪些内容属于同一业务边界，哪些应保持未归类；
- 这些事实能否安全写入目标项目自己的现实资料，并由独立验证方确认。

## 适用范围

- 接手没有完整现状文档的存量项目；
- 为重构、交接、契约核对或风险识别建立事实底稿；
- 为已经接入 Maglev 的项目补齐当前现实资料；
- 为没有页面的服务、任务、命令行工具、软件开发工具包、事件系统或数据系统建立入口和边界。

不用于修复业务代码、补测试、补数据、修改接口实现或替系统做设计决策。

## 模板定位

本能力的模板登记入口固定为能力仓库根目录下的 `templates/reality-packs/registry.yaml`。新会话
先读取该入口，再按其中的 `default_pack_id` 或本轮明确的模板标识解析登记清单；若登记入口没有
默认包，必须由本轮显式提供已批准的模板标识；不能从目标项目、样本产物或模板目录名称猜测模板。

## 触发条件与阶段边界

### 能力触发

当用户要为已有项目重建当前现状、功能边界、流程、数据或验证依据时，入口路由到本能力。
如果只是要查看现状同步、做需求收敛、设计方案或验证已有结果，不在本能力内重复接管。

实际触发链是：用户提出逆向请求 → `entry-router` 识别并交接 → 本能力执行准备检查 →
准备检查通过后才进入阶段 A。用户不能只通过打开某个参考文件来触发阶段 A。

### 阶段 A 触发

阶段 A 不是看到本技能就自动开始。必须先完成“准备检查”，并同时具备：

- 目标项目和基线已锁定；
- 读取契约已列出允许的来源单元及来源角色；
- 本轮用途和需要的事实范围已明确；
- 模板包已选定；
- 人读产物与机器证据目录已隔离；
- 本轮静态材料读取已获授权。

上述条件成立后，阶段 A 才从“直接阅读一手材料”开始。阶段 A 先形成模块地图和语义审阅包，
再由用户完成 Gate A 边界裁决；这一阶段不写入现实资料，不做事实准入。

### 阶段 B 触发

只有阶段 A 已产生模块地图和语义审阅包，且用户已经通过 Gate A 裁决模块边界、依赖顺序、
公共内容和未归类项，才进入阶段 B。阶段 B 先完成后置结构校验，生成项目级入口页面和第一个模块的纵切片，
再由用户完成 Gate B；Gate B 通过后，按依赖批次逐模块生成其余内容，最后进行模板/流程/模块质量
复验、事实核对、现实资料写入、独立验证和准入。未裁决、需要改范围或仍有阻断问题时，停留在
当前阶段或返回准备阶段。

## 唯一工作顺序

```mermaid
flowchart LR
    A0[准备检查与 Work Contract] --> A1[阶段 A：直接阅读与模块地图]
    A1 --> A2[Gate A：人工边界与依赖裁决]
    A2 --> B0[后置结构校验]
    B0 --> B1[项目级入口页面与首个模块纵切片]
    B1 --> B2[Gate B：人工内容质量裁决]
    B2 --> B3[按依赖批次逐模块生成]
    B3 --> B4[模板、流程和模块质量复验]
    B4 --> B5[事实核对与适用维度]
    B5 --> B6[写入目标项目现实资料]
    B6 --> B7[完整资料对抗审查]
    B7 --> B8[独立验证与准入]
```

其中：

- `step-00-integrity-check.md` 只负责 A0，不能生成模块；
- `stage-a-agent-first.md` 负责 A1 和 A2，是阶段 A 的唯一总协议；
- `step-01-evidence-acquisition.md`、`step-01-project-map.md`、`step-01b-router-analysis.md` 和
  `step-02-page-analysis.md` 是阶段 A 按入口形态选用的辅助阅读步骤，不是额外阶段；
- `step-02b-module-partition.md`、`step-03-*`、`step-03b-*` 和 `reverse-extension-pack.md` 只在
  阶段 B 按用途选用；
- `stage-b-intermediate-review.md` 负责阶段 B 写入前的模板、流程和逐模块质量复验；
- `step-04-cross-examination.md`、`wrapper-04-reality-projection.md` 和
  `step-06-verify-output.md` 负责阶段 B 的完整资料审查、写入和准入。

阶段 A 和阶段 B 都不按文件编号逐个执行。每个参考文件只产出自己的最小结果，不能再次生成
其他文件已经生成的入口、模块或边界。

## 输入

每个项目由适配说明提供以下信息。模板登记入口相对能力仓库根目录解析，不相对目标项目根目录
解析：

- 目标项目根目录和本轮用途；
- 修改前的基线提交；
- 允许读取的来源单元；
- 每个来源单元可承担的来源角色；
- 当前项目自己的现实资料和资料契约（如果已有）；
- 模板登记入口和本轮模板包选择；
- 人读产物和机器证据的隔离目录。

最小机器输入可以表达为：

```yaml
reverse:
  project_id: <项目标识>
  project_root: <项目相对路径>
  baseline: <基线提交>
  source_units:
    - unit_id: <来源单元>
      relative_path: <允许读取的相对路径>
      roles: [intent, implementation, verification]
      exclusions: []
  template_registry_path: templates/reality-packs/registry.yaml
  template_pack:
    pack_id: <模板包标识；缺省时必须由登记入口提供 default_pack_id>
    manifest_path: <由登记入口解析出的登记清单相对能力仓库根目录路径>
    manifest_digest: <登记清单摘要>
    pack_digest: <模板包摘要>
  output:
    human_review_root: <人读产物目录>
    machine_evidence_root: <机器证据目录>
    target_reality_root: <目标项目的 Reality 根目录>
  permissions:
    static_read: true
    runtime_read: false
    business_write: false
    reality_write: false
    project_execution: false
    material_reduction_tools: false
    script_execution: true
```

`script_execution: true` 只表示 Work Contract 可以在既有工作流声明的阶段执行已登记脚本；不表示
可以新增脚本、缩窄语义材料或把脚本输出当作模块/边界结论。机器字段 `intent`、`implementation`、
`verification` 分别表示目标意图、当前实现和验证依据。
它们是来源角色，不是模块名称，也不能互相替代。
`template_registry_path` 是模板选择的唯一入口，默认值为 `templates/reality-packs/registry.yaml`；
`template_pack.manifest_path` 必须由登记入口解析，不能由项目适配说明随意指定。该路径所在目录
就是本轮模板包目录，模板资产路径相对该目录解析，不能按目录名自行枚举。

机器交接契约：

- [Work Contract](protocol/work_contract.schema.json)；
- [Semantic Review Package](protocol/semantic_review_package.schema.json)；
- [Reverse Review Result](protocol/reverse_review_result.schema.json)。

这些 Schema 约束交接字段和状态，不生成事实，也不替代人类对模块边界、内容丰富度和置信度的裁决。

## 模板包的使用

逆向能力不自带一套页面模板。每轮先从 `templates/reality-packs/registry.yaml` 解析模板包；
只有登记入口明确指定的模板包才能使用。模板包负责页面契约、方法论、正向示例和审阅项；
智能体负责把当前项目的一手材料填入适用页面。模板包不提供项目事实，也不决定模块边界。

模板包的实际消费方式固定为：

1. 读取 `template_registry_path`；使用登记入口的 `default_pack_id`，或使用本轮明确且已批准的模板
   包标识；两者都没有时直接阻断；
2. 从登记入口解析唯一的 `template_pack.manifest_path`，核对登记清单、模板包标识、登记清单
   摘要和模板包摘要；
3. 按登记清单中的资产标识、公开路径和页面映射读取模板包说明、方法论、页面契约、正向示例
   和模板审阅项，不按目录名自行挑选文件；
4. 先读取方法论和采纳边界，确认页面结构的适用范围；
5. 根据项目入口、本轮用途和已有证据，选择适用的项目级入口页面、能力页面、证据页面及阶段 B 页面；
6. 对每个适用页面，按页面契约的读者问题、来源角色和落地结构写入当前项目事实，并用正向
   示例校准表达深度，用模板审阅项做提交前自查；
7. 页面适用但证据不足时仍按契约生成页面，明确标记 `[UNKNOWN]` 或 `[BLOCKED]`，写明缺失
   证据和下一步静态入口；不能用其他来源角色补齐，也不能静默省略；
8. 页面不适用时只记录 `not_applicable`、判断依据和落地位置，不创建空页面；
9. 模板资产缺失、登记清单与页面契约不一致或来源真相无法确认时停止并记录阻断；
10. 保留页面契约声明的页面标识和归属，不另造“模块清单”“来源定位页”或其他逆向专用页面模板。

阶段 B 继续消费同一模板包中与事实核对、接口、运行、数据和验证有关的适用页面契约。完整
调用链、数据结构和现实资料页面必须落在模板包声明的页面中，而不是落在逆向能力自定义的
平行页面结构中。

## 输出

按阶段生成适用内容，不追求无证据的全量覆盖。

阶段 A 只产出：

- 入口与来源地图；
- `reverse_module_map`：模块边界、适用 Slot、依赖顺序、公共内容和未归类项；
- `semantic_review_package`：按模块组织的页面适用性、事实草稿、Claim、SourceRef 和前序摘要；
- 公共内容和未归类账本；
- `reverse_gate_record`（Gate A）；
- 事实、推断、未知和阻断项。

阶段 B 才产出：

- 后置问题项；
- 项目级入口页面和首个模块纵切片及 `reverse_gate_record`（Gate B）；
- 按依赖批次生成的逐模块语义包；
- 模板、流程和逐模块质量复验记录；
- 事实核对资料和适用维度账本；
- 现实资料投影；
- `reverse_review_result` 三层独立验证结果或明确的阻断交接；
- 准入记录（仅在独立验证通过后生成）。

人读产物至少应能让接手者回答“从哪里进入、做了什么、依赖什么、证据在哪里、还缺什么”。

## 不可越过的边界

- 来源单元只表示读取许可，不能直接变成模块；
- 技术目录、仓库、子模块、包名、文件数量和命名相似度不能单独决定业务边界；
- 模块可以跨来源单元，一个来源单元也可以支撑多个模块；
- 需求材料只说明目标意图，代码只说明当前实现，测试只说明验证依据；
- 缺少某类来源时保留未知或阻断，不用其他来源补齐；
- 无法归属的内容进入未归类账本，不创建默认“其他”模块；
- 公共内容必须有真实、直接、可解释的跨模块依赖；
- 失败产物、历史候选和未授权路径不得进入当前输入；
- 自动化工具只能做导航或后置结构校验，不能决定模块、边界、公共内容或语义归属；
- Gate A 和 Gate B 各最多允许一次受控返工；人工审阅裁决范围和质量，不逐页代写；
- 项目级入口页面必须按 Pack 声明的 `target_path` 物化到目标 Reality 根目录，不得创建未声明的输出容器；
- 模块生成必须遵守 Gate A 接受的依赖顺序，并将前序模块摘要作为输入；
- 逆向期间不修改业务代码、数据、接口实现或运行状态。

若目标项目已有自己的现实资料，阶段 B 必须先读取目标项目自己的资料契约；不能把 Maglev 自身
的资料目录、业务域或事实页复制到消费者项目。

## 参考文件

- [唯一工作流](references/reverse-spec.workflow.md)
- [通用原则](references/reverse-principles.md)
- [准备检查](references/step-00-integrity-check.md)
- [适用维度账本](references/step-00b-dimension-ledger.md)

阶段 A：

- [语义审阅总协议](references/stage-a-agent-first.md)
- [静态证据地图](references/step-01-evidence-acquisition.md)
- [入口与功能地图](references/step-01-project-map.md)
- [入口深入分析](references/step-01b-router-analysis.md)
- [页面与交互分析](references/step-02-page-analysis.md)

阶段 B：

- [模板、流程和模块质量复验](references/stage-b-intermediate-review.md)
- [现实边界映射](references/step-02b-module-partition.md)
- [调用链分析](references/step-03-stack-trace.md)
- [数据结构分析](references/step-03-data-structure-analysis.md)
- [证据解释](references/step-03b-evidence-interpretation.md)
- [现实资料对抗审查](references/step-04-cross-examination.md)
- [现实资料投影](references/wrapper-04-reality-projection.md)
- [独立验证与准入](references/step-06-verify-output.md)
- [按需补充维度](references/reverse-extension-pack.md)
