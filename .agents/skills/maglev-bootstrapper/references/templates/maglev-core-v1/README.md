# maglev-core-v1 Reality Profile

此模板为 Maglev 仓库创建固定的 Reality 知识库骨架。

初始化器必须复制 `00_profile.yaml`，再按其中的 domains、domain_entry_files 和 crosscutting_entry_files 创建所有路径。
业务 domain 的固定入口包含 `README.md`、`capability/`、`implementation/`、`interfaces/`、
`operations/`、`verification/` 和 `evidence/`；不能把一个 domain 或模块压缩成同级单文件。
初始化器不得自行增加能力域、槽位或 `INDEX.md` 内容；索引由 index-librarian 生成，额外事实页必须先登记到 Profile 的 `documents` 后写入。
Profile 中的 domains 必须由 `domain_registry` 说明业务边界、`boundary_basis` 和证据引用。
仓库、submodule 或 package 只能登记为 `source_units`，不能直接成为 domain。

对存量 Reality，先使用迁移清单映射已证实事实，再创建骨架并迁移；不能确认的事实保持 unknown，不把旧目录原样复制为新结构。
