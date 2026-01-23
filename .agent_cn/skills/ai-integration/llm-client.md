# LLM 客户端设计规范

> 定义与 LLM/AI 服务交互的客户端架构和最佳实践。

---

## 1. 架构模式

### 1.1 配置与客户端分离

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    """LLM 配置（可序列化）"""
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30

class LLMClient:
    """LLM 客户端（管理连接状态）"""
    def __init__(self, config: LLMConfig):
        self._config = config
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self._session:
            await self._session.close()
```

### 1.2 Session 复用

```python
class LLMClientPool:
    """客户端连接池"""
    _instance: Optional['LLMClientPool'] = None
    
    def __init__(self, config: LLMConfig):
        self._config = config
        self._session: Optional[aiohttp.ClientSession] = None
    
    @classmethod
    def get_instance(cls, config: LLMConfig) -> 'LLMClientPool':
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance
    
    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self._config.timeout)
            )
        return self._session
```

---

## 2. 异常处理

### 2.1 统一异常层次

```python
class LLMError(Exception):
    """LLM 操作基础异常"""
    pass

class LLMConnectionError(LLMError):
    """连接错误"""
    pass

class LLMRateLimitError(LLMError):
    """速率限制"""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limited, retry after {retry_after}s")

class LLMResponseError(LLMError):
    """响应错误"""
    def __init__(self, status: int, message: str):
        self.status = status
        super().__init__(f"API error {status}: {message}")

class LLMParseError(LLMError):
    """响应解析错误"""
    pass
```

### 2.2 重试机制

```python
import asyncio
from typing import TypeVar, Callable

T = TypeVar('T')

async def with_retry(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
) -> T:
    """指数退避重试"""
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return await func()
        except LLMRateLimitError as e:
            delay = min(e.retry_after, max_delay)
            await asyncio.sleep(delay)
            last_error = e
        except LLMConnectionError as e:
            delay = min(base_delay * (2 ** attempt), max_delay)
            await asyncio.sleep(delay)
            last_error = e
        except LLMResponseError as e:
            if e.status >= 500:  # 服务器错误可重试
                delay = min(base_delay * (2 ** attempt), max_delay)
                await asyncio.sleep(delay)
                last_error = e
            else:
                raise  # 客户端错误不重试
    
    raise last_error
```

---

## 3. JSON 响应处理

### 3.1 提取 JSON

```python
import json
import re
from typing import Any

def extract_json(response: str) -> dict | None:
    """
    从 LLM 响应中提取 JSON。
    支持 Markdown 代码块格式。
    """
    # 尝试提取 Markdown 代码块
    patterns = [
        r'```json\s*([\s\S]*?)```',
        r'```\s*([\s\S]*?)```',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response)
        if match:
            content = match.group(1).strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                continue
    
    # 直接尝试解析
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        return None

def extract_json_strict(response: str) -> dict:
    """严格模式，失败时抛出异常"""
    result = extract_json(response)
    if result is None:
        raise LLMParseError(f"Failed to extract JSON from: {response[:100]}...")
    return result
```

### 3.2 JSON 模式请求

```python
async def complete_json(
    self,
    prompt: str,
    schema: dict | None = None,
) -> dict:
    """请求 JSON 格式响应"""
    messages = [
        {"role": "system", "content": "You must respond with valid JSON only."},
        {"role": "user", "content": prompt},
    ]
    
    response = await self._call_api(
        messages=messages,
        temperature=0.1,  # 低温度提高一致性
        response_format={"type": "json_object"},  # OpenAI 特定
    )
    
    return extract_json_strict(response)
```

---

## 4. 批处理模式

### 4.1 生成器模式

```python
from typing import Iterator, AsyncIterator

async def batch_process(
    items: list[Any],
    processor: Callable[[Any], Awaitable[Any]],
    concurrency: int = 5,
) -> AsyncIterator[tuple[int, Any | None, Exception | None]]:
    """
    批量处理，返回 (索引, 结果, 错误)。
    单条失败不影响整体。
    """
    semaphore = asyncio.Semaphore(concurrency)
    
    async def process_one(index: int, item: Any):
        async with semaphore:
            try:
                result = await processor(item)
                return (index, result, None)
            except Exception as e:
                logger.warning(f"Item {index} failed: {e}")
                return (index, None, e)
    
    tasks = [process_one(i, item) for i, item in enumerate(items)]
    
    for coro in asyncio.as_completed(tasks):
        yield await coro
```

### 4.2 进度报告

```python
async def batch_with_progress(
    items: list[Any],
    processor: Callable[[Any], Awaitable[Any]],
    progress_callback: Callable[[int, int], None] | None = None,
) -> list[Any]:
    """带进度回调的批处理"""
    results = [None] * len(items)
    completed = 0
    
    async for index, result, error in batch_process(items, processor):
        results[index] = result
        completed += 1
        
        if progress_callback:
            progress_callback(completed, len(items))
        
        if error:
            logger.warning(f"Item {index} failed: {error}")
    
    return results
```

---

## 5. 流式响应

### 5.1 SSE 处理

```python
async def stream_complete(
    self,
    prompt: str,
) -> AsyncIterator[str]:
    """流式生成响应"""
    messages = [{"role": "user", "content": prompt}]
    
    async with self._session.post(
        f"{self._config.base_url}/chat/completions",
        json={
            "model": self._config.model,
            "messages": messages,
            "stream": True,
        },
        headers={"Authorization": f"Bearer {self._config.api_key}"},
    ) as response:
        async for line in response.content:
            line = line.decode('utf-8').strip()
            if line.startswith('data: '):
                data = line[6:]
                if data == '[DONE]':
                    break
                try:
                    chunk = json.loads(data)
                    content = chunk['choices'][0]['delta'].get('content', '')
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue
```

---

## 6. 配置模板

### 6.1 环境变量配置

```python
import os
from dataclasses import dataclass, field

@dataclass
class LLMConfig:
    api_key: str = field(
        default_factory=lambda: os.environ.get('LLM_API_KEY', '')
    )
    base_url: str = field(
        default_factory=lambda: os.environ.get(
            'LLM_BASE_URL', 'https://api.openai.com/v1'
        )
    )
    model: str = field(
        default_factory=lambda: os.environ.get('LLM_MODEL', 'gpt-4')
    )
    temperature: float = field(
        default_factory=lambda: float(os.environ.get('LLM_TEMPERATURE', '0.7'))
    )
    max_tokens: int = field(
        default_factory=lambda: int(os.environ.get('LLM_MAX_TOKENS', '2000'))
    )

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("LLM_API_KEY is required")
```

### 6.2 多提供商支持

```python
from enum import Enum

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"

def create_client(provider: LLMProvider, config: LLMConfig) -> LLMClient:
    """工厂方法创建客户端"""
    clients = {
        LLMProvider.OPENAI: OpenAIClient,
        LLMProvider.ANTHROPIC: AnthropicClient,
        LLMProvider.DEEPSEEK: DeepSeekClient,
    }
    client_class = clients.get(provider)
    if not client_class:
        raise ValueError(f"Unsupported provider: {provider}")
    return client_class(config)
```

---

## 7. 测试策略

### 7.1 Mock 客户端

```python
class MockLLMClient(LLMClient):
    """测试用 Mock 客户端"""
    
    def __init__(self, responses: dict[str, str]):
        self._responses = responses
    
    async def complete(self, prompt: str) -> str:
        # 根据 prompt 关键词返回预设响应
        for key, response in self._responses.items():
            if key in prompt:
                return response
        return "Default mock response"

# 使用
mock = MockLLMClient({
    "分析": '{"result": "分析结果"}',
    "总结": '{"summary": "总结内容"}',
})
```

---

*此文件为 AI 集成技能的一部分*
*协议版本: 2.1.0*
