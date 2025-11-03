import os
from models.user import Usuario
from models.categories import Categoria
from models.fornec import Fornecedor
from models.products import Produto

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
    print("teste")

def menu_estoque():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")