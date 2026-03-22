from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(file_path="cars.csv")

docs = loader.load()

print(docs[0])

print(type(docs[0]))