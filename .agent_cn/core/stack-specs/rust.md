# Rust 开发规约

> 适用于 Rust 项目的开发规范。

---

## 1. 项目结构

### 1.1 单 crate 项目

```
project/
├── src/
│   ├── main.rs          # 二进制入口
│   ├── lib.rs           # 库入口
│   ├── config.rs
│   └── modules/
├── tests/
│   └── integration/
├── benches/
├── .agent/
├── Cargo.toml
└── README.md
```

### 1.2 Workspace 项目

```
workspace/
├── Cargo.toml           # [workspace] 配置
├── crates/
│   ├── core/
│   │   ├── src/
│   │   └── Cargo.toml
│   ├── api/
│   │   ├── src/
│   │   └── Cargo.toml
│   └── cli/
│       ├── src/
│       └── Cargo.toml
├── tests/
├── .agent/
└── README.md
```

---

## 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| crate | snake_case | `my_crate` |
| 模块 | snake_case | `user_service` |
| 类型/结构体 | PascalCase | `UserManager` |
| trait | PascalCase | `Serializable` |
| 函数/方法 | snake_case | `get_user_by_id()` |
| 变量 | snake_case | `user_count` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 枚举变体 | PascalCase | `Status::Active` |

---

## 3. 错误处理

### 3.1 使用 thiserror

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),
    
    #[error("Not found: {resource} with id {id}")]
    NotFound { resource: String, id: String },
    
    #[error("Validation error: {0}")]
    Validation(String),
}

pub type Result<T> = std::result::Result<T, AppError>;
```

### 3.2 错误传播

```rust
// ✅ 使用 ? 传播错误
fn read_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

// ❌ 避免在生产代码使用 unwrap
fn bad_example() {
    let config = std::fs::read_to_string("config.toml").unwrap(); // 危险！
}

// ⚠️ expect 用于不应失败的情况
fn init() {
    let config = std::fs::read_to_string("config.toml")
        .expect("Config file must exist"); // 提供有意义的消息
}
```

### 3.3 使用 anyhow（应用程序）

```rust
use anyhow::{Context, Result};

fn process_file(path: &str) -> Result<()> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read file: {}", path))?;
    
    // 处理逻辑
    Ok(())
}
```

---

## 4. 异步编程

### 4.1 Tokio 运行时

```rust
use tokio;

#[tokio::main]
async fn main() {
    // 异步代码
}

// 或自定义运行时
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .build()
        .unwrap();
    
    runtime.block_on(async {
        // 异步代码
    });
}
```

### 4.2 异步 trait

```rust
use async_trait::async_trait;

#[async_trait]
pub trait Repository: Send + Sync {
    async fn find_by_id(&self, id: &str) -> Result<Option<Entity>>;
    async fn save(&self, entity: &Entity) -> Result<()>;
}
```

### 4.3 并发模式

```rust
use tokio::sync::{mpsc, Mutex, RwLock};
use std::sync::Arc;

// Channel 通信
async fn producer_consumer() {
    let (tx, mut rx) = mpsc::channel(100);
    
    tokio::spawn(async move {
        tx.send("message").await.unwrap();
    });
    
    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}

// 共享状态
struct SharedState {
    cache: RwLock<HashMap<String, String>>,
    counter: Mutex<u64>,
}
```

---

## 5. 结构体设计

### 5.1 Builder 模式

```rust
#[derive(Debug, Clone)]
pub struct Config {
    host: String,
    port: u16,
    timeout: Duration,
}

#[derive(Default)]
pub struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    timeout: Option<Duration>,
}

impl ConfigBuilder {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }
    
    pub fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }
    
    pub fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            host: self.host.ok_or("host is required")?,
            port: self.port.unwrap_or(8080),
            timeout: self.timeout.unwrap_or(Duration::from_secs(30)),
        })
    }
}
```

### 5.2 使用 derive

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: String,
    pub user_name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub email: Option<String>,
}
```

---

## 6. 模块组织

### 6.1 模块声明

```rust
// src/lib.rs
pub mod config;
pub mod error;
pub mod models;
pub mod services;

// 重新导出常用类型
pub use config::Config;
pub use error::{Error, Result};
```

### 6.2 可见性

```rust
// pub - 公开
pub fn public_function() {}

// pub(crate) - crate 内可见
pub(crate) fn crate_function() {}

// pub(super) - 父模块可见
pub(super) fn parent_visible() {}

// 私有（默认）
fn private_function() {}
```

---

## 7. 测试规范

### 7.1 单元测试

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_valid_input() {
        let result = parse("valid input");
        assert!(result.is_ok());
    }

    #[test]
    fn test_parse_invalid_input_returns_error() {
        let result = parse("");
        assert!(matches!(result, Err(ParseError::EmptyInput)));
    }

    #[tokio::test]
    async fn test_async_function() {
        let result = fetch_data().await;
        assert!(result.is_ok());
    }
}
```

### 7.2 集成测试

```rust
// tests/integration/api_test.rs
use my_crate::api::Client;

#[tokio::test]
async fn test_api_workflow() {
    let client = Client::new("http://localhost:8080");
    
    // 创建
    let id = client.create_resource(&data).await.unwrap();
    
    // 查询
    let resource = client.get_resource(&id).await.unwrap();
    assert_eq!(resource.name, data.name);
    
    // 删除
    client.delete_resource(&id).await.unwrap();
}
```

### 7.3 测试数据隔离

```rust
fn generate_run_id() -> String {
    use rand::Rng;
    format!("{:08x}", rand::thread_rng().gen::<u32>())
}

#[tokio::test]
async fn test_with_isolated_data() {
    let run_id = generate_run_id();
    let test_name = format!("autotest_user_{}", run_id);
    
    // 预清理
    cleanup_test_data("autotest_").await;
    
    // 测试逻辑
    let user = create_user(&test_name).await.unwrap();
    
    // 清理
    delete_user(user.id).await.unwrap();
}
```

---

## 8. 性能优化

### 8.1 避免不必要的克隆

```rust
// ❌ 不必要的克隆
fn process(data: String) {
    let owned = data.clone(); // 不需要
}

// ✅ 使用借用
fn process(data: &str) {
    // 直接使用引用
}

// ✅ 需要所有权时取得所有权
fn consume(data: String) {
    // 拥有数据
}
```

### 8.2 使用迭代器

```rust
// ✅ 惰性迭代
let result: Vec<_> = items
    .iter()
    .filter(|x| x.is_valid())
    .map(|x| x.transform())
    .collect();

// ❌ 中间集合
let filtered: Vec<_> = items.iter().filter(|x| x.is_valid()).collect();
let result: Vec<_> = filtered.iter().map(|x| x.transform()).collect();
```

---

## 9. Cargo 配置

### 9.1 Cargo.toml

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"

[dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
thiserror = "1"

[dev-dependencies]
tokio-test = "0.4"

[profile.release]
lto = true
codegen-units = 1

[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
all = "warn"
pedantic = "warn"
```

---

## 10. 代码检查命令

```bash
# 格式化
cargo fmt

# Lint
cargo clippy -- -D warnings

# 检查（不编译）
cargo check

# 测试
cargo test

# 文档
cargo doc --no-deps --open

# 全部检查
cargo fmt --check && cargo clippy -- -D warnings && cargo test
```

---

*此文件为通用引擎规则，禁止包含任何项目特定信息*
*协议版本: 2.1.0*
