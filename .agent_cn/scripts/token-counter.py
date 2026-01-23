#!/usr/bin/env python3
"""
Token 统计脚本

分析 .agent 协议文档的 Token 占用，帮助优化协议大小。

注意：使用简单的 Token 估算方法（单词 + 标点），
实际 Token 数量取决于具体的 tokenizer。
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FileStats:
    """文件统计"""
    path: str
    chars: int
    words: int
    lines: int
    tokens_estimate: int


def estimate_tokens(text: str) -> int:
    """
    估算 Token 数量。
    
    简单估算方法：
    - 英文：约 1 token / 4 chars
    - 中文：约 1 token / 2 chars
    - 代码/标点：额外计数
    
    这是粗略估算，实际请使用 tiktoken 等库。
    """
    # 分离中英文
    chinese = re.findall(r'[\u4e00-\u9fff]', text)
    english_words = re.findall(r'[a-zA-Z]+', text)
    numbers = re.findall(r'\d+', text)
    punctuation = re.findall(r'[^\w\s]', text)
    
    # 估算
    chinese_tokens = len(chinese) * 1.5  # 中文字符通常 1-2 tokens
    english_tokens = sum(max(1, len(w) / 4) for w in english_words)
    number_tokens = len(numbers)
    punct_tokens = len(punctuation) * 0.5
    
    return int(chinese_tokens + english_tokens + number_tokens + punct_tokens)


def analyze_file(path: Path, base_dir: Path) -> FileStats:
    """分析单个文件"""
    content = path.read_text(encoding="utf-8")
    
    return FileStats(
        path=str(path.relative_to(base_dir)),
        chars=len(content),
        words=len(content.split()),
        lines=content.count('\n') + 1,
        tokens_estimate=estimate_tokens(content),
    )


def analyze_directory(agent_dir: Path) -> dict[str, list[FileStats]]:
    """分析目录"""
    results: dict[str, list[FileStats]] = {}
    
    for path in agent_dir.rglob("*.md"):
        relative = path.relative_to(agent_dir)
        
        # 按顶级目录分组
        if len(relative.parts) > 1:
            category = relative.parts[0]
        else:
            category = "root"
        
        if category not in results:
            results[category] = []
        
        results[category].append(analyze_file(path, agent_dir))
    
    return results


def format_size(size: int) -> str:
    """格式化大小"""
    if size < 1000:
        return str(size)
    elif size < 1000000:
        return f"{size/1000:.1f}K"
    else:
        return f"{size/1000000:.1f}M"


def main():
    parser = argparse.ArgumentParser(description="Count tokens in .agent protocol")
    parser.add_argument(
        "--agent-dir",
        default=".agent",
        help="Path to .agent directory",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--sort",
        choices=["path", "tokens", "chars"],
        default="tokens",
        help="Sort by",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Show only top N files",
    )
    
    args = parser.parse_args()
    
    agent_dir = Path(args.agent_dir)
    if not agent_dir.exists():
        print(f"Error: .agent directory not found at {agent_dir}")
        sys.exit(1)
    
    results = analyze_directory(agent_dir)
    
    # 汇总统计
    all_files: list[FileStats] = []
    for category_files in results.values():
        all_files.extend(category_files)
    
    # 排序
    sort_key = {
        "path": lambda x: x.path,
        "tokens": lambda x: -x.tokens_estimate,
        "chars": lambda x: -x.chars,
    }[args.sort]
    all_files.sort(key=sort_key)
    
    if args.top > 0:
        all_files = all_files[:args.top]
    
    # 输出
    if args.format == "json":
        import json
        output = {
            "files": [vars(f) for f in all_files],
            "summary": {
                "total_files": len(all_files),
                "total_tokens": sum(f.tokens_estimate for f in all_files),
                "total_chars": sum(f.chars for f in all_files),
            }
        }
        print(json.dumps(output, indent=2))
    
    elif args.format == "csv":
        print("path,chars,words,lines,tokens_estimate")
        for f in all_files:
            print(f"{f.path},{f.chars},{f.words},{f.lines},{f.tokens_estimate}")
    
    else:
        print("=== Token Statistics ===\n")
        
        # 按类别汇总
        print("By Category:")
        print("-" * 50)
        for category in sorted(results.keys()):
            files = results[category]
            total_tokens = sum(f.tokens_estimate for f in files)
            total_chars = sum(f.chars for f in files)
            print(f"  {category:20} {len(files):3} files  "
                  f"{format_size(total_tokens):>8} tokens  "
                  f"{format_size(total_chars):>8} chars")
        
        print("\nTop Files by Tokens:")
        print("-" * 50)
        
        display_files = all_files[:10] if args.top == 0 else all_files
        for f in display_files:
            print(f"  {f.path:40} {format_size(f.tokens_estimate):>8} tokens")
        
        # 总计
        total_tokens = sum(f.tokens_estimate for f in all_files)
        total_chars = sum(f.chars for f in all_files)
        total_lines = sum(f.lines for f in all_files)
        
        print("\n" + "=" * 50)
        print(f"Total: {len(all_files)} files")
        print(f"  Tokens (estimated): {format_size(total_tokens)}")
        print(f"  Characters: {format_size(total_chars)}")
        print(f"  Lines: {format_size(total_lines)}")
        
        # Token 预算建议
        print("\n📊 Token Budget Analysis:")
        if total_tokens < 5000:
            print("  ✓ Small protocol - suitable for single-context loading")
        elif total_tokens < 10000:
            print("  ⚠ Medium protocol - consider selective loading")
        else:
            print("  ❌ Large protocol - requires on-demand loading strategy")


if __name__ == "__main__":
    main()
