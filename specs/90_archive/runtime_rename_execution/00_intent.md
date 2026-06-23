# runtime rename execution Intent

## 目标

为主流程核心四对象的 `skill-only` rename execution 形成一份可以直接执行的规格，避免后续进入物理改名时还要再次临场决定顺序、验证方式和回滚边界。

## 本轮只处理

1. `skill-only` 执行顺序
2. 验证方式
3. 回滚边界

## 本轮不处理

1. 直接修改 skill 目录名
2. 直接修改 `.agents/private-catalog.yaml`
3. 直接切换 `runtime_name_status`
