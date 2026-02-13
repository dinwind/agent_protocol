# ADR 006: 规约适用范围与 Emoji 审核

**状态**: 已实施  
**日期**: 2026-02-13

---

## 1. 审核目的

确认 .agent 规约中是否存在「适用范围」歧义（仅 .agent 内 vs 整个项目），并统一表述；同时检查是否符合 core-rules §3.4（优先 ASCII、不用 emoji）。

---

## 2. 适用范围审核结论

### 2.1 已明确或无疑义

| 文件/条文 | 适用范围 | 说明 |
|-----------|----------|------|
| core-rules §3.1 Encoding | 全项目 | 已注明 Scope: entire project |
| core-rules §3.4 No emoji | 全项目 | 已注明 Scope: entire project |
| core-rules §3.2 File Naming | 仅 .agent | 明确 "under .agent directory" |
| core-rules §3.3 Rule Consistency | 全项目 | "all files... in project" |
| core-rules §1 Three Prohibitions | 全项目 | "All resources", "All UI changes" 等 |
| core-rules §2 ILI | .agent 结构与约束 | 整节描述 .agent |

### 2.2 已补充或建议补充 Scope 的条文

| 文件/条文 | 实际适用范围 | 修改 |
|-----------|--------------|------|
| core-rules §4.3 Terminal Encoding | 全项目（所有终端输出） | 增加 Scope: entire project |
| conventions.md | §1.1 仅 .agent；§1.2 及以下全项目 | 文首或节内注明 |
| instructions.md | 全项目（开发协作） | 注明适用全项目开发 |
| workflows/bug-prevention.md | 全项目（源码、测试、配置） | 文首增加 Scope |
| workflows/design-principles.md | 全项目（架构与代码设计） | 文首增加 Scope |
| core/security.md | 全项目（涉输入/认证/敏感数据代码） | 文首增加 Scope |
| stack-specs/*.md | 全项目（对应语言所有文件，见 core-rules §3.3） | 各 spec 增加一句 Scope |
| workflows/token-budget.md | 仅 .agent 协议文档 | 注明 Scope: .agent protocol only |

---

## 3. Emoji 使用审核（§3.4）

- **core/** 下多处在代码示例或表格中使用 `# ✅` / `# ❌` 或表格列名「Correct ✅」「Wrong ❌」，与 §3.4 冲突。
- **已处理**：conventions.md 表格、bug-prevention / design-principles / security 及 stack-specs 中代码注释改为 `# Correct` / `# Wrong` 或 `[OK]` / `[X]`；core-rules 表格已为 [OK]/[X]。
- **未改**：meta/、project/、templates/ 中中文说明或占位符用 emoji（如 🔒、✅❌）——若规约解释为「§3.4 主要约束 core 交付物」，可保留或后续统一。

---

## 4. 实施清单

- [x] core-rules §4.3 增加 Scope
- [x] conventions.md 增加 §1.1/§1.2 适用范围说明，表格改用 [OK]/[X]
- [x] instructions.md 增加 Scope 一句
- [x] bug-prevention / design-principles / security 文首增加 Scope，代码示例中 ✅❌ → Correct/Wrong
- [x] stack-specs (python, rust, qt, git) 增加 Scope 一句
- [x] token-budget 增加 Scope: .agent only
- [x] core 内 emoji 替换为 ASCII（conventions 表、workflows、security、stack-specs、examples）
