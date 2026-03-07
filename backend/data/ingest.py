import pandas as pd

def load_and_clean(path:str)->pd.DataFrame:
    df=pd.read_csv(path)
    
    cols = [
        "mal_id", "title", "title_english", "synopsis", "genres",
        "themes", "demographics", "score", "rank", "popularity",
        "episodes", "type", "status", "studios", "source", "rating"
    ]

    df=df[cols]

    # Drop any data that does not have synopsis
    df=df.dropna(subset=["synopsis"])

    df["title_english"] = df["title_english"].fillna(df["title"])

    df=df.fillna("Unknown")

    df=df.reset_index(drop=True)

    return df

def save_clean(df: pd.DataFrame, output_path: str) -> None:
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")

if __name__ == "__main__":
    df = load_and_clean("backend/data/raw/anime.csv")

    print("Clean shape:", df.shape)
    print("\nMissing values after cleaning:")
    print(df.isnull().sum())

    save_clean(df, "backend/data/processed/anime_clean.csv")