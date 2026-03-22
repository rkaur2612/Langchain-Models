from langchain_community.document_loaders import WebBaseLoader

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt = PromptTemplate(
    template ="Answer the following question \n {question} from the following text \n {text}",
    input_variables = ['question', 'text']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()


loader = WebBaseLoader(
    "https://www.amazon.com/Judge-Stone-Novel-James-Patterson/dp/0316579831/ref=books_amz-books_desktop_mfs_bookzg_4?_encoding=UTF8&pd_rd_w=CGiNO&content-id=amzn1.sym.74bdf9d7-9f96-43e4-946d-433829cf865a&pf_rd_p=74bdf9d7-9f96-43e4-946d-433829cf865a&pf_rd_r=0SP1M0VKMQCY18ZG1ADS&pd_rd_wg=GXz71&pd_rd_r=9272431a-6c13-4dd0-ad9a-243daf281daa"
)

docs = loader.load()

# how many documents loaded?
# print(len(docs))

# print(docs[0].page_content)

chain = prompt | model | parser
result = chain.invoke({'question':'Which product is metioned and what is its price', 'text':docs[0].page_content})

print(result)