import pandas as pd
import os
import sys
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CHROMA_PATH, EMBEDDING_MODEL, COLLECTION_NAME


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    cols = [
        "mal_id", "title", "title_english", "synopsis", "genres",
        "themes", "demographics", "score", "rank", "popularity",
        "episodes", "type", "status", "studios", "source", "rating"
    ]

    df = df[cols]
    df = df.dropna(subset=["synopsis"])
    df["title_english"] = df["title_english"].fillna(df["title"])
    df = df.fillna("Unknown")
    df = df.replace("unknown", "Unknown")
    df = df.reset_index(drop=True)

    return df


def save_clean(df: pd.DataFrame, output_path: str) -> None:
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")


def build_documents(df: pd.DataFrame) -> list[dict]:
    documents = []

    for index, row in df.iterrows():
        text = f"""Title: {row['title_english']}
Type: {row['type']} | Episodes: {int(float(row['episodes'])) if row['episodes'] != 'Unknown' else 'Unknown'} | Status: {row['status']}
Score: {row['score']} | Rank: {int(float(row['rank'])) if row['rank'] != 'Unknown' else 'Unknown'} | Popularity: {row['popularity']}
Rating: {row['rating']}
Genres: {row['genres']}
Themes: {row['themes']}
Demographics: {row['demographics']}
Studios: {row['studios']} | Source: {row['source']}
Synopsis: {row['synopsis']}"""

        try:
            score = float(row['score'])
        except:
            score = 0.0

        try:
            popularity = int(float(row['popularity']))
        except:
            popularity = 99999

        documents.append({
            "id": str(index),
            "text": text,
            "metadata": {
                "score": score,
                "popularity": popularity,
                "genres": str(row['genres']),
                "rating": str(row['rating'])
            }
        })

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    chunked = []

    for doc in documents:
        text = doc['text']

        if len(text) > 1500:
            lines = text.split('\n')
            trimmed = []
            total = 0
            for line in lines:
                if total + len(line) > 1500:
                    break
                trimmed.append(line)
                total += len(line)
            text = '\n'.join(trimmed)

        chunked.append({
            "id": doc['id'],
            "text": text,
            "metadata": doc['metadata']
        })

    return chunked


def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def store_in_chroma(chunks: list[dict], embeddings) -> None:
    texts = [chunk['text'] for chunk in chunks]
    ids = [chunk['id'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]

    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )

    print("Storing chunks in ChromaDB...")
    batch_size = 500

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        batch_metadatas = metadatas[i:i + batch_size]
        db.add_texts(texts=batch_texts, ids=batch_ids, metadatas=batch_metadatas)
        print(f"Stored {min(i + batch_size, len(texts))}/{len(texts)}")

    print("Done. ChromaDB is ready.")


if __name__ == "__main__":
    df = pd.read_csv("backend/data/processed/anime_clean.csv")

    docs = build_documents(df)
    chunks = chunk_documents(docs)
    print(f"Total chunks ready: {len(chunks)}")

    embeddings = get_embeddings()
    store_in_chroma(chunks, embeddings)