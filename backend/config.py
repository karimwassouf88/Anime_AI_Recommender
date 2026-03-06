import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama3-8b-8192"

# --- Embeddings ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- ChromaDB ---
CHROMA_PATH = "db/chroma"
COLLECTION_NAME = "anime"

# --- Memory ---
MEMORY_DB_PATH = "db/memory.sqlite"

# --- RAG ---
TOP_K_RESULTS = 5