# 雅 Miyabi

> An AI that finds your next anime — based on how you feel, not just what you search.

[**Try it →**](your-deployed-link-here)

---

Miyabi is a conversational anime recommender. You describe a mood, a vibe, an anime you loved — and it finds what you should watch next.

It remembers your conversation, understands context, and recommends based on atmosphere and feeling — not just genre tags.

---

## Built with

|            |                             |
| ---------- | --------------------------- |
| Frontend   | Next.js + TypeScript        |
| Backend    | FastAPI                     |
| LLM        | Groq — Llama 3.1 8B         |
| Embeddings | HuggingFace (local, no API) |
| Vector DB  | ChromaDB                    |
| Memory     | LangChain + SQLite          |
| Data       | MyAnimeList — 23,000+ anime |

---

## How it works

Every message goes through a full RAG pipeline:

```
your message
    → semantic search across 23k anime (ChromaDB)
    → retrieved context + conversation history
    → LLM generates a recommendation grounded in real data
    → your exchange is saved for next time
```

The embedding model runs locally. Memory persists across sessions. No anime is invented — every recommendation comes from the actual database.

---

## Run it locally

```bash
# Backend
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt

# Add your Groq API key to .env
GROQ_API_KEY=your_key_here

# Build the vector database (first time only)
python backend/data/ingest.py

# Start the backend
cd backend && uvicorn main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

---

## What I learned building this

This was my first end-to-end AI engineering project. I touched every layer — data cleaning, vector embeddings, RAG pipeline design, prompt engineering, persistent memory, REST API, and a production UI.

The most interesting discovery: the quality of a recommendation system has less to do with the model and more to do with how well you retrieve context and instruct the model to use it.

---

_Miyabi (雅) — elegance, refinement, grace._
