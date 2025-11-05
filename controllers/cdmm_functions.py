import os
from models.user import Usuario
from models.categories import Categoria
from models.fornec import Fornecedor
from models.products import Produto
from models.orders import Pedido
from models.stock_movement import MovimentacaoEstoque
from reports.reports import (
    r_estoque_por_categoria,
    r_pedidos_por_fornecedor,                  #Chat NÃO aconselhou usar '*'...
    r_produtos_sem_estoque,
    r_produtos_mais_vendidos
)

def menu_usuarios():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========== Usuários ===========")
        print("=  1. Cadastrar Usuários       =")
        print("=  2. Listar Usuários          =")
        print("=  3. Editar Usuários          =")
        print("=  4. Excluir Usuários         =")
        print("=  0. Voltar                   =")
        print("================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")                             #Os usuários não "reaproveitam" os ID's antigos pois isso pode conflitar o projeto...
            telefone = input("Telefone: ")
            user = Usuario(nome, email, telefone)
            user.salvar()
        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Usuario.listar()
            input("\nPressione 'Enter' para continuar...")
        elif opcao == "3":
            id_usuario = input("ID do usuário que deseja editar: ")
            novo_nome = input("Novo nome: ")
            novo_email = input("Novo email: ")
            novo_telefone = input("Novo telefone: ")
            Usuario.editar(id_usuario, novo_nome, novo_email, novo_telefone)
        elif opcao == "4":
            id_usuario = input("ID do usuário que deseja excluir: ")
            Usuario.excluir(id_usuario)
        elif opcao == "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")

def menu_categorias():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=============== Categoria ===============")
        print("=  1. Cadastrar Categorias de Produtos  =")
        print("=  2. Listar Categorias                 =")
        print("=  3. Editar Categorias                 =")
        print("=  4. Excluir Categorias                =")
        print("=  5. Editar Descrição de Categorias    =")
        print("=  0. Voltar                            =")
        print("=========================================")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descricao: ")
            categori = Categoria(nome, descricao)
            categori.salvar()
            input("\nPressione 'Enter' para continuar...")
            
        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Categoria.listar()
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            id_categoria = input("ID da categoria a ser editada: ")
            novo_nome = input("Novo nome da categoria: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar(id_categoria, novo_nome, nova_descricao)
            input("\nPressione 'Enter' para continuar...")

        elif opcao == "4":
            id_categoria = input("ID da categoria a ser excluída:")
            Categoria.excluir(id_categoria)
            input("\nPressione 'Enter' para continuar...")

        elif opcao == "5":
            id_categoria = input("ID da categoria a ser editada: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar_descricao(id_categoria, nova_descricao)
            input("\nPressione 'Enter' para continuar...")
            
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")


def menu_fornecedores():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========== Fornecedores =============")
        print("=  1. Cadastrar Fornecedores         =")
        print("=  2. Listar Fornecedores            =")
        print("=  3. Editar nos Fornecedores        =")
        print("=  4. Excluir Fornecedores           =")
        print("=  0. Voltar                         =")
        print("======================================")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            contato = input("Contato: ")
            fornecedor = Fornecedor(nome, contato)
            fornecedor.salvar()
            input("\nPressione 'Enter' para continuar...")

        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Fornecedor.listar()
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            id_fornecedor = input("ID do fornecedor que deseja editar: ")
            novo_nome = input("Novo nome: ")
            novo_contato = input("Novo contato: ")
            Fornecedor.editar(id_fornecedor, novo_nome, novo_contato)
            input("\nPressione 'Enter' para continuar...")

        elif opcao == "4":
            id_fornecedor = input("ID do fornecedor que deseja excluir: ")
            Fornecedor.excluir(id_fornecedor)
            input("\nPressione 'Enter' para continuar...")

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")

def menu_produtos():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n============ Produtos ============")
        print("=  1. Cadastrar Produto          =")
        print("=  2. Listar Produtos            =")
        print("=  3. Editar Produto             =")
        print("=  4. Excluir Produto            =")
        print("=  0. Voltar                     =")
        print("==================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do Produto: ")
            sku = input("SKU: ")
            id_categoria = input("ID da Categoria (ou deixe vazio): ")
            id_fornecedor = input("ID do Fornecedor (ou deixe vazio): ")
            preco = input("Preço (Ex: 19.99): ")
            quantidade_estoque = input("Quantidade em Estoque: ")
            id_categoria = int(id_categoria) if id_categoria.strip() else None
            id_fornecedor = int(id_fornecedor) if id_fornecedor.strip() else None
            produto = Produto(nome, sku, id_categoria, id_fornecedor, preco, quantidade_estoque)
            produto.salvar()

        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Produto.listar()

        elif opcao == "3":
            id_produto = input("ID do produto que deseja editar: ")
            novo_nome = input("Novo nome: ")
            novo_sku = input("Novo SKU: ")
            novo_preco = input("Novo preço: ")
            nova_qtd = input("Nova quantidade em estoque: ")
            novo_id_categoria = input("Novo ID da categoria (ou deixe vazio): ")
            novo_id_fornecedor = input("Novo ID do fornecedor (ou deixe vazio): ")
            novo_id_categoria = int(novo_id_categoria) if novo_id_categoria.strip() else None
            novo_id_fornecedor = int(novo_id_fornecedor) if novo_id_fornecedor.strip() else None

            Produto.editar(id_produto, novo_nome, novo_sku, novo_preco, nova_qtd, novo_id_categoria, novo_id_fornecedor)

        elif opcao == "4":
            id_produto = input("ID do produto que deseja excluir: ")
            Produto.excluir(id_produto)

        elif opcao == "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")


def menu_pedidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========== Pedidos ===========")
        print("=  1. Cadastrar Pedido        =")
        print("=  2. Listar Pedidos          =")
        print("=  3. Editar Pedido           =")
        print("=  4. Excluir Pedido          =")
        print("=  0. Voltar                  =")
        print("================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            id_usuario = input("ID do usuário: ")
            total_pedido = input("Total do pedido: R$ ")
            observacao = input("Observação (opcional): ")

            print("\nEscolha o status do pedido:")
            print("1. Em Andamento")
            print("2. Concluído")
            print("3. Cancelado")

            status_opcao = input("Digite o número correspondente: ")
            status_map = {
                "1": "em_andamento",
                "2": "concluido",
                "3": "cancelado"
            }

            status = status_map.get(status_opcao)
            if not status:
                print("\nStatus inválido!")
                input("Pressione 'Enter' para continuar...")
                continue

            pedido = Pedido(id_usuario, total_pedido, status, observacao)
            pedido.salvar()

        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            Pedido.listar()

        elif opcao == "3":
            id_pedido = input("ID do pedido que deseja editar: ")
            novo_total = input("Novo total do pedido: R$ ")
            nova_observacao = input("Nova observação (opcional): ")

            print("\nEscolha o novo status do pedido:")
            print("1. Em Andamento")
            print("2. Concluído")
            print("3. Cancelado")

            status_opcao = input("Digite o número correspondente: ")
            status_map = {
                "1": "em_andamento",
                "2": "concluido",
                "3": "cancelado"
            }

            novo_status = status_map.get(status_opcao)
            if not novo_status:
                print("\nStatus inválido!")
                input("Pressione 'Enter' para continuar...")
                continue

            Pedido.editar(id_pedido, novo_status, novo_total, nova_observacao)

        elif opcao == "4":
            id_pedido = input("ID do pedido que deseja excluir: ")
            Pedido.excluir(id_pedido)

        elif opcao == "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")

def menu_movimentacoes():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=========== Movimentações de Estoque ===========")
        print("=  1. Registrar Movimentação de Estoque       =")
        print("=  2. Listar Movimentações                    =")
        print("=  0. Voltar                                  =")
        print("===============================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n======= Registrar Movimentação =======")
            id_produto = input("ID do Produto: ")

            print("\nSelecione o tipo de movimentação:")
            print("1. Entrada (adiciona ao estoque)")
            print("2. Saída (retira do estoque)")
            print("3. Ajuste (define novo valor no estoque)")
            tipo_opcao = input("Digite o número correspondente: ")

            tipo_map = {
                "1": "entrada",
                "2": "saida",
                "3": "ajuste"
            }
            tipo_movimentacao = tipo_map.get(tipo_opcao)

            if not tipo_movimentacao:
                print("\nTipo inválido!")
                input("Pressione 'Enter' para continuar...")
                continue

            quantidade = input("Quantidade: ")
            referencia = input("Referência (opcional): ")
            observacao = input("Observação (opcional): ")

            mov = MovimentacaoEstoque(id_produto, tipo_movimentacao, quantidade, referencia, observacao)
            mov.salvar()

        elif opcao == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            MovimentacaoEstoque.listar()

        elif opcao == "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")

def menu_relatorios():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n============ MENU DE RELATÓRIOS ============")
        print("1. Estoque por Categoria")
        print("2. Pedidos por Fornecedor")
        print("3. Produtos sem Estoque")
        print("4. Produtos mais Vendidos")
        print("0. Voltar")
        print("==============================================")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            r_estoque_por_categoria()
        elif opcao == "2":
            r_pedidos_por_fornecedor()
        elif opcao == "3":
            r_produtos_sem_estoque()
        elif opcao == "4":
            r_produtos_mais_vendidos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")