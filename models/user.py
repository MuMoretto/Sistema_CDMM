import re
from dotenv import load_dotenv
from db.connection import Transaction

load_dotenv()

class Usuario:
    def __init__(self, nome, email, telefone):
        self.nome = nome.strip() if nome else None
        self.email = email.strip() if email else None
        self.telefone = telefone.strip() if telefone else None

    def salvar(self):
        if not self.nome:
            print("Erro: O Nome é obrigatório e não pode ser vazio.")
            input("\nPressione 'Enter' para continuar...")
            return
        
        if not re.search(r'[a-zA-Z]', self.nome):
            print("Erro: O Nome deve conter pelo menos uma letra.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not self.email:
            print("Erro: O E-mail é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao_email, self.email):
            print("Erro: E-mail inválido. O formato esperado é: exemplo@dominio.com")
            input("\nPressione 'Enter' para continuar...")
            return

        if not self.telefone:
            print("Erro: O Telefone é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not self.telefone.isdigit() or len(self.telefone) != 11:
            print("Erro: O Telefone deve conter apenas números e ter exatamente 11 dígitos (com DDD).")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transaction() as cursor:
                cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE telefone = %s", (self.telefone,))
                if cursor.fetchone()["total"] > 0:
                    print(f"Erro: O telefone {self.telefone} já está cadastrado para outro usuário.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                cursor.execute("SELECT COUNT(*) AS total FROM usuarios WHERE email = %s", (self.email,))
                if cursor.fetchone()["total"] > 0:
                    print(f"Erro: O e-mail {self.email} já está cadastrado em outro usuário.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                cursor.execute(
                    "INSERT INTO usuarios (nome, email, telefone) VALUES (%s, %s, %s)",
                    (self.nome, self.email, self.telefone)
                )

            print("Usuário cadastrado com sucesso!")
            input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT * FROM usuarios ORDER BY id ASC")
                usuarios = cursor.fetchall()

                if not usuarios:
                    print("Nenhum usuário cadastrado.")
                else:
                    print("\n============= Usuários Cadastrados =============\n")
                    for u in usuarios:
                        print(f"{u['id']} - {u['nome']} ({u['email']} - {u['telefone']})")


        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def editar(id_usuario, novo_nome, novo_email, novo_telefone):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "UPDATE usuarios SET nome = %s, email = %s, telefone = %s WHERE id = %s",
                    (novo_nome, novo_email, novo_telefone, id_usuario)
                )

                if cursor.rowcount > 0:
                    print("Usuário atualizado com sucesso!")
                else:
                    print("Usuário não encontrado.")

            input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(id_usuario):
        try:
            with Transaction() as cursor:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
                if cursor.rowcount > 0:
                    print("Usuário excluído com sucesso!")
                else:
                    print("Usuário não encontrado.")

            input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            input("\nPressione 'Enter' para continuar...")
