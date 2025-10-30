from db.connection import get_connection

class Usuario:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def salvar(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, telefone) VALUES (%s, %s, %s)",
                    (self.nome, self.email, self.telefone)
                )
                conn.commit()
                print("Usuário cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar usuário: {e}")
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()

            if not usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                print("\n=== Usuários Cadastrados ===")
                for u in usuarios:
                    print(f"{u['id']} - {u['nome']} ({u['email']})")

            cursor.close()
            conn.close()