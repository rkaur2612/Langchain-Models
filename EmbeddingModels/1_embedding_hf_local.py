from langchain_huggingface import HuggingFaceEmbeddings

#object of class HuggingFaceEmbeddings
embedding = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

#text = "Sky is blue"

document = [
    "Delhi is Capital of India",
    "Kolkata is Capital of West Bengal",
    "Paris is Capital of France"
]

#vector = embedding.embed_query(text) # This is for single query
vector = embedding.embed_documents(document)

print(str(vector))