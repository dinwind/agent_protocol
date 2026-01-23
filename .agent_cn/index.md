# 文档导航索引

> **目的**: 快速定位 AI 协议层各类文档
>
> **注**: `$AGENT_DIR` 指协议根目录（如 `.agent`、`.agent_cn`），实际名称见 `manifest.json`。

---

## 🚀 快速入口

### 新手必读（按顺序）
1. [start-here.md](start-here.md) - ⭐ AI 启动指令（首次必读）
2. [quick-reference.md](quick-reference.md) - 📋 速查卡片（一页纸参考）
3. [core/instructions.md](core/instructions.md) - 协作规则入口
4. [project/context.md](project/context.md) - 项目业务上下文
5. [project/tech-stack.md](project/tech-stack.md) - 技术栈说明

---

## 📋 核心规范文档

### 治理引擎 (core/)
| 文档 | 用途 | 阅读时机 |
|------|------|---------|
| [core-rules.md](core/core-rules.md) | 核心哲学、ILI 隔离、三不原则 | 首次接触 |
| [instructions.md](core/instructions.md) | AI 协作指南、能力边界定义 | 首次接触 |
| [conventions.md](core/conventions.md) | 命名规范、Git 约定 | 提交前 |
| [security.md](core/security.md) | 安全开发规范 ⭐ | 涉及安全时 |

### 工作流 (core/workflows/)
| 文档 | 用途 | 阅读时机 |
|------|------|---------|
| [bug-prevention.md](core/workflows/bug-prevention.md) | Bug 预防知识库 ⭐ | 编码前 |
| [design-principles.md](core/workflows/design-principles.md) | SSOT、依赖注入、简单优先 | 设计时 |
| [testing.md](core/workflows/testing.md) | 测试协议、数据隔离 | 写测试时 |
| [pre-task-checklist.md](core/workflows/pre-task-checklist.md) | 任务预检清单 | 开始任务前 |
| [documentation.md](core/workflows/documentation.md) | 文档编写规范 | 写文档时 |
| [quality-assurance.md](core/workflows/quality-assurance.md) | 质量保证流程 | 交付前 |
| [review-process.md](core/workflows/review-process.md) | 代码审查流程 | PR 前 |

### 技术栈规约 (core/stack-specs/)
| 文档 | 用途 | 适用项目 |
|------|------|---------|
| [python.md](core/stack-specs/python.md) | Python 开发规约 | Python 项目 |
| [rust.md](core/stack-specs/rust.md) | Rust 开发规约 | Rust 项目 |
| [qt.md](core/stack-specs/qt.md) | Qt/C++/QML 开发规约 | Qt 项目 |
| [git.md](core/stack-specs/git.md) | Git 工作流规约 | 所有项目 |

---

## 📋 项目实例 (project/)

| 文档 | 用途 | 更新频率 |
|------|------|---------|
| [context.md](project/context.md) | 项目业务上下文 | 需求变更时 |
| [tech-stack.md](project/tech-stack.md) | 技术栈与环境 | 技术选型时 |
| [known-issues.md](project/known-issues.md) | 已知问题与解决方案 | 发现问题时 |
| [adr/](project/adr/) | 业务架构决策记录 | 重要决策时 |

---

## 🛠️ 技能模块 (skills/)

可复用的自动化能力封装：

| 文档 | 用途 |
|------|------|
| [skill-interface.md](skills/skill-interface.md) | 技能接口规范（开发新技能前必读） |

| 技能 | 功能 | 使用场景 |
|------|------|---------|
| [guardian](skills/guardian/SKILL.md) | 代码/文档质量门禁 | 提交前检查 |
| [ai-integration](skills/ai-integration/) | LLM/AI 服务集成规范 ⭐ | AI 功能开发 |
| [agent-governance](skills/agent-governance/SKILL.md) | 协议健康检查 | 协议维护 |

### AI 集成技能详情 (skills/ai-integration/)
| 文档 | 内容 |
|------|------|
| [llm-client.md](skills/ai-integration/llm-client.md) | LLM 客户端设计模式 |
| [prompt-engineering.md](skills/ai-integration/prompt-engineering.md) | Prompt 工程最佳实践 |
| [domain-adaptation.md](skills/ai-integration/domain-adaptation.md) | 领域适配方法论 |

---

## 📜 协议演进 (meta/)

| 文档 | 用途 |
|------|------|
| [protocol-adr.md](meta/protocol-adr.md) | 协议架构决策记录 |

---

## 🔌 AI 工具适配器 (adapters/)

| 适配器 | 用途 |
|--------|------|
| [github-copilot/](adapters/github-copilot/) | GitHub Copilot 指令模板 |
| [cursor/](adapters/cursor/) | Cursor 配置模板 |
| [claude/](adapters/claude/) | Claude 指令模板 |
| [google-antigravity/](adapters/google-antigravity/) | Google Antigravity Agent 适配 ⭐ |
| [ci/](adapters/ci/) | CI/CD 集成模板 |

---

## 🔧 辅助脚本 (scripts/)

| 脚本 | 功能 | 命令 |
|------|------|------|
| init_agent.py | 协议初始化 | `python scripts/init_agent.py` |
| lint-protocol.py | 协议合规检查 | `python scripts/lint-protocol.py` |
| token-counter.py | Token 统计 | `python scripts/token-counter.py` |

---

## 📁 目录树结构

```
$AGENT_DIR/
├── start-here.md      ⭐ 入口（必读）
├── quick-reference.md 📋 速查卡片
├── index.md           文档导航（你在这里）
├── manifest.json      📦 加载策略与元数据
│
├── core/              🔧 治理引擎（通用）
│   ├── core-rules.md
│   ├── instructions.md
│   └── stack-specs/   按技术栈选读
├── project/           📋 项目实例（特定）
│   ├── context.md
│   └── tech-stack.md
├── skills/            🛠️ 技能模块
│   ├── skill-interface.md
│   ├── guardian/
│   ├── ai-integration/
│   └── agent-governance/
│
├── meta/              📜 协议演进
│   └── protocol-adr.md
│
├── adapters/          🔌 AI 工具适配器
│   ├── github-copilot/
│   ├── cursor/
│   ├── claude/
│   └── ci/
│
└── scripts/           🔧 辅助工具
    ├── init_agent.py
    ├── lint-protocol.py
    └── token-counter.py
```

---

## 💡 使用技巧

### AI 助手工作流
1. **每次会话开始**: 阅读 `start-here.md`
2. **编码前**: 参考 `core/instructions.md` + 对应 `stack-specs/`
3. **提交前**: 检查 `core/conventions.md`
4. **遇到问题**: 查阅 `core/workflows/bug-prevention.md`

### 文档维护
- 发现新坑 → 记录到 `bug-prevention.md`
- 重要决策 → 创建 ADR 文档
- 协议变更 → 更新 `meta/protocol-adr.md`

---

*最后更新: 2026-01-23*
*协议版本: 2.1.0*
