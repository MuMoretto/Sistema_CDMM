from dotenv import load_dotenv
load_dotenv()
import re

from db.connection import get_connection

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
        
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO fornecedores (nome, contato) VALUES (%s, %s)",
                    (self.nome, self.contato)
                )
                conn.commit()
                print("Fornecedor cadastrado com sucesso!")
            except Exception as e:
                print(f"Erro ao cadastrar fornecedor: {e}")
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fornecedores")
            fornecedores = cursor.fetchall()

            if not fornecedores:
                print("Nenhum fornecedor cadastrado.")
            else:
                print("\n=== Fornecedores Cadastrados ===")
                for f in fornecedores:
                    print(f"{f['id']} - {f['nome']} (Contato: {f['contato']})")

            cursor.close()
            conn.close()

    @staticmethod
    def listar():
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM fornecedores")
            fornecedores = cursor.fetchall()

            if not fornecedores:
                print("Nenhum fornecedor cadastrado.")
            else:
                print("\n============= Fornecedores Cadastrados =============\n")
                for f in fornecedores:
                    print(f"{f['id']} - {f['nome']} (Contato: {f['contato']})")

            cursor.close()
            conn.close()

    @staticmethod
    def editar(id_fornecedor, novo_nome, novo_contato):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE fornecedores SET nome = %s, contato = %s WHERE id = %s",
                    (novo_nome, novo_contato, id_fornecedor)
                )
                conn.commit()
                if cursor.rowcount == 0:
                    print("Fornecedor não encontrado.")
                else:
                    print("Fornecedor atualizado com sucesso!")
            except Exception as e:
                print(f"Erro ao editar fornecedor: {e}")
            finally:
                cursor.close()
                conn.close()
                
    @staticmethod
    def excluir(id_fornecedor):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "DELETE FROM fornecedores WHERE id = %s",
                    (id_fornecedor,)
                )
                conn.commit()
                if cursor.rowcount > 0:
                    print("Fornecedor excluído com sucesso!")
                else:
                    print("Fornecedor não encontrado.")
            except Exception as e:
                print(f"Erro ao excluir fornecedor: {e}")
            finally:
                cursor.close()
                conn.close()
