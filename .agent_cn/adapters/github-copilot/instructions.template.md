# {{PROJECT_NAME}} - GitHub Copilot Instructions

> 此文件为 GitHub Copilot 的指令配置，充当 `.agent` 协议栈的**连接器**。

---

## 协议指针 (Protocol Pointers)

**主协议入口**: `.agent/start-here.md`

### 优先级权重 (Priority Weights)

| 文档 | 权重 | 说明 |
|------|------|------|
| `.agent/core/core-rules.md` | ⭐⭐⭐ | 不可妥协的核心规则 |
| `.agent/core/instructions.md` | ⭐⭐⭐ | AI 协作准则 |
| `.agent/core/conventions.md` | ⭐⭐ | 命名与 Git 约定 |
| `.agent/project/context.md` | ⭐⭐ | 项目业务上下文 |
| `.agent/project/tech-stack.md` | ⭐⭐ | 技术栈说明 |
| `.agent/core/stack-specs/{{STACK}}.md` | ⭐⭐ | 技术栈规约 |

---

## 核心指令

### 1. 协议遵守

在每次代码生成或修改前，请参考 `.agent/start-here.md` 中定义的规则。

### 2. 命名规范

- **Python**: 类名 PascalCase，函数/变量 snake_case
- **Rust**: 类型 PascalCase，函数/变量 snake_case
- **文件**: `.agent/` 目录下使用 kebab-case

### 3. 编码要求

- 所有文件使用 UTF-8 编码
- `open()` 必须显式指定 `encoding='utf-8'`
- 路径分隔符使用正斜杠 `/`

### 4. 测试数据

- 使用 `autotest_` 前缀
- 使用动态 RunID
- 测试前执行预清理

---

## 禁止事项

1. ❌ 不要引入外部 CDN 链接
2. ❌ 不要使用硬编码路径
3. ❌ 不要使用裸 `except:`
4. ❌ 不要在 UI 中使用硬跳变

---

## 技能调用

当需要特定能力时，参考：

- 代码质量检查: `.agent/skills/guardian/SKILL.md`
- AI 集成开发: `.agent/skills/ai-integration/`
- 协议维护: `.agent/skills/agent-governance/SKILL.md`

---

*此文件为适配器模板，由 `scripts/init_agent.py` 生成*
*协议版本: 2.1.0*
