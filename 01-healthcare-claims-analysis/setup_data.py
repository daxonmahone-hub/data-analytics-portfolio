"""Download the Synthea synthetic patient sample and load it into a DuckDB database."""
# Run once:  pip install -r ../requirements.txt
# Then:      python setup_data.py
# Creates data/healthcare.duckdb (about 15 MB). All data is synthetic, no real patients.

import glob
import io
import os
import urllib.request
import zipfile

import duckdb

URL = "https://synthetichealth.github.io/synthea-sample-data/downloads/latest/synthea_sample_data_csv_latest.zip"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "data", "synthea_csv")
DB_PATH = os.path.join(HERE, "data", "healthcare.duckdb")


def download():
    """Fetch and unzip the Synthea CSVs if they aren't already here."""
    if glob.glob(os.path.join(RAW_DIR, "*.csv")):
        print("CSVs already downloaded, skipping.")
        return
    print("Downloading Synthea sample (~6 MB)...")
    data = urllib.request.urlopen(URL).read()
    os.makedirs(RAW_DIR, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in z.namelist():
            if name.endswith(".csv"):
                with open(os.path.join(RAW_DIR, os.path.basename(name)), "wb") as f:
                    f.write(z.read(name))


def load():
    """Create one table per CSV and print row counts."""
    con = duckdb.connect(DB_PATH)
    for path in sorted(glob.glob(os.path.join(RAW_DIR, "*.csv"))):
        table = os.path.basename(path)[:-4]
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto(?, header=true)", [path])
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<22}{n:>8,} rows")
    con.close()
    print(f"\nDone -> {DB_PATH}")


if __name__ == "__main__":
    download()
    load()
