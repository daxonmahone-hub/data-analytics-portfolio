"""Download the Steam games dataset and load a cleaned table into DuckDB."""
# Run once:  pip install -r ../requirements.txt
# Then:      python setup_data.py
# Downloads ~190 MB, keeps a slim table in data/steam.duckdb. Source: FronkonGames Steam Games Dataset (MIT).

import os
import urllib.request

import duckdb

URL = "https://huggingface.co/datasets/FronkonGames/steam-games-dataset/resolve/main/data/train-00000-of-00001.parquet"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "steam_raw.parquet")
DB_PATH = os.path.join(HERE, "data", "steam.duckdb")


def download():
    """Fetch the raw parquet file if it isn't already here."""
    os.makedirs(os.path.dirname(RAW), exist_ok=True)
    if not os.path.exists(RAW):
        print("Downloading Steam dataset (~190 MB, takes a minute)...")
        urllib.request.urlretrieve(URL, RAW)


def load():
    """Keep the analysis columns, parse dates and owner ranges, and build a genre lookup table."""
    con = duckdb.connect(DB_PATH)
    con.execute("""
        CREATE OR REPLACE TABLE games AS
        SELECT appID                                            AS app_id,
               name,
               CAST(strptime(release_date, '%b %d, %Y') AS DATE) AS release_date,
               price,
               CAST(split_part(estimated_owners, ' - ', 1) AS BIGINT) AS owners_low,
               CAST(split_part(estimated_owners, ' - ', 2) AS BIGINT) AS owners_high,
               peak_ccu,
               positive,
               negative,
               metacritic_score,
               achievements,
               dlc_count,
               average_playtime_forever,
               median_playtime_forever,
               windows, mac, linux,
               developers,
               publishers,
               genres
        FROM read_parquet(?)
    """, [RAW])
    con.execute("""
        CREATE OR REPLACE TABLE game_genres AS
        SELECT app_id, UNNEST(genres) AS genre FROM games
    """)
    for t in ["games", "game_genres"]:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t:<14}{n:>9,} rows")
    con.close()
    print(f"\nDone -> {DB_PATH}")


if __name__ == "__main__":
    download()
    load()
