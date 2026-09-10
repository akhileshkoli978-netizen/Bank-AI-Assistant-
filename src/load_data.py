from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "banking_faq.txt"
DATABASE_DIR = BASE_DIR / "database" / "chroma_db"


# 1. Read banking knowledge
with open(DATA_FILE, "r", encoding="utf-8") as file:
    banking_text = file.read()


# 2. Create a LangChain document
document = Document(
    page_content=banking_text,
    metadata={"source": "banking_faq.txt"}
)


# 3. Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

documents = text_splitter.split_documents([document])


# 4. Load a free local embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 5. Create ChromaDB
vector_store = Chroma(
    collection_name="banking_knowledge",
    embedding_function=embeddings,
    persist_directory=str(DATABASE_DIR)
)


# 6. Add documents to ChromaDB
vector_store.add_documents(documents)


print("======================================")
print("Banking knowledge loaded successfully!")
print(f"Documents/chunks added: {len(documents)}")
print(f"Database location: {DATABASE_DIR}")
print("======================================")