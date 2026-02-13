# ADR-004: v3.1.0 改进方案

**状态**: Proposed
**日期**: 2026-02-13
**来源**: AuthNexus / Axlinker 实战经验复盘

---

## 背景

基于 AuthNexus 和 Axlinker 两个项目对 v3.0.0 协议的实际使用情况，总结出以下改进方向。
Axlinker 的 `.agent` 继承自 AuthNexus 并独立演进，两者的共性需求代表了协议模板的结构性缺口。

---

## 变更清单

### A. 新增标准模板（P0）

| 编号 | 文件 | 依据 |
|------|------|------|
| A1 | `templates/project/deploy.md` | 两项目均自发创建部署文档（server-info.md / deploy-verification.md） |
| A2 | `templates/project/conventions.md` | Axlinker 创建了项目级约定补充文件 |

### B. 增强现有机制（P1）

| 编号 | 目标 | 内容 |
|------|------|------|
| B1 | ADR 工作流 | 新增触发规则 + 轻量模板，降低 ADR 记录门槛 |
| B2 | Skill 参数化 | 更新 skill-interface.md，支持配置驱动的多后端策略 |
| B3 | Token 预算 | 新增文档量管理指南，防止协议文档膨胀 |

### C. 结构同步（P0）

| 编号 | 目标 | 内容 |
|------|------|------|
| C1 | agent-protocol-rules.md | 将新增模板注册到目录结构、必需文件列表、权限矩阵 |
| C2 | manifest.json | 注册新文件到 loading_strategy 和 required_files |

### D. 待评估项（TODO — 后续单独讨论）

| 编号 | 主题 | 状态 |
|------|------|------|
| D1 | `me/` 目录标准化 | 初期探索，暂不扩大；探索方向：在 AI 执行不同阶段对人类思考和输入做标准化要求 |
| D2 | 跨项目对齐/依赖 | 需深入讨论 `project/dependencies.md` 的设计 |
| D3 | Cursor / Claude Code 适配器策略 | 详见下方评估目标 |

---

## D3 详细说明：AI IDE 适配器评估目标

### 核心原则
- 保持 `.agent` 的**独立有效性**（不依赖任何特定 IDE 即可使用）
- 借助 AI IDE 的自动加载功能，将 `.agent/start-here.md` 作为入口被自动发现

### 评估范围

| IDE/Tool | 原生规则机制 | 加载方式 | 需评估内容 |
|----------|------------|----------|-----------|
| **Cursor** | `.cursor/rules/*.mdc` | frontmatter glob + alwaysApply | 如何自动引导到 start-here.md；哪些 core 规则应生成为 .mdc |
| **Claude Code** | `CLAUDE.md` / `.claude/` | 项目根自动加载 | 如何作为指针指向 .agent；内容粒度控制 |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 仓库级自动加载 | 指针模板是否够用 |

### 预期产出
1. 每个 IDE 的适配器生成脚本（从 .agent 自动生成 IDE 原生配置）
2. 映射规范文档（哪些规则同步、哪些仅保留在 .agent）
3. 冲突解决策略（当 IDE 规则与 .agent 规则不一致时）

---

## 版本规划

- 当前: v3.0.0
- 目标: v3.1.0（向后兼容，新增功能）
- 范围: A + B + C（D 项不纳入本版本）

---

*本 ADR 为改进方案总纲，各项具体实现见对应文件变更。*
