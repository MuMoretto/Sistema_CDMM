from dotenv import load_dotenv
load_dotenv()
import re

from db.connection import Transaction

class Categoria:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    def salvar(self):

        if not self.nome or not self.descricao:
            print("Nome e descrição são obrigatórios.")
            return
        
        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.nome):
            print("Nome inválido. Use apenas letras.")
            return
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "INSERT INTO categorias (nome, descricao) VALUES (%s, %s)",
                    (self.nome, self.descricao)
                )
                print("Categoria cadastrada com sucesso!")
        except Exception as e:
                print(f"Erro ao cadastrar categoria: {e}")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT * FROM categorias")
                categorias = cursor.fetchall()

            if not categorias:
                print("Nenhuma categoria cadastrada.")
            else:
                print("\n=========== Categorias Cadastradas ===========\n")
                for c in categorias:
                    print(f"{c['id']} - {c['nome']} ({c['descricao']})")
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")


    @staticmethod
    def editar(id_categoria, novo_nome, nova_descricao):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "UPDATE categorias SET nome = %s, descricao = %s WHERE id = %s",
                    (novo_nome, nova_descricao, id_categoria)
                )
                if cursor.rowcount > 0:
                    print("Categoria atualizada com sucesso!")
                else:
                    print("Categoria não encontrada.")
        except Exception as e:
            print(f"Erro ao atualizar categoria: {e}")
                
    @staticmethod
    def excluir(id_categoria):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "DELETE FROM categorias WHERE id = %s",
                    (id_categoria,)
                )
                if cursor.rowcount > 0:
                    print("Categoria excluída com sucesso!")
                else:
                    print("Categoria não encontrada.")
        except Exception as e:
                print(f"Erro ao excluir categoria: {e}")

    @staticmethod
    def editar_descricao(id_categoria, nova_descricao):
        try:
            with Transaction() as cursor:
                cursor.execute(
                    "UPDATE categorias SET descricao = %s WHERE id = %s",
                    (nova_descricao, id_categoria)
                )
                if cursor.rowcount > 0:
                    print("Descrição da categoria atualizada com sucesso!")
                else:
                    print("Categoria não encontrada.")
        except Exception as e:
                print(f"Erro ao atualizar descrição da categoria: {e}")