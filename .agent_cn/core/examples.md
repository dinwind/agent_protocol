# 协议代码示例 (Protocol Code Examples)

> 本文件包含协议中提到的最佳实践代码示例，按需加载。

---

## 1. UTF-8 显式编码 (UTF-8 Explicit Encoding)

在所有文件读写操作中，必须显式指定 UTF-8 编码。

### Python
```python
# ✅ 正确
with open('file.txt', 'r', encoding='utf-8') as f:
    content = f.read()

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(content)
```

### Rust
```rust
// Rust 默认使用 UTF-8
use std::fs;
let content = fs::read_to_string("file.txt")?; 
```

### PowerShell
```powershell
# 在脚本开头设置默认编码
$InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

---

## 2. 测试数据隔离 (Test Data Isolation)

使用动态生成的 `RunID` 和统一前缀 `autotest_` 进行数据隔离。

### Python
```python
import uuid

RUN_ID = uuid.uuid4().hex[:8]
TEST_USER = f"autotest_user_{RUN_ID}"
TEST_DATA = f"autotest_data_{RUN_ID}"

# 预清理逻辑
def cleanup():
    old_test_data = db.query(User).filter(User.name.startswith('autotest_')).all()
    for item in old_test_data:
        db.delete(item)
```

### TypeScript / JavaScript
```typescript
const RUN_ID = Math.random().toString(36).substring(2, 7);
const TEST_USER = `autotest_user_${RUN_ID}`;

// 预清理逻辑
async function cleanup() {
  const oldTestData = await db.findMany({
    where: { name: { startsWith: 'autotest_' } }
  });
  for (const item of oldTestData) {
    await db.delete(item.id);
  }
}
```

---

## 3. 终端 UTF-8 设置 (Terminal UTF-8 Setup)

### PowerShell
```powershell
# 设置控制台输出编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
chcp 65001
```

### Bash
```bash
# 确保 locale 设置正确
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

---

*此文件为参考示例，按需加载。*
