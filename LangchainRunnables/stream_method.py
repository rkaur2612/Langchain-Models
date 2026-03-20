"""
What it does
Instead of waiting for the full output, it returns the result chunk by chunk (in real-time).

Think:
Like ChatGPT typing response live instead of showing everything at once

stream() → Watch coffee being made ☕👀

"""
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt1= PromptTemplate(
    template ="write a joke about {topic}",
    input_variables = ['topic']
)

# prompt2 = PromptTemplate(
#     template ="explain following joke \n {joke}",
#     input_variables = ['joke']
# )


model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

chain = RunnableSequence(prompt1, model, parser)

# result = chain.invoke({'topic':'AI'})
# print(result)

for chunk in chain.stream({'topic': 'cricket'}):
    print(chunk, end="", flush=True)