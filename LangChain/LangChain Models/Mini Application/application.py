from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
load_dotenv()

input_docs = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

input_query = "Tell me about Sachin"

embedding = HuggingFaceEmbeddings(
    model = "sentence-transformers/all-MiniLM-L6-v2"
)

docs_embeddings = embedding.embed_documents(input_docs)
query_embedding = embedding.embed_query(input_query)

#Finding the cosine similarity between the query embedding and each document embedding.
similarities = cosine_similarity(
    [query_embedding],
    docs_embeddings
)[0]

#Printing the similarity scores for each document along with the document itself.
for doc, score in zip(input_docs, similarities):
    print(f"{score:.4f} -> {doc}")
    
#Finding the index of the document with the highest similarity score.
most_similar_doc_index = similarities.argmax()

#Threshold that defines the minimum similarity score to consider a document relevant.
threshold = 0.5

if similarities[most_similar_doc_index] >= threshold:
    print(input_docs[most_similar_doc_index])
else:
    print("No relevant document found.")
