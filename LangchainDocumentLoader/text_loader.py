from langchain_community.document_loaders import TextLoader

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt = PromptTemplate(
    template ="write summary for following poem \n {poem}",
    input_variables = ['poem']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

#Text loader object
loader = TextLoader('poem.txt', encoding='utf-8')

"""
# object is stored as document object in list
# [Document(page_content = "text",
            meta_date = {}
            )]
"""
docs = loader.load()

print(docs)

print(type(docs)) # <class 'list'>

print(len(docs))

# access first document in list
print(docs[0])

print(type(docs[0])) # <class 'langchain_core.documents.base.Document'>

# get page_content from first document
print(docs[0].page_content)

chain = prompt | model | parser

result = chain.invoke({'poem':docs[0].page_content})

print(result)