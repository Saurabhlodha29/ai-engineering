from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(
    top_k_results = 2,
    lang = "en"
)

query = "The geopolitical history of India and Pakistan from the perspective of Chinese."

docs = retriever.invoke(query)

for i,doc in enumerate(docs):
    print(f"\n --- {i+1} ---")
    print(f"Content:\n{doc.page_content}...")