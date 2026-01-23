# {{PROJECT_NAME}} - Cursor Rules

> 此文件为 Cursor 的规则配置，充当 `.agent` 协议栈的**连接器**。

---

## 协议指针

**主协议入口**: `.agent/start-here.md`

### 核心规则

1. 每次会话开始时，阅读 `.agent/start-here.md`
2. 遵循 `.agent/core/core-rules.md` 中的不可妥协原则
3. 参考 `.agent/project/context.md` 了解项目背景

---

## 编码规范

### 文件编码
- 所有文件使用 UTF-8 编码
- `open()` 必须显式指定 `encoding='utf-8'`

### 命名规范
- `.agent/` 目录：kebab-case
- 代码文件：按技术栈规范

### 路径规范
- 使用正斜杠 `/` 作为路径分隔符
- 避免硬编码绝对路径

---

## 禁止事项

- ❌ 外部 CDN 链接
- ❌ 硬编码路径
- ❌ 裸 `except:` 捕获
- ❌ UI 硬跳变

---

## 技能参考

- 代码质量：`.agent/skills/guardian/`
- AI 集成：`.agent/skills/ai-integration/`
- 协议维护：`.agent/skills/agent-governance/`

---

*此文件由 init_agent.py 生成*
*协议版本: 2.1.0*
