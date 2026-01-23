# Claude 适配器

> 基于 [Claude 官方文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) 的集成指南。

---

## 🎯 兼容性概述

Claude 支持 **Agent Skills** 功能，采用与 [agentskills.io](https://agentskills.io) 相同的开放标准！

| Claude 产品 | Skills 路径 | 与本协议兼容性 |
|-------------|-------------|----------------|
| **Claude Code** | `.claude/skills/` | 需目录映射 |
| **Claude API** | 上传 Skill zip | 需打包上传 |
| **Claude.ai** | 设置中上传 | 需打包上传 |

---

## 📁 Skills 标准对比

| 特性 | 本协议 | Claude |
|------|--------|--------|
| 目录位置 | `.agent/skills/` | `.claude/skills/` |
| 入口文件 | `SKILL.md` | `SKILL.md` |
| Frontmatter | 推荐 | **必需** |
| 最大字符 | 无限制 | name: 64, desc: 1024 |

---

## 🔧 适配方案

### 方案 A: 符号链接（推荐用于 Claude Code）

```powershell
# Windows (管理员权限)
mklink /D ".claude\skills" ".agent\skills"

# Linux/Mac
ln -s .agent/skills .claude/skills
```

这样 Claude Code 就能直接识别 `.agent/skills/` 中的技能。

### 方案 B: 复制并适配

运行适配脚本将技能复制到 `.claude/skills/`：

```python
# scripts/adapt_for_claude.py
"""将 .agent 协议适配为 Claude 格式"""

import shutil
from pathlib import Path

def adapt_skills(agent_root: Path, claude_root: Path):
    """复制并适配 Skills"""
    agent_skills = agent_root / "skills"
    claude_skills = claude_root / "skills"
    claude_skills.mkdir(parents=True, exist_ok=True)
    
    for skill_dir in agent_skills.iterdir():
        if not skill_dir.is_dir():
            continue
        
        # 跳过接口文件
        if skill_dir.name == "skill-interface.md":
            continue
        
        target_dir = claude_skills / skill_dir.name
        
        # 复制整个技能目录
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(skill_dir, target_dir)
        
        # 确保 SKILL.md 有正确的 frontmatter
        skill_file = target_dir / "SKILL.md"
        
        if old_file.exists():
            content = old_file.read_text(encoding='utf-8')
            
            # 确保有 frontmatter
            if not content.startswith('---'):
                skill_name = skill_dir.name
                frontmatter = f"""---
name: {skill_name}
description: |
  {skill_name} skill from .agent protocol.
---

"""
                content = frontmatter + content
            
            new_file.write_text(content, encoding='utf-8')
            old_file.unlink()
            
        print(f"✅ Adapted: {skill_dir.name}")

if __name__ == "__main__":
    adapt_skills(Path(".agent"), Path(".claude"))
    print("✅ Done! Skills copied to .claude/skills/")
```

---

## 📋 SKILL.md 格式要求

Claude 要求每个 Skill 必须有 YAML frontmatter：

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
```

**字段要求**：

| 字段 | 要求 |
|------|------|
| `name` | 最多 64 字符，小写字母、数字、连字符 |
| `description` | 最多 1024 字符，描述功能和使用场景 |

---

## 🚀 Claude Code 集成步骤

### 步骤 1: 创建 .claude 目录

```powershell
mkdir .claude\skills
```

### 步骤 2: 创建符号链接或复制技能

```powershell
# 方式 A: 符号链接
mklink /D ".claude\skills\guardian" ".agent\skills\guardian"
mklink /D ".claude\skills\ai-integration" ".agent\skills\ai-integration"

# 方式 B: 运行适配脚本
python .agent/adapters/claude/adapt_for_claude.py
```

### 步骤 3: 验证技能被识别

在 Claude Code 中输入：
```
/skills
```

应该能看到已安装的技能列表。

---

## 🔌 Claude API 集成

### 使用预构建技能

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02", "files-api-2025-04-14"],
    messages=[{"role": "user", "content": "Create a presentation about AI"}],
    tools=[{"type": "code_execution"}],
    tool_choice={"type": "auto"},
    metadata={
        "container": {
            "skill_ids": ["pptx"]  # 使用 PowerPoint 技能
        }
    }
)
```

### 上传自定义技能

```python
import anthropic
import zipfile
from pathlib import Path

def create_skill_zip(skill_path: Path) -> bytes:
    """将技能目录打包为 zip"""
    import io
    buffer = io.BytesIO()
    
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in skill_path.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(skill_path)
                zf.write(file, arcname)
    
    return buffer.getvalue()

# 上传技能
client = anthropic.Anthropic()
skill_zip = create_skill_zip(Path(".agent/skills/guardian"))

response = client.post(
    "/v1/skills",
    body={
        "name": "guardian",
        "description": "Code quality and security checks",
        "content": skill_zip
    }
)

skill_id = response["id"]
print(f"Skill uploaded: {skill_id}")
```

---

## 📊 Claude 平台功能对比

| 功能 | Claude.ai | Claude Code | Claude API |
|------|-----------|-------------|------------|
| 预构建技能 | ✅ | ❌ | ✅ |
| 自定义技能 | ✅ (上传) | ✅ (本地) | ✅ (上传) |
| 技能共享 | 仅个人 | 项目级 | 工作区级 |
| 网络访问 | 可配置 | 完全 | ❌ |

---

## 🔗 与 .agent 协议的映射

| .agent 概念 | Claude 对应 |
|-------------|-------------|
| `skills/` | `.claude/skills/` (Code) 或 上传 (API) |
| `core/` 规则 | System Prompt |
| `project/` 上下文 | System Prompt 或 Knowledge |
| `workflows/` | Skill 内的指令 |

---

## 💡 System Prompt 模板

对于不使用 Skills 的场景，可以在 System Prompt 中引用协议：

```markdown
You are an AI assistant following the .agent protocol.

## Core Rules

1. **UTF-8 Encoding**: Always specify `encoding='utf-8'` for file operations
2. **Forward Slashes**: Use `/` for paths in commands
3. **Test Prefix**: Use `autotest_` prefix for test data
4. **Explicit Error Handling**: No bare `except:` clauses

## Project Context

{{PROJECT_CONTEXT}}

## Technical Stack

{{TECH_STACK}}

## Coding Conventions

- Python: PascalCase for classes, snake_case for functions
- Follow PEP 8 style guidelines
- Maximum function length: 50 lines
- Maximum cyclomatic complexity: 10

When you need detailed rules, ask the user to provide the relevant .agent file content.
```

---

## 📚 参考资源

- [Claude Agent Skills 文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Claude Code Skills 文档](https://code.claude.com/docs/en/skills)
- [Skills 最佳实践](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Agent Skills 开放标准](https://agentskills.io)

---

*此适配器基于 Claude 官方文档编写*
*协议版本: 2.1.0*
*最后更新: 2026-01-23*
