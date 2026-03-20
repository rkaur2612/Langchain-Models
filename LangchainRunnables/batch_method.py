"""
What it does
Runs the same runnable on multiple inputs at once

Think:
Process many requests together instead of one-by-one

Optimized for:
Bulk processing
Cost & performance efficiency

Real-world use case:
Processing multiple documents
Generating summaries for many inputs
Bulk API calls

batch() → Order 10 coffees together ☕☕☕

batch() sends all inputs together and executes them concurrently (not strictly sequential), depending on system capability.
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

# 🔥 BATCH INPUTS
inputs = [
    {'topic': 'AI'},
    {'topic': 'cricket'}
]

results = chain.batch(inputs)

for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(res)