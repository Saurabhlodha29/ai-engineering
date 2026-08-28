from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

text = "My name is saurabh, I live in Noida"

vector = embedding.embed_query(text)

print(vector[:32])      # First 32 values


#We can embed multiple vectors at once using embed_documents() method like before.