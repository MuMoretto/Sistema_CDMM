import os
import sys

import pytest


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


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
    
    db_conn.start_transaction()
    try:
        yield cursor
    finally:
        
        db_conn.rollback()
        cursor.close()
