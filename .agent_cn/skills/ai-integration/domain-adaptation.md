# 领域适配方法论

> 定义将 AI/LLM 能力适配到特定业务领域的方法和最佳实践。

---

## 1. 领域适配三要素

### 1.1 信息建模

将领域知识结构化，便于 AI 理解和处理：

```python
from dataclasses import dataclass
from typing import Any

@dataclass
class DomainEntity:
    """领域实体基类"""
    id: str
    name: str
    category: str
    attributes: dict[str, Any]
    
    def to_prompt_context(self) -> str:
        """转换为 Prompt 上下文"""
        lines = [
            f"实体: {self.name}",
            f"类型: {self.category}",
            "属性:",
        ]
        for key, value in self.attributes.items():
            lines.append(f"  - {key}: {value}")
        return "\n".join(lines)
```

### 1.2 风险信号识别

定义领域特定的风险指标：

```python
RISK_SIGNALS = {
    "high": [
        "缺少依赖",
        "无法复现",
        "等待硬件",
        "生产环境",
        "数据丢失",
    ],
    "medium": [
        "需要确认",
        "暂时搁置",
        "性能下降",
        "兼容性问题",
    ],
    "low": [
        "文档缺失",
        "代码重复",
        "风格不一致",
    ],
}

def assess_risk(text: str) -> str:
    """评估文本中的风险级别"""
    text_lower = text.lower()
    
    for level, signals in RISK_SIGNALS.items():
        for signal in signals:
            if signal in text_lower:
                return level
    
    return "unknown"
```

### 1.3 输出适配

将 AI 输出转换为领域模型：

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class DomainAdapter(Generic[T]):
    """领域适配器"""
    
    def __init__(self, entity_class: type[T]):
        self.entity_class = entity_class
    
    def from_llm_response(self, response: dict) -> T:
        """从 LLM 响应构建领域实体"""
        # 字段映射
        mapped = self.map_fields(response)
        # 验证
        self.validate(mapped)
        # 构建
        return self.entity_class(**mapped)
    
    def map_fields(self, response: dict) -> dict:
        """字段映射（子类实现）"""
        return response
    
    def validate(self, data: dict) -> None:
        """数据验证（子类实现）"""
        pass
```

---

## 2. 领域 Prompt 模板

### 2.1 代码分析领域

```python
CODE_ANALYSIS_TEMPLATE = """
你是一位专业的代码分析师，专注于 {language} 项目。

## 分析背景
项目类型: {project_type}
技术栈: {tech_stack}
分析目标: {analysis_goal}

## 待分析代码
```{language}
{code}
```

## 分析维度
1. **结构质量**: 模块化、命名、可读性
2. **潜在问题**: Bug、边界条件、异常处理
3. **安全风险**: 输入验证、敏感数据、注入风险
4. **性能考量**: 复杂度、资源使用、可优化点

## 输出格式
```json
{{
  "summary": "一句话总结",
  "quality_score": 1-10,
  "findings": [
    {{
      "category": "结构|问题|安全|性能",
      "severity": "high|medium|low",
      "location": "行号或位置描述",
      "description": "发现描述",
      "suggestion": "改进建议"
    }}
  ],
  "highlights": ["值得肯定的点"]
}}
```
"""
```

### 2.2 文档生成领域

```python
DOC_GENERATION_TEMPLATE = """
你是一位技术文档专家，擅长编写清晰、实用的文档。

## 文档目标
类型: {doc_type}
受众: {audience}
风格: {style}

## 输入内容
{input_content}

## 文档要求
- 结构清晰，层次分明
- 语言简洁，避免冗余
- 提供具体示例
- 包含注意事项

## 输出格式
{output_format}
"""
```

### 2.3 问题诊断领域

```python
DIAGNOSIS_TEMPLATE = """
你是一位经验丰富的问题诊断专家。

## 问题描述
{problem_description}

## 相关上下文
- 环境: {environment}
- 时间: {timestamp}
- 频率: {frequency}
- 影响范围: {impact}

## 已尝试的解决方案
{attempted_solutions}

## 诊断要求
1. 分析可能的原因（按可能性排序）
2. 建议的排查步骤
3. 推荐的解决方案
4. 预防措施

## 输出格式
```json
{{
  "probable_causes": [
    {{"cause": "原因描述", "probability": "高|中|低", "evidence": "支持证据"}}
  ],
  "investigation_steps": ["步骤1", "步骤2"],
  "solutions": [
    {{"solution": "方案描述", "complexity": "简单|中等|复杂", "risk": "低|中|高"}}
  ],
  "prevention": ["预防措施"]
}}
```
"""
```

---

## 3. 领域词汇表

### 3.1 定义和使用

```python
class DomainGlossary:
    """领域词汇表"""
    
    def __init__(self):
        self.terms: dict[str, str] = {}
        self.synonyms: dict[str, str] = {}
    
    def add_term(self, term: str, definition: str, synonyms: list[str] = None):
        """添加术语"""
        self.terms[term.lower()] = definition
        if synonyms:
            for syn in synonyms:
                self.synonyms[syn.lower()] = term.lower()
    
    def normalize(self, text: str) -> str:
        """标准化术语"""
        words = text.split()
        normalized = []
        for word in words:
            lower = word.lower()
            if lower in self.synonyms:
                normalized.append(self.synonyms[lower])
            else:
                normalized.append(word)
        return " ".join(normalized)
    
    def to_prompt_context(self) -> str:
        """转换为 Prompt 上下文"""
        lines = ["## 术语定义"]
        for term, definition in self.terms.items():
            lines.append(f"- **{term}**: {definition}")
        return "\n".join(lines)

# 使用示例
glossary = DomainGlossary()
glossary.add_term(
    "PR",
    "Pull Request，代码合并请求",
    synonyms=["MR", "Merge Request"]
)
glossary.add_term(
    "CI",
    "Continuous Integration，持续集成",
    synonyms=["CI/CD", "持续集成"]
)
```

### 3.2 术语注入

```python
def inject_glossary(prompt: str, glossary: DomainGlossary) -> str:
    """将术语表注入到 Prompt"""
    glossary_context = glossary.to_prompt_context()
    return f"{glossary_context}\n\n{prompt}"
```

---

## 4. 领域验证器

### 4.1 输出验证

```python
from typing import Callable

class DomainValidator:
    """领域输出验证器"""
    
    def __init__(self):
        self.rules: list[Callable[[dict], tuple[bool, str]]] = []
    
    def add_rule(self, rule: Callable[[dict], tuple[bool, str]]):
        """添加验证规则"""
        self.rules.append(rule)
    
    def validate(self, data: dict) -> list[str]:
        """验证数据，返回错误列表"""
        errors = []
        for rule in self.rules:
            passed, message = rule(data)
            if not passed:
                errors.append(message)
        return errors

# 使用示例
validator = DomainValidator()

# 添加规则
validator.add_rule(
    lambda d: (
        "quality_score" in d and 1 <= d["quality_score"] <= 10,
        "quality_score must be between 1 and 10"
    )
)

validator.add_rule(
    lambda d: (
        isinstance(d.get("findings"), list),
        "findings must be a list"
    )
)
```

---

## 5. 领域适配检查清单

### 5.1 准备阶段

- [ ] 识别领域核心概念
- [ ] 定义领域实体模型
- [ ] 建立术语词汇表
- [ ] 识别风险信号词

### 5.2 实现阶段

- [ ] 设计领域 Prompt 模板
- [ ] 实现领域适配器
- [ ] 编写输出验证器
- [ ] 准备测试用例

### 5.3 验证阶段

- [ ] 测试典型场景
- [ ] 测试边界情况
- [ ] 验证输出一致性
- [ ] 评估准确率

---

## 6. 常见领域适配模式

### 6.1 代码分析

```
输入 → 代码解析 → 结构化表示 → LLM 分析 → 领域模型 → 输出
```

### 6.2 文档处理

```
输入文档 → 分段 → 提取关键信息 → LLM 处理 → 格式化 → 输出文档
```

### 6.3 对话系统

```
用户输入 → 意图识别 → 领域上下文注入 → LLM 生成 → 后处理 → 响应
```

---

*此文件为 AI 集成技能的一部分*
*协议版本: 2.1.0*
