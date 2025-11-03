from dotenv import load_dotenv
load_dotenv("../implement_bd.env")
import re

from db.connection import get_connection

class Usuario:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone

    def salvar(self):
        if not self.nome or not self.nome.strip():
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
            print("Erro: O Telefone deve conter apenas números e ter exatamente 11 dígitos (Com o DDD).")
            input("\nPressione 'Enter' para continuar...")
            return

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE telefone = %s", (self.telefone,))
                if cursor.fetchone()[0] > 0:
                    print(f"Erro: O telefone {self.telefone} já está cadastrado para outro usuário.")
                    input("\nPressione 'Enter' para continuar...")
                    return
            except Exception as e:
                print(f"Erro ao verificar unicidade do telefone: {e}")
                input("\nPressione 'Enter' para continuar...")
                cursor.close()
                conn.close()
                return
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nome, email, telefone) VALUES (%s, %s, %s)",
                    (self.nome, self.email, self.telefone)
                )
                conn.commit()
                print("Usuário cadastrado com sucesso!")
                input("\nPressione 'Enter' para continuar...")
            except Exception as e:
                print(f"Erro ao cadastrar usuário: {e}")
                input("\nPressione 'Enter' para continuar...")
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
                input("\nPressione 'Enter' para continuar...")
            else:
                print("\n============= Usuários Cadastrados =============\n")
                for u in usuarios:
                    print(f"{u['id']} - {u['nome']} ({u['email']} - {u['telefone']})")
            cursor.close()
            conn.close()

    @staticmethod
    def editar(id_usuario, novo_nome, novo_email, novo_telefone):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "UPDATE usuarios SET nome = %s, email = %s, telefone = %s WHERE id = %s",
                    (novo_nome, novo_email, novo_telefone, id_usuario)
                )
                if cursor.rowcount > 0:
                    conn.commit()
                    print("Usuário atualizado com sucesso!")
                    input("\nPressione 'Enter' para continuar...")
                else:
                    print("Usuário não encontrado.")
                    input("\nPressione 'Enter' para continuar...")
            except Exception as e:
                print(f"Erro ao atualizar usuário: {e}")
                input("\nPressione 'Enter' para continuar...")
            finally:
                cursor.close()
                conn.close()

    @staticmethod
    def excluir(id_usuario):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
                if cursor.rowcount > 0:
                    conn.commit()
                    print("Usuário excluído com sucesso!")
                    input("\nPressione 'Enter' para continuar...")
                else:
                    print("Usuário não encontrado.")
                    input("\nPressione 'Enter' para continuar...")
            except Exception as e:
                print(f"Erro ao excluir usuário: {e}")
                input("\nPressione 'Enter' para continuar...")
            finally:
                cursor.close()
                conn.close()