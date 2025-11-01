import os
from models.user import Usuario
from models.categories import Categoria
from models.fornec import Fornecedor

def menu_usuarios():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Usuários ---")
        print("1. Cadastrar usuário")
        print("2. Listar usuários")
        print("3. Editar usuário")
        print("4. Excluir usuário")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")                             #Os usuários não "reaproveitam" os ID's antigos pois isso pode conflitar o projeto...
            telefone = input("Telefone: ")
            user = Usuario(nome, email, telefone)
            user.salvar()
        elif opcao == "2":
            Usuario.listar()
            input("\nPressione Enter para continuar...")
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

def menu_categorias():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Categoria ---")
        print("1. Cadastrar Categorias de Produtos")
        print("2. Listar Categorias")
        print("3. Editar Categoria")
        print("4. Excluir Categoria")
        print("5. Editar Descrição de Categoria")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descricao: ")
            categori = Categoria(nome, descricao)
            categori.salvar()
            
        elif opcao == "2":
            Categoria.listar()
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            id_categoria = input("ID da categoria a ser editada: ")
            novo_nome = input("Novo nome da categoria: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar(id_categoria, novo_nome, nova_descricao)

        elif opcao == "4":
            id_categoria = input("ID da categoria a ser excluída:")
            Categoria.excluir(id_categoria)

        elif opcao == "5":
            id_categoria = input("ID da categoria a ser editada: ")
            nova_descricao = input("Nova descrição da categoria: ")
            Categoria.editar_descricao(id_categoria, nova_descricao)
            
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")


def menu_fornecedores():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n--- Fornecedores ---")
        print("1. Cadastrar fornecedor")
        print("2. Listar fornecedores")
        print("3. Editar no fornecedor")
        print("4. Excluir fornecedor")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            contato = input("Contato: ")
            fornecedor = Fornecedor(nome, contato)
            fornecedor.salvar()

        elif opcao == "2":
            Fornecedor.listar()
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            id_fornecedor = input("ID do fornecedor que deseja editar: ")
            novo_nome = input("Novo nome: ")
            novo_contato = input("Novo contato: ")
            Fornecedor.editar(id_fornecedor, novo_nome, novo_contato)

        elif opcao == "4":
            id_fornecedor = input("ID do fornecedor que deseja excluir: ")
            Fornecedor.excluir(id_fornecedor)

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def menu_produtos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

def menu_pedidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")

def menu_estoque():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("teste")