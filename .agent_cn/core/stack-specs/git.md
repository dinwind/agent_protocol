# Git 工作流规约

> 定义项目的 Git 工作流和版本控制规范。

---

## 1. 分支策略

### 1.1 主要分支

| 分支 | 用途 | 保护级别 |
|------|------|----------|
| `main` | 生产就绪代码 | 高（需 PR + 审查） |
| `develop` | 开发集成分支 | 中（需 PR） |

### 1.2 临时分支

| 前缀 | 用途 | 生命周期 |
|------|------|----------|
| `feature/` | 新功能 | 合并后删除 |
| `bugfix/` | Bug 修复 | 合并后删除 |
| `hotfix/` | 紧急修复 | 合并后删除 |
| `release/` | 发布准备 | 发布后删除 |

### 1.3 分支命名

```bash
# ✅ 正确
feature/user-authentication
feature/issue-123-add-login
bugfix/fix-memory-leak
hotfix/security-patch

# ❌ 错误
Feature/UserAuth
feature_user_auth
my-branch
```

---

## 2. Commit 规范

### 2.1 Commit 消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 2.2 Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | 添加用户登录功能 |
| `fix` | Bug 修复 | 修复内存泄漏 |
| `docs` | 文档更新 | 更新 API 文档 |
| `style` | 代码格式 | 格式化代码 |
| `refactor` | 重构 | 重构用户服务 |
| `perf` | 性能优化 | 优化查询性能 |
| `test` | 测试 | 添加单元测试 |
| `build` | 构建系统 | 升级依赖版本 |
| `ci` | CI 配置 | 更新 GitHub Actions |
| `chore` | 其他 | 更新 .gitignore |
| `revert` | 回滚 | 回滚某次提交 |

### 2.3 Commit 示例

```bash
# 简单提交
feat(auth): add JWT token support

# 带正文的提交
fix(api): handle null response gracefully

The external API sometimes returns null for optional fields.
Added null checks and default values to prevent crashes.

Fixes #456

# 破坏性变更
feat(api)!: change response format

BREAKING CHANGE: The API response format has changed.
Users must update their clients to handle the new format.
```

### 2.4 Commit 检查清单

- [ ] 消息清晰描述了变更内容
- [ ] Type 正确反映变更性质
- [ ] Scope 明确（如适用）
- [ ] 相关 Issue 已关联
- [ ] 一个 commit 只做一件事

---

## 3. 工作流程

### 3.1 功能开发流程

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/user-auth

# 2. 开发并提交
git add .
git commit -m "feat(auth): implement login API"

# 3. 保持与 develop 同步
git fetch origin
git rebase origin/develop

# 4. 推送并创建 PR
git push origin feature/user-auth
# 在 GitHub/GitLab 创建 PR

# 5. 合并后删除分支
git checkout develop
git pull origin develop
git branch -d feature/user-auth
```

### 3.2 Bug 修复流程

```bash
# 1. 从相关分支创建修复分支
git checkout develop  # 或 main（如果是紧急修复）
git checkout -b bugfix/fix-memory-leak

# 2. 修复并提交
git add .
git commit -m "fix(core): resolve memory leak in cache"

# 3. 推送并创建 PR
git push origin bugfix/fix-memory-leak
```

### 3.3 发布流程

```bash
# 1. 创建发布分支
git checkout develop
git checkout -b release/1.2.0

# 2. 更新版本号和 CHANGELOG
# 编辑相关文件
git commit -m "chore(release): bump version to 1.2.0"

# 3. 合并到 main
git checkout main
git merge release/1.2.0

# 4. 打标签
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 5. 合并回 develop
git checkout develop
git merge release/1.2.0
git push origin develop

# 6. 删除发布分支
git branch -d release/1.2.0
```

---

## 4. 常用命令

### 4.1 基础操作

```bash
# 查看状态
git status

# 查看历史
git log --oneline --graph -20

# 查看差异
git diff
git diff --staged

# 暂存变更
git stash
git stash pop
git stash list
```

### 4.2 分支操作

```bash
# 查看分支
git branch -a

# 切换分支
git checkout branch-name
git switch branch-name  # Git 2.23+

# 创建并切换
git checkout -b new-branch
git switch -c new-branch  # Git 2.23+

# 删除分支
git branch -d branch-name  # 已合并
git branch -D branch-name  # 强制删除
```

### 4.3 同步操作

```bash
# 拉取更新
git fetch origin
git pull origin main

# 推送
git push origin branch-name
git push -u origin branch-name  # 设置上游

# Rebase
git rebase origin/main
git rebase -i HEAD~3  # 交互式 rebase
```

### 4.4 撤销操作

```bash
# 撤销工作区修改
git checkout -- file.txt
git restore file.txt  # Git 2.23+

# 撤销暂存
git reset HEAD file.txt
git restore --staged file.txt  # Git 2.23+

# 撤销最近一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最近一次提交（丢弃修改）
git reset --hard HEAD~1

# 回滚某次提交
git revert <commit-hash>
```

---

## 5. .gitignore 模板

```gitignore
# 编辑器
.idea/
.vscode/
*.swp
*.swo

# 系统文件
.DS_Store
Thumbs.db

# 构建产物
build/
dist/
target/
*.o
*.pyc
__pycache__/

# 依赖
node_modules/
.venv/
vendor/

# 环境配置
.env
.env.local
*.local

# 日志
*.log
logs/

# 测试覆盖率
coverage/
htmlcov/
.coverage

# IDE 配置
*.iml

# 临时文件
tmp/
temp/
*.tmp
```

---

## 6. Git Hooks

### 6.1 pre-commit 示例

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# 格式检查
if ! make fmt-check; then
    echo "Format check failed. Run 'make fmt' to fix."
    exit 1
fi

# Lint 检查
if ! make lint; then
    echo "Lint check failed."
    exit 1
fi

echo "Pre-commit checks passed."
```

### 6.2 commit-msg 示例

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z-]+\))?: .+"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "Invalid commit message format."
    echo "Expected: <type>(<scope>): <subject>"
    exit 1
fi
```

---

## 7. 协作规范

### 7.1 PR 规范

- PR 标题遵循 commit 消息格式
- 描述清晰说明变更内容
- 关联相关 Issue
- 保持 PR 大小合理（< 500 行）
- 所有 CI 检查通过
- 至少一位审查者批准

### 7.2 代码审查

- 及时响应审查请求
- 提供建设性反馈
- 区分必须修改和建议修改
- 批准前确认所有问题已解决

### 7.3 冲突解决

```bash
# 1. 拉取最新代码
git fetch origin

# 2. Rebase 到目标分支
git rebase origin/main

# 3. 解决冲突
# 编辑冲突文件
git add .
git rebase --continue

# 4. 如果需要中止
git rebase --abort
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
