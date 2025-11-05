from dotenv import load_dotenv
load_dotenv()
import re

from db.connection import Transaction

class Fornecedor:
    def __init__(self, nome, contato):
        self.nome = nome
        self.contato = contato

    def salvar(self):

        if not self.nome or not self.contato:
            print("Nome e contato de fornecedor são obrigatórios.")
            return
        
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.nome):
            print("Nome inválido. Use apenas letras.")
            return 
        
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "INSERT INTO fornecedores (nome, contato) VALUES (%s, %s)",
                    (self.nome, self.contato)
                )
                print("Fornecedor cadastrado com sucesso!")
        except Exception as e:
                print(f"Erro ao cadastrar fornecedor: {e}")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT * FROM fornecedores")
                fornecedores = cursor.fetchall()

            if not fornecedores:
                print("Nenhum fornecedor cadastrado.")
            else:
                print("\n=== Fornecedores Cadastrados ===")
                for f in fornecedores:
                    print(f"{f['id']} - {f['nome']} (Contato: {f['contato']})")
        except Exception as e:
            print(f"Erro ao listar fornecedores: {e}")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT * FROM fornecedores")
                fornecedores = cursor.fetchall()

            if not fornecedores:
                print("Nenhum fornecedor cadastrado.")
            else:
                print("\n============= Fornecedores Cadastrados =============\n")
                for f in fornecedores:
                    print(f"{f['id']} - {f['nome']} (Contato: {f['contato']})")
        except Exception as e:
            print(f"Erro ao listar fornecedores: {e}")

    @staticmethod
    def editar(id_fornecedor, novo_nome, novo_contato):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "UPDATE fornecedores SET nome = %s, contato = %s WHERE id = %s",
                    (novo_nome, novo_contato, id_fornecedor)
                )
                if cursor.rowcount == 0:
                    print("Fornecedor não encontrado.")
                else:
                    print("Fornecedor atualizado com sucesso!")
        except Exception as e:
                print(f"Erro ao editar fornecedor: {e}")

    @staticmethod
    def excluir(id_fornecedor):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "DELETE FROM fornecedores WHERE id = %s",
                    (id_fornecedor,)
                )
                if cursor.rowcount > 0:
                    print("Fornecedor excluído com sucesso!")
                else:
                    print("Fornecedor não encontrado.")
        except Exception as e:
                print(f"Erro ao excluir fornecedor: {e}")