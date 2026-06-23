# migration shape decision v1

> 状态：已完成
> 作用：为主流程核心四对象确定未来 rename execution 的迁移形态。

## 1. 候选方案

1. `skill-only`
2. `skill + workflow`

## 2. 当前判断

当前更适合采用：

> `skill-only`

## 3. 选择理由

### A. workflow 已经具备较强的历史入口价值

当前：

- `standup.md`
- `create-spec.md`
- `quick-dev.md`
- `validate-all.md`

已经不只是内部文件名，而是带有用户习惯与操作记忆的历史入口。

若当前连 workflow 一起改，会明显放大迁移成本。

### B. 当前核心矛盾在 skill 运行名，不在 workflow 表述

现在 workflow 描述层已经可以通过双写兼容处理。

真正还处于 `active_legacy_name` 治理问题中心的，是 skill 运行名本身。

### C. `validate-all.md` 与正式动作名并不一一对应

四个 workflow 中，`validate-all.md` 本身就是历史命令式入口，而不是对象名直译。

这说明 workflow 命名体系和 skill 命名体系并不需要强绑定同步迁移。

## 4. 当前结论

未来若进入 rename execution，当前推荐顺序是：

1. 先执行 `skill-only`
2. workflow 文件名继续兼容保留
3. 若未来真的需要，再单独开 workflow rename 主题

## 5. 当前不建议

当前不建议：

1. skill 与 workflow 一起改
2. 把 workflow 文件名视作必须同步迁移项
3. 在本轮 preflight 就提前决定 workflow 也必须 rename
