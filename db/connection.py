import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[ERRO] Falha na conexão com o banco de dados: {err}")
        return None


class Transaction:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = get_connection()
        if not self.conn:
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        
        self.cursor = self.conn.cursor(dictionary=True, buffered=True)
        self.conn.start_transaction()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
                print(f"Transação revertida devido a erro: {exc_val}")
            if exc_val:
                raise exc_val
        finally:
            if self.cursor:
                try:
                    self.cursor.close()
                except Exception:
                    pass  # Garante que o fechamento não quebre o fluxo
            if self.conn:
                try:
                    self.conn.close()
                except Exception:
                    pass
