from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

embedding = NVIDIAEmbeddings(
    model = "nvidia/nemotron-3-embed-1b"
)

doc1 = Document(
    page_content = "MS Dhoni: Calm captain who led India to three ICC trophies and finished matches with powerful hitting.",
    metadata = {"team" : "Chennai Super Kings"}
)

doc2 = Document(
    page_content = "Virat Kohli: Aggressive run-machine who holds records for many centuries and dominant chasing in all formats.",
    metadata = {"team" : "Royal Challengers Banglore"}
)   # id = '0ba0f0aa-86a0-4d8d-b69a-c7531b95bd10'

doc3 = Document(
    page_content = "Rohit Sharma: Elite opening batsman famous for scoring three double centuries in One Day Internationals and hitting massive sixes.",
    metadata = {"team" : "Mumbai Indians"}
)

doc4 = Document(
    page_content = "Yuvraj Singh: All-rounder who won the Player of the Tournament award in the 2011 World Cup and hit six sixes in one over.",
    metadata = {"team" : "Kings XI Punjab"}
)

doc5 = Document(
    page_content = "Ravindra Jadeja: World-class spin-bowling all-rounder known for his fast left-arm bowling, brilliant fielding, and clutch batting.",
    metadata = {"team" : "Rajasthan Royals"}
)

docs = [doc1, doc2, doc3, doc4, doc5]

vector_store = Chroma(
    embedding_function = embedding,
    persist_directory = "chroma_db",
    collection_name = "sample"
)

# print(vector_store.add_documents(docs))

# print(vector_store.get(include = ["embeddings","documents","metadatas"]))

# bowler = vector_store.similarity_search(
#     query = "Who among these are bowlers?",
#     k = 2
# )

# bowler = vector_store.similarity_search_with_score(
#     query = "Who among these are bowlers?",
#     k = 2
# )

# csk = vector_store.similarity_search_with_score(
#     query = "Move as per the Filter",
#     filter = {"team" : "Chennai Super Kings"},
#     k = 1
# )

# print(csk)

updated_document = Document(
    page_content = "Virat Kohli is a master of modern cricket whose smooth strokeplay and steady run-scoring have rewritten the record books.",
    metadata = {"team" : "Royal Challengers Banglore"}
)

vector_store.update_document(document_id = "0ba0f0aa-86a0-4d8d-b69a-c7531b95bd10", document = updated_document)

vector_store.delete(ids = ["0ba0f0aa-86a0-4d8d-b69a-c7531b95bd10"])