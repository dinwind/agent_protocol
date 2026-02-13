# ADR 005: UTF-8 规则收敛与命名规则兼容性确认

**状态**: 草案 (Proposed)  
**日期**: 2026-02-13

---

## 1. 目标

- 将分散在多处的 UTF-8 规则收敛到单一权威来源，减少重复与日后分歧。
- 确认协议命名规则与 Cursor / Claude / Copilot / Gemini 的官方命名要求无冲突。

---

## 2. 命名规则与第三方 IDE 兼容性结论

### 2.1 协议侧命名规则（当前）

- **core-rules.md §3.2**、**conventions.md §1**：`.agent/` 目录下所有 Markdown 与目录使用 **kebab-case**（小写 + 连字符），无例外。
- 适用范围：仅针对 **`.agent/` 目录内部** 的文件与目录名。

### 2.2 各 IDE 官方要求（依据公开文档）

| IDE | 规约文件位置与名称 | 官方要求 | 与协议关系 |
|-----|-------------------|----------|------------|
| **Cursor** | `.cursor/rules/*.mdc` | 推荐 **kebab-case** 命名（如 `agent-protocol.mdc`） | 一致。我们生成 `agent-protocol.mdc`，符合 Cursor 推荐。 |
| **Claude Code** | 项目根或 `.claude/` | 文件名须为 **`CLAUDE.md`**（全大写） | 无冲突。协议不规定项目根文件名；生成器按官方要求输出。 |
| **GitHub Copilot** | 项目根或 `.github/` | **`AGENTS.md`** 或 `.github/copilot-instructions.md`、`.github/instructions/*.instructions.md` | 无冲突。协议不规定项目根；生成器按官方命名。 |
| **Gemini** | 项目根等 | 默认 **`GEMINI.md`**（全大写）；可配置为 AGENTS.md、CONTEXT.md 等 | 无冲突。生成器使用默认名。 |

### 2.3 结论

- **无冲突**。协议命名规则只约束 **`.agent/` 内部**；各 IDE 规约文件在项目根或 `.cursor/`、`.github/` 下，命名按各厂商要求，由 cokodo-agent 生成器保证一致。
- **建议**：在 `core/conventions.md` 或 `meta/agent-protocol-rules.md` 中增加一句说明：「本协议命名规则仅适用于 `.agent/` 目录内；各 AI IDE 的入口文件命名遵循各厂商规范，由适配器生成器负责。」

---

## 3. UTF-8 规则收敛：具体修改草案

### 3.1 权威定义保留（两处）

**A. core/core-rules.md**

- **§3.1 编码标准**（保留，可微调措辞）  
  - 条文：所有源码与配置文件必须使用 UTF-8；读写文件时必须**显式指定** encoding 为 UTF-8。  
  - 保留指向：「实现示例见 [core/examples.md](../../core/examples.md#1-utf-8-explicit-encoding)」。  
- **§4.3 终端编码**（保留）  
  - 条文：终端输出必须使用 UTF-8，避免非 ASCII 显示问题。  
  - 保留指向：「终端设置示例见 [core/examples.md](../../core/examples.md#3-terminal-utf-8-setup)」。  
- **§5 交付清单**（保留）  
  - 保留「explicit UTF-8 encoding」检查项，不展开。

**B. core/examples.md**

- **§1 UTF-8 Explicit Encoding**（保留）  
  - 继续作为**唯一**文件读写编码示例（Python / Rust / PowerShell）。  
- **§3 Terminal UTF-8 Setup**（保留）  
  - 继续作为**唯一**终端/控制台 UTF-8 设置示例（PowerShell / Bash）。  

以上两处为「权威定义 + 示例」，其余文件仅引用，不重复条文或示例。

---

### 3.2 改为引用的文件（删除本地重复，改为一句引用）

**C. core/instructions.md**

- **当前**：§2 有「Core requirement: Explicitly specify UTF-8 encoding, never omit. See [core/examples.md](../../core/examples.md).」  
- **修改**：保留一句，并明确指向 core-rules：  
  - 「文件编码与终端输出须符合 [core/core-rules.md](../../core/core-rules.md) §3.1、§4.3；实现与终端设置示例见 [core/examples.md](../../core/examples.md)。」  
- **删除**：无（已是简短要求 + 链接）。

**D. core/workflows/bug-prevention.md**

- **当前**：§ Encoding Issues / BUG-001 含根因、预防及多行代码示例。  
- **修改**：  
  - 保留 BUG-001 标题与症状、根因、预防**一句话**（「读写文件时必须显式指定 encoding，见 [core-rules §3.1](../../core/core-rules.md) 与 [examples §1](../../core/examples.md#1-utf-8-explicit-encoding)。」）。  
  - **删除** 本文件内的 Python 正确/错误代码块（约 6 行），避免与 examples.md 重复。

**可直接替换的 BUG-001 段落示例：**

```markdown
## Encoding Issues

### BUG-001: File Read/Write Encoding Error

**Symptoms**: Garbled characters, `UnicodeDecodeError`  
**Root cause**: Not specifying encoding when opening files  
**Prevention**: Always explicitly specify `encoding='utf-8'`. See [core-rules §3.1](../../core/core-rules.md) and [examples §1](../../core/examples.md#1-utf-8-explicit-encoding).
```

**E. core/workflows/design-principles.md**

- **当前**：示例代码中有 `path.read_text(encoding='utf-8')`。  
- **修改**：在该示例旁加一句注释或括号说明：「（文件编码须符合 [core-rules §3.1](../../core/core-rules.md)，示例见 [examples](../../core/examples.md)。）」  
- **是否删除该行示例**：可不删，仅加引用说明，以保持本工作流内示例自洽。

**F. core/stack-specs/python.md**

- **当前**：§4 File Operations 有「# ✅ Always specify encoding」及 `with open(..., encoding='utf-8')`。  
- **修改**：  
  - 保留「Always specify encoding」标题与一行示例（或改为「见 [core/examples.md](../../core/examples.md)」）。  
  - 在段落首加一句：「遵循 [core 编码规则](../../core/core-rules.md) §3.1。」  
  - 若希望进一步精简，可删除本文件内多行 open 示例，仅保留一句 + 链接到 examples.md。

**G. core/security.md**

- **当前**：示例中有 `file_path.read_text(encoding='utf-8')`。  
- **修改**：在该示例附近加一句：「（编码规范见 [core-rules](../../core/core-rules.md) §3.1 与 [examples](../../core/examples.md)。）」  
- 不强制删除该行，保留示例并注明出处即可。

---

### 3.3 适配器模板（.agent/adapters/）

- **当前**：`adapters/github-copilot/instructions.template.md`、`adapters/cursor/rules.template.md` 等含「encoding='utf-8'」或「Encoding: Always encoding='utf-8'」。  
- **说明**：实际输出已由 cokodo-agent 的 generator 生成，协议仓库内模板多为参考或兼容旧流程。  
- **修改建议**：  
  - 若保留模板：将 UTF-8 条改为一句「文件与终端编码须符合 .agent 协议（见 .agent/core/core-rules.md 与 .agent/core/examples.md）。」  
  - 或：在模板中仅保留「遵循 .agent 核心规则（含编码）」类概括，不重复具体 encoding 写法。  

（具体改哪几个模板、是否删除重复句，可按仓库当前是否仍从这些模板拷贝决定。）

---

### 3.4 可选：conventions 与 core-rules 命名约定去重

- **当前**：core-rules.md §3.2 与 conventions.md §1 均规定 .agent 下 kebab-case。  
- **修改**：  
  - 在 **core-rules.md §3.2** 保留完整规定（含表格）。  
  - 在 **conventions.md §1.1** 改为：「协议目录下命名规范见 [core-rules §3.2](../../core/core-rules.md)。」并保留 conventions 中**源码目录**（Source Code Directory）及语言风格（Python/Rust/C++）的约定，避免与 core-rules 重复描述同一张 kebab-case 表。

---

## 4. 修改清单汇总

| 序号 | 文件 | 操作 |
|------|------|------|
| 1 | core/core-rules.md | 保持 §3.1、§4.3、§5 现状；可微调「见 examples」链接文案。 |
| 2 | core/examples.md | 保持 §1、§3 为唯一编码与终端示例，不删减。 |
| 3 | core/instructions.md | §2 改为明确引用 core-rules §3.1/§4.3 + examples。 |
| 4 | core/workflows/bug-prevention.md | BUG-001 保留症状/根因/预防一句，删除本地 Python 代码块，增加指向 core-rules 与 examples 的链接。 |
| 5 | core/workflows/design-principles.md | 在含 read_text(encoding='utf-8') 的示例旁加「见 core-rules §3.1、examples」说明。 |
| 6 | core/stack-specs/python.md | §4 加「遵循 core 编码规则」引用；可选：缩为一句+链接，删本地多行示例。 |
| 7 | core/security.md | 在 read_text(encoding='utf-8') 示例旁加「见 core-rules、examples」说明。 |
| 8 | adapters/* (模板) | UTF-8 条改为「遵循 .agent 核心规则（含编码）」或保留一句引用，不重复 encoding 写法。 |
| 9 | core/conventions.md | §1.1 协议目录命名改为引用 core-rules §3.2，避免重复 kebab-case 表格。 |
| 10 | meta/agent-protocol-rules.md 或 conventions | 新增一句：协议命名规则仅适用于 .agent/ 内；IDE 入口文件命名遵循各厂商规范。 |

---

## 5. quick-reference 与 essential 层（可选）

- 若存在 `quick-reference.md` 且与 start-here、core-rules 重复较多：可考虑合并进 start-here 的「速查」小节，或将 quick-reference 从 essential 改为 on_demand，以控制 token。  
- 若当前仓库无 quick-reference.md：在 manifest 的 essential 层中移除该条目，或保留条目待后续补文件，避免加载报错。

---

## 6. 实施顺序建议

1. 命名兼容性说明（第 2 节结论 + 第 4 节序号 10）— 先加说明，无需改生成器。  
2. core 内收敛（序号 1–7）：先 core-rules / examples 不动，再改 instructions、bug-prevention、design-principles、python.md、security。  
3. conventions 与 core-rules 去重（序号 9）。  
4. adapters 模板（序号 8）按实际使用情况决定是否改、改哪些。  
5. quick-reference / manifest（第 5 节）视仓库现状再动。

---

*本 ADR 为修改草案，实施时需同步更新 manifest 中涉及文件的 checksum（若有）。*
