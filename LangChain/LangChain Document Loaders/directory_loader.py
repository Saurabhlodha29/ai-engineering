from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path = "books",  # Directory to look for files
    glob = "*.pdf",  # Searches for similarity in the directory by name. The current one fetches every pdf.
    loader_cls = PyPDFLoader  # Which Class to use as primary document loader
)

# docs = loader.load()

# for doc in docs:
#     print(doc.metadata)

docs = loader.lazy_load()

for doc in docs:
    print(doc.metadata)
