# Cokodo Agent 使用指南

> 在项目中快速配置 AI 协作协议的完整指南

[![CLI 版本](https://img.shields.io/badge/CLI-v1.0.0-blue.svg)](../cokodo-agent)
[![协议版本](https://img.shields.io/badge/Protocol-v2.1.0-green.svg)](../.agent/manifest.json)

---

## 目录

- [安装](#安装)
- [快速开始](#快速开始)
- [命令参考](#命令参考)
- [生成的目录结构](#生成的目录结构)
- [配置选项](#配置选项)
- [初始化后设置](#初始化后设置)
- [AI 会话模板](#ai-会话模板)
- [常用操作](#常用操作)
- [环境变量](#环境变量)
- [常见问题](#常见问题)
- [协议升级](#协议升级)

---

## 安装

### 使用 pip

```bash
pip install cokodo-agent
```

### 使用 pipx（推荐）

```bash
pipx install cokodo-agent
```

### 验证安装

```bash
co version
# 或: cokodo version
```

---

## 快速开始

### 交互模式（默认）

```bash
# 进入项目目录
cd my-project

# 运行生成器（以下命令等效）
co init           # 简短命令（推荐）
cokodo init       # 完整命令
cokodo-agent init # 包名命令
```

CLI 将引导你完成配置：

```
╭─────────────────────────╮
│  Cokodo Agent v1.0.0    │
╰─────────────────────────╯

Fetching protocol...
  OK Protocol v2.1.0

? Project name: my-awesome-app
? Brief description: 一个任务管理应用
? Primary tech stack: Python
? AI tools to configure (at least one required):
  [x] Cokodo (Protocol Only)    <- 默认
  [ ] Cursor
  [ ] GitHub Copilot
  [ ] Claude Projects
  [ ] Google Antigravity

Generating .agent/
  OK Created .agent/

╭─────────────────────────────────────────────────╮
│ Success! Created .agent in /path/to/my-project  │
│                                                 │
│ Next steps:                                     │
│   1. Review .agent/project/context.md           │
│   2. Customize .agent/project/tech-stack.md     │
│   3. Start coding with AI assistance!           │
╰─────────────────────────────────────────────────╯
```

### 快速模式（非交互）

```bash
# 使用默认值（Cokodo 模式 - 仅生成协议）
co init --yes

# 指定项目名和技术栈
co init --name "MyApp" --stack python --yes

# 在指定目录初始化
co init ./new-project --yes
```

---

## 命令参考

### `co init [PATH]`（别名：`cokodo init`）

在目标位置创建 `.agent` 协议目录。

**参数：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `PATH` | 目标目录 | 当前目录 |

**选项：**

| 选项 | 简写 | 说明 |
|------|------|------|
| `--yes` | `-y` | 跳过交互提示，使用默认值 |
| `--name` | `-n` | 项目名称 |
| `--stack` | `-s` | 技术栈（`python`/`rust`/`qt`/`mixed`/`other`） |
| `--force` | `-f` | 覆盖已存在的 `.agent` 目录 |
| `--offline` | | 使用内置协议（无需网络） |

**示例：**

```bash
# 交互式初始化
co init

# 使用默认值快速初始化
co init -y

# 指定所有选项
co init ./my-project -n "My Project" -s python -y

# 强制覆盖已有协议
co init --force

# 离线模式（使用内置协议）
co init --offline
```

### `co version`（别名：`cokodo version`）

显示 CLI 和内置协议的版本信息。

```bash
$ co version
cokodo-agent v1.0.0

Protocol versions:
  Built-in: v2.1.0
```

---

## 生成的目录结构

运行 `co init` 后，将创建以下结构：

```
your-project/
├── .agent/                         # 协议目录
│   ├── start-here.md              # ⭐ AI 入口文件（首次必读）
│   ├── quick-reference.md         # 📋 一页纸速查卡片
│   ├── index.md                   # 🗂️ 文档导航索引
│   ├── manifest.json              # ⚙️ 加载策略与元数据
│   │
│   ├── core/                      # 🔧 治理引擎（可跨项目复用）
│   │   ├── core-rules.md          #    核心哲学与铁律
│   │   ├── instructions.md        #    AI 协作指南
│   │   ├── conventions.md         #    命名与 Git 约定
│   │   ├── security.md            #    安全开发规范
│   │   ├── examples.md            #    代码示例
│   │   ├── workflows/             #    工作流规范集
│   │   │   ├── ai-boundaries.md
│   │   │   ├── bug-prevention.md
│   │   │   ├── design-principles.md
│   │   │   ├── documentation.md
│   │   │   ├── pre-task-checklist.md
│   │   │   ├── quality-assurance.md
│   │   │   ├── review-process.md
│   │   │   └── testing.md
│   │   └── stack-specs/           #    技术栈规约
│   │       ├── git.md
│   │       ├── python.md
│   │       ├── rust.md
│   │       └── qt.md
│   │
│   ├── project/                   # 📋 项目实例（定制化）
│   │   ├── context.md             #    ✏️ 业务上下文
│   │   ├── tech-stack.md          #    ✏️ 技术栈配置
│   │   ├── known-issues.md        #    已知问题库
│   │   └── adr/                   #    架构决策记录
│   │       └── readme.md
│   │
│   ├── skills/                    # 🛠️ 技能模块
│   │   ├── skill-interface.md     #    技能开发指南
│   │   ├── guardian/              #    代码质量门禁
│   │   ├── ai-integration/        #    AI 服务集成
│   │   └── agent-governance/      #    协议健康检查
│   │
│   ├── adapters/                  # 🔌 工具适配器（模板）
│   │   ├── cursor/
│   │   ├── github-copilot/
│   │   ├── claude/
│   │   └── google-antigravity/
│   │
│   ├── meta/                      # 📚 协议演进
│   │   ├── protocol-adr.md
│   │   └── adr-archive.md
│   │
│   └── scripts/                   # 🔧 辅助脚本
│       ├── init_agent.py
│       ├── lint-protocol.py
│       └── token-counter.py
│
├── .cursorrules                   # [可选] Cursor 配置
├── .github/
│   └── copilot-instructions.md    # [可选] Copilot 配置
└── .claude/
    └── instructions.md            # [可选] Claude 配置
```

### 目录类型

| 类型 | 目录 | 用途 | 可移植性 |
|------|------|------|----------|
| **引擎文件** | `core/` | 通用治理规则 | ✅ 跨项目复用 |
| **实例文件** | `project/` | 项目特定信息 | ❌ 项目专属 |

**核心规则：** 引擎文件严禁包含项目特定的名称、路径或业务逻辑。

---

## 配置选项

### 技术栈选项

| 值 | 说明 | 推荐工具 |
|----|------|----------|
| `python` | Python 项目 | uv/pip, ruff, pytest, mypy |
| `rust` | Rust 项目 | cargo, clippy, rustfmt |
| `qt` | Qt/C++ 项目 | CMake/qmake, Qt Creator |
| `mixed` | Python + Rust | 组合工具链 |
| `other` | 其他技术栈 | 自定义配置 |

### AI 工具配置

| 工具 | 配置文件 | 说明 |
|------|----------|------|
| Cursor | `.cursorrules` | Cursor IDE 规则 |
| GitHub Copilot | `.github/copilot-instructions.md` | Copilot 指令 |
| Claude | `.claude/instructions.md` | Claude 项目指令 |

---

## 初始化后设置

### 第一步：配置项目上下文

编辑 `.agent/project/context.md`：

```markdown
# 项目业务上下文

## 项目名称

YourProjectName

## 项目定位

简要描述项目是什么、解决什么问题。

## 当前状态

[开发阶段、MVP、生产环境等]

## 核心功能

1. 功能 A - 描述
2. 功能 B - 描述
3. 功能 C - 描述

## 业务规则

- 规则 1：描述
- 规则 2：描述
```

### 第二步：配置技术栈

编辑 `.agent/project/tech-stack.md`：

```markdown
# 技术栈说明

## 主要技术栈

Python

## 语言版本

- Python 3.11+
- Node.js 18+（如适用）

## 核心依赖

- FastAPI 0.100+
- SQLAlchemy 2.0+
- Pydantic 2.0+

## 开发环境

- OS: Windows/Linux/macOS
- IDE: Cursor / VS Code
- 包管理器: uv / pip

## 构建命令

pip install -r requirements.txt
pytest tests/
```

### 第三步：配置 AI 工具（可选）

如需自定义生成的 AI 工具配置：

| AI 工具 | 操作 |
|---------|------|
| **Cursor** | 编辑 `.cursorrules` 或从 `.agent/adapters/cursor/rules.template.md` 复制 |
| **GitHub Copilot** | 编辑 `.github/copilot-instructions.md` |
| **Claude** | 运行 `python .agent/adapters/claude/adapt_for_claude.py` |

---

## AI 会话模板

### 快速启动（日常使用）

```
请先阅读 .agent/start-here.md 建立项目上下文，然后严格遵守协议规则。

今天的任务是：[描述你的任务]
```

### 完整上下文（首次或复杂任务）

```
请按以下顺序阅读文件建立项目上下文：

1. .agent/start-here.md
2. .agent/project/context.md
3. .agent/project/tech-stack.md
4. .agent/core/instructions.md
5. .agent/core/stack-specs/python.md  # 根据技术栈选择

然后开始今天的任务：[描述你的任务]
```

### 调试会话

```
请阅读 .agent/start-here.md 和 .agent/core/workflows/bug-prevention.md 
了解已知问题。

我遇到了这个 Bug：[描述问题]
```

---

## 常用操作

### 检查协议健康度

```bash
python .agent/scripts/lint-protocol.py
```

### 统计 Token 消耗

```bash
python .agent/scripts/token-counter.py
```

### 记录 Bug 预防知识

编辑 `.agent/core/workflows/bug-prevention.md` 添加新条目：

```markdown
### 问题：[简要描述]

**现象：** 发生了什么
**原因：** 为什么发生
**解决方案：** 如何修复/预防
**日期：** YYYY-MM-DD
```

### 记录架构决策

在 `.agent/project/adr/` 下创建新的 ADR 文件：

```markdown
# ADR-001: [决策标题]

## 状态
已采纳

## 背景
[为什么需要这个决策]

## 决策
[做出了什么决定]

## 影响
[决策的影响]
```

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `COKODO_OFFLINE` | 强制离线模式（`1`、`true`、`yes`） | 禁用 |
| `COKODO_CACHE_DIR` | 自定义缓存目录 | 系统相关 |
| `COKODO_REMOTE_SERVER` | 远程协议服务器 URL | 无（保留） |

### 缓存位置

| 操作系统 | 默认路径 |
|----------|----------|
| Linux/macOS | `~/.cache/cokodo/` |
| Windows | `%LOCALAPPDATA%\cokodo\cache\` |

---

## 常见问题

### Q: AI 没有遵循协议规则？

**解决方案：** 确保在每次会话开始时让 AI 先阅读 `start-here.md`。

```
请先阅读 .agent/start-here.md，然后再处理任何任务。
```

### Q: 协议文件太多，Token 消耗太大？

**解决方案：** 使用 `manifest.json` 定义的分层加载策略，只加载当前任务需要的文件。

必要文件（约 3,000 tokens）：
- `start-here.md`
- `quick-reference.md`

上下文文件（约 2,000 tokens）：
- `project/context.md`
- `project/tech-stack.md`

### Q: 协议初始化失败？

**解决方案：** 检查以下常见问题：

1. **权限不足：** 使用适当的权限运行
2. **目录已存在：** 使用 `--force` 覆盖
3. **网络错误：** 使用 `--offline` 使用内置协议

```bash
# 强制覆盖 + 离线模式
cokodo init --force --offline
```

### Q: 如何更改协议目录名？

**解决方案：** 协议内部使用 `$AGENT_DIR` 占位符。重命名步骤：

1. 重命名目录：
   ```bash
   mv .agent .agent_custom
   ```

2. 更新 `manifest.json`：
   ```json
   {
     "directory_name": ".agent_custom"
   }
   ```

---

## 协议升级

### 升级步骤

1. **备份当前项目文件：**
   ```bash
   cp -r .agent/project ./project-backup
   ```

2. **删除旧协议：**
   ```bash
   rm -rf .agent
   ```

3. **初始化新版本：**
   ```bash
   cokodo init --force
   ```

4. **恢复项目文件：**
   ```bash
   cp -r ./project-backup/* .agent/project/
   ```

5. **查看变更：**
   检查 `.agent/meta/protocol-adr.md` 了解版本变更。

### 版本兼容性

| CLI 版本 | 协议版本 | 备注 |
|----------|----------|------|
| 1.0.x | 2.1.0 | 当前稳定版 |

---

## 铁律

以下规则必须始终遵守：

| 规则 | 说明 |
|------|------|
| **UTF-8 编码** | 所有文件操作显式指定 `encoding='utf-8'` |
| **正斜杠路径** | 命令行中使用 `/` 而非 `\` |
| **测试数据前缀** | 测试数据使用 `autotest_` 前缀 |
| **kebab-case 文件名** | `.agent/` 内文件使用小写连字符命名 |
| **SKILL.md 大写** | 技能入口文件使用大写（符合 agentskills.io 标准） |

---

## 延伸阅读

| 文档 | 内容 |
|------|------|
| `.agent/start-here.md` | 协议入口和架构概览 |
| `.agent/quick-reference.md` | 一页纸速查 |
| `.agent/meta/protocol-adr.md` | 协议演进历史 |
| `.agent/skills/skill-interface.md` | 如何开发新技能 |

---

## 协议来源

CLI 从多个来源获取协议，自动降级：

```
优先级 1: GitHub Release（最新版本）
    ↓ [不可用]
优先级 2: 远程服务器（保留，未来使用）
    ↓ [不可用]
优先级 3: 内置版本（离线备用）
```

---

## 支持

- **文档：** [Agent Protocol 仓库](https://github.com/dinwind/agent_protocol)
- **问题反馈：** [提交 Issue](https://github.com/dinwind/agent_protocol/issues)
- **讨论：** [GitHub Discussions](https://github.com/dinwind/agent_protocol/discussions)

---

<div align="center">

**让 AI 协作更规范、更高效、更可持续**

*文档版本: 1.0.0 | 协议版本: 2.1.0 | 最后更新: 2026-01-24*

</div>
