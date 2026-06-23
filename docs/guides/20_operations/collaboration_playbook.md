# 协作实战手册 (Collaboration Playbook)

本文档是 **“铁三角”角色** 在 **“全资产同仓”** 模式下的实战操作指南。
请所有参与者（VO, TP, XG）将其视为**标准作业程序 (SOP)**。

## 1. 环境准备 (Environment Setup)

### 1.1 工具链
- **IDE**: 推荐 VS Code / Cursor (必须安装 AI 插件)。
- **Git Client**: 命令行或 GUI，必须熟练使用 `pull`, `commit`, `push`。
- **Repo 权限**: 三角色均需拥有 `Write` 权限 (主干开发或短分支模型)。

### 1.2 本地工作区
```bash
# 所有角色检出同一个 Repo
git clone git@github.com:company/project-maglev.git
cd project-maglev
# 确保目录结构完整
ls -F # 应看到 src/, specs/, issues/, design/, tests/
```

---

## 2. 场景演练：开发“用户登录”功能 (Scenario Run)

以下是完成一个 Feature 的完整微操流程。

### Step 1: 意图定义 (VO Action)
**角色**: Value Owner
1.  在 `specs/stories/` 下新建 `login_feature.md`。
2.  **编写内容** (Markdown):
    ```markdown
    # 用户登录功能
    ## 核心价值
    用户可以通过手机号+验证码登录，以便保存个人数据。
    
    ## 验收标准 (Acceptance Criteria)
    - [ ] 输入非法手机号应实时提示错误（红色文字）。
    - [ ] 发送验证码后，按钮进入 60s 倒计时。
    - [ ] 登录成功后跳转至首页。
    
    ## 参考设计
    > [点击查看 Figma 设计稿](https://figma.com/...)
    > (或者直接粘贴一张手绘草图截图)
    ```
3.  **操作**: `git add specs/stories/login_feature.md`, `git commit -m "feat(spec): add login intent"`

### Step 2: 智能构建 (TP Action)
**角色**: Tech Pilot
1.  **拉取需求**: `git pull`，阅读 `specs/stories/login_feature.md`。
2.  **Prompting (在 IDE 中)**:
    - 打开 Chat 窗口，引用 `@login_feature.md` 和 `@design/tokens.json`。
    - 输入 Prompt: *"基于这个需求文档和设计规范，请生成 React 登录组件。使用 Tailwind CSS。"*
3.  **生成与微调**:
    - AI 生成代码至 `src/components/Login.tsx`。
    - **TP 介入**: 发现 AI 漏了“60s 倒计时”的逻辑，进行手动补全或追问 AI。
4.  **本地自测**: 确保编译通过，页面能跑。
5.  **操作**: `git add .`, `git commit -m "feat(dev): implement login basic logic"`

### Step 3: 体验验收 (XG Action)
**角色**: Experience Guardian
1.  **拉取代码**: `git pull`，运行项目 (e.g., `npm run dev`)。
2.  **探索性测试**:
    - 尝试输入 "123" (非法手机号)，发现提示文字是黑色的，不是设计要求的红色。
3.  **提 Bug**:
    - 复制 `solutions/templates/issues/bug_template.md` 到 `issues/active/20260118-fix-LoginStyle.md`。
    - **填写内容**:
        ```markdown
        # Bug: 手机号错误提示颜色不对
        ## 1. Reproduction Steps
        1. 输入 "123"
        2. 观察提示文字颜色
        
        ## 2. Expected Behavior
        红色文字 (#FF0000)
        
        ## 3. Actual Behavior
        黑色文字
        ```
4.  **操作**: `git add issues/`, `git commit -m "test(bug): report login style issue"`

### Step 4: 快速修复 (TP Action)
1.  TP 看到 Commit 或被通知。
2.  直接把 `20260118-BUG-LoginStyle.md` 喂给 AI: *"Fix this bug in Login.tsx"*。
3.  AI 修正代码。
4.  TP 验证无误后 Commit。
5.  TP 将 Issue 文件移动到 `issues/closed/` 目录。

---

## 3. 协作协议 (Protocols)

### 3.1 Commit Message 规范
为了配合 AI 理解历史，Commit 信息必须语义化：
- `feat(spec)`: VO 提交需求
- `feat(dev)`: TP 提交代码
- `test(bug)`: XG 提交 Bug
- `fix(dev)`: TP 修复 Bug

### 3.2 冲突处理 (Conflict Resolution)
- 由于大家都在改同一个 Repo，难免遇到冲突。
- **原则**: 
    - 文档类冲突 (`specs/`, `issues/`)：通常是追加内容，Git 会自动合并，手动修一下即可。
    - 代码类冲突 (`src/`)：**必须由 TP 解决**。VO 和 XG 不要尝试解决代码冲突。

---

## 4. 危机处理 (Crisis Management)

### 当 AI "发疯" (Hallucination) 时...
- **现象**: AI 生成的代码完全跑不通，或者逻辑胡编乱造。
- **熔断机制**: 
    1.  TP 停止 Prompting，不要试图“说服”AI。
    2.  TP **手动接管**控制权，回退到上一个稳定版本。
    3.  TP 分析原因：通常是 Context 太长或 Spec 描述矛盾。
    4.  VO 配合修改 Spec，简化描述；或者 TP 将大任务拆解为小任务 (Chain of Thought)。

---

## 总结
**手中有剑，心中有谱。**
这份手册是团队协作的底线。任何超出此手册的即兴发挥，都应在事后通过 Retrospective (复盘) 更新到本手册中。
