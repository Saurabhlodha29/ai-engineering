from langchain_text_splitters import CharacterTextSplitter 
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Interview_notes.pdf")

docs = loader.lazy_load()

# text = """Space exploration has led to incredible scientific discoveries. From landing on the Moon to
# exploring Mars, humanity continues to push the boundaries of what's possible beyond our planet.

# These missions have not only expanded our knowledge of the universe but have also contributed to
# advancements in technology here on Earth. Satellite communications, GPS, and even certain medical
# imaging techniques trace their roots back to innovations driven by space programs."""

splitter = CharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 0,
    separator = ''
)

result = splitter.split_documents(docs)
print(result)