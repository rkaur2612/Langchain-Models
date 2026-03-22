from langchain_community.document_loaders import PyPDFLoader

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

# prompt = PromptTemplate(
#     template ="write summary for following poem \n {poem}",
#     input_variables = ['poem']
# )

# model = ChatGroq(model="llama-3.1-8b-instant")

# parser = StrOutputParser()

#Text loader object
loader = PyPDFLoader('Automatic Subject Generation – Technical Documentation.pdf')

docs = loader.load()

print(type(docs)) # <class 'list'>

print(len(docs))

# access first document in list, will contains first page doc objectd
print(docs[0].page_content)

print(docs[0].metadata)