# AI Agent Collaboration Protocol

> 标准化 AI 协作协议与配套 CLI：将 AI 开发规范作为可复用的数字资产管理。

[![Protocol](https://img.shields.io/badge/Protocol-v3.1.1-blue.svg)](.agent/manifest.json) [![PyPI](https://img.shields.io/badge/pypi-cokodo--agent-green.svg)](https://pypi.org/project/cokodo-agent/)

---

## cokodo-agent 使用方法

**cokodo-agent** 是本仓库提供的 CLI 工具，用于在项目中初始化、更新协议（`.agent/`）并生成各 AI IDE 的入口文件。

### 安装

```bash
# 推荐：使用 pipx 安装
pipx install cokodo-agent

# 或使用 pip
pip install cokodo-agent
```

若需要从 GitHub 拉取最新协议（`co init` 默认会尝试），可安装网络依赖：

```bash
pip install "cokodo-agent[network]"
# 或
pipx inject cokodo-agent httpx
```

离线使用时执行 `co init --offline` 即可使用内置协议。

### 快速开始

```bash
# 进入你的项目目录
cd my-project

# 交互式初始化（推荐）
co init

# 快速模式：使用默认值，仅生成 .agent/
co init --yes

# 指定项目名与技术栈
co init --name "MyApp" --stack python --yes
```

初始化后会生成 `.agent/` 目录。接下来可编辑 `.agent/project/context.md` 和 `.agent/project/tech-stack.md`，然后即可在 AI 会话中按协议协作。

### 常用命令

| 命令 | 说明 |
|------|------|
| `co init [path]` | 在目标目录创建 `.agent` 协议 |
| `co adapt <cursor\|claude\|copilot\|gemini\|all> [path]` | 根据已有 `.agent` 生成 IDE 入口文件 |
| `co detect [path]` | 检测项目中已有的 IDE 规约文件（只读） |
| `co import [path]` | 从 IDE 规约文件导入到 `.agent/project/` |
| `co lint [path]` | 检查协议合规性 |
| `co diff [path]` | 对比本地 `.agent` 与最新协议 |
| `co sync [path]` | 将本地 `.agent` 同步为最新协议（保留 `project/`） |
| `co context [path]` | 按技术栈与任务类型输出上下文文件列表 |
| `co journal [path]` | 向 session-journal.md 追加会话记录 |
| `co version` | 显示 CLI 与协议版本 |

### 生成 IDE 入口文件（co adapt）

在已有 `.agent/` 的项目中执行：

```bash
# 生成 Cursor 规则
co adapt cursor

# 生成 Claude / Copilot / Gemini 入口文件
co adapt claude
co adapt copilot
co adapt gemini

# 一次性生成全部
co adapt all
```

生成位置遵循各 IDE 官方约定：

| IDE | 生成文件 |
|-----|----------|
| Cursor | `.cursor/rules/agent-protocol.mdc` |
| Claude Code | `CLAUDE.md`（项目根） |
| GitHub Copilot | `AGENTS.md`（项目根） |
| Gemini Code Assist | `GEMINI.md`（项目根） |

### 更多说明

- 完整命令与选项：[使用指南 (中文)](docs/usage-guide_cn.md) / [Usage Guide (English)](docs/usage-guide.md)
- cokodo-agent 包说明与开发方式：[cokodo-agent/README.md](cokodo-agent/README.md)

---

## Agent Protocol 简介

协议定义在 **`.agent/`** 目录中，采用**引擎-实例分离**：通用规则在 `core/`，项目特定信息在 `project/`。

### 设计理念

- **长期主义**：规则面向项目全生命周期的经验传承。
- **资产化**：`.agent` 与源码同等重要，可独立复用、迁移。
- **防腐蚀**：通过物理与逻辑隔离，避免 AI 工具污染业务代码。

### 协议结构

```
.agent/
+-- start-here.md           # AI 会话入口
+-- manifest.json           # 加载策略与元数据
+-- core/                   # 治理引擎（通用规则）
|   +-- core-rules.md
|   +-- instructions.md
|   +-- conventions.md
|   +-- workflows/
|   +-- stack-specs/
+-- project/                # 项目实例（需自行维护）
|   +-- context.md
|   +-- tech-stack.md
|   +-- known-issues.md
+-- adapters/               # IDE 适配模板
+-- meta/                   # 协议运维（含 self-check-prompt）
+-- scripts/                # 辅助脚本（如 lint-protocol.py）
```

### 智能层隔离 (ILI)

| 层级 | 目录 | 职责 |
|------|------|------|
| 业务代码 | `src/`, `tests/` 等 | 项目主代码与测试 |
| 智能协议 | `.agent/` | 规则、上下文、适配器，与业务隔离 |

删除 `.agent/` 不应影响项目构建与运行；复制到新项目即可复用协议。

---

## 文档

| 文档 | 说明 |
|------|------|
| [使用指南 (中文)](docs/usage-guide_cn.md) | cokodo-agent 与协议使用详解 |
| [Usage Guide (English)](docs/usage-guide.md) | Full usage guide in English |
| [Token 对比分析](docs/token-comparison-analysis.md) | 协议文档 Token 估算与对比 |

---

## 仓库结构

```
agent_protocol/
+-- .agent/                 # 协议定义（本仓库即参考实现）
+-- cokodo-agent/           # CLI 源码（pip 安装的包）
+-- docs/                   # 使用指南与说明
```

---

*Protocol: 3.1.1 | CLI: see [cokodo-agent](cokodo-agent/)*
