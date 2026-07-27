from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = NVIDIAEmbeddings(
    model = "nvidia/nv-embedqa-e5-v5"
)

documents = [
    "Delhi is the capital of India",
    "Mumbai is the financial capital of India",
    "Bangalore is the IT hub of India",
]

result = embedding.embed_documents(documents)

print(result[0][:32],"\\n")      # First 32 values of the first document embedding
print(result[1][:32],"\\n")      # First 32 values of the second document embedding
print(result[2][:32],"\\n")      # First 32 values of the third document embedding

