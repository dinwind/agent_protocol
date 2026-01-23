#!/usr/bin/env python3
"""
协议合规检查脚本

检查 .agent 协议层是否符合规范：
1. 文件命名规范（kebab-case）
2. 引擎文件污染检测
3. 必需文件存在性
4. 内部链接有效性
"""

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple


class LintResult(NamedTuple):
    """检查结果"""
    rule: str
    passed: bool
    message: str
    file: str | None = None
    line: int | None = None


class ProtocolLinter:
    """协议检查器"""
    
    def __init__(self, agent_dir: Path):
        self.agent_dir = agent_dir
        self.results: list[LintResult] = []
    
    def lint_all(self) -> list[LintResult]:
        """执行所有检查"""
        self.check_required_files()
        self.check_naming_convention()
        self.check_engine_pollution()
        self.check_internal_links()
        return self.results
    
    def check_required_files(self) -> None:
        """检查必需文件"""
        required = [
            "start-here.md",
            "index.md",
            "core/core-rules.md",
            "core/instructions.md",
            "core/conventions.md",
            "project/context.md",
            "project/tech-stack.md",
            "meta/protocol-adr.md",
        ]
        
        for file in required:
            path = self.agent_dir / file
            if path.exists():
                self.results.append(LintResult(
                    "required-files",
                    True,
                    f"Required file exists",
                    file,
                ))
            else:
                self.results.append(LintResult(
                    "required-files",
                    False,
                    f"Required file missing",
                    file,
                ))
    
    def check_naming_convention(self) -> None:
        """检查命名规范"""
        # kebab-case 模式
        pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
        exceptions = {"MANIFEST.json", "VERSION", "SKILL.md"}
        
        for path in self.agent_dir.rglob("*.md"):
            relative = path.relative_to(self.agent_dir)
            
            if path.name in exceptions:
                continue
            
            if pattern.match(path.name):
                self.results.append(LintResult(
                    "naming-convention",
                    True,
                    "Follows kebab-case",
                    str(relative),
                ))
            else:
                self.results.append(LintResult(
                    "naming-convention",
                    False,
                    f"Should use kebab-case: {path.name}",
                    str(relative),
                ))
    
    def check_engine_pollution(self) -> None:
        """检查引擎文件污染"""
        core_dir = self.agent_dir / "core"
        
        if not core_dir.exists():
            return
        
        # 不应出现在 core/ 的模式
        pollution_patterns = [
            (r"C:\\\\", "Windows path"),
            (r"D:\\\\", "Windows path"),
            (r"/home/\w+/", "Unix home path"),
            (r"/Users/\w+/", "macOS user path"),
            (r"localhost:\d+", "Hardcoded localhost"),
            (r"127\.0\.0\.1:\d+", "Hardcoded IP"),
        ]
        
        for path in core_dir.rglob("*.md"):
            relative = path.relative_to(self.agent_dir)
            content = path.read_text(encoding="utf-8")
            
            found_pollution = False
            for pattern, desc in pollution_patterns:
                matches = list(re.finditer(pattern, content))
                if matches:
                    found_pollution = True
                    # 计算行号
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        self.results.append(LintResult(
                            "engine-pollution",
                            False,
                            f"Found {desc}: {match.group()}",
                            str(relative),
                            line_num,
                        ))
            
            if not found_pollution:
                self.results.append(LintResult(
                    "engine-pollution",
                    True,
                    "No pollution detected",
                    str(relative),
                ))
    
    def check_internal_links(self) -> None:
        """检查内部链接有效性"""
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        
        for path in self.agent_dir.rglob("*.md"):
            relative = path.relative_to(self.agent_dir)
            content = path.read_text(encoding="utf-8")
            
            for match in link_pattern.finditer(content):
                link_text, link_target = match.groups()
                
                # 跳过外部链接和锚点
                if link_target.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue
                
                # 解析相对路径
                if link_target.startswith('/'):
                    target_path = self.agent_dir / link_target[1:]
                else:
                    target_path = path.parent / link_target
                
                # 处理锚点
                if '#' in str(target_path):
                    target_path = Path(str(target_path).split('#')[0])
                
                line_num = content[:match.start()].count('\n') + 1
                
                if target_path.exists():
                    self.results.append(LintResult(
                        "internal-links",
                        True,
                        f"Link valid: {link_target}",
                        str(relative),
                        line_num,
                    ))
                else:
                    self.results.append(LintResult(
                        "internal-links",
                        False,
                        f"Broken link: {link_target}",
                        str(relative),
                        line_num,
                    ))


def main():
    parser = argparse.ArgumentParser(description="Lint .agent protocol")
    parser.add_argument(
        "--agent-dir",
        default=".agent",
        help="Path to .agent directory",
    )
    parser.add_argument(
        "--rule",
        choices=["required-files", "naming-convention", "engine-pollution", "internal-links"],
        help="Check specific rule only",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    
    args = parser.parse_args()
    
    agent_dir = Path(args.agent_dir)
    if not agent_dir.exists():
        print(f"Error: .agent directory not found at {agent_dir}")
        sys.exit(1)
    
    linter = ProtocolLinter(agent_dir)
    results = linter.lint_all()
    
    # 过滤规则
    if args.rule:
        results = [r for r in results if r.rule == args.rule]
    
    # 输出结果
    errors = [r for r in results if not r.passed]
    
    if args.format == "json":
        import json
        print(json.dumps([r._asdict() for r in results], indent=2))
    else:
        print(f"=== Protocol Lint Results ===\n")
        
        # 按规则分组
        rules = set(r.rule for r in results)
        for rule in sorted(rules):
            rule_results = [r for r in results if r.rule == rule]
            passed = sum(1 for r in rule_results if r.passed)
            total = len(rule_results)
            
            status = "✓" if passed == total else "✗"
            print(f"[{status}] {rule}: {passed}/{total} passed")
            
            # 显示错误
            for r in rule_results:
                if not r.passed:
                    loc = f"{r.file}"
                    if r.line:
                        loc += f":{r.line}"
                    print(f"    - {loc}: {r.message}")
        
        print(f"\n{'='*40}")
        print(f"Total: {len(results) - len(errors)}/{len(results)} passed")
        
        if errors:
            print(f"\n❌ {len(errors)} error(s) found")
            sys.exit(1)
        else:
            print(f"\n✓ All checks passed")
            sys.exit(0)


if __name__ == "__main__":
    main()
