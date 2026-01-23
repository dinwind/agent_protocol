# 安全开发规范

> 定义项目安全开发的标准和检查清单。

---

## 1. 敏感数据处理

### 1.1 禁止硬编码

```python
# ❌ 严禁
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "mysecretpassword"

# ✅ 正确 - 使用环境变量
import os
API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

# ✅ 正确 - 使用配置管理
from config import settings
API_KEY = settings.api_key
```

### 1.2 敏感数据分类

| 级别 | 数据类型 | 处理要求 |
|------|----------|----------|
| **L1 极敏感** | 密钥、密码、令牌 | 加密存储，不记录日志 |
| **L2 敏感** | 个人身份信息、财务数据 | 加密传输，访问控制 |
| **L3 内部** | 业务数据、配置 | 访问控制 |
| **L4 公开** | 公开信息 | 无特殊要求 |

### 1.3 日志脱敏

```python
# ❌ 错误 - 记录敏感信息
logger.info(f"User login: {username}, password: {password}")

# ✅ 正确 - 脱敏处理
logger.info(f"User login: {username}, password: ****")

# ✅ 正确 - 使用脱敏函数
def mask_sensitive(value: str, visible: int = 4) -> str:
    if len(value) <= visible:
        return "****"
    return value[:visible] + "****"

logger.info(f"Token: {mask_sensitive(token)}")
```

---

## 2. 认证与授权

### 2.1 认证规范

```python
# 密码哈希 - 使用 bcrypt 或 argon2
from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)
```

### 2.2 会话管理

| 要求 | 说明 |
|------|------|
| 会话超时 | 默认 30 分钟无活动后过期 |
| 安全 Cookie | 设置 `HttpOnly`, `Secure`, `SameSite` |
| 会话 ID | 使用加密安全的随机数生成 |
| 登出处理 | 服务端销毁会话 |

### 2.3 授权检查

```python
# ✅ 正确 - 每个敏感操作都检查权限
def delete_user(current_user: User, target_user_id: int):
    if not current_user.has_permission("user:delete"):
        raise PermissionDeniedError()
    
    if current_user.id == target_user_id:
        raise InvalidOperationError("Cannot delete yourself")
    
    # 执行删除
```

---

## 3. 输入验证

### 3.1 验证原则

```
永远不要信任用户输入
在边界处验证，在内部假设已验证
```

### 3.2 验证模式

```python
from pydantic import BaseModel, validator, constr

class UserInput(BaseModel):
    username: constr(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
    email: str
    age: int
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
    
    @validator('age')
    def validate_age(cls, v):
        if not 0 < v < 150:
            raise ValueError('Invalid age')
        return v
```

### 3.3 常见攻击防护

| 攻击类型 | 防护措施 |
|----------|----------|
| SQL 注入 | 参数化查询，ORM |
| XSS | 输出编码，CSP |
| CSRF | CSRF Token |
| 路径遍历 | 路径规范化，白名单 |
| 命令注入 | 避免 shell，参数化 |

```python
# SQL 注入防护
# ❌ 危险
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ 安全 - 参数化查询
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, (user_id,))

# ✅ 安全 - ORM
user = session.query(User).filter(User.id == user_id).first()
```

---

## 4. 依赖安全

### 4.1 依赖扫描

```bash
# Python
pip-audit
safety check

# Rust
cargo audit

# Node.js
npm audit

# 通用
snyk test
```

### 4.2 依赖管理规则

| 规则 | 说明 |
|------|------|
| 锁定版本 | 使用 lock 文件固定版本 |
| 定期更新 | 每月检查安全更新 |
| 最小依赖 | 仅引入必要依赖 |
| 来源可信 | 使用官方源 |

### 4.3 许可证检查

确保依赖许可证与项目兼容：

| 许可证 | 商业项目兼容性 |
|--------|----------------|
| MIT | ✅ 兼容 |
| Apache 2.0 | ✅ 兼容 |
| BSD | ✅ 兼容 |
| GPL | ⚠️ 需评估 |
| AGPL | ❌ 通常不兼容 |

---

## 5. 安全配置

### 5.1 生产环境配置

```yaml
# ✅ 生产环境安全配置示例
security:
  debug: false
  allowed_hosts:
    - "example.com"
    - "*.example.com"
  
  ssl:
    enabled: true
    redirect_http: true
    hsts_max_age: 31536000
  
  cors:
    allowed_origins:
      - "https://example.com"
    allow_credentials: true
  
  rate_limit:
    enabled: true
    requests_per_minute: 60
```

### 5.2 HTTP 安全头

```python
# 推荐的安全响应头
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
}
```

---

## 6. 错误处理

### 6.1 安全错误响应

```python
# ❌ 危险 - 暴露内部信息
@app.errorhandler(Exception)
def handle_error(e):
    return {"error": str(e), "traceback": traceback.format_exc()}

# ✅ 安全 - 隐藏内部信息
@app.errorhandler(Exception)
def handle_error(e):
    logger.exception("Unhandled exception")  # 内部记录
    return {"error": "Internal server error"}, 500  # 外部通用消息
```

### 6.2 错误信息分级

| 环境 | 错误详情 |
|------|----------|
| 开发 | 完整堆栈跟踪 |
| 测试 | 错误类型和消息 |
| 生产 | 仅通用错误提示 |

---

## 7. 审计日志

### 7.1 必须记录的事件

| 事件类型 | 示例 |
|----------|------|
| 认证事件 | 登录、登出、密码修改 |
| 授权事件 | 权限变更、访问拒绝 |
| 数据变更 | 创建、修改、删除关键数据 |
| 系统事件 | 配置变更、服务启停 |
| 安全事件 | 攻击尝试、异常访问 |

### 7.2 日志格式

```json
{
  "timestamp": "2026-01-23T10:30:00Z",
  "level": "INFO",
  "event_type": "auth.login",
  "user_id": "user123",
  "ip_address": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "result": "success",
  "details": {
    "method": "password"
  }
}
```

---

## 8. 安全检查清单

### 8.1 开发阶段

- [ ] 无硬编码敏感信息
- [ ] 输入已验证和消毒
- [ ] 使用参数化查询
- [ ] 输出已编码
- [ ] 错误处理不暴露内部信息
- [ ] 日志不包含敏感数据

### 8.2 代码审查

- [ ] 认证逻辑正确
- [ ] 授权检查完整
- [ ] 加密使用正确
- [ ] 依赖无已知漏洞
- [ ] 安全配置正确

### 8.3 发布前

- [ ] 依赖安全扫描通过
- [ ] 代码安全扫描通过
- [ ] 敏感信息检查通过
- [ ] 安全配置已审查
- [ ] 渗透测试（如适用）

---

## 9. 应急响应

### 9.1 安全事件分级

| 级别 | 描述 | 响应时间 |
|------|------|----------|
| P1 | 数据泄露、系统入侵 | 立即 |
| P2 | 服务中断、DDoS | 1 小时内 |
| P3 | 漏洞发现、异常行为 | 24 小时内 |
| P4 | 安全改进建议 | 下个迭代 |

### 9.2 响应流程

```
发现 → 确认 → 遏制 → 根除 → 恢复 → 总结
```

1. **发现**: 监控告警或人工报告
2. **确认**: 验证是否为真实安全事件
3. **遏制**: 限制影响范围
4. **根除**: 消除安全威胁
5. **恢复**: 恢复正常服务
6. **总结**: 事后分析和改进

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
