from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

splitter = RecursiveCharacterTextSplitter.from_language(
    language = Language.MARKDOWN,
    chunk_size = 150,
    chunk_overlap = 0
)

code = """
# Smart Campus Food Ordering System

A multi-campus food ordering and outlet management platform designed to reduce wait times, manage peak-hour load, and optimize campus food operations.

## Status
🚧 Under active development (Phase 1: Core System)

## Vision
Single-campus deployment initially, architected for multi-campus scalability.
"""

chunks = splitter.split_text(code)
print(len(chunks))
print(chunks[1])