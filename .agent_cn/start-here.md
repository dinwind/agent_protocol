# AI 协作起点

> **给新 AI 会话的第一句话**: 请先阅读本文件建立项目上下文，然后严格遵守协议规则。

> **目录名约定**: 本协议目录可命名为 `.agent`、`.agent_cn` 等。文档中使用 `$AGENT_DIR` 表示协议根目录，实际名称见 `manifest.json` 中的 `directory_name` 配置。

---

## 📍 协议架构简述

本协议采用**引擎-实例分离**架构，将通用治理规则与项目特定信息解耦：

- **`core/`**: 治理引擎（通用规则，禁止项目特定信息）。
- **`project/`**: 实例数据（项目上下文、技术栈、已知问题）。
- **`skills/`**: 模块化能力（按需加载的工具与规范）。
- **`adapters/`**: AI 工具适配器（Cursor, Claude, Copilot 等）。

详细目录结构见 [index.md](index.md) 或 [quick-reference.md](quick-reference.md)。

---

## 📚 上下文建立路径（必读）

⚠️ **强制要求**: AI 首次会话时必须按以下顺序加载文档，建立基础认知。

### 1. 核心协议（每次会话必读）

- [quick-reference.md](quick-reference.md): **一页纸速查** (编码、Git、常用命令)。
- [core/core-rules.md](core/core-rules.md): **核心铁律** (隔离、安全、交付质量)。
- [project/context.md](project/context.md): **项目上下文** (业务逻辑、功能状态)。

### 2. 技术规范（任务开始前阅读）

- [core/instructions.md](core/instructions.md): AI 协作指南与行为边界。
- [project/tech-stack.md](project/tech-stack.md): 技术栈、依赖与环境配置。
- [core/stack-specs/](core/stack-specs/): 按需选择对应语言的开发规范（Python/Rust/Qt/Git）。

### 3. 按需加载（遇到特定场景）

- [project/known-issues.md](project/known-issues.md): 调试遇到困难或新 Bug 时查阅。
- [core/workflows/](core/workflows/): 编码、测试、文档或评审时的标准流程。
- [skills/](skills/): 需要自动化检查或集成特定功能时查阅。

---

## 🛠️ 快速起步命令

```powershell
# 设置协议目录变量（根据实际目录名修改）
$AGENT_DIR = ".agent_cn"

# 1. 检查协议合规性
python $AGENT_DIR/scripts/lint-protocol.py

# 2. 统计 Token 使用量
python $AGENT_DIR/scripts/token-counter.py

# 3. 运行代码质量检查
python $AGENT_DIR/skills/guardian/scripts/check_all.py
```

---

*最后更新: 2026-01-23*
*协议版本: 2.1.0*
