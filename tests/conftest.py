# tests/conftest.py
import os
import sys

import pytest

# Garante que a raiz do projeto (onde está main.py) fique no sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Tenta importar a conexão tanto como pacote (db.connection)
# quanto como módulo solto (connection.py na raiz), para cobrir os dois cenários
try:
    from db.connection import get_connection
except ModuleNotFoundError:
    from connection import get_connection


@pytest.fixture(scope="session")
def db_conn():
    """
    Abre uma conexão real com o banco para a sessão de testes inteira.
    Fecha no final.
    """
    conn = get_connection()
    assert conn is not None, "Não foi possível abrir conexão com o banco. Verifique o .env e o MySQL."
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_conn):
    """
    Cria um cursor para cada teste.
    Tudo que for feito dentro do teste é desfeito com rollback no final,
    para não sujar o banco.
    """
    cursor = db_conn.cursor(dictionary=True, buffered=True)
    # Inicia transação manualmente só pra garantir
    db_conn.start_transaction()
    try:
        yield cursor
    finally:
        # Desfaz qualquer alteração feita durante o teste
        db_conn.rollback()
        cursor.close()
