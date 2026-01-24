# AI Agent Collaboration Protocol

> 一套标准化的 AI 协作协议，将 AI 开发规范作为可复用的数字资产进行管理。

[![Protocol Version](https://img.shields.io/badge/Protocol-v2.1.0-blue.svg)](.agent/manifest.json)

---

## 设计理念

### 为什么需要 Agent Protocol？

在 AI 辅助开发时代，我们面临新的挑战：

- **知识碎片化**: AI 每次对话都从零开始，缺乏项目上下文
- **规则不一致**: 不同 AI 工具各自为政，产出风格迥异
- **经验难沉淀**: 好的实践无法系统化传承
- **代码被污染**: AI 生成的辅助代码与业务代码混杂

**Agent Protocol** 通过建立一套标准化的协议栈，解决这些问题。

---

## 核心价值

### 1. 长期主义 (Long-termism)

规则的制定不仅解决当前问题，更着眼于**项目全生命周期的经验传承**。

### 2. 资产化 (Assetization)

`.agent` 目录被视为与源代码**同等重要的数字资产**，独立于业务代码，可跨项目复用。

### 3. 防腐蚀 (Anti-corrosion)

通过严格的**物理与逻辑隔离**，防止 AI 工具污染业务代码。

---

## 架构设计

### 智能层隔离 (ILI)

```
+-----------------------------------------------------+
|                    Project Root                      |
+-----------------------------------------------------+
|  src/          业务代码层                            |
|  tests/        测试代码层                            |
+-----------------------------------------------------+
|  .agent/       智能协议层 (完全隔离)                  |
|  +-- core/         治理引擎 (通用规则)               |
|  +-- project/      实例数据 (项目特定)               |
|  +-- skills/       技能模块 (按需加载)               |
|  +-- adapters/     工具适配 (多平台支持)             |
+-----------------------------------------------------+
```

### 引擎-实例分离

| 类型 | 目录 | 职能 | 可移植性 |
|------|------|------|----------|
| **引擎文件** | `core/` | 通用治理规则 | [Y] 跨项目复用 |
| **实例文件** | `project/` | 项目特定信息 | [N] 项目专属 |

---

## 协议结构

```
.agent/
+-- start-here.md           # * AI 入口文件
+-- quick-reference.md      # 速查卡片
+-- index.md                # 文档导航
+-- manifest.json           # 加载策略
|
+-- core/                   # 治理引擎
|   +-- core-rules.md
|   +-- instructions.md
|   +-- workflows/
|   +-- stack-specs/
|
+-- project/                # 项目实例
+-- skills/                 # 技能模块
+-- adapters/               # 工具适配器
+-- scripts/                # 辅助脚本
```

---

## 快速开始

### 使用生成器 (推荐)

```bash
# 安装 cokodo-agent
pipx install cokodo-agent

# 初始化协议（以下命令等效）
co init my-project/        # 简短命令
cokodo init my-project/    # 完整命令

# 快速模式（跳过交互）
co init my-project/ -y
```

### 手动复制

```bash
# 复制协议到目标项目
cp -r .agent my-project/

# 配置项目上下文
vim my-project/.agent/project/context.md

# 验证协议
python .agent/scripts/lint-protocol.py
```

---

## 多语言版本

| 版本 | 目录 | Token 估算 |
|------|------|-----------|
| English | `.agent/` | ~22K |
| 中文 | `.agent_cn/` | ~63K |

---

## 文档

- [Usage Guide (English)](docs/usage-guide.md)
- [使用指南 (中文)](docs/usage-guide_cn.md)
- [Token 对比分析](docs/token-comparison-analysis.md)

---

*Protocol Version: 2.1.0*
