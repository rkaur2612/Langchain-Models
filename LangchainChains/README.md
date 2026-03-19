# Langchain Chains

This document provides an overview of different types of chains available in Langchain and how to use them. 

## Simple Chain

A simple chain is the most basic type of chain where you pipe together a prompt, a model, and an output parser.

**Use Case:** Generate 5 interesting facts about a given topic.

### Code

```python
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

prompt = PromptTemplate(
    template="Generate 5 interesting facts about {topic}",
    input_variables=['topic']
)

model = ChatGroq(model="llama-3.1-8b-instant")
parser = StrOutputParser()

chain = prompt | model | parser

# The input is sent to the prompt, then to the model, and the model's output is sent to the parser.
result = chain.invoke({'topic': 'cricket'})
print(result)
```

### Flow

```
+---------------+
|  PromptInput  |
+---------------+
        |
        v
+----------------+
| PromptTemplate |
+----------------+
        |
        v
+----------+
| ChatGroq |
+----------+
        |
        v
+-----------------+
| StrOutputParser |
+-----------------+
        |
        v
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
```

---

## Sequential Chain

A sequential chain allows you to run multiple chains in sequence, where the output of one chain is the input to the next.

**Use Case:** A user sends a topic to a model to create a detailed report. Then, the detailed report is sent to the model again to generate a 5-line summary.

### Code

```python
# Assuming prompt1, model, parser, prompt2 are defined
chain = prompt1 | model | parser | prompt2 | model | parser
```

### Flow

```
+---------------+
|  PromptInput  |
+---------------+
        |
        v
+----------------+
| PromptTemplate |
+----------------+
        |
        v
+----------+
| ChatGroq |
+----------+
        |
        v
+-----------------+
| StrOutputParser |
+-----------------+
        |
        v
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
        |
        v
+----------------+
| PromptTemplate |
+----------------+
        |
        v
+----------+
| ChatGroq |
+----------+
        |
        v
+-----------------+
| StrOutputParser |
+-----------------+
        |
        v
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
```

---

## Parallel Chain

A parallel chain allows you to execute multiple chains in parallel and combine their results.

**Use Case:** A user sends a document/text to a model and asks it to create notes and a quiz from it.

### Code

```python
from langchain_core.runnables import RunnableParallel

# RunnableParallel class is used to create a parallel chain.

# Pass notes to prompt1 -> model -> parser
# Pass quiz to prompt2 -> model -> parser
# This chain will return {notes} and {quiz} which is then passed to a merge chain as input.

parallel_chain = RunnableParallel({
    'notes': prompt1 | model | parser,
    'quiz' : prompt2 | model | parser
})

merge_chain = prompt3 | model | parser

chain = parallel_chain | merge_chain

result = chain.invoke({'text': text})
```

### Flow

```
+---------------------------+
| Parallel<notes,quiz>Input |
+---------------------------+
       /               \
      /                 \
     v                   v
+----------------+   +----------------+
| PromptTemplate |   | PromptTemplate |
+----------------+   +----------------+
     |                   |
     v                   v
+----------+         +----------+
| ChatGroq |         | ChatGroq |
+----------+         +----------+
     |                   |
     v                   v
+-----------------+   +-----------------+
| StrOutputParser |   | StrOutputParser |
+-----------------+   +-----------------+
      \                 /
       \               /
        v             v
+----------------------------+
| Parallel<notes,quiz>Output |
+----------------------------+
              |
              v
+----------------+
| PromptTemplate |
+----------------+
              |
              v
+----------+
| ChatGroq |
+----------+
              |
              v
+-----------------+
| StrOutputParser |
+-----------------+
              |
              v
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
```

---

## Conditional Chain

A conditional chain allows you to execute different branches of a chain based on a condition. `RunnableBranch` is used for this purpose.

**Use Case:** A user sends feedback. The model classifies it as positive or negative. Then, the sentiment is sent to another model to reply with an appropriate response.

### Code

```python
from langchain_core.runnables import RunnableBranch

# if condition1 = true -> run chain1
# else if condition2 = true -> run chain2
# else default_chain

branch_chain = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default_chain
)
```

### Flow

```
+-------------+
| PromptInput |
+-------------+
      |
      v
+----------------+
| PromptTemplate |
+----------------+
      |
      v
+----------+
| ChatGroq |
+----------+
      |
      v
+----------------------+
| PydanticOutputParser |
+----------------------+
      |
      v
+--------+
| Branch |
+--------+
      |
      v
(Executes one of the provided chains based on the condition)
```