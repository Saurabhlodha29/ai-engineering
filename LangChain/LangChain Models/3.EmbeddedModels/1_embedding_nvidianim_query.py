from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = NVIDIAEmbeddings(
    model="nvidia/nv-embedqa-e5-v5"
    )

result = embedding.embed_query("Delhi is the capital of India")

print(result[:32])      # First 32 values
print(len(result))      # Total embedding dimensions