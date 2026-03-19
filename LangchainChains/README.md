### Simple Chain

prompt = PromptTemplate(
    template ="Generate 5 interesting facts about {topic}",
    input_variables =['topic']
)

model = ChatGroq(model="llama-3.1-8b-instant")
parser = StrOutputParser()

chain = prompt | model | parser

# this i/p sent to prompt in chain - send prompt to model - model o/p result send to parser - parser return ouptut
result = chain.invoke({'topic':'cricket'})

    +-------------+       
     | PromptInput |
     +-------------+
            *
            *
            *
    +----------------+
    | PromptTemplate |
    +----------------+
            *
            *
            *
      +----------+
      | ChatGroq |
      +----------+
            *
            *
            *
   +-----------------+
   | StrOutputParser |
   +-----------------+
            *
            *
            *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+

### Sequential Chain
# USE CASE - User send topic to model and ask to create detailed report. Then the detailed report again sent to model to generate 5 lines summary

chain = prompt1 | model | parser | prompt2 | model | parser

  +-------------+       
     | PromptInput |
     +-------------+
            *
            *
            *
    +----------------+
    | PromptTemplate |
    +----------------+
            *
            *
            *
      +----------+
      | ChatGroq |
      +----------+
            *
            *
            *
   +-----------------+
   | StrOutputParser |
   +-----------------+
            *
            *
            *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+
            *
            *
            *
    +----------------+
    | PromptTemplate |
    +----------------+
            *
            *
            *
      +----------+
      | ChatGroq |
      +----------+
            *
            *
            *
   +-----------------+
   | StrOutputParser |
   +-----------------+
            *
            *
            *
+-----------------------+
| StrOutputParserOutput |
+-----------------------+

### Parallel Chain

# Use Case - user send document/text to model and asks it to create notes and quiz from it

# RunnableParallel class used to created parallel chain

#pass notes to prompt1 -> model -> parser
#pass quiz to prompt2 -> model -> parser
#this chain will return {notes} and {quiz} which is then passed to merge chain as input

parallel_chain = RunnableParallel({
    'notes': prompt1 | model | parser,
    'quiz' : prompt2 | model | parser
})

merge_chain = prompt3 | model | parser

chain = parallel_chain | merge_chain

result = chain.invoke({'text': text})

+---------------------------+
          | Parallel<notes,quiz>Input |
          +---------------------------+
                ***             ***
              **                   **
            **                       **
+----------------+              +----------------+
| PromptTemplate |              | PromptTemplate |
+----------------+              +----------------+
          *                             *
          *                             *
          *                             *
    +----------+                  +----------+
    | ChatGroq |                  | ChatGroq |
    +----------+                  +----------+
          *                             *
          *                             *
          *                             *
+-----------------+            +-----------------+
| StrOutputParser |            | StrOutputParser |
+-----------------+            +-----------------+
                ***             ***
                   **         **
                     **     **
          +----------------------------+
          | Parallel<notes,quiz>Output |
          +----------------------------+
                         *
                         *
                         *
                +----------------+
                | PromptTemplate |
                +----------------+
                         *
                         *
                         *
                   +----------+
                   | ChatGroq |
                   +----------+
                         *
                         *
                         *
                +-----------------+
                         *
                         *
                         *
                +-----------------+
                | StrOutputParser |
                +-----------------+
                         *
                         *
                         *
            +-----------------------+
            | StrOutputParserOutput |
            +-----------------------+

### Conditional Chain

# Use Case - User send feedback -> model classfies as positive/negative -> then sentiment sent to another model to reply back with approapriate response 

Runnable branch used to execute conditional branches

# if condition1 = true -> run chain1 
# else if condition2 = true -> run chain2
# else default chain
branch_chain = RunnableBranch(
    (condition1, chain1),
    (condition2, chain2),
    default chain
)

 +-------------+      
    | PromptInput |
    +-------------+
            *
            *
            *
   +----------------+
   | PromptTemplate |
   +----------------+
            *
            *
            *
      +----------+
      | ChatGroq |
      +----------+
            *
            *
            *
+----------------------+
| PydanticOutputParser |
+----------------------+
            *
            *
            *
       +--------+
       | Branch |
       +--------+
| PydanticOutputParser |
+----------------------+