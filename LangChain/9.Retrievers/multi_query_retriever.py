from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

embedding_model = NVIDIAEmbeddings(model  = "nvidia/nemotron-3-embed-1b")

chat_model = ChatHuggingFace(llm = HuggingFaceEndpoint(repo_id = "Qwen/Qwen2.5-7B-Instruct"))

all_docs = [
    Document(page_content="Regular walking boosts heart health and can reduce symptoms of depression.", metadata={"source": "H1"}),
    Document(page_content="Consuming leafy greens and fruits helps detox the body and improve longevity.", metadata={"source": "H2"}),
    Document(page_content="Deep sleep is crucial for cellular repair and emotional regulation.", metadata={"source": "H3"}),
    Document(page_content="Mindfulness and controlled breathing lower cortisol and improve mental clarity.", metadata={"source": "H4"}),
    Document(page_content="Drinking sufficient water throughout the day helps maintain metabolism and energy.", metadata={"source": "H5"}),
    Document(page_content="The solar energy system in modern homes helps balance electricity demand.", metadata={"source": "I1"}),
    Document(page_content="Python balances readability with power, making it a popular system design language.", metadata={"source": "I2"}),
    Document(page_content="Photosynthesis enables plants to produce energy by converting sunlight.", metadata={"source": "I3"}),
    Document(page_content="The 2022 FIFA World Cup was held in Qatar and drew global energy and excitement.", metadata={"source": "I4"}),
    Document(page_content="Black holes bend spacetime and store immense gravitational energy.", metadata={"source": "I5"})
]

vectorstore = FAISS.from_documents(
    documents = all_docs,
    embedding = embedding_model
)

# Create retrievers

similarity_retriever = vectorstore.as_retriever(
    search_type = "similarity",
    search_kwargs = {"k":5}
)

multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever = vectorstore.as_retriever(search_kwargs = {"k":5}),
    llm = chat_model
)

# Creating query
query = "How to improve energy levels and maintain balance?"

similarity_results = similarity_retriever.invoke(query)
multiquery_results = multiquery_retriever.invoke(query)

# Printing results

for i, doc in enumerate(similarity_results):
    print(f"\n -- {i+1} --")
    print(f"\n -- {doc.page_content} --")
    
print("-"*100)

for i, doc in enumerate(multiquery_results):
    print(f"\n -- {i+1} --")
    print(f"\n -- {doc.page_content} --")
    