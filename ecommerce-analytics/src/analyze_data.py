import pandas as pd
import matplotlib.pyplot as plt

PROCESSED_DATA_PATH = "data/processed/vendas_processado.csv"

def load_data():
    return pd.read_csv(PROCESSED_DATA_PATH)

def vendas_por_categoria(df):
    df.groupby("category")["revenue"].sum().plot(kind="bar")
    plt.title("Vendas por Categoria")
    plt.show()

def vendas_mensais(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df.groupby(df["order_date"].dt.to_period("M"))["revenue"].sum().plot(kind="line")
    plt.title("Faturamento Mensal")
    plt.show()

def main():
    df = load_data()
    vendas_por_categoria(df)
    vendas_mensais(df)

if __name__ == "__main__":
    main()
