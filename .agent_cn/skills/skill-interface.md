# 技能模块接口规范

> 定义技能模块的标准结构、接口和生命周期。

---

## 1. 概述

技能（Skill）是 `.agent` 协议中可复用的能力模块，用于封装特定领域的知识和自动化脚本。

### 1.1 设计原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 每个技能专注于一个领域 |
| **自包含** | 技能所需的文档、脚本、规则都在目录内 |
| **可发现** | 通过 manifest.json 声明元数据 |
| **松耦合** | 技能之间不应有强依赖 |

---

## 2. 目录结构

### 2.1 标准结构

```
skills/
└── {skill-name}/
    ├── SKILL.md           # 技能主文档（必需，大写）
    ├── manifest.json      # 元数据声明（推荐）
    ├── rules/             # 规则定义（可选）
    │   └── *.json
    ├── scripts/           # 自动化脚本（可选）
    │   └── *.py
    └── templates/         # 模板文件（可选）
        └── *.template
```

> **注意**: 入口文件必须命名为 `SKILL.md`（大写），以兼容 [agentskills.io](https://agentskills.io) 开放标准。

### 2.2 文件说明

| 文件 | 必需性 | 说明 |
|------|--------|------|
| `SKILL.md` | ✅ 必需 | 技能的主文档，定义功能、使用方法（大写） |
| `manifest.json` | 📋 推荐 | 元数据声明，用于自动发现和加载 |
| `rules/*.json` | 可选 | 结构化规则定义 |
| `scripts/*.py` | 可选 | 自动化检查/生成脚本 |
| `templates/*` | 可选 | 代码/文档模板 |

---

## 3. Manifest 规范

### 3.1 完整示例

```json
{
  "$schema": "https://agent-protocol.dev/schemas/skill-manifest.json",
  "name": "guardian",
  "version": "1.0.0",
  "description": "代码质量和安全检查技能",
  
  "triggers": {
    "explicit": ["check code", "review", "validate"],
    "automatic": ["pre-commit", "pull-request"]
  },
  
  "capabilities": [
    {
      "name": "banned-pattern-check",
      "description": "检查禁止的代码模式",
      "input": "source_files",
      "output": "violation_report"
    },
    {
      "name": "architecture-check",
      "description": "检查架构层依赖",
      "input": "source_files",
      "output": "dependency_report"
    }
  ],
  
  "dependencies": {
    "python": ">=3.9",
    "packages": ["ruff", "mypy"]
  },
  
  "entry_points": {
    "main": "SKILL.md",
    "check": "scripts/check_all.py"
  },
  
  "tags": ["quality", "security", "automation"],
  
  "metadata": {
    "author": "Protocol Team",
    "license": "MIT",
    "created": "2026-01-23",
    "updated": "2026-01-23"
  }
}
```

### 3.2 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 技能唯一标识（kebab-case） |
| `version` | string | 语义化版本号 |
| `description` | string | 简短描述 |
| `triggers` | object | 触发条件 |
| `capabilities` | array | 提供的能力列表 |
| `dependencies` | object | 运行时依赖 |
| `entry_points` | object | 入口点映射 |
| `tags` | array | 分类标签 |
| `metadata` | object | 元信息 |

---

## 4. 技能生命周期

### 4.1 生命周期阶段（Progressive Disclosure）

```
Discovery → Activation → Execution → Deactivation
   ↓            ↓            ↓            ↓
 发现技能    加载上下文    执行能力    清理资源
```

**Progressive Disclosure 模式**（与 Claude/Antigravity 一致）：
1. **Level 1 - 元数据**：始终加载 YAML frontmatter（~100 tokens/skill）
2. **Level 2 - 指令**：触发时加载 SKILL.md 正文（<5k tokens）
3. **Level 3 - 资源**：按需加载额外文件（无限制）

### 4.2 生命周期钩子

```python
# scripts/lifecycle.py（可选实现）

def on_discover() -> dict:
    """技能被发现时调用，返回元数据"""
    return {
        "name": "guardian",
        "capabilities": ["check", "validate"]
    }

def on_activate(context: dict) -> bool:
    """技能被激活时调用，初始化资源"""
    # 检查依赖
    # 加载配置
    return True

def on_execute(capability: str, params: dict) -> dict:
    """执行具体能力"""
    if capability == "check":
        return run_check(params)
    raise ValueError(f"Unknown capability: {capability}")

def on_deactivate() -> None:
    """技能被停用时调用，清理资源"""
    pass
```

---

## 5. 能力接口

### 5.1 输入/输出规范

```python
# 标准输入结构
SkillInput = {
    "capability": str,        # 要执行的能力
    "params": dict,           # 能力参数
    "context": {
        "project_root": str,  # 项目根目录
        "tech_stack": list,   # 技术栈
        "config": dict        # 技能配置
    }
}

# 标准输出结构
SkillOutput = {
    "success": bool,          # 执行是否成功
    "results": list | dict,   # 执行结果
    "errors": list,           # 错误列表
    "warnings": list,         # 警告列表
    "metrics": dict           # 指标数据
}
```

### 5.2 示例实现

```python
# scripts/check_all.py

from pathlib import Path
from typing import TypedDict

class CheckResult(TypedDict):
    success: bool
    results: list
    errors: list
    warnings: list

def run_check(params: dict) -> CheckResult:
    """执行代码检查"""
    project_root = Path(params.get("project_root", "."))
    patterns_file = Path(__file__).parent.parent / "rules" / "banned_patterns.json"
    
    errors = []
    warnings = []
    
    # 检查逻辑...
    
    return {
        "success": len(errors) == 0,
        "results": [],
        "errors": errors,
        "warnings": warnings
    }

if __name__ == "__main__":
    import sys
    result = run_check({"project_root": sys.argv[1] if len(sys.argv) > 1 else "."})
    sys.exit(0 if result["success"] else 1)
```

---

## 6. 规则文件格式

### 6.1 标准格式

```json
{
  "$schema": "https://agent-protocol.dev/schemas/rules.json",
  "version": "1.0",
  "rules": [
    {
      "id": "rule-001",
      "name": "no-hardcoded-secrets",
      "description": "禁止硬编码密钥和密码",
      "severity": "error",
      "pattern": "(password|secret|api_key)\\s*=\\s*['\"][^'\"]+['\"]",
      "file_types": [".py", ".js", ".ts"],
      "exclude": ["**/tests/**", "**/*_test.py"],
      "fix_suggestion": "使用环境变量或配置管理"
    }
  ]
}
```

### 6.2 严重级别

| 级别 | 说明 | CI 行为 |
|------|------|---------|
| `error` | 必须修复 | 阻断 |
| `warning` | 应该修复 | 警告 |
| `info` | 建议 | 仅提示 |

---

## 7. 模板文件格式

### 7.1 模板语法

使用 `{{变量名}}` 作为占位符：

```python
# templates/component.py.template
"""{{COMPONENT_NAME}} - {{DESCRIPTION}}

Created: {{DATE}}
"""

class {{CLASS_NAME}}:
    """{{CLASS_DESCRIPTION}}"""
    
    def __init__(self):
        pass
```

### 7.2 模板变量

| 变量 | 来源 | 说明 |
|------|------|------|
| `{{PROJECT_NAME}}` | project/context.md | 项目名称 |
| `{{AUTHOR}}` | 配置或 git | 作者 |
| `{{DATE}}` | 系统 | 当前日期 |
| `{{YEAR}}` | 系统 | 当前年份 |
| 自定义变量 | 用户输入 | 按需定义 |

---

## 8. 技能发现机制

### 8.1 发现流程

```
1. 扫描 skills/ 目录
2. 查找包含 SKILL.md 的子目录
3. 读取 YAML frontmatter（name, description）
4. 读取 manifest.json（如存在）
5. 注册到技能清单
```

### 8.2 发现脚本示例

```python
# scripts/discover_skills.py

from pathlib import Path
import json
import re

def extract_frontmatter(content: str) -> dict:
    """从 SKILL.md 提取 YAML frontmatter"""
    if not content.startswith('---'):
        return {}
    
    end = content.find('---', 3)
    if end == -1:
        return {}
    
    frontmatter = content[3:end].strip()
    # 简单解析 YAML（生产环境建议使用 PyYAML）
    result = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()
    return result

def discover_skills(agent_root: Path) -> list[dict]:
    """发现所有可用技能"""
    skills = []
    skills_dir = agent_root / "skills"
    
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_md = skill_dir / "SKILL.md"
        manifest = skill_dir / "manifest.json"
        
        if not skill_md.exists():
            continue
        
        # 从 SKILL.md 提取元数据
        content = skill_md.read_text(encoding='utf-8')
        frontmatter = extract_frontmatter(content)
        
        skill_info = {
            "name": frontmatter.get("name", skill_dir.name),
            "description": frontmatter.get("description", ""),
            "path": str(skill_dir),
            "entry": str(skill_md)
        }
        
        # 合并 manifest.json（如存在）
        if manifest.exists():
            with open(manifest, 'r', encoding='utf-8') as f:
                skill_info.update(json.load(f))
        
        skills.append(skill_info)
    
    return skills
```

---

## 9. 最佳实践

### 9.1 技能开发清单

- [ ] 创建 `SKILL.md` 并包含 YAML frontmatter（name, description）
- [ ] 创建 `manifest.json` 声明元数据（可选但推荐）
- [ ] 脚本支持命令行调用
- [ ] 脚本输出结构化结果
- [ ] 提供使用示例
- [ ] 文档齐全

### 9.2 命名约定

| 元素 | 约定 | 示例 |
|------|------|------|
| 技能目录 | kebab-case | `code-guardian` |
| 脚本文件 | snake_case | `check_all.py` |
| 规则 ID | kebab-case | `no-bare-except` |
| 能力名称 | kebab-case | `banned-pattern-check` |

### 9.3 避免的模式

| 模式 | 原因 |
|------|------|
| 技能间强依赖 | 增加耦合，难以维护 |
| 硬编码路径 | 影响可移植性 |
| 无错误处理 | 影响可靠性 |
| 缺少文档 | 影响可用性 |

---

*此文件为技能模块的接口规范，所有技能应遵循此规范*
*协议版本: 2.1.0*
