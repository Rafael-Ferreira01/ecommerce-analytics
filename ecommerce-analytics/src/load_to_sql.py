# src/load_to_sql.py
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import sys

def parquet_to_sqlite(parquet_path: str, sqlite_path: str, table_name: str = "orders"):
    parquet_path = Path(parquet_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet not found: {parquet_path}")
    df = pd.read_parquet(parquet_path)
    engine = create_engine(f"sqlite:///{sqlite_path}")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[OK] Saved to SQLite: {sqlite_path} (table: {table_name}, rows: {len(df)})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python src/load_to_sql.py data/orders_clean.parquet data/ecommerce.db")
        sys.exit(1)
    parquet = sys.argv[1]
    sqlite = sys.argv[2]
    parquet_to_sqlite(parquet, sqlite)
