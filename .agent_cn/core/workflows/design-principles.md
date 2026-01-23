# 架构设计原则

> 指导项目架构决策的核心原则。

---

## 1. SSOT - 单一真实数据源

### 原则

每类数据只有**唯一**的权威来源，其他地方通过引用获取。

### 应用

```python
# ❌ 违反 SSOT - 多处定义配置
class ServiceA:
    timeout = 30

class ServiceB:
    timeout = 30  # 重复定义，容易不一致

# ✅ 遵循 SSOT - 配置集中管理
class Config:
    timeout = 30

class ServiceA:
    def __init__(self, config: Config):
        self.timeout = config.timeout
```

### 检查清单

- [ ] 配置是否集中管理？
- [ ] 常量是否只定义一次？
- [ ] 状态是否有唯一来源？

---

## 2. 依赖注入

### 原则

组件不自行创建依赖，而是从外部接收。

### 应用

```python
# ❌ 硬依赖 - 难以测试和替换
class UserService:
    def __init__(self):
        self.db = PostgresDatabase()  # 硬编码依赖
        self.cache = RedisCache()

# ✅ 依赖注入 - 灵活可测试
class UserService:
    def __init__(self, db: Database, cache: Cache):
        self.db = db
        self.cache = cache

# 使用时注入
db = PostgresDatabase()
cache = RedisCache()
service = UserService(db, cache)

# 测试时注入 Mock
mock_db = MockDatabase()
mock_cache = MockCache()
test_service = UserService(mock_db, mock_cache)
```

### 检查清单

- [ ] 依赖是否通过构造函数或参数传入？
- [ ] 是否可以轻松替换依赖进行测试？
- [ ] 是否避免了全局状态？

---

## 3. 简单优先

### 原则

选择最简单的解决方案，除非有明确理由需要复杂方案。

### 应用

```python
# ❌ 过度设计 - 为单一用途创建复杂抽象
class AbstractStrategyFactory:
    def create_strategy(self, type: str) -> Strategy:
        ...

# ✅ 简单优先 - 直接解决问题
def get_discount(user_type: str) -> float:
    discounts = {
        "regular": 0.0,
        "vip": 0.1,
        "premium": 0.2,
    }
    return discounts.get(user_type, 0.0)
```

### 检查清单

- [ ] 是否有更简单的方案？
- [ ] 复杂度是否与问题规模匹配？
- [ ] 是否在解决实际问题而非假设问题？

---

## 4. 分层架构

### 原则

代码按职责分层，层间单向依赖。

### 标准分层

```
┌─────────────────────────┐
│     Presentation        │  UI、API 接口
├─────────────────────────┤
│     Application         │  业务流程、用例
├─────────────────────────┤
│       Domain            │  核心业务逻辑
├─────────────────────────┤
│    Infrastructure       │  数据库、外部服务
└─────────────────────────┘

依赖方向: 上层 → 下层
禁止: 下层 → 上层
```

### 应用

```python
# domain/ - 核心业务，无外部依赖
class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

# application/ - 业务流程，依赖 domain
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    def get_user(self, id: int) -> User:
        return self.user_repo.find_by_id(id)

# infrastructure/ - 数据访问，实现 domain 接口
class PostgresUserRepository(UserRepository):
    def find_by_id(self, id: int) -> User:
        # 数据库访问逻辑
        ...
```

### 检查清单

- [ ] 每个模块职责是否单一？
- [ ] 依赖方向是否正确？
- [ ] Domain 层是否无外部依赖？

---

## 5. 接口隔离

### 原则

不强迫依赖方依赖不需要的接口。

### 应用

```python
# ❌ 胖接口 - 强迫实现不需要的方法
class Repository:
    def find(self, id): ...
    def find_all(self): ...
    def save(self, entity): ...
    def delete(self, id): ...
    def export_to_csv(self): ...  # 不是所有仓库都需要

# ✅ 接口隔离 - 按需组合
class Readable:
    def find(self, id): ...
    def find_all(self): ...

class Writable:
    def save(self, entity): ...
    def delete(self, id): ...

class Exportable:
    def export_to_csv(self): ...

# 按需实现
class UserRepository(Readable, Writable):
    ...
```

---

## 6. 防腐层

### 原则

隔离外部系统/遗留代码，防止其复杂性污染核心代码。

### 应用

```python
# 外部 API 返回的复杂结构
external_response = {
    "usr_nm": "alice",
    "usr_email_addr": "alice@example.com",
    "crt_dt": "2026-01-23T10:00:00Z"
}

# 防腐层 - 转换为内部模型
class ExternalUserAdapter:
    @staticmethod
    def to_user(data: dict) -> User:
        return User(
            name=data["usr_nm"],
            email=data["usr_email_addr"],
            created_at=parse_datetime(data["crt_dt"])
        )

# 核心代码使用干净的内部模型
user = ExternalUserAdapter.to_user(external_response)
```

### 检查清单

- [ ] 外部数据是否在边界处转换？
- [ ] 核心代码是否依赖外部数据结构？
- [ ] 外部 API 变更是否只影响适配层？

---

## 7. 快速失败

### 原则

发现错误时立即报告，不要尝试"修复"或忽略。

### 应用

```python
# ❌ 静默失败 - 隐藏问题
def get_user(id: int) -> User:
    try:
        return db.find_user(id)
    except:
        return None  # 调用方不知道发生了什么

# ✅ 快速失败 - 明确报告错误
def get_user(id: int) -> User:
    user = db.find_user(id)
    if user is None:
        raise UserNotFoundError(f"User {id} not found")
    return user
```

### 检查清单

- [ ] 是否在入口处验证参数？
- [ ] 错误是否被明确报告？
- [ ] 是否避免了静默失败？

---

## 8. 契约式设计

### 原则

明确定义函数的前置条件、后置条件和不变式。

### 应用

```python
def withdraw(account: Account, amount: float) -> None:
    """
    从账户取款。
    
    前置条件:
        - amount > 0
        - account.balance >= amount
    
    后置条件:
        - account.balance == old_balance - amount
    
    不变式:
        - account.balance >= 0
    """
    # 检查前置条件
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if account.balance < amount:
        raise InsufficientFundsError()
    
    # 执行操作
    account.balance -= amount
    
    # 后置条件由设计保证
    assert account.balance >= 0, "Balance invariant violated"
```

---

## 设计决策检查清单

在做架构决策时，逐一检查：

- [ ] 是否遵循 SSOT？
- [ ] 依赖是否可注入？
- [ ] 是否选择了最简单的方案？
- [ ] 分层是否清晰？
- [ ] 接口是否足够小？
- [ ] 是否隔离了外部复杂性？
- [ ] 是否快速失败？
- [ ] 契约是否明确？

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
