from models.orders import Pedido

def test_pedido_salvar_id_usuario_obrigatorio(capsys, monkeypatch):
    """ID do usuário vazio deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido("", 100.00, "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O ID do usuário é obrigatório." in out


def test_pedido_salvar_id_usuario_negativo(capsys, monkeypatch):
    """ID de usuário <= 0 deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido(-1, 100.00, "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O ID do usuário deve ser um número positivo." in out


def test_pedido_salvar_id_usuario_invalido(capsys, monkeypatch):
    """ID de usuário não numérico deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido("abc", 100.00, "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O ID do usuário deve ser um número inteiro." in out


def test_pedido_salvar_total_negativo(capsys, monkeypatch):
    """Total do pedido negativo deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido(1, -10.0, "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O total do pedido não pode ser negativo." in out


def test_pedido_salvar_total_invalido(capsys, monkeypatch):
    """Total do pedido não numérico deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido(1, "abc", "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O total do pedido deve ser um número válido." in out


def test_pedido_salvar_status_invalido(capsys, monkeypatch):
    """Status inválido deve ser rejeitado."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    pedido = Pedido(1, 100.0, "status_errado", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: Status inválido." in out


def test_pedido_salvar_usuario_inexistente(capsys, monkeypatch):
    """
    Se o usuário não existir no banco (COUNT(*) = 0),
    deve mostrar mensagem de erro e não inserir.
    """

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._step = 0

        def execute(self, query, params=None):
           
            pass

        def fetchone(self):
            
            return [0]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False  

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    pedido = Pedido(999, 100.0, "1", "teste")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Erro: O usuário com ID 999 não existe." in out


def test_pedido_salvar_sucesso(capsys, monkeypatch):
    """
    Caminho feliz: usuário existe e pedido é cadastrado com sucesso,
    sem acessar o banco de verdade.
    """

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._call = 0

        def execute(self, query, params=None):
            
            self._call += 1

        def fetchone(self):
            
            return [1]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    pedido = Pedido(1, 150.0, "1", "teste ok")
    pedido.salvar()

    out = capsys.readouterr().out
    assert "Pedido cadastrado com sucesso!" in out


def test_pedido_editar_nao_encontrado(capsys, monkeypatch):
    """Se o pedido não existir, deve avisar e não atualizar nada."""
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._step = 0

        def execute(self, query, params=None):
            self._step += 1

        def fetchone(self):
            
            return [0]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.editar(999, "1")

    out = capsys.readouterr().out
    assert "Pedido não encontrado." in out


def test_pedido_editar_status_invalido(capsys, monkeypatch):
    """Status inválido ao editar deve ser rejeitado."""

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._step = 0

        def execute(self, query, params=None):
            self._step += 1

        def fetchone(self):
            
            return [1]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.editar(1, "status_errado")

    out = capsys.readouterr().out
    assert "Erro: Status inválido." in out


def test_pedido_editar_total_negativo(capsys, monkeypatch):
    """Novo total negativo deve ser rejeitado ao editar."""

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self._step = 0

        def execute(self, query, params=None):
            self._step += 1

        def fetchone(self):
            # Pedido existe
            return [1]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.editar(1, "1", novo_total=-10.0)

    out = capsys.readouterr().out
    assert "Erro: O total não pode ser negativo." in out


def test_pedido_editar_sucesso(capsys, monkeypatch):
    """Edição bem-sucedida (status + total + observação)."""

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self.executed = []

        def execute(self, query, params=None):
            self.executed.append((query, params))

        def fetchone(self):
            # Pedido existe
            return [1]

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.editar(1, "2", novo_total=200.0, nova_observacao="atualizado")

    out = capsys.readouterr().out
    assert "Pedido atualizado com sucesso!" in out


def test_pedido_excluir_sucesso(capsys, monkeypatch):
    """Exclusão de pedido com rowcount > 0."""

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self.rowcount = 1

        def execute(self, query, params=None):
            pass

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.excluir(1)

    out = capsys.readouterr().out
    assert "Pedido excluído com sucesso!" in out


def test_pedido_excluir_nao_encontrado(capsys, monkeypatch):
    """Exclusão de pedido com rowcount = 0 deve avisar que não encontrou."""

    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    class FakeCursor:
        def __init__(self):
            self.rowcount = 0

        def execute(self, query, params=None):
            pass

    class FakeTransaction:
        def __enter__(self):
            return FakeCursor()

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    monkeypatch.setattr("models.orders.Transaction", FakeTransaction)

    Pedido.excluir(999)

    out = capsys.readouterr().out
    assert "Pedido não encontrado." in out
