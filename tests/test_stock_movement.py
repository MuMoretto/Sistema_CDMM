# tests/test_stock_movement.py
from models.stock_movement import MovimentacaoEstoque


def test_movimentacao_id_produto_invalido(capsys, monkeypatch):
    """
    Deve rejeitar ID de produto não numérico.
    """
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    mov = MovimentacaoEstoque("abc", "entrada", 10)
    mov.salvar()

    out = capsys.readouterr().out.lower()
    assert "id do produto deve ser um número inteiro" in out


def test_movimentacao_tipo_invalido(capsys, monkeypatch):
    """
    Deve rejeitar tipo de movimentação inválido.
    """
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    mov = MovimentacaoEstoque(1, "compra", 5)  # "compra" não é entrada/saida/ajuste
    mov.salvar()

    out = capsys.readouterr().out.lower()
    assert "tipo inválido" in out


def test_movimentacao_quantidade_invalida(capsys, monkeypatch):
    """
    Deve rejeitar quantidade <= 0.
    """
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    mov = MovimentacaoEstoque(1, "entrada", 0)
    mov.salvar()

    out = capsys.readouterr().out.lower()
    assert "quantidade deve ser positiva" in out


def test_movimentacao_valida_sem_banco(capsys, monkeypatch):
    """
    Caminho feliz: movimentação válida, mockando Transaction para não usar o banco.
    """
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._first = True

        def execute(self, query, params=None):
            # Não faz nada de verdade, só finge
            pass

        def fetchone(self):
            # Primeira chamada: SELECT COUNT(*) FROM produtos -> produto existe
            return [1]

        def fetchall(self):
            return []

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False  # não suprime exceções

    # Substitui a Transaction usada dentro do módulo stock_movement
    monkeypatch.setattr("models.stock_movement.Transaction", FakeTransaction)

    mov = MovimentacaoEstoque(1, "entrada", 5, "ref-teste", "obs-teste")
    mov.salvar()

    out = capsys.readouterr().out.lower()
    assert "movimentação registrada com sucesso" in out
