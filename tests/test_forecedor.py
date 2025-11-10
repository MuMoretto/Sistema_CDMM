from models.fornec import Fornecedor


def test_fornecedor_nome_obrigatorio(capsys):
    """
    Nome e contato são obrigatórios.
    """
    fornecedor = Fornecedor("", "")
    fornecedor.salvar()

    out = capsys.readouterr().out.lower()
    assert "nome e contato de fornecedor são obrigatórios" in out


def test_fornecedor_nome_invalido(capsys):
    """
    Nome com números deve ser rejeitado.
    """
    fornecedor = Fornecedor("Fornecedor 123", "contato@teste.com")
    fornecedor.salvar()

    out = capsys.readouterr().out.lower()
    assert "nome inválido" in out


def test_fornecedor_valido_sem_banco(capsys, monkeypatch):
    """
    Caminho feliz: fornecedor válido, sem usar banco de verdade.
    """
    class FakeCursor:
        def execute(self, query, params=None):
            pass

        def fetchone(self):
            return [0]

        def fetchall(self):
            return []

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.fornec.Transaction", FakeTransaction)

    fornecedor = Fornecedor("Fornecedor Teste", "contato@teste.com")
    fornecedor.salvar()

    out = capsys.readouterr().out.lower()
    assert "fornecedor cadastrado com sucesso" in out
