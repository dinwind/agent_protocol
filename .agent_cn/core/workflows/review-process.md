# 代码审查流程

> 定义代码审查的标准流程和最佳实践。

---

## 1. 审查流程概览

```
提交 PR
    ↓
自动检查（CI）
    ↓
分配审查者
    ↓
代码审查
    ↓
修改/讨论
    ↓
批准
    ↓
合并
```

---

## 2. PR 提交规范

### 2.1 PR 标题

格式: `<type>(<scope>): <description>`

```
feat(auth): add JWT refresh token support
fix(api): handle null response from external service
docs(readme): update installation instructions
```

### 2.2 PR 描述模板

```markdown
## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 文档 (docs)
- [ ] 测试 (test)
- [ ] 其他

## 变更描述
[描述本次变更的内容和原因]

## 相关 Issue
Closes #xxx

## 测试说明
[描述如何测试这些变更]

## 检查清单
- [ ] 代码符合项目规范
- [ ] 已添加必要的测试
- [ ] 文档已更新
- [ ] 本地测试通过

## 截图（如适用）
[UI 变更的截图]
```

### 2.3 PR 大小

| 大小 | 行数 | 审查时间 | 建议 |
|------|------|----------|------|
| XS | < 50 | 10 min | ✅ 理想 |
| S | 50-200 | 30 min | ✅ 推荐 |
| M | 200-500 | 1 hour | ⚠️ 可接受 |
| L | 500-1000 | 2 hours | ⚠️ 考虑拆分 |
| XL | > 1000 | > 2 hours | ❌ 必须拆分 |

---

## 3. 审查者职责

### 3.1 审查重点

1. **正确性**: 实现是否符合需求？
2. **设计**: 架构是否合理？
3. **可读性**: 代码是否易于理解？
4. **安全性**: 是否有安全隐患？
5. **测试**: 测试是否充分？

### 3.2 审查态度

**应该**:
- ✅ 提供建设性反馈
- ✅ 解释修改建议的原因
- ✅ 认可好的实现
- ✅ 提问而非指责

**避免**:
- ❌ 人身攻击
- ❌ 不解释的否定
- ❌ 过于主观的偏好
- ❌ 拖延审查

### 3.3 响应时间

| 优先级 | 首次响应 | 后续响应 |
|--------|----------|----------|
| 紧急 | 2 小时内 | 1 小时内 |
| 高 | 4 小时内 | 2 小时内 |
| 普通 | 1 工作日内 | 4 小时内 |

---

## 4. 反馈分类

### 4.1 反馈类型

| 前缀 | 含义 | 必须处理 |
|------|------|----------|
| `[Blocking]` | 阻止合并，必须修改 | ✅ |
| `[Suggestion]` | 建议，可讨论 | ⚠️ |
| `[Nitpick]` | 小问题，可忽略 | ❌ |
| `[Question]` | 疑问，需解答 | ⚠️ |
| `[Praise]` | 表扬好的实现 | - |

### 4.2 反馈示例

```markdown
[Blocking] 这里存在 SQL 注入风险，需要使用参数化查询。

[Suggestion] 考虑将这个逻辑抽取为独立函数，提高可复用性。

[Nitpick] 这个变量名可以更具描述性，比如 `user_count` 而非 `cnt`。

[Question] 这里为什么选择使用递归而非迭代？

[Praise] 这个错误处理方式很优雅！
```

---

## 5. 审查检查清单

### 5.1 功能审查

- [ ] 实现符合需求描述
- [ ] 边界情况已处理
- [ ] 错误情况已处理
- [ ] 向后兼容（如适用）

### 5.2 代码质量

- [ ] 命名清晰有意义
- [ ] 函数职责单一
- [ ] 无重复代码
- [ ] 复杂度可接受
- [ ] 符合项目规范

### 5.3 安全审查

- [ ] 无硬编码凭据
- [ ] 输入已验证
- [ ] 无注入风险
- [ ] 敏感数据已保护

### 5.4 测试审查

- [ ] 测试覆盖新功能
- [ ] 测试覆盖边界情况
- [ ] 测试命名清晰
- [ ] 测试独立可重复

### 5.5 文档审查

- [ ] 公共 API 有文档
- [ ] 复杂逻辑有注释
- [ ] README 已更新（如需要）

---

## 6. 常见审查意见

### 6.1 命名问题

```python
# 问题代码
def proc(d):
    return [x for x in d if x > 0]

# 审查意见
# [Blocking] 请使用有意义的名称：
def filter_positive_numbers(numbers):
    return [n for n in numbers if n > 0]
```

### 6.2 错误处理

```python
# 问题代码
def get_user(id):
    return db.query(User).filter_by(id=id).first()

# 审查意见
# [Suggestion] 建议处理用户不存在的情况：
def get_user(id):
    user = db.query(User).filter_by(id=id).first()
    if user is None:
        raise UserNotFoundError(f"User {id} not found")
    return user
```

### 6.3 安全问题

```python
# 问题代码
query = f"SELECT * FROM users WHERE id = {user_id}"

# 审查意见
# [Blocking] SQL 注入风险！使用参数化查询：
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))
```

---

## 7. 合并策略

### 7.1 合并方式

| 方式 | 使用场景 | Git 命令 |
|------|----------|----------|
| Merge | 保留完整历史 | `git merge` |
| Squash | 合并为单个提交 | `git merge --squash` |
| Rebase | 线性历史 | `git rebase` |

### 7.2 推荐策略

- **功能分支 → main**: Squash merge
- **发布分支 → main**: Merge commit
- **热修复 → main**: Merge commit

### 7.3 合并前检查

- [ ] 所有 CI 检查通过
- [ ] 至少 1 位审查者批准
- [ ] 所有 Blocking 问题已解决
- [ ] 分支已更新到最新 main

---

## 8. 审查工具

### 8.1 GitHub/GitLab 功能

- 行级评论
- 建议更改 (Suggested changes)
- 代码所有者 (CODEOWNERS)
- 状态检查 (Status checks)

### 8.2 辅助工具

- **Reviewpad**: 自动化 PR 工作流
- **Danger**: PR 自动检查
- **CodeClimate**: 代码质量分析

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
