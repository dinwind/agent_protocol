---
name: agent-governance
description: |
  协议健康检查技能 - 确保 AI 协议层的完整性和合规性。
  支持协议完整性检查、命名规范验证、Token 分析等。
---

# Agent Governance Skill

> 协议健康检查技能 - 确保 AI 协议层的完整性和合规性

---

## 技能概述

| 属性 | 值 |
|------|-----|
| 名称 | Agent Governance |
| 版本 | 2.0.0 |
| 类型 | 协议维护 |
| 触发 | 协议变更后 |

---

## 功能

1. **协议完整性检查** - 验证所有必需文件存在
2. **命名规范检查** - 确保 kebab-case 零例外
3. **引擎污染检测** - 检查 core/ 是否包含项目特定信息
4. **Token 统计** - 分析协议文档的 Token 占用
5. **链接有效性** - 检查内部链接是否有效

---

## 检查规则

### 1. 必需文件清单

```
.agent/
├── start-here.md          # 入口文件
├── index.md               # 导航索引
├── core/
│   ├── core-rules.md      # 核心规则
│   ├── instructions.md    # 协作指南
│   └── conventions.md     # 命名约定
├── project/
│   ├── context.md         # 项目上下文
│   └── tech-stack.md      # 技术栈
└── meta/
    └── protocol-adr.md    # 协议 ADR
```

### 2. 命名规范

```python
# 检查规则
NAMING_RULES = {
    "markdown_files": r"^[a-z0-9]+(-[a-z0-9]+)*\.md$",
    "directories": r"^[a-z0-9]+(-[a-z0-9]+)*$",
    "exceptions": ["MANIFEST.json", "VERSION"],
}
```

### 3. 引擎污染关键词

```python
# 不应出现在 core/ 目录的项目特定关键词
POLLUTION_KEYWORDS = [
    # 项目名称（需要根据实际项目配置）
    "project_name_placeholder",
    
    # 硬编码路径
    r"C:\\",
    r"D:\\",
    "/home/",
    "/Users/",
    
    # 特定服务名
    "localhost:8080",
    "127.0.0.1:",
]
```

---

## 使用方法

### 1. 完整检查

```bash
python .agent/skills/agent-governance/scripts/check_protocol.py
```

输出示例：
```
=== Agent Protocol Health Check ===

[✓] Required files check: PASSED
[✓] Naming convention check: PASSED
[✓] Engine pollution check: PASSED
[✓] Internal links check: PASSED

Token Statistics:
  - core/: 3,500 tokens
  - project/: 1,200 tokens
  - skills/: 2,800 tokens
  - Total: 7,500 tokens

Overall: HEALTHY
```

### 2. 单项检查

```bash
# 检查必需文件
python scripts/check_protocol.py --check required

# 检查命名规范
python scripts/check_protocol.py --check naming

# 检查引擎污染
python scripts/check_protocol.py --check pollution

# Token 统计
python scripts/check_protocol.py --check tokens
```

### 3. CI 集成

```yaml
# .github/workflows/protocol-check.yml
name: Protocol Check

on:
  push:
    paths:
      - '.agent/**'

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Protocol Health
        run: python .agent/skills/agent-governance/scripts/check_protocol.py
```

---

## 脚本实现

### check_protocol.py

```python
#!/usr/bin/env python3
"""协议健康检查脚本"""

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

class CheckResult(NamedTuple):
    name: str
    passed: bool
    message: str

def check_required_files(agent_dir: Path) -> CheckResult:
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
    
    missing = []
    for file in required:
        if not (agent_dir / file).exists():
            missing.append(file)
    
    if missing:
        return CheckResult(
            "Required Files",
            False,
            f"Missing: {', '.join(missing)}"
        )
    return CheckResult("Required Files", True, "All required files present")

def check_naming_convention(agent_dir: Path) -> CheckResult:
    """检查命名规范"""
    pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
    exceptions = {"MANIFEST.json", "VERSION"}
    
    violations = []
    for file in agent_dir.rglob("*.md"):
        if file.name not in exceptions:
            if not pattern.match(file.name):
                violations.append(str(file.relative_to(agent_dir)))
    
    if violations:
        return CheckResult(
            "Naming Convention",
            False,
            f"Violations: {', '.join(violations[:5])}"
        )
    return CheckResult("Naming Convention", True, "All files follow kebab-case")

def check_engine_pollution(agent_dir: Path) -> CheckResult:
    """检查引擎污染"""
    core_dir = agent_dir / "core"
    # 简化示例，实际需要配置项目特定关键词
    pollution_patterns = [
        r"C:\\\\",
        r"/home/[a-z]+/",
        r"/Users/[a-z]+/",
    ]
    
    violations = []
    for file in core_dir.rglob("*.md"):
        content = file.read_text(encoding="utf-8")
        for pattern in pollution_patterns:
            if re.search(pattern, content):
                violations.append(f"{file.name}: {pattern}")
    
    if violations:
        return CheckResult(
            "Engine Pollution",
            False,
            f"Found: {', '.join(violations[:3])}"
        )
    return CheckResult("Engine Pollution", True, "Core files are clean")

def main():
    agent_dir = Path(".agent")
    if not agent_dir.exists():
        print("Error: .agent directory not found")
        sys.exit(1)
    
    print("=== Agent Protocol Health Check ===\n")
    
    checks = [
        check_required_files(agent_dir),
        check_naming_convention(agent_dir),
        check_engine_pollution(agent_dir),
    ]
    
    all_passed = True
    for result in checks:
        status = "✓" if result.passed else "✗"
        print(f"[{status}] {result.name}: {result.message}")
        if not result.passed:
            all_passed = False
    
    print(f"\nOverall: {'HEALTHY' if all_passed else 'UNHEALTHY'}")
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
```

---

## 维护指南

### 添加新检查项

1. 在 `check_protocol.py` 中添加新的检查函数
2. 函数返回 `CheckResult`
3. 在 `main()` 中注册新检查

### 更新必需文件清单

修改 `check_required_files()` 中的 `required` 列表。

### 添加污染关键词

修改 `check_engine_pollution()` 中的 `pollution_patterns` 列表。

---

*此技能为可移植组件，可在多项目间复用*
*版本: 2.0.0*
