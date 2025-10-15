from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# creating object of ChatGroq
model = ChatGroq(model="llama-3.1-8b-instant", temperature=1.8, max_tokens=10) 

# Calling invoke function of ChatGroq
result = model.invoke("Write poem on clouds")

print(result.content)
