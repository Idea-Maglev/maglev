---
description: maglev-reverse-spec Step 8 - Verify Output
---

# Step 8: Verify Output (产出验证)

## 目标
作为 Quality Gate，验证 reality 产物是否完整、可追溯、可交接，而不是只检查文件存在。

## 验证逻辑

### 1. 输出目标确认
根据当前仓库形态确定目标路径：
- Maglev 仓库: `specs/10_reality/{module_slug}/`
- 非 Maglev 仓库: 使用用户或项目约定的等价路径

### 2. 核心文件检查
检查以下文件或等价产物是否存在：
- [ ] `00_index.md` (索引)
- [ ] `01_requirements.md` (核心需求)
- [ ] `02_design.md` (设计)
- [ ] `context/input_facts.md` 或等价事实档案

### 3. 证据与未知项检查
- [ ] 关键断言是否有文件引用
- [ ] 推断是否被标注为 Hypothesis / Inference
- [ ] 未知项是否进入 Quest / Expert Queue

### 4. 深度增强检查
如果本轮目标是支持后续开发、重构或审计，则还应检查：
- [ ] `03_rmm_scorecard.md`
- [ ] `99_expert_review_queue.md`
- [ ] 关键路径是否覆盖 13 点鲁棒性问题

### 5. 归档检查
检查 Facts 是否已成功归档，且输出路径中没有丢失中间证据。

### 6. 越界行为检查
- [ ] 本轮 reverse 是否没有直接修改业务代码
- [ ] 本轮 reverse 是否没有新增回填/修复/迁移类脚本作为“顺手修复”
- [ ] 本轮 reverse 是否没有执行数据修复、契约修复或其他改变现状的动作
- [ ] 如存在修复建议，是否已与 reality 产物明确分离

## 最终报告

### Pass (通过)
如果核心文件与证据链完整：
```
[SUCCESS - Quality Gate Passed]
🎉 reality 校验圆满完成！

📍 产出位置: specs/10_reality/{module_slug}/
✅ 核心文件: 完整
✅ 证据链: 可追溯
✅ 上下文归档: 完整
✅ 未知项: 已登记
✅ 执行边界: 未越界到业务修复

您可以随时开始下一个功能逆向。
```

### Fail (失败)
如果有文件、证据或归档缺失：
```
[WARNING - Archival Incomplete]
⚠️ 检测到 reality 产物不完整！

缺失项:
- {Missing File Name}
- {Missing Evidence or Queue}
- {Mutation or Remediation Leak}

建议: 请检查 spec handoff、crystallize 或 reality boost 阶段是否执行完整。
```
