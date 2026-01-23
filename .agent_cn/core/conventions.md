# 命名规范与约定 (Conventions)

本文件定义项目中的命名规范、Git 约定和文档格式标准。

---

## 1. 文件命名规范

### 1.1 协议目录 ($AGENT_DIR/)

**强制使用 kebab-case（零例外）**

| 类型 | 正确 ✅ | 错误 ❌ |
|------|---------|---------|
| Markdown | `start-here.md`, `bug-prevention.md` | `StartHere.md`, `bug_prevention.md` |
| 目录 | `stack-specs/`, `ai-integration/` | `StackSpecs/`, `ai_integration/` |
| JSON | `banned_patterns.json` | `BannedPatterns.json` |

### 1.2 源代码目录

按技术栈规范执行：

| 技术栈 | 文件 | 目录 |
|--------|------|------|
| Python | `snake_case.py` | `snake_case/` |
| Rust | `snake_case.rs` | `snake_case/` |
| C++/Qt | `PascalCase.cpp` | `PascalCase/` |
| QML | `PascalCase.qml` | `components/` |

---

## 2. 代码命名规范

### 2.1 Python

```python
# 类名: PascalCase
class UserManager:
    pass

# 函数/方法: snake_case
def get_user_by_id(user_id: int) -> User:
    pass

# 变量: snake_case
user_count = 0
current_user = None

# 常量: UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 私有属性: 单下划线前缀
class Config:
    def __init__(self):
        self._cache = {}      # 私有
        self.timeout = 30     # 公开

# 模块级私有: 单下划线前缀
_internal_cache = {}
```

### 2.2 Rust

```rust
// 类型: PascalCase
struct UserManager {
    users: Vec<User>,
}

// 枚举: PascalCase，变体也是 PascalCase
enum Status {
    Active,
    Inactive,
    Pending,
}

// 函数/方法: snake_case
fn get_user_by_id(user_id: u64) -> Option<User> {
    None
}

// 变量: snake_case
let user_count = 0;
let mut current_user = None;

// 常量: UPPER_SNAKE_CASE
const MAX_RETRY_COUNT: u32 = 3;
static DEFAULT_TIMEOUT: u64 = 30;

// 模块: snake_case
mod user_manager;
```

### 2.3 C++/Qt

```cpp
// 类名: PascalCase
class UserManager {
public:
    // 公共方法: camelCase
    User* getUserById(int userId);
    
private:
    // 私有成员: m_ 前缀 + camelCase
    int m_userCount;
    QList<User*> m_users;
};

// 函数: camelCase
void processUserData();

// 常量/宏: UPPER_SNAKE_CASE
#define MAX_RETRY_COUNT 3
const int DEFAULT_TIMEOUT = 30;
```

---

## 3. Git 约定

### 3.1 分支命名

```
main              # 主分支，始终可部署
develop           # 开发分支
feature/xxx       # 功能分支
bugfix/xxx        # Bug 修复分支
hotfix/xxx        # 紧急修复分支
release/x.x.x     # 发布分支
```

### 3.2 Commit 消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响逻辑） |
| `refactor` | 重构（不新增功能或修复 Bug） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具变更 |

#### 示例

```
feat(auth): add JWT token refresh mechanism

- Implement automatic token refresh before expiry
- Add refresh token storage in secure cookie
- Update auth middleware to handle refresh flow

Closes #123
```

### 3.3 提交检查清单

提交前必须确认：

- [ ] 代码符合命名规范
- [ ] 无 lint 错误
- [ ] 测试通过
- [ ] Commit 消息规范

---

## 4. 文档格式标准

### 4.1 Markdown 规范

```markdown
# 一级标题（文档标题，仅一个）

> 文档简介或重要提示

---

## 二级标题（主要章节）

### 三级标题（子章节）

#### 四级标题（最深层级，避免更深）
```

### 4.2 代码块

必须指定语言标签：

````markdown
```python
def hello():
    print("Hello, World!")
```
````

### 4.3 表格

对齐和格式：

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
```

### 4.4 链接

- 内部链接使用相对路径
- 外部链接使用完整 URL

```markdown
[内部文档](../project/context.md)
[外部链接](https://example.com)
```

---

## 5. 版本号规范

### 5.1 语义化版本 (SemVer)

```
MAJOR.MINOR.PATCH

1.0.0  → 首个稳定版本
1.1.0  → 向后兼容的新功能
1.1.1  → 向后兼容的 Bug 修复
2.0.0  → 不兼容的 API 变更
```

### 5.2 预发布版本

```
1.0.0-alpha.1  → Alpha 测试版
1.0.0-beta.1   → Beta 测试版
1.0.0-rc.1     → 发布候选版
```

---

## 6. 注释规范

### 6.1 Python Docstring

```python
def calculate_total(items: list[Item], tax_rate: float = 0.1) -> float:
    """
    计算订单总金额（含税）。
    
    Args:
        items: 订单项列表
        tax_rate: 税率，默认 10%
    
    Returns:
        含税总金额
    
    Raises:
        ValueError: 当 items 为空时
    
    Example:
        >>> items = [Item(price=100), Item(price=200)]
        >>> calculate_total(items)
        330.0
    """
    if not items:
        raise ValueError("Items cannot be empty")
    subtotal = sum(item.price for item in items)
    return subtotal * (1 + tax_rate)
```

### 6.2 Rust Doc Comments

```rust
/// 计算订单总金额（含税）。
///
/// # Arguments
///
/// * `items` - 订单项列表
/// * `tax_rate` - 税率，默认 10%
///
/// # Returns
///
/// 含税总金额
///
/// # Errors
///
/// 当 `items` 为空时返回 `CalculationError::EmptyItems`
///
/// # Examples
///
/// ```
/// let items = vec![Item::new(100.0), Item::new(200.0)];
/// let total = calculate_total(&items, 0.1)?;
/// assert_eq!(total, 330.0);
/// ```
pub fn calculate_total(items: &[Item], tax_rate: f64) -> Result<f64, CalculationError> {
    // ...
}
```

---

## 7. 日志规范

### 7.1 日志级别

| 级别 | 用途 |
|------|------|
| `DEBUG` | 调试信息，仅开发环境 |
| `INFO` | 常规运行信息 |
| `WARNING` | 警告，不影响运行 |
| `ERROR` | 错误，需要关注 |
| `CRITICAL` | 严重错误，影响服务 |

### 7.2 日志格式

```
[时间] [级别] [模块] 消息
2026-01-23 10:30:00 INFO  [auth] User login successful: user_id=123
2026-01-23 10:30:01 ERROR [db] Connection failed: timeout after 30s
```

---

## 8. 开发日志规范

### 8.1 格式

```markdown
## YYYY-MM-DD

### 完成
- [x] 任务描述

### 进行中
- [ ] 任务描述（进度说明）

### 问题
- 问题描述及处理方式

### 明日计划
- 计划的任务
```

### 8.2 位置

开发日志记录在 `lessons/` 目录下，按日期命名：

```
lessons/
└── 2026-01-23-feature-name.md
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
