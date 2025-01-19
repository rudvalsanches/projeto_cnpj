from fastapi import FastAPI
from psycopg2 import connect

app = FastAPI()

def get_db_connection():
    return connect(
        dbname="cnpj_db",
        user="usuario_cnpj",
        password="cnpj",
        host="localhost"
    )

@app.get("/cnae/{codigo}")
def read_cnae(codigo: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cnae WHERE codigo_cnae = %s", (codigo,))
    result = cur.fetchone()
    conn.close()
    if result:
        return {"codigo_cnae": result[0], "descricao": result[1]}
    return {"error": "CNAE não encontrado"}
