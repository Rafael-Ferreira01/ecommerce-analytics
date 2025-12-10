from process_data import run_etl

def main():
    print("Iniciando pipeline de dados...")
    run_etl()
    print("Pipeline finalizado!")

if __name__ == "__main__":
    main()
