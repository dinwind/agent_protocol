# CI/CD 集成模板

> 此目录包含常用 CI/CD 平台的配置模板。

---

## 可用模板

| 文件 | 平台 | 说明 |
|------|------|------|
| `github-actions.template.yml` | GitHub Actions | GitHub 工作流配置 |
| `pre-commit-config.template.yaml` | Pre-commit | 本地提交前检查 |

---

## 使用方法

### GitHub Actions

1. 复制模板到项目根目录：
   ```bash
   cp .agent/adapters/ci/github-actions.template.yml .github/workflows/ci.yml
   ```

2. 替换 `{{PROJECT_NAME}}` 为项目名称

3. 根据项目技术栈启用/禁用相应 job

### Pre-commit

1. 安装 pre-commit：
   ```bash
   pip install pre-commit
   ```

2. 复制模板：
   ```bash
   cp .agent/adapters/ci/pre-commit-config.template.yaml .pre-commit-config.yaml
   ```

3. 安装 hooks：
   ```bash
   pre-commit install
   ```

4. 初次运行（可选）：
   ```bash
   pre-commit run --all-files
   ```

---

## 自定义

### 添加项目特定检查

在 `pre-commit-config.yaml` 中添加 local hook：

```yaml
- repo: local
  hooks:
    - id: custom-check
      name: Custom Check
      entry: python scripts/custom_check.py
      language: system
      pass_filenames: false
```

### 调整 CI 触发条件

在 `github-actions.yml` 中修改 `on` 部分：

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'tests/**'
  pull_request:
    branches: [main]
```

---

*此目录为 .agent 协议适配器的一部分*
*协议版本: 2.1.0*
