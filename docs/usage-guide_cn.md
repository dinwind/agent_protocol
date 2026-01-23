# AI Agent 协议试用指南

> 如何在新项目中快速启用 AI 协作协议 v2.1.0

---

## 📛 目录命名约定

### 占位符说明

本协议文档中使用 `$AGENT_DIR` 作为协议根目录的占位符。实际目录名可根据项目需求自定义：

| 示例目录名 | 适用场景 |
|-----------|----------|
| `.agent` | 通用默认名称 |
| `.agent_cn` | 中文项目/中文文档版本 |
| `.claude` | Claude Code 原生兼容 |

### 改名操作

当需要更改协议目录名时，只需：

1. **重命名目录**
   ```powershell
   # 例如：从 .agent 改为 .agent_cn
   mv .agent .agent_cn
   ```

2. **更新 manifest.json**
   ```json
   {
     "directory_name": ".agent_cn",
     "directory_name_comment": "协议目录名，文档中使用 $AGENT_DIR 占位符引用"
   }
   ```

**无需修改其他文档**：协议内部使用相对路径，命令示例使用 `$AGENT_DIR` 占位符。

---

## 🚀 快速开始（3 分钟）

### 方式一：直接复制（推荐新手）

```powershell
# 1. 复制协议到你的项目（根据需要选择目录名）
xcopy /E /I "path\to\release\.agent_cn" "your-project\.agent_cn"

# 2. 进入项目目录
cd your-project

# 3. 编辑项目配置（必须）
notepad $AGENT_DIR\project\context.md
notepad $AGENT_DIR\project\tech-stack.md
```

### 方式二：使用初始化脚本（推荐）

```powershell
# 1. 复制协议到你的项目
xcopy /E /I "path\to\release\.agent_cn" "your-project\.agent_cn"

# 2. 设置目录变量
$AGENT_DIR = ".agent_cn"

# 3. 运行初始化脚本
cd your-project
python $AGENT_DIR\scripts\init_agent.py --project-name "YourProjectName" --stack python
```

---

## 📋 初始化后必做事项

### 1️⃣ 配置项目上下文

编辑 `$AGENT_DIR/project/context.md`：

```markdown
# 项目业务上下文

## 项目名称
YourProjectName

## 项目定位
简要描述项目是什么、解决什么问题

## 核心功能
1. 功能 A
2. 功能 B

## 目标用户
谁会使用这个项目

## 约束条件
- 性能要求
- 兼容性要求
```

### 2️⃣ 配置技术栈

编辑 `$AGENT_DIR/project/tech-stack.md`：

```markdown
# 技术栈说明

## 主要技术栈
- **语言**: Python 3.11
- **框架**: FastAPI
- **数据库**: PostgreSQL

## 开发环境
- **OS**: Windows/Linux
- **IDE**: VSCode/Cursor

## 构建命令
pip install -r requirements.txt
pytest tests/
```

### 3️⃣ 配置 AI 工具（可选）

根据使用的 AI 工具，复制对应的适配器配置：

| AI 工具 | 操作 |
|---------|------|
| **Cursor** | 复制 `$AGENT_DIR/adapters/cursor/rules.template.md` 内容到 `.cursorrules` |
| **GitHub Copilot** | 复制 `$AGENT_DIR/adapters/github-copilot/instructions.template.md` 到 `.github/copilot-instructions.md` |
| **Claude Code** | 运行 `python $AGENT_DIR/adapters/claude/adapt_for_claude.py` |
| **Google Antigravity** | 直接使用或运行 `python $AGENT_DIR/adapters/google-antigravity/adapt_for_antigravity.py` |

---

## 💬 AI 会话启动模板

### 简版（日常使用）

```
请先阅读 $AGENT_DIR/start-here.md 建立项目上下文，然后严格遵守协议规则。

今天的任务是：[描述你的任务]
```

### 完整版（首次或复杂任务）

```
请按以下顺序阅读文件建立项目上下文：

1. $AGENT_DIR/start-here.md
2. $AGENT_DIR/project/context.md
3. $AGENT_DIR/project/tech-stack.md
4. $AGENT_DIR/core/instructions.md
5. $AGENT_DIR/core/stack-specs/python.md  # 根据技术栈选择

然后开始今天的任务：[描述你的任务]
```

---

## 🔧 常用操作

### 检查协议健康度

```powershell
$AGENT_DIR = ".agent_cn"  # 设置实际目录名
python $AGENT_DIR/scripts/lint-protocol.py
```

### 统计 Token 消耗

```powershell
python $AGENT_DIR/scripts/token-counter.py
```

### 记录新发现的 Bug 预防知识

编辑 `$AGENT_DIR/core/workflows/bug-prevention.md`，添加新条目。

### 记录架构决策

在 `$AGENT_DIR/project/adr/` 下创建新的 ADR 文件。

---

## ⚠️ 注意事项

### 1. 不要修改 `core/` 目录

`core/` 下的文件是通用规则，修改会影响协议的可移植性。如需定制：
- 项目特定信息 → 放在 `project/`
- 架构决策 → 放在 `project/adr/`

### 2. 保持协议与代码同步提交

```bash
git add $AGENT_DIR/
git commit -m "chore: update agent protocol"
```

### 3. 遵循铁律

| 规则 | 说明 |
|------|------|
| UTF-8 编码 | 所有文件操作显式指定 `encoding='utf-8'` |
| 正斜杠路径 | 命令行中使用 `/` 而非 `\` |
| autotest_ 前缀 | 测试数据使用 `autotest_` 前缀 |
| kebab-case | `$AGENT_DIR/` 内文件使用小写连字符命名 |
| SKILL.md 大写 | 技能入口文件使用大写（符合 agentskills.io 标准） |

---

## 🆘 常见问题

### Q: AI 没有遵循协议规则？

确保在会话开始时让 AI 先阅读 `start-here.md`。

### Q: 协议文件太多，Token 消耗太大？

使用 `manifest.json` 定义的分层加载策略，只加载当前任务需要的文件。

### Q: 如何升级协议版本？

1. 备份当前 `project/` 目录
2. 复制新版本的协议目录
3. 恢复 `project/` 目录内容
4. 检查 `meta/protocol-adr.md` 了解变更

### Q: 如何改名协议目录？

见本文档顶部的 **目录命名约定** 章节。只需重命名目录并更新 `manifest.json` 中的 `directory_name` 字段。

---

## 📚 延伸阅读

| 文档 | 内容 |
|------|------|
| `$AGENT_DIR/start-here.md` | 协议入口和架构概览 |
| `$AGENT_DIR/quick-reference.md` | 一页纸速查 |
| `$AGENT_DIR/meta/protocol-adr.md` | 协议演进历史 |
| `$AGENT_DIR/skills/skill-interface.md` | 如何开发新技能 |

---

*文档版本: 1.2.0*
*适用协议版本: 2.1.0*
*最后更新: 2026-01-23*
