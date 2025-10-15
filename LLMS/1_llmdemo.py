from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()

# creating object of ChatGroq
llm = ChatGroq(model="llama-3.1-8b-instant") 

# calling invoke function of ChatGroq
response = llm.invoke([HumanMessage(content="Explain LangChain in simple terms")])

print(response.content)



