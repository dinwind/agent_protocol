#!/usr/bin/env python3
"""
将 .agent 协议适配为 Claude Code 格式

使用方法:
    python .agent/adapters/claude/adapt_for_claude.py

功能:
    1. 创建 .claude/skills/ 目录
    2. 复制 Skills 到 .claude/skills/
    3. 确保 SKILL.md 有正确的 YAML frontmatter

注意: 协议已标准化使用 SKILL.md（大写），无需重命名。
"""

import shutil
import re
from pathlib import Path


def extract_first_paragraph(content: str) -> str:
    """从 markdown 内容中提取第一个段落作为描述"""
    # 跳过 frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end + 3:].strip()
    
    # 跳过标题
    lines = content.split('\n')
    description_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if description_lines:
                break
            continue
        if line.startswith('#'):
            continue
        description_lines.append(line)
        if len(' '.join(description_lines)) > 200:
            break
    
    desc = ' '.join(description_lines)
    # 截断到 1000 字符（留点余量）
    if len(desc) > 1000:
        desc = desc[:997] + '...'
    return desc or 'Skill from .agent protocol.'


def sanitize_name(name: str) -> str:
    """确保名称符合 Claude 要求：小写字母、数字、连字符"""
    # 转换为小写
    name = name.lower()
    # 替换下划线和空格为连字符
    name = re.sub(r'[_\s]+', '-', name)
    # 只保留小写字母、数字、连字符
    name = re.sub(r'[^a-z0-9-]', '', name)
    # 截断到 64 字符
    return name[:64]


def adapt_skill_file(source_file: Path, target_file: Path, skill_name: str) -> None:
    """适配单个 skill 文件"""
    content = source_file.read_text(encoding='utf-8')
    
    # 检查是否已有 frontmatter
    has_frontmatter = content.startswith('---')
    
    if has_frontmatter:
        # 提取现有 frontmatter
        end = content.find('---', 3)
        if end != -1:
            frontmatter = content[3:end].strip()
            body = content[end + 3:].strip()
            
            # 检查是否有 name 和 description
            has_name = 'name:' in frontmatter
            has_desc = 'description:' in frontmatter
            
            if has_name and has_desc:
                # 已经完整，只需写入
                target_file.write_text(content, encoding='utf-8')
                return
            
            # 需要补充字段
            if not has_name:
                frontmatter = f"name: {sanitize_name(skill_name)}\n" + frontmatter
            if not has_desc:
                desc = extract_first_paragraph(body)
                frontmatter += f"\ndescription: |\n  {desc}"
            
            content = f"---\n{frontmatter}\n---\n\n{body}"
    else:
        # 需要添加 frontmatter
        safe_name = sanitize_name(skill_name)
        desc = extract_first_paragraph(content)
        
        frontmatter = f"""---
name: {safe_name}
description: |
  {desc}
---

"""
        content = frontmatter + content
    
    target_file.write_text(content, encoding='utf-8')


def adapt_skills(agent_root: Path, claude_root: Path) -> None:
    """复制并适配所有 Skills"""
    agent_skills = agent_root / "skills"
    claude_skills = claude_root / "skills"
    
    if not agent_skills.exists():
        print("⚠️  .agent/skills/ 目录不存在，跳过")
        return
    
    claude_skills.mkdir(parents=True, exist_ok=True)
    
    for item in agent_skills.iterdir():
        # 跳过非目录文件
        if not item.is_dir():
            continue
        
        # 跳过特殊目录
        if item.name.startswith('.') or item.name == '__pycache__':
            continue
        
        skill_name = item.name
        target_dir = claude_skills / skill_name
        
        # 清理目标目录
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        # 复制整个目录
        shutil.copytree(item, target_dir)
        
        # 处理入口文件（协议已标准化使用 SKILL.md）
        skill_file = target_dir / "SKILL.md"
        
        if skill_file.exists():
            # 确保有正确的 frontmatter
            adapt_skill_file(skill_file, skill_file, skill_name)
            print(f"✅ 适配完成: {skill_name}")
        else:
            print(f"⚠️  跳过: {skill_name} (无 SKILL.md)")


def create_global_rules_reference(agent_root: Path, claude_root: Path) -> None:
    """创建指向 .agent 规则的说明文件"""
    readme = claude_root / "README.md"
    
    content = """# Claude Skills from .agent Protocol

此目录包含从 `.agent` 协议适配的 Skills。

## 源目录

Skills 原始来源: `.agent/skills/`

## 更新方式

```bash
python .agent/adapters/claude/adapt_for_claude.py
```

## 注意事项

- 修改应在 `.agent/skills/` 中进行
- 然后运行适配脚本同步到此目录
- 不要直接修改此目录下的文件

## 相关文档

- [.agent 协议入口](.agent/start-here.md)
- [Claude Skills 文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
"""
    
    readme.write_text(content, encoding='utf-8')
    print("✅ 创建 .claude/README.md")


def main():
    """主函数"""
    # 查找 .agent 目录
    agent_root = Path(".agent")
    claude_root = Path(".claude")
    
    if not agent_root.exists():
        # 尝试从脚本位置推断
        script_path = Path(__file__).resolve()
        agent_root = script_path.parent.parent.parent
        claude_root = agent_root.parent / ".claude"
    
    if not agent_root.exists() or not (agent_root / "start-here.md").exists():
        print("❌ 错误: 找不到 .agent 目录")
        print("   请在项目根目录运行此脚本")
        return 1
    
    print("🚀 开始适配 .agent 协议为 Claude Code 格式...")
    print(f"   源目录: {agent_root.resolve()}")
    print(f"   目标目录: {claude_root.resolve()}")
    print()
    
    print("📦 适配 Skills...")
    adapt_skills(agent_root, claude_root)
    print()
    
    print("📋 创建说明文件...")
    create_global_rules_reference(agent_root, claude_root)
    print()
    
    print("✅ 适配完成!")
    print()
    print("📝 后续步骤:")
    print("   1. 在 Claude Code 中打开项目")
    print("   2. 输入 /skills 查看已安装的技能")
    print("   3. 技能会在相关任务中自动激活")
    
    return 0


if __name__ == "__main__":
    exit(main())
