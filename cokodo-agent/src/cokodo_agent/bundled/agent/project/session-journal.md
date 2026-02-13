# Session Journal

> agent_protocol AI 会话日志

---

## 2026-01-26 Session: 协议 v3.0 发布与全项目迁移

### Completed
- 完成协议 v3.0 架构设计
- 统一 start-here.md 为纯入口模板
- 标准化 project/ 目录结构
- 同步 core/, adapters/, meta/, scripts/ 到所有项目
- 创建 agent-protocol-rules.md 操作约束规范

### Technical Debt
- 无

### Decisions
- 采用引擎-实例分离架构
- skills/ 采用混合策略（标准 skill 同步，项目特定放 _project/）

---

*Append new sessions below this line.*

## 2026-01-26 Session: cokodo-agent v1.2.0 开发

### Completed
- 重新设计 lint-protocol.py，实现 8 项协议合规检查规则
- 实现 SHA256 文件完整性校验机制，checksums 存储于 manifest.json
- 开发 `co lint` 命令 - 协议合规性检查（支持 text/json/github 输出格式）
- 开发 `co diff` 命令 - 对比本地与最新协议差异
- 开发 `co sync` 命令 - 同步协议更新（保留 project/ 目录）
- 开发 `co context` 命令 - 基于 manifest.json loading_strategy 动态加载上下文
- 开发 `co update-checksums` 命令 - 更新锁定文件签名
- 开发 `co journal` 命令 - 记录会话日志
- 创建 linter.py 和 sync.py 模块
- 同步 lint-protocol.py 和 manifest.json 到 8 个工作区项目
- 更新 README.md 和 usage-guide_cn.md 文档

### Technical Debt
- 无

### Decisions
- 保持 checksums + lint + sync 机制，不采用文件只读或打包方案
- co journal 支持交互模式和命令行模式两种使用方式

---
