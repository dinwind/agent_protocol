# 质量保证流程

> 定义代码质量保证的标准流程和检查点。

---

## 1. 质量门禁

### 1.1 提交前检查

```bash
# 自动化检查脚本示例
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# 1. 代码格式化
echo "Formatting code..."
# Python: black src/ tests/
# Rust: cargo fmt --check

# 2. Lint 检查
echo "Running linter..."
# Python: ruff check src/ tests/
# Rust: cargo clippy -- -D warnings

# 3. 类型检查
echo "Type checking..."
# Python: mypy src/

# 4. 单元测试
echo "Running unit tests..."
# Python: pytest tests/unit/
# Rust: cargo test --lib

echo "All checks passed!"
```

### 1.2 PR 检查

| 检查项 | 必须通过 | 说明 |
|--------|----------|------|
| 代码格式 | ✅ | 符合项目格式规范 |
| Lint | ✅ | 无错误，警告已审查 |
| 类型检查 | ✅ | 类型注解完整 |
| 单元测试 | ✅ | 所有测试通过 |
| 集成测试 | ✅ | 相关测试通过 |
| 覆盖率 | ⚠️ | 不低于基准线 |
| 代码审查 | ✅ | 至少 1 人批准 |

### 1.3 发布检查

| 检查项 | 必须通过 | 说明 |
|--------|----------|------|
| 全部测试 | ✅ | 包括 E2E |
| 性能测试 | ⚠️ | 无明显退化 |
| 安全扫描 | ✅ | 无高危漏洞 |
| 文档同步 | ✅ | 文档已更新 |
| 变更日志 | ✅ | CHANGELOG 已更新 |

---

## 2. 代码质量标准

### 2.1 复杂度限制

| 指标 | 阈值 | 说明 |
|------|------|------|
| 圈复杂度 | ≤ 10 | 单个函数 |
| 函数行数 | ≤ 50 | 不含注释和空行 |
| 文件行数 | ≤ 500 | 建议拆分 |
| 参数数量 | ≤ 5 | 考虑使用对象 |
| 嵌套深度 | ≤ 4 | 提前返回 |

### 2.2 命名质量

```python
# ❌ 差的命名
def proc(d):
    for i in d:
        ...

# ✅ 好的命名
def process_orders(orders: list[Order]):
    for order in orders:
        ...
```

### 2.3 注释质量

```python
# ❌ 无用注释
i += 1  # 增加 i

# ✅ 有价值的注释
# 使用指数退避策略，避免请求风暴
retry_delay = base_delay * (2 ** attempt)
```

---

## 3. 静态分析配置

### 3.1 Python (ruff.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # allow assert in tests
```

### 3.2 Rust (clippy)

```toml
# .cargo/config.toml
[target.'cfg(all())']
rustflags = [
    "-Wclippy::all",
    "-Wclippy::pedantic",
    "-Wclippy::nursery",
    "-Aclippy::module_name_repetitions",
]
```

---

## 4. 代码审查标准

### 4.1 审查检查清单

**功能正确性**
- [ ] 实现符合需求
- [ ] 边界情况已处理
- [ ] 错误处理完善

**代码质量**
- [ ] 命名清晰有意义
- [ ] 逻辑清晰易懂
- [ ] 无重复代码
- [ ] 符合设计原则

**安全性**
- [ ] 无敏感信息硬编码
- [ ] 输入已验证
- [ ] 无 SQL 注入风险
- [ ] 无 XSS 风险

**可维护性**
- [ ] 有必要的注释
- [ ] 测试充分
- [ ] 文档已更新

### 4.2 审查反馈模板

```markdown
## 整体评价
[总体印象]

## 优点
- 优点 1
- 优点 2

## 建议修改
### 必须修改 (Blocking)
1. [文件:行号] 问题描述
   建议: ...

### 建议修改 (Non-blocking)
1. [文件:行号] 问题描述
   建议: ...

## 疑问
1. [文件:行号] 疑问内容
```

---

## 5. 性能检查

### 5.1 性能基准

| 场景 | 目标 | 测量方式 |
|------|------|----------|
| 冷启动 | < 2s | 首次加载时间 |
| API 响应 | < 200ms | P95 延迟 |
| 内存占用 | < 500MB | 稳态内存 |
| CPU 占用 | < 30% | 空闲时平均 |

### 5.2 性能测试

```python
import pytest
from pytest_benchmark.fixture import BenchmarkFixture

def test_performance(benchmark: BenchmarkFixture):
    result = benchmark(target_function, arg1, arg2)
    assert result.mean < 0.1  # 平均执行时间 < 100ms
```

---

## 6. 安全检查

### 6.1 依赖扫描

```bash
# Python
pip-audit

# Rust
cargo audit

# Node.js
npm audit
```

### 6.2 代码扫描

```bash
# Python
bandit -r src/

# 通用
semgrep --config auto src/
```

### 6.3 安全检查清单

- [ ] 无硬编码凭据
- [ ] 敏感数据已加密
- [ ] 输入已验证和消毒
- [ ] 输出已编码
- [ ] 使用参数化查询
- [ ] 认证机制安全
- [ ] 授权检查完整
- [ ] 日志无敏感信息

---

## 7. 持续集成

### 7.1 CI 流水线

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Format Check
        run: |
          # 格式检查命令
          
      - name: Lint
        run: |
          # Lint 命令
          
      - name: Type Check
        run: |
          # 类型检查命令
          
      - name: Test
        run: |
          # 测试命令
          
      - name: Coverage
        run: |
          # 覆盖率检查命令
```

### 7.2 质量报告

每次 CI 运行后生成：

- 测试报告
- 覆盖率报告
- Lint 报告
- 安全扫描报告

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
