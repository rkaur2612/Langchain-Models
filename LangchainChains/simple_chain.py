from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate(
    template ="Generate 5 interesting facts about {topic}",
    input_variables =['topic']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

chain = prompt | model | parser

# this i/p sent to prompt in chain - send prompt to model - model o/p result send to parser - parser return ouptut
result = chain.invoke({'topic':'cricket'})

print(result)

# visualise chain
chain.get_graph().print_ascii()