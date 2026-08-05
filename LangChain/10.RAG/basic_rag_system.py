from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


from dotenv import load_dotenv

# Loading API keys
load_dotenv()


# Step-1 : INDEXING
# A. Document Ingestion

video_id = "Gfr50f6ZBvo"   # Only the ID, not full URL

try:
    # If we don't care about the language, it returns the best one
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.fetch(video_id, languages = ["en"])
    
    # Convert the list of dictionaries with timestamps to a plain text transcript
    transcript = " ".join(line.text for line in transcript_list)
    
except TranscriptsDisabled:
    print("No captions available for this video!")
    

# B. Text Splitting

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

chunks = splitter.create_documents([transcript])


# C.Embedding Generation and D. Storing in Vector Store

# Embedding Model
embedding_model = NVIDIAEmbeddings(model = "nvidia/nemotron-3-embed-1b")

vector_store = FAISS.from_documents(chunks,embedding_model)



# Step-2: RETRIEVAL

retriever = vector_store.as_retriever(search_type = "similarity", search_kwargs = {"k":4})



# Step-3: AUGMENTATION

prompt = PromptTemplate(
    template = """
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.
    
    Context : {context}
    Question : {question}
    """,
    input_variables = ["context", "question"]
)

# Creating function to format the documents

def format_docs(retrieved_docs):
    return  "\n\n".join(doc.page_content for doc in retrieved_docs)

parellel_chain = RunnableParallel(
    {
        "context" : retriever | RunnableLambda(format_docs),
        "question" : RunnablePassthrough()
    }
)


# Step-4: GENERATION

# Chat Model
model = ChatHuggingFace(llm = HuggingFaceEndpoint(repo_id = "Qwen/Qwen2.5-7B-Instruct"))

# Output Parser
parser = StrOutputParser()

final_chain = parellel_chain | prompt | model | parser

ans = final_chain.invoke("Is there a discussion about aliens in the given transcript? if yes then summarize it.")

print(ans)