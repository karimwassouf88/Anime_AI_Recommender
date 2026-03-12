import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- LLM ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "llama-3.1-8b-instant"

# --- Embeddings ---
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- ChromaDB ---
CHROMA_PATH = os.path.join(BASE_DIR, "db", "chroma")
COLLECTION_NAME = "anime"

# --- Memory ---
MEMORY_DB_PATH = os.path.join(BASE_DIR, "db", "memory.sqlite")

# --- RAG ---
TOP_K_RESULTS = 5