#!/usr/bin/env python3
"""
Agent 协议初始化脚本

用于在新项目中初始化 .agent 协议层，包括：
1. 创建项目实例文件
2. 生成 AI 工具适配器配置
3. 验证协议完整性
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_template(template_path: Path) -> str:
    """加载模板文件"""
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def render_template(template: str, variables: dict[str, Any]) -> str:
    """渲染模板，替换 {{VAR}} 形式的变量"""
    result = template
    for key, value in variables.items():
        pattern = r"\{\{" + re.escape(key) + r"\}\}"
        result = re.sub(pattern, str(value), result)
    return result


def initialize_project_files(agent_dir: Path, config: dict[str, Any]) -> None:
    """初始化项目实例文件"""
    project_dir = agent_dir / "project"
    
    # context.md
    context_template = project_dir / "context.md"
    if context_template.exists():
        content = load_template(context_template)
        content = render_template(content, config)
        context_template.write_text(content, encoding="utf-8")
        print(f"  ✓ Updated {context_template}")
    
    # tech-stack.md
    tech_template = project_dir / "tech-stack.md"
    if tech_template.exists():
        content = load_template(tech_template)
        content = render_template(content, config)
        tech_template.write_text(content, encoding="utf-8")
        print(f"  ✓ Updated {tech_template}")


def generate_adapter(
    agent_dir: Path,
    adapter_name: str,
    config: dict[str, Any],
    output_dir: Path,
) -> None:
    """生成 AI 工具适配器配置"""
    adapter_dir = agent_dir / "adapters" / adapter_name
    
    if not adapter_dir.exists():
        print(f"  ⚠ Adapter not found: {adapter_name}")
        return
    
    # 查找模板文件
    templates = list(adapter_dir.glob("*.template.md"))
    
    for template_path in templates:
        template_content = load_template(template_path)
        rendered = render_template(template_content, config)
        
        # 输出文件名（去掉 .template）
        output_name = template_path.name.replace(".template", "")
        
        # 根据适配器类型决定输出位置
        if adapter_name == "github-copilot":
            output_path = output_dir / ".github" / output_name
        else:
            output_path = output_dir / f".{adapter_name}" / output_name
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
        print(f"  ✓ Generated {output_path}")


def verify_protocol(agent_dir: Path) -> bool:
    """验证协议完整性"""
    required_files = [
        "start-here.md",
        "index.md",
        "core/core-rules.md",
        "core/instructions.md",
        "core/conventions.md",
        "project/context.md",
        "project/tech-stack.md",
        "meta/protocol-adr.md",
    ]
    
    missing = []
    for file in required_files:
        if not (agent_dir / file).exists():
            missing.append(file)
    
    if missing:
        print(f"  ✗ Missing files: {', '.join(missing)}")
        return False
    
    print("  ✓ All required files present")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize .agent protocol for a new project"
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Project name",
    )
    parser.add_argument(
        "--project-type",
        default="Application",
        help="Project type (Application/Library/CLI)",
    )
    parser.add_argument(
        "--stack",
        default="python",
        choices=["python", "rust", "qt", "mixed"],
        help="Primary technology stack",
    )
    parser.add_argument(
        "--adapter",
        action="append",
        default=[],
        help="Generate adapter config (can specify multiple)",
    )
    parser.add_argument(
        "--agent-dir",
        default=".agent",
        help="Path to .agent directory",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Output directory for generated files",
    )
    
    args = parser.parse_args()
    
    agent_dir = Path(args.agent_dir)
    output_dir = Path(args.output_dir)
    
    if not agent_dir.exists():
        print(f"Error: .agent directory not found at {agent_dir}")
        sys.exit(1)
    
    # 配置变量
    config = {
        "PROJECT_NAME": args.project_name,
        "PROJECT_TYPE": args.project_type,
        "PRIMARY_STACK": args.stack,
        "STACK": args.stack,
        "VERSION": "0.1.0",
        "LAST_UPDATE": datetime.now().strftime("%Y-%m-%d"),
        "DATE": datetime.now().strftime("%Y-%m-%d"),
    }
    
    print(f"\n=== Initializing Agent Protocol for '{args.project_name}' ===\n")
    
    # 1. 初始化项目文件
    print("1. Initializing project files...")
    initialize_project_files(agent_dir, config)
    
    # 2. 生成适配器配置
    if args.adapter:
        print("\n2. Generating adapter configs...")
        for adapter in args.adapter:
            generate_adapter(agent_dir, adapter, config, output_dir)
    
    # 3. 验证协议
    print("\n3. Verifying protocol integrity...")
    if not verify_protocol(agent_dir):
        print("\n⚠ Protocol verification failed!")
        sys.exit(1)
    
    print(f"\n✓ Agent protocol initialized successfully!")
    print(f"\nNext steps:")
    print(f"  1. Review and update .agent/project/context.md")
    print(f"  2. Review and update .agent/project/tech-stack.md")
    print(f"  3. Read .agent/start-here.md to understand the protocol")


if __name__ == "__main__":
    main()
