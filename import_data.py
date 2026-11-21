import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATABASE_URL = (
    "postgresql+psycopg2://postgres@localhost:5432/business"
)

engine = create_engine(DATABASE_URL)

files = {
    "olist_customers_dataset.csv": "customers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "product_category_name_translation.csv": "category_translation"
}

try:
    with engine.connect() as connection:
        print("PostgreSQL connected successfully!")

except Exception as e:
    print("Database connection failed:", e)
    raise SystemExit

for filename, table_name in files.items():

    file_path = DATA_DIR / filename

    if not file_path.exists():
        print(f"File not found: {filename}")
        continue

    print(f"\nImporting: {filename}")

    first_chunk = True

    try:
        for chunk in pd.read_csv(file_path, chunksize=50000):

            chunk.to_sql(
                table_name,
                engine,
                if_exists="replace" if first_chunk else "append",
                index=False,
                method="multi",
                chunksize=1000
            )

            first_chunk = False

        print(f"Successfully imported: {table_name}")

    except Exception as e:
        print(f"Error importing {filename}: {e}")

print("\nOlist data import process finished!")
