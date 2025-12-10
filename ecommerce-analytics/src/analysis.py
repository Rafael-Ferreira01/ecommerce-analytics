import pandas as pd
import matplotlib.pyplot as plt
import os

# caminho para o arquivo processado
PROCESSED_DATA_PATH = "data/processed/vendas_processado.csv"

def load_processed_data():
    print("Carregando dados processados...")
    return pd.read_csv(PROCESSED_DATA_PATH)

def generate_revenue_by_category(df):
    print("Gerando gráfico: Receita por Categoria...")

    revenue = df.groupby("category")["revenue"].sum()

    plt.figure(figsize=(8,5))
    revenue.plot(kind="bar")   # sem cor definida (recomendação default)
    plt.title("Receita por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Receita Total")
    plt.tight_layout()

    # criar pasta caso não exista
    os.makedirs("reports/plots", exist_ok=True)

    plt.savefig("reports/plots/revenue_by_category.png")
    plt.close()

def generate_monthly_sales(df):
    print("Gerando gráfico: Vendas Mensais...")

    df["order_date"] = pd.to_datetime(df["order_date"])
    monthly = df.groupby(df["order_date"].dt.to_period("M"))["revenue"].sum()

    plt.figure(figsize=(8,5))
    monthly.plot(kind="line", marker="o")
    plt.title("Receita Mensal")
    plt.xlabel("Mês")
    plt.ylabel("Receita Total")
    plt.tight_layout()

    os.makedirs("reports/plots", exist_ok=True)
    plt.savefig("reports/plots/revenue_monthly.png")
    plt.close()

def run_analysis():
    df = load_processed_data()
    generate_revenue_by_category(df)
    generate_monthly_sales(df)
    print("Análises geradas em: reports/plots/")

if __name__ == "__main__":
    run_analysis()
