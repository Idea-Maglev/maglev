# naming governance rule v1

> 状态：已形成首版规则
> 作用：固化 Maglev 当前 runtime naming 的长期治理规则。

## 1. 四层名字的职责边界

### A. `formal_action_name`

定义：

- 给人理解的正式动作名

用途：

1. 面向用户解释“这是什么动作”
2. 出现在技能说明、Reality、guides、marketing 等面向人的文案里

要求：

1. 使用自然语言动作表达
2. 优先服务“人理解”，不是服务系统引用

### B. `skill runtime name`

定义：

- 运行面真实对象名

用途：

1. skill 目录名
2. `SKILL.md` 中的 `name`
3. catalog 中 skill 对象的 `name`

要求：

1. 必须是仓库内该对象的唯一运行标识
2. 一旦切换，catalog `name`、skill 目录、skill 文件头必须同轮同步

### C. `workflow filename / slash entry`

定义：

- 面向使用的入口名

用途：

1. `.agents/workflows/*.md`
2. slash command 习惯入口
3. 教学、导航、排障中的“怎么触发”

要求：

1. 可以与 skill runtime name 不同
2. 若不同，必须显式标注为“兼容入口”
3. 不得被误写成当前 skill runtime name

### D. `catalog relation target`

定义：

- 系统内部关系引用名

用途：

1. `.agents/private-catalog.yaml` 中的 `relations.target`
2. 对象间调用关系与治理关系

要求：

1. 必须始终指向当前 active 的 skill runtime name
2. 不允许继续指向历史 skill runtime name
3. 不允许直接指向 workflow filename

## 2. 允许保留的差异

当前明确允许：

1. `formal_action_name` 与 `skill runtime name` 不同
2. `workflow filename / slash entry` 与 `skill runtime name` 不同

只要满足以下条件，这种差异就是合法的：

1. skill 文档写清当前 runtime name
2. workflow 文档写清“兼容入口”语义
3. Reality / guides / tutor 不混淆三层名字

## 3. 必须同轮同步的修改

若修改 `skill runtime name`，以下对象必须同轮同步：

1. skill 目录名
2. `SKILL.md` 里的 `name`
3. `metadata.runtime_name_status`
4. `.agents/private-catalog.yaml` 中该 skill 的：
   - `name`
   - `path`
   - 所有相关 `relations.target`

若不同步，视为结构错误，而不是文档欠账。

## 4. 双写兼容的使用边界

只有以下情况允许双写兼容：

1. runtime rename 迁移期
2. workflow 入口保留期
3. 面向用户解释历史入口时

双写兼容必须满足：

1. 新名优先
2. 旧名只作为历史或兼容说明出现
3. 不能让读者误判哪个是当前 active 名

## 5. 应阻断的命名请求

以下请求默认应阻断：

1. 只改 skill 文档显示名，不改 catalog `name/path/relations.target`
2. 把 workflow filename 当成系统内部关系引用名
3. 为追求整齐而强推 workflow 与 skill 同名
4. 新对象同时引入多个未分层解释的名字
5. 在用户文档中混写“当前 runtime name”和“历史入口”而不做说明

## 6. 对新对象的默认要求

新对象进入仓库时，至少要一次性回答：

1. `formal_action_name` 是什么
2. `skill runtime name` 是什么
3. 是否需要独立 workflow 入口
4. 若需要 workflow，入口名是否刻意与 runtime name 分离
5. catalog relation target 应该引用哪个名字

## 7. 当前白名单原则

当前允许长期保留的差异白名单：

1. 主流程四对象：
   - skill runtime name 使用新名
   - workflow 入口保留旧 slash 名
2. 文档中的“历史入口”说明
3. execution / migration / strategy 主题中的过程差异记录
