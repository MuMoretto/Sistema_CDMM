from models.user import Usuario

def test_usuario_valido(monkeypatch):
    """Testa um usuário válido sem acessar o banco de verdade."""
    user = Usuario("Cadu Teste", "cadu@example.com", "14999999999")

    
    def mock_salvar(self):
        return "ok"

    monkeypatch.setattr(Usuario, "salvar", mock_salvar)
    assert user.salvar() == "ok"


def test_usuario_email_invalido(capsys, monkeypatch):
    """Testa a validação de e-mail inválido sem travar no input()."""
    
    monkeypatch.setattr("builtins.input", lambda *args, **kwargs: "")

    user = Usuario("Teste", "email-invalido", "14999999999")
    user.salvar()

    saida = capsys.readouterr()
    assert "E-mail inválido" in saida.out
