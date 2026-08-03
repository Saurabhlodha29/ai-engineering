from langchain_community.vectorstores import Chroma
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

embedding = NVIDIAEmbeddings(
    model = "nvidia/nemotron-3-embed-1b"
)

documents = [
    Document (page_content="LangChain helps developers build LLM applications easily."),
    Document(page_content="Chroma is a vector database optimized for LLM-based search."),
    Document(page_content="Embeddings convert text into high-dimensional vectors."),
    Document(page_content="OpenAI provides powerful embedding models."),
]

vector_store = Chroma.from_documents(
    documents = documents,
    embedding = embedding,
    collection_name = "my_collection"
)

retriever = vector_store.as_retriever(search_kwargs = {"k":2})

query = "What is Chroma used for?"

results = retriever.invoke(query)

for i, doc in enumerate(results):
    print(f"\n--{i+1}--")
    print(f"\n--{doc}--")