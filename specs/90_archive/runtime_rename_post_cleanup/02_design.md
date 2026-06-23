# Design

## 1. 处理原则

rename 后旧名残留按四层处理：

1. `运行面残留`
   - 若仍出现在 `.agents/` 现役层、Reality、guides、marketing 主表述中，应视为应清理对象
2. `兼容说明`
   - 若用于解释旧 workflow 入口、历史入口或迁移兼容，应允许保留，但必须显式说明是兼容语义
3. `过程记录`
   - 若存在于 rename strategy / migration / execution 主题，用于记录差异和迁移步骤，应保留
4. `历史与 archive`
   - 若存在于 `docs/thinking/` 或 archive 中，默认按历史记录保留，除非它会误导当前仓库路径事实

## 2. 本主题的主要输出

1. 一份残留 inventory
2. 一份分层判断
3. 一份最小清理建议

## 3. 当前判断边界

当前最应优先清理的，不是 execution 文档中的旧名，而是：

1. active 主题中仍引用旧 skill 路径但会让人误以为当前路径仍存在的说明
2. `docs/thinking/` 中直接链接到已不存在目录的旧路径
3. 未显式标注“兼容入口”却继续使用旧运行名的用户说明
