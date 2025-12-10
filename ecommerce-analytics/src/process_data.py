import pandas as pd
import os

RAW_DATA_PATH = "data/raw/vendas.csv"
PROCESSED_DATA_PATH = "data/processed/vendas_processado.csv"

def load_data():
    """Carrega os dados brutos"""
    print("Carregando dados...")
    return pd.read_csv(RAW_DATA_PATH)

def clean_data(df):
    """Limpa e padroniza os dados"""
    print("Limpando dados...")

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["price"] = pd.to_numeric(df["price"])
    df["quantity"] = pd.to_numeric(df["quantity"])
    df["revenue"] = pd.to_numeric(df["revenue"])

    df["category"] = df["category"].str.strip().str.title()
    df["payment_method"] = df["payment_method"].str.lower().str.replace("_", " ")

    return df

def save_data(df):
    """Salva o arquivo processado"""
    print("Salvando dados processados...")
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Arquivo salvo em {PROCESSED_DATA_PATH}")

def run_etl():
    """Executa o pipeline ETL"""
    df = load_data()
    df = clean_data(df)
    save_data(df)
    print("Processamento concluído!")

if __name__ == "__main__":
    run_etl()
