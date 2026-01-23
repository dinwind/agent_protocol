# Google Antigravity 适配器

> 基于 [Google Antigravity 官方文档](https://antigravity.google/docs) 的集成指南。

---

## 🎯 兼容性概述

**好消息**：Google Antigravity 的目录结构与本 `.agent` 协议**高度兼容**！

| Antigravity 概念 | 路径 | 本协议对应 |
|------------------|------|------------|
| Workspace Rules | `.agent/rules/` | `core/` 规则文件 |
| Workspace Skills | `.agent/skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` ✅ |
| Global Rules | `~/.gemini/GEMINI.md` | - |
| Global Skills | `~/.gemini/antigravity/global_skills/` | - |

---

## 📁 目录结构适配

### 当前协议结构

```
.agent/
├── core/                    # 治理规则
├── project/                 # 项目上下文
├── skills/                  # ✅ Antigravity 原生支持！
│   ├── guardian/
│   │   └── SKILL.md        # ✅ 已标准化
│   └── ai-integration/
│       └── ...
└── ...
```

### Antigravity 兼容性

**已实现零适配兼容**：协议已标准化使用 `SKILL.md`（大写），与 Antigravity 完全一致。

如需添加 YAML frontmatter，运行适配脚本即可。

---

## 🔧 配置步骤

### 步骤 1: 创建 Workspace Rules

在 `.agent/rules/` 目录下创建规则文件：

```
.agent/rules/
├── core-rules.md          # 核心规则
├── coding-conventions.md  # 编码约定
└── security.md            # 安全规范
```

**规则激活模式**（在 Antigravity UI 中设置）：

| 模式 | 说明 | 推荐用于 |
|------|------|----------|
| **Always On** | 始终应用 | `core-rules.md` |
| **Manual** | @ 提及时应用 | `security.md` |
| **Model Decision** | 模型自动判断 | `coding-conventions.md` |
| **Glob** | 文件匹配时应用 | 技术栈特定规则 |

### 步骤 2: 配置核心规则文件

创建 `.agent/rules/core-rules.md`：

```markdown
# 核心开发规则

## 铁律（不可妥协）

1. **UTF-8 编码**: 所有文件操作必须指定 `encoding='utf-8'`
2. **正斜杠路径**: 命令行中使用 `/` 而非 `\`
3. **测试数据前缀**: 使用 `autotest_` 作为测试数据前缀
4. **显式错误处理**: 禁止裸 `except:` 捕获

## 引用详细规范

更多细节请参考：
@.agent/core/core-rules.md
@.agent/core/instructions.md
@.agent/core/conventions.md

## 项目上下文

@.agent/project/context.md
@.agent/project/tech-stack.md
```

> 💡 使用 `@filename` 语法引用其他文件，Antigravity 会自动加载。

### 步骤 3: 确保 Skills 有 Frontmatter

协议已标准化使用 `SKILL.md`，只需确保有正确的 frontmatter：

**示例: `.agent/skills/guardian/SKILL.md`**

```markdown
---
name: guardian
description: |
  Performs code quality and security checks before commits.
  Use this skill when reviewing code, checking for banned patterns,
  or ensuring architecture layer compliance.
---

# Guardian - 质量守护技能

## 功能

- 禁止模式检查（硬编码密钥、裸 except 等）
- 架构层依赖检查
- 测试覆盖率验证

## 使用方式

在对话中提及代码审查、质量检查时自动激活。

## 详细规则

@.agent/skills/guardian/rules/banned-patterns.json
@.agent/core/security.md
```

**示例: `.agent/skills/ai-integration/SKILL.md`**

```markdown
---
name: ai-integration
description: |
  Provides patterns and best practices for integrating LLM/AI services.
  Use this skill when building AI features, designing prompts, or
  implementing LLM clients.
---

# AI Integration 技能

## 包含内容

- LLM 客户端设计模式
- Prompt 工程最佳实践
- 领域适配方法论

## 详细文档

@.agent/skills/ai-integration/llm-client.md
@.agent/skills/ai-integration/prompt-engineering.md
@.agent/skills/ai-integration/domain-adaptation.md
```

### 步骤 4: 创建 Workflows（可选）

将常用操作流程定义为 Workflow，通过 `/workflow-name` 调用。

**示例: 代码审查工作流**

在 Antigravity 的 Workflows 面板创建：

```markdown
# Code Review Workflow

## 描述
执行完整的代码审查流程

## 步骤

### 1. 加载上下文
阅读项目技术栈和编码规范：
@.agent/project/tech-stack.md
@.agent/core/conventions.md

### 2. 检查代码质量
参考 Guardian 技能执行检查：
- 运行 `python .agent/scripts/lint-protocol.py`
- 检查禁止模式

### 3. 生成审查报告
输出发现的问题和建议
```

使用时在 Agent 中输入: `/code-review`

---

## 📋 快速迁移脚本

运行以下脚本自动适配 Antigravity：

```python
# scripts/adapt_for_antigravity.py
"""将 .agent 协议适配为 Antigravity 格式"""

import os
import shutil
from pathlib import Path

def adapt_skills():
    """确保 SKILL.md 有正确的 frontmatter"""
    skills_dir = Path(".agent/skills")
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        if old_file.exists():
            # 读取原内容
            content = old_file.read_text(encoding='utf-8')
            
            # 检查是否已有 frontmatter
            if not content.startswith('---'):
                # 添加 frontmatter
                skill_name = skill_dir.name
                frontmatter = f"""---
name: {skill_name}
description: |
  {skill_name} skill - please update this description.
---

"""
                content = frontmatter + content
            
            # 写入新文件
            new_file.write_text(content, encoding='utf-8')
            old_file.unlink()
            print(f"✅ Adapted: {skill_dir.name}")

def create_rules_symlinks():
    """创建规则文件的符号链接或复制"""
    rules_dir = Path(".agent/rules")
    rules_dir.mkdir(exist_ok=True)
    
    # 核心规则文件映射
    mappings = {
        "core-rules.md": ".agent/core/core-rules.md",
        "instructions.md": ".agent/core/instructions.md",
        "conventions.md": ".agent/core/conventions.md",
        "security.md": ".agent/core/security.md",
    }
    
    for rule_name, source in mappings.items():
        target = rules_dir / rule_name
        if not target.exists():
            # 创建引用文件
            target.write_text(f"# {rule_name}\n\n@{source}\n", encoding='utf-8')
            print(f"✅ Created rule: {rule_name}")

if __name__ == "__main__":
    print("🚀 Adapting .agent for Google Antigravity...")
    adapt_skills()
    create_rules_symlinks()
    print("✅ Done!")
```

---

## 🔗 与 Antigravity 功能的映射

| 本协议概念 | Antigravity 功能 | 说明 |
|------------|------------------|------|
| `core/` 规则 | Rules (Always On) | 核心规则始终生效 |
| `project/` 上下文 | Rules + @ mentions | 通过引用加载 |
| `skills/` | Skills | 原生兼容 |
| `workflows/` | Workflows | 定义为可调用流程 |
| `lessons/` | Knowledge Items | Antigravity 自动生成 |
| `scripts/` | 脚本工具 | Agent 可直接调用 |

---

## ⚙️ 推荐设置

### Agent Settings

在 Antigravity 的 Agent Settings 中：

| 设置 | 推荐值 | 原因 |
|------|--------|------|
| **Default Model** | Gemini 2.0 Flash | 平衡速度和质量 |
| **Auto-apply Rules** | On | 自动应用 Always On 规则 |
| **Skill Discovery** | On | 自动发现可用技能 |

### Secure Mode

如果处理敏感代码，启用 [Secure Mode](https://antigravity.google/docs/secure-mode)。

---

## 📚 参考资源

- [Google Antigravity 官方文档](https://antigravity.google/docs)
- [Rules / Workflows 文档](https://antigravity.google/docs/rules-workflows)
- [Skills 文档](https://antigravity.google/docs/skills)
- [Agent Skills 开放标准](https://agentskills.io/home)
- [MCP 集成](https://antigravity.google/docs/mcp)

---

*此适配器基于 Google Antigravity 官方文档编写*
*协议版本: 2.1.0*
*最后更新: 2026-01-23*
