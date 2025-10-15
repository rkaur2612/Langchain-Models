from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Note: HuggingFaceEmbeddings does not accept a `dimension` kwarg.
# Remove the `dimension` argument — the model determines the embedding size.
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

document = [
    "Virat Kohli is known for his aggressive batting style and consistent performances across all formats.",
    "Rohit Sharma holds the record for the highest individual score in a One Day International match.",
    "Jasprit Bumrah is one of the most effective fast bowlers in the world with a unique bowling action.",
    "Ravindra Jadeja contributes to the team as an all-rounder with his sharp fielding, reliable batting, and spin bowling.",
    "KL Rahul is admired for his elegant stroke play and versatility as both an opener and a middle-order batsman."
]

#user query
query = "Tell me about Virat Kohli"

# we need to return the document similar with the user query
doc_embedding = embedding.embed_documents(document)
query_embedding = embedding.embed_query(query)

# Convert to numpy arrays and print shapes for verification
# doc_embedding = np.array(doc_embedding)
# query_embedding = np.array(query_embedding)
# print("doc_embedding shape:", doc_embedding.shape)
# print("query_embedding shape:", query_embedding.shape)
print("Cosine similarities:")

scores = cosine_similarity([query_embedding], doc_embedding)[0]
print(scores)

# added enumerate function to add an index to each score
# sorted scores in ascending order and fecth last element which is the document with highest score i.e. most similar
highest_score = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]
print(highest_score)

# capture the highest matched score index and score separately
index, score = sorted(list(enumerate(scores)),key=lambda x:x[1])[-1]

print(f"\n {query}")
#printing the most matched document
print(document[index])
print(f"\n similarity score is:", score)






