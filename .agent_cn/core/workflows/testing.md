# 测试协议

> 定义项目的测试策略、数据隔离和质量标准。

---

## 1. 测试金字塔

```
        /\
       /  \
      / E2E \        少量端到端测试
     /--------\
    /Integration\    适量集成测试
   /--------------\
  /   Unit Tests   \ 大量单元测试
 /------------------\
```

### 各层比例建议

| 类型 | 比例 | 执行频率 |
|------|------|----------|
| 单元测试 | 70% | 每次提交 |
| 集成测试 | 20% | 每次 PR |
| E2E 测试 | 10% | 每日/发布前 |

---

## 2. 测试数据隔离 ⭐⭐⭐

### 2.1 强制规则

1. **动态 RunID**: 每次测试生成唯一标识
2. **专用前缀**: 使用 `autotest_` 前缀
3. **预清理**: 测试开始前清理残留数据

### 2.2 实现示例

**Python**:
```python
import uuid
import pytest

@pytest.fixture
def run_id():
    """生成测试运行 ID"""
    return uuid.uuid4().hex[:8]

@pytest.fixture
def test_user(run_id, db_session):
    """创建测试用户"""
    # 预清理
    db_session.query(User).filter(
        User.name.startswith('autotest_')
    ).delete()
    
    # 创建测试数据
    user = User(name=f"autotest_user_{run_id}")
    db_session.add(user)
    db_session.commit()
    
    yield user
    
    # 清理
    db_session.delete(user)
    db_session.commit()
```

**Rust**:
```rust
fn generate_run_id() -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    format!("{:08x}", rng.gen::<u32>())
}

#[tokio::test]
async fn test_create_user() {
    let run_id = generate_run_id();
    let user_name = format!("autotest_user_{}", run_id);
    
    // 预清理
    cleanup_test_data("autotest_").await;
    
    // 测试逻辑
    let user = create_user(&user_name).await.unwrap();
    assert_eq!(user.name, user_name);
    
    // 清理
    delete_user(user.id).await.unwrap();
}
```

---

## 3. 测试命名规范

### 3.1 测试文件

```
tests/
├── unit/
│   └── test_user_service.py
├── integration/
│   └── test_user_api.py
└── e2e/
    └── test_user_flow.py
```

### 3.2 测试函数

**格式**: `test_<功能>_<场景>_<预期>`

```python
# ✅ 好的命名
def test_login_with_valid_credentials_returns_token():
    ...

def test_login_with_invalid_password_raises_error():
    ...

def test_create_user_when_email_exists_fails():
    ...

# ❌ 不好的命名
def test_login():  # 太笼统
    ...

def test1():  # 无意义
    ...
```

---

## 4. 测试覆盖率

### 4.1 最低要求

| 类型 | 最低覆盖率 |
|------|-----------|
| 整体 | 60% |
| 关键路径 | 80% |
| 新代码 | 80% |

### 4.2 关键路径定义

- 认证/授权逻辑
- 支付/交易逻辑
- 数据持久化逻辑
- 核心业务规则

### 4.3 覆盖率工具

**Python**:
```bash
pytest --cov=src --cov-report=html
```

**Rust**:
```bash
cargo tarpaulin --out Html
```

---

## 5. 测试独立性

### 5.1 原则

每个测试必须：

- ✅ 可单独运行
- ✅ 不依赖其他测试的执行顺序
- ✅ 不依赖外部状态
- ✅ 自行设置和清理状态

### 5.2 反模式

```python
# ❌ 错误 - 依赖全局状态
global_counter = 0

def test_increment():
    global global_counter
    global_counter += 1
    assert global_counter == 1  # 如果其他测试先运行会失败

# ✅ 正确 - 独立状态
def test_increment():
    counter = Counter()
    counter.increment()
    assert counter.value == 1
```

---

## 6. Mock 使用规范

### 6.1 何时使用 Mock

- ✅ 外部服务（API、数据库）
- ✅ 时间相关操作
- ✅ 随机数生成
- ✅ 文件系统操作

### 6.2 何时避免 Mock

- ❌ 核心业务逻辑
- ❌ 简单的数据转换
- ❌ 可以用真实对象的情况

### 6.3 示例

```python
from unittest.mock import Mock, patch

def test_send_notification(mocker):
    # Mock 外部 API
    mock_api = mocker.patch('services.notification_api.send')
    mock_api.return_value = {"status": "sent"}
    
    # 测试业务逻辑
    result = notification_service.notify_user(user_id=1, message="Hello")
    
    # 验证调用
    mock_api.assert_called_once_with(
        user_id=1,
        message="Hello"
    )
    assert result.success is True
```

---

## 7. 异步测试

### 7.1 Python

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_service.fetch_data()
    assert result is not None
```

### 7.2 Rust

```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_service::fetch_data().await;
    assert!(result.is_ok());
}
```

---

## 8. 测试检查清单

### 提交前

- [ ] 所有测试通过
- [ ] 新代码有对应测试
- [ ] 测试数据使用动态 RunID
- [ ] 无跳过的测试（除非有充分理由）

### PR 前

- [ ] 覆盖率达标
- [ ] 集成测试通过
- [ ] 无测试警告

### 发布前

- [ ] E2E 测试通过
- [ ] 性能测试无退化
- [ ] 关键路径 100% 覆盖

---

## 9. 测试配置

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
asyncio_mode = auto
addopts = -v --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

### Cargo.toml

```toml
[dev-dependencies]
tokio-test = "0.4"
mockall = "0.11"

[[test]]
name = "integration"
path = "tests/integration/main.rs"
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
