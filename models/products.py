from dotenv import load_dotenv
load_dotenv()
import re

from db.connection import Transaction

class Produto:
    def __init__(self, nome, id_categoria, id_fornecedor, preco, quantidade_estoque):
        self.nome = nome
        self.id_categoria = id_categoria
        self.id_fornecedor = id_fornecedor
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def salvar(self):
        if not self.nome or not self.nome.strip():
            print("Erro: O nome do produto é obrigatório e não pode ser vazio.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.preco = float(self.preco)
            if self.preco < 0:
                print("Erro: O preço não pode ser negativo.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: O preço deve ser um número válido.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.quantidade_estoque = int(self.quantidade_estoque)
            if self.quantidade_estoque < 0:
                print("Erro: A quantidade em estoque não pode ser negativa.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: A quantidade em estoque deve ser um número inteiro.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transaction() as cursor:
                cursor.execute("""
                    INSERT INTO produtos (nome, id_categoria, id_fornecedor, preco, quantidade_estoque)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.nome, self.id_categoria, self.id_fornecedor, self.preco, self.quantidade_estoque))

                print("Produto cadastrado com sucesso!")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("""
                SELECT p.id, p.nome, p.preco, p.quantidade_estoque, p.ativo,
                       c.nome AS categoria, f.nome AS fornecedor
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                LEFT JOIN fornecedores f ON p.id_fornecedor = f.id
                ORDER BY p.id;
                """)
                produtos = cursor.fetchall()

                if not produtos:
                    print("Nenhum produto cadastrado.")
                else:
                    print("\n============= Produtos Cadastrados =============")
                    for p in produtos:
                        status = "Ativo" if p['ativo'] else "Inativo"
                        print(f"\nID: {p['id']} | Nome: {p['nome']}")
                        print(f"Categoria: {p['categoria'] or 'N/A'} | Fornecedor: {p['fornecedor'] or 'N/A'}")
                        print(f"Preço: R${p['preco']:.2f} | Estoque: {p['quantidade_estoque']} | Status: {status}")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def editar(id_produto, novo_nome, novo_preco, nova_qtd, novo_id_categoria, novo_id_fornecedor):
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (id_produto,))
                if cursor.fetchone()[0] == 0:
                    print("Produto não encontrado.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                cursor.execute("""
                    UPDATE produtos
                    SET nome = %s, preco = %s, quantidade_estoque = %s,
                        id_categoria = %s, id_fornecedor = %s
                    WHERE id = %s
                """, (novo_nome, novo_preco, nova_qtd, novo_id_categoria, novo_id_fornecedor, id_produto))
                
                print("Produto atualizado com sucesso!")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(id_produto):
        try:
            with Transaction() as cursor:
                cursor.execute("DELETE FROM produtos WHERE id = %s", (id_produto,))
                if cursor.rowcount > 0:
                    print("Produto excluído com sucesso!")
                else:
                    print("Produto não encontrado.")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            input("\nPressione 'Enter' para continuar...")