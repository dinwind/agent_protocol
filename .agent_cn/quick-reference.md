# 协议速查卡片

> 一页纸快速参考，适合打印或常驻标签页。
> 
> **注**: `$AGENT_DIR` 指协议根目录（如 `.agent`、`.agent_cn`），实际名称见 `manifest.json`。

---

## 🚨 铁律清单

| ✅ 必须 | ❌ 禁止 |
|---------|---------|
| UTF-8 编码 (`encoding='utf-8'`) | 裸 `except:` 捕获 |
| 正斜杠路径 (`src/main.py`) | 硬编码绝对路径 |
| `autotest_` 测试前缀 | UI 硬跳变（无动画） |
| 动态 RunID | 外部 CDN 链接 |
| 显式错误处理 | 未授权 API 暴露 |

---

## 📛 命名速查

| 场景 | 规范 | 示例 |
|------|------|------|
| `$AGENT_DIR/` 文件 | kebab-case | `bug-prevention.md` |
| Python 类 | PascalCase | `UserManager` |
| Python 函数/变量 | snake_case | `get_user_by_id` |
| Python 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| Rust 类型 | PascalCase | `SyncTask` |
| Rust 函数/变量 | snake_case | `process_file` |
| C++ 类 | PascalCase | `FileManager` |
| C++ 方法 | camelCase | `getUserById` |
| C++ 成员变量 | m_ + camelCase | `m_userName` |
| Git 分支 | 前缀/kebab | `feature/user-auth` |

---

## 📁 协议结构

```
$AGENT_DIR/
├── start-here.md      ⭐ 入口（必读）
├── quick-reference.md 📋 本文件
├── core/              🔧 通用规则
│   ├── core-rules.md  ⚠️ 不可妥协
│   ├── instructions.md
│   └── stack-specs/   按技术栈选读
├── project/           📋 项目特定
│   ├── context.md
│   └── tech-stack.md
└── skills/            🛠️ 按需加载
```

---

## 🔧 常用命令

```bash
# 协议检查
python $AGENT_DIR/scripts/lint-protocol.py

# Token 统计
python $AGENT_DIR/scripts/token-counter.py

# 初始化新项目
python $AGENT_DIR/scripts/init_agent.py --project-name "Name" --stack python
```

---

## 📝 Commit 格式

```
<type>(<scope>): <subject>

类型: feat|fix|docs|style|refactor|perf|test|chore
```

**示例**:
- `feat(auth): add JWT refresh`
- `fix(api): handle null response`
- `docs(readme): update setup guide`

---

## 🧪 测试数据

```python
# Python
run_id = uuid.uuid4().hex[:8]
test_name = f"autotest_user_{run_id}"

# 预清理
db.query(User).filter(User.name.startswith('autotest_')).delete()
```

```rust
// Rust
let run_id = format!("{:08x}", rand::random::<u32>());
let test_name = format!("autotest_user_{}", run_id);
```

---

## 📊 代码质量阈值

| 指标 | 阈值 |
|------|------|
| 圈复杂度 | ≤ 10 |
| 函数行数 | ≤ 50 |
| 文件行数 | ≤ 500 |
| 参数数量 | ≤ 5 |
| 嵌套深度 | ≤ 4 |
| 测试覆盖率 | ≥ 60% |
| 关键路径覆盖 | ≥ 80% |

---

## 🔗 快速链接

| 场景 | 文档 |
|------|------|
| 开始任务前 | `workflows/pre-task-checklist.md` |
| 编码时 | `stack-specs/{python,rust,qt}.md` |
| 写测试时 | `workflows/testing.md` |
| 遇到 Bug | `workflows/bug-prevention.md` |
| 提交前 | `conventions.md` |
| AI 集成 | `skills/ai-integration/` |
| 代码审查 | `workflows/review-process.md` |

---

## ⚡ 紧急检查

提交前 30 秒检查：

- [ ] `encoding='utf-8'` 已指定
- [ ] 无硬编码路径/密钥
- [ ] 测试通过
- [ ] 无 lint 错误

---

*协议版本: 2.1.0*
