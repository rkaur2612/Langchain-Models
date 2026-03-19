"""
# USE CASE

user -> topic -> LLM -> generated detailed report -> LLM -> extract summary -> o/p

"""

from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt1 = PromptTemplate(
    template ="Generate a detailed report on {topic}",
    input_variables = ['topic']
)

prompt2 = PromptTemplate(
    template ="Generate a 5 pointer summary from the following text \n {text}",
    input_variables = ['text']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

# this i/p sent to prompt in chain - send prompt to model - model o/p result send to parser - parser return ouptut
result = chain.invoke({'topic':'cricket'})

print(result)

# visualise chain
chain.get_graph().print_ascii()