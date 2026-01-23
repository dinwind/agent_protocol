# Python 开发规约

> 适用于 Python 3.10+ 项目的开发规范。

---

## 1. 项目结构

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
├── .agent/
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块 | snake_case | `user_service.py` |
| 类 | PascalCase | `UserManager` |
| 函数/方法 | snake_case | `get_user_by_id()` |
| 变量 | snake_case | `user_count` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 私有 | _前缀 | `_internal_cache` |

---

## 3. 类型注解

### 3.1 强制使用类型注解

```python
# ✅ 正确
def get_user(user_id: int) -> User | None:
    ...

def process_items(items: list[Item]) -> dict[str, int]:
    ...

# ❌ 错误
def get_user(user_id):
    ...
```

### 3.2 常用类型

```python
from typing import Any, Callable, TypeVar, Generic
from collections.abc import Iterable, Mapping

# 可选类型
def find_user(id: int) -> User | None:
    ...

# 联合类型
def parse_input(value: str | int) -> str:
    ...

# 泛型
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## 4. 文件操作

### 4.1 必须指定编码

```python
# ✅ 正确
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ 错误 - 缺少编码
with open('file.txt', 'r') as f:
    content = f.read()
```

### 4.2 使用 pathlib

```python
from pathlib import Path

# ✅ 推荐
config_path = Path(__file__).parent / 'config' / 'settings.yaml'
if config_path.exists():
    content = config_path.read_text(encoding='utf-8')

# ⚠️ 可接受但不推荐
config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yaml')
```

---

## 5. 异常处理

### 5.1 具体异常

```python
# ✅ 正确 - 捕获具体异常
try:
    result = api.fetch_data()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise
except TimeoutError as e:
    logger.warning(f"Request timeout: {e}")
    return None

# ❌ 错误 - 裸 except
try:
    result = api.fetch_data()
except:
    pass
```

### 5.2 自定义异常

```python
class AppError(Exception):
    """应用基础异常"""
    pass

class ValidationError(AppError):
    """验证错误"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """资源未找到"""
    def __init__(self, resource: str, id: Any):
        super().__init__(f"{resource} with id {id} not found")
```

---

## 6. 日志规范

### 6.1 使用 logging

```python
import logging

logger = logging.getLogger(__name__)

def process_order(order: Order) -> None:
    logger.info(f"Processing order: {order.id}")
    try:
        # 处理逻辑
        logger.debug(f"Order details: {order}")
    except Exception as e:
        logger.error(f"Failed to process order {order.id}: {e}")
        raise
```

### 6.2 日志级别

| 级别 | 用途 |
|------|------|
| DEBUG | 详细调试信息 |
| INFO | 常规运行信息 |
| WARNING | 警告，不影响运行 |
| ERROR | 错误，需要关注 |
| CRITICAL | 严重错误 |

---

## 7. 异步编程

### 7.1 async/await

```python
import asyncio
from aiohttp import ClientSession

async def fetch_data(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_all(urls: list[str]) -> list[dict]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### 7.2 避免阻塞

```python
# ❌ 错误 - 阻塞异步上下文
async def bad_example():
    time.sleep(1)  # 阻塞！
    
# ✅ 正确 - 使用异步版本
async def good_example():
    await asyncio.sleep(1)

# 如果必须调用同步代码
async def run_sync_in_async():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, sync_function)
```

---

## 8. 测试规范

### 8.1 pytest 配置

```python
# conftest.py
import pytest

@pytest.fixture
def db_session():
    """数据库会话 fixture"""
    session = create_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def run_id():
    """测试运行 ID"""
    import uuid
    return uuid.uuid4().hex[:8]
```

### 8.2 测试命名

```python
def test_create_user_with_valid_data_succeeds():
    ...

def test_create_user_with_duplicate_email_raises_error():
    ...

def test_get_user_when_not_exists_returns_none():
    ...
```

---

## 9. AI/LLM 集成速查

### 9.1 客户端设计

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class LLMConfig:
    api_key: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000

class LLMClient:
    def __init__(self, config: LLMConfig):
        self._config = config
        self._session = None
    
    async def complete(self, prompt: str) -> str:
        # 实现调用逻辑
        ...
```

### 9.2 JSON 响应提取

```python
import json
import re

def extract_json(response: str) -> dict | None:
    """从 LLM 响应中提取 JSON"""
    # 尝试提取 Markdown 代码块
    pattern = r'```(?:json)?\s*([\s\S]*?)```'
    match = re.search(pattern, response)
    
    content = match.group(1) if match else response
    
    try:
        return json.loads(content.strip())
    except json.JSONDecodeError:
        return None
```

### 9.3 批处理

```python
from typing import Iterator, TypeVar

T = TypeVar('T')

def batch_process(
    items: list[T],
    processor: Callable[[T], Any],
    batch_size: int = 10
) -> Iterator[Any]:
    """批量处理，单条失败不影响整体"""
    for i, item in enumerate(items):
        try:
            yield processor(item)
        except Exception as e:
            logger.warning(f"Item {i} failed: {e}")
            yield None
```

---

## 10. 依赖管理

### 10.1 pyproject.toml

```toml
[project]
name = "project-name"
version = "0.1.0"
requires-python = ">=3.10"

dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "mypy>=1.0",
    "ruff>=0.1",
]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.mypy]
python_version = "3.10"
strict = true
```

### 10.2 requirements.txt

```
# 生产依赖
pydantic>=2.0,<3.0
httpx>=0.24,<1.0

# 锁定版本
# pip freeze > requirements-lock.txt
```

---

## 11. 代码检查命令

```bash
# 格式化
ruff format src/ tests/

# Lint
ruff check src/ tests/ --fix

# 类型检查
mypy src/

# 测试
pytest tests/ -v --cov=src

# 全部检查
ruff format src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
