import os
from db.connection import Transaction

def r_estoque_por_categoria():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: ESTOQUE POR CATEGORIA ===")
    try:
        with Transaction() as cursor:
            query = """
                SELECT 
                    c.nome AS categoria,
                    SUM(p.quantidade_estoque) AS total_estoque,
                    SUM(p.preco * p.quantidade_estoque) AS valor_total
                FROM produtos p
                JOIN categorias c ON p.id_categoria = c.id
                GROUP BY c.nome
                ORDER BY c.nome;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum resultado encontrado.")
                return

            print()
            print(f"{'Categoria':<20} {'| Qtde Estoque':<15} {'| Valor Total (R$)':<20}")
            print("-" * 60)
            for r in resultados:
                print(f"{r['categoria']:<20} | {r['total_estoque']:<13} | {r['valor_total']:>10.2f}")
            print("=" * 60)
            input("\nPressione 'Enter' para continuar...")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        input("\nPressione 'Enter' para continuar...")


def r_pedidos_por_fornecedor():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: PEDIDOS POR FORNECEDOR ===")
    try:
        with Transaction() as cursor:
            query = """
                SELECT 
                    f.nome AS fornecedor,
                    COUNT(ped.id) AS total_pedidos,
                    SUM(ped.total_pedido) AS valor_total_pedidos
                FROM pedidos ped
                JOIN usuarios u ON ped.id_usuario = u.id
                JOIN itens_pedido i ON ped.id = i.id_pedido
                JOIN produtos p ON i.id_produto = p.id
                JOIN fornecedores f ON p.id_fornecedor = f.id
                GROUP BY f.nome
                ORDER BY valor_total_pedidos DESC;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum resultado encontrado.")
                input("\nPressione 'Enter' para continuar...")
                return

            print()
            print(f"{'Fornecedor':<25} {'| Qtde Pedidos':<15} {'| Valor Total (R$)':<20}")
            print("-" * 65)
            for r in resultados:
                print(f"{r['fornecedor']:<25} | {r['total_pedidos']:<13} | {r['valor_total_pedidos']:>10.2f}")
            print("=" * 65)
            input("\nPressione 'Enter' para continuar...")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        input("\nPressione 'Enter' para continuar...")


def r_produtos_sem_estoque():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: PRODUTOS SEM ESTOQUE ===")
    try:
        with Transaction() as cursor:
            query = """
                SELECT 
                    p.nome AS produto,
                    c.nome AS categoria,
                    f.nome AS fornecedor
                FROM produtos p
                LEFT JOIN categorias c ON p.id_categoria = c.id
                LEFT JOIN fornecedores f ON p.id_fornecedor = f.id
                WHERE p.quantidade_estoque = 0
                ORDER BY c.nome, p.nome;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum produto sem estoque.")
                input("\nPressione 'Enter' para continuar...")
                return

            print("\nProduto\t| Categoria\t| Fornecedor")
            print("-" * 60)
            for r in resultados:
                print(f"{r['produto']}\t| {r['categoria']}\t| {r['fornecedor']}")
            print("===================================================")
            input("\nPressione 'Enter' para continuar...")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        input("\nPressione 'Enter' para continuar...")


def r_produtos_mais_vendidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: PRODUTOS MAIS VENDIDOS ===")
    try:
        with Transaction() as cursor:
            query = """
                SELECT 
                    p.nome AS produto,
                    SUM(CASE WHEN m.tipo_movimentacao = 'saida' THEN m.quantidade ELSE 0 END) AS total_vendido,
                    SUM(CASE WHEN m.tipo_movimentacao = 'saida' THEN m.quantidade * p.preco ELSE 0 END) AS valor_total
                FROM estoque_movimentacoes m
                JOIN produtos p ON m.id_produto = p.id
                WHERE m.tipo_movimentacao = 'saida'
                GROUP BY p.nome
                HAVING total_vendido > 0
                ORDER BY total_vendido DESC
                LIMIT 10;
            """
            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum produto vendido encontrado.")
                input("\nPressione 'Enter' para continuar...")
                return

            print()
            print(f"{'Produto':<30} {'| Qtde Vendida':<15} {'| Valor Total (R$)':<20}")
            print("-" * 70)
            for r in resultados:
                print(f"{r['produto']:<30} | {r['total_vendido']:<13} | {r['valor_total']:>10.2f}")
            print("=" * 70)
            input("\nPressione 'Enter' para continuar...")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")
        input("\nPressione 'Enter' para continuar...")
