# Cokodo Agent 使用指南

> 在项目中快速配置 AI 协作协议的完整指南

[![CLI 版本](https://img.shields.io/badge/CLI-v1.2.0-blue.svg)](../cokodo-agent)
[![协议版本](https://img.shields.io/badge/Protocol-v3.0.0-green.svg)](../.agent/manifest.json)

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
│  Cokodo Agent v1.2.0    │
╰─────────────────────────╯

Fetching protocol...
  OK Protocol v3.0.0

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

### `co init [PATH]`

在目标位置创建 `.agent` 协议目录。

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

### `co lint [PATH]`

检查协议合规性，包含 8 项检查规则。

| 选项 | 简写 | 说明 |
|------|------|------|
| `--rule` | `-r` | 只检查特定规则 |
| `--format` | `-f` | 输出格式（`text`/`json`/`github`） |

**检查规则：**

| 规则 | 说明 |
|------|------|
| `directory-structure` | 标准目录是否存在 |
| `required-files` | 必需文件是否存在 |
| `integrity-violation` | 锁定文件完整性（SHA256 校验） |
| `start-here-spec` | start-here.md 不含项目特定信息 |
| `naming-convention` | kebab-case 命名规范 |
| `skills-placement` | 项目技能在 _project/ 下 |
| `engine-pollution` | 锁定目录无硬编码路径 |
| `internal-links` | 内部链接有效性 |

**示例：**

```bash
# 运行所有检查
co lint

# 只检查完整性
co lint --rule integrity-violation

# JSON 格式输出（用于 CI）
co lint --format json

# GitHub Actions 注解格式
co lint --format github
```

### `co diff [PATH]`

对比本地 `.agent` 与最新协议的差异。

| 选项 | 说明 |
|------|------|
| `--offline` | 使用内置协议对比 |

**示例：**

```bash
# 对比最新协议
co diff

# 离线对比
co diff --offline
```

**输出示例：**

```
Comparing with latest protocol...

Local version:  3.0.0
Remote version: 3.0.1

       Changes
┌───────────┬───────┐
│ Status    │ Count │
├───────────┼───────┤
│ Added     │ 2     │
│ Modified  │ 5     │
│ Unchanged │ 33    │
└───────────┴───────┘

Added files:
  + core/workflows/new-workflow.md

Modified files:
  ~ core/core-rules.md
  ~ scripts/lint-protocol.py

Run co sync to update your protocol.
```

### `co sync [PATH]`

同步本地 `.agent` 到最新协议版本。

| 选项 | 简写 | 说明 |
|------|------|------|
| `--offline` | | 使用内置协议同步 |
| `--dry-run` | | 预览变更，不实际修改 |
| `--yes` | `-y` | 跳过确认提示 |

**重要：** `project/` 目录下的文件不会被覆盖，保留你的项目配置。

**示例：**

```bash
# 交互式同步
co sync

# 预览变更
co sync --dry-run

# 自动确认同步
co sync -y

# 离线同步
co sync --offline -y
```

### `co context [PATH]`

根据技术栈和任务类型获取相关上下文文件。

| 选项 | 简写 | 说明 |
|------|------|------|
| `--stack` | `-s` | 技术栈（`python`/`rust`/`qt`/`mixed`） |
| `--task` | `-t` | 任务类型（见下表） |
| `--output` | `-o` | 输出格式（`list`/`paths`/`content`） |

**任务类型：**

| 任务 | 说明 | 加载的文件 |
|------|------|-----------|
| `coding` | 编码任务 | bug-prevention.md, design-principles.md |
| `testing` | 测试任务 | testing.md |
| `review` | 代码审查 | review-process.md, quality-assurance.md |
| `documentation` | 文档任务 | documentation.md |
| `bug_fix` | Bug 修复 | coding workflows + guardian skill |
| `feature_development` | 功能开发 | coding + testing workflows |

**示例：**

```bash
# 列出 Python 编码任务的上下文文件
co context --stack python --task coding

# 输出文件路径（用于脚本）
co context --task bug_fix --output paths

# 输出文件内容（可管道传递给 AI）
co context --stack python --output content

# 复制到剪贴板（macOS）
co context --task coding --output content | pbcopy

# 复制到剪贴板（Windows）
co context --task coding --output content | clip
```

### `co journal [PATH]`

记录会话日志到 session-journal.md。

| 选项 | 简写 | 说明 |
|------|------|------|
| `--title` | `-t` | 会话标题（如 "功能 X 实现"） |
| `--completed` | `-c` | 完成的工作项（逗号分隔） |
| `--debt` | `-d` | 技术债务（逗号分隔） |
| `--decisions` | | 关键决策（逗号分隔） |
| `--interactive` | `-i` | 交互模式 |

**示例：**

```bash
# 交互模式（推荐）
co journal -i

# 命令行模式
co journal --title "用户认证功能" \
  --completed "实现登录API,添加JWT验证,编写单元测试" \
  --decisions "采用JWT而非Session"

# 快速记录
co journal -t "Bug修复" -c "修复登录超时问题,更新错误处理"
```

### `co update-checksums [PATH]`

更新 `manifest.json` 中的文件签名（仅协议维护者使用）。

```bash
co update-checksums
```

### `co version`

显示 CLI 和内置协议的版本信息。

```bash
$ co version
cokodo-agent v1.2.0

Protocol versions:
  Built-in: v3.0.0
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
│   ├── core/                      # 🔒 治理引擎（锁定，跨项目复用）
│   │   ├── core-rules.md          #    核心哲学与铁律
│   │   ├── instructions.md        #    AI 协作指南
│   │   ├── conventions.md         #    命名与 Git 约定
│   │   ├── security.md            #    安全开发规范
│   │   ├── examples.md            #    代码示例
│   │   ├── workflows/             #    工作流规范集
│   │   └── stack-specs/           #    技术栈规约
│   │
│   ├── project/                   # ✏️ 项目实例（可编辑）
│   │   ├── context.md             #    业务上下文
│   │   ├── tech-stack.md          #    技术栈配置
│   │   ├── known-issues.md        #    已知问题库
│   │   ├── commands.md            #    常用命令
│   │   └── session-journal.md     #    会话日志
│   │
│   ├── skills/                    # 🛠️ 技能模块
│   │   ├── skill-interface.md     #    🔒 技能开发指南
│   │   ├── guardian/              #    🔒 代码质量门禁
│   │   ├── ai-integration/        #    🔒 AI 服务集成
│   │   ├── agent-governance/      #    🔒 协议健康检查
│   │   └── _project/              #    ✏️ 项目自定义技能
│   │
│   ├── adapters/                  # 🔒 工具适配器（模板）
│   ├── meta/                      # 🔒 协议演进
│   └── scripts/                   # 🔒 辅助脚本
│
├── .cursorrules                   # [可选] Cursor 配置
├── .github/
│   └── copilot-instructions.md    # [可选] Copilot 配置
└── .claude/
    └── instructions.md            # [可选] Claude 配置
```

### 目录权限

| 标记 | 目录 | 权限 | 说明 |
|------|------|------|------|
| 🔒 | `core/`, `adapters/`, `meta/`, `scripts/` | 只读 | 协议引擎，由 `co sync` 更新 |
| ✏️ | `project/`, `skills/_project/` | 可编辑 | 项目特定配置 |

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

---

## AI 会话模板

### 快速启动（日常使用）

```
请先阅读 .agent/start-here.md 建立项目上下文，然后严格遵守协议规则。

今天的任务是：[描述你的任务]
```

### 使用动态上下文（推荐）

```bash
# 获取编码任务的上下文
co context --stack python --task coding --output content
```

然后将输出粘贴给 AI，或使用管道：

```bash
# macOS/Linux
co context --task bug_fix --output content | pbcopy

# Windows
co context --task bug_fix --output content | clip
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
co lint
```

### 查看协议更新

```bash
co diff
```

### 同步协议更新

```bash
co sync
```

### 统计 Token 消耗

```bash
python .agent/scripts/token-counter.py
```

### 记录 Bug 预防知识

编辑 `.agent/project/known-issues.md` 添加新条目：

```markdown
### 问题：[简要描述]

**现象：** 发生了什么
**原因：** 为什么发生
**解决方案：** 如何修复/预防
**日期：** YYYY-MM-DD
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

**解决方案：** 使用 `co context` 命令按需加载：

```bash
# 只加载编码任务需要的文件
co context --task coding --output content
```

### Q: 协议初始化失败？

**解决方案：** 检查以下常见问题：

1. **权限不足：** 使用适当的权限运行
2. **目录已存在：** 使用 `--force` 覆盖
3. **网络错误：** 使用 `--offline` 使用内置协议

```bash
# 强制覆盖 + 离线模式
co init --force --offline
```

### Q: 如何检查协议完整性？

**解决方案：** 使用 lint 命令检查：

```bash
co lint --rule integrity-violation
```

如果发现文件被修改，可以使用 `co sync` 恢复。

---

## 协议升级

### 使用 co sync（推荐）

```bash
# 查看有哪些更新
co diff

# 同步更新（project/ 目录会保留）
co sync
```

### 手动升级

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
   co init --force
   ```

4. **恢复项目文件：**
   ```bash
   cp -r ./project-backup/* .agent/project/
   ```

### 版本兼容性

| CLI 版本 | 协议版本 | 备注 |
|----------|----------|------|
| 1.2.x | 3.0.0 | 当前稳定版 |
| 1.1.x | 2.1.0 | 旧版本 |

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

## 支持

- **文档：** [Agent Protocol 仓库](https://github.com/dinwind/agent_protocol)
- **问题反馈：** [提交 Issue](https://github.com/dinwind/agent_protocol/issues)
- **讨论：** [GitHub Discussions](https://github.com/dinwind/agent_protocol/discussions)

---

<div align="center">

**让 AI 协作更规范、更高效、更可持续**

*文档版本: 1.2.0 | 协议版本: 3.0.0 | 最后更新: 2026-01-26*

</div>
