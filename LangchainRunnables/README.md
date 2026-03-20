# Langchain Runnables: An Interview Guide

## What are Langchain Runnables?

Think of Langchain components (like prompts, LLMs, and parsers) as individual Lego blocks. Each block has a specific shape and function. **Runnables** are the standardized connectors (the studs and tubes) on these Lego blocks. They provide a common interface that allows you to seamlessly connect different components, no matter their specific function.

Just as you can snap any two Lego blocks together, you can pipe any two Runnables together. The resulting chain of blocks itself becomes a new, larger Lego creation, which can then be connected to other blocks or creations. This is the core idea behind the Langchain Expression Language (LCEL) and the power of Runnables.

---

## Core Concepts

### Key Features of Runnables

1.  **Unit of Work**: Every runnable is a self-contained unit that takes an input, processes it, and produces an output.
2.  **Common Interface**: All runnables share a common set of methods (`invoke`, `batch`, `stream`, etc.), ensuring predictability and ease of use.
3.  **Composability**: Because they share the same interface, you can easily connect one runnable to another using the `|` (pipe) operator.
4.  **Chains are Runnables**: When you combine runnables, the resulting sequence is also a runnable. This means you can build complex chains and treat them as single components.

### The Runnable Interface

Runnables offer a unified way to interact with Langchain components:

-   `invoke(input)`: Executes the runnable on a single input.
-   `batch([input1, input2, ...])`: Executes the runnable on a list of inputs in parallel.
-   `stream(input)`: Streams the output of the runnable as it's being generated. This is useful for displaying real-time responses.
-   `ainvoke`, `abatch`, `astream`: Asynchronous versions of the above methods.

**🔥 Key Insight:** In modern LangChain, almost everything is a Runnable! This includes `PromptTemplate`, `LLM`, `ChatModel`, `StrOutputParser`, and even entire `Chains`. This is why you can pipe them all together so elegantly.

```python
# This works because prompt, llm, and parser are all runnables
chain = prompt | llm | parser
```

---

## Types of Runnables

Runnables can be broken down into two main categories:

### 1. Runnable Primitives (The "How")

These are the structural components that control the *flow* and *logic* of your chain. They direct the data but don't perform the core "work" themselves.

-   `RunnableSequence` (`|`): The most common primitive. It chains components sequentially, where the output of one step becomes the input for the next.
    ```python
    chain = prompt | llm | parser
    ```
-   `RunnableParallel`: Executes multiple runnables simultaneously on the *same input*, producing a dictionary of outputs.
    ```python
    from langchain_core.runnables import RunnableParallel

    parallel_chain = RunnableParallel({
        "summary": summary_chain,
        "keywords": keyword_chain
    })
    # Input -> {"summary": "...", "keywords": "..."}
    ```
-   `RunnableLambda`: Converts any Python function into a runnable. Perfect for quick data transformations or custom logic.
    ```python
    from langchain_core.runnables import RunnableLambda

    uppercase_chain = RunnableLambda(lambda x: x.upper())
    ```
-   `RunnablePassthrough`: Passes the input through unchanged. This is useful when you need to preserve the original input for a later step in the chain.
-   `RunnableBranch`: Implements conditional if-else logic, routing the execution to different runnables based on a condition.

### 2. Task-Specific Runnables (The "What")

These are the worker bees of your pipeline. They perform the actual tasks.

-   **Prompt Templates** (`PromptTemplate`, `ChatPromptTemplate`): Format input data into a prompt that an LLM can understand.
-   **LLMs / Chat Models** (`ChatOpenAI`, `ChatGroq`): The core language models that generate responses.
-   **Output Parsers** (`StrOutputParser`, `JsonOutputParser`): Transform the raw LLM output into a more usable format (e.g., string, JSON, Pydantic object).
-   **Retrievers**: Fetch relevant documents from a data source, forming the backbone of RAG (Retrieval-Augmented Generation) pipelines.
-   **Tools**: Allow the LLM to interact with the outside world by executing external actions like calling an API, querying a database, or running a custom function.

---

## Summary: Primitives vs. Task-Specific

| Type                | Role           | Description                               |
| ------------------- | -------------- | ----------------------------------------- |
| **Primitives**      | Control Flow   | Defines **how** the pipeline runs.        |
| **Task-Specific**   | Execute Tasks  | Defines **what** work is done in the pipeline. |

### Putting It All Together: Example

Here's how you can combine both types of runnables to create a chain.

```python
from langchain_core.runnables import RunnablePassthrough

# This chain takes a 'question' as input and also passes it through
# to the end, along with the 'answer'.
chain = {
    "context": retriever,
    "question": RunnablePassthrough()
} | prompt | llm | parser

```

**Breakdown:**

1.  `RunnablePassthrough()` and the dictionary structure are **Primitives** that manage the data flow.
2.  `retriever`, `prompt`, `llm`, and `parser` are **Task-Specific** runnables that each perform a distinct job.
