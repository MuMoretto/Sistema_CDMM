from dotenv import load_dotenv
load_dotenv()
import re

from db.connection import Transaction

class MovimentacaoEstoque:
    def __init__(self, id_produto, tipo_movimentacao, quantidade, referencia=None, observacao=None):
        self.id_produto = id_produto
        self.tipo_movimentacao = tipo_movimentacao
        self.quantidade = quantidade
        self.referencia = referencia
        self.observacao = observacao

    def salvar(self):

        if not re.match(r"^\d+$", str(self.id_produto)):
            print("Erro: O ID do produto deve conter apenas números.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.id_produto = int(self.id_produto)
            if self.id_produto <= 0:
                print("Erro: O ID do produto deve ser positivo.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: O ID do produto deve ser um número inteiro.")
            input("\nPressione 'Enter' para continuar...")
            return

        if self.tipo_movimentacao not in ["entrada", "saida", "ajuste"]:
            print("Erro: Tipo inválido. Use 'entrada', 'saida' ou 'ajuste'.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.quantidade = int(self.quantidade)
            if self.quantidade <= 0:
                print("Erro: A quantidade deve ser positiva.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: A quantidade deve ser um número inteiro.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transaction() as cursor:
                cursor.execute("SELECT COUNT(*) FROM produtos WHERE id = %s", (self.id_produto,))
                if cursor.fetchone()[0] == 0:
                    print("Erro: O produto informado não existe.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                cursor.execute("""
                    INSERT INTO estoque_movimentacoes (id_produto, tipo_movimentacao, quantidade, referencia, observacao)
                    VALUES (%s, %s, %s, %s, %s)
                """, (self.id_produto, self.tipo_movimentacao, self.quantidade, self.referencia, self.observacao))

                if self.tipo_movimentacao == "entrada":
                    cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque + %s WHERE id = %s",
                                   (self.quantidade, self.id_produto))
                elif self.tipo_movimentacao == "saida":
                    cursor.execute("UPDATE produtos SET quantidade_estoque = quantidade_estoque - %s WHERE id = %s",
                                   (self.quantidade, self.id_produto))
                elif self.tipo_movimentacao == "ajuste":
                    cursor.execute("UPDATE produtos SET quantidade_estoque = %s WHERE id = %s",
                                   (self.quantidade, self.id_produto))

                print("Movimentação registrada com sucesso!")
                input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            print(f"Erro ao registrar movimentação: {e}")
            input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("""
                    SELECT m.id, m.data_movimentacao, m.tipo_movimentacao, m.quantidade, 
                           m.referencia, m.observacao, p.nome AS produto
                    FROM estoque_movimentacoes m
                    INNER JOIN produtos p ON m.id_produto = p.id
                    ORDER BY m.data_movimentacao DESC
                """)
                movimentacoes = cursor.fetchall()

                if not movimentacoes:
                    print("Nenhuma movimentação registrada.")
                else:
                    print("\n========== Movimentações de Estoque ==========\n")
                    for mov in movimentacoes:
                        print(f"ID: {mov['id']} | Produto: {mov['produto']}")
                        print(f"Data: {mov['data_movimentacao']} | Tipo: {mov['tipo_movimentacao']} | Qtde: {mov['quantidade']}")
                        print(f"Ref: {mov['referencia'] or '---'} | Obs: {mov['observacao'] or '---'}")
                        print("------------------------------------------------")

                input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            print(f"Erro ao listar movimentações: {e}")
            input("\nPressione 'Enter' para continuar...")
