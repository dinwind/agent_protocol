#!/usr/bin/env python3
"""
将 .agent 协议适配为 Google Antigravity 格式

使用方法:
    python .agent/adapters/google-antigravity/adapt_for_antigravity.py

功能:
    1. 确保 SKILL.md 有正确的 YAML frontmatter
    2. 在 .agent/rules/ 创建规则引用文件

注意: 协议已标准化使用 SKILL.md（大写），无需重命名。
"""

import os
import re
from pathlib import Path


def extract_description_from_content(content: str) -> str:
    """从 markdown 内容中提取描述"""
    # 尝试提取第一个段落作为描述
    lines = content.split('\n')
    description_lines = []
    in_content = False
    
    for line in lines:
        # 跳过 frontmatter
        if line.strip() == '---':
            continue
        # 跳过标题
        if line.startswith('#'):
            in_content = True
            continue
        # 收集非空行作为描述
        if in_content and line.strip():
            description_lines.append(line.strip())
            if len(description_lines) >= 2:
                break
    
    return ' '.join(description_lines) if description_lines else 'Please update this description.'


def adapt_skills(agent_root: Path) -> None:
    """确保 SKILL.md 有正确的 YAML frontmatter"""
    skills_dir = agent_root / "skills"
    
    if not skills_dir.exists():
        print("⚠️  skills/ 目录不存在，跳过")
        return
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        
        # 跳过非技能目录
        if skill_dir.name in ('__pycache__', '.git'):
            continue
        
        skill_file = skill_dir / "SKILL.md"
        
        # 协议已标准化使用 SKILL.md
        if not skill_file.exists():
            print(f"⚠️  跳过: {skill_dir.name} (无 SKILL.md)")
            continue
        
        content = skill_file.read_text(encoding='utf-8')
        
        # 检查是否已有 frontmatter
        if content.startswith('---'):
            print(f"✅ 已就绪: {skill_dir.name}")
            continue
        
        # 添加 frontmatter
        skill_name = skill_dir.name
        description = extract_description_from_content(content)
        
        frontmatter = f"""---
name: {skill_name}
description: |
  {description}
---

"""
        content = frontmatter + content
        skill_file.write_text(content, encoding='utf-8')
        print(f"✅ 添加 frontmatter: {skill_dir.name}")


def create_rules_references(agent_root: Path) -> None:
    """创建规则引用文件"""
    rules_dir = agent_root / "rules"
    rules_dir.mkdir(exist_ok=True)
    
    # 核心规则文件映射
    mappings = {
        "core-rules.md": {
            "source": "core/core-rules.md",
            "title": "核心规则",
            "activation": "Always On"
        },
        "instructions.md": {
            "source": "core/instructions.md",
            "title": "AI 协作指南",
            "activation": "Always On"
        },
        "conventions.md": {
            "source": "core/conventions.md",
            "title": "命名与 Git 约定",
            "activation": "Model Decision"
        },
        "security.md": {
            "source": "core/security.md",
            "title": "安全开发规范",
            "activation": "Manual"
        },
    }
    
    for rule_name, config in mappings.items():
        target = rules_dir / rule_name
        if not target.exists():
            content = f"""# {config['title']}

> 激活模式: {config['activation']}

详细规则请参考:

@.agent/{config['source']}
"""
            target.write_text(content, encoding='utf-8')
            print(f"✅ 创建规则: {rule_name}")
        else:
            print(f"⏭️  规则已存在: {rule_name}")


def create_project_rule(agent_root: Path) -> None:
    """创建项目上下文规则"""
    rules_dir = agent_root / "rules"
    rules_dir.mkdir(exist_ok=True)
    
    project_rule = rules_dir / "project-context.md"
    if not project_rule.exists():
        content = """# 项目上下文

> 激活模式: Always On

项目业务上下文和技术栈信息:

@.agent/project/context.md
@.agent/project/tech-stack.md
@.agent/project/known-issues.md
"""
        project_rule.write_text(content, encoding='utf-8')
        print("✅ 创建规则: project-context.md")


def create_readme(agent_root: Path) -> None:
    """在 rules 目录创建 README"""
    rules_dir = agent_root / "rules"
    readme = rules_dir / "README.md"
    
    if not readme.exists():
        content = """# Antigravity Rules

此目录包含 Google Antigravity 的工作区规则。

## 规则说明

| 文件 | 说明 | 激活模式 |
|------|------|----------|
| `core-rules.md` | 核心开发规则 | Always On |
| `instructions.md` | AI 协作指南 | Always On |
| `conventions.md` | 命名与 Git 约定 | Model Decision |
| `security.md` | 安全开发规范 | Manual (@security) |
| `project-context.md` | 项目上下文 | Always On |

## 激活模式说明

- **Always On**: 始终应用
- **Manual**: 在对话中使用 @rule-name 手动激活
- **Model Decision**: 模型根据任务自动决定是否应用
- **Glob**: 匹配特定文件类型时应用

## 更多信息

参考 [Google Antigravity Rules 文档](https://antigravity.google/docs/rules-workflows)
"""
        readme.write_text(content, encoding='utf-8')
        print("✅ 创建 rules/README.md")


def main():
    """主函数"""
    # 查找 .agent 目录
    agent_root = Path(".agent")
    if not agent_root.exists():
        # 尝试从脚本位置推断
        script_path = Path(__file__).resolve()
        agent_root = script_path.parent.parent.parent
    
    if not agent_root.exists() or not (agent_root / "start-here.md").exists():
        print("❌ 错误: 找不到 .agent 目录")
        print("   请在项目根目录运行此脚本")
        return 1
    
    print("🚀 开始适配 .agent 协议为 Google Antigravity 格式...")
    print(f"   目标目录: {agent_root.resolve()}")
    print()
    
    print("📦 适配 Skills...")
    adapt_skills(agent_root)
    print()
    
    print("📋 创建 Rules 引用...")
    create_rules_references(agent_root)
    create_project_rule(agent_root)
    create_readme(agent_root)
    print()
    
    print("✅ 适配完成!")
    print()
    print("📝 后续步骤:")
    print("   1. 在 Antigravity 中打开项目")
    print("   2. 检查 Customizations > Rules 确认规则已加载")
    print("   3. 检查 Skills 面板确认技能已识别")
    print("   4. 根据需要调整各规则的激活模式")
    
    return 0


if __name__ == "__main__":
    exit(main())
