# src/etl.py
import pandas as pd
from pathlib import Path
import sys

def clean_orders(infile: str, outfile: str):
    infile = Path(infile)
    outfile = Path(outfile)
    if not infile.exists():
        raise FileNotFoundError(f"Input file not found: {infile}")
    df = pd.read_csv(infile, parse_dates=['order_date'], low_memory=False)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Common renames
    rename_map = {
        'orderid':'order_id','order id':'order_id','orderid':'order_id',
        'orderdate':'order_date','order date':'order_date'
    }
    df.rename(columns={k:v for k,v in rename_map.items() if k in df.columns}, inplace=True)

    # Convert order_date safely
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    # Filter completed orders if column exists
    if 'order_status' in df.columns:
        df['order_status'] = df['order_status'].astype(str).str.lower().str.strip()
        valid_status = ['completed','complete','entregue','finalizado','concluido','shipped']
        df = df[df['order_status'].isin(valid_status) | df['order_status'].isna()==False]

    # Drop duplicates
    df = df.drop_duplicates()

    # Numeric conversions & fillna
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(1).astype(int)
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)

    # Remove negative prices
    if 'price' in df.columns:
        df = df[df['price'] >= 0]

    # Revenue column
    df['revenue'] = df['price'] * df['quantity']

    # Text cleanup
    for col in ['category','product_name','country']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Derived columns
    if 'order_date' in df.columns:
        df['year_month'] = df['order_date'].dt.to_period('M').dt.to_timestamp()
        df['order_day'] = df['order_date'].dt.date
        df['dayofweek'] = df['order_date'].dt.day_name()

    outfile.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(outfile, index=False)
    print(f"[OK] Cleaned data saved to: {outfile} (rows: {len(df)})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python src/etl.py data/raw/orders.csv data/orders_clean.parquet")
        sys.exit(1)
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    clean_orders(in_path, out_path)
