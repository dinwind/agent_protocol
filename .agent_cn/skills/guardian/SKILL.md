---
name: guardian
description: |
  质量守护技能 - 代码与文档的自动化检查与质量门禁。
  支持禁用模式检测、架构层次验证、测试策略检查、文档格式规范等。
---

# Guardian Skill

> 质量守护技能 - 代码与文档的自动化检查与质量门禁

---

## 技能概述

| 属性 | 值 |
|------|-----|
| 名称 | Guardian |
| 版本 | 2.0.0 |
| 类型 | 自动化检查 |
| 触发 | PR/Commit 前检查 |

## 功能模块

### 1. 代码守护 (Code Guardian)

- **禁用模式检测** - 识别代码中的反模式和禁用调用
- **架构层次验证** - 确保代码遵循分层架构
- **测试策略检查** - 验证测试命名和隔离规则
- **编码规范检查** - UTF-8、命名规范等

### 2. 内容守护 (Content Guardian)

- **格式规范检测** - 检查 Markdown 语法、标题层级、列表格式
- **术语一致性** - 验证专业术语与标准一致
- **死链检查** - 扫描文档中的失效图片链接和内部跳转
- **数学公式验证** - 检查 LaTeX 公式语法是否正确

---

## 规则配置

### 禁用模式 (rules/banned_patterns.json)

```json
{
  "version": "2.0",
  "patterns": [
    {
      "id": "no-hardcoded-paths",
      "pattern": "C:\\\\|D:\\\\|/home/|/Users/",
      "severity": "error",
      "message": "禁止硬编码绝对路径，使用配置或环境变量",
      "scope": "code"
    },
    {
      "id": "no-print-debug",
      "pattern": "print\\s*\\(.*debug|console\\.log",
      "severity": "warning",
      "message": "请使用日志系统代替 print/console.log",
      "scope": "code"
    },
    {
      "id": "no-bare-except",
      "pattern": "except\\s*:",
      "severity": "error",
      "message": "禁止裸 except，请指定具体异常类型",
      "scope": "code"
    },
    {
      "id": "no-encoding-missing",
      "pattern": "open\\([^)]*\\)(?!.*encoding)",
      "severity": "error",
      "message": "open() 必须显式指定 encoding='utf-8'",
      "scope": "code"
    },
    {
      "id": "no-unsafe-unwrap",
      "pattern": "\\.unwrap\\(\\)",
      "severity": "warning",
      "message": "避免在生产代码中使用 unwrap()，请使用 ? 或 expect()",
      "scope": "rust"
    }
  ]
}
```

### 架构层次 (rules/layers.json)

```json
{
  "version": "2.0",
  "layers": [
    {
      "name": "presentation",
      "patterns": ["*/ui/*", "*/views/*", "*/qml/*", "*/gui/*"],
      "can_import": ["application", "domain"],
      "cannot_import": ["infrastructure", "data"]
    },
    {
      "name": "application",
      "patterns": ["*/services/*", "*/use_cases/*"],
      "can_import": ["domain"],
      "cannot_import": ["presentation", "infrastructure"]
    },
    {
      "name": "domain",
      "patterns": ["*/models/*", "*/entities/*", "*/core/*"],
      "can_import": [],
      "cannot_import": ["presentation", "application", "infrastructure"]
    },
    {
      "name": "infrastructure",
      "patterns": ["*/data/*", "*/repositories/*", "*/api/*", "*/db/*"],
      "can_import": ["domain"],
      "cannot_import": ["presentation", "application"]
    }
  ]
}
```

### 测试策略 (rules/test_policy.json)

```json
{
  "version": "2.0",
  "naming": {
    "test_prefix": "autotest_",
    "run_id_pattern": "[a-f0-9]{8}",
    "required_format": "autotest_{run_id}_{description}"
  },
  "isolation": {
    "require_cleanup": true,
    "temp_dir_required": true,
    "no_shared_state": true
  },
  "coverage": {
    "minimum": 60,
    "critical_paths": 80
  }
}
```

### 内容规范 (rules/content_policy.json)

```json
{
  "version": "1.0",
  "markdown": {
    "max_heading_level": 4,
    "require_alt_text": true,
    "require_code_language": true
  },
  "links": {
    "check_internal": true,
    "check_external": false,
    "allowed_protocols": ["https", "http", "mailto"]
  }
}
```

---

## 使用方法

### 1. 手动检查

```bash
# 运行所有检查
python .agent/skills/guardian/scripts/check_all.py

# 仅代码检查
python .agent/skills/guardian/scripts/check_code.py src/

# 仅文档检查
python .agent/skills/guardian/scripts/check_content.py docs/

# 仅架构检查
python .agent/skills/guardian/scripts/check_layers.py src/
```

### 2. AI 协作触发

```
[AI 内部流程]
1. 代码/文档修改完成
2. 调用 Guardian 检查
3. 如有违规，自动修复或报告
4. 通过后才提交
```

### 3. CI/CD 集成

```yaml
# .github/workflows/guardian.yml
name: Guardian
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Guardian Checks
        run: python .agent/skills/guardian/scripts/check_all.py
```

---

## 目录结构

```
skills/guardian/
├── SKILL.md                # 技能说明（本文件）
├── rules/
│   ├── banned_patterns.json
│   ├── layers.json
│   ├── test_policy.json
│   └── content_policy.json
└── scripts/
    ├── check_all.py        # 完整检查
    ├── check_code.py       # 代码检查
    ├── check_content.py    # 内容检查
    └── check_layers.py     # 架构检查
```

---

## 扩展规则

### 添加新的禁用模式

1. 编辑 `rules/banned_patterns.json`
2. 添加新规则条目，指定 `scope` (code/rust/python/markdown)
3. 测试：`python scripts/check_code.py --test`

### 自定义严重级别

| 级别 | 行为 |
|------|------|
| `error` | 阻止提交 |
| `warning` | 警告但允许 |
| `info` | 仅记录 |

---

## 与其他技能协作

- **Agent Governance**: 协议遵守检查
- **AI Integration**: AI 生成代码质量保证
- **QML UI Style**: UI 代码规范验证

---

*此技能为可移植组件，可在多项目间复用*
*版本: 2.0.0*
