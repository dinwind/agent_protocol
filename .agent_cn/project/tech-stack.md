# 技术栈与环境说明

> **注意**: 这是项目实例模板，使用时需替换为实际项目信息。

---

## 技术栈概览

| 类别 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **语言** | {{LANGUAGE}} | {{LANG_VERSION}} | 主要开发语言 |
| **框架** | {{FRAMEWORK}} | {{FW_VERSION}} | 应用框架 |
| **数据库** | {{DATABASE}} | {{DB_VERSION}} | 数据持久化 |
| **测试** | {{TEST_FW}} | {{TEST_VERSION}} | 自动化测试 |

---

## 开发环境

### 系统要求

- **操作系统**: {{OS_REQUIREMENT}}
- **内存**: >= {{MIN_RAM}}
- **磁盘**: >= {{MIN_DISK}}

### 环境搭建

#### 1. 安装依赖

```powershell
# {{INSTALL_COMMAND}}
```

#### 2. 配置环境

```powershell
# {{CONFIG_COMMAND}}
```

#### 3. 验证安装

```powershell
# {{VERIFY_COMMAND}}
```

---

## 项目配置

### 配置文件

| 文件 | 用途 | 示例 |
|------|------|------|
| `{{CONFIG_FILE}}` | 主配置 | `config/{{CONFIG_FILE}}.example` |
| `.env` | 环境变量 | `.env.example` |

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `{{ENV_VAR_1}}` | ✅ | {{ENV_VAR_1_DESC}} |
| `{{ENV_VAR_2}}` | ❌ | {{ENV_VAR_2_DESC}} |

---

## 常用命令

### 开发

```powershell
# 启动开发服务器
{{DEV_SERVER_CMD}}

# 运行测试
{{TEST_CMD}}

# 代码检查
{{LINT_CMD}}
```

### 构建

```powershell
# 开发构建
{{DEV_BUILD_CMD}}

# 生产构建
{{PROD_BUILD_CMD}}
```

### 部署

```powershell
# 部署到测试环境
{{DEPLOY_TEST_CMD}}

# 部署到生产环境
{{DEPLOY_PROD_CMD}}
```

---

## 目录结构

```
{{PROJECT_NAME}}/
├── src/                    # 源代码
├── tests/                  # 测试代码
├── docs/                   # 文档
├── config/                 # 配置文件
├── scripts/                # 辅助脚本
├── .agent/                 # AI 协议层
├── {{CONFIG_FILE}}         # 项目配置
└── README.md               # 项目说明
```

---

## 依赖管理

### 主要依赖

详见 `{{DEPS_FILE}}` (如 `requirements.txt`, `Cargo.toml`, `package.json`)

### 添加依赖规则

1. 优先使用已有依赖解决问题
2. 新依赖需评估：
   - 维护活跃度
   - 许可证兼容性
   - 包大小影响
3. 记录添加原因

---

## 编码规范

详见：
- [core/stack-specs/{{STACK}}.md](../../.agent/core/stack-specs/{{STACK}}.md)
- [core/conventions.md](../../.agent/core/conventions.md)

---

*此文件为项目实例数据，包含特定项目信息*
*最后更新: {{LAST_UPDATE}}*
