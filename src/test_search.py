from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database" / "chroma_db"


# Load the same embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Connect to existing ChromaDB
vector_store = Chroma(
    collection_name="banking_knowledge",
    embedding_function=embeddings,
    persist_directory=str(DATABASE_DIR)
)


# Test question
question = "What is a savings account?"


# Search for relevant information
results = vector_store.similarity_search(
    question,
    k=3
)


print("\n========== SEARCH RESULTS ==========\n")

for i, result in enumerate(results, start=1):
    print(f"Result {i}:")
    print(result.page_content)
    print("------------------------------------")