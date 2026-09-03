# pip install -U langchain langchain-community faiss-cpu pypdf python-dotenv langchain-huggingface transformers

import os
from dotenv import load_dotenv

from langsmith import traceable  # <-- Key import

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

os.environ['LANGCHAIN_PROJECT'] = 'RAG Chatbot V2'

PDF_PATH = "islr.pdf"

# Traced Setup steps

@traceable(name = 'load_pdf')
def load_pdf(path : str):
    loader = PyPDFLoader(path)
    return loader.load()  # list(Documents)

@traceable(name = 'split_documents')
def split_documents(docs, chunk_size = 1000, chunk_overlap = 150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, chunk_overlap = chunk_overlap
    )
    return splitter.split_documents(docs)

@traceable(name = 'build_vectorstore')
def build_vectorstore(splits):
    emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    # FAISS.from_documents internally calls embedding model
    vs = FAISS.from_documents(splits, emb)
    return vs

@traceable(name = 'setup_pipeline')
def setup_pipeline(pdf_path : str):
    docs = load_pdf(pdf_path)
    splits = split_documents(docs)
    vs = build_vectorstore(splits)
    
    return vs


# --------------------- Pipeline ----------------------

# Embedding model
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

def format_docs(docs): 
    return "\n\n".join(d.page_content for d in docs)


# Build the index under traced setup

vectorstore = setup_pipeline(PDF_PATH)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

parallel = RunnableParallel({
    "context": retriever | RunnableLambda(format_docs),
    "question": RunnablePassthrough()
})

chain = parallel | prompt | llm | StrOutputParser()

# Run a query, also traced
print("\nPDF RAG ready. Ask a question (or Ctrl+C to exit).")
q = input("\nQ: ").strip()

# Give a visible metadata, tags so easy to locate
config = {
    'run_name' : 'pdf_rag_query'
}

ans = chain.invoke(q, config)
print("\nA:", ans)