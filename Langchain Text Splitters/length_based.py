from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('../LangchainDocumentLoader/Automatic Subject Generation – Technical Documentation.pdf')

docs = loader.load()

# print("docs 0")
# print(docs[0])

splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
    separator=""
)

result = splitter.split_documents(docs)

print("result 0")
print(result[0].page_content)