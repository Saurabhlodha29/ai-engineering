from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding_model = NVIDIAEmbeddings(
    model = "nvidia/nemotron-3-embed-1b"
)

docs =[
    Document(page_content="LangChain makes it easy to work with LLMs."),
    Document(page_content="LangChain is used to build LLM based applications."),
    Document(page_content="Chroma is used to store and search document embeddings."),
    Document(page_content="Embeddings are vector representations of text."),
    Document(page_content="MMR helps you get diverse results when doing similarity search."),
    Document(page_content="LangChain supports Chroma, FAISS, Pinecone, and more."),
]

vectorstore = FAISS.from_documents(
    documents = docs,
    embedding = embedding_model
)

retriever = vectorstore.as_retriever(
    search_type = "mmr",         # <-- This enables MMR 
    search_kwargs = {"k":3, "lambda_mult":0.5}      # lambda_mult = relevance-diversity balance (0-1)
)

query = "What is Langchain?"
result = retriever.invoke(query)

print(result)