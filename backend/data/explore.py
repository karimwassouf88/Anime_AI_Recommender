import pandas as pd

df= pd.read_csv("backend/data/raw/anime.csv")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print("shape",df.shape)

cols = [
    "mal_id", "title", "title_english", "synopsis", "genres",
    "themes", "demographics", "score", "rank", "popularity",
    "episodes", "type", "status", "season", "year",
    "studios", "source", "rating"
]

df_clean = df[cols]

print(df_clean.head(1))

print("\nmissing values")
print(df_clean.isnull().sum())