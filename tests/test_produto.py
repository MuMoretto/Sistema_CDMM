# tests/test_pedido.py
from models.orders import Pedido

def test_pedido_status_invalido(capsys, monkeypatch):
    """Status inválido deve gerar mensagem de erro e não travar no input()."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido(1, 100.00, "status_errado", "teste")
    pedido.salvar()

    saida = capsys.readouterr()
    assert "status inválido" in saida.out.lower()
