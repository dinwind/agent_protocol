# ADR 007: IDE 全局上下文与协议权威性

**状态**: 已接受 (Accepted)  
**日期**: 2026-02-13

---

## 1. 问题

Claude、Cursor 等 IDE 会使用**全局/用户级**的上下文存储（规则、技能、记忆）。导致：

- 部分上下文来自 IDE 或用户应用目录，**不在当前项目目录**；
- 与当前项目的 `.agent/` 协议混在一起，信息脱离 Agent Protocol，产生**信息混乱**和优先级不清。

---

## 2. 改进措施与评估

### 2.1 在 agent-protocol.mdc 里写清「本仓库优先」

**做法**：在生成出的 `agent-protocol.mdc` 正文**最前面**加一段（或加粗一句）：

- 中文示例：「本规则仅适用于当前仓库。项目相关的上下文与约定以本仓库内 `.agent/` 为准；若与用户级/全局 Cursor 规则冲突，以本仓库 .agent 协议为准。」
- 或英文：「For this project, rules under `.agent/` and this file are the single source of truth; user/global IDE rules are for editor behavior only.」

**评估**：

| 维度 | 结论 |
|------|------|
| 有效性 | 高。直接约束模型：冲突时以本仓库 .agent 为准，减少混用全局规则的歧义。 |
| 成本 | 低。仅在生成内容中增加 1–2 句，不改变 IDE 行为，不增加运行时依赖。 |
| 副作用 | 无。不禁止全局规则，只明确优先级。 |
| 一致性 | 与协议「引擎-实例分离」「.agent 为项目权威」一致。 |

**结论**：**建议实施。** 实际落点在 **cokodo-agent 的 generator**（生成 `.cursor/rules/agent-protocol.mdc` 的代码），在输出正文最前插入权威性说明；若需中英兼顾可各保留一句或二选一（推荐英文以与现有 mdc 一致）。

---

### 2.2 在协议/使用指南里写「推荐用法」

**做法**：在使用指南（及可选 start-here）中增加一条建议：

- 使用 .agent 协议时，尽量不在 Cursor/IDE 的「用户级/全局规则」里放与**当前项目强相关**的约定；
- 或明确说明「本项目仅用项目内 `.cursor/rules` 与 `.agent`」。

**评估**：

| 维度 | 结论 |
|------|------|
| 有效性 | 中。从使用方式上减少干扰源，但依赖用户阅读并遵守。 |
| 成本 | 低。使用指南加一小节或几行；start-here 可加一句简短提示。 |
| 副作用 | 无。属建议，不强制。 |
| 一致性 | 与「适配层尽量薄、项目内规则为准」一致。 |

**结论**：**建议实施。** 在使用指南（如 `docs/usage-guide_cn.md`）中增加「与 IDE 全局规则配合」或「推荐用法」类小节；start-here 可加一句「使用 IDE 时建议仅依赖本仓库 .cursor/rules 与 .agent」。

---

### 2.3 适配器模板里加「权威性」说明

**做法**：在 `adapters/cursor/rules.template.md` 中加一句与 2.1 等价的「single source of truth」说明，使生成出的 agent-protocol.mdc 自带该说明。

**评估**：

- **实际生成来源**：当前 Cursor 的 `agent-protocol.mdc` 内容由 **cokodo-agent 的 generator.py** 内联生成，并非从 `.agent/adapters/cursor/rules.template.md` 读取。因此：
  - 若只在 `.agent` 的 template 中加文，**不会**改变已生成文件内容；
  - 要生效必须在 **generator 的输出**中加入权威性说明（即与 2.1 同一处）。
- 将 template 与 generator 输出**同步**更新，可让模板成为「应生成内容」的文档与参考，便于维护。

**结论**：**与 2.1 合并实施。** 在 generator 中加权威性说明（2.1）；同时更新 `.agent/adapters/cursor/rules.template.md`，使其与生成内容一致，作为参考模板。

---

## 3. 综合结论与实施顺序

| 措施 | 评估结论 | 实施位置 |
|------|----------|----------|
| 在 agent-protocol.mdc 中写清「本仓库优先」 | 建议实施 | cokodo-agent `generator.py` 中 `_generate_cursor_adapter` 输出正文最前 |
| 使用指南中写「推荐用法」 | 建议实施 | `docs/usage-guide_cn.md`（及可选 `usage-guide.md`、start-here 一句） |
| 适配器模板加权威性说明 | 与 2.1 合并 | generator 输出 + `.agent/adapters/cursor/rules.template.md` 同步 |

**实施顺序建议**：

1. 修改 **generator.py**：在 Cursor 适配器生成内容正文最前插入权威性段落（中或英，与现有 mdc 风格一致）。
2. 更新 **.agent/adapters/cursor/rules.template.md**：加入相同权威性说明，与生成结果一致。
3. 在 **usage-guide_cn.md**（及可选英文指南、start-here）中增加「与 IDE 全局规则配合」的推荐用法说明。

---

## 4. 与 Claude/Copilot/Gemini 的扩展

同一原则适用于其他 IDE：在 CLAUDE.md、AGENTS.md、GEMINI.md 等入口文件**开头**可加类似一句：

- 「本项目以本仓库内 `.agent/` 为唯一项目规则来源；用户/全局配置仅作环境与编辑器行为使用。」

可在后续适配器迭代中按需加入。

---

*本 ADR 仅评估「本仓库优先」与「推荐用法」方案；Session init（先读 start-here 等）的改进见单独讨论或 ADR。*
