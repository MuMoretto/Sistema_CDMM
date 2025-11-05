from dotenv import load_dotenv
load_dotenv()
from db.connection import Transaction

class Pedido:
    def __init__(self, id_usuario, total_pedido, status="1", observacao=None):
        self.id_usuario = id_usuario
        self.total_pedido = total_pedido
        self.status = status
        self.observacao = observacao

    def salvar(self):
        if not self.id_usuario:
            print("Erro: O ID do usuário é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.id_usuario = int(self.id_usuario)
            if self.id_usuario <= 0:
                print("Erro: O ID do usuário deve ser um número positivo.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: O ID do usuário deve ser um número inteiro.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            self.total_pedido = float(self.total_pedido)
            if self.total_pedido < 0:
                print("Erro: O total do pedido não pode ser negativo.")
                input("\nPressione 'Enter' para continuar...")
                return
        except ValueError:
            print("Erro: O total do pedido deve ser um número válido.")
            input("\nPressione 'Enter' para continuar...")
            return

        if isinstance(self.status, str) and self.status.isdigit():
            self.status = {
                "1": "em_andamento",
                "2": "concluido",
                "3": "cancelado"
            }.get(self.status, None)

        if self.status not in ["em_andamento", "concluido", "cancelado"]:
            print("Erro: Status inválido. Use 1 (Em andamento), 2 (Concluído) ou 3 (Cancelado).")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transaction() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s", (self.id_usuario,))
                if cursor.fetchone()[0] == 0:
                    print(f"Erro: O usuário com ID {self.id_usuario} não existe.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                cursor.execute("""
                    INSERT INTO pedidos (id_usuario, total_pedido, status, observacao)
                    VALUES (%s, %s, %s, %s)
                """, (self.id_usuario, self.total_pedido, self.status, self.observacao))

                print("Pedido cadastrado com sucesso!")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
                print(f"Erro ao cadastrar pedido: {e}")
                input("\nPressione 'Enter' para continuar...")


    @staticmethod
    def listar():
        try:
            with Transaction() as cursor:
                cursor.execute("""
                    SELECT p.id, p.data_pedido, p.total_pedido, p.status, p.observacao,
                           u.nome AS usuario
                    FROM pedidos p
                    INNER JOIN usuarios u ON p.id_usuario = u.id
                    ORDER BY p.id DESC
                """)
                pedidos = cursor.fetchall()

                if not pedidos:
                    print("Nenhum pedido cadastrado.")
                    input("\nPressione 'Enter' para continuar...")
                else:
                    print("\n============= Pedidos Cadastrados =============\n")
                    for ped in pedidos:
                        status_formatado = ped['status'].replace("_", " ").title()
                        print(f"ID: {ped['id']} | Usuário: {ped['usuario']}")
                        print(f"Data: {ped['data_pedido']} | Total: R${ped['total_pedido']:.2f}")
                        print(f"Status: {status_formatado} | Obs: {ped['observacao'] or '---'}")
                        print("------------------------------------------------")
                    input("\nPressione 'Enter' para continuar...")
        except Exception as e:
                print(f"Erro ao listar pedidos: {e}")
                input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def editar(id_pedido, novo_status, novo_total=None, nova_observacao=None):
        try:
            with Transaction() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pedidos WHERE id = %s", (id_pedido,))
                if cursor.fetchone()[0] == 0:
                    print("Pedido não encontrado.")
                    input("\nPressione 'Enter' para continuar...")
                    return

                if isinstance(novo_status, str) and novo_status.isdigit():
                    novo_status = {
                        "1": "em_andamento",
                        "2": "concluido",
                        "3": "cancelado"
                    }.get(novo_status, None)

                if novo_status not in ["em_andamento", "concluido", "cancelado"]:
                    print("Erro: Status inválido. Use 1 (Em andamento), 2 (Concluído) ou 3 (Cancelado).")
                    input("\nPressione 'Enter' para continuar...")
                    return

                campos = []
                valores = []

                if novo_total:
                    try:
                        novo_total = float(novo_total)
                        if novo_total < 0:
                            print("Erro: O total não pode ser negativo.")
                            input("\nPressione 'Enter' para continuar...")
                            return
                        campos.append("total_pedido = %s")
                        valores.append(novo_total)
                    except ValueError:
                        print("Erro: O total deve ser um número válido.")
                        input("\nPressione 'Enter' para continuar...")
                        return

                campos.append("status = %s")
                valores.append(novo_status)

                if nova_observacao is not None:
                    campos.append("observacao = %s")
                    valores.append(nova_observacao)

                valores.append(id_pedido)

                query = f"UPDATE pedidos SET {', '.join(campos)} WHERE id = %s"
                cursor.execute(query, tuple(valores))
 
                print("Pedido atualizado com sucesso!")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
                print(f"Erro ao editar pedido: {e}")
                input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(id_pedido):
        try:
            with Transaction() as cursor:
                cursor.execute("DELETE FROM pedidos WHERE id = %s", (id_pedido,))
                if cursor.rowcount > 0:

                    print("Pedido excluído com sucesso!")
                else:
                    print("Pedido não encontrado.")
                input("\nPressione 'Enter' para continuar...")
        except Exception as e:
                print(f"Erro ao excluir pedido: {e}")
                input("\nPressione 'Enter' para continuar...")