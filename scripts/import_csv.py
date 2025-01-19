import psycopg2
import pandas as pd

def importar_csv(caminho_arquivo):
    # Conexão com o banco de dados
    conn = psycopg2.connect(
        dbname="cnpj_db",
        user="usuario_cnpj",
        password="cnpj",
        host="localhost"
    )
    cur = conn.cursor()

    # Carregar o CSV sem cabeçalho e definir nomes das colunas
    df = pd.read_csv(caminho_arquivo, sep=";", encoding="latin1", header=None)
    df.columns = ["codigo_cnae", "descricao"]  # Define os nomes das colunas

    # Inserir os dados no PostgreSQL
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO cnae (codigo_cnae, descricao) VALUES (%s, %s) ON CONFLICT (codigo_cnae) DO NOTHING;",
            (row['codigo_cnae'], row['descricao'])
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Dados importados com sucesso!")

if __name__ == "__main__":
    importar_csv("../dados/arquivo.csv")
