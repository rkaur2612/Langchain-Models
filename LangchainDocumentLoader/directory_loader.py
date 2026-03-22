from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader

loader = DirectoryLoader(
    path='../LangchainDocumentLoader',
    glob='*.pdf', # extract all pdf from given path # in or case there are two pdfs
    loader_cls=PyPDFLoader
)

docs = loader.load()

# docs = loader.lazy_load()

# how many documents loaded?
# 8 pages in one pdf (automatic sub gen) + 1 page in 2nd pdf (resume pdf)
print(len(docs))

# inspecting 8 document content (indexing start with 0)
print(docs[7].page_content)
print(docs[7].metadata)

for document in docs:
    print(document.metadata)