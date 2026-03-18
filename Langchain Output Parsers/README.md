# 📦 LangChain Output Parsers — Quick Revision Guide

## 🔍 Overview

**Output Parsers** in LangChain are used to:  
> Convert raw LLM output (text) → structured, reliable format

### Why needed?
LLMs:  
- Generate **unstructured / inconsistent text**  
- May include extra words, formatting, errors  

👉 Parsers enforce:  
- Structure  
- Validation  
- Type safety

---

## 🧠 Types of Output Parsers

### 1. 📝 String Output Parser

#### ✅ What it does
Returns plain text output (default behavior)

#### ✅ When to use
- Simple Q&A  
- No strict structure needed

#### 👍 Pros
- Fast  
- Can use `result` directly instead of `result.content` (handy for multi-step chains)

#### 👎 Cons
- No validation  
- Hard to use in pipelines

#### 💻 Example
```python
from langchain_core.output_parsers import StringOutputParser

parser = StringOutputParser()
# Assuming prompt is already defined or using PromptTemplate
# prompt = PromptTemplate.from_template("Tell me a short joke on any topic {topic}")

chain = prompt | model | parser

result = chain.invoke({'topic':'politics'})

# Can directly print result
print(result)
```
> **Note:** Unlike structured parsers, there is no need to do `result.content`. This is very handy when chaining multiple steps.

### 2. 📄 JSON Output Parser

#### ✅ What it does
Ensures output is valid JSON and optionally enforces a schema via `get_format_instructions()`.

#### ✅ When to use
- When you need structured data (API response, UI, etc.)
- When flexibility is needed (no strict type checking)

#### 👍 Pros
- Structured output
- Easy to integrate

When you need structured data (API response, UI, etc.)

#### 👎 Cons
- No full schema validation
- Can still break if JSON is malformed

#### 💻 Example
```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = f"""
Give 2 facts about India.
{parser.get_format_instructions()}
"""

result = model.invoke(prompt)
parsed = parser.parse(result.content)

print(parsed)
# Output will be a Python dict like:
# {'fact_1': '...', 'fact_2': '...'}
```
> **Note:** We use `parser.get_format_instructions()` inside the prompt to tell the LLM exactly how to structure the JSON output. This helps reduce parsing errors.

### 3. 🧾 Pydantic Output Parser (MOST IMPORTANT)

#### ✅ What it does
- Converts output → Python object
- Validates using a defined schema

#### ✅ When to use
- Production systems
- APIs / pipelines
- Interview scenarios

#### 👍 Pros
- Type-safe
- Schema validation
- Cleaner code (e.g., `result.fact_1`)

#### 👎 Cons
- Slightly complex setup
- May fail if LLM output is incorrect/malformed

#### 💻 Example
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Facts(BaseModel):
    fact_1: str = Field(description="Fact 1")
    fact_2: str = Field(description="Fact 2")

parser = PydanticOutputParser(pydantic_object=Facts)

prompt = f"""
Give 2 facts about India.
{parser.get_format_instructions()}
"""

result = model.invoke(prompt)
parsed = parser.parse(result.content)

print(parsed.fact_1)
```

---

## ⚠️ Common Issues

| Issue | Cause |
| :--- | :--- |
| **Invalid JSON** | LLM adds extra text or markdown code blocks |
| **Missing fields** | LLM ignored the schema instructions |
| **Wrong type** | LLM hallucination (e.g., returning a string instead of an int) |

## 🛠️ Error Handling (MUST)

```python
from pydantic import ValidationError

try:
    parsed = parser.parse(output)
except ValidationError as ve:
    print("❌ Validation Error:", ve)
except Exception as e:
    print("❌ Parsing Failed:", e)
```

## 🔁 OutputFixingParser (Advanced)

#### ✅ What it does
Auto-fixes bad LLM output using another LLM call to correct the format.

```python
from langchain_core.output_parsers import OutputFixingParser

fixing_parser = OutputFixingParser.from_llm(
    parser=parser,
    llm=model
)

parsed = fixing_parser.parse(output)
```

#### ⚠️ Tradeoff
- ✅ **More reliable**
- ❌ **Extra cost + latency** (requires an additional LLM call)

---

## 🚀 Best Practices

1. **Use String parser** for simple tasks and multi-step chains.
2. **Use JSON parser** for basic structure and schema hints.
3. **Use Pydantic parser** for production environments (Recommended).

**Always:**
- Add format instructions to your prompt.
- Use `try/except` blocks for robustness.
- Consider `OutputFixingParser` for critical data paths.

---

## 🧠 Final Mental Model

```mermaid
graph LR
    A[LLM] -->|Messy Text| B[Parser]
    B -->|Structured Output| C[App/Reliable Data]
```

## 🔥 Interview One-Liner
> "Output parsers convert raw LLM text into structured, validated formats like JSON or typed Python objects, enabling reliable downstream processing."
