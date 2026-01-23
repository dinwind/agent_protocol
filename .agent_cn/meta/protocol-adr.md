# AI 协议层架构决策记录 (Protocol ADR)

本文件记录 AI 协议层（Intelligence Layer）本身的开发、演进与架构决策。该协议层被视为一个独立于业务项目的数字资产。

> 📦 **历史 ADR 归档**: 基础架构决策 (ADR-001 ~ ADR-006) 已归档至 [adr-archive.md](adr-archive.md)

---

## 当前有效 ADR

| ADR | 名称 | 状态 |
|-----|------|------|
| [ADR-007](#adr-007) | kebab-case 零例外命名 | 已实施 |
| [ADR-008](#adr-008) | 技能模块架构 | 已实施 |
| [ADR-009](#adr-009) | AI/LLM 集成技能 | 已实施 |
| [ADR-010](#adr-010) | AI 工具适配器模式 | 已实施 |
| [ADR-011](#adr-011) | 模板变量与初始化脚手架 | 已实施 |
| [ADR-012](#adr-012) | 协议统一合并 | 已实施 |
| [ADR-013](#adr-013) | 协议增强与工程化 | 已实施 |
| [ADR-014](#adr-014) | SKILL.md 标准化 | 已实施 |

---

<a id="adr-007"></a>
## ADR-007: kebab-case 零例外命名 (Zero-Exception Kebab-Case Naming)

### 状态
已实施

### 日期
2026-01-09

### 决策
1. `.agent` 目录下**所有** markdown 文件必须使用 kebab-case（小写字母+连字符）
2. **零例外**原则：任何例外都会导致混乱，因此不允许任何特殊情况
3. 仅有极少数元数据文件例外：`MANIFEST.json`, `VERSION`, `SKILL.md`

> **2026-01-23 更新**: 添加 `SKILL.md` 为例外，以兼容 [agentskills.io](https://agentskills.io) 开放标准。详见 ADR-014。

### 后果
- 100% 的命名一致性
- 与主流 AI 工具的 Skills 标准兼容

---

<a id="adr-008"></a>
## ADR-008: 技能模块架构 (Skill Module Architecture)

### 状态
已实施

### 日期
2026-01-12

### 决策
1. **引入 Skills 概念**：在 `.agent/skills/` 下创建独立的技能模块目录
2. **标准技能结构**：
   ```
   skills/{skill-name}/
   ├── SKILL.md          # 技能说明书（输入/输出/使用方式）
   ├── prompts/          # 相关提示词模板
   └── scripts/          # 配套脚本（可选）
   ```

### 后果
- 实现了 AI 能力的模块化封装
- 技能可独立演进、测试和复用

---

<a id="adr-009"></a>
## ADR-009: AI/LLM 集成技能模块化 (AI/LLM Integration Skill Modularization)

### 状态
已实施

### 日期
2026-01-16

### 决策
1. **技能模块化**：在 `skills/ai-integration/` 创建独立的 AI 集成技能模块
2. **三层文档结构**：
   - `llm-client.md` - 客户端设计规范
   - `prompt-engineering.md` - Prompt 工程规范
   - `domain-adaptation.md` - 领域适配方法论

### 后果
- AI 集成经验成为可复用资产
- 新项目可直接参考，避免重复踩坑

---

<a id="adr-010"></a>
## ADR-010: AI 工具适配器模式 (AI Tool Adapter Pattern)

### 状态
已实施

### 日期
2026-01-19

### 决策
1. **引入 `.agent/adapters/` 目录**：专门存放各主流 AI 工具的配置模板
2. **指针策略 (Pointer Strategy)**：
   - 真正的规则保留在 `.agent/start-here.md` 及核心层
   - 工具配置文件仅充当**连接器 (Connector)**

### 后果
- 实现了协议栈对 AI 工具的"零侵入"
- 确立了 `.agent` 作为单一真实数据源 (SSOT) 的地位

---

<a id="adr-011"></a>
## ADR-011: 模板变量与初始化脚手架 (Templates & Initializer)

### 状态
已实施

### 日期
2026-01-19

### 决策
1. **Scope 限制**：模板变量（`{{...}}`）**仅限**在 `adapters/` 目录下的模板文件中使用
2. **初始化脚本**：引入 `scripts/init_agent.py` 作为协议的"编译器/脚手架"

### 后果
- 保持了核心文档 Human-Readable 的特性
- 实现了项目的自动化初始化

---

<a id="adr-012"></a>
## ADR-012: 协议统一合并 (Protocol Unification & Merge)

### 状态
已实施

### 日期
2026-01-23

### 决策
1. **目录命名统一**：采用 `.agent/` 作为标准目录名
2. **超集合并策略**：共性内容直接采用，差异内容取并集
3. **技能模块重组**：统一 code-guardian 和 content-guardian 为 `guardian/`

### 后果
- 协议层版本统一为 2.0.0
- 支持 Python/Rust/Qt/C++ 多技术栈
- 技能模块可按需加载

---

<a id="adr-013"></a>
## ADR-013: 协议增强与工程化 (Protocol Enhancement & Engineering)

### 状态
已实施

### 日期
2026-01-23

### 决策
1. **引入 manifest.json**：定义协议加载策略和 Token 预算
2. **AI 能力边界明确化**：在 `instructions.md` 中定义自主性级别
3. **安全规范集中化**：创建 `core/security.md`
4. **技能接口标准化**：创建 `skills/skill-interface.md`
5. **CI/CD 集成模板**：在 `adapters/ci/` 添加工作流模板
6. **快速参考卡片**：创建 `quick-reference.md`

### 后果
- 协议层版本升级至 2.1.0
- 加载策略可量化配置
- 新手上手更快（速查卡片）

---

<a id="adr-014"></a>
## ADR-014: Skills 入口文件标准化 (SKILL.md Standardization)

### 状态
已实施

### 日期
2026-01-23

### 决策
1. **采用 `SKILL.md` 作为技能入口文件名**（大写）
2. **更新 ADR-007 例外列表**：添加 `SKILL.md` 到命名例外
3. **理由**：符合 [agentskills.io](https://agentskills.io) 开放标准

### 后果
- 与 Google Antigravity **零适配兼容**
- 与 Claude Agent Skills **零适配兼容**
- 技能可直接跨工具使用

---

## 变更日志

| 日期 | ADR | 变更 |
|------|-----|------|
| 2026-01-23 | ADR-014 | Skills 入口文件标准化为 SKILL.md |
| 2026-01-23 | ADR-013 | 协议增强与工程化，升级至 v2.1.0 |
| 2026-01-23 | ADR-012 | 协议统一合并，升级至 v2.0.0 |
| 2026-01-19 | ADR-011 | 建立模板变量与初始化脚手架机制 |
| 2026-01-19 | ADR-010 | 建立 AI 工具适配器模式 |
| 2026-01-16 | ADR-009 | 建立 AI/LLM 集成技能模块 |
| 2026-01-12 | ADR-008 | 引入 Skills 技能模块架构 |
| 2026-01-09 | ADR-007 | 确立 kebab-case 零例外命名规范 |
| 2026-01-06 | ADR-001~006 | 基础架构决策 → [已归档](adr-archive.md) |

---

*此文件记录协议层自身的演进历史，禁止包含业务项目特定信息*
*协议版本: 2.1.0*
