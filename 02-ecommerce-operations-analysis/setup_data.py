"""Download the Olist Brazilian e-commerce dataset and load it into a DuckDB database."""
# Run once:  pip install -r ../requirements.txt
# Then:      python setup_data.py
# Creates data/ecommerce.duckdb. Source: Olist public dataset (~100K real, anonymized orders, 2016-2018).

import os
import urllib.request

import duckdb

BASE = "https://huggingface.co/datasets/aviahYadler/Olist_Ecommerce_Dataset/resolve/main/"
FILES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "data", "olist_csv")
DB_PATH = os.path.join(HERE, "data", "ecommerce.duckdb")


def download():
    """Fetch each CSV if it isn't already here."""
    os.makedirs(RAW_DIR, exist_ok=True)
    for fname in FILES.values():
        path = os.path.join(RAW_DIR, fname)
        if not os.path.exists(path):
            print(f"Downloading {fname}...")
            urllib.request.urlretrieve(BASE + fname, path)


def load():
    """Create one table per CSV and print row counts."""
    con = duckdb.connect(DB_PATH)
    for table, fname in FILES.items():
        path = os.path.join(RAW_DIR, fname)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto(?, header=true)", [path])
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<22}{n:>9,} rows")
    con.close()
    print(f"\nDone -> {DB_PATH}")


if __name__ == "__main__":
    download()
    load()
