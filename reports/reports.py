from db.connection import Transaction


# ==========================================================
# 1️⃣ RELATÓRIO DE ESTOQUE TOTAL POR CATEGORIA (JOIN + SUM)
# ==========================================================
def relatorio_estoque_por_categoria():
    print("\n=== RELATÓRIO: ESTOQUE POR CATEGORIA ===")

    try:
        with Transaction() as cursor:
            query = """
            SELECT c.nome AS categoria,
                   SUM(p.quantidade_estoque) AS total_estoque
            FROM produtos p
            INNER JOIN categorias c ON p.categoria_id = c.id
            GROUP BY c.nome
            ORDER BY total_estoque DESC;
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum dado encontrado.")
            else:
                for categoria, total in resultados:
                    print(f"Categoria: {categoria:<20} | Total em estoque: {total}")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

    print("=========================================")



# ==========================================================
# 2️⃣ RELATÓRIO DE PEDIDOS POR FORNECEDOR (JOIN + COUNT)
# ==========================================================
def relatorio_pedidos_por_fornecedor():
    print("\n=== RELATÓRIO: PEDIDOS POR FORNECEDOR ===")

    try:
        with Transaction() as cursor:
            query = """
            SELECT f.nome AS fornecedor,
                   COUNT(ped.id) AS total_pedidos
            FROM fornecedores f
            LEFT JOIN produtos p ON p.fornecedor_id = f.id
            LEFT JOIN pedidos ped ON ped.produto_id = p.id
            GROUP BY f.nome
            ORDER BY total_pedidos DESC;
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum pedido registrado.")
            else:
                for fornecedor, total in resultados:
                    print(f"Fornec.: {fornecedor:<25} | Pedidos: {total}")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

    print("==========================================")


# ==========================================================
# 3️⃣ RELATÓRIO DE FORNECEDORES SEM PEDIDOS (EXISTS)
# ==========================================================
def relatorio_fornecedores_sem_pedidos():
    print("\n=== RELATÓRIO: FORNECEDORES SEM PEDIDOS ===")

    try:
        with Transaction() as cursor:
            query = """
            SELECT f.nome
            FROM fornecedores f
            WHERE NOT EXISTS (
                SELECT 1
                FROM produtos p
                INNER JOIN pedidos ped ON ped.produto_id = p.id
                WHERE p.fornecedor_id = f.id
            )
            ORDER BY f.nome;
            """

            cursor.execute(query)
            resultados = cursor.fetchall()

            if not resultados:
                print("Todos os fornecedores possuem pedidos registrados.")
            else:
                for (nome,) in resultados:
                    print(f"- {nome}")

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

    print("=============================================")
