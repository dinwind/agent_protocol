# Bug 预防知识库

> 记录项目中遇到的 Bug 根因，防止同类问题再次发生。

---

## 使用方法

1. **编码前**: 浏览相关章节，了解常见陷阱
2. **修复后**: 将新发现的 Bug 根因添加到此文档
3. **代码审查**: 检查是否触犯已知陷阱

---

## 1. 编码类 Bug

### 1.1 UTF-8 编码问题

**问题**: 文件读写时未指定编码，导致跨平台乱码

```python
# ❌ 错误
with open('file.txt', 'r') as f:
    content = f.read()

# ✅ 正确
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()
```

**根因**: Windows 默认使用 GBK，Linux/Mac 默认 UTF-8

**预防**: 所有 `open()` 必须显式指定 `encoding='utf-8'`

---

### 1.2 路径分隔符问题

**问题**: 使用反斜杠导致 Git Bash 等环境路径解析失败

```python
# ❌ 错误
path = "src\\main.py"

# ✅ 正确
path = "src/main.py"
# 或
from pathlib import Path
path = Path("src") / "main.py"
```

**根因**: 反斜杠在 Unix shell 中被解释为转义字符

**预防**: 统一使用正斜杠或 `pathlib`

---

### 1.3 裸 except 捕获

**问题**: 裸 `except:` 捕获所有异常，包括系统退出

```python
# ❌ 错误
try:
    do_something()
except:
    pass  # 吞掉所有异常，包括 KeyboardInterrupt

# ✅ 正确
try:
    do_something()
except Exception as e:
    logger.error(f"Error: {e}")
    raise
```

**根因**: `except:` 会捕获 `BaseException`，包括 `KeyboardInterrupt`、`SystemExit`

**预防**: 始终指定具体异常类型，至少使用 `Exception`

---

### 1.4 可变默认参数

**问题**: 使用可变对象作为默认参数

```python
# ❌ 错误
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ 正确
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**根因**: 默认参数在函数定义时求值，所有调用共享同一对象

**预防**: 可变默认参数使用 `None`，在函数内初始化

---

## 2. 异步/并发类 Bug

### 2.1 阻塞异步上下文

**问题**: 在异步函数中使用阻塞调用

```python
# ❌ 错误
async def fetch_data():
    time.sleep(1)  # 阻塞整个事件循环
    return data

# ✅ 正确
async def fetch_data():
    await asyncio.sleep(1)  # 非阻塞
    return data
```

**根因**: 阻塞调用会暂停整个事件循环，影响所有协程

**预防**: 异步上下文中使用 `await` 版本的 API

---

### 2.2 竞态条件

**问题**: 多线程访问共享状态未加锁

```python
# ❌ 错误
counter = 0
def increment():
    global counter
    counter += 1  # 非原子操作

# ✅ 正确
counter = 0
lock = threading.Lock()
def increment():
    global counter
    with lock:
        counter += 1
```

**根因**: `counter += 1` 实际是读-改-写三步操作

**预防**: 共享状态访问必须使用锁或原子操作

---

## 3. 配置类 Bug

### 3.1 配置硬编码

**问题**: 配置值硬编码在代码中

```python
# ❌ 错误
def connect():
    return Database("localhost:5432/mydb")

# ✅ 正确
def connect():
    return Database(config.database_url)
```

**根因**: 硬编码导致环境切换困难，敏感信息泄露

**预防**: 配置通过 ConfigManager 集中管理

---

### 3.2 配置缺失默认值

**问题**: 读取配置时未处理缺失情况

```python
# ❌ 错误
timeout = config['timeout']  # KeyError if missing

# ✅ 正确
timeout = config.get('timeout', 30)  # 提供默认值
```

**根因**: 配置文件可能缺少某些键

**预防**: 始终提供合理的默认值

---

## 4. 测试类 Bug

### 4.1 测试数据冲突

**问题**: 测试使用固定名称，与手动测试数据冲突

```python
# ❌ 错误
def test_create_user():
    user = User(name="test_user")  # 可能已存在

# ✅ 正确
def test_create_user():
    run_id = uuid.uuid4().hex[:8]
    user = User(name=f"autotest_user_{run_id}")
```

**根因**: 固定名称在多次运行或并发测试时冲突

**预防**: 使用动态 RunID 和 `autotest_` 前缀

---

### 4.2 测试依赖顺序

**问题**: 测试之间存在隐式依赖

```python
# ❌ 错误
def test_a():
    global_state.value = 1

def test_b():
    assert global_state.value == 1  # 依赖 test_a 先执行

# ✅ 正确
def test_b():
    # 独立设置所需状态
    global_state.value = 1
    assert global_state.value == 1
```

**根因**: 测试执行顺序不确定

**预防**: 每个测试独立设置和清理状态

---

## 5. UI 类 Bug

### 5.1 硬跳变

**问题**: UI 状态变化没有过渡动画

```qml
// ❌ 错误
visible: isExpanded

// ✅ 正确
opacity: isExpanded ? 1 : 0
Behavior on opacity {
    NumberAnimation { duration: 250 }
}
```

**根因**: 直接改变属性导致视觉突变

**预防**: 使用 Behavior 或 Transition 添加动画

---

### 5.2 布局重心跳动

**问题**: 内容变化导致布局重心移动

```qml
// ❌ 错误 - 宽度变化导致跳动
width: contentWidth

// ✅ 正确 - 固定宽度或使用 anchors
anchors.left: parent.left
anchors.right: parent.right
```

**根因**: 动态内容改变容器尺寸

**预防**: 使用固定尺寸或锚点布局

---

## 6. Rust 特定 Bug

### 6.1 Unwrap Panic

**问题**: 在生产代码中使用 `unwrap()`

```rust
// ❌ 错误
let config = fs::read_to_string("config.toml").unwrap();

// ✅ 正确
let config = fs::read_to_string("config.toml")
    .context("Failed to read config file")?;
```

**根因**: `unwrap()` 在 `None`/`Err` 时 panic

**预防**: 使用 `?` 传播错误或 `expect()` 提供有意义的消息

---

### 6.2 生命周期悬垂引用

**问题**: 返回对局部变量的引用

```rust
// ❌ 错误
fn get_name() -> &str {
    let name = String::from("Alice");
    &name  // name 在函数结束时被释放
}

// ✅ 正确
fn get_name() -> String {
    String::from("Alice")
}
```

**根因**: 引用的生命周期不能超过被引用数据

**预防**: 理解所有权和借用规则

---

## 记录模板

```markdown
### X.X 问题简述

**问题**: 一句话描述问题现象

**代码示例**:
```language
# ❌ 错误示例

# ✅ 正确示例
```

**根因**: 问题的根本原因

**预防**: 如何避免此问题
```

---

*此文件持续更新，发现新 Bug 后必须记录*
*协议版本: 2.1.0*
